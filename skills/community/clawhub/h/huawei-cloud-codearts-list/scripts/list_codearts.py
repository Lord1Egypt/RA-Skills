#!/usr/bin/env python3
"""List Huawei Cloud CodeArts resources (read-only) via KooCLI.

Routes to one of four read-only CodeArts list APIs selected with `--resource`:

    projects      hcloud ProjectMan       ListProjectsV4            GET  /v4/projects
    repos         hcloud CodeArtsRepo     ListProjectRepositories   GET  /v4/projects/{project_id}/repositories
    pipelines     hcloud CodeArtsPipeline ListPipelines             POST /v5/{project_id}/api/pipelines/list
    deploy-tasks  hcloud CodeArtsDeploy   ListDeployTasks           GET  /v2/{project_id}/tasks/list

Primary execution path is KooCLI; when the hcloud binary is not installed the
script falls back to the matching official Python SDK
(huaweicloudsdkprojectman / huaweicloudsdkcodeartsrepo /
huaweicloudsdkcodeartspipeline / huaweicloudsdkcodeartsdeploy). Credentials are
only ever taken from the active KooCLI profile / standard environment variables;
the script never reads, echoes, or stores secrets itself.

The repositories / pipelines / deploy-task APIs are project-scoped: they need a
`--project-id`. When it is omitted the script resolves it from the project list
and proceeds automatically only when exactly one project exists.

Supports three output modes (full-field table / --json / --names-only), an
optional --name filter and a client-side --status filter, automatic paging, and a
strict write-intent guard: any mutating intent is rejected before a single
command is executed.

Usage:
    python3 scripts/list_codearts.py [--resource projects|repos|pipelines|deploy-tasks]
                                     [--region cn-north-4] [--project-id <id>]
                                     [--name NAME] [--status STATUS]
                                     [--json | --names-only] [--page-size 100]
                                     [--operation ListProjectsV4]

Environment overrides (mostly for tests):
    CODEARTS_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    CODEARTS_LIST_HCLOUD_ARGS  extra args injected before the operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
MAX_PAGES = 100

# --- KooCLI routing table ---------------------------------------------------
# Service codes and operation names are verified against the live KooCLI
# metadata (`hcloud <Service> --help`, KooCLI 7.3.12) and the official SDK
# `_<op>_http_info` resource paths. See references/verification-method.md.
RESOURCES = {
    "projects": {
        "label": "CodeArts 项目",
        "service": "ProjectMan",
        "operation": "ListProjectsV4",
        "rest": "GET /v4/projects",
        "list_keys": ("projects",),
        "total_keys": ("total",),
        "name_keys": ("project_name", "name"),
        "id_keys": ("project_id", "id"),
        "status_keys": ("project_type",),
        "name_param": "search",       # server-side fuzzy name filter
        "paging": "offset",
        "needs_project": False,
    },
    "repos": {
        "label": "CodeArts 代码托管仓库",
        "service": "CodeArtsRepo",
        "operation": "ListProjectRepositories",
        "rest": "GET /v4/projects/{project_id}/repositories",
        "list_keys": (),
        "total_keys": (),
        "name_keys": ("name",),
        "id_keys": ("id",),
        "status_keys": ("status",),
        "name_param": "search",       # server-side fuzzy name filter
        "paging": "offset",
        "needs_project": True,
    },
    "pipelines": {
        "label": "CodeArts 流水线",
        "service": "CodeArtsPipeline",
        "operation": "ListPipelines",
        "rest": "POST /v5/{project_id}/api/pipelines/list",
        "list_keys": ("pipelines",),
        "total_keys": ("total",),
        "name_keys": ("name",),
        "id_keys": ("pipeline_id", "id"),
        "status_keys": ("status",),
        "name_param": "name",         # server-side exact-ish name filter
        "paging": "offset",
        "needs_project": True,
    },
    "deploy-tasks": {
        "label": "CodeArts 部署任务",
        "service": "CodeArtsDeploy",
        "operation": "ListDeployTasks",
        "rest": "GET /v2/{project_id}/tasks/list",
        "list_keys": ("result",),
        "total_keys": ("total_num", "total"),
        "name_keys": ("name",),
        "id_keys": ("id", "task_id"),
        "status_keys": ("state", "status"),
        "name_param": None,           # NO server-side name param -> client-side
        "paging": "page",             # page starts at 1
        "needs_project": True,
    },
}

ALLOWED_OPERATIONS = frozenset(spec["operation"] for spec in RESOURCES.values())

# Mutating CodeArts intents — strictly rejected by the guard.
# NOTE: read-only vocabulary (list / show / get / describe / search) and words
# that appear inside our own read-only operations/resource names must never be
# listed here (e.g. "deploy", "repository", "archive" — `archive` is a real
# read-only project query parameter).
WRITE_INTENT_KEYWORDS = (
    "createprojectandforkrepositories",
    "createprojectandrepositories",
    "createproject",
    "deleteproject",
    "updateproject",
    "removeproject",
    "createrepository",
    "deleterepository",
    "updaterepository",
    "transferrepository",
    "importrepository",
    "exportrepositories",
    "createrepositorylabel",
    "deleterepositorylabel",
    "createrepositorycommitrule",
    "updaterepositorycommitrule",
    "batchdelete",
    "batchupdate",
    "batchmove",
    "batchcreate",
    "createpipeline",
    "deletepipeline",
    "removepipeline",
    "updatepipeline",
    "runpipeline",
    "startnewpipeline",
    "stoppipeline",
    "retrypipeline",
    "runactionspipeline",
    "retryrunactionspipeline",
    "deleteaction",
    "createpipelin",
    "createchange",
    "createmicroservice",
    "createdeploytask",
    "deletedeploytask",
    "updatedeploytask",
    "startdeploytask",
    "createdeployment",
    "deletedeployment",
    "updatedeployment",
    "createbranch",
    "deletebranch",
    "updatebranchname",
    "createtag",
    "deletetag",
    "createmerge",
    "mergemerge",
    "updatemerge",
    "deletemerge",
    "approvalmerge",
    "createreview",
    "deleterepository",
    "lockrepository",
    "unlockrepository",
    "addprojectwebhook",
    "removeprojectwebhook",
    "updateprojectwebhook",
    "create",
    "delete",
    "update",
    "modify",
    "remove",
    "transfer",
    "import",
    "publish",
    "unpublish",
    "execute",
    "run",
    "start",
    "stop",
    "retry",
    "merge",
    "approval",
    "approve",
    "batch",
    "create",
    "destroy",
    "terminate",
)

# Flags whose *values* are pure read data (filters / selectors) and must NOT be
# scanned by the write-intent guard, otherwise legitimate read filters such as
# `--name restart-me`, `--status failed`, `--resource deploy-tasks` or
# `--project-id <uuid>` would be rejected. `--operation` is intentionally left
# out: it is validated separately against the operation whitelist.
_VALUE_STRIPPED_FLAGS = (
    "--region",
    "-r",
    "--resource",
    "--project-id",
    "--name",
    "--status",
    "--page-size",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "name",
    "project_name",
    "id",
    "pipeline_id",
    "project_id",
    "status",
    "project_type",
    "visibility",
    "archived",
    "deploy_system",
    "owner",
    "executor",
    "create_time",
    "created_time",
    "update_time",
    "updated_time",
    "developer",
    "description",
]

_CREDENTIAL_MISSING_PATTERNS = (
    "cli-ak",
    "cli-sk",
    "access key",
    "secret key",
    "credential",
    "configure",
    "未配置",
    "配置为空",
    "no ak",
    "no sk",
    "ak/sk",
    "profile",
)

_AUTH_PATTERNS = (
    "401",
    "403",
    "unauthorized",
    "forbidden",
    "apigw.0301",
    "认证失败",
    "权限不足",
    "permission denied",
)

# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — the marker must be treated as a hard failure even
# when the return code looks successful.
_USE_ERROR_MARKER = "[use_error]"


class CodeArtsListError(Exception):
    """Base error for the CodeArts list skill."""


class GuardError(CodeArtsListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(CodeArtsListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(CodeArtsListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(CodeArtsListError):
    """hcloud / network / unexpected API failure."""


class ProjectResolutionError(CodeArtsListError):
    """--project-id was neither given nor resolvable (0 or >1 projects)."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-project`, `CreateProjectV4` and
    `create_project` all hit the same keyword. Read-only vocabulary
    (list / show / get / describe / search / archive) never matches.
    """
    low = re.sub(r"[\s_\-:]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读列表查询"
                "（ProjectMan/CodeArtsRepo/CodeArtsPipeline/CodeArtsDeploy 的 List 接口），"
                "创建/删除/更新/运行等变更操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation, expected):
    """Only the read-only list operation for the selected resource may run."""
    if operation not in ALLOWED_OPERATIONS or operation != expected:
        raise GuardError(
            "不允许的操作 %r：当前资源仅允许只读操作 %s。" % (operation, expected)
        )
    return True


def guard_text_from_argv(argv):
    """Build the text the write-intent guard should scan.

    Scans flag names and positional tokens, but strips the values of the
    read-only selector/filter flags (region / resource / project-id / name /
    status / page-size): those are pure read data and may legitimately contain
    write-looking words.
    """
    tokens = list(argv if argv is not None else sys.argv[1:])
    kept = []
    skip_next = False
    for tok in tokens:
        if skip_next:
            skip_next = False
            continue
        key = tok.split("=", 1)[0]
        if tok in _VALUE_STRIPPED_FLAGS:
            skip_next = True
            continue
        if tok.startswith("-") and "=" in tok and key in _VALUE_STRIPPED_FLAGS:
            continue
        kept.append(tok)
    return " ".join(kept)


def build_command(resource, region, project_id=None, name=None,
                  limit=DEFAULT_PAGE_SIZE, offset=0):
    """Build the hcloud argv (without executable) for the selected resource.

    Parameter names mirror the live KooCLI metadata exactly:

    - projects:      --cli-region --limit --offset [--search]
    - repos:         --cli-region --project_id --limit --offset [--search]
    - pipelines:     --cli-region --project_id --limit --offset [--name]
    - deploy-tasks:  --cli-region --project_id --page --size

    `deploy-tasks` (ListDeployTasks) has no name query parameter, so `--name`
    is never forwarded for that resource; it is applied client-side instead.
    """
    spec = RESOURCES[resource]
    argv = [
        spec["service"],
        spec["operation"],
        "--cli-region=%s" % region,
    ]
    if spec["needs_project"]:
        argv.append("--project_id=%s" % project_id)
    if spec["paging"] == "page":
        page = (offset // limit) + 1 if limit else 1
        argv.append("--page=%d" % page)
        argv.append("--size=%d" % limit)
    else:
        argv.append("--limit=%d" % limit)
        argv.append("--offset=%d" % offset)
    param = spec["name_param"]
    if name and param:
        argv.append("--%s=%s" % (param, name))
    return argv


def _hcloud_executable():
    return os.environ.get("CODEARTS_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("CODEARTS_LIST_HCLOUD_ARGS", "").split()
    if extra:
        cmd.extend(extra)
    cmd.extend(argv)
    try:
        proc = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=120, universal_newlines=True,
        )
    except FileNotFoundError:
        raise ConfigError(
            "未找到 hcloud（KooCLI）。请先安装 KooCLI 并完成认证配置，"
            "参见 references/cli-installation-guide.md。"
        )
    except subprocess.TimeoutExpired:
        raise ApiError("hcloud 执行超时（120s），请检查网络后重试。")
    return proc.stdout or "", proc.stderr or "", proc.returncode


def extract_json(stdout):
    """Parse hcloud stdout as JSON; tolerate wrapper/noise lines.

    Handles both JSON objects (``{...}``) and bare JSON arrays (``[...]``) —
    ListProjectRepositories returns a top-level array.
    """
    text = stdout.strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Tolerate wrapper/noise lines: parse the outermost JSON value, choosing
    # whichever bracket type opens first so a bare array is not mistaken for
    # its first object element.
    obj_at, arr_at = text.find("{"), text.find("[")
    candidates = []
    if arr_at >= 0 and (obj_at < 0 or arr_at < obj_at):
        candidates = [("[", "]"), ("{", "}")]
    else:
        candidates = [("{", "}"), ("[", "]")]
    for open_ch, close_ch in candidates:
        start, end = text.find(open_ch), text.rfind(close_ch)
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                continue
    raise ApiError("hcloud 输出无法解析为 JSON：%s" % text[:200])


def classify_hcloud_failure(stdout, stderr, returncode, service=None,
                            operation=None):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = (stderr + " " + stdout).strip()
    low = blob.lower()
    hint = ("`hcloud %s %s --help`" % (service or "<Service>",
                                      operation or "<Operation>"))
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：真实参数清单可通过 "
            "%s 查看。详情：%s" % (returncode, hint, blob[:300])
        )
    if any(p in low for p in _CREDENTIAL_MISSING_PATTERNS) and not re.search(
            r"\b40[13]\b", blob):
        return ConfigError(
            "缺少 AK/SK 凭证：hcloud 未配置有效凭证。请先运行 hcloud configure 或"
            "设置凭证环境变量（严禁在对话中粘贴 AK/SK），参见"
            " references/cli-installation-guide.md。详情：%s" % blob[:300]
        )
    if any(p in low for p in _AUTH_PATTERNS):
        return AuthError(
            "无权限访问 CodeArts，请检查 IAM 权限（403：AK/SK 无效、区域不符或未授予"
            " CodeArts 只读权限），参见 references/iam-policies.md。详情：%s"
            % blob[:300]
        )
    return ApiError("hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300]))


def extract_items(payload, resource):
    """Pull the item list out of a list response.

    Handles a bare JSON array (repos) and the wrapped shapes
    ``{projects: [...]}`` / ``{pipelines: [...]}`` / ``{result: [...]}``.
    """
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []
    for key in RESOURCES[resource]["list_keys"]:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    for key in ("projects", "repositories", "repos", "pipelines", "result",
                "items", "data"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _payload_total(payload, resource):
    if not isinstance(payload, dict):
        return None
    for key in RESOURCES[resource]["total_keys"]:
        value = payload.get(key)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
    for key in ("total", "total_count", "totalCount", "count", "total_num"):
        value = payload.get(key)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
    return None


def _has_more(batch, collected, limit, payload, resource):
    if not batch:
        return False
    total = _payload_total(payload, resource)
    if total is not None and total >= 0:
        return collected < total
    return len(batch) >= limit


def _field(item, *names, **kwargs):
    default = kwargs.get("default", "-")
    for name in names:
        if name in item and item[name] not in (None, ""):
            return item[name]
    return default


def filter_by_name(items, name, resource):
    """Client-side name filter (case-insensitive substring match)."""
    if not name:
        return list(items)
    wanted = str(name).strip().lower()
    names = RESOURCES[resource]["name_keys"]
    out = []
    for item in items:
        value = _field(item, *names, default=None) if isinstance(item, dict) else None
        if value is not None and wanted in str(value).lower():
            out.append(item)
    return out


def filter_by_status(items, status, resource):
    """Client-side status filter (case-insensitive).

    Applied uniformly for every resource after the full list is fetched. For
    pipelines the server also exposes a status body parameter, but a single
    client-side implementation keeps the two fields (pipeline-level vs
    latest-run) consistent and avoids array-parameter drift.
    """
    if not status:
        return list(items)
    wanted = str(status).strip().lower()
    keys = RESOURCES[resource]["status_keys"]
    out = []
    for item in items:
        if not isinstance(item, dict):
            continue
        value = _field(item, *keys, default=None)
        if value is not None and str(value).strip().lower() == wanted:
            out.append(item)
    return out


# --- SDK fallback -----------------------------------------------------------

_SDK_SPEC = {
    "projects": {
        "modules": ("huaweicloudsdkprojectman.v4",
                    "huaweicloudsdkprojectman.v4.region.projectman_region"),
        "endpoint": "https://projectman-ext.%s.myhuaweicloud.com",
        "client": "ProjectManClient",
        "region": "ProjectManRegion",
        "request": "ListProjectsV4Request",
        "list_attr": "projects",
        "total_attr": "total",
    },
    "repos": {
        "modules": ("huaweicloudsdkcodeartsrepo.v4",
                    "huaweicloudsdkcodeartsrepo.v4.region.codeartsrepo_region"),
        "endpoint": "https://codeartsrepo-ext.%s.myhuaweicloud.com",
        "client": "CodeArtsRepoClient",
        "region": "CodeArtsRepoRegion",
        "request": "ListProjectRepositoriesRequest",
        "list_attr": "body",
        "total_attr": None,
    },
    "pipelines": {
        "modules": ("huaweicloudsdkcodeartspipeline.v2",
                    "huaweicloudsdkcodeartspipeline.v2.region.codeartspipeline_region"),
        "endpoint": "https://cloudpipeline-ext.%s.myhuaweicloud.com",
        "client": "CodeArtsPipelineClient",
        "region": "CodeArtsPipelineRegion",
        "request": "ListPipelinesRequest",
        "query": "ListPipelineQuery",
        "list_attr": "pipelines",
        "total_attr": "total",
    },
    "deploy-tasks": {
        "modules": ("huaweicloudsdkcodeartsdeploy.v2",
                    "huaweicloudsdkcodeartsdeploy.v2.region.codeartsdeploy_region"),
        "endpoint": "https://codearts-deploy.%s.myhuaweicloud.com",
        "client": "CodeArtsDeployClient",
        "region": "CodeArtsDeployRegion",
        "request": "ListDeployTasksRequest",
        "list_attr": "result",
        "total_attr": "total_num",
    },
}


def _env_credential(markers):
    for key, value in os.environ.items():
        upper = key.upper()
        if not upper.startswith(("HUAWEI", "HW_", "HWC")):
            continue
        if any(marker in upper for marker in markers) and value:
            return value
    return None


def _sdk_item_to_dict(item):
    if isinstance(item, dict):
        return dict(item)
    try:
        return item.to_dict()
    except AttributeError:
        return dict(item) if item else {}


def list_resource_via_sdk(resource, region, project_id=None, name=None,
                          limit=DEFAULT_PAGE_SIZE, max_pages=MAX_PAGES):
    """SDK fallback: query one CodeArts resource through its official SDK.

    Only invoked when hcloud is not installed. Credentials are read explicitly
    from standard environment variables (HUAWEI_*/HW_*/HWC_* AK/SK markers):
    the official SDK's `BasicCredentials` performs no env auto-discovery.
    Region resolution uses each SDK's own Region catalog (official endpoints),
    falling back to an explicit `Region(id, endpoint)` for custom regions.
    """
    spec = _SDK_SPEC[resource]
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        import importlib
        root_mod = importlib.import_module(spec["modules"][0])
        region_mod = importlib.import_module(spec["modules"][1])
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且对应的 CodeArts SDK 未安装，无法回退到 SDK。"
            "请安装 KooCLI 或 pip install huaweicloudsdkcore %s。详情：%s"
            % (spec["modules"][0].split(".")[0], exc)
        )

    client_cls = getattr(root_mod, spec["client"])
    region_cls = getattr(region_mod, spec["region"])
    request_cls = getattr(root_mod, spec["request"])
    query_cls = getattr(root_mod, spec["query"]) if spec.get("query") else None

    ak = _env_credential(("ACCESS_KEY", "_AK"))
    sk = _env_credential(("SECRET_KEY", "_SK"))
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 BasicCredentials 不会自动读取环境"
            "变量，且当前环境未检测到 HUAWEI_*/HW_*/HWC_* 形式的 AK/SK 环境变量。"
            "请在会话外设置 HUAWEI_ACCESS_KEY / HUAWEI_SECRET_KEY（严禁在对话中粘贴"
            " AK/SK），参见 references/cli-installation-guide.md。"
        )
    credentials = BasicCredentials(ak=ak, sk=sk)  # env-sourced, never literals
    try:
        try:
            region_obj = region_cls.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, spec["endpoint"] % region)
        client = client_cls.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（resource=%s region=%s）：%s。请检查对应 CodeArts SDK "
            "安装与区域配置。" % (resource, region, exc)
        )

    call = getattr(client, _sdk_method(resource))
    items = []
    offset = 0
    for _ in range(max_pages):
        request = _build_sdk_request(resource, request_cls, query_cls,
                                     project_id, name, limit, offset)
        try:
            response = call(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问 CodeArts，请检查 IAM 权限（403）。详情：%s"
                    % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(getattr(response, spec["list_attr"], None) or [])
        items.extend(_sdk_item_to_dict(item) for item in batch)
        total = getattr(response, spec["total_attr"], None) \
            if spec["total_attr"] else None
        if total is not None and len(items) >= total:
            break
        if len(batch) < limit:
            break
        offset += len(batch)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return items


def _sdk_method(resource):
    return {
        "projects": "list_projects_v4",
        "repos": "list_project_repositories",
        "pipelines": "list_pipelines",
        "deploy-tasks": "list_deploy_tasks",
    }[resource]


def _build_sdk_request(resource, request_cls, query_cls,
                       project_id, name, limit, offset):
    """Construct the SDK request, matching each operation's real signature."""
    if resource == "projects":
        kwargs = {"limit": limit, "offset": offset}
        if name:
            kwargs["search"] = name
        return request_cls(**kwargs)
    if resource == "repos":
        kwargs = {"project_id": project_id, "limit": limit, "offset": offset}
        if name:
            kwargs["search"] = name
        return request_cls(**kwargs)
    if resource == "pipelines":
        body_kwargs = {"limit": limit, "offset": offset}
        if name:
            body_kwargs["name"] = name
        return request_cls(project_id=project_id,
                           body=query_cls(**body_kwargs))
    if resource == "deploy-tasks":
        page = (offset // limit) + 1 if limit else 1
        return request_cls(project_id=project_id, page=page, size=limit)
    raise ApiError("未知资源：%s" % resource)


# --- Orchestration ----------------------------------------------------------

def _collect(resource, region, project_id=None, name=None,
             limit=DEFAULT_PAGE_SIZE, max_pages=MAX_PAGES):
    """Fetch all pages for one resource (KooCLI first, SDK fallback on absence).

    `name` is only forwarded when the resource has a real server-side name
    parameter; otherwise it is applied client-side by the caller.
    """
    spec = RESOURCES[resource]
    items = []
    offset = 0
    for _page in range(max_pages):
        argv = build_command(resource, region, project_id=project_id, name=name,
                             limit=limit, offset=offset)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            return list_resource_via_sdk(
                resource, region, project_id=project_id, name=name,
                limit=limit, max_pages=max_pages,
            )
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode,
                                          spec["service"], spec["operation"])
        payload = extract_json(stdout)
        batch = extract_items(payload, resource)
        items.extend(batch)
        if not _has_more(batch, len(items), limit, payload, resource):
            break
        offset += len(batch) if batch else limit
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return items


