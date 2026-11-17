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
pip install huaweicloudsdkcore huaweicloudsdkbms
```

The SDK fallback reads credentials from `HUAWEI_*` / `HW_*` / `HWC_*` AK/SK
environment variables — never from chat or literals.

## Used by this skill

```bash
hcloud BMS ListBareMetalServers --cli-region=cn-north-4 --limit=100 --offset=1
```

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.
