# Troubleshooting: Common Graph API Errors

Explain errors to the user in their language, then suggest the fix.
Never include the client secret in any diagnostic output.

| Symptom | Likely cause | Fix |
|---|---|---|
| `401 InvalidAuthenticationToken` | Token expired or malformed | `graph.sh` refreshes once automatically; if persistent: `scripts/get_token.sh --force`, check tenant/client ID |
| `AADSTS7000215` (invalid client secret) | Secret wrong or expired | Create a new secret in the App Registration; secrets expire (default 6–24 months) |
| `403 Forbidden` on `/identity/conditionalAccess/...` | Missing `Policy.Read.All` / `Policy.ReadWrite.ConditionalAccess` | Add the application permission + grant admin consent |
| `403 Forbidden` on `/auditLogs/...` | Missing `AuditLog.Read.All` | Add permission + admin consent |
| `403` elsewhere | Permission missing or admin consent not granted | Compare against the permission table in README; re-grant consent after adding |
| `400 Request_UnsupportedQuery` on `/users` or `/groups` | Advanced query without `ConsistencyLevel: eventual` + `$count=true` | Use `graph.sh` (adds them automatically) |
| `400` "Invalid filter clause" with dates | Non-ISO date format | Use `2026-06-06T00:00:00Z` style (UTC, `Z` suffix) |
| `404` on a `/beta/...` path | Beta contract changed/moved | Check the reference file for a v1.0 alternative; beta is not stable |
| `429 TooManyRequests` | Throttling | `graph.sh` retries with `Retry-After` automatically; for large jobs add `$select` to reduce payload |
| Results look incomplete (exactly 1000 items) | Pagination not followed | Use `graph.sh` (merges all pages); check its `pages` field |
| `400` when adding member to group | Dynamic group | Membership is rule-based; adjust the `membershipRule` instead |
| POST compliance policy rejected | Missing `scheduledActionsForRule` | Include at least one scheduled action block in the body |
| Empty `value` although objects exist in portal | Wrong API surface (v1.0 vs beta) or `$filter` typo | Try the beta path from the reference file; verify property names are camelCase |
