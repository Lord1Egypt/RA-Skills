# Verification Method

## Offline unit tests (primary, CI-safe)

```bash
cd skills/devtools/codearts/huawei-cloud-codearts-list
python3 -m unittest discover -s tests -v
```

- hcloud is replaced by a `subprocess.run` mock (`FakeRunner`) — no credentials,
  no network, deterministic.
- The SDK fallback is tested via a `list_resource_via_sdk` mock (no real SDK
  import, no network) and via direct `_build_sdk_request` assertions against
  lightweight fake request/query classes, so the request shapes are verified
  without any SDK installed.
- Cases cover: write-intent guard (selector values not scanned / operation
  whitelist), command construction for all four resources, JSON extraction
  (object / bare array / noise), failure classification (missing AK/SK / 403 /
  generic / `[USE_ERROR]` with rc=0), client-side name and status filtering,
  paging (total-aware, full-page, page-based), project auto-resolution (single /
  zero / several / explicit), SDK fallback (success / unavailable / missing
  credentials), rendering and all main() output modes (table / json / names-only
  / empty / error).

## Live verification (performed while authoring, 2026-10-19)

The four operations were executed read-only against a real tenant
(region `cn-north-4`) using KooCLI 7.3.12, confirming service codes, parameter
names and response shapes:

```bash
hcloud ProjectMan ListProjectsV4 --cli-region=cn-north-4 --limit=1 --offset=0
# -> {"projects":[{project_id,project_name,project_type,...}], "total": N}
hcloud CodeArtsRepo ListProjectRepositories --cli-region=cn-north-4 --project_id=<id> --limit=2 --offset=0
# -> [ {id,name,namespace,visibility,status,archived}, ... ]  (bare array)
hcloud CodeArtsPipeline ListPipelines --cli-region=cn-north-4 --project_id=<id> --limit=2 --offset=0
# -> {"offset":0,"limit":2,"total":N,"pipelines":[{pipeline_id,name,latest_run:{status},...}]}
hcloud CodeArtsDeploy ListDeployTasks --cli-region=cn-north-4 --project_id=<id> --page=1 --size=2
# -> {"result":[{id,name,state,project_name,...}],"total_num":N}
```

The end-to-end script (`scripts/list_codearts.py`) was then run against the same
tenant for all four resources in table / `--json` / `--names-only` modes,
including unique-project auto-resolution.

## KooCLI service/operation provenance

Service codes and operation names were verified against the live KooCLI metadata
(`hcloud <Service> --help` / `hcloud <Service> <Operation> --help`, KooCLI
7.3.12):

- `ProjectMan ListProjectsV4` (the `CodeHub` / `CodeArtsReq` service names are
  **not** supported by KooCLI; `ProjectMan` is).
- `CodeArtsRepo ListProjectRepositories` (the legacy `CodeHub` service is not
  supported).
- `CodeArtsPipeline ListPipelines`.
- `CodeArtsDeploy ListDeployTasks` (the legacy `CloudDeploy` service is not
  supported; `CodeArtsDeploy` is).

Parameter lists were read from the same `--help` output:
`ListProjectsV4` → `--limit` `--offset` `--search` `--project_type` `--archive`
`--query_type` `--sort`; `ListProjectRepositories` → `--project_id` `--limit`
`--offset` `--search` `--order_by` `--sort`; `ListPipelines` → `--project_id`
`--limit` `--offset` `--name` `--status.[N]` ...; `ListDeployTasks` →
`--project_id` `--page` `--size` (no name parameter).

## REST path provenance

REST paths come from the official SDK `_<op>_http_info` `resource_path`
metadata (the same paths the SDK fallback invokes):

- `huaweicloudsdkprojectman` v4 `_list_projects_v4_http_info` → `GET /v4/projects`
- `huaweicloudsdkcodeartsrepo` v4 `_list_project_repositories_http_info` →
  `GET /v4/projects/{project_id}/repositories`
- `huaweicloudsdkcodeartspipeline` v2 `_list_pipelines_http_info` →
  `POST /v5/{project_id}/api/pipelines/list`
- `huaweicloudsdkcodeartsdeploy` v2 `_list_deploy_tasks_http_info` →
  `GET /v2/{project_id}/tasks/list`

No endpoint was inferred from naming patterns.

## IAM action provenance

See [iam-policies.md](iam-policies.md) — the read actions were verified against
the live IAM authorization schema (`GetAuthorizationSchemaV5`) on 2026-10-19.
