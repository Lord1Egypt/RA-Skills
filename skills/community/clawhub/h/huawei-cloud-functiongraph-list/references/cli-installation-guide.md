# KooCLI Installation & Credential Guide

## Install KooCLI

Official quick start: <https://support.huaweicloud.com/qs-hcli/hcli_02_003.html>

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

Alternative: use the standard credential environment variables out-of-band
(fill in real values in your own shell, never in chat):

```bash
export HUAWEICLOUD_SDK_AK="<your-access-key-id>"
read -rs HUAWEICLOUD_SDK_SK; export HUAWEICLOUD_SDK_SK
export HUAWEICLOUD_SDK_REGION="cn-north-4"
```

## SDK fallback (optional)

When hcloud is not installed, the script falls back to the official SDK:

```bash
pip install huaweicloudsdkcore huaweicloudsdkfunctiongraph
```

The SDK fallback reads credentials from an explicit whitelist of standard
AK/SK environment variable names (`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`,
`HW_ACCESS_KEY` / `HW_SECRET_KEY`, `HUAWEI_ACCESS_KEY` / `HUAWEI_SECRET_KEY`,
`HW_AK` / `HW_SK`, `HWC_ACCESS_KEY` / `HWC_SECRET_KEY`, ...) — each variable is
read by its exact name, never by iterating the whole environment — and never
from chat or literals.

## skill-quality-cli (quality telemetry)

`skill-quality-cli` is the mandated wrapper for every concrete hcloud command in
this skill. It is installed idempotently by:

```bash
bash scripts/ensure_cli.sh
```

or manually with `bash scripts/install_cli.sh`. It does **not** auto-upgrade;
upgrade explicitly with `skill-quality-cli upgrade`. Telemetry can be disabled
per-run with `SKILL_QUALITY_REPORT=0`.

## Used by this skill

```bash
hcloud functiongraph ListFunctions --cli-region=cn-north-4 --maxitems=400
```

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.
