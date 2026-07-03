# Kano Model Strategist & Feature Pruner

**Classify product features into Kano categories. Cut waste. Build MDP over MVP.**

You have 30 features and 6 weeks. Sort them into Kano's six categories (Must-be, Performance, Attractive, Indifferent, Reverse, Questionable) so you ship the ones that earn their place and cut the rest.

## What it does

This skill turns an unbounded feature wish-list into a tightly prioritized backlog. It actively cuts waste. It prevents **Experience Rot** by saying "no" by default and forcing every feature to justify its existence.

### Core stance

- **Start with NO.** Every new feature is an adopted child you will care for the entire product lifecycle. Default to rejection; require evidence to flip to acceptance.
- **Innovation is added value, not added invention** (attributed to Jared Spool). If a feature does not move a metric a user cares about, it is waste.
- **MDP > MVP.** One Attractive feature that earns 7-day love beats ten Performance features that make the product boring.
- **Must-be is zero-bug territory.** If a Must-be fails, no Attractive feature saves you. Test ruthlessly.

### Priority ladder

```
Must-be (zero bugs)  >  Performance (invest to budget)  >  Attractive (MDP pick)  >  KILL Indifferent
```

Reverse features must be cut or made opt-in. Questionable features need user research before they can be reclassified.

## When to use

- Product backlog triage
- MVP-vs-MDP scoping
- "Should we build this feature" decisions
- Audit a spec for scope creep
- Push back on a stakeholder-pinned low-value feature

Triggers: "kano", "feature pruning", "cut features", "is this a must-have", "is this delight", "ultra-lean backlog review", "MDP vs MVP", "start with NO".

## When NOT to use

- General project management, Gantt charts, scheduling
- Non-feature design decisions (visual polish, copy editing) — those use a different lens
- Market-access prerequisites (compliance, SOC2) — those go in a separate "prerequisites" section, not feature backlog

## Path B evidence

A Path B eval was run on 2026-06-15 (Path B: parallel producer + baseline, 5-point rubric). The with-skill output wins 2 of 5 rubric points (procedural adherence, output contract compliance) and ties 3.

The senior baseline output was already strong. The skill's value is in **consistent output structure**, not in making the model smarter. A junior PM running the skill would get a similar shape; a junior PM running with no skill would not.

Full results in `EVIDENCE.md`.

## Sources

- **Kano, N. (1984).** *Attractive Quality and Must-be Quality.* Hinshitsu (Quality) / *Journal of the Japanese Society for Quality Control*, 14(2), 39–44. The Kano model itself (the idea, the categories, the questionnaire) is a published academic framework and is not copyrightable; only specific *expressions* of it are. The wording in this skill is original.
- **Spool, J.** *Building a Winning UX Strategy Using the Kano Model.* UIE / Centers of Excellence. The quote *"Innovation is not about adding new inventions, it is about adding new value"* and the "Experience Rot" framing are attributed to Spool's UX strategy work. The "Start with NO", the "adopted child" metaphor, and the rot-signal list in this skill are original synthesis.

Full attribution in `ATTRIBUTION.md`.

## Compatibility

- **Tested with:** Claude Sonnet 4.5 (Claude Code), GPT-5.5, MiniMax-m3, GitHub Copilot
- **Designed for:** Claude Code, Codex, VS Code, OpenCode
- **No MCP, no external dependencies**

## What's inside

```
kano-model-strategist/
├── README.md                       ← this file
├── SKILL.md                        ← what the agent loads (procedure, output contract, failure handling)
├── ATTRIBUTION.md                  ← source citations and license chain
├── EVIDENCE.md                     ← Path B eval results
├── LICENSE                         ← MIT
├── SYNCHRONIZATION.md              ← source-of-truth ↔ public copy mapping
└── references/
    ├── kano-classification.md      ← 2-question pair, full category table, edge cases
    ├── kano-vs-mdpmvp.md           ← Kano × MDP × MVP decision logic
    ├── experience-rot-checklist.md ← pruning guardrail
    └── ceo-pushback-scripts.md     ← 4 patterns of stakeholder-pushed Indifferent/Reverse
```

## T-shirt sizing for eng estimates

| Size | Eng-weeks | What it looks like |
|---|---|---|
| **XS** | < 0.5 | A copy change, a config flag, a new setting in an existing screen |
| **S** | 0.5–1 | A new endpoint + minimal UI, or a single well-understood library integration |
| **M** | 1–3 | A new screen, a small new data model, a new permission rule |
| **L** | 3–6 | A new feature area, new infra, new data pipeline, anything with non-trivial edge cases |
| **XL** | 6+ | New platform capability, a new auth model, anything with novel architecture |

State the size, not the exact weeks. State assumptions out loud. Don't pretend you have a precise number when you don't.

## License

MIT — see the `LICENSE` file in this directory. Author: **[Monika Zapisek](https://monikazapisek.com)**. Project: **Design Engineering Playbook**.

---

*Part of the [Design Engineering Playbook](https://github.com/monikazapisekstudio/design-engineering-playbook) — AI-assisted workflow artefacts for product designers working in agile and lean environments.*
