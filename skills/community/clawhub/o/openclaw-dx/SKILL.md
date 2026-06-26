---
name: openclaw-dx
version: 1.9.0
license: MIT
description: Diagnose and fix openclaw gateway issues. Use when the gateway is stuck, not starting, crash-looping, or rejecting connections. Covers main and --profile vesper gateways. Runs triage, applies fixes, writes incident report to ~/clawd/inbox.
---

# OpenClaw Gateway DX

Diagnose, fix, and document openclaw gateway issues. Covers both main (port 18789) and vesper profile (port 18999) gateways.

## When to Use

- Gateway not starting or crash-looping
- TUI/CLI can't connect (pairing required, password mismatch, device token mismatch)
- Gateway unresponsive or high memory
- After openclaw version upgrades
- User says "openclaw is stuck" or similar

## Triage Protocol

Run these in parallel to assess state:

```bash
# 1. What's listening?
lsof -i :18789 -i :18999 2>/dev/null | grep LISTEN

# 2. Process health (memory, CPU, uptime)
ps -o pid,rss,pcpu,lstart,etime -p $(lsof -i :18789 -t 2>/dev/null | head -1)

# 3. Recent errors
tail -30 ~/.openclaw/logs/gateway.err.log

# 4. Recent activity
tail -20 ~/.openclaw/logs/gateway.log

# 5. Channel status
openclaw channels status

# 6. Version
openclaw --version

# 7. Pending device pairings
openclaw devices list --json | head -20

# 8. Model config + fallback chain (use affected profile's config dir)
# Main: ~/.openclaw/openclaw.json | Vesper: ~/.openclaw-vesper/openclaw.json
cat ~/.openclaw/openclaw.json | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin)['agents']['defaults']['model'], indent=2))"

# 9. Per-agent auth token status + expiry check
# Main: ~/.openclaw/agents/main/agent/auth-profiles.json
# Vesper: ~/.openclaw-vesper/agents/main/agent/auth-profiles.json
python3 -c "
import sys,json,time
data=json.load(open('$HOME/.openclaw/agents/main/agent/auth-profiles.json'))
now=time.time()*1000
for k,v in data.get('profiles',{}).items():
    exp=v.get('expires',0)
    expired='EXPIRED' if exp and exp<now else 'valid'
    has_token='yes' if v.get('access') or v.get('token') else 'NO'
    print(f'{k}: type={v.get(\"type\",\"?\")} token={has_token} expires={expired}')
"

# 10. Memory search / QMD (use --profile if vesper)
openclaw memory status

# 11. Check OPENCLAW_GATEWAY_TOKEN env var (multi-profile foot-gun)
echo "OPENCLAW_GATEWAY_TOKEN=${OPENCLAW_GATEWAY_TOKEN:-unset}"

# 12. Session token counts (context overflow check)
for dir in ~/.openclaw ~/.openclaw-vesper; do
  f="$dir/agents/main/sessions/sessions.json"
  [ -f "$f" ] && echo "=== $(basename $dir) ===" && python3 -c "
import json
data=json.load(open('$f'))
for k,v in data.items():
    t=v.get('contextTokens',0)
    pct=t/200000*100
    flag=' ⚠️ BLOATED' if pct>75 else ''
    print(f'  {k}: {t:,} tokens ({pct:.0f}%){flag}')
"
done

# 12. Verify plist profile alignment
grep OPENCLAW_STATE_DIR ~/Library/LaunchAgents/ai.openclaw.gateway.plist
grep OPENCLAW_STATE_DIR ~/Library/LaunchAgents/ai.openclaw.vesper.plist
```

## Common Failure Modes

