---
name: prisma-access
description: All-in-one Prisma Access management for Strata Cloud Manager (SCM). Generate configurations, audit against best practices, migrate between tenants, troubleshoot issues, and automate via SCM API.
argument-hint: "[command] [details]"
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
    emoji: "\U0001F6E1\uFE0F"
    homepage: https://github.com/leesandao/prismaaccess-skill
---

# Prisma Access All-in-One Skill

Complete Prisma Access configuration management for Strata Cloud Manager (SCM).

This is the all-in-one version. Individual skills are also available: `prisma-config`, `prisma-audit`, `prisma-migrate`, `prisma-troubleshoot`, `prisma-api`.

## Commands

Determine the user's intent from `$ARGUMENTS` and execute the corresponding workflow:

- **config** / **generate** → [Configuration Generator](#1-configuration-generator)
- **audit** / **review** / **check** → [Configuration Auditor](#2-configuration-auditor)
- **migrate** / **move** / **copy** → [Tenant Migration](#3-tenant-migration)
- **troubleshoot** / **debug** / **diagnose** → [Troubleshooting](#4-troubleshooting)
- **api** / **query** / **list** / **create** / **update** / **delete** → [SCM API Operations](#5-scm-api-operations)

If no command is specified, ask the user what they need.

---

## 1. Configuration Generator

Generate production-ready Prisma Access configurations as SCM API-compatible JSON payloads.

### Supported Configuration Types

- **Security Policy Rules**: pre-rules, post-rules, source/destination zones, App-ID, security profiles, log forwarding
- **NAT Rules**: source NAT (dynamic IP/port, static IP), destination NAT, bidirectional NAT
- **Decryption Policy**: SSL forward proxy, SSL inbound inspection, no-decrypt rules, decryption profiles
- **URL Filtering Profiles**: category actions, custom URL categories, credential phishing prevention
- **GlobalProtect**: portal, gateway, authentication profiles (SAML/LDAP/RADIUS), HIP profiles, split tunneling
- **Address Objects/Groups**: IP netmask, FQDN, IP range, wildcard mask, static/dynamic groups
- **Service Connections**: IPSec tunnels, BGP routing, static routes, QoS
- **Other**: application filters/groups, custom applications, EDLs, tags, log forwarding profiles, security profile groups

### Output Format

Always output as SCM API-compatible JSON:
```
POST https://api.sase.paloaltonetworks.com/sse/config/v1/{resource}?folder={folder}
```

Include the JSON payload, API endpoint, required `folder` parameter, and any query parameters.

### Best Practices Applied

1. Application-based rules over port-based; logging on all rules; security profiles on all allow rules
2. Distinct zones for Mobile Users, Remote Networks, Service Connections
3. Clear naming conventions with consistent prefixes (e.g., `PA-SEC-`, `PA-NAT-`)
4. Specific rules before general; best-practice security profile groups
5. Log-at-session-end enabled; log forwarding to SIEM or Cortex Data Lake

---

## 2. Configuration Auditor

Audit Prisma Access configurations for security, compliance, and operational best practices.

### Audit Categories

1. **Security Policy**: shadow rules, overly permissive rules (`any/any/any/allow`), missing security profiles, missing logging, disabled/unused rules, port-based rules
2. **NAT Policy**: missing corresponding security rules, overlapping translations, source NAT exhaustion risks
3. **Decryption Policy**: unjustified bypass, missing profiles, expired certificates, overly broad no-decrypt rules
4. **GlobalProtect**: weak authentication, missing HIP checks, permissive split tunnel, missing client certificates
5. **Object Hygiene**: unused objects, overlapping addresses, unresolvable FQDNs, empty groups, duplicates
6. **Compliance**: PAN-OS Best Practice Assessment (BPA), CIS Palo Alto Benchmark, Zero Trust principles

### Output Format

For each finding:
```
[SEVERITY] Category - Finding Title
  Description: What was found
  Location: Rule/object name and position
  Risk: Why this is a problem
  Recommendation: How to fix it
```

Severity: CRITICAL > HIGH > MEDIUM > LOW > INFO

Summary: health score (0-100), finding counts by severity, top 5 priorities, quick wins.

---

## 3. Tenant Migration

Migrate configurations between Prisma Access tenants (TSGs) via SCM API.

### Prerequisites

```bash
# Source tenant
export SRC_SCM_CLIENT_ID="source-client-id"
export SRC_SCM_CLIENT_SECRET="source-client-secret"
export SRC_SCM_TSG_ID="source-tsg-id"

# Target tenant
export DST_SCM_CLIENT_ID="target-client-id"
export DST_SCM_CLIENT_SECRET="target-client-secret"
export DST_SCM_TSG_ID="target-tsg-id"
```

### Migration Workflow

1. **Export** from source tenant in dependency order: tags → addresses → groups → services → profiles → policies
2. **Conflict Detection**: check target for name conflicts, reference conflicts, zone mismatches. Options: skip / overwrite / rename
3. **Transform & Import**: strip server fields (`id`, `created`, `last_modified`), update folder, resolve renamed references, POST to target
4. **Validate**: push candidate config without committing
5. **Commit**: only after explicit user confirmation

### Safety Guardrails

- Dry-run by default: always show what would be imported first
- No auto-commit: never commit without user confirmation
- Rate limiting: respect SCM API limits

---

## 4. Troubleshooting

Diagnose and resolve common Prisma Access issues.

### Troubleshooting Areas

**GlobalProtect Connectivity**: certificates, SAML IdP, HIP check failures, DNS, MTU, UDP 4501 blocking

**Security Policy Not Matching**: rule ordering, shadow rules, missing SSL decryption for App-ID, zone confusion, stale FQDN, User-ID mapping

**Configuration Push Failures**: reference errors, duplicate names, invalid values, dependency conflicts, concurrent edits

**Remote Network / Service Connection**: IKE/IPSec parameter mismatch, pre-shared key, BGP peer config, overlapping IPs

**SCM API Errors**:
| Code | Solution |
|------|----------|
| 400 | Check JSON payload format |
| 401 | Token expired — re-authenticate |
| 403 | Check role-based access and TSG ID |
| 404 | Verify object name and folder |
| 409 | Object exists — use PUT to update |
| 429 | Back off and retry |

**Performance**: bandwidth allocation, QoS policy, service edge location, routing, session limits

### Diagnostic Approach

1. Identify the category → 2. Gather info (errors, affected users, timeline) → 3. Check config via API → 4. Identify root cause → 5. Provide fix → 6. Verify

---

## 5. SCM API Operations

Execute operations against the Strata Cloud Manager API.

### Authentication

```bash
TOKEN=$(curl -s -X POST "https://auth.apps.paloaltonetworks.com/am/oauth2/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=${SCM_CLIENT_ID}" \
  -d "client_secret=${SCM_CLIENT_SECRET}" \
  -d "scope=tsg_id:${SCM_TSG_ID}" | jq -r '.access_token')
```

### API Base URL

```
https://api.sase.paloaltonetworks.com
```

### Operations

**List**: `GET /sse/config/v1/{resource}?folder={folder}&limit=200`

**Create**: `POST /sse/config/v1/{resource}?folder={folder}` with JSON body

**Update**: `PUT /sse/config/v1/{resource}/{id}` with JSON body

**Delete**: `DELETE /sse/config/v1/{resource}/{id}`

**Push Config**: `POST /sse/config/v1/config-versions/candidate:push`

**Job Status**: `GET /sse/config/v1/jobs/{job-id}`

### Available Resources

`addresses`, `address-groups`, `services`, `service-groups`, `tags`, `security-rules`, `nat-rules`, `decryption-rules`, `application-filters`, `application-groups`, `external-dynamic-lists`, `custom-url-categories`, `url-filtering-profiles`, `anti-virus-profiles`, `anti-spyware-profiles`, `vulnerability-protection-profiles`, `file-blocking-profiles`, `wildfire-anti-virus-profiles`, `profile-groups`, `log-forwarding-profiles`, `decryption-profiles`, `hip-objects`, `hip-profiles`

### Folder Values

`"Prisma Access"`, `"Mobile Users"`, `"Remote Networks"`, `"Service Connections"`

### Safety Rules

1. Always authenticate first
2. Never commit without user confirmation
3. Use dry-run when possible
4. Respect rate limits
5. Log all changes for audit trail
