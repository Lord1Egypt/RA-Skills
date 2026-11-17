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

When hcloud is not installed, the script falls back to the official SDK. BSS is
a global service, so the SDK uses `GlobalCredentials` + `with_endpoints`:

```bash
pip install huaweicloudsdkcore huaweicloudsdkbss
```

The SDK reads credentials from the environment / cached auth — never from chat
or literals. Set `HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK` out-of-band (the
script auto-scans `HUAWEI*` / `HW*` / `HWC*` AK/SK markers).

## Used by this skill

```bash
hcloud BSS ListSubCustomerCoupons --cli-region=cn-north-1 --offset=0 --limit=100
```

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached. BSS is a global service — use
`cn-north-1`.
