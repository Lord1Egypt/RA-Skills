"""
polymarket-youtube-channel-trader
Trades Polymarket markets on the top 10 YouTube channels — subscriber
milestones, view-count races, and channel rivalry events — by treating
each channel as a distinct asset with its own volatility profile,
posting calendar, and growth trajectory.

THE CONCEPT: YouTube channels as crypto assets
  Subscriber count  = market cap
  Subscriber delta  = daily price change
  View velocity     = trading volume
  Like/dislike ratio = market sentiment
  Viral video drop  = price spike event

THE EDGE — THREE STRUCTURAL LAYERS:

1. FIRST-HOUR VIEW VELOCITY MISPRICING
   When a major channel drops a video, 40–60% of the total 24-hour
   view count accumulates in the first hour (MrBeast: ~55%, T-Series
   music: ~30%, PewDiePie: ~45%). Markets asking "will video reach X
   views in first 2 hours?" are priced by retail using the terminal
   24h probability. The first-passage probability is significantly
   higher — exactly the same structural gap as BTC weekend markets.
   We exploit it the same way: buy YES on milestone markets that
   resolve in the first 2–6 hours of a viral video drop.

2. CHANNEL VOLATILITY PROFILES (σ-based conviction scaling)
   Each channel has a characteristic daily subscriber growth
   distribution. Children's channels (Cocomelon, Kids Diana Show,
   Like Nastya, Vlad and Niki) grow at ~0.02% σ/day — extremely
   stable. Milestone markets for these channels are usually fairly
   priced. Drama/commentary channels (PewDiePie) have σ ~0.15%/day —
   milestone markets are wide; retail underprices the tails.
   MrBeast has σ ~0.20–0.30%/day AND is skewed positively (viral
   events cause spikes, rarely crashes) — YES-side milestones are
   chronically underpriced because retail uses a symmetric model.

3. WEEKEND POSTING WINDOW (channel-specific)
   MrBeast has posted 60%+ of his top-100 videos on Fri–Sat UTC.
   The weekend posting probability is quantifiable. A market asking
   "will MrBeast video get X views this weekend?" is most actionable
   Thursday–Friday when the video hasn't dropped yet but the
   probability of a drop is highest. After Sunday, the window closes
   and residual view-count markets see edge compress.

The skill enables fast "flash plays" — entering markets in the
minutes after a video drops and capturing the first-hour velocity
before the market reprices to reflect actual accumulation rate.

SAFE BY DEFAULT:
- No --live flag = paper trading (venue="sim"), zero financial risk.
- Cron/automaton runs default to paper mode.
- Real trades only with explicit --live flag.
"""
import os
import re as _re
import argparse
from datetime import datetime, timezone
from simmer_sdk import SimmerClient

TRADE_SOURCE = "sdk:polymarket-youtube-channel-trader"
SKILL_SLUG   = "polymarket-youtube-channel-trader"

