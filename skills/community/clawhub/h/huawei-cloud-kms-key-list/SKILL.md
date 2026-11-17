---
name: huawei-cloud-kms-key-list
description: |
  1. Query the Huawei Cloud KMS (Data Encryption Workshop / 数据加密服务) master
     keys (CMK) of the current account in one region, strictly read-only.
     Primary path: KooCLI `hcloud KMS ListKeys` (read-only POST
     /v1.0/{project_id}/kms/list-keys); when hcloud is unavailable or fails,
     fall back to the official `huaweicloudsdk` KMS SDK (huaweicloudsdkkms).
  2. Output modes: a compact list of 别名 | 密钥ID | 状态 (default), a full
     8-column table with --table (密钥ID / 别名 / 状态 / 密钥用途 / 密钥类型 /
     轮转周期 / 创建时间 / region), and --json for the raw merged response body.
  3. Filters: --alias (exact match, --fuzzy for substring), --key-id, --state
     (client-side; 1-5 or enabled/disabled/pending-deletion/pending-import/
     pending-activation), --region (default cn-north-4).
  4. Pagination: --limit 1-200 with automatic paging driven by the response
     fields truncated / next_marker / total.
  5. Built-in read-only guard: any mutating intent (create / enable / disable /
     schedule-deletion / cancel-deletion / rotate / create-grant / delete /
     update ...) is rejected before execution with exit code 1 — this skill
     never writes to KMS.
  6. Explicit error hints for an empty key list, 403 / insufficient IAM
     permission, missing credentials, missing hcloud, and KooCLI [USE_ERROR].
  7. Triggers include: "list KMS keys", "KMS 密钥列表", "查询KMS密钥",
     "密钥盘点", "CMK 列表", "密钥轮转状态", "KMS 巡检", "kms key inventory",
     "list cmk", "华为云KMS密钥".
  8. Offline unit tests cover routing, pagination, output modes, filters, error
     classification and the write-intent guard (mock hcloud subprocess + fake
     SDK client).
tags: [huawei-cloud, kms, security, readonly, koo-cli]
---

# Huawei Cloud KMS Key List

## Overview

Inventory the KMS master keys (CMK) of a tenant region through KooCLI
`hcloud KMS ListKeys`, returning alias, key ID, state, usage, type, rotation
status and creation time. Aimed at key inventory (密钥盘点), compliance review
(合规核对), daily patrol (日常巡检), and as a pre-query step for other KMS tasks
that need a key ID.

| Operation | REST path | Method | Purpose |
| --------- | --------- | ------ | ------- |
| `KMS ListKeys` | `/v1.0/{project_id}/kms/list-keys` | POST | list all CMKs of the region |
| `KMS ShowKeyRotationStatus` | `/v1.0/{project_id}/kms/get-key-rotation-status` | POST | rotation interval of one CMK |

Architecture:

```text
agent → python3 scripts/list_kms_keys.py [--region=<region>] [--table|--json]
      → hcloud KMS ListKeys --cli-region=<region> --limit=<n> [--marker=<m>]
        └─ (hcloud missing / failed) → huaweicloudsdk KMS SDK ListKeys
      → Huawei Cloud KMS OpenAPI → parsed JSON → compact list / table / JSON
```

Key properties:

- **Read-only by design** — only `ListKeys` and `ShowKeyRotationStatus` are
  ever constructed; a write-intent guard inspects `--action`, `--alias` and
  `--key-id` and rejects mutating intent (create / enable / disable /
  schedule-deletion / cancel-deletion / rotate / create-grant ...) before any
  command runs. Write operations (if ever needed) require a dedicated
  write-capable skill and explicit user confirmation.
- **CLI first, SDK fallback** — `hcloud` is the primary path; when it is
  missing or fails with a transient/backend error the script falls back to
  `huaweicloudsdkkms` (SDK credentials come from
  `HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK` only). `403` and credential
  errors never fall back — they are reported as-is.
- **Complete inventory** — pagination loops on `truncated` / `next_marker`
  until the last page, with `--max-pages` as a safety cap; `--key_spec=ALL`
  is always passed so asymmetric keys are included (the API defaults to
  `AES_256`, which would hide RSA/EC/SM2 keys).
