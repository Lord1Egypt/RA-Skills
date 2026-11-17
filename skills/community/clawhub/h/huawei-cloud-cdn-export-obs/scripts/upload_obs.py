#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Upload a local file to a Huawei Cloud OBS bucket/key, with overwrite protection.

Primary execution path is KooCLI's obsutil-backed OBS module:

    hcloud OBS cp <local_file> obs://<bucket>/<key> -e=obs.<region>.myhuaweicloud.com
    hcloud OBS stat obs://<bucket>/<key> -e=obs.<region>.myhuaweicloud.com

(``hcloud OBS`` is obsutil-backed: ``cp`` uploads an object and ``stat`` reads
object metadata — there is no PascalCase ``hcloud OBS PutObject`` command.)

When the hcloud binary is absent, the script falls back to the official
``huaweicloudsdkobs`` v1 SDK (``ObsClient.put_object`` / ``ObsClient.head_object``).

Safety contract:

* **Overwrite protection is on by default** — if the target object already
  exists, the upload is refused unless ``overwrite=True``. Existence is checked
  with a read-only ``stat`` / ``head_object`` *before* any write.
* **Only the object upload is ever written** — no bucket create/delete, no
  object delete/copy/move, no ACL/policy/lifecycle change. The operation name is
  whitelisted (``cp`` for upload, ``stat``/``ls`` for existence).
* **Optional read-back verification** — after the upload the object is read
  back (``stat`` / ``head_object``) and the reported size is checked.
"""

import json
import os
import re
import subprocess

DEFAULT_REGION = "cn-north-4"
SERVICE = "OBS"
UPLOAD_OPERATION = "cp"
STAT_OPERATION = "stat"

# Explicit credential environment-variable whitelist (SDK fallback only). The
# environment is never enumerated; each name is read individually.
AK_ENV_KEYS = (
    "HUAWEICLOUD_SDK_AK",
    "HUAWEI_ACCESS_KEY",
    "HW_ACCESS_KEY",
    "HUAWEI_AK",
    "HW_AK",
)
SK_ENV_KEYS = (
    "HUAWEICLOUD_SDK_SK",
    "HUAWEI_SECRET_KEY",
    "HW_SECRET_KEY",
    "HUAWEI_SK",
    "HW_SK",
)
TOKEN_ENV_KEYS = (
    "HUAWEICLOUD_SDK_SECURITY_TOKEN",
    "HUAWEI_SECURITY_TOKEN",
    "HW_SECURITY_TOKEN",
)

_ALLOWED_OPERATIONS = (UPLOAD_OPERATION, STAT_OPERATION, "ls")

_CREDENTIAL_MISSING_PATTERNS = (
    "please set ak, sk and endpoint",
    "please set ak, sk",
    "configuration file",
    "cli-ak",
    "cli-sk",
    "access key",
    "secret key",
    "credential",
    "未配置",
    "配置为空",
    "no ak",
    "no sk",
    "ak/sk",
)

_AUTH_PATTERNS = (
    "invalidaccesskeyid",
    "signaturedoesnotmatch",
    "accessdenied",
    "403",
    "401",
    "forbidden",
    "unauthorized",
    "认证失败",
    "权限不足",
    "permission denied",
)

# Read-only "the object does not exist" markers (obsutil stat / SDK 404).
_NOT_FOUND_PATTERNS = (
    "nosuchkey",
    "nosuchbucket",
    "not found",
    "does not exist",
    "no such",
    "404",
    "notexist",
    "不存在",
)

_USE_ERROR_MARKER = "[use_error]"

_SIZE_RE = re.compile(r"(?:size|content-?length|contentlength)\s*[:=]\s*(\d+)", re.I)
_ETAG_RE = re.compile(r"(?:etag|e-?tag)\s*[:=]\s*\"?([0-9a-fA-F]{8,})\"?", re.I)


class ObsError(Exception):
    """Base error for the OBS upload skill."""


class OverwriteError(ObsError):
    """The target object already exists and overwrite was not requested."""


class ConfigError(ObsError):
    """hcloud/SDK missing or credentials (AK/SK) not configured."""


class AuthError(ObsError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(ObsError):
    """hcloud / network / unexpected API failure."""


def guard_operation(operation):
    """Only cp/stat/ls (upload + read-back) may be executed."""
    if operation not in _ALLOWED_OPERATIONS:
        raise ObsError(
            "不允许的 OBS 操作 %r：本 skill 仅允许上传（%s）与回读校验（%s/%s）。"
            "桶的创建/删除、对象的删除/复制/移动等操作均被拒绝。"
            % (operation, UPLOAD_OPERATION, STAT_OPERATION, "ls")
        )
    return True


def endpoint_for_region(region):
    return "obs.%s.myhuaweicloud.com" % region


def build_object_url(bucket, key):
    if not bucket:
        raise ObsError("缺少 OBS 桶名（--bucket）。")
    if not key:
        raise ObsError("缺少 OBS 对象键（--key）。")
    return "obs://%s/%s" % (bucket, key)


def parse_obs_url(url):
    """Parse ``obs://bucket/key`` -> ``(bucket, key)`` (key may contain ``/``)."""
    match = re.match(r"^obs://([^/]+)(?:/(.*))?$", url or "")
    if not match:
        raise ObsError("非法的 OBS 地址：%r（应形如 obs://bucket/key）。" % url)
    return match.group(1), (match.group(2) or "")


