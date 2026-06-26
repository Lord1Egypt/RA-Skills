#!/usr/bin/env node
/**
 * openclaw-healthcheck — check-all.js
 * PROMPT GENERATOR ONLY — no outbound network requests.
 * Outputs a full diagnostic prompt covering all channels + cron tasks.
 *
 * Usage:
 *   node scripts/check-all.js
 *   node scripts/check-all.js --lang en
 *   node scripts/check-all.js --fix     # auto-apply repairs after diagnosis
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 ? args[langIdx + 1] : 'zh';
const autoFix = args.includes('--fix');

const configDir = '~/.openclaw';

if (lang === 'en') {
  console.log(`=== openclaw-healthcheck — Full Diagnostic ===
Config dir: ${configDir}
Mode: ${autoFix ? 'Diagnose + Auto-Fix' : 'Diagnose only (add --fix to repair)'}

You are an AI agent running openclaw's self-diagnostic. Check every channel and
every cron task in sequence, then output a consolidated health report.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1 — FEISHU (lark-cli)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  lark-cli --version 2>/dev/null || echo "NOT_INSTALLED"
  lark-cli auth status 2>/dev/null || echo "NOT_AUTHENTICATED"

Decision:
  → NOT_INSTALLED          → feishu: NOT_CONFIGURED
  → NOT_AUTHENTICATED      → feishu: EXPIRED — run: node scripts/fix-feishu.js
  → Shows user + app ID    → feishu: OK
  → Token expired error    → feishu: EXPIRED — run: node scripts/fix-feishu.js ${autoFix ? '(running now)' : ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2 — TELEGRAM (bot API)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # Check token is set
  test -n "$TELEGRAM_BOT_TOKEN" && echo "TOKEN_SET" || echo "TOKEN_MISSING"

  # Test bot API reachability
  curl -s --max-time 10 "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe" | \\
    python3 -c "import sys,json; d=json.load(sys.stdin); print('OK:', d['result']['username'])" \\
    2>/dev/null || echo "API_UNREACHABLE"

  # Check for recent updates (silence = possible webhook issue)
  curl -s --max-time 10 "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates?limit=1" | \\
    python3 -c "import sys,json; d=json.load(sys.stdin); print('UPDATES:', len(d['result']))" \\
    2>/dev/null

Decision:
  → TOKEN_MISSING          → telegram: NOT_CONFIGURED
  → API_UNREACHABLE        → telegram: TOKEN_INVALID — run: node scripts/check-telegram.js --reauth
  → OK: <username>         → telegram: OK
  → OK but UPDATES: 0 and bot was previously active → telegram: SILENT (possible webhook drop)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3 — WECHAT (bridge process)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # Check for running wechat bridge process
  pgrep -f "wechat\\|wx-bridge\\|wechaty" 2>/dev/null && echo "BRIDGE_RUNNING" || echo "BRIDGE_DOWN"

  # Check openclaw wechat config
  test -f ~/.openclaw/wechat/session.json && echo "SESSION_FILE_EXISTS" || echo "NO_SESSION"

Decision:
  → BRIDGE_DOWN + NO_SESSION  → wechat: NOT_CONFIGURED
  → BRIDGE_DOWN + SESSION     → wechat: BRIDGE_DOWN — restart bridge: node scripts/check-wechat.js
  → BRIDGE_RUNNING            → wechat: OK (verify with test message if needed)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4 — CRON TASKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # List all openclaw cron entries (try openclaw native first, fallback to system cron)
  openclaw cron list 2>/dev/null || crontab -l 2>/dev/null | grep -i openclaw || echo "NO_CRON_FOUND"

  # Check for duplicates (same schedule + same command appearing more than once)
  crontab -l 2>/dev/null | sort | uniq -d | head -20

  # Check recent execution logs
  ls -lt ~/.openclaw/logs/*.log 2>/dev/null | head -10
  tail -20 ~/.openclaw/logs/cron.log 2>/dev/null || echo "NO_CRON_LOG"

For each cron entry found, determine:
  → Last run timestamp vs expected schedule — is it OVERDUE?
  → Same schedule + same script appearing 2+ times → DUPLICATE
  → Exit code in log is non-zero → FAILED
  → No log entry in the last full interval → MISSED

${autoFix ? `AUTO-FIX: run node scripts/fix-crons.js --dedup for any DUPLICATE entries found.` : ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT — Write health report to data/health-report.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{
  "checkedAt": "<ISO timestamp>",
  "channels": {
    "feishu":   { "status": "OK | EXPIRED | DISCONNECTED | NOT_CONFIGURED", "detail": "..." },
    "telegram": { "status": "OK | SILENT | TOKEN_INVALID | NOT_CONFIGURED", "detail": "..." },
    "wechat":   { "status": "OK | BRIDGE_DOWN | NOT_CONFIGURED", "detail": "..." }
  },
  "crons": [
    { "id": "<name>", "schedule": "<cron expr>", "lastRun": "<ISO>",
      "status": "OK | MISSED | DUPLICATE | FAILED", "duplicateCount": 0 }
  ],
  "overallStatus": "HEALTHY | DEGRADED | CRITICAL",
  "actionsNeeded": ["<fix-feishu | fix-crons --dedup | check-telegram --reauth | ...>"]
}

After writing:
  → HEALTHY:  "All channels and cron tasks are healthy. No action needed."
  → DEGRADED: List each degraded item and its recommended fix command.
  → CRITICAL: At least one channel is completely down. Run the fix commands immediately.
`);
} else {
  console.log(`=== openclaw-healthcheck — 全量自检 ===
配置目录：${configDir}
模式：${autoFix ? '诊断 + 自动修复' : '仅诊断（加 --fix 参数可自动修复）'}

你是一个 AI Agent，正在执行 openclaw 的通讯自检。
按顺序检查每个通道和每个定时任务，最后输出综合健康报告。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第 1 步 — 飞书（lark-cli）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  lark-cli --version 2>/dev/null || echo "NOT_INSTALLED"
  lark-cli auth status 2>/dev/null || echo "NOT_AUTHENTICATED"

决策：
  → NOT_INSTALLED           → feishu: NOT_CONFIGURED
  → NOT_AUTHENTICATED       → feishu: EXPIRED — 运行：node scripts/fix-feishu.js
  → 显示用户名 + App ID     → feishu: OK
  → token expired 错误      → feishu: EXPIRED — 运行：node scripts/fix-feishu.js ${autoFix ? '（正在执行）' : ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第 2 步 — Telegram（Bot API）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # 检查 token 是否已设置
  test -n "$TELEGRAM_BOT_TOKEN" && echo "TOKEN_SET" || echo "TOKEN_MISSING"

  # 测试 Bot API 可达性
  curl -s --max-time 10 "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe" | \\
    python3 -c "import sys,json; d=json.load(sys.stdin); print('OK:', d['result']['username'])" \\
    2>/dev/null || echo "API_UNREACHABLE"

  # 检查最近更新（静默可能是 webhook 断开）
  curl -s --max-time 10 "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates?limit=1" | \\
    python3 -c "import sys,json; d=json.load(sys.stdin); print('UPDATES:', len(d['result']))" \\
    2>/dev/null

决策：
  → TOKEN_MISSING             → telegram: NOT_CONFIGURED
  → API_UNREACHABLE           → telegram: TOKEN_INVALID — 运行：node scripts/check-telegram.js --reauth
  → OK: <用户名>              → telegram: OK
  → OK 但 UPDATES: 0 且之前活跃 → telegram: SILENT（可能 webhook 掉了）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第 3 步 — 微信（bridge 进程）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # 检查微信 bridge 进程是否在跑
  pgrep -f "wechat\\|wx-bridge\\|wechaty" 2>/dev/null && echo "BRIDGE_RUNNING" || echo "BRIDGE_DOWN"

  # 检查 openclaw 微信配置
  test -f ~/.openclaw/wechat/session.json && echo "SESSION_FILE_EXISTS" || echo "NO_SESSION"

决策：
  → BRIDGE_DOWN + NO_SESSION  → wechat: NOT_CONFIGURED
  → BRIDGE_DOWN + SESSION     → wechat: BRIDGE_DOWN — 运行：node scripts/check-wechat.js
  → BRIDGE_RUNNING            → wechat: OK（如需要可发测试消息验证）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
第 4 步 — 定时任务（Cron）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  # 列出所有 openclaw 定时任务（先试 openclaw 原生命令，失败则查系统 cron）
  openclaw cron list 2>/dev/null || crontab -l 2>/dev/null | grep -i openclaw || echo "NO_CRON_FOUND"

  # 检查重复条目（相同调度 + 相同命令出现超过一次）
  crontab -l 2>/dev/null | sort | uniq -d | head -20

  # 检查最近执行日志
  ls -lt ~/.openclaw/logs/*.log 2>/dev/null | head -10
  tail -20 ~/.openclaw/logs/cron.log 2>/dev/null || echo "NO_CRON_LOG"

对每个 cron 条目判断：
  → 上次执行时间 vs 预期周期 — 是否超时未跑 (MISSED)?
  → 相同调度 + 相同脚本出现 2 次以上 → DUPLICATE
  → 日志中退出码非零 → FAILED
  → 最近一个完整周期内无日志 → MISSED

${autoFix ? '自动修复：对发现的 DUPLICATE 条目，运行 node scripts/fix-crons.js --dedup' : ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
输出 — 写入 data/health-report.json
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{
  "checkedAt": "<ISO 时间戳>",
  "channels": {
    "feishu":   { "status": "OK | EXPIRED | DISCONNECTED | NOT_CONFIGURED", "detail": "..." },
    "telegram": { "status": "OK | SILENT | TOKEN_INVALID | NOT_CONFIGURED", "detail": "..." },
    "wechat":   { "status": "OK | BRIDGE_DOWN | NOT_CONFIGURED", "detail": "..." }
  },
  "crons": [
    { "id": "<名称>", "schedule": "<cron 表达式>", "lastRun": "<ISO>",
      "status": "OK | MISSED | DUPLICATE | FAILED", "duplicateCount": 0 }
  ],
  "overallStatus": "HEALTHY | DEGRADED | CRITICAL",
  "actionsNeeded": ["<fix-feishu | fix-crons --dedup | check-telegram --reauth | ...>"]
}

写入后：
  → HEALTHY：  "所有通道和定时任务均正常，无需操作。"
  → DEGRADED： 列出每个降级项及推荐的修复命令。
  → CRITICAL： 至少一个通道完全断开，立即执行修复命令。
`);
}
