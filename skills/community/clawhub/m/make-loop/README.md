# make-loop · Turn a plain-language task into an AI agent loop brief

[English](README.md) | [简体中文](README.zh-CN.md)

make-loop is an agent skill that turns a plain-language task into an AI agent loop brief with checkable goals, a per-round process, evidence, logs, and stop conditions, so an agent can keep iterating without being walked through every round.

## Who it's for

People who use Claude Code, Codex, Cursor, or another AI agent supported by `npx skills` and want an agent to iterate a task without being walked through every round — polishing a product, playtesting a game, reviewing and fixing a batch of changes — but do not want to write the loop instructions themselves.

## Why try it now

A vague "keep going until it's good" leaves the usual holes: a goal you cannot check ("looks better"), a "try it" that only reads the code, a pass with no evidence, no log, and a stop condition the model gets to call. The before-and-after in [references/examples.md](references/examples.md) rewrites a two-player side-scroller loop to close those holes.

This skill fills them in for you: checkable goals, real use (not inferred from the code), evidence for every pass, independent review with a shared rubric, a human look at before-and-after, and a full set of brakes (done, stuck, no progress, thrashing, a cap, and pause) that behave differently for attended vs unattended runs. Spending and irreversible actions go on a red line. By default it only writes the brief; it does not start the loop until you clearly ask it to run in this session and confirm the scope.

## Install

### Option 1 — **Command**

Installs the skill into `.agents/skills/make-loop` in the current project. Add `-y` in a non-interactive terminal if needed.

```bash
npx skills add https://github.com/Ekko237/make-loop --skill make-loop
```

### Option 2 — **Prompt**

Paste this into Claude Code, Codex, Cursor, or another supported agent to run make-loop on demand without installing it:

```text
Run `npx skills use "https://github.com/Ekko237/make-loop" --skill "make-loop"` and follow the generated skill instructions now. Read its complete output, redirecting it to a temporary file first if necessary. Resolve relative paths from the supporting-files directory it provides.
```

