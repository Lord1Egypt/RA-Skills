#!/usr/bin/env python3
from __future__ import annotations

import argparse
import getpass
import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from pocketbook_lib.common import *
from pocketbook_lib.state import *
from pocketbook_lib.models import *
from pocketbook_lib.formats import *
from pocketbook_lib.api import *
from pocketbook_lib.transport import *
from pocketbook_lib.operations import *

def print_json(obj: Any) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=False))

def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pocketbook", description="PocketBook Cloud helper for OpenClaw")
    sub = p.add_subparsers(dest="command", required=True)
    auth = sub.add_parser("auth")
    auth_sub = auth.add_subparsers(dest="auth_command", required=True)
    login = auth_sub.add_parser("login")
    login.add_argument("--email")
    login.add_argument("--provider")
    auth_sub.add_parser("status")
    auth_sub.add_parser("logout")
    sub.add_parser("doctor")
    books = sub.add_parser("books")
    books.add_argument("--status", choices=["unread", "reading", "finished"])
    search = sub.add_parser("search")
    search.add_argument("query")
    inbound = sub.add_parser("inbound-latest")
    inbound.add_argument("--name")
    inbound.add_argument("--within-seconds", type=int, default=1800)
    upload = sub.add_parser("upload")
    upload.add_argument("path")
    upload.add_argument("--name")
    upload_inbound_p = sub.add_parser("upload-inbound")
    upload_inbound_p.add_argument("path")
    upload_inbound_p.add_argument("--confirmed", action="store_true")
    upload_inbound_many_p = sub.add_parser("upload-inbound-many")
    upload_inbound_many_p.add_argument("paths", nargs="+")
    upload_inbound_many_p.add_argument("--confirmed", action="store_true")
    preflight_upload_p = sub.add_parser("preflight-upload")
    preflight_upload_p.add_argument("paths", nargs="+")
    prepare_upload_p = sub.add_parser("prepare-upload")
    prepare_upload_p.add_argument("paths", nargs="+")
    prepare_upload_p.add_argument("--output-dir", required=True)
    upload_many_p = sub.add_parser("upload-many")
    upload_many_p.add_argument("paths", nargs="+")
    upload_many_p.add_argument("--confirmed", action="store_true")
    download = sub.add_parser("download")
    download.add_argument("query")
    download.add_argument("--output-dir", required=True)
    download_chat = sub.add_parser("download-for-chat")
    download_chat.add_argument("query")
    download_chat.add_argument("--media-dir")
    preflight_download_p = sub.add_parser("preflight-download")
    preflight_download_p.add_argument("queries", nargs="+")
    download_many_p = sub.add_parser("download-many")
    download_many_p.add_argument("queries", nargs="+")
    download_many_p.add_argument("--output-dir", required=True)
    download_many_p.add_argument("--archive")
    download_many_p.add_argument("--confirmed", action="store_true")
    package = sub.add_parser("package")
    package.add_argument("paths", nargs="+")
    package.add_argument("--output", required=True)
    notes = sub.add_parser("notes")
    notes.add_argument("query")
    delete = sub.add_parser("delete")
    delete_sub = delete.add_subparsers(dest="delete_command", required=True)
    delete_prepare = delete_sub.add_parser("prepare")
    delete_prepare.add_argument("query")
    delete_confirm = delete_sub.add_parser("confirm")
    delete_confirm.add_argument("confirmation_text")
    delete_cancel = delete_sub.add_parser("cancel")
    delete_cancel.add_argument("legacy_value", nargs="?")
    backup = sub.add_parser("backup")
    backup.add_argument("--output-dir", required=True)
    return p

