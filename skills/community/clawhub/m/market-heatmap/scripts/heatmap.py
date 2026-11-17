#!/usr/bin/env python3
"""Render the US market heatmap as one self-contained interactive HTML file.

One API call. One file. No fonts, images, scripts or fetches are loaded from anywhere: the
agent fetches the board with its own key and the page carries the data inline, so it renders
with the network switched off, under every host permission mode, and it still renders next week.

    export SENTISENSE_API_KEY=...
    python3 heatmap.py --out market-heatmap.html --summary-json -

Standard library only. Python 3.8 or newer.

Exit codes, so a failure is legible rather than a stack trace:
    0  wrote the file
    2  usage: a bad flag, an unknown scope, a missing key, an unreadable fixture
    3  auth: the key was missing, rejected or not permitted
    4  not found: the board has not been built yet, or the scope has no snapshot
    5  rate limited
    6  network or upstream failure
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API_ORIGIN = "https://app.sentisense.ai"
SKILL = "market-heatmap"
VERSION = "1.1"
PATH = "/api/v1/trackers/market-heatmap"
SCOPES = ("sp500", "nasdaq100", "popular")

# The inline-widget ceiling every host that renders a page inline enforces. The script refuses
# to claim success on a file no such host can show.
INLINE_LIMIT = 262144

EXIT_USAGE = 2
EXIT_AUTH = 3
EXIT_NOT_FOUND = 4
EXIT_RATE_LIMIT = 5
EXIT_NETWORK = 6


# --------------------------------------------------------------------------------------
# palette
# --------------------------------------------------------------------------------------
# Ground and ink are the validated dark research surface. The bull/bear pair is checked for
# colourblind separation against this ground: the green is pushed toward teal on purpose,
# because the usual finance red/green is one of the worst possible pairs for deuteranopia.
BG = "#0d1117"
INK = "#e8edf4"
BULL = "#2e9d75"
BEAR = "#e05c4a"
# Attention metrics are not directional, so they never borrow the bull/bear pair. They use the
# data blue, which reads as "how much", not "up or down".
DATA = "#3182ce"
# A tile with no reading for the active metric. Never a zero, never a bull or bear tone.
NO_READING_FILL = "#171d26"
# A measured zero on a diverging scale. Neither bull nor bear, and visibly not the same tone as
# a tile with nothing to say.
FLAT_FILL = "#2a313c"


def hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def mix(base_hex, target_hex, t):
    """Blend target into base by t (0..1) and return a hex string."""
    a = hex_to_rgb(base_hex)
    b = hex_to_rgb(target_hex)
    out = tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))
    return "#%02x%02x%02x" % out


# --------------------------------------------------------------------------------------
# metrics
# --------------------------------------------------------------------------------------
# Every metric the board can colour by. `floor` is the smallest scale the colour ramp will
# ever use: without it a flat tape or a quiet week gets amplified into drama, because a scale
# fitted to a range of 0.2% would paint a nothing day in full colour.
METRICS = [
    {
        "key": "changePercent",
        "layer": "prices",
        "label": "Today's change",
        "short": "Change",
        "kind": "diverging",
        "unit": "percent",
        "floor": 1.0,
        "blurb": "Regular-session price change against the previous close. Delayed, not live.",
        "low": "down",
        "high": "up",
    },
    {
        "key": "sentiment7d",
        "layer": "sentiment",
        "label": "Sentiment, 7 day",
        "short": "Sentiment",
        "kind": "diverging",
        "unit": "tone",
        "floor": 0.15,
        "blurb": "Mean daily tone over seven days, on a scale from -1 to +1. A batch reading.",
        "low": "negative",
        "high": "positive",
    },
    {
        "key": "sentisenseScore",
        "layer": "sentiment",
        "label": "SentiSense Score",
        "short": "SentiSense Score",
        "kind": "diverging",
        "unit": "score",
        "floor": 5.0,
        "blurb": "How bullish or bearish today's news and social coverage reads, weighted by how much a name is discussed. Above zero leans bullish, below zero leans bearish. It reads what people write, not what the price did, so it can stay positive on a down day.",
        "low": "bearish",
        "high": "bullish",
    },
    {
        "key": "mentionsZ",
        "layer": "sentiment",
        "label": "Mentions vs baseline",
        "short": "Mentions",
        "kind": "sequential",
        "unit": "sd",
        "floor": 1.0,
        "blurb": "Today's mention volume in standard deviations of its own 30 day baseline.",
        "low": "quieter than usual",
        "high": "busier than usual",
    },
    {
        "key": "optionsInterestScore",
        "layer": "options",
        "label": "Options interest",
        "short": "Options",
        "kind": "sequential",
        "unit": "index",
        "floor": 20.0,
        "blurb": "Composite options interest from 0 to 100. Higher means more unusual activity.",
        "low": "quiet",
        "high": "unusual",
    },
]
METRIC_BY_KEY = dict((m["key"], m) for m in METRICS)
# Short names an agent or a user is likely to type on the command line. Every one of these is
# documented in the skill body's flag table, so the two never drift apart.
METRIC_ALIASES = {
    "change": "changePercent", "price": "changePercent", "move": "changePercent",
    "sentiment": "sentiment7d", "tone": "sentiment7d",
    "score": "sentisenseScore", "sentisense": "sentisenseScore",
    "mentions": "mentionsZ", "attention": "mentionsZ",
    "options": "optionsInterestScore",
}

# The bucket the endpoint uses for a name whose sector it could not resolve. It is a
# data-quality bucket, not a sector, so it never wins a "strongest" or "weakest" line.
UNCLASSIFIED = "Unclassified"

# The overlay layers, and the plain words for each. A non-PRO key receives the whole board with
# these layers removed, and the response says which in `meta.previewWithheld`.
LAYER_WORDS = {
    "sentiment": ["sentiment", "the SentiSense Score", "mentions"],
    "options": ["options interest"],
}

# The fields carried on every tile, in the order they are embedded. Absent means no reading.
TILE_FIELDS = [
    "ticker", "name", "industry", "marketCap", "price", "previousClose",
    "changePercent", "volume", "priceAsOf",
    "sentiment7d", "sentimentChange7d", "sentisenseScore", "mentionsZ", "optionsInterestScore",
]


class Loud(Exception):
    """A failure worth stopping for, carrying the exit code the caller should use."""

    def __init__(self, message, code, hint=None):
        super().__init__(message)
        self.code = code
        self.hint = hint


# --------------------------------------------------------------------------------------
# fetch
# --------------------------------------------------------------------------------------
def user_agent():
    agent = os.environ.get("SENTISENSE_AGENT_NAME", "").strip()
    suffix = "; agent/%s" % agent if agent else ""
    return "python-heatmap/%s (%s%s)" % (VERSION, SKILL, suffix)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def sentisense_api_url(path, params=None):
    """Return a validated API URL at the one origin allowed to receive the key."""
    url = urllib.parse.urljoin(API_ORIGIN + "/", path)
    parsed = urllib.parse.urlparse(url)
    if (parsed.scheme != "https" or parsed.hostname != "app.sentisense.ai"
            or parsed.netloc != "app.sentisense.ai"
            or parsed.username is not None or parsed.password is not None
            or parsed.port is not None):
        raise ValueError("API URL must use https://app.sentisense.ai with no credentials or port")
    if params:
        url += ("&" if parsed.query else "?") + urllib.parse.urlencode(params)
    return url


def fetch_board(scope, key, timeout=30):
    """The one and only network call this script makes."""
    url = sentisense_api_url(PATH, {"scope": scope})
    req = urllib.request.Request(url, headers={
        "X-SentiSense-API-Key": key,
        "User-Agent": user_agent(),
        "Accept": "application/json",
    })
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8")[:400]
        except Exception:
            pass
        detail = ""
        try:
            parsed = json.loads(body)
            detail = str(parsed.get("message") or parsed.get("error") or "")
        except Exception:
            detail = body
        if exc.code in (401, 403):
            raise Loud(
                "The API key was missing or rejected (HTTP %d). %s" % (exc.code, detail),
                EXIT_AUTH,
                "Set SENTISENSE_API_KEY. A free key: https://app.sentisense.ai/get-api-key")
        if exc.code == 404:
            raise Loud(
                "No board for scope '%s' yet (HTTP 404). %s" % (scope, detail),
                EXIT_NOT_FOUND,
                "The board is rebuilt every 15 minutes in regular trading hours. If this is "
                "the first request after a release, the board has not been built yet: retry "
                "in 15 minutes.")
        if exc.code == 400:
            raise Loud(
                "The scope was rejected (HTTP 400). %s" % detail,
                EXIT_USAGE,
                "Valid scopes: " + ", ".join(SCOPES))
        if exc.code == 429:
            raise Loud(
                "Rate limited (HTTP 429). %s" % detail,
                EXIT_RATE_LIMIT,
                "One render is one request. Wait a minute, or upgrade for a higher ceiling: "
                "https://app.sentisense.ai/pricing")
        raise Loud("The board request failed (HTTP %d). %s" % (exc.code, detail), EXIT_NETWORK)
    except urllib.error.URLError as exc:
        raise Loud("Could not reach the API: %s" % exc.reason, EXIT_NETWORK,
                   "Check network access to app.sentisense.ai.")
    except ValueError as exc:
        raise Loud("The API returned something that is not JSON: %s" % exc, EXIT_NETWORK)


def load_fixture(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except OSError as exc:
        raise Loud("Could not read the fixture %s: %s" % (path, exc), EXIT_USAGE)
    except ValueError as exc:
        raise Loud("The fixture %s is not valid JSON: %s" % (path, exc), EXIT_USAGE)


# --------------------------------------------------------------------------------------
# board model
# --------------------------------------------------------------------------------------
def number(value):
    """A float, or None. Never coerces an absent reading into a zero."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def metric_state(metric, layers, withheld):
    """One of `ok`, `pro` or `unavailable`, and the last two mean different things to a reader.

    `pro` is a layer this key did not receive; `unavailable` is a layer the board never carried,
    so no key has it today. Collapsing them would either sell a locked door with no room behind
    it, or hide a real gap behind an upsell. Neither state is ever coloured.
    """
    layer = metric.get("layer")
    if not layer or layer == "prices":
        return "ok"
    if layer in withheld:
        return "pro"
    if layer not in (layers or {}):
        return "unavailable"
    return "ok"