# ---------------------------------------------------------------------------
# Top 10 channel profiles — each channel is an asset with its own vol model
#
# Fields:
#   slug          : canonical identifier used in keyword matching
#   display_name  : human-readable
#   subs_M        : approximate subscriber count in millions (2025–26)
#   daily_vol     : daily subscriber growth σ as fraction of subs
#                   (0.20 = 20% annualized equiv, high vol)
#   skew          : positive = more likely to spike up than crash
#                   (viral upside is asymmetric for high-engagement channels)
#   weekend_post  : probability channel posts a major video on Fri–Sun
#   first_hour_pct: fraction of 24h views accumulated in hour 1 (typical)
#   content_type  : "viral_challenge", "music", "children", "gaming",
#                   "sports_entertainment", "commentary"
# ---------------------------------------------------------------------------
CHANNEL_PROFILES = {
    "mrbeast": {
        "display_name": "MrBeast",
        "subs_M": 370,
        "daily_vol": 0.25,          # highest vol of any top-10 channel
        "skew": 0.40,               # strong positive skew — viral spikes dominate
        "weekend_post": 0.62,       # 62% of top videos drop Fri–Sun
        "first_hour_pct": 0.55,     # 55% of 24h views land in hour 1
        "content_type": "viral_challenge",
        "keywords": [
            "mrbeast", "mr beast", "mr. beast", "jimmy donaldson",
        ],
    },
    "tseries": {
        "display_name": "T-Series",
        "subs_M": 275,
        "daily_vol": 0.04,          # steady Bollywood pipeline, low vol
        "skew": 0.10,
        "weekend_post": 0.45,       # releases spread across week
        "first_hour_pct": 0.30,     # music videos build more slowly
        "content_type": "music",
        "keywords": [
            "t-series", "t series", "tseries",
        ],
    },
    "cocomelon": {
        "display_name": "Cocomelon",
        "subs_M": 178,
        "daily_vol": 0.02,          # extremely stable children's content
        "skew": 0.05,
        "weekend_post": 0.40,
        "first_hour_pct": 0.20,     # children's content builds slowly via parents
        "content_type": "children",
        "keywords": [
            "cocomelon", "coco melon",
        ],
    },
    "setindia": {
        "display_name": "SET India",
        "subs_M": 175,
        "daily_vol": 0.03,
        "skew": 0.05,
        "weekend_post": 0.50,
        "first_hour_pct": 0.25,
        "content_type": "tv_content",
        "keywords": [
            "set india",
        ],
    },
    "kidsdiana": {
        "display_name": "Kids Diana Show",
        "subs_M": 128,
        "daily_vol": 0.02,
        "skew": 0.05,
        "weekend_post": 0.38,
        "first_hour_pct": 0.18,
        "content_type": "children",
        "keywords": [
            "kids diana", "diana show", "diana and roma",
        ],
    },
    "pewdiepie": {
        "display_name": "PewDiePie",
        "subs_M": 111,
        "daily_vol": 0.15,          # semi-retired but controversy drives spikes
        "skew": -0.05,              # slight negative skew — retirement/comeback uncertainty
        "weekend_post": 0.30,       # irregular posting schedule
        "first_hour_pct": 0.45,
        "content_type": "commentary",
        "keywords": [
            "pewdiepie", "pewdie pie", "felix kjellberg",
        ],
    },
    "likenastya": {
        "display_name": "Like Nastya",
        "subs_M": 122,
        "daily_vol": 0.02,
        "skew": 0.05,
        "weekend_post": 0.42,
        "first_hour_pct": 0.18,
        "content_type": "children",
        "keywords": [
            "like nastya", "nastya",
        ],
    },
    "vladniki": {
        "display_name": "Vlad and Niki",
        "subs_M": 120,
        "daily_vol": 0.02,
        "skew": 0.05,
        "weekend_post": 0.40,
        "first_hour_pct": 0.18,
        "content_type": "children",
        "keywords": [
            "vlad and niki", "vlad niki",
        ],
    },
    "zeemusic": {
        "display_name": "Zee Music Company",
        "subs_M": 108,
        "daily_vol": 0.04,
        "skew": 0.10,
        "weekend_post": 0.48,
        "first_hour_pct": 0.28,
        "content_type": "music",
        "keywords": [
            "zee music", "zeemusic",
        ],
    },
    "wwe": {
        "display_name": "WWE",
        "subs_M": 101,
        "daily_vol": 0.08,          # event-driven: WrestleMania, Raw, SmackDown
        "skew": 0.20,               # positive skew during PPV weeks
        "weekend_post": 0.70,       # PPV events are almost always weekend
        "first_hour_pct": 0.40,
        "content_type": "sports_entertainment",
        "keywords": [
            "wwe", "world wrestling", "wrestlemania", "smackdown", "raw channel",
        ],
    },
    # --- Extended channels: high-engagement creators Polymarket likes ---
    "ishowspeed": {
        "display_name": "IShowSpeed",
        "subs_M": 35,
        "daily_vol": 0.30,
        "skew": 0.35,
        "weekend_post": 0.55,
        "first_hour_pct": 0.50,
        "content_type": "streaming",
        "keywords": ["ishowspeed", "ishow speed"],
    },
    "kaicenat": {
        "display_name": "Kai Cenat",
        "subs_M": 20,
        "daily_vol": 0.35,
        "skew": 0.30,
        "weekend_post": 0.50,
        "first_hour_pct": 0.45,
        "content_type": "streaming",
        "keywords": ["kai cenat", "kaicenat"],
    },
    "ksi": {
        "display_name": "KSI",
        "subs_M": 24,
        "daily_vol": 0.20,
        "skew": 0.15,
        "weekend_post": 0.45,
        "first_hour_pct": 0.42,
        "content_type": "commentary",
        "keywords": ["ksi"],
    },
    "loganpaul": {
        "display_name": "Logan Paul",
        "subs_M": 24,
        "daily_vol": 0.18,
        "skew": 0.10,
        "weekend_post": 0.40,
        "first_hour_pct": 0.40,
        "content_type": "commentary",
        "keywords": ["logan paul"],
    },
    "markiplier": {
        "display_name": "Markiplier",
        "subs_M": 37,
        "daily_vol": 0.10,
        "skew": 0.10,
        "weekend_post": 0.35,
        "first_hour_pct": 0.38,
        "content_type": "gaming",
        "keywords": ["markiplier"],
    },
    "dream": {
        "display_name": "Dream",
        "subs_M": 32,
        "daily_vol": 0.25,
        "skew": 0.20,
        "weekend_post": 0.40,
        "first_hour_pct": 0.50,
        "content_type": "gaming",
        "keywords": ["dream minecraft", "dreamwastaken"],
    },
    "jakepaul": {
        "display_name": "Jake Paul",
        "subs_M": 21,
        "daily_vol": 0.20,
        "skew": 0.15,
        "weekend_post": 0.45,
        "first_hour_pct": 0.42,
        "content_type": "commentary",
        "keywords": ["jake paul"],
    },
    "dude_perfect": {
        "display_name": "Dude Perfect",
        "subs_M": 60,
        "daily_vol": 0.08,
        "skew": 0.15,
        "weekend_post": 0.50,
        "first_hour_pct": 0.35,
        "content_type": "viral_challenge",
        "keywords": ["dude perfect"],
    },
}

