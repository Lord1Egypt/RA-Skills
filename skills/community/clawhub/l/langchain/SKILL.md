---
name: langchain
slug: langchain
version: 1.0.1
description: >-
  Builds and debugs LangChain apps in Python: LCEL chains, agents, tools, retrievers, streaming, and structured output. Use when writing or reviewing a chain, agent, tool, retriever, or prompt template; when a prompt raises KeyError or "missing variables"; when streaming arrives as one blob or astream_events yields nothing; when an agent loops until GraphRecursionError or repeats a tool; when tool calls fail validation or the provider rejects a tool_call_id; when chat history disappears or the context window overflows; when with_structured_output returns None or a parser crashes on valid JSON; when retrieval returns the wrong chunks; when LangSmith traces are empty; when retries, rate limits, or token cost need bounding; or when imports break after an upgrade. Covers LangGraph state, checkpointers, and middleware. Not for framework-agnostic agent architecture (agents), retrieval design (rag), or chunk tuning (rag-chunking).
homepage: https://clawic.com/skills/langchain
changelog: "Full coverage pass: deeper guides, situation-named files, and per-user configuration"
metadata:
  clawdbot:
    emoji: 🦜
    requires:
      bins:
      - python3
    os:
    - linux
    - darwin
    - win32
    displayName: LangChain
    configPaths:
    - ~/Clawic/data/langchain/
---

User preferences and memory live in `~/Clawic/data/langchain/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/langchain/` or `~/clawic/langchain/`), move it to `~/Clawic/data/langchain/`.

## When To Use

- Writing or reviewing LCEL chains, agents, tools, prompt templates, retrievers, or LangGraph graphs
- Debugging a running app: empty streams, silent parser failures, agents that loop, history that vanishes, traces that never appear
- Choosing the abstraction: plain model call vs chain vs prebuilt agent vs hand-built graph
- Hardening for production: retries, rate limits, timeouts, caching, concurrency, cost ceilings, secret hygiene in traces
- Upgrading across versions: moved imports, `langchain-classic`, deprecated memory classes, pydantic v1→v2
- Not for framework-agnostic agent architecture (`agents`), retrieval strategy (`rag`), chunk-size tuning (`rag-chunking`), or provider API reference — this covers how all of those land in LangChain code

## Quick Reference

| Situation | Play |
|-----------|------|
| `Input to ChatPromptTemplate is missing variables` | Name mismatch or a literal `{` in the template — double it to `{{` → `debug.md` |
| A key I need later disappears mid-chain, or I am composing branches, fallbacks, or a configurable model | `RunnablePassthrough.assign` keeps what `RunnablePassthrough()` replaces; `RunnableBranch`, `.with_fallbacks`, `configurable_fields` → `lcel.md` |
| Building a prompt with few-shot examples, history, or partials | Templates, placeholders, and example selectors → `prompts.md` |
| Chain returns nothing useful and you cannot see why | `chain.get_graph().print_ascii()` for shape, then `astream_events(version="v2")` for the actual step I/O → `debug.md` |
| Streaming arrives as one blob at the end | A non-transform step buffers the stream; find the least streamable link → `streaming.md` |
| `astream_events` empty inside a custom function | Async config not propagated (Python ≤3.10 threads `config` by hand) → `streaming.md` |
| Agent never stops / `GraphRecursionError` | `recursion_limit` reached (Core Rule 5); bound the loop and handle the failure branch → `agent-loop.md` |
| Model ignores a tool, or calls the wrong one | The tool description is the whole prompt the model sees for it → `tools.md` |
| Provider 400: assistant tool_calls not followed by tool messages | History trimming split an AIMessage from its ToolMessage → `chat-history.md` |
| History resets on restart | `InMemorySaver` dies with the process; move to Sqlite/Postgres checkpointer → `chat-history.md` |
| `with_structured_output` returns None or raises | Use `include_raw=True` and read `parsing_error` before blaming the model → `structured-output.md` |
| Retrieval returns plausible-but-wrong chunks | Check k, splitter settings, and whether the score is distance or similarity → `retrieval.md` |
| Re-ingesting documents duplicates the index | Deterministic ids or the record-manager indexing API, not a second `add_documents` → `retrieval.md` |
| `ImportError` after upgrading | Moved to a partner package or `langchain-classic` → `migration.md` |
| 429s, cost spikes, or a hung request | Rate limiter, timeouts, caching, and concurrency caps → `production.md` |
| Traces empty or tokens unaccounted | Tracing env vars, `usage_metadata`, request-time vs constructor callbacks → `observability.md` |
| Tests hit the real API, or are flaky | Deterministic fake models and cached fixtures → `testing.md` |
| Untrusted documents reach the model, a tool can spend money or delete, or users share an index | Injection defense, approval gates, tenant isolation, trace privacy → `security.md` |
| Need branching, cycles, human approval, or shared state | The prebuilt agent loop is the wrong shape — build a graph → `langgraph.md` |
| Provider-specific parameter or multimodal input | `init_chat_model`, standard content blocks, per-provider differences → `models.md` |
| Anything else | Reproduce with the smallest runnable that fails (`prompt \| model` alone), then add one link at a time until it breaks |

