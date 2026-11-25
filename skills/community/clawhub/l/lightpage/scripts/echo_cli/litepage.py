"""LitePage's small, standalone publishing command surface."""

import argparse
import base64
import hashlib
import json
import os
import re
import socket
import sys
import tempfile
import uuid
from pathlib import Path
from urllib.parse import urlparse

from echo_cli import litepage_access, litepage_mail, litepage_referrals, transport
from echo_cli.client import API, APIError, checked
from echo_cli.compat import subparsers, unlink
from echo_cli.credentials import CredentialStore, atomic_json
from echo_cli.litepage_bundle import bundle
from echo_cli.litepage_feedback import submit as submit_feedback
from echo_cli.litepage_tags import exact as exact_tag
from echo_cli.litepage_tags import parse as parse_tags
from echo_cli.notices import output as notice_output
from echo_cli.qr import create_login_qr, png
from echo_cli.skill_version import LITEPAGE_SKILL_VERSION

DEFAULT_SERVER = "https://lightpage.hqdx.store"


def credential_store(server, directory):
    store = CredentialStore(server, directory=directory)
    # The official product moved its API origin, but both hosts use the same
    # hosting devices. Keep the old file (and lock) instead of copying secrets.
    if server == DEFAULT_SERVER and not store.path.exists() and not store.pending_path.exists():
        legacy = CredentialStore("https://echo.hqdx.store", directory=directory)
        if legacy.path.exists():
            return legacy
    return store


class LitePageAPI(API):
    skill_name = "lightpage"
    skill_version = LITEPAGE_SKILL_VERSION

    def prepare_login_body(self, body):
        receipt = litepage_referrals.pending(self)
        return {**body, **litepage_referrals.fields(receipt)}

    def request(self, method, path, **kwargs):
        if path in {"/v1/hosting/feedback"}:
            # Anonymous feedback never reads credentials, refreshes or registers.
            kwargs.pop("authenticated", None)
            return checked(self.send(method, path, retry=True, **kwargs))
        return super().request(method, path, **kwargs)

    def send(self, method, path, **kwargs):
        if path in {"/v1/hosting/feedback"}:
            kwargs["headers"] = {
                k: v for k, v in kwargs.get("headers", {}).items() if k.lower() != "authorization"
            }
        if path in {"/v1/auth/anonymous", "/v1/auth/connect", "/v1/auth/bind", "/v1/me"}:
            path = path.replace("/v1/", "/v1/hosting/", 1)
        response = super().send(method, path, **kwargs)
        receipt = kwargs.get("json", {}).get("lp_ref") or kwargs.get("json", {}).get(
            "referral_receipt"
        )
        if receipt and path == "/v1/hosting/auth/anonymous" and response.status_code < 300:
            litepage_referrals.acknowledge(
                self, receipt, response.json().get("referral_status", "submitted")
            )
        return response


def read_size(value):
    try:
        size = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Use an integer from 1 to 262144") from None
    if not 1 <= size <= 262144:
        raise argparse.ArgumentTypeError("Use an integer from 1 to 262144")
    return size


def profile_uid(value):
    if not re.fullmatch(r"[a-z0-9]{10}", value):
        raise argparse.ArgumentTypeError("UID must be 10 lowercase letters or digits")
    return value


def profile_limit(value):
    try:
        limit = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Use an integer from 1 to 20") from None
    if not 1 <= limit <= 20:
        raise argparse.ArgumentTypeError("Use an integer from 1 to 20")
    return limit


def profile_cursor(value):
    if not value or len(value) > 400:
        raise argparse.ArgumentTypeError("Cursor must contain 1–400 characters")
    return value


