# KooCLI Installation & Credential Guide

## Install KooCLI

Official quick start: https://support.huaweicloud.com/qs-hcli/hcli_02_003.html

```bash
# Linux/macOS
curl -sSL https://cn-north-4-res.hcccloud.com/cli/latest/install.sh -o install.sh
bash install.sh
hcloud version
```

This skill was verified against **KooCLI 7.2.12** (also compatible with 7.3.x).

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
hcloud DDS ListInstances --cli-region=cn-north-4 --limit=100 --offset=0
hcloud DDS ListInstances --cli-region=cn-north-4 --name=dds-demo
hcloud DDS ListInstances --cli-region=cn-north-4 --cli-mode=AKSK --mode=Sharding
hcloud DDS ListInstances --cli-region=cn-north-4 --tags=env=prod
```

Notes:

- Leading `*` in `--name` switches to fuzzy matching (`--name=*demo`);
  without it the match is exact — the script forwards `*` when `--fuzzy` is set.
- There is **no server-side `--status` parameter** on this API; the script's
  `--status` filter is applied client-side.
- **`mode` parameter collision**: KooCLI reserves `--mode` for the
  authentication mode (`AKSK|ecsAgency|SSO|AssumeRole`). When the API `mode`
  filter is used, pass the system parameter as `--cli-mode=<auth mode>` and
  the API parameter as `--mode=<Sharding|ReplicaSet|Single>`. KooCLI then
  prefers `--cli-mode` for the system parameter and treats the other as the
  API parameter. The script does this automatically (auth mode defaults to
  `AKSK`; set `DDS_LIST_CLI_MODE` to the active profile mode, e.g. `SSO`).
  Without `--cli-mode`, KooCLI prompts interactively and fails with
  `[USE_ERROR]EOF` in non-interactive runs.

## SDK fallback (optional)

When hcloud is not installed, the script falls back to the official SDK. The
bundled helper installs it on demand (mirrors first, then the official index):

```bash
python3 scripts/ensure_env.py            # check + install
python3 scripts/ensure_env.py --check    # check only (non-zero when missing)
python3 scripts/ensure_env.py --upgrade  # force upgrade
# or manually:
pip install huaweicloudsdkcore huaweicloudsdkdds
```

The fallback reads credentials from a fixed whitelist of environment variable
names — `HUAWEI_ACCESS_KEY` / `HUAWEI_SECRET_KEY` (or `HW_*` /
`HUAWEICLOUD_SDK_AK` / `HUAWEI_CLOUD_ACCESS_KEY` family) — never from chat or
literals, plus `HUAWEI_PROJECT_ID` / `HUAWEICLOUD_SDK_PROJECT_ID` for the
`/v3/{project_id}/instances` path. A temporary security token can be supplied
with `HUAWEI_SECURITY_TOKEN` / `HUAWEICLOUD_SDK_SECURITY_TOKEN`.

## REST fallback (standard library only)

When both hcloud and the SDK are missing, the script calls
`GET https://dds.<region>.myhuaweicloud.com/v3/{project_id}/instances`
directly, signing the request locally with AK/SK Signature V4
(`SDK-HMAC-SHA256`). No extra package is needed. The same whitelisted AK/SK,
project-id and security-token environment variables are used. This tier is
read-only (GET) and is covered by the offline unit tests (URL construction,
deterministic signature, security token, pagination, error mapping).

## skill-quality-cli (quality telemetry)

Every `hcloud` call in this skill must be wrapped with `skill-quality-cli run
--skill-name huawei-cloud-dds-list -- `. The CLI itself is installed by the
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
