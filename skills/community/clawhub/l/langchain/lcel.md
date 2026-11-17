# LCEL — Composing Runnables

Everything with `.invoke` is a Runnable, and every Runnable supports `invoke / batch / stream / ainvoke / abatch / astream / astream_events`. Compose with `|` and you get all of them for free — that is the entire value proposition.

## The Coercion Rules (source of most "why is my input wrong")

Inside a chain, LangChain coerces three things:

| You write | It becomes | Consequence |
|---|---|---|
| `{"a": chainA, "b": chainB}` | `RunnableParallel` | Branches run concurrently, each receiving the SAME input |
| `lambda x: ...` or a plain function | `RunnableLambda` | Receives the whole input as one argument — never destructured |
| `itemgetter("q")` | `RunnableLambda` | The idiomatic key extractor: `from operator import itemgetter` |

Coercion only happens when at least one operand is already a Runnable. `{"a": lambda x: x} | prompt` works; `{"a": lambda x: x}` alone is a dict.

## The Canonical Shapes

```python
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

# 1. Straight pipeline
chain = prompt | model | StrOutputParser()

# 2. Fan-in: build the prompt's variables from one input
rag = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt | model | StrOutputParser()
)

# 3. Keep the input AND add fields (assign never drops keys)
chain = RunnablePassthrough.assign(context=itemgetter("question") | retriever) | prompt | model

# 4. Return the answer plus what produced it
chain = RunnableParallel(answer=rag, sources=itemgetter("question") | retriever)
```

- `RunnablePassthrough()` forwards input unchanged; `.assign(k=...)` forwards it **and** adds keys. Choosing `assign` is what keeps `question` available three steps later.
- `.pick("answer")` narrows a dict output; `.map()` applies a runnable to every element of a list input.

## Per-Runnable Behavior

| Method | Use | Watch out |
|---|---|---|
| `.bind(stop=["\n"], tools=[...])` | Freeze a model kwarg inside a chain | Silently overridden by the same kwarg at invoke time |
| `.with_config(run_name="rag", tags=["prod"])` | Name the step in traces | Cosmetic, but it is what makes a 40-node trace readable |
| `.with_retry(stop_after_attempt=3)` | Retry a step on exception | Composes with client retries — multiply them (SKILL.md Core Rule 4) |
| `.with_fallbacks([cheap_chain])` | Swap in another runnable on failure | Fallback receives the ORIGINAL input, not the partial output |
| `.with_types(input_type=..., output_type=...)` | Fix schemas the inference gets wrong | Needed when a lambda erases typing |
| `.with_listeners(on_start=, on_end=, on_error=)` | Side effects around one step | Prefer callbacks for anything cross-cutting |

## Branching

```python
from langchain_core.runnables import RunnableBranch
route = RunnableBranch(
    (lambda x: "sql" in x["question"].lower(), sql_chain),
    (lambda x: len(x["question"]) > 500, summarize_chain),
    default_chain,   # required: the last positional arg is the else branch
)
```

A `RunnableBranch` without a default raises at construction. For anything beyond two or three static predicates, a plain function that RETURNS a runnable is easier to read and still streams:

```python
def pick(x):
    return sql_chain if x["route"] == "sql" else default_chain
chain = pick_route_prompt | model | StrOutputParser() | RunnableLambda(lambda x: pick({"route": x}))
```

Returning a Runnable from a lambda is supported: LangChain invokes it with the same input.

## Configurable Chains

Instead of building three chains that differ by one field:

```python
from langchain_core.runnables import ConfigurableField
model = ChatOpenAI(temperature=0).configurable_fields(
    temperature=ConfigurableField(id="temperature")
)
chain.invoke(x, config={"configurable": {"temperature": 0.7}})
```

`configurable_alternatives` swaps whole components (model A vs model B) behind one id. This is the clean way to A/B a model without duplicating chain code — and the alternative id shows up in traces.

## Inspecting A Chain Before Blaming It

```python
chain.get_graph().print_ascii()          # actual wiring, including coerced nodes
chain.input_schema.model_json_schema()   # what it accepts — settles KeyError arguments
chain.output_schema.model_json_schema()
chain.get_prompts()                      # every prompt template inside, after composition
```

`print_ascii()` needs `grandalf` installed. The shape it prints is the shape that runs — if a step you expected is missing, you built a dict instead of a chain somewhere.

## Sync, Async, and Batch

- `.batch(inputs, config={"max_concurrency": 5})` runs sync inputs in a thread pool; `.abatch` uses the event loop. Without `max_concurrency` you will find the provider's rate limit.
- `return_exceptions=True` on `batch`/`abatch` returns exceptions in place instead of failing the whole batch — mandatory for bulk jobs, then filter and retry the failures.
- A sync-only `RunnableLambda` inside an async chain is run in a thread; correct but it burns a worker per call. Give lambdas an async twin: `RunnableLambda(sync_fn, afunc=async_fn)`.
- Do not call `asyncio.run()` inside a runnable that may already run in a loop — that is the `this event loop is already running` error in notebooks and FastAPI.

## When Not To Use LCEL

Deeply conditional logic, retries with bespoke state, or loops read worse as a chain than as Python. The moment you find yourself writing three nested `RunnableBranch`es, the shape you want is a graph or an ordinary function that calls two small chains.
