# How to Harness

<p align="left">
  <a href="./README.md">简体中文</a> ·
  <a href="./README-en.md"><b>English</b></a>
</p>

<p align="left">
  <a href="https://github.com/dimayip/how-to-harness/stargazers"><img src="https://img.shields.io/github/stars/dimayip/how-to-harness?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/dimayip/how-to-harness/network/members"><img src="https://img.shields.io/github/forks/dimayip/how-to-harness?style=flat-square" alt="Forks"></a>
  <a href="https://github.com/dimayip/how-to-harness/issues"><img src="https://img.shields.io/github/issues/dimayip/how-to-harness?style=flat-square" alt="Issues"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/github/license/dimayip/how-to-harness?style=flat-square" alt="License"></a>
</p>

> **A facilitation skill dedicated to designing Harness-style closed-loop, self-optimizing, human-steer-plus-agent-execute systems — turning *"I want to build an AI loop"* into a deliverable plan that aligns with the 7 Harness principles.**

`how-to-harness` operationalizes OpenAI's [Harness Engineering](https://openai.com/index/harness-engineering/) methodology — **"Humans steer, agents execute"** — into a rule set that can actually run inside a real conversation. On top of ordinary Socratic facilitation, it stacks one extra layer of **hard domain constraints** (Layer 0 · 7 Harness Principles), so that every locked-in decision is forced to align with the methodology's core rules.

Whether you're designing an agent loop, a Ralph loop, a CI-style eval loop, or a governance system that needs tiered automation and human gates, this skill makes you **set the constraints first**, then start asking.

---

## What problem it solves

Design failures in Harness-style systems **almost never come from "not asking enough questions"** — they come from **asking the wrong questions**. Decisions get locked in at points that violate the Harness principles, and three months later, when the system is finally running, you discover the real inflection point was never even debated. Typical collapse modes:

| What the user said | The cost a few months later | Principle violated |
|---|---|---|
| *"We'll skip the eval set for now and ship first."* | Lots of changes shipped, but no one can tell whether they're good or bad. | HP-1 |
| *"The manager will personally rewrite the prompts."* | The manager becomes the bottleneck; the system slows down as it grows. | HP-2 |
| *"It's fine if each run produces different results."* | Not reproducible / not debuggable / not rollback-able. | HP-3 |
| *"Once improved, ship directly — no soak period."* | A single failure takes down the entire pipeline. | HP-4 |
| *"Either fully automated or fully manual."* | No tiers, no escalation path. | HP-5 |
| *"Assets live on someone's laptop."* | Three months later, no one knows who changed what. | HP-6 |
| *"If we're short on people, we'll just work overtime."* | Hidden cost explodes; the team burns out. | HP-7 |

Asking an AI to "help me design a self-optimizing system" usually triggers exactly this failure mode: the plan sounds polished, but the hard constraints that would have caught the collapse get politely waved through.

`how-to-harness` is built around a single shift in perspective:

> **The designer steers (owns every decision); the agent executes (asks, cross-checks, organizes) — and the agent must use the 7 Harness principles as a ruler, refusing to let decisions lock in while violating domain constraints.**

That sentence isn't a slogan — it's the root of every rule in the skill.

---

## Core idea: Layer 0 is the soul of this skill

A generic design-facilitation skill only helps you "ask clearly". `how-to-harness` adds one layer on top of that: a layer of **hard domain constraints** — Layer 0's 7 Harness Principles.

```
Layer 0: Harness Principles (non-negotiable domain constraints)  ← the soul of this skill
   ↓
Layer 1: Capture Context — anchor + current state + deliverable consumer
   ↓
Layer 2: Brainstorming discipline (internalized) — 6 hard rules that enforce tempo
   ↓
Layer 3: Socratic questioning — A/B/C/D candidates + dependency topology + 4 consistency checks
   ↓
Layer 4: Deliverable organization — pick schema by consumer, slot in locked decisions
```

**Layers 1–4 alone = ordinary brainstorming** — flows nicely but easily locks decisions in the wrong places.
**Layer 0 alone = a pile of dogma** — no questioning rhythm, can't actually be run.
**All 5 layers stacked = combining "ask well" with "use the domain as a ruler".**

---

## The 7 Harness Principles (Layer 0 hard constraints)

