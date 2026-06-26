# Tenant-to-Tenant Migration Workflow Reference

## SCM API Authentication

Each tenant requires its own OAuth2 token:

```bash
curl -s -X POST "https://auth.apps.paloaltonetworks.com/am/oauth2/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=${SCM_CLIENT_ID}" \
  -d "client_secret=${SCM_CLIENT_SECRET}" \
  -d "scope=tsg_id:${SCM_TSG_ID}"
```

Response provides a Bearer token valid for ~15 minutes. Re-authenticate before expiry during long migrations.

## Export API Calls by Resource Type

All exports use:
```
GET https://api.sase.paloaltonetworks.com/sse/config/v1/{resource}?folder={folder}&limit=200
```

Handle pagination with `offset` parameter when total exceeds limit.

### Dependency-Ordered Export Sequence

| Order | Resource              | API Path                    | API Support |
|-------|-----------------------|-----------------------------|-------------|
| 1     | Tags                  | `/sse/config/v1/tags`       | Full |
| 2     | Addresses             | `/sse/config/v1/addresses`  | Full |
| 3     | Address Groups        | `/sse/config/v1/address-groups` | Full |
| 4     | Services              | `/sse/config/v1/services`   | Full |
| 5     | Service Groups        | `/sse/config/v1/service-groups` | Full |
| 6     | Application Filters   | `/sse/config/v1/application-filters` | Full |
| 7     | Application Groups    | `/sse/config/v1/application-groups` | Full |
| 8     | External Dynamic Lists| `/sse/config/v1/external-dynamic-lists` | Full |
| 9     | Custom URL Categories | `/sse/config/v1/custom-url-categories` | May return Access denied |
| 10    | HIP Objects           | `/sse/config/v1/hip-objects` | Full |
| 11    | HIP Profiles          | `/sse/config/v1/hip-profiles` | Full |
| 12    | File Blocking Profiles| `/sse/config/v1/file-blocking-profiles` | Full |
| 13    | URL Filtering Profiles| `/sse/config/v1/url-filtering-profiles` | May return Access denied |
| 14    | Data Filtering Profiles| `/sse/config/v1/data-filtering-profiles` | May return Access denied |
| 15    | AI Security Profiles  | `/sse/config/v1/ai-security-profiles` | May return Access denied |
| 16    | Antivirus Profiles    | `/sse/config/v1/anti-virus-profiles` | Full |
| 17    | Anti-Spyware Profiles | `/sse/config/v1/anti-spyware-profiles` | Full |
| 18    | Vulnerability Profiles| `/sse/config/v1/vulnerability-protection-profiles` | Full |
| 19    | Wildfire Profiles     | `/sse/config/v1/wildfire-anti-virus-profiles` | Full |
| 20    | Profile Groups        | `/sse/config/v1/profile-groups` | Full (but refs may be broken) |
| 21    | Log Forwarding Profiles| `/sse/config/v1/log-forwarding-profiles` | Full |
| 22    | Decryption Profiles   | `/sse/config/v1/decryption-profiles` | Full |
| 23    | Security Rules (Pre)  | `/sse/config/v1/security-rules?position=pre` | Full |
| 24    | Security Rules (Post) | `/sse/config/v1/security-rules?position=post` | Full |
| 25    | NAT Rules             | `/sse/config/v1/nat-rules`  | Full |
| 26    | Decryption Rules      | `/sse/config/v1/decryption-rules` | Full |

### Folder Values

Common SCM folder values:
- `"Shared"` — shared configuration (recommended for export/import)
- `"All"` — includes system presets (read-only, don't import here)
- `"Prisma Access"` — Prisma Access specific configuration
- `"Mobile Users"` — GlobalProtect mobile user settings
- `"Remote Networks"` — remote network site settings
- `"Service Connections"` — service connection settings

**Important**: When detecting conflicts, check ALL folders, not just `Shared`. Rules in `All` or `Prisma Access` folders will cause `UNIQUEIN_ERROR` when creating in `Shared`.

## Import API Calls

All imports use:
```
POST https://api.sase.paloaltonetworks.com/sse/config/v1/{resource}?folder={folder}
Content-Type: application/json
Authorization: Bearer {token}

{object-json-body}
```

For security rules, add position to query parameter:
```
POST .../security-rules?folder=Shared&position=pre
```

### Fields to Strip Before Import

Remove these server-generated fields from exported objects before importing:
- `id`
- `created`
- `last_modified`
- `snippet` (if present)
- `override_loc`
- `override_type`
- `override_id`
- `rule_uuid`
- `folder` (goes in query parameter)
- `policy_type`
- `position` (for rules — goes in query parameter)

### Handling Profile Groups with Missing References

When a Profile Group references sub-profiles that cannot be exported (URL Filtering, Data Filtering, AI Security), strip those references before import:

```python
# Example: strip unavailable references
invalid_refs = ["SE_DLP_O365", "Block_QQ_Website", "rali-AI-Runtime-Profile"]
for field in ["data_filtering", "ai_security", "url_filtering"]:
    if field in profile_group:
        remaining = [v for v in profile_group[field] if v not in invalid_refs]
        if remaining:
            profile_group[field] = remaining
        else:
            del profile_group[field]
```

The profile group will be created without those references. Add them back manually in the SCM console after creating the sub-profiles in the target tenant.

### Error Handling

| HTTP Code | Error Type | Meaning | Action |
|-----------|------------|---------|--------|
| 400 | `INVALID_REFERENCE` | Rule references a non-existent object | Create the missing object first, then retry |
| 400 | `Invalid Request Payload` | Nested object structure not supported | Recreate manually in SCM console |
| 409 | `UNIQUEIN_ERROR` | Object with same name exists (any folder) | Skip — likely a system preset |
| 409 | `OBJECT_ALREADY_EXISTS` | Object exists in another folder | Skip — check if it's in `All` or `Prisma Access` folder |
| 429 | Rate limited | Too many requests | Wait and retry with exponential backoff |
| 401/403 | Auth error / Access denied | Token expired or insufficient permissions | Refresh token; check Service Account role |

## Candidate Config Validation

After importing, validate by pushing candidate config without committing:

```bash
curl -s -X POST "https://api.sase.paloaltonetworks.com/sse/config/v1/config-versions/candidate:push" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"folders": ["Prisma Access"]}'
```

Check push job status:
```
GET https://api.sase.paloaltonetworks.com/sse/config/v1/jobs/{job-id}
```
