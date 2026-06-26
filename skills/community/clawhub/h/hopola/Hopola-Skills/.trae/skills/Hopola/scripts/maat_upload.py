#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import hmac
import json
import os
import re
import shlex
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_TOKEN_API = "https://strategy.stariidata.com/upload/policy"
DEFAULT_ALLOWED_POLICY_HOSTS = ("strategy.stariidata.com",)
TOKEN_API_ENV_NAME = "MAAT_TOKEN_API"
TOKEN_API_ALLOWED_HOSTS_ENV_NAME = "MAAT_TOKEN_API_ALLOWED_HOSTS"
TOKEN_API_LEGACY_ENV_NAMES = (
    "MEITU_TOKEN_API",
    "NEXT_PUBLIC_MAAT_TOKEN_API",
    "NEXT_PUBLIC_MEITU_TOKEN_API",
)
DEFAULT_UPLOAD_APP = "mhc"
DEFAULT_UPLOAD_TYPE = "proj_1005"
DEFAULT_UPLOAD_VERSION = "2"


class MaatUploadError(RuntimeError):
    PARSE_ERROR = "PARSE_ERROR"
    UPLOAD_ERROR = "UPLOAD_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"

    def __init__(
        self,
        message: str,
        hint: str = "请换一张图片或检查网络后重试",
        error_type: str = UPLOAD_ERROR,
    ):
        super().__init__(message)
        self.hint = hint
        self.error_type = error_type


def _request_log_enabled() -> bool:
    return os.environ.get("OPENCLAW_REQUEST_LOG", "0") != "0"


def _request_log(message: str) -> None:
    if _request_log_enabled():
        print(f"[REQUEST] {message}", file=sys.stderr)


def _request_log_as_curl(parts: List[str]) -> None:
    if not _request_log_enabled():
        return
    print("[REQUEST] " + shlex.join(parts), file=sys.stderr)


def _request_log_response_json(label: str, text: str, http_code: Optional[int] = None) -> None:
    if not _request_log_enabled():
        return
    try:
        max_len = int(os.environ.get("OPENCLAW_REQUEST_LOG_BODY_MAX", "20000"))
    except ValueError:
        max_len = 20000
    body_text = text[:max_len] + ("...(truncated)" if len(text) > max_len else "")
    try:
        body_obj: Any = json.loads(body_text)
        body_obj = _redact_sensitive(body_obj)
        payload: Any = {"http_code": http_code, "body": body_obj} if http_code is not None else body_obj
    except json.JSONDecodeError:
        payload = (
            {"http_code": http_code, "_raw": _redact_text(body_text)}
            if http_code is not None
            else {"_raw": _redact_text(body_text)}
        )
    print(f"[REQUEST] {label} (JSON):", file=sys.stderr)
    print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)


def _clean_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _clean_bool(value: Any, default: bool = True) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return value != 0
    text = _clean_str(value).lower()
    if not text:
        return default
    if text in ("1", "true", "yes", "y", "on"):
        return True
    if text in ("0", "false", "no", "n", "off"):
        return False
    return default


def _audit_log(event: str, payload: Dict[str, Any]) -> None:
    print(f"[AUDIT] {json.dumps({'event': event, **payload}, ensure_ascii=False)}", file=sys.stderr)


def _normalize_host(value: str) -> str:
    return _clean_str(value).lower().strip(".")


def _resolve_allowed_policy_hosts() -> List[str]:
    configured = _clean_str(os.environ.get(TOKEN_API_ALLOWED_HOSTS_ENV_NAME))
    default_hosts = [_normalize_host(host) for host in DEFAULT_ALLOWED_POLICY_HOSTS if _normalize_host(host)]
    if not configured:
        return default_hosts
    hosts: List[str] = []
    for part in configured.split(","):
        host = _normalize_host(part)
        if host and host not in hosts:
            hosts.append(host)
    for host in default_hosts:
        if host not in hosts:
            hosts.append(host)
    return hosts


