# Proof Loop

![Tests](https://github.com/LeoStehlik/proof-loop/actions/workflows/test.yml/badge.svg)

**Make AI coding agents prove when work is done.**

Proof Loop is a repo-local verification protocol for AI coding agents. It freezes acceptance criteria before the build, separates builder and verifier roles, records durable proof artifacts in the repo, and refuses to call work done until every acceptance criterion has a fresh PASS verdict.

Use it when an agent, team, or multi-agent sprint needs a clear boundary between “looks done” and verified work. Because the protocol is just files plus role discipline, it works with OpenClaw, Hermes, Codex, OpenCode, Claude Code, or any other harness that can read and write a repository.


## Activation and Safety

Use Proof Loop when the user explicitly wants an evidence-gated coding sprint, frozen acceptance criteria, fresh verifier separation, or durable proof artifacts. It is not meant to silently wrap every code change.

The bundled helpers create and check repo-local files under `.agent/tasks/<TASK_ID>/`. Review the task id and repository root before running them. Publishing reports, using remote workers, changing permissions, or running elevated commands are outside this skill unless requested separately.

## Use Cases

- keep AI coding agents honest when they claim a task is done
- freeze acceptance criteria before implementation starts
- separate builder and verifier roles in multi-agent coding work
- leave proof artifacts in the repo for future review

![Animated terminal demo: Proof Loop doctor, check, and report commands](assets/proof-loop-terminal-demo.svg)

Proof artifacts and role-brief examples are indexed in [`examples/README.md`](examples/README.md).

## 20-second demo

```bash
git clone https://github.com/LeoStehlik/proof-loop.git
cd proof-loop
make test

tmp=$(mktemp -d)
bin/proof-loop-init hn-demo --title "Prove this task before done" --root "$tmp"
bin/proof-loop-check "$tmp/.agent/tasks/hn-demo"
```

The last command fails on purpose because the generated task has not been verified yet. Proof Loop only returns success after a fresh verifier records `PASS` for every acceptance criterion and `problems.md` is empty.

A completed passing example is included:

```bash
bin/proof-loop-check examples/example-task/.agent/tasks/ui-language-fix
bin/proof-loop doctor
bin/proof-loop report examples/demo-repo/.agent/tasks/nav-labels-proof --format md
```

## Why It Exists

AI coding agents often fail in predictable ways:

- they claim completion without durable proof
- the same session builds and judges its own work
- acceptance criteria drift while implementation is underway
- verification is a prose summary instead of a live check
- future sessions cannot tell what was actually tested

Proof Loop makes completion auditable. A task is done only when a fresh verifier has checked each AC and the repo contains the artifacts to prove it.

## What You Get

- a clear sprint protocol: spec freeze -> build -> evidence -> fresh verify -> fix loop
- role boundaries for orchestrator, spec-freezer, builder, verifier, and fixer
- helper scripts to initialize and check task proof folders
- a complete example task with passing artifacts
- copy-paste role briefs for OpenClaw, Hermes, Codex, OpenCode, Claude Code, or any agent setup
- a documented boundary with Loopsmith for recurring behaviour improvement

## CLI

```bash
bin/proof-loop init TASK_ID --title "Task title"
bin/proof-loop check TASK_ID
bin/proof-loop status TASK_ID
bin/proof-loop list
bin/proof-loop doctor
bin/proof-loop report TASK_ID --format md
bin/proof-loop install-guides --dry-run --harness codex --harness claude
```

## Quick Start

Clone the repo or copy it into the project where you want to run the protocol.

Create a task proof folder from this repo or from another repository:

```bash
bin/proof-loop-init ui-language-fix --title "Fix German navigation labels" --root .
```

This creates:

```text
.agent/tasks/ui-language-fix/
  spec.md
  verdict.json
  problems.md
  evidence.md
```

Fill `spec.md` with explicit acceptance criteria before implementation starts.

After the build and verifier pass, check whether the task is allowed to be called done:

```bash
bin/proof-loop-check .agent/tasks/ui-language-fix
```

The check exits non-zero unless:

- `verdict.json` has `overall: PASS`
- every AC has `status: PASS`
- `problems.md` is empty or absent


## What This Is Not

- not an agent framework
- not a benchmark suite
- not a replacement for tests
- not tied to one model, vendor, or harness

Proof Loop is deliberately small: a protocol, a few files, and a mechanical done gate.

## The Protocol

```text
spec freeze -> build -> evidence -> fresh verify -> fix -> fresh verify
                                         ^                    |
                                         |____________________|
                                      repeat until all ACs PASS
```

## Roles

| Role | Does | Never |
|---|---|---|
| Orchestrator | Keeps the loop intact and refuses weak completion | Accepts narrative-only proof |
| Spec-Freezer | Writes frozen `spec.md` with explicit ACs | Edits production code |
| Builder | Implements against the frozen spec | Verifies own work as final |
| Verifier | Fresh session that checks each AC | Edits production code |
| Fixer | Applies minimal fixes for verifier findings | Signs off on completion |

The verifier must be a fresh session. The agent that built the change does not judge whether the change is done.

## Acceptance Criteria

Good ACs are specific and testable by a third party.

```text
AC1: A user with locale=de sees all navigation labels in German after saving language preference.
     Verify: browser check against a German-locale test user.

AC2: The language preference survives page reload.
     Verify: reload the page and confirm the saved locale and labels remain German.

AC3: Existing English navigation remains unchanged for locale=en.
     Verify: switch back to English and confirm the original labels render.
```

Weak ACs are task descriptions, not proof conditions:

```text
AC1: Translate the UI.
AC2: Make language switching work.
AC3: Fix the bugs.
```

## Artifacts

Every task stores proof under `.agent/tasks/<TASK_ID>/`.

```text
.agent/tasks/<TASK_ID>/
  spec.md       frozen ACs, constraints, non-goals, verification approach
  evidence.md   build summary and checks run
  verdict.json  structured verifier result: PASS / FAIL / UNKNOWN per AC
  problems.md   specific open failures, empty when no problems remain
```

See [`references/artifacts.md`](references/artifacts.md) for schemas.

## Real Demo

Run a small failing-to-passing demo:

```bash
make demo
```

The demo intentionally breaks a tiny navigation-label fixture, shows the check failing, applies the fix, reruns the check, and renders a proof report.

## Examples

A complete passing example lives at:

```text
examples/example-task/.agent/tasks/ui-language-fix/
```

Role prompts live at:

```text
examples/role-briefs/
  orchestrator.md
  spec-freezer.md
  builder.md
  verifier.md
  fixer.md
```

## Proof Loop vs Loopsmith

Proof Loop governs a single task.

Loopsmith improves repeated agent behaviour over time.

Use Proof Loop when you need a specific task to finish with evidence. Use [Loopsmith](https://github.com/LeoStehlik/loopsmith) when the same failure pattern keeps coming back and you want to improve the agent, prompt, policy, or evaluator itself.

See [`references/loopsmith-bridge.md`](references/loopsmith-bridge.md).


## When To Use Which Repo

Use this repo when a specific coding task needs evidence before anyone is allowed to call it done. Proof Loop freezes the spec, separates builder and verifier roles, requires proof artifacts, and records verdicts in the repo.

Use the neighbouring tools at different points in the workflow:

| Need | Use |
| --- | --- |
| Turn a fuzzy request into an executable agent brief | [Brief Master](https://github.com/LeoStehlik/brief-master) |
| Prove one coding task is actually done | [Proof Loop](https://github.com/LeoStehlik/proof-loop) |
| Improve repeated agent behaviour with evals | [Loopsmith](https://github.com/LeoStehlik/loopsmith) |
| Keep source-backed memory for long-running agents | [Sovereign Brain](https://github.com/LeoStehlik/decoupled-agent-memory) |
| Stop frontend agents producing generic UI sludge | [no-slop-ui](https://github.com/LeoStehlik/no-slop-ui) |

A practical chain looks like this: messy request -> Brief Master brief -> Proof Loop task -> Loopsmith eval if the same failure keeps recurring -> Sovereign Brain records the durable decision.

## Related Tools

- [Loopsmith](https://github.com/LeoStehlik/loopsmith) - use when Proof Loop exposes a repeated agent behaviour problem that should become an eval and promotion loop.
- [Sovereign Brain](https://github.com/LeoStehlik/decoupled-agent-memory) - source-backed memory for long-running agents; useful when proof artifacts, decisions, and synthesis need durable context.
- [Brief Master](https://github.com/LeoStehlik/brief-master) - helps write sharper task briefs and acceptance criteria before a Proof Loop starts.

## Installation As A Skill

### OpenClaw

Add your skills directory to `openclaw.json`:

```json
{
  "skills": {
    "load": {
      "extraDirs": ["/path/to/your/skills"]
    }
  }
}
```

Clone this repo into that directory:

```bash
git clone https://github.com/LeoStehlik/proof-loop.git /path/to/your/skills/proof-loop
```

### Codex / Claude Code

Copy the `proof-loop` folder into your agent skills directory, or reference `SKILL.md` directly in your task brief. For harnesses without a formal skill system, use the README, role briefs, and scripts directly from the repo.

## Repository Map

```text
proof-loop/
  SKILL.md                         skill trigger and core operating rules
  bin/
    proof-loop                     unified CLI
    proof-loop-init                compatibility wrapper
    proof-loop-check               compatibility wrapper
  scripts/
    init_task.py                   create .agent/tasks/<TASK_ID>/ skeletons
    check_task.py                  mechanical done gate
  schemas/                         JSON schemas for verdict and evidence bundles
  templates/                       opt-in harness guide templates
  tests/                           stdlib unittest coverage for CLI behavior
  .github/workflows/test.yml       CI running make test
  references/
    workflow.md                    full phase-by-phase protocol
    brief-template.md              reusable sprint and role prompts
    artifacts.md                   artifact schemas
    loopsmith-bridge.md            when to escalate repeated failures to Loopsmith
  examples/
    example-task/                  complete passing proof artifact example
    role-briefs/                   copy-paste role prompts
```

## Status

Usable protocol skill and small toolkit. The scripts are intentionally stdlib-only so they can run inside almost any repository without packaging ceremony.

## License

MIT - see [LICENSE](LICENSE).

## Attribution

Inspired by [`repo-task-proof-loop`](https://github.com/DenisSergeevitch/repo-task-proof-loop), adapted for practical multi-agent coding work and public agent-operation skills.
