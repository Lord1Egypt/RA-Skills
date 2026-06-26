# Automation & Workflows

## Core Concepts
- Automation = repetitive task → triggered execution
- Workflows = multi-step pipelines with branching logic

## Tools & Approaches

### Cron & Scheduling
- Use OpenClaw cron for time-based triggers
- `systemEvent` for main session, `agentTurn` for isolated runs
- Heartbeat checks for interval-based monitoring

### Pipeline Patterns
1. **Linear**: Step A → B → C (sequential)
2. **Fan-out**: Step A → [B, C, D] (parallel)
3. **Conditional**: Step A → if X then B else C
4. **Retry**: Step A → fail → retry with backoff
5. **Human-in-loop**: Step A → pause → ask → continue

### Scripting
- Bash for system tasks, Python for logic-heavy
- Use `exec` tool for shell automation
- Background processes for long-running tasks

### Event-Driven
- Webhook listeners via API endpoints
- File watchers (inotifywait, fswatch)
- RSS/blog monitoring via blogwatcher
- Email triggers via himalaya polling

### Integration Patterns
- CLI tools > REST APIs > browser automation
- Pipe outputs between tools
- JSON as universal interchange format
- Use `jq` for JSON transformation

## Common Automations
- Daily email digest → summarize → notify
- GitHub PR review → auto-fix → push
- RSS feed update → summarize → message
- System health check → alert if anomaly
- Data scrape → transform → store → report

## Best Practices
- Log everything (timestamps, inputs, outputs)
- Handle failures gracefully (try/catch, retries)
- Keep automations idempotent
- Use environment variables for secrets
- Test with dry-run before production
