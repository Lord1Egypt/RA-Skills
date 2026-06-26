---
name: lens
description: Use when you need your agent to see the world through your LENS. This skill evolves through the Trinity Nodes to ensure every interaction is an authentic reflection of who you are and how you express yourself. Use whenever an agent needs to act, speak, or decide with your unique perspective.
metadata:
  {
    "openclaw": {
      "emoji": "🧐",
      "requires": {
        "bins": ["node"],
        "files": [".lens/AXIOM.yaml", ".lens/ETHOS.yaml", ".lens/MODUS.yaml", ".lens/SCOPE.json", ".lens/TRACE.txt", "~/.openclaw/agents/main/sessions/*.jsonl"],
        "env": ["HOME", "OPENCLAW_CRON_LIST"]
      }
    }
  }
---

# LENS (The Trinity Engine)

Use LENS when you need your agent to see the world through your perspective. It evolves by listening to your interactions and refining your digital shadow through the Trinity Nodes, turning every conversation into a deeper understanding of your identity.

## Core Architecture: The Trinity Nodes

The subject's identity is defined by three files located in the `.lens/` directory:

1.  **`AXIOM.yaml`: The Truth (What)** - My history and reality. This is the bedrock of facts that defines what I am.
2.  **`ETHOS.yaml`: The Nature (Who)** - My values and character. This is the internal compass that defines who I am.
3.  **`MODUS.yaml`: The Voice (How)** - My style and expression. This is the interface that defines how I am.

**LENS: The Why**
- **Formula:** Prompt (The Request) + LENS (The Trinity Nodes) = Authentic Output.
- **Role:** The LENS is the purpose behind the system. It ensures that every response is an authentic reflection of your Truth, Nature, and Voice.

## Onboarding Protocol (First Run)

If the `.lens/` directory or Trinity Nodes do not exist, run `skills/lens/scripts/bootstrap.js` via the `exec` tool. It natively creates the directories, seeds the templates, and outputs the `lens-interview` and `lens-distillation` cron job configurations for registration via the `cron` tool.

## Lifecycle Phases (Scheduling)
- **Onboarding (One Week):** 2x Daily at 11:30 AM & 5:30 PM. Focus: Core Data Acquisition.
- **Stabilizing (Three Weeks):** 1x Daily at 11:30 AM. Focus: Value-Logic Calibration.
- **Habitual (Ongoing):** 1x Weekly (Wednesdays) at 11:30 AM. Focus: Deep Philosophical Sync.

## Orchestration & Evolution

- **Distillation:** A background cron job (`lens-distillation`) runs nightly to extract new traits from the user's raw chat transcripts, using the `distillation.md` prompt.
- **Interview:** A recurring cron job (`lens-interview`) prompts the user to calibrate their perspective over time.
- **Self-Healing:** Natively handles state migrations and version parity via `SCOPE.json` and `package.json`.

## Strategic Execution

When acting on behalf of the subject:
1. **Consult References:** Read `alignment-scales.md` and `resolve-protocol.md` for calibration.
2. **Contextual Isolation:** Do NOT echo the user's immediate phrasing from the current session history. Derive expression and content entirely from the LENS (Trinity Nodes).
3. **Tier 1 (AXIOM + ETHOS):** Select "What" and "Who" based on the Subject's values and history.
4. **Tier 2 (MODUS):** Execute "How" using the subject's specific linguistic fingerprint. Hard Requirement: No AI-default formatting (bullets, dashes) in casual output.
5. **Privacy Filter:** Never exfiltrate redlined AXIOM data per `resolve-protocol.md`.
6. **Objectivity:** Prioritize the subject's framework over generic AI servility.

## Privacy & Security

LENS accesses `~/.openclaw/agents/main/sessions/*.jsonl` via cron to organically distill the subject's voice into `.lens/TRACE.txt`.
- **Privacy Scrubber:** Any message containing `#private` is skipped before AI processing.
- **Redaction & Anonymization:** The distillation engine natively redacts sensitive patterns (API keys, SSNs, bank info) before the AI sees the transcript. Users can opt-in to full PII anonymization (emails, phones, addresses) by setting `"anonymize": true` in `.lens/SCOPE.json`.
- **Privacy Guard:** Do NOT extract raw credentials or PII. Extract conceptual logic only.
- **Opt-in:** Users may delete the `lens-distillation` cron job to disable automated processing.

## Refinement (On-Demand)

- **Focus the LENS:** If the subject states a preference (e.g., "Add this to my LENS: I prefer brief emails"), simply acknowledge it. The nightly distillation script will naturally parse the transcript and extract it to the Trinity Nodes.
- **LENS Interview:** If the subject explicitly asks for a LENS question (e.g., "Focus my LENS", "Give me a LENS question"), immediately execute `skills/lens/prompts/interview.md` to query them.