def resolve_project_id(region, explicit=None, limit=DEFAULT_PAGE_SIZE):
    """Return the project id to use for project-scoped resources.

    - explicit id → used as-is.
    - otherwise the project list is fetched: exactly one project is adopted
      automatically; zero or several raise `ProjectResolutionError`.
    """
    if explicit:
        return explicit
    projects = _collect("projects", region, limit=limit)
    if len(projects) == 1:
        pid = _field(projects[0], "project_id", "id", default=None)
        if pid:
            return str(pid)
    raise ProjectResolutionError(
        "无法自动确定项目：当前区域（%s）检测到 %d 个项目。"
        "请使用 --project-id 指定目标项目。"
        % (region, len(projects))
    )


def list_codearts(resource, region, project_id=None, name=None, status=None,
                  limit=DEFAULT_PAGE_SIZE, max_pages=MAX_PAGES):
    """Query a CodeArts resource list (paged) and apply client-side filters.

    Returns ``(items, resolved_project_id)``. `resolved_project_id` is None for
    the project list itself and the adopted id for project-scoped resources.
    """
    spec = RESOURCES[resource]
    resolved = explicit = project_id
    if spec["needs_project"]:
        resolved = resolve_project_id(region, explicit=project_id, limit=limit)
    items = _collect(resource, region, project_id=resolved, name=name,
                     limit=limit, max_pages=max_pages)
    if name and not spec["name_param"]:
        items = filter_by_name(items, name, resource)
    items = filter_by_status(items, status, resource)
    return items, resolved


