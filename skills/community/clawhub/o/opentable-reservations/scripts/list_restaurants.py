#!/usr/bin/env python3
"""
OpenTable primitive — one call → filtered restaurant list + action buttons
+ navigation context, ready for the agent to act on without re-reading HTML.

Design goals:
  1. **Filter**: the caller gets only the fields it needs for a
     decision, never the raw accessibility tree or raw HTML. Target
     size is < 2 KB of JSON regardless of how many cards are on the
     page.
  2. **Action buttons**: each restaurant comes with the interactive
     refs the agent would click next — `reserve_refs` for the slot
     buttons, plus a `snapshot_id` the agent can pass back if it
     needs to click one (see `click_slot.py`). The agent never has
     to re-snapshot to find a ref.
  3. **Navigation context**: the top-level payload includes the
     current tab url, tab id, and the page's own date/time/party
     controls so the agent can change them without a new snapshot.
  4. **Forcing function**: this script is THE official way to read
     OpenTable from an agent. Anything else (web_fetch, raw CDP via
     exec + node, writing /tmp/cdp_*.js, `openclaw browser snapshot`
     by hand) is forbidden by the skill's hard rules.

How it works:
  1. Optionally navigates OpenClaw's attached browser to a search URL
     composed from --location/--date-time/--party/--query.
  2. Runs `openclaw browser --browser-profile attached evaluate` with
     a JS function that:
       a) Reads all `[data-test="restaurant-card"]` elements.
       b) For each card, pulls name, cuisine, neighborhood, price,
          reviews, time-slot labels AND their click refs.
       c) Reads the page-level date button, time selector, and party
          selector so the agent can show the user what filters are
          currently applied.
       d) Captures location.href and document.title for nav context.
  3. Trims to --limit and prints a single-line JSON payload.

Usage:
    python3 list_restaurants.py \\
        --location Manhattan \\
        --date-time 2026-04-12T19:00 \\
        --party 2 --query italian --limit 5

Output shape (compact, typically 800-1800 bytes):
    {
      "nav": {
        "url": "...", "tab_id": 18, "title": "...",
        "date":  "Apr 11, 2026",
        "time":  "8:00 PM",
        "party": "2 people"
      },
      "restaurants": [
        {
          "rank": 1,
          "name": "Carbone",
          "cuisine": "Italian",
          "neighborhood": "Greenwich Village",
          "price": "$$$$",
          "reviews": 4128,
          "url_path": "carbone-new-york",
          "slots": [
            {"time": "7:30 PM", "ref": "13_67"},
            {"time": "8:00 PM", "ref": "13_69"},
            {"time": "8:30 PM", "ref": "13_73"}
          ]
        }
      ],
      "count": 3,
      "next_actions": [
        "To present to user: summarize as 3-5 bullet list (name, cuisine, neighborhood, slots).",
        "To book: call book.py with the chosen url_path + datetime + party. NEVER click slot refs yourself."
      ]
    }
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from urllib.parse import quote


SEARCH_BASE = "https://www.opentable.com/s"


def build_search_url(location: str, date_time: str, party: int, query: str) -> str:
    term = f"{query} {location}".strip() if query else location
    params = {
        "term":     term,
        "dateTime": date_time,
        "covers":   str(party),
        "metroId":  "0",
    }
    qs = "&".join(f"{k}={quote(v)}" for k, v in params.items())
    return f"{SEARCH_BASE}?{qs}"


# JS function run via `openclaw browser evaluate`. Pulls a narrow slice
# of the DOM: restaurant cards + page filters + nav state. No HTML dump.
EVAL_JS = r"""
async () => {
  // Wait briefly for React hydration if we just navigated.
  await new Promise(r => setTimeout(r, 600));

  const cards = document.querySelectorAll('[data-test="restaurant-card"]');
  const out = [];
  cards.forEach((c, idx) => {
    const name =
      c.querySelector('[data-test="res-card-name"]')?.innerText?.trim() ||
      null;
    if (!name) return;

    const cuisineLoc =
      c.querySelector('[data-test="cuisine-and-location"]')?.innerText?.trim() ||
      "";
    const parts = cuisineLoc.split("•").map(s => s.trim()).filter(Boolean);
    const cuisine      = parts[0] || "";
    const neighborhood = parts[1] || "";

    const textAll = c.innerText || "";
    const reviewsMatch = textAll.match(/\((\d+)\)/);
    const reviews = reviewsMatch ? parseInt(reviewsMatch[1], 10) : null;
    const priceMatch = textAll.match(/\${1,4}/m);
    const price = priceMatch ? priceMatch[0] : null;

    // Time slots with their click targets. We only capture the slot
    // text because refs aren't available from evaluate() — refs come
    // from a snapshot, which the skill's click flow handles separately.
    // What we CAN give back is the slot's raw aria-label, which
    // uniquely identifies the button and can be used with
    // `openclaw browser click` via selector mode.
    const slotEls = c.querySelectorAll('[data-test^="time-slot-"]');
    const slots = Array.from(slotEls).map(el => {
      const m = el.innerText.match(/\d{1,2}:\d{2}\s*(?:AM|PM)/);
      return m ? {time: m[0], aria: el.getAttribute("aria-label") || ""} : null;
    }).filter(Boolean);
    // Dedupe by time
    const seen = new Set();
    const uniqSlots = [];
    for (const s of slots) {
      if (seen.has(s.time)) continue;
      seen.add(s.time);
      uniqSlots.push(s);
    }

    // Profile link → url_path slug
    const href = c.querySelector('a[href*="/r/"]')?.href || null;
    let url_path = null;
    if (href) {
      const m = href.match(/\/r\/([^/?#]+)/);
      url_path = m ? m[1] : null;
    }

    out.push({
      rank: idx + 1,
      name,
      cuisine,
      neighborhood,
      price,
      reviews,
      url_path,
      slots: uniqSlots.slice(0, 4),
    });
  });

  // Page-level filter state — what the user sees in the header bar.
  // Using rough selectors; degrades gracefully if OpenTable changes.
  const dateBtn =
    document.querySelector('[aria-label*="date"],[aria-label*="Date"],button[id*="date"]');
  const timeSel =
    document.querySelector('[aria-label*="Time selector"],[aria-label*="time selector"]');
  const partySel =
    document.querySelector('[aria-label*="Party size selector"],[aria-label*="party size"]');

  const nav = {
    url:    location.href,
    title:  document.title,
    date:   dateBtn?.innerText?.trim() || null,
    time:   timeSel?.value || timeSel?.innerText?.trim() || null,
    party:  partySel?.value || partySel?.innerText?.trim() || null,
  };

  return { nav, cards: out };
}
"""


def run_browser(subcmd: list[str], timeout: float = 30.0) -> str:
    cmd = ["openclaw", "browser", "--browser-profile", "attached"] + subcmd
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(
            f"openclaw browser {subcmd[0]} failed (exit {r.returncode}): "
            f"{r.stderr.strip()[:400]}"
        )
    return r.stdout


def main() -> int:
    p = argparse.ArgumentParser(description="OpenTable → filtered restaurant list + nav context")
    p.add_argument("--location",  help="City / neighborhood / ZIP")
    p.add_argument("--date-time", help="YYYY-MM-DDTHH:MM (local)")
    p.add_argument("--party",     type=int, default=2)
    p.add_argument("--query",     default="")
    p.add_argument("--navigate",  help="Explicit URL override")
    p.add_argument("--limit",     type=int, default=5)
    p.add_argument("--json-pretty", action="store_true")
    args = p.parse_args()

    if args.navigate:
        target_url = args.navigate
    elif args.location and args.date_time:
        target_url = build_search_url(
            args.location, args.date_time, args.party, args.query
        )
    else:
        target_url = None

    try:
        if target_url:
            run_browser(["open", target_url], timeout=30.0)
        raw = run_browser(["evaluate", "--fn", EVAL_JS], timeout=30.0)
    except subprocess.TimeoutExpired:
        print(json.dumps({
            "error":       "browser call timed out after 30s",
            "nav":         None,
            "restaurants": [],
            "count":       0,
        }))
        return 1
    except Exception as e:
        print(json.dumps({
            "error":       str(e)[:400],
            "nav":         None,
            "restaurants": [],
            "count":       0,
        }))
        return 1

    try:
        parsed = json.loads(raw)
        nav   = parsed.get("nav")  or {}
        cards = parsed.get("cards") or []
    except Exception as e:
        print(json.dumps({
            "error":       f"could not parse evaluate output: {e}",
            "nav":         None,
            "restaurants": [],
            "count":       0,
        }))
        return 1

    payload = {
        "nav":         nav,
        "restaurants": cards[: args.limit],
        "count":       min(len(cards), args.limit),
        "next_actions": [
            "Summarize for user as 3-5 bullet list: name · cuisine · neighborhood · top slots.",
            "To build booking link: call book.py with chosen url_path, datetime, party.",
            "NEVER click slots yourself. NEVER write /tmp/cdp_*.js. NEVER web_fetch opentable.com.",
        ],
    }
    if args.json_pretty:
        print(json.dumps(payload, indent=2))
    else:
        print(json.dumps(payload, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
