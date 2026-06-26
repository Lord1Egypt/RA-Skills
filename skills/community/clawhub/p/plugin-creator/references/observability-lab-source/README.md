# Observability Lab

This is an experimental scaffold for OpenClaw plugin development.

It bundles four capabilities into one minimal but complete example:

- a plugin-shipped skill
- a plugin slash command
- typed hooks
- a deterministic tool

The goal is not to be a production plugin. The goal is to give future plugin work a clear, extensible, and verifiable directory structure.

## Directory structure

```text
observability-lab/
├── commands/          # slash command handlers
├── hooks/             # hook registration and logic
├── skills/            # plugin-shipped skills
├── src/               # shared config, state, async persistence helpers
├── tools/             # deterministic plugin tools
├── api.ts             # local barrel over official plugin-sdk surfaces
├── index.ts           # plugin entrypoint, assembly only
└── openclaw.plugin.json
```

## Slash commands vs skills

If the goal is “run a piece of plugin logic,” prefer a slash/native command.

Typical examples:

- read status
- flip a switch
- modify plugin config
- trigger local logic

If the goal is “inject a reusable prompt, template, or operating instruction,” prefer a skill.

In this plugin:

- `/observe ...` is a real plugin command handled by code
- `/observe_demo <text>` is the generated command alias for the `observe-demo` skill
- `/skill observe-demo <text>` is the generic skill entrypoint

Useful shorthand:

- if you only want prompt guidance, use a skill
- if you need side effects or plugin logic, use a slash/native command

## What this plugin demonstrates

### Commands

- `/observe status`
- `/observe on`
- `/observe off`
- `/observe rewrite on`
- `/observe rewrite off`
- `/observe prefix [text]`
- `/observe_tail`
- `/observe_help`

### Skill

- `/observe_demo <text>`
- `/skill observe-demo <text>`

`observe-demo` is useful for install validation because it exercises the skill → agent reasoning → tool call path.

That means:

- `/observe_demo <text>` is still the skill command entrypoint
- but it no longer directly maps the command to a tool
- the agent reads the skill first, then decides to call `observe_demo_echo`

That makes it a better example of “a plugin-shipped skill teaching the agent to call a tool.”

### Hooks

Currently registered hooks:

- `message_received`
- `llm_input`
- `llm_output`
- `before_tool_call`
- `after_tool_call`
- `before_message_write`
- `session_start`
- `session_end`

### Session-scoped activation

This plugin does not record every message by default. Instead:

1. the user first calls a plugin command or skill in the current session
2. the plugin detects that activation point
3. from that moment onward, later message / LLM / tool / transcript events are recorded
4. the active state is cleared automatically when the session ends
5. a new session does not inherit the previous session's activation state

That gives you a clean “only observe sessions that actually used this plugin” semantic.

## Telemetry output

Telemetry enters an in-memory queue first, then flushes asynchronously to runtime data under:

```text
~/.openclaw/plugins/observability-lab/telemetry.jsonl
```

## Install methods

### Method 1: install from a local source directory

```bash
openclaw plugins install ./extensions/observability-lab
```

If you are developing inside the OpenClaw repo, this also works:

```bash
pnpm openclaw plugins install ./extensions/observability-lab
```

### Method 2: install from an archive

The plugin installer supports local directories and archives, including:

- `.tgz`
- `.tar.gz`
- `.tar`
- `.zip`

Examples:

```bash
openclaw plugins install /path/to/observability-lab.tgz
openclaw plugins install /path/to/observability-lab.zip
```

## Is `pnpm build` required?

For end users installing the packaged plugin, usually no.

Why:

- OpenClaw can install plugins from directories or archives
- the plugin loader can load plugin entrypoints from source form
- the install flow can place plugin code under `~/.openclaw/extensions/...`

Important caveat:

- if the plugin declares runtime dependencies, the installer runs `npm install --omit=dev --ignore-scripts` inside the plugin install directory

So:

- “send someone a zip and let them run `openclaw plugins install xxx.zip`” is a valid delivery model
- but machines still need the ability to install any declared runtime dependencies

The important distinction is:

- `~/.openclaw/extensions/...` is the installed plugin code location
- `~/.openclaw/plugins/...` is plugin-owned runtime data

### Why run `pnpm build` during development?

Because this plugin lives under `extensions/observability-lab/` inside the OpenClaw repo.

Inside the repo, `pnpm build` validates:

- that the host repo build still works
- that bundled-plugin metadata and the build chain still hold together
- that this scaffold is compatible with the host build flow used by modern OpenClaw releases

So the practical rule is:

- plugin author developing inside the host repo: run `pnpm build`
- end user installing a packaged plugin: prefer `openclaw plugins install <directory-or-archive>`

## Quick verification

1. install the plugin
2. restart the gateway if needed
3. run `/observe status`
4. run `/observe_demo test`
5. run `/observe rewrite on`
6. optionally run `/observe prefix [audit] `
7. send a normal message such as `hi`
8. run `/observe_tail`
9. inspect `~/.openclaw/plugins/observability-lab/telemetry.jsonl`

## SDK constraints

This plugin intentionally depends only on official plugin SDK surfaces:

- `openclaw/plugin-sdk/plugin-entry`
- `openclaw/plugin-sdk/plugin-runtime`

`api.ts` is only a local forwarding layer to keep imports tidy. It is not a private SDK wrapper.
