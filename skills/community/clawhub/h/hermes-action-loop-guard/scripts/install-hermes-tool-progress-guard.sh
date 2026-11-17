#!/usr/bin/env bash
set -euo pipefail
cmd="${1:-status}"; shift || true
hermes_home="${HERMES_HOME:-$HOME/.hermes}"
agent_dir="${HERMES_AGENT_DIR:-$hermes_home/hermes-agent}"
service="${HERMES_GATEWAY_SERVICE:-hermes-gateway.service}"
guard_file="${HERMES_TOOL_GUARD_FILE:-$agent_dir/agent/tool_guardrails.py}"
config="${HERMES_CONFIG:-$hermes_home/config.yaml}"
python_bin="${HERMES_PYTHON:-$agent_dir/venv/bin/python}"
backup_root="${HERMES_GUARD_BACKUP_ROOT:-$hermes_home/backups}"
backup_arg=""; dry_run=0
while (($#)); do case "$1" in --dry-run) dry_run=1;; --backup) shift; backup_arg="${1:-}";; *) echo "unknown argument: $1" >&2; exit 2;; esac; shift; done
die(){ echo "error: $*" >&2; exit 2; }
active(){ systemctl --user is-active --quiet "$service"; }
detect(){
  test -f "$guard_file" || die "missing $guard_file"
  test -f "$config" || die "missing $config"
  test -x "$python_bin" || die "missing $python_bin"
  "$python_bin" - "$guard_file" <<'PY'
from pathlib import Path
import sys
s=Path(sys.argv[1]).read_text()
anchors=[
'    no_progress_block_after: int = 5\n',
'        self._turn_subagent_count = 0\n',
'        if not self._is_idempotent(tool_name):\n            self._no_progress.pop(signature, None)\n            return ToolGuardrailDecision(tool_name=tool_name, signature=signature)\n',
]
if 'successful_no_progress_tools' in s:
 print('already-patched'); raise SystemExit(0)
missing=[a for a in anchors if s.count(a)!=1]
if missing: raise SystemExit('unsupported or ambiguous tool_guardrails layout')
print('compatible')
PY
}
patch(){
 "$python_bin" - "$guard_file" "$config" <<'PY'
from pathlib import Path
import re,sys
p=Path(sys.argv[1]); cfg=Path(sys.argv[2]); s=p.read_text()
if 'successful_no_progress_tools' not in s:
 s=s.replace('    no_progress_block_after: int = 5\n',
'''    no_progress_block_after: int = 5
    successful_no_progress_tools: frozenset[str] = field(
        default_factory=lambda: frozenset({"execute_code", "terminal", "process"})
    )
    max_total_calls_warn_after: int = 20
    max_total_calls_second_warn_after: int = 40
    max_total_calls_per_turn: int = 60
    max_strategy_redirects_per_turn: int = 60
''',1)
 s=s.replace('            loop_caps=LoopCapConfig.from_mapping(data.get("loop_caps")),\n',
'''            successful_no_progress_tools=frozenset(
                str(x) for x in data.get(
                    "successful_no_progress_tools",
                    defaults.successful_no_progress_tools,
                )
            ),
            max_total_calls_warn_after=_non_negative_int(
                data.get("max_total_calls_warn_after"),
                defaults.max_total_calls_warn_after,
            ),
            max_total_calls_second_warn_after=_non_negative_int(
                data.get("max_total_calls_second_warn_after"),
                defaults.max_total_calls_second_warn_after,
            ),
            max_total_calls_per_turn=_non_negative_int(
                data.get("max_total_calls_per_turn"),
                defaults.max_total_calls_per_turn,
            ),
            max_strategy_redirects_per_turn=_non_negative_int(
                data.get("max_strategy_redirects_per_turn"),
                defaults.max_strategy_redirects_per_turn,
            ),
            loop_caps=LoopCapConfig.from_mapping(data.get("loop_caps")),
''',1)
 s=s.replace('        self._turn_subagent_count = 0\n',
'''        self._turn_subagent_count = 0
        self._turn_total_call_count = 0
        self._turn_strategy_redirect_count = 0
''',1)
 s=s.replace('        signature = ToolCallSignature.from_call(tool_name, _coerce_args(args))\n',
'''        signature = ToolCallSignature.from_call(tool_name, _coerce_args(args))
        if (
            self.config.max_total_calls_per_turn
            and self._turn_total_call_count >= self.config.max_total_calls_per_turn
        ):
            decision = ToolGuardrailDecision(
                action="halt",
                code="total_tool_call_cap",
                message=(
                    f"Stopped this turn after {self._turn_total_call_count} tool calls. "
                    "The tool budget was exhausted; summarize progress and choose a new strategy."
                ),
                tool_name=tool_name,
                count=self._turn_total_call_count,
                signature=signature,
            )
            return self._redirect_or_halt(decision)
        self._turn_total_call_count += 1
        if (
            self.config.warnings_enabled
            and self._turn_total_call_count in {
                self.config.max_total_calls_warn_after,
                self.config.max_total_calls_second_warn_after,
            }
        ):
            return ToolGuardrailDecision(
                action="warn",
                code="total_tool_call_checkpoint_warning",
                message=(
                    f"This turn has used {self._turn_total_call_count} tool calls. "
                    "Summarize concrete new evidence, check for repeated paths, and "
                    "continue only with a clear remaining strategy."
                ),
                tool_name=tool_name,
                count=self._turn_total_call_count,
                signature=signature,
            )
''',1)
 s=s.replace('        if self._is_idempotent(tool_name):\n',
'''        if self._is_idempotent(tool_name) or tool_name in self.config.successful_no_progress_tools:
''',1)
 old='''        if not self._is_idempotent(tool_name):
            self._no_progress.pop(signature, None)
            return ToolGuardrailDecision(tool_name=tool_name, signature=signature)
'''
 new='''        tracks_success = (
            self._is_idempotent(tool_name)
            or tool_name in self.config.successful_no_progress_tools
        )
        if not tracks_success:
            self._no_progress.pop(signature, None)
            return ToolGuardrailDecision(tool_name=tool_name, signature=signature)
        if file_mutation_result_landed(tool_name, result or ""):
            self._no_progress.pop(signature, None)
            return ToolGuardrailDecision(tool_name=tool_name, signature=signature)
'''
 if old not in s: raise SystemExit('after_call anchor changed')
 s=s.replace(old,new,1)
 s,replaced_halts=re.subn(
  r'(?m)^(\s*)self\._halt_decision = decision\n\1return decision$',
  r'\1return self._redirect_or_halt(decision)',
  s,
 )
 if replaced_halts < 3:
  raise SystemExit(f'expected at least 3 hard-stop anchors, found {replaced_halts}')
 redirect_helper='''    def _redirect_or_halt(self, decision: ToolGuardrailDecision) -> ToolGuardrailDecision:
        """Turn a bounded hard stop into a synthetic strategy redirect."""
        if self._turn_strategy_redirect_count >= self.config.max_strategy_redirects_per_turn:
            self._halt_decision = decision
            return decision
        self._turn_strategy_redirect_count += 1
        self._exact_failure_counts.clear()
        self._same_tool_failure_counts.clear()
        self._no_progress.clear()
        self._turn_total_call_count = 0
        return ToolGuardrailDecision(
            action="redirect",
            code=f"{decision.code}_strategy_redirect",
            message="换思路",
            tool_name=decision.tool_name,
            count=decision.count,
            signature=decision.signature,
        )

'''
 marker='    def before_call(self, tool_name: str, args: Mapping[str, Any] | None) -> ToolGuardrailDecision:\n'
 if marker not in s: raise SystemExit('before_call method anchor changed')
 s=s.replace(marker,redirect_helper+marker,1)
 s=s.replace('    if decision.action not in {"warn", "halt"} or not decision.message:\n','    if decision.action not in {"warn", "redirect", "halt"} or not decision.message:\n',1)
 s=s.replace('    label = "Tool loop hard stop" if decision.action == "halt" else "Tool loop warning"\n','    label = "Tool loop hard stop" if decision.action == "halt" else "Tool loop strategy redirect" if decision.action == "redirect" else "Tool loop warning"\n',1)
 p.write_text(s)
elif 'max_total_calls_warn_after' not in s:
 s=s.replace(
  '    max_total_calls_per_turn: int = 20\n',
  '    max_total_calls_warn_after: int = 20\n'
  '    max_total_calls_second_warn_after: int = 40\n'
  '    max_total_calls_per_turn: int = 60\n'
  '    max_strategy_redirects_per_turn: int = 60\n',
  1,
 )
 s=s.replace(
  '''            max_total_calls_per_turn=_non_negative_int(
                data.get("max_total_calls_per_turn"),
                defaults.max_total_calls_per_turn,
            ),
''',
  '''            max_total_calls_warn_after=_non_negative_int(
                data.get("max_total_calls_warn_after"),
                defaults.max_total_calls_warn_after,
            ),
            max_total_calls_second_warn_after=_non_negative_int(
                data.get("max_total_calls_second_warn_after"),
                defaults.max_total_calls_second_warn_after,
            ),
            max_total_calls_per_turn=_non_negative_int(
                data.get("max_total_calls_per_turn"),
                defaults.max_total_calls_per_turn,
            ),
            max_strategy_redirects_per_turn=_non_negative_int(
                data.get("max_strategy_redirects_per_turn"),
                defaults.max_strategy_redirects_per_turn,
            ),
''',
  1,
 )
 s=s.replace(
  '        self._turn_total_call_count += 1\n\n        # ── Per-turn runaway-loop caps',
  '''        self._turn_total_call_count += 1
        if (
            self.config.warnings_enabled
            and self._turn_total_call_count in {
                self.config.max_total_calls_warn_after,
                self.config.max_total_calls_second_warn_after,
            }
        ):
            return ToolGuardrailDecision(
                action="warn",
                code="total_tool_call_checkpoint_warning",
                message=(
                    f"This turn has used {self._turn_total_call_count} tool calls. "
                    "Summarize concrete new evidence, check for repeated paths, and "
                    "continue only with a clear remaining strategy."
                ),
                tool_name=tool_name,
                count=self._turn_total_call_count,
                signature=signature,
            )

        # ── Per-turn runaway-loop caps''',
  1,
 )
 p.write_text(s)
if 'max_strategy_redirects_per_turn' not in s:
 s=s.replace(
  '    max_total_calls_per_turn: int = 60\n',
  '    max_total_calls_per_turn: int = 60\n'
  '    max_strategy_redirects_per_turn: int = 60\n',
  1,
 )
 s=s.replace(
  '''            max_total_calls_per_turn=_non_negative_int(
                data.get("max_total_calls_per_turn"),
                defaults.max_total_calls_per_turn,
            ),
''',
  '''            max_total_calls_per_turn=_non_negative_int(
                data.get("max_total_calls_per_turn"),
                defaults.max_total_calls_per_turn,
            ),
            max_strategy_redirects_per_turn=_non_negative_int(
                data.get("max_strategy_redirects_per_turn"),
                defaults.max_strategy_redirects_per_turn,
            ),
''',
  1,
 )
 s=s.replace(
  '        self._turn_total_call_count = 0\n',
  '        self._turn_total_call_count = 0\n'
  '        self._turn_strategy_redirect_count = 0\n',
  1,
 )
 s,replaced_halts=re.subn(
  r'(?m)^(\s*)self\._halt_decision = decision\n\1return decision$',
  r'\1return self._redirect_or_halt(decision)',
  s,
 )
 if replaced_halts < 3:
  raise SystemExit(f'expected at least 3 v1.2 hard-stop anchors, found {replaced_halts}')
 redirect_helper='''    def _redirect_or_halt(self, decision: ToolGuardrailDecision) -> ToolGuardrailDecision:
        """Turn a bounded hard stop into a synthetic strategy redirect."""
        if self._turn_strategy_redirect_count >= self.config.max_strategy_redirects_per_turn:
            self._halt_decision = decision
            return decision
        self._turn_strategy_redirect_count += 1
        self._exact_failure_counts.clear()
        self._same_tool_failure_counts.clear()
        self._no_progress.clear()
        self._turn_total_call_count = 0
        return ToolGuardrailDecision(
            action="redirect",
            code=f"{decision.code}_strategy_redirect",
            message="换思路",
            tool_name=decision.tool_name,
            count=decision.count,
            signature=decision.signature,
        )

'''
 marker='    def before_call(self, tool_name: str, args: Mapping[str, Any] | None) -> ToolGuardrailDecision:\n'
 if marker not in s: raise SystemExit('v1.2 before_call method anchor changed')
 s=s.replace(marker,redirect_helper+marker,1)
 if 'decision.action not in {"warn", "halt"}' in s:
  s=s.replace('decision.action not in {"warn", "halt"}', 'decision.action not in {"warn", "redirect", "halt"}', 1)
 if 'label = "Tool loop hard stop" if decision.action == "halt" else "Tool loop warning"' in s:
  s=s.replace(
   'label = "Tool loop hard stop" if decision.action == "halt" else "Tool loop warning"',
   'label = "Tool loop hard stop" if decision.action == "halt" else "Tool loop strategy redirect" if decision.action == "redirect" else "Tool loop warning"',
   1,
  )
 p.write_text(s)
raw=cfg.read_text()
if 'successful_no_progress_tools:' not in raw:
 raw=re.sub(r'(?m)^(\s*hard_stop_enabled:\s*true\s*)$',r'''\1
  successful_no_progress_tools:
    - execute_code
    - terminal
    - process
  max_total_calls_warn_after: 20
  max_total_calls_second_warn_after: 40
  max_total_calls_per_turn: 60
  max_strategy_redirects_per_turn: 60''',raw,1)
elif 'max_total_calls_warn_after:' not in raw:
 raw=re.sub(
  r'(?m)^(\s*)max_total_calls_per_turn:\s*20\s*$',
  r'\1max_total_calls_warn_after: 20\n'
  r'\1max_total_calls_second_warn_after: 40\n'
  r'\1max_total_calls_per_turn: 60',
  raw,
  count=1,
 )
raw=re.sub(r'(?m)^(\s*exact_failure:)\s*5\s*$',r'\1 3',raw)
if 'max_strategy_redirects_per_turn:' not in raw:
 raw=re.sub(r'(?m)^(\s*max_total_calls_per_turn:\s*60\s*)$',r'\1\n  max_strategy_redirects_per_turn: 60',raw,count=1)
raw=re.sub(r'(?m)^(\s*same_tool_failure:)\s*8\s*$',r'\1 5',raw)
raw=re.sub(r'(?m)^(\s*idempotent_no_progress:)\s*5\s*$',r'\1 3',raw)
cfg.write_text(raw)
PY
}
case "$cmd" in
 status) detect; grep -E 'hard_stop_enabled:|successful_no_progress_tools:|max_total_calls_warn_after:|max_total_calls_second_warn_after:|max_total_calls_per_turn:|max_strategy_redirects_per_turn:|exact_failure:|same_tool_failure:|idempotent_no_progress:' "$config" || true;;
 install)
  detect
  if grep -q max_strategy_redirects_per_turn "$guard_file"; then echo "already installed"; exit 0; fi
  if test "$dry_run" = 1; then echo "compatible dry_run=true"; exit 0; fi
  backup="$backup_root/hermes-tool-progress-guard-$(date -u +%Y%m%dT%H%M%SZ)"; mkdir -p "$backup"
  cp -a "$guard_file" "$backup/tool_guardrails.py"; cp -a "$config" "$backup/config.yaml"
  printf 'HERMES_TOOL_GUARD_FILE=%q\nHERMES_CONFIG=%q\nHERMES_GATEWAY_SERVICE=%q\n' "$guard_file" "$config" "$service" >"$backup/manifest.env"
  was=0; active && was=1 || true; systemctl --user stop "$service"
  trap 'cp -a "$backup/tool_guardrails.py" "$guard_file"; cp -a "$backup/config.yaml" "$config"; test "$was" = 1 && systemctl --user start "$service" || true' ERR
  patch
  "$python_bin" -m py_compile "$guard_file"
  cd "$agent_dir"
  if "$python_bin" -c 'import pytest' >/dev/null 2>&1; then
    "$python_bin" -m pytest -q tests/agent/test_tool_guardrails.py tests/run_agent/test_tool_call_guardrail_runtime.py
  else
    "$python_bin" - <<'PY'
