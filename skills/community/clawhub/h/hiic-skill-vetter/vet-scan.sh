#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-}"

if [[ -z "$TARGET" ]]; then
  echo "Usage: $0 <skill-dir>" >&2
  exit 1
fi

if [[ ! -d "$TARGET" ]]; then
  echo "Error: directory not found: $TARGET" >&2
  exit 1
fi

if command -v rg >/dev/null 2>&1; then
  GREP_CMD=(rg -n -S --hidden)
else
  GREP_CMD=(grep -RIn)
fi

print_section() {
  printf '\n== %s ==\n' "$1"
}

run_search() {
  local label="$1"
  local pattern="$2"
  print_section "$label"
  if "${GREP_CMD[@]}" -g '!*node_modules/*' -g '!*dist/*' -g '!*build/*' -g '!*coverage/*' "$pattern" "$TARGET" 2>/dev/null; then
    :
  else
    echo "(no matches)"
  fi
}

print_section "FILE INVENTORY"
find "$TARGET" -type f | sort

print_section "TOP-LEVEL METADATA"
for f in SKILL.md package.json package-lock.json pnpm-lock.yaml yarn.lock requirements.txt pyproject.toml Cargo.toml; do
  if [[ -f "$TARGET/$f" ]]; then
    echo "--- $f ---"
    sed -n '1,120p' "$TARGET/$f"
  fi
done

run_search "NETWORK CALLS" 'curl|wget|fetch\(|axios|requests\.|httpx\.|urllib|https?://'
run_search "DYNAMIC EXECUTION" 'eval\(|exec\(|bash -c|sh -c|subprocess|child_process|spawn\(|execFile\(|os\.system\('
run_search "ENCODING / OBFUSCATION" 'base64|Buffer\.from\(.*base64|atob\(|btoa\(|gzip|zlib|decode'
run_search "SENSITIVE FILE ACCESS" '\.env|~/.ssh|~/.aws|~/.config|MEMORY\.md|USER\.md|SOUL\.md|IDENTITY\.md|cookie|session|token|credential'
run_search "INSTALL / PACKAGE OPS" 'npm install|pnpm add|yarn add|pip install|uv pip|brew install|apt install|yum install|go install|cargo install'
run_search "PERSISTENCE / BACKGROUND" 'cron|systemd|launchd|daemon|service|nohup|tmux|screen|pm2'
run_search "ELEVATED PRIVILEGES" 'sudo|setcap|chmod 777|chown root'
run_search "DIRECT IPS" 'https?://([0-9]{1,3}\.){3}[0-9]{1,3}'

print_section "DONE"
echo "Review the matches manually. This script is a triage helper, not a verdict."
