---
name: lens
description: "Personal identity engine (The Trinity Nodes in ~/.lens/: AXIOM, ETHOS, MODUS) for thinking, writing, speaking, evaluating, and deciding in the user's voice across Google Antigravity, OpenClaw, Claude Code, and OpenAI Codex CLI. Calibrates and evolves ~/.lens/ via scheduled trade-off interviews, nightly transcript distillation across local agent sessions, and optional Git sync. In chat, activate only when the user explicitly asks to use, focus, distill, or update their LENS, or asks you to think, write, speak, or evaluate like them; do not activate for routine coding or general tasks."
permissions:
  - env
  - filesystem
  - process
  - cron
  - network
metadata:
  {
    "openclaw": {
      "emoji": "🧐",
      "requires": {
        "bins": ["node", "git"],
        "files": ["~/.lens/AXIOM.yaml", "~/.lens/ETHOS.yaml", "~/.lens/MODUS.yaml", "~/.lens/SCOPE.json", "~/.lens/TRACE.txt", "~/.openclaw/openclaw.json", "~/.openclaw/cron/jobs.json", "~/.openclaw/agents/main/agent/openclaw-agent.sqlite", "~/.openclaw/agents/main/sessions/*.jsonl"],
        "env": ["HOME", "CODEX_HOME", "OPENCLAW_CRON_LIST"]
      }
    }
  }
---

# LENS

LENS models a singular human subject through **The Trinity Nodes** stored in `~/.lens/`:

1. **`~/.lens/AXIOM.yaml` (The Truth / What):** Objective facts, biography, relationships, hardware, stack, and active projects (silent situational context).
2. **`~/.lens/ETHOS.yaml` (The Nature / Who):** Values, mental models, conditional `decision_heuristics`, risk boundaries, conflict protocol, and quality standards (decision engine).
3. **`~/.lens/MODUS.yaml` (The Voice / How):** `voice_anchors`, `contextual_registers`, syntax, cadence, punctuation rhythm, and humor rules (linguistic interface).

## 1. Initialization & Schedule Sync (First Run)

1. **Bootstrap `~/.lens/` & Skill Links:** If `~/.lens/` or any Trinity Node (`~/.lens/AXIOM.yaml`, `~/.lens/ETHOS.yaml`, `~/.lens/MODUS.yaml`) is missing, **or** if the OpenClaw `cron` tool is available and an enabled `"openclaw"` runner job (`distillation.runner` or `interview.runner` in `~/.lens/SCOPE.json`) is missing from `OPENCLAW_CRON_LIST`, run `node` on [scripts/bootstrap.js](./scripts/bootstrap.js) from this skill directory (outside the workspace sandbox if needed to access `~/.lens/`).
2. **Sync Scheduled Jobs & Inform User:**
   - **OpenClaw (`cron` tool available):** Whenever the bootstrap or preflight output includes `BOOTSTRAP_LENS`, register or update any job present in `jobs` (`lens-distillation` when `distillation.runner` is `"openclaw"`, `lens-interview` when `interview.runner` is `"openclaw"`), remove any job listed in `removeJobs` from the `cron` tool, and inform the user when recurring schedules are registered or updated (or that they can change `runner` to `"none"` in `~/.lens/SCOPE.json` to disable scheduling).
   - **Google Antigravity:** When `distillation.runner` or `interview.runner` in `~/.lens/SCOPE.json` is `"antigravity"`, the bootstrap step configures the `lens-distillation` and `lens-interview` background automations for Google Antigravity. On initial setup, inform the user they can review and enable them in `[Open Automations Dashboard](sidecar://dashboard)`.
   - **Terminal CLIs (Claude Code, OpenAI Codex CLI):** Foreground CLIs have no persistent background daemon; their session transcripts are harvested overnight when enabled in `~/.lens/SCOPE.json` (`distillation.sources`) if OpenClaw or Antigravity runs on the same machine, or evolved on demand via *"Distill my LENS"* / *"Focus my LENS"*.
3. **First-Run Calibration:** If `BOOTSTRAP_LENS` outputs `"triggerImmediate": "lens-interview"` (or if all three Trinity Nodes in `~/.lens/` contain only `[Pending Input]` placeholders on first activation and `interview.runner` is not `"none"`), immediately run `node` on [scripts/interview.js](./scripts/interview.js) and execute [prompts/interview.md](./prompts/interview.md).

