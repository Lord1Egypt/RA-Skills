#!/usr/bin/env bash
set -euo pipefail

root="$(mktemp -d)"
trap 'rm -rf "$root"' EXIT
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

make_fixture() {
  local name="$1" initial_state="$2"
  local case_root="$root/$name" home agent
  home="$case_root/.hermes"
  agent="$home/hermes-agent"
  mkdir -p "$case_root/bin" "$agent/agent" "$agent/venv/bin" "$home/backups"
  ln -s "$(command -v python3)" "$agent/venv/bin/python"
  printf '%s\n' "$initial_state" > "$case_root/service-state"
  cat > "$case_root/bin/systemctl" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
test "${1:-}" = --user && shift
cmd="${1:-}"; shift || true
case "$cmd" in
  is-active)
    test "${1:-}" = --quiet && shift || true
    test "$(cat "$MOCK_SERVICE_STATE")" = active
    ;;
  stop) printf '%s\n' inactive > "$MOCK_SERVICE_STATE" ;;
  start) printf '%s\n' active > "$MOCK_SERVICE_STATE" ;;
  *) echo "unsupported mock systemctl command: $cmd" >&2; exit 2 ;;
esac
SH
  chmod +x "$case_root/bin/systemctl"
  cat > "$agent/agent/conversation_loop.py" <<'PY'
def run(agent, messages, final_msg, final_response, finish_reason, moa_config):
    if moa_config is None:
        pass
    while True:
        if True:
            if True:
                messages.append(final_msg)

                _turn_exit_reason = f"text_response(finish_reason={finish_reason})"
PY
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
  printf '%s\n' "$case_root"
}

run_case() {
  local name="$1" initial_state="$2" state_before_rollback="$3"
  local case_root home agent output backup
  case_root="$(make_fixture "$name" "$initial_state")"
  home="$case_root/.hermes"; agent="$home/hermes-agent"
  output="$(
    PATH="$case_root/bin:$PATH" MOCK_SERVICE_STATE="$case_root/service-state" \
    HERMES_HOME="$home" HERMES_AGENT_DIR="$agent" \
    bash "$script_dir/install-hermes-action-guard.sh" install
  )"
  backup="${output##*backup=}"
  test -f "$backup/manifest.env"
  # shellcheck disable=SC1090
  source "$backup/manifest.env"
  if test "$initial_state" = active; then test "$SERVICE_WAS_ACTIVE" = 1; else test "$SERVICE_WAS_ACTIVE" = 0; fi
  test "$(cat "$case_root/service-state")" = "$initial_state"

  printf '%s\n' "$state_before_rollback" > "$case_root/service-state"
  PATH="$case_root/bin:$PATH" MOCK_SERVICE_STATE="$case_root/service-state" \
    HERMES_HOME="$home" HERMES_AGENT_DIR="$agent" \
    bash "$script_dir/install-hermes-action-guard.sh" rollback --backup "$backup" >/dev/null
  test "$(cat "$case_root/service-state")" = "$initial_state"
  ! grep -q 'Messaging action-promise stop guard' "$agent/agent/conversation_loop.py"
  test ! -e "$agent/agent/action_stop.py"
}

run_case active-install active inactive
run_case inactive-install inactive active

verify_root="$(make_fixture verify-inactive inactive)"
verify_home="$verify_root/.hermes"; verify_agent="$verify_home/hermes-agent"
PATH="$verify_root/bin:$PATH" MOCK_SERVICE_STATE="$verify_root/service-state" \
  HERMES_HOME="$verify_home" HERMES_AGENT_DIR="$verify_agent" \
  bash "$script_dir/install-hermes-action-guard.sh" install >/dev/null
verify_output="$(
  PATH="$verify_root/bin:$PATH" MOCK_SERVICE_STATE="$verify_root/service-state" \
  HERMES_HOME="$verify_home" HERMES_AGENT_DIR="$verify_agent" \
  bash "$script_dir/install-hermes-action-guard.sh" verify
)"
grep -q '^service_state=inactive$' <<<"$verify_output"
grep -q '^verify=ok$' <<<"$verify_output"

run_tool_rollback_case() {
  local name="$1" recorded_state="$2" current_state="$3"
  local case_root="$root/$name" home agent backup
  home="$case_root/.hermes"; agent="$home/hermes-agent"; backup="$home/backups/tool"
  mkdir -p "$case_root/bin" "$agent/agent" "$agent/venv/bin" "$backup"
  ln -s "$(command -v python3)" "$agent/venv/bin/python"
  printf '%s\n' "$current_state" > "$case_root/service-state"
  cp "$verify_root/bin/systemctl" "$case_root/bin/systemctl"
  chmod +x "$case_root/bin/systemctl"
  printf '%s\n' 'successful_no_progress_tools = True' > "$agent/agent/tool_guardrails.py"
  printf '%s\n' 'patched: true' > "$home/config.yaml"
  printf '%s\n' 'ORIGINAL = True' > "$backup/tool_guardrails.py"
  printf '%s\n' 'original: true' > "$backup/config.yaml"
  if test "$recorded_state" = active; then recorded=1; else recorded=0; fi
  cat > "$backup/manifest.env" <<EOF
HERMES_TOOL_GUARD_FILE=$agent/agent/tool_guardrails.py
HERMES_CONFIG=$home/config.yaml
HERMES_GATEWAY_SERVICE=mock.service
SERVICE_WAS_ACTIVE=$recorded
EOF
  PATH="$case_root/bin:$PATH" MOCK_SERVICE_STATE="$case_root/service-state" \
    HERMES_HOME="$home" HERMES_AGENT_DIR="$agent" \
    bash "$script_dir/install-hermes-tool-progress-guard.sh" rollback --backup "$backup" >/dev/null
  test "$(cat "$case_root/service-state")" = "$recorded_state"
  grep -q '^ORIGINAL = True$' "$agent/agent/tool_guardrails.py"
  grep -q '^original: true$' "$home/config.yaml"
}

run_tool_rollback_case tool-active active inactive
run_tool_rollback_case tool-inactive inactive active

tool_verify_root="$root/tool-verify-inactive"
tool_verify_home="$tool_verify_root/.hermes"; tool_verify_agent="$tool_verify_home/hermes-agent"
mkdir -p "$tool_verify_root/bin" "$tool_verify_agent/agent" "$tool_verify_agent/venv/bin"
ln -s "$(command -v python3)" "$tool_verify_agent/venv/bin/python"
cp "$verify_root/bin/systemctl" "$tool_verify_root/bin/systemctl"; chmod +x "$tool_verify_root/bin/systemctl"
printf '%s\n' inactive > "$tool_verify_root/service-state"
printf '%s\n' 'successful_no_progress_tools = True' > "$tool_verify_agent/agent/tool_guardrails.py"
printf '%s\n' 'hard_stop_enabled: true' > "$tool_verify_home/config.yaml"
tool_verify_output="$(
  PATH="$tool_verify_root/bin:$PATH" MOCK_SERVICE_STATE="$tool_verify_root/service-state" \
  HERMES_HOME="$tool_verify_home" HERMES_AGENT_DIR="$tool_verify_agent" \
  bash "$script_dir/install-hermes-tool-progress-guard.sh" verify
)"
grep -q '^service_state=inactive$' <<<"$tool_verify_output"
grep -q '^verify=ok$' <<<"$tool_verify_output"

echo "installer_lifecycle_tests=ok cases=6"
