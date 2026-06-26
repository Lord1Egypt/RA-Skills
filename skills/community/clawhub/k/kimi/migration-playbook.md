# Kimi Migration Playbook

Use this when existing OpenAI-compatible code needs the smallest possible change set.

## Migration Order

1. Replace the base URL with `https://api.moonshot.ai/v1`.
2. Replace the auth env var lookup with `MOONSHOT_API_KEY`.
3. Refresh model IDs from `/models` instead of copying old names.
4. Re-run one minimal request before touching prompts or business logic.
5. Re-validate parser assumptions, retries, and token limits.

## Minimal Diff Mindset

Keep the request shape as stable as possible:
- same message structure
- same downstream parser
- same observability hooks

Change one variable at a time and record the first working payload.

## Fast Failure Isolation

| Symptom | Most likely class | First fix |
|---------|-------------------|-----------|
| `401` | auth | re-export `MOONSHOT_API_KEY` and retry `/models` |
| `404` or model not found | stale model ID | refresh `/models` and copy exact live ID |
| parse breakage | output contract mismatch | add a strict normalization pass |
| timeout under big prompts | oversized payload | shrink context or split into batches |
| cost spike | route too large or too chatty | move to a smaller route and cap retries |

## Evidence to Save

For recurring migrations, keep:
- first working curl example
- rejected model IDs
- parser quirks discovered during rollout
- approved redaction rules for sensitive prompts

Do not save raw secrets, copied bearer tokens, or private production payloads.
