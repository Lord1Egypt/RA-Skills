# Verification Method — huawei-cloud-asm-fuzzy-list

## 1. Prerequisites Verification

```bash
# SDK installed?
python3 -c "from huaweicloudsdkasm.v1 import AsmClient, ListMeshesRequest; print('SDK OK')"

# Credentials present?
[ -n "$HUAWEICLOUD_SDK_AK" ] && [ -n "$HUAWEICLOUD_SDK_SK" ] && echo "AK/SK OK"
```

## 2. Functional Verification (SDK)

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
print('total meshes:', len(resp.items or []))
for m in resp.items or []:
    print(m.metadata.name, m.metadata.uid, m.status.phase, m.metadata.creation_timestamp)
"
```

Expected: a line per mesh with `name`, `uid`, `phase` and creation timestamp.
An empty list (or `total meshes: 0`) means the tenant has no ASM meshes in the
`cn-north-4` region (the only region supported by the ASM service).

> **Region constraint:** The ASM service supports **only** `cn-north-4`.
> Passing another region id to `AsmRegion.value_of()` raises a `KeyError`
> (`region_id ... is not in the following supported regions of service 'Asm'`).

## 3. Fuzzy Name Matching Verification

```bash
# Pick a keyword that should match at least one mesh name, e.g. 'a'
python3 -c "
import os
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkasm.v1 import AsmClient, ListMeshesRequest
from huaweicloudsdkasm.v1.region.asm_region import AsmRegion

keyword = 'a'
client = AsmClient.new_builder() \\
    .with_credentials(BasicCredentials(os.environ['HUAWEICLOUD_SDK_AK'],
                                       os.environ['HUAWEICLOUD_SDK_SK'])) \\
    .with_region(AsmRegion.value_of('cn-north-4')) \\
    .build()
resp = client.list_meshes(ListMeshesRequest())
matched = [m for m in (resp.items or []) if keyword.lower() in (m.metadata.name or '').lower()]
for m in matched:
    print(m.metadata.name, m.metadata.uid, m.status.phase)
print('matched', len(matched))
"
```

Expected: `matched N` where N is the number of meshes whose name contains the
keyword. A keyword that matches nothing (e.g. an unlikely string) must return
`matched 0` without error — this validates the empty-result path.

## 4. Automated Test Cases

The test cases are stored in `templates/test-vars.json`. Run them with:

```bash
bash scripts/test-cli-commands.sh {skill-path} --executor sdk
```

## 5. Read-Only Assertion

Verify that the skill only issues the `GET /v1/{project_id}/meshes` call. It
must never invoke `create_mesh`, `delete_mesh`, `show_mesh` or any other
mutation/management operation.
