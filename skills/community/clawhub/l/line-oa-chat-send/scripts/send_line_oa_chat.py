#!/usr/bin/env python3
"""Send one authorized LINE OA Chat message through an existing authenticated browser.

The default mode is dry-run: it finds and opens the chat without sending anything.
Use --send only after the user has authorized the exact recipient and message.
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass

try:
    from playwright.sync_api import Error, Locator, Page, sync_playwright
except ModuleNotFoundError:
    print(
        "ERROR: Playwright is not installed in this Python. Run "
        "scripts/run_line_oa_chat.sh, or provision a private runtime with "
        "scripts/setup_line_oa_runtime.sh --runtime-dir <private-runtime-dir>.",
        file=sys.stderr,
    )
    raise SystemExit(2)


@dataclass(frozen=True)
class Result:
    recipient: str
    sent: bool
    verified: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recipient", required=True, help="Exact LINE OA chat recipient name")
    parser.add_argument("--message", required=True, help="Exact message text to send")
    parser.add_argument(
        "--send",
        action="store_true",
        help="Actually send the message. Without this flag, the command is a dry-run.",
    )
    parser.add_argument(
        "--cdp-url",
        default="http://127.0.0.1:9222",
        help="Local Chromium CDP endpoint (default: %(default)s)",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=10,
        help="Maximum UI wait time in seconds (default: %(default)s)",
    )
    args = parser.parse_args()
    if not args.recipient.strip():
        parser.error("--recipient must not be blank")
    if not args.message.strip():
        parser.error("--message must not be blank")
    if args.timeout_seconds <= 0:
        parser.error("--timeout-seconds must be positive")
    return args


def chat_page(browser) -> Page:
    pages = [page for context in browser.contexts for page in context.pages]
    matches = [page for page in pages if page.url.startswith("https://chat.line.biz/")]
    if len(matches) != 1:
        raise RuntimeError(
            "Expected exactly one authenticated LINE OA Chat page; found "
            f"{len(matches)}. Use the protected interactive browser to complete login or close duplicates."
        )
    return matches[0]


def unique_chat_result(page: Page, recipient: str, timeout_ms: int) -> Locator:
    # `exact=True` prevents matching the unrelated "輸入搜尋內容" field.
    search = page.get_by_placeholder("搜尋", exact=True)
    search.fill(recipient)
    page.wait_for_timeout(min(timeout_ms, 1000))

    # The chat label can be hidden on responsive layouts. Its anchor remains clickable.
    results = page.locator("mark").filter(has_text=recipient).locator("xpath=ancestor::a")
    deadline = time.monotonic() + timeout_ms / 1000
    while results.count() == 0 and time.monotonic() < deadline:
        page.wait_for_timeout(200)

    count = results.count()
    if count != 1:
        raise RuntimeError(
            f"Recipient search for {recipient!r} returned {count} chat candidates; "
            "do not guess when the recipient is ambiguous."
        )
    return results.first


def run(args: argparse.Namespace) -> Result:
    timeout_ms = int(args.timeout_seconds * 1000)
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(args.cdp_url, timeout=timeout_ms)
        page = chat_page(browser)
        result = unique_chat_result(page, args.recipient, timeout_ms)
        result.click(timeout=timeout_ms)

        composer = page.locator("textarea-ex").locator("textarea")
        composer.wait_for(state="visible", timeout=timeout_ms)
        if not args.send:
            print(f"DRY-RUN OK: selected chat {args.recipient!r}; no message was sent.")
            return Result(args.recipient, sent=False, verified=False)

        composer.fill(args.message)
        send = page.locator('input[type="submit"][value="傳送"]')
        send.click(timeout=timeout_ms)

        deadline = time.monotonic() + args.timeout_seconds
        while time.monotonic() < deadline:
            transcript = page.locator("body").inner_text()
            try:
                composer_cleared = composer.input_value() == ""
            except Error:
                composer_cleared = False
            if composer_cleared and args.message in transcript:
                print(f"SENT AND VERIFIED: {args.recipient!r}")
                return Result(args.recipient, sent=True, verified=True)
            page.wait_for_timeout(250)

        raise RuntimeError(
            "Send was clicked but the UI did not verify the exact message in the active transcript. "
            "Inspect the protected browser before retrying to avoid a duplicate send."
        )


def main() -> int:
    args = parse_args()
    try:
        run(args)
    except (Error, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
