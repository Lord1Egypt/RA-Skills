# KooCLI Installation & Credential Guide

## Install KooCLI

Official quick start: https://support.huaweicloud.com/qs-hcli/hcli_02_003.html

```bash
# Linux / macOS (one-shot installer; use the arm64 tarball on aarch64 hosts)
curl -sSL https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/hcloud_install.sh -o ./hcloud_install.sh
bash ./hcloud_install.sh -y
hcloud version
```

KooCLI downloads the service metadata on first use; run a `<Service> --help`
once (e.g. `hcloud CSE --help`) so the operation list is cached.

## Configure credentials (out-of-band only)

The skill script never reads, echoes or stores AK/SK — authentication is fully
delegated to the active KooCLI profile. Configure it in your own terminal:

```bash
hcloud configure   # interactive; NEVER paste AK/SK into an agent chat
```

Verify (read-only, no secrets echoed):

```bash
hcloud configure list
```

## SDK fallback (optional)

When hcloud is not installed, the script falls back to the official SDK:

```bash
pip install huaweicloudsdkcore huaweicloudsdkcse
```

The package exposes `list_engines` in module `huaweicloudsdkcse.v1`; it calls
the same v2 REST endpoint (`GET /v2/{project_id}/enginemgr/engines`). The SDK
fallback reads AK/SK explicitly from standard environment variables
(`HUAWEI_*` / `HW_*` / `HWC_*` AK/SK markers) because the SDK's
`BasicCredentials` performs no environment auto-discovery — never from chat or
literals.

```bash
# Out-of-band only; never paste the secret into a chat.
export HUAWEI_ACCESS_KEY="<your-access-key-id>"
read -rs HUAWEI_SECRET_KEY; export HUAWEI_SECRET_KEY
export HUAWEI_REGION="cn-north-4"
```

## Used by this skill

```bash
hcloud CSE ListEngines --cli-region=cn-north-4 --limit=100 --offset=0 --type=ALL
```

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.