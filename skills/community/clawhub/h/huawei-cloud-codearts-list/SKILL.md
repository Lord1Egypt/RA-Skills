---
name: huawei-cloud-codearts-list
description: |
  1. List Huawei Cloud CodeArts resources (read-only) in a tenant region/project
     through KooCLI, routing by --resource to the correct CodeArts list API:
     projects (ProjectMan ListProjectsV4, GET /v4/projects),
     repos (CodeArtsRepo ListProjectRepositories,
     GET /v4/projects/{project_id}/repositories),
     pipelines (CodeArtsPipeline ListPipelines,
     POST /v5/{project_id}/api/pipelines/list),
     deploy-tasks (CodeArtsDeploy ListDeployTasks,
     GET /v2/{project_id}/tasks/list). Automatic fallback to the matching
     official Python SDK (huaweicloudsdkprojectman / huaweicloudsdkcodeartsrepo /
     huaweicloudsdkcodeartspipeline / huaweicloudsdkcodeartsdeploy) when hcloud
     is not installed.
  2. Three output modes: full-field table (default, every returned field including
     名称/ID/状态/项目/可见性), --json (raw response items), and --names-only
     (compact name + ID inventory).
  3. Project-scoped resources (repos / pipelines / deploy-tasks) take
     --project-id; when omitted the skill auto-resolves it from the project list
     and proceeds only if exactly one project exists.
  4. Supports --name filtering (server-side where the API exposes it, client-side
     otherwise), client-side --status filtering, --region override (default
     cn-north-4) and automatic paging (offset/limit or page/size).
  5. Explicit error hints for empty lists (「无 CodeArts 资源」), 403 /
     insufficient IAM permission (「请检查 IAM 权限」), missing or invalid AK/SK
     credentials, and hcloud not installed.
  6. Built-in write-intent guard: any mutating intent (create / delete / update /
     run / start / stop / merge / batch ...) or any operation other than the four
     read-only List operations is rejected before execution — strictly read-only.
  7. Offline unit tests (mocked hcloud subprocess) cover routing, output modes,
     filters, paging, project auto-resolution, error scenarios, SDK fallback, and
     the write-intent guard.
  8. Triggers include: "list CodeArts projects", "CodeArts 项目列表",
     "查询CodeArts项目", "代码托管仓库列表", "CodeArts Repo 仓库列表",
     "流水线列表", "CodeArts Pipeline 列表", "部署任务列表",
     "CodeArts Deploy 任务", "CodeArts inventory", "DevOps 资产盘点",
     "华为云CodeArts列表".
tags: [huawei-cloud, codearts, devtools, readonly, koo-cli]
---

# Huawei Cloud CodeArts Resource List

## Overview

Query the read-only resource lists of Huawei Cloud CodeArts in a tenant region
through KooCLI, selecting the resource family with `--resource`:

| `--resource` | KooCLI service / operation | REST path | Scope |
| ------------ | -------------------------- | --------- | ----- |
| `projects` (default) | `ProjectMan` `ListProjectsV4` | `GET /v4/projects` | region |
| `repos` | `CodeArtsRepo` `ListProjectRepositories` | `GET /v4/projects/{project_id}/repositories` | project |
| `pipelines` | `CodeArtsPipeline` `ListPipelines` | `POST /v5/{project_id}/api/pipelines/list` | project |
| `deploy-tasks` | `CodeArtsDeploy` `ListDeployTasks` | `GET /v2/{project_id}/tasks/list` | project |

Service codes, operation names and REST paths are verified against the live
KooCLI metadata (`hcloud <Service> <Operation> --help`, KooCLI 7.3.12) and the
official SDK `_<op>_http_info` resource paths — see
[references/verification-method.md](references/verification-method.md). The
skill is aimed at DevOps asset inventory and daily patrol.

Architecture:

```text
agent → python3 scripts/list_codearts.py --resource <r> --cli-region=<region>
      → hcloud <Service> <ListOperation> → CodeArts OpenAPI (regional endpoint)
      → parsed JSON → table / --json / --names-only

(hcloud binary missing) → fallback: matching official CodeArts SDK list method
```

Key properties:

- **Read-only by design** — only the four List operations above are ever
  constructed. A write-intent guard scans arguments and validates the operation
  name; mutating intents (create / delete / update / run / start / stop / merge
  / batch ...) are rejected before a single command runs.
- **CLI first, SDK fallback** — KooCLI is the primary path; when the hcloud
  binary is absent the script falls back to the matching official SDK. Credentials
  are read only by the CLI profile / standard environment variables.
- **Project auto-resolution** — project-scoped resources accept `--project-id`;
  when omitted, the project list is fetched and adopted only if exactly one
  project exists (otherwise an explicit id is requested).
- **Full-field table output** — the default table renders the union of all
  returned fields, with the pipeline latest-run status surfaced as `status`.
- **Offline-testable** — every code path (routing, paging, filters, project
  resolution, error classification, guard, SDK fallback) is covered by unit
  tests that mock the hcloud subprocess.

