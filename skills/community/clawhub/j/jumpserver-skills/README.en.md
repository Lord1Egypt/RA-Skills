# jumpserver-skills

`jumpserver-skills` is a query-oriented skill repository for JumpServer V4. It supports queries for assets, accounts, users, user groups, platforms, nodes, permissions, audits, and access analysis, making it suitable for day-to-day operations troubleshooting, permission review, audit investigation, object resolution, and environment initialization. It can generate `.env.local` from user-provided config and persist `JMS_ORG_ID`, but business-object and permission actions are limited to queries only.

## Overview

| Entry point | Purpose | Current scope |
|---|---|---|
| `scripts/jms_assets.py` | asset, account, user, user-group, platform, node, and organization queries | `list`, `get` |
| `scripts/jms_permissions.py` | permission rule queries | `list`, `get` |
| `scripts/jms_audit.py` | login, operate, session, and command audits | `list`, `get` |
| `scripts/jms_diagnose.py` | config checks, config writes, connectivity, org selection, resolution, and access analysis | environment init + read-only diagnostics |

## Capability Boundary

- environment initialization writes are allowed: `config-write --confirm` generates or updates `.env.local`, and `select-org --confirm` persists `JMS_ORG_ID`
- the reserved-org special case is allowed: when the accessible org set is exactly `{0002}` or `{0002,0004}`, runtime may auto-write `0002`
- asset, permission, and audit business writes remain unsupported; `create/update/delete/append/remove/unblock` are still forbidden
- this repository is a query-oriented skill, not a general operations executor

## Core Rules

- start with `python3 scripts/jms_diagnose.py config-status --json`
- if config is incomplete, collect user-provided values and run `python3 scripts/jms_diagnose.py config-write --payload '<json>' --confirm`
- then run `python3 scripts/jms_diagnose.py ping`
- if org context is missing, run `python3 scripts/jms_diagnose.py select-org --org-id <org-id> --confirm`
- only the exact reserved org sets `{0002}` or `{0002,0004}` may auto-write `0002`
- business `create/update/delete/append/remove/unblock` operations remain unsupported

## Capability Matrix

| User intent | Recommended entry point | Key input | Output | Common blocker |
|---|---|---|---|---|
| initialize or repair environment | `config-status`, `config-write --confirm`, `ping`, `select-org --confirm` | address, auth, optional `org-id` | config state, `.env.local` write result, connectivity, org persistence result | missing address/auth, connectivity failure, inaccessible org |
| query assets, accounts, users, groups, platforms, nodes, orgs | `jms_assets.py list/get`, `resolve`, `resolve-platform` | `resource` + `id/name/filters` | lists, details, resolution output | ambiguous names, unclear object, org not ready |
| query permission rules | `jms_permissions.py list/get` | `id` or `filters` | permission list and detail | org not ready |
| query audits | `jms_audit.py list/get` | `audit-type`, time window, `command_storage_id` for command audit | login, operate, session, and command audit results | missing `command_storage_id`, org not ready |
| analyze access | `user-assets`, `user-nodes`, `user-asset-access`, `recent-audit` | `username`, optional `asset-name` / time window | effective asset/node access, single-asset access view, recent audit summary | unknown user, too many candidates, org not ready |

## Repository Structure

```text
.
├── SKILL.md
├── README.md
├── README.en.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── audit-queries.md
│   ├── object-mapping.md
│   ├── object-queries.md
│   ├── permission-pagination-validation.md
│   ├── permission-queries.md
│   ├── preflight-and-diagnostics.md
│   ├── query-boundaries.md
│   ├── runtime-behavior.md
│   └── troubleshooting-guide.md
├── scripts/
│   ├── jms_assets.py
│   ├── jms_audit.py
│   ├── jms_bootstrap.py
│   ├── jms_diagnose.py
│   ├── jms_permissions.py
│   └── jms_runtime.py
├── env.sh
└── requirements.txt
```

## Tech Stack and Dependencies

| Item | Current implementation |
|---|---|
| Language | Python 3 |
| Core dependency | `jumpserver-sdk-python>=0.9.1` |
| Execution model | local CLI scripts invoked as `python3 scripts/jms_*.py ...` |
| Target system | JumpServer V4 |
| Config sources | `.env.local` + process environment variables |
| Config write path | `jms_diagnose.py config-write --confirm` |
| Org persistence | `jms_diagnose.py select-org --confirm` |

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Quick Start

Check and initialize config:

```bash
python3 scripts/jms_diagnose.py config-status --json
python3 scripts/jms_diagnose.py config-write --payload '{"JMS_API_URL":"https://jump.example.com","JMS_ACCESS_KEY_ID":"<ak>","JMS_ACCESS_KEY_SECRET":"<sk>","JMS_VERSION":"4"}' --confirm
python3 scripts/jms_diagnose.py ping
```

Inspect and persist org selection:

```bash
python3 scripts/jms_diagnose.py select-org
python3 scripts/jms_diagnose.py select-org --org-id <org-id>
python3 scripts/jms_diagnose.py select-org --org-id <org-id> --confirm
```

