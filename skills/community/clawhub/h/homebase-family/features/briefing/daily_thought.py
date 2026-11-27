"""Daily upbeat "Thought of the Day" for the morning briefing.

Pulls a fresh quote-of-the-day from ZenQuotes (free, no API key, no PII sent).
On ANY failure — network down, timeout, rate-limit placeholder, junk response —
falls back to a small local pool rotated by day-of-year, so the briefing always
has a fresh-feeling upbeat line and never breaks or goes silent (CLAUDE.md
principles 4 & 6). Python returns data only: no LLM, no WhatsApp send (principle 2).

Returns a ready-to-send, pre-formatted string (like the snack field) so the
agent pastes it verbatim rather than composing it — the composing model is not
relied on for daily variety, which is exactly why the old closing line repeated.
"""

import html
import json
import urllib.request
from datetime import date

ZENQUOTES_TODAY_URL = "https://zenquotes.io/api/today"

# Used only when the live fetch fails. Rotated by day-of-year so even the
# offline path varies day to day. Warm, family-facing, no attribution needed.
_FALLBACK_POOL = [
    "Small moments with your kids today are the ones they'll remember. Be present. ❤️",
    "Deep breath — you've handled every hard morning so far. Today's no different. \U0001f4aa",
    "You're doing better than you think. Enjoy the little wins today. \U0001f31f",
    "The days are long but the years are short. Soak up today. \U0001f490",
    "However today goes, your kids feel safe and loved — that's the whole game. \U0001f49b",
    "Go easy on yourself today. Good enough really is good enough. ✨",
    "One kind moment can change someone's whole day. Be that moment. \U0001f60a",
    "Progress, not perfection. Just take the next small step. \U0001f463",
    "Today is a fresh page. Make it a good one. \U0001f4d6",
    "Slow down for one minute today and just notice something good. \U0001f342",
    "You bring something to this family no one else can. Keep going. \U0001f31e",
    "Whatever today holds, you don't have to do it perfectly — just together. \U0001f91d",
    "A little laughter today goes a long way. Find a reason to smile. \U0001f604",
    "Be where your feet are today. This moment is the one that counts. \U0001f9e1",
]

_HEADER = "✨ *Thought of the Day*"


def _clean(text: str) -> str:
    return html.unescape((text or "").strip())


def _fetch_zenquotes(timeout: int = 5):
    """Return a formatted quote string from ZenQuotes, or None on any problem."""
    try:
        with urllib.request.urlopen(ZENQUOTES_TODAY_URL, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        item = data[0]
        quote = _clean(item.get("q"))
        author = _clean(item.get("a"))
        if not quote:
            return None
        # ZenQuotes serves a placeholder quote when rate-limited — reject it.
        low = quote.lower()
        if "too many requests" in low or "obtaining quotes" in low:
            return None
        if author and author.lower() != "zenquotes.io":
            return f"“{quote}” — {author}"
        return f"“{quote}”"
    except Exception:
        return None


def _fallback_line() -> str:
    idx = date.today().timetuple().tm_yday % len(_FALLBACK_POOL)
    return _FALLBACK_POOL[idx]


def get_daily_thought() -> str:
    """Return a ready-to-send upbeat closing block for the briefing. Never raises."""
    try:
        body = _fetch_zenquotes() or _fallback_line()
    except Exception:
        body = _fallback_line()
    return f"{_HEADER}\n{body}"
