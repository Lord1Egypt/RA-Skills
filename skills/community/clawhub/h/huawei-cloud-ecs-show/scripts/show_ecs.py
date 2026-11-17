#!/usr/bin/env python3
"""Show a single Huawei Cloud ECS instance by its instance ID (read-only).

Primary execution path is KooCLI `hcloud ECS ShowServer` (official read-only GET
/v1/{project_id}/cloudservers/{server_id}); when hcloud is not installed the
script falls back to the official `huaweicloudsdkecs` v2 SDK (`show_server`).
It reads nothing but the active credential profile / environment. The result is
rendered as a key/detail block (default) or raw JSON (`--json`) on stdout; with
`--md-file` the same key fields are rendered as Markdown and written to a local
file. The script performs no cloud write operation — the only file it may touch
is the explicitly requested Markdown export target.

Usage:
    python3 scripts/show_ecs.py --instance-id <server_id>
                                [--region cn-north-4]
                                [--project-id <project_id>]
                                [--json]
                                [--md-file <path>]

Environment overrides (mostly for tests):
    HUAWEI_CLOUD_ECS_SHOW_HCLOUD_BIN   hcloud executable (default "hcloud")
    HUAWEI_CLOUD_ECS_SHOW_HCLOUD_ARGS  extra args injected before the operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
SERVICE = "ECS"
ALLOWED_OPERATION = "ShowServer"

# Mutating ECS operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createserver",
    "createservers",
    "deleteserver",
    "deleteservers",
    "updateserver",
    "modifyserver",
    "rebuildserver",
    "resizeserver",
    "serveraction",
    "batchaction",
    "startserver",
    "stopserver",
    "restartserver",
    "rebootserver",
    "resetserver",
    "migrateserver",
    "lockserver",
    "unlockserver",
    "attachvolume",
    "detachvolume",
    "createservergroup",
    "deleteservergroup",
    "batchstart",
    "batchstop",
    "batchreboot",
    "addservergroup",
    "delete",
    "create",
    "update",
    "modify",
    "restart",
    "reboot",
    "resize",
    "rebuild",
    "migrate",
    "attach",
    "detach",
    "start",
    "stop",
    "shutdown",
    "reset",
    "destroy",
    "restore",
    "terminate",
)

# Option flags whose *values* are pure read data (a region name / a server ID /
# a project ID). Their values must NOT be scanned by the write-intent guard — a
# flag following them is still scanned (defense in depth).
_VALUE_STRIPPED_FLAGS = (
    "--region",
    "-r",
    "--instance-id",
    "--instance_id",
    "--server-id",
    "--server_id",
    "--project-id",
    "--project_id",
    "--md-file",
    "--output-md",
)

# Key/detail fields rendered explicitly (order preserved); the wire names come
# from the ECS ShowServer / ServerDetail response.
_KEY_FIELDS = [
    ("id", "实例 ID"),
    ("name", "名称"),
    ("status", "状态"),
    ("flavor", "规格"),
    ("image_id", "镜像"),
    ("privateIps", "私网 IP"),
    ("publicIps", "公网 IP"),
    ("availability_zone", "可用区"),
    ("created", "创建时间"),
    ("tags", "标签"),
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

_NOT_FOUND_PATTERNS = (
    "404",
    "not found",
    "notfound",
    "no such",
    "server not exist",
    "does not exist",
    "不存在",
    "未找到",
)

# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — the marker must be treated as a hard failure even
# when the return code looks successful.
_USE_ERROR_MARKER = "[use_error]"

# Whitelisted credential environment variables — read by name only, never by
# enumerating os.environ.
_AK_ENV_NAMES = (
    "HW_ACCESS_KEY",
    "HUAWEI_ACCESS_KEY",
    "HUAWEICLOUD_SDK_AK",
    "HUAWEI_CLOUD_ACCESS_KEY",
)
_SK_ENV_NAMES = (
    "HW_SECRET_KEY",
    "HUAWEI_SECRET_KEY",
    "HUAWEICLOUD_SDK_SK",
    "HUAWEI_CLOUD_SECRET_KEY",
)


class EcsShowError(Exception):
    """Base error for the ECS show skill."""


class GuardError(EcsShowError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(EcsShowError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(EcsShowError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class NotFoundError(EcsShowError):
    """The requested instance ID does not exist (404)."""


class ApiError(EcsShowError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-server`, `CreateServers`, and
    `create_server` all hit the same keyword. Read-only vocabulary
    (show/get/describe/list) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（ECS ShowServer），创建/删除/启停/重启/变配等变更操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ShowServer operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。" % (operation, ALLOWED_OPERATION)
        )
    return True


def guard_text_from_argv(argv):
    """Build the text the write-intent guard should scan.

    Scans flag names and positional tokens, but strips the values of read-only
    data flags (`--region` / `--instance-id` / `--project-id`): those are pure
    read data and may legitimately contain write-looking words. A *flag*
    following such an option is never swallowed — otherwise a mutating flag
    like `--instance-id --create-server` could hide from the guard.
    """
    tokens = list(argv if argv is not None else sys.argv[1:])
    kept = []
    skip_next = False
    for tok in tokens:
        if tok in _VALUE_STRIPPED_FLAGS:
            skip_next = True
            continue
        if tok.startswith("-") and "=" in tok and tok.split("=", 1)[0] in _VALUE_STRIPPED_FLAGS:
            continue
        if skip_next:
            skip_next = False
            if not tok.startswith("-"):
                # This token is the flag's read value — strip it.
                continue
        kept.append(tok)
    return " ".join(kept)


def validate_instance_id(instance_id):
    """Reject a missing / obviously malformed instance ID with a clear hint."""
    if instance_id is None or not str(instance_id).strip():
        raise ConfigError("实例 ID 不能为空：请通过 --instance-id 传入一个有效的 ECS 实例 ID。")
    value = str(instance_id).strip()
    if re.search(r"\s", value):
        raise ConfigError(
            "实例 ID 含空白字符，疑似非法：%r。请确认传入的是单个 ECS 实例 ID（UUID）。"
            % instance_id
        )
    return value


def build_command(region, instance_id, project_id=None):
    """Build the hcloud ECS ShowServer argv (without the executable).

    Mirrors the real KooCLI parameter list: `--cli-region` / `--server_id`
    (verified against `huaweicloudsdkecs` v2 `ShowServerRequest` — the only
    operation parameter is `server_id`; KooCLI resolves project_id from the
    credential profile, so `project_id` is only used on the SDK fallback path).
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--server_id=%s" % instance_id,
    ]
    return argv


