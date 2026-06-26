# Pitfalls and Debugging Guide

This reference records the places where agents most often think they understand the plugin model but still get it wrong.

## Pitfall 1: a registered tool is not automatically usable by the agent

This is the most common and highest-impact mistake.

### Symptom

- `api.registerTool(...)` ran successfully
- `openclaw plugins inspect <id>` shows the tool
- but the skill or agent still says the tool is unavailable

### Root cause

The actual runtime tool set is filtered again by tool policy.

In local development, a common source of confusion is:

- `tools.profile: "coding"`

That profile is a base allowlist. It does not automatically include plugin tools.

Key source entrypoints:

- `src/agents/tool-catalog.ts`
- `src/agents/pi-tools.ts`
- `src/agents/tool-policy-pipeline.ts`

### Correct handling

If you are already using a base profile such as `tools.profile: "coding"` and want to add plugin tools on top, prefer:

```json
{
  "tools": {
    "profile": "coding",
    "alsoAllow": ["<plugin-id-or-tool-name>"]
  }
}
```

Examples:

- `alsoAllow: ["observability-lab"]`
- `alsoAllow: ["observe_demo_echo"]`

If you are already operating in explicit allowlist mode, `tools.allow` may also be appropriate. The real question is whether you are **adding to** an allowlist or **rebuilding** it.

## Pitfall 2: skill frontmatter does not mount tools

Skill frontmatter controls metadata such as:

- `name`
- `description`
- `user-invocable`
- `command-dispatch`
- `command-tool`

It does **not** automatically place a tool into the agent's runtime tool set.

### Real relationship

- the skill body can guide the agent toward a tool
- whether the tool is actually callable still depends on the runtime tool set

## Pitfall 3: `command-dispatch: tool` is not the same as a normal skill path

If a skill frontmatter includes:

- `command-dispatch: tool`
- `command-tool: xxx`

then `/skill-command ...` routes directly to the tool without model judgment. That is deterministic command → tool dispatch.

Without that declaration, the skill command is rewritten into a normal agent request so the model reads `SKILL.md` first and then decides whether to call a tool.

Do not confuse those two paths.

## Pitfall 4: plugin hooks do not perform the default skill-command rewrite

Default skill commands are rewritten by host core logic, not by plugin hooks.

Entry point:

- `src/auto-reply/reply/get-reply-inline-actions.ts`

## Pitfall 5: `message_received` is inbound, not outbound

The perspective is:

- user/channel → OpenClaw

So it is a good hook for raw input, slash commands, and activation conditions, not for outbound send behavior.

## Pitfall 6: `before_message_write` is not a universal pre-send hook

It runs before transcript persistence. It can rewrite persisted message content, but it should not be treated as “the one hook that rewrites all outbound text on every surface.”

## Pitfall 7: `plugins.entries.<id>.config` cannot contain arbitrary fields

If `openclaw.plugin.json` does not declare a field in `configSchema`, config validation fails.

Typical error:

```text
invalid config: must NOT have additional properties
```

### Correct handling

- add the field to `configSchema.properties`
- or remove the invalid field from `openclaw.json`

## Pitfall 8: a plugin can ship a skill even when not every surface shows the command menu

Command visibility depends on the surface and the command-registration path.

A command may execute successfully even when the UI menu does not show it. When validating skill commands, do not rely only on menu visibility. Send the command directly.

Also inspect:

- `commands.native`
- `commands.nativeSkills`
- whether the current surface supports native command registration and display

## Pitfall 9: a plugin can use subagent runtime helpers, but it cannot define a new native subagent type

Distinguish these two ideas:

- calling `api.runtime.subagent.*` at runtime
- defining a new plugin-level agent or subagent capability type

The first is supported. The second is not part of the normal OpenClaw plugin registration model.

## Pitfall 10: skill/config/tool changes may not fully affect the current session

OpenClaw snapshots skills and related state per session. That means a fresh edit may not fully affect an already-running session.

When debugging:

- retest in a fresh session
- restart the gateway if needed
- do not immediately conclude the implementation is wrong when the current session simply has stale state

## Pitfall 11: treating a tool as a guaranteed business step

In OpenClaw, a tool is a callable capability, not an automatically executed workflow step.

Common mistakes:

- assuming tool + skill guarantees the model will call the tool
- assuming seeing the tool in `plugins inspect` means it is available in the current run
- assuming tool-backed behavior appears in every surface menu

Correct model:

- model-driven tool choice is probabilistic
- deterministic behavior requires `command-dispatch: tool` or `api.registerCommand(...)`
- tool availability requires all of the following: registered + policy allowed + visible in the current run

## Pitfall 12: repacked plugin, old package still handed off

This is a classic remote-install delivery mistake.

### Symptom

- the plugin changed and was repacked
- but the remote operator still gets the old filename, old version, or a vague instruction like “install the package in dist”
- the remote environment installs the wrong iteration

### Root cause

- code iteration and package delivery were not treated as one release action
- `package.json` version was not bumped before repackaging
- `dist/` still contains multiple historical tgz files, so humans and agents grab the wrong one

### Correct handling

- bump the version every time a new installable package is handed off
- after repackaging, name the exact latest tgz file
- give the remote operator the full path, version, and checksum when needed

Recommended wording:

```text
Install ./dist/openclaw-<plugin-id>-<version>.tgz and do not use an older package.
```

## Debugging order

When the question is “why didn’t it take effect?”, use this order:

1. `openclaw plugins inspect <id>`
   - check load state, hooks, tools, commands, diagnostics
2. `openclaw.plugin.json`
   - check manifest and `configSchema`
3. the registration code for the relevant skill/command/tool
4. session logs
   - check what the model actually saw and called
5. `sessions.json` and `systemPromptReport`
   - check which tools were truly exposed in that run
6. tool policy / `tools.profile` / `alsoAllow`

## Lessons worth preserving

If the plugin is meant for other people to install or extend, do not assume they already know:

- the difference between a skill command and tool dispatch
- the difference between `plugins inspect` and runtime availability
- the difference between manifest validation and runtime registration
- the difference between inbound, transcript, and outbound hook semantics

Those distinctions should appear in the plugin docs, tests, and debugging output.
