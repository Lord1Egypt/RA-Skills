---
name: hermes-continuation-maintainer
description: Diagnose and repair Hermes Agent runs that silently stop and require manual "continue" messages even though no user input is needed. Use this skill when Hermes does not keep working, appears to think without acting, repeatedly waits after short status text, or when asked to scan Hermes logs for premature continuation stalls and patch the control loop.
---

# Hermes Continuation Maintainer

Use this skill for one narrow failure mode: Hermes ends a turn after a short non-final work-status message instead of continuing with tool calls.

The usual root cause is control-loop classification, not machine slowness:

- The provider returns visible assistant text with `finish_reason=stop`.
- The text says what Hermes will do next, but it is not a final answer and does not ask the user for input.
- The conversation loop treats that stop as terminal, so Hermes waits silently.
- A later user "continue" message proves the previous stop was premature.

## Use The Scanner First

Run the bundled scanner from the Hermes WSL distro:

```bash
python3 <skill_dir>/scripts/scan_hermes_continuation.py --since-minutes 360 --format text
```

Default paths used by the scanner:

- log: `/root/.hermes/logs/agent.log`
- state DB: `/root/.hermes/state.db`

The scanner emits deterministic classifications:

- `continuation_candidate`: likely premature stop; patch or extend tests.
- `asks_user`: valid stop; do not auto-continue.
- `final_or_summary`: valid completion or summary; do not patch.
- `review`: inspect manually before changing code.

## Patch Policy

Patch only after the scanner finds concrete phrase families in recent logs. Keep the change local and regression-tested.

Known Hermes files:

- `/usr/local/lib/hermes-agent/agent/agent_runtime_helpers.py`
- `/usr/local/lib/hermes-agent/agent/conversation_loop.py`
- `/usr/local/lib/hermes-agent/run_agent.py`
- `/usr/local/lib/hermes-agent/tests/run_agent/test_run_agent.py`

The continuation heuristic should require all of these:

- an execution-oriented recent user prompt, previous tool activity, or a known continuation context;
- a short assistant text stop with future-action language;
- an action term such as read, inspect, run, test, execute, update, write, patch, fix, implement, or verify.

The heuristic must reject:

- questions or clarification requests;
- text that asks the user to provide information;
- true final answers such as done, completed, finished, or all tests passed;
- long summaries.

## Minimum Regression Checks

Run focused tests before reporting success:

```bash
cd /usr/local/lib/hermes-agent
PYTHONDONTWRITEBYTECODE=1 venv/bin/python -m pytest -q \
  tests/run_agent/test_run_agent.py::test_run_conversation_continues_after_nonfinal_work_status_after_tools \
  tests/run_agent/test_run_agent.py::test_run_conversation_continues_after_chinese_future_action_status \
  tests/run_agent/test_run_agent.py::test_run_conversation_does_not_continue_when_status_requests_user_input

PYTHONDONTWRITEBYTECODE=1 venv/bin/python -m pytest -q \
  tests/run_agent/test_run_agent_codex_responses.py::test_run_conversation_codex_continues_after_ack_stop_message \
  tests/run_agent/test_run_agent_codex_responses.py::test_run_conversation_codex_continues_after_ack_for_directory_listing_prompt

PYTHONDONTWRITEBYTECODE=1 venv/bin/python -m py_compile \
  agent/agent_runtime_helpers.py agent/conversation_loop.py run_agent.py tests/run_agent/test_run_agent.py
```

## Runtime Handling

Code edits do not hot-load into already-running interactive Hermes CLI processes. Tell the user to exit and reopen stale CLI sessions. Do not kill interactive Hermes CLI processes unless explicitly asked.

Gateway and Dashboard can be restarted separately if they are down, but that is a different problem from continuation stalls.

## Report Format

Keep the report short:

- root cause;
- scanner counts and phrase families found;
- files changed;
- tests run;
- whether an old CLI process still needs restart.
