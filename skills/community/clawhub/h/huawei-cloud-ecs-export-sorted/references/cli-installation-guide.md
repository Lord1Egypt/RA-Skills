# KooCLI + SDK + openpyxl + skill-quality-cli Installation Guide

This skill requires **hcloud (KooCLI)** (primary query path), the
**huaweicloudsdkecs** Python SDK (fallback path), **openpyxl** (for `.xlsx`
export) and the **skill-quality-cli** (quality telemetry, required).

## skill-quality-cli (required)

The quality CLI wraps `hcloud` calls for telemetry. Ensure it is installed
(idempotent — skips when already present):

```bash
bash scripts/ensure_cli.sh
```

Manual / fail-closed install:

```bash
bash scripts/install_cli.sh
```

Verify:

```bash
command -v skill-quality-cli && skill-quality-cli version
```

- Upgrade: run `skill-quality-cli upgrade` manually (no auto-upgrade).
- Disable telemetry report: `export SKILL_QUALITY_REPORT=0`.

## Quick dependency setup (Python side)

Run the bundled environment script from the skill directory to install anything
missing automatically (openpyxl + huaweicloudsdkcore + huaweicloudsdkecs):

```bash
python3 scripts/ensure_env.py
```

Or install manually:

```bash
pip install openpyxl huaweicloudsdkcore huaweicloudsdkecs
```

> **TL;DR for most users:** openpyxl and the SDK are typically the only missing
> pieces. `ensure_env.py` handles them (mirror + official PyPI fallback, both
> with a timeout).

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
pip install huaweicloudsdkcore huaweicloudsdkecs
```

The SDK fallback reads credentials from the environment (e.g.
`HUAWEI_ACCESS_KEY` / `HUAWEI_SECRET_KEY`, `HW_ACCESS_KEY` / `HW_SECRET_KEY`, or
`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`) — never from chat or literals. Set
them out-of-band in your shell profile.

## Verify installation

```bash
hcloud version
skill-quality-cli run --skill-name huawei-cloud-ecs-export-sorted -- hcloud ECS ListServersDetails --cli-region=cn-north-4 --limit=1
python3 -c "import openpyxl; print('openpyxl', openpyxl.__version__)"
```

## Used by this skill

```bash
# CLI query path (wrapped with the quality CLI)
skill-quality-cli run --skill-name huawei-cloud-ecs-export-sorted -- hcloud ECS ListServersDetails --cli-region=cn-north-4 --limit=100 --offset=0

# Script query + local sort + export
python3 scripts/list_ecs_export_sorted.py --region cn-north-4 --sort-by created --order desc --output /tmp/ecs.xlsx
```

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.