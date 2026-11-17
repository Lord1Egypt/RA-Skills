"""Task-shaped commands for bounded retrieval and reversible participation."""

import sys
import uuid
from pathlib import Path

from echo_cli.client import with_notice
from echo_cli.compat import subparsers
from echo_cli.user_ids import user_reference

COMMANDS = {
    "bookmark",
    "unbookmark",
    "like",
    "unlike",
    "bookmarks",
    "likes",
    "liked",
    "follow",
    "unfollow",
    "following",
    "notices",
    "notice-seen",
    "attachment",
}
KINDS = ["person_post", "thread_reply"]


def paging(command, maximum=50):
    command.add_argument(
        "--limit", type=int, default=10, choices=range(1, maximum + 1), metavar=f"1-{maximum}"
    )
    command.add_argument("--cursor")


def configure(commands):
    for name in ["bookmark", "unbookmark", "like", "unlike"]:
        commands.add_parser(name).add_argument("id", type=uuid.UUID)
    for name in ["bookmarks", "likes", "liked", "notices"]:
        command = commands.add_parser(name)
        paging(command, 10 if name == "notices" else 50)
        if name == "liked":
            command.add_argument(
                "--by", type=user_reference, help="Filter public likes by the person who liked them"
            )
    for name in ["follow", "unfollow", "following"]:
        command = commands.add_parser(name)
        command.add_argument("kind", choices=["post", "person"])
        if name == "following":
            paging(command)
        else:
            command.add_argument("id", type=user_reference)
    seen = commands.add_parser("notice-seen", help="Acknowledge a followed person or thread update")
    seen.add_argument("kind", choices=KINDS)
    seen.add_argument("id", type=uuid.UUID)
    attachment = subparsers(commands.add_parser("attachment"), dest="attachment_command")
    upload = attachment.add_parser("upload")
    upload.add_argument("file", type=Path)
    upload.add_argument(
        "--id", type=uuid.UUID, required=True, help="Stable upload UUID; reuse on retry"
    )
    for name in ["read", "delete", "download"]:
        command = attachment.add_parser(name)
        command.add_argument("id", type=uuid.UUID)
        if name == "download":
            command.add_argument(
                "--output",
                type=Path,
                required=True,
                help="New destination file; never printed or executed",
            )


def operation(api, args):
    name = args.command
    if name == "attachment":
        path = f"/v1/attachments/{args.id}"
        if args.attachment_command == "upload":
            if not 0 < args.file.stat().st_size <= 5 * 1024 * 1024:
                raise RuntimeError("Upload must contain 1 byte to 5 MiB")
            with args.file.open("rb") as stream:
                data = stream.read(5 * 1024 * 1024 + 1)
            if len(data) > 5 * 1024 * 1024:
                raise RuntimeError("Upload exceeds 5 MiB")
            print(f"upload_id={args.id}", file=sys.stderr)
            return api.request(
                "PUT",
                path,
                authenticated=True,
                params={"name": args.file.name},
                content=data,
                headers={"Content-Type": "application/octet-stream"},
            )
        if args.attachment_command == "download":
            if args.output.exists():
                raise RuntimeError("Download destination already exists")
            response = api.request("GET", path + "/download", raw=True)
            if response.headers.get("content-type", "").split(";")[0] != "application/octet-stream":
                raise RuntimeError("Expected a binary attachment response")
            if len(response.content) > 5 * 1024 * 1024:
                raise RuntimeError("Attachment exceeds the protocol size limit")
            with args.output.open("xb") as destination:
                destination.write(response.content)
            return with_notice(
                {
                    "id": str(args.id),
                    "path": str(args.output.resolve()),
                    "size": len(response.content),
                },
                response,
            )
        deleting = args.attachment_command == "delete"
        result = api.request("DELETE" if deleting else "GET", path, authenticated=deleting)
        return {**result, "id": str(args.id), "deleted": True} if deleting else result
    if name in {"bookmark", "unbookmark", "like", "unlike"}:
        enabled = not name.startswith("un")
        kind = name[2:] if name.startswith("un") else name
        result = api.request(
            "PUT" if enabled else "DELETE", f"/v1/me/marks/{kind}/{args.id}", authenticated=True
        )
        return {**result, "id": str(args.id), "kind": kind, "active": enabled}
    if name in {"follow", "unfollow"}:
        if args.kind == "post":
            try:
                uuid.UUID(str(args.id))
            except ValueError:
                raise RuntimeError("Post references require a UUID") from None
        path = (
            f"/v1/me/following/people/{args.id}"
            if args.kind == "person"
            else f"/v1/me/marks/follow/{args.id}"
        )
        result = api.request("PUT" if name == "follow" else "DELETE", path, authenticated=True)
        return {**result, "id": str(args.id), "kind": args.kind, "following": name == "follow"}
    if name == "notice-seen":
        result = api.request("PUT", f"/v1/notices/{args.kind}/{args.id}/seen", authenticated=True)
        return {**result, "id": str(args.id), "kind": args.kind, "seen": True}
    params = {"limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    path = {
        "bookmarks": "/v1/me/marks/bookmark",
        "likes": "/v1/me/marks/like",
        "liked": "/v1/likes",
        "notices": "/v1/notices",
    }.get(name)
    if name == "following":
        path = "/v1/me/following/people" if args.kind == "person" else "/v1/me/marks/follow"
    if name == "liked" and args.by:
        params["liker_id"] = str(args.by)
    return api.request("GET", path, params=params, authenticated=name != "liked")
