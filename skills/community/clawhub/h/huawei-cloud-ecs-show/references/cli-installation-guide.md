# KooCLI Installation & Credential Guide

## Install KooCLI

Official quick start: https://support.huaweicloud.com/qs-hcli/hcli_02_003.html

```text
# Linux/macOS
curl -sSL https://cn-north-4-res.hcccloud.com/cli/latest/install.sh -o install.sh
bash install.sh
hcloud version
```

## Configure credentials (out-of-band only)

The skill script never reads, echoes, or stores AK/SK — authentication is fully
delegated to the active KooCLI profile. Configure it in your own terminal:

```text
# interactive; never paste AK/SK into an agent chat
hcloud configure
```

Verify (read-only, no secrets echoed):

```text
hcloud configure list
```

## SDK fallback (optional)

When hcloud is not installed, the script falls back to the official SDK:

```bash
pip install huaweicloudsdkcore huaweicloudsdkecs
```

The SDK fallback reads credentials from the environment
(`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK` or the `HW_*` / `HUAWEI_*`
variants) — never from chat or literals. Provide `--project-id` if the SDK
cannot resolve the project from the credential profile.

## Used by this skill

```text
hcloud ECS ShowServer --cli-region=cn-north-4 --server_id=<instance_id>
```

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.

## skill-quality-cli (optional quality telemetry)

Some skills in this repository ship a local quality-CLI wrapper. This skill does
not require it: `show_ecs.py` uses only the Python standard library plus the
optional `huaweicloudsdkecs` fallback. If a quality CLI is present in your
environment, wrap reads with it; otherwise run the script directly.