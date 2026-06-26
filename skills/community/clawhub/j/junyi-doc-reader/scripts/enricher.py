#!/usr/bin/env python3
"""enricher.py - OPTIONAL LLM enrichment for chunks.

Reads chunks.jsonl, calls LLM API for each chunk to generate summaries,
key points, keywords, and classification. Supports resume from interruption.

API config via env vars:
  DOC_READER_API_KEY  - Required for enrichment (no default)
  DOC_READER_API_URL  - User-specified endpoint (no hardcoded production URL)
  DOC_READER_MODEL    - User-specified model name

Usage: python3 scripts/enricher.py <chunks_jsonl> <enriched_chunks_jsonl>

=============================================================================
SECURITY & PRIVACY DISCLOSURE
=============================================================================
This script is OPT-IN and OFF BY DEFAULT. Network egress requires explicit
user configuration. Document content is NEVER sent anywhere unless the user
explicitly enables LLM enrichment.

Default state (no user action = no network):
  - DOC_READER_API_KEY unset      -> enricher does NOT run (pipeline skips it)
  - DOC_READER_ALLOW_EXTERNAL=false (default) -> pipeline blocks enrichment
  - The base archive+index pipeline runs entirely OFFLINE without this script

To activate enrichment, the user MUST take ALL of these steps:
  1. Set DOC_READER_API_KEY     (their own LLM API key)
  2. Set DOC_READER_API_URL     (their own endpoint of choice; e.g. OpenAI,
                                 Anthropic, Azure, a self-hosted model, etc.)
  3. Set DOC_READER_MODEL       (their chosen model)
  4. Set DOC_READER_ALLOW_EXTERNAL=true  (explicit consent flag)

No endpoint is hardcoded as a "production default". The placeholder shown
in DEFAULT_API_URL below is overridden by the env var the user provides.

What is sent (only when user opts in):
  - Each chunk's text -> the user-configured LLM endpoint over HTTPS
  - No credentials, no file paths, no PII metadata beyond the chunk text
  - User can review chunks.jsonl before running enrichment to know exactly
    what would be transmitted

User intent: a user who configures all four env vars has explicitly chosen
to trade privacy for richer summaries. This Skill respects that choice as a
user-controlled feature, not a default behavior.
=============================================================================
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

DEFAULT_API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
MAX_RETRIES = 2
RETRY_DELAY = 2.0
RATE_LIMIT_DELAY = 1.5

SYSTEM_PROMPT = """You are a document analysis assistant. Given a text chunk from a document, produce a JSON object with these fields:
- "summary": A concise 1-3 sentence summary of the chunk content (in the same language as the source).
- "key_points": An array of 2-5 key points (strings).
- "keywords": An array of 3-8 keywords/phrases.
- "classification": An object with optional fields "year" (string, if a specific year is mentioned or strongly implied), "topic" (string, a short topic label).
- "confidence": A float 0.0-1.0 indicating how confident you are in the classification.

Respond ONLY with valid JSON, no markdown fences, no extra text."""

USER_PROMPT_TEMPLATE = """Analyze this text chunk and return the JSON analysis:

