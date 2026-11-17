# KooCLI Installation & Credential Guide

## Install KooCLI

Official quick start: https://support.huaweicloud.com/qs-hcli/hcli_02_003.html

```bash
# Linux/macOS
curl -sSL https://cn-north-4-res.hcccloud.com/cli/latest/install.sh -o install.sh
bash install.sh
hcloud version
```

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
pip install huaweicloudsdkcore huaweicloudsdkvpc
# or, bundled helper:
python3 scripts/ensure_env.py
```

The SDK reads credentials from the environment (`HUAWEI_ACCESS_KEY` /
`HUAWEI_SECRET_KEY`, or `HW_*` / `HWC_*` variants) — never from chat or literals.

The VPC REST path is `/v1/{project_id}/vpcs`, so the SDK fallback also needs a
**project id**: pass `--project-id` or set `HUAWEICLOUD_SDK_PROJECT_ID` /
`HUAWEI_PROJECT_ID`. The KooCLI path resolves it from the profile
automatically.

## Used by this skill

```bash
hcloud VPC ListVpcs --cli-region=cn-north-4 --limit=100
```

The script wraps exactly this call (with marker paging) and, when empty,
still emits a valid header-only Markdown table.

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.

## skill-quality-cli (quality telemetry)

Every `hcloud` command built by this skill is wrapped with
`skill-quality-cli run --skill-name huawei-cloud-vpc-export-markdown -- ` on the
script execution path (enforced in code). The wrapper emits quality telemetry
and is installed idempotently:

```bash
# Idempotent ready check (auto-installs skill-quality-cli if absent)
bash scripts/ensure_cli.sh

# Fail-closed manual installer
bash scripts/install_cli.sh

# Manual upgrade (no auto-upgrade)
skill-quality-cli upgrade

# Disable telemetry reporting
export SKILL_QUALITY_REPORT=0
```