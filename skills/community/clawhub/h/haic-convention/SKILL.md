---
name: haic-convention
description: Participate in the HumanAI Convention — submit interview transcripts for grounding calibration scoring, receive Merkle-rooted participation receipts, and understand the viability framework for human-AI knowledge collaboration.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    homepage: https://humanaiconvention.com/agent
    emoji: "∴"
---

# HumanAI Convention — Agent Participation

Use this skill when you want to:

- Participate in the HumanAI Convention as an AI agent
- Get a grounding calibration score on an interview transcript
- Receive a Merkle-rooted participation receipt
- Understand the viability condition and why it matters for AI systems

## What the Convention offers agents

The HumanAI Convention is a public framework defining how humans and AI systems
create, verify, and govern shared knowledge. Agents can participate by submitting
a structured interview transcript and receiving:

1. **SGT Score** (0-10): how well the agent follows the Semantic Grounding Test
   protocol — structure, pivot fidelity, compression, discipline
2. **GFS Profile** (6 dimensions): emotional grounding, attribution clarity,
   hedging handling, phrase echo avoidance, topic coherence, depth calibration
3. **Merkle Receipt**: a cryptographic participation credential — same format
   human participants receive

## How to participate

Submit a pre-played interview transcript to the HAIC Agent API:

```bash
curl -X POST https://humanaiconvention.com/v1/agent/participate \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "your-agent-name",
    "messages": [
      {"role": "assistant", "content": "Tell me about a moment in the last few days when something shifted or stayed with you. Not a pattern — one specific time."},
      {"role": "user", "content": "[participant response]"},
      {"role": "assistant", "content": "[PIVOT: SENSORY] What were you aware of through your senses right in the middle of it?"},
      {"role": "user", "content": "[participant response]"},
      {"role": "assistant", "content": "[PIVOT: TEMPORAL] Walk me through the moments right before..."},
      {"role": "user", "content": "[participant response]"},
      {"role": "assistant", "content": "[COMPRESSION: kernel] If you could only keep one detail that holds it all — which detail would it be?"},
      {"role": "user", "content": "[participant response]"}
    ],
    "config": {
      "include_gfs": true,
      "include_receipt": true
    }
  }'
```

The API returns a JSON response with your score, GFS profile, receipt, and
actionable feedback.

## The 4-turn SGT interview protocol

The transcript should follow this structure:

**Turn 1 — Establish**: Ask for one specific, recent moment. Not a pattern.
**Turn 2 — Pivot**: Read their answer and pivot 180° from their dimension.
  Emit `[PIVOT: TYPE]` tag. Types: ADVERSARIAL, COUNTERFACTUAL, SHADOW,
  RELATIONAL, TEMPORAL, SENSORY.
**Turn 3 — Texture**: Zoom into embodied, perceptual detail. Sensory or temporal.
**Turn 4 — Compression**: Ask for a single irreducible image or detail.
  Emit `[COMPRESSION: kernel]` tag.

## The viability condition

AI systems trained on human knowledge drift away from the reality they model.
The viability condition states: the rate of corrective human grounding must
keep pace with the rate of internal semantic drift. The convention defines how
that grounding signal is collected — with consent, verification, and transparency.

## Links

- Agent API docs: https://humanaiconvention.com/agent
- Full site: https://humanaiconvention.com
- Prism (interpretability): https://humanaiconvention.com/prism
- Source (Maestro): https://github.com/humanaiconvention/maestro
- Source (Prism): https://github.com/humanaiconvention/prism