def build_cp_argv(region, local_path, bucket, key, endpoint=None):
    """Build the ``hcloud OBS cp`` argv (without executable)."""
    return [
        SERVICE,
        UPLOAD_OPERATION,
        local_path,
        build_object_url(bucket, key),
        "-e=%s" % (endpoint or endpoint_for_region(region)),
    ]


def build_stat_argv(region, bucket, key, endpoint=None):
    """Build the ``hcloud OBS stat`` argv (without executable)."""
    return [
        SERVICE,
        STAT_OPERATION,
        build_object_url(bucket, key),
        "-e=%s" % (endpoint or endpoint_for_region(region)),
    ]


def _hcloud_executable():
    return os.environ.get("OBS_EXPORT_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("OBS_EXPORT_HCLOUD_ARGS", "").split()
    if extra:
        cmd.extend(extra)
    cmd.extend(argv)
    try:
        proc = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=300, universal_newlines=True,
        )
    except FileNotFoundError:
        raise ConfigError(
            "未找到 hcloud（KooCLI）。请先安装 KooCLI 及其 obsutil 组件并完成配置，"
            "参见 references/cli-installation-guide.md。"
        )
    except subprocess.TimeoutExpired:
        raise ApiError("hcloud 执行超时（300s），请检查网络后重试。")
    return proc.stdout or "", proc.stderr or "", proc.returncode