# --- Rendering --------------------------------------------------------------

def normalize_item(item, resource):
    """Flatten a few nested fields into table-friendly keys."""
    flat = dict(item)
    if resource == "pipelines" and "status" not in flat:
        latest = item.get("latest_run")
        if isinstance(latest, dict) and latest.get("status"):
            flat["status"] = latest["status"]
    if resource == "repos" and "id" in flat:
        flat.setdefault("name", flat.get("name", "-"))
    return flat


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(items, resource):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_item(item, resource) for item in items]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in i for i in rows_data):
            columns.append(key)
    for key in sorted({k for i in rows_data for k in i}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["name", "id"]
    rows = [[_cell(_field(i, col)) for col in columns] for i in rows_data]
    widths = [max(len(col), *(len(row[i]) for row in rows))
              for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i])
                               for i in range(len(columns))))
    return "\n".join(lines)


def item_summary_lines(items, resource):
    """Compact `name  (id: ...)` lines for the --names-only inventory mode."""
    name_keys = RESOURCES[resource]["name_keys"]
    id_keys = RESOURCES[resource]["id_keys"]
    lines = []
    for item in items:
        name = _field(item, *name_keys, default=None)
        if name is None:
            name = _field(item, *id_keys, default="-")
        iid = _field(item, *id_keys, default="-")
        lines.append("%s  (id: %s)" % (name, iid))
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云 CodeArts 资源列表（KooCLI 只读 List，默认 projects）。")
    parser.add_argument("--resource", default="projects",
                        choices=sorted(RESOURCES.keys()),
                        help="要列出的 CodeArts 资源（默认 projects）")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（repos/pipelines/deploy-tasks 必需；"
                             "省略时若唯一项目则自动解析）")
    parser.add_argument("--name", help="按名称过滤（服务端或本地，视资源而定）")
    parser.add_argument("--status",
                        help="按状态过滤（本地过滤；projects 匹配 project_type）")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出名称+ID 清单")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="分页大小（默认 %d）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--operation", default=None,
                        help="hcloud 操作名（仅允许当前资源的只读 List 操作）")

    # Guard runs on the RAW argv before argparse so a mutating flag is reported
    # as a guard violation rather than an argparse error. Filter/selector
    # *values* are read data and deliberately not scanned.
    try:
        guard_write_intent(guard_text_from_argv(argv))
    except CodeArtsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parser.parse_args(argv)
    spec = RESOURCES[args.resource]

    try:
        guard_operation(args.operation or spec["operation"], spec["operation"])
        items, resolved = list_codearts(
            args.resource,
            args.region,
            project_id=args.project_id,
            name=args.name,
            status=args.status,
            limit=args.page_size,
        )
    except CodeArtsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
        return 0

    if args.names_only:
        print("%s（region=%s%s，共 %d 个）："
              % (spec["label"], args.region,
                 "，project=%s" % resolved if resolved else "",
                 len(items)))
        for line in item_summary_lines(items, args.resource):
            print("- %s" % line)
        return 0

    if not items:
        filters = []
        if args.name:
            filters.append("name=%s" % args.name)
        if args.status:
            filters.append("status=%s" % args.status)
        suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
        scope = "当前区域（%s）" % args.region
        if resolved:
            scope += "项目（%s）" % resolved
        print("%s无 CodeArts 资源（resource=%s）%s。"
              % (scope, args.resource, suffix))
        return 0

    print("%s（region=%s%s，共 %d 个，完整字段）："
          % (spec["label"], args.region,
             "，project=%s" % resolved if resolved else "", len(items)))
    print(render_table(items, args.resource))
    return 0


if __name__ == "__main__":
    sys.exit(main())