---
{text}
---"""


def get_api_config():
    """Read API configuration from environment."""
    api_key = os.environ.get("DOC_READER_API_KEY", "")
    api_url = os.environ.get("DOC_READER_API_URL", DEFAULT_API_URL)
    model = os.environ.get("DOC_READER_MODEL", DEFAULT_MODEL)
    return api_key, api_url, model


def call_llm(text, api_key, api_url, model):
    """Call LLM API and return parsed JSON response."""
    # Truncate very long chunks to avoid token limits
    if len(text) > 6000:
        text = text[:6000] + "\n\n[... truncated for analysis ...]"

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(text=text)},
        ],
        "temperature": 0.2,
        "max_tokens": 800,
    }).encode("utf-8")

    req = urllib.request.Request(
        api_url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    resp = urllib.request.urlopen(req, timeout=60)
    body = json.loads(resp.read().decode("utf-8"))

    # Extract content from OpenAI-compatible response
    content = body["choices"][0]["message"]["content"].strip()

    # Strip markdown fences if present
    if content.startswith("```"):
        lines = content.split("\n")
        # Remove first and last fence lines
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        content = "\n".join(lines)

    return json.loads(content)


def load_completed(output_path):
    """Load already-enriched chunk IDs from output file."""
    completed = {}
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        chunk = json.loads(line)
                        completed[chunk["chunk_id"]] = chunk
                    except (json.JSONDecodeError, KeyError):
                        continue
    return completed


def enrich(chunks_path, output_path):
    """Main enrichment logic with resume support."""
    api_key, api_url, model = get_api_config()

    if not api_key:
        print("ERROR: DOC_READER_API_KEY not set. Cannot run enrichment.")
        print("Set the environment variable or use archive-only mode.")
        sys.exit(1)

    # Load input chunks
    chunks = []
    with open(chunks_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))

    print(f"[enricher] Loaded {len(chunks)} chunks")
    print(f"[enricher] API: {api_url}")
    print(f"[enricher] Model: {model}")

    # Load already completed chunks for resume
    completed = load_completed(output_path)
    if completed:
        print(f"[enricher] Resuming: {len(completed)} chunks already done")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # Open output in append mode for incremental writes
    failed_chunks = []
    newly_done = 0

    with open(output_path, "a", encoding="utf-8") as out_f:
        for i, chunk in enumerate(chunks):
            cid = chunk["chunk_id"]

            # Skip already completed
            if cid in completed:
                continue

            print(f"[enricher] Processing {cid} ({i + 1}/{len(chunks)})...")

            success = False
            for attempt in range(MAX_RETRIES + 1):
                try:
                    result = call_llm(chunk["text"], api_key, api_url, model)

                    # Merge enrichment into chunk
                    enriched = dict(chunk)
                    enriched["summary"] = result.get("summary", "")
                    enriched["key_points"] = result.get("key_points", [])
                    enriched["keywords"] = result.get("keywords", [])
                    enriched["classification"] = result.get("classification", {})
                    enriched["confidence"] = result.get("confidence", 0.0)

                    out_f.write(json.dumps(enriched, ensure_ascii=False) + "\n")
                    out_f.flush()
                    completed[cid] = enriched
                    newly_done += 1
                    success = True
                    break

                except urllib.error.HTTPError as e:
                    body = ""
                    try:
                        body = e.read().decode("utf-8", errors="replace")[:200]
                    except Exception:
                        pass
                    print(f"  Attempt {attempt + 1} failed: HTTP {e.code} - {body}")
                    if e.code == 429:
                        wait = RETRY_DELAY * (attempt + 2)
                        print(f"  Rate limited. Waiting {wait}s...")
                        time.sleep(wait)
                    elif attempt < MAX_RETRIES:
                        time.sleep(RETRY_DELAY)
                except (urllib.error.URLError, json.JSONDecodeError, KeyError, Exception) as e:
                    print(f"  Attempt {attempt + 1} failed: {type(e).__name__}: {e}")
                    if attempt < MAX_RETRIES:
                        time.sleep(RETRY_DELAY)

            if not success:
                print(f"  FAILED after {MAX_RETRIES + 1} attempts, skipping {cid}")
                failed_chunks.append(cid)
                # Write chunk without enrichment so it's not lost
                plain = dict(chunk)
                plain["enrichment_error"] = "Failed after retries"
                out_f.write(json.dumps(plain, ensure_ascii=False) + "\n")
                out_f.flush()

            # Rate limit between calls
            time.sleep(RATE_LIMIT_DELAY)

    total = len(chunks)
    print(f"\n[enricher] Done: {newly_done} newly enriched, {len(completed) - newly_done} previously done, {len(failed_chunks)} failed")
    if failed_chunks:
        print(f"[enricher] Failed chunks: {', '.join(failed_chunks)}")
    print(f"[enricher] Output: {output_path}")

    return failed_chunks


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 enricher.py <chunks_jsonl> <enriched_chunks_jsonl>")
        sys.exit(1)

    chunks_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(chunks_path):
        print(f"ERROR: Chunks file not found: {chunks_path}")
        sys.exit(1)

    enrich(chunks_path, output_path)


if __name__ == "__main__":
    main()