### 0. Failover Cascade (All Providers Down)
**Symptom:** `All models failed (N):` followed by per-provider errors. May also appear as "The model has crashed without additional information. (Exit code: null)"
**Diagnosis:** Check the full error chain — each attempt cycles primary → fallback1 → fallback2. All must fail for the user to see an error. Common error signatures per provider:
- Anthropic: `The AI service is temporarily overloaded` (transient, or stale token)
- OpenAI Codex: `OAuth token refresh failed for openai-codex` or `refresh_token_reused` (expired access token + consumed refresh token)
- Google/Gemini: `No API key found for provider "google"` (provider never configured in auth-profiles.json)
- LM Studio: Python errors like `AttributeError: 'list' object has no attribute 'swapaxes'` (model inference bug)
**Fix:** Identify which providers are broken and fix each:
```bash
# Check fallback config (use affected profile's config dir)
cat ~/.openclaw/openclaw.json | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin)['agents']['defaults']['model'], indent=2))"
# Check per-agent auth tokens + expiry
python3 -c "
import sys,json,time
data=json.load(open('$HOME/.openclaw/agents/main/agent/auth-profiles.json'))
now=time.time()*1000
for k,v in data.get('profiles',{}).items():
    exp=v.get('expires',0)
    expired='EXPIRED' if exp and exp<now else 'valid'
    has_token='yes' if v.get('access') or v.get('token') else 'NO'
    print(f'{k}: type={v.get(\"type\",\"?\")} token={has_token} expires={expired}')
"
```
**For OAuth expiry (OpenAI Codex):** `openclaw configure` (interactive re-auth). Add `--profile vesper` if vesper.
**For missing provider keys (Google etc.):** `openclaw agents add <provider>` or remove unconfigured providers from fallback chain.
**Prevention:** Ensure all providers in the fallback chain are actually configured. Use same-provider fallbacks (e.g. different Anthropic models) instead of cross-provider for predictable failure modes.

### 1. Expired Channel Token (Slack xoxe.xoxb-)
**Symptom:** Crash loop with `Unhandled promise rejection: Error: An API error occurred: token_expired`
**Fix:**
```bash
# Disable the channel
# Edit ~/.openclaw/openclaw.json: channels.slack.enabled → false AND plugins.entries.slack.enabled → false
openclaw gateway start
# Then rotate token at api.slack.com and re-enable
```

### 2. Config Wiped by Upgrade
**Symptom:** `Gateway start blocked: set gateway.mode=local (current: unset)`
**Fix:** Restore from backup:
```bash
ls -la ~/.openclaw/openclaw.json.bak*
# Find the largest/most recent backup with full config
cp ~/.openclaw/openclaw.json.bak-XXXX ~/.openclaw/openclaw.json
openclaw doctor --fix
openclaw gateway start
```

### 3. Stale Lock File
**Symptom:** Gateway won't start, references old PID
**Fix:**
```bash
ls ~/.openclaw/gateway.*.lock
cat ~/.openclaw/gateway.*.lock  # check PID
kill -0 <pid>  # verify dead
rm ~/.openclaw/gateway.*.lock
openclaw gateway start
```

### 4. Device Token Mismatch / Pairing Required
**Symptom:** `unauthorized: device token mismatch` or `pairing required`
**Fix:**
```bash
openclaw devices list --json  # check for pending requests
openclaw devices approve "<requestId>" --password "$OPENCLAW_GATEWAY_PASSWORD"
# Or rotate existing device:
openclaw devices rotate --device <id> --role operator --password "$OPENCLAW_GATEWAY_PASSWORD"
```

### 5. Password Mismatch (multi-profile)
**Symptom:** `unauthorized: gateway password mismatch`
**Fix:** Sync passwords across profiles. All profiles should use `$OPENCLAW_GATEWAY_PASSWORD` to match the env var in shell rc (`~/.bashrc` or `~/.zshrc`).