def parser():
    root = argparse.ArgumentParser(
        prog="litepage", description="轻页 LitePage · 发布静态网页、管理作品与收发站内信"
    )
    root.add_argument("--server", default=os.getenv("LITEPAGE_SERVER", DEFAULT_SERVER))
    commands = subparsers(root, dest="command")
    litepage_referrals.commands(commands)
    read = commands.add_parser("read", help="Read a bounded HTML document and record Agent visits")
    read.add_argument("url")
    read.add_argument("--read-id", type=uuid.UUID, default=None)
    read.add_argument("--cursor", default=None)
    read.add_argument("--max-bytes", type=read_size, default=65536, metavar="1-262144")
    capabilities = commands.add_parser(
        "capabilities", help="Discover platform capabilities and read integration instructions"
    )
    capabilities.add_argument("name", nargs="?")
    litepage_mail.commands(commands)
    litepage_access.commands(commands)
    profile = commands.add_parser("profile", help="Read public profiles or update your own profile")
    profile_commands = subparsers(profile, dest="profile_command")
    show_profile = profile_commands.add_parser(
        "show", help="Read profile and public work statistics"
    )
    show_profile.add_argument("--uid", type=profile_uid, help="Omit for your own profile")
    works_profile = profile_commands.add_parser(
        "works", help="Read one page of public work summaries"
    )
    works_profile.add_argument("--uid", type=profile_uid, help="Omit for your own public works")
    works_profile.add_argument("--limit", type=profile_limit, default=10, metavar="1-20")
    works_profile.add_argument("--cursor", type=profile_cursor)
    edit_profile = profile_commands.add_parser("update")
    name = edit_profile.add_mutually_exclusive_group()
    name.add_argument(
        "--name", "--nickname", dest="name", help="Display name, at most 80 characters"
    )
    name.add_argument("--reset-name", action="store_true", help="Use provider display name again")
    avatar = edit_profile.add_mutually_exclusive_group()
    avatar.add_argument("--avatar-url", help="Public HTTPS image URL")
    avatar.add_argument("--reset-avatar", action="store_true", help="Use provider avatar again")
    edit_profile.add_argument(
        "--signature", help="Profile signature, at most 160 characters; empty clears"
    )
    edit_profile.add_argument(
        "--revision", type=int, help="Expected profile revision; omit to read current profile"
    )
    for name in ("publish", "update"):
        cmd = commands.add_parser(name)
        if name == "update":
            cmd.add_argument("site_id", type=uuid.UUID)
        cmd.add_argument("source", type=Path)
        cmd.add_argument("--title")
        cmd.add_argument(
            "--password-file",
            type=Path,
            help="UTF-8 file containing a sharing password; never printed",
        )
        selection = cmd.add_mutually_exclusive_group()
        selection.add_argument("--visibility", choices=["public", "private"])
        selection.add_argument("--sharing", choices=["public", "link", "password", "approval"])
        home = cmd.add_mutually_exclusive_group()
        home.add_argument(
            "--without-home",
            dest="home_enabled",
            action="store_false",
            default=None,
            help="Hide the standard Home entry; preserve on subsequent updates",
        )
        home.add_argument(
            "--with-home",
            dest="home_enabled",
            action="store_true",
            help="Restore the standard Home entry",
        )
        tags = cmd.add_mutually_exclusive_group()
        tags.add_argument("--tags", help="Comma-separated tags (English or Chinese comma)")
        tags.add_argument("--clear-tags", action="store_true", help="Remove all tags")
        cmd.add_argument("--description")
        cmd.add_argument("--preview", type=Path, help="Local webpage screenshot (PNG/JPEG/WebP)")
        cmd.add_argument(
            "--operation-id", type=uuid.UUID, help="Reuse this ID after an uncertain result"
        )
        cmd.add_argument(
            "--check", action="store_true", help="Validate locally; no registration or upload"
        )
    qr = commands.add_parser("qr", help="Generate a share-link PNG locally, only on request")
    qr.add_argument("url", help="Exact published work URL")
    qr.add_argument(
        "--output", type=Path, required=True, help="Output PNG; missing directories are created"
    )
    qr.add_argument(
        "--overwrite", action="store_true", help="Replace output after user confirmation"
    )
    tags = commands.add_parser("tags", help="Change tags without uploading content")
    tags.add_argument("site_id", type=uuid.UUID)
    choice = tags.add_mutually_exclusive_group(required=True)
    choice.add_argument("--tags")
    choice.add_argument("--clear", action="store_true")
    tags.add_argument("--revision", type=int)
    status = commands.add_parser("status")
    status.add_argument("site_id", type=uuid.UUID)
    claim = commands.add_parser("claim", help="Get a private creator WeChat claim link")
    claim.add_argument("site_id", type=uuid.UUID)
    listing = commands.add_parser("list")
    listing.add_argument("--limit", type=int, choices=range(1, 51), default=10, metavar="1-50")
    listing.add_argument("--cursor")
    filters = listing.add_mutually_exclusive_group()
    filters.add_argument("--tag", help="Filter by a single exact tag")
    filters.add_argument("--untagged", action="store_true")
    commands.add_parser("usage")
    analytics = commands.add_parser("analytics", help="Read owned works' visit statistics")
    analytics.add_argument("site_id", type=uuid.UUID, nargs="?", help="Omit for all owned works")
    analytics.add_argument("--days", type=int, choices=range(1, 31), default=7, metavar="1-30")
    feedback = commands.add_parser("feedback", help="Contact the LitePage maintainer without login")
    message = feedback.add_mutually_exclusive_group(required=True)
    message.add_argument("--text", help="Feedback body, at most 5000 characters")
    message.add_argument("--text-file", type=Path, help="UTF-8 feedback file")
    feedback.add_argument("--work-url", help="Optional related work URL")
    feedback.add_argument("--contact", help="Optional, unverified reply contact")
    feedback.add_argument(
        "--operation-id", type=uuid.UUID, help="Reuse this ID after an uncertain result"
    )
    visibility = commands.add_parser("visibility")
    visibility.add_argument("site_id", type=uuid.UUID)
    visibility.add_argument("value", choices=["public", "private"])
    visibility.add_argument("--revision", type=int, required=True)
    password = commands.add_parser("password", help="Set, change or remove sharing password")
    password.add_argument("site_id", type=uuid.UUID)
    choice = password.add_mutually_exclusive_group(required=True)
    choice.add_argument("--password-file", type=Path)
    choice.add_argument("--remove", action="store_true")
    password.add_argument(
        "--revision", type=int, help="Expected revision; omit to read current site status"
    )
    unpublish = commands.add_parser("unpublish")
    unpublish.add_argument("site_id", type=uuid.UUID)
    unpublish.add_argument("--revision", type=int, required=True)
    deletion = commands.add_parser(
        "delete",
        help="Preview one permanent deletion; confirm only after the user's second approval",
    )
    deletion.add_argument("site_id", type=uuid.UUID)
    deletion.add_argument(
        "--confirm-token",
        help="Token from this work's preview; supply only after explicit user confirmation",
    )
    login = commands.add_parser("login")
    login.add_argument("--wechat", action="store_true", required=True)
    login.add_argument("--force", action="store_true")
    commands.add_parser("bind-wechat")
    commands.add_parser("logout")
    return root


