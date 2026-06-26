# Continuation Checklist

Use this checklist before writing any continuation or resume chapter.

## Required confirmations
- [ ] New project, continuation, or truncated resume?
- [ ] Have candidate projects been discovered and shown to the user?
- [ ] If multiple projects exist, has the user chosen one?
- [ ] Multi-agent role mapping provided when multi-agent is selected?
- [ ] If multi-agent is selected, has the correct agent/role been invoked for the current stage?
- [ ] If multi-agent is selected, has the designated agent/role been invoked for every stage in this turn?
- [ ] Is the main session drafting prose? (must be no in multi-agent mode)
- [ ] Which chapter/scene checkpoint is current?
- [ ] Is project.json present and valid?
- [ ] Is state/current.json present or writable?
- [ ] Are outline / batch-outline / memory / recent chapter summaries available?

## Resume flow
1. Read project.json.
2. Read the smallest relevant canon slice.
3. Verify checkpoint matches the request.
4. Confirm batch-outline availability or mark it stale if the full outline changed.
5. Summarize what is known / uncertain.
6. Draft only after confirmation.
6. For multi-agent stage execution, provide the stage’s minimal input packet and wait for the designated agent output before advancing.

## Stop conditions
- Missing checkpoint
- Missing role mapping
- Missing or malformed project state
- Contradicted resume metadata
- Multi-agent execution has not been confirmed
