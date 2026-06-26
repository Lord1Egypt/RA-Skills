# Logging and Review

## Decision logs

Every classification decision should be logged as JSONL with:

- timestamp
- account
- messageId
- sender
- subject
- senderType
- filterId
- kind
- confidence
- reasons
- planned actions
- notification route
- execution mode

Errors should also be logged as JSONL entries.

## Log location

Keep logs in a separate directory outside the skill source tree.

Recommended default:

```text
/home/ubuntu/.openclaw/gmail-labeler-logs/
```

Daily file format:

```text
YYYY-MM-DD.jsonl
```

## Retention

Purge logs older than 30 days automatically at runtime.

## Review loop

Use the previous day's logs to review:

- false positives
- false negatives
- over-aggressive archiving
- missed urgent billing signals
- noisy notifications that should be silenced
- user-requested corrections or preference changes

The self-improvement routine should update:

- local overlay custom filters
- confidence thresholds
- never-archive lists
- multilingual keywords

Keep the shared skill generic; write user-specific tuning into the local overlay.
