# Recipe — RAG with Embeddings

## Goal

Answer a question grounded in a document set using embeddings + a cheap chat model.

## When

Knowledge-base Q&A, semantic search, grounding answers in your own data.

## Inputs

- A set of source documents.
- A user query.
- Embedding model `text-embedding-3-small` (1536 dims).

## Steps

1. **Chunk** documents (~200–800 tokens each).
2. **Embed chunks in batches** (array `input`) with `openai_embeddings`.
3. **Store** each vector with its source text. Never mix models/dims in one index.
4. **Embed the query** with the same model.
5. **Score** by cosine similarity; take top-k.
6. **Generate** the answer with `openai_chat`, passing top-k chunks as context.
7. Report `usage` from both the embedding and chat calls.

## Output

A grounded answer string + token usage.

## Example

Index (batched):

```json
{
  "tool": "openai_embeddings",
  "arguments": {
    "model": "text-embedding-3-small",
    "input": ["Refunds are processed in 5 business days.", "Support hours are 9am-5pm ET."]
  }
}
```

Query:

```json
{ "tool": "openai_embeddings", "arguments": { "model": "text-embedding-3-small", "input": "How long do refunds take?" } }
```

Cosine similarity:

```
cos(q, d) = dot(q, d) / (||q|| * ||d||)
```

Top chunk → "Refunds are processed in 5 business days." Then:

```json
{
  "tool": "openai_chat",
  "arguments": {
    "model": "gpt-4o-mini",
    "messages": [
      { "role": "system", "content": "Answer only from the context." },
      { "role": "user", "content": "Context: Refunds are processed in 5 business days.\n\nQuestion: How long do refunds take?" }
    ],
    "max_tokens": 40
  }
}
```

## Edge cases

- Query matches nothing well (low top score) → say you don't know rather than hallucinate.
- Index grew → re-embed only **new/changed** chunks.
- Need higher recall → try `text-embedding-3-large` (3072) but re-index fully.

## Production notes

- **Cost:** embedding cost scales with total tokens. **Batch** inputs, **cache** vectors, re-embed only changes.
- Use `dimensions` to shrink vectors if your store benefits.
- Keep retrieval k small to limit chat prompt size (and cost).

> Verification needed: confirm dimensions/pricing with <https://platform.openai.com/docs/api-reference>.
