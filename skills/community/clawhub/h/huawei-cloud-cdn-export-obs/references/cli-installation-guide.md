# KooCLI & obsutil Installation and Credential Guide

## Install KooCLI

Official quick start: https://support.huaweicloud.com/qs-hcli/hcli_02_003.html

```bash
# Linux/macOS
curl -sSL https://cn-north-4-res.hcccloud.com/cli/latest/install.sh -o install.sh
bash install.sh
hcloud version
```

The `hcloud OBS` sub-command is obsutil-backed and ships with KooCLI.

## Configure credentials (out-of-band only)

The skill script never reads, echoes, or stores AK/SK — authentication is fully
delegated to the active tool profiles. Configure them in your own terminal:

```bash
hcloud configure          # CDN (KooCLI profile); interactive, never paste AK/SK into chat
hcloud obs config         # OBS module (obsutil config: AK/SK/endpoint)
```

Verify (read-only, no secrets echoed):

```bash
hcloud configure list
```

## SDK fallback (optional)

When hcloud is not installed, the script falls back to the official SDKs:

```bash
pip install huaweicloudsdkcore huaweicloudsdkcdn huaweicloudsdkobs
# or: python3 scripts/ensure_env.py
```

The SDK fallbacks read AK/SK from whitelisted environment variables (e.g.
`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`, or `HUAWEI_ACCESS_KEY` /
`HUAWEI_SECRET_KEY`, `HW_*`) — never from chat or literals.

## Used by this skill

```bash
hcloud CDN ListDomains --cli-region=cn-north-4 --page_size=100 --page_number=1
hcloud OBS cp /tmp/cdn_domains.json obs://my-bucket/inventory/cdn_domains.json -e=obs.cn-north-4.myhuaweicloud.com
hcloud OBS stat obs://my-bucket/inventory/cdn_domains.json -e=obs.cn-north-4.myhuaweicloud.com
```

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.