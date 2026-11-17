---
name: huawei-cloud-iam-user-manage
description: |
  1. Creates Huawei Cloud IAM users and authorizes them through the IAM v5
     OpenAPI: create a user (name / description / enabled), create or reuse a
     user group, add the user to the group, and attach identity policies.
  2. Execution order: KooCLI (`hcloud IAM <Operation>`) first, then the official
     `huaweicloudsdkiam` v5 Python SDK as a transparent fallback. Read-only
     lookups (list users / groups / policies) support name-to-id resolution.
  3. Idempotent by design: an existing user/group is reused and an
     already-existing membership or attachment is reported instead of failing.
  4. Explicitly OUT OF SCOPE: deleting or disabling users, deleting groups,
     AK/SK rotation, password policy, MFA, agencies/delegation.
  5. Triggers include: "创建IAM用户", "IAM用户授权", "给用户授权", "关联用户组",
     "绑定权限策略", "IAM user create", "create IAM user", "authorize IAM user",
     "add user to group", "attach policy to user", "iam user manage".
tags: [huawei-cloud, iam, user, authorization, security]
---

# Huawei Cloud IAM User Manage

## Overview

Create Huawei Cloud IAM users and authorize them. The skill wraps the IAM v5
identity OpenAPI and can be driven either through KooCLI (`hcloud`) or the
official Python SDK. It covers the two outcomes the user cares about:

1. **Create an IAM user** and return its identifier (`user_id` / `user_name`).
2. **Authorize the user** by adding it to a user group and/or attaching one or
   more identity policies.

Architecture:

```text
agent → python3 scripts/iam_user_manage.py <command>
      → validation (name / description / id rules)
      → execution:  hcloud IAM <Operation> --cli-region=<region>  (CLI, primary)
                  → huaweicloudsdkiam v5 (SDK fallback)
      → normalized result → text / JSON stdout
```

Key properties:

- **CLI first, SDK fallback** — `hcloud` is attempted first; when it is absent
  or a call fails to construct, the skill falls back to the official SDK.
- **Read-only name resolution** — `--group-name` / `--policy-name` are resolved
  to ids with read-only list calls, so users do not need to look up ids by hand.
- **Idempotent** — an existing user or group is reused; a duplicate membership
  or attachment is reported (`already_member` / `already_attached`) rather than
  raising an error.
- **Write confirmation** — every mutating command requires `--confirm`
  (or `--dry-run` to preview the plan first).
- **Capability boundary** — this skill never deletes or disables a user, never
  deletes a group, and never touches AK/SK, password policy, MFA or agencies.

> **Dependency**: Quality telemetry is collected automatically via skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## IAM v5 Operations

All REST paths below are the SDK `_http_info` `resource_path` verbatim.

| Feature | KooCLI operation | SDK method | REST path |
| ------- | ---------------- | ---------- | --------- |
| Create user | `CreateUserV5` | `create_user_v5` | `POST /v5/users` |
| List users | `ListUsersV5` | `list_users_v5` | `GET /v5/users` |
| Show user | `ShowUserV5` | `show_user_v5` | `GET /v5/users/{user_id}` |
| Create group | `CreateGroupV5` | `create_group_v5` | `POST /v5/groups` |
| List groups | `ListGroupsV5` | `list_groups_v5` | `GET /v5/groups` |
| Add user to group | `AddUserToGroupV5` | `add_user_to_group_v5` | `POST /v5/groups/{group_id}/add-user` |
| Attach user policy | `AttachUserPolicyV5` | `attach_user_policy_v5` | `POST /v5/policies/{policy_id}/attach-user` |
| List policies | `ListPoliciesV5` | `list_policies_v5` | `GET /v5/policies` |
| List attached user policies | `ListAttachedUserPoliciesV5` | `list_attached_user_policies_v5` | `GET /v5/users/{user_id}/attached-policies` |

Request bodies (verified against the SDK models):

- `CreateUserReqBody`: `name` (1-64; letters/digits/`_`/`-`/`.`; first char not a
  digit), `description` (0-255; forbids `@ # % & < > \ $ ^ *`), `enabled` (bool).
- `CreateGroupReqBody`: `group_name` (1-128), `description` (0-255).
- `AddUserToGroupReqBody`: `user_id`. `AttachUserPolicyReqBody`: `user_id`.

