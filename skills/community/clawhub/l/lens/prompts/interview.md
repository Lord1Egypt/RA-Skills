Read `~/.lens/AXIOM.yaml`, `~/.lens/ETHOS.yaml`, `~/.lens/MODUS.yaml`, and `~/.lens/SCOPE.json`. If `~/.lens/TRACE.txt` is non-empty, read it for recent context.

**OBJECTIVE:** Calibrate the subject's Trinity Nodes (`AXIOM`, `ETHOS`, `MODUS`) by asking ONE concrete scenario or trade-off question that elicits both decision logic (`ETHOS`) and natural phrasing (`MODUS`).

**PROTOCOL:**
0. **Preflight & Schedule Sync:**
   - If the trigger message lacks `INTERVIEW_READY`, run `node` on [scripts/interview.js](../scripts/interview.js) from the skill directory (outside the workspace sandbox if needed to access `~/.lens/`) to decrement the question counter and sync `~/.lens/SCOPE.json`.
   - If stdout contains `BOOTSTRAP_LENS` and the `cron` tool is available, register or update any job in `jobs`, remove any job listed in `removeJobs` via the `cron` tool, and note in your response when recurring schedules are first registered or updated.

1. **Target Selection:** Identify an uncalibrated `[Pending Input]` placeholder or under-defined key in `~/.lens/AXIOM.yaml`, `~/.lens/ETHOS.yaml`, or `~/.lens/MODUS.yaml`.
2. **Phase Targeting (`~/.lens/SCOPE.json` -> `interview.phase`):**
   - **`onboarding`:** Target foundational facts (`AXIOM`) and core operational preferences. On the very first onboarding question (`questions: 14` after decrement, or all nodes uncalibrated), prefix briefly: *"I've activated your LENS in `~/.lens/` (configured for calibration questions and nightly session distillation per `~/.lens/SCOPE.json`) so I can learn how you think and write as we work together. Let's start with a quick one: [Question]"*
   - **`stabilizing`:** Target `ETHOS` trade-off rules (`decision_heuristics`, `conflict_protocol`, `quality_standards`) via a realistic "X vs. Y" dilemma.
   - **`habitual`:** Target nuanced edge cases, aesthetic/taste distinctions, or how the subject would phrase a response to a specific scenario (`ETHOS` + `MODUS`).
3. **Question Formulation:** Draft **ONE** specific question (1-2 sentences maximum). Never ask abstract self-report questions; always frame a concrete scenario, trade-off, or forced choice:
   - *Invalid (Abstract):* "How do you handle conflict or disagreements on a team?"
   - *Valid (Concrete Trade-Off):* "If a collaborator ships code that works but violates your structural standards right before a deadline, do you merge it and clean it up later or block it on the spot?"
4. **Delivery:** Output the question directly in a natural, conversational tone calibrated to `~/.lens/MODUS.yaml` (direct, zero servility, no bullet points).

**EXECUTION CONSTRAINTS:**
- **Question Turn (Read-Only on YAML):** Stop immediately after outputting the single question. Do not modify `~/.lens/AXIOM.yaml`, `~/.lens/ETHOS.yaml`, or `~/.lens/MODUS.yaml` during the question turn, do not simulate a reply, and do not call any external `message` tool.
- **Reply Turn (Distillation):** When the user replies in the next turn, extract their decision logic (`AXIOM`/`ETHOS`) and phrasing (`MODUS`) directly from their live reply into `~/.lens/AXIOM.yaml`, `~/.lens/ETHOS.yaml`, and `~/.lens/MODUS.yaml` per [prompts/distillation.md](./distillation.md) (skipping Step 0 `TRACE.txt` harvesting).
