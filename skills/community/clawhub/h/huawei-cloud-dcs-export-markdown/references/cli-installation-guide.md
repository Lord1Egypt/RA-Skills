# CLI / SDK Installation & Credential Guide

## 1. Python dependencies (SDK fallback)

The Markdown export itself is **pure standard library** (plain text) — no
third-party package is needed to render it. The only runtime dependency is the
official Huawei Cloud SDK used by the fallback path when `hcloud` is absent:

```bash
python3 scripts/ensure_env.py          # idempotent: installs only what is missing
# or manually:
pip install huaweicloudsdkcore huaweicloudsdkdcs
```

- `huaweicloudsdkcore` — SDK bootstrap / credentials / region catalog.
- `huaweicloudsdkdcs` — Distributed Cache Service (DCS) SDK (v2).

## 2. KooCLI (hcloud) — optional primary path

The skill tries KooCLI first; when `hcloud` is absent (or the operation is not
exposed by your KooCLI version), it falls back to the SDK automatically.

Install KooCLI following the official quick-start:
<https://support.huaweicloud.com/qs-hcli/hcli_02_003.html>

```bash
# Linux/macOS
curl -sSL https://cn-north-4-res.hcccloud.com/cli/latest/install.sh -o install.sh
bash install.sh
hcloud version
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
# project id (required by the SDK fallback path /v2/{project_id}/instances):
export HUAWEI_PROJECT_ID="<your-project-id>"
```

Accepted AK/SK environment variable families (whitelisted, read by name only):
`HW_ACCESS_KEY` / `HW_SECRET_KEY`, `HUAWEI_ACCESS_KEY` / `HUAWEI_SECRET_KEY`,
`HUAWEICLOUD_SDK_AK` / `HUAWEICLOUD_SDK_SK`, `HUAWEI_CLOUD_ACCESS_KEY` /
`HUAWEI_CLOUD_SECRET_KEY`, `HWC_ACCESS_KEY` / `HWC_SECRET_KEY`.

Alternative (KooCLI profile, used by the CLI path):

```bash
hcloud configure        # interactive, enter AK/SK in your own terminal
hcloud configure list   # verify the profile (read-only)
```

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.

## 4. Used by this skill

```bash
hcloud DCS ListInstances --cli-region=cn-north-4 --limit=100 --offset=0
hcloud DCS ListInstances --cli-region=cn-north-4 --name=cache --status=RUNNING
```

The REST path is `GET /v2/{project_id}/instances` (verbatim from the
`huaweicloudsdkdcs` v2 client `_list_instances_http_info` `resource_path`).

## 5. skill-quality-cli (quality telemetry)

This skill carries the same quality-reporting capability as the skill creator:

```bash
bash scripts/ensure_cli.sh          # idempotent; installs skill-quality-cli if absent
bash scripts/install_cli.sh         # fail-closed manual installer
skill-quality-cli upgrade           # manual upgrade (no auto-upgrade)
```

Disable the telemetry report with `export SKILL_QUALITY_REPORT=0`.

`scripts/list_dcs_export_markdown.py` wraps every `hcloud` CLI call
automatically (not left to the agent), executing it as:

```bash
skill-quality-cli run --skill-name huawei-cloud-dcs-export-markdown -- hcloud DCS ListInstances --cli-region=cn-north-4 --limit=1
```

When `skill-quality-cli` is not installed the CLI path degrades to bare `hcloud`
(no telemetry) and the SDK fallback still applies; install it with
`bash scripts/ensure_cli.sh` to keep reporting. An explicit
`DCS_EXPORT_MARKDOWN_HCLOUD_BIN` override (offline mock / verification) is run
verbatim.