Depth on demand: `lcel.md` composition · `prompts.md` templates and few-shot · `streaming.md` tokens and events · `models.md` providers and parameters · `chat-history.md` sessions and persistence · `retrieval.md` loaders, splitters, retrievers · `tools.md` tool definition and errors · `agent-loop.md` loop control and middleware · `langgraph.md` custom graphs · `structured-output.md` schemas and parsers · `debug.md` symptom→cause · `observability.md` tracing and token accounting · `security.md` injection, blast radius, isolation · `production.md` limits, caching, deployment · `testing.md` deterministic tests · `migration.md` version boundaries.

## Core Rules

1. **Every Runnable takes exactly one argument; a bare dict is a `RunnableParallel` and a bare function is a `RunnableLambda`.** `{"context": retriever, "question": RunnablePassthrough()} | prompt | model` works because of that coercion. The corollary bites: a coerced function receives the WHOLE input, so write `lambda x: x["question"]`, never `lambda question: ...`.
2. **Prompt variables are literal and case-sensitive; every real brace must be doubled.** `{Question}` and `{question}` are different variables, and one JSON example pasted into a template turns `{"a": 1}` into a variable named `"a": 1`. Escape as `{{"a": 1}}`, or keep examples out of the template and pass them as a variable.
3. **A chain streams end-to-end only if every link is a transform.** One step that returns a value instead of yielding buffers everything upstream: first-token latency becomes total generation time. `StrOutputParser` and `JsonOutputParser` stream; Pydantic parsing and any ordinary `RunnableLambda` do not (`streaming.md`).
4. **Count your retry layers — they multiply.** Client retries × chain retries: `ChatOpenAI(max_retries=2)` is 3 attempts, wrapped in `.with_retry(stop_after_attempt=3)` is 3 outer attempts, so 9 billed provider requests for one `invoke`. Pick one layer per failure class: client for transport/429, `.with_retry` for parse and validation failures.
5. **Bound the agent loop with a number you chose.** LangGraph's `recursion_limit` (default 25) counts node steps, and a tool-calling agent spends ~2 steps per tool call — 25 ≈ 12 tool calls before `GraphRecursionError`. Set it per invocation (`config={"recursion_limit": 40}`) and write the branch that handles hitting it.
6. **Persistence is a checkpointer keyed by `thread_id`, not an object you attach to a chain.** The old memory classes (`ConversationBufferMemory`, deprecated in 0.3.1) held state in a Python object that died with the process. `InMemorySaver` dies with it too; only a Sqlite/Postgres checkpointer survives a restart (`chat-history.md`).
7. **Trim on message boundaries, before you overflow.** `trim_messages(max_tokens=N, strategy="last", token_counter=model, include_system=True, start_on="human")` — a window starting on a `ToolMessage`, or one that keeps an AIMessage's `tool_calls` without their `ToolMessage`s, makes the provider reject the request outright.
8. **Invoke-time config is inherited; constructor config is not.** Callbacks, tags, and metadata passed as `.invoke(x, config={...})` reach every child runnable; callbacks set on a component's constructor apply to that component alone. In async code on Python ≤3.10 (`python_runtime: 3.10`), `config` must be threaded into every custom function by hand — `async def f(x, config): await inner.ainvoke(x, config)` — or child runs vanish from traces and `astream_events` yields nothing. Check this before shipping any async path on 3.10.
9. **Pin `langchain`, `langchain-core`, and every partner package together.** They all resolve one `langchain-core`; a mismatch surfaces as `ImportError` or a pydantic `ValidationError` deep inside a call that looks like your bug. One lockfile, one upgrade commit, and read `migration.md` before bumping a major.

## Error Messages

The message names a layer, rarely the cause. Decode before editing code.

