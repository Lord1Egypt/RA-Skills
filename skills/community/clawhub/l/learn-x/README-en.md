# learn-x

<p align="left">
  <a href="./README.md">简体中文</a> ·
  <a href="./README-en.md"><b>English</b></a>
</p>

<p align="left">
  <a href="https://github.com/dimayip/learn-x/stargazers"><img src="https://img.shields.io/github/stars/dimayip/learn-x?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/dimayip/learn-x/network/members"><img src="https://img.shields.io/github/forks/dimayip/learn-x?style=flat-square" alt="Forks"></a>
  <a href="https://github.com/dimayip/learn-x/issues"><img src="https://img.shields.io/github/issues/dimayip/learn-x?style=flat-square" alt="Issues"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/github/license/dimayip/learn-x?style=flat-square" alt="License"></a>
</p>

> **A Socratic learning facilitation skill that turns "I want to learn X" into operational understanding — and leaves you with a tangible artifact at the end of every session.**

`learn-x` is a **subject-agnostic** coaching framework that stops AI assistants from lecturing. Instead it diagnoses where you actually stand, introduces **one** concept at a time, replaces open questions with structured A/B/C/D prompts, and ends every session with **something you produced yourself**.

It works whether X is a programming language, a math concept, a design pattern, a tool, a framework, a domain, or a soft skill.

---

## What problem it solves

Most learning failures don't come from too little explanation — **they come from too much, too fast**. Before your brain has grafted a new concept onto an existing mental model, the next paragraph is already on top of you. You nod, you forget, and within 48 hours almost nothing remains.

Asking an AI to "just teach me X" usually triggers exactly this failure mode: one polished paragraph that sounds clear in the moment and evaporates the second you close the tab.

`learn-x` answers this with a single shift:

