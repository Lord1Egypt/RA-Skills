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
pip install huaweicloudsdkcore huaweicloudsdkcdn
```

The SDK reads credentials from the environment (`HUAWEI_ACCESS_KEY` /
`HUAWEI_SECRET_KEY`, or `HW_*` / `HWC_*` variants) — never from chat or literals.

## Used by this skill

```bash
hcloud CDN ListDomains --cli-region=cn-north-4 --page_size=100 --page_number=1
```

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.