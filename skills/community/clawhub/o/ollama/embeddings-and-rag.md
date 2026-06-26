# Embeddings and RAG

## Embedding Model Discipline

Use a dedicated embedding model for indexing and querying unless you are intentionally migrating the whole vector store.
If the embedding model changes, re-index the corpus instead of mixing vectors from different spaces.

## Native Embedding Check

```bash
curl -s http://127.0.0.1:11434/api/embed -d '{
  "model": "embeddinggemma",
  "input": "hello world"
}' | jq '.embeddings[0] | length'
```

Record the vector length and keep it consistent with the target database schema.

## Retrieval Workflow

For local RAG, validate the whole loop:
1. chunk documents to fit the retrieval task, not the maximum context
2. embed with one exact model tag
3. inspect top-k retrieved chunks for a known query
4. only then tune prompt structure or answer formatting

## Common Failure Patterns

- index with one embedding model and query with another -> weak retrieval without explicit errors
- chunks too large -> retrieval looks relevant but misses the exact fact
- chunks too small -> context loses coherence and answer quality drops
- jumping to a bigger chat model first -> cost and latency rise while retrieval remains broken

## Privacy Boundary

Local RAG is only local if ingestion, embedding, storage, and inference all stay on approved local systems.
If any leg uses a hosted vector database or cloud inference, state that boundary clearly.