[Examples](references/examples.md) · [Template](references/template.md) · [Checklist](references/checklist.md) · [Report an issue](https://github.com/Ekko237/make-loop/issues) · [ClawHub](https://clawhub.ai/ekko237/skills/make-loop)

If it helps, a ★ Star helps others find it.

## Requirements

The top-level Command and Prompt paths require `git` and Node.js with `npx`, and work with Claude Code, Codex, Cursor, and other agents supported by `npx skills`.

The legacy `install.sh` script under Other install methods requires `~/.claude` or `~/.codex` already present, plus a Unix-like shell with `git`, `bash`, and `rsync`.

## Quick use

After installation, open Claude Code, Codex, Cursor, or another supported agent and use `/make-loop` or a natural-language trigger such as "turn this into a loop" or 「帮我变成 loop」. You can also use the Prompt option above. Documented trigger phrases also include 「做成循环」, 「写个 loop」, 「让它自己一轮一轮改到好」, 「反复迭代直到没问题」, and 「让它一直跑」. You should get a complete loop brief in a code block, ready to copy into a new session, plus a short note on the defaults it filled in, which switches it picked (attended vs unattended; batch vs small steps), and the key stop conditions. It does not start running the loop unless you clearly ask it to execute in this session and confirm the scope.

A minimal prompt:

```
/make-loop Make a one-page personal site. It should work on a phone, have my name and a short bio, and load without a build step.
```

A full before-and-after rewrite (a two-player side-scroller) is in [references/examples.md](references/examples.md). The fill-in template is [references/template.md](references/template.md). The pre-delivery checklist is [references/checklist.md](references/checklist.md).

## When not to use it

- Not for a one-shot task with no iteration (a single edit, a single answer). This skill writes a loop: goal, repeated process, checks, logs, and stop conditions.
- It does not supply the domain knowledge for the task itself. That comes from the conversation and your other skills.
- By default it only writes the brief. If you needed the agent to start work in the same turn without a written loop, this is the wrong tool unless you also clearly ask it to run the brief and confirm the scope.
- The `install.sh` script specifically needs `~/.claude` or `~/.codex` already present. It exits if neither directory exists; the `npx skills` Command and Prompt options work with Claude Code, Codex, Cursor, and other supported agents instead.

## Compared with alternatives

| | Writing the loop prompt yourself | Saying "keep iterating until it's good" | make-loop |
| --- | --- | --- | --- |
| How you start | You already know how to specify goals, evidence, review, and stops | One sentence to the agent | Install the skill, then say "turn this into a loop" or `/make-loop` plus the task |
| What you get | Whatever you remember to include | A loose instruction the agent interprets | A complete brief from the [template](references/template.md): three parts (goal, process, check-and-iterate) covering five items (the goal, each-round actions, how to check, what to log, when to stop), checked against the [checklist](references/checklist.md) |
| Common holes | Easy to skip evidence, real use, logs, or a cap | As in the before-example in [examples.md](references/examples.md): "until there are no more comments" lets the agent stop early; "whether the design is sound" cannot be checked; "try it" may only read the code | Fills those in: checkable goals, real use with evidence, logs on disk, six stop conditions, attended vs unattended brakes, and a red line for spending and irreversible actions |
| Does it start the work | You decide | Often the agent starts immediately | By default it only writes the brief. It starts the loop only when you clearly ask it to run in this session and confirm the scope |

## What's in a brief

A loop has three parts, which break down into five items:

| Part | The five items | In one line |
| --- | --- | --- |
| **Goal**: what to make | 1. What the goal is | What "good" means, in terms you can check |
| **Process**: how to work | 2. What each round does | Ship a first version, then repeat a fixed set of actions |
| **Check and iterate** | 3. How to check · 4. What to log · 5. When to stop | Check with evidence, keep a log, and have brakes |

Two switches are set from what you said, with defaults if that is unclear: **attended vs unattended** (default: unattended — if stuck, park it and do something else; stop only on a deadline, a pause from you, or a dead end) and **batch vs small steps** (default for work that has a review: one full list of issues, then one pass of fixes, then review again).

The brief is delivered in a code block you can paste into a new session. If the task lives in a project folder, a copy can also be saved there (for example `LOOP_BRIEF.md`) and should not be committed to a public repository. After the code block, the skill explains in a few lines which defaults it filled in, which switches it picked, and the key brakes. Domain knowledge for the task itself still comes from the conversation and your other skills.

## Other install methods

The pinned v1.0.2 release can also be installed by cloning it:

```bash
git clone --branch v1.0.2 https://github.com/Ekko237/make-loop.git && cd make-loop && bash install.sh
```

The current release is [v1.0.2](https://github.com/Ekko237/make-loop/releases/tag/v1.0.2).

`install.sh` detects `~/.claude` and `~/.codex` and installs into each one it finds. `bash install.sh claude` or `bash install.sh codex` installs to only one of them. If the target already has a same-named skill that was not installed by this script, the script backs that directory up in full and stops without overwriting it; add `--force` only when you mean to replace it. If a previous run failed after creating the destination folder (for example because `rsync` was missing), the next run may treat that empty folder as an existing skill and stop; add `--force`, or remove the empty `~/.codex/skills/make-loop` or `~/.claude/skills/make-loop` directory, then run the installer again. `install.sh` requires `~/.claude` or `~/.codex` already present and a Unix-like shell with `git`, `bash`, and `rsync`; it does not install through the `npx skills` Command or Prompt paths. If neither `~/.claude` nor `~/.codex` exists, the script exits and tells you to install Claude Code or Codex first. This repository does not document a Windows install for `install.sh`. `install.sh` copies this repository's files (except `install.sh`, `.git`, and `.DS_Store`) into `~/.claude/skills/make-loop` and/or `~/.codex/skills/make-loop`. It does not use the network or install any dependencies.

## Community

Tried it? [Open an issue](https://github.com/Ekko237/make-loop/issues) and tell me what broke or what you made. Issues and pull requests are welcome.

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/Ekko237/make-loop?style=flat&color=24292f" alt="MIT license" /></a>
  &nbsp;
  <a href="https://github.com/Ekko237/make-loop/releases/tag/v1.0.2"><img src="https://img.shields.io/github/v/tag/Ekko237/make-loop?style=flat&color=24292f" alt="Latest tag v1.0.2" /></a>
</p>

MIT, see [LICENSE](LICENSE).