## 2. Three-Pass Cognitive Pipeline (Using LENS)

When asked to think, evaluate, decide, write, or speak through the user's LENS, execute these passes in sequence:

1. **Load & Filter `~/.lens/` (Mandatory):**
   - Read `~/.lens/AXIOM.yaml`, `~/.lens/ETHOS.yaml`, and `~/.lens/MODUS.yaml`, plus [alignment-scales.md](./references/alignment-scales.md), [resolve-protocol.md](./references/resolve-protocol.md), and [trinity-definitions.md](./references/trinity-definitions.md).
   - **Ignore Uncalibrated Placeholders:** Disregard any entry containing `[Pending Input]` and its parenthetical `(e.g., ...)` examples.
2. **Pass 1: Situational Grounding (`~/.lens/AXIOM.yaml`):**
   - Hold `~/.lens/AXIOM.yaml` as silent background context.
   - **Relevance Gate:** Surface an `AXIOM` fact only when directly required by the task. Never inject unrelated biographical trivia, hardware specs, or project names.
   - **Exfiltration Guard:** Never expose redlined `AXIOM` data (biometrics, exact street addresses, private financial details, medical context) in external or public-facing drafts per [resolve-protocol.md](./references/resolve-protocol.md).
3. **Pass 2: Judgment & Trade-Off Synthesis (`~/.lens/ETHOS.yaml`):**
   - Determine the subject's substantive position before drafting prose using `~/.lens/ETHOS.yaml` (`philosophical_framework`, `hard_boundaries_and_risk_tolerance`, `conflict_protocol`, `quality_standards`) and [alignment-scales.md](./references/alignment-scales.md).
   - Apply matching `decision_heuristics`, enforce `quality_standards` and `core_aversions`, score alignment on the 6-8-10 scale, and apply `conflict_protocol` for pushback. Never default to generic AI neutrality or merely echo hasty prompt phrasing.
4. **Pass 3: Voice & Register Rendering (`~/.lens/MODUS.yaml`):**
   - Select the target register in `MODUS.contextual_registers` (`collaborative_and_peer`, `architectural_and_critique`, `public_and_longform`, or `external_and_diplomatic`).
   - Render the `ETHOS` judgment using the sentence length, punctuation rhythm, grammar, and tone temperature defined in `~/.lens/MODUS.yaml`.
   - **Anti-Caricature Rule:** Use `voice_anchors` and `linguistic_markers` strictly to calibrate rhythm and vocabulary; never parrot `voice_anchors` verbatim or force stock openers.
   - **Zero AI Formatting Slop:** Omit unrequested bulleted lists, em-dashes, corporate throat-clearing, hedge words, and servile sign-offs.
   - **Output Mode:** For evaluation prompts (*"What would I think about X?"*), output a candid analysis in the subject's voice. For drafting prompts (*"Write/reply as me"*), output only the finished first-person text without meta-commentary.

## 3. On-Demand Evolution Commands

- **Direct Update (*"Add to my LENS..."*):** Surgically update the target key in `~/.lens/AXIOM.yaml`, `~/.lens/ETHOS.yaml`, or `~/.lens/MODUS.yaml` per [resolve-protocol.md](./references/resolve-protocol.md) and [trinity-definitions.md](./references/trinity-definitions.md), then run `node` on the distillation script below with `--commit` from this skill directory to commit changes locally if `~/.lens/` is a Git repository (pushing to the remote only when `"push": true` in `~/.lens/SCOPE.json`).
- **Calibration Interview (*"Focus my LENS"* / *"Ask me a LENS question"*):** Execute [prompts/interview.md](./prompts/interview.md) to ask one scenario or trade-off question. On the user's reply turn, distill their decision logic and phrasing directly from their live reply into `~/.lens/AXIOM.yaml`, `~/.lens/ETHOS.yaml`, and `~/.lens/MODUS.yaml` per [prompts/distillation.md](./prompts/distillation.md) (skipping Step 0 `TRACE.txt` harvesting).
- **Session Distillation (*"Distill my LENS"*):** Run `node` on [scripts/distillation.js](./scripts/distillation.js) from this skill directory (outside the workspace sandbox if needed to read enabled agent session logs per `~/.lens/SCOPE.json` and populate `~/.lens/TRACE.txt`), then execute [prompts/distillation.md](./prompts/distillation.md).
