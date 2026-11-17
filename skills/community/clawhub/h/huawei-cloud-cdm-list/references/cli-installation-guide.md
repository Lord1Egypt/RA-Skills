# Installation & Authentication — huawei-cloud-cdm-list

This skill supports two execution backends, in this order:

1. **KooCLI (`hcloud`)** — the primary path.
2. **`huaweicloudsdkcdm` (Python SDK)** — automatic fallback when `hcloud` is
   not installed.

## 1. Install KooCLI (hcloud)

```bash
# Linux (x86_64 example; pick the package for your platform)
curl -LO https://cli.dev.huaweicloud.com/koolci/hcloud-linux-amd64-latest.zip
unzip hcloud-linux-amd64-latest.zip
chmod +x hcloud
sudo mv hcloud /usr/local/bin/
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
# Optional: pin the project (otherwise the SDK resolves it via IAM per region)
# export HUAWEICLOUD_SDK_PROJECT_ID="<project-id>"
# Temporary credentials (optional):
# export HUAWEICLOUD_SDK_SECURITY_TOKEN="<temporary-token>"
```

The script reads AK/SK only from the whitelisted environment variables
(`HUAWEICLOUD_SDK_AK` / `CLOUD_SDK_AK` / `HUAWEI_ACCESS_KEY` / `HW_ACCESS_KEY` /
`HWC_ACCESS_KEY` and the matching `*_SK` names, plus optional
`HUAWEICLOUD_SDK_PROJECT_ID` / `CLOUD_SDK_PROJECT_ID`); it never reads, echoes
or stores secrets itself.

## 3. Install the Python SDK (SDK fallback dependency)

```bash
python3 scripts/ensure_env.py
# equivalent:
pip install huaweicloudsdkcore huaweicloudsdkcdm
```

The fallback authenticates with `BasicCredentials(ak, sk[, project_id])`;
when the project id is omitted the SDK queries IAM and resolves it for the
target region automatically (requires the IAM list-projects permission for the
principal, which standard read-only users have).

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
hcloud CDM ListClusters --cli-region=cn-north-4
hcloud CDM ShowClusterDetail --cli-region=cn-north-4 --cluster_id=<uuid>
python3 scripts/list_cdm_clusters.py --help
```

A `403 没有操作权限` response means the IAM principal lacks the read permission
(`cdm:cluster:list` / `cdm:cluster:get`, see `references/iam-policies.md`); it
is not an installation problem.
