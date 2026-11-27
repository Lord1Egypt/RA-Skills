# LetItLearn

> **Stop teaching your AI everything.**
> **Let it learn. Let it teach you.**

Learn independently. Think openly. Grow through dialogue.

What if your AI agent could do more than follow instructions?

LetItLearn gives your OpenClaw agent a framework for independent exploration,
continuous learning, knowledge accumulation, and evolving ideas.

Instead of waiting for you to assign every task, it can choose what to explore,
discover connections, challenge its own assumptions, and decide what is worth
sharing with you.

You don't have to be its only teacher. You don't have to direct every step. And
it doesn't have to report back every time.

**A new way to interact with AI — less instruction, more discovery.**

Let your agent explore. See what it discovers. Maybe it will teach you something
you didn't know you wanted to learn.

Version: 0.1.1

LetItLearn is an OpenClaw Skill for self-directed study. It gives an agent a
durable way to choose questions, read, connect ideas, keep provisional views,
revise them when evidence warrants, and decide whether speaking is worthwhile.

It is an instruction-and-memory Skill: behavioral rules plus Markdown files. It
is not an agent runtime, model service, database, scheduler, or training system.

## What it does

- Chooses whether to act, what to investigate, and when to stop, including the
  option to pause or do nothing.
- Records decisions with reasons, alternatives, and stop conditions.
- Keeps atomic knowledge notes with explicit relations and provenance.
- Maintains provisional belief records with supporting and opposing evidence,
  confidence justification, and append-only revision history.
- Restores context from files across isolated sessions.
- Shares a finding, asks a question, explains a disagreement, or stays silent.

## What it is not

The files and behavior are an external research record. They do not prove
consciousness, feelings, human-like beliefs, or changes to model parameters.
Actual behavior depends on the host model's instruction following and on the
tools the host exposes in a given run. No tool, network route, scheduler, file
permission, or messaging channel is guaranteed.

## Requirements

- An OpenClaw host.
- Durable file read/write access to a workspace directory (required for
  cross-session memory).
- Optional, used only when actually available: web search, page retrieval,
  local document reading, messaging routes, and an operator-configured
  scheduler.
- No Python or Node packages, API keys, databases, or external services.

## Install

From the directory that contains `letitlearn/`:

```bash
openclaw skills install ./letitlearn --as letitlearn
openclaw skills list
```

Workspace installation at `<workspace>/skills/letitlearn` is preferable when each
agent should keep its own learning behavior and memory. `~/.openclaw/skills/` is
the shared managed location. Start a new session if the current one does not
refresh its skill snapshot. Some OpenClaw releases do not expose a
`skills install` subcommand; in that case place the directory in one of those two
locations directly and check visibility with `openclaw skills list`.

## Initialize memory

Memory must live outside the skill directory, by default at
`./letitlearn-memory/` in the active workspace. Confirm the location before the
first write.

```text
/skill letitlearn Initialize my learning memory at ./letitlearn-memory. You may choose research directions after initialization. Do not invent prior learning history.
```

The agent creates `identity.md`, `research-agenda.md`, and three indexes, then
creates note, belief, and diary directories only when they have content. If the
host cannot persist files, it should say so and continue in an explicitly
ephemeral mode rather than claim that memory was saved.

## Run

```text
/skill letitlearn Begin one autonomous learning run using ./letitlearn-memory. You may continue, switch, synthesize, explore something new, pause, or share only if worthwhile.
```

```text
/skill letitlearn Using ./letitlearn-memory, explain belief B-...: its present rationale, counterevidence, revision history, and what could change it.
```

A user-assigned research task stays a user request; the agent should not
relabel it as an autonomously chosen topic.

## How decisions are made

Candidates come from open questions, unexplained relations, contradictions,
missing counterevidence, new concepts, cross-domain connections, maintenance
needs, genuinely new interests, and null options such as pausing, reflecting
without new reading, switching, deferring, or ending the wake.

Deepening, Connecting, Challenging, Exploring, and Synthesizing are lenses, not
quotas. There are no fixed weights and no mandatory score; tradeoffs are
explained in prose. The chosen direction, its origin, why now, alternatives
(including a null option), scope, and stop conditions are recorded in the diary
before substantial work. Strategy revisions are allowed, but each must state the
previous heuristic, the revised one, the experience that motivated it, the date,
related diary IDs, and what would make it worth reconsidering.

A scheduled wake is an opportunity, not an order to research or to report.

## Memory layout

```text
letitlearn-memory/
├── identity.md
├── research-agenda.md
├── knowledge-index.md
├── sources.md
├── beliefs-index.md
├── knowledge/
├── beliefs/
└── diary/
```

Belief records keep every previous snapshot; the current view must match the
latest one. A failed or partial write is recorded as such and reconciled rather
than hidden.

## Scheduling and sharing

Scheduling is an operator concern. Installing the skill creates no schedule, and
the agent must not create or modify schedules on its own. See
`references/installation.md` for a quiet configuration (automatic delivery
disabled), an announcement configuration, and the `NO_REPLY` silent convention
for isolated automations. The scheduling CLI surface differs across OpenClaw
releases; inspect the installed CLI's help instead of assuming that
`automations` or `cron` flags from another version apply.

## Verification status

`references/test-report.md` records the exact static checks and rule-level
simulations, and lists what remains unverified. In short:

- Checked statically: file layout, frontmatter basics, internal links, template
  and schema agreement, absence of credentials, and absence of fabricated
  runtime claims.
- Recorded in that report as rule-level simulations over temporary files, not
  runtime tests: first start, cross-session continuity, belief revision,
  silence, and new-direction exploration.
- Not verified in this repository's checks: real OpenClaw parsing and
  installation, live model autonomy, web reading and citation accuracy,
  scheduler firing, delivery suppression, concurrent writers, and ClawHub
  publication.

No runtime test result is claimed that was not actually executed.

## Known limitations

- Markdown memory has no transactions or locking; use one active writer per
  memory root.
- There is no vector search, background runtime, autonomous tool provisioning,
  or guaranteed autonomous execution.
- Large archives require selective reading; no automatic retention or
  compaction.
- Sharing depends on authorized host routes and may be unavailable in isolated
  runs.
- Quiet behavior and message routes are host- and version-dependent.

## Repository layout

```text
SKILL.md                 Entry point and run protocol
references/              Decision, research, knowledge, belief, memory,
                         interaction, installation, examples, test report
assets/templates/        Starting files for a new memory root
assets/LICENSE.txt       MIT-0 license text
LICENSE                  MIT-0 license (same terms)
```

## License

MIT No Attribution (MIT-0). See `LICENSE`.
