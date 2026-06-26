# Agent Configuration Reference

## Basic Configuration

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxSpawnDepth: 1,         // Child Agent depth (recommended 1-2)
        maxChildrenPerAgent: 5,   // Max parallel child processes
        runTimeoutSeconds: 300    // Default timeout of 5 minutes
      }
    },
    list: [
      {
        id: "main",
        subagents: {
          allowAgents: ["code-reviewer", "doc-writer"]  // Whitelist
        }
      }
    ]
  },
  session: {
    agentToAgent: {
      enabled: true,
      allow: ["*"],              // Allow all cross-Agent communication
      maxPingPongTurns: 5        // A2A negotiation capped at 5 rounds
    }
  }
}
```

## Advanced Configuration (Complex Tasks)

```json5
{
  agents: {
    defaults: {
      subagents: {
        maxSpawnDepth: 2,         // Two levels of nesting
        maxChildrenPerAgent: 10,  // More parallel processes
        runTimeoutSeconds: 600    // 10-minute timeout
      }
    }
  }
}
```

## Permission Configuration (Whitelist)

```json5
{
  agents: {
    list: [
      {
        id: "main",
        subagents: {
          allowAgents: ["analyzer", "reviewer", "writer"]  // Only allow these child Agents
        }
      }
    ]
  }
}
```

## Constraint Type Summary

| Constraint | Type | Default | Purpose |
|------------|------|---------|---------|
| maxSpawnDepth | int | 1 | Prevent infinite recursion |
| maxChildrenPerAgent | int | 5 | Prevent resource exhaustion |
| allowAgents | string[] | Configurable | Whitelist permission control |
| runTimeoutSeconds | int | 300 | Single task timeout |
| maxPingPongTurns | int | 5 | A2A negotiation round cap |