---
name: huawei-cloud-asm-fuzzy-list
description: |
  Query the list of Huawei Cloud ASM (Application Service Mesh) meshes
  belonging to the current tenant / project and fuzzy-match them by mesh name.
  Returns the mesh name (metadata.name), mesh id (metadata.uid), status phase
  and creation timestamp for every mesh whose name contains the given keyword
  (case-insensitive substring match, client-side). Uses the huaweicloudsdkasm
  Python SDK ListMeshes call (GET /v1/{project_id}/meshes). Read-only — never
  creates, modifies or deletes any mesh or related resource.
  Use this skill whenever the user wants to list/inspect the ASM meshes of the
  tenant or query the ASM name list with fuzzy matching, e.g. for mesh
  inventory, locating a mesh by name, daily inspection or troubleshooting.
  Triggers include: "query ASM list", "list ASM", "ASM name list",
  "ASM mesh list", "模糊查询ASM", "查询ASM列表", "ASM名称", "查询ASM网格列表",
  "list meshes", "查询服务网格", "服务网格列表", "ASM inventory",
  "find ASM mesh by name".
tags:
  - huawei-cloud
  - asm
  - list
  - mesh
  - query
---

# Huawei Cloud ASM List Skill

## Overview

This skill queries the list of **ASM (Application Service Mesh) meshes** under
the current Huawei Cloud tenant / project and fuzzy-matches them by **mesh
name**. It returns the matching meshes together with their key attributes: the
mesh name (`metadata.name`), mesh id (`metadata.uid`), status (`status.phase`)
and creation timestamp (`metadata.creation_timestamp`).

The ASM list API (`GET /v1/{project_id}/meshes`) returns **all** meshes of the
project and has **no server-side name filter**. Therefore the skill performs a
**client-side fuzzy match**: it lists all meshes and keeps only those whose
name contains the requested keyword (case-insensitive substring match).

**Architecture:**

```text
Agent → huaweicloudsdkasm.v1 AsmClient.list_meshes() → Huawei Cloud ASM API (GET /v1/{project_id}/meshes)
         ↘ client-side fuzzy filter on metadata.name → matched meshes
```

**API used (verified from SDK `_http_info`):**

| Operation | SDK Method | API Path |
|-----------|------------|----------|
| List meshes | `AsmClient.list_meshes()` | `GET /v1/{project_id}/meshes` |

Region endpoint (from SDK `AsmRegion`): `cn-north-4` →
`https://asm.cn-north-4.myhuaweicloud.com`. Note: the ASM service currently
supports **only** the `cn-north-4` region — `AsmRegion.value_of()` rejects any
other region id.

**Applicable Scenarios:**

- ASM inventory: "list all ASM meshes of this tenant" or "show me the ASM name list"
- Locate a mesh by name: "find the mesh whose name contains 'prod'"
- Daily inspection: snapshot of all meshes and their status phase
- Troubleshooting: check a mesh's status by fuzzy name lookup

> **能力边界（Capability Boundary）：**
> 本 Skill **仅查询 ASM 网格列表并按名称模糊匹配**。不创建/删除/修改网格，
> 也不查询/操作网格内的服务、虚拟服务、目标规则、网关等子资源。若用户询问
> "创建/删除/更新ASM网格" 或 "查询网格内资源" 等，请明确告知本 Skill 不提供
> 该能力。

## Prerequisites

1. **Python 3.8+** with the Huawei Cloud Python SDK installed:

   ```bash
   pip3 install huaweicloudsdkasm
   ```

2. **Authentication credentials** — `HUAWEICLOUD_SDK_AK` and
   `HUAWEICLOUD_SDK_SK` environment variables (or the alternate
   `HUAWEI_ACCESS_KEY`/`HUAWEI_SECRET_KEY`, or `HWC_AK`/`HWC_SK`). Credentials
   are read from the environment only — never hardcode them.
3. **IAM permissions** — the account needs the mesh list permission. See
   `references/iam-policies.md`.
4. A region where the tenant owns ASM meshes; specify it with
   `AsmRegion.value_of(...)`.

## Workflow

1. **Identify the intent** — Confirm the user wants to list ASM meshes and, if
   given, the fuzzy name keyword (the substring to match).
2. **Confirm region** — Default `cn-north-4`; let the user override with
   another region if needed.
3. **Run the query** — Call `list_meshes()` through the SDK to fetch all meshes.
4. **Apply the fuzzy filter** — If a keyword is provided, keep only meshes
   whose `metadata.name` contains the keyword (case-insensitive). If no keyword
   is given, list all meshes.
5. **Present the results** — Show name, id, status phase and creation
   timestamp for each matching mesh.
6. **Handle errors** — If the call fails:
   - **Region not supported** (`region_id ... is not in the following supported
     regions`): the ASM service only supports `cn-north-4` — use that region.
   - **Credentials/permissions** (`APIGW.0802 forbidden` or a 403): the account
     lacks permission — verify the IAM policy grants the mesh list action.
   - **SDK not installed**: `pip3 install huaweicloudsdkasm`.

