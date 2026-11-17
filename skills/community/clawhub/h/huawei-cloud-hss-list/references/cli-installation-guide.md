# KooCLI Installation & Credential Guide

## Install KooCLI

Official quick start: https://support.huaweicloud.com/qs-hcli/hcli_02_003.html

| OS | Download |
| -- | -------- |
| Linux amd64 | https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-linux-amd64.tar.gz |
| Linux arm64 | https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-linux-arm64.tar.gz |

```bash
# Linux/macOS
curl -sSL https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/huaweicloud-cli-linux-amd64.tar.gz -o koocli.tar.gz
tar -xzf koocli.tar.gz
sudo mv hcloud /usr/local/bin/
hcloud version
```

## Configure credentials (out-of-band only)

The skill script never reads, echoes, or stores AK/SK — authentication is fully
delegated to the active KooCLI profile. Configure it in your own terminal with
the interactive wizard (never paste AK/SK into an agent chat):

```bash
hcloud configure  # interactive (recommended)
hcloud configure list  # verify a valid profile exists
```

Never paste AK/SK into an agent chat. The HSS REST path
`/v5/{project_id}/host-management/hosts` requires a project ID; KooCLI resolves
it automatically from the region in the active profile.

## Verify

```bash
hcloud HSS ListHostStatus --cli-region=cn-north-4 --limit=10 --offset=0
```

If the user has no HSS permission you will see a `common.01010013` / `403` IAM
error — the command is valid, the IAM role needs `hss:host:listHostStatus`.

See `references/iam-policies.md` for the least-privilege policy.

## skill-quality-cli (quality telemetry)

Every `hcloud` command in this skill must be wrapped with
`skill-quality-cli run --skill-name huawei-cloud-hss-list --`. The wrapper
emits quality telemetry and is installed idempotently:

```bash
# Idempotent ready check (auto-installs skill-quality-cli if absent)
bash scripts/ensure_cli.sh

# Fail-closed manual installer
bash scripts/install_cli.sh

# Manual upgrade (no auto-upgrade)
skill-quality-cli upgrade

# Disable telemetry reporting
export SKILL_QUALITY_REPORT=0
```

If `skill-quality-cli` cannot be installed (network / checksum / platform),
do not fall back to a bare `hcloud` call — resolve the CLI first.