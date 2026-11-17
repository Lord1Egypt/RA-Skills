# KooCLI (hcloud) Installation Guide

The skill's primary execution path is KooCLI (`hcloud`). The SDK fallback uses
`huaweicloudsdkbss` when `hcloud` is not installed.

## 1. Install KooCLI

```bash
# Linux / macOS (official installer)
curl -sSL https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/hcloud_install.sh -o hcloud_install.sh
bash hcloud_install.sh
hcloud --version
```

Refer to the official KooCLI documentation for the current download URL of your
platform. After installation, `hcloud` must be on `PATH`.

## 2. Configure credentials (out-of-band)

Configure the credential profile interactively in your terminal — the AK/SK is
stored locally by KooCLI and is **never** typed into the chat nor handled by the
skill:

```bash
hcloud configure init
```

A non-interactive profile can be selected with the standard KooCLI environment
variables. Set them in your shell profile (replace the values with your own;
never commit them):

```bash
export HUAWEICLOUD_SDK_AK=<your-access-key-id>
export HUAWEICLOUD_SDK_SK=<your-secret-access-key>
export HUAWEI_REGION=cn-north-1
```

> Never paste AK/SK into a chat message, an Issue comment, or a script. The skill
> reads only the active profile / environment and never echoes secrets.

## 3. Verify readiness

```bash
hcloud configure list            # shows the active profile / region
hcloud BSS CreatePartnerCoupons --cli-region=cn-north-1 --help
```

The `--help` output lists the exact parameter names for the issue-coupon
operation (the skill wraps exactly this call).

## 4. SDK fallback (optional)

```bash
pip install huaweicloudsdkcore huaweicloudsdkbss
```

When `hcloud` is absent, `send_voucher.py` transparently switches to
`huaweicloudsdkbss` v2 (`BssClient.create_partner_coupons`, global endpoint
`https://bss.myhuaweicloud.com`, `GlobalCredentials`). The SDK reads AK/SK from
the standard environment variables listed above.