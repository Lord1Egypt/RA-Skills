# KooCLI Installation & Credential Guide

## 1. Install KooCLI (hcloud)

This skill is driven through the Huawei Cloud KooCLI (`hcloud`). Install and
match versions following the official quick-start:

<https://support.huaweicloud.com/qs-hcli/hcli_02_003.html>

Verify the installation (read-only):

```bash
hcloud version
hcloud configure list
```

Upgrade KooCLI to the latest version (recommended once per environment):

```bash
hcloud update -y
```

Confirm the AAD service and the operation are available:

```bash
hcloud AAD --help
hcloud AAD ListProtectedIp --help
```

`hcloud AAD ListProtectedIp --help` must show `Method: GET`, `--cli-region` and
the optional query parameters `--ip`, `--limit`, `--offset`, `--package_id`,
`--policy_id`, `--tag`.

## 2. Credential configuration (out-of-band)

**Never** paste AK/SK into a chat / command line. Configure credentials outside
this session, then re-run the skill.

Recommended (KooCLI interactive profile):

```bash
hcloud configure            # enter AK/SK in your own terminal
hcloud configure list       # verify the profile (read-only)
```

Alternative (environment variables, read by hcloud and the SDK fallback):

```bash
# Set these in your shell profile OUTSIDE this session (SK entered silently).
export HUAWEICLOUD_SDK_AK="<your-access-key-id>"
read -rs HUAWEICLOUD_SDK_SK; export HUAWEICLOUD_SDK_SK
export HUAWEICLOUD_SDK_REGION="cn-north-4"
# Temporary credentials (optional):
# export HUAWEICLOUD_SDK_SECURITY_TOKEN="<temporary-token>"
```

The script never reads, echoes, or stores credentials — authentication is
delegated entirely to the KooCLI profile or the environment.

## 3. SDK fallback (optional)

Install the official SDK so the skill can still work when KooCLI is missing:

```bash
pip install huaweicloudsdkaad
```

The SDK fallback reads credentials from a fixed whitelist of environment
variable names (`HUAWEICLOUD_SDK_AK` / `HUAWEI_ACCESS_KEY` / `HW_ACCESS_KEY` /
`HWC_ACCESS_KEY` for the AK, the matching `*_SK` names for the secret key, and
`HUAWEICLOUD_SDK_SECURITY_TOKEN` / `HUAWEI_SECURITY_TOKEN` / `HW_SECURITY_TOKEN`
/ `HWC_SECURITY_TOKEN` for a temporary token); the environment is never
enumerated and KooCLI profile files are not read.
The supported SDK regions for AAD are `cn-north-4` and `ap-southeast-1`.

## 4. skill-quality-cli (quality telemetry)

This skill carries quality-reporting capability:

```bash
bash scripts/ensure_cli.sh          # idempotent; installs skill-quality-cli if absent
bash scripts/install_cli.sh         # fail-closed manual installer
skill-quality-cli upgrade           # manual upgrade (no auto-upgrade)
```

Disable the telemetry report with `export SKILL_QUALITY_REPORT=0`.