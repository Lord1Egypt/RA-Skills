#!/usr/bin/env python3
"""Google Docs API — read document content via domain-wide delegation."""

import argparse
import json
import sys
from typing import Optional

from auth import get_service


def get_document(
    user: str,
    document_id: str,
) -> dict:
    """Get document metadata and structure.

    Args:
        user: Email address (impersonated via DWD).
        document_id: Google Docs document ID.

    Returns:
        Dict with document metadata.
    """
    service = get_service("docs", impersonate=user)
    doc = service.documents().get(documentId=document_id).execute()

    return {
        "document_id": doc.get("documentId", ""),
        "title": doc.get("title", ""),
        "revision_id": doc.get("revisionId", ""),
        "body_text": _extract_text(doc),
    }


def get_text(
    user: str,
    document_id: str,
) -> dict:
    """Get just the plain text content of a document.

    Args:
        user: Email address.
        document_id: Google Docs document ID.

    Returns:
        Dict with document text.
    """
    service = get_service("docs", impersonate=user)
    doc = service.documents().get(documentId=document_id).execute()

    return {
        "document_id": doc.get("documentId", ""),
        "title": doc.get("title", ""),
        "text": _extract_text(doc),
    }


def _extract_text(doc: dict) -> str:
    """Extract plain text from a Google Docs document structure."""
    body = doc.get("body", {})
    content = body.get("content", [])

    text_parts = []
    for element in content:
        if "paragraph" in element:
            paragraph = element["paragraph"]
            for elem in paragraph.get("elements", []):
                text_run = elem.get("textRun")
                if text_run:
                    text_parts.append(text_run.get("content", ""))

    return "".join(text_parts)


def main():
    parser = argparse.ArgumentParser(description="Google Docs read")
    sub = parser.add_subparsers(dest="command", required=True)

    # get
    p_get = sub.add_parser("get", help="Get document with full text")
    p_get.add_argument("--user", required=True)
    p_get.add_argument("--id", required=True, help="Document ID")

    # text
    p_text = sub.add_parser("text", help="Get document text only")
    p_text.add_argument("--user", required=True)
    p_text.add_argument("--id", required=True, help="Document ID")

    args = parser.parse_args()

    try:
        if args.command == "get":
            result = get_document(args.user, args.id)
        elif args.command == "text":
            result = get_text(args.user, args.id)
        else:
            result = {"error": f"Unknown command: {args.command}"}

        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