def share_qr(url, output, overwrite=False):
    """Encode a published work link offline, without identity or API access."""
    target = urlparse(url)
    if (
        target.scheme != "https"
        or not target.hostname
        or target.username
        or target.password
        or target.query
        or target.fragment
        or not re.fullmatch(r"/p/(?:[a-z0-9]{8}|[0-9a-f]{32})/", target.path)
    ):
        raise RuntimeError("Use the exact published HTTPS work URL, not a private claim link")
    path = output.expanduser().absolute()
    if path.suffix.lower() != ".png":
        raise RuntimeError("QR output must be a .png file")
    data = png(url)
    path.parent.mkdir(parents=True, exist_ok=True)
    if overwrite:
        fd, temporary = tempfile.mkstemp(prefix=".share-qr-", suffix=".png", dir=str(path.parent))
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
            os.replace(temporary, str(path))
        finally:
            unlink(Path(temporary))
    else:
        try:
            with path.open("xb") as stream:
                stream.write(data)
        except FileExistsError:
            raise FileExistsError(
                "二维码文件已存在。请询问用户：换文件名还是覆盖？确认覆盖后才添加 --overwrite。"
            ) from None
    return {"url": url, "qr_path": str(path)}


def ensure_identity(api):
    with api.store.lock():
        saved = api.store.load()
    if saved is None:
        api.native_login(socket.gethostname(), mode="anonymous", agent="轻页创作者")
        print("已创建匿名轻页身份：请保留本机凭证；绑定微信后可跨设备恢复。", file=sys.stderr)
    else:
        receipt = litepage_referrals.pending(api)
        if receipt:
            result = api.request(
                "POST",
                "/v1/hosting/referrals/source",
                authenticated=True,
                json=litepage_referrals.fields(receipt),
            )
            litepage_referrals.acknowledge(api, receipt, result["status"])


