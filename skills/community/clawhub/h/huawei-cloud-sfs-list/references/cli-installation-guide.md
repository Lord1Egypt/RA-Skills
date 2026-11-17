# KooCLI Installation & Credential Guide

This skill requires **hcloud (KooCLI)**; the SDK fallback additionally requires
`huaweicloudsdkcore` + `huaweicloudsdksfsturbo`.

## Install hcloud

```bash
# Linux/macOS quick start
curl -sSL https://cn-north-4-res.hcccloud.com/cli/latest/install.sh -o install.sh
bash install.sh
hcloud version
```

Official quick start: https://support.huaweicloud.com/qs-hcli/hcli_02_003.html

## Configure credentials (out-of-band only)

The skill script never reads, echoes, or stores AK/SK. Configure credentials in
your own terminal (never paste AK/SK into an agent chat):

```bash
# Interactive configuration (recommended); enter AK/SK at the prompt.
hcloud configure
# Verify the active profile (read-only, no secrets echoed):
hcloud configure list
```

Environment-variable alternative (fill in the values **outside** this session;
the secret is entered silently):

```bash
export HUAWEICLOUD_SDK_AK="<your-access-key-id>"
read -rs HUAWEICLOUD_SDK_SK; export HUAWEICLOUD_SDK_SK
export HUAWEICLOUD_SDK_REGION="cn-north-4"
```

## SDK fallback (optional)

When hcloud is not installed, the script falls back to the official SDK:

```bash
pip install huaweicloudsdkcore huaweicloudsdksfsturbo
```

The SDK fallback reads credentials from the environment (e.g. `HW_ACCESS_KEY` /
`HW_SECRET_KEY`, `HUAWEI_ACCESS_KEY` / `HUAWEI_SECRET_KEY`, or
`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`) — never from chat or literals.

## Verify installation

```bash
hcloud version
hcloud SFSTurbo ListShares --cli-region=cn-north-4 --limit=1 --offset=0
```

A successful run prints a JSON document with a `shares` array and a `count`
field. A `403` indicates a permission problem (see
[iam-policies.md](iam-policies.md)); a credential error means `hcloud
configure` has not been run.

## Used by this skill

```bash
hcloud SFSTurbo ListShares --cli-region=cn-north-4 --limit=200 --offset=0
```

The SFS `ListShares` request accepts only `limit` / `offset`; name / ID /
status / protocol filtering is applied by the script after the query. The
underlying REST path is `GET /v1/{project_id}/sfs-turbo/shares/detail`
(official `huaweicloudsdksfsturbo` v1 `_list_shares_http_info`).