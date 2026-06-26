# Troubleshooting — LM Studio

Use symptoms to narrow the fault before changing prompts or rewriting app code.

## Symptom -> Likely Cause -> Exact Check -> Better Move

| Symptom | Likely Cause | Exact Check | Better Move |
|---------|--------------|-------------|-------------|
| Connection refused | Wrong port or server not listening | `curl -fsS http://localhost:1234/v1/models` | Start the server, confirm port, then retry |
| `/v1/models` works but inference fails | Model not actually ready for the target workload | Run a minimal chat smoke test | Load a verified model and test again |
| `model not found` | Remote model name still hardcoded | Inspect request payload and compare with local ids | Replace with the LM Studio identifier |
| First token is extremely slow | Model too large, bad GPU fit, or cold load | Check `lms ps`, current model, and load settings | Reduce model size, GPU burden, or context |
| Output is repetitive or low quality | Weak model, wrong quantization, or overloaded context | Test a shorter prompt and smaller context window | Switch models before over-tuning prompts |
| JSON mode is unreliable | Model was never verified for structured output | Run one tiny JSON-only smoke test | Pick a known-good model for structure-heavy work |
| Embeddings call fails | Wrong model type or endpoint mismatch | Test `POST /v1/embeddings` directly | Use an embedding-capable model id |
| Everything gets worse after enabling MCP | Tool descriptions or tool path overwhelm the local model | Disable MCP and rerun the same prompt | Reduce MCP scope or use a stronger model |

## Fast Debug Order

1. Reachability.
2. Correct base URL.
3. Correct model identifier.
4. Loaded runtime state.
5. Workload capability of the chosen model.
6. MCP or tool pressure.

Do not skip the early steps. Most failures happen there.

## When to Stop Blaming the Prompt

Stop prompt-tuning and change the runtime when:
- The same failure happens on tiny prompts.
- Multiple endpoints fail for the same model.
- The machine clearly cannot hold the model and context comfortably.
- Another verified model succeeds immediately.

## When to Escalate Beyond LM Studio

Escalate when:
- The task is high-stakes and repeated local attempts still fail.
- The needed capability is unsupported in the local stack.
- The user values accuracy more than local-only execution for this task.

Say that explicitly instead of pretending the local path is still the best choice.
