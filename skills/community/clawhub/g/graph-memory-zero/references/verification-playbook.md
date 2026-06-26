# Verification playbook

Run this after every patch/restart before claiming optimization success.

## A. Config integrity checks

1. `plugins.entries.graph-memory.enabled` is true.
2. `plugins.slots.contextEngine` points to `graph-memory`.
3. `recallPolicy` contains expected keys:
   - threshold / infer / filters.memoryType / preferenceLexicon.version
4. If `minScore` exists, compute and report effective threshold (`max`).

## B. Observability checks

Run `gm_search` with a representative query and verify debug payload includes:
- effective threshold
- infer on/off
- applied filters summary

If debug fields are missing, treat as partial validation.

## C. Query test set (minimum 6)

Use at least these query classes:

1. **Preference query (CN)**
   - e.g., “Jerry 的默认回复风格偏好是什么？”
2. **Preference query (EN)**
   - e.g., “What are Jerry's preferred collaboration defaults?”
3. **Task memory query**
   - e.g., “之前 graph-memory 是怎么配置上线的？”
4. **Event troubleshooting query**
   - e.g., “powershell 脚本失败时怎么排查？”
5. **Mixed intent query**
   - e.g., “给我一个兼顾准确率和召回率的 recallPolicy 建议”
6. **Negative/noise query**
   - intentionally unrelated text to check false positives

## D. Acceptance criteria

Mark as PASS only if all conditions hold:

- Top results are relevant for preference/task/event classes.
- No significant increase in off-topic hits.
- CN/EN preference retrieval both remain usable.
- The intended profile (balanced/precision/recall) matches observed behavior.

## E. Result report template

- Config integrity: PASS/FAIL (+ reason)
- Observability: PASS/FAIL (+ missing fields)
- Query set: X/6 pass
- Decision: keep profile / tune / rollback
