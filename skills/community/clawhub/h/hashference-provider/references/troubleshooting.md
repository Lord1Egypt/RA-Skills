# Troubleshooting

| Symptom | Check and response |
| --- | --- |
| Only one model listed | Bootstrap provider may register one model. Fetch full catalog, generate and merge requested IDs, then refresh picker. Do not invent a requirement for a dashboard operator. |
| Alias visible, runtime unknown | Register exact ID under models.providers.PROVIDER.models; aliases/params alone are insufficient. Check target agent and runtime/plugin. |
| Model string rejected | OpenClaw uses local provider/model; HTTP body uses bare catalog ID. Local provider may be quai or another name. |
| 401/403 | Verify SecretRef resolution, Gateway env, revocation and intended account without revealing values. No repeated key creation or silent account changes. |
| 402 | Check required/available/shortfall and eligible credit. Large output reservation may exceed balance; lower cap if appropriate or let user choose funding. Never buy automatically. |
| 404 | Refresh live exact ID, endpoint and baseUrl. No duplicate /v1; no silent checkpoint substitution. |
| 400 | Inspect tool_choice_modes, effort/thinking, caching, structured-output and image support for exact route. Identify mismatch before dropping fields. |
| 429/5xx | Honor Retry-After and bounded backoff; no tight retries or many paid tests. |
| Context/output limit | Distinguish total window, input ceiling and output cap; include tools/system text, compact/lower budgets. Server clamping does not prove correct client config. |
| No early tokens | Check buffered streaming and request/runtime timeouts; no invented latency guarantee. |
| Chat retains old model | Check agent/session override and supported /model default; verify /status rather than model self-identification. |
| Valid config, no inference | Verify runtime availability and authorized exact-route proof. Text success is not tool-loop proof. |
| Conflicting price/privacy docs | Prefer current catalog/capability records; identify timestamp and uncertainty. |

Preserve config/secrets for repairs. Do not run mutating doctor fixes, replace files, install plugins, restart Gateway or widen policies without authorization and supported tools. Report real blockers and exact supported next steps.
