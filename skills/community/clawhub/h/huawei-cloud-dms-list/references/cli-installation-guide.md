# KooCLI Installation & Credential Guide

## Install KooCLI

Official quick start: https://support.huaweicloud.com/qs-hcli/hcli_02_003.html

```bash
# Linux/macOS
curl -sSL https://cn-north-4-res.hcccloud.com/cli/latest/install.sh -o install.sh
bash install.sh
hcloud version
```

This skill was verified against **KooCLI 7.3.12**.

## Configure credentials (out-of-band only)

The skill script never reads, echoes or stores AK/SK — authentication is fully
delegated to the active KooCLI profile. Configure it in your own terminal:

```bash
hcloud configure  # interactive; never paste AK/SK into an agent chat
```

Alternatively export the standard environment variables before starting the
agent (the secret is entered silently, never in chat):

```bash
export HUAWEICLOUD_SDK_AK="<your-access-key-id>"
read -rs HUAWEICLOUD_SDK_SK; export HUAWEICLOUD_SDK_SK
export HUAWEICLOUD_SDK_REGION="cn-north-4"
# temporary credentials (optional):
# export HUAWEICLOUD_SDK_SECURITY_TOKEN="<temporary-token>"
```

Verify (read-only, no secrets echoed):

```bash
hcloud configure list
```

The KooCLI path resolves `project_id` from the active profile, so a separate
project-id setting is normally unnecessary.

## Used by this skill

```bash
hcloud Kafka    ListInstances         --cli-region=cn-north-4 --engine=kafka    --limit=50 --offset=0
hcloud RabbitMQ ListInstancesDetails  --cli-region=cn-north-4 --engine=rabbitmq --limit=50 --offset=0
hcloud Kafka    ListInstances         --cli-region=cn-north-4 --engine=kafka    --name=dms-demo --status=RUNNING
```

`hcloud DMS ListInstances` does **not** exist — KooCLI has no `DMS` service name
and answers `[USE_ERROR]Unsupported service: DMS`. Always use the engine service
(`Kafka` / `RabbitMQ`).

## SDK fallback (optional)

When hcloud is not installed, the script falls back to the official SDKs:

```bash
pip install huaweicloudsdkcore huaweicloudsdkkafka huaweicloudsdkrabbitmq
```

The fallback reads credentials from a fixed whitelist of environment variable
names — `HUAWEI_ACCESS_KEY` / `HUAWEI_SECRET_KEY` (or `HW_*` /
`HUAWEICLOUD_SDK_AK` / `HUAWEI_CLOUD_ACCESS_KEY` family) — never from chat or
literals, plus `HUAWEI_PROJECT_ID` / `HUAWEICLOUD_SDK_PROJECT_ID` for the
`/v2/{project_id}/instances` path. `huaweicloudsdkdms` is **not** the right
package for instance lists: its v2 client only exposes queue/consumer-group
operations and has no list-instances method.

## skill-quality-cli (quality telemetry)

Every `hcloud` call in this skill must be wrapped with `skill-quality-cli run
--skill-name huawei-cloud-dms-list -- `. The CLI itself is installed by the
bundled scripts:

```bash
bash scripts/ensure_cli.sh          # idempotent; installs skill-quality-cli if absent
bash scripts/install_cli.sh         # fail-closed manual install (checksum verified)
skill-quality-cli version
```

- Upgrade: run `skill-quality-cli upgrade` manually (there is no auto-upgrade).
- Disable telemetry: set `SKILL_QUALITY_REPORT=0`.

If `skill-quality-cli` cannot be installed, stop and report the failure instead
of falling back to bare `hcloud` calls.

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.