# Link Opens

Whether and when a link was opened: total opens, the last open, and the latest opens with country,
device and referrer. Paid plans (`FEATURE_LOCKED` on Free).

## When to use

- "Did my client open it?", "has anyone seen the proposal?", "who opened the link?"

---

## Get Link Opens

```
GET /v1/projects/{projectId}/analytics
Authorization: Bearer <key>
```

### Example

```bash
scripts/litehost.sh api GET /v1/projects/PROJECT_ID/analytics
```

### Response (200)

```json
{
  "status": "success",
  "data": {
    "projectId": "…",
    "analyticsEnabled": true,
    "opens": { "total": 3, "last24h": 1, "last7d": 3 },
    "lastOpenedAt": "2026-09-30T10:12:00.000Z",
    "recentOpens": [
      { "at": "2026-09-30T10:12:00.000Z", "country": "ES", "device": "mobile", "browser": "Safari", "os": "iOS", "referrer": null }
    ],
    "topCountries": [{ "country": "ES", "opens": 3 }],
    "visits": { "total": 7, "last24h": 2, "last7d": 7 },
    "ownerOpens": { "total": 2 }
  }
}
```

### What counts as an open

An open is a person viewing the link in a browser. Link previews (WhatsApp, Slack…), bots, email
scanners, AI assistants fetching the link and the owner's own views are not opens. `visits` counts
every non-bot page request, previews included; `ownerOpens` counts the owner's own views.

Tell the user plainly, e.g. "Opened 3 times, last today at 10:12 from a phone in Spain", or "Not
opened yet". Do not report `visits` as opens.

### Errors

| Status | Code | Do this |
|---|---|---|
| 403 | `FEATURE_LOCKED` | Needs a paid plan. Tell the user and link https://litehost.io/dashboard?upgrade=plans. |
| 404 | — | Project not found. List projects and let the user pick. |