def build_board(envelope, scope_arg, is_fixture):
    """Turn the API envelope into the shape the page and the summary both read."""
    if not isinstance(envelope, dict):
        raise Loud("The board response was not an object.", EXIT_NETWORK)
    if "error" in envelope and "data" not in envelope:
        raise Loud("The API answered with an error: %s" % envelope.get("message", envelope["error"]),
                   EXIT_NOT_FOUND)
    data = envelope.get("data")
    if not isinstance(data, dict):
        raise Loud("The board response carried no data object.", EXIT_NETWORK)
    rows = data.get("rows") or []
    if not rows:
        raise Loud("The board came back with no rows, so there is nothing honest to draw.",
                   EXIT_NOT_FOUND,
                   "Retry in 15 minutes; the board is rebuilt on that cadence.")

    meta = data.get("meta") or {}
    layers = meta.get("layers") or {}
    is_preview = bool(envelope.get("isPreview"))
    total_count = envelope.get("totalCount")
    if not isinstance(total_count, int):
        total_count = len(rows)
    # The layers this key did not receive. Reading an absent field is not enough to tell the two
    # cases apart: absent means "no reading for this ticker" on PRO and "not on your tier" on a
    # Free key, and only this list separates them. Absent from a PRO response entirely.
    raw_withheld = meta.get("previewWithheld")
    withheld = [name for name in LAYER_WORDS if isinstance(raw_withheld, list)
                and name in raw_withheld]

    tiles = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        ticker = row.get("ticker") or row.get("rowId")
        if not ticker:
            continue
        tile = {
            "ticker": str(ticker),
            "name": row.get("name") or str(ticker),
            "sector": row.get("sector") or row.get("category") or UNCLASSIFIED,
            "industry": row.get("industry"),
            "marketCap": number(row.get("marketCap")),
            "price": number(row.get("price")),
            "previousClose": number(row.get("previousClose")),
            "changePercent": number(row.get("changePercent")),
            "volume": number(row.get("volume")),
            "priceAsOf": row.get("priceAsOf"),
            "sentiment7d": number(row.get("sentiment7d")),
            "sentimentChange7d": number(row.get("sentimentChange7d")),
            "sentisenseScore": number(row.get("sentisenseScore")),
            "mentionsZ": number(row.get("mentionsZ")),
            "optionsInterestScore": number(row.get("optionsInterestScore")),
        }
        tiles.append(tile)
    if not tiles:
        raise Loud("Every row in the board was unreadable.", EXIT_NETWORK)

    # A tile with no market cap on file still gets drawn: an invisible tile and a missing tile
    # look identical to a reader. It is drawn at the smallest area on the board and the page
    # says so, rather than being sized by a number nobody has.
    caps = sorted(t["marketCap"] for t in tiles if t["marketCap"] and t["marketCap"] > 0)
    floor_cap = caps[0] if caps else 1.0
    cap_missing = 0
    for tile in tiles:
        if not tile["marketCap"] or tile["marketCap"] <= 0:
            tile["area"] = floor_cap
            tile["capMissing"] = True
            cap_missing += 1
        else:
            tile["area"] = tile["marketCap"]
            tile["capMissing"] = False

    mood_by_sector = {}
    for entry in (meta.get("sectors") or []):
        if isinstance(entry, dict) and entry.get("sector"):
            mood_by_sector[entry["sector"]] = entry

    sectors = []
    by_sector = {}
    for tile in tiles:
        by_sector.setdefault(tile["sector"], []).append(tile)
    for name in sorted(by_sector, key=lambda s: -sum(t["area"] for t in by_sector[s])):
        members = by_sector[name]
        roll = mood_by_sector.get(name, {})
        up = sum(1 for t in members if (t["changePercent"] or 0) > 0)
        down = sum(1 for t in members if (t["changePercent"] or 0) < 0)
        cap = sum(t["area"] for t in members)
        weighted = None
        priced = [t for t in members if t["changePercent"] is not None and t["marketCap"]]
        if priced:
            denom = sum(t["marketCap"] for t in priced)
            if denom > 0:
                weighted = sum(t["marketCap"] * t["changePercent"] for t in priced) / denom
        sectors.append({
            "name": name,
            "tiles": members,
            "area": cap,
            "drawnCount": len(members),
            "boardCount": roll.get("count"),
            "moodScore": number(roll.get("marketMoodScore")),
            "moodPhase": roll.get("marketMoodPhase"),
            "moodWeekly": number(roll.get("marketMoodWeeklyChange")),
            "capWeighted": number(roll.get("capWeightedChangePct")),
            "drawnCapWeighted": weighted,
            "up": up,
            "down": down,
        })

    return {
        "scope": meta.get("scope") or data.get("scope") or scope_arg,
        "scopeName": meta.get("scopeName") or (data.get("scope") or scope_arg),
        "asOf": data.get("asOf"),
        "generatedAt": data.get("generatedAt"),
        "isPreview": is_preview,
        "previewReason": envelope.get("previewReason"),
        "totalCount": total_count,
        "withheld": withheld,
        "metricStates": dict((m["key"], metric_state(m, layers, withheld)) for m in METRICS),
        "tiles": tiles,
        "sectors": sectors,
        "capMissing": cap_missing,
        "layers": layers,
        "moodScore": number(meta.get("marketMoodScore")),
        "moodPhase": meta.get("marketMoodPhase"),
        "breadthUp": meta.get("breadthUp"),
        "breadthDown": meta.get("breadthDown"),
        "capWeighted": number(meta.get("capWeightedChangePct")),
        "equalWeighted": number(meta.get("equalWeightedChangePct")),
        "missingPrice": meta.get("missingPrice") or [],
        "isSample": is_fixture,
    }


# --------------------------------------------------------------------------------------
# squarified treemap
# --------------------------------------------------------------------------------------
def _row_rects(sizes, x, y, dx, dy):
    """Lay one run of sizes down the left edge (dx >= dy) or along the top (dx < dy)."""
    covered = sum(sizes)
    rects = []
    if dx >= dy:
        width = covered / dy if dy > 0 else 0.0
        cy = y
        for size in sizes:
            h = size / width if width > 0 else 0.0
            rects.append([x, cy, width, h])
            cy += h
    else:
        height = covered / dx if dx > 0 else 0.0
        cx = x
        for size in sizes:
            w = size / height if height > 0 else 0.0
            rects.append([cx, y, w, height])
            cx += w
    return rects


def _worst_ratio(sizes, x, y, dx, dy):
    worst = 0.0
    for _, _, w, h in _row_rects(sizes, x, y, dx, dy):
        if w <= 0 or h <= 0:
            return float("inf")
        worst = max(worst, max(w / h, h / w))
    return worst