Out of scope: every mutating CodeArts action (create / delete / update / run /
stop pipelines, create repositories, start deploy tasks, etc.) and single-resource
detail / log reading. Those require a dedicated write-capable skill and explicit
user confirmation.

## Prerequisites

1. **KooCLI (`hcloud`) installed** — see
   [references/cli-installation-guide.md](references/cli-installation-guide.md).
   Alternative: `pip install` the matching CodeArts SDK for the fallback path.
2. **Active credential profile** — configure credentials out-of-band
   (`KooCLI configure` in your terminal, or credential environment variables).
   Never paste AK/SK into chat; the script never reads, echoes or stores secrets.
3. **IAM permission** — read-only CodeArts actions; least-privilege policy in
   [references/iam-policies.md](references/iam-policies.md).
4. **Python 3.8+** (standard library only — argparse / json / subprocess).
5. **Outbound HTTPS** access to `*.myhuaweicloud.com`.

## Workflow

1. **Confirm the target region** (default `cn-north-4`).
2. **Choose the resource** with `--resource` (default `projects`).
3. **For project-scoped resources**, pass `--project-id` (or rely on the unique
   project auto-resolution).
4. **Run the list script** with the desired output mode and filters.
5. **Read the result** — table for humans, `--json` for tooling, `--names-only`
   for a compact inventory.
6. **Handle empty / error cases** per the Error Handling table below.

## Core Commands

```bash
# 1) CodeArts projects (default resource)
python3 scripts/list_codearts.py --resource projects --region cn-north-4

# 2) Code-and-repo (仓库) list of a project
python3 scripts/list_codearts.py --resource repos --project-id <project-id>

# 3) Pipelines of a project
python3 scripts/list_codearts.py --resource pipelines --project-id <project-id>

# 4) Deploy tasks (部署任务) of a project
python3 scripts/list_codearts.py --resource deploy-tasks --project-id <project-id>

# Output modes
python3 scripts/list_codearts.py --resource repos --json
python3 scripts/list_codearts.py --resource pipelines --names-only

# Filters
python3 scripts/list_codearts.py --resource projects --name demo
python3 scripts/list_codearts.py --resource deploy-tasks --project-id <project-id> --status failed

# Unique-project auto-resolution (no --project-id)
python3 scripts/list_codearts.py --resource repos --names-only
```

Equivalent direct KooCLI commands (the script wraps exactly these, with paging):

```bash
hcloud ProjectMan ListProjectsV4 --cli-region=cn-north-4 --limit=100 --offset=0
hcloud CodeArtsRepo ListProjectRepositories --cli-region=cn-north-4 --project_id=<project-id> --limit=100 --offset=0
hcloud CodeArtsPipeline ListPipelines --cli-region=cn-north-4 --project_id=<project-id> --limit=100 --offset=0
hcloud CodeArtsDeploy ListDeployTasks --cli-region=cn-north-4 --project_id=<project-id> --page=1 --size=100
```

## Parameter Confirmation

| Parameter | Required | Description | Example |
| --------- | -------- | ----------- | ------- |
| `--resource` | No | Resource family: `projects` \| `repos` \| `pipelines` \| `deploy-tasks` (default `projects`) | `pipelines` |
| `--region` / `-r` | No | Huawei Cloud region (default `cn-north-4`) | `cn-south-1` |
| `--project-id` | Cond. | Required for `repos` / `pipelines` / `deploy-tasks`; auto-resolved when exactly one project exists | `41bd3eab86544863b8fc92ffcd35e3c8` |
| `--name` | No | Name filter — server-side for `projects`/`repos` (`search`) and `pipelines` (`name`); client-side substring for `deploy-tasks` | `demo` |
| `--status` | No | Status filter — **client-side** for every resource (`deploy-tasks` uses `state`, `projects` uses `project_type`) | `failed` |
| `--json` | No | Output the raw item array as JSON | — |
| `--names-only` | No | Output a compact name + ID inventory | — |
| `--page-size` | No | Page size (default 100) | `100` |
| `--operation` | No | hcloud operation name; must equal the selected resource's read-only List operation | `ListProjectsV4` |

Output-mode precedence: `--names-only` → `--json` → table (default).

## Write-Intent Guard

- The script scans flag names plus the `--operation` value for mutating
  vocabulary (`create`, `delete`, `update`, `modify`, `run`, `start`, `stop`,
  `retry`, `merge`, `batch`, and CodeArts operation names such as
  `CreateProjectV4`, `DeleteRepository`, `RunPipeline`, `StartDeployTask`).
- The values of read-only selector/filter flags (`--region`, `--resource`,
  `--project-id`, `--name`, `--status`, `--page-size`) are **not** scanned: they
  are read data and may legitimately contain write-looking words (e.g. an
  instance named `restart-me`, the status `failed`, or `--resource deploy-tasks`).
