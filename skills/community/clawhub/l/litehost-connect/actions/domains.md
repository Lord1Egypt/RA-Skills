# Domains

View custom domains and manage their project assignments.

Domains are created and verified through the Litehost dashboard. This API provides read access and allows assigning/removing domains from projects.

**Paid plan required.** All domain endpoints return `403 FREE_TIER_RESTRICTED` for free-tier users.

---

## List Domains

```
GET /v1/domains
```

Returns all custom domains for the authenticated user.

```bash
curl https://connect.litehost.io/v1/domains \
  -H "Authorization: Bearer $LITEHOST_API_KEY"
```

### Response (200)

```json
{
  "status": "success",
  "data": {
    "domains": [
      {
        "id": "uuid",
        "domain": "example.com",
        "status": "active",
        "verifiedAt": "...",
        "projectCount": 2,
        "createdAt": "..."
      }
    ]
  }
}
```

### Domain status values

| Status | Meaning |
|---|---|
| `pending_verification` | DNS records not yet verified. |
| `propagation_wait` | DNS verified, waiting for propagation. |
| `active` | Domain is ready to use. |
| `error_dns` | DNS configuration error. |
| `ssl_pending` | SSL certificate being provisioned. |
| `ssl_active` | SSL active and serving traffic. |

Only assign domains with status `active` or `ssl_active` to projects.

---

## Get Domain Details

```
GET /v1/domains/{domainId}
```

Returns domain info plus all projects currently assigned to it.

```bash
curl https://connect.litehost.io/v1/domains/{domainId} \
  -H "Authorization: Bearer $LITEHOST_API_KEY"
```

---

## Assign Domain to Project

Use `update-project.md` (PATCH) with `domainId` set to the domain UUID. The project's slug becomes a subdomain of that domain.

```bash
curl -X PATCH https://connect.litehost.io/v1/projects/{projectId} \
  -H "Authorization: Bearer $LITEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domainId": "domain-uuid-here"}'
```

---

## Remove Domain from Project

Use `update-project.md` (PATCH) with `domainId` set to `null`.

```bash
curl -X PATCH https://connect.litehost.io/v1/projects/{projectId} \
  -H "Authorization: Bearer $LITEHOST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domainId": null}'
```

---

## Error Handling

| Status | Action |
|---|---|
| 401 | Follow `utils/auth.md`. |
| 403 | Free-tier restricted. Requires paid plan. Tell user to upgrade at https://litehost.io/dashboard. |
| 404 | Domain or project not found. List domains first to verify the ID. |