| Message | What it actually means | First move |
|---|---|---|
| `KeyError: 'x'` / `missing variables {'x'}` | Template expects a variable the chain never passes, or an unescaped `{` created a phantom one | `prompt.input_variables` vs `chain.input_schema.model_json_schema()` |
| `Expected mapping type as input to ChatPromptTemplate` | A bare string reached a chain whose first step is a prompt with named variables | Wrap: `chain.invoke({"question": q})` |
| `OutputParserException` | The model returned prose, a fenced block, or a near-miss schema | `include_raw=True` and read the raw message (`structured-output.md`) |
| `ValidationError` (pydantic) | Schema mismatch, or a v1 `BaseModel` passed where v2 is expected | Check which pydantic the model class was defined with (`migration.md`) |
| `GraphRecursionError` | Loop hit `recursion_limit` (Core Rule 5) | Read the last 3 steps in the trace: the agent is usually re-calling one failing tool |
| `An assistant message with 'tool_calls' must be followed by tool messages` | History trimming or manual editing broke tool-call pairing | `chat-history.md` trimming rules |
| `ImportError: cannot import name … from 'langchain'` | The symbol moved to a partner package or `langchain-classic` | `migration.md` import table |
| `NotImplementedError` on `.stream()` | A component has no streaming implementation; the chain falls back to one chunk | `streaming.md` |
| `de-serialization relies on loading a pickle file` | FAISS refuses to load an index without `allow_dangerous_deserialization=True` | Only pass it for files you produced (`security.md`) |
| `RateLimitError` / HTTP 429 | Provider throughput limit, usually from unbounded `.batch()` | `InMemoryRateLimiter` + `max_concurrency` (`production.md`) |
| Empty trace, no error | Tracing env vars unset, or async config not propagated | `observability.md` |

## Choosing The Abstraction

| Need | Build | Why |
|---|---|---|
| One call with a schema | `model.with_structured_output(Schema)` | No chain needed; a chain around a single call only adds indirection |
| Fixed sequence known in advance | LCEL chain (`prompt \| model \| parser`) | Free streaming, batching, async, and per-step traces |
| Model decides which tools to call, until done | `create_agent(model, tools)` | The loop, tool execution, and message bookkeeping are the part you should not rewrite |
| Branching, cycles, human approval, parallel fan-out over shared state | A LangGraph graph | The prebuilt loop has one shape; a graph has the shape you draw (`langgraph.md`) |
| Anything else | Start with the chain | Promote to an agent only when the tool sequence genuinely cannot be known ahead of time |

## Cost Grows Quadratically In Agent Steps

Every agent step resends the whole transcript. If each step adds `T` tokens, total input across `N` steps is `T × N(N+1)/2`, not `T × N`.

Worked: `T` = 1,500 tokens per step (tool result + reasoning), `N` = 10 tool calls → 1,500 × 10 × 11 / 2 = **82,500 input tokens** for one task, against the 15,000 a linear estimate predicts. Consequences: cap tool output size at the tool (`tools.md`), summarize or trim mid-run (`chat-history.md`), and set `recursion_limit` as a cost ceiling, not just a safety net.

## Output Gates

Before shipping a chain, agent, or graph:

