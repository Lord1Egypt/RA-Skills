# Chat History — Sessions, Persistence, Trimming

The mental model changed: history is not an object bolted onto a chain, it is checkpointed state keyed by a thread id (SKILL.md Core Rule 6). The old classes still appear in every tutorial written before the change.

## Status Of The Old API

| Legacy | Status | Replacement |
|---|---|---|
| `ConversationBufferMemory` and friends | Deprecated in 0.3.1, moved to `langchain-classic` in 1.0 | Checkpointer |
| `ConversationChain` | Same | `create_agent` or an LCEL chain plus a checkpointer |
| `RunnableWithMessageHistory` | Deprecated in 0.3, still functional | Checkpointer; keep only for a chain you are not migrating yet |
| `BaseChatMessageHistory` stores (Redis, Postgres, file) | Alive — they are storage backends | Still usable directly when you want to own the read/write yourself |

## Persistence With A Checkpointer

```python
from langgraph.checkpoint.memory import InMemorySaver
agent = create_agent(model, tools, checkpointer=InMemorySaver())

cfg = {"configurable": {"thread_id": session_id}}
agent.invoke({"messages": [("user", "hi")]}, cfg)
agent.invoke({"messages": [("user", "what did I just say?")]}, cfg)   # same thread → remembers
```

- `thread_id` IS the session boundary. Derive it from the authenticated session or conversation record; a constant id merges every user into one conversation and leaks history across them (SKILL.md Traps).
- `InMemorySaver` (aliased `MemorySaver`) is process-local: correct in tests and notebooks, wrong in any deployment with restarts or more than one worker.
- Durable options: `SqliteSaver` for a single-node app, `PostgresSaver` for anything multi-worker. Both need their `setup()` migration run once before first use, and the async variants (`AsyncSqliteSaver`, `AsyncPostgresSaver`) must be used on the async path.
- Checkpointers store a full state snapshot per step, so a long thread costs storage. Prune or archive old threads on a schedule; nothing does it for you.

## Threads vs Long-Term Memory

- **Thread-scoped** (checkpointer): the running conversation, including tool calls and interrupts. Dies with the thread.
- **Cross-thread** (`BaseStore`, e.g. `InMemoryStore` / a Postgres store): facts about the user that must outlive the conversation, namespaced by user id and written deliberately, never by dumping every turn.
- The mistake is using the checkpointer as the user profile: the moment the session id rotates, the "memory" is gone. Decide per fact which store it belongs to.

## Trimming Before Overflow

```python
from langchain_core.messages import trim_messages
trimmed = trim_messages(
    messages,
    max_tokens=4000,
    strategy="last",          # keep the newest; "first" keeps the oldest
    token_counter=model,      # the model's own counter, not len()
    include_system=True,      # keep the system prompt regardless
    start_on="human",         # windows may not start mid-exchange
    allow_partial=False,
)
```

Rules that turn into provider 400s when broken (SKILL.md Core Rule 7):

- A window must not start on a `ToolMessage` or on an `AIMessage` — `start_on="human"`.
- An `AIMessage` carrying `tool_calls` must keep every matching `ToolMessage` in the window; drop the pair together or keep it together.
- The system message is not automatically preserved — `include_system=True` or it silently disappears and behavior drifts.
- Counting with `len()` or a word count under-counts non-English text and code; use the model as `token_counter`.

Wire it into the chain so it always runs:

```python
chain = RunnablePassthrough.assign(history=lambda x: trim_messages(x["history"], ...)) | prompt | model
```

For an agent, trimming and summarization belong in middleware so they apply on every model call inside the loop.

## Summarization Instead Of Dropping

When old turns carry decisions you cannot lose, replace them rather than truncate:

1. Keep the last `k` turns verbatim (the model needs recent wording).
2. Summarize everything older into one system-level note, and store the summary in state so it is computed once per overflow, not per request.
3. Re-summarize the summary plus the newly dropped turns when you overflow again — otherwise the summary itself grows into the problem it solved.

Cost note: summarization is an extra model call per overflow, cheap next to resending the transcript every step (SKILL.md Cost Grows Quadratically).

## Inspecting And Editing State

```python
state = agent.get_state(cfg)                 # current values + next node
history = list(agent.get_state_history(cfg)) # every checkpoint, newest first
agent.update_state(cfg, {"messages": [...]}) # append or overwrite by reducer
```

Time travel — resume from an older checkpoint by passing its `checkpoint_id` in config — is what makes "undo the last tool call and retry with a different argument" possible.

## Retrofitting An Existing LCEL Chain

The lowest-friction path for a chain you do not want to rewrite: keep your own list of messages in your own store, pass it as a template variable, and trim on the way in. That is honest and debuggable. Reach for `RunnableWithMessageHistory` only if it is already in the codebase — it is deprecated, and its `session_id` config plumbing is the reason.