| # | Principle | One-line meaning | Why this is a hard constraint |
|---|-----------|------------------|--------------------------------|
| **HP-1** | Eval is foundation | Any improvement loop starts by building a Gold Set. No evals → no automated changes. | A loop with no evals is only "thinking it's improving" — you can't tell good from bad; direction-sense becomes pure illusion. |
| **HP-2** | Humans steer via gates, not via code | Humans define / approve / tune gates; they do not personally rewrite the code. | The moment humans rewrite code, they become the bottleneck. Humans defining gates is what lets the system scale. |
| **HP-3** | Loops must be idempotent & resumable | Every step reruns with the same result; interruptions resume from a checkpoint. | A non-idempotent loop = not reproducible = not debuggable = not rollback-able. |
| **HP-4** | Small, reversible steps | Small diffs · soak period · failures roll back automatically. | Big-bang releases are doubly dangerous in a self-optimizing system — you don't even know which step caused the failure. |
| **HP-5** | Automation tiers with clear escalation | Automation split into L1/L2/L3, each tier has clear boundaries and escalation conditions. | A 0/1 automation toggle inevitably gets abused — either over-trusted or completely turned off. |
| **HP-6** | Asset versioning | Evolving assets must be versioned; any version must be individually rollback-able. | Evolving assets without versioning = three months later, no one can answer "who changed it, and why". |
| **HP-7** | Human time budget is a first-class constraint | Human time is a budget set up front, not something accounted for after the fact. | Defaulting to "we'll work overtime" hides the cost in team fatigue — until the team burns out. |

Execution details, mandatory questions, and red-flag signals for each principle live in [`SKILL.md`](./SKILL.md) and [`references/decision-checklists.md`](./references/decision-checklists.md).

---

## How it differs from default AI design facilitation

| Default AI design facilitation | A `how-to-harness`-driven session |
|----------------|-----------------|
| Starts drawing the architecture diagram immediately | Round 1 **draws nothing** — runs the Layer 0 acceptance (7 questions) first |
| Asks *"do we want a Gold Set?"* | *"A Gold Set is mandatory (HP-1). Where does it come from — A. human labeling / B. rule-based nomination / C. historical samples? My recommendation is..."* |
| Accepts *"the manager will rewrite the prompts"* | Calls out the HP-2 violation on the spot; pushes toward *"the manager only tunes the gates"* |
| Accepts *"just ship after the change"* | Calls out the HP-4 violation; demands a soak period and a rollback trigger |
| Defaults to producing a PRD | Asks who the consumer is first, then chooses PRD / Design Doc / RFC / Kickoff / ADR / One-Pager |
| Asks about 5 axes per turn | One axis per turn, strictly dependency-ordered |
| Open-ended questions like *"what would you like to do?"* | A/B/C/D candidates + an explicit recommendation + reasoning |
| Locks in decisions and writes the doc | Runs 4 consistency checks every turn, especially against HP-1~HP-7 |
| *"OK, here's the whole plan!"* — single dump | Section-by-section presentation with explicit approval; lock-in review every ~3 turns |
| Auto-invents repo / system names | Offers 2–3 candidates, lets the user pick |

If you've used AI to design a self-optimizing / agent-loop system before and ended up with *"the eval set never got built"*, *"the manager is stuck tuning prompts"*, or *"the auto-improver isn't rollback-able"* — you almost certainly ran the left column.

---

## Design rationale (why this works)

The 7 principles aren't invented from scratch. They compress lessons from multiple engineering traditions into executable hard constraints:

- **OpenAI's Harness Engineering methodology** — the "humans steer, agents execute" idea. HP-2 / HP-5 / HP-7 come directly from it.
- **CI/CD and Site Reliability practice** — observability, gradual rollout, rollback-ability, and resumable execution are why large systems can scale at all. The root of HP-3 / HP-4 / HP-6.
- **ML evaluation engineering** — "continuous improvement" without a Gold Set has been disproven in ML over and over. The root of HP-1.
- **Socratic facilitation + cognitive-load management** — A/B/C/D candidates, dependency-ordered questions, one-axis-per-turn, section-by-section approval — all mature brainstorming practices that prevent "asked too much, too scattered" forcing the user to pick something at random. The root of Layer 2 / Layer 3.

In other words: `how-to-harness` is not "another design-facilitation style". It **forces the hard constraints — already proven in real engineering practice — back onto the designer**. Only the designer can make the final calls on gates, budgets, and granularity, but the agent must put those constraints on the table first.

---

## When to use it

