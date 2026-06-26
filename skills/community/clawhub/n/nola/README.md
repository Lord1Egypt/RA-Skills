# Nola Squad

An AI engineering squad for [OpenClaw](https://openclaw.ai). 14 specialist agents that build, test, review, and ship code — led by Nola.

## Install

```bash
# Via ClawHub
npx clawhub@latest install nola-squad

# Or manually
git clone https://github.com/flikq/nola-squad ~/.openclaw/workspace/skills/nola-squad
```

## What It Does

When you ask OpenClaw to build something, Nola takes over as your engineering lead. She breaks down the work and dispatches specialist agents:

| Agent | Role |
|---|---|
| **Architect** | System design, API contracts, types |
| **Spark** | Frontend — components, hooks, state |
| **Conduit** | Backend — API routes, DB ops, auth |
| **Prism** | UI/UX — visual polish, layout, animation |
| **Oracle** | Database — queries, migrations, schema |
| **Sentinel** | Security — vulnerabilities, auth review |
| **Forge** | Testing — unit, integration, coverage |
| **Bloodhound** | Debugging — root cause analysis |
| **Sage** | Code review — logic errors, edge cases |
| **Navigator** | DevOps — CI/CD, deploy safety |
| **Scribe** | Documentation — specs, API docs |
| **Releaser** | Git — commit, push, PR creation |
| **Scraper** | Data acquisition — APIs, websites |
| **Stage** | Browser testing — Playwright, E2E |

## How It Works

1. You ask OpenClaw to build/fix/review something
2. Nola plans the work and spawns specialist sub-agents
3. Agents run in parallel where possible
4. Results flow back, Nola dispatches next steps (review, polish, fix)
5. You get a summary of what was done

## Recommended Config

Add to your `openclaw.json` to enable parallel agent execution:

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "maxSpawnDepth": 2,
        "maxChildrenPerAgent": 8,
        "maxConcurrent": 8
      }
    }
  }
}
```

## Stack Agnostic

The squad works with any tech stack. Agents detect your project's language, framework, and tooling from config files and existing code — no configuration needed.

## License

MIT
