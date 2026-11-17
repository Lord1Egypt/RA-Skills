---
name: godot-plugin
version: 1.2.10
description: Control Godot Editor via OpenClaw Godot Plugin. Use for Godot game development tasks including scene management, node manipulation, input simulation, debugging, and editor control. Can modify, save, and delete scenes/nodes and capture project metadata and screenshots — destructive operations should be confirmed with the user. Use only on explicit Godot Editor requests like inspecting scenes, creating nodes, taking screenshots, testing gameplay, or controlling the editor, in trusted local projects.
homepage: https://github.com/TomLeeLive/openclaw-godot-skill
author: Tom Jaejoon Lee
disableModelInvocation: true
---

# Godot Plugin Skill

Control Godot 4.x Editor through 30 built-in tools. Supports 80+ node types.

## Connection Modes

### Mode A: OpenClaw Gateway (Remote)
For Telegram, Discord, and other OpenClaw channels:
- Plugin connects TO Gateway via WebSocket
- Gateway URL: configurable in Godot dock UI
- Best for: remote access, mobile messaging

### Mode B: MCP Bridge (Local)
For Claude Code, Cursor, and local AI tools:
- Built-in HTTP server in Godot Plugin
- Start: Click "Start MCP" in dock UI (port 27183)
- Add to Claude Code: `claude mcp add godot -- node <path>/MCP~/index.js`

## First-Time Setup

If `godot_execute` tool is not available, install the gateway extension:

```bash
# From skill directory
./scripts/install-extension.sh

# Restart gateway
openclaw gateway restart
```

The extension files are in `extension/` directory.

## Quick Reference

### Core Tools

| Category | Key Tools |
|----------|-----------|
| **Scene** | `scene.create`, `scene.getCurrent`, `scene.open`, `scene.save` |
| **Node** | `node.find`, `node.create`, `node.delete`, `node.getData` |
| **Transform** | `transform.setPosition`, `transform.setRotation`, `transform.setScale` |
| **Debug** | `debug.tree`, `debug.screenshot`, `console.getLogs` |
| **Input** | `input.keyPress`, `input.mouseClick`, `input.actionPress` |
| **Editor** | `editor.play`, `editor.stop`, `editor.getState` |

## Common Workflows

### 1. Scene Creation

Use `godot_execute` tool:
- `godot_execute(tool="scene.create", parameters={rootType: "Node2D", name: "Level1"})`
- `godot_execute(tool="node.create", parameters={type: "CharacterBody2D", name: "Player"})`
- `godot_execute(tool="scene.save")`

### 2. Find & Modify Nodes

- `godot_execute(tool="node.find", parameters={name: "Player"})`
- `godot_execute(tool="node.getData", parameters={path: "Player"})`
- `godot_execute(tool="transform.setPosition", parameters={path: "Player", x: 100, y: 200})`

### 3. Game Testing with Input

- `godot_execute(tool="editor.play")`
- `godot_execute(tool="input.keyPress", parameters={key: "W"})`
- `godot_execute(tool="input.actionPress", parameters={action: "jump"})`
- `godot_execute(tool="debug.screenshot")`
- `godot_execute(tool="editor.stop")`

### 4. Check Logs

- `godot_execute(tool="console.getLogs", parameters={limit: 50})`
- `godot_execute(tool="console.getLogs", parameters={type: "error", limit: 20})`

## Tool Categories

