# PRD_046: Reviewer Physical Artifact Enforcement & Template Injection

## 1. Problem Statement
The Reviewer agent frequently evaluates code and outputs its decision (`[LGTM]` or `[ACTION_REQUIRED]`) directly in the chat interface. It fails to write these decisions to the required physical artifact (`review_report.txt`). Because the `merge_code.py` script depends entirely on this physical file, the pipeline halts, requiring human operators to manually forge the report to unblock the merge.

## 2. Solution
Enforce strict physical file generation by injecting a rigid Markdown template into the Reviewer's prompt and implementing a fail-fast Python guardrail that guarantees the file's existence upon completion.

### 2.1 Template Creation
Create a new file: `TEMPLATES/Review_Report.md.template`.
**Content Requirements**:
- A clear checkbox or header for the final verdict: `[LGTM]` or `[ACTION_REQUIRED]`.
- A structured section for "Feedback & Action Items" (if rejection occurs).
- A structured section for "Security & Redline Checks" (e.g., CWD isolation, Test passage).

### 2.2 Prompt Upgrade (`scripts/spawn_reviewer.py`)
1. Read the `Review_Report.md.template` from the `TEMPLATES` directory.
2. Inject it into the `task_string` of the `openclaw agent` call.
3. Add a **CRITICAL DIRECTIVE** in all caps:
   `"You MUST use the \`write\` tool to save your final evaluation into exactly '{workdir}/review_report.txt' using the provided template. DO NOT just print the evaluation in the chat."`

### 2.3 Python Guardrail (Fail-Fast)
Immediately after the `subprocess.run(["openclaw", "agent", ...])` completes in `scripts/spawn_reviewer.py`:
1. Check if `{workdir}/review_report.txt` exists.
2. If it does NOT exist, print a fatal error to `stderr`:
   `[FATAL] The Reviewer agent failed to generate the physical 'review_report.txt'. This is a severe process violation.`
3. Exit the script with code `1`. (This will allow future Orchestrator scripts to detect the failure and retry the Reviewer).

## 3. Testing Strategy (TDD)
Update `scripts/test_triad_reviewer.sh` or create a new test `scripts/test_reviewer_artifact_guardrail.sh`.

- **Scenario 1: Agent Fails to Write File (Mock Mode)**
  - Configure the mock Reviewer to exit `0` but purposely *not* create `review_report.txt`.
  - **Assert**: `spawn_reviewer.py` must exit with `1` and output the `[FATAL]` missing artifact message.
- **Scenario 2: Agent Writes File Successfully (Mock Mode)**
  - Configure the mock Reviewer to touch `review_report.txt` and exit `0`.
  - **Assert**: `spawn_reviewer.py` must exit with `0`.

## 4. Acceptance Criteria
- [ ] `Review_Report.md.template` exists in `TEMPLATES/`.
- [ ] `spawn_reviewer.py` successfully injects the template.
- [ ] `spawn_reviewer.py` reliably crashes (`exit 1`) if the file is missing after execution.
- [ ] `./preflight.sh` passes with the new/updated tests.