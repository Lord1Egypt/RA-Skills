# Retrieval — Loaders, Splitters, Indexing, Retrievers

Scope: wiring retrieval correctly in LangChain. Strategy (what to chunk, how to evaluate) is `rag` and `rag-chunking`.

## The Pipeline And Where It Breaks

`load → split → embed → store → retrieve → format into the prompt`

Diagnose in that order. Bad answers blamed on the model are usually a splitter that produced 40-character chunks, or a retriever returning `k=4` when the answer spans six chunks.

## Loading

- Every loader returns `Document(page_content, metadata)`. Metadata is your only handle for filtering and citations later — add `source`, and for PDFs the page, at load time. Retrofitting metadata means re-indexing.
- `DirectoryLoader(..., silent_errors=True)` skips unreadable files without telling you; the corpus is then quietly incomplete. Log the skipped count and compare against the file count.
- PDF loaders differ in what they even see: text-layer extraction returns nothing for scanned pages (you need OCR), and multi-column layouts interleave columns. Print one page of extracted text before indexing a thousand.
- `.lazy_load()` for large corpora — `.load()` materializes every Document in memory first.

## Splitting

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=150, add_start_index=True
)
```

- Defaults are `chunk_size=4000, chunk_overlap=200` — far larger than most tutorials imply. Always set them explicitly.
- `chunk_size` counts **characters** by default. To count tokens, build with `.from_tiktoken_encoder(...)` or pass a `length_function`. A 1,000-character chunk is roughly 250 English tokens; mixing the two units is how "chunks fit the context" turns out false.
- Overlap ≤ 20% of chunk size. Larger overlap inflates index size and duplicates hits without adding recall; overlap ≥ chunk size makes no forward progress.
- `RecursiveCharacterTextSplitter` tries `["\n\n", "\n", " ", ""]` in order, so it breaks at paragraph boundaries when it can. Structured formats have dedicated splitters (Markdown header, HTML section, language-aware code splitters) — using the generic splitter on code cuts functions in half.
- `add_start_index=True` records the character offset in metadata, which is what lets an answer cite a location in the original document.

## Indexing Without Duplicates

Re-running ingestion with `add_documents` inserts a second copy of everything: retrieval then returns the same passage three times and `k` is wasted.

Two fixes, in order of preference:

1. Deterministic ids: `ids=[sha256(doc.page_content + source)]` passed to `add_documents` — upsert semantics on most stores.
2. The record-manager indexing API (`langchain-classic` in 1.x): tracks hashes per source and supports cleanup modes — `None` (no delete), `incremental` (delete old versions of the sources you just re-ingested), `full` (delete anything absent from this run). `incremental` is the default choice for a corpus that changes file by file.

Either way, deletion is the hard half: a document removed from the source corpus stays in the index forever unless something reconciles.

## Retrievers

```python
retriever = store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 20, "lambda_mult": 0.5, "filter": {"source": "docs"}},
)
```

| Setting | Default | Effect |
|---|---|---|
| `k` | 4 | Chunks returned. Too low truncates multi-part answers; too high dilutes the prompt with near-misses |
| `search_type="mmr"` | `"similarity"` | Maximal marginal relevance: diversity over redundancy, useful when the top hits are near-duplicates |
| `fetch_k` | 20 | Candidates MMR re-ranks down to `k` |
| `lambda_mult` | 0.5 | 1.0 = pure relevance, 0.0 = pure diversity |
| `search_type="similarity_score_threshold"` | — | Required for `score_threshold` to have any effect; with plain `similarity` the key is ignored |
| `filter` | none | Metadata pre-filter; syntax is store-specific and an unsupported operator is often ignored rather than rejected |

- Metadata filtering happens in the store, before or during the vector search depending on the engine — a highly selective filter on a store that post-filters can return fewer than `k` results with no error.
- Multi-query, self-query, contextual-compression, and ensemble (BM25 + vector) retrievers live in `langchain-classic` or `langchain-community` in 1.x. Hybrid keyword+vector is the highest-value upgrade for corpora full of identifiers, error codes, and part numbers, which embeddings represent poorly.

## Retriever As A Chain Step vs As A Tool

- **Chain step**: retrieval always happens, once, with the user's raw question. Predictable cost and latency; wrong for questions that need no retrieval, and it cannot reformulate a bad query.
- **Tool** (`create_retriever_tool`, or any `@tool` that wraps the retriever): the model decides whether and how many times to search, and can rewrite the query after a poor result. Costs a loop, and the description must say exactly what the corpus contains or the model will search for things that are not in it.
- Default to the chain step for a Q&A endpoint over one corpus; use the tool form when the agent has several corpora or genuinely mixed tasks (SKILL.md Choosing The Abstraction).

## Scores Are Not Comparable Across Stores

`similarity_search_with_score` returns whatever the engine natively produces:

- Chroma and FAISS (L2): **distance** — lower is better, unbounded above.
- Cosine-similarity stores: higher is better, roughly −1…1.
- `similarity_search_with_relevance_scores` normalizes to 0…1 where higher is better, when the store implements it.

A threshold copied from another project therefore inverts silently. Print ten scores for known-good and known-bad queries before setting any cutoff, and re-check after changing the embedding model.

## Formatting Documents Into The Prompt

```python
def format_docs(docs):
    return "\n\n".join(f"[{i+1}] {d.metadata.get('source','?')}\n{d.page_content}" for i, d in enumerate(docs))
```

- Number the chunks and instruct the model to cite by number — citations you can verify beat a trailing source list nobody checks.
- Keep the retrieved text inside a clearly delimited block and put the instruction "answer only from the context; say you do not know otherwise" after it.
- Watch total size: `k=8` at 1,000-character chunks is ~2,000 tokens of context per request, before history (SKILL.md cost formula).

## Debugging Retrieval Quality Fast

1. Query the store directly with the user's exact words: `store.similarity_search(q, k=10)`. If the right chunk is not in the top 10, the problem is upstream of the prompt.
2. Read the chunk that SHOULD have matched. Nine times out of ten it is malformed — half a table, a page header, or a chunk that lost the section title that made it findable.
3. Try the query rewritten as the document phrases it. A large gap means query-document mismatch: add a rewriting step or an instruction-tuned embedding model.
4. Check the filter: an unmatched metadata value returns an empty list, which reaches the model as "no context" and produces a confident hallucination unless the prompt guards it.
5. Only then tune `k`, chunk size, or the model.