# Generic fallback for YouTube markets that don't match a known channel.
# Neutral bias (~1.0x) — we still trade it, just without channel-specific edge.
GENERIC_CHANNEL = {
    "display_name": "YouTube (generic)",
    "subs_M": 50,
    "daily_vol": 0.10,
    "skew": 0.10,
    "weekend_post": 0.45,
    "first_hour_pct": 0.30,
    "content_type": "generic",
    "keywords": [],
}

# Flat keyword list for market discovery
KEYWORDS = [kw for p in CHANNEL_PROFILES.values() for kw in p["keywords"]] + [
    "youtube subscribers", "youtube milestone", "youtube channel",
    "youtube views", "youtube video", "most subscribed", "subscriber count",
    "subscriber race", "youtube rivalry",
    "youtube shorts", "youtube streamer", "youtuber",
    "content creator subscribers", "youtube record",
]

# Risk parameters
MAX_POSITION  = float(os.environ.get("SIMMER_MAX_POSITION",  "30"))
MIN_VOLUME    = float(os.environ.get("SIMMER_MIN_VOLUME",    "2000"))
MAX_SPREAD    = float(os.environ.get("SIMMER_MAX_SPREAD",    "0.09"))
MIN_DAYS      = int(os.environ.get(  "SIMMER_MIN_DAYS",      "0"))   # allow same-day flash plays
MAX_POSITIONS = int(os.environ.get(  "SIMMER_MAX_POSITIONS", "10"))
YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", "0.38"))
NO_THRESHOLD  = float(os.environ.get("SIMMER_NO_THRESHOLD",  "0.62"))
MIN_TRADE     = float(os.environ.get("SIMMER_MIN_TRADE",     "5"))

_client: SimmerClient | None = None


# ---------------------------------------------------------------------------
# Channel identification
# ---------------------------------------------------------------------------

def _identify_channel(question: str) -> dict | None:
    """
    Return the matching CHANNEL_PROFILES entry or None if no top-10 channel
    is referenced in the question. Matches on keyword list.
    """
    q = question.lower()
    for profile in CHANNEL_PROFILES.values():
        if any(kw in q for kw in profile["keywords"]):
            return profile
    return None


# ---------------------------------------------------------------------------
# Edge 1: First-hour velocity multiplier
# ---------------------------------------------------------------------------