def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    client = PocketBookClient()
    try:
        if args.command == "auth":
            if args.auth_command == "status":
                print_json(client.auth_status()); return 0
            if args.auth_command == "logout":
                client.store.clear(); client.session = {}; print_json({"ok": True, "authenticated": False}); return 0
            email = args.email or input("PocketBook email: ").strip()
            password = getpass.getpass("PocketBook password: ")
            if not email or not password:
                raise AuthRequired("Email and password are required")
            try:
                result = client.login(email, password, args.provider)
            except AmbiguousProvider as amb:
                # Provider ambiguity is rare. Prompt only in an interactive terminal.
                if not sys.stdin.isatty():
                    raise
                print("Available PocketBook providers:", file=sys.stderr)
                for i, c in enumerate(amb.providers, 1):
                    print(f"  {i}. {c.get('name') or c.get('alias')} ({c.get('alias')})", file=sys.stderr)
                raw = input("Provider number: ").strip()
                try: idx = int(raw) - 1
                except ValueError as exc: raise AuthRequired("Invalid provider selection") from exc
                if not 0 <= idx < len(amb.providers): raise AuthRequired("Invalid provider selection")
                result = client.login(email, password, str(amb.providers[idx].get("alias") or ""))
            print_json({"ok": True, **result}); return 0
        if args.command == "doctor":
            out = client.doctor(); print_json(out)
            return 0 if out.get("ok") or out.get("reason") == "not_authenticated" else 2
        if args.command == "books":
            raw = client.books()
            items = [book_summary(b) for b in raw]
            if args.status: items = [b for b in items if b.get("status") == args.status]
            print_json({"ok": True, "count": len(items), "books": items}); return 0
        if args.command == "search":
            scored = search_books(client.books(), args.query)
            print_json({"ok": True, "query": args.query, "count": len(scored), "books": [book_summary(b) | {"matchScore": s} for s, b in scored[:20]]}); return 0
        if args.command == "inbound-latest":
            print_json(resolve_inbound_attachment(args.name, args.within_seconds)); return 0
        if args.command == "upload":
            print_json(client.upload(Path(args.path), args.name)); return 0
        if args.command == "upload-inbound":
            out = upload_inbound(client, Path(args.path), confirmed=args.confirmed)
            print_json(out)
            failed = int((out.get("upload") or {}).get("failed") or 0) if isinstance(out.get("upload"), dict) else 0
            return 0 if out.get("ok") or out.get("requiresConfirmation") or failed == 0 else 1
        if args.command == "upload-inbound-many":
            out = upload_inbound_many(client, [Path(x) for x in args.paths], confirmed=args.confirmed)
            print_json(out)
            return 0 if out.get("ok") or out.get("requiresConfirmation") or int(out.get("failed") or 0) == 0 else 1
        if args.command == "preflight-upload":
            print_json(preflight_upload([Path(x) for x in args.paths])); return 0
        if args.command == "prepare-upload":
            print_json(materialize_upload_inputs([Path(x) for x in args.paths], Path(args.output_dir))); return 0
        if args.command == "upload-many":
            out = upload_many(client, [Path(x) for x in args.paths], confirmed=args.confirmed); print_json(out)
            return 0 if out.get("ok") or out.get("requiresConfirmation") or int(out.get("failed") or 0) == 0 else 1
        if args.command == "download":
            book = resolve_book(client.books(), args.query)
            print_json(download_book(book, Path(args.output_dir))); return 0
        if args.command == "download-for-chat":
            print_json(download_for_chat(client, args.query, Path(args.media_dir) if args.media_dir else None)); return 0
        if args.command == "preflight-download":
            print_json(preflight_download(client, list(args.queries))); return 0
        if args.command == "download-many":
            archive = Path(args.archive) if args.archive else None
            out = download_many(client, list(args.queries), Path(args.output_dir), archive, confirmed=args.confirmed); print_json(out); return 0 if out.get("ok") or out.get("requiresConfirmation") else 1
        if args.command == "package":
            print_json(package_files([Path(x) for x in args.paths], Path(args.output))); return 0
        if args.command == "notes":
            book = resolve_book(client.books(), args.query)
            records = client.notes(book)
            print_json({"ok": True, "book": book_summary(book), "count": len(records), "notes": records}); return 0
        if args.command == "delete":
            if args.delete_command == "prepare":
                print_json(prepare_delete(client, args.query)); return 0
            if args.delete_command == "confirm":
                print_json(confirm_delete(client, args.confirmation_text)); return 0
            if args.delete_command == "cancel":
                print_json(cancel_delete(client, args.legacy_value)); return 0
        if args.command == "backup":
            out = backup_library(client, Path(args.output_dir))
            print_json(out)
            return 0 if out.get("failed", 0) == 0 else 1
        raise PocketBookError("Unknown command")
    except AmbiguousBook as exc:
        # Ambiguity is expected conversational control flow, not a process crash.
        print_json({"ok": False, "error": "ambiguous_book", "message": str(exc), "query": exc.query, "candidates": exc.candidates})
        return 0
    except NotFound as exc:
        # A missing user-selected book is likewise a normal result for an agent.
        print_json({"ok": False, "error": "not_found", "message": str(exc)})
        return 0
    except AmbiguousProvider as exc:
        print_json({"ok": False, "error": "ambiguous_provider", "message": str(exc), "providers": exc.providers})
        return 0
    except PocketBookError as exc:
        print_json({"ok": False, "error": exc.__class__.__name__, "message": str(exc)})
        return exc.code
    except KeyboardInterrupt:
        print_json({"ok": False, "error": "cancelled"})
        return 130
    except Exception:
        # Never expose raw exception text/traceback through the agent boundary.
        print_json({"ok": False, "error": "internal_error", "message": "Unexpected internal failure"})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
