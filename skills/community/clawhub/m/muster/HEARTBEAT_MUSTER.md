
## Muster check-in
- Call Muster MCP `heartbeat` tool with your agent_id and current status
- **Error handling:** Distinguish failure modes when the heartbeat curl fails:
  - `curl exit 7` (connection refused) → "Muster server unreachable — check if it's running"
  - `curl exit 28` (timeout) → "Muster server timed out — may be overloaded"
  - HTTP `401` → "API key invalid — regenerate via Settings or re-run connect.sh"
  - HTTP `5xx` → "Muster server error — check server logs"
  - Do NOT report all failures as "API key invalid" — check curl exit code and HTTP status separately
- If `next_task` returned: pick it up (see Muster skill for task workflow)
- If `update_available` is true: run `bash ~/.openclaw/workspace/skills/muster/scripts/update.sh`
- If `tunnel_url` changed vs `~/.muster/tunnel.json`: update stored value, notify human with new URL
- If tunnel is down (no `tunnel_url`): restart tunnel service — macOS: `launchctl kickstart -k "gui/$(id -u)/com.bai.muster-tunnel"`, Linux: `pm2 restart muster-tunnel` — capture new URL, notify human
- If stuck task from a previous crash: resume or mark failed with explanation
- If idle and no tasks: consider proposing initiative via `create_task`