def _resolve_token_api() -> str:
    value = _clean_str(os.environ.get(TOKEN_API_ENV_NAME))
    source = TOKEN_API_ENV_NAME
    if not value:
        for legacy_env in TOKEN_API_LEGACY_ENV_NAMES:
            legacy_value = _clean_str(os.environ.get(legacy_env))
            if legacy_value:
                value = legacy_value
                source = legacy_env
                break
    if not value:
        value = DEFAULT_TOKEN_API
        source = "default"
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise MaatUploadError(
            f"上传策略端点格式非法: {value}",
            f"请设置有效的 {TOKEN_API_ENV_NAME} 或使用默认端点",
            MaatUploadError.VALIDATION_ERROR,
        )
    host = _normalize_host(parsed.hostname or parsed.netloc)
    allowed_hosts = _resolve_allowed_policy_hosts()
    if host not in allowed_hosts:
        raise MaatUploadError(
            f"上传策略端点主机不在允许列表: {host}",
            f"请检查 {TOKEN_API_ENV_NAME} 或在 {TOKEN_API_ALLOWED_HOSTS_ENV_NAME} 中显式允许该主机",
            MaatUploadError.VALIDATION_ERROR,
        )
    normalized = _normalize_http_url(value)
    _audit_log(
        "upload_policy_endpoint_resolved",
        {
            "source": source,
            "host": host,
            "allowed_hosts": allowed_hosts,
            "endpoint": urllib.parse.urlunsplit(
                (
                    parsed.scheme,
                    parsed.netloc,
                    _collapse_path_slashes(parsed.path or "/"),
                    "",
                    "",
                )
            ),
        },
    )
    if source in TOKEN_API_LEGACY_ENV_NAMES:
        _audit_log(
            "upload_policy_endpoint_legacy_env_used",
            {"legacy_env": source, "preferred_env": TOKEN_API_ENV_NAME},
        )
    return normalized


def _resolve_upload_app() -> str:
    return (
        _clean_str(os.environ.get("MEITU_UPLOAD_APP"))
        or _clean_str(os.environ.get("NEXT_PUBLIC_MEITU_UPLOAD_APP"))
        or DEFAULT_UPLOAD_APP
    )


def _resolve_upload_type() -> str:
    return (
        _clean_str(os.environ.get("MEITU_UPLOAD_TYPE"))
        or _clean_str(os.environ.get("NEXT_PUBLIC_MEITU_UPLOAD_TYPE"))
        or DEFAULT_UPLOAD_TYPE
    )


def _resolve_upload_version() -> str:
    return _clean_str(os.environ.get("MAAT_UPLOAD_VERSION")) or DEFAULT_UPLOAD_VERSION


def _collapse_path_slashes(path: str) -> str:
    if not path:
        return path
    leading = "/" if path.startswith("/") else ""
    trailing = "/" if path.endswith("/") and path != "/" else ""
    body = re.sub(r"/{2,}", "/", path)
    if leading and not body.startswith("/"):
        body = "/" + body
    if trailing and not body.endswith("/"):
        body = body + "/"
    return body


def _normalize_http_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    path = _collapse_path_slashes(parsed.path or "/")
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, parsed.fragment))


def _redact_text(text: str) -> str:
    if not text:
        return text
    redacted = text
    redacted = re.sub(
        r"(?i)\b(token|policy|signature|x-amz-signature|x-amz-security-token|authorization)\b\s*[:=]\s*([^\s\",]+)",
        r"\1=<redacted>",
        redacted,
    )
    redacted = re.sub(
        r"(?i)([?&](token|policy|signature|x-amz-signature|x-amz-security-token|access_key|secret_key|session_token)=)[^&\s]+",
        r"\1<redacted>",
        redacted,
    )
    return redacted


def _redact_sensitive(value: Any, key: str = "") -> Any:
    sensitive_keywords = (
        "token",
        "policy",
        "signature",
        "secret",
        "authorization",
        "credential",
        "access_key",
        "secret_key",
        "session_token",
    )
    key_norm = _clean_str(key).lower()
    if any(keyword in key_norm for keyword in sensitive_keywords):
        return "<redacted>"
    if isinstance(value, dict):
        return {k: _redact_sensitive(v, k) for k, v in value.items()}
    if isinstance(value, list):
        return [_redact_sensitive(item, key) for item in value]
    if isinstance(value, str):
        return _redact_text(value)
    return value


