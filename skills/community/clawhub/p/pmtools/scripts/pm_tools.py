import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional, Tuple


BASE_URL = os.environ.get("FEISHU_OKR_BASE_URL", "https://open.feishu.cn/open-apis/okr/v1").rstrip("/")
OPEN_API_BASE_URL = os.environ.get("FEISHU_OPEN_API_BASE_URL", "https://open.feishu.cn/open-apis").rstrip("/")


def _skill_dir() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _cache_path() -> str:
    override = os.environ.get("PM_TOOLS_UPDATE_CACHE_PATH")
    if override:
        return override
    return os.path.join(os.path.expanduser("~"), ".cache", "pmtools", "update_check.json")


def _token_cache_path() -> str:
    override = os.environ.get("PM_TOOLS_TOKEN_CACHE_PATH")
    if override:
        return override
    return os.path.join(os.path.expanduser("~"), ".cache", "pmtools", "tenant_token.json")


def _read_version() -> str:
    p = os.path.join(_skill_dir(), "VERSION")
    try:
        with open(p, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"


def _ensure_parent_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def _now_ts() -> int:
    return int(time.time())


def _load_json(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def _save_json(path: str, data: dict) -> None:
    _ensure_parent_dir(path)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
    os.replace(tmp, path)


def _run(cmd: List[str], cwd: Optional[str] = None) -> Tuple[int, str]:
    try:
        p = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        return p.returncode, (p.stdout or "").strip()
    except FileNotFoundError:
        return 127, f"command not found: {cmd[0]}"


def self_update() -> dict:
    cache_path = _cache_path()
    cache = _load_json(cache_path)
    last_checked = int(cache.get("last_checked_ts", 0) or 0)
    now = _now_ts()
    if now - last_checked < 7 * 24 * 60 * 60:
        return {"skipped": True, "reason": "checked_within_7_days", "version": _read_version()}

    skill_dir = _skill_dir()
    updated = False
    update_attempts: List[Dict[str, Any]] = []

    if os.path.isdir(os.path.join(skill_dir, ".git")):
        rc, out = _run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], cwd=skill_dir)
        if rc == 0 and out:
            _run(["git", "fetch", "--all", "--prune"], cwd=skill_dir)
            rc2, out2 = _run(["git", "rev-parse", "HEAD"], cwd=skill_dir)
            rc3, out3 = _run(["git", "rev-parse", out], cwd=skill_dir)
            if rc2 == 0 and rc3 == 0 and out2 and out3 and out2 != out3:
                rc4, out4 = _run(["git", "pull", "--ff-only"], cwd=skill_dir)
                updated = rc4 == 0
                update_attempts.append({"type": "git", "updated": updated, "output": out4})
            else:
                update_attempts.append({"type": "git", "updated": False, "output": "no_update"})
        else:
            update_attempts.append({"type": "git", "updated": False, "output": "no_upstream"})

    clawhub_slug = os.environ.get("PM_TOOLS_CLAWHUB_SLUG", "pmtools")
    rc, out = _run(["clawhub", "update", clawhub_slug])
    if rc == 0:
        updated = True
    update_attempts.append({"type": "clawhub", "updated": rc == 0, "output": out})

    cache["last_checked_ts"] = now
    cache["last_checked_version"] = _read_version()
    _save_json(cache_path, cache)

    return {
        "skipped": False,
        "updated": updated,
        "version": _read_version(),
        "attempts": update_attempts,
        "cache_path": cache_path,
    }


