# KooCLI / SDK Installation & Credential Guide

## 1. Python dependencies (SDK fallback)

The Markdown export itself uses only the Python standard library. The official
SDK packages are needed only for the hcloud-absent fallback path:

```bash
python3 scripts/ensure_env.py          # idempotent: installs only what is missing
# or manually:
pip install huaweicloudsdkcore huaweicloudsdksfsturbo
```

- `huaweicloudsdkcore` — SDK bootstrap / credentials / region catalog.
- `huaweicloudsdksfsturbo` — SFS Turbo v1 SDK (`SFSTurboClient.list_shares`).

## 2. KooCLI (hcloud) — primary path

The skill tries KooCLI first; if hcloud is absent it falls back to the SDK
automatically.

Install KooCLI following the official quick-start:
<https://support.huaweicloud.com/qs-hcli/hcli_02_003.html>

```bash
# Linux/macOS
curl -sSL https://cn-north-4-res.hcccloud.com/cli/latest/install.sh -o install.sh
bash install.sh
hcloud version
hcloud configure list
```

## 3. Credential configuration (out-of-band)

**Never** paste AK/SK into a chat / command line. Configure credentials outside
this session, then re-run the skill.

Recommended (environment variables, read by the SDK fallback):

```bash
# Set these in your shell profile OUTSIDE this session (SK entered silently).
export HUAWEI_ACCESS_KEY="<your-access-key-id>"
read -rs HUAWEI_SECRET_KEY; export HUAWEI_SECRET_KEY
export HUAWEI_REGION="cn-north-4"
# Temporary credentials (optional):
# export HUAWEI_SECURITY_TOKEN="<temporary-token>"
```

Accepted AK/SK environment variable names (an explicit whitelist, read by name
only — the script never enumerates or harvests the whole environment):

`HW_ACCESS_KEY` / `HW_SECRET_KEY`,
`HUAWEI_ACCESS_KEY` / `HUAWEI_SECRET_KEY`,
`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`,
`HUAWEI_CLOUD_ACCESS_KEY` / `HUAWEI_CLOUD_SECRET_KEY`.

Alternative (KooCLI profile, used by the CLI path):

```bash
hcloud configure        # interactive, enter AK/SK in your own terminal
hcloud configure list   # verify the profile (read-only)
```

## 4. Used by this skill

```bash
hcloud SFSTurbo ListShares --cli-region=cn-north-4 --limit=200 --offset=0
```

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.

## 5. skill-quality-cli (quality telemetry)

This skill carries the same quality-reporting capability as the skill creator:

```bash
bash scripts/ensure_cli.sh          # idempotent; installs skill-quality-cli if absent
bash scripts/install_cli.sh         # fail-closed manual installer
skill-quality-cli upgrade           # manual upgrade (no auto-upgrade)
```

Disable the telemetry report with `export SKILL_QUALITY_REPORT=0`.

Every `hcloud` call must be wrapped, e.g.:

```bash
skill-quality-cli run --skill-name huawei-cloud-sfs-export-markdown -- hcloud SFSTurbo ListShares --cli-region=cn-north-4 --limit=1
```