## Core Commands

This skill runs through the **Python SDK** because the KooCLI (`hcloud`) does
not support the ASM service. Use the following pattern:

### List all ASM meshes of the project (compact fields)

```bash
python3 -c "
import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkasm.v1 import AsmClient, ListMeshesRequest
from huaweicloudsdkasm.v1.region.asm_region import AsmRegion

client = AsmClient.new_builder() \\
    .with_credentials(BasicCredentials(os.environ['HUAWEICLOUD_SDK_AK'],
                                       os.environ['HUAWEICLOUD_SDK_SK'])) \\
    .with_region(AsmRegion.value_of('cn-north-4')) \\
    .build()
resp = client.list_meshes(ListMeshesRequest())
for m in resp.items or []:
    print(m.metadata.name, m.metadata.uid, m.status.phase)
"
```

### Fuzzy-match meshes by name (case-insensitive substring)

```bash
python3 -c "
import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkasm.v1 import AsmClient, ListMeshesRequest
from huaweicloudsdkasm.v1.region.asm_region import AsmRegion

keyword = 'prod'   # the fuzzy name keyword
client = AsmClient.new_builder() \\
    .with_credentials(BasicCredentials(os.environ['HUAWEICLOUD_SDK_AK'],
                                       os.environ['HUAWEICLOUD_SDK_SK'])) \\
    .with_region(AsmRegion.value_of('cn-north-4')) \\
    .build()
resp = client.list_meshes(ListMeshesRequest())
matched = [m for m in (resp.items or []) if keyword.lower() in (m.metadata.name or '').lower()]
for m in matched:
    print(m.metadata.name, m.metadata.uid, m.status.phase, m.metadata.creation_timestamp)
print('matched', len(matched))
"
```

> **Note:** `ListMeshesRequest` accepts no parameters. Fuzzy matching is done
> client-side on `metadata.name`. An empty `items` array (or no matches) means
> the tenant has no meshes matching in that region.

## Parameter Confirmation（参数确认）

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `{region}` | No | Huawei Cloud region. **Only `cn-north-4` is supported by the ASM service** (default `cn-north-4`) | `cn-north-4` |
| `{keyword}` | No | Fuzzy name substring to match (case-insensitive). Empty = list all meshes | `prod` |

> **Note:** The ASM service supports **only** the `cn-north-4` region; passing
> any other region id to `AsmRegion.value_of()` raises a `KeyError`. If the
> user does not provide a keyword, the skill lists **all** meshes of the
> project. If a keyword is provided, only meshes whose name contains it are
> returned.

## Output Format（输出格式）

Each mesh is printed on one line as:

```text
<mesh_name> <mesh_id> <status_phase> <creation_timestamp>
```

- `mesh_name` — `metadata.name`
- `mesh_id` — `metadata.uid`
- `status_phase` — `status.phase` (e.g. `available`)
- `creation_timestamp` — `metadata.creation_timestamp`

When a fuzzy keyword is used, the output ends with `matched <N>` where N is the
number of matching meshes. An empty list (or `matched 0`) is a valid result and
means no mesh matches in the region.

## Notes（注意事项）

- The ASM list API returns **all** meshes of the project; the name filter is
  applied client-side and is **case-insensitive substring** matching.
- The ASM service supports **only** the `cn-north-4` region.
- This skill is strictly read-only: it never creates, modifies or deletes any
  mesh.

## Verification Method（验证方法）

1. **SDK availability**: `python3 -c "from huaweicloudsdkasm.v1 import AsmClient, ListMeshesRequest; print('SDK OK')"`
2. **Live list**: run the Core Commands snippet above and confirm a line per mesh
   (or `total meshes: 0` when the tenant has no meshes).
3. **Fuzzy match**: filter with a keyword and confirm `matched N`; a keyword with
   no matches must return `matched 0` without error.
4. **Read-only assertion**: the skill only issues `GET /v1/{project_id}/meshes`.

See `references/verification-method.md` for the full procedure.

## Best Practices（最佳实践）

- Always pass the region explicitly; only `cn-north-4` is supported by ASM.
- Prefer a keyword when the tenant owns many meshes — the filter runs client-side.
- Keep AK/SK in environment variables (`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`);
  never embed credentials in the conversation or files.

## KooCLI Command Format Standard

This skill is **SDK-based** — the KooCLI (`hcloud`) has no ASM service (the
service name `ASM` is rejected by the CLI with `[USE_ERROR]Unsupported
service: ASM`). All operations are performed via the `huaweicloudsdkasm`
Python SDK. There are therefore no `hcloud <Service> <Operation>` commands to
document here.

## Reference Documents

- [IAM Policies](references/iam-policies.md) — Least-privilege IAM permissions
- [CLI Installation Guide](references/cli-installation-guide.md) — SDK and authentication setup
- [Verification Method](references/verification-method.md) — How to verify the skill works
- [Dataflow Diagram](references/dataflow-diagram.md) — Request flow diagram
- [Acceptance Criteria](references/acceptance-criteria.md) — Acceptance test checklist
