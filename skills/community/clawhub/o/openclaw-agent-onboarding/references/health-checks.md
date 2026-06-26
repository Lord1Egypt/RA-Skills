# Health Checks

## Dimensions

```text
Skill health
Memory health
Knowledge-base health
Context hygiene
Agent team config
cron/heartbeat
OpenClaw service status
logs/errors
workspace git state
security risks
```

## Suggested cadence

Daily:

```text
OpenClaw service status, failed tasks, P0 anomalies
```

Weekly:

```text
skill usage, memory pollution, Inbox cleanup, context bloat, Agent team config
```

Monthly:

```text
outdated skills, knowledge graph orphans, memory architecture audit, maturity scoring, stale rule archive
```

## Report format

```text
OpenClaw AgentOS Health Report
score: 84/100
P0: 0
P1: 2
P2: 6
completed checks:
issues:
auto-fixable:
needs confirmation:
manual:
next actions:
```