- **Rotation period** — `ListKeys` only returns `key_rotation_enabled`; the
  numeric period (30-365 days) comes from the read-only
  `ShowKeyRotationStatus`, queried per rotation-enabled key for `--table`
  (cap 50 lookups; `--no-rotation-detail` disables it, failures degrade to
  `开启` instead of aborting).
- **No files written** — everything goes to stdout; secrets are delegated to
  the KooCLI profile or environment.
- **Offline-testable** — all code paths are covered by unit tests that mock
  the hcloud subprocess and inject a fake SDK client.

Out of scope: creating / enabling / disabling / deleting / scheduling
deletion of keys, rotation changes, grant management, cross-region
aggregation, and key-material export.

> **Dependency**: Quality telemetry is collected automatically via
> skill-quality-cli (installed by scripts/ensure_cli.sh if absent).

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Missing hcloud is not fatal: the script falls back to the SDK.
2. **Active credential profile** — configure credentials out-of-band (run the
   KooCLI configure command in your terminal, or export
   `HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`). Never paste AK/SK into chat;
   the script never reads, echoes, or stores secrets itself.
3. **IAM permission** — read-only `kms:cmk:list` (key list) and
   `kms:cmk:getRotation` (rotation period); least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** — standard library only for the CLI path; the SDK fallback
   additionally needs `huaweicloudsdkcore` + `huaweicloudsdkkms`.
5. **Outbound HTTPS** access to `*.myhuaweicloud.com`.
6. **`skill-quality-cli`** — ensured by `bash scripts/ensure_cli.sh` (idempotent,
   skips if present). Upgrade with `skill-quality-cli upgrade`; disable
   telemetry with `SKILL_QUALITY_REPORT=0`.

## Workflow

1. **Confirm the region** (default `cn-north-4`) — KMS keys are region-scoped.
2. **Run the list script** with the desired output mode and filters.
3. **Read the result** — compact list for a quick look, `--table` for the
   full inventory columns, `--json` for downstream tooling.
4. **Handle the empty / error cases** per the Edge Cases table (the script
   prints an explicit, actionable hint for each of them).

## Core Commands

> **⚠️ Mandatory: every `hcloud` command in this skill MUST be wrapped with
> `skill-quality-cli run --skill-name huawei-cloud-kms-key-list -- ` — bare
> `hcloud` calls are strictly forbidden.**

### List keys (default compact output)

```bash
skill-quality-cli run --skill-name huawei-cloud-kms-key-list -- python3 scripts/list_kms_keys.py --region={region}
```

Under the hood the skill runs:

```
`hcloud KMS ListKeys --cli-region=<region> --limit=<n> --key_spec=ALL [--marker=<m>]`
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--cli-region` | Yes (auto) | Region, filled by the script |
| `--limit` | No | Page size 1-200 (default 100) |
| `--key_spec` | No | Always `ALL` so asymmetric keys are listed |
| `--marker` | No | Next-page marker taken from `next_marker` |

### Full table

```bash
skill-quality-cli run --skill-name huawei-cloud-kms-key-list -- python3 scripts/list_kms_keys.py --table --region={region}
```

Renders 密钥ID | 别名 | 状态 | 密钥用途 | 密钥类型 | 轮转周期 | 创建时间 | region.
Rotation-enabled keys additionally trigger one read-only rotation-status call
each (cap 50); add `--no-rotation-detail` to skip those lookups.

### Raw JSON

```bash
skill-quality-cli run --skill-name huawei-cloud-kms-key-list -- python3 scripts/list_kms_keys.py --json --region={region}
```

Returns the merged raw response: `keys`, `key_details`, `truncated`,
`next_marker`, `total` (+ `region`).

### Filtering

```bash
skill-quality-cli run --skill-name huawei-cloud-kms-key-list -- python3 scripts/list_kms_keys.py --alias my-key --region={region}
skill-quality-cli run --skill-name huawei-cloud-kms-key-list -- python3 scripts/list_kms_keys.py --alias prod --fuzzy --region={region}
skill-quality-cli run --skill-name huawei-cloud-kms-key-list -- python3 scripts/list_kms_keys.py --state enabled --region={region}
skill-quality-cli run --skill-name huawei-cloud-kms-key-list -- python3 scripts/list_kms_keys.py --key-id 0d0466b0 --region={region}
```

