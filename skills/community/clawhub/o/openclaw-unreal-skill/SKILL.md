---
name: unreal-plugin
version: 1.1.0
description: Control Unreal Engine Editor via OpenClaw Unreal Plugin. Use for Unreal development tasks including level/actor management, transforms, PIE control, debugging, input simulation, and console commands. Can create/delete actors, save levels, run console commands, simulate input, and capture viewport screenshots and logs. Project-changing and destructive operations are refused at runtime unless the operator starts the gateway with OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE=1 and the call passes confirm: true; read-only inspection needs neither, and dryRun: true previews any call without sending it. Use only on explicit Unreal Editor requests, in trusted local projects.
homepage: https://github.com/TomLeeLive/openclaw-unreal-skill
author: Tom Jaejoon Lee
disableModelInvocation: true
---

# OpenClaw Unreal Plugin

MCP skill for controlling Unreal Engine Editor via OpenClaw.

## Safety and permissions

**What this skill can change:** anything the Unreal Editor can — actors and their
components and transforms, the open level, imported assets, PIE (Play In Editor),
and whatever a console command reaches (`console.execute`).

**What runs without asking:** read-only tools only — `level.getCurrent`,
`level.list`, `actor.find`, `actor.getAll`, `actor.getData`, `transform.get*`,
`component.get`, `editor.getState`, `asset.list`, `blueprint.list`,
`debug.hierarchy`, `debug.screenshot`, `console.getLogs`, `debug.log`. Their
behaviour is unchanged.

**What is gated at runtime:** every project-changing tool — `actor.create`,
`actor.delete`, `actor.setProperty`, `transform.set*`, `component.add`/`remove`,
`level.open`, `level.save`, `asset.import`, `console.execute`, `input.simulate*`,
`editor.play`/`stop`/`pause`/`resume`, `blueprint.open` — and any batch that
carries one of them. The gateway extension refuses these by default. A tool name
it does not recognise counts as project-changing unless its verb is clearly
read-only: the gate fails closed, never open.

**How to enable them** — both steps are required:

1. The operator starts the gateway with the opt-in environment variable. It is
   read from the gateway process, so the model cannot set it:

   ```bash
   OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE=1 openclaw gateway restart
   # or, scoped to this skill only:
   OPENCLAW_UNREAL_ALLOW_DESTRUCTIVE=1 openclaw gateway restart
   ```

2. The caller passes `confirm: true` on each project-changing call, after the
   user has approved that specific change:

   ```
   unreal_execute: actor.delete {name: "Cube_01"}, confirm: true
   ```

Missing either one is a refusal with an explanation of what was blocked and how
to allow it. Nothing reaches the Editor in the meantime.

**Preview first:** `dryRun: true` reports how a call is classified and what would
be sent, and sends nothing:

```
unreal_execute: level.save, dryRun: true
→ {risk: "project-changing", requiresConfirmation: true, wouldRun: false, executed: false}
```

**Check the current state:** `openclaw unreal status` prints whether
project-changing tools are enabled, and `GET /unreal/status` reports the same as
`destructiveOperations: "enabled" | "blocked"`.

**Scope of the gate:** it lives in the gateway extension that ships with this
skill (`extension/index.ts`), so it covers every call routed through the OpenClaw
gateway — Telegram, Discord and the other channels. The Unreal Editor plugin's
embedded HTTP server (port 27184, Mode B below) is a separate install from the
plugin repository and is not gated by this package: keep that port on the local
machine and review the plugin repository for its own controls.

## Connection Modes

### Mode A: OpenClaw Gateway (Remote)
The plugin connects to OpenClaw Gateway via HTTP polling. Works automatically when Gateway is running.

### Mode B: MCP Direct (Claude Code / Cursor)
The plugin runs an embedded HTTP server on port **27184**. Use the included MCP bridge:

```bash
# Claude Code
claude mcp add unreal -- node /path/to/Plugins/OpenClaw/MCP~/index.js

# Cursor — add to .cursor/mcp.json
{"mcpServers":{"unreal":{"command":"node","args":["/path/to/Plugins/OpenClaw/MCP~/index.js"]}}}
```