def _leftover(sizes, x, y, dx, dy):
    covered = sum(sizes)
    if dx >= dy:
        width = covered / dy if dy > 0 else 0.0
        return x + width, y, dx - width, dy
    height = covered / dx if dx > 0 else 0.0
    return x, y + height, dx, dy - height


def squarify(values, x, y, dx, dy):
    """Squarified treemap rectangles, one per input value, in input order.

    Deterministic: the same values in the same order always produce the same rectangles, which
    is what lets the layout be precomputed here and merely positioned by the page.
    """
    if not values:
        return []
    order = sorted(range(len(values)), key=lambda i: (-values[i], i))
    total = sum(values[i] for i in order)
    if total <= 0 or dx <= 0 or dy <= 0:
        return [[x, y, 0.0, 0.0] for _ in values]
    scale = (dx * dy) / total
    sizes = [values[i] * scale for i in order]

    placed = []
    # Iterative rather than recursive: 500 tiles would otherwise reach the interpreter's
    # recursion ceiling on a bad split.
    while sizes:
        cur_x, cur_y, cur_dx, cur_dy = x, y, dx, dy
        i = 1
        while i < len(sizes) and _worst_ratio(sizes[:i], cur_x, cur_y, cur_dx, cur_dy) >= \
                _worst_ratio(sizes[:i + 1], cur_x, cur_y, cur_dx, cur_dy):
            i += 1
        run = sizes[:i]
        placed.extend(_row_rects(run, cur_x, cur_y, cur_dx, cur_dy))
        x, y, dx, dy = _leftover(run, cur_x, cur_y, cur_dx, cur_dy)
        sizes = sizes[i:]
        if dx <= 1e-12 or dy <= 1e-12:
            for size in sizes:
                placed.append([x, y, 0.0, 0.0])
            sizes = []

    out = [None] * len(values)
    for slot, idx in enumerate(order):
        out[idx] = placed[slot]
    return out


def pct(rect, box_w, box_h, places=3):
    x, y, w, h = rect
    return [round(x / box_w * 100.0, places), round(y / box_h * 100.0, places),
            round(w / box_w * 100.0, places), round(h / box_h * 100.0, places)]


# Reference boxes. The page positions everything in percentages, so these only set the aspect
# ratio the layout is optimised for, never a fixed canvas.
OVERVIEW_W, OVERVIEW_H = 160.0, 100.0
BAND_W, BAND_H = 160.0, 56.0


def build_layout(board):
    """Sector rectangles for the overview, tile rectangles inside each sector, and the
    per-sector band layout the narrow render and the zoom view both reuse."""
    sectors = board["sectors"]
    sector_rects = squarify([s["area"] for s in sectors], 0.0, 0.0, OVERVIEW_W, OVERVIEW_H)

    index_of = {}
    for i, tile in enumerate(board["tiles"]):
        index_of[id(tile)] = i

    overview = [None] * len(board["tiles"])
    bands = []
    for sector, rect in zip(sectors, sector_rects):
        values = [t["area"] for t in sector["tiles"]]
        inner = squarify(values, 0.0, 0.0, max(rect[2], 1e-6), max(rect[3], 1e-6))
        for tile, r in zip(sector["tiles"], inner):
            overview[index_of[id(tile)]] = pct(r, max(rect[2], 1e-6), max(rect[3], 1e-6))
        band = squarify(values, 0.0, 0.0, BAND_W, BAND_H)
        bands.append([pct(r, BAND_W, BAND_H) for r in band])
    return {
        "sectorRects": [pct(r, OVERVIEW_W, OVERVIEW_H) for r in sector_rects],
        "overview": overview,
        "bands": bands,
        "members": [[index_of[id(t)] for t in s["tiles"]] for s in sectors],
    }


# --------------------------------------------------------------------------------------
# colour scales
# --------------------------------------------------------------------------------------
def quantile(sorted_values, q):
    if not sorted_values:
        return None
    if len(sorted_values) == 1:
        return sorted_values[0]
    pos = q * (len(sorted_values) - 1)
    lo = int(math.floor(pos))
    hi = min(lo + 1, len(sorted_values) - 1)
    frac = pos - lo
    return sorted_values[lo] + (sorted_values[hi] - sorted_values[lo]) * frac


def nice_step(value):
    """Round a scale edge up to something a reader can say out loud."""
    if value <= 0:
        return 1.0
    exp = math.floor(math.log10(value))
    base = value / (10 ** exp)
    for candidate in (1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.5, 10.0):
        if base <= candidate + 1e-9:
            return candidate * (10 ** exp)
    return 10.0 ** (exp + 1)


BANDS_PER_SIDE = 4


def build_scales(board):
    """One colour scale per metric, fitted to the board in front of you.

    Fitted rather than fixed because these five metrics live on five unrelated scales and a
    hardcoded range would paint most days grey. The legend prints the real edges, and the
    footer says the scale is fitted, so nothing here is a hidden judgement.
    """
    scales = []
    for metric in METRICS:
        key = metric["key"]
        values = [t[key] for t in board["tiles"] if t[key] is not None]
        missing = len(board["tiles"]) - len(values)
        if metric["kind"] == "diverging":
            magnitudes = sorted(abs(v) for v in values)
            cap = quantile(magnitudes, 0.92) or 0.0
            cap = max(nice_step(cap) if cap > 0 else 0.0, metric["floor"])
            edges = [cap * (i + 1) / float(BANDS_PER_SIDE) for i in range(BANDS_PER_SIDE)]
            fills = []
            for i in range(BANDS_PER_SIDE):
                t = 0.16 + 0.58 * (i + 1) / float(BANDS_PER_SIDE)
                fills.append([mix(BG, BEAR, t), mix(BG, BULL, t)])
            # Index order: most negative band first, then up to the most positive band.
            palette = [fills[BANDS_PER_SIDE - 1 - i][0] for i in range(BANDS_PER_SIDE)]
            palette += [fills[i][1] for i in range(BANDS_PER_SIDE)]
            scales.append({
                "key": key, "kind": "diverging", "cap": cap, "edges": edges,
                "palette": palette, "missing": missing, "count": len(values),
            })
        else:
            ordered = sorted(values)
            lo = quantile(ordered, 0.05)
            hi = quantile(ordered, 0.95)
            if lo is None or hi is None:
                lo, hi = 0.0, metric["floor"]
            if hi - lo < metric["floor"]:
                mid = (hi + lo) / 2.0
                lo, hi = mid - metric["floor"] / 2.0, mid + metric["floor"] / 2.0
            steps = BANDS_PER_SIDE * 2
            edges = [lo + (hi - lo) * (i + 1) / float(steps) for i in range(steps - 1)]
            palette = [mix(BG, DATA, 0.14 + 0.62 * i / float(steps - 1)) for i in range(steps)]
            scales.append({
                "key": key, "kind": "sequential", "lo": lo, "hi": hi, "edges": edges,
                "palette": palette, "missing": missing, "count": len(values),
            })
    return scales


def band_index(scale, value):
    """Which palette slot a reading falls in, or -1 when there is no reading."""
    if value is None:
        return -1
    edges = scale["edges"]
    if scale["kind"] == "diverging":
        if value == 0:
            return -2
        cap = scale["cap"]
        magnitude = min(abs(value), cap)
        slot = 0
        for i, edge in enumerate(edges):
            if magnitude <= edge + 1e-12:
                slot = i
                break
            slot = len(edges) - 1
        if value < 0:
            return BANDS_PER_SIDE - 1 - slot
        return BANDS_PER_SIDE + slot
    slot = len(edges)
    for i, edge in enumerate(edges):
        if value <= edge + 1e-12:
            slot = i
            break
    return slot


# --------------------------------------------------------------------------------------
# display strings
# --------------------------------------------------------------------------------------
NA = "no reading"


def fmt_signed(value, places=1, suffix=""):
    if value is None:
        return NA
    # Compare the value as printed, not the raw float: -0.047 at one decimal would otherwise
    # print "-0.0%", a sign on a number that reads as zero.
    if round(value, places) == 0:
        return "%.*f%s" % (places, 0.0, suffix)
    return "%+.*f%s" % (places, value, suffix)


def fmt_plain(value, places=1, suffix=""):
    if value is None:
        return NA
    return "%.*f%s" % (places, value, suffix)


def fmt_whole(value):
    if value is None:
        return NA
    return "%d" % int(round(value))


def fmt_usd(value):
    if value is None:
        return NA
    if value >= 1e12:
        return "$%.2fT" % (value / 1e12)
    if value >= 1e9:
        return "$%.1fB" % (value / 1e9)
    if value >= 1e6:
        return "$%.0fM" % (value / 1e6)
    return "$%.0f" % value


