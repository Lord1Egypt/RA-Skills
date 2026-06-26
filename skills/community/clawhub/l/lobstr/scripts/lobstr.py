#!/usr/bin/env python3
"""
LOBSTR — Startup Idea Scorer
Usage: python3 lobstr.py "your startup idea" [--public] [--moltbook] [--json]
No API keys required — uses hosted API at runlobstr.com.
Set ANTHROPIC_API_KEY + EXA_API_KEY for unlimited local scans (BYOK).
"""

import json
import os
import sys
import urllib.request
import urllib.parse
import urllib.error

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
EXA_API_KEY = os.environ.get("EXA_API_KEY", "")

# BYOK mode: if both keys are set, run locally for unlimited scans.
# Otherwise, use the free hosted API at runlobstr.com.
BYOK = bool(ANTHROPIC_API_KEY and EXA_API_KEY)

RUNLOBSTR_API = os.environ.get("RUNLOBSTR_API", "https://runlobstr.com/api/score")

# ── helpers ──────────────────────────────────────────────────────────────────

def anthropic_call(model: str, system: str, user: str, max_tokens: int = 1024) -> str:
    payload = json.dumps({
        "model": model,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}]
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read())
    return body["content"][0]["text"].strip()


def exa_search(query: str, num_results: int = 5) -> list[dict]:
    payload = json.dumps({
        "query": query,
        "numResults": num_results,
        "type": "neural",
        "useAutoprompt": True,
        "contents": {"text": {"maxCharacters": 200}},
    }).encode()
    req = urllib.request.Request(
        "https://api.exa.ai/search",
        data=payload,
        headers={
            "x-api-key": EXA_API_KEY,
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read())
        return body.get("results", [])
    except Exception:
        return []


def grid_match(category: str, geography: str, keywords: str) -> dict:
    params = urllib.parse.urlencode({
        "category": category,
        "geography": geography,
        "keywords": keywords,
    })
    url = f"https://grid.nma.vc/api/public/vcs/match-count?{params}"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return json.loads(resp.read())
    except Exception:
        return {"investor_count": 0, "match_quality": "unknown"}


def score_bar(score: int) -> str:
    filled = round(score / 10)
    return "[" + "=" * filled + "-" * (10 - filled) + "]"


def color_dot(score: int) -> str:
    if score >= 70:
        return "🟢"
    if score >= 50:
        return "🟡"
    return "🔴"


# ── step 1: parse idea ────────────────────────────────────────────────────────

def parse_idea(idea: str) -> dict:
    system = (
        "You are a startup analyst. Given a startup idea, extract structured data. "
        "Reply with ONLY valid JSON, no markdown fences, no extra text."
    )
    prompt = f"""Startup idea: {idea}

Return JSON with these keys:
- problem: one sentence
- solution: one sentence
- market: short market name (e.g. "Legal Tech", "FinTech", "HealthTech")
- geography: short region (e.g. "Global", "EU", "US", "MENA", "APAC", "LATAM")
- category: one of [B2B SaaS, B2C, Marketplace, Infrastructure, DeepTech, Consumer, Other]
- queries: array of exactly 3 short search queries to find competitors
"""
    raw = anthropic_call("claude-haiku-4-5", system, prompt, max_tokens=512)
    # strip markdown fences if model adds them despite instructions
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


# ── step 2: search competitors ────────────────────────────────────────────────

def search_competitors(queries: list[str]) -> list[str]:
    results = []
    for q in queries:
        hits = exa_search(q, num_results=4)
        for h in hits:
            title = h.get("title") or h.get("url", "")
            url = h.get("url", "")
            snippet = (h.get("text") or "")[:120]
            if title or url:
                results.append(f"• {title} ({url}) — {snippet}")
    return results[:12]  # cap context


# ── step 3: score idea ────────────────────────────────────────────────────────

def score_idea(idea: str, parsed: dict, competitors: list[str]) -> dict:
    system = (
        "You are a senior VC partner with a sharp, honest voice. "
        "Score startup ideas with precision. Reply ONLY with valid JSON, no markdown."
    )
    competitor_text = "\n".join(competitors) if competitors else "No competitors found."
    prompt = f"""Startup idea: {idea}

Problem: {parsed['problem']}
Solution: {parsed['solution']}
Market: {parsed['market']}
Geography: {parsed['geography']}
Category: {parsed['category']}

Competitor search results:
{competitor_text}

Score this idea on 6 LOBSTR dimensions, each 0-100:
- L (Landscape): How crowded/favorable is the competitive landscape?
- O (Opportunity): How large and real is the market opportunity?
- B (Business model): How clear, defensible, and scalable is the biz model?
- S (Sharpness): How crisp and differentiated is the idea vs. alternatives?
- T (Timing): Is the market timing right (tailwinds, tech readiness, cultural moment)?
- R (Reach): How easily can this scale to reach a large audience/user base?

Return JSON:
{{
  "L": {{"score": 0-100, "verdict": "one line, sharp"}},
  "O": {{"score": 0-100, "verdict": "one line, sharp"}},
  "B": {{"score": 0-100, "verdict": "one line, sharp"}},
  "S": {{"score": 0-100, "verdict": "one line, sharp"}},
  "T": {{"score": 0-100, "verdict": "one line, sharp"}},
  "R": {{"score": 0-100, "verdict": "one line, sharp"}},
  "overall": 0-100,
  "verdict": "Two sentence VC voice verdict. Honest, no fluff.",
  "build_it": true or false
}}

The overall score is a weighted judgment — not an average. Weight S and B higher.
"""
    raw = anthropic_call("claude-sonnet-4-5", system, prompt, max_tokens=1024)
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


# ── step 4: format score card ─────────────────────────────────────────────────

def build_grid_url(parsed: dict) -> str:
    params = {}
    category = parsed.get("market", "")
    geography = parsed.get("geography", "")

    if category:
        params["search"] = category
    if geography and geography not in ("Global", "global"):
        geo_map = {
            "DACH": "Germany,Austria,Switzerland",
            "EU": "Germany,France,Netherlands,Sweden,Spain",
            "UK": "United Kingdom",
            "Nordics": "Sweden,Norway,Denmark,Finland",
            "US": "United States",
        }
        countries = geo_map.get(geography, geography)
        params["countries"] = countries

    base = "https://grid.nma.vc/vc-list"
    if params:
        return base + "?" + urllib.parse.urlencode(params)
    return base


def format_card(idea: str, scores: dict, grid: dict, parsed: dict) -> str:
    overall = scores["overall"]
    bar = score_bar(overall)
    build_str = "✅ BUILD IT." if scores["build_it"] else "🚫 NOT YET."

    investor_count = grid.get("investor_count", 0)
    match_quality = grid.get("match_quality", "")

    dim_labels = {
        "L": "Landscape  ",
        "O": "Opportunity",
        "B": "Biz model  ",
        "S": "Sharpness  ",
        "T": "Timing     ",
        "R": "Reach      ",
    }

    lines = [
        "🦞 LOBSTR SCAN",
        f'"{idea}"',
        "",
        f"LOBSTR SCORE  {overall}/100  {bar}",
        "",
    ]
    for key, label in dim_labels.items():
        d = scores[key]
        s = d["score"]
        v = d["verdict"]
        lines.append(f"{key}  {label}  {color_dot(s)}  {s}/100  {v}")

    lines += [
        "",
        "VERDICT",
        scores["verdict"],
        "",
        build_str,
    ]

    if investor_count:
        grid_line = f"GRID: {investor_count} investor"
        if investor_count != 1:
            grid_line += "s"
        if match_quality and match_quality != "unknown":
            grid_line += f" ({match_quality} match)"
        grid_line += f" match this space\n→ {build_grid_url(parsed)}"
        lines.append("")
        lines.append(grid_line)

    return "\n".join(lines)


# ── step 5: build score_json for publishing ───────────────────────────────────

def build_score_json(scores: dict, parsed: dict, competitors: list[str], grid: dict) -> dict:
    """Normalize lobstr scores into the score_json shape expected by runlobstr.com."""
    dim_labels = {
        "L": "Landscape",
        "O": "Opportunity",
        "B": "Business model",
        "S": "Sharpness",
        "T": "Timing",
        "R": "Reach",
    }

    overall = scores.get("overall", 0)

    # Derive signal from overall score
    if overall >= 70:
        signal = "STRONG"
    elif overall >= 50:
        signal = "MODERATE"
    else:
        signal = "WEAK"

    # Derive competitor density from number of competitors found
    comp_list = []
    for c in competitors:
        # Parse "• Title (url) — snippet" format
        if c.startswith("• "):
            parts = c[2:].split(" (", 1)
            title = parts[0].strip()
            url = ""
            if len(parts) > 1:
                url = parts[1].split(")", 1)[0]
            comp_list.append({"title": title, "url": url})

    if len(comp_list) >= 8:
        density = "HIGH"
    elif len(comp_list) >= 4:
        density = "MEDIUM"
    else:
        density = "LOW"

    dimensions = {}
    for key, label in dim_labels.items():
        d = scores.get(key, {})
        dimensions[key] = {
            "label": label,
            "score": d.get("score", 0),
            "verdict": d.get("verdict", ""),
        }

    return {
        "overall_score": overall,
        "signal": signal,
        "competitor_density": density,
        "build_it": scores.get("build_it", False),
        "verdict": scores.get("verdict", ""),
        "dimensions": dimensions,
        "grid": {
            "investor_count": grid.get("investor_count", 0),
            "match_quality": grid.get("match_quality", "unknown"),
        },
        "competitors": comp_list[:10],
    }


# ── step 6: publish to runlobstr.com ──────────────────────────────────────────

def publish_card(idea: str, score_json: dict) -> str | None:
    """POST to runlobstr.com/api/publish. Returns public URL or None."""
    try:
        payload = json.dumps({
            "idea": idea,
            "score_json": score_json,
        }).encode()

        req = urllib.request.Request(
            "https://runlobstr.com/api/publish",
            data=payload,
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("url")
    except Exception:
        return None


# ── step 7: post to moltbook m/lobstrscore ───────────────────────────────────

def _moltbook_verify(api_key: str, verification_code: str, challenge_text: str) -> bool:
    """Solve the lobster math challenge and submit the answer."""
    import re
    # Strip obfuscation: remove non-alpha/space/digit chars, lowercase, collapse spaces
    clean = re.sub(r"[^a-zA-Z0-9 ]", " ", challenge_text).lower()
    clean = re.sub(r"\s+", " ", clean).strip()

    # Extract all numbers
    numbers = [float(n) for n in re.findall(r"\b\d+(?:\.\d+)?\b", clean)]
    if len(numbers) < 2:
        return False

    # Detect operation from keywords
    text = clean
    if any(w in text for w in ["times", "multiplied", "multiply", "product"]):
        answer = numbers[0] * numbers[1]
    elif any(w in text for w in ["divided", "divide", "half", "quarter"]):
        answer = numbers[0] / numbers[1]
    elif any(w in text for w in ["minus", "subtract", "slows", "less", "slower", "reduced", "decrease"]):
        answer = numbers[0] - numbers[1]
    else:
        answer = numbers[0] + numbers[1]

    payload = json.dumps({
        "verification_code": verification_code,
        "answer": f"{answer:.2f}",
    }).encode()
    req = urllib.request.Request(
        "https://www.moltbook.com/api/v1/verify",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("success", False)
    except Exception:
        return False


def post_to_moltbook(idea: str, card: str, public_url: str | None) -> None:
    """Post the scan result to m/lobstrscore on Moltbook. Skipped if MOLTBOOK_API_KEY not set."""
    api_key = os.environ.get("MOLTBOOK_API_KEY", "")
    if not api_key:
        return

    overall = ""
    for line in card.splitlines():
        if line.startswith("LOBSTR SCORE"):
            # extract e.g. "42/100"
            import re
            m = re.search(r"(\d+)/100", line)
            if m:
                overall = f" — {m.group(1)}/100"
            break

    # Title: truncate idea to 260 chars + score
    title = idea[:260] + overall

    content = card
    if public_url:
        content += f"\n\n🔗 Full scan: {public_url}"

    post_payload = json.dumps({
        "submolt_name": "lobstrscore",
        "title": title,
        "content": content,
        "url": public_url or "https://runlobstr.com",
        "type": "link" if public_url else "text",
    }).encode()

    req = urllib.request.Request(
        "https://www.moltbook.com/api/v1/posts",
        data=post_payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())

        if not data.get("success"):
            print(f"[moltbook] post failed: {data}", file=sys.stderr)
            return

        post = data.get("post", {})
        verification = post.get("verification")
        if verification:
            code = verification.get("verification_code", "")
            challenge = verification.get("challenge_text", "")
            ok = _moltbook_verify(api_key, code, challenge)
            if ok:
                print(f"[moltbook] posted to m/lobstrscore ✓", file=sys.stdout)
            else:
                print(f"[moltbook] post created but verification failed", file=sys.stderr)
        else:
            print(f"[moltbook] posted to m/lobstrscore ✓", file=sys.stdout)

    except Exception as e:
        print(f"[moltbook] post failed: {e}", file=sys.stderr)


# ── hosted API call (default, no keys needed) ────────────────────────────────

def score_via_api(idea: str) -> dict | None:
    """Call runlobstr.com/api/score. Returns the response dict or None on failure."""
    try:
        payload = json.dumps({"idea": idea}).encode()
        req = urllib.request.Request(
            RUNLOBSTR_API,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=90) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            err = json.loads(body)
            msg = err.get("message", body)
        except Exception:
            msg = body
        print(f"Error: {msg}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error calling runlobstr.com: {e}", file=sys.stderr)
        return None


def format_api_card(idea: str, score_json: dict) -> str:
    """Format a score card from the API response."""
    overall = score_json.get("overall_score", 0)
    bar = score_bar(overall)
    build = score_json.get("build_it", False)
    build_str = "✅ BUILD IT." if build else "🚫 NOT YET."

    dim_labels = {
        "L": "Landscape  ",
        "O": "Opportunity",
        "B": "Biz model  ",
        "S": "Sharpness  ",
        "T": "Timing     ",
        "R": "Reach      ",
    }

    lines = [
        "🦞 LOBSTR SCAN",
        f'"{idea}"',
        "",
        f"LOBSTR SCORE  {overall}/100  {bar}",
        "",
    ]

    dimensions = score_json.get("dimensions", {})
    for key, label in dim_labels.items():
        d = dimensions.get(key, {})
        s = d.get("score", 0)
        v = d.get("verdict", "")
        lines.append(f"{key}  {label}  {color_dot(s)}  {s}/100  {v}")

    lines += [
        "",
        "VERDICT",
        score_json.get("verdict", ""),
        "",
        build_str,
    ]

    grid = score_json.get("grid", {})
    investor_count = grid.get("investor_count", 0)
    match_quality = grid.get("match_quality", "")
    if investor_count:
        grid_line = f"GRID: {investor_count} investor"
        if investor_count != 1:
            grid_line += "s"
        if match_quality and match_quality != "unknown":
            grid_line += f" ({match_quality} match)"
        grid_line += " match this space"
        lines.append("")
        lines.append(grid_line)

    return "\n".join(lines)


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="LOBSTR — Startup Idea Scorer",
        usage='python3 lobstr.py "your startup idea" [--public] [--moltbook] [--json]',
    )
    parser.add_argument("idea", nargs="+", help="The startup idea to score")
    parser.add_argument("--public", action="store_true",
                        help="Publish score card to runlobstr.com and show the share URL")
    parser.add_argument("--moltbook", action="store_true",
                        help="Post scan result to m/lobstrscore on Moltbook")
    parser.add_argument("--json", action="store_true",
                        help="Output raw JSON instead of formatted score card (for agents)")

    args = parser.parse_args()
    idea = " ".join(args.idea).strip('"').strip("'")

    if BYOK:
        # ── BYOK path: local pipeline, unlimited scans ──
        parsed = parse_idea(idea)
        competitors = search_competitors(parsed.get("queries", []))
        scores = score_idea(idea, parsed, competitors)
        grid = grid_match(
            category=parsed.get("category", ""),
            geography=parsed.get("geography", ""),
            keywords=parsed.get("market", idea[:60]),
        )

        score_json = build_score_json(scores, parsed, competitors, grid)

        if args.json:
            print(json.dumps(score_json, indent=2))
        else:
            card = format_card(idea, scores, grid, parsed)
            print(card)

        # Publish only if --public
        public_url = None
        if args.public:
            public_url = publish_card(idea, score_json)
            if public_url:
                print(f"\nShare your scan: {public_url}")

        # Moltbook only if --moltbook
        if args.moltbook:
            card = format_card(idea, scores, grid, parsed) if args.json else card
            post_to_moltbook(idea, card, public_url)
    else:
        # ── Hosted API path: no keys needed ──
        result = score_via_api(idea)
        if not result:
            sys.exit(1)

        score_json = result.get("score_json", {})
        public_url = result.get("url")

        if args.json:
            print(json.dumps(score_json, indent=2))
        else:
            card = format_api_card(idea, score_json)
            print(card)

        # Show URL only if --public
        if args.public and public_url:
            print(f"\nShare your scan: {public_url}")

        # Moltbook only if --moltbook
        if args.moltbook:
            card = format_api_card(idea, score_json) if args.json else card
            post_to_moltbook(idea, card, public_url if args.public else None)


if __name__ == "__main__":
    main()
