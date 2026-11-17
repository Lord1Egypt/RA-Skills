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

Confirm the WAF service is available:

```bash
hcloud WAF --help
```

The operations used by this skill are `WAF ListHost` and
`WAF ListCompositeHosts`.

## 2. Credential configuration (out-of-band)

**Never** paste AK/SK into a chat / command line. Configure credentials outside
this session, then re-run the skill.

Recommended (KooCLI interactive profile):

```bash
hcloud configure            # enter AK/SK in your own terminal
hcloud configure list       # verify the profile (read-only)
```

Alternative (environment variables, read by hcloud):

```bash
# Set these in your shell profile OUTSIDE this session (SK entered silently).
export HUAWEICLOUD_SDK_AK="<your-access-key-id>"
read -rs HUAWEICLOUD_SDK_SK; export HUAWEICLOUD_SDK_SK
export HUAWEICLOUD_SDK_REGION="cn-north-4"
# Temporary credentials (optional):
# export HUAWEICLOUD_SDK_SECURITY_TOKEN="<temporary-token>"
```

The script never reads, echoes, or stores credentials — authentication is
delegated entirely to the hcloud profile / environment.

## 3. skill-quality-cli (quality telemetry)

This skill carries quality-reporting capability:

```bash
bash scripts/ensure_cli.sh          # idempotent; installs skill-quality-cli if absent
bash scripts/install_cli.sh         # fail-closed manual installer
skill-quality-cli upgrade           # manual upgrade (no auto-upgrade)
```

Disable the telemetry report with `export SKILL_QUALITY_REPORT=0`.