✅ **Trigger this skill when:**

- The system contains a **closed-loop / self-optimizing** structure (agent loop / Ralph loop / CI-style eval loop / periodic self-improvement).
- The system has explicit **human–machine collaboration gates** (tiered automation L1/L2/L3, who approves what, when does it escalate).
- The system is **evaluation-driven** (Gold Set, regression tests, LLM-as-judge, hard gates / soft evals).
- The user explicitly mentions Harness Engineering / Ralph loop / LLM-as-judge / gatekeeper / closed-loop / autonomy / agent autonomy / escalation path.

**Key diagnostic question**: *"Will this system execute itself, and improve itself, on its own?"* If the answer is not clearly "yes", this skill does not apply.

❌ **Not the right skill for** (route elsewhere or just write the doc directly):

- Ordinary product features / internal tools / platform refactors / APIs / data models / workflows
- One-shot dialogue / Q&A features
- Pure CRUD requirement docs that are already well-thought-out

---

## The final deliverable is not just "a PRD"

The output of this skill is **chosen based on the real consumer**, not fixed in advance:

| Scenario | Recommended deliverable | Primary consumer |
|----------|-------------------------|------------------|
| New system from scratch (engineering-heavy) | **Design Doc + Kickoff checklist** | Developers + AI coding agent |
| Product pitch / upward reporting | **PRD + One-Pager** | Product review + leadership |
| Internal tech refactor / cross-team work | **RFC / technical proposal** | Engineering team + architecture review |
| Requirements still exploratory | **ADR + open-question list** | Self + follow-up |
| Existing plan needs execution | **Milestone plan + ownership matrix** | Execution team |

Multiple deliverables can be produced **in parallel** (e.g. PRD + One-Pager + Kickoff as a bundle, each aimed at a different audience). Templates and a selection decision tree live in [`references/deliverables.md`](./references/deliverables.md).

---

## Standard workflow

```
Step 0    Decide whether this skill applies (30 sec: "does the system run and improve itself?")
   │
   ▼
Step 0.5  Layer 0 hard-constraint acceptance (7 questions across HP-1~HP-7; if any fail, park)
   │
   ▼
Step 1    Capture Context (turn 1: current state + anchor + deliverable form + consumer, with restatement)
   │
   ▼
Step 2    Socratic questioning (N turns, dependency-ordered, lock-in review every ~3 turns, 4 checks per turn)
   │
   ▼
Step 3    Section-by-section presentation (2–5 sections, each ends with "approve or adjust?")
   │
   ▼
Step 4    Organize the deliverable by chosen schema (ship multiple deliverables in parallel + label consumers)
   │
   ▼
Step 5    Retrospective (optional but strongly recommended) — answer honestly: "what framework did I use, and which HPs did I hold the line on?"
```

Full execution details (per-step hard constraints, mandatory questions, prohibitions) live in [`SKILL.md`](./SKILL.md).

---

## Repository layout

```
how-to-harness/
├── SKILL.md                               # AI execution spec — 5-layer framework + HP-1~HP-7 + workflow + prohibitions
├── README.md                              # Human-facing Chinese overview
├── README-en.md                           # (this file) Human-facing English overview
└── references/
    ├── decision-checklists.md             # Hard decision checklists for Harness systems (each section aligned to one HP)
    ├── deliverables.md                    # Templates for 6 deliverable types + selection decision tree
    └── ralph-case-study.md                # Real case: from "I want to build an AI loop" to a full Ralph Harness design in 9 turns
```

The four files are **non-overlapping** by design: execution steps live only in SKILL, decision checklists only in `decision-checklists`, deliverable templates only in `deliverables`, narrative case studies only in `ralph-case-study`.

- **[`SKILL.md`](./SKILL.md)** — Canonical spec. The file an AI agent actually loads to operate. Start here if you want to use or port the skill.
- **[`references/decision-checklists.md`](./references/decision-checklists.md)** — Hard decision checklist for the Socratic phase. Each section aligns with one HP (HP-1 evals / HP-2 gates / HP-3 idempotency / HP-4 granularity / HP-5 tiers / HP-6 versioning / HP-7 budget).
- **[`references/deliverables.md`](./references/deliverables.md)** — Full templates for 6 deliverable types + a Capture-phase selection decision tree.
- **[`references/ralph-case-study.md`](./references/ralph-case-study.md)** — End-to-end case: starting from *"based on Harness Engineering, build me a self-optimizing loop for my diagnose agent"*, 9 turns of dialogue produce a full Ralph Harness design. **The single best learning material.**

