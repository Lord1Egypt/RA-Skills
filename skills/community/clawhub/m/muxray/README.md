# muxray — OpenClaw skill

Teaches an OpenClaw agent how and when to use [`muxray`](https://github.com/dandriscoll/muxray)
to inspect tmux panes: snapshot output, diff against a previous capture, and
classify the program + state of terminal coding agents (Claude Code, Codex,
Copilot) — one pane or the whole fleet.

This is a standard SKILL.md skill (the [AgentSkills](https://agentskills.io)
format OpenClaw follows). It does **not** bundle the `muxray` binary — see
"Why the binary isn't bundled" below.

## Layout

```
muxray/
├── SKILL.md                     # frontmatter + agent instructions
├── README.md                    # this file
├── scripts/
│   ├── muxray-run.sh            # validating front door (fixed subcommands, checked args)
│   └── muxray-watch-diff.sh     # snapshot → wait until settled → diff (one pane)
├── references/
│   └── json-contract.md         # compact field/state cheat-sheet
└── examples/
    └── inspect-agent.md         # worked end-to-end example
```

## Requirements / gating

The skill gates on `metadata.openclaw` so it only loads where it can work:

- `requires.bins: ["muxray", "tmux"]` — both must be on `PATH`.
- `os: ["darwin", "linux"]` — muxray reads tmux, which is POSIX-only.
- `install` spec: `go install github.com/dandriscoll/muxray/cmd/muxray@latest`.

Per the OpenClaw docs, `requires.bins` is checked on the **host** at load time;
if the agent runs in a sandbox, `muxray` (and `tmux`) must also exist **inside
the container** (install via `agents.defaults.sandbox.docker.setupCommand` or a
custom image).

### Why the binary isn't bundled

`muxray` is a compiled, platform-specific Go binary. Bundling one platform's
build into a skill that may load on darwin or linux (and in or out of a sandbox)
would ship the wrong artifact half the time. The idiomatic OpenClaw pattern for
CLI-backed skills (e.g. `blucli`, `gog`) is to **gate on the binary and provide
an `install` spec** instead — which is what this skill does. Install paths:

```bash
go install github.com/dandriscoll/muxray/cmd/muxray@latest   # matches the skill's install spec
# or the project installer / a GitHub release:
curl -fsSL https://raw.githubusercontent.com/dandriscoll/muxray/main/install.sh | sh
```

## Install the skill

This skill ships from `skills/muxray/` inside the muxray repo. Two supported
channels:

```bash
# Local checkout (development / direct use):
openclaw skills install ./skills/muxray --as muxray

# ClawHub (published registry — the primary distribution channel):
openclaw skills install muxray
```

> Git-shorthand install (`openclaw skills install git:dandriscoll/muxray`) is
> **not** supported for this skill: OpenClaw's git install reads `SKILL.md` from
> the **repo root** and has no subdirectory form (verified in
> `src/skills/lifecycle/source-install.ts`). The skill lives at `skills/muxray/`
> to keep it out of this Go binary project's root, so use the local-path or
> ClawHub channel above.

## Local testing

```bash
# 1. Confirm the skill loaded (start a fresh session if you were mid-chat):
openclaw skills list            # muxray should appear; gated off if muxray/tmux absent

# 2. Trigger it by intent:
openclaw agent --message "use muxray to inspect my tmux sessions"
openclaw agent --message "with muxray, show me what changed in pane work:1.0 since the last snapshot"
openclaw agent --message "summarize what the coding agent in tmux pane work:1.0 is doing"

# 3. Invoke explicitly by name:
openclaw agent --message "/skill muxray status of every pane"
```

If `openclaw skills list` doesn't show it, the gate likely failed — check that
both `muxray` and `tmux` are on `PATH` and you're on darwin/linux. `muxray
doctor` reports environment readiness.

## Safety

- The agent is taught to call **fixed read-only subcommands** with explicit
  flags — never an interpolated shell string.
- `scripts/muxray-run.sh` is the safe front door: it allowlists the read-only
  subcommands (`list scan status snapshot diff inspect watch doctor`), validates
  every `--pane`/`--session` target against a strict charset (rejecting spaces,
  `;`, backticks, and leading `-`), and execs `muxray` through an argv array.
  It deliberately does **not** expose `update`/`telemetry`/`bundle`/`shim`.
- muxray is read-only and does no network egress (except the explicit
  `muxray update`); pane content never leaves the machine.
- Pane text can contain secrets. The skill instructs the agent to summarize or
  redact obvious secrets and to report classifications rather than raw dumps.

## Publishing to ClawHub

Per the OpenClaw docs:

1. Ensure `SKILL.md` `name`, `description`, and `metadata.openclaw` gating are
   complete (they are), and `homepage` is set (it is).
2. Install the publishing skill: `openclaw skills install clawhub-publish`.
3. Publish: `clawhub publish` (or `clawhub sync --all`).

Do not add marketplace metadata OpenClaw does not define — only the documented
`metadata.openclaw` keys are used.