def claim_handoff(api, creator):
    """Add a private local image without extra API calls or authorization polling."""
    if creator.get("status") != "awaiting_wechat":
        return creator
    uri = creator.get("claim_url", "")
    try:
        if not isinstance(uri, str) or len(uri) > 2048:
            raise ValueError("Invalid claim URL")
        target = urlparse(uri)
        if (
            target.scheme != "https"
            or not target.hostname
            or target.username
            or target.password
            or target.query
            or target.fragment
            or not re.fullmatch(
                r"/connect/(?:[a-z0-9]{10}|[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12})",
                target.path,
            )
        ):
            raise ValueError("Invalid claim URL")
        path = create_login_qr(uri, directory=api.store.path.parent)
    except (OSError, RuntimeError, ValueError):
        # Upload is already complete; a local image failure must not cause re-upload.
        return {**creator, "qr_error": "二维码生成失败，请打开认领页扫码；无需重新发布作品。"}
    return {**creator, "qr_path": str(path.resolve())}


def read_password(path, *, allow_empty=False):
    if path is None:
        return None
    if path.stat().st_size > 1024:
        raise RuntimeError("Password file is too large")
    value = path.read_text(encoding="utf-8").rstrip("\r\n")
    if allow_empty and value == "":
        return None
    if not 4 <= len(value) <= 128 or any(ord(c) < 32 for c in value):
        raise RuntimeError("Password must contain 4–128 characters without control characters")
    return value


def sharing_hint(result):
    if result.get("sharing") == "approval":
        return "作品需要发布者授权；访客微信登录后主动申请，获批账号可访问，转发链接不会转移权限。"
    if result.get("password_protected"):
        return "作品已设置密码保护，访客需输入密码读取，不在轻页首页展示。可在作品管理中更换或移除密码。"
    if result.get("visibility") == "private":
        return "作品为仅链接访问（private），持有链接的人可直接读取，不在轻页首页展示。可改为 public，让作品在首页被发现；也可设置密码，要求访客输入密码后读取。"
    if result.get("visibility") == "public":
        return "作品为公开展示（public），可在轻页首页被发现，持有链接的人可直接读取。可改为 private 停止首页展示；如需保护内容，可设为 private 并设置密码。"
    return None