Then run queries, for example:

```bash
python3 scripts/jms_assets.py list --resource user --filters '{"username":"demo-user"}'
python3 scripts/jms_permissions.py list --filters '{"limit":20}'
python3 scripts/jms_audit.py list --audit-type operate --filters '{"limit":30}'
```

## Environment Variables

The table below reflects the current implementation and is sourced from `references/runtime-behavior.md` and `scripts/jms_runtime.py`. On first use, the skill can collect these values in dialog and write the result into a local `.env.local`.

| Variable | Required | Description | Example |
|---|---|---|---|
| `JMS_API_URL` | required | JumpServer API/access URL | `https://jump.example.com` |
| `JMS_VERSION` | recommended | JumpServer version, currently treated as `4` by default | `4` |
| `JMS_ACCESS_KEY_ID` | must be paired with `JMS_ACCESS_KEY_SECRET`, or use username/password instead | AK/SK auth ID | `your-access-key-id` |
| `JMS_ACCESS_KEY_SECRET` | must be paired with `JMS_ACCESS_KEY_ID`, or use username/password instead | AK/SK auth secret | `your-access-key-secret` |
| `JMS_USERNAME` | must be paired with `JMS_PASSWORD`, or use AK/SK instead | username/password auth username | `ops-user` |
| `JMS_PASSWORD` | must be paired with `JMS_USERNAME`, or use AK/SK instead | username/password auth password | `your-password` |
| `JMS_ORG_ID` | optional during initialization | written before business execution through `select-org` or the reserved-org auto-selection rule | `00000000-0000-0000-0000-000000000000` |
| `JMS_TIMEOUT` | optional | SDK request timeout in seconds | `30` |
| `JMS_SDK_MODULE` | optional | custom SDK module path, default `jms_client.client` | `jms_client.client` |
| `JMS_SDK_GET_CLIENT` | optional | custom client factory function name, default `get_client` | `get_client` |

Generated `.env.local` example:

```dotenv
JMS_API_URL="https://jump.example.com"
JMS_VERSION="4"
JMS_ORG_ID=""

JMS_ACCESS_KEY_ID="your-access-key-id"
JMS_ACCESS_KEY_SECRET="your-access-key-secret"

# JMS_USERNAME="ops-user"
# JMS_PASSWORD="your-password"

# JMS_TIMEOUT="30"
# JMS_SDK_MODULE="jms_client.client"
# JMS_SDK_GET_CLIENT="get_client"
```

Environment variable rules:

- `JMS_API_URL` is required
- choose exactly one auth mode: `AK/SK` or `username/password`
- `.env.local` is auto-loaded by the scripts
- when first-time config is missing, start with `python3 scripts/jms_diagnose.py config-status --json`
- if you switch JumpServer targets, accounts, orgs, or `.env.local` content, rerun the full first-run validation flow

Implementation notes:

- `scripts/jms_runtime.py` currently constructs the client with `verify=False`
- HTTPS certificate warnings are suppressed
- these two behaviors are not currently controlled by environment variables

## Common Commands

Object queries:

```bash
python3 scripts/jms_assets.py list --resource asset --filters '{"name":"demo-asset"}'
python3 scripts/jms_assets.py get --resource user --id <user-id>
python3 scripts/jms_diagnose.py resolve --resource node --name demo-node
python3 scripts/jms_diagnose.py resolve-platform --value Linux
```

Access analysis:

```bash
python3 scripts/jms_diagnose.py user-assets --username demo-user
python3 scripts/jms_diagnose.py user-nodes --username demo-user
python3 scripts/jms_diagnose.py user-asset-access --username demo-user --asset-name demo-asset
```

Audit queries:

```bash
python3 scripts/jms_audit.py list --audit-type login --filters '{"limit":10}'
python3 scripts/jms_audit.py get --audit-type command --id <command-id> --filters '{"command_storage_id":"<command-storage-id>"}'
```

## Docs Map

| File | Purpose |
|---|---|
| `SKILL.md` | routing rules, environment-init boundaries, and query boundaries |
| `references/runtime-behavior.md` | environment model, `.env.local` writes, and org persistence |
| `references/object-queries.md` | asset, account, user, group, platform, node, and organization query guide |
| `references/permission-queries.md` | permission query guide |
| `references/audit-queries.md` | audit query guide |
| `references/preflight-and-diagnostics.md` | config, org, resolution, and access-analysis guide |
| `references/object-mapping.md` | natural-language-to-resource mapping guide |
| `references/query-boundaries.md` | allowed environment writes and forbidden business writes |
| `references/troubleshooting-guide.md` | common troubleshooting paths |
| `references/permission-pagination-validation.md` | validation record for `jms_permissions.py list` auto-pagination |

## Unsupported Scope

- asset, platform, node, account, user, user-group, and organization create/update/delete/unblock operations
- permission create/update/append/remove/delete operations
- temporary SDK/HTTP scripts that bypass the supported workflow