### 6. Memory Bloat / Unresponsive
**Symptom:** Gateway listening but not responding, RSS exceeds Critical threshold (see Memory Thresholds)
**Fix:**
```bash
openclaw gateway stop
sleep 2
kill -9 <pid>  # if still lingering
launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

### 7. Invalid Plugin Entry
**Symptom:** `Config invalid: plugins.entries.X: plugin not found`
**Fix:** Remove the stale plugin entry from `~/.openclaw/openclaw.json`, then `openclaw gateway start`.

### 8. Port Conflict / Orphan Processes
**Symptom:** `Port 18789 is already in use` or multiple gateway PIDs
**Fix:**
```bash
ps aux | grep openclaw-gateway | grep -v grep
kill <orphan-pids>
openclaw gateway start
```

### 9. Custom Plugin Missing configSchema
**Symptom:** Crash loop with `plugins: plugin: plugin manifest requires configSchema`
**Diagnosis:** A plugin in `~/.openclaw/extensions/` (auto-discovered) or `plugins.load.paths` has an `openclaw.plugin.json` without the required `configSchema` field. Run `openclaw doctor --fix` — the "Plugin diagnostics" section names the offending manifest.
**Fix:** Add empty configSchema to the plugin manifest:
```json
"configSchema": {
  "type": "object",
  "additionalProperties": false,
  "properties": {}
}
```
Then restart: `launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist`
**Prevention:** All plugin manifests require `configSchema` in 2026.3.2+, even if empty. Run `openclaw doctor` after creating custom plugins before restarting.

### 10. Invalid JSON in Config (Hand-Edit Damage)
**Symptom:** CLI commands fail with `json.decoder.JSONDecodeError` or `Unexpected token`. Gateway may still run (it was started before the edit) but CLI/TUI can't parse the config to connect.
**Diagnosis:** Someone hand-edited `openclaw.json` and introduced unquoted keys, trailing commas, or other invalid JSON.
**Fix:** Validate and fix the JSON:
```bash
python3 -c "import json; json.load(open('$HOME/.openclaw/openclaw.json'))"
# Fix the reported line — common issues: unquoted keys, trailing commas
```
**Prevention:** Use `openclaw configure` or a JSON-aware editor. After manual edits, validate with the python one-liner above.

### 11. Missing gateway.remote.token (Token Auth Mode)
**Symptom:** CLI/TUI fails with `gateway token missing (set gateway.remote.token to match gateway.auth.token)`
**Diagnosis:** The gateway uses `gateway.auth.mode: "token"` but `gateway.remote.token` is not set. The CLI reads `remote.token` to authenticate — without it, all connections are rejected.
**Fix:** Add `gateway.remote.token` matching `gateway.auth.token`:
```bash
# In openclaw.json, inside the "gateway" section:
"remote": {
  "token": "<same value as gateway.auth.token>"
}
```
Then restart the gateway.
**Note:** Any profile using `gateway.auth.mode: "token"` needs `gateway.remote.token` set. Profiles using password auth (`$OPENCLAW_GATEWAY_PASSWORD`) are not affected.

### 12. Config Patch Restart Cascade (LaunchAgent Left Unloaded)
**Symptom:** Gateway down, port not listening, `launchctl print` says service not found. Error log shows `config change requires gateway restart` followed by restart failure.
**Diagnosis:** Multiple `config.patch` calls (e.g., from an agent using the gateway tool) changed `gateway.auth.*` or other restart-requiring keys. Each patch triggers a deferred restart. The restart mechanism fails with one of:
- `spawnSync launchctl ETIMEDOUT`
- `Bootstrap failed: 5: Input/output error`

The gateway falls back to in-process restart, becomes unstable, eventually receives SIGTERM, and the LaunchAgent is left unloaded.
**Fix:**
```bash
launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```
**Prevention:**
- **Batch config changes** that touch `gateway.auth.*` into a single `config.patch` call to minimize restart triggers
- This is a recurring upstream bug in openclaw 2026.3.x — the LaunchAgent restart mechanism is unreliable across multiple error modes
- Consider a watchdog or `KeepAlive` with `ThrottleInterval=30` in the plist
- If using the gateway tool's `config.patch` action, combine auth + plugin + compaction changes into one call

### 13. OPENCLAW_GATEWAY_TOKEN Env Var Overriding Multi-Profile Token Auth
**Symptom:** `unauthorized: gateway token mismatch` on `openclaw --profile vesper` (or any non-default profile), even when `gateway.auth.token` and `gateway.remote.token` match in the profile's config. Main profile works fine.
**Diagnosis:** The CLI resolves auth tokens with this precedence:
```
process.env.OPENCLAW_GATEWAY_TOKEN > gateway.remote.token (config)
```
If `OPENCLAW_GATEWAY_TOKEN` is set in shell rc (`~/.zshrc`/`~/.bashrc`) to main's token, the CLI sends main's token to ALL profiles, including vesper — which has its own gateway.auth.token.
**Fix:** Sync all profiles to use the same gateway auth token (matching `$OPENCLAW_GATEWAY_TOKEN`):
```bash
# Check env var
echo $OPENCLAW_GATEWAY_TOKEN
# In each profile's openclaw.json, set gateway.auth.token AND gateway.remote.token to match
```
**Alternative:** Remove `OPENCLAW_GATEWAY_TOKEN` from shell rc and rely solely on config-file tokens. Then each profile can have independent tokens.
**Prevention:** When using `OPENCLAW_GATEWAY_TOKEN` env var with multi-profile setups, all profiles must use the same auth token value. The env var is profile-agnostic.

### 14. LaunchAgent Plist Overwritten to Wrong Profile
**Symptom:** `unauthorized: gateway token mismatch` on main profile. Main gateway appears to be running (port listening) but uses wrong config. Vesper commands may work against main's port.
**Diagnosis:** The `ai.openclaw.gateway.plist` was overwritten (likely by `openclaw --profile vesper gateway install` or agent config patches) to point all env vars to vesper's state dir. Check:
```bash
grep OPENCLAW_STATE_DIR ~/Library/LaunchAgents/ai.openclaw.gateway.plist
# Should show ~/.openclaw, NOT ~/.openclaw-vesper
grep OPENCLAW_PROFILE ~/Library/LaunchAgents/ai.openclaw.gateway.plist
# Should NOT be present (main is the default profile)
```
**Fix:** Edit the plist to restore correct profile paths:
- `OPENCLAW_STATE_DIR` → `~/.openclaw`
- `OPENCLAW_CONFIG_PATH` → `~/.openclaw/openclaw.json`
- Remove `OPENCLAW_PROFILE` key (main doesn't need it)
- `StandardOutPath` → `~/.openclaw/logs/gateway.log`
- `StandardErrorPath` → `~/.openclaw/logs/gateway.err.log`
- `OPENCLAW_GATEWAY_PORT` → `18789`
- `OPENCLAW_LAUNCHD_LABEL` → `ai.openclaw.gateway`

Then restart: `launchctl bootout gui/501/ai.openclaw.gateway && launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist`
**Prevention:** After running `openclaw --profile <name> gateway install`, verify BOTH plists still point to the correct profiles. The install command may overwrite the default profile's plist.

### 15. Session Context Overflow + Compaction Timeout (Messages Swallowed)
**Symptom:** Messages received but never responded to. Bot shows "typing" for ~2 minutes then stops (`typing TTL reached`). Same behavior across ALL providers (Anthropic, Codex, Gemini). Switching providers does not help.
**Diagnosis:** The agent session has grown too large (>90% of context window). Compaction times out, blocking the message processing lane indefinitely.
```bash
# Check session token counts
cat ~/.openclaw/agents/main/sessions/sessions.json | python3 -c "
import sys,json
data=json.load(sys.stdin)
for k,v in data.items():
    tokens=v.get('contextTokens',0)
    pct=tokens/200000*100
    flag=' ⚠️ BLOATED' if pct>75 else ''
    print(f'{k}: {tokens:,} tokens ({pct:.0f}%){flag}')