def _request_raw(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    json_body: Optional[Dict[str, Any]] = None,
    body_bytes: Optional[bytes] = None,
) -> Dict[str, Any]:
    h: Dict[str, str] = {}
    if headers:
        h.update(headers)

    data = None
    if json_body is not None:
        h["Content-Type"] = "application/json; charset=utf-8"
        data = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
    elif body_bytes is not None:
        data = body_bytes

    req = urllib.request.Request(url=url, method=method, headers=h, data=data)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
        return json.loads(raw.decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            raise RuntimeError(f"http_error: {e.code} {e.reason}")


def _fetch_tenant_access_token(app_id: str, app_secret: str) -> Tuple[str, int]:
    url = OPEN_API_BASE_URL + "/auth/v3/tenant_access_token/internal"
    payload = _request_raw("POST", url, json_body={"app_id": app_id, "app_secret": app_secret})
    if not isinstance(payload, dict) or payload.get("code") != 0:
        raise RuntimeError(json.dumps(payload, ensure_ascii=False))
    token = str(payload.get("tenant_access_token", "") or "").strip()
    expire = int(payload.get("expire", 0) or 0)
    if not token or expire <= 0:
        raise RuntimeError(json.dumps(payload, ensure_ascii=False))
    return token, expire


def _tenant_access_token_from_cache_or_fetch() -> str:
    app_id = os.environ.get("FEISHU_APP_ID", "").strip()
    app_secret = os.environ.get("FEISHU_APP_SECRET", "").strip()
    if not app_id or not app_secret:
        raise RuntimeError("missing env: FEISHU_APP_ID and FEISHU_APP_SECRET")

    cache_path = _token_cache_path()
    cache = _load_json(cache_path)
    now = _now_ts()

    token = str(cache.get("tenant_access_token", "") or "").strip()
    expire_at = int(cache.get("expire_at_ts", 0) or 0)

    if token and expire_at and now < (expire_at - 300):
        return token

    token, expire = _fetch_tenant_access_token(app_id, app_secret)
    cache = {"tenant_access_token": token, "expire_at_ts": now + expire}
    _save_json(cache_path, cache)
    return token


def _tenant_access_token() -> str:
    v = os.environ.get("FEISHU_TENANT_ACCESS_TOKEN", "").strip()
    if v:
        return v
    if os.environ.get("FEISHU_APP_ID", "").strip() and os.environ.get("FEISHU_APP_SECRET", "").strip():
        return _tenant_access_token_from_cache_or_fetch()
    raise RuntimeError("missing tenant auth: set FEISHU_TENANT_ACCESS_TOKEN or (FEISHU_APP_ID + FEISHU_APP_SECRET)")


def _access_token() -> str:
    v = os.environ.get("FEISHU_ACCESS_TOKEN", "").strip()
    if v:
        return v
    v = os.environ.get("FEISHU_USER_ACCESS_TOKEN", "").strip()
    if v:
        return v
    return _tenant_access_token()


def _request(
    method: str,
    path: str,
    token: str,
    query: Optional[Dict[str, Any]] = None,
    json_body: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    body_bytes: Optional[bytes] = None,
) -> Dict[str, Any]:
    url = BASE_URL + path
    if query:
        url += "?" + urllib.parse.urlencode(query, doseq=True)

    h = {"Authorization": f"Bearer {token}"}
    if headers:
        h.update(headers)

    data = None
    if json_body is not None:
        h["Content-Type"] = "application/json; charset=utf-8"
        data = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
    elif body_bytes is not None:
        data = body_bytes

    req = urllib.request.Request(url=url, method=method, headers=h, data=data)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
        parsed = json.loads(raw.decode("utf-8"))
        return parsed
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except Exception:
            raise RuntimeError(f"http_error: {e.code} {e.reason}")
        return parsed


def _assert_ok(payload: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(payload, dict) and payload.get("code", 0) == 0:
        return payload
    raise RuntimeError(json.dumps(payload, ensure_ascii=False))


def periods_create(period_rule_id: str, start_month: str) -> Dict[str, Any]:
    token = _access_token()
    body = {"period_rule_id": period_rule_id, "start_month": start_month}
    return _assert_ok(_request("POST", "/periods", token, json_body=body))


def periods_update_status(period_id: str, status: int) -> Dict[str, Any]:
    token = _access_token()
    body = {"status": status}
    return _assert_ok(_request("PATCH", f"/periods/{period_id}", token, json_body=body))


def periods_list(page_token: Optional[str], page_size: Optional[int]) -> Dict[str, Any]:
    token = _access_token()
    q: dict = {}
    if page_token:
        q["page_token"] = page_token
    if page_size is not None:
        q["page_size"] = page_size
    return _assert_ok(_request("GET", "/periods", token, query=q))


def period_rules_list() -> Dict[str, Any]:
    token = _access_token()
    return _assert_ok(_request("GET", "/period_rules", token))


def user_okrs_list(
    user_id: str,
    offset: str,
    limit: str,
    user_id_type: Optional[str],
    lang: Optional[str],
    period_ids: List[str],
) -> Dict[str, Any]:
    token = _access_token()
    q: dict = {"offset": offset, "limit": limit}
    if user_id_type:
        q["user_id_type"] = user_id_type
    if lang:
        q["lang"] = lang
    if period_ids:
        q["period_ids"] = period_ids
    return _assert_ok(_request("GET", f"/users/{user_id}/okrs", token, query=q))


def okrs_batch_get(okr_ids: List[str], user_id_type: Optional[str], lang: Optional[str]) -> Dict[str, Any]:
    token = _access_token()
    q: dict = {"okr_ids": okr_ids}
    if user_id_type:
        q["user_id_type"] = user_id_type
    if lang:
        q["lang"] = lang
    return _assert_ok(_request("GET", "/okrs/batch_get", token, query=q))


def _plain_text_content(text: str) -> Dict[str, Any]:
    return {
        "blocks": [
            {
                "type": "paragraph",
                "paragraph": {"elements": [{"type": "textRun", "textRun": {"text": text, "style": {}}}]},
            }
        ]
    }


def _load_content(content_json: Optional[str], content_file: Optional[str], text: Optional[str]) -> Dict[str, Any]:
    if content_json:
        return json.loads(content_json)
    if content_file:
        with open(content_file, "r", encoding="utf-8") as f:
            return json.load(f)
    if text is None:
        raise RuntimeError("content is required: provide --text, --content_json, or --content_file")
    return _plain_text_content(text)


def progress_create(
    source_title: str,
    source_url: str,
    target_id: str,
    target_type: int,
    text: Optional[str],
    content_json: Optional[str],
    content_file: Optional[str],
    percent: Optional[float],
    status: Optional[int],
    source_url_pc: Optional[str],
    source_url_mobile: Optional[str],
    user_id_type: Optional[str],
) -> Dict[str, Any]:
    token = _access_token()
    if not re.match(r"^https?://.*$", source_url):
        raise RuntimeError("source_url must match ^https?://.*$")
    body: dict = {
        "source_title": source_title,
        "source_url": source_url,
        "target_id": target_id,
        "target_type": target_type,
        "content": _load_content(content_json, content_file, text),
    }
    if source_url_pc:
        body["source_url_pc"] = source_url_pc
    if source_url_mobile:
        body["source_url_mobile"] = source_url_mobile
    if percent is not None or status is not None:
        pr: dict = {}
        if percent is not None:
            pr["percent"] = percent
        if status is not None:
            pr["status"] = status
        body["progress_rate"] = pr
    q: Dict[str, Any] = {}
    if user_id_type:
        q["user_id_type"] = user_id_type
    return _assert_ok(_request("POST", "/progress_records", token, query=q, json_body=body))


def progress_update(
    progress_id: str,
    text: Optional[str],
    content_json: Optional[str],
    content_file: Optional[str],
    user_id_type: Optional[str],
) -> Dict[str, Any]:
    token = _access_token()
    body: dict = {"content": _load_content(content_json, content_file, text)}
    q: dict = {}
    if user_id_type:
        q["user_id_type"] = user_id_type
    return _assert_ok(_request("PUT", f"/progress_records/{progress_id}", token, query=q, json_body=body))


def progress_delete(progress_id: str) -> Dict[str, Any]:
    token = _access_token()
    return _assert_ok(_request("DELETE", f"/progress_records/{progress_id}", token))


def progress_get(progress_id: str, user_id_type: Optional[str]) -> Dict[str, Any]:
    token = _access_token()
    q: dict = {}
    if user_id_type:
        q["user_id_type"] = user_id_type
    return _assert_ok(_request("GET", f"/progress_records/{progress_id}", token, query=q))


def _multipart_form(fields: Dict[str, str], file_field: str, file_path: str) -> Tuple[bytes, str]:
    boundary = "pmtools" + str(int(time.time() * 1000))
    crlf = "\r\n"

    with open(file_path, "rb") as f:
        file_bytes = f.read()
    filename = os.path.basename(file_path)

    parts: list[bytes] = []
    for k, v in fields.items():
        parts.append(f"--{boundary}{crlf}".encode("utf-8"))
        parts.append(f'Content-Disposition: form-data; name="{k}"{crlf}{crlf}'.encode("utf-8"))
        parts.append(str(v).encode("utf-8"))
        parts.append(crlf.encode("utf-8"))

    parts.append(f"--{boundary}{crlf}".encode("utf-8"))
    parts.append(
        f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"{crlf}'.encode("utf-8")
    )
    parts.append(f"Content-Type: application/octet-stream{crlf}{crlf}".encode("utf-8"))
    parts.append(file_bytes)
    parts.append(crlf.encode("utf-8"))
    parts.append(f"--{boundary}--{crlf}".encode("utf-8"))

    body = b"".join(parts)
    content_type = f"multipart/form-data; boundary={boundary}"
    return body, content_type


def image_upload(file_path: str, target_id: str, target_type: int) -> Dict[str, Any]:
    token = _access_token()
    body, content_type = _multipart_form(
        fields={"target_id": target_id, "target_type": str(target_type)},
        file_field="data",
        file_path=file_path,
    )
    return _assert_ok(_request("POST", "/images/upload", token, headers={"Content-Type": content_type}, body_bytes=body))


def reviews_query(user_ids: List[str], period_ids: List[str], user_id_type: Optional[str]) -> Dict[str, Any]:
    token = _tenant_access_token()
    q: dict = {"user_ids": user_ids, "period_ids": period_ids}
    if user_id_type:
        q["user_id_type"] = user_id_type
    return _assert_ok(_request("GET", "/reviews/query", token, query=q))


def _print(payload: Dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    sys.stdout.write("\n")


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(prog="pmtools")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("self-update")

    p = sub.add_parser("periods-create")
    p.add_argument("--period_rule_id", required=True)
    p.add_argument("--start_month", required=True)

    p = sub.add_parser("periods-update-status")
    p.add_argument("--period_id", required=True)
    p.add_argument("--status", required=True, type=int)

    p = sub.add_parser("periods-list")
    p.add_argument("--page_token")
    p.add_argument("--page_size", type=int)

    sub.add_parser("period-rules-list")

    p = sub.add_parser("user-okrs-list")
    p.add_argument("--user_id", required=True)
    p.add_argument("--offset", required=True)
    p.add_argument("--limit", required=True)
    p.add_argument("--user_id_type")
    p.add_argument("--lang")
    p.add_argument("--period_id", action="append", default=[])

    p = sub.add_parser("okrs-batch-get")
    p.add_argument("--okr_id", action="append", required=True)
    p.add_argument("--user_id_type")
    p.add_argument("--lang")

    p = sub.add_parser("progress-create")
    p.add_argument("--source_title", required=True)
    p.add_argument("--source_url", required=True)
    p.add_argument("--target_id", required=True)
    p.add_argument("--target_type", required=True, type=int)
    p.add_argument("--text")
    p.add_argument("--content_json")
    p.add_argument("--content_file")
    p.add_argument("--percent", type=float)
    p.add_argument("--status", type=int)
    p.add_argument("--source_url_pc")
    p.add_argument("--source_url_mobile")
    p.add_argument("--user_id_type")

    p = sub.add_parser("progress-update")
    p.add_argument("--progress_id", required=True)
    p.add_argument("--text")
    p.add_argument("--content_json")
    p.add_argument("--content_file")
    p.add_argument("--user_id_type")

    p = sub.add_parser("progress-delete")
    p.add_argument("--progress_id", required=True)

    p = sub.add_parser("progress-get")
    p.add_argument("--progress_id", required=True)
    p.add_argument("--user_id_type")

    p = sub.add_parser("image-upload")
    p.add_argument("--file", required=True)
    p.add_argument("--target_id", required=True)
    p.add_argument("--target_type", required=True, type=int)

    p = sub.add_parser("reviews-query")
    p.add_argument("--user_id", action="append", required=True)
    p.add_argument("--period_id", action="append", required=True)
    p.add_argument("--user_id_type")

    args = parser.parse_args(argv)

    try:
        if args.cmd != "self-update" and os.environ.get("PM_TOOLS_DISABLE_AUTO_UPDATE", "").strip() != "1":
            self_update()
        if args.cmd == "self-update":
            _print(self_update())
            return 0
        if args.cmd == "periods-create":
            _print(periods_create(args.period_rule_id, args.start_month))
            return 0
        if args.cmd == "periods-update-status":
            _print(periods_update_status(args.period_id, args.status))
            return 0
        if args.cmd == "periods-list":
            _print(periods_list(args.page_token, args.page_size))
            return 0
        if args.cmd == "period-rules-list":
            _print(period_rules_list())
            return 0
        if args.cmd == "user-okrs-list":
            _print(user_okrs_list(args.user_id, args.offset, args.limit, args.user_id_type, args.lang, args.period_id))
            return 0
        if args.cmd == "okrs-batch-get":
            _print(okrs_batch_get(args.okr_id, args.user_id_type, args.lang))
            return 0
        if args.cmd == "progress-create":
            _print(
                progress_create(
                    source_title=args.source_title,
                    source_url=args.source_url,
                    target_id=args.target_id,
                    target_type=args.target_type,
                    text=args.text,
                    content_json=args.content_json,
                    content_file=args.content_file,
                    percent=args.percent,
                    status=args.status,
                    source_url_pc=args.source_url_pc,
                    source_url_mobile=args.source_url_mobile,
                    user_id_type=args.user_id_type,
                )
            )
            return 0
        if args.cmd == "progress-update":
            _print(
                progress_update(
                    progress_id=args.progress_id,
                    text=args.text,
                    content_json=args.content_json,
                    content_file=args.content_file,
                    user_id_type=args.user_id_type,
                )
            )
            return 0
        if args.cmd == "progress-delete":
            _print(progress_delete(args.progress_id))
            return 0
        if args.cmd == "progress-get":
            _print(progress_get(args.progress_id, args.user_id_type))
            return 0
        if args.cmd == "image-upload":
            _print(image_upload(args.file, args.target_id, args.target_type))
            return 0
        if args.cmd == "reviews-query":
            _print(reviews_query(args.user_id, args.period_id, args.user_id_type))
            return 0
        raise RuntimeError("unknown command")
    except Exception as e:
        sys.stderr.write(str(e).strip() + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
