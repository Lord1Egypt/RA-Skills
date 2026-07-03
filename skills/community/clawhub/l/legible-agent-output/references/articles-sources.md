---
load: on demand — when citing the literature or evaluating a quote
parent: ../SKILL.md
---

# Article Sources — Legible Agent Output

Six sources that ground this skill in published UX-research and agent-design literature. Each entry links to the original article, names the author, and records the specific claim this skill relies on.

> **Note on verification:** All six URLs were fetched on 2026-06-30 and verified to resolve to the cited articles. Specific claims below are paraphrases; where a direct quote is given, it is anchored to the article body. Before publishing this skill outside the workspace, re-verify any direct quotes against the current article versions in case they have been edited.

---

## 1. Smashing Magazine — *Designing For Agentic AI: Practical UX Patterns For Control, Consent, And Accountability* (Feb 2026)

**URL:** https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/

**Author:** Victor Yocco

**Specific claim:** The "Intent Preview" pattern requires agents to summarize the primary actions and outcomes in plain language before executing, avoiding technical jargon. The article's own example: instead of *"Executing API call to cancel_booking(id: 4A7B),"* the preview should state *"Cancel flight AA123 to San Francisco."* This is the direct analog of the problem this skill solves.

**Direct quote:** *"The preview must be immediately digestible. It should summarize the primary actions and outcomes in plain language, avoiding technical jargon."*

**How this skill uses it:** Direct source of law #1 ("title first, code second") and law #3 ("translate every error code into a sentence"). We synthesize the article's "Intent Preview" as the principle *plain-language action preview* in this skill's description.

---

## 2. Hatchworks — *Agent UX Patterns: Chat-First UX Fails. Use These Patterns Instead* (Mar 2026)

**URL:** https://hatchworks.com/blog/ai-agents/agent-ux-patterns/

**Author:** Andy Smith

**Specific claim:** Names two specific failure modes — *Invisible actions* and *Unclear state*. When a user cannot see what the agent is doing or why, they lose trust not because the agent is wrong, but because the agent's behaviour is opaque to them.

**Direct quote:** *"users don't trust the agent — not because it's wrong, but because they can't see what it's doing."*

**How this skill uses it:** Direct source of laws #4 ("never expose framework names as nouns") and #5 ("status messages describe visible state, not internal plumbing"). We synthesize these as the principle *legible agent state* in this skill's description. Also why the eval loop tests "status updates" explicitly.

---

## 3. Exalt Studio — *UI/UX Design for AI Startups: Best Practices for Agents, Tools & Interfaces* (Jun 2026)

**URL:** https://exalt-studio.com/blog/uiux-design-for-ai-startups-best-practices-for-agents-tools-interfaces

**Specific claim:** Best-practice agent UX requires agents to communicate in user-language, not developer-language. Contextual, specific feedback builds trust; generic messages do not.

**Direct quotes:**
- *"Avoid overwhelming users with technical jargon."*
- *"Instead of generic messages, provide specific explanations like, 'This result is based on your past searches'."*

**How this skill uses it:** Source of the "contextual + concrete" framing in law #2 ("one concrete verb + one concrete object") and in the workflow's Phase 1 ("would my mother understand this without explanation"). Reinforces the same principles as Smashing Magazine from a product/UX-design angle rather than a research angle.

---

## 4. boost.ai — *Common Conversational AI Mistakes (and How to Avoid Them)* (Jun 2025)

**URL:** https://boost.ai/blog/common-conversational-ai-mistakes/

**Specific claim:** Identifies five common failure modes in conversational AI: limited context understanding, over-reliance on predefined scripts, lack of personalization, inability to handle complex queries, and security/privacy concerns. Demonstrates good vs poor responses side-by-side — high-quality responses are concrete, contextual, and specific; poor responses are generic, miss parts of the user's request, or expose sensitive data.

**How this skill uses it:** Validates the principle that concrete, contextual user-language beats generic or technically-precise output. The "personalization" section especially reinforces the "contextual + concrete" framing sourced from Exalt Studio (section 3 above).

---

## 5. Orange Loops — *Designing Trustworthy AI Assistants: 9 Simple UX Patterns That Make a Big Difference* (Jul 2025)

**URL:** https://orangeloops.com/2025/07/9-ux-patterns-to-build-trustworthy-ai-assistants/

**Author:** Juan José Reyes

**Specific claim:** Of the article's nine UX patterns, two are most directly relevant to legible agent state: **#1 Expectation Management** (the agent must communicate its limitations, capabilities, and uncertainty clearly) and **#3 Failing Gracefully** (when the agent doesn't know or can't help, the response should explain and suggest next steps rather than dead-ending).

**Direct quote:** *"expectation management is the most important UX pattern. When users know what an AI can and can't do, they trust it more, use it better, and stick with it longer."*

**How this skill uses it:** Reinforces that legible state is a *trust primitive* — when users know what the agent can and cannot do, they trust it more. The "Failing Gracefully" pattern maps directly onto our law #3 (translate every error code into an actionable sentence).

---

## 6. Medium Bootcamp — *What UX Designers Should Understand About AI Agents* (Dec 2025)

**URL:** https://medium.com/design-bootcamp/what-ux-designers-should-understand-about-ai-agents-ded69d00ebf6

**Author:** Yanshi Tyagi

**Specific claim:** UX designers working on agentic products must understand that agent output is a UX surface — every string the agent emits is part of the product's interface, not an internal log. The article's central questions: *"How does the agent show what step it is currently on? How does the user know when to intervene? How does the agent explain what it needs?"*

**How this skill uses it:** Source of the principle *"every status message, every cycle report, every plan summary ends up in front of a human eventually."* This is the foundation of the anti-patterns section in SKILL.md.

---

## How to cite this skill in agent output

When an agent rewrites output per this skill, it may footnote:

> Rewritten for legibility per the *Legible Agent Output* skill (Smashing Magazine, Hatchworks, Exalt Studio).

Three citations are enough; full source list above. The footnote is optional — its purpose is to give technical users a way to learn more, not to clutter the user-facing output.

---

## Changelog

**2026-06-30 — Audit pass.** Reduced source list from seven to six after re-verifying every claim against the actual article body. Three corrections were made:

- **boost.ai ↔ Exalt Studio swap.** The previous version attributed the *"This result is based on your past searches"* quote and the "contextual + concrete" framing to boost.ai. That quote is verbatim from Exalt Studio, not boost.ai. Sections 3 and 4 were swapped and their content rewritten to reflect each article's actual claims.
- **Orange Loops overstatement removed.** The previous version said *"legibility-of-actions is one of the strongest"* of the nine patterns. The article does not include "legibility-of-actions" by that name. Section 5 now correctly identifies **Expectation Management** (Pattern #1) and **Failing Gracefully** (Pattern #3) as the two most relevant, with a direct quote supporting the claim.
- **LogRocket source removed.** The previous version attributed to LogRocket the claim *"AI features are routinely shipped without the surrounding UX scaffolding users need to understand them."* The actual article (*Overusing AI is ruining UX*, Nov 2025) is about UX designers overusing AI for ideation, research, and automation — it does not make a specific claim about agent transparency or UX scaffolding. The attribution was a stretch, so the source was removed rather than risk an unverifiable claim.