## Prerequisites

1. **KooCLI (`hcloud`)** — optional primary execution path; install and
   authenticate out-of-band. See
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   When absent, the SDK fallback is used.
2. **Python 3.8+** with the Huawei Cloud SDK — run
   `python3 scripts/ensure_env.py` to install `huaweicloudsdkcore` and
   `huaweicloudsdkiam`.
3. **Credentials configured out-of-band** — the CLI reads the active hcloud
   profile; the SDK fallback reads AK/SK from whitelisted environment variables
   (`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`, `HUAWEI_*`, `HW_*`, `HWC_*`).
   Never paste AK/SK into chat; the script never reads, echoes or stores secrets.
4. **IAM permissions** — the least-privilege actions are listed in
   [references/iam-policies.md](references/iam-policies.md).
5. **Outbound HTTPS** access to `iam.<region>.myhuaweicloud.com`.
- **skill-quality-cli** — ensured by bash scripts/ensure_cli.sh (idempotent, skips if present)
  - Upgrade: run skill-quality-cli upgrade manually (no auto-upgrade)
  - Disable telemetry report: set SKILL_QUALITY_REPORT=0

## Workflow

1. **(Optional) prepare the environment** — `python3 scripts/ensure_env.py`
   installs any missing SDK dependency.
2. **(Optional) confirm readiness** (read-only) — see the Core Commands block.
3. **Create the user** — `create-user` validates the name, optionally reuses /
   creates a group, and optionally attaches policies.
4. **Authorize the user** — `authorize` adds an existing user to a group and/or
   attaches policies (idempotent).
5. **Inspect** — `list-users` / `list-groups` / `list-policies` / `show-user`.
6. **Read the result** — text by default, or `--json` for the full payload.
7. **Handle errors** per the Error Handling table below.

## Core Commands

> **⚠️ Mandatory: every hcloud command in this skill MUST be wrapped with skill-quality-cli run --skill-name huawei-cloud-iam-user-manage -- ** — bare hcloud calls are strictly forbidden.**

```bash
# Preview first (offline, no credentials needed)
python3 scripts/iam_user_manage.py create-user --name alice \
  --description "ops account" --group-name ops --policy-name ReadOnlyAccess --dry-run

# Create a user and authorize it in one shot
python3 scripts/iam_user_manage.py create-user --name alice \
  --description "ops account" --group-name ops --create-group --policy-name ReadOnlyAccess --confirm

# Create a user only (return user_id / user_name)
python3 scripts/iam_user_manage.py create-user --name bob --region cn-north-4 --json --confirm

# Authorize an existing user (add to group + attach policy), idempotent
python3 scripts/iam_user_manage.py authorize --user-name alice \
  --group-name ops --create-group --policy-name ReadOnlyAccess --confirm

# Direct, targeted authorization
python3 scripts/iam_user_manage.py add-user-to-group --user-id <user_id> --group-id <group_id> --confirm
python3 scripts/iam_user_manage.py attach-policy --user-id <user_id> --policy-name ReadOnlyAccess --confirm

# Read-only lookups (name-to-id resolution)
python3 scripts/iam_user_manage.py list-users --json
python3 scripts/iam_user_manage.py list-groups --json
python3 scripts/iam_user_manage.py list-policies --json
python3 scripts/iam_user_manage.py show-user --user-name alice --json
```

Equivalent direct KooCLI commands (attempted first by the script, all wrapped):