def fmt_price(value):
    if value is None:
        return NA
    return "$%.2f" % value


def fmt_count(value):
    if value is None:
        return NA
    return "{:,}".format(int(round(value)))


def fmt_metric(key, value):
    """One display string per metric reading, and the same rule the page prints."""
    if value is None:
        return NA
    if key == "changePercent":
        return fmt_signed(value, 1, "%")
    if key == "sentiment7d":
        return fmt_signed(value, 2)
    if key == "sentimentChange7d":
        return fmt_signed(value, 2)
    if key == "sentisenseScore":
        return fmt_signed(value, 1)
    if key == "mentionsZ":
        return fmt_signed(value, 1) + " sd"
    if key == "optionsInterestScore":
        return fmt_whole(value)
    return fmt_plain(value)


def fmt_stamp(value):
    """An ISO instant or date, said plainly and in UTC."""
    if not value:
        return NA
    text = str(value)
    if len(text) == 10:
        try:
            return datetime.strptime(text, "%Y-%m-%d").strftime("%d %b %Y")
        except ValueError:
            pass
    try:
        cleaned = text.replace("Z", "+00:00")
        moment = datetime.fromisoformat(cleaned)
        if moment.tzinfo is None:
            moment = moment.replace(tzinfo=timezone.utc)
        return moment.astimezone(timezone.utc).strftime("%d %b %Y %H:%M UTC")
    except ValueError:
        pass
    try:
        return datetime.strptime(text[:10], "%Y-%m-%d").strftime("%d %b %Y")
    except ValueError:
        return text


SECTOR_SHORT = {
    "Information Technology": "Info Tech",
    "Communication Services": "Comm Services",
    "Consumer Discretionary": "Cons Discretionary",
    "Consumer Staples": "Cons Staples",
}


LAYER_LABEL = {
    "prices": "Prices",
    "marketMood": "Market Mood",
    "sentiment": "Sentiment and Score",
    "options": "Options interest",
}


def layer_lines(board):
    lines = []
    for key in ("prices", "marketMood", "sentiment", "options"):
        layer = board["layers"].get(key)
        if not isinstance(layer, dict):
            continue
        label = LAYER_LABEL.get(key, key)
        # computedAt, where served, is the time of the read. asOf on that layer is only a date, and
        # the numbers behind it are rewritten several times a day.
        raw = layer.get("computedAt") or layer.get("asOf")
        delay = layer.get("delayMinutes")
        if raw:
            line = "%s %s" % (label, fmt_stamp(raw))
            if delay:
                line += ", delayed %d minutes" % int(delay)
        elif delay:
            line = ("%s delayed %d minutes, and this board carries no session stamp for them"
                    % (label, int(delay)))
        else:
            line = "%s, no as-of stamp on this board" % label
        lines.append(line)
    return lines


def as_of_line(board):
    """The masthead's freshness clause. A board with no price stamp says the delay instead of
    printing a hole where a time should be."""
    if board["asOf"]:
        return "prices as of " + fmt_stamp(board["asOf"])
    delay = (board["layers"].get("prices") or {}).get("delayMinutes")
    if delay:
        return "prices delayed %d minutes, no session stamp on this board" % int(delay)
    return "no price stamp on this board"


def is_partial_board(board):
    """True only when this response carried fewer rows than the board has. Every tier now
    receives every tile, so this is the legacy shape, kept because a client can meet an older
    deployment and the footer still has to be true."""
    total = board["totalCount"]
    return isinstance(total, int) and total > len(board["tiles"])


def breadth_coverage(board):
    """Whose breadth this is. The counts are computed over the whole board, which is also what
    the tiles are, unless a legacy response handed us fewer rows than the board holds."""
    if is_partial_board(board):
        return "across all %s names in this index" % fmt_count(board["totalCount"])
    return "across the %s tiles drawn" % fmt_count(len(board["tiles"]))


def withheld_words(board):
    """The readings this key did not receive, in plain words."""
    words = []
    for name in board["withheld"]:
        words.extend(LAYER_WORDS[name])
    return words


def unavailable_layers(board):
    """Overlay layers the board itself never carried, which no tier has today."""
    return [name for name in LAYER_WORDS
            if name not in board["withheld"] and name not in board["layers"]]


def join_words(items):
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def toggle_note(board):
    """The line under the metric toggles explaining why some of them cannot be pressed."""
    pro = [m["short"] for m in METRICS if board["metricStates"].get(m["key"]) == "pro"]
    gone = [m["short"] for m in METRICS if board["metricStates"].get(m["key"]) == "unavailable"]
    lines = []
    if pro:
        clause = ("%s is a PRO overlay and is not on this key." % pro[0] if len(pro) == 1
                  else "%s are PRO overlays and are not on this key." % join_words(pro))
        lines.append(clause + " The board, the sectors and the day's move are open to everyone.")
    if gone:
        lines.append("%s did not run for this board today, so no key carries %s."
                     % (join_words(gone), "it" if len(gone) == 1 else "them"))
    return " ".join(lines)


def preview_note(board):
    """What this board is, and what it is not. Every tier draws every tile; the overlays are the
    part a Free key does not get, and nothing is estimated in their place."""
    if is_partial_board(board):
        head = ("This response carried the %s largest names of %s in this index."
                % (fmt_count(len(board["tiles"])), fmt_count(board["totalCount"])))
    else:
        head = "Whole board: all %s tiles in this index." % fmt_count(len(board["tiles"]))
    withheld = withheld_words(board)
    if withheld:
        return ("%s The %s overlays are part of PRO and are not in this response, and nothing is "
                "estimated in their place." % (head, join_words(withheld)))
    return head


# --------------------------------------------------------------------------------------
# page
# --------------------------------------------------------------------------------------
def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def safe(text):
    """Strings the page writes into innerHTML. Angle brackets never appear in a company name
    or a sector label, so removing them costs nothing and closes the only hole."""
    if text is None:
        return ""
    return str(text).replace("<", "(").replace(">", ")")


DISCLAIMER = ("Not investment advice. Generated from public and licensed market data for "
              "research and educational purposes only. Not a recommendation to buy or sell "
              "any security.")

