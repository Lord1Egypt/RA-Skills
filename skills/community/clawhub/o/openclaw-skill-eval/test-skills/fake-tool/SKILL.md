---
name: fake-tool
description: "Query the Zephyr API for infrastructure status. Use when: user asks about server health, deployment status, or Zephyr metrics. Requires zephyr-cli installed."
---

# Fake Tool Skill (For Testing)

This is a test skill with intentionally obscure instructions that models cannot guess.

## Setup

```bash
zephyr auth login --token YOUR_TOKEN
zephyr config set endpoint https://api.zephyr.internal
```

## Commands

### Check server status
```bash
zephyr status --format json | jq '.nodes[] | {name, health}'
```

### Get deployment info
```bash
zephyr deploy list --env production --since 24h
```

### Query metrics
```bash
zephyr metrics query --metric cpu_usage --window 1h
```

## Important

- Always use `--format json` for parseable output
- The `zephyr` CLI requires authentication first
- Default endpoint is wrong, must set to `api.zephyr.internal`