---

## Self-contained by design

`how-to-harness` internalizes Socratic brainstorming discipline + the schema knowledge for 6 mainstream document types + every Harness hard constraint, and **does not depend on other skills**. Why:

1. **Keeping the complete methodology in one skill** makes it easier to teach, evolve, and retrospect on — you don't need to learn another brainstorming skill first.
2. **Eliminates orchestration risk** — if an external dependency fails to trigger, the whole chain breaks. Self-containment means the core methodology survives no matter how clumsy the agent platform's routing is.
3. **Allows cross-phase references** — decisions locked in the Capture phase can be used directly in the Layer 4 write-up without losing context.

---

## Install

Via [skills.sh](https://skills.sh) (works for Claude Code / Cursor / Codex / CodeBuddy / OpenCode / 50+ agents):

```bash
# global (available in all projects)
npx skills add dimayip/how-to-harness -g -a claude-code

# project-only (committed with your repo)
npx skills add dimayip/how-to-harness -a codebuddy
```

Or drop the repo manually into your agent's skills directory, e.g.
`~/.claude/skills/how-to-harness/` or `.codebuddy/skills/how-to-harness/`.

Compatible with the [Agent Skills Specification](https://agentskills.io).

---

## How to use it

**As an AI agent user:**

1. Install via `npx skills add dimayip/how-to-harness` (see above), or place this directory under your platform's skills folder.
2. When the user's request clearly involves closed-loop / self-optimizing / agent-loop / eval-driven systems (mentions of Harness Engineering / Ralph / LLM-as-judge / gatekeeper, etc.), the agent loads this skill's `SKILL.md`.
3. Files under `references/` are loaded **on demand** — the agent pulls them only when the current turn genuinely needs the decision checklist, a deliverable template, or the case study, keeping `SKILL.md` itself lean.

**As a human facilitator:** read `SKILL.md` end-to-end once, internalize HP-1~HP-7 until they become intuition, and keep the three reference files open during conversations. Strongly recommended: read `references/ralph-case-study.md` first — 9 turns of dialogue show how this methodology actually runs in practice.

---

## For anyone forking or adapting this skill

- **Domain hard constraints first.** Layer 0's 7 HPs are the soul of this skill — when you modify it, **only add, never dilute**. If you want to adapt it to another domain (security audit, compliance governance), add new HPs instead of weakening existing ones.
- **Rules over tips.** HP-1~HP-7 are *hard constraints*, not *soft suggestions*. Soft suggestions get ignored under pressure; hard constraints survive. Keep the wording uncompromising — *"must / cannot / call out immediately"*, no hedging.
- **References load on demand.** `SKILL.md` stays lean so the agent can hold it cheaply; deeper material (decision checklists, deliverable templates, case studies) is opt-in per turn.
- **Decision ownership stays with the user, always.** The agent's job is to *ask the right things, use the HPs as a ruler, and call out violations honestly* — but never to decide for the user. Even when the user says *"I know this violates HP-3, but I accept it,"* that's an informed decision the agent should record, not push back on repeatedly.

---

## Meta principle

> **The point of this skill is not to make an agent better at *asking* — it's to add one more layer on top of good questioning: use the Harness principles as a ruler, and *refuse* to let decisions lock in while violating domain constraints.**
>
> "Good questions + domain criteria = good decisions = good deliverables" (whether the output is a PRD, RFC, Design Doc, or something else).
> The user always owns the decisions — the agent just helps the user express them, and **honestly calls out when the user is violating a Harness principle**.

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=dimayip/how-to-harness&type=Date)](https://star-history.com/#dimayip/how-to-harness&Date)

---

## License

Unless noted otherwise in individual files, content in this repository is released under the MIT License. See [`LICENSE`](./LICENSE) if present.

---

## Credits

Designed and maintained by [@dimayip](https://github.com/dimayip). The core ideas come from OpenAI's [Harness Engineering](https://openai.com/index/harness-engineering/), fused with CI/SRE engineering practice, ML evaluation engineering, and Socratic facilitation — distilled into a hard rule set that can actually be run inside a real conversation, with Layer 0's HP-1~HP-7 acting as the domain ruler that guides designers through locking in every key decision of a Harness-style closed-loop system.