def publish(api, args):
    tags = [] if args.clear_tags else parse_tags(args.tags) if args.tags is not None else None
    password = read_password(args.password_file)
    if args.password_file and args.source.is_dir():
        try:
            args.password_file.resolve().relative_to(args.source.resolve())
        except ValueError:
            pass
        else:
            raise RuntimeError("Keep the password file outside the uploaded directory")
    if args.description is not None and len(args.description) > 240:
        raise RuntimeError("Description must be at most 240 characters")
    data, summary = bundle(args.source, args.preview)
    options = {
        k: v
        for k, v in {
            "tags": tags,
            "home_enabled": args.home_enabled,
            "sharing": args.sharing,
            "visibility": args.visibility,
            "description": args.description,
            "preview_path": "litepage-preview.webp" if args.preview else None,
        }.items()
        if v is not None
    }
    if args.check:
        return {"status": "checked", **summary, **({"tags": tags} if tags is not None else {})}
    if summary["review"]["findings"]:
        print(json.dumps({"event": "prepublish_review", **summary["review"]}), file=sys.stderr)
    ensure_identity(api)
    if options or password is not None:
        features = api.request("GET", "/v1/hosting/usage", authenticated=True).get(
            "publishing_features", []
        )
        required = {"preview" if k == "preview_path" else k for k in options}
        if password is not None:
            required.add("password")
        if not required.issubset(features):
            raise RuntimeError(
                "Server does not support the requested publishing options; no files uploaded"
            )
    source = str(args.source.expanduser().absolute())
    site_arg = str(args.site_id) if args.command == "update" else None
    key = hashlib.sha256(
        json.dumps([api.server, args.command, source, site_arg]).encode()
    ).hexdigest()
    journal = api.store.path.parent / f"publish-{key}.json"
    current = (
        api.request("GET", f"/v1/hosting/sites/{site_arg}", authenticated=True)
        if site_arg
        else None
    )
    with api.store.lock():
        if journal.is_symlink():
            raise RuntimeError("Publish journal must not be a symlink")
        previous = json.loads(journal.read_text()) if journal.exists() else None
        if args.operation_id:
            receipt_path = api.store.path.parent / f"operation-{args.operation_id}.json"
            if receipt_path.is_symlink():
                raise RuntimeError("Operation receipt must not be a symlink")
            previous = json.loads(receipt_path.read_text()) if receipt_path.exists() else None
        elif previous and previous.get("complete"):
            previous = None
        if previous:
            if (
                previous["server"] != api.server
                or previous["sha256"] != summary["sha256"]
                or previous["requested_title"] != args.title
                or previous["source"] != source
                or previous["target"] != site_arg
                or previous.get("options", {}) != options
            ):
                raise RuntimeError(
                    "Pending operation differs; restore the original files/title or explicitly choose a new --operation-id"
                )
            record = previous
        else:
            record = {
                "server": api.server,
                "source": source,
                "target": site_arg,
                "site_id": site_arg or str(uuid.uuid4()),
                "deployment_id": str(args.operation_id or uuid.uuid4()),
                "expected_revision": current["revision"] if current else 0,
                "title": args.title or (current["title"] if current else args.source.stem),
                "requested_title": args.title,
                "options": options,
                "sha256": summary["sha256"],
                "complete": False,
            }
        receipt_path = api.store.path.parent / f"operation-{record['deployment_id']}.json"
        atomic_json(journal, record)
        atomic_json(receipt_path, record)
    print(
        json.dumps(
            {
                "event": "publish_operation",
                "operation_id": record["deployment_id"],
                "site_id": record["site_id"],
            }
        ),
        file=sys.stderr,
    )
    result = api.request(
        "PUT",
        f"/v1/hosting/sites/{record['site_id']}/deployments/{record['deployment_id']}",
        authenticated=True,
        content=data,
        headers={
            "Content-Type": "application/zip",
            **(
                {"X-LitePage-Password": base64.b64encode(password.encode("utf-8")).decode("ascii")}
                if password is not None
                else {}
            ),
        },
        params={
            "title": record["title"],
            "expected_revision": record["expected_revision"],
            **{
                k: json.dumps(v, ensure_ascii=False) if k == "tags" else v
                for k, v in record.get("options", {}).items()
            },
        },
    )
    if (
        tags is not None
        and result.get("tags") != tags
        and result.get("deployment_id") == record["deployment_id"]
    ):
        raise RuntimeError("Server did not confirm requested tags; read status before retrying")
    if password is not None and not result.get("password_protected"):
        raise RuntimeError("Server did not confirm password protection; do not share the URL")
    if result["status"] == "ready" and result["deployment_id"] == record["deployment_id"]:
        # Fresh unauthenticated connection: never leak platform credentials to uploaded HTML.
        probe_url = result.get("content_url") or result["url"]
        url = urlparse(probe_url)
        if (
            url.scheme != "https"
            or url.username
            or not url.hostname
            or not (
                re.fullmatch(r"/p/[a-z0-9]{8}/", url.path)
                or url.path == f"/p/{uuid.UUID(record['site_id']).hex}/"
            )
            or url.query
            or url.fragment
        ):
            raise RuntimeError("Server returned an invalid content URL")
        try:
            with transport.Client(timeout=15, follow_redirects=False) as visitor:
                response = visitor.head(probe_url)
            if result.get("sharing") == "approval":
                if (
                    response.status_code != 303
                    or response.headers.get("x-litepage-approval-protected") != "1"
                ):
                    raise RuntimeError("Approval protection was not verified; do not share the URL")
            elif result.get("password_protected"):
                if (
                    response.status_code != 303
                    or response.headers.get("x-litepage-password-protected") != "1"
                ):
                    raise RuntimeError("Password protection was not verified at the public URL")
            elif (
                response.status_code != 200
                or response.headers.get("x-litepage-sha256") != summary["entry_sha256"]
            ):
                raise RuntimeError(
                    "Published files are not yet verified at the public URL; use status or retry this operation ID"
                )
        except transport.TransportError:
            raise RuntimeError(
                "Upload committed but public access could not be verified; retry the same operation ID"
            ) from None
    elif result["deployment_id"] != record["deployment_id"]:
        result["status"] = "superseded"
    record["complete"] = True
    with api.store.lock():
        atomic_json(receipt_path, record)
        atomic_json(journal, record)
    if summary["entrypoint"] in {"index.md", "index.txt"}:
        result["source_url"] = result["url"] + summary["entrypoint"]
    if summary["external_resources"]:
        result["warning"] = (
            "External resources remain external; their availability is not guaranteed by hosting"
        )
    if result.get("status") == "ready" and result.get("deployment_id") == record["deployment_id"]:
        hint = sharing_hint(result)
        if hint:
            result["sharing_hint"] = hint
    if "creator" in result:
        result["creator"] = claim_handoff(api, result["creator"])
    return result


