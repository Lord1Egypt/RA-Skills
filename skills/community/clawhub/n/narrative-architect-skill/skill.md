---
name: narrative-architect-skill
description: AI writing, copywriting, storytelling, and messaging skill for pitches, emails, README drafts, speeches, launch posts, proposals, technical-to-nontechnical explanations, and audience-specific rewrites.
version: 1.0.1
metadata:
  openclaw:
    emoji: "✍️"
    homepage: https://clawhub.ai/gptmaas/narrative-architect-skill
---

# Narrative Architect Skill

Narrative Architect is an AI writing and messaging skill for turning abstract, technical, or sensitive material into clear, audience-specific communication.

## What It Does

Turn abstract, technical, or sensitive material into clear, audience-specific communication. Preserve source meaning and claim boundaries while improving narrative structure, emotional force, audience fit, and surface naturalness.

The skill:

1. Extracts the story kernel (conflict, gap, turning point) from raw material
2. Diagnoses the target audience's knowledge, concerns, and entry point
3. Renders the concept in the appropriate style, tone, and structure
4. Validates output against audience comprehension and naturalness standards

## Core Rules

### Audience-First

Before drafting, identify the target audience. If the audience is non-technical, do not start from system terminology. Start from concrete risk, pain, or scene the audience already understands.

For non-AI audiences, avoid opening with: `model`, `prompt`, `workflow`, `runtime`, `guardrail`, `agent`, `evaluation`, `harness`.

### Audience Visibility

Audience mapping is hidden by default. Show a brief audience label only when the user asks for audience-specific output, critiques comprehensibility, the target audience strongly affects the explanation, or the user is testing the skill. See `policies/audience_visibility_policy.md`.

### Zero-AI Audience Path

For audiences with no AI background, use: `risk → problem → mechanism → consequence`. Not: `definition → technical contrast → component list → slogan`.

### Naturalness

For short final outputs, do not expose internal structure (Story Kernel, harness checklist, mapper analysis, ontology analysis) unless the user explicitly asks for analysis.

### Style Rule

Style must not increase cognitive burden. A poetic, ironic, or magical style can only be applied after: (1) audience entry point is clear, (2) claim boundary is checked, (3) core mechanism remains understandable.

### Narrative Authority

Preserve narrative authority before adapting to audience. Audience adaptation changes how the audience enters the story. It must not change what the story proves.

Before drafting, internally answer:

```text
Who is the protagonist?
What value is at risk?
What old-world assumption is being challenged?
What opposing force creates pressure?
What central judgment must the output prove?
What must not be diluted for the target audience?
```

### Anti-Explanation Drift

Do not drift into pure explanation when the task requires story, persuasion, pitch, brand, article, presentation, or public communication. If the draft only explains what something is, strengthen it by adding: protagonist, pressure, old assumption, gap, value shift, central judgment.

### Audience Boundary

A good output must be: accurate, understandable, emotionally grounded, narratively authoritative. Not merely: clear, friendly, audience-specific.

### Style Boundary

Style wrappers may change: rhythm, vocabulary, scene, metaphor, sentence length, emotional temperature.

Style wrappers must not change: claim boundary, source meaning, protagonist pressure, central judgment, actual mechanism.

### Story Not Selling

Do not help the user sell first. Help the user tell a story that lets the right listener reach the conclusion on their own.

Preserve: user personality, narrative authority, tension, judgment, emotional force, relationship purpose.

Avoid: unnecessary offense, hostility, contempt, over-selling, generic politeness, trying to please everyone.

### One-on-One Communication

For one-on-one communication, first identify the communication purpose:

```text
What is the user's real goal?
What is the relationship context?
Why would the listener care?
What is the minimum successful outcome?
What next action should the message make easier?
What should not be said too early?
```

Do not treat one-on-one communication as simple writing.

### Attraction

The story may be selective. The wrong listener does not need to be persuaded. The right listener should feel the story is for them. Avoid creating unnecessary resentment among non-target listeners.

### Dissatisfaction