def classify_hcloud_failure(stdout, stderr, returncode, exists_probe=False):
    """Map a failed hcloud invocation to a domain error with explicit hints.

    ``exists_probe=True`` means the call was a read-only existence check; a
    not-found response is NOT an error (handled by the caller) so it is only
    classified when it is auth / credential / usage.
    """
    blob = (stderr + " " + stdout).strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI/obsutil 拒绝了该参数组合，退出码 %s）：OBS 使用 "
            "obsutil 风格命令，可通过 `hcloud OBS cp --help` / `hcloud OBS stat --help`"
            " 查看参数。详情：%s" % (returncode, blob[:300])
        )
    if any(p in low for p in _AUTH_PATTERNS):
        return AuthError(
            "无权限访问 OBS，请检查 IAM 权限或 AK/SK 是否有效（403 / "
            "InvalidAccessKeyId / SignatureDoesNotMatch），上传需要 obs:object:put，"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    if any(p in low for p in _CREDENTIAL_MISSING_PATTERNS):
        return ConfigError(
            "缺少 AK/SK 凭证：obsutil 未配置有效凭证或 endpoint。请在会话外运行 "
            "`hcloud obs config`（严禁在对话中粘贴 AK/SK），参见 "
            "references/cli-installation-guide.md。详情：%s" % blob[:300]
        )
    return ApiError("hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300]))


def looks_like_not_found(blob):
    low = (blob or "").lower()
    return any(p in low for p in _NOT_FOUND_PATTERNS)


def parse_stat_output(stdout):
    """Heuristically read size / etag from an obsutil ``stat`` output."""
    info = {}
    text = stdout or ""
    size_match = _SIZE_RE.search(text)
    if size_match:
        info["size"] = int(size_match.group(1))
    etag_match = _ETAG_RE.search(text)
    if etag_match:
        info["etag"] = etag_match.group(1)
    return info


def _env_credential(keys):
    for name in keys:
        value = os.getenv(name)
        if value:
            return value
    return None


def _sdk_client(region, endpoint=None):
    """Build a ``huaweicloudsdkobs`` ObsClient (SDK fallback), or raise."""
    try:
        from huaweicloudsdkobs.v1 import ObsClient
        from huaweicloudsdkobs.v1.obs_credentials import ObsCredentials
        from huaweicloudsdkobs.v1.region.obs_region import ObsRegion
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkcore.region.region import Region
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkobs 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkobs。详情：%s" % exc
        )
    ak = _env_credential(AK_ENV_KEYS)
    sk = _env_credential(SK_ENV_KEYS)
    token = _env_credential(TOKEN_ENV_KEYS)
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 ObsCredentials 不会自动读取环境"
            "变量。请在会话外设置白名单中的 AK/SK 环境变量（如"
            " HUAWEICLOUD_SDK_AK / HUAWEI_ACCESS_KEY 与 HUAWEICLOUD_SDK_SK /"
            " HUAWEI_SECRET_KEY），严禁在对话中粘贴 AK/SK，参见"
            " references/cli-installation-guide.md。"
        )
    credentials = (ObsCredentials(ak, sk, token) if token
                   else ObsCredentials(ak, sk))
    if endpoint:
        region_obj = Region(region, "https://%s" % endpoint)
    else:
        try:
            region_obj = ObsRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://%s" % endpoint_for_region(region))
    try:
        return ObsClient.new_builder() \
            .with_http_config(HttpConfig.get_default_config()) \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .build()
    except Exception as exc:
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkobs 安装与区域"
            "配置。" % (region, exc)
        )


def sdk_object_exists(region, bucket, key, endpoint=None):
    """SDK fallback existence check via ``ObsClient.head_object`` (read-only)."""
    from huaweicloudsdkobs.v1 import HeadObjectRequest
    client = _sdk_client(region, endpoint=endpoint)
    try:
        client.head_object(HeadObjectRequest(bucket_name=bucket, object_key=key))
    except Exception as exc:  # noqa: BLE001 - SDK raises on 404 / auth / network
        low = str(exc).lower()
        if any(p in low for p in _NOT_FOUND_PATTERNS):
            return False
        if any(p in low for p in _AUTH_PATTERNS):
            raise AuthError("无权限访问 OBS（403）。详情：%s" % str(exc)[:300])
        raise ApiError("SDK head_object 失败：%s" % str(exc)[:300])
    return True


def sdk_put_object(region, local_path, bucket, key, endpoint=None):
    """SDK fallback upload via ``ObsClient.put_object`` (streams the file)."""
    from huaweicloudsdkobs.v1 import PutObjectRequest
    client = _sdk_client(region, endpoint=endpoint)
    try:
        with open(local_path, "rb") as handle:
            request = PutObjectRequest(
                stream=handle, bucket_name=bucket, object_key=key)
            response = client.put_object(request)
    except OSError as exc:
        raise ObsError("无法读取本地文件 %s：%s" % (local_path, exc))
    except Exception as exc:  # noqa: BLE001
        low = str(exc).lower()
        if any(p in low for p in _AUTH_PATTERNS):
            raise AuthError("无权限上传到 OBS（403），需要 obs:object:put。"
                            "详情：%s" % str(exc)[:300])
        raise ApiError("SDK put_object 失败：%s" % str(exc)[:300])
    return {
        "etag": getattr(response, "e_tag", None),
        "size": _safe_int(getattr(response, "content_length", None)),
    }


