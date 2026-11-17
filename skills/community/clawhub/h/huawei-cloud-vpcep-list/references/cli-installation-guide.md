# KooCLI Installation & Credential Guide

## Install KooCLI

Official quick start: https://support.huaweicloud.com/qs-hcli/hcli_02_003.html

```bash
# Linux/macOS
curl -sSL https://cn-north-4-res.hcccloud.com/cli/latest/install.sh -o install.sh
bash install.sh
hcloud version
```

Verified working version for this skill: KooCLI 7.3.12.

## Configure credentials (out-of-band only)

The skill script never reads, echoes, or stores AK/SK — authentication is fully
delegated to the active KooCLI profile. Configure it in your own terminal:

```bash
hcloud configure  # interactive; never paste AK/SK into an agent chat
```

Verify (read-only, no secrets echoed):

```bash
hcloud configure list
```

## SDK fallback (optional)

When hcloud is not installed, the script falls back to the official SDK:

```bash
pip install huaweicloudsdkcore huaweicloudsdkvpcep
```

The SDK reads credentials from the environment (`HUAWEI_ACCESS_KEY` /
`HUAWEI_SECRET_KEY`, or `HW_*` / `HUAWEICLOUD_SDK_*` variants) — never from chat
or literals.

The VPCEP REST paths are `/v1/{project_id}/vpc-endpoints` and
`/v1/{project_id}/vpc-endpoint-services`, so the SDK fallback also needs a
**project id**: pass `--project-id` or set `HUAWEICLOUD_SDK_PROJECT_ID` /
`HUAWEI_PROJECT_ID`. The KooCLI path resolves it from the profile
automatically.

SDK package note: `huaweicloudsdkvpcep` 3.1.x exposes the VPCEP **v3 API**
under the Python module path `huaweicloudsdkvpcep.v1` (the module suffix is the
package's internal API group, not the public API version).

## Used by this skill

```bash
hcloud VPCEP ListEndpoints --cli-region=cn-north-4 --limit=100 --offset=0
hcloud VPCEP ListEndpointService --cli-region=cn-north-4 --limit=100 --offset=0
hcloud VPCEP ListServicePublicDetails --cli-region=cn-north-4 --limit=100 --offset=0
```

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.
