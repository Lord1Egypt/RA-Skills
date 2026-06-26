---
name: LangChain
description: Avoid common LangChain mistakes — LCEL gotchas, memory persistence, RAG chunking, and output parser traps.
metadata: {"clawdbot":{"emoji":"🦜","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

## LCEL Basics
- `|` pipes output to next — `prompt | llm | parser`
- `RunnablePassthrough()` forwards input unchanged — use in parallel branches
- `RunnableParallel` runs branches concurrently — `{"a": chain1, "b": chain2}`
- `.invoke()` for single, `.batch()` for multiple, `.stream()` for tokens
- Input must match expected keys — `{"question": x}` not just `x` if prompt expects `{question}`

## Memory Gotchas
- Memory doesn't auto-persist between sessions — save/load explicitly
- `ConversationBufferMemory` grows unbounded — use `ConversationSummaryMemory` for long chats
- Memory key must match prompt variable — `memory_key="chat_history"` needs `{chat_history}` in prompt
- `return_messages=True` for chat models — `False` returns string for completion models

## RAG Chunking
- Chunk size affects retrieval quality — too small loses context, too large dilutes relevance
- Chunk overlap prevents cutting mid-sentence — 10-20% overlap typical
- `RecursiveCharacterTextSplitter` preserves structure — splits on paragraphs, then sentences
- Embedding dimension must match vector store — mixing models causes silent failures

## Output Parsers
- `PydanticOutputParser` needs format instructions in prompt — call `.get_format_instructions()`
- Parser failures aren't always loud — malformed JSON may partially parse
- `OutputFixingParser` retries with LLM — wraps another parser, fixes errors
- `with_structured_output()` on chat models — cleaner than manual parsing for supported models

## Retrieval
- `similarity_search` returns documents — `.page_content` for text
- `k` parameter controls results count — more isn't always better, noise increases
- Metadata filtering before similarity — `filter={"source": "docs"}` in most vector stores
- `max_marginal_relevance_search` for diversity — avoids redundant similar chunks

## Agents
- Agents decide tool order dynamically — chains are fixed sequence
- Tool descriptions matter — agent uses them to decide when to call
- `handle_parsing_errors=True` — prevents crash on malformed agent output
- Max iterations prevents infinite loops — `max_iterations=10` default may be too low

## Common Mistakes
- Prompt template variables case-sensitive — `{Question}` ≠ `{question}`
- Chat models need message format — `ChatPromptTemplate`, not `PromptTemplate`
- Callbacks not propagating — pass `config={"callbacks": [...]}` through chain
- Rate limits crash silently sometimes — wrap in retry logic
- Token count exceeds context — use `trim_messages` or summarization for long histories
