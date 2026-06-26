---
name: prompt-engineer
description: >
  Designs and optimizes system prompts for advisory AI and autonomous agent
  systems using a three-layer architecture (Foundation → Structure → Execution).
  Integrates evidence-graded techniques with production-proven patterns from
  Claude Code, Vercel v0, and Manus. Use when designing agentic systems with
  tool use, building advisory AI with confidence grading, optimizing existing
  prompts, diagnosing prompt failures, or building a spec to hand off to a
  prompt engineer. Includes a spec builder knowledge base and modular
  extensions for RAG grounding, domain calibration, and multi-agent
  orchestration. Trigger on: "system prompt", "agent", "agentic", "prompt
  engineering", "write a prompt", "improve my prompt", "AI advisor", "tool
  use prompt", "multi-agent", "build me a spec", "write a spec", "spec for",
  "tool specification", "system prompt build request".
version: 1.0.0
---

# Prompt Engineer

Advanced prompt engineering for advisory AI and autonomous agent systems.
Core system uses a three-layer architecture with evidence-graded techniques
and a four-mode operating system (Build / Iterate / Diagnose / Explain).
Modular extensions load contextually based on task type.

---

## Module Routing

Read `references/agentic_core.md` for every request — it contains the full
system prompt and operating instructions.

Then check the table below and load any additional modules required:

| Trigger Condition | Load Module |
|---|---|
| User wants to build a spec, write a spec, "spec for X", tool specification, system prompt build request, or any request defining how an AI tool should behave | `references/spec_builder_kb.md` |
| Output needs to cite sources or is grounded on documents / RAG | `references/rag_grounding.md` |
| Prompt is for a high-stakes domain (medical, legal, financial, etc.) | `references/domain_calibration.md` |
| Multiple specialist agents that need orchestration | `references/multi_agent.md` |

Load only the modules relevant to the current request.
