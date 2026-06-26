# LDR Skill Usage Examples

## Modes and language

- **Quick Summary** (`--mode quick`): faster, shorter output; good for a brief overview.
- **Detailed Report** (`--mode detailed`): full multi-cycle report with full citations.
- **Output language** (`--language <code>`): e.g. `en`, `es`, `fr`, `de`, `zh`, `ja`. Set default via `LDR_DEFAULT_LANGUAGE`.

## Quick Start

### One-shot Research (wait for completion)

```bash
# Ensure LDR_SERVICE_USER and LDR_SERVICE_PASSWORD are set (env or local .env)
research_id=$(scripts/ldr-research.sh start_research \
  --query "latest developments in solid-state batteries" \
  --mode detailed | jq -r '.research_id')

echo "Started research: $research_id"
scripts/ldr-research.sh poll_until_complete --research_id "$research_id" --interval 15
scripts/ldr-research.sh get_result --research_id "$research_id" | jq -r '.report_markdown'
```

### Quick Summary in Spanish

```bash
scripts/ldr-research.sh start_research --query "tendencias en IA 2026" --mode quick --language es
```

### Fire-and-forget (async)

```bash
response=$(scripts/ldr-research.sh start_research \
  --query "quantum computing advances 2026" \
  --mode detailed \
  --language en \
  --search_tool searxng)

research_id=$(echo "$response" | jq -r '.research_id')
echo "Research ID: $research_id"
echo "Check later: scripts/ldr-research.sh get_status --research_id $research_id"

# When ready:
status=$(scripts/ldr-research.sh get_status --research_id "$research_id")
state=$(echo "$status" | jq -r '.state')
[[ "$state" == "completed" ]] && scripts/ldr-research.sh get_result --research_id "$research_id" > report.json
```

## OpenClaw integration

Credentials: set `LDR_SERVICE_USER` and `LDR_SERVICE_PASSWORD` (or `LDR_USERNAME`/`LDR_PASSWORD`) via env or `~/.config/local_deep_research/config/.env`. The script performs session + CSRF login automatically.

```bash
LDR_SCRIPT="$(pwd)/scripts/ldr-research.sh"   # when run from skill root

query="$1"
result=$("$LDR_SCRIPT" start_research --query "$query" --mode detailed)
research_id=$(echo "$result" | jq -r '.research_id')

echo "Started deep research: $query (ID: $research_id)"

while true; do
  status=$("$LDR_SCRIPT" get_status --research_id "$research_id")
  state=$(echo "$status" | jq -r '.state')
  echo "Progress: $(echo "$status" | jq -r '.progress')% - $(echo "$status" | jq -r '.message')"

  case "$state" in
    completed) "$LDR_SCRIPT" get_result --research_id "$research_id" | jq -r '.report_markdown'; break ;;
    failed|timeout) echo "Research $state"; exit 1 ;;
  esac
  sleep 20
done
```

## Configuration (env only for secrets)

Store credentials in env or a **private** .env (add to .gitignore). LDR uses session + CSRF; do not put username/password in OpenClaw config.

```bash
# In shell or private .env
export LDR_BASE_URL="http://127.0.0.1:5000"
export LDR_SERVICE_USER="openclaw_service"
export LDR_SERVICE_PASSWORD="your-strong-password"
export LDR_DEFAULT_MODE="detailed"
export LDR_DEFAULT_LANGUAGE="en"
export LDR_DEFAULT_SEARCH_TOOL="searxng"
```

If LDR uses a different login path:

```bash
export LDR_LOGIN_URL="http://127.0.0.1:5000/login"
```

## Troubleshooting

### Authentication failures

LDR uses **session-cookie + CSRF**, not Basic Auth. Ensure credentials are set (env or local .env) and run the script; look for "Login successful". If LDR’s login form uses different field names (e.g. `email` instead of `username`), you may need to adjust the script’s login POST or set `LDR_LOGIN_URL` to the correct path.

### Connection refused

```bash
curl -s "$LDR_BASE_URL/health"
# Start LDR service if not running
```

### Research stuck

Check LDR service health and logs; consider timeout/restart if there’s no progress for a long time.
