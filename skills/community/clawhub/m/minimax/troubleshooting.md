# Troubleshooting - MiniMax

Use this file when MiniMax calls are failing, stalling, or behaving inconsistently.

## Fast Triage

Check these in order:
1. auth
2. interface choice
3. model name
4. payload shape
5. queue state
6. output fetch

## Common Failure Patterns

### 401 or auth failure
- confirm `MINIMAX_API_KEY` is present in the active environment
- check whether the request is hitting the intended MiniMax endpoint
- verify the key belongs to the account or workspace expected by the user

### Text call succeeds but behavior is wrong
- confirm the integration is using the intended interface: native, Anthropic-compatible, or OpenAI-compatible
- check whether a parameter is ignored by the compatibility layer
- shrink the request to the minimum payload that still reproduces the problem

### Speech output is slow or wrong
- verify whether HD versus turbo was chosen intentionally
- check whether the script should be chunked instead of synthesized in one pass
- confirm the selected endpoint and output format match the user goal

### Video or music jobs appear stuck
- separate submit success from poll success
- inspect whether the job is queued, failed, or completed with a bad fetch step
- stop blind reruns until the first job state is understood

### Results are inconsistent across retries
- pin the model and interface exactly
- keep the successful payload as a baseline
- change one variable at a time: prompt, asset, duration, or output settings

## Recovery Rule

When in doubt, return to the smallest reproducible request on the native MiniMax API, confirm it works, and only then reintroduce compatible SDKs, media assets, or orchestration layers.
