# Integrate: LangChain / LangGraph

LangChain and LangGraph share one integration: `NoveumTraceCallbackHandler`. Once attached,
it automatically traces LLM calls, chains, agents, tools, retrieval, and LangGraph
nodes/routing — no per-call wrapping needed.

## 1. Install and initialize

```bash
pip install "noveum-trace[langchain]"
```

```python
import noveum_trace
noveum_trace.init(project="<NOVEUM_PROJECT>", environment="production")
# api key via env NOVEUM_API_KEY; set NOVEUM_SERVICE_VERSION to the release/commit
```

## 2. Attach the handler

Preferred — set it where the model/graph is constructed so every call inherits it:

```python
from noveum_trace.integrations.langchain import NoveumTraceCallbackHandler

handler = NoveumTraceCallbackHandler()

# LangChain
llm = ChatOpenAI(model="gpt-4o", callbacks=[handler])

# or per-invocation (works for chains, agents, and LangGraph graphs)
result = chain.invoke(inputs, config={"callbacks": [handler]})
graph_result = graph.invoke(state, config={"callbacks": [handler]})
```

LangGraph note: pass the handler in the `config` of the top-level `invoke`/`astream` —
it propagates to every node, tool call, and LLM call in the run.

## 3. Coverage check (do not skip)

The handler only sees calls that flow through LangChain. Grep for direct SDK usage that
bypasses it (`openai.`, `client.chat.completions`, `anthropic.`) and wrap those per
`integrate-openai-manual.md` §2.

## 4. Lifecycle

Same as every integration: background batching means short-lived processes must flush.

```python
import atexit
atexit.register(noveum_trace.shutdown)
```

Async apps: the handler is async-aware; no special handling needed beyond shutdown.

## 5. What you get

Rich attributes per span: `llm.model`, token usage, `chain.*`, `agent.*`, `tool.*`,
`retrieval.*`, full message inputs/outputs where available. This feeds the conversational,
agent, and RAG scorer families directly.

Proceed to `verify-traces.md` for the acceptance check.
