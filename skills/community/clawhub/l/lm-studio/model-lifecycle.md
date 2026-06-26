# Model Lifecycle — LM Studio

This is the operating model: discover, load, verify, use, unload.

## 1. Discover What Exists

If `lms` is available:

```bash
lms ls
```

If the local server is reachable:

```bash
curl -fsS http://localhost:1234/v1/models | jq '.data[].id'
```

Important:
- Disk inventory is not runtime readiness.
- The server list can include models visible for Just-In-Time loading.
- A model name in the UI is not automatically the identifier you should hardcode into app code.

## 2. Load a Model Intentionally

Use explicit load commands when you want deterministic control:

```bash
lms load openai/gpt-oss-20b --identifier="local-chat"
```

Useful options from the CLI docs:

```bash
lms load [--gpu=max|auto|0.0-1.0] [--context-length=1-N]
```

Use cases:
- `--gpu=max` when the machine should use as much GPU offload as possible.
- `--gpu=auto` when you want the runtime to choose.
- `--context-length` when long contexts are pushing the machine too hard.

## 3. Verify the Loaded Runtime

After loading, verify with both the CLI and the API:

```bash
lms ps
curl -fsS http://localhost:1234/v1/models | jq '.data'
```

Then run one inference smoke test before declaring the model ready.

## 4. Match Workload to Model Reality

Use this progression instead of jumping to the largest model:

- Extraction, classification, summarization -> start small and fast.
- Day-to-day chat or agent loops -> use the smallest model that stays coherent on the real task.
- Coding or structured output -> verify with task-specific smoke tests before rollout.
- Embeddings -> use a model that is intended for embedding requests, not a chat model by assumption.

If a model fails a basic workload, downgrade the ambition or switch models early.

## 5. Unload on Purpose

When debugging performance or freeing memory:

```bash
lms unload --all
```

Then confirm the machine is actually clear:

```bash
lms ps
```

Unload before comparing models. Otherwise leftover memory pressure corrupts the test.

## 6. Stable Identifier Strategy

If the user wants repeatable app wiring, give the loaded model a stable identifier.

Why:
- The downloaded model name can change across pulls.
- A stable identifier makes app config and smoke tests cleaner.
- Swapping the backing model later becomes safer.

## 7. What to Record After a Good Run

Store only facts that help future work:
- Model identifier that passed.
- Context length that stayed stable.
- Whether GPU offload helped or hurt.
- Which workloads the model passed or failed.
