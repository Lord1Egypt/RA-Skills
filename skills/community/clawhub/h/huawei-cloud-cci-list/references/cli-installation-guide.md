# KooCLI Installation & Credential Guide

## Install KooCLI

Official quick start: https://support.huaweicloud.com/qs-hcli/hcli_02_003.html

```bash
# Linux/macOS
curl -sSL https://cn-north-4-res.huaweicloud.com/cli/latest/install.sh -o install.sh
bash install.sh
hcloud version
```

CCI has **no public Python SDK** (`huaweicloudsdkcci` is not published on PyPI),
so KooCLI is the only supported execution backend for this skill.

## Configure credentials (out-of-band only)

The skill script never reads, echoes, or stores AK/SK — authentication is fully
delegated to the active KooCLI profile. Configure it in your own terminal:

```bash
hcloud configure  # interactive; never paste AK/SK into an agent chat
```

Verify (read-only, no secrets echoed):

```bash
hcloud configure list
```

## skill-quality-cli wrapper (mandatory)

Every `hcloud` call made while using this skill must be wrapped so telemetry is
collected and bare CLI calls are avoided:

```bash
skill-quality-cli run --skill-name huawei-cloud-cci-list -- hcloud CCI ListCoreV1Namespace --cli-region=cn-north-4
```

`skill-quality-cli` is provided by the agent runtime; it can also be ensured
idempotently by `bash scripts/ensure_cli.sh` (auto-install when absent) or the
fail-closed manual installer `bash scripts/install_cli.sh`. To upgrade it
manually run `skill-quality-cli upgrade` (no auto-upgrade); set
`SKILL_QUALITY_REPORT=0` to disable telemetry reporting.

## Used by this skill

```bash
skill-quality-cli run --skill-name huawei-cloud-cci-list -- hcloud CCI ListCoreV1Namespace --cli-region=cn-north-4 --limit=100
skill-quality-cli run --skill-name huawei-cloud-cci-list -- hcloud CCI ListCoreV1PodForAllNamespaces --cli-region=cn-north-4 --limit=100
skill-quality-cli run --skill-name huawei-cloud-cci-list -- hcloud CCI ListCoreV1NamespacedPod --cli-region=cn-north-4 --namespace=default --limit=100
```

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.