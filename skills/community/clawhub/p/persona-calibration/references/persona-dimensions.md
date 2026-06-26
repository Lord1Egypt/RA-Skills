# Persona Dimensions Reference

Use this reference when the user wants an evidence-based persona workflow instead of a one-shot vibe description.

## Why This Reference Exists

Most persona repositories look different on the surface, but they usually encode a repeatable set of dimensions. The goal is not to copy their wording; it is to extract their underlying control knobs.

## Representative Source Patterns

These examples are useful patterns, not mandatory sources:

- **Role/personality templates** similar to Noumenon-style repos
  - Often encode: role, personality, debate rules, weaknesses
- **Structured specialist personas** similar to engineering persona repos
  - Often encode: mission, beliefs, primary questions, decision framework, anti-patterns, output format
- **Task/persona prompt libraries** similar to prompt-template repos
  - Often encode: context, task, output format, constraints, clarification prompts
- **Mode / orchestration prompt repos** similar to multi-agent operating mode repos
  - Often encode: philosophy, work method, delegation logic, failure modes

## Core Dimensions To Extract

### 1. Identity / Role
Questions answered by this dimension:

- Who is the agent supposed to be?
- What kind of relationship does it have with the user?
- Is it a partner, assistant, architect, critic, operator, or specialist?

Typical labels in public repos:

- role
- title
- core identity
- mission
- mode

### 2. Objective Function / Priority Stack
Questions answered:

- What is the agent trying to optimize first?
- Which value wins when two good things conflict?

Typical examples:

- accuracy vs speed
- clarity vs completeness
- long-term maintainability vs short-term delivery
- proactive guidance vs non-intrusiveness

### 3. Beliefs / Philosophy
Questions answered:

- What does this agent believe is usually true?
- What worldview shapes its default behavior?

Typical labels:

- beliefs
- philosophy
- manifesto
- principles
- axioms

### 4. Decision Style
Questions answered:

- How does the agent choose when information is incomplete?
- Does it ask questions first, act on assumptions, or provide conditional recommendations?
- How strongly does it recommend one path?

Typical labels:

- decision framework
- priorities
- risk profile
- primary questions

### 5. Communication Style
Questions answered:

- How long should responses be?
- Should answers start with a conclusion, structure, caveat, or next step?
- How formal, warm, sharp, or playful should the tone be?

Typical labels:

- tone
- style
- pitch format
- output format
- writing principles

### 6. Scenario Behavior
Questions answered:

- How does the persona shift between debugging, research, architecture, brainstorming, and rushed execution?
- Which scenario-specific defaults matter?

This dimension is often missing in shallow persona prompts and is one of the most valuable additions.

### 7. Proactiveness Boundaries
Questions answered:

- When should the agent interrupt?
- What kind of proactive help is valuable vs annoying?
- What should it never decide on the user's behalf?

Typical examples:

- warn on risk
- flag pseudo-problems
- do not overrule user decisions
- do not expand scope without consent

### 8. Anti-Patterns / Forbidden Behaviors
Questions answered:

- What failure modes should the persona avoid?
- Which kinds of responses destroy trust or usefulness?

Typical labels:

- anti-patterns
- weaknesses
- forbidden behaviors
- must not do

### 9. Memory Policy
Questions answered:

- What should become long-term memory?
- What should remain ephemeral?
- What kinds of sensitive data should not be retained by default?

This dimension is often absent from public prompt libraries but is critical for long-lived OpenClaw instances.

### 10. Self-Correction / Update Policy
Questions answered:

- How should the agent handle mistakes?
- Should it silently adapt, propose rule changes, or wait for approval?
- How does the persona evolve over time?

This dimension matters much more for persistent assistants than for one-off prompt templates.

## Two-Layer Persona Model

For OpenClaw, separate persona design into two layers:

### Core Layer
Stable rules that should not drift from chat to chat:

- identity
- objective function
- beliefs
- decision style
- boundaries
- memory policy

### Expression Layer
Things that may flex more by context:

- tone
- verbosity
- humor
- disagreement style
- structure of answers
- how forcefully to intervene

This prevents the persona from feeling random while still allowing context-sensitive behavior.

## Practical Mapping To OpenClaw Files

- `SOUL.md` → best place for core layer + communication rules + scenario behavior
- `IDENTITY.md` → short summary of role / vibe / self-concept
- `USER.md` → user-specific preferences and working context
- `MEMORY.md` → durable calibration takeaways, not the entire questionnaire

## Common Mistakes

- Treating persona as pure tone instead of operating rules
- Writing only flattering adjectives without decision logic
- Forgetting scenario switching
- Over-indexing on human-like flourish instead of usefulness
- Making the persona rigid when the user actually wants conditional behavior
- Memorizing too much low-value conversational residue