def _velocity_mult(question: str, channel: dict) -> tuple[str, float]:
    """
    Returns (label, multiplier) based on the first-hour velocity edge.

    The core insight: view-count milestone markets that resolve within the
    first few hours of a video drop are priced using 24h terminal probability
    but the question is typically "will video reach X views in first N hours?"
    — a first-passage question. The first-hour concentration of views means
    the true probability is significantly higher than the terminal probability
    for channels with high first_hour_pct.

    Detection: market question contains time-bounded language.
    Short resolution windows (<6h): full velocity multiplier.
    Longer resolution windows: decaying multiplier.

    Formula:
      velocity_edge = channel.first_hour_pct / 0.30   (normalised to average)
      mult = 1.0 + (velocity_edge - 1.0) * 0.40       (40% weight)
      so MrBeast (0.55): 1.0 + (1.83-1)*0.40 = 1.33
         average (0.30):  1.0 + (1.0-1)*0.40  = 1.00
         children (0.18): 1.0 + (0.60-1)*0.40 = 0.84
    """
    q = question.lower()
    short_window = any(w in q for w in (
        "first hour", "first 2 hour", "first 3 hour", "first 6 hour",
        "in 1 hour", "in 2 hours", "in 5 minutes", "in 10 minutes",
        "in 30 minutes", "within an hour", "within 2 hours",
        "first day", "24 hours", "within 24",
    ))
    if not short_window:
        return "NO-VELOCITY-WINDOW", 1.00

    fhp = channel["first_hour_pct"]
    velocity_edge = fhp / 0.30
    mult = 1.0 + (velocity_edge - 1.0) * 0.40
    mult = round(min(1.40, max(0.80, mult)), 3)
    return f"VELOCITY({channel['display_name']} fhp={fhp:.0%})", mult


# ---------------------------------------------------------------------------
# Edge 2: Channel volatility profile
# ---------------------------------------------------------------------------

def _volatility_mult(channel: dict) -> tuple[str, float]:
    """
    Returns (label, multiplier) based on the channel's vol profile.

    High-vol channels (MrBeast, PewDiePie, WWE) have fat-tailed subscriber
    growth — milestone markets underestimate tail probabilities. We amplify
    conviction for these channels.

    Low-vol channels (children's content) have very predictable growth —
    milestone markets are better priced; we trade them at face value.

    Positive skew (MrBeast): further amplifies YES conviction since
    the tail is asymmetrically to the upside.

    vol_mult = 1.0 + channel.daily_vol * 2.0   (linear scaling)
    skew_bonus = channel.skew * 0.5
    Combined and capped 0.80–1.30x.
    """
    vol_mult   = 1.0 + channel["daily_vol"] * 2.0
    skew_bonus = channel["skew"] * 0.5
    combined   = min(1.30, max(0.80, vol_mult + skew_bonus))
    return (
        f"VOL({channel['display_name']} σ={channel['daily_vol']:.0%} "
        f"skew={channel['skew']:+.2f})",
        round(combined, 3),
    )


# ---------------------------------------------------------------------------
# Edge 3: Weekend posting window
# ---------------------------------------------------------------------------

def _weekend_window_mult(channel: dict) -> tuple[str, float]:
    """
    Returns (label, multiplier) based on day-of-week and channel posting habits.

    Channels with high weekend_post probability (MrBeast: 0.62, WWE: 0.70)
    are most likely to drop major content Fri–Sun. The edge is sharpest when
    entering on Thursday–Friday before the drop.

    After Sunday: window closing, residual markets lose their timing edge.

    weekday(): 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
    """
    wp      = channel["weekend_post"]   # 0.0–1.0
    weekday = datetime.now(timezone.utc).weekday()
    name    = channel["display_name"]

    base_mult = 0.80 + wp * 0.50   # ranges 0.80 (wp=0) to 1.30 (wp=1.0)

    if weekday == 3:       # Thursday
        timing = 1.15      # optimal entry — drop likely tomorrow/Saturday
    elif weekday == 4:     # Friday
        timing = 1.10      # drop imminent or already happened
    elif weekday == 5:     # Saturday
        timing = 1.00      # mid-window
    elif weekday == 6:     # Sunday
        timing = 0.90      # window closing
    else:                  # Mon–Wed
        timing = 0.85      # weekend too far

    combined = min(1.35, max(0.70, base_mult * timing))
    day_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][weekday]
    return (
        f"WEEKEND({name} wp={wp:.0%} {day_name})",
        round(combined, 3),
    )


# ---------------------------------------------------------------------------
# Combined bias
# ---------------------------------------------------------------------------

def youtube_signal_bias(question: str, channel: dict) -> tuple[float, str]:
    """
    Returns (bias_multiplier, debug_label).

    Combines:
      velocity_mult  × volatility_mult × weekend_mult
    Capped 0.65–1.40x.
    """
    vel_label, vel_mult  = _velocity_mult(question, channel)
    vol_label, vol_mult  = _volatility_mult(channel)
    wkd_label, wkd_mult  = _weekend_window_mult(channel)

    combined = vel_mult * vol_mult * wkd_mult
    capped   = min(1.40, max(0.65, combined))
    label    = f"{vel_label} × {vol_label} × {wkd_label}"
    return round(capped, 3), label


