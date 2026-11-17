# KooCLI Installation & Credential Guide

This skill requires **hcloud (KooCLI)**; the SDK fallback additionally requires
`huaweicloudsdkcore` + `huaweicloudsdkcbr`.

## Install hcloud

```text
# Linux/macOS quick start
curl -sSL https://cn-north-4-res.hcccloud.com/cli/latest/install.sh -o install.sh
bash install.sh
hcloud version
```

Official quick start: https://support.huaweicloud.com/qs-hcli/hcli_02_003.html

## Configure credentials (out-of-band only)

The skill script never reads, echoes, or stores AK/SK. Configure credentials in
your own terminal (never paste AK/SK into an agent chat):

```text
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
pip install huaweicloudsdkcore huaweicloudsdkcbr
```

The SDK fallback reads credentials from the environment (e.g. `HW_ACCESS_KEY` /
`HW_SECRET_KEY`, `HUAWEI_ACCESS_KEY` / `HUAWEI_SECRET_KEY`, or
`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`) — never from chat or literals. If a
project ID is required by the target account, export it as
`HUAWEICLOUD_SDK_PROJECT_ID`.

## quality-cli (telemetry)

The skill ships the same quality-reporting wrapper as the rest of the Huawei
Cloud skill family:

```bash
# Idempotent: skips when skill-quality-cli is already usable
bash scripts/ensure_cli.sh
# Manual install / repair
bash scripts/install_cli.sh
# Upgrade (manual only — no auto-upgrade)
skill-quality-cli upgrade
# Disable telemetry reporting
export SKILL_QUALITY_REPORT=0
```

Every hcloud call in this skill must be wrapped as
`skill-quality-cli run --skill-name huawei-cloud-cbr-vault-list -- hcloud ...`.

## Verify installation

```text
hcloud version
hcloud CBR ListVault --cli-region=cn-north-4 --limit=1 --offset=0
```

A successful run prints a JSON document with a `vaults` array and a `count`
field. A `403` indicates a permission problem (see
[iam-policies.md](iam-policies.md)); a credential error means `hcloud configure`
has not been run.

## Used by this skill

```text
hcloud CBR ListVault --cli-region=cn-north-4 --limit=100 --offset=0
```

The CBR `ListVault` request accepts `limit` / `offset` plus native server-side
filters (`name` / `status` / `object_type` / `protect_type` /
`enterprise_project_id` / `id` (array) / `cloud_type` / `policy_id` /
`resource_ids` / `availability_zone`); the script passes the supported ones
through and also re-filters the rendered rows locally. The vault ID filter is
emitted as `--id.1=<vault_id>`. The underlying REST path is
`GET /v3/{project_id}/vaults` (official `huaweicloudsdkcbr` v1
`_list_vault_http_info`).