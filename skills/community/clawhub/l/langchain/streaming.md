# Streaming — Tokens, Events, and What Silently Buffers

Two different mechanisms, constantly confused: `.stream()` yields the chain's OUTPUT incrementally; `.astream_events()` yields a structured event per step of the whole chain, including intermediate ones.

## The Streamability Rule

A chain streams end-to-end only if every link implements `transform` (consumes an iterator, yields as it goes). One buffering link and everything upstream is collected first — the chain still "works", it just delivers first token at total-generation latency (SKILL.md Core Rule 3).

| Component | Streams? |
|---|---|
| Chat models | Yes, token by token |
| `StrOutputParser` | Yes — passthrough transform |
| `JsonOutputParser` | Yes — emits progressively completed partial objects |
| `PydanticOutputParser`, `with_structured_output` | No — needs the complete text to validate |
| Retrievers, most tools | No — single result, by nature |
| `RunnableLambda(f)` where `f` returns a value | **No** — the usual culprit |
| `RunnableLambda(g)` where `g` is a generator | Yes |

Make a custom step streamable by writing it as a generator over the input iterator:

```python
def upper(chunks):          # receives an iterator, yields chunks
    for c in chunks:
        yield c.upper()
chain = model | StrOutputParser() | upper      # coerced, and it streams
```

## Diagnosing "It Doesn't Stream"

1. `for c in (prompt | model).stream(x): print(c.content, end="")` — if the raw model streams, the model is not the problem.
2. Add links back one at a time; the link that restores the pause is the buffering one.
3. Confirm with timing, not feel: record `time.perf_counter()` at first chunk and at last. First-token ≈ total means fully buffered.
4. Providers that stream only with a flag are a separate class: some clients need `streaming=True` or return usage only with `stream_usage=True`.

## astream_events

```python
async for ev in chain.astream_events({"question": q}, version="v2"):
    kind = ev["event"]          # on_chat_model_stream, on_retriever_end, on_tool_start, ...
    if kind == "on_chat_model_stream":
        print(ev["data"]["chunk"].content, end="")
    elif kind == "on_retriever_end":
        docs = ev["data"]["output"]
```

- `version="v2"` is required; v1 is the legacy shape and its event payloads differ.
- Filter with `include_names=[...]`, `include_tags=[...]`, `include_types=["chat_model"]` — pair with `.with_config(run_name=...)` so filtering is stable when you refactor.
- Event names follow `on_<type>_<start|stream|end>`. `on_chat_model_stream` is tokens; `on_chain_end` for a named sub-chain is the clean place to grab an intermediate result.

## The Async Propagation Trap (Python ≤3.10)

Inside a custom async function, child runnables lose their parent context unless you pass `config` through. Python 3.11+ propagates it via contextvars automatically; 3.10 and below do not — and the failure is silent: no error, just an empty `astream_events` stream and missing trace nodes.

```python
from langchain_core.runnables import RunnableConfig

async def step(x: dict, config: RunnableConfig):     # accept it
    return await sub_chain.ainvoke(x["q"], config)   # and forward it
```

Same rule for callbacks passed into tools and for `astream_events` inside a tool implementation. Set `python_runtime` in config so this warning is emitted only where it applies.

## Streaming Structured Output

You cannot stream a validated Pydantic object, but you can stream toward one:

- `JsonOutputParser` yields partial dicts as the JSON completes — good for progressively filling a UI, unusable for anything that must be valid before use.
- With tool-calling schemas, chunk `.tool_call_chunks` carry partial arguments; accumulate and validate once at the end.
- Practical split: stream the prose to the user, run the structured extraction as a second, non-streamed call.

## Streaming Through A Web Layer

- Yield strings, not model chunk objects — serialize at the boundary (`chunk.content`).
- Flush per chunk. A buffering proxy or a response object that batches will hide a perfectly good stream; test against the real deployment, not the dev server.
- Send a terminal sentinel event so the client can distinguish "done" from "connection dropped mid-generation", and handle client disconnects by cancelling the task — an abandoned generation still bills.
- Errors thrown mid-stream arrive after headers are sent: reserve an error event type in the protocol instead of relying on status codes.

## Cancellation and Timeouts

`astream` respects task cancellation, so wrapping a stream in `asyncio.wait_for` stops generation at the provider. A sync `.stream()` in a thread does not cancel — for user-facing endpoints with a hard latency budget, use the async path.
