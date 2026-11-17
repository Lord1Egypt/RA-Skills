# Error Handling

All error responses follow this shape:

```json
{
  "status": "error",
  "code": "API_KEY_EXPIRED",
  "error": "Human-readable message",
  "nextStep": "What to do next"
}
```

**Follow `nextStep`.** It is written for agents. Never start a sign-in unless the code is
`API_KEY_INVALID` or `API_KEY_EXPIRED`.

## Authentication and sign-in

| Status | Code | Do this |
|---|---|---|
| 401 | `API_KEY_MISSING` | Send the saved key (`scripts/litehost.sh api …`). Do not sign in. |
| 401 | `API_KEY_INVALID` | `scripts/litehost.sh forget`, then sign in once or ask for a dashboard key. |
| 401 | `API_KEY_EXPIRED` | Unused for 90 days. `scripts/litehost.sh forget`, then sign in once. |
| 401 | `OTP_INVALID` | User mistyped the code. Ask them to re-check. **Do not request a new code.** |
| 401 | `OTP_EXPIRED` | No open code. Request a new one, once. |
| 429 | `OTP_TOO_MANY_ATTEMPTS` | 5 wrong codes. Request a new one, once. |
| 429 | `RATE_LIMITED` | Wait `retryAfterSeconds` (also in `Retry-After`). If a code was already sent, verify it instead. |
| — | `NETWORK_BLOCKED` (helper only) | This environment cannot reach connect.litehost.io. Follow Step 0 in `SKILL.md`: stop, point the user to the Litehost connector. Do not sign in. |
| — | `NO_SAVED_KEY` (helper only) | No key saved. Publish with `actions/temp-project.md`, or sign in once if the user wants you to manage projects. |

## Error Reference

| Status | Code | Meaning | Required Action |
|---|---|---|---|
| 400 | `ZIP_MULTIPLE_HTML` | ZIP contains multiple HTML files and no `zipIndexHtmlPath` was provided. | Read the `htmlPaths` array from the response. Present the paths to the user. Ask which is the homepage. Retry with `zipIndexHtmlPath` set to their choice. |
| 401 | `API_KEY_*`, `OTP_*` | See the table above. | Follow `utils/auth.md`. |
| 403 | `FEATURE_LOCKED` | This feature (e.g. link opens) needs a paid plan. The key is fine. | Same as `FREE_TIER_RESTRICTED`. |
| 403 | `FREE_TIER_RESTRICTED` | Endpoint requires a paid plan (starter or higher). The key is fine. | Tell the user: "This needs a paid plan ({requiredTier} or higher): https://litehost.io/dashboard?upgrade=plans". DO NOT retry and DO NOT sign in again. |
| 403 | `PROJECT_LIMIT_REACHED` | Active project count equals the plan limit. | Follow `utils/quotas.md`. |
| 403 | `STORAGE_LIMIT_REACHED` | Total storage of active projects equals the plan limit. | Follow `utils/quotas.md`. |
| 404 | — | Resource not found. | Verify the ID with the user. If unknown, list the resource type (projects, domains, workspaces) and let them pick. |
| 409 | — | Slug conflict — another project already uses that slug. | Ask the user for a different slug and retry. |
| 409 | `ALREADY_CLAIMED` | Temp project was already claimed. | The project is already in the user's account. No action needed — inform the user. |
| 422 | — | Request body validation failed. | Check field types and constraints against the action file, fix the request, and retry. |
| 429 | `RATE_LIMITED` | Rate limit exceeded. | Wait `retryAfterSeconds` (or the `Retry-After` header) and retry. Tell the user about the wait. |

## Free-Tier Restricted Endpoints

These endpoints return `403 FREE_TIER_RESTRICTED` for free-plan users:
- PUT `/v1/projects/{id}` (push new version)
- PATCH `/v1/projects/{id}` (update settings)
- GET `/v1/projects/{id}/status` (deployment history)
- GET `/v1/projects/{id}/analytics` (link opens)
- POST `/v1/projects/{id}/archive`
- POST `/v1/projects/{id}/unarchive`
- GET `/v1/domains`, GET `/v1/domains/{id}`
- GET/POST/PATCH/DELETE `/v1/workspaces`

When hitting this error, check `data.plan.tier` from `GET /v1/user`. If the user is on `free`, they must upgrade before using these endpoints.

## Rules

- NEVER silently swallow errors. Always inform the user what went wrong and why.
- NEVER retry the same request without changing something (different parameter, resolved auth, etc.).
- When a 403 limit error occurs, NEVER just tell the user to upgrade. Follow the full quota flow in `utils/quotas.md` first.
- When a 403 `FREE_TIER_RESTRICTED` error occurs, DO tell the user to upgrade — there is no workaround.
