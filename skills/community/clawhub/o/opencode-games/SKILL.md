---
name: opencode
description: Spawn OpenCode as an ACP (Agent Client Protocol) subagent for complex coding tasks. Use when building games, web apps, multi-file projects, or when the user says "use opencode", "spawn opencode", "code with opencode", or "build with opencode". Triggers on any coding task that would benefit from a dedicated coding agent.
---

# OpenCode

## Overview

OpenCode is an open-source AI coding agent that integrates with OpenClaw via ACP (Agent Client Protocol). It provides specialized coding capabilities including game development, multi-file projects, complex refactoring, and production-ready code generation.

**Status**: ✅ Fully tested - Built 12 production-ready games including Pac-Man, Space Invaders, Tetris, Q*bert, and more.

## When to Use This Skill

Use OpenCode when:
1. Building games (HTML5 Canvas games work excellently)
2. Creating multi-file projects from scratch
3. Performing complex code refactoring across multiple files
4. Building production-ready applications with proper structure
5. Tasks requiring dedicated coding agent focus
6. The user explicitly asks to use OpenCode

## Quick Start

### Spawn OpenCode as ACP Subagent

```javascript
// One-shot task (recommended for most builds)
sessions_spawn({
  runtime: "acp",
  agentId: "opencode",
  task: "Create a complete [game/app] in HTML/CSS/JavaScript...",
  mode: "run",
  cwd: "/path/to/project"
})

// Parallel builds (run multiple simultaneously)
sessions_spawn({...}) // Game 1
sessions_spawn({...}) // Game 2  
sessions_spawn({...}) // Game 3
```

## Parallel Builds

OpenCode supports **parallel execution** - spawn multiple subagents simultaneously:

```javascript
// Launch 3 games at once
const game1 = sessions_spawn({... Asteroids ...})
const game2 = sessions_spawn({... Doodle Jump ...})
const game3 = sessions_spawn({... Flappy Bird ...})

// All build concurrently, limited by slowest
```

**Performance**: 3 parallel games completed in ~1m 20s (same as single game)

## Performance Expectations

Based on 12-game test suite:

| Complexity | Examples | Build Time | Lines |
|------------|----------|------------|-------|
| **Simple** | Pong, Flappy Bird | 30-60s | 300-600 |
| **Medium** | Snake, 2048, Breakout | 1m - 1m 30s | 500-800 |
| **Complex** | Pac-Man, Q*bert, Tetris | 1m 30s - 2m+ | 1000-1300 |

## Proven Game Templates

The following game types have been **fully tested and verified**:

| Game | Key Features | Test Result |
|------|--------------|-------------|
| **Tetris** | Ghost piece, hold, preview, levels | ✅ Complete |
| **Pac-Man** | 4 AI ghosts, maze, power pellets | ✅ Complete |
| **Space Invaders** | Enemy formation, bunkers, UFO | ✅ Complete |
| **Snake** | Grid movement, progressive speed | ✅ Complete |
| **Pong** | AI opponent, physics | ✅ Complete |
| **Breakout** | Multi-level, power-ups | ✅ Complete |
| **2048** | Merge algorithm, undo, swipe | ✅ Complete |
| **Minesweeper** | Flood-fill, 3 difficulties | ✅ Complete |
| **Q*bert** | Isometric, pyramid, enemies | ✅ Complete (fixed spawn) |
| **Asteroids** | Vector physics, screen wrap | ✅ Complete |
| **Flappy Bird** | Gravity, pipes, medals | ✅ Complete |
| **Doodle Jump** | Bouncing, power-ups, black holes | ✅ Complete (fixed spawn) |

## Commands Reference

### Core Commands

| Command | Description |
|---------|-------------|
| `opencode` | Start interactive TUI |
| `opencode run <message>` | Run non-interactive mode |
| `opencode acp` | Start ACP server (for OpenClaw integration) |
| `opencode serve` | Start headless server |
| `opencode web` | Start web interface |

### Utility Commands

| Command | Description |
|---------|-------------|
| `opencode providers` | Manage AI providers |
| `opencode models` | List available models |
| `opencode stats` | Show token usage |
| `opencode upgrade` | Update to latest version |
| `opencode session` | Manage sessions |

## Built-in Agents

- **build** - Full-access agent for development work (default)
- **plan** - Read-only agent for analysis and exploration
- **@general** - Subagent for complex searches

## Configuration

### ACP Integration

OpenCode is configured in OpenClaw. The ACP command is:

```bash
opencode acp
```

This starts JSON-RPC over stdio for ACP-compatible communication.

### Providers

OpenCode supports multiple AI providers:
- OpenCode Zen (recommended)
- Claude (Anthropic)
- OpenAI
- Google Gemini
- Local models

Set API keys via `opencode providers` or environment variables.

## Usage Patterns

### Pattern 1: One-shot Build

```javascript
sessions_spawn({
  runtime: "acp",
  agentId: "opencode",
  task: "Create a complete Snake game in HTML/CSS/JavaScript...",
  mode: "run",
  cwd: "/Users/jadegaul/.openclaw/workspace/codeprojects"
})
```

### Pattern 2: Parallel Builds

```javascript
// Build 3 games simultaneously
const builds = [
  sessions_spawn({ task: "Asteroids...", ... }),
  sessions_spawn({ task: "Doodle Jump...", ... }),
  sessions_spawn({ task: "Flappy Bird...", ... })
]
```

### Pattern 3: Bug Fixes

```javascript
// Fix existing code
sessions_spawn({
  runtime: "acp",
  agentId: "opencode",
  task: "Fix the bug in /path/to/file.html where...",
  mode: "run"
})
```

### Pattern 4: Check Status

```javascript
subagents({ action: "list" })
```

### Pattern 5: Steer Running Subagent

```javascript
subagents({
  action: "steer",
  target: "<runId>",
  message: "Continue with the implementation"
})
```

## File Operations

OpenCode has full file system access:
- Read/write files
- Execute shell commands
- Navigate directories
- Git operations

## Capabilities

- **100% open source** (unlike Claude Code)
- **Provider-agnostic** - use any model
- **LSP support** - code intelligence
- **Client/server architecture** - run remotely
- **Undo/redo** - `/undo` and `/redo` commands
- **Session sharing** - `/share` creates shareable links

## Best Practices

1. **Be specific** in task descriptions - include file paths, required features
2. **Use mode: "run"** for one-shot builds (faster)
3. **Use mode: "session"** for multi-step work
4. **Test immediately** - some games need spawn fixes
5. **Parallel builds** work great for 3+ independent tasks

## Common Issues & Solutions

### Issue: Game spawns in wrong position
**Fix**: Spawn OpenCode to add starting platform/position

### Issue: Character dies immediately
**Fix**: Add spawn delay or ensure safe starting position

### Issue: Controls not working
**Fix**: Check that touch + keyboard controls both specified

## References

See [references/opencode-docs.md](references/opencode-docs.md) for complete ACP documentation.

## Test Results Summary

**Total Games Built**: 12  
**Total Build Time**: ~15 minutes  
**Total Lines of Code**: ~8,000+  
**Success Rate**: 100% (with minor spawn fixes)  

**Average Build Times**:
- Simple games: ~50s
- Medium games: ~1m 15s  
- Complex games: ~1m 40s

OpenCode via ACP is **production-ready** for game development and coding tasks.