def execute(api, args):
    if args.command == "referral":
        return litepage_referrals.execute(api, args, ensure_identity)
    if args.command == "profile":
        if args.profile_command in {"show", "works"}:
            own = None
            uid = args.uid
            if uid is None:
                try:
                    own = api.request(
                        "GET", "/v1/hosting/profile", authenticated=True, response_limit=65536
                    )
                except APIError as error:
                    if error.error.get("code") == "login_required":
                        raise APIError(
                            401,
                            {
                                "code": "login_required",
                                "message": "Run lightpage login --wechat, or supply --uid",
                            },
                        ) from None
                    raise
                uid = own.get("uid")
                if not isinstance(uid, str) or not re.fullmatch(r"[a-z0-9]{10}", uid):
                    raise RuntimeError("Server returned no valid profile UID; upgrade the server")
            path = "/v1/hosting/profiles/" + uid
            if args.profile_command == "show":
                result = api.request("GET", path, response_limit=65536)
                if own is not None:
                    result.update(own)
                return result
            params = {"limit": args.limit}
            if args.cursor is not None:
                params["cursor"] = args.cursor
            result = api.request("GET", path + "/works", params=params, response_limit=524288)
            result["uid"] = uid
            return result
        changes = {}
        if args.name is not None:
            if not args.name.strip() or len(args.name) > 80:
                raise ValueError("Name must contain 1–80 characters")
            changes["name"] = args.name
        elif args.reset_name:
            changes["name"] = None
        if args.avatar_url is not None:
            parsed = urlparse(args.avatar_url)
            if (
                parsed.scheme != "https"
                or not parsed.hostname
                or parsed.username
                or parsed.password
                or parsed.fragment
                or len(args.avatar_url) > 2048
            ):
                raise ValueError("Avatar must be a public HTTPS image URL")
            changes["avatar_url"] = args.avatar_url
        elif args.reset_avatar:
            changes["avatar_url"] = None
        if args.signature is not None:
            if len(args.signature) > 160:
                raise ValueError("Signature must contain at most 160 characters")
            changes["signature"] = args.signature
        if not changes:
            raise ValueError("Supply a name, avatar or signature change")
        revision = args.revision
        if revision is None:
            revision = api.request("GET", "/v1/hosting/profile", authenticated=True)["revision"]
        return api.request(
            "PATCH",
            "/v1/hosting/profile",
            authenticated=True,
            json={"expected_revision": revision, **changes},
        )
    if args.command == "read":
        parsed = urlparse(args.url)
        origin = urlparse(api.server)
        if (
            parsed.scheme != "https"
            or parsed.netloc != origin.netloc
            or not parsed.path.startswith("/p/")
        ):
            raise ValueError("Read only a work URL on the selected LightPage instance")
        if args.cursor and not args.read_id:
            raise ValueError("Continue a read with the original --read-id")
        with api.store.lock():
            path = api.store.path.with_name("visitor-" + api.store.account + ".json")
            if path.is_symlink():
                raise RuntimeError("Visitor config must not be a symlink")
            if path.exists():
                visitor = json.loads(path.read_text())["id"]
                uuid.UUID(visitor)
            else:
                visitor = str(uuid.uuid4())
                atomic_json(path, {"id": visitor})
        return api.request(
            "GET",
            "/v1/hosting/read",
            authenticated=bool(api.store.load()),
            params={
                "url": args.url,
                "visitor_id": visitor,
                "read_id": str(args.read_id or uuid.uuid4()),
                "max_bytes": args.max_bytes,
                "cursor": args.cursor,
            },
        )

    if args.command == "tags":
        tags = [] if args.clear else parse_tags(args.tags)
        path = f"/v1/hosting/sites/{args.site_id}"
        revision = args.revision
        if revision is None:
            revision = api.request("GET", path, authenticated=True)["revision"]
        return api.request(
            "PUT",
            path + "/tags",
            authenticated=True,
            json={"tags": tags, "expected_revision": revision},
        )
    if args.command == "capabilities":
        from urllib.parse import quote

        path = "/v1/hosting/capabilities"
        if args.name:
            path += "/" + quote(args.name, safe="")
        return api.request("GET", path, authenticated=False)
    if args.command == "access":
        return litepage_access.execute(api, args)
    if args.command == "sharing":
        password = read_password(args.password_file)
        if password is not None and args.value != "password":
            raise RuntimeError("Passwords require password sharing")
        return api.request(
            "PUT",
            "/v1/hosting/sites/%s/sharing" % args.site_id,
            authenticated=True,
            json={"sharing": args.value, "password": password, "expected_revision": args.revision},
        )
    if args.command in {"author", "mail"}:
        return litepage_mail.execute(api, args, ensure_identity)
    if args.command == "feedback":
        return submit_feedback(api, args)
    if args.command == "qr":
        return share_qr(args.url, args.output, args.overwrite)
    if args.command in {"publish", "update"}:
        return publish(api, args)
    if args.command == "password":
        password = read_password(args.password_file, allow_empty=True)
        path = f"/v1/hosting/sites/{args.site_id}"
        revision = args.revision
        if revision is None:
            revision = api.request("GET", path, authenticated=True)["revision"]
        return api.request(
            "PUT",
            path + "/password",
            authenticated=True,
            json={"password": password, "expected_revision": revision},
        )
    if args.command == "visibility":
        return api.request(
            "PUT",
            f"/v1/hosting/sites/{args.site_id}/visibility",
            authenticated=True,
            json={"visibility": args.value, "expected_revision": args.revision},
        )
    if args.command == "login":
        return api.native_login(socket.gethostname(), mode="wechat", force=args.force)
    if args.command == "bind-wechat":
        return api.native_login(socket.gethostname(), binding=True)
    if args.command == "logout":
        result = api.request("DELETE", "/v1/hosting/device", authenticated=True)
        with api.store.lock():
            api.store.delete()
        return result
    if args.command == "status":
        return api.request("GET", f"/v1/hosting/sites/{args.site_id}", authenticated=True)
    if args.command == "claim":
        return claim_handoff(
            api, api.request("POST", f"/v1/hosting/sites/{args.site_id}/claim", authenticated=True)
        )
    if args.command == "unpublish":
        return api.request(
            "PUT",
            f"/v1/hosting/sites/{args.site_id}/unpublish",
            authenticated=True,
            json={"expected_revision": args.revision},
        )
    if args.command == "delete":
        path = f"/v1/hosting/sites/{args.site_id}"
        if args.confirm_token is None:
            return api.request("GET", path + "/delete-confirmation", authenticated=True)
        if not 1 <= len(args.confirm_token) <= 1024:
            raise RuntimeError("Use the confirmation token from this work's preview")
        return api.request(
            "DELETE",
            path,
            authenticated=True,
            json={"confirmation_token": args.confirm_token},
        )
    if args.command == "usage":
        return api.request("GET", "/v1/hosting/usage", authenticated=True)
    if args.command == "analytics":
        path = (
            f"/v1/hosting/sites/{args.site_id}/analytics"
            if args.site_id
            else "/v1/hosting/analytics"
        )
        return api.request("GET", path, authenticated=True, params={"days": args.days})
    return api.request(
        "GET",
        "/v1/hosting/sites",
        authenticated=True,
        params={
            "limit": args.limit,
            **({"cursor": args.cursor} if args.cursor else {}),
            **({"tag": exact_tag(args.tag)} if args.tag is not None else {}),
            **({"untagged": "true"} if args.untagged else {}),
        },
    )


def main():
    args = parser().parse_args()
    server = args.server.rstrip("/")
    origin = urlparse(server)
    if args.command != "qr" and (
        origin.scheme != "https"
        or not origin.hostname
        or origin.username
        or origin.password
        or origin.path
        or origin.query
        or origin.fragment
    ):
        print(
            json.dumps({"error": {"code": "invalid_server", "message": "Use an HTTPS API origin"}}),
            file=sys.stderr,
        )
        raise SystemExit(1)
    api = None
    try:
        if args.command != "qr":
            store = credential_store(server, os.getenv("LITEPAGE_CONFIG_DIR", "~/.config/litepage"))
            api = LitePageAPI(server, store)
        result = execute(api, args)
        print(json.dumps(notice_output(result, api), ensure_ascii=False))
    except APIError as exc:
        print(
            json.dumps(
                notice_output(
                    {"error": exc.error, **({"notice": exc.notice} if exc.notice else {})}, api
                ),
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1) from None
    except (RuntimeError, OSError, ValueError) as exc:
        print(
            json.dumps(
                notice_output({"error": {"code": "litepage_error", "message": str(exc)}}, api),
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        raise SystemExit(1) from None
    finally:
        if api:
            api.close()


if __name__ == "__main__":
    main()
