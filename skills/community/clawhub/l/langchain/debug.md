# Debugging — Symptom To Cause

LangChain failures mislead because the error surfaces one or two layers below where you wrote the bug: a prompt typo arrives as a `KeyError` from a template, a config problem arrives as an empty stream, a provider rejection arrives as a pydantic error. Work symptom-first; every step is a check, not a guess.

## The Universal First Three

1. **Shape**: `chain.get_graph().print_ascii()` — the wiring that actually runs, including coerced dicts and lambdas. A missing step here explains most "it ignores my X".
2. **Contract**: `chain.input_schema.model_json_schema()` against what you pass. Settles every missing-variable argument in one command.
3. **Traffic**: `astream_events(version="v2")` (or a trace) — the input and output of every step. Print `ev["event"]`, `ev["name"]`, and `ev["data"]` for the first twenty events and the wrong value announces itself.

`set_debug(True)` from `langchain_core.globals` dumps everything and is fine for a five-line script; it is unreadable for anything real and prints nothing useful about async children.

## Missing Or Wrong Prompt Variables

1. `prompt.input_variables` — includes anything created by an unescaped `{`. A variable you never wrote means a literal brace needs doubling (SKILL.md Core Rule 2).
2. Compare with the keys the previous step emits: `prev.invoke(x)` and look at the dict.
3. `RunnablePassthrough` vs `.assign`: plain passthrough REPLACES the dict with the input; `.assign` keeps it and adds keys. Losing `question` three steps in is always this.
4. Bare string into a multi-variable chain → wrap in a dict, or start the chain with `{"question": RunnablePassthrough()}`.

## The Chain Runs But The Answer Is Wrong

1. Print the FINAL prompt, not the template: `prompt.invoke(inputs).to_string()`. Half of "the model is dumb" is a prompt with an empty context block.
2. Empty context → the retriever returned nothing; query the store directly with the user's exact words before touching the prompt.
3. Correct context, wrong answer → test the same prompt in isolation against the model. If it fails there, it is a prompt problem, not a LangChain problem.
4. Right sometimes → temperature, history contamination from a shared `thread_id`, or a fallback model silently serving the request.

## Nothing Streams / Events Are Empty

1. Does the raw model stream? `(prompt | model).stream(x)`.
2. Add links back one at a time until the pause returns — that link buffers.
3. Empty `astream_events` inside a custom async function on Python ≤3.10 → `config` was not threaded through (SKILL.md Core Rule 8).
4. Everything streams in a script but not in the service → the web layer buffers; test against the deployed stack.

## Agent Loops Or Stops Early

1. Read the last three steps of the trace. Repeated identical tool calls → the tool's error text is not actionable.
2. `GraphRecursionError` → the loop hit `recursion_limit`; raise it only after ruling out a tool that fails identically every time, two tools with overlapping descriptions, an unstated success condition, and oversized tool output.
3. Stops without answering → the model emitted a tool call the executor could not match (renamed tool, schema mismatch), or an unhandled tool exception ended the run.
4. Right answer, absurd cost → count the steps and apply the quadratic formula (SKILL.md); the fix is smaller tool output, not a bigger budget.

## Import And Version Errors

| Symptom | Cause |
|---|---|
| `ImportError: cannot import name X from 'langchain'` | Moved to a partner package or `langchain-classic` |
| `ModuleNotFoundError: langchain_community` | Community integrations are a separate install |
| pydantic `ValidationError` inside library code | v1 model passed where v2 expected, or mismatched `langchain-core` versions |
| Two versions of `langchain-core` resolved | A partner package pinned an older core; `pip list \| grep langchain` and align in one lockfile (SKILL.md Core Rule 9) |
| Code from a tutorial fails wholesale | The tutorial predates the version split; check its imports against the migration table |

## Async Errors

- `this event loop is already running` → `asyncio.run()` (or `.invoke()` wrapping something that starts a loop) inside an existing loop — notebooks and web handlers. Use the `a*` methods.
- `coroutine was never awaited` → an async tool or lambda invoked from a sync chain path.
- Async works alone, hangs in the service → a sync-only step is blocking the event loop; give it an `afunc`.

## Intermittent Failures

- Only at concurrency → rate limits (429s retried into latency) or a shared mutable object captured by a chain. Runnables are safe to share; your closures over mutable state are not.
- Only for some inputs → length. Check whether the input crossed the context window or `max_tokens` truncated the output mid-object.
- Only in production → different model tier, different keys/region, missing env var, or a `config.yaml` you have locally and the server does not.
- Only after a deploy → a floating dependency version. Diff the lockfile before debugging anything else.

## When You Are Truly Stuck

Rebuild the smallest failing unit: `prompt | model` with a hardcoded input, no parser, no retriever, no history. Add one link at a time. The link that reintroduces the failure names the guide to open next in SKILL.md Quick Reference — and if nothing does, the problem is the input data, not the chain.
