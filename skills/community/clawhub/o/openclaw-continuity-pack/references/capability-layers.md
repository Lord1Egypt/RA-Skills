# Capability Layers

## What this pack can carry

This pack can carry the parts of an OpenClaw assistant that are **portable, inspectable, and safe to share**.

### Layer 1 — Assistant operating style
- reasoning / quality bar (`SOUL.md`)
- durable task discipline (`AGENTS.md` + `SESSION_CONTINUITY.md`)
- heartbeat entry template (`HEARTBEAT.md`)
- generic human-context / environment-notes templates (`USER.md`, `TOOLS.md`)

### Layer 2 — Continuity workflow
- `memory / plans / status / handoff` directory structure
- continuity templates
- context-pressure rules
- checkpoint / resume workflow

### Layer 3 — Runtime/UI continuity assets
- thread continuity patch
- deployment notes
- verification notes
- rollback notes

## What this pack cannot carry by itself

### Not portable or not safe to ship
- hidden system prompts
- provider-side model behavior itself
- real user memory
- secrets / tokens / keys
- live channel configuration
- live runtime state
- one machine's current session store
- local plugin install state
- tool-approval policy that lives outside the skill

### Requires external equivalence
Even after installing this pack, another machine will only become "close" to the original assistant if it also has:
- a comparable base model
- a compatible OpenClaw version
- the same or equivalent tools / plugins
- similar permission policy
- matching source tree for patch application
- comparable workspace conventions

## Practical interpretation

Installing this pack gives you the **maximum safe reproducible subset** of the assistant.

That means:
- you can reproduce the operating style
- you can reproduce the long-task continuity workflow
- you may reproduce runtime continuity features if you patch and rebuild a matching source tree

It does **not** mean:
- you cloned the original assistant completely
- you copied secrets or real memory
- you reproduced all live permissions and infrastructure automatically
