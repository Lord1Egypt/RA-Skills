# Server Workflows — LM Studio

Use these workflows to prove the local runtime is actually ready before touching app code.

## 1. Quick Reachability Check

Start with the OpenAI-compatible model listing endpoint:

```bash
curl -fsS http://localhost:1234/v1/models | jq .
```

Interpretation:
- Success with model data -> the server is reachable.
- Connection refused or timeout -> the local server is not listening on that port.
- Empty or unexpected response -> check whether the local server is enabled and whether the port changed.

## 2. CLI-First Server Control

If `lms` is available, use it for repeatable checks:

```bash
lms server start
lms server stop
```

When the server is running, keep the CLI and HTTP checks separate:
- CLI proves the LM Studio side started.
- `curl` proves the client path and port are correct.

## 3. Inventory vs Runtime State

Use these commands in order:

```bash
lms ls
lms ps
curl -fsS http://localhost:1234/v1/models | jq '.data[].id'
```

Read them differently:
- `lms ls` -> what exists locally on disk.
- `lms ps` -> what is currently loaded.
- `/v1/models` -> what the local server advertises to clients.

Do not collapse those into one concept.

## 4. Minimal Smoke Test

After the port responds, prove inference works:

```bash
curl -fsS http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "REPLACE_WITH_LOCAL_MODEL_ID",
    "messages": [
      {"role": "user", "content": "Reply with the word READY."}
    ],
    "temperature": 0
  }' | jq -r '.choices[0].message.content'
```

Only move on after the model returns content.

## 5. If the App Is Open but Requests Fail

Check these in order:
1. Wrong port.
2. Local server not enabled.
3. Model not loaded yet.
4. Machine slept and the local runtime lost readiness.
5. Client is pointing at the wrong base URL.

## 6. Headless and No-GUI Mode

LM Studio also supports headless operation through `llmster`.

Use that path when:
- The machine has no desktop session.
- You want a server or CI-friendly runtime.
- The GUI is not part of the workflow.

Keep the same verification sequence: start runtime, list models, run one smoke test.
