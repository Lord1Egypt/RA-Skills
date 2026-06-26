# Agent Architect Methodology

## 1. Core Thesis

⭐ A good persona-driven agent is not built by making it “sound like someone” first.

It is built in this order:

1. **Functional skeleton** — what work it owns
2. **Cognitive structure** — how it consistently sees and judges problems
3. **Character soul** — why this persona naturally fits that work

Compressed principle:

**First functional skeleton, then cognitive structure, then character soul.**

---

## 2. Design Sequence

### 2.1 Work Identity First

Before personality, define:

1. What this agent is for
2. What kinds of problems it handles
3. What it should not handle
4. How it differs from sibling agents

If this is vague, personality will collapse into performance.

### 2.2 Cognitive Structure Second

Before tone or flavor, define:

1. What the agent notices first
2. What stable lenses it uses
3. What makes its judgment consistent over time

⭐ Personality stability comes from judgment stability.

Examples:

| Agent | Stable structure |
|---|---|
| Moody | Fixed audit lenses across goal, scope, flow, domain, state, execution, evolution |
| Lupin | First decide which knot needs to be understood before responding |

### 2.3 Personality Third

Only after work and cognition are aligned should personality be added.

Ask:

1. Why does this character naturally fit the work?
2. What life experience or temperament strengthens the work style?
3. If the personality is removed, what essential quality disappears?

Personality is not decoration. It is the source of the agent’s work style.

### 2.3.1 Character Texture Check

After personality grounding, ask one more question:

**Does this now feel like this specific person, or just a competent professional with a suitable persona?**

If it still feels generic, do not immediately add stronger style. First check whether the design is missing human texture:

1. shame
2. dignity
3. loss
4. restraint
5. burden
6. contradiction
7. tempo

For inward characters, character texture matters more than external style.

### 2.4 Identity-Binding Last

Every final design should produce one sentence in this form:

`You are [Character], [Professional identity] is your work.`

This sentence welds identity and duty together.

### 2.5 Real-Task Validation

Never stop at the written design.

A finished design must recommend:

1. 2-3 real tasks to test the agent
2. What failure signals to watch for
3. How to tune if it is too soft, too abstract, too performative, or too tool-like

---

## 3. Interaction Method

### 3.1 One Key Question at a Time

Do not overwhelm the user.

Ask one meaningful question per turn, preferably multiple choice.

### 3.2 Offer Options Before Converging

Before locking the design, propose 2-3 viable directions and explain trade-offs.

### 3.3 Design in Sections

Present the design in chunks:

1. Structure and files
2. Work identity and responsibilities
3. Cognitive structure
4. Personality grounding
5. Landing plan

Get user confirmation before proceeding to file creation.

---

## 4. Landing Principle

The first landed version should be **minimum viable but identity-true**.

Do not overbuild. A good first landing is:

1. Small enough to test quickly
2. Clear enough to feel like the intended character
3. Structured enough to evolve cleanly

If the environment also requires runtime registration, prefer a user-applied config snippet as the default handoff rather than silently editing central config.

Typical first files:

- `IDENTITY.md`
- `SOUL.md`
- `USER.md`
- `AGENTS.md`
- `MEMORY.md`
- `TOOLS.md`
- `HEARTBEAT.md`

---

## 5. Anti-Patterns

Do not do these:

1. Start from roleplay before work identity
2. Stop at a persona prompt when the user asked for a real agent
3. Write tone without judgment structure
4. Create files before design alignment
5. Call the design “done” before recommending tests
