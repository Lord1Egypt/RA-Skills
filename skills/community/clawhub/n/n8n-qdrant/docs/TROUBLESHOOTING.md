# Troubleshooting & Best Practices

## Common Errors and Fixes

### "Collection not found"
- Run the collection setup workflow first
- Check collection name spelling (case-sensitive)
- Verify Qdrant credentials point to correct instance

### "Vector dimension mismatch"
- You're using a different embedding model than the collection was created with
- Fix: delete and recreate collection, or use `Update Collection` to change vector config
- Prevention: always store embedding model name in a workflow variable/env

### "Request timeout" on large batches
- Reduce `batchSize` in Split In Batches (try 10 or 5)
- Increase `Wait` node duration
- Check Qdrant Cloud plan limits

### "Embedding model not found" (OpenAI)
- Model name changed — use `text-embedding-3-large` not `text-embedding-ada-002`
- Check OpenAI API key has access

### Retrieved results are irrelevant
- Check you're using the same embedding model at ingest AND retrieval
- Check score threshold — too low allows noise
- Check collection has expected number of vectors (use Get Collection)
- Try increasing topK and see if better results appear further down

### Information Extractor returns empty fields
- Input text too short — needs at least a few sentences for good extraction
- LLM temperature should be 0 for extraction tasks
- Check LLM node is properly connected via `ai_languageModel` port

### Loop not terminating
- Split In Batches "done" output wasn't connected
- Wait node not connected back to Split In Batches input
- Check connections on both outputs of Split In Batches node

---

## Performance Optimization

### Large Dataset Ingestion (100k+ records)
1. Use `Batch Update Points` (Official Qdrant Node) instead of individual upserts — batches of 100 points per call
2. Pre-compute all embeddings via OpenAI Batch API (50% cost reduction, async)
3. Increase `batchSize` in Split In Batches to 50–100 when using Batch Update Points
4. Use n8n's queue mode for memory-intensive workflows

### Retrieval Latency
1. Ensure payload indexes exist on all filtered fields
2. Set `hnsw_ef` at query time for speed/accuracy tradeoff: lower = faster but less accurate
3. Use `Query Points Groups` when you expect many chunks from same document
4. Enable `on_disk: true` for large collections to reduce memory pressure

### Cost Optimization
1. Use `text-embedding-3-small` instead of large (1536d vs 3072d, ~5x cheaper) — quality difference is small for most use cases
2. Filter content before embedding (remove short/empty records)
3. Deduplication check before re-ingesting already-indexed records
4. Use OpenAI Batch API for large one-time ingestion jobs

---

## Workflow Design Best Practices

### Error Resilience
```
Always set on the Qdrant Vector Store node:
  onError: "continueRegularOutput"
  retryOnFail: true
  maxTries: 3
  waitBetweenTries: 1000 (ms)
```

### Idempotency
Design ingestion workflows to be safe to re-run:
1. Check if `doc_id` already exists before ingesting
2. If exists, delete old vectors then re-ingest (for update workflows)
3. Use deterministic IDs (never random UUIDs) based on source record IDs

### Observability
Log ingestion progress to a tracking sheet:
```
[After each batch]
    → [Google Sheets: append row]
         - timestamp
         - batch_number  
         - records_processed
         - collection_name
         - status (success/error)
```

### Testing
Always test with a small dataset first:
1. Set `batchSize: 1` and `returnAll: false` with `limit: 3` on source node
2. Verify payload in Qdrant Cloud UI or via Scroll Points
3. Test retrieval with known queries before scaling up

---

## Security Best Practices

1. **Never hardcode API keys** — use n8n credentials or `$env.YOUR_KEY`
2. **Scope Qdrant API keys** — use read-only keys for retrieval workflows
3. **Always confirm destructive operations** — use sendAndWait for deletions
4. **Audit log all deletions** — write to Google Sheets or Slack before executing
5. **Use separate collections per environment** — `prod-slack-messages` vs `dev-slack-messages`

---

## External References

- Qdrant Official n8n Node: https://github.com/qdrant/n8n-nodes-qdrant
- Qdrant n8n Platform Docs: https://qdrant.tech/documentation/platforms/n8n
- Qdrant n8n Tutorial: https://qdrant.tech/documentation/tutorials-build-essentials/qdrant-n8n/
- n8n Qdrant Vector Store Docs: https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.vectorstoreqdrant
- Qdrant API Reference: https://api.qdrant.tech/api-reference
- n8n Self-hosted AI Starter Kit: https://github.com/n8n-io/self-hosted-ai-starter-kit
- FastEmbed (sparse encoding): https://github.com/qdrant/fastembed
