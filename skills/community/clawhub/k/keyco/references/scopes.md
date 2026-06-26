# Keyco API Scopes

When creating API keys via `keyco api-keys create`, pick the minimum required scopes.

## Common Scope Combinations

| Use case | Scopes |
|---|---|
| Read-only dashboards | `dubs:read`, `analytics:read`, `groups:read` |
| CI/CD reporting | `dubs:read`, `analytics:read`, `lifecycles:read`, `workflows:read` |
| Full asset management | `dubs:read`, `dubs:update`, `groups:read`, `groups:update`, `workflows:read` |
| Compliance / audit tooling | `dubs:read`, `lifecycles:read`, `lifecycles:create`, `analytics:read` |
| Fleet device provisioning | `fleet:provision` |

## Full Scope List

### Assets (DUBs)
- `dubs:read` — View assets
- `dubs:create` — Create/claim assets
- `dubs:update` — Update assets
- `dubs:delete` — Delete assets

### Workflows
- `workflows:read`, `workflows:create`, `workflows:update`, `workflows:delete`

### Lifecycles
- `lifecycles:read`, `lifecycles:create`, `lifecycles:update`

### Analytics
- `analytics:read`

### Groups
- `groups:read`, `groups:write`, `groups:update`

### Members
- `members:read`, `members:create`, `members:update`, `members:delete`

### Administrative
- `access:control` — API keys, roles, MFA
- `billing:manage`
- `integrations:read`, `integrations:manage`

### Templates
- `templates:read`, `templates:create`, `templates:update`, `templates:delete`

### Other
- `imports:create` — CSV/JSON asset import
- `fleet:provision` — Fleet auto-claim
