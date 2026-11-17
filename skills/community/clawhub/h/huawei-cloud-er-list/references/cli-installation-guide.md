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
pip install huaweicloudsdkcore huaweicloudsdker
```

The SDK reads credentials from the environment (`HUAWEI_ACCESS_KEY` /
`HUAWEI_SECRET_KEY`, or `HW_*` / `HWC_*` variants) — never from chat or literals.

The ER REST paths are under `/v3/{project_id}/enterprise-router/...`, so the SDK
fallback also needs a **project id**: pass `--project-id` or set
`HUAWEICLOUD_SDK_PROJECT_ID` / `HUAWEI_PROJECT_ID`. The KooCLI path resolves it
from the profile automatically.

## Used by this skill

```bash
hcloud ER ListEnterpriseRouters --cli-region=cn-north-4 --limit=100
hcloud ER ShowEnterpriseRouter --cli-region=cn-north-4 --er_id=<er-id>
hcloud ER ListVpcAttachments --cli-region=cn-north-4 --er_id=<er-id> --limit=100
hcloud ER ListRouteTables --cli-region=cn-north-4 --er_id=<er-id> --limit=100
```

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.

## skill-quality-cli (telemetry)

The generated skill ships the same quality-reporting helper as the creator:

```bash
bash scripts/ensure_cli.sh      # idempotent: installs skill-quality-cli if absent
bash scripts/install_cli.sh     # fail-closed manual installer (offline / checksum path)
```

- Every hcloud command documented in this skill is intended to be wrapped as
  `skill-quality-cli run --skill-name huawei-cloud-er-list -- hcloud ...`.
- Upgrade manually with `skill-quality-cli upgrade` (no auto-upgrade).
- Disable telemetry with `SKILL_QUALITY_REPORT=0`.