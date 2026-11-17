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

When hcloud is not installed, the script falls back to the official SDK. Self-heal
the dependency with:

```bash
python3 scripts/ensure_env.py
# or manually:
pip install huaweicloudsdkcore huaweicloudsdkbss
```

The SDK reads credentials from an explicit whitelist of fixed environment
variable names (`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`, or
`HUAWEI_ACCESS_KEY` / `HUAWEI_SECRET_KEY`, or `HW_ACCESS_KEY` / `HW_SECRET_KEY`)
— never from chat or literals.

BSS is a **global** service, so the SDK fallback uses `GlobalCredentials` +
`with_endpoints(["https://bss.myhuaweicloud.com"])` (not `BasicCredentials` +
`with_region`). No project id is required.

## Region

BSS is a global service; use a BSS-reachable region such as `cn-north-1` (the
skill default). The catalog itself is not region-scoped.

## Used by this skill

```bash
hcloud BSS ListServiceTypes --cli-region=cn-north-1 --limit=100 --offset=0
```

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.