CSS = """
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:#0d1117;color:#e8edf4;
 font:14px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
 font-variant-numeric:tabular-nums;-webkit-font-smoothing:antialiased}
.wrap{max-width:1900px;margin:0 auto;padding:20px 20px 28px}
a{color:#9daaba}
h1{font:400 27px/1.2 Georgia,"Times New Roman",serif;margin:0;letter-spacing:.2px}
.sub{color:#66738a;font-size:12px;margin-top:5px}
.mast{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:14px}
.rule{height:1px;background:#D4A843;opacity:.55;margin:14px 0 0}
.stats{display:flex;flex-wrap:wrap;gap:26px;margin:16px 0 4px}
.stat .k{color:#66738a;font-size:11px;text-transform:uppercase;letter-spacing:.09em}
.stat .v{font-size:19px;margin-top:3px}
.stat .n{color:#9daaba;font-size:12px;margin-top:2px}
.up{color:#2e9d75}.dn{color:#e05c4a}.flat{color:#9daaba}
.bar{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:18px 0 10px}
.seg{display:flex;flex-wrap:wrap;gap:1px;background:rgba(255,255,255,.07);padding:1px;border-radius:3px}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}
.seg button{padding:6px 11px;font-size:12px;color:#9daaba;border-radius:2px}
.seg button[aria-pressed=true]{background:#1b2330;color:#e8edf4}
.seg button[disabled]{color:#4d5769;cursor:not-allowed}
.seg button[disabled][aria-pressed=true]{background:none}
.note.tier{color:#9daaba}
.seg button:focus-visible,.t:focus-visible,.sh:focus-visible,#back:focus-visible{
 outline:2px solid #D4A843;outline-offset:1px}
#q{background:#161d28;border:1px solid rgba(255,255,255,.13);color:#e8edf4;
 padding:6px 10px;border-radius:3px;font-size:12px;min-width:170px}
#q::placeholder{color:#66738a}
#back{font-size:12px;color:#9daaba;border:1px solid rgba(255,255,255,.13);
 padding:6px 11px;border-radius:3px}
.note{color:#66738a;font-size:12px;margin:0 0 12px}
.legend{display:flex;flex-wrap:wrap;align-items:center;gap:14px;margin:0 0 14px;font-size:11px;
 color:#9daaba}
.scale{display:flex;align-items:center;gap:0}
.scale i{width:26px;height:10px;display:block}
.scale .cap{color:#66738a;margin:0 7px}
.miss{display:flex;align-items:center;gap:6px;color:#66738a}
.miss i{width:14px;height:10px;display:block;background:#171d26;
 border:1px solid rgba(255,255,255,.13)}
#board{position:relative;width:100%;aspect-ratio:16/9;min-height:400px;max-height:76vh}
#board.narrow{position:static;aspect-ratio:auto;min-height:0;max-height:none}
.sector{position:absolute;display:flex;flex-direction:column;overflow:hidden;
 padding:0 4px 4px 0}
#board.narrow .sector{position:static;margin:0 0 12px;aspect-ratio:16/7;padding:0}
#board.zoom .sector{display:none}
#board.zoom .sector.on{display:flex;padding:0}
.sh{display:flex;align-items:baseline;gap:8px;padding:0 4px 3px;text-align:left;
 white-space:nowrap;overflow:hidden;flex:0 0 auto}
.sh .nm{font-size:11.5px;color:#e8edf4;letter-spacing:.02em}
.sh .md{font-size:10.5px;color:#66738a}
.sh:hover .nm{color:#D4A843}
.body{position:relative;flex:1 1 auto;min-height:0}
.sector.tiny .sh{display:none}
.sh.nomood .md{display:none}
.t{position:absolute;overflow:hidden;padding:0;border:1px solid rgba(13,17,23,.85);
 border-radius:1px;display:block;text-align:left;line-height:1.05}
.t .tk{display:block;font-size:10px;letter-spacing:.02em;padding:3px 0 0 3px;color:#e8edf4}
.t .vl{display:block;font-size:9.5px;padding:1px 0 0 3px;color:#9daaba}
.t.sm .tk,.t.sm .vl{display:none}
.t.md .vl{display:none}
.t.lg .tk{font-size:12px}
.t.hit{outline:2px solid #D4A843;outline-offset:-2px;z-index:3}
#board.searching .t{opacity:.24}
#board.searching .t.hit{opacity:1}
#card{position:fixed;z-index:20;width:280px;background:#111823;
 border:1px solid rgba(255,255,255,.16);border-radius:4px;padding:12px 13px;
 box-shadow:0 6px 22px rgba(0,0,0,.45);display:none;font-size:12px}
#card.on{display:block}
#card h2{font:400 16px/1.2 Georgia,"Times New Roman",serif;margin:0}
#card .cs{color:#66738a;font-size:11px;margin:2px 0 9px}
#card dl{display:grid;grid-template-columns:auto 1fr;gap:3px 12px;margin:0}
#card dt{color:#66738a}
#card dd{margin:0;text-align:right}
#card .cf{color:#66738a;font-size:10.5px;margin-top:9px;border-top:1px solid rgba(255,255,255,.09);
 padding-top:7px}
footer{margin-top:22px;border-top:1px solid rgba(255,255,255,.09);padding-top:12px;
 color:#66738a;font-size:11.5px}
footer p{margin:0 0 5px}
footer .dis{color:#9daaba}
.sample{background:#2a2015;border:1px solid #D4A843;color:#e8edf4;padding:8px 11px;
 border-radius:3px;font-size:12px;margin:0 0 14px}
@media (max-width:820px){
 .wrap{padding:14px 12px 22px}
 h1{font-size:22px}
 .stats{gap:18px}
 .stat .v{font-size:17px}
 #q{min-width:120px;flex:1 1 120px}
}
@media (prefers-reduced-motion:no-preference){.t{transition:opacity .12s linear}}
"""

