# KooCLI Installation & Credential Guide

## Install KooCLI

Official quick start: https://support.huaweicloud.com/qs-hcli/hcli_02_003.html

```bash
# Linux / macOS (one-shot installer; use the arm64 tarball on aarch64 hosts)
curl -sSL https://cn-north-4-hdn-koocli.obs.cn-north-4.myhuaweicloud.com/cli/latest/hcloud_install.sh -o ./hcloud_install.sh
bash ./hcloud_install.sh -y
hcloud version
```

KooCLI downloads the service metadata on first use; run a `<Service> --help`
once (e.g. `hcloud CodeArtsRepo --help`) so the operation list is cached.

## Configure credentials (out-of-band only)

The skill script never reads, echoes or stores AK/SK — authentication is fully
delegated to the active KooCLI profile. Configure it in your own terminal:

```bash
hcloud configure   # interactive; NEVER paste AK/SK into an agent chat
```

Verify (read-only, no secrets echoed):

```bash
hcloud configure list
```

## SDK fallback (optional)

When hcloud is not installed, the script falls back to the official SDK for the
selected resource. Install only the package(s) you need:

```bash
pip install huaweicloudsdkcore huaweicloudsdkprojectman   # projects
pip install huaweicloudsdkcore huaweicloudsdkcodeartsrepo # repos
pip install huaweicloudsdkcore huaweicloudsdkcodeartspipeline  # pipelines
pip install huaweicloudsdkcore huaweicloudsdkcodeartsdeploy    # deploy-tasks
```

The SDK fallback reads AK/SK explicitly from standard environment variables
(`HUAWEI_*` / `HW_*` / `HWC_*` AK/SK markers) because the SDK's
`BasicCredentials` performs no environment auto-discovery — never from chat or
literals.

## Used by this skill

```bash
hcloud ProjectMan ListProjectsV4 --cli-region=cn-north-4 --limit=100 --offset=0
hcloud CodeArtsRepo ListProjectRepositories --cli-region=cn-north-4 --project_id=<project-id> --limit=100 --offset=0
hcloud CodeArtsPipeline ListPipelines --cli-region=cn-north-4 --project_id=<project-id> --limit=100 --offset=0
hcloud CodeArtsDeploy ListDeployTasks --cli-region=cn-north-4 --project_id=<project-id> --page=1 --size=100
```

If hcloud reports a credential problem, the script surfaces it as
`缺少 AK/SK 凭证` with this reference attached.
