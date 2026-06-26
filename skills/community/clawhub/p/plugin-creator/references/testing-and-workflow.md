# Development, Testing, and Validation Workflow

This reference describes a practical workflow for developing OpenClaw plugins inside the OpenClaw repo.

## Base environment

- Node.js 22+
- `pnpm install`
- work from the repo root

## Recommended development flow

### 1. Develop inside the repo when possible

Put the plugin under:

```text
extensions/<plugin-id>/
```

That lets you reuse the repo's build, test, type-check, and bundled-plugin behavior.

### 2. Start the dev environment

Common choices:

- `pnpm gateway:watch`
  - good for continuously watching gateway behavior during development
- `pnpm openclaw gateway restart`
  - good for manual restart-and-verify loops after each change

If there is no global `openclaw` command available, prefer:

```bash
pnpm openclaw <subcommand>
```

When developing plugins, skills, or command interactions locally, split validation into two questions:

- was the plugin loaded?
- can the current session/surface actually use it?

### 3. Prefer scoped tests first

Run the most direct plugin tests before anything broad:

```bash
pnpm test -- extensions/<plugin-id>/
pnpm test -- extensions/<plugin-id>/index.test.ts
```

### 4. Build validation

If the plugin lives inside the OpenClaw repo, run at least one:

```bash
pnpm build
```

This validates more than the plugin itself. It also validates the host build chain, bundled-plugin metadata, and SDK export boundaries.

### 5. Install-package version management

If you are handing the plugin to someone else for installation, or sending a new package to a remote environment, do not reuse an old version.

- update `package.json` version first
- repack
- hand off the new filename explicitly

Minimal recommended packaging step:

```bash
npm pack --pack-destination dist
```

Then treat the newest `dist/<new-package-version>.tgz` as the only valid deliverable.

For cross-machine collaboration, it is best to provide:

- the full tgz path
- the exact version
- a SHA256 or similar checksum

## Most useful validation commands

### Plugin status

```bash
pnpm openclaw plugins inspect <plugin-id>
pnpm openclaw plugins inspect <plugin-id> --json
```

Inspect at least:

- load state (`loaded` / `disabled` / `error`)
- typed hooks
- commands
- tools
- source / origin / shape
- diagnostics

### Install a local plugin

```bash
pnpm openclaw plugins install ./extensions/<plugin-id>
```

In a normal user environment, these also work:

```bash
openclaw plugins install ./my-plugin
openclaw plugins install ./my-plugin.tgz
openclaw plugins install ./my-plugin.zip
```

When installing a specific iteration into a remote environment, prefer an exact file reference:

```bash
openclaw plugins install ./dist/openclaw-<plugin-id>-<version>.tgz
```

Do not say “install the package in dist,” because one `dist/` directory may contain both old and new packages.

### Restart the gateway

```bash
pnpm openclaw gateway restart
```

## Pre-install validation gate

Do not use install as the first validation step.

Before anyone runs `openclaw plugins install ...`, the minimum in-repo gate should be:

1. scoped tests pass
2. `pnpm build` passes
3. the target runtime version is known
4. `pnpm openclaw plugins inspect <plugin-id> --json` shows the expected shape

Recommended order:

```bash
pnpm test -- extensions/<plugin-id>/index.test.ts
pnpm build
pnpm check
pnpm openclaw plugins inspect <plugin-id> --json
```

Use `pnpm check` whenever the touched surface is broader than a small isolated plugin-local change.

## Real conversation-surface verification

If the plugin involves commands, skills, or hooks, do not stop at unit tests. Walk the real interaction path:

1. install or enable the plugin
2. restart the gateway if needed
3. trigger the command or skill on the target surface
4. confirm you get the expected response
5. then inspect plugin telemetry, session logs, and `plugins inspect`

Two important realities:

- a command executing successfully does not guarantee it appears in a menu
- changes to skill/config/tool visibility may not fully appear until a fresh session

## Where to look when behavior does not match expectations

### 1. Start with `plugins inspect`

It answers:

- did the plugin load?
- were the command/tool/hook registrations observed?

### 2. Then inspect session logs

The main OpenClaw agent session logs are usually under:

```text
~/.openclaw/agents/main/sessions/*.jsonl
```

Look for:

- whether the model really saw the skill
- whether the tool call was actually emitted
- what the stop reason was

If the problem is “why does the skill command look like a normal prompt,” check these first:

- `docs/tools/skills.md`
- `src/auto-reply/reply/get-reply-inline-actions.ts`

### 3. Then inspect `systemPromptReport` in `sessions.json`

Look for:

- the real tool list exposed to the agent during that run

This is especially important for debugging “the tool is registered, but the model says it is unavailable.”

### 4. Then inspect tool policy and command visibility

Confirm at least:

- `tools.profile`
- `tools.alsoAllow` / `tools.allow`
- `commands.native`
- `commands.nativeSkills`
- whether the current surface supports native command display

## Recommended test checklist

### For a tool

- unit-test `execute(...)`
- then verify that it really enters the agent tool set

### For a command

- unit-test the handler output
- then send the real `/command ...`

### For a plugin skill

- verify the skill loads
- verify `/skill <name>` or the generated command can trigger it
- verify whether the path is a core skill rewrite or deterministic tool dispatch
- verify the tool is truly present in the run's tool set

### For a hook

- unit-test the hook logic
- then verify the real runtime trigger path

## Final bar

For in-repo plugin development, try to reach at least this bar:

1. scoped tests pass
2. `pnpm openclaw plugins inspect <id>` looks correct
3. one real-surface verification passes
4. `pnpm build` passes
