# Permission Parity Rules (Gusnais)

Goal: keep API interaction behavior consistent with gusnais.com web UX across different account permissions.

## Source priority
1. Resource `abilities` in response payload (highest)
2. HTTP status (`401/403/404`)
3. Static defaults (fallback only)

## UI/action gating
For each actionable resource:
- If abilities indicate deny -> `enabled=false`, keep reason explicit.
- If abilities indicate allow -> `enabled=true`.
- If abilities absent -> allow tentative UI but enforce at submit.

## Must-follow cases
- Topic update/delete and special actions (`ban|excellent|unexcellent|close|open`) must be gated.
- Reply update/delete must be gated when abilities are available via detail payload.

## Denial mapping
- `403` => `no_permission`
- `404` => `resource_unavailable`
- `401` => `auth_required`

## Retry & refresh
- On 401: attempt token refresh once then retry once.
- On repeated 401: force re-auth.
- On 403 after optimistic gating: refresh abilities cache and keep denied.

## Cache policy
- abilities cache TTL: 60-180 seconds.
- Invalidate cache on:
  - token refresh
  - user switch
  - explicit permission failure (403)

## Plugin-specific parity notes

### Press (`press-master`)
- Member can create post.
- Member can update/destroy own post only when status is `upcoming`.
- Admin/maintainer can manage posts and publish.
- Anonymous is read-only (`read`, `upcoming`).

### Note (`note-master`)
- Logged-in user can create notes.
- Logged-in user can read/update/destroy own notes.
- Everyone can read `publish=true` notes.
- Preview is allowed by plugin ability.

### Site (`site-master`)
- Anonymous/read-only for sites.
- Create/update/delete are restricted (current deployment uses admin-only style ability for write actions).
- API exposes `site_nodes` read for client-side validation (`site_node_id` lookup).
- Admin routes (`admin/sites`, `admin/site_nodes`) remain server-enforced.

### Jobs (`jobs-master`)
- Jobs listing is public (`/jobs` view).
- Job posting is constrained by builtin node policy (`node_id=25`):
  - default deny for non-admin users;
  - allow only HR role or whitelist login.

## Security
- Never attempt hidden admin actions without server-side permission.
- Never infer elevated roles from UI hints alone.
- Never bypass ability checks by direct ID probing.
