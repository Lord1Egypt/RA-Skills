#!/usr/bin/env python3
"""
Google Slides API helper - uses gog's stored OAuth credentials.

Usage:
  python3 slides.py create "My Presentation"
  python3 slides.py info <presentationId>
  python3 slides.py add-slide <presentationId> --title "Slide Title" --body "Bullet 1\nBullet 2"
  python3 slides.py batch <presentationId> requests.json
  python3 slides.py export <presentationId> --format pdf --out /tmp/deck.pdf
  python3 slides.py list-comments <presentationId> [--include-deleted]
  python3 slides.py resolve-comment <presentationId> <commentId> [--reply "Text"]
"""

import sys
import os
import json
import subprocess
import argparse

GOG_CREDS = os.path.expanduser("~/.config/gogcli/credentials.json")
TOKEN_TMP = "/tmp/gog_slides_token.json"
ACCOUNT = os.environ.get("GOG_ACCOUNT", "david@hml.tech")


def get_creds():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    
    result = subprocess.run(
        ["gog", "auth", "tokens", "export", ACCOUNT, "--out", TOKEN_TMP, "--overwrite"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error exporting token: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    with open(TOKEN_TMP) as f:
        token_data = json.load(f)

    with open(GOG_CREDS) as f:
        creds_data = json.load(f)

    creds = Credentials(
        token=None,
        refresh_token=token_data["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=creds_data["client_id"],
        client_secret=creds_data["client_secret"],
    )
    creds.refresh(Request())
    return creds


def get_service():
    """Build authenticated Google Slides service using gog's stored tokens."""
    from googleapiclient.discovery import build
    return build("slides", "v1", credentials=get_creds())


def get_drive_service():
    """Build authenticated Google Drive service for comments using gog's stored tokens."""
    from googleapiclient.discovery import build
    return build("drive", "v3", credentials=get_creds())


def cmd_create(args):
    """Create a new presentation."""
    service = get_service()
    body = {"title": args.title}
    result = service.presentations().create(body=body).execute()
    print(json.dumps({
        "presentationId": result["presentationId"],
        "title": result["title"],
        "url": f"https://docs.google.com/presentation/d/{result['presentationId']}/edit"
    }, indent=2))


def cmd_info(args):
    """Get presentation info."""
    service = get_service()
    result = service.presentations().get(presentationId=args.presentation_id).execute()
    slides_summary = [{
        "slideIndex": i,
        "objectId": s["objectId"],
        "elements": len(s.get("pageElements", []))
    } for i, s in enumerate(result.get("slides", []))]
    print(json.dumps({
        "presentationId": result["presentationId"],
        "title": result["title"],
        "slideCount": len(result.get("slides", [])),
        "slides": slides_summary,
        "url": f"https://docs.google.com/presentation/d/{result['presentationId']}/edit"
    }, indent=2))


def cmd_add_slide(args):
    """Add a text slide with title and optional bullet body."""
    service = get_service()

    slide_id = f"slide_{os.urandom(4).hex()}"
    title_id = f"title_{os.urandom(4).hex()}"
    body_id = f"body_{os.urandom(4).hex()}"

    requests = [
        {
            "createSlide": {
                "objectId": slide_id,
                "slideLayoutReference": {"predefinedLayout": "TITLE_AND_BODY"},
                "placeholderIdMappings": [
                    {"layoutPlaceholder": {"type": "TITLE"}, "objectId": title_id},
                    {"layoutPlaceholder": {"type": "BODY"}, "objectId": body_id},
                ]
            }
        }
    ]

    if args.insert_at is not None:
        requests[0]["createSlide"]["insertionIndex"] = args.insert_at

    if args.title:
        requests.append({
            "insertText": {"objectId": title_id, "text": args.title}
        })

    if args.body:
        requests.append({
            "insertText": {"objectId": body_id, "text": args.body}
        })

    result = service.presentations().batchUpdate(
        presentationId=args.presentation_id,
        body={"requests": requests}
    ).execute()

    print(json.dumps({
        "slideId": slide_id,
        "presentationId": args.presentation_id,
        "url": f"https://docs.google.com/presentation/d/{args.presentation_id}/edit"
    }, indent=2))


def cmd_batch(args):
    """Execute a batch update from a JSON file of requests."""
    service = get_service()
    with open(args.requests_file) as f:
        requests = json.load(f)

    result = service.presentations().batchUpdate(
        presentationId=args.presentation_id,
        body={"requests": requests}
    ).execute()
    print(json.dumps(result, indent=2))


def cmd_export(args):
    """Export presentation to PDF or PPTX using gog."""
    out = args.out or f"/tmp/{args.presentation_id}.{args.format}"
    result = subprocess.run(
        ["gog", "slides", "export", args.presentation_id,
         "--format", args.format, "--out", out],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"Exported to: {out}")


def cmd_list_comments(args):
    """List comments on a presentation via Drive API."""
    service = get_drive_service()
    results = service.comments().list(
        fileId=args.presentation_id,
        fields="comments(id,content,anchor,resolved,quotedFileContent,author(displayName),replies(content,action))",
        includeDeleted=args.include_deleted
    ).execute()
    print(json.dumps(results, indent=2))


def cmd_resolve_comment(args):
    """Resolve a comment, optionally with a reply message."""
    service = get_drive_service()
    body = {"action": "resolve"}
    if args.reply:
        body["content"] = args.reply
    
    reply = service.replies().create(
        fileId=args.presentation_id,
        commentId=args.comment_id,
        fields="id,content,action",
        body=body
    ).execute()
    print(json.dumps(reply, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Google Slides helper")
    sub = parser.add_subparsers(dest="command", required=True)

    # create
    p_create = sub.add_parser("create", help="Create a new presentation")
    p_create.add_argument("title", help="Presentation title")

    # info
    p_info = sub.add_parser("info", help="Get presentation info")
    p_info.add_argument("presentation_id")

    # add-slide
    p_add = sub.add_parser("add-slide", help="Add a text slide")
    p_add.add_argument("presentation_id")
    p_add.add_argument("--title", default="")
    p_add.add_argument("--body", default="")
    p_add.add_argument("--insert-at", type=int, default=None)

    # batch
    p_batch = sub.add_parser("batch", help="Run batch update from JSON file")
    p_batch.add_argument("presentation_id")
    p_batch.add_argument("requests_file")

    # export
    p_export = sub.add_parser("export", help="Export to PDF or PPTX")
    p_export.add_argument("presentation_id")
    p_export.add_argument("--format", default="pdf", choices=["pdf", "pptx"])
    p_export.add_argument("--out", default=None)

    # list-comments
    p_list_comments = sub.add_parser("list-comments", help="List comments on the document")
    p_list_comments.add_argument("presentation_id")
    p_list_comments.add_argument("--include-deleted", action="store_true")

    # resolve-comment
    p_resolve = sub.add_parser("resolve-comment", help="Resolve a comment via Drive API")
    p_resolve.add_argument("presentation_id")
    p_resolve.add_argument("comment_id")
    p_resolve.add_argument("--reply", default="Resolved.", help="Text of the reply")

    args = parser.parse_args()
    commands = {
        "create": cmd_create,
        "info": cmd_info,
        "add-slide": cmd_add_slide,
        "batch": cmd_batch,
        "export": cmd_export,
        "list-comments": cmd_list_comments,
        "resolve-comment": cmd_resolve_comment,
    }
    
    # Supress google api deprecation warnings for cleaner JSON output
    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)
    
    commands[args.command](args)


if __name__ == "__main__":
    main()
