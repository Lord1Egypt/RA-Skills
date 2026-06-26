#!/usr/bin/env bash
set -euo pipefail

# NeverDie Setup — Manual bootstrap for when the agent isn't available
# Usage:
#   bash setup.sh --telegram-token BOT_TOKEN --chat-id CHAT_ID
#   bash setup.sh                                                   # File-only alerts (no Telegram)
#   bash setup.sh --uninstall                                       # Remove cron job and config

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="${HOME}/.openclaw/workspace"
CRON_FILE="${HOME}/.openclaw/cron/jobs.json"
CONFIG_FILE="${WORKSPACE}/.neverdie-config.json"
MONITOR_SRC="${SCRIPT_DIR}/fallback-monitor.js"
MONITOR_DST="${WORKSPACE}/fallback-monitor.js"

TELEGRAM_TOKEN=""
CHAT_ID=""
HOSTNAME_TAG=""
TIMEZONE="UTC"
UNINSTALL=false

# --- Parse args ---
while [[ $# -gt 0 ]]; do
  case $1 in
    --telegram-token) TELEGRAM_TOKEN="$2"; shift 2 ;;
    --chat-id)        CHAT_ID="$2"; shift 2 ;;
    --hostname)       HOSTNAME_TAG="$2"; shift 2 ;;
    --timezone)       TIMEZONE="$2"; shift 2 ;;
    --uninstall)      UNINSTALL=true; shift ;;
    -h|--help)
      cat <<'HELPEOF'
NeverDie Setup — LLM resilience for OpenClaw

Usage:
  bash setup.sh --telegram-token TOKEN --chat-id ID   # Full setup with Telegram alerts
  bash setup.sh                                        # File-only alerts (no Telegram)
  bash setup.sh --uninstall                            # Remove NeverDie

Options:
  --telegram-token TOKEN   Telegram bot token (from @BotFather)
  --chat-id ID             Telegram chat ID to send alerts to
  --hostname NAME          Identifier for this instance (default: system hostname)
  --timezone TZ            IANA timezone for alert timestamps (default: UTC)
  --uninstall              Remove cron job, config, and deployed monitor
  -h, --help               Show this help
HELPEOF
      exit 0
      ;;
    *) echo "Unknown option: $1 (use --help for usage)"; exit 1 ;;
  esac
done

# Default hostname to system hostname
if [[ -z "$HOSTNAME_TAG" ]]; then
  HOSTNAME_TAG="$(hostname -s 2>/dev/null || echo 'openclaw')"
fi

# --- Uninstall ---
if [[ "$UNINSTALL" == true ]]; then
  echo "=== NeverDie Uninstall ==="

  if [[ -f "$CRON_FILE" ]]; then
    echo -n "Removing cron job... "
    node -e "
      const data = JSON.parse(require('fs').readFileSync(process.env.CRON_FILE, 'utf8'));
      const before = data.jobs.length;
      data.jobs = data.jobs.filter(j => !j.name.includes('NeverDie') && !j.name.includes('Fallback Monitor'));
      const removed = before - data.jobs.length;
      require('fs').writeFileSync(process.env.CRON_FILE, JSON.stringify(data, null, 2));
      console.log(removed > 0 ? 'OK (removed ' + removed + ')' : 'none found');
    " 2>&1
  fi

  for f in "$CONFIG_FILE" "$MONITOR_DST" "$WORKSPACE/.fallback-monitor-state.json" "$WORKSPACE/.fallback-alert-latest.json"; do
    if [[ -f "$f" ]]; then
      rm "$f"
      echo "Removed: $f"
    fi
  done

  echo "Done. Skill files in skills/neverdie/ are untouched (remove manually or via clawhub uninstall)."
  exit 0
fi

# --- Install ---
echo "=== NeverDie Setup ==="
echo ""

# 1. Check prerequisites
echo -n "Checking Node.js... "
if command -v node &>/dev/null; then
  echo "OK ($(node --version))"
else
  echo "MISSING — Node.js is required"
  exit 1
fi

echo -n "Checking Ollama... "
if curl -s --max-time 3 http://localhost:11434/api/tags > /dev/null 2>&1; then
  MODELS=$(curl -s http://localhost:11434/api/tags | node -e "
    let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{
      try{console.log(JSON.parse(d).models.map(m=>m.name).join(', '))}
      catch(e){console.log('(parse error)')}
    })
  ")
  echo "OK (models: ${MODELS})"
else
  echo "WARNING — not reachable at localhost:11434"
  echo "  Recommended: install from https://ollama.com then: ollama pull llama3.2:3b"
fi

# 2. Deploy monitor script
echo ""
echo -n "Deploying monitor... "
cp "$MONITOR_SRC" "$MONITOR_DST"
chmod +x "$MONITOR_DST"
echo "OK"