- Prompt template variables verified against what the chain passes (`chain.input_schema`), and every literal brace doubled?
- Exercised with `.stream()`, not only `.invoke()` — first-token latency actually observed?
- Limits counted and bounded — retry layers (Core Rule 4), a client `timeout`, and a `recursion_limit` or iteration cap plus a wall clock on every agent path — each with the branch that handles hitting it written?
- Structured output has an explicit failure path (`include_raw=True` or a caught parser exception)?
- History on a checkpointer that survives a restart (or ephemerality documented on purpose), keyed by a `thread_id` derived from real session identity — never a constant, never shared across users?
- Nothing secret in tags, metadata, or traced payloads; PII redaction decided per `trace_pii`?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/langchain/config.yaml`. Never interview the user — record a preference the moment it is stated.

| Variable | Type | Default | Effect |
|---|---|---|---|
| lc_version_line | 0.3 \| 1.x | 1.x | Selects import paths and APIs everywhere: `1.x` uses `langchain.agents.create_agent` and assumes legacy chains live in `langchain-classic`; `0.3` keeps `langgraph.prebuilt.create_react_agent` and the pre-split imports (`migration.md`) |
| chat_provider | openai \| anthropic \| google \| azure \| bedrock \| ollama | openai | Provider used in every emitted example and in `init_chat_model` strings; drives which parameter quirks and rate-limit advice apply (`models.md`) |
| vector_store | chroma \| faiss \| pgvector \| qdrant \| pinecone | chroma | Retrieval examples, persistence advice, and score interpretation (distance vs similarity) in `retrieval.md` |
| python_runtime | 3.10 \| 3.11+ | 3.11+ | At `3.10`, async examples thread `RunnableConfig` manually through custom functions (Core Rule 8) and callback-propagation warnings are emitted |
| async_style | sync \| async | sync | Whether emitted code uses `invoke`/`stream` or `ainvoke`/`astream`, and which concurrency controls are shown |
| tracing | none \| langsmith \| otel | none | Whether scaffolds wire tracing env vars and which observability path `observability.md` recommends |
| trace_pii | redact \| allow | redact | Whether prompts and tool payloads may reach a tracing backend unmasked; gates the tracing Output Gate |
| structured_output_method | tool_calling \| json_schema \| parser | tool_calling | Default strategy in `structured-output.md` when a schema is requested |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **Tooling**: package manager and lock strategy, LangGraph vs plain LCEL, LangSmith vs OpenTelemetry vs plain logging, notebook vs module layout — affects every scaffold and `observability.md`
- **Conventions**: where prompts live (code, YAML, or a prompt registry), run and tag naming, chain/module file layout, typed state classes vs dicts — affects `lcel.md` and `langgraph.md` examples
- **Platform**: deployment target (script, FastAPI service, worker queue, serverless, LangGraph Platform) and whether cold starts and event-loop constraints apply — affects `production.md`
- **Safety posture**: human approval before destructive tools, tool allowlists, whether `allow_dangerous_deserialization` and arbitrary-code tools are permitted at all — affects `tools.md` and `agent-loop.md`
- **Cost posture**: model tiering (cheap draft, expensive final), caching aggressiveness, per-request token ceilings, acceptable latency-for-cost trades — affects `production.md`
- **Retrieval conventions**: chunk sizing habits, metadata fields carried on every document, whether citations are mandatory in answers — affects `retrieval.md`
- **Cadence**: when the eval set runs (every prompt or model change vs nightly vs pre-release), when recorded fixtures get re-recorded (every model upgrade vs only on failure), how often langchain packages are bumped (scheduled upgrade PR vs on demand) — affects `testing.md` CI Shape and `migration.md`
- **Output format**: full files vs diffs, inline type hints, how much explanation accompanies emitted code

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| `for x in items: chain.invoke(x)` | Serial round-trips; latency is the sum, and provider concurrency sits idle | `chain.batch(items, config={"max_concurrency": 5})`, or `abatch` under async |
| One `thread_id` for every user | Checkpointer state is keyed only by that id — user B reads user A's conversation | Derive it from the authenticated session id (`chat-history.md`) |
| `handle_parsing_errors=True` as the fix | Hides a schema bug and pays for an extra model call every time it fires | Read the raw output once, fix the schema or the prompt, keep the handler as a floor |
| Chunk overlap set near or above chunk size | Overlap is subtracted from forward progress; the splitter loops or explodes the chunk count | Overlap ≤ 20% of chunk size (`retrieval.md`) |
| Comparing scores across vector stores | Some return distance (lower is better), others similarity (higher is better) — thresholds silently invert | Check the store's semantics before setting any threshold (`retrieval.md`) |
| Building the retriever inside the request handler | Re-loads or re-embeds the index on every call; p99 is dominated by setup | Build once at startup, inject the retriever |
| `verbose=True` as the debugging strategy | Prints a partial, unstructured view and nothing about async children | `astream_events(version="v2")` or a trace (`debug.md`) |
| `except Exception as e: log(str(e))` around a provider call | Discards the provider's response body, which contains the actual reason | Log `e.response.text` / `e.body` where the client exposes it |
| Pasting the whole document into the prompt when retrieval "doesn't work" | Trades a fixable retrieval bug for a permanent cost and recall problem | Fix k, the splitter, or the query first (`retrieval.md`) |
| Wrapping every step in `RunnableLambda` | Each opaque lambda kills streaming and flattens the trace into one box | Compose runnables; use lambdas for genuinely custom logic, as generators when they sit in a streaming path |
| `FAISS.load_local(..., allow_dangerous_deserialization=True)` on a downloaded index | It is a pickle — loading executes arbitrary code | Only load indexes you built; otherwise re-embed from source |

## Where Experts Disagree

- **LCEL vs plain Python.** LCEL buys streaming, batching, async, retries, and per-step traces for free; plain functions are easier to step through in a debugger. Boundary: token streaming, parallel branches, or step-level observability → LCEL; a linear script that calls the model twice → plain Python with the model client.
- **Framework vs provider SDK.** The framework earns its place with tool loops, retrieval integrations, and provider portability. A single prompt-in/JSON-out endpoint does not need it — that is where "LangChain is bloated" arguments are actually right.
- **Prebuilt agent vs hand-built graph.** Start prebuilt: the loop, tool bookkeeping, and streaming are solved. Move to a graph when you need control flow BETWEEN tool calls (approval gates, validation nodes, fan-out) — not because the graph looks more serious.
- **Long context vs retrieval.** Stuffing a large corpus works and is simple until cost per request or corpus churn dominates. Boundary: recompute the per-request token bill at real traffic; retrieval wins when the corpus changes faster than you can re-send it.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/langchain (install if the user confirms):
- `agents` — agent architecture, framework selection, and memory design before any of it is LangChain code
- `rag` — retrieval pipeline design, framework-agnostic
- `rag-chunking` — chunk strategy and size tuning
- `prompting` — what to write inside the templates
- `structured-output` — schema constraint and constrained decoding across providers

## Feedback

- If useful, star it: https://clawic.com/skills/langchain
- Latest version: https://clawic.com/skills/langchain

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/langchain.