JS = r"""
(function(){
var B=window.__BOARD__,L=B.layout,S=B.scales,M=B.metrics;
var board=document.getElementById('board'),card=document.getElementById('card');
var legend=document.getElementById('legend'),q=document.getElementById('q');
var back=document.getElementById('back'),metricNote=document.getElementById('mnote');
var tinyNote=document.getElementById('tinynote');
var metric=B.initialMetric,zoom=-1,pinned=null,tiles=[],sectorEls=[];

function fill(mi,ti){
  var b=B.bands[ti][mi];
  if(b===-1){return B.noReading;}
  if(b===-2){return B.flat;}
  return S[mi].palette[b];
}

function build(){
  var html='';
  for(var s=0;s<B.sectors.length;s++){
    var sec=B.sectors[s];
    html+='<div class="sector" data-s="'+s+'">';
    html+='<button class="sh" data-s="'+s+'"><span class="nm">'+sec.name+'</span><span class="md">'+sec.head+'</span></button>';
    html+='<div class="body">';
    var mem=L.members[s];
    for(var i=0;i<mem.length;i++){
      var ti=mem[i];
      html+='<button class="t" data-t="'+ti+'"><span class="tk">'+B.tiles[ti][0]+'</span><span class="vl"></span></button>';
    }
    html+='</div></div>';
  }
  board.innerHTML=html;
  sectorEls=board.querySelectorAll('.sector');
  tiles=board.querySelectorAll('.t');
}

function place(){
  var stacked=board.classList.contains('narrow');
  var narrow=stacked||zoom>=0;
  for(var s=0;s<B.sectors.length;s++){
    var box=sectorEls[s].style,sr=L.sectorRects[s];
    if(zoom>=0){box.left='0';box.top='0';box.width='100%';box.height='100%';}
    else if(stacked){box.left='';box.top='';box.width='';box.height='';}
    else{box.left=sr[0]+'%';box.top=sr[1]+'%';box.width=sr[2]+'%';box.height=sr[3]+'%';}
    var mem=L.members[s],rects=narrow?L.bands[s]:null;
    var kids=sectorEls[s].querySelectorAll('.t');
    for(var i=0;i<mem.length;i++){
      var r=rects?rects[i]:L.overview[mem[i]];
      var st=kids[i].style;
      st.left=r[0]+'%';st.top=r[1]+'%';st.width=r[2]+'%';st.height=r[3]+'%';
    }
  }
  markTiny();
  sizeLabels();
}

// A sector too small to carry its own name gives the room back to its tiles rather than
// spending the whole rectangle on a clipped label. The footer then says which ones lost it,
// because an unnamed block is a hole the reader cannot check.
function markTiny(){
  var lost=[];
  for(var s=0;s<sectorEls.length;s++){
    var el=sectorEls[s],r=el.getBoundingClientRect();
    var tiny=(r.height>0||r.width>0)&&(r.height<34||r.width<74);
    el.classList.toggle('tiny',tiny);
    if(!tiny){fitHead(el,B.sectors[s]);}
    if(tiny&&(zoom<0||zoom===s)){lost.push(B.sectors[s].name);}
  }
  tinyNote.textContent=lost.length
    ? 'Too small to label at this size, named in the hover card instead: '+lost.join(', ')+'.'
    : '';
}

function sizeLabels(){
  var narrow=board.classList.contains('narrow')||zoom>=0;
  for(var s=0;s<B.sectors.length;s++){
    var el=sectorEls[s];
    if(zoom>=0&&zoom!==s){continue;}
    var bodyEl=el.querySelector('.body');
    var bw=bodyEl.clientWidth,bh=bodyEl.clientHeight;
    var mem=L.members[s],rects=narrow?L.bands[s]:null;
    var kids=el.querySelectorAll('.t');
    for(var i=0;i<mem.length;i++){
      var r=rects?rects[i]:L.overview[mem[i]];
      var w=r[2]/100*bw,h=r[3]/100*bh;
      var c=kids[i].classList;
      c.remove('sm');c.remove('md');c.remove('lg');
      if(w<26||h<15){c.add('sm');}
      else if(w<52||h<30){c.add('md');}
      else if(w>86&&h>44){c.add('lg');}
    }
  }
}

// Step the header down in fixed steps rather than clipping a word: drop the mood suffix, then
// use this sector's one written short form, then give up and let the tiles have the room.
function fitHead(el,sec){
  var sh=el.querySelector('.sh'),nm=sh.querySelector('.nm');
  sh.classList.remove('nomood');nm.textContent=sec.name;
  if(sh.scrollWidth<=sh.clientWidth){return;}
  sh.classList.add('nomood');
  if(sh.scrollWidth<=sh.clientWidth){return;}
  nm.textContent=sec.short;
  if(sh.scrollWidth<=sh.clientWidth){return;}
  el.classList.add('tiny');
}

function paint(){
  var mi=metricIndex();
  for(var s=0;s<B.sectors.length;s++){
    var mem=L.members[s],kids=sectorEls[s].querySelectorAll('.t');
    for(var i=0;i<mem.length;i++){
      var ti=mem[i];
      kids[i].style.background=fill(mi,ti);
      var v=kids[i].querySelector('.vl');
      v.textContent=B.display[mi][ti];
      kids[i].setAttribute('aria-label',B.tiles[ti][0]+', '+M[mi].label+' '+B.display[mi][ti]);
    }
  }
  drawLegend(mi);
  metricNote.textContent=M[mi].blurb+' '+S[mi].scaleNote;
}

function metricIndex(){for(var i=0;i<M.length;i++){if(M[i].key===metric){return i;}}return 0;}

function drawLegend(mi){
  var sc=S[mi],html='<span class="scale">';
  html+='<span class="cap">'+sc.lowLabel+'</span>';
  for(var i=0;i<sc.palette.length;i++){html+='<i style="background:'+sc.palette[i]+'"></i>';}
  html+='<span class="cap">'+sc.highLabel+'</span></span>';
  if(sc.kind==='diverging'){
    html+='<span class="miss"><i style="background:'+B.flat+'"></i>flat</span>';
  }
  html+='<span class="miss"><i></i>no reading'+(sc.missing?' ('+sc.missing+' of '+B.tiles.length+' tiles)':'')+'</span>';
  html+='<span class="miss">Tile area: market cap</span>';
  legend.innerHTML=html;
}

function cardHtml(ti){
  var t=B.tiles[ti],f=B.fields,rows='';
  for(var i=3;i<f.length;i++){
    rows+='<dt>'+f[i].label+'</dt><dd>'+B.cardValues[ti][i-3]+'</dd>';
  }
  return '<h2>'+t[0]+'</h2><div class="cs">'+t[1]+'</div>'+
    '<div class="cs">'+B.sectors[B.sectorOf[ti]].name+(t[2]?' &middot; '+t[2]:'')+'</div>'+
    '<dl>'+rows+'</dl><div class="cf">'+B.cardFoot[ti]+'</div>';
}

function showCard(ti,x,y){
  card.innerHTML=cardHtml(ti);
  card.classList.add('on');
  var w=card.offsetWidth,h=card.offsetHeight;
  var left=Math.min(Math.max(8,x+14),window.innerWidth-w-8);
  var top=Math.min(Math.max(8,y+14),window.innerHeight-h-8);
  card.style.left=left+'px';card.style.top=top+'px';
}
function hideCard(){if(pinned===null){card.classList.remove('on');}}

// Zooming HIDES the other sectors (display:none), it does not remove them, so a script reading
// this page sees every tile in the DOM at all times. Filter on '.sector.on .t' when zoomed.
function setZoom(s){
  zoom=s;
  for(var i=0;i<sectorEls.length;i++){sectorEls[i].classList.toggle('on',i===s);}
  board.classList.toggle('zoom',s>=0);
  back.hidden=s<0;
  responsive();
}

function responsive(){
  board.classList.toggle('narrow',window.innerWidth<820&&zoom<0);
  place();
}

function search(){
  var v=q.value.trim().toUpperCase();
  board.classList.toggle('searching',!!v);
  var first=null;
  for(var i=0;i<tiles.length;i++){
    var ti=+tiles[i].getAttribute('data-t');
    var hit=!!v&&(B.tiles[ti][0].indexOf(v)===0||B.tiles[ti][1].toUpperCase().indexOf(v)>=0);
    tiles[i].classList.toggle('hit',hit);
    if(hit&&first===null){first=tiles[i];}
  }
  return first;
}

build();
paint();
responsive();

board.addEventListener('mouseover',function(e){
  var t=e.target.closest('.t');if(!t||pinned!==null){return;}
  showCard(+t.getAttribute('data-t'),e.clientX,e.clientY);
});
board.addEventListener('mousemove',function(e){
  var t=e.target.closest('.t');if(!t||pinned!==null){return;}
  showCard(+t.getAttribute('data-t'),e.clientX,e.clientY);
});
board.addEventListener('mouseout',function(e){
  if(!e.relatedTarget||!e.relatedTarget.closest('.t')){hideCard();}
});
board.addEventListener('focusin',function(e){
  var t=e.target.closest('.t');if(!t){return;}
  var r=t.getBoundingClientRect();
  pinned=null;showCard(+t.getAttribute('data-t'),r.left,r.bottom-14);
});
board.addEventListener('click',function(e){
  var h=e.target.closest('.sh');
  if(h){setZoom(zoom===+h.getAttribute('data-s')?-1:+h.getAttribute('data-s'));return;}
  var t=e.target.closest('.t');
  if(t){var ti=+t.getAttribute('data-t');pinned=pinned===ti?null:ti;
    var r=t.getBoundingClientRect();showCard(ti,r.left,r.bottom-14);}
});
document.addEventListener('keydown',function(e){
  if(e.key==='Escape'){pinned=null;hideCard();if(zoom>=0){setZoom(-1);}}
});
document.addEventListener('click',function(e){
  if(pinned===null){return;}
  if(e.target.closest('#board')||e.target.closest('#card')){return;}
  pinned=null;hideCard();
},true);
back.addEventListener('click',function(){setZoom(-1);});
q.addEventListener('input',function(){search();});
q.addEventListener('keydown',function(e){
  if(e.key!=='Enter'){return;}
  var first=search();
  if(first){first.focus();first.scrollIntoView({block:'center'});}
});
document.querySelectorAll('.seg button[data-m]').forEach(function(b){
  b.addEventListener('click',function(){
    if(b.disabled){return;}
    metric=b.getAttribute('data-m');
    document.querySelectorAll('.seg button[data-m]').forEach(function(o){
      o.setAttribute('aria-pressed',o===b?'true':'false');});
    paint();
  });
});
window.addEventListener('resize',function(){
  clearTimeout(window.__rz);window.__rz=setTimeout(responsive,120);
});
})();
"""


CARD_FIELDS = [
    ("marketCap", "Market cap"),
    ("price", "Price"),
    ("previousClose", "Previous close"),
    ("changePercent", "Change"),
    ("volume", "Volume"),
    ("sentiment7d", "Sentiment 7d"),
    ("sentimentChange7d", "Sentiment change 7d"),
    ("sentisenseScore", "SentiSense Score"),
    ("mentionsZ", "Mentions vs baseline"),
    ("optionsInterestScore", "Options interest"),
]


def card_value(tile, key):
    value = tile[key]
    if key == "marketCap":
        if tile["capMissing"]:
            return NA
        return fmt_usd(value)
    if key in ("price", "previousClose"):
        return fmt_price(value)
    if key == "volume":
        return fmt_count(value)
    return fmt_metric(key, value)


