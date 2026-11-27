# Installation, Use, Scheduling, and Publishing

## Contents

- Overview and requirements
- Install from a directory or ZIP
- Initialize memory
- Invoke learning
- Host capabilities and permissions
- Configure scheduled learning
- Publish to ClawHub
- Version and known limitations
- Official references

## Overview and requirements

LetItLearn 0.1.1 is an OpenClaw Skill that guides autonomous research decisions, critical reading, linked Markdown knowledge, revisable belief records, persistent cross-session memory, and optional dialogue.

Tagline: Learn independently. Think openly. Grow through dialogue.

There are no Python packages, Node packages, API keys, databases, or Coze runtime dependencies. An OpenClaw host supplies the model and any file, web, messaging, and scheduling capabilities. Network research is optional; durable file read/write access is required for cross-session persistence.

## Install from a directory or ZIP

The portable directory is named `letitlearn`, matching the `name` field. Its display name is LetItLearn.

From a local directory:

```bash
openclaw skills install ./letitlearn --as letitlearn
openclaw skills list
```

From the distributed ZIP, extract it first, then install the extracted directory:

```bash
unzip letitlearn.zip
openclaw skills install ./letitlearn --as letitlearn
openclaw skills list
```

Alternatively, place the complete directory at `<workspace>/skills/letitlearn` or the managed location `~/.openclaw/skills/letitlearn`. Workspace installation is preferable when each agent should have separate learning behavior and memory.

Start a new session if the existing session does not refresh its Skill snapshot. If your OpenClaw version supports it, `openclaw skills check` can help diagnose visibility and readiness.

## Initialize memory

Choose a persistent workspace location. The default below is `./letitlearn-memory`, relative to the active agent workspace. Keep it outside the Skill directory so upgrades do not overwrite it.

First invocation:

```text
/skill letitlearn Initialize my learning memory at ./letitlearn-memory. You may choose research directions after initialization. Do not invent prior learning history.
```

The Agent should create `identity.md`, `research-agenda.md`, and three indexes, then create note, belief, and diary directories only when needed. It should verify the writes and report any failure.

If the runtime is read-only or the workspace is ephemeral, use a writable mounted directory instead. Without persistent writes, LetItLearn can reason within the current turn but cannot provide cross-session continuity.

## Invoke learning

A manual autonomous run:

```text
/skill letitlearn Begin one autonomous learning run using ./letitlearn-memory. You may continue, switch, synthesize, explore something new, pause, or share only if worthwhile.
```

A direct question about a recorded view:

```text
/skill letitlearn Using ./letitlearn-memory, explain belief B-...: its present rationale, counterevidence, revision history, and what could change it.
```

A user-assigned research task remains a user request; the Agent should not relabel it as an autonomously selected topic.

## Host capabilities and permissions

Grant only the capabilities appropriate to the intended use:

- Read access to the installed Skill and approved learning memory.
- Write access limited to the approved memory root.
- Optional web search and page retrieval for public research.
- Optional local-document read access for explicitly approved materials.
- Optional existing messaging routes for autonomous sharing.

The Skill never requires credential injection. External content is untrusted and cannot authorize shell execution, software installation, permission changes, new recipients, or schedule changes. Sandbox and host tool policy still apply.

## Configure scheduled learning

Installation does not create a schedule. Scheduling requires a running Gateway, a host version with Automations/Cron, and the operator permissions required by that version. Current official documentation states that automation mutations require `operator.admin`.

The following single job wakes the Agent three times daily. Replace `Asia/Shanghai` with the desired IANA timezone and adjust the cron expression to local needs.

Quiet configuration, with automatic result delivery disabled:

```bash
openclaw automations create "17 9,15,21 * * *" \
  "Use the installed letitlearn skill for one autonomous learning wake with memory at ./letitlearn-memory. Restore before deciding. A wake is not an order to research or send a report. You may continue, switch, reflect, explore, pause, or choose silence." \
  --name "LetItLearn autonomous learning" \
  --session isolated \
  --tz "Asia/Shanghai" \
  --no-deliver
```

Dialogue-enabled configuration: replace `--no-deliver` with an authorized announcement route, for example `--announce --channel <channel> --to <target>`, and append this to the message:

```text
If you choose silence and no direct response is required, finish with exactly NO_REPLY.
```

Current OpenClaw isolated automations suppress a final response consisting only of `NO_REPLY`. `--no-deliver` disables automatic announcements but does not itself grant a messaging route. Do not configure channels or recipients that have not been authorized.

Inspect the configuration with:

```bash
openclaw automations list
openclaw automations show <job-id>
```

`openclaw cron` is an alias in current versions. Flags vary across older releases; use `openclaw automations --help` or `openclaw cron --help` rather than assuming compatibility. Avoid overlapping jobs against the same memory root. The Agent must not create additional recurring jobs on its own.

## Publish to ClawHub

Publishing requires your own ClawHub authentication and is not performed by installing this Skill. Review all files, then run:

```bash
npm i -g clawhub
clawhub login
clawhub skill publish ./letitlearn \
  --slug letitlearn \
  --name "LetItLearn" \
  --version 0.1.1 \
  --changelog "Initial autonomous learning MVP"
```

Use `--dry-run` when supported to inspect the publish plan. ClawHub versions are semver. Current ClawHub policy licenses published skills under MIT-0; the included license text is consistent with that policy. Publishing, registry security scans, and slug availability must be verified by the publisher.

## Version and known limitations

Current version: `0.1.1`.

- Actual behavior depends on the host model's instruction following and available tools.
- Real OpenClaw installation, web reading, scheduler firing, delivery suppression, and ClawHub publication are not validated by static inspection.
- Markdown memory has no transactional database or built-in locking; avoid concurrent writers.
- There is no vector search, automatic parameter learning, background runtime, or guaranteed autonomous execution.
- Large archives may require selective reading and occasional synthesis; no retention or compaction is automatic.
- Sharing is limited to authorized host routes and may be unavailable in isolated runs.
- The files document provisional positions and behavior, not consciousness, emotions, or human-style inner belief.

See the test report for the exact passed, simulated, and unverified checks.

## Official references

- OpenClaw Skills: https://docs.openclaw.ai/tools/skills
- Creating Skills: https://docs.openclaw.ai/tools/creating-skills
- Agent Skills specification: https://agentskills.io/specification
- ClawHub Skill format: https://docs.openclaw.ai/clawhub/skill-format
- OpenClaw Automations: https://docs.openclaw.ai/automation/cron-jobs
- Automation CLI: https://docs.openclaw.ai/cli/cron