### SDK fallback (no hcloud)

```bash
skill-quality-cli run --skill-name huawei-cloud-kms-key-list -- python3 scripts/list_kms_keys.py --backend sdk --region={region}
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--region` | No | Huawei Cloud region (`--cli-region`) | `cn-north-4` |
| `--table` | No | Full 8-column table | flag |
| `--json` | No | Raw merged response JSON | flag |
| `--alias` | No | Exact alias filter (fuzzy with `--fuzzy`) | `my-key` |
| `--fuzzy` | No | Substring match for `--alias` | flag |
| `--key-id` | No | Key ID filter (substring) | `0d0466b0-e727-...` |
| `--state` | No | `1`-`5` or `enabled` / `disabled` / `pending-deletion` / `pending-import` / `pending-activation` | `enabled` |
| `--limit` | No | Page size, 1-200 (default `100`) | `100` |
| `--max-pages` | No | Pagination safety cap (default `50`) | `10` |
| `--no-rotation-detail` | No | Skip per-key rotation-status lookups | flag |
| `--backend` | No | `auto` (default) / `cli` / `sdk` | `sdk` |
| `--timeout` | No | Per-call timeout in seconds (default `60`) | `60` |
| `--action` | No | Only `list` is accepted; other values are refused by the guard | `list` |

Key state codes: `1` 待激活 / `2` 启用 / `3` 禁用 / `4` 计划删除 / `5` 待导入.

## Edge Cases

| Scenario | Behavior (exit code) |
|----------|----------------------|
| No keys in the region | `当前区域无 KMS 密钥（区域: <region>）。` + region hint (0) |
| Filters match nothing | `未找到匹配的 KMS 密钥（区域: <region>）。` (0) |
| IAM permission missing (403) | `无权限访问 KMS 密钥列表（403）…kms:cmk:list / kms:cmk:getRotation` (1) |
| Missing / invalid AK/SK | Credential hint with `HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK` and profile guidance (1) |
| hcloud not installed | SDK fallback in `auto` mode; explicit install hint in `--backend cli` (1) |
| KooCLI `[USE_ERROR]` | Parameter/usage hint pointing at `--region` / `--limit` (1) |
| Write intent (`--alias create-me`, `--action rotate`, …) | Read-only guard message, no cloud call (1) |
| `--limit` out of 1-200 / invalid `--state` | Argument validation message (1) |

## References

- [references/iam-policies.md](references/iam-policies.md) — least-privilege read-only IAM policy
- [references/cli-installation-guide.md](references/cli-installation-guide.md) — KooCLI install & profile setup
- [references/verification-method.md](references/verification-method.md) — how to verify the skill
- [references/dataflow-diagram.md](references/dataflow-diagram.md) — request/data flow
- [references/acceptance-criteria.md](references/acceptance-criteria.md) — acceptance checklist

## KooCLI Command Format Standard

```bash
skill-quality-cli run --skill-name huawei-cloud-kms-key-list -- hcloud <service> <Operation> --cli-region=<region> [--key=value ...]
```

| Feature | Description | Example |
|---------|-------------|---------|
| Service name | `KMS` (verified from `hcloud KMS ListKeys --help`) | `KMS` |
| Operation name | PascalCase | `ListKeys`, `ShowKeyRotationStatus` |
| Region parameter | `--cli-region=<value>` | `--cli-region=cn-north-4` |
| Simple parameter | `--key=value` | `--limit=100` |

Service and parameter names are taken verbatim from
`hcloud KMS ListKeys --help` / `hcloud KMS ShowKeyRotationStatus --help` —
never invented.

## Security Notes

- Strictly read-only: only `ListKeys` / `ShowKeyRotationStatus` are executed.
- No key material, plaintext, or secret is retrieved, printed, or written.
- Credentials stay in the KooCLI profile / environment; the script never
  reads, echoes, or persists them.