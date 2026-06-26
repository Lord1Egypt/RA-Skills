# Recipe — Build Embeddings for RAG

## Goal

Turn a corpus of text into embedding vectors for semantic search / retrieval-augmented generation.

## When

You need similarity search, clustering, deduplication, or a RAG retrieval step.

## Inputs

- A list of document texts (chunks).
- An embedding model id (default `sentence-transformers/all-MiniLM-L6-v2`).

## Steps

1. **Pick and pin the model.** Use the default or confirm another feature-extraction model with `hf_model_info` (`pipeline_tag: feature-extraction`). Pin its id.
2. **Index (billed, batch).** Call `hf_embeddings` with an **array** of document chunks. Store each vector with its source text/metadata in a vector store.
3. **Query (billed).** Embed the user question with the **same** model.
4. **Retrieve.** Compute cosine similarity between the query vector and stored vectors; take top-k.
5. **Answer.** Pass the top-k documents as context to `hf_chat`.

## Output

A vector index and, at query time, a grounded answer plus its sources.

## Example

```json
{
  "tool": "hf_embeddings",
  "arguments": {
    "inputs": [
      "Paris is the capital of France.",
      "The Eiffel Tower is in Paris.",
      "Berlin is the capital of Germany."
    ]
  }
}
```

```json
[[0.012, -0.045, "..."], [0.021, -0.033, "..."], [0.050, 0.010, "..."]]
```

Query:

```json
{ "tool": "hf_embeddings", "arguments": { "inputs": "Where is the Eiffel Tower?" } }
```

Then retrieve the nearest stored vector (the Eiffel Tower chunk) and feed it to `hf_chat`.

## Edge cases

- **Mismatched models**: indexing and querying with different models breaks similarity → use one model.
- **Wrong model type**: a non-feature-extraction model yields `model_not_supported` → switch to one with `pipeline_tag: feature-extraction`.
- **Large corpora**: chunk and batch; cache vectors to avoid re-embedding.

## Production notes

- Embeddings are **billed** — batch inputs and cache aggressively.
- Re-embed only changed documents.
- Pin the embedding model id (and revision) so the index stays consistent.
