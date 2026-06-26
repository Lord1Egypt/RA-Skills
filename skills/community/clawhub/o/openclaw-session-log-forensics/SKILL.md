---
name: session-logs
description: Analyze OpenClaw session JSONL history for cost spikes, tool-call anomalies, and behavior regressions with jq + rg.
metadata: { "openclaw": { "emoji": "📜", "requires": { "bins": ["jq", "rg"] } } }
---

# session-logs

Search your complete conversation history stored in session JSONL files. Use this when a user references older/parent conversations or asks what was said before.

This fork is tuned for OpenClaw operators who need fast incident forensics (cost spikes, tool-call drift, and behavior regressions) across many sessions.

## Trigger

Use this skill when the user asks about prior chats, parent conversations, or historical context that isn't in memory files.

## Location

Session logs live at: `~/.openclaw/agents/<agentId>/sessions/` (use the `agent=<id>` value from the system prompt Runtime line).

- **`sessions.json`** - Index mapping session keys to session IDs
- **`<session-id>.jsonl`** - Full conversation transcript per session

## Structure

Each `.jsonl` file contains messages with:

- `type`: "session" (metadata) or "message"
- `timestamp`: ISO timestamp
- `message.role`: "user", "assistant", or "toolResult"
- `message.content[]`: Text, thinking, or tool calls (filter `type=="text"` for human-readable content)
- `message.usage.cost.total`: Cost per response

## Common Queries

### List all sessions by date and size

```bash
for f in ~/.openclaw/agents/<agentId>/sessions/*.jsonl; do
  date=$(head -1 "$f" | jq -r '.timestamp' | cut -dT -f1)
  size=$(ls -lh "$f" | awk '{print $5}')
  echo "$date $size $(basename $f)"
done | sort -r
```

### Find sessions from a specific day

```bash
for f in ~/.openclaw/agents/<agentId>/sessions/*.jsonl; do
  head -1 "$f" | jq -r '.timestamp' | grep -q "2026-01-06" && echo "$f"
done
```

### Extract user messages from a session

```bash
jq -r 'select(.message.role == "user") | .message.content[]? | select(.type == "text") | .text' <session>.jsonl
```

### Search for keyword in assistant responses

```bash
jq -r 'select(.message.role == "assistant") | .message.content[]? | select(.type == "text") | .text' <session>.jsonl | rg -i "keyword"
```

### Get total cost for a session

```bash
jq -s '[.[] | .message.usage.cost.total // 0] | add' <session>.jsonl
```

### Daily cost summary

```bash
for f in ~/.openclaw/agents/<agentId>/sessions/*.jsonl; do
  date=$(head -1 "$f" | jq -r '.timestamp' | cut -dT -f1)
  cost=$(jq -s '[.[] | .message.usage.cost.total // 0] | add' "$f")
  echo "$date $cost"
done | awk '{a[$1]+=$2} END {for(d in a) print d, "$"a[d]}' | sort -r
```

### Count messages and tokens in a session

```bash
jq -s '{
  messages: length,
  user: [.[] | select(.message.role == "user")] | length,
  assistant: [.[] | select(.message.role == "assistant")] | length,
  first: .[0].timestamp,
  last: .[-1].timestamp
}' <session>.jsonl
```

### Tool usage breakdown

```bash
jq -r '.message.content[]? | select(.type == "toolCall") | .name' <session>.jsonl | sort | uniq -c | sort -rn
```

### Daily tool-call volume (find sudden jumps)

```bash
for f in ~/.openclaw/agents/<agentId>/sessions/*.jsonl; do
  date=$(head -1 "$f" | jq -r '.timestamp' | cut -dT -f1)
  calls=$(jq -r '.message.content[]? | select(.type=="toolCall") | .name' "$f" | wc -l | tr -d ' ')
  echo "$date $calls"
done | awk '{a[$1]+=$2} END {for(d in a) print d, a[d]}' | sort
```

### Cost outlier scan (quick anomaly triage)

```bash
for f in ~/.openclaw/agents/<agentId>/sessions/*.jsonl; do
  sid=$(basename "$f" .jsonl)
  cost=$(jq -s '[.[] | .message.usage.cost.total // 0] | add' "$f")
  echo "$sid $cost"
done | sort -k2,2nr | head -20
```

### Threshold anomaly flagger (cost or tool-call spikes)

```bash
COST_THRESHOLD=2
CALL_THRESHOLD=40
for f in ~/.openclaw/agents/<agentId>/sessions/*.jsonl; do
  sid=$(basename "$f" .jsonl)
  cost=$(jq -s '[.[] | .message.usage.cost.total // 0] | add' "$f")
  calls=$(jq -r '.message.content[]? | select(.type=="toolCall") | .name' "$f" | wc -l | tr -d ' ')
  if awk "BEGIN {exit !($cost > $COST_THRESHOLD || $calls > $CALL_THRESHOLD)}"; then
    printf "%s cost=%s tool_calls=%s\n" "$sid" "$cost" "$calls"
  fi
done | sort -t= -k2,2nr
```

Set `COST_THRESHOLD` and `CALL_THRESHOLD` from your baseline, then run this after incidents to immediately shortlist suspicious sessions.

### Compare two sessions (message mix regression)

```bash
for s in <old-session>.jsonl <new-session>.jsonl; do
  echo "== $s =="
  jq -s '{
    total: length,
    user: ([.[] | select(.message.role=="user")] | length),
    assistant: ([.[] | select(.message.role=="assistant")] | length),
    tool_calls: ([.[] | .message.content[]? | select(.type=="toolCall")] | length),
    total_cost: ([.[] | .message.usage.cost.total // 0] | add)
  }' "$s"
done
```

### Compact forensic snapshot for one session

```bash
jq -s '
  def tool_names: [.[] | .message.content[]? | select(.type=="toolCall") | .name];
  {
    session_id: (input_filename | split("/")[-1] | sub("\\.jsonl$"; "")),
    first: .[0].timestamp,
    last: .[-1].timestamp,
    messages: length,
    user_msgs: ([.[] | select(.message.role=="user")] | length),
    assistant_msgs: ([.[] | select(.message.role=="assistant")] | length),
    tool_calls: (tool_names | length),
    top_tools: (
      tool_names
      | group_by(.)
      | map({name: .[0], count: length})
      | sort_by(-.count)
      | .[:5]
    ),
    total_cost: ([.[] | .message.usage.cost.total // 0] | add)
  }
' <session>.jsonl
```

Use this when you need a fast "what changed?" summary to share in incident notes.

### Search across ALL sessions for a phrase

```bash
rg -l "phrase" ~/.openclaw/agents/<agentId>/sessions/*.jsonl
```

## Tips

- Sessions are append-only JSONL (one JSON object per line)
- Large sessions can be several MB - use `head`/`tail` for sampling
- The `sessions.json` index maps chat providers (discord, whatsapp, etc.) to session IDs
- Deleted sessions have `.deleted.<timestamp>` suffix
- Keep one baseline "healthy" session id around to compare against regressions quickly.

## Fast text-only hint (low noise)

```bash
jq -r 'select(.type=="message") | .message.content[]? | select(.type=="text") | .text' ~/.openclaw/agents/<agentId>/sessions/<id>.jsonl | rg 'keyword'
```