from agent.tool_guardrails import ToolCallGuardrailConfig, ToolCallGuardrailController
cfg=ToolCallGuardrailConfig.from_mapping({
 "hard_stop_enabled":True,
 "hard_stop_after":{"idempotent_no_progress":3},
 "successful_no_progress_tools":["execute_code"],
 "max_total_calls_warn_after":20,
 "max_total_calls_second_warn_after":40,
 "max_total_calls_per_turn":60,
 "max_strategy_redirects_per_turn":60,
})
g=ToolCallGuardrailController(cfg)
args={"code":"print(1)"}
for _ in range(3):
 d=g.before_call("execute_code",args); assert d.allows_execution, d
 g.after_call("execute_code",args,'{"status":"success","output":"same"}',failed=False)
d=g.before_call("execute_code",args)
assert d.action=="redirect" and d.message=="换思路" and not d.should_halt,d
g=ToolCallGuardrailController(ToolCallGuardrailConfig.from_mapping({
 "hard_stop_enabled":True,"max_total_calls_per_turn":1,
 "max_strategy_redirects_per_turn":60,
}))
for index in range(60):
 assert g.before_call("execute_code",{"code":f"allowed-{index}"}).allows_execution
 d=g.before_call("execute_code",{"code":f"redirect-{index}"})
 assert d.action=="redirect" and d.message=="换思路" and not d.should_halt,d