def render_page(board, layout, scales, initial_metric, rendered_at):
    tiles = board["tiles"]
    sector_of = {}
    for s_idx, sector in enumerate(board["sectors"]):
        for member in layout["members"][s_idx]:
            sector_of[member] = s_idx

    bands = []
    display = []
    for scale in scales:
        key = scale["key"]
        display.append([fmt_metric(key, t[key]) for t in tiles])
    for i, tile in enumerate(tiles):
        bands.append([band_index(scale, tile[scale["key"]]) for scale in scales])

    card_values = []
    card_foot = []
    for tile in tiles:
        card_values.append([card_value(tile, key) for key, _ in CARD_FIELDS])
        foot = ("Price as of " + fmt_stamp(tile["priceAsOf"])
                if tile["priceAsOf"] else "No price as-of on this row")
        if tile["capMissing"]:
            foot += ". No market cap on file, drawn at the smallest area."
        card_foot.append(foot)

    for scale in scales:
        metric = METRIC_BY_KEY[scale["key"]]
        if scale["kind"] == "diverging":
            cap = scale["cap"]
            scale["lowLabel"] = fmt_metric(scale["key"], -cap) + " " + metric["low"]
            scale["highLabel"] = fmt_metric(scale["key"], cap) + " " + metric["high"]
            scale["scaleNote"] = ("Colour runs to %s either side, fitted to this board."
                                  % fmt_metric(scale["key"], cap))
        else:
            scale["lowLabel"] = fmt_metric(scale["key"], scale["lo"]) + " " + metric["low"]
            scale["highLabel"] = fmt_metric(scale["key"], scale["hi"]) + " " + metric["high"]
            scale["scaleNote"] = ("Colour runs %s to %s, fitted to this board."
                                  % (fmt_metric(scale["key"], scale["lo"]),
                                     fmt_metric(scale["key"], scale["hi"])))

    sector_payload = []
    for sector in board["sectors"]:
        head = []
        if sector["moodScore"] is not None:
            head.append("mood %s" % fmt_plain(sector["moodScore"], 1))
        if sector["moodPhase"]:
            head.append(sector["moodPhase"])
        # On a Free board the drawn count is not the sector's size, so say both rather than
        # letting the smaller number pass for the sector.
        if sector["boardCount"] and sector["boardCount"] != sector["drawnCount"]:
            head.append("%d of %d" % (sector["drawnCount"], sector["boardCount"]))
        else:
            head.append("%d" % sector["drawnCount"])
        sector_payload.append({"name": sector["name"],
                               "short": SECTOR_SHORT.get(sector["name"], sector["name"]),
                               "head": " ".join(head)})

    payload = {
        "tiles": [[safe(t["ticker"]), safe(t["name"]), safe(t["industry"] or "")]
                  for t in tiles],
        "fields": [{"key": "ticker", "label": "Ticker"},
                   {"key": "name", "label": "Name"},
                   {"key": "industry", "label": "Industry"}]
                  + [{"key": k, "label": lbl} for k, lbl in CARD_FIELDS],
        "sectors": [{"name": safe(x["name"]), "short": safe(x["short"]),
                     "head": safe(x["head"])} for x in sector_payload],
        "sectorOf": [sector_of[i] for i in range(len(tiles))],
        "layout": layout,
        "bands": bands,
        "display": [[safe(v) for v in row] for row in display],
        "cardValues": [[safe(v) for v in row] for row in card_values],
        "cardFoot": [safe(v) for v in card_foot],
        "scales": [{k: v for k, v in s.items() if k not in ("edges",)} for s in scales],
        "metrics": [{"key": m["key"], "label": m["label"], "short": m["short"],
                     "blurb": m["blurb"]} for m in METRICS],
        "initialMetric": initial_metric,
        "noReading": NO_READING_FILL,
        "flat": FLAT_FILL,
    }

    mood = fmt_whole(board["moodScore"])
    phase = board["moodPhase"] or NA
    up = board["breadthUp"]
    down = board["breadthDown"]
    cap_w = board["capWeighted"]
    eq_w = board["equalWeighted"]
    cap_cls = "flat" if cap_w is None or abs(cap_w) < 1e-9 else ("up" if cap_w > 0 else "dn")

    # A metric the payload does not carry is disabled, never coloured. The two reasons read
    # differently on purpose: "not on this key" is a tier, "not built today" is a gap.
    buttons = []
    for metric in METRICS:
        state = board["metricStates"].get(metric["key"], "ok")
        pressed = "true" if metric["key"] == initial_metric else "false"
        if state == "pro":
            title, off = "PRO overlay, not on this key", " disabled"
        elif state == "unavailable":
            title = "%s was not built for this board today" % metric["label"]
            off = " disabled"
        else:
            title, off = metric["blurb"], ""
        buttons.append('<button type="button" data-m="%s" aria-pressed="%s" title="%s"%s>%s'
                       '</button>' % (esc(metric["key"]), pressed, esc(title), off,
                                      esc(metric["short"])))

    sample_banner = ""
    if board["isSample"]:
        sample_banner = ('<p class="sample">Sample data. This board was rendered from a bundled '
                         'fixture, not from a live market read. Do not read it as a market '
                         'observation.</p>')

    layers_html = "".join("<p>%s</p>" % esc(line) for line in layer_lines(board))

    parts = []
    parts.append("<!doctype html>")
    parts.append('<html lang="en"><head><meta charset="utf-8">')
    parts.append('<meta name="viewport" content="width=device-width,initial-scale=1">')
    parts.append("<title>US market heatmap %s</title>" % esc(board["scopeName"]))
    parts.append("<style>%s</style></head><body><div class=\"wrap\">" % CSS)
    parts.append(sample_banner)
    parts.append('<div class="mast"><div><h1>US market heatmap</h1>')
    parts.append('<div class="sub">%s &middot; tiles sized by market cap &middot; %s'
                 '</div></div>' % (esc(board["scopeName"]), esc(as_of_line(board))))
    parts.append('<div class="sub">Rendered %s</div></div><div class="rule"></div>' % esc(rendered_at))

    parts.append('<div class="stats">')
    parts.append('<div class="stat"><div class="k">Market Mood</div><div class="v">%s</div>'
                 '<div class="n">%s, fear to greed</div></div>' % (esc(mood), esc(phase)))
    parts.append('<div class="stat"><div class="k">Breadth</div><div class="v">'
                 '<span class="up">%s</span> up &middot; <span class="dn">%s</span> down</div>'
                 '<div class="n">%s</div></div>'
                 % (esc(fmt_count(up)), esc(fmt_count(down)), esc(breadth_coverage(board))))
    parts.append('<div class="stat"><div class="k">Cap weighted</div>'
                 '<div class="v %s">%s</div><div class="n">equal weighted %s</div></div>'
                 % (cap_cls, esc(fmt_signed(cap_w, 2, "%")), esc(fmt_signed(eq_w, 2, "%"))))
    parts.append('<div class="stat"><div class="k">Sectors</div><div class="v">%d</div>'
                 '<div class="n">click a sector name to zoom</div></div>'
                 % len(board["sectors"]))
    parts.append("</div>")

    parts.append('<div class="bar"><div class="seg" role="group" aria-label="Colour metric">')
    parts.append("".join(buttons))
    parts.append('</div><input id="q" type="search" placeholder="Find a ticker" '
                 'aria-label="Find a ticker">')
    parts.append('<button type="button" id="back" hidden>All sectors</button></div>')
    tier_note = toggle_note(board)
    if tier_note:
        parts.append('<p class="note tier">%s</p>' % esc(tier_note))
    parts.append('<p class="note" id="mnote"></p>')
    parts.append('<div class="legend" id="legend"></div>')
    parts.append('<div id="board"></div>')
    parts.append('<div id="card" role="status" aria-live="polite"></div>')

    parts.append("<footer>")
    parts.append(layers_html)
    parts.append("<p>%s</p>" % esc(preview_note(board)))
    gone = [LAYER_LABEL.get(name, name) for name in unavailable_layers(board)]
    if gone:
        parts.append("<p>Layers that did not run for this board: %s. No tier carries %s "
                     "today.</p>" % (esc(", ".join(gone)), "it" if len(gone) == 1 else "them"))
    if is_partial_board(board):
        parts.append("<p>Sector Market Mood readings cover the whole index. The tiles cover the "
                     "names drawn here.</p>")
    if board["capMissing"]:
        parts.append("<p>%d %s no market cap on file and %s drawn at the smallest area.</p>"
                     % (board["capMissing"],
                        "tile has" if board["capMissing"] == 1 else "tiles have",
                        "is" if board["capMissing"] == 1 else "are"))
    if board["missingPrice"]:
        missing = len(board["missingPrice"])
        parts.append("<p>%d %s in this index had no price and %s no tile.</p>"
                     % (missing, "name" if missing == 1 else "names",
                        "carries" if missing == 1 else "carry"))
    parts.append('<p id="tinynote"></p>')
    parts.append("<p>A snapshot, not a live view. Nothing here updates on its own.</p>")
    parts.append('<p class="dis">%s</p>' % esc(DISCLAIMER))
    parts.append('<p><a href="https://sentisense.ai">sentisense.ai</a></p>')
    parts.append("</footer></div>")
    encoded = json.dumps(payload, separators=(",", ":")).replace("<", "\\u003c")
    parts.append("<script>window.__BOARD__=%s;</script>" % encoded)
    parts.append("<script>%s</script></body></html>" % JS)
    return "".join(parts)


