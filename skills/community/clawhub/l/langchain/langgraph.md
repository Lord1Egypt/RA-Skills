# LangGraph — When The Loop Is Not The Shape You Need

The prebuilt agent loop is one graph with one shape. Build your own when you need control flow BETWEEN model calls: branching, cycles you define, parallel fan-out over shared state, approval gates, or retry logic that depends on state.

## State, Nodes, Edges

```python
from typing import Annotated, TypedDict
from operator import add
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    messages: Annotated[list, add]   # reducer: appended, not replaced
    draft: str                       # no reducer: last write wins
    attempts: int

def draft_node(state: State) -> dict:
    return {"draft": model.invoke(state["messages"]).content}   # return ONLY changed keys

g = StateGraph(State)
g.add_node("draft", draft_node)
g.add_node("review", review_node)
g.add_edge(START, "draft")
g.add_conditional_edges("draft", lambda s: "review" if s["attempts"] < 3 else END)
g.add_edge("review", "draft")
app = g.compile(checkpointer=checkpointer)
```

- A node returns a **partial** state update. Returning the whole state is legal and is how people accidentally clobber a key another branch just wrote.
- The reducer decides merge semantics. Without one, concurrent writes to the same key from parallel branches raise `InvalidUpdateError`; with `add` (or `add_messages` for message lists) they combine.
- `add_messages` also handles updates by message id — that is what lets you replace a message rather than append a duplicate.
- Conditional edges return the next node name (or a list, to fan out). Returning a name that is not a node fails at runtime, not at compile.

## Cycles Need Their Own Counter

`recursion_limit` (default 25, same value as the agent loop — SKILL.md Core Rule 5) is a safety net, not your business rule. Put an explicit `attempts` counter in state and branch on it, so hitting the ceiling is a decision you made rather than an exception you caught.

## Parallelism

- Several edges out of one node run those nodes in the same superstep; their updates merge through reducers at the end of the step.
- A node that must wait for two branches simply has both as predecessors — the graph joins there automatically.
- `Send` dispatches a dynamic number of parallel node invocations (map over a list), each with its own payload; the classic map-reduce shape for "process every document, then combine".

## Human In The Loop

```python
from langgraph.types import interrupt, Command

def approve(state):
    decision = interrupt({"action": state["proposed_action"]})   # execution stops here
    return {"approved": decision == "yes"}

app.invoke(Command(resume="yes"), cfg)     # later, same thread_id
```

- `interrupt` requires a checkpointer: state is persisted, the process can exit, and the run resumes later on the same `thread_id` (SKILL.md Core Rule 6).
- `interrupt_before=["tools"]` at compile time is the coarse version — good for approving every tool call during development.
- On resume the node re-executes from its start, so any side effect performed BEFORE the `interrupt` call runs twice. Put side effects after the gate.

## Durability And Recovery

- Every superstep writes a checkpoint, so a crashed run resumes from the last completed step rather than the beginning — the reason long or expensive graphs belong here rather than in a plain loop.
- `get_state_history(cfg)` lists checkpoints; passing an older `checkpoint_id` in config resumes from it, optionally after `update_state` — undo and retry with a different value.
- Long-running steps still need their own idempotency: the checkpoint records that a node ran, not that a remote payment succeeded.

## Subgraphs

A compiled graph is a node. Two contracts:

- Shared state keys → the subgraph reads and writes the parent's state directly.
- Different schema → wrap it in a function that maps parent state in and subgraph output back out.

Subgraphs keep their own checkpoints; `get_state(cfg, subgraphs=True)` is how you see inside one when debugging.

## Streaming A Graph

`stream_mode` values: `"values"` (full state per step), `"updates"` (only what each node changed), `"messages"` (LLM tokens with node metadata), `"custom"` (whatever a node emits via the stream writer), `"debug"` (everything). Pass a list to get several at once — `["updates", "messages"]` is the practical default for a UI that shows both progress and tokens.

## When To Stop Using A Graph

Two nodes and one edge is a chain with extra ceremony. Rewrite as a graph when at least one of these is true: a cycle with a stopping rule, a branch the model chooses at runtime, an approval gate, parallel fan-out with a join, or resumability across process restarts.
