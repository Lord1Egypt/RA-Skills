"""Unified CLI entry point (LinkedIn Extension Bridge version)

Connects to the user's browser via the LinkedIn Bridge extension.
Start bridge_server.py first, install the LinkedIn Bridge extension in Chrome, then run this CLI.

Output: JSON (ensure_ascii=False)
Exit codes: 0=success, 1=not logged in, 2=error
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("linkedin-cli")


def _output(data: dict, exit_code: int = 0) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))
    sys.exit(exit_code)


class _DummyBrowser:
    def close(self) -> None:
        pass


def _ensure_bridge_ready(bridge_url: str) -> None:
    """Ensure bridge server is running and extension is connected."""
    import subprocess
    import time
    from pathlib import Path

    from linkedin.bridge import BridgePage

    page = BridgePage(bridge_url)

    if not page.is_server_running():
        logger.info("Bridge server not running, starting...")
        scripts_dir = Path(__file__).parent
        kwargs: dict = {}
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NEW_CONSOLE
        subprocess.Popen(
            [sys.executable, str(scripts_dir / "bridge_server.py")],
            **kwargs,
        )
        for _ in range(10):
            time.sleep(1)
            if page.is_server_running():
                logger.info("Bridge server started")
                break
        else:
            logger.warning("Bridge server start timeout. Please run bridge_server.py manually.")
            return

    if page.is_extension_connected():
        return

    logger.info("Browser extension not connected, opening Chrome...")
    _open_chrome()

    for _ in range(20):
        time.sleep(1)
        if page.is_extension_connected():
            logger.info("Browser extension connected")
            return

    logger.warning(
        "Extension connection timeout. "
        "Please ensure Chrome has the LinkedIn Bridge extension installed and enabled."
    )


def _open_chrome() -> None:
    """Try to launch Chrome browser."""
    import subprocess

    for cmd in [["open", "-a", "Google Chrome"], ["google-chrome"], ["chromium-browser"]]:
        try:
            subprocess.Popen(cmd)
            return
        except FileNotFoundError:
            continue
    logger.warning("Chrome not found. Please open your browser manually.")


def _connect(args: argparse.Namespace):
    from linkedin.bridge import BridgePage

    bridge_url = getattr(args, "bridge_url", "ws://localhost:9336")
    _ensure_bridge_ready(bridge_url)
    return _DummyBrowser(), BridgePage(bridge_url)


# ─── Subcommand implementations ──────────────────────────────────


def cmd_check_login(args: argparse.Namespace) -> None:
    from linkedin.login import check_login_status, get_current_username

    browser, page = _connect(args)
    try:
        logged_in = check_login_status(page)
        if logged_in:
            username = get_current_username(page)
            _output({"logged_in": True, "username": username})
        else:
            _output(
                {
                    "logged_in": False,
                    "hint": "Not logged in. Please log in to LinkedIn in your browser.",
                },
                exit_code=1,
            )
    finally:
        browser.close()


def cmd_delete_cookies(args: argparse.Namespace) -> None:
    from linkedin.login import logout

    browser, page = _connect(args)
    try:
        logged_out = logout(page)
        msg = "Logged out successfully" if logged_out else "Not logged in"
        _output({"success": True, "message": msg})
    finally:
        browser.close()


def cmd_home_feed(args: argparse.Namespace) -> None:
    from linkedin.feed import home_feed

    browser, page = _connect(args)
    try:
        posts = home_feed(page)
        _output({"posts": [p.to_dict() for p in posts], "count": len(posts)})
    finally:
        browser.close()


def cmd_search(args: argparse.Namespace) -> None:
    from linkedin.search import search

    browser, page = _connect(args)
    try:
        results = search(
            page, args.query, args.type or "content",
            title=getattr(args, "title", "") or "",
            location_urn=getattr(args, "location_urn", "") or "",
            company=getattr(args, "company", "") or "",
            network=getattr(args, "network", "") or "",
        )
        _output({"results": [r.to_dict() for r in results], "count": len(results)})
    finally:
        browser.close()


def cmd_get_post_detail(args: argparse.Namespace) -> None:
    from linkedin.post_detail import get_post_detail

    browser, page = _connect(args)
    try:
        detail = get_post_detail(page, args.url)
        _output(detail.to_dict())
    finally:
        browser.close()


def cmd_user_profile(args: argparse.Namespace) -> None:
    from linkedin.profile import get_user_profile

    browser, page = _connect(args)
    try:
        result = get_user_profile(page, args.username)
        _output(result)
    finally:
        browser.close()


def cmd_company_profile(args: argparse.Namespace) -> None:
    from linkedin.profile import get_company_profile

    browser, page = _connect(args)
    try:
        result = get_company_profile(page, args.company_slug)
        _output(result)
    finally:
        browser.close()


def cmd_like_post(args: argparse.Namespace) -> None:
    from linkedin.interact import like_post

    browser, page = _connect(args)
    try:
        result = like_post(page, args.url)
        _output(result.to_dict())
    finally:
        browser.close()


def cmd_comment_post(args: argparse.Namespace) -> None:
    from linkedin.interact import comment_post

    browser, page = _connect(args)
    try:
        comment_post(page, args.url, args.content)
        _output({"success": True, "message": "Comment posted successfully"})
    finally:
        browser.close()


def cmd_send_connection(args: argparse.Namespace) -> None:
    from linkedin.interact import send_connection_request

    note = ""
    if args.note_file and os.path.exists(args.note_file):
        with open(args.note_file, encoding="utf-8") as f:
            note = f.read().strip()

    browser, page = _connect(args)
    try:
        result = send_connection_request(page, args.url, note=note)
        _output(result.to_dict())
    finally:
        browser.close()


def cmd_send_message(args: argparse.Namespace) -> None:
    from linkedin.interact import send_message

    with open(args.content_file, encoding="utf-8") as f:
        message_text = f.read().strip()

    browser, page = _connect(args)
    try:
        result = send_message(page, args.url, message_text)
        _output(result.to_dict())
    finally:
        browser.close()


def cmd_submit_post(args: argparse.Namespace) -> None:
    from linkedin.publish import submit_text_post
    from linkedin.types import SubmitPostContent

    with open(args.content_file, encoding="utf-8") as f:
        text = f.read().strip()

    browser, page = _connect(args)
    try:
        submit_text_post(page, SubmitPostContent(text=text))
        _output({"success": True, "message": "Post submitted successfully"})
    finally:
        browser.close()


def cmd_submit_image(args: argparse.Namespace) -> None:
    from image_downloader import process_images
    from linkedin.publish import submit_image_post
    from linkedin.types import SubmitPostContent

    text = ""
    if args.content_file:
        with open(args.content_file, encoding="utf-8") as f:
            text = f.read().strip()

    images = process_images(args.images or [])

    browser, page = _connect(args)
    try:
        submit_image_post(page, SubmitPostContent(text=text, images=images))
        _output({"success": True, "message": "Image post submitted successfully"})
    finally:
        browser.close()


# ─── Argument parser ─────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="linkedin-cli",
        description="LinkedIn automation via browser extension bridge",
    )
    parser.add_argument(
        "--bridge-url", default="ws://localhost:9336", dest="bridge_url"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # Auth
    sub.add_parser("check-login", help="Check LinkedIn login status")
    sub.add_parser("delete-cookies", help="Log out of LinkedIn")

    # Feed
    sub.add_parser("home-feed", help="Get home feed posts")

    # Search
    p = sub.add_parser("search", help="Search LinkedIn")
    p.add_argument("--query", required=True, help="Search query")
    p.add_argument(
        "--type",
        default="content",
        choices=["content", "people", "companies"],
        dest="type",
        help="Search type (default: content/posts)",
    )
    p.add_argument("--title", default="", help="Job title filter (people search)")
    p.add_argument(
        "--location-urn", default="", dest="location_urn",
        help="LinkedIn geo URN, e.g. 103644278 for India",
    )
    p.add_argument("--company", default="", help="Company name filter (people search)")
    p.add_argument(
        "--network", default="",
        choices=["", "F", "S", "O"],
        help="Connection degree: F=1st, S=2nd, O=3rd+",
    )

    # Post detail
    p = sub.add_parser("get-post-detail", help="Get post content and comments")
    p.add_argument("--url", required=True, help="Post URL or URN")

    # Profiles
    p = sub.add_parser("user-profile", help="Get a user profile")
    p.add_argument(
        "--username", required=True, help="LinkedIn profile slug or full profile URL"
    )

    p = sub.add_parser("company-profile", help="Get a company page")
    p.add_argument(
        "--company-slug",
        required=True,
        dest="company_slug",
        help="Company URL slug (e.g. 'microsoft') or full company URL",
    )

    # Publish
    p = sub.add_parser("submit-post", help="Submit a text post to the feed")
    p.add_argument(
        "--content-file",
        required=True,
        dest="content_file",
        help="Absolute path to a text file with the post content",
    )

    p = sub.add_parser("submit-image", help="Submit an image post to the feed")
    p.add_argument(
        "--content-file",
        dest="content_file",
        help="Absolute path to a text file with the post caption (optional)",
    )
    p.add_argument(
        "--images",
        nargs="+",
        default=[],
        help="Absolute paths or URLs of images to attach",
    )

    # Interact
    p = sub.add_parser("like-post", help="Like a post")
    p.add_argument("--url", required=True, help="Post URL")

    p = sub.add_parser("comment-post", help="Comment on a post")
    p.add_argument("--url", required=True, help="Post URL")
    p.add_argument("--content", required=True, help="Comment text")

    p = sub.add_parser("send-connection", help="Send a connection request")
    p.add_argument("--url", required=True, help="Profile URL or slug")
    p.add_argument(
        "--note-file",
        dest="note_file",
        help="Absolute path to a text file with a personalised connection note (optional)",
    )

    p = sub.add_parser("send-message", help="Send a direct message")
    p.add_argument("--url", required=True, help="Profile URL or slug")
    p.add_argument(
        "--content-file",
        required=True,
        dest="content_file",
        help="Absolute path to a text file with the message body",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "check-login": cmd_check_login,
        "delete-cookies": cmd_delete_cookies,
        "home-feed": cmd_home_feed,
        "search": cmd_search,
        "get-post-detail": cmd_get_post_detail,
        "user-profile": cmd_user_profile,
        "company-profile": cmd_company_profile,
        "submit-post": cmd_submit_post,
        "submit-image": cmd_submit_image,
        "like-post": cmd_like_post,
        "comment-post": cmd_comment_post,
        "send-connection": cmd_send_connection,
        "send-message": cmd_send_message,
    }

    handler = dispatch.get(args.command)
    if not handler:
        parser.print_help()
        sys.exit(2)

    try:
        handler(args)
    except Exception as e:
        logger.error("Command failed: %s", e)
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(2)


if __name__ == "__main__":
    main()
