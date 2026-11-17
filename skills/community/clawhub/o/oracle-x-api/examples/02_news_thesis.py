#!/usr/bin/env python3
"""Turn a headline into something with a precedent attached.

The shape worth copying is the cache check. News analysis is generated once and
stored, so the common path is a single GET. Starting a job for an article that
was already analysed spends the operator's own LLM budget to reproduce a result
they already have — which is why the job call only happens after the cached
read misses.

    python 02_news_thesis.py            # newest crypto item
    python 02_news_thesis.py <news_id>
"""

from __future__ import annotations

import sys
import time
from typing import Any

from client import OracleXError, get, post

POLL_INTERVAL_SECONDS = 3.0
POLL_TIMEOUT_SECONDS = 180.0


def latest_news_id(asset_type: str = "crypto") -> str:
    feed = get("/api/news", {"limit": 5, "asset_type": asset_type})
    rows = feed.get("items") or []
    if not rows:
        raise OracleXError(
            "The news cache is empty. The scheduler may not have run yet — "
            "check /api/system/health."
        )
    return str(rows[0]["id"])


def analysis_for(news_id: str) -> dict[str, Any]:
    """Return the LLM read of one article, generating it only if needed.

    The cached read answers 200 with a JSON `null` body when nothing has been
    generated yet — not 404. Treating a falsy body as an answer is how a caller
    ends up reporting "no analysis available" for an article the terminal would
    happily analyse in twenty seconds.
    """
    cached = get(f"/api/news/{news_id}/analysis")
    if cached:
        return cached

    job = post(f"/api/news/{news_id}/analysis/jobs")
    job_id = job.get("job_id") or job.get("id")
    if not job_id:
        raise OracleXError(f"Analysis job did not return an id: {job}")

    deadline = time.monotonic() + POLL_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        time.sleep(POLL_INTERVAL_SECONDS)
        state = get(f"/api/news/analysis/jobs/{job_id}")
        status = state.get("status")
        if status in {"completed", "done", "finished"}:
            return state.get("result") or state
        if status in {"failed", "error", "cancelled"}:
            raise OracleXError(f"Analysis failed: {state.get('error', status)}")

    raise OracleXError(
        f"Analysis for {news_id} did not finish within "
        f"{POLL_TIMEOUT_SECONDS:.0f}s. It may still complete — poll "
        f"/api/news/analysis/jobs/{job_id} again later."
    )


def precedent(headline: str, summary: str = "") -> dict[str, Any]:
    """Ask the store whether this story has run before.

    This is the step that separates a summary from a thesis. A regulatory
    headline resembling four earlier ones, each followed by a drawdown, is a
    different object from one with no precedent — and the answer only exists
    inside this instance's own memory.

    Skip it when the cached analysis already carries a `precedents` list: the
    analysis pipeline runs the same lookup, so calling again re-embeds the
    headline for a result already in hand.
    """
    return post("/api/rag/news-similarity", {"title": headline, "summary": summary})


def main() -> int:
    news_id = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        news_id = news_id or latest_news_id()
        article = get(f"/api/news/{news_id}")
        headline = article.get("title", "")
        print(f"# {headline}\n")

        analysis = analysis_for(news_id)
        print("## Analysis")
        print(
            f"Sentiment: {analysis.get('sentiment')} "
            f"(confidence {analysis.get('confidence')})"
        )
        print(
            f"Risk: {analysis.get('risk_level')} · "
            f"horizon {analysis.get('time_horizon')} · "
            f"impact {analysis.get('price_impact')}"
        )
        print(f"\n{analysis.get('reasoning', '')}")
        if analysis.get("invalidation"):
            print(f"\nInvalidated by: {analysis['invalidation']}")

        print("\n## Precedent")
        # The analysis already ran the similarity lookup. Reuse it, and only
        # pay for a fresh embedding when it did not.
        matches = analysis.get("precedents")
        if matches is None:
            similar = precedent(headline, article.get("summary", ""))
            matches = similar.get("similar_events") or []
            if similar.get("summary"):
                print(similar["summary"])
        if not matches:
            print("Nothing in the store resembles this. Treat it as unprecedented.")
        for match in matches[:5]:
            print(
                f"- {match.get('title')} ({match.get('date')}) → "
                f"{match.get('outcome')}, {match.get('price_change')}% "
                f"(similarity {match.get('similarity', '?')})"
            )
    except OracleXError as exc:
        print(exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
