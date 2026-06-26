---
name: prisma-migrate
description: Migrate Prisma Access configurations between different SCM tenants (TSGs). Use when moving security policies, NAT rules, address objects, and other configurations from one Prisma Access tenant to another. Includes migration compatibility matrix based on real-world testing.
argument-hint: "[source-tsg] [target-tsg]"
disable-model-invocation: true
version: 1.1.0
metadata:
  openclaw:
    requires:
      env:
        - SCM_CLIENT_ID
        - SCM_CLIENT_SECRET
      bins:
        - curl
        - jq
    primaryEnv: SCM_CLIENT_ID
    emoji: "\U0001F500"
    homepage: https://github.com/leesandao/prismaaccess-skill
---

# Prisma Access Tenant-to-Tenant Configuration Migration

Migrate configurations between Prisma Access tenants (TSGs) via the Strata Cloud Manager API.

## Overview

This skill helps you export configurations from a source tenant and import them into a target tenant. It handles naming conflicts, reference resolution, and dependency ordering.

For detailed API call reference, see [migration-workflow.md](reference/migration-workflow.md).

## Migration Compatibility Matrix

Based on real-world migration testing, here is what can and cannot be migrated directly via SCM API:

### Directly Migratable (API fully supported)

| Resource | Notes |
|----------|-------|
| Tags | No issues |
| Address Objects | IP netmask, FQDN, IP range, IP wildcard all supported |
| Address Groups | Static and dynamic; referenced addresses must exist first |
| Service Objects | No issues |
| Service Groups | No issues |
| Application Filters | No issues |
| Application Groups | No issues |
| External Dynamic Lists (EDL) | No issues |
| HIP Objects | No issues |
| HIP Profiles | No issues |
| File Blocking Profiles | No issues |
| Profile Groups | Supported, but referenced sub-profiles must exist first |
| Security Rules (most) | Simple rules migrate directly |
| NAT Rules | No issues |
| Decryption Rules (most) | Simple rules migrate directly |

### Not Directly Migratable (require manual handling)

| Resource | Issue | Workaround |
|----------|-------|------------|
| URL Filtering Profiles | Service Account returns `Access denied` | Grant additional API permissions, or recreate manually in SCM console |
| Data Filtering Profiles | Service Account returns `Access denied` | Same as above |
| AI Security Profiles | Service Account returns `Access denied` | Same as above |
| Custom URL Categories | API returns 0 results or `Access denied` | Recreate manually in SCM console before migrating rules that reference them |
| Profile Groups with inaccessible refs | References URL Filtering / Data Filtering / AI Security profiles that can't be exported | Migrate with invalid references stripped; add them back manually after creating the sub-profiles in the target tenant |
| Rules referencing missing objects | Security/Decryption rules fail with `INVALID_REFERENCE` | Create the missing referenced objects first, then retry the rule |
| `app-tagging` rules | Nested object arrays cause `Invalid Request Payload` | Recreate manually in SCM console |
| Cross-folder name conflicts | Rules with same name in `All` or `Prisma Access` folder cause `UNIQUEIN_ERROR` | Skip — these are typically system-preset rules already present in the target |

### Key Lessons

1. **Dependency order is critical**: Tags → Addresses → Groups → Services → File Blocking Profiles → URL/Data/AI Profiles → Profile Groups → Rules
2. **Service Account permissions are the biggest blocker**: URL Filtering, Data Filtering, and AI Security profile APIs require elevated permissions that default Service Accounts may not have
3. **Conflict detection must check ALL folders**: Rules exist across `Shared`, `All`, `Prisma Access`, `Mobile Users` folders — checking only `Shared` misses conflicts
4. **Profile Groups can be partially migrated**: Strip invalid references, import the group, then manually add the missing references later
5. **System-preset objects should be skipped**: Both tenants share identical predefined objects (best-practice profiles, default EDLs, default HIP objects)
6. **Fields to strip before import**: `id`, `created`, `last_modified`, `snippet`, `override_loc`, `override_type`, `override_id`, `rule_uuid`, `folder`, `policy_type`, `position` (position goes in the query parameter instead)

## Prerequisites

Set the following environment variables:

```bash
# Source tenant credentials
export SRC_SCM_CLIENT_ID="source-client-id"
export SRC_SCM_CLIENT_SECRET="source-client-secret"
export SRC_SCM_TSG_ID="source-tsg-id"

# Target tenant credentials
export DST_SCM_CLIENT_ID="target-client-id"
export DST_SCM_CLIENT_SECRET="target-client-secret"
export DST_SCM_TSG_ID="target-tsg-id"
```

## Migration Workflow

### Step 1: Export from Source Tenant

Authenticate and export all configuration objects from the source tenant via SCM API:

```
GET https://api.sase.paloaltonetworks.com/sse/config/v1/{resource}?folder={folder}&limit=200
```

Export objects in dependency order. Handle pagination with `offset` when total exceeds limit.

### Step 2: Conflict Detection

Before importing, check the target tenant for conflicts across **all folders** (`Shared`, `All`, `Prisma Access`, `Mobile Users`, `Remote Networks`):

- **Name conflicts**: objects with the same name — typically skip (system presets)
- **Reference conflicts**: objects referencing things not in the target — need to create dependencies first or strip invalid references
- **Cross-folder conflicts**: rules in `All` folder that block creation in `Shared` — skip these

For each conflict, present the user with options:
- **Skip**: do not import (recommended for system presets)
- **Overwrite**: replace the target object with the source object
- **Rename**: import with a prefix/suffix (e.g., `migrated-` prefix)
- **Strip references**: import without invalid references, fix manually later

### Step 3: Transform and Import

For each object:
1. Remove source-tenant-specific fields (`id`, `created`, `last_modified`, `snippet`, `override_loc`, `override_type`, `override_id`, `rule_uuid`)
2. Remove `folder` and `policy_type` from the body (folder goes in query param)
3. For rules: remove `position` from body (goes in query param as `&position=pre` or `&position=post`)
4. For Profile Groups with invalid references: strip the unavailable sub-profile references
5. POST to the target tenant API

```
POST https://api.sase.paloaltonetworks.com/sse/config/v1/{resource}?folder={folder}
```

### Step 4: Validation

After import:
1. List all imported objects and verify counts match source
2. Check for broken references
3. Run a candidate config push to validate (without committing)

```
POST https://api.sase.paloaltonetworks.com/sse/config/v1/config-versions/candidate:push
```

### Step 5: Commit (User-Confirmed)

Only commit after user explicitly confirms:

```
POST https://api.sase.paloaltonetworks.com/sse/config/v1/config-versions/running:push
```

## Usage Examples

```
/prisma-access:prisma-migrate
```
Interactive mode: prompts for source and target tenant details.

```
/prisma-access:prisma-migrate 1234567890 0987654321
```
Migrate from TSG 1234567890 to TSG 0987654321.

## Safety Guardrails

- **Dry-run by default**: always show what would be imported before making changes
- **No auto-commit**: never commit configuration without explicit user confirmation
- **Rollback guidance**: provide instructions to undo changes if needed
- **Rate limiting**: respect SCM API rate limits (avoid bulk API flooding)
- **Skip system presets**: automatically skip predefined objects that exist in both tenants