# 3. Write config
echo -n "Writing config... "
_ND_TOKEN="$TELEGRAM_TOKEN" _ND_CHATID="$CHAT_ID" _ND_TZ="$TIMEZONE" \
  _ND_HOST="$HOSTNAME_TAG" _ND_CFGFILE="$CONFIG_FILE" \
  node -e "
  const config = {
    telegramBotToken: process.env._ND_TOKEN || '',
    telegramChatId: process.env._ND_CHATID || '',
    cooldownMinutes: 15,
    timezone: process.env._ND_TZ || 'UTC',
    hostname: process.env._ND_HOST || 'openclaw'
  };
  require('fs').writeFileSync(
    process.env._ND_CFGFILE,
    JSON.stringify(config, null, 2) + '\n'
  );
" 2>&1
echo "OK (${CONFIG_FILE})"

# 4. Register cron job
echo -n "Registering cron job... "
if [[ -f "$CRON_FILE" ]]; then
  EXISTING=$(CRON_FILE="$CRON_FILE" node -e "
    const jobs = JSON.parse(require('fs').readFileSync(process.env.CRON_FILE, 'utf8')).jobs;
    const found = jobs.find(j => j.name.includes('NeverDie') || j.name.includes('Fallback Monitor'));
    console.log(found ? 'yes' : 'no');
  ")
  if [[ "$EXISTING" == "yes" ]]; then
    echo "SKIPPED (existing job found)"
  else
    CRON_FILE="$CRON_FILE" MONITOR_DST="$MONITOR_DST" node -e "
      const data = JSON.parse(require('fs').readFileSync(process.env.CRON_FILE, 'utf8'));
      const now = Date.now();
      data.jobs.push({
        id: require('crypto').randomUUID(),
        agentId: 'main',
        name: 'NeverDie Fallback Monitor',
        enabled: true,
        createdAtMs: now,
        updatedAtMs: now,
        schedule: { kind: 'every', everyMs: 300000, anchorMs: now },
        sessionTarget: 'isolated',
        wakeMode: 'now',
        payload: { kind: 'systemEvent', text: 'exec:node ' + process.env.MONITOR_DST },
        delivery: { mode: 'announce', channel: 'session', bestEffort: true },
        state: {}
      });
      require('fs').writeFileSync(process.env.CRON_FILE, JSON.stringify(data, null, 2));
      console.log('OK');
    " 2>&1
  fi
else
  echo "WARNING — ${CRON_FILE} not found"
fi

# 5. Test Telegram (if configured)
if [[ -n "$TELEGRAM_TOKEN" && -n "$CHAT_ID" ]]; then
  echo ""
  echo -n "Testing Telegram... "
  _ND_TOKEN="$TELEGRAM_TOKEN" _ND_CHATID="$CHAT_ID" _ND_HOST="$HOSTNAME_TAG" node -e "
    const https = require('https');
    const data = JSON.stringify({
      chat_id: process.env._ND_CHATID,
      text: '\u{1F6E1}\u{FE0F} <b>NeverDie Setup Complete</b>\n\nMonitor deployed on <b>' + process.env._ND_HOST + '</b>.\nAlerts will be sent here when model failures are detected.',
      parse_mode: 'HTML'
    });
    const req = https.request({
      hostname: 'api.telegram.org', port: 443,
      path: '/bot' + process.env._ND_TOKEN + '/sendMessage',
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) },
      timeout: 10000
    }, res => {
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => {
        if (res.statusCode === 200) { console.log('OK'); }
        else { console.log('FAIL (HTTP ' + res.statusCode + ')'); process.exit(1); }
      });
    });
    req.on('error', e => { console.log('FAIL (' + e.message + ')'); process.exit(1); });
    req.write(data);
    req.end();
  " 2>&1
else
  echo ""
  echo "Telegram: not configured (file-only alerts)"
  echo "  To add later: edit ${CONFIG_FILE} or re-run with --telegram-token and --chat-id"
fi

# 6. Test monitor
echo -n "Running monitor test... "
node "$MONITOR_DST" 2>&1 && echo "OK (exit 0)" || echo "WARNING (exit $?)"

# Summary
echo ""
echo "=== NeverDie is active ==="
echo "Monitor:  runs every 5 min via systemEvent cron"
echo "Config:   ${CONFIG_FILE}"
if [[ -n "$TELEGRAM_TOKEN" ]]; then
  echo "Telegram: chat ${CHAT_ID}"
else
  echo "Telegram: not configured"
fi
echo ""
echo "Verify anytime:  node ${MONITOR_DST} --status"
echo "Send test alert: node ${MONITOR_DST} --test"
