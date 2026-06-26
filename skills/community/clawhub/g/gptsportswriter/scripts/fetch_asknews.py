#!/usr/bin/env python3
import argparse
import json
import os
import sys

from asknews_sdk import AskNewsSDK


def main():
    ap = argparse.ArgumentParser(description="Fetch AskNews articles for GPTSportswriter context")
    ap.add_argument("query", help="Search query")
    ap.add_argument("--n-articles", type=int, default=5)
    ap.add_argument("--return-type", default="dicts")
    args = ap.parse_args()

    api_key = os.getenv("ASKNEWS_API_KEY")
    client_id = os.getenv("ASKNEWS_CLIENT_ID")
    client_secret = os.getenv("ASKNEWS_CLIENT_SECRET")
    if api_key:
        sdk = AskNewsSDK(api_key=api_key)
    elif client_id and client_secret:
        sdk = AskNewsSDK(client_id=client_id, client_secret=client_secret)
    else:
        print("ASKNEWS_API_KEY or ASKNEWS_CLIENT_ID / ASKNEWS_CLIENT_SECRET not set", file=sys.stderr)
        sys.exit(1)

    resp = sdk.news.search_news(
        query=args.query,
        n_articles=args.n_articles,
        return_type=args.return_type,
        method="kw",
    )

    articles = []
    if isinstance(resp, dict):
        articles = resp.get("as_dicts") or resp.get("articles") or []
    else:
        articles = getattr(resp, "as_dicts", None) or getattr(resp, "articles", None) or []

    normalized = []
    for a in articles:
        if isinstance(a, dict):
            normalized.append(a)
        elif hasattr(a, "model_dump"):
            normalized.append(a.model_dump())
        elif hasattr(a, "__dict__"):
            normalized.append(dict(a.__dict__))
        else:
            normalized.append({"value": str(a)})

    print(json.dumps({"query": args.query, "articles": normalized}, indent=2, default=str))


if __name__ == "__main__":
    main()