### Console (2 tools)
- `console.getLogs` - Get logs from Godot log file {limit: 100, type: "error"|"warning"|""}
- `console.clear` - Placeholder (logs can't be cleared programmatically)

### Scene (5 tools)
- `scene.getCurrent` - Get current scene info
- `scene.list` - List all .tscn/.scn files
- `scene.open` - Open scene by path
- `scene.save` - Save current scene
- `scene.create` - Create new scene {rootType: "Node2D"|"Node3D"|"Control", name: "SceneName"}

### Node (6 tools)
- `node.find` - Find by name, type, or group
- `node.create` - Create node (80+ types: CSGBox3D, MeshInstance3D, ColorRect, etc.)
- `node.delete` - Delete node by path
- `node.getData` - Get node info, children, transform
- `node.getProperty` - Get property value
- `node.setProperty` - Set property value (Vector2/3 auto-converted)

### Transform (3 tools)
- `transform.setPosition` - Set position {x, y} or {x, y, z}
- `transform.setRotation` - Set rotation (degrees)
- `transform.setScale` - Set scale

### Editor (4 tools)
- `editor.play` - Play current or custom scene
- `editor.stop` - Stop playing
- `editor.pause` - Toggle pause
- `editor.getState` - Get playing state, version, project name

### Debug (3 tools)
- `debug.screenshot` - Capture viewport
- `debug.tree` - Get scene tree as text
- `debug.log` - Print message

### Input (7 tools) - For Game Testing
- `input.keyPress` - Press and release key {key: "W"}
- `input.keyDown` - Hold key down
- `input.keyUp` - Release key
- `input.mouseClick` - Click at position {x, y, button: "left"|"right"|"middle"}
- `input.mouseMove` - Move mouse to position {x, y}
- `input.actionPress` - Press input action {action: "jump"}
- `input.actionRelease` - Release input action

### Script (2 tools)
- `script.list` - List .gd files
- `script.read` - Read script content

### Resource (1 tool)
- `resource.list` - List files by extension

## Supported Keys for Input

```
A-Z, 0-9, SPACE, ENTER, ESCAPE, TAB, BACKSPACE, DELETE
UP, DOWN, LEFT, RIGHT
SHIFT, CTRL, ALT
F1-F12
```

## Node Types for Creation

| Type | Description |
|------|-------------|
| `Node2D` | 2D spatial |
| `Node3D` | 3D spatial |
| `Sprite2D` | 2D sprite |
| `CharacterBody2D` | 2D character |
| `CharacterBody3D` | 3D character |
| `RigidBody2D/3D` | Physics body |
| `Area2D/3D` | Trigger area |
| `Camera2D/3D` | Camera |
| `Label`, `Button` | UI elements |

## Tips

### Input Simulation
- Only works during **Play mode**
- Use `input.actionPress` for mapped actions (from Input Map)
- Use `input.keyPress` for direct key simulation

### Finding Nodes
```
node.find {name: "Player"}      # By name substring
node.find {type: "Sprite2D"}    # By exact type
node.find {group: "enemies"}    # By group
```

### Vector Properties
`node.setProperty` auto-converts dictionaries to Vector2/Vector3:
```
{path: "Cam", property: "zoom", value: {x: 2, y: 2}}  # → Vector2(2, 2)
```

### Console Logs
```
console.getLogs {limit: 50}           # Last 50 lines
console.getLogs {type: "error"}       # Errors only
console.getLogs {type: "warning"}     # Warnings only
```

## 🔐 Security: Model Invocation Setting

When publishing to ClawHub, you can configure `disableModelInvocation`:

| Setting | AI Auto-Invoke | User Explicit Request |
|---------|---------------|----------------------|
| `false` (default) | ✅ Allowed | ✅ Allowed |
| `true` | ❌ Blocked | ✅ Allowed |

### Recommendation: **`true`**

**Reason:** During Godot development, it's useful for AI to autonomously perform supporting tasks like checking scene tree, taking screenshots, and inspecting nodes.

**When to use `true`:** For sensitive tools (payments, deletions, message sending, etc.)

As of v1.2.10 this skill ships with `disableModelInvocation: true` — it runs only on explicit user request.

## Security & Privacy Disclosure

This skill drives a live Godot Editor. Full disclosure of capabilities and current limitations:

- **Local HTTP bridge has no authentication (current limitation)**: the MCP bridge (port 27183) accepts requests without auth or origin restriction. **Keep it bound to localhost and never expose the port on shared or public networks** — any local process could otherwise send editor commands. Token authentication and origin allow-listing are on the roadmap.
- **Destructive operations** — confirm with the user before: modifying/deleting nodes, saving scenes, simulating input. Keep the project under version control before automation sessions.
- **Data visibility**: tools can read and transmit project name, engine version, scene structure, script contents, and viewport screenshots to the connected agent. Don't use on projects whose contents must not leave the machine.
- **Trigger scope**: routine-sounding requests ("clean up the scene", "save everything") map to state-changing editor operations — confirm once before the first state-changing call in a session.

## License

Apache-2.0 — See LICENSE.md