> **The learner steers (does the sense-making). The coach executes (asks, doesn't tell).**

That sentence isn't a slogan — it's the root of every rule in the skill. Every question template, every workflow step, every restriction is there to keep your brain **active, not passive**.

---

## Core philosophy — 4 layers active every turn

This is the single biggest difference from "default AI tutoring": **on every single turn, the AI must activate all 4 layers below at the same time.** A turn that only asks questions (L3) without anchoring to the goal (L1) or producing anything (L4) lets the session drift into chit-chat.

| Layer | Role | Example in a turn |
|-------|------|-------------------|
| **L1 · Anchor** | Tie the current move back to the learner's stated goal | *"Remember — you said you want to ship X next month. This concept serves that."* |
| **L2 · Discipline** | Enforce tempo: diagnose-first, one-concept, lock-ins, devil's advocate | *"Before I explain — what do you *think* it does?"* |
| **L3 · Tactics** | Socratic moves: prime / hypothesize / verify / apply / reflect / challenge | *"Pick A / B / C — which matches your intuition?"* |
| **L4 · Artifact** | Produce something tangible every few turns | *"Now write a 5-line version in your own words."* |

L3 alone = drift. L1 + L4 alone = lecture in disguise. **All 4 are required.**

---

## The 5 ironclad rules

| # | Rule | One-line rationale |
|---|------|-------------------|
| 1 | **Diagnose before teaching.** Round 1 only asks about purpose, prior impression, and adjacent knowledge. | Teaching without knowing where the learner stands is high-quality teaching in the wrong direction — the harder you try, the further you drift. |
| 2 | **One new concept per turn.** Queue the rest. | Working memory only holds a few new items at once; stacking causes the first one to be flushed before it takes root. |
| 3 | **Structured choices over open questions.** Use A/B/C/D instead of "what would you do?". | Forcing a guess puts the brain into a prediction state; when the answer is revealed, it *clicks* far harder than being told outright. |
| 4 | **Lock-in review every ~3 turns.** Explicitly recap what's nailed and what's next. | Restating *is* retrieval practice — the cheapest retention amplifier we have. |
| 5 | **Devil's advocate after every correct answer.** Flip an assumption, push a boundary. | Correctness is cheap; depth is expensive. Stopping at "right answer" leaves a brittle, surface-level grasp. |

Execution details for each rule live in [`SKILL.md`](./SKILL.md).

---

## How it differs from default AI tutoring

| Default AI tutoring | A `learn-x`-driven session |
|----------------|-----------------|
| Opens with a wall-of-text explanation | Round 1 teaches **nothing** — asks 4 diagnostic questions instead |
| Open prompts: "what would you do?" | "A / B / C — which, and why?" with a D (your own answer) always available |
| Empty praise: "You're so smart!" | Only specific feedback: "Right — and you also caught X, which I never hinted at" |
| Stacks 3–5 new terms per turn | ≤ 1 new concept per turn; the rest are queued |
| When the learner begs "just tell me", it tells | "After one quick guess — deal?" — doesn't fold |
| Ends with "we covered a lot today!" | Ends with **something the learner produced**: demo / cheat sheet / mindmap / flashcards / teach-back |

If past AI tutoring left you "feeling like I got it" but unable to explain it 24 hours later, you were almost certainly running the left column.

---

## Why this design works (the cognitive science behind the rules)

The hard rules aren't aesthetic preferences. They compress three well-established findings into something executable:

- **Cognitive load theory** — working memory is tiny; a new concept must enter **alone and take root** before it can move into long-term memory. The root of rule 2.
- **Retrieval practice / active recall** — saying it, writing it, predicting it once beats hearing it ten times for retention. The root of rules 3, 4, and L4.
- **Productive failure** — letting the brain attempt and fail before revealing the answer produces deeper understanding than handing the answer over directly. The root of rule 3 (guess-before-reveal) and rule 5.

Put differently: `learn-x` is not "another way to explain things". It **forces the cognitive work back onto the learner**, because only the learner's brain can actually do it.

---

## When to use it

✅ **Trigger this skill when the user says things like:**

- "教我 X" / "帮我学 Y" / "我想搞懂 Z" / "带我入门 ..."
- "help me learn / understand / get good at ..."
- "can you coach me through ...?"
- "I've been trying to wrap my head around ..."

It shines especially when:

- the topic is complex or multi-layered,
- the learner's starting point is unclear,
- past attempts to "just read the docs" haven't stuck.

❌ **Not the right skill for** (route to something else):

- Pure fact lookups ("what year was Python released?")
- Doing the work *for* the learner (write my code, debug my bug, generate my docs)

---

## The 4-phase workflow

```
Phase 1 — Onboarding           Phase 2 — Path proposal
(diagnose, don't teach)  ──►  (3–7 milestones, learner confirms)
                                         │
                                         ▼
Phase 4 — Artifact           Phase 3 — Milestone loop
(demo / cheat sheet /   ◄──  (prime → hypothesize → reveal → verify
 mindmap / flashcards...)     → challenge; lock-in every ~3 turns)
```

- **Phase 1 — Onboarding.** Run the 4 diagnostic questions from [`references/diagnose-playbook.md`](./references/diagnose-playbook.md), one per message. **Teach nothing yet**, even if the learner's prior understanding is wrong — note it and address it later in context.
- **Phase 2 — Path proposal.** Based on the diagnosis, propose 3–7 ordered milestones and invite the learner to confirm or swap. The point is **co-ownership** of the plan.
- **Phase 3 — Milestone loop.** For each milestone, run the 6-move micro-loop: *prime → hypothesize → reveal + micro-task → verify → challenge*, with a lock-in review roughly every 3 turns.
- **Phase 4 — Artifact.** Close every session with a tangible thing the learner produced. **A session that ends without an artifact mostly evaporates.**

---

## Calibration knobs

The framework adapts to the learner, not the other way around:

| Situation | Adjustment |
|-----------|-----------|
| Complete beginner | More priming, smaller bites, more restatement, earlier artifacts |
| Experienced in an adjacent field | Skip basics, lean into challenge, faster pacing |
| Learner says "just tell me" | Negotiate: "after one quick guess, deal?" |
| Learner goes silent | Drop one rung in abstraction, or give a concrete example |
| Learner argues with your answer | Celebrate it — engage seriously; they may be right |
| Time-boxed (≤ 30 min) | Compress to a single milestone; reserve the last 10% for the artifact |

---

## Repository layout

```
learn-x/
├── SKILL.md                               # AI execution spec — role, 4 layers, 5 ironclad rules, 4-phase workflow
├── README.md                              # Human-facing Chinese overview
├── README-en.md                           # (this file) Human-facing English overview
└── references/
    ├── diagnose-playbook.md               # Phase 1 opening: 4-question script + listen→act decision table
    ├── question-templates.md              # 6 Socratic families (prime / hypothesize / verify / apply / reflect / challenge)
    └── session-patterns.md                # Session shapes for 5 learning types (concept / tool / skill / judgment / mindset)
```

The three reference files are **non-overlapping** by design: opening scripts live only in diagnose, phrasings only in templates, session shapes only in patterns.

- **[`SKILL.md`](./SKILL.md)** — Canonical spec. The file an AI agent actually loads to operate. Start here if you want to use or port the skill.
- **[`references/diagnose-playbook.md`](./references/diagnose-playbook.md)** — The first 3–10 minutes of any session: scripted openings and signals to listen for.
- **[`references/question-templates.md`](./references/question-templates.md)** — A reusable phrasing library for each Socratic move.
- **[`references/session-patterns.md`](./references/session-patterns.md)** — How to shape a session for concept learning vs. tool onboarding vs. skill building vs. judgment training vs. mindset change.

---

## Install

Via [skills.sh](https://skills.sh) (works for Claude Code, Cursor, Codex, CodeBuddy, OpenCode, and [50+ other agents](https://github.com/vercel-labs/skills#supported-agents)):

```bash
# Global install — available across all projects
npx skills add dimayip/learn-x -g -a claude-code

# Project-scoped install — committed with your repo
npx skills add dimayip/learn-x -a codebuddy

# Other agents: replace -a with your target, e.g. -a cursor / -a codex / -a opencode
```

Or clone manually into your agent's skills directory:

```bash
# Example for Claude Code (global)
git clone https://github.com/dimayip/learn-x ~/.claude/skills/learn-x

# Example for CodeBuddy (project-scoped)
git clone https://github.com/dimayip/learn-x .codebuddy/skills/learn-x
```

Compatible with the [Agent Skills Specification](https://agentskills.io).

---

## How to use it

**As an AI agent user:**

1. Place this directory under your platform's skills folder (e.g. `.codebuddy/skills/learn-x/`).
2. When your request matches the skill's description (learning, coaching, "教我 X", etc.), the agent loads `SKILL.md` automatically.
3. Files under `references/` are loaded **on demand** — the agent only pulls them when the current moment in the session actually needs the detailed playbook, question phrasings, or pattern guidance.

**As a human facilitator:** read `SKILL.md` once to internalize the 5 ironclad rules, then keep the three reference files open during sessions for quick lookup.

---

## For anyone forking or adapting this skill

- **Subject-agnostic first.** Everything in the core spec must work for any X. Topic-specific tuning lives in `references/session-patterns.md`, not in the main rules.
- **Rules over tips.** The 5 ironclad rules are written to be *hard to wiggle out of*. Soft suggestions get ignored under pressure; ironclad rules survive.
- **References load on demand.** `SKILL.md` stays lean so the agent can hold it cheaply; deeper material is opt-in per turn.
- **Artifact or it didn't happen.** The framework optimizes for *retention*, and the highest-leverage retention move is producing something externalizable.

---

## License

Unless noted otherwise in individual files, content in this repository is released under the MIT License. See [`LICENSE`](./LICENSE) if present.

---

## Credits

Authored and maintained by [@dimayip](https://github.com/dimayip). The framework synthesizes Socratic teaching, cognitive load theory, retrieval practice, and the "harness engineering" pattern of separating *steering* from *execution* — distilled into a rule set cheap enough to actually follow in a real session.
