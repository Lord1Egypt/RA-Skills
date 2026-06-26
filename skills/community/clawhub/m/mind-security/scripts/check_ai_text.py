#!/usr/bin/env python3
"""
check_ai_text.py — Detect AI-generated text (ChatGPT, Claude, Gemini, etc.).

Uses GPTZero API — the leading AI text detection service with per-sentence
scoring, ~99% accuracy, and support for GPT-5, Claude, Gemini, LLaMA models.

Requires: GPTZERO_API_KEY environment variable.

Usage:
    python3 check_ai_text.py "The text to analyze goes here..."
    python3 check_ai_text.py --file essay.txt
    echo "some text" | python3 check_ai_text.py --stdin

No pip dependencies — uses Python stdlib only.
Requires GPTZERO_API_KEY — get it at https://gptzero.me/dashboard
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


# ---------------------------------------------------------------------------
# GPTZero API integration
# ---------------------------------------------------------------------------

GPTZERO_API = "https://api.gptzero.me/v2/predict/text"
USER_AGENT = "Mozilla/5.0 (compatible; mind-security/1.0; +https://github.com/mind-sec/mind-security)"


def _detect_gptzero(text: str, api_key: str) -> dict:
    """Detect AI-generated text via GPTZero API.

    GPTZero uses deep learning models (Model 4.3b, March 2026) trained to
    distinguish human from AI text by analyzing perplexity, burstiness,
    and learned stylistic patterns across GPT-4/5, Claude, Gemini, and LLaMA.
    """
    payload = json.dumps({"document": text}).encode()
    req = urllib.request.Request(
        GPTZERO_API,
        data=payload,
        headers={
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            return {"error": "Invalid GPTZero API key. Check your key at https://gptzero.me/dashboard"}
        if exc.code == 403:
            return {"error": "GPTZero API access forbidden. Ensure your plan includes API access."}
        if exc.code == 429:
            return {"error": "GPTZero rate limit exceeded. Free tier: 10,000 words/month."}
        body = ""
        try:
            body = exc.read().decode()
        except Exception:
            pass
        return {"error": f"GPTZero HTTP {exc.code}", "detail": body}
    except urllib.error.URLError as exc:
        return {"error": f"GPTZero connection failed: {exc.reason}"}
    except Exception as exc:
        return {"error": f"Unexpected error: {exc}"}

    # Parse GPTZero response
    documents = raw.get("documents", [])
    doc = documents[0] if documents else {}

    completely_generated = doc.get("completely_generated_prob", 0)
    average_generated = doc.get("average_generated_prob", 0)
    class_probabilities = doc.get("class_probabilities", {})

    # Per-sentence analysis
    sentences = doc.get("sentences", [])
    sentence_scores = []
    for sent in sentences[:30]:  # Cap at 30 sentences
        sentence_scores.append({
            "text": sent.get("sentence", "")[:200],
            "ai_probability": round(sent.get("generated_prob", 0), 4),
            "perplexity": round(sent.get("perplexity", 0), 2),
        })

    return {
        "completely_generated_prob": round(completely_generated, 4),
        "average_generated_prob": round(average_generated, 4),
        "class_probabilities": {
            k: round(v, 4) for k, v in class_probabilities.items()
        } if class_probabilities else {},
        "sentences": sentence_scores,
    }


# ---------------------------------------------------------------------------
# Detection orchestrator
# ---------------------------------------------------------------------------

def detect_ai_text(text: str, api_key: str) -> dict:
    """Run AI text detection via GPTZero API."""
    result = _detect_gptzero(text, api_key)

    if "error" in result:
        return {
            "result": "error",
            "method": "gptzero",
            "error": result["error"],
            "detail": result.get("detail", ""),
        }

    ai_probability = result.get("completely_generated_prob", 0)

    # Classify
    if ai_probability >= 0.8:
        verdict = "ai_generated"
        confidence = min(0.7 + ai_probability * 0.25, 0.99)
    elif ai_probability >= 0.5:
        verdict = "mixed_or_uncertain"
        confidence = 0.5 + (ai_probability - 0.5) * 0.6
    else:
        verdict = "likely_human"
        confidence = max(0.6, 1.0 - ai_probability)

    return {
        "result": verdict,
        "ai_probability": round(ai_probability, 4),
        "confidence": round(confidence, 4),
        "method": "gptzero",
        "details": result,
    }


# ---------------------------------------------------------------------------
# Setup instructions
# ---------------------------------------------------------------------------

SETUP_INSTRUCTIONS = """\
Error: GPTZERO_API_KEY not set.

GPTZero is the leading AI text detection service with ~99% accuracy
and per-sentence scoring across GPT-4/5, Claude, Gemini, and LLaMA.

Get your API key:

  1. Create a free account at https://gptzero.me
  2. Go to https://gptzero.me/dashboard
  3. Navigate to the API section and generate a key
  4. Free tier includes 10,000 words/month

Then set the environment variable:

  export GPTZERO_API_KEY=your_key_here

Pricing (as of March 2026):
  Free:         10,000 words/month
  Premium:      300,000 words/month — $12.99/mo (annual)
  Professional: 500,000 words/month — $24.99/mo (annual)
  API access:   starts at $45/month (300,000 words)

Documentation: https://gptzero.me/docs
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Detect AI-generated text (ChatGPT, Claude, Gemini, etc.).",
        epilog="Requires GPTZERO_API_KEY. Get your key at https://gptzero.me/dashboard",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "text",
        nargs="?",
        help="Text to analyze for AI generation.",
    )
    group.add_argument(
        "--file", "-f",
        help="Read text from a file.",
    )
    group.add_argument(
        "--stdin",
        action="store_true",
        help="Read text from stdin.",
    )
    args = parser.parse_args()

    # Check API key
    api_key = os.environ.get("GPTZERO_API_KEY", "").strip()
    if not api_key:
        print(SETUP_INSTRUCTIONS, file=sys.stderr)
        sys.exit(1)

    if args.stdin:
        text = sys.stdin.read()
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()
        except OSError as exc:
            print(json.dumps({"result": "error", "error": str(exc)}), file=sys.stderr)
            sys.exit(1)
    else:
        text = args.text

    if not text or not text.strip():
        print(json.dumps({"result": "error", "error": "Empty input text"}))
        sys.exit(1)

    result = detect_ai_text(text, api_key)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("result") != "error" else 1)


if __name__ == "__main__":
    main()
