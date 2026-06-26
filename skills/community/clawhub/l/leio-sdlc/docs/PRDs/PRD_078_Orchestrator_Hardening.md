# PRD-078: Orchestrator Param Enforcement & Coder Session Strategy

## 1. Problem Statement
The SDLC `orchestrator.py` engine lacks strict input validation for the working directory, defaulting to the local directory. This violates the "CWD Guardrail" principle and leads to project context leakage. Furthermore, Coder sessions (LLM memory) are reused across rejection loops without an easy way for the operator to force a clean slate, leading to cognitive bias/path dependency in AI agents.

## 2. Objective
1.  Enforce explicit project selection by making `--workdir` mandatory.
2.  Provide an interface to configure Coder session lifecycle management.

## 3. Technical Requirements

### 3.1 CLI Argument Hardening
- Modify `orchestrator.py`:
  - Change `parser.add_argument("--workdir", default=".")` to `parser.add_argument("--workdir", required=True, help="Absolute path to the target project workspace")`.
  - Add `parser.add_argument("--coder-session-strategy", choices=["always", "per-pr", "on-escalation"], default="on-escalation")`.

### 3.2 Logic Implementation
- **Always**: Call `teardown_coder_session(workdir)` at the beginning of the `while True` loop in State 3 (just before calling `spawn_coder.py`).
- **Per-PR**: Call `teardown_coder_session(workdir)` once after `current_pr` is selected but before entering the inner retry loop.
- **On-Escalation**: Call `teardown_coder_session(workdir)` inside State 5 (3-Tier Escalation Protocol) before triggered resets or micro-slicing.

### 3.3 Definition of "3-Tier Escalation"
As established in the FSM logic:
- **State 5** is the 3-Tier Escalation Protocol.
- **Tier 1**: Branch Reset.
- **Tier 2**: Micro-slicing.
- **Tier 3**: DLQ (Manual Intervention).
"On-escalation" means the session is wiped as soon as State 5 is entered.

## 4. TDD & Acceptance Criteria
- Running `python3 scripts/orchestrator.py --prd-file ...` without `--workdir` must exit with a CLI usage error.
- Verify through logs/mock-calls that `teardown_coder_session` is called at the correct timestamps according to the selected strategy.
- Existing E2E tests in `leio-sdlc/preflight.sh` must be updated to include `--workdir "$(pwd)"`.