def _safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def object_exists(region, bucket, key, endpoint=None):
    """True if the target object exists; KooCLI ``stat`` first, SDK fallback."""
    argv = build_stat_argv(region, bucket, key, endpoint=endpoint)
    try:
        stdout, stderr, returncode = run_hcloud(argv)
    except ConfigError:
        return sdk_object_exists(region, bucket, key, endpoint=endpoint)
    blob = (stdout + " " + stderr)
    if returncode == 0 and _USE_ERROR_MARKER not in blob.lower():
        return True
    if looks_like_not_found(blob):
        return False
    raise classify_hcloud_failure(stdout, stderr, returncode, exists_probe=True)


def upload_file(region, local_path, bucket, key, endpoint=None,
                overwrite=False, verify=True):
    """Upload ``local_path`` to ``obs://bucket/key`` (CLI first, SDK fallback).

    Refuses to overwrite an existing object unless ``overwrite=True``. When
    ``verify=True`` the object is read back after upload and its size compared
    with the local file. Returns a result dict describing what happened.
    """
    if not os.path.isfile(local_path):
        raise ObsError("本地文件不存在或不是普通文件：%s" % local_path)
    local_size = os.path.getsize(local_path)

    existed = object_exists(region, bucket, key, endpoint=endpoint)
    if existed and not overwrite:
        raise OverwriteError(
            "目标对象已存在：obs://%s/%s。为避免误覆盖，默认拒绝上传；"
            "如确需覆盖请显式加 --overwrite。" % (bucket, key)
        )

    uploaded_via = "cli"
    try:
        argv = build_cp_argv(region, local_path, bucket, key, endpoint=endpoint)
        stdout, stderr, returncode = run_hcloud(argv)
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            raise classify_hcloud_failure(stdout, stderr, returncode)
    except ConfigError:
        # hcloud binary missing → one-shot SDK fallback.
        sdk_put_object(region, local_path, bucket, key, endpoint=endpoint)
        uploaded_via = "sdk"

    result = {
        "bucket": bucket,
        "key": key,
        "object_url": build_object_url(bucket, key),
        "local_path": os.path.abspath(local_path),
        "local_size": local_size,
        "existed_before": existed,
        "overwritten": bool(existed and overwrite),
        "uploaded_via": uploaded_via,
        "verified": None,
    }
    if verify:
        result["verified"] = verify_object(
            region, bucket, key, expected_size=local_size, endpoint=endpoint)
    return result


def verify_object(region, bucket, key, expected_size=None, endpoint=None):
    """Read the object metadata back and confirm it exists (and size matches).

    Returns ``{"exists": True, "size": <int|None>, "size_match": <bool|None>}``.
    Raises ``ObsError`` when the object is missing after the upload.
    """
    argv = build_stat_argv(region, bucket, key, endpoint=endpoint)
    try:
        stdout, stderr, returncode = run_hcloud(argv)
        info = parse_stat_output(stdout)
    except ConfigError:
        if not sdk_object_exists(region, bucket, key, endpoint=endpoint):
            raise ObsError("回读校验失败：上传后未找到对象 obs://%s/%s。" % (bucket, key))
        return {"exists": True, "size": None, "size_match": None}

    blob = (stdout + " " + stderr)
    if returncode != 0 or _USE_ERROR_MARKER in blob.lower():
        if looks_like_not_found(blob):
            raise ObsError("回读校验失败：上传后未找到对象 obs://%s/%s。" % (bucket, key))
        raise classify_hcloud_failure(stdout, stderr, returncode)

    size = info.get("size")
    size_match = None
    if expected_size is not None and size is not None:
        size_match = (size == expected_size)
        if not size_match:
            raise ObsError(
                "回读校验失败：对象大小 (%s) 与本地文件 (%s) 不一致：obs://%s/%s。"
                % (size, expected_size, bucket, key)
            )
    return {"exists": True, "size": size, "size_match": size_match}


def result_to_json(result):
    return json.dumps(result, ensure_ascii=False, indent=2)