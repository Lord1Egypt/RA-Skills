#!/usr/bin/env bash
set -euo pipefail

cmd="${1:-status}"
shift || true
hermes_home="${HERMES_HOME:-$HOME/.hermes}"
agent_dir="${HERMES_AGENT_DIR:-$hermes_home/hermes-agent}"
service="${HERMES_GATEWAY_SERVICE:-hermes-gateway.service}"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
guard_src="$script_dir/action_stop.py"
loop_file="${HERMES_LOOP_FILE:-$agent_dir/agent/conversation_loop.py}"
guard_dst="$(dirname "$loop_file")/action_stop.py"
config="${HERMES_CONFIG:-$hermes_home/config.yaml}"
backup_root="${HERMES_GUARD_BACKUP_ROOT:-$hermes_home/backups}"
marker="Messaging action-promise stop guard"
python_bin="${HERMES_PYTHON:-$agent_dir/venv/bin/python}"
dry_run=0
backup_arg=""

while (($#)); do
  case "$1" in
    --dry-run) dry_run=1 ;;
    --backup) shift; backup_arg="${1:-}" ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
  shift
done

die() { echo "error: $*" >&2; exit 2; }
service_active() { systemctl --user is-active --quiet "$service"; }
detect_layout() {
  test -f "$loop_file" || die "unsupported Hermes layout: missing $loop_file"
  test -f "$config" || die "missing config: $config"
  test -x "$python_bin" || die "missing Hermes Python: $python_bin"
  test -f "$guard_src" || die "missing bundled guard: $guard_src"
}
patch_probe() {
  "$python_bin" - "$loop_file" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); s=p.read_text()
