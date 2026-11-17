# KooCLI + obsutil + openpyxl Installation & Credential Guide

This skill requires **hcloud (KooCLI)** with its **obsutil** OBS module (primary
query path), the **huaweicloudsdkobs** Python SDK (fallback path) and
**openpyxl** (for .xlsx export).

## Quick dependency setup (Python side)

Run the bundled environment script from the skill directory to install anything
missing automatically (openpyxl + huaweicloudsdkcore + huaweicloudsdkobs):

```bash
python3 scripts/ensure_env.py
```

Or install manually:

```bash
pip install openpyxl huaweicloudsdkcore huaweicloudsdkobs
```

> **TL;DR for most users:** openpyxl and the SDK are typically the only missing
> pieces. `ensure_env.py` handles them (mirror + official PyPI fallback, both
> with a timeout).

## Install hcloud

```bash
# Linux/macOS quick start
curl -sSL https://cn-north-4-res.hcccloud.com/cli/latest/install.sh -o install.sh
bash install.sh
hcloud version
```

Official quick start: https://support.huaweicloud.com/qs-hcli/hcli_02_003.html

## Configure OBS credentials (obsutil, out-of-band only)

> **Important:** the `hcloud OBS` module does **not** inherit the KooCLI account
> credentials. It reads AK/SK/endpoint from the obsutil config file
> (`~/.obsutilconfig`).

The skill script never reads, echoes, or stores AK/SK. Configure obsutil in your
own terminal (never paste AK/SK into an agent chat):

```bash
hcloud obs config -i=<YourAK> -k=<YourSK> -e=obs.<Region>.myhuaweicloud.com
```

Example (cn-north-4):

```bash
hcloud obs config -i=<YourAK> -k=<YourSK> -e=obs.cn-north-4.myhuaweicloud.com
```

Common endpoints:

| Region | Endpoint |
| -------- | ---------- |
| cn-north-4 | `obs.cn-north-4.myhuaweicloud.com` |
| cn-east-3 | `obs.cn-east-3.myhuaweicloud.com` |
| cn-south-1 | `obs.cn-south-1.myhuaweicloud.com` |
| cn-southwest-2 | `obs.cn-southwest-2.myhuaweicloud.com` |

## SDK fallback (optional)

When hcloud is not installed, the script falls back to the official SDK:

```bash
pip install huaweicloudsdkcore huaweicloudsdkobs
```

The SDK fallback reads credentials from the environment (e.g. `HW_ACCESS_KEY` /
`HW_SECRET_KEY`, `HUAWEI_ACCESS_KEY` / `HUAWEI_SECRET_KEY`, or
`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`) — never from chat or literals.

## Verify installation

```bash
hcloud version
hcloud OBS ls -limit=1
python3 -c "import openpyxl; print('openpyxl', openpyxl.__version__)"
```

A successful `hcloud OBS ls` prints `Bucket number is: N` followed by `obs://`
bucket names. If it prints `Please set ak, sk and endpoint in the
configuration file!`, the obsutil credentials are not configured — run
`hcloud obs config` as above.

## Used by this skill

```bash
# CLI query path
hcloud OBS ls -limit=1000 -e=obs.cn-north-4.myhuaweicloud.com

# Script query + export
python3 scripts/list_obs_buckets_excel.py --region cn-north-4 --output /tmp/obs.xlsx
```

Note: `hcloud OBS` is obsutil-backed — there is no PascalCase
`hcloud OBS ListBuckets` command, and the OBS module does not accept
`--cli-region` (use `-e=<endpoint>`). If hcloud reports a credential problem,
the script surfaces it as `缺少 AK/SK 凭证` with this reference attached.