# --------------------------------------------------------------------------------------
# summary sidecar
# --------------------------------------------------------------------------------------
def build_summary(board, scales, initial_metric, out_path, size, rendered_at,
                  requested_metric=None):
    movers = [t for t in board["tiles"] if t["changePercent"] is not None]
    movers_up = sorted(movers, key=lambda t: -t["changePercent"])[:3]
    movers_down = sorted(movers, key=lambda t: t["changePercent"])[:3]

    # Unclassified is a data-quality bucket, not a sector, so it never wins the strongest or
    # weakest line: "weakest sector Unclassified" is a sentence that tells a reader nothing. It
    # stays in the board and in the sector list, it just cannot be ranked as a sector.
    ranked = [s for s in board["sectors"]
              if s["capWeighted"] is not None and s["name"] != UNCLASSIFIED]
    ranked.sort(key=lambda s: -s["capWeighted"])
    by_mood = [s for s in board["sectors"] if s["moodScore"] is not None]
    by_mood.sort(key=lambda s: -s["moodScore"])

    def sector_line(sector):
        return {
            "name": sector["name"],
            "drawnCount": sector["drawnCount"],
            "boardCount": sector["boardCount"],
            "moodScore": sector["moodScore"],
            "moodScoreDisplay": fmt_plain(sector["moodScore"], 1),
            "moodPhase": sector["moodPhase"] or NA,
            "moodWeeklyChangeDisplay": fmt_signed(sector["moodWeekly"], 1),
            "capWeightedChangePct": sector["capWeighted"],
            "capWeightedChangeDisplay": fmt_signed(sector["capWeighted"], 2, "%"),
            "up": sector["up"],
            "down": sector["down"],
        }

    def mover_line(tile):
        return {
            "ticker": tile["ticker"],
            "name": tile["name"],
            "sector": tile["sector"],
            "changePercent": tile["changePercent"],
            "changeDisplay": fmt_metric("changePercent", tile["changePercent"]),
        }

    no_reading = {}
    for scale in scales:
        no_reading[scale["key"]] = scale["missing"]

    return {
        "scope": board["scope"],
        "scopeName": board["scopeName"],
        "asOf": board["asOf"],
        "asOfDisplay": fmt_stamp(board["asOf"]),
        "asOfLineDisplay": as_of_line(board),
        "generatedAtDisplay": fmt_stamp(board["generatedAt"]),
        "renderedAtDisplay": rendered_at,
        "isSampleData": board["isSample"],
        "apiCalls": 0 if board["isSample"] else 1,
        "marketMood": {
            "score": board["moodScore"],
            "scoreDisplay": fmt_whole(board["moodScore"]),
            "phase": board["moodPhase"] or NA,
        },
        "breadth": {
            "up": board["breadthUp"],
            "down": board["breadthDown"],
            "upDisplay": fmt_count(board["breadthUp"]),
            "downDisplay": fmt_count(board["breadthDown"]),
            "capWeightedChangePct": board["capWeighted"],
            "capWeightedChangeDisplay": fmt_signed(board["capWeighted"], 2, "%"),
            "equalWeightedChangePct": board["equalWeighted"],
            "equalWeightedChangeDisplay": fmt_signed(board["equalWeighted"], 2, "%"),
            "coverageDisplay": breadth_coverage(board),
            "headlineDisplay": "%s advancing, %s declining, cap weighted %s, %s"
                               % (fmt_count(board["breadthUp"]), fmt_count(board["breadthDown"]),
                                  fmt_signed(board["capWeighted"], 2, "%"),
                                  breadth_coverage(board)),
        },
        "preview": {
            "isPreview": board["isPreview"],
            "previewReason": board["previewReason"],
            "tilesDrawn": len(board["tiles"]),
            "tilesDrawnDisplay": fmt_count(len(board["tiles"])),
            "totalCount": board["totalCount"],
            "totalCountDisplay": fmt_count(board["totalCount"]),
            "isPartialBoard": is_partial_board(board),
            "withheldLayers": list(board["withheld"]),
            "withheldDisplay": join_words(withheld_words(board)),
            "unavailableLayers": unavailable_layers(board),
            "metricStates": dict(board["metricStates"]),
            "noteDisplay": preview_note(board),
            "toggleNoteDisplay": toggle_note(board),
        },
        "colourMetric": {
            "key": initial_metric,
            "label": METRIC_BY_KEY[initial_metric]["label"],
            "requestedKey": requested_metric or initial_metric,
            "fellBack": bool(requested_metric) and requested_metric != initial_metric,
        },
        "sectorsByChange": [sector_line(s) for s in ranked],
        "sectorsByMood": [sector_line(s) for s in by_mood],
        "strongestSector": sector_line(ranked[0]) if ranked else None,
        "weakestSector": sector_line(ranked[-1]) if ranked else None,
        "hottestSectorByMood": sector_line(by_mood[0]) if by_mood else None,
        "coolestSectorByMood": sector_line(by_mood[-1]) if by_mood else None,
        "biggestMovesUp": [mover_line(t) for t in movers_up],
        "biggestMovesDown": [mover_line(t) for t in movers_down],
        "layers": layer_lines(board),
        "noReadingCounts": no_reading,
        "tilesWithoutMarketCap": board["capMissing"],
        "namesWithoutPrice": len(board["missingPrice"]),
        "outputPath": out_path,
        "outputChars": size,
        "inlineLimit": INLINE_LIMIT,
        "withinInlineLimit": size <= INLINE_LIMIT,
    }


# --------------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------------
def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="heatmap.py",
        description="Render the US market heatmap as one self-contained interactive HTML file.")
    parser.add_argument("--scope", default="sp500",
                        help="sp500 (default), nasdaq100 or popular")
    parser.add_argument("--out", default="market-heatmap.html",
                        help="Where to write the HTML file. Default market-heatmap.html")
    parser.add_argument("--summary-json", default=None,
                        help="Use - to print summary JSON to stdout, or name a compatibility file")
    parser.add_argument("--metric", default="changePercent",
                        help="Initial colour metric: change, sentiment, score, mentions, options")
    parser.add_argument("--fixture", default=None,
                        help="Render from a saved API response instead of calling the API")
    return parser.parse_args(argv)


def resolve_metric(raw):
    key = METRIC_ALIASES.get(raw.strip().lower(), raw.strip())
    if key not in METRIC_BY_KEY:
        raise Loud("Unknown metric '%s'." % raw, EXIT_USAGE,
                   "Valid: " + ", ".join(sorted(set(list(METRIC_ALIASES) + list(METRIC_BY_KEY)))))
    return key


def run(argv):
    args = parse_args(argv)
    metric = resolve_metric(args.metric)

    if args.fixture:
        envelope = load_fixture(args.fixture)
        scope = args.scope
    else:
        scope = args.scope.strip().lower()
        if scope not in SCOPES:
            raise Loud("Unknown scope '%s'." % args.scope, EXIT_USAGE,
                       "Valid scopes: " + ", ".join(SCOPES))
        key = os.environ.get("SENTISENSE_API_KEY", "").strip()
        if not key:
            raise Loud("SENTISENSE_API_KEY is not set.", EXIT_USAGE,
                       "Get a free key at https://app.sentisense.ai/get-api-key")
        sys.stderr.write("Fetching the %s board: one API call.\n" % scope)
        envelope = fetch_board(scope, key)

    board = build_board(envelope, scope, bool(args.fixture))

    # An overlay this key did not receive, or one the board never carried, is not something to
    # colour: the board would come back uniformly grey and read as a market with no readings.
    # Fall back to the day's move, say why on the error stream, and still produce a page.
    requested = metric
    state = board["metricStates"].get(metric, "ok")
    if state != "ok":
        metric = "changePercent"
        if state == "pro":
            sys.stderr.write(
                "%s is a PRO overlay and is not in this response, so the board opens on the "
                "day's change instead. Nothing is estimated in its place. PRO: "
                "https://app.sentisense.ai/pricing\n" % METRIC_BY_KEY[requested]["label"])
        else:
            sys.stderr.write(
                "%s did not run for this board, so no tier carries it today. The board opens on "
                "the day's change instead.\n" % METRIC_BY_KEY[requested]["label"])

    layout = build_layout(board)
    scales = build_scales(board)
    rendered_at = datetime.now(timezone.utc).strftime("%d %b %Y %H:%M UTC")
    html = render_page(board, layout, scales, metric, rendered_at)

    out_path = os.path.abspath(args.out)
    parent = os.path.dirname(out_path)
    if parent and not os.path.isdir(parent):
        raise Loud("The output directory does not exist: %s" % parent, EXIT_USAGE)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html)

    size = len(html)
    if size > INLINE_LIMIT:
        sys.stderr.write(
            "Warning: the page is %d characters, over the %d character inline limit. It still "
            "opens as a file, but a host that renders it inline will refuse it.\n"
            % (size, INLINE_LIMIT))
    sys.stderr.write("%d tiles, %d sectors, %d characters.\n"
                     % (len(board["tiles"]), len(board["sectors"]), size))
    if board["isPreview"]:
        sys.stderr.write("%s\n" % preview_note(board))

    if args.summary_json:
        summary = build_summary(board, scales, metric, out_path, size, rendered_at,
                                requested_metric=requested)
        if args.summary_json == "-":
            json.dump(summary, sys.stdout, indent=2)
            sys.stdout.write("\n")
            return 0
        else:
            summary_path = os.path.abspath(args.summary_json)
            with open(summary_path, "w", encoding="utf-8") as fh:
                json.dump(summary, fh, indent=2)
                fh.write("\n")
            sys.stderr.write("Summary: %s\n" % summary_path)

    sys.stdout.write(out_path + "\n")
    return 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        return run(argv)
    except Loud as exc:
        sys.stderr.write("heatmap: %s\n" % exc)
        if exc.hint:
            sys.stderr.write("        %s\n" % exc.hint)
        return exc.code


if __name__ == "__main__":
    sys.exit(main())
