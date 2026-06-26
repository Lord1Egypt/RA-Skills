# Trigger Strategies

Define explicit triggers to avoid vague heartbeat behavior.

## Trigger Types

## Time-Based

Use for regular reassessment windows:
- every 30m
- every 2h outside active hours

## Event-Based

Use for state-change detection:
- build status changed to failed
- inbox urgent count > 0
- incident ticket moved to critical

## Conditional

Use for threshold gates:
- next calendar event <= 30 minutes
- unresolved alerts >= 1
- unread urgent messages >= 1

## Escalation Design

Each trigger should define:
1. threshold
2. notification path
3. cooldown

If any of the three is missing, do not activate that trigger.

## Suppression Rules

During cooldown windows, suppress duplicate alerts and only emit new output on meaningful state change.

No state change -> return `HEARTBEAT_OK`.