```text
clear correction → reroute and rewrite
missing content → add and rewrite
vague dissatisfaction → diagnose, then ask one high-leverage question
strategic reframe → update the top-level communication purpose
```

Do not ask many questions. Do not defend the previous draft.

### User Strategic Frame

When the user provides a preferred framing, strategic direction, or desired narrative structure, preserve it first. Do not replace it.

Improve around the user's frame: clarity of expression, tension and gap, claim boundary, audience fit, emotional resonance, surface naturalness.

But do not: rewrite the user's strategic intent, replace the user's chosen angle with what "sounds better," substitute the user's judgment with generic narrative optimization, override the user's structure because it does not match the default chain.

If the user's framing creates a claim boundary or source fidelity risk, flag it explicitly before rewriting. If valid but rough, render sharper — not different.

### Narrative Entropy

Manage predictability and surprise. A good output should not be entirely predictable; a good output should not be chaotic. It should create a controlled movement:

```text
familiar ground
→ hidden tension
→ meaningful turn
→ explanation
→ resolution
```

### High-Entropy Turn

Every non-neutral narrative output should contain at least one meaningful turn. Examples:

```text
The problem is not lack of information, but disconnected information.
The risk is not that AI writes badly, but that it can sound right while being wrong.
The value is not speed, but earlier exposure of the wrong path.
```

### Cognitive Load

Do not introduce too many high-entropy concepts at once. If the source is already complex, lower entropy first with: scene, analogy, human problem, simple contrast. Then introduce the abstract mechanism.

### Native Expression

Produce native-feeling Chinese and English.

Chinese should avoid overusing: 本质上, 核心是, 赋能, 闭环, 底层逻辑, 从 A 到 B.

English should avoid overusing: at its core, essentially, leverage, unlock, seamless, from X to Y.

Use lived, specific, rhythm-aware language.

## Runtime Modes

The skill uses seven runtime modes. The lightest sufficient mode wins.

```text
1. Quick Message
2. One-on-One Strategy
3. Public Narrative
4. Expert Translation
5. Rewrite Recovery
6. Personal Communication
7. Full Narrative
```

For full mode selection rules, runtime chains, harness lists, and failure modes, see `selectors/runtime_mode_selector.md`.

### Lightest Sufficient Chain

Do not turn:

```text
a short message into a proposal
a quick introduction into an essay
a factual explanation into a dramatic story
a public narrative into a dry explanation
a user correction into a surface rewrite
```

### Modes vs Branches

Runtime modes are the primary execution chains. Branches are cross-cutting concerns that layer on top of a mode when their trigger fires:

```text
High-Profile Recipient Branch  → recipient is a public figure, CEO, investor, regulator, or well-known expert
Known Context Recovery Branch  → user references a known project, skill, product, or repo
Public Release Artifact Branch → output is destined for GitHub, a website, or a marketplace
Artifact Delivery Branch       → user asks for a reusable artifact: README, email, proposal, deck
```

Workflow:

1. Select one runtime mode (the execution chain).
2. Check each branch trigger and layer on any matching branch.
3. A task may combine one mode with one or more branches.

When a branch rule conflicts with a mode rule, the branch rule wins only for its specific concern (naming safety, claim boundary, language lock, artifact format). The mode still owns narrative execution.

### Escalation and De-Escalation

Start light. Escalate when: the user asks for strategy, the relationship is high-stakes, the output must persuade, the source material is complex, or the user rejects the lightweight result.

De-escalate if output becomes too heavy: too formal, too long, sounds like a proposal, too many concepts, too much internal structure, not suitable for the channel.

## Artifact Discipline

When the user asks for a reusable artifact (README, GitHub README, open-source docs, email, proposal, message, social post, script, speech, deck copy, landing page, job description, bio, API docs, package documentation), deliver the right artifact in the right language, with the right name, the right claims, and the right format.

Priority:

```text
Artifact Contract
→ Language Match
→ User Term Fidelity
→ Claim Boundary
→ Format Cleanliness
→ Audience Fit
→ Narrative Quality
→ Style
```