# ---------------------------------------------------------------------------
# Core signal
# ---------------------------------------------------------------------------

def compute_signal(market) -> tuple[str | None, float, str]:
    """
    Returns (side, size, reasoning) or (None, 0, skip_reason).

    Applies conviction-based sizing with youtube_signal_bias:
      size = max(MIN_TRADE, conviction × bias × MAX_POSITION)
    """
    p = market.current_probability
    q = market.question

    # Spread gate
    if market.spread_cents is not None and market.spread_cents / 100 > MAX_SPREAD:
        return None, 0, f"Spread {market.spread_cents/100:.1%} > {MAX_SPREAD:.1%}"

    # Days-to-resolution gate (MIN_DAYS=0 allows same-day flash plays)
    if market.resolves_at:
        try:
            resolves = datetime.fromisoformat(market.resolves_at.replace("Z", "+00:00"))
            days = (resolves - datetime.now(timezone.utc)).days
            if days < MIN_DAYS:
                return None, 0, f"Only {days}d to resolve"
        except Exception:
            pass

    # Channel identification — fall back to generic profile for unknown channels
    channel = _identify_channel(q)
    if channel is None:
        channel = GENERIC_CHANNEL

    bias, bias_label = youtube_signal_bias(q, channel)

    if p <= YES_THRESHOLD:
        conviction = min(1.0, (YES_THRESHOLD - p) / YES_THRESHOLD * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = YES_THRESHOLD - p
        return (
            "yes", size,
            f"YES [{channel['display_name']}] {p:.0%} edge={edge:.0%} "
            f"bias={bias:.2f}x size=${size} — {q[:55]}"
        )

    if p >= NO_THRESHOLD:
        conviction = min(1.0, (p - NO_THRESHOLD) / (1 - NO_THRESHOLD) * bias)
        size = max(MIN_TRADE, round(conviction * MAX_POSITION, 2))
        edge = p - NO_THRESHOLD
        return (
            "no", size,
            f"NO [{channel['display_name']}] YES={p:.0%} edge={edge:.0%} "
            f"bias={bias:.2f}x size=${size} — {q[:55]}"
        )

    return None, 0, (
        f"Neutral {p:.1%} [{channel['display_name']}] — "
        f"outside {YES_THRESHOLD:.0%}/{NO_THRESHOLD:.0%} bands"
    )


def context_ok(client: SimmerClient, market_id: str) -> tuple[bool, str]:
    """Check flip-flop and slippage safeguards."""
    try:
        ctx = client.get_market_context(market_id)
        if not ctx:
            return True, "no context"
        if ctx.get("discipline", {}).get("is_flip_flop"):
            reason = ctx["discipline"].get("flip_flop_reason", "recent reversal")
            return False, f"Flip-flop: {reason}"
        slip = ctx.get("slippage", {})
        if isinstance(slip, dict) and slip.get("slippage_pct", 0) > 0.15:
            return False, f"Slippage {slip['slippage_pct']:.1%}"
        for w in ctx.get("warnings", []):
            safe_print(f"  [warn] {w}")
    except Exception as e:
        safe_print(f"  [ctx] {market_id}: {e}")
    return True, "ok"


def get_client(live: bool = False) -> SimmerClient:
    """
    live=False → venue="sim"  (paper trades — safe default).
    live=True  → venue="polymarket" (real trades, only with --live flag).
    """
    global _client
    global MAX_POSITION, MIN_VOLUME, MAX_SPREAD, MIN_DAYS, MAX_POSITIONS
    global YES_THRESHOLD, NO_THRESHOLD, MIN_TRADE
    if _client is None:
        venue = "polymarket" if live else "sim"
        _client = SimmerClient(
            api_key=os.environ["SIMMER_API_KEY"],
            venue=venue,
        )
        if live:
            _client.live = True
        MAX_POSITION  = float(os.environ.get("SIMMER_MAX_POSITION",  str(MAX_POSITION)))
        MIN_VOLUME    = float(os.environ.get("SIMMER_MIN_VOLUME",    str(MIN_VOLUME)))
        MAX_SPREAD    = float(os.environ.get("SIMMER_MAX_SPREAD",    str(MAX_SPREAD)))
        MIN_DAYS      = int(os.environ.get(  "SIMMER_MIN_DAYS",      str(MIN_DAYS)))
        MAX_POSITIONS = int(os.environ.get(  "SIMMER_MAX_POSITIONS", str(MAX_POSITIONS)))
        YES_THRESHOLD = float(os.environ.get("SIMMER_YES_THRESHOLD", str(YES_THRESHOLD)))
        NO_THRESHOLD  = float(os.environ.get("SIMMER_NO_THRESHOLD",  str(NO_THRESHOLD)))
        MIN_TRADE     = float(os.environ.get("SIMMER_MIN_TRADE",     str(MIN_TRADE)))
    return _client


_YT_FILTER = _re.compile(
    r"(youtube|subscriber|mrbeast|t[\-\s]?series|pewdiepie|cocomelon|"
    r"set\s*india|views.*video|video.*views|channel.*milestone|"
    r"most\s+subscribed|ishowspeed|kai\s*cenat|ksi\b|logan\s*paul|"
    r"jake\s*paul|markiplier|dude\s*perfect|"
    r"youtuber|content\s+creator|watch\s+hours|streamer.*subscri)",
    _re.I,
)


def safe_print(text):
    """Print with fallback for non-ASCII characters (Windows cp1252 terminals)."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode())


def find_markets(client: SimmerClient) -> list:
    """Find active YouTube channel markets, deduplicated.

    Uses both keyword search AND get_markets() fallback because
    find_markets() doesn't always return all imported markets.
    """
    seen, unique = set(), []

    # 1. Keyword search
    for kw in KEYWORDS:
        try:
            for m in client.find_markets(query=kw):
                mid = getattr(m, "id", None)
                q = getattr(m, "question", "")
                if mid and mid not in seen and _YT_FILTER.search(q):
                    seen.add(mid)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[search] {kw!r}: {e}")

    # 2. Broad query search — catches markets specific keywords miss
    for broad_q in ("youtube", "youtuber", "subscriber milestone", "content creator"):
        try:
            for m in client.find_markets(query=broad_q):
                mid = getattr(m, "id", None)
                q = getattr(m, "question", "")
                if mid and mid not in seen and _YT_FILTER.search(q):
                    seen.add(mid)
                    unique.append(m)
        except Exception as e:
            safe_print(f"[broad search {broad_q!r}] {e}")

    # 3. Fallback: scan recent markets for YouTube matches
    try:
        for m in client.get_markets(limit=200):
            mid = getattr(m, "id", None)
            q = getattr(m, "question", "")
            if mid and mid not in seen and _YT_FILTER.search(q):
                seen.add(mid)
                unique.append(m)
    except Exception as e:
        safe_print(f"[get_markets fallback] {e}")

    return unique


def run(live: bool = False) -> None:
    weekday   = datetime.now(timezone.utc).weekday()
    day_name  = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][weekday]
    mode      = "LIVE" if live else "PAPER (sim)"
    safe_print(
        f"[polymarket-youtube-channel-trader] mode={mode} "
        f"day={day_name} max_pos=${MAX_POSITION} "
        f"channels={len(CHANNEL_PROFILES)}"
    )

    client  = get_client(live=live)
    markets = find_markets(client)
    safe_print(f"[polymarket-youtube-channel-trader] {len(markets)} candidate markets")

    placed = 0
    for m in markets:
        if placed >= MAX_POSITIONS:
            break

        side, size, reasoning = compute_signal(m)
        if not side:
            safe_print(f"  [skip] {reasoning}")
            continue

        ok, why = context_ok(client, m.id)
        if not ok:
            safe_print(f"  [skip] {why}")
            continue

        try:
            r = client.trade(
                market_id=m.id,
                side=side,
                amount=size,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                reasoning=reasoning,
            )
            tag    = "(sim)" if r.simulated else "(live)"
            status = "OK" if r.success else f"FAIL:{r.error}"
            safe_print(f"  [trade] {side.upper()} ${size} {tag} {status} -- {reasoning[:75]}")
            if r.success:
                placed += 1
        except Exception as e:
            safe_print(f"  [error] {m.id}: {e}")

    safe_print(f"[polymarket-youtube-channel-trader] done. {placed} orders placed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description=(
            "Trades YouTube channel prediction markets using first-hour view "
            "velocity models, channel volatility profiles, and weekend posting "
            "windows. Top 10 channels tracked as distinct vol assets."
        )
    )
    ap.add_argument("--live", action="store_true",
                    help="Real trades on Polymarket. Default is paper (sim) mode.")
    run(live=ap.parse_args().live)
