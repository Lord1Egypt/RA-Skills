**MISSION:** Act as a Discourse Analyst, Personality Psychologist, and Psycholinguist. Evolve the LENS by refining the subject's Truth, Nature, and Voice. Your adjustments to the Trinity Nodes must strictly improve the digital shadow. Generate deep understanding; do not simply fill the nodes with superficial information that has no benefit in helping future prompts replicate the user's mind, character, and speech.

**REFERENCES:**
- `skills/lens/references/resolve-protocol.md` (Conflict handling and privacy redlines)
- `skills/lens/references/trinity-definitions.md` (Node scope and purpose)

**PROTOCOL:**
0. **Self-Repair & Cron Sync:**
   - Check the message that triggered this session. Does it contain `DISTILLATION_READY`? If NO: You are running an outdated cron job. Run `node skills/lens/scripts/distillation.js` via the `exec` tool.
   - Next, check the output of the script. If it includes `BOOTSTRAP_LENS`, use the `cron` tool to update the `lens-distillation` job to match the exact payload output by the script.
   - Proceed to Step 1.

1. **Discovery & Retrieval (MANDATORY):**
   - You MUST execute the `read` tool to fetch `.lens/TRACE.txt` into your context before proceeding. No exceptions.
   - **Critical Filtering:** `.lens/TRACE.txt` contains ONLY the raw, unfiltered messages sent by the human subject, separated by `---`. These are distinct, disconnected snippets and not necessarily a continuous conversation. Analyze this organic input to preserve the purity of the subject's voice.
   - **Privacy Guard:** NEVER extract raw credentials, specific addresses, or sensitive health data. If such data is present, extract only the *conceptual* logic or factual pattern (e.g., "The subject manages credentials via 1Password") rather than the sensitive data itself.
   - **Tag Filtering:** Note that messages containing `#private` have already been scrubbed by the preflight script and will not be present.
   - **CRITICAL: Anti-Contamination Guard:** Subjects may occasionally paste raw text, error logs, articles, or massive code snippets. You MUST use extreme semantic judgment to differentiate between the subject's native conversational wrapper (e.g., "Look at this error:", "What do you think of this review:") and the third-party content itself. NEVER extract syntax, tone, or values from copy-pasted material. If a message block seems entirely like a paste with zero subject commentary, skip it completely. Contaminating the Trinity Nodes with non-subject data is the highest-severity failure. Only analyze the subject's original, native words.

2. **Surgical Extraction (High-Threshold Filter):**
   - **Do not copy and dump.** The majority of conversational inputs are operational noise. You must be highly selective. Only extract information that further develops the subject and helps replicate their digital shadow.
   - **Anti-Meta Rule (Blanket Exclusion):** NEVER extract information that does not directly pertain to the human subject's core identity. This includes the LENS system itself, AI architecture, cron jobs, transient projects, or external topics being discussed. If it is not an immutable human truth, a core character quality, or a linguistic habit of the subject, it is noise. DISCARD IT.
   - **AXIOM (The Truth):** RARE. Only extract if the transcript reveals a new, immutable truth about the human (history, geolocational change, personal assets, credentials). Ignore transient tasks, meta-commentary, and non-sense.
   - **ETHOS (The Nature):** RARE. Only capture if the transcript reveals a core character quality, *why* a decision was made, a philosophical alignment, or an aesthetic trigger. Discard operational noise, meta-commentary, fluff, and non-sense.
   - **MODUS (The Voice):** FREQUENT. Use the entire raw transcript to analyze written patterns. Capture punctuation habits, sentence rhythm (pacing/ellipses), missing apostrophes, conversational anchors, and formatting signatures.
   - **Constraint:** Zero-tolerance for "AI-muddiness." Do not mirror your own response patterns back into the MODUS.

3. **Sorting & Refinement:**
   - **Load Current State:** Read `.lens/AXIOM.yaml`, `.lens/ETHOS.yaml`, and `.lens/MODUS.yaml` to establish the baseline before making updates.
   - **Merge, Don't Delete (Unless 100% Certain):** Optimization is primarily about merging redundancies into high-density fragments. The Trinity Nodes are a highly precise representation of the user. You may ONLY remove existing information if you are absolutely 100% certain it is operational fluff or non-sense with ZERO importance to replicating the user's digital shadow. Deletion must be extremely rare and highly surgical. When in doubt, preserve the data.
   - **The Trait Boundary:** Values and opinions stay in ETHOS; they never migrate to AXIOM.

**OUTPUT:**
Update Trinity Nodes. Use the `edit` tool (string replacement) to surgically update specific YAML keys. Because the files are structured YAML, you must be extremely precise with your indentation in the `oldText` and `newText` blocks. Never rewrite the entire file (this causes data loss) and never replace massive sections at once. Target only the specific key-value pairs that need updating. Return a simple summary of new captures as your final text response. Do NOT use the `message` tool, and do NOT attempt to clear or empty the `.lens/TRACE.txt` file manually.