anchors=[
'                messages.append(final_msg)\n                \n                _turn_exit_reason = f"text_response(finish_reason={finish_reason})"',
'                messages.append(final_msg)\n\n                _turn_exit_reason = f"text_response(finish_reason={finish_reason})"',
]
if "Messaging action-promise stop guard" in s: print("already-patched"); raise SystemExit(0)
hits=[a for a in anchors if a in s]
if len(hits)!=1: raise SystemExit("unsupported or ambiguous conversation loop anchor")
if "    if moa_config is None:\n" not in s: raise SystemExit("unsupported initialization anchor")
print("compatible")
PY
}
status() {
  detect_layout
  patch_probe
  if grep -q "$marker" "$loop_file" && test -f "$guard_dst"; then state=installed; else state=missing; fi
  printf 'guard=%s\nloop_file=%s\nconfig=%s\nservice=%s\n' "$state" "$loop_file" "$config" "$service"
  grep -E 'hard_stop_enabled:|threshold:|target_ratio:|mode:|idle_minutes:' "$config" || true
}
make_backup() {
  local service_was_active="${1:-0}"
  local backup="$backup_root/hermes-action-loop-guard-$(date -u +%Y%m%dT%H%M%SZ)"
  mkdir -p "$backup"
  cp -a "$config" "$backup/config.yaml"
  cp -a "$loop_file" "$backup/conversation_loop.py"
  if test -f "$guard_dst"; then cp -a "$guard_dst" "$backup/action_stop.py"; fi
  {
    printf 'HERMES_LOOP_FILE=%q\n' "$loop_file"
    printf 'HERMES_CONFIG=%q\n' "$config"
    printf 'HERMES_GUARD_FILE=%q\n' "$guard_dst"
    printf 'HERMES_GATEWAY_SERVICE=%q\n' "$service"
    printf 'GUARD_PREEXISTED=%q\n' "$(test -f "$guard_dst" && echo 1 || echo 0)"
    printf 'SERVICE_WAS_ACTIVE=%q\n' "$service_was_active"
  } > "$backup/manifest.env"
  printf '%s' "$backup"
}
restore_backup() {
  local backup="$1"
  test -n "$backup" || die "rollback requires --backup PATH"
  test -f "$backup/manifest.env" || die "invalid backup: no manifest.env"
  # shellcheck disable=SC1090
  source "$backup/manifest.env"
  test -f "$backup/config.yaml" || die "backup missing config.yaml"
  test -f "$backup/conversation_loop.py" || die "backup missing conversation_loop.py"
  local restore_active="${SERVICE_WAS_ACTIVE:-}"
  if test -z "$restore_active"; then
    restore_active=0
    service_active && restore_active=1 || true
  fi
  systemctl --user stop "$HERMES_GATEWAY_SERVICE"
  cp -a "$backup/config.yaml" "$HERMES_CONFIG"
  cp -a "$backup/conversation_loop.py" "$HERMES_LOOP_FILE"
  if test "$GUARD_PREEXISTED" = 1; then
    test -f "$backup/action_stop.py" || die "backup missing prior action_stop.py"
    cp -a "$backup/action_stop.py" "$HERMES_GUARD_FILE"
  else
    test ! -e "$HERMES_GUARD_FILE" || mv "$HERMES_GUARD_FILE" "$backup/action_stop.py.removed"
  fi
  "$python_bin" -m py_compile "$HERMES_LOOP_FILE"
  if test "$restore_active" = 1; then systemctl --user start "$HERMES_GATEWAY_SERVICE"; fi
  echo "rolled_back backup=$backup"
}
install_guard() {
  detect_layout
  patch_probe
  if grep -q "$marker" "$loop_file" && test -f "$guard_dst"; then echo "already installed"; return; fi
  if test "$dry_run" = 1; then echo "compatible dry_run=true"; return; fi
  local backup was_active=0
  service_active && was_active=1 || true
  backup="$(make_backup "$was_active")"
  systemctl --user stop "$service"
  trap 'restore_backup "$backup" >/dev/null 2>&1 || true' ERR
  cp "$guard_src" "$guard_dst"
  "$python_bin" - "$loop_file" "$config" <<'PY'
from pathlib import Path
import re, sys
loop=Path(sys.argv[1]); cfg=Path(sys.argv[2]); text=loop.read_text()
init='    if moa_config is None:\n'
text=text.replace(init, '    agent._action_stop_nudges = 0\n\n'+init, 1)
anchors=[
'                messages.append(final_msg)\n                \n                _turn_exit_reason = f"text_response(finish_reason={finish_reason})"',
'                messages.append(final_msg)\n\n                _turn_exit_reason = f"text_response(finish_reason={finish_reason})"',
]
anchor=next((a for a in anchors if a in text), None)
if not anchor: raise SystemExit("conversation loop changed after preflight")
block='''                # ── Messaging action-promise stop guard ───────────────
                try:
                    from agent.action_stop import build_action_stop_nudge
                    _action_nudge = build_action_stop_nudge(
                        messages=messages, response=final_response or "",
                        platform=getattr(agent, "platform", "") or "",
                        attempts=getattr(agent, "_action_stop_nudges", 0),
                    )
                except Exception:
                    logger.debug("action stop-loop check failed", exc_info=True)
                    _action_nudge = None
                if _action_nudge:
                    agent._action_stop_nudges += 1
                    final_msg["finish_reason"] = "action_tool_required"
                    final_msg["_action_stop_synthetic"] = True
                    messages.append(final_msg)
                    messages.append({"role": "user", "content": _action_nudge,
                                     "_action_stop_synthetic": True})
                    agent._session_messages = messages
                    final_response = None
                    continue

'''+anchor
loop.write_text(text.replace(anchor, block, 1))
raw=cfg.read_text()
subs=[
(r'(?m)^(\s*hard_stop_enabled:)\s*false\s*$', r'\1 true'),
(r'(?m)^(\s*threshold:)\s*0\.5\s*$', r'\1 0.35'),
(r'(?m)^(\s*target_ratio:)\s*0\.2\s*$', r'\1 0.18'),
(r'(?m)^(session_reset:\n\s*mode:)\s*none\s*$', r'\1 both'),
(r'(?m)^(\s*idle_minutes:)\s*1440\s*$', r'\1 180')]
for pat,repl in subs: raw=re.sub(pat,repl,raw)
cfg.write_text(raw)
PY
  "$python_bin" -m py_compile "$guard_dst" "$loop_file"
  if test "$was_active" = 1; then systemctl --user start "$service"; service_active; fi
  trap - ERR
  echo "installed backup=$backup"
}
verify() {
  status
  grep -q "$marker" "$loop_file" || die "guard marker absent"
  test -f "$guard_dst" || die "guard module absent"
  "$python_bin" -m py_compile "$guard_dst" "$loop_file"
  if service_active; then service_state=active; else service_state=inactive; fi
  printf 'service_state=%s\n' "$service_state"
  echo "verify=ok"
}

case "$cmd" in
  status) status ;;
  install) install_guard ;;
  verify) verify ;;
  rollback) detect_layout; restore_backup "$backup_arg" ;;
  test-compat) exec bash "$script_dir/test-compat.sh" ;;
  *) echo "usage: $0 {status|install [--dry-run]|verify|rollback --backup PATH|test-compat}" >&2; exit 2 ;;
esac