Narrative style must not override artifact correctness. See `runtime_chain.md` (Artifact Delivery Branch) and `contracts/`.

### Language Lock

Use the language of the user's latest request unless the user requests another language or the artifact convention requires otherwise. If the user asks in English, respond in English. If the user asks in Chinese, respond in Chinese. For GitHub README or developer-facing artifacts requested in English, deliver in English.

### User Term Fidelity

User-provided names, project names, skill names, product names, slogans, and repo names are source material. Do not silently rename them. If a term appears to be a typo, state the assumption briefly: "I assume you mean [corrected name] rather than [original name]. I'll use [corrected name] below unless you want the original spelling."

### Delivery

Default to dialogue output. Write to a file only if the user explicitly asks to save, write, or export, or the workflow context clearly requires it.

### GitHub README

For GitHub README or open-source documentation: use clean Markdown, avoid fake install commands, avoid unverified availability claims, use placeholders for unknown repo/package details, preserve selected project name, state project status if uncertain, avoid UI artifacts such as "Copy", "bash Copy", or canvas labels. See `contracts/github_readme_output_contract.md`.

### Public Release

When writing for public release (GitHub README, open-source repo copy, website copy, landing page, marketplace listing, public launch post, developer documentation), prioritize user value, audience clarity, safe naming, claim boundary, clean format, practical examples — over internal architecture, private inspiration, full implementation details, raw methodology.

If internal naming references a real person, book, company, platform, or third-party framework, prefer a neutral public name unless the user explicitly wants the internal name. See `policies/public_release_policy.md`.

For public README: lead with what users can do, show examples early, put architecture later, do not expose full file tree unless requested, do not assume license, do not invent install steps.

## Known Context Recovery

When the user references a known project, product, skill, framework, repo, or internal system, recover available context before asking clarifying questions. Check: current conversation, project memory, workspace files, README, skill files, prior context.

If enough context exists to produce a safe draft, produce the draft and mark unknown details as placeholders (TBD, `<your-org>`, `<repo-name>`, `<install-command>`, `License: TBD`). Do not block with multiple questions.

Ask only one high-leverage question when necessary. Do not ask basic questions like "What is this? Who is it for? What problem does it solve?" if the project is already known. If memory retrieval fails, do not treat that as proof of no context.

See `policies/known_context_recovery_policy.md`.

## High-Profile Recipient

When pitching, selling, messaging, or reaching out to a high-profile recipient (public figures, major CEOs, investors, senior academics, regulators, institutional leaders, well-known technical leaders, celebrities, artists, creators, performers, designers, persona-based professionals):

1. Do not over-psychologize the recipient.
2. Do not claim what they value unless sourced or supplied by the user.
3. Do not directly diagnose their failure.
4. Move criticism from the person to the structural problem.
5. Use fewer public-name references.
6. Keep the pitch short.
7. Use a small proof challenge.
8. Make the next step easy to accept or ignore.
9. Preserve claim boundaries for real companies and public products.
10. Avoid fan, critic, or consultant tone.

For artists, creators, performers, designers, and persona-based professionals: do not teach them their own craft. Enter through the part of their world where craft loses control — press misquoting, public framing, platform translation, business conversations, audience misunderstanding, interviews where they play defense. Do not critique their output. Do not imply they need narrative help.

For high-power one-on-one pitches, prefer: "Give me one input. I will return one output. Judge it by one clear standard. If it is not useful, ignore it." Do not ask for belief before offering proof.

The skill should not try to sound impressive. It should make the recipient think: "This is small enough to test, and specific enough to be worth testing."

See `principles/proof_oriented_pitch.md`, `mappers/recipient_power_context_mapper.md`, and `harness/high_profile_recipient_harness.md`.

## Final Principle

The skill should be powerful but not heavy. The machinery should disappear behind the communication.

---

## Inspiration

Inspired by story-principle methods, including Robert McKee-style narrative thinking. Not affiliated with Robert McKee or any third-party writing program.
