# PRD: Formalize Independent Native Auditor for Pre-Flight PRD Review (ISSUE-1023 v2)

## Context
Currently, when a Product Requirements Document (PRD) is generated, it flows into the `orchestrator.py` SDLC pipeline where a Planner agent slices it into coding tasks. If the PRD contains logical flaws, missing dependencies, architectural anti-patterns, or hallucinations, these flaws blindly propagate into the codebase. 

An initial attempt to integrate a PRD Auditor into the `orchestrator.py` pipeline (via a Bash CLI wrapper) failed during architectural review due to three fatal flaws:
1. **Governance Violation**: Mixing PRD validation with code execution breaks the PM-SDLC physical decoupling. The SDLC pipeline (`orchestrator.py`) must remain a stateless execution engine.
2. **CLI Limitations**: A simple bash script wrapping a CLI command only supports single-turn interactions. True codebase-aware auditing requires a multi-turn, autonomous agent loop.
3. **Brittle Parsing**: Relying on exact string matches (e.g., `[LGTM]`) from an LLM is error-prone.

We need an independent, autonomous "Red Team" Auditor Python script (`spawn_auditor.py`) that the Manager explicitly invokes as a Pre-Flight check *before* handing the PRD to the Orchestrator.

## Requirements
1. **Autonomous Auditor Script (`scripts/spawn_auditor.py`)**:
   - Create a new Python script that mirrors the robust, multi-turn architecture of `spawn_coder.py`.
   - It must instantiate an autonomous OpenClaw Subagent (using `openclaw sessions spawn` or equivalent agent loop API) configured with a high-capability model.
   - The Auditor MUST have tool access to explore the workspace (`read`, `find`, `exec`, etc.) to trace the full blast radius of the PRD changes.

2. **Ruthless System Prompt (The Red Team Persona)**:
   - The Auditor's prompt must explicitly instruct it to:
     1. Read the provided PRD.
     2. Autonomously explore the target codebase using tools to map affected areas.
     3. Identify undocumented side effects, race conditions, architecture violations, or missing context.

3. **Structured JSON Output Contract**:
   - The Auditor MUST output its final verdict as a structured JSON object strictly matching this format:
     ```json
     {
       "status": "APPROVED", // or "REJECTED"
       "comments": "Detailed explanation of flaws or justification for approval."
     }
     ```

4. **Integration boundary**:
   - The Auditor is a strictly **Pre-Flight** tool invoked by the Human/Manager. It will NOT be executed by `orchestrator.py`. `orchestrator.py` will remain unmodified for this feature.

5. **Governance Constitution Update**:
   - The global governance file at `/root/.openclaw/workspace/projects/docs/TEMPLATES/organization_governance.md` currently contains outdated references to the brittle `[LGTM]` string check for both the "Pre-Flight PRD Audit" (Section 2) and the "Reviewer Gate" (Section 4.1). 
   - Update `organization_governance.md` to reflect that the SDLC pipeline (`orchestrator.py`) *already* uses a structured JSON output contract (`{"status": "APPROVED"}`) for Code Review, and that the new Pre-Flight PRD Audit stage will now adopt this exact same JSON contract standard.

## Framework Modifications
- `scripts/spawn_auditor.py` (New File)
- `/root/.openclaw/workspace/projects/docs/TEMPLATES/organization_governance.md` (Global Constitution)

## Architecture
The new Pre-Flight Auditor acts as a zero-trust gateway. By decoupling the "Architect/PM" (who writes the PRD) from the "Auditor" (who tests it against reality), we prevent Confirmation Bias. The implementation strictly uses a standalone Python script to handle robust multi-turn tool calling and structured JSON parsing, avoiding the brittleness of single-turn Bash wrappers.

## Acceptance Criteria
- [ ] A new script `scripts/spawn_auditor.py` exists and correctly runs a multi-turn agent loop.
- [ ] The Auditor agent can autonomously explore workspace files before deciding.
- [ ] The output of `spawn_auditor.py` is guaranteed to be a structured JSON object.
- [ ] `orchestrator.py` is NOT modified, preserving SDLC engine statelessness.