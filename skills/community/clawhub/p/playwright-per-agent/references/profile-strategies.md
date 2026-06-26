# Profile Strategies — When to use which mode

> **本文件不硬编码任何具体 agent 名字**。所有示例用 `agent-a` / `agent-b` 占位符，
> 用户在自己环境里替换为实际 agent id 即可。映射文件放 `~/.config/playwright-per-agent/agents.json`
> 等用户私有位置（详见 `assets/example-config.json`）。

## Decision tree

```
Need persistent login state across agents?        ─┐
  ├─ No  → ephemeral                              │  Single-shot
  │         (test, scrape one URL)                │  use
  │                                               │
  └─ Yes → Multiple agents share the same login? ─┤
            ├─ Yes → shared                       │  Many agents
            │         (one Chrome for everyone,   │  same identity
            │          cheap but stateful)        │
            │                                    │
            └─ No  → per-agent                    │  Per-agent
                      (each agent has its own    │  isolation
                       login, no cross-contamination)
```

## Mode comparison

| Aspect | shared | per-agent | ephemeral |
|---|---|---|---|
| Chrome processes | 1 | N (one per agent) | 1 per call |
| Memory | Lowest | High (1× per agent) | High (transient) |
| Cookies / login | Shared | Isolated | None (deleted) |
| Cross-agent state | Visible | Hidden | None |
| Cross-process attach | ✅ registry | ✅ registry | ❌ |
| Subagent support | inherit | inherit | n/a |
| Persistent profile | ✅ | ✅ | ❌ (deleted) |
| Best for | Same-identity parallel work | Independent agents | Tests, one-off scrapes |

## Subagent patterns

### Pattern A — Inherit (default)
Subagent opens a new tab in parent's context. Cheap, shared login.

```javascript
const ab = new AgentBrowser({ mode: 'per-agent' });
const parent = await ab.getBrowser('agent-a');
const sub = await ab.getBrowser('agent-a:scout-1', { inherit: true });
// sub.page and parent.page share cookies / localStorage
```

### Pattern B — Independent subagent
Subagent gets own chrome instance, like a real separate agent.

```javascript
const sub = await ab.getBrowser('agent-a:scout-1', { inherit: false });
// sub has its own profile, port, state — fully isolated
```

### Pattern C — Sub-subagent
Nesting supported up to any depth.

```javascript
const grand = await ab.getBrowser('agent-a:scout-1:finder-3', { inherit: true });
// grand inherits from scout-1 which inherits from agent-a (or each gets its own)
```

## State cleanup

- **shared / per-agent**: profile persists in `~/.cache/agent-browser/<id>/`. Delete
  manually to wipe state.
- **ephemeral**: profile auto-deleted on `ab.close(id)` or process exit (if
  `cleanupOnExit: true`).

## Cross-process attach

If another process (or terminal) launches a per-agent browser, the port + profile
are recorded in `/tmp/agent-browser-registry.json`. A new `AgentBrowser` instance
in another process can connect:

```javascript
const ab = new AgentBrowser({ mode: 'per-agent' });
const { page, cdpPort } = await ab.getBrowser('agent-a');
// If 'agent-a' was already launched elsewhere, attaches to its CDP port
```

(Attach happens automatically when `getBrowser` detects an in-registry port is
already listening — see `loadRegistry()` + `isPortInUse()` in the source.)