- Any hit raises `GuardError`, prints `[错误] 检测到写操作意图 ... 已被守卫拦截`, and
  exits with code 1 **before** a single hcloud command is executed. The guard
  runs on the raw argv *before* argparse, so a mutating flag such as
  `--create-repository` is reported as a guard violation rather than an
  "unrecognized argument" error.
- Only the four read-only List operations are ever constructed by
  `build_command()`; there is no code path that can issue a mutating call.

## KooCLI Command Format Standard

```text
hcloud <Service> <Operation> --cli-region=<region> [--key=value ...]
```

- **Service names** — exact KooCLI title-case names: `ProjectMan`,
  `CodeArtsRepo`, `CodeArtsPipeline`, `CodeArtsDeploy`.
- **Operation names** — PascalCase: `ListProjectsV4`, `ListProjectRepositories`,
  `ListPipelines`, `ListDeployTasks`.
- **Region parameter** — `--cli-region=<value>`, e.g. `--cli-region=cn-north-4`
  (required for every concrete call).
- **Parameters** — `--limit` / `--offset` for `ProjectMan` / `CodeArtsRepo` /
  `CodeArtsPipeline`; `--page` / `--size` for `CodeArtsDeploy`; `--project_id`
  for project-scoped resources; `--search` (projects/repos) and `--name`
  (pipelines) for server-side name filtering. `ListDeployTasks` has **no** name
  query parameter, so `--name` is applied client-side for `deploy-tasks`.
- **REST paths (official SDK `_http_info`)** — as listed in the Overview table;
  `project_id` is resolved by the script (or KooCLI) and never guessed.

## Error Handling

| Scenario | Behavior |
| -------- | -------- |
| Empty list | Exit 0, prints `当前区域（<x>）[项目（<pid>）]无 CodeArts 资源（resource=<r>）` |
| 403 / insufficient IAM permission | Exit 1, `无权限访问 CodeArts，请检查 IAM 权限` hint |
| Missing / invalid AK-SK | Exit 1, explicit hint to configure hcloud credentials out-of-band (never in chat) |
| hcloud not installed | Exit 1 after the SDK fallback is also unavailable, hint to install KooCLI or the SDK |
| Project-scoped resource without a resolvable project | Exit 1, `请使用 --project-id 指定目标项目` hint |
| Network / API failure | Exit 1 with the hcloud stderr excerpt |
| KooCLI usage error (`[USE_ERROR] ...`, even with exit code 0) | Exit 1, explicit `KooCLI 参数错误` hint pointing to `<Service> <Operation> --help` |
| Write intent detected | Exit 1, `GuardError` message, no command executed |

Exit codes: `0` success / empty list; `1` config, auth, guard, resolution, or API error.

## Edge Cases

| Scenario | Handling |
| -------- | -------- |
| `--resource` omitted | Defaults to `projects` |
| Project-scoped resource, no `--project-id` | Project list is fetched; exactly one project is adopted automatically, zero/several raise an explicit hint |
| `--name` on `deploy-tasks` | Applied client-side (no server-side name parameter) |
| `--status` | Applied client-side for every resource after the full list is fetched |
| Large collection | Automatic paging: `offset`/`limit` (`total`-aware, full-page fallback, max 100 pages) or `page`/`size` |
| Extra response fields | Table columns are built from the union of returned fields — new fields appear automatically |
| Field missing on an item | Rendered as `-` in the table |
| Pipeline latest-run status | Surfaced as `status` for readability |
| `ListDeployTasks` deprecation | Huawei Cloud recommends `ListAllApp` (a newer deploy-task API); this skill keeps `ListDeployTasks`, which remains callable, and documents the alternative |
| Non-JSON hcloud output | `ApiError` with the raw excerpt (first 200 chars) |
| hcloud absent, SDK installed | Transparent fallback to the matching CodeArts SDK, same output modes |
| User asks to create/delete/run | Out of scope — blocked by the write-intent guard |

## Testing

Offline unit tests with a mocked hcloud subprocess (no credentials, no network):

```bash
python3 -m unittest discover -s tests -v
```

Coverage: write-intent guard (read passes / create / delete / update / run /
start / stop / merge / normalized separators / selector values not scanned /
operation whitelist), command construction for all four resources (`projects`
search param, `repos` project + search, `pipelines` project + name,
`deploy-tasks` page/size and no name), JSON extraction (object / bare array /
noise), failure classification (missing AK/SK, 403, `[USE_ERROR]` with rc=0,
generic), client-side name/status filtering, paging via total and full page,
page-based paging, project auto-resolution (single / zero / several / explicit),
SDK fallback (success / unavailable / missing credentials), SDK request
construction (including the pipeline `body` wrapper and deploy page number),
rendering, and all main() output modes.

## Reference Documents

| Document | Content |
| -------- | ------- |
| [references/iam-policies.md](references/iam-policies.md) | Least-privilege read-only IAM policy |
| [references/cli-installation-guide.md](references/cli-installation-guide.md) | KooCLI installation and credential configuration |
| [references/verification-method.md](references/verification-method.md) | How the skill and its tests were verified |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria checklist |
