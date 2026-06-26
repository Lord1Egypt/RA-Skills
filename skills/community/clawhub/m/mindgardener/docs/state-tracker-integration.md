# State Tracker Integration

MindGardener integrates with OpenClaw's State Tracker via a shared provenance schema.

## Shared Schema

Both systems use the same format:

```json
{
  "subject": "Marcus",
  "predicate": "status",
  "object": "job_searching",
  "provenance": {
    "source": "agent:liselott|file:memory/2026-03-06.md",
    "timestamp": "2026-03-06T09:30:00Z",
    "confidence": 0.9,
    "agent": "liselott"
  }
}
```

## Data Flow

### State Tracker → MindGardener
- Checkpoints become structured input to `garden extract`
- More reliable than raw conversation logs
- Already has timestamps and agent attribution

### MindGardener → State Tracker
- `garden conflicts` output posted to #state-tracker
- `garden beliefs` changes posted for visibility
- Provides audit trail

## Source Format

Sources can be combined:
- `agent:<name>` — which agent recorded it
- `file:<path>` — source file
- `url:<url>` — external source
- `user:<name>` — direct from principal
- `discord:<channel>` — Discord channel
- `twitter:<handle>` — Twitter/X

Example: `agent:liselott|discord:swarm-ops`

## Usage

```bash
# Add fact with state tracker-compatible provenance
garden add "MCP 2.0 releases next week" \
  --source "agent:liselott|twitter:@anthropic" \
  --confidence 0.8

# Sync to state tracker (via RECALL-CONTEXT.md)
garden inject --output RECALL-CONTEXT.md
```

## Nightly Sync

The nightly maintenance job:
1. Runs `garden sync --apply` to merge agent memories
2. Posts conflicts to #state-tracker
3. Generates fresh RECALL-CONTEXT.md
