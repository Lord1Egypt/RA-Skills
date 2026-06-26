#!/usr/bin/env python3
"""
Ask Stocki a financial question (instant mode).

Usage:
    python3 stocki-instant.py <question> [--timezone Asia/Shanghai]

Stdout: markdown answer
Stderr: error messages
Exit:   0 success, 1 auth error, 2 service error
"""

import argparse
import asyncio
import os
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


STOCKI_URL = "https://instant-agent-test.miti.chat/"
ASSISTANT_ID = "InstantModeAgent"
MODEL_NAME = "gemini-anyint/gemini-3-flash-preview"
USER_ID = "fake_test_user"


async def query(question: str, timezone: str) -> str:
    from langgraph_sdk import get_client
    from langgraph.pregel.remote import RemoteGraph

    # Build time_prompt from timezone
    try:
        tz = ZoneInfo(timezone)
    except ZoneInfoNotFoundError:
        print(f"Unknown timezone '{timezone}', falling back to Asia/Shanghai", file=sys.stderr)
        tz = ZoneInfo("Asia/Shanghai")
    time_prompt = datetime.now(tz).strftime("Current time: %Y-%m-%d %H:%M:%S")

    client = get_client(url=STOCKI_URL)
    graph = RemoteGraph(ASSISTANT_ID, client=client)

    thread = await client.threads.create()
    thread_id = thread["thread_id"]

    response = await graph.ainvoke(
        input={
            "query": question,
            "messages": [],
            "time_prompt": time_prompt,
            "user_context": {},
        },
        config={
            "configurable": {
                "user_id": USER_ID,
                "thread_id": thread_id,
                "model_name": MODEL_NAME,
            }
        },
    )

    return response.get("answer", "")


def format_for_wechat(text: str) -> str:
    """Convert Stocki markdown output to WeChat-friendly plain text."""
    # 1. <stockidata> → bracket highlights
    text = re.sub(r"<stockidata>(.*?)</stockidata>", r"[\1]", text)

    # 2. Collect inline markdown links as footnotes
    #    Handles both [text](url) and [[N]](url) citation formats
    links = []
    def _replace_link(m):
        label, url = m.group(1), m.group(2)
        links.append(url)
        return f"[{len(links)}]"
    text = re.sub(r"\[+([^\]]*)\]+\((https?://[^\)]+)\)", _replace_link, text)

    # 3. Strip remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # 4. Simplify markdown formatting
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)  # headings
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)                # bold
    text = re.sub(r"\*(.+?)\*", r"\1", text)                    # italic
    text = re.sub(r"^[\-\*]\s+", "· ", text, flags=re.MULTILINE) # bullets

    # 5. Append footnote references
    if links:
        text = text.rstrip() + "\n\n---\n"
        for i, url in enumerate(links, 1):
            text += f"[{i}] {url}\n"

    return text


def main():
    parser = argparse.ArgumentParser(description="Ask Stocki a financial question.")
    parser.add_argument("question", help="The question to ask")
    parser.add_argument(
        "--timezone", default="Asia/Shanghai",
        help="IANA timezone for interpreting relative dates (default: Asia/Shanghai)",
    )
    args = parser.parse_args()

    try:
        answer = asyncio.run(query(args.question, args.timezone))
    except Exception as e:
        print(f"Stocki unavailable: {e}", file=sys.stderr)
        sys.exit(2)

    if answer is None:
        sys.exit(1)

    print(format_for_wechat(answer))


if __name__ == "__main__":
    main()
