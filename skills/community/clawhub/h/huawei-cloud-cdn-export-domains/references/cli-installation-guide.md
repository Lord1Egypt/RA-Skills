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

## Region note (CDN ListDomains)

CDN is a global service. KooCLI advertises the read-only `ListDomains` operation
for the regions **`cn-north-1`** and **`ap-southeast-1`** (verified via
`hcloud CDN ListDomains --help`: `Supported regions: cn-north-1, ap-southeast-1`).
Pass one of those via `--region` / `--cli-region`; the skill defaults to
`cn-north-1`.

## SDK fallback (optional)

When hcloud is not installed, the script falls back to the official SDK:

```bash
pip install huaweicloudsdkcore huaweicloudsdkcdn
# or, bundled helper:
python3 scripts/ensure_env.py
```

CDN is a global service, so the SDK client is authenticated with
`GlobalCredentials(ak=..., sk=...)`. The SDK reads credentials from the
environment (`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`, `HUAWEI_ACCESS_KEY` /
`HUAWEI_SECRET_KEY`, or `HW_*` variants) — never from chat or literals.

## Used by this skill

```bash
hcloud CDN ListDomains --cli-region=cn-north-1 --page_size=100 --page_number=1
```

The script wraps exactly this call (with `page_number` paging) and, when empty,
still emits a valid header-only export file.

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.

## skill-quality-cli (quality telemetry)

Every `hcloud` command built by this skill is wrapped with
`skill-quality-cli run --skill-name huawei-cloud-cdn-export-domains -- ` on the
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