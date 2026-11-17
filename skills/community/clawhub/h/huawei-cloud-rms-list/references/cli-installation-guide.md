# Installation & Authentication — huawei-cloud-rms-list

This skill supports two execution backends, in this order:

1. **KooCLI (`hcloud`)** — the primary path.
2. **`huaweicloudsdkrms` (Python SDK)** — automatic fallback when `hcloud` is
   not installed.

## 1. Install KooCLI (hcloud)

```bash
# Linux (x86_64 example; pick the package for your platform)
curl -LO https://cli.dev.huaweicloud.com/koolci/hcloud-linux-amd64-latest.zip
unzip hcloud-linux-amd64-latest.zip
chmod +x hcloud && sudo mv hcloud /usr/local/bin/
hcloud --version
```

Official guide: <https://support.huaweicloud.com/qs-hcli/hcli_02_003.html>

## 2. Configure credentials (out-of-band)

Configure the CLI profile in your own terminal — **never** paste AK/SK into chat
and never pass them as literal command-line arguments:

```bash
hcloud configure
hcloud configure list          # read-only verification (no secrets echoed)
```

Alternatively, provide environment variables that the SDK fallback reads:

```bash
# Set these in your shell profile OUTSIDE of this session.
export HUAWEICLOUD_SDK_AK="<your-access-key-id>"
read -rs HUAWEICLOUD_SDK_SK; export HUAWEICLOUD_SDK_SK
export HUAWEICLOUD_SDK_REGION="cn-north-4"
# Temporary credentials (optional):
# export HUAWEICLOUD_SDK_SECURITY_TOKEN="<temporary-token>"
```

The script reads AK/SK only from the whitelisted environment variables
(`HUAWEICLOUD_SDK_AK` / `HUAWEI_ACCESS_KEY` / `HW_ACCESS_KEY` / `HWC_ACCESS_KEY`
and the matching `*_SK` names); it never reads, echoes or stores secrets itself.

## 3. Install the Python SDK (SDK fallback dependency)

```bash
python3 scripts/ensure_env.py
# equivalent:
pip install huaweicloudsdkcore huaweicloudsdkrms
```

## 4. skill-quality-cli (telemetry, optional)

Every `hcloud` call on the script path is reported through `skill-quality-cli`
when it is available. It is optional — when missing, the call degrades to bare
`hcloud` and the read-only semantics are unchanged.

```bash
bash scripts/ensure_cli.sh              # idempotent ensure
bash scripts/install_cli.sh             # fail-closed manual install
skill-quality-cli upgrade               # manual upgrade (no auto-upgrade)
export SKILL_QUALITY_REPORT=0           # disable telemetry reporting entirely
```

## 5. Verify

```bash
hcloud RMS ListRegions --cli-region=cn-north-4
hcloud RMS ListProviders --cli-region=cn-north-4 --limit=5 --offset=1
hcloud RMS ListAllResources --cli-region=cn-north-4 --limit=1
```

A `RMS.00010006` / `not authorized with rms:resources:list` response means the IAM
principal lacks the read permission (see `references/iam-policies.md`); it is not
an installation problem.