Both modes run simultaneously.

## Editor Panel

**Window → OpenClaw Unreal Plugin** — opens a dockable tab with:
- Connection status indicator
- MCP server info (address, protocol)
- Connect / Disconnect buttons
- Live log of tool calls and messages

## Tools

### Level
- `level.getCurrent` — current level name
- `level.list` — all levels in project
- `level.open` — open level by name
- `level.save` — save current level

### Actor
- `actor.find` — find by name/class
- `actor.getAll` — list all actors
- `actor.create` — create actors: StaticMeshActor (Cube, Sphere, Cylinder, Cone), PointLight, Camera
- `actor.delete` — delete by name
- `actor.getData` — detailed actor info
- `actor.setProperty` — set properties via UE reflection system

### Transform
- `transform.getPosition` / `transform.setPosition`
- `transform.getRotation` / `transform.setRotation`
- `transform.getScale` / `transform.setScale`

> Transform tools require a valid RootComponent (works on StaticMeshActor, PointLight, etc. — not on bare Actor).

### Component
- `component.get` — get component data
- `component.add` — add component (not yet implemented)
- `component.remove` — remove component (not yet implemented)

### Editor
- `editor.play` — start PIE (uses RequestPlaySession)
- `editor.stop` — stop PIE
- `editor.pause` / `editor.resume` — pause/resume PIE
- `editor.getState` — current editor state

### Debug
- `debug.hierarchy` — actor hierarchy tree
- `debug.screenshot` — capture editor viewport
- `debug.log` — write to output log

### Input
- `input.simulateKey` — simulate key press
- `input.simulateMouse` — simulate mouse
- `input.simulateAxis` — simulate axis

### Asset
- `asset.list` — list assets at path
- `asset.import` — import asset (not yet implemented)

### Console
- `console.execute` — run console command
- `console.getLogs` — read project log file; params: `count` (number of lines), `filter` (text filter)

### Blueprint
- `blueprint.list` — list blueprints
- `blueprint.open` — open blueprint (not yet implemented)

## Troubleshooting

### Stale binaries / plugin not loading

Clear the build cache and restart the editor:

```bash
rm -rf YourProject/Plugins/OpenClaw/Binaries YourProject/Plugins/OpenClaw/Intermediate
```

### Connection issues

- Ensure OpenClaw Gateway is running: `openclaw gateway status`
- Check the Editor Panel log for errors
- Verify the MCP port is not blocked by firewall

## Security & Privacy Disclosure

This skill drives a live Unreal Editor. Full disclosure of capabilities and current limitations:

- **Local HTTP server hardening (plugin v1.3.1+)**: the embedded server (port 27184) rejects browser-originated requests (any `Origin` header → 403) and supports optional shared-secret auth — set `OPENCLAW_BRIDGE_TOKEN` for both the Unreal Editor process and the MCP client to require `X-OpenClaw-Token` on every request. Without the token set, keep the port on trusted machines only — any local process can send editor commands.
- **Destructive operations are gated at runtime (v1.1.0+)**: deleting actors, saving levels, importing assets, running console commands (`console.execute`) and simulating keyboard/mouse input are refused by the gateway extension unless it was started with `OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE=1` **and** the call carries `confirm: true`. Confirm the change with the user before setting it — see [Safety and permissions](#safety-and-permissions). None of these should run implicitly from a vague request.
- **Data visibility**: `debug.screenshot` and `console.getLogs` can capture whatever is on screen or in project logs — including credentials, tokens, or source paths if present. Review before sharing captures outside the machine.
- **Trigger scope**: routine-sounding requests ("clean up the level", "save everything", "just run it") map to state-changing Editor operations — confirm once before the first state-changing call in a session.
- **Safety defaults**: `disableModelInvocation: true` is set — the model cannot auto-invoke this skill; it runs only on explicit user request. Project-changing tools default to refused, and `dryRun: true` previews any call without sending it. Keep the project under source control before automation sessions. The Korean `SKILL_KO.md` states the same recommendation; if the two ever disagree, this file governs.

## License

Apache-2.0 — See LICENSE.md