assert g.before_call("execute_code",{"code":"final-allowed"}).allows_execution
d=g.before_call("execute_code",{"code":"hard-stop"})
assert d.should_halt and d.code=="total_tool_call_cap",d
print("tool_progress_smoke=ok")
PY
  fi
  test "$was" = 0 || systemctl --user start "$service"
  trap - ERR
  echo "installed backup=$backup";;
 verify)
  detect; grep -q successful_no_progress_tools "$guard_file" || die "patch absent"
  "$python_bin" -m py_compile "$guard_file"
  if active; then service_state=active; else service_state=inactive; fi
  printf 'service_state=%s\nverify=ok\n' "$service_state";;
 rollback)
  test -f "$backup_arg/manifest.env" || die "invalid backup"
  source "$backup_arg/manifest.env"
  restore_active="${SERVICE_WAS_ACTIVE:-}"
  if test -z "$restore_active"; then restore_active=0; active && restore_active=1 || true; fi
  systemctl --user stop "$HERMES_GATEWAY_SERVICE"
  cp -a "$backup_arg/tool_guardrails.py" "$HERMES_TOOL_GUARD_FILE"; cp -a "$backup_arg/config.yaml" "$HERMES_CONFIG"
  "$python_bin" -m py_compile "$HERMES_TOOL_GUARD_FILE"; test "$restore_active" = 0 || systemctl --user start "$HERMES_GATEWAY_SERVICE"
  echo rolled_back;;
 *) echo "usage: $0 {status|install [--dry-run]|verify|rollback --backup PATH}" >&2; exit 2;;
esac
