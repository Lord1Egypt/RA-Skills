# PRD: Formalize Independent Native Auditor for Pre-Flight PRD Review (ISSUE-1023)

## Context
Currently, when a Product Requirements Document (PRD) is generated, it immediately flows into the `orchestrator.py` SDLC pipeline where a Planner agent blindly slices it into coding tasks. If the PRD contains logical flaws, missing dependencies, architectural anti-patterns, or hallucinations (e.g., instructing an agent to perform actions that break the host system), these flaws are blindly propagated into the codebase. 

Historical attempts used hardcoded Bash scripts (`spawn_native_auditor.sh`, `run_independent_audit.sh`) that injected static code snippets (`cat`) into an LLM context. This "static injection" approach is brittle: if the PRD author forgets to declare a modified file, the auditor will never see it and miss the blast radius.
We need an intelligent, codebase-aware "Red Team" Auditor that autonomously searches the workspace to validate the PRD before any code is written.

## Requirements
1. **Agentic Auditor Script (`scripts/prd_auditor.sh`)**:
   - Create a robust, reusable bash script that takes a PRD file path as an argument.
   - The script must launch an independent OpenClaw Subagent (e.g., via `openclaw agent`) configured with a high-capability model.
   - The Auditor MUST be granted tools to explore the workspace (`exec`, `read`, etc. depending on the underlying agent runtime) so it is NOT limited to statically fed code.

2. **Ruthless System Prompt (The Red Team Persona)**:
   - The Auditor's prompt must explicitly instruct it to:
     1. Read the provided PRD.
     2. Autonomously explore the codebase using its tools to map the affected areas.
     3. Identify undocumented side effects, race conditions, architecture violations, or missing context.
     4. Fail the audit (`[REJECTED]`) with a detailed "Architectural Audit Report" if any flaws exist.
     5. Pass the audit by outputting the exact string `[LGTM]` if and only if the PRD is flawless.

3. **Orchestrator Integration (State 0 Pre-Flight Gate)**:
   - Modify `scripts/orchestrator.py` to enforce this audit at the very beginning of the pipeline (State 0, before `spawn_planner.py` is invoked).
   - If the auditor script does not return `[LGTM]`, the pipeline MUST halt immediately with a fatal exit code and notify the manager with the audit report.

## Framework Modifications
- `scripts/orchestrator.py`
- `scripts/prd_auditor.sh` (New File)

## Architecture
The new Pre-Flight Auditor acts as a zero-trust gateway. By decoupling the "Architect/PM" (who writes the PRD) from the "Auditor" (who tears it down), and by giving the Auditor autonomous workspace exploration capabilities, we prevent Confirmation Bias. The integration inside `orchestrator.py` ensures no un-audited PRD can ever trigger code changes.

## Acceptance Criteria
- [ ] A new script `scripts/prd_auditor.sh` exists and successfully invokes an OpenClaw agent to evaluate a given PRD.
- [ ] The Auditor agent autonomously reads workspace files (not just fed via `cat`).
- [ ] `orchestrator.py` halts execution if the Auditor outputs an error or rejection report.
- [ ] `orchestrator.py` proceeds to the Planner only if the Auditor explicitly outputs `[LGTM]`.