def _hcloud_executable():
    return os.environ.get("HUAWEI_CLOUD_ECS_SHOW_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("HUAWEI_CLOUD_ECS_SHOW_HCLOUD_ARGS", "").split()
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
    """Parse hcloud stdout as JSON; tolerate wrapper/noise lines."""
    text = stdout.strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                pass
        raise ApiError("hcloud 输出无法解析为 JSON：%s" % text[:200])


def classify_hcloud_failure(stdout, stderr, returncode):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = (stderr + " " + stdout).strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：ECS ShowServer "
            "真实参数清单可通过 `hcloud ECS ShowServer --help` 查看。"
            "详情：%s" % (returncode, blob[:300])
        )
    if any(p in low for p in _NOT_FOUND_PATTERNS) and not re.search(r"\b40[13]\b", blob):
        return NotFoundError(
            "未找到该 ECS 实例（实例 ID 不存在或不属于当前项目/区域，404）。"
            "请确认 --instance-id 与 --region 是否正确。详情：%s" % blob[:300]
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
            "无权限访问 ECS，请检查 IAM 权限（403：AK/SK 无效或未授予 ECS 只读权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_server(payload):
    """Pull the single server object out of a ShowServer response."""
    if isinstance(payload, dict):
        server = payload.get("server")
        if isinstance(server, dict):
            return server
        if "id" in payload or "name" in payload:
            return payload
    return None


def to_jsonable(value):
    """Recursively convert `value` into JSON-serializable primitives.

    The official `huaweicloudsdkecs` model `to_dict()` does not recurse into
    every container (e.g. ServerDetail.addresses holds lists of ServerAddress
    model objects). This helper normalizes any nested structure: SDK models via
    their own `to_dict()`, containers rebuilt element-wise, and anything else
    non-primitive degrades to `str()` (never raises).
    """
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {key: to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_jsonable(item) for item in value]
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        try:
            return to_jsonable(to_dict())
        except Exception:
            return str(value)
    return str(value)


def _env_value(names):
    """Read the first non-empty value from an explicit whitelist of env names."""
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def sdk_server_to_dict(server):
    """Convert a `huaweicloudsdkecs` ServerDetail into wire-name-keyed dict.

    The SDK `to_dict()` emits Python attribute names (`access_i_pv4`,
    `os_ext_a_zavailability_zone`); the KooCLI/OpenAPI JSON uses wire names
    (`accessIPv4`, `OS-EXT-AZ:availability_zone`). Remapping through the
    official `ServerDetail.attribute_map` keeps both execution paths producing
    the same shape.
    """
    if isinstance(server, dict):
        raw = dict(server)
    else:
        try:
            raw = server.to_dict()
        except AttributeError:
            return dict(server)
    if not isinstance(raw, dict):
        return {}
    try:
        from huaweicloudsdkecs.v2 import ServerDetail
        attr_map = ServerDetail.attribute_map
    except Exception:
        attr_map = {}
    out = {}
    attr_keys = set(attr_map.keys())
    for attr, wire in attr_map.items():
        if attr in raw and raw[attr] is not None:
            out[wire] = to_jsonable(raw[attr])
    for key, value in raw.items():
        if key not in attr_keys and key not in out and value is not None:
            out[key] = to_jsonable(value)
    return out


def show_server_via_sdk(region, instance_id, project_id=None):
    """SDK fallback: query one server through `huaweicloudsdkecs` v2.

    Only invoked when hcloud is not installed. Credentials are taken from the
    whitelisted AK/SK environment variables — never passed as literals here.
    `project_id` (optional) is forwarded to BasicCredentials; region resolution
    uses the SDK's own `EcsRegion` catalog (official endpoints, no guessing),
    falling back to an explicit `Region(id, endpoint)` for custom regions.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkecs.v2 import EcsClient, ShowServerRequest
        from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkecs 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkecs。详情：%s" % exc
        )

    ak = _env_value(_AK_ENV_NAMES)
    sk = _env_value(_SK_ENV_NAMES)
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 BasicCredentials 不会自动读取环境"
            "变量，且当前环境未检测到 HW_ACCESS_KEY / HUAWEI_ACCESS_KEY / "
            "HUAWEICLOUD_SDK_AK 形式的 AK/SK 环境变量。"
            "请在会话外设置 HUAWEI_ACCESS_KEY / HUAWEI_SECRET_KEY（严禁在对话中粘贴"
            " AK/SK），参见 references/cli-installation-guide.md。"
        )
    cred_kwargs = {"ak": ak, "sk": sk}
    if project_id:
        cred_kwargs["project_id"] = project_id
    credentials = BasicCredentials(**cred_kwargs)  # env-sourced, never literals
    try:
        try:
            region_obj = EcsRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://ecs.%s.myhuaweicloud.com" % region)
        client = EcsClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkecs 安装与区域配置。"
            % (region, exc)
        )
    request = ShowServerRequest(server_id=instance_id)
    try:
        response = client.show_server(request)
    except Exception as exc:
        low = str(exc).lower()
        if any(p in low for p in _NOT_FOUND_PATTERNS):
            raise NotFoundError(
                "未找到该 ECS 实例（实例 ID 不存在或不属于当前项目/区域，404）。"
                "详情：%s" % str(exc)[:300]
            )
        if any(p in low for p in _AUTH_PATTERNS):
            raise AuthError(
                "无权限访问 ECS，请检查 IAM 权限（403）。详情：%s" % str(exc)[:300]
            )
        raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
    server = getattr(response, "server", None)
    if server is None:
        raise NotFoundError(
            "未找到该 ECS 实例（实例 ID %s 不存在或不属于当前项目/区域）。" % instance_id
        )
    return sdk_server_to_dict(server)


def show_server(region, instance_id, project_id=None):
    """Query one ECS server by ID; KooCLI first, SDK fallback."""
    instance_id = validate_instance_id(instance_id)
    argv = build_command(region, instance_id, project_id=project_id)
    try:
        stdout, stderr, returncode = run_hcloud(argv)
    except ConfigError:
        # hcloud binary missing → one-shot SDK fallback (no CLI retry).
        return show_server_via_sdk(region, instance_id, project_id=project_id)
    if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
        # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
        raise classify_hcloud_failure(stdout, stderr, returncode)
    payload = extract_json(stdout)
    server = extract_server(payload)
    if server is None:
        raise NotFoundError(
            "未找到该 ECS 实例（实例 ID %s 不存在或不属于当前 region=%s）。"
            % (instance_id, region)
        )
    return server


def _extract_ips(addresses):
    """Split a ServerDetail `addresses` map into (private_ips, public_ips)."""
    private, public = [], []
    if not isinstance(addresses, dict):
        return private, public
    for entries in addresses.values():
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            addr = entry.get("addr") or entry.get("ip_address")
            if not addr:
                continue
            ip_type = (entry.get("OS-EXT-IPS:type")
                       or entry.get("os_ext_ip_stype")
                       or entry.get("type"))
            if ip_type and "float" in str(ip_type).lower():
                public.append(str(addr))
            else:
                private.append(str(addr))
    return private, public


def normalize_server(server):
    """Flatten nested flavor / addresses / AZ fields into detail-friendly keys.

    Also flattens `image` / `tags` so the rendered detail block is stable across
    the CLI and SDK paths (both wire-name keys).
    """
    flat = dict(server)
    flavor = server.get("flavor")
    if isinstance(flavor, dict):
        flat["flavor"] = flavor.get("name") or flavor.get("id") or "-"
        flat.setdefault("vcpus", flavor.get("vcpus", "-"))
        flat.setdefault("ram", flavor.get("ram", "-"))
    elif flavor is None:
        flat["flavor"] = "-"
    az = (server.get("OS-EXT-AZ:availability_zone")
          or server.get("os_ext_a_zavailability_zone")
          or server.get("availability_zone"))
    flat["availability_zone"] = az or "-"
    private, public = _extract_ips(server.get("addresses"))
    flat["privateIps"] = ",".join(private) if private else "-"
    public_ips = list(public)
    access_v4 = server.get("accessIPv4") or server.get("access_i_pv4")
    if access_v4 and str(access_v4) not in public_ips:
        public_ips.insert(0, str(access_v4))
    flat["publicIps"] = ",".join(public_ips) if public_ips else "-"
    image = server.get("image")
    if isinstance(image, dict):
        flat["image_id"] = image.get("id", "-")
    elif image:
        flat["image_id"] = image
    if "tags" not in flat or flat.get("tags") in (None, ""):
        flat["tags"] = "-"
    return flat


def _cell(value):
    if isinstance(value, (dict, list, tuple)):
        try:
            return json.dumps(to_jsonable(value), ensure_ascii=False,
                              separators=(",", ":"))
        except (TypeError, ValueError):
            return str(value)
    return str(value)


def render_detail(server):
    """Render a single-instance key/detail block (key fields first)."""
    flat = normalize_server(server)
    used = set()
    lines = []
    for key, label in _KEY_FIELDS:
        value = flat.get(key)
        used.add(key)
        lines.append("  %-10s: %s" % (label, "-" if value in (None, "") else _cell(value)))
    extras = sorted(k for k in flat if k not in used and k not in
                    ("vcpus", "ram"))
    if extras:
        lines.append("  其他字段  :")
        for key in extras:
            lines.append("    %-14s: %s" % (key, _cell(flat.get(key))))
    return "\n".join(lines)


def _md_cell(value):
    """Render one value as a safe Markdown table cell (escape `|` / newlines)."""
    text = _cell(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def render_markdown(server, region=None):
    """Render a single-instance detail document as Markdown.

    Reuses `normalize_server()` + `_KEY_FIELDS` so the exported key fields are
    exactly the ones shown by the default detail block; any additional fields
    are appended in an "其他字段" table so new response fields surface
    automatically.
    """
    flat = normalize_server(server)
    lines = ["# ECS 实例详情", ""]
    if region:
        lines.append("- Region: %s" % region)
        lines.append("")
    used = set()
    lines.append("| 字段 | 值 |")
    lines.append("| --- | --- |")
    for key, label in _KEY_FIELDS:
        value = flat.get(key)
        used.add(key)
        lines.append("| %s | %s |"
                     % (label, "-" if value in (None, "") else _md_cell(value)))
    extras = sorted(k for k in flat if k not in used and k not in
                    ("vcpus", "ram"))
    if extras:
        lines.append("")
        lines.append("## 其他字段")
        lines.append("")
        lines.append("| 字段 | 值 |")
        lines.append("| --- | --- |")
        for key in extras:
            lines.append("| %s | %s |" % (key, _md_cell(flat.get(key))))
    return "\n".join(lines) + "\n"


def write_markdown(path, content):
    """Write `content` to `path` (local Markdown export), with explicit errors.

    Exists to give a clear message (instead of a silent failure / raw traceback)
    when the export path is empty, its parent directory is missing, it points at
    a directory, or it is not writable. An existing file is overwritten.
    """
    if path is None or not str(path).strip():
        raise ConfigError("导出路径不能为空：请通过 --md-file 传入一个 .md 文件路径。")
    target = os.path.abspath(os.path.expanduser(str(path).strip()))
    parent = os.path.dirname(target)
    if parent and not os.path.isdir(parent):
        raise ConfigError(
            "导出路径的上级目录不存在：%s。请先创建该目录，或换一个可写路径。"
            % parent
        )
    if os.path.isdir(target):
        raise ConfigError(
            "导出路径是一个目录，无法写入：%s。请指定一个 .md 文件路径。"
            % target
        )
    try:
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(content)
    except PermissionError:
        raise ConfigError("导出路径不可写（权限不足）：%s。请换一个可写路径。" % target)
    except OSError as exc:
        raise ConfigError("写入 Markdown 失败：%s（%s）。" % (target, exc))
    return target


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云单个 ECS 实例详情（KooCLI hcloud ECS ShowServer，只读）。")
    parser.add_argument("--instance-id", "--instance_id", "--server-id",
                        dest="instance_id", required=True,
                        help="要查询的 ECS 实例 ID（必填）")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--project-id", "--project_id", dest="project_id",
                        default=None,
                        help="项目 ID（可选；仅用于 SDK 兜底路径）")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出实例完整原始字段")
    parser.add_argument("--md-file", "--output-md", dest="md_file", default=None,
                        help="将实例详情渲染为 Markdown 并写入指定文件路径"
                             "（可选；已存在则覆盖；给定该参数时优先于 --json）")
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud ECS 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)

    # Write-intent guard runs on the RAW argv before argparse, so that a
    # mutating flag (e.g. `--create-server`) is reported as a guard violation
    # instead of an argparse "unrecognized argument" error. Data-flag values
    # (region / instance-id / project-id) are deliberately not scanned.
    try:
        guard_write_intent(guard_text_from_argv(argv))
    except EcsShowError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parser.parse_args(argv)

    try:
        guard_operation(args.operation)
        server = show_server(args.region, args.instance_id,
                             project_id=args.project_id)
    except EcsShowError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.md_file:
        # Markdown export wins over --json: the file is the requested deliverable
        # and the stdout confirmation keeps the command usable in scripts.
        try:
            markdown = render_markdown(server, region=args.region)
            target = write_markdown(args.md_file, markdown)
        except EcsShowError as exc:
            print("[错误] %s" % exc, file=sys.stderr)
            return 1
        print("已导出 ECS 实例详情 Markdown：%s" % target)
    elif args.as_json:
        # Normalize before serialization: never leak an SDK model object
        # (e.g. ServerAddress nested in `addresses`) into json.dumps.
        print(json.dumps(to_jsonable(server), ensure_ascii=False, indent=2))
    else:
        print("Region %s 的 ECS 实例详情：" % args.region)
        print(render_detail(server))

    return 0


if __name__ == "__main__":
    sys.exit(main())