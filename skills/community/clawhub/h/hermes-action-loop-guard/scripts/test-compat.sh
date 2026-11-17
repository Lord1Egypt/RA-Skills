#!/usr/bin/env bash
set -euo pipefail
root="$(mktemp -d)"
trap 'rm -rf "$root"' EXIT
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for spacing in spaced compact; do
  home="$root/$spacing/.hermes"; agent="$home/hermes-agent"
  mkdir -p "$agent/agent" "$agent/venv/bin" "$home/backups"
  ln -s "$(command -v python3)" "$agent/venv/bin/python"
  cp "$script_dir/action_stop.py" "$agent/agent/action_stop.py.source"
  if test "$spacing" = spaced; then gap="                "; else gap=""; fi
  {
    printf 'def run(agent, messages, final_msg, final_response, finish_reason, moa_config):\n'
    printf '    if moa_config is None:\n        pass\n'
    printf '                messages.append(final_msg)\n%s\n' "$gap"
    printf '                _turn_exit_reason = f"text_response(finish_reason={finish_reason})"\n'
  } > "$agent/agent/conversation_loop.py"
  cat > "$home/config.yaml" <<'YAML'
tool_call_loop:
  hard_stop_enabled: false
compression:
  threshold: 0.5
  target_ratio: 0.2
session_reset:
  mode: none
  idle_minutes: 1440
YAML
  HERMES_HOME="$home" HERMES_AGENT_DIR="$agent"     HERMES_ACTION_STOP_NUDGE=1     bash "$script_dir/install-hermes-action-guard.sh" install --dry-run | grep compatible >/dev/null
done
echo "compatibility_tests=ok fixtures=2"
