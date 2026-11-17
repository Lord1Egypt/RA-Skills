# Migration — Version Boundaries And Moved Imports

Most LangChain code found online is written against a version that no longer exists. Identify which era the code belongs to before debugging it.

Version-specific claims below verified 2026-07. Check what is actually installed first:

```bash
pip list | grep -E "langchain|langgraph"     # every package and its version
python -c "import langchain; print(langchain.__version__)"
```

## The Four Eras

| Era | Marker in the code | What to know |
|---|---|---|
| Pre-0.1 | `from langchain.llms import OpenAI`, `LLMChain`, `initialize_agent` | Everything in one package; no partner packages |
| 0.1–0.2 | `langchain_core`, `langchain_openai`, LCEL everywhere | The package split; LCEL replaced `LLMChain` |
| 0.3 (Sept 2024) | pydantic v2 required | v1 models raise inside library code |
| 1.0 (GA 22 Oct 2025) | `langchain.agents.create_agent`, `langchain-classic` | Slim core surface; legacy moved out; Python 3.10+ |

LangChain 1.0 committed to no breaking changes before 2.0, so the 1.x line is a stable target. 1.1 added model profiles (`model.profile`, capability metadata used by middleware) and expanded middleware; it did not move imports again.

## Where Things Went In 1.0

| Old import | Now |
|---|---|
| `from langchain.chains import ...` | `from langchain_classic.chains import ...` (`pip install langchain-classic`) |
| `from langchain.retrievers import ...` | `langchain_classic.retrievers` (multi-query, self-query, compression, ensemble) |
| `from langchain import hub` | `from langchain_classic import hub` |
| Record-manager indexing API | `langchain-classic` |
| `langgraph.prebuilt.create_react_agent` | `langchain.agents.create_agent` |
| `AgentExecutor`, `initialize_agent` | `create_agent` |
| `ConversationBufferMemory` and the other memory classes | Checkpointers (SKILL.md Core Rule 6) |
| `RunnableWithMessageHistory` | Checkpointers; deprecated since 0.3, still importable |
| `langchain.llms` / `langchain.chat_models.ChatOpenAI` | Partner packages: `langchain_openai`, `langchain_anthropic`, … or `init_chat_model` |
| `langchain.embeddings` | Partner packages, or `init_embeddings` |
| Community integrations | `langchain-community`, installed separately |

The slim `langchain` package now holds `agents`, `messages`, `tools`, `chat_models`, `embeddings`.

`langchain-classic` exists so a large codebase can upgrade without rewriting everything at once: install it, rewrite the imports, ship, then migrate the actual patterns one by one. It is not a place to build new code.

## Migration Order That Minimizes Breakage

1. **Pin and freeze.** Record the working versions before touching anything; you need a known-good state to diff against.
2. **Imports only.** Add `langchain-classic`, rewrite import paths, run the test suite. No behavior change yet — this is the commit that must stay green.
3. **Agents.** `AgentExecutor` / `create_react_agent` → `create_agent`. Output shape changes from `{"output": str}` to a message list: read `result["messages"][-1].content`.
4. **Memory.** Memory objects → a checkpointer plus `thread_id`. This is the step with real semantic change: decide per fact whether it belongs in thread state or a cross-thread store.
5. **Chains.** Legacy chains (`RetrievalQA`, `ConversationalRetrievalChain`, `LLMChain`) → explicit LCEL. `LLMChain(llm, prompt)` becomes `prompt | model | StrOutputParser()`; `RetrievalQA` becomes an explicit retriever → prompt → model chain. You gain streaming and traces you did not have.
6. **Parsers.** Prompt-side parsers → `with_structured_output` where the provider supports it.
7. **Re-run the eval set.** Import-level success is not behavioral success — prompt formatting inside legacy chains differed subtly from what you write by hand.

`langchain-cli migrate` mechanizes most of step 2 for the older 0.2/0.3 hops. Review its diff; it rewrites imports, not semantics.

## Pydantic v1 → v2

- 0.3+ requires pydantic v2. Symptom of a leftover v1 model: `ValidationError` or a "model not fully defined" error raised from inside library code, not from your call.
- Mixing is the trap — a v1 `BaseModel` from a third-party library passed as an `args_schema` or to `with_structured_output` fails even though your own models are v2.
- Field metadata syntax changed (`Field(..., description=)` still works; validators and config did not). A schema that stops reaching the model is usually a validator that silently no longer runs.

## Reading Old Tutorials Safely

- `LLMChain`, `initialize_agent`, `ConversationChain`, `SequentialChain`, `AgentType.` → pre-LCEL, at least two eras old. Read for intent, rewrite the code.
- `from langchain.chat_models import ChatOpenAI` → pre-split.
- `RunnableWithMessageHistory` → 0.2/0.3-era memory; use a checkpointer.
- `create_react_agent` from `langgraph.prebuilt` → 0.3-era agent; use `create_agent`.
- Anything with no import block at all → unusable; the imports are the version fingerprint.
