---
name: prisma-api
description: Interact with the Strata Cloud Manager (SCM) API to manage Prisma Access configurations. Authenticate, query, create, update, and delete configuration objects. Use when automating Prisma Access operations or querying live tenant state.
argument-hint: "[operation] [resource]"
disable-model-invocation: true
allowed-tools: Bash(curl *)
version: 1.1.0
metadata:
  openclaw:
    requires:
      env:
        - SCM_CLIENT_ID
        - SCM_CLIENT_SECRET
        - SCM_TSG_ID
      bins:
        - curl
        - jq
    primaryEnv: SCM_CLIENT_ID
    emoji: "\U0001F310"
    homepage: https://github.com/leesandao/prismaaccess-skill
---

# Strata Cloud Manager API Operations

Execute operations against the Strata Cloud Manager (SCM) API for Prisma Access.

## Prerequisites

The following environment variables must be set:

```bash
export SCM_CLIENT_ID="your-client-id"
export SCM_CLIENT_SECRET="your-client-secret"
export SCM_TSG_ID="your-tsg-id"
```

## Authentication

Obtain an OAuth2 Bearer token before making API calls:

```bash
TOKEN=$(curl -s -X POST "https://auth.apps.paloaltonetworks.com/am/oauth2/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=${SCM_CLIENT_ID}" \
  -d "client_secret=${SCM_CLIENT_SECRET}" \
  -d "scope=tsg_id:${SCM_TSG_ID}" | jq -r '.access_token')
```

Token validity: ~15 minutes. Re-authenticate before expiry.

## API Base URL

```
https://api.sase.paloaltonetworks.com
```

## Supported Operations

When the user specifies `$ARGUMENTS`, execute the corresponding operation.

### List / Query Resources

```bash
curl -s -X GET "https://api.sase.paloaltonetworks.com/sse/config/v1/{resource}?folder={folder}&limit=200" \
  -H "Authorization: Bearer ${TOKEN}"
```

Available resources:
- `addresses`, `address-groups`
- `services`, `service-groups`
- `tags`
- `security-rules` (add `&position=pre` or `&position=post`)
- `nat-rules`
- `decryption-rules`
- `application-filters`, `application-groups`
- `external-dynamic-lists`
- `custom-url-categories`
- `url-filtering-profiles`
- `anti-virus-profiles`, `anti-spyware-profiles`
- `vulnerability-protection-profiles`
- `file-blocking-profiles`, `wildfire-anti-virus-profiles`
- `profile-groups`
- `log-forwarding-profiles`
- `decryption-profiles`
- `hip-objects`, `hip-profiles`

Folder values: `"Prisma Access"`, `"Mobile Users"`, `"Remote Networks"`, `"Service Connections"`

### Create a Resource

```bash
curl -s -X POST "https://api.sase.paloaltonetworks.com/sse/config/v1/{resource}?folder={folder}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

### Update a Resource

```bash
curl -s -X PUT "https://api.sase.paloaltonetworks.com/sse/config/v1/{resource}/{id}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

### Delete a Resource

```bash
curl -s -X DELETE "https://api.sase.paloaltonetworks.com/sse/config/v1/{resource}/{id}" \
  -H "Authorization: Bearer ${TOKEN}"
```

### Push Candidate Configuration

Validate and push the candidate configuration:

```bash
# Push candidate config
curl -s -X POST "https://api.sase.paloaltonetworks.com/sse/config/v1/config-versions/candidate:push" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"folders": ["Prisma Access"]}'
```

### Check Job Status

```bash
curl -s -X GET "https://api.sase.paloaltonetworks.com/sse/config/v1/jobs/{job-id}" \
  -H "Authorization: Bearer ${TOKEN}"
```

### List Config Versions

```bash
curl -s -X GET "https://api.sase.paloaltonetworks.com/sse/config/v1/config-versions?limit=10" \
  -H "Authorization: Bearer ${TOKEN}"
```

## Pagination

For resources with more than 200 items, paginate with `offset`:

```bash
# Page 1
curl -s "...?folder=Prisma Access&limit=200&offset=0"
# Page 2
curl -s "...?folder=Prisma Access&limit=200&offset=200"
```

Continue until `total` in response matches items retrieved.

## Error Handling

- **401**: Token expired. Re-run authentication.
- **429**: Rate limited. Wait 60 seconds before retrying.
- **400**: Check the request body for invalid fields.
- **409**: Object already exists. Use PUT to update.

## Safety Rules

1. **Always authenticate first** before making any API calls
2. **Never commit without user confirmation** — push candidate config and ask user to review before committing
3. **Use dry-run when possible** — show what will change before executing
4. **Respect rate limits** — add delays between bulk operations
5. **Log all changes** — output every API call made for audit trail
