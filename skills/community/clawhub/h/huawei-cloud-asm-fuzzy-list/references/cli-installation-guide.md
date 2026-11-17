# CLI Installation Guide — huawei-cloud-asm-fuzzy-list

> This skill is **SDK-based**. The KooCLI (`hcloud`) does not support the ASM
> service (`hcloud ASM` returns `[USE_ERROR]Unsupported service: ASM`), so no
> KooCLI profile is required. This guide covers installing the Python SDK and
> configuring authentication.

## Install the Huawei Cloud Python SDK for ASM

```bash
pip3 install huaweicloudsdkasm
```

The `huaweicloudsdkcore` package (credentials, client builder) is installed
automatically as a dependency.

## Configure Authentication (AK/SK)

The skill reads credentials from the environment. The recommended variables (in
priority order) are:

| Priority | Variable | Description |
|----------|----------|-------------|
| 1 | `HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK` | Primary AK/SK pair |
| 2 | `HUAWEI_ACCESS_KEY` / `HUAWEI_SECRET_KEY` | Alternative AK/SK pair |
| 3 | `HWC_AK` / `HWC_SK` | Alternative AK/SK pair |

Example:

```bash
export HUAWEICLOUD_SDK_AK=<your-access-key>
export HUAWEICLOUD_SDK_SK=<your-secret-key>
```

Never ask a user to paste their AK/SK into a conversation; have them set the
environment variables in their own terminal.

## Verify Installation

```bash
python3 -c "from huaweicloudsdkasm.v1 import AsmClient, ListMeshesRequest; print('SDK OK')"
```

## Minimal Working Example

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

## Region Endpoints

From the SDK `AsmRegion` definition:

| Region | Endpoint |
|--------|----------|
| `cn-north-4` | `https://asm.cn-north-4.myhuaweicloud.com` |

**Important:** the ASM service supports **only** the `cn-north-4` region. The
SDK `AsmRegion` class defines a single region, and `AsmRegion.value_of()` with
any other region id raises a `KeyError`. If a call fails with `APIGW.0802
forbidden` or a 403, verify the IAM policy grants the mesh list action rather
than switching regions.
