# CLI / SDK Installation & Credential Guide

## 1. Python dependencies (SDK fallback)

The SDK fallback needs the official Huawei Cloud SDK packages:

```bash
python3 scripts/ensure_env.py          # idempotent: installs only what is missing
# or manually:
pip install huaweicloudsdkcore huaweicloudsdkces huaweicloudsdkeps
```

- `huaweicloudsdkcore` — SDK bootstrap / credentials / region catalog.
- `huaweicloudsdkces` — Cloud Eye (CES) management-plane SDK (v2).
- `huaweicloudsdkeps` — Enterprise Project Service (EPS) SDK (v1).

## 2. KooCLI (hcloud) — optional primary path

The skill tries KooCLI first; if the operation is not available in your KooCLI
version (or hcloud is absent), it falls back to the SDK automatically.

Install KooCLI following the official quick-start:
<https://support.huaweicloud.com/qs-hcli/hcli_02_003.html>

Verify the installation (read-only):

```bash
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

Accepted AK/SK environment variable families (whitelisted, read by name only):
`HW_ACCESS_KEY` / `HW_SECRET_KEY`, `HUAWEI_ACCESS_KEY` / `HUAWEI_SECRET_KEY`,
`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`, `HUAWEI_CLOUD_ACCESS_KEY` /
`HUAWEI_CLOUD_SECRET_KEY`, `HUAWEI_AK` / `HUAWEI_SK`, `HW_AK` / `HW_SK`,
`HWC_ACCESS_KEY` / `HWC_SECRET_KEY`.

Alternative (KooCLI profile, used by the CLI path):

```bash
hcloud configure        # interactive, enter AK/SK in your own terminal
hcloud configure list   # verify the profile (read-only)
```

## 4. REST fallback credentials (optional)

The token-based REST fallback is used only when neither CLI nor SDK is
available. It needs an IAM token and a project id:

```bash
export CES_EPS_TOKEN="<X-Auth-Token>"          # or HW_AUTH_TOKEN / HUAWEI_AUTH_TOKEN
export CES_EPS_PROJECT_ID="<project-id>"       # or HUAWEI_PROJECT_ID
```

## 5. skill-quality-cli (quality telemetry)

This skill carries the same quality-reporting capability as the skill creator:

```bash
bash scripts/ensure_cli.sh          # idempotent; installs skill-quality-cli if absent
bash scripts/install_cli.sh         # fail-closed manual installer
skill-quality-cli upgrade           # manual upgrade (no auto-upgrade)
```

Disable the telemetry report with `export SKILL_QUALITY_REPORT=0`.

`scripts/ces_eps_query.py` wraps every `hcloud` CLI call automatically (not left
to the agent), executing it as:

```bash
skill-quality-cli run --skill-name huawei-cloud-ces-eps-query -- hcloud CES ListAlarmRules --cli-region=cn-north-4 --limit=1
```

When `skill-quality-cli` is not installed the CLI path degrades to bare `hcloud`
(no telemetry) and the SDK/REST fallback still applies; install it with
`bash scripts/ensure_cli.sh` to keep reporting. An explicit
`CES_EPS_HCLOUD_BIN` override (offline mock / verification) is run verbatim.