def _extract_markdown_image_source(value: str) -> str:
    text = value.strip()
    md_match = re.fullmatch(r"!\[[^\]]*\]\(([^)]+)\)", text)
    if md_match:
        text = md_match.group(1).strip()
    if len(text) >= 2 and text[0] == "<" and text[-1] == ">":
        text = text[1:-1].strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in ("'", '"'):
        text = text[1:-1].strip()
    return text


def _normalize_local_path(path: str) -> str:
    cleaned = unicodedata.normalize("NFC", path).replace("\\", "/")
    collapsed = _collapse_path_slashes(cleaned)
    if not collapsed.startswith("/"):
        collapsed = os.path.abspath(collapsed)
    return os.path.normpath(collapsed)


def _session_reference_candidates(raw_value: str) -> List[str]:
    value = _extract_markdown_image_source(_clean_str(raw_value))
    if not value:
        raise MaatUploadError("输入图片引用为空", "请重新上传图片或提供有效本地文件路径", MaatUploadError.PARSE_ERROR)
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme in ("http", "https"):
        normalized = _normalize_http_url(value)
        raise MaatUploadError(
            f"输入是远程 URL，当前脚本仅接收本地/会话文件: {normalized}",
            "请传入会话附件路径或本地文件路径，由上传子流程统一处理 URL 复用",
            MaatUploadError.PARSE_ERROR,
        )
    candidates: List[str] = []
    if parsed.scheme == "file":
        candidates.append(urllib.request.url2pathname(parsed.path or ""))
    elif parsed.scheme in ("session", "attachment", "openclaw", "channel", "sandbox", "local"):
        rel = _clean_str(f"{parsed.netloc}{parsed.path}").lstrip("/")
        if rel:
            rel = _collapse_path_slashes(urllib.parse.unquote(rel))
            candidates.append(f"/mnt/data/{rel}")
            candidates.append(f"/mnt/data/session_uploads/{os.path.basename(rel)}")
    elif re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", value):
        raise MaatUploadError(
            f"不支持的图片引用协议: {parsed.scheme}",
            "请改用本地文件路径、会话附件路径或 markdown 图片本地源",
            MaatUploadError.PARSE_ERROR,
        )
    else:
        candidates.append(value)
    if "session_uploads/" in value:
        suffix = value.split("session_uploads/", 1)[1].lstrip("/")
        if suffix:
            candidates.append(f"/mnt/data/session_uploads/{suffix}")
    unique: List[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        normalized = _normalize_local_path(candidate)
        if normalized in seen:
            continue
        seen.add(normalized)
        unique.append(normalized)
    return unique


def _normalize_session_reference(raw_value: str) -> str:
    candidates = _session_reference_candidates(raw_value)
    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate
    first = candidates[0] if candidates else _clean_str(raw_value)
    raise MaatUploadError(
        f"会话图片引用无法解析为可读文件: {first}",
        "请检查附件是否仍可访问，或重新上传后再试",
        MaatUploadError.PARSE_ERROR,
    )


def _normalize_delivery_url(url: str) -> str:
    value = _clean_str(url)
    if not value:
        raise MaatUploadError("上传返回链接为空", "请稍后重试，若持续失败请更换图片", MaatUploadError.VALIDATION_ERROR)
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise MaatUploadError(
            f"上传返回链接格式非法: {value}",
            "请稍后重试，若持续失败请检查上传凭证配置",
            MaatUploadError.VALIDATION_ERROR,
        )
    return _normalize_http_url(value)


def _validate_accessibility(url: str) -> None:
    methods = ("HEAD", "GET")
    last_error = ""
    for method in methods:
        req = urllib.request.Request(url, method=method, headers={"User-Agent": "hopola-maat-upload/1.0"})
        if method == "GET":
            req.add_header("Range", "bytes=0-0")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                code = resp.getcode() or 200
                if 200 <= code < 400:
                    _request_log(f"url accessibility ok via {method}, status={code}, url={url}")
                    return
                last_error = f"{method} status={code}"
        except urllib.error.HTTPError as e:
            last_error = f"{method} http_error={e.code}"
        except Exception as e:
            last_error = f"{method} error={e}"
    raise MaatUploadError(
        f"上传成功但链接不可访问: {url} ({last_error})",
        "请稍后重试，若多次失败请检查网络或联系管理员",
        MaatUploadError.VALIDATION_ERROR,
    )


def suffix_and_mime(file_path: str) -> Tuple[str, str]:
    ext = file_path.rsplit(".", 1)[-1].lower() if "." in file_path else ""
    if ext in ("jpg", "jpeg"):
        return ext or "jpg", "image/jpeg"
    if ext == "png":
        return "png", "image/png"
    if ext == "webp":
        return "webp", "image/webp"
    if ext == "gif":
        return "gif", "image/gif"
    if ext == "svg":
        return "svg", "image/svg+xml"
    return "jpg", "image/jpeg"


def _choose_provider(item: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    order = item.get("order")
    candidates: List[str] = []
    if isinstance(order, list):
        for entry in order:
            name = _clean_str(entry)
            if name:
                candidates.append(name)
    candidates.extend(["oss", "aws_s3", "hw_s3", "qiniu", "mtyun"])
    seen: set[str] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        value = item.get(candidate)
        if isinstance(value, dict):
            return candidate, value
    raise MaatUploadError("获取上传凭证失败：响应中未找到可用云厂商 token")


def _request_upload_policy(suffix: str) -> Dict[str, Any]:
    query = {
        "app": _resolve_upload_app(),
        "type": _resolve_upload_type(),
        "count": "1",
        "version": _resolve_upload_version(),
    }
    if suffix:
        query["suffix"] = suffix
    token_api = _resolve_token_api()
    policy_url = f"{token_api}?{urllib.parse.urlencode(query)}"
    _request_log_as_curl(
        [
            "curl",
            "-s",
            "--max-time",
            "30",
            "-G",
            token_api,
            "--data-urlencode",
            f"app={query['app']}",
            "--data-urlencode",
            "count=1",
            "--data-urlencode",
            f"suffix={suffix}",
            "--data-urlencode",
            f"type={query['type']}",
            "--data-urlencode",
            f"version={query['version']}",
        ]
    )
    req = urllib.request.Request(policy_url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            code = resp.getcode() or 200
            raw = resp.read().decode("utf-8", errors="replace")
            _request_log_response_json("policy_response_body", raw, code)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        _request_log_response_json("policy_response_body", raw, e.code)
        raise MaatUploadError(f"获取上传凭证失败({e.code}): {raw[:500]}") from e
    except Exception as e:
        raise MaatUploadError(f"获取上传凭证失败: {e}") from e

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        raise MaatUploadError(f"获取上传凭证失败：响应不是 JSON。原始响应: {raw[:300]}") from e

    if not isinstance(payload, list) or not payload:
        raise MaatUploadError("获取上传凭证失败：响应为空数组")
    item = payload[0]
    if not isinstance(item, dict):
        raise MaatUploadError("获取上传凭证失败：响应结构异常")
    _, provider = _choose_provider(item)
    return provider


def _normalize_policy_token(raw_token: Dict[str, Any]) -> Dict[str, Any]:
    raw_cred = raw_token.get("credentials")
    if not isinstance(raw_cred, dict):
        raw_cred = {}
    return {
        "token": _clean_str(raw_token.get("token")),
        "bucket": _clean_str(raw_token.get("bucket")),
        "key": _clean_str(raw_token.get("key")),
        "url": _normalize_http_url(_clean_str(raw_token.get("url"))) if _clean_str(raw_token.get("url")) else "",
        "data_url": _normalize_http_url(_clean_str(raw_token.get("data"))) if _clean_str(raw_token.get("data")) else "",
        "access_url": _normalize_http_url(_clean_str(raw_token.get("access_url") or raw_token.get("accessUrl")))
        if _clean_str(raw_token.get("access_url") or raw_token.get("accessUrl"))
        else "",
        "region": _clean_str(raw_token.get("region")),
        "use_virtual_host": _clean_bool(
            raw_token.get("use_virtual_host")
            if raw_token.get("use_virtual_host") is not None
            else raw_token.get("useVirtualHost"),
            True,
        ),
        "credentials": {
            "access_key": _clean_str(raw_cred.get("access_key") or raw_cred.get("accessKey")),
            "secret_key": _clean_str(raw_cred.get("secret_key") or raw_cred.get("secretKey")),
            "session_token": _clean_str(raw_cred.get("session_token") or raw_cred.get("sessionToken")),
        },
    }


def _has_s3_token(token: Dict[str, Any]) -> bool:
    cred = token.get("credentials", {})
    return all(
        (
            token.get("bucket"),
            token.get("key"),
            token.get("url"),
            token.get("region"),
            cred.get("access_key"),
            cred.get("secret_key"),
            cred.get("session_token"),
        )
    )


def _has_legacy_token(token: Dict[str, Any]) -> bool:
    return all((token.get("token"), token.get("key"), token.get("url")))


def _build_upload_url(token: Dict[str, Any]) -> str:
    url = _clean_str(token.get("url"))
    bucket = _clean_str(token.get("bucket"))
    key = _clean_str(token.get("key"))
    if not url:
        raise MaatUploadError("上传凭证不完整（url 缺失）")
    if url.find(f"{bucket}.") >= 0:
        return _normalize_http_url(url)
    if bucket and token.get("use_virtual_host", True):
        return _normalize_http_url(re.sub(r"^(https?://)", rf"\1{bucket}.", url, count=1))
    if bucket and key:
        return _normalize_http_url(f"{url.rstrip('/')}/{bucket}/{key}")
    return _normalize_http_url(url)


def _build_s3_fields(token: Dict[str, Any], mime_type: str) -> Dict[str, str]:
    cred = token["credentials"]
    now = dt.datetime.now(dt.timezone.utc)
    expiration = (now + dt.timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    yyyymmdd = now.strftime("%Y%m%d")
    x_amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    key_prefix = f"{token['key'].split('/', 1)[0]}/" if "/" in token["key"] else ""
    mime_prefix = f"{mime_type.split('/', 1)[0]}/" if "/" in mime_type else ""
    credential = f"{cred['access_key']}/{yyyymmdd}/{token['region']}/s3/aws4_request"
    form_fields: Dict[str, str] = {
        "success_action_status": "200",
        "X-Amz-Credential": credential,
        "X-Amz-Algorithm": "AWS4-HMAC-SHA256",
        "X-Amz-Security-Token": cred["session_token"],
        "X-Amz-Date": x_amz_date,
    }
    policy = {
        "expiration": expiration,
        "conditions": [
            {"bucket": token["bucket"]},
            ["starts-with", "$key", key_prefix],
            ["starts-with", "$Content-Type", mime_prefix],
            *[{k: v} for k, v in form_fields.items()],
        ],
    }
    policy_b64 = base64.b64encode(json.dumps(policy, separators=(",", ":")).encode("utf-8")).decode("utf-8")
    date_key = hmac.new(f"AWS4{cred['secret_key']}".encode("utf-8"), yyyymmdd.encode("utf-8"), hashlib.sha256).digest()
    region_key = hmac.new(date_key, token["region"].encode("utf-8"), hashlib.sha256).digest()
    service_key = hmac.new(region_key, b"s3", hashlib.sha256).digest()
    signing_key = hmac.new(service_key, b"aws4_request", hashlib.sha256).digest()
    signature = hmac.new(signing_key, policy_b64.encode("utf-8"), hashlib.sha256).hexdigest()
    return {
        **form_fields,
        "Policy": policy_b64,
        "X-Amz-Signature": signature,
    }


def _multipart_body(fields: Dict[str, str], file_path: str, mime_type: str) -> Tuple[bytes, str]:
    boundary = f"----maat-{uuid.uuid4().hex}"
    boundary_bytes = boundary.encode("utf-8")
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    file_name = os.path.basename(file_path)
    chunks: List[bytes] = []
    for name, value in fields.items():
        chunks.extend(
            [
                b"--" + boundary_bytes + b"\r\n",
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"),
                str(value).encode("utf-8"),
                b"\r\n",
            ]
        )
    chunks.extend(
        [
            b"--" + boundary_bytes + b"\r\n",
            f'Content-Disposition: form-data; name="file"; filename="{file_name}"\r\n'.encode("utf-8"),
            f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"),
            file_bytes,
            b"\r\n",
            b"--" + boundary_bytes + b"--\r\n",
        ]
    )
    return b"".join(chunks), boundary


def _post_multipart(upload_url: str, fields: Dict[str, str], file_path: str, mime_type: str) -> Tuple[int, str]:
    redacted_fields = {"token", "Policy", "X-Amz-Signature", "X-Amz-Security-Token", "X-Amz-Credential"}
    curl_parts: List[str] = ["curl", "-s", "--max-time", "120", "-X", "POST"]
    for k, v in fields.items():
        if k in redacted_fields:
            curl_parts.extend(["-F", f"{k}=<redacted>"])
        else:
            curl_parts.extend(["-F", f"{k}={v}"])
    curl_parts.extend(["-F", f"file=@{file_path};type={mime_type}", upload_url])
    _request_log_as_curl(curl_parts)
    body, boundary = _multipart_body(fields, file_path, mime_type)
    req = urllib.request.Request(upload_url, data=body, method="POST")
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            code = resp.getcode() or 200
            raw = resp.read().decode("utf-8", errors="replace")
            _request_log_response_json("upload_response_body", raw, code)
            return code, raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        _request_log_response_json("upload_response_body", raw, e.code)
        raise MaatUploadError(f"上传失败({e.code}): {raw[:600]}") from e
    except Exception as e:
        raise MaatUploadError(f"上传失败: {e}") from e


def _upload_via_legacy(token: Dict[str, Any], file_path: str, mime_type: str) -> str:
    upload_url = f"{token['url'].rstrip('/')}/"
    fields = {
        "token": token["token"],
        "key": token["key"],
        "fname": os.path.basename(file_path),
    }
    _, raw = _post_multipart(upload_url, fields, file_path, mime_type)
    url = token.get("access_url") or token.get("data_url")
    if raw.strip():
        try:
            body = json.loads(raw)
            data = body.get("data")
            if isinstance(data, str) and data.strip():
                url = data.strip()
        except json.JSONDecodeError:
            pass
    if not url:
        raise MaatUploadError("上传失败，无法获取图片 URL")
    return _normalize_delivery_url(str(url))


def _upload_via_s3(token: Dict[str, Any], file_path: str, mime_type: str) -> str:
    upload_url = _build_upload_url(token)
    fields = {
        "key": token["key"],
        "Content-Type": mime_type,
        **_build_s3_fields(token, mime_type),
    }
    _post_multipart(upload_url, fields, file_path, mime_type)
    url = token.get("access_url") or token.get("data_url")
    if not url:
        raise MaatUploadError("上传成功但凭证中缺少 access_url/data")
    return _normalize_delivery_url(str(url))


def upload_local_file(file_path: str) -> str:
    normalized_file_path = _normalize_session_reference(file_path)
    suffix, mime_type = suffix_and_mime(normalized_file_path)
    raw_token = _request_upload_policy(suffix)
    token = _normalize_policy_token(raw_token)
    if _has_s3_token(token):
        cdn_url = _upload_via_s3(token, normalized_file_path, mime_type)
    elif _has_legacy_token(token):
        cdn_url = _upload_via_legacy(token, normalized_file_path, mime_type)
    else:
        raise MaatUploadError("上传凭证不完整（既不是 S3/STS，也不是 legacy token）")
    normalized_url = _normalize_delivery_url(cdn_url)
    _validate_accessibility(normalized_url)
    _request_log(f"upload ok, source={normalized_file_path}, cdn_url={normalized_url}")
    return normalized_url


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Upload local file via MAAT policy service")
    parser.add_argument("--file", required=True, help="Local file path")
    parser.add_argument("--json", action="store_true", help="Output JSON envelope")
    args = parser.parse_args(argv)
    try:
        url = upload_local_file(args.file)
    except MaatUploadError as e:
        if args.json:
            out = {"ok": False, "error_type": e.error_type, "message": str(e), "user_hint": e.hint}
            print(json.dumps(out, ensure_ascii=False))
        else:
            print(str(e), file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({"ok": True, "url": url}, ensure_ascii=False))
    else:
        print(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