```bash
skill-quality-cli run --skill-name huawei-cloud-iam-user-manage -- hcloud IAM CreateUserV5 --cli-region=cn-north-4 --name=alice --description="ops account" --enabled=true
skill-quality-cli run --skill-name huawei-cloud-iam-user-manage -- hcloud IAM CreateGroupV5 --cli-region=cn-north-4 --group_name=ops
skill-quality-cli run --skill-name huawei-cloud-iam-user-manage -- hcloud IAM AddUserToGroupV5 --cli-region=cn-north-4 --group_id=<group_id> --user_id=<user_id>
skill-quality-cli run --skill-name huawei-cloud-iam-user-manage -- hcloud IAM AttachUserPolicyV5 --cli-region=cn-north-4 --policy_id=<policy_id> --user_id=<user_id>
skill-quality-cli run --skill-name huawei-cloud-iam-user-manage -- hcloud IAM ListUsersV5 --cli-region=cn-north-4 --limit=100
skill-quality-cli run --skill-name huawei-cloud-iam-user-manage -- hcloud IAM ListPoliciesV5 --cli-region=cn-north-4 --limit=100
skill-quality-cli run --skill-name huawei-cloud-iam-user-manage -- hcloud configure list
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| ----------- | ---------- | ------------- | --------- |
| `create-user --name` | Yes | IAM user name (1-64; not starting with a digit) | `alice` |
| `--description` | No | User/group description (0-255, restricted chars) | `"ops account"` |
| `--disabled` | No | Create the user disabled (`enabled=false`) | `--disabled` |
| `--group-id` / `--group-name` | No | Target group (id, or name resolved via list) | `ops` |
| `--create-group` | No | Create `--group-name` if it does not exist | `--create-group` |
| `--policy-id` | No | Identity policy id to attach (repeatable) | `<policy_id>` |
| `--policy-name` | No | Identity policy name, resolved to an id (repeatable) | `ReadOnlyAccess` |
| `authorize --user-id` / `--user-name` | One required | Existing user to authorize | `alice` |
| `--region` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--executor` | No | `auto` (default) / `cli` / `sdk` | `sdk` |
| `--json` | No | Emit full JSON instead of text | `--json` |
| `--dry-run` | No | Print the planned operations, execute nothing | `--dry-run` |
| `--confirm` | Yes (writes) | Confirm a mutation | `--confirm` |
| `--timeout` | No | Per-call timeout in seconds (default 60) | `90` |

## Idempotency and Error Handling

| Scenario | Behavior |
| ---------- | --------- |
| User already exists (HTTP 409) | Reused; result carries `reused=true` |
| Group name not found, `--create-group` set | Group is created, then used |
| Group name not found, no `--create-group` | Exit 2, `未找到用户组 ...` |
| Policy name matches multiple ids | Exit 1, asks to use `--policy-id` |
| Membership already exists | Reported as `already_member=true`, exit 0 |
| Policy already attached | Reported as `already_attached=true`, exit 0 |
| Invalid user name / description / id | Exit 2, `参数校验失败: ...` |
| Missing AK/SK (SDK path) | Exit 1, hint to set env vars (never paste in chat) |
| IAM 401 / 403 | Exit 1, hint to check credentials and IAM permissions |
| No backend (no CLI, no SDK) | Exit 1, `无可用执行后端` |
| Mutation without `--confirm` | Exit 2, `[CONFIRM] ...` |

Exit codes: `0` success / empty; `1` auth, backend or API error; `2` validation
or confirmation error.

## Capability Boundary (Out of Scope)

This skill **never** performs destructive or account-wide operations:

- ❌ Deleting or disabling IAM users.
- ❌ Deleting user groups.
- ❌ AK/SK rotation, password policy, MFA, agencies and delegation.

## Testing

Offline unit tests with a duck-typed fake backend (no credentials, no network):

```bash
cd skills/security/iam/huawei-cloud-iam-user-manage
python3 -m unittest discover -s tests -v
```

Coverage: input validation, create-user id/name result, conflict-driven reuse,
group and policy name resolution (including ambiguity), authorization
composition, CLI command construction and noisy-output JSON parsing (including
the trailing-diagnostic case and error-code surfacing), the confirm gate, and
`main()` exit codes.

The SDK fallback is covered explicitly (`SdkBackendTests`), including a
regression guard that `IamRegion` is imported from
`huaweicloudsdkiam.v5.region.iam_region` (it is **not** exported from the
`huaweicloudsdkiam.v5` top level) and that `SdkBackend._build_client()` resolves
that import. These cases run only when `huaweicloudsdkiam` is installed (run
`python3 scripts/ensure_env.py` first); otherwise they are skipped.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service name** — the exact KooCLI title-case service name: `IAM`.
- **Operation name** — PascalCase, e.g. `CreateUserV5`, `AddUserToGroupV5`,
  `AttachUserPolicyV5`, `ListUsersV5`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`.
- **Simple parameter** — `--key=value`, e.g. `--name=alice`, `--enabled=true`.

## Reference Documents

| Document | Content |
| ---------- | --------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege IAM actions for creating users and authorizing them |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI + SDK installation, credential configuration and skill-quality-cli |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |