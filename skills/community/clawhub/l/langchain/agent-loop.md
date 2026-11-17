# Agents — The Loop, Its Limits, and Middleware

An agent is a loop: model → tool calls → tool results → model, until the model answers without calling a tool. Everything hard about agents is bounding that loop and controlling what enters the prompt on each pass.

## Building One

```python
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-4.1-mini",
    tools=[search_orders, issue_refund],
    system_prompt="You are a support agent. Verify the order before refunding.",
    checkpointer=checkpointer,     # persistence, keyed by thread_id
    middleware=[...],              # cross-cutting control, below
)
result = agent.invoke({"messages": [("user", q)]}, {"configurable": {"thread_id": sid}, "recursion_limit": 40})
print(result["messages"][-1].content)
```

- Input and output are message lists in state, not a bare string — `result["messages"][-1]` is the answer, and everything before it is the audit trail.
- In 1.x this lives in `langchain.agents`; `langgraph.prebuilt.create_react_agent` is the deprecated predecessor and `AgentExecutor` the legacy one before that.
- `stream_mode="values"` yields state after each step, `"updates"` yields only deltas, `"messages"` yields tokens. Pick per UI need.

## Bounding The Loop

| Control | Default | What it does |
|---|---|---|
| `recursion_limit` (config) | 25 | Node steps before `GraphRecursionError`; ~2 steps per tool call → ~12 tool calls (SKILL.md Core Rule 5) |
| `max_iterations` (legacy `AgentExecutor`) | 15 | Tool-call iterations before stopping; only relevant on the legacy path |
| Per-run wall clock | none | Enforce with `asyncio.wait_for` around `ainvoke`/`astream` — a bounded step count is not a bounded duration |
| Token budget | none | Track cumulative `usage_metadata` and stop the loop yourself |

Always write the branch that handles the limit:

```python
from langgraph.errors import GraphRecursionError
try:
    result = agent.invoke(state, cfg)
except GraphRecursionError:
    result = fallback_answer(state)     # partial state is still in the checkpointer
```

## Why Agents Loop (in order of frequency)

1. **A tool fails the same way every time** and the error text does not say what to do differently — the model retries verbatim. Fix the error message first: it is the only instruction the model gets after a failure.
2. **Two tools overlap** and neither description disambiguates; the model alternates between them.
3. **The success condition is unstated.** Add it to the system prompt: what "done" looks like and that it should answer directly when it has enough.
4. **Tool output is too large**, so the relevant fact scrolls out of attention and the model re-fetches it.
5. **The task genuinely needs more steps** — raise `recursion_limit` deliberately, after ruling out the four above.

Read the trace before changing the prompt: the last three steps name the cause every time.

## Middleware

Middleware is where cross-cutting behavior belongs in 1.x — the hooks run around the agent loop, so they apply to every model call and every tool call without touching the tools themselves.

| Hook | Runs | Typical use |
|---|---|---|
| `before_agent` | Once per invocation | Load user context, seed state |
| `before_model` | Before each model call | Trim or summarize history, inject dynamic instructions |
| `wrap_model_call` | Around each model call | Model fallback, per-call parameter changes, retries with a different model |
| `after_model` | After each model call | Validate or reject the proposed tool calls, guardrails |
| `wrap_tool_call` | Around each tool execution | Timeouts, argument sanitization, approval gates, result truncation |
| `after_agent` | Once at the end | Persist results, emit metrics |

Built-ins cover the common needs: summarization when context grows, human-in-the-loop approval for named tools, PII redaction. Reach for a custom hook only when the behavior is genuinely yours.

Rule of placement: anything that must hold for EVERY step goes in middleware; anything specific to one tool goes in the tool. Prompt-level pleading ("always check the balance first") is the weakest of the three.

## Dynamic Tool Selection

**Canonical ceiling: ~20 tools bound to one agent.** Past that, route instead of adding — this is the number `tools.md` cites. Two costs compound: every bound description is resent on every step (prompt weight = one description × tools bound × steps, SKILL.md cost formula), and each additional near-neighbour makes the choice between two similar tools more like a coin flip.

Options in order of preference:

1. Select per turn in `before_model` — filter the bound tools by the current task or user role.
2. Split into sub-agents by domain, with a router agent whose "tools" are the sub-agents.
3. A retrieval step over tool descriptions when the catalog is genuinely open-ended.

Each unused tool description is prompt weight on every step and one more chance to be picked wrongly.

## Structured Answers From An Agent

Ask for a schema on the final answer via the agent's structured-output support rather than parsing prose afterwards; the loop can then produce the object as its terminal step instead of paying for a second extraction call.

## Multi-Agent Shapes

- **Supervisor**: one router delegates to specialists and owns the final answer. Predictable, easy to trace, one extra model call per hop.
- **Handoff**: agents transfer control to each other as tools. Fewer hops, harder to bound — cap total handoffs explicitly.
- **Pipeline**: fixed sequence of agents. If the sequence is truly fixed, you want a chain or a graph, not agents (SKILL.md Choosing The Abstraction).

Multi-agent multiplies the cost formula: every hop resends its own transcript. Prove a single agent cannot do it before splitting.