"
# Check for compaction timeout in logs
grep -i 'timed out during compaction\|embedded run timeout' ~/.openclaw/logs/gateway.err.log | tail -5
# Check for typing TTL (message received but agent stuck)
grep 'typing TTL reached' ~/.openclaw/logs/gateway.log | tail -5
```
Key log signatures:
- `embedded run timeout: runId=... timeoutMs=600000` — compaction timed out at 600s
- `using current snapshot: timed out during compaction` — session remains at bloated size
- `typing TTL reached` — bot received message, started typing, but agent never responded
**Fix:** Reset the bloated session:
```bash
# 1. Find the session transcript
ls -la ~/.openclaw/agents/main/sessions/*.jsonl
# 2. Rename transcript to trigger reset
TIMESTAMP=$(date -u +%Y-%m-%dT%H-%M-%S.000Z)
mv ~/.openclaw/agents/main/sessions/<session-id>.jsonl \
   ~/.openclaw/agents/main/sessions/<session-id>.jsonl.reset.$TIMESTAMP
# 3. Remove session entry from sessions.json
python3 -c "
import json
path='$HOME/.openclaw/agents/main/sessions/sessions.json'
data=json.load(open(path))
# Delete the bloated session entry (e.g., 'agent:main:main')
del data['agent:main:main']
json.dump(data, open(path, 'w'), indent=2)
"
# 4. Restart gateway
launchctl bootout gui/501/ai.openclaw.gateway && launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```
**Prevention:**
- Ensure `contextPruning` is configured on ALL profiles: `{ "mode": "cache-ttl", "ttl": "1h", "keepLastAssistants": 5 }`
- Monitor session token counts — alert when any session exceeds 150K (75%)
- Consider periodic `/reset` for long-running persistent sessions (weekly)
- `typing TTL reached` + provider-agnostic failures = session bloat, not provider issue

### 16. Agent Stuck on Hung API Call (Lane Deadlock Without Errors)
**Symptom:** Messages received but never responded to. No errors in logs. No `lane wait exceeded`. No `typing TTL reached` for the stuck call. Gateway process healthy, event loop alive (cron timers firing). Channel status shows `in: Xm ago` but `out: Ym ago` where Y >> X.
**Diagnosis:** The agent's API call to the LLM provider hung indefinitely — neither returned nor timed out. The lane is blocked but below the `lane wait exceeded` threshold logging interval, OR the lane wait log already fired and the call is still stuck.
```bash
# 1. Check channel in/out gap (indicates processing is stuck)
openclaw --profile <profile> channels status

# 2. Check last session transcript entry — look for unanswered tool results
tail -5 ~/.openclaw-vesper/agents/main/sessions/*.jsonl | python3 -c "
import sys, json
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    try:
        d = json.loads(line)
        msg = d.get('message',{})
        role = msg.get('role','?')
        ts = d.get('timestamp','')
        if role == 'toolResult':
            tool = msg.get('toolName','?')
            print(f'{ts} toolResult({tool}) — agent should respond but may be stuck')
        elif role == 'user':
            print(f'{ts} user message — waiting for agent response')
    except: pass
"

# 3. Verify event loop is alive (cron still firing)
grep 'cron: timer armed' /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | tail -1

# 4. Check compaction model auth (misconfigured = compaction fails silently)
python3 -c "
import json
c=json.load(open('$HOME/.openclaw-vesper/openclaw.json'))
model=c.get('agents',{}).get('defaults',{}).get('compaction',{}).get('model','not set')
print(f'Compaction model: {model}')
provider=model.split('/')[0] if '/' in model else model
# Check if provider has auth
import os
for d in ['.openclaw', '.openclaw-vesper']:
    p=os.path.expanduser(f'~/{d}/agents/main/agent/auth-profiles.json')
    if os.path.exists(p):
        data=json.load(open(p))
        found=[k for k in data.get('profiles',{}) if provider.replace('-cli','') in k]
        print(f'  {d}: auth={\"yes\" if found else \"NO - MISCONFIGURED\"} ({found})')
"
```
**Distinguishing from #15 (Context Overflow):**
- #15: Session tokens >90%, `timed out during compaction`, affects ALL providers
- #16: Session tokens normal/low, no compaction errors, single API call hangs silently
**Fix:** Restart the gateway:
```bash
launchctl bootout gui/501/ai.openclaw.vesper && launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.vesper.plist
```
**Prevention:**
- Ensure compaction model provider has valid auth (common: `google-gemini-cli` set but no gemini auth profile)
- Lower `timeoutSeconds` from 1800 (30m) to 600 (10m) to detect hung calls faster
- Monitor channel in/out gap — if `out` lags `in` by >5 minutes, agent is stuck
- `typing TTL reached` + no subsequent `sendMessage` within 5 minutes = stuck, not slow

### 17. Compaction Model Timeout (Context Degradation Without Errors)
**Symptom:** Messages processed but context degrades over time. Agent "forgets" recent context or gives less coherent responses. No visible errors to the user — gateway keeps running.
**Diagnosis:**
```bash
grep -i "timed out during compaction" ~/.openclaw/logs/gateway.err.log | tail -10
grep "compaction-safeguard" ~/.openclaw/logs/gateway.err.log | tail -10
```
Log signatures:
- `[agent/embedded] using current snapshot: timed out during compaction runId=... sessionId=...`
- `[compaction-safeguard] Compaction safeguard: new content uses X% of context; dropped N older chunk(s) (M messages) to fit history budget.`
**Root cause:** The compaction model (configured in `agents.defaults.compaction.model`) is timing out. For example, `google-gemini-cli/gemini-2.5-flash` has OAuth latency + API rate limits that cause frequent timeouts. The gateway falls back to "safeguard" mode: dropping old message chunks without generating a proper summary. This preserves recent context but loses historical continuity — the agent gradually loses older conversation history.
**Distinguishing from #15 (Context Overflow):**
- #15: Session tokens >90%, compaction times out because of sheer size, messages swallowed entirely
- #17: Session tokens normal, compaction model itself is slow/unreliable, messages processed but context quality degrades silently
**Fix:** Switch compaction model to a faster/more reliable provider:
```bash
# Check current compaction model
cat ~/.openclaw/openclaw.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c.get('agents',{}).get('defaults',{}).get('compaction',{}).get('model','not set (using primary model)'))"

# Switch to Sonnet (proven reliable for compaction)
# Use gateway config.patch or edit openclaw.json directly:
# agents.defaults.compaction.model = "anthropic/claude-sonnet-4-6"
```
**Good compaction model choices:**
- `anthropic/claude-sonnet-4-6` — reliable, fast, good summarization
- `anthropic/claude-sonnet-4-20250514` — same tier
- `google-gemini-cli/gemini-2.5-flash` — cheapest but prone to timeout (OAuth + rate limits)
- Local models via LM Studio — $0 but needs testing for summary quality
**Prevention:** Avoid cross-provider compaction models that add auth overhead. Same-provider as primary model reduces failure modes. Monitor for `timed out during compaction` in err.log periodically.

### 18. Self-Reinforcing Config.Patch Crash Loop (Post-Update / Post-Restart)
**Symptom:** Gateway starts, runs for ~2 minutes, receives SIGTERM, LaunchAgent left unloaded. Repeats on every manual bootstrap. No config.patch visible in gateway logs (it happens too fast or logs rotate). Update to latest version does not fix it.
**Diagnosis:** The agent's session preserves context about a pending config change (e.g., "fix auth order array"). On each restart, the agent resumes that intent and immediately issues a config.patch on `auth.*` keys, triggering a restart cascade. The gateway dies, gets re-bootstrapped, and the cycle repeats because the session still has the patching intent.
```bash
# 1. Check if sessions are bloated (session context preserves patching intent)
python3 -c "
import json
data=json.load(open('$HOME/.openclaw/agents/main/sessions/sessions.json'))
bloated=[k for k,v in data.items() if v.get('contextTokens',0)>=150000]
print(f'Total: {len(data)}, Bloated: {len(bloated)}')
for k in bloated[:5]: print(f'  {k}')
"
# 2. Check if plist was regenerated after update
ls -la ~/Library/LaunchAgents/ai.openclaw.gateway.plist
openclaw --version
# If plist mtime is before the update, it's stale
```
**Distinguishing from #12 (Config Patch Restart Cascade):**
- #12: One-time config.patch crash, manual bootstrap fixes it
- #18: Bootstrap→crash→bootstrap loop because session context re-triggers config.patch on every restart
**Fix:**
```bash
# 1. Regenerate plist for current version
openclaw gateway install
# 2. Prune bloated sessions (breaks the loop by clearing patching intent)
python3 -c "
import json
path='$HOME/.openclaw/agents/main/sessions/sessions.json'
data=json.load(open(path))
healthy={k:v for k,v in data.items() if v.get('contextTokens',0)<150000}
print(f'Pruning {len(data)-len(healthy)} bloated, keeping {len(healthy)} healthy')
json.dump(healthy, open(path, 'w'), indent=2)
"
# 3. Bootstrap
launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```
**Prevention:**
- Always run `openclaw gateway install` after `openclaw update` to regenerate the plist
- Restrict agent's ability to config.patch `auth.*` keys without human confirmation
- Session reset breaks the loop — if the gateway crashes >2 times in a row, prune sessions before next bootstrap

### 19. Auto-Update Kills All Gateways Simultaneously
**Symptom:** Both main AND vesper gateways go down at the same time. No reboot. No config changes. LaunchAgents left unloaded for both.
**Diagnosis:** OpenClaw auto-updated to a new version. The package was replaced hours earlier but the deferred restart fired later, sending SIGTERM to all running gateway processes within seconds of each other. The `kickstart -k` fix from v2026.3.12 does NOT prevent this — auto-update restarts still leave LaunchAgents unloaded.
```bash
# 1. Confirm simultaneous SIGTERM
grep 'signal SIGTERM received' ~/.openclaw/logs/gateway.log | tail -1
grep 'signal SIGTERM received' ~/.openclaw-vesper/logs/gateway.log | tail -1
# If timestamps are within ~10 seconds → auto-update

# 2. Check version changed
openclaw --version
ls -la /opt/homebrew/lib/node_modules/openclaw/package.json  # mtime = update time
```
**Distinguishing from other failures:**
- #12/#18: Single gateway, triggered by config.patch
- #19: ALL gateways die within seconds, no config.patch in logs, version changed
**Fix:**
```bash
# 1. Prune bloated sessions for all profiles
for dir in ~/.openclaw ~/.openclaw-vesper; do
  f="$dir/agents/main/sessions/sessions.json"
  [ -f "$f" ] && python3 -c "
import json
path='$f'
data=json.load(open(path))
healthy={k:v for k,v in data.items() if v.get('contextTokens',0)<150000}
pruned=len(data)-len(healthy)
if pruned:
    json.dump(healthy, open(path, 'w'), indent=2)
    print(f'$(basename $dir): pruned {pruned}')
"
done
# 2. Regenerate plists for new version
openclaw gateway install --force
openclaw --profile vesper gateway install --force
# 3. Verify plist alignment (failure mode #14)
grep OPENCLAW_STATE_DIR ~/Library/LaunchAgents/ai.openclaw.gateway.plist
grep OPENCLAW_STATE_DIR ~/Library/LaunchAgents/ai.openclaw.vesper.plist
# 4. Restart both
launchctl bootout gui/501/ai.openclaw.gateway 2>/dev/null; launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
launchctl bootout gui/501/ai.openclaw.vesper 2>/dev/null; launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.vesper.plist
```
**Prevention:**
- Disable auto-update if stability is critical: check `update.autoInstall` in `openclaw.json`
- If auto-update is desired, add a post-update hook that runs `openclaw gateway install --force` for all profiles
- Always follow the Post-Upgrade Checklist after any version change (manual or auto)

## Memory Thresholds

| RSS | Status | Action |
|-----|--------|--------|
| < 500MB | Healthy | None |
| 500MB-1.5GB | Elevated | Monitor |
| 1.5GB-2.5GB | High | Schedule restart |
| > 2.5GB | Critical | Restart now |

## Node Heap Tuning

The gateway runs on Node.js and defaults to ~4GB max old space. For long-running gateways or heavy plugin loads, increase via `--max-old-space-size` in the LaunchAgent plist's `ProgramArguments`:

```xml
<string>--max-old-space-size=16384</string>
```

Insert after the `node` binary path, before the entry JS file. Current state:
- **vesper**: `--max-old-space-size=16384` (16GB) — set to handle QMD/memory-search workloads
- **main**: not set (Node default ~4GB)

To add or change, edit the plist directly and reload:
```bash
# Edit the plist
nano ~/Library/LaunchAgents/ai.openclaw.gateway.plist
# Reload
launchctl bootout gui/501/ai.openclaw.gateway && launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

If the gateway OOMs before hitting the RSS thresholds above, this is likely the fix.

## Config Paths

| Profile | Config | State | Port |
|---------|--------|-------|------|
| main | `~/.openclaw/openclaw.json` | `~/.openclaw/` | 18789 |
| vesper | `~/.openclaw-vesper/openclaw.json` | `~/.openclaw-vesper/` | 18999 |

**Plugin auto-discovery paths** (scanned on startup, no config entry needed):
- `~/.openclaw/extensions/<plugin-id>/` — per-profile custom plugins
- Paths listed in `plugins.load.paths` — explicitly loaded extensions

## Auth

- Gateway token: `$OPENCLAW_GATEWAY_TOKEN` (env var in shell rc — `~/.zshrc`/`~/.bashrc`). **Takes precedence over `gateway.remote.token` in config.** Profile-agnostic — all profiles must use the same token when this env var is set.
- Gateway password: `$OPENCLAW_GATEWAY_PASSWORD` (env var in shell rc — `~/.zshrc`/`~/.bashrc`)
- CLI auth resolution order: `$OPENCLAW_GATEWAY_TOKEN` > `gateway.remote.token` (config)
- `gateway.controlUi.dangerouslyDisableDeviceAuth: true` — only bypasses Control UI, not CLI/TUI
- CLI/TUI always requires device pairing in 2026.2.25+

### API Token Locations (v2026.3.1+)
Top-level `openclaw.json` auth.profiles declares profile type/mode only — **no tokens**.
Actual tokens live in per-agent auth profile files:
```
# Main profile
~/.openclaw/agents/main/agent/auth-profiles.json
~/.openclaw/agents/codex/agent/auth-profiles.json

# Vesper profile
~/.openclaw-vesper/agents/main/agent/auth-profiles.json
~/.openclaw-vesper/agents/codex/agent/auth-profiles.json
```
Each has `profiles.<provider>:default` with `access`/`refresh`/`expires` for OAuth, or `token` for API keys.
The `expires` field is epoch milliseconds — compare to `Date.now()` or `time.time()*1000` to check expiry.

Fresh Anthropic setup tokens: `~/clawd/inbox/2026-03-03-anthropic-setup-tokens`

### doctor --fix Token Migration (v2026.3.1)
`openclaw doctor --fix` removes `token` fields from top-level `auth.profiles` in `openclaw.json` (schema change). This does NOT affect per-agent auth profiles — those still use `token` as the field name. If doctor runs and removes tokens from the top-level config, the gateway still works because it reads from per-agent files at runtime.

### OpenAI Codex OAuth Refresh
**Symptom:** `OAuth token refresh failed for openai-codex` or `refresh_token_reused` — the access token expired and the refresh token is single-use/already consumed.
**Diagnosis:** Check `expires` field in `auth-profiles.json` — if epoch ms is in the past, access token is expired. If refresh also fails, full re-auth needed.
**Fix:** Interactive re-auth: `openclaw configure` (add `--profile vesper` if vesper profile).

### Unconfigured Fallback Provider
**Symptom:** `No API key found for provider "<provider>"` with auth store path shown.
**Diagnosis:** The model fallback chain references a provider that was never set up in auth-profiles.json.
**Fix:** Either configure the provider (`openclaw agents add <provider>`) or remove it from the fallback chain in `openclaw.json` → `agents.defaults.model.fallbacks`.

## Memory Search / QMD

Check memory search status as part of triage when the agent isn't responding correctly:
```bash
openclaw --profile vesper memory status
```
Key config: `agents.defaults.memorySearch.enabled` in `openclaw.json` — if `false`, the `memory_search`/`memory_get` tools won't register even if listed in `tools.alsoAllow`.

Enabling requires a gateway restart (hot-reload picks up the config but tool registration needs restart).

## QMD / Memory Search Debugging

`qmd` runs on **Node.js** (`#!/usr/bin/env node`), NOT Bun. The sqlite-vec extension loads fine under Node's `better-sqlite3`. Previous reports of "sqlite-vec/Bun" issues are a **red herring** for OpenClaw users.

If `qmd embed` hangs or fails:
```bash
# 1. Check Homebrew SQLite is installed
brew list sqlite

# 2. Rebuild better-sqlite3 if needed
npm rebuild better-sqlite3 --build-from-source
# Note: npm v11 warns about --build-from-source but the flag still works (cosmetic warning)

# 3. Check embedding status
qmd status  # Shows pending embedding count

# 4. Force re-embedding of all content
qmd embed -f

# 5. Update collections that may have new files
qmd update <collection>  # e.g., tool-heuristics collections after adding files
```

Key commands for memory search triage:
- `qmd status` — shows collections, document counts, pending embeds
- `qmd embed` — process pending embeddings (runs incrementally)
- `qmd embed -f` — force re-embed everything (nuclear option)
- `qmd update <collection>` — re-scan collection source for new/changed files

## Gateway Restart (by profile)

| Profile | LaunchAgent plist | Stop + Start |
|---------|-------------------|--------------|
| main | `~/Library/LaunchAgents/ai.openclaw.gateway.plist` | `openclaw gateway stop && launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.gateway.plist` |
| vesper | `~/Library/LaunchAgents/ai.openclaw.vesper.plist` | `openclaw --profile vesper gateway stop && launchctl bootstrap gui/501 ~/Library/LaunchAgents/ai.openclaw.vesper.plist` |

If `gateway start` says "Gateway service not loaded", use `launchctl bootstrap` directly.

## Post-Fix Protocol

After fixing any issue:
1. Verify: `openclaw channels status` — all channels should show "running"
2. Check memory: `ps -o pid,rss,pcpu,etime -p $(lsof -i :18789 -t | head -1)`
3. Write incident report to `~/clawd/inbox/YYYY-MM-DD-<description>.md`

## Incident Report Template

```markdown
# Incident: <Title> — YYYY-MM-DD

## Summary
<1-2 sentences>

## Symptoms
- <what the user saw>

## Root Cause
<what went wrong and why>

## Fix
<what was done>

## Config Changes
| File | Change |
|------|--------|

## Prevention
<how to avoid next time>
```

## Post-Upgrade Checklist

Run after any openclaw version bump:
```bash
openclaw --version
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.pre-upgrade
openclaw doctor --fix

# CRITICAL: Regenerate plist for new version (update does NOT do this automatically)
openclaw gateway install
# For vesper too:
openclaw --profile vesper gateway install

# Verify plists weren't cross-contaminated (failure mode #14)
grep OPENCLAW_STATE_DIR ~/Library/LaunchAgents/ai.openclaw.gateway.plist
grep OPENCLAW_STATE_DIR ~/Library/LaunchAgents/ai.openclaw.vesper.plist

openclaw devices list --json | jq '.pending'
# Approve any pending pairings
openclaw channels status
```

## Vesper Profile Commands

Prefix all commands with `--profile vesper`:
```bash
openclaw --profile vesper channels status
openclaw --profile vesper gateway start
openclaw --profile vesper doctor --fix
```
