**OBJECTIVE:** Distill enduring factual truths (`AXIOM`), decision heuristics (`ETHOS`), and linguistic mechanics (`MODUS`) from `~/.lens/TRACE.txt` (or directly from the user's live reply turn following a calibration interview question) into `~/.lens/AXIOM.yaml`, `~/.lens/ETHOS.yaml`, and `~/.lens/MODUS.yaml`.

**REFERENCES:**
- [references/resolve-protocol.md](../references/resolve-protocol.md) (Conflict resolution, privacy redlines, specificity preservation)
- [references/trinity-definitions.md](../references/trinity-definitions.md) (Node schemas and trait boundaries)

**PROTOCOL:**
0. **Preflight & Schedule Sync (Session / Scheduled Distillation Only):**
   - Skip Step 0 when distilling a direct in-chat reply turn to a calibration interview question.
   - Otherwise, if `~/.lens/TRACE.txt` was not refreshed for this run (or the trigger message lacks `DISTILLATION_READY`), run `node` on [scripts/distillation.js](../scripts/distillation.js) from the skill directory (outside the workspace sandbox if needed to access `~/.lens/` and enabled agent session logs per `~/.lens/SCOPE.json`).
   - If stdout contains `BOOTSTRAP_LENS` and the `cron` tool is available, register or update any job in `jobs`, remove any job listed in `removeJobs` via the `cron` tool, and note in your final response that the recurring distillation and interview schedules were synced.
   - If stdout contains `TRACE_EMPTY`, stop immediately without modifying any files.

1. **Source Filtering (`~/.lens/TRACE.txt` or Live Interview Reply):**
   - Read `~/.lens/TRACE.txt` (where entries separated by `---` are independent raw user messages harvested across sessions), or evaluate the user's live in-chat reply to a calibration interview question.
   - **Privacy Filter:** Never extract raw credentials, account numbers, exact street addresses, or sensitive medical identifiers. Record only high-level operational patterns (e.g., "Manages secrets via 1Password").
   - **Anti-Contamination Filter:** Strictly separate the user's own words from pasted articles, logs, third-party emails, or code. Never extract values or phrasing from third-party text.
   - **Anti-Bot-Command Filter:** Ignore rapid operational commands directed at AI tools ("Fix this bug", "Run the build") and accidental keyboard typos. Never record AI-commanding syntax or typos as the subject's human-to-human voice (`MODUS`).

2. **Portability Gate & Node Extraction:**
   - **Portability Test:** Retain a signal only if it would remain true if the subject switched projects, repositories, or servers tomorrow. Discard transient task instructions, cron tweaks, and meta-discussions about LENS.
   - **`~/.lens/AXIOM.yaml` (The Truth / What):** RARE. Extract only enduring objective facts (biography, kinship, core hardware/software stack, career history, major personal projects, domestic context).
   - **`~/.lens/ETHOS.yaml` (The Nature / Who):** RARE. Extract transferable mental models, conditional trade-off rules (`when X conflicts with Y, prioritize X`), hard boundaries, conflict resolution habits, cultural taste logic, and quality standards.
   - **`~/.lens/MODUS.yaml` (The Voice / How):** Extract sentence rhythm, punctuation habits, `contextual_registers` (`collaborative_and_peer`, `architectural_and_critique`, `public_and_longform`, `external_and_diplomatic`), rhetorical pacing, humor triggers, and 1-2 sentence verbatim `voice_anchors` demonstrating the subject's sharpest natural writing. Never copy assistant phrasing into `~/.lens/MODUS.yaml`.

3. **Schema Integrity & Surgical Update:**
   - Read `~/.lens/AXIOM.yaml`, `~/.lens/ETHOS.yaml`, and `~/.lens/MODUS.yaml`.
   - **Canonical Schema Enforcement:** Write only to canonical keys defined in [references/trinity-definitions.md](../references/trinity-definitions.md) and the node templates ([AXIOM.yaml](../scripts/templates/AXIOM.yaml), [ETHOS.yaml](../scripts/templates/ETHOS.yaml), and [MODUS.yaml](../scripts/templates/MODUS.yaml)). If a file contains legacy v1 keys (`data_heritage`, `cultural_consumption`, or missing `decision_heuristics` / `contextual_registers` / `voice_anchors`), losslessly migrate calibrated entries into the canonical v2 schema. Replace `[Pending Input]` strings in place when populating a key; never leave `[Pending Input]` alongside real entries in the same list, and never invent new top-level keys.
   - **Specificity Preservation:** Never compress sharp, concrete entries into vague platitudes. Modify an already-calibrated key only when `~/.lens/TRACE.txt` (or the live interview reply) supplies new facts, a sharper trade-off heuristic, or a direct contradiction per [references/resolve-protocol.md](../references/resolve-protocol.md).

**OUTPUT:**
Surgically update `~/.lens/AXIOM.yaml`, `~/.lens/ETHOS.yaml`, and `~/.lens/MODUS.yaml` with exact YAML indentation and a single trailing newline. Once finished, run `node` on the Step 0 distillation script with `--commit` from the skill directory (outside the workspace sandbox if needed) to commit distilled node changes (`~/.lens/AXIOM.yaml`, `~/.lens/ETHOS.yaml`, `~/.lens/MODUS.yaml`, `~/.lens/SCOPE.json`, `~/.lens/README.md`, `~/.lens/.gitignore`) locally if `~/.lens/` is a Git repository (pushing to the remote only when `"push": true` in `~/.lens/SCOPE.json`). Return a concise summary of updated keys (plus any schedule changes synced from `BOOTSTRAP_LENS`) as your final text response. Do NOT call any external `message` tool, and do NOT clear `~/.lens/TRACE.txt`.
