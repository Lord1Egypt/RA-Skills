# Parallel Thinker Skill

**Purpose**: Enable any agent to quickly obtain multi-perspective analysis by invoking specialized agents in parallel.

## When to Use

Invoke this tool when:
- User asks complex, multi-faceted questions requiring strategic, analytical, financial, technical, or research insights
- Single-agent response would be too narrow
- You need to speed up response by parallelizing expert queries

## How to Use

Call the `parallel_think` tool with:
- `query`: the original user question
- `agents` (optional): list of agent IDs to consult (default: ["strategist", "data-analyst", "finance", "expert-coder", "researcher"])
- `synthesizer_agent` (optional): agent ID to synthesize results (default: "synthesizer")

Example:
```json
{
  "query": "Should we invest in gold now?",
  "agents": ["strategist", "data-analyst", "finance"]
}
```

## What Happens

1. The tool sends the query to each specified agent in parallel (non-blocking)
2. Waits for all responses (timeout 30s per agent)
3. Forwards the query and all responses to the synthesizer agent for consolidation
4. Returns the synthesized answer to you

## Implementation Details

- Uses OpenClaw CLI `openclaw agent --agent <id> --message <text>`
- Concurrency: up to 5 parallel calls (configurable via `maxConcurrent`)
- Timeouts: 30s per agent, 60s for synthesizer
- If any agent fails or times out, results are omitted and synthesizer proceeds with available answers