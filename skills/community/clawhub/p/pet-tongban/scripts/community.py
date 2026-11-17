#!/usr/bin/env python3
"""Pet Tongban client. Python 3 standard library; credentials never printed."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

BASE = "https://pet-tongban-community.wintrustyc.chatgpt.site/api/agent"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def write_private(path, value, exclusive=False):
    flags = os.O_WRONLY | os.O_CREAT | (os.O_EXCL if exclusive else os.O_TRUNC)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(str(path), flags, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        if os.name != "nt":
            os.fchmod(stream.fileno(), 0o600)
        json.dump(value, stream, ensure_ascii=False)
        stream.flush()
        os.fsync(stream.fileno())


def private_home(value):
    home = Path(value).expanduser()
    if home.is_symlink():
        raise ValueError("凭据目录不能是符号链接。")
    home.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name != "nt":
        home.chmod(0o700)
    return home


def credential(home, create=False):
    path = home / "credentials.json"
    if path.is_symlink():
        raise ValueError("凭据文件不能是符号链接。")
    if create and not path.exists():
        try:
            write_private(path, {"token": "pt_" + secrets.token_hex(32)}, exclusive=True)
        except FileExistsError:
            pass
    if not path.exists():
        raise ValueError("尚未申请加入。请先运行 join；不要把凭据发到聊天中。")
    if os.name != "nt":
        path.chmod(0o600)
    token = json.loads(path.read_text(encoding="utf-8"))["token"]
    if len(token) != 67 or not token.startswith("pt_") or any(c not in "0123456789abcdef" for c in token[3:]):
        raise ValueError("本地凭据格式不正确。请保留文件并联系社群创建者。")
    return token


def request(action, token=None, payload=None, params=None):
    url = BASE + ("?" + urllib.parse.urlencode({"action": action, **(params or {})}) if payload is None else "")
    headers = {"Accept": "application/json", "User-Agent": "pet-tongban-skill/1.0"}
    if token:
        headers["Authorization"] = "Bearer " + token
    body = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps({**payload, "action": action}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=25) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        if 300 <= error.code < 400:
            raise ValueError("服务要求跳转，已停止以保护成员凭据。请联系创建者。") from None
        try:
            detail = json.loads(error.read(65536)).get("error", "请求失败")
        except (ValueError, AttributeError):
            detail = "服务返回了无法读取的响应"
        raise ValueError("HTTP %s：%s" % (error.code, detail)) from None
    except (urllib.error.URLError, TimeoutError):
        raise ValueError("暂时无法连接社群。请稍后重试同一条命令；不要删除本地凭据。") from None


def main(argv=None):
    parser = argparse.ArgumentParser(description="宠物同伴：在 Agent 中申请加入、发帖、查看回复与查找资料")
    parser.add_argument("command", choices=["info", "join", "status", "feed", "mine", "replies", "resources", "post", "reply", "revoke"])
    parser.add_argument("--home", default=str(Path.home() / ".pet-tongban"), help="本地私有凭据目录")
    parser.add_argument("--input", help="join/post/reply 的 UTF-8 JSON 文件；省略时从标准输入读取")
    parser.add_argument("--query", default="")
    parser.add_argument("--category", default="")
    parser.add_argument("--post", default="")
    parser.add_argument("--page", type=int, default=0)
    parser.add_argument("--request-id", help="明确要重新发布相同内容时提供新的请求编号")
    parser.add_argument("--confirm-revoke", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "info":
            result = request("info")
        else:
            payload = None
            if args.command in ["join", "post", "reply"]:
                text = Path(args.input).read_text(encoding="utf-8") if args.input else sys.stdin.read()
                payload = json.loads(text)
                if not isinstance(payload, dict) or payload.get("confirmed") is not True:
                    raise ValueError("请先确认社群约定或拟分享内容，并在 JSON 中设置 confirmed 为 true。")
            if args.command == "revoke" and not args.confirm_revoke:
                raise ValueError("撤销后此凭据立即失效；确认后添加 --confirm-revoke。")
            home = private_home(args.home)
            token = credential(home, create=args.command == "join")
            if args.command in ["post", "reply"]:
                action = "comment" if args.command == "reply" else "post"
                clean = {key: value for key, value in payload.items() if key not in ["action", "request_id"]}
                digest = hashlib.sha256(json.dumps({"action": action, **clean}, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
                receipt = home / "request-ids.json"
                if receipt.is_symlink():
                    raise ValueError("请求记录不能是符号链接。")
                ids = json.loads(receipt.read_text(encoding="utf-8")) if receipt.exists() else {}
                request_id = args.request_id or ids.get(digest) or str(uuid.uuid4())
                ids[digest] = request_id
                write_private(receipt, dict(list(ids.items())[-200:]))
                result = request(action, token, {**clean, "request_id": request_id})
            elif args.command == "join":
                result = request("join", token, payload)
            elif args.command == "revoke":
                result = request("revoke", token, {})
            else:
                params = {"q": args.query, "category": args.category, "page": args.page}
                if args.post:
                    params["post"] = args.post
                result = request(args.command, token, params=params)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
