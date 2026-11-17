#!/usr/bin/env python3
"""
Stage 2 (LLM): Read manifest.json raw_text, call LLM to extract metadata.
Writes to manifest_llm.json with title/author/venue/year/abstract filled.
"""
import os, json, sys, re

MANIFEST_IN  = os.path.join(os.path.dirname(__file__), 'manifest.json')
MANIFEST_OUT = os.path.join(os.path.dirname(__file__), 'manifest_llm.json')


LLM_PROMPT = """You are a research paper metadata extractor. Given the raw OCR/text from the first pages of an academic PDF, extract:

- **title**: the paper title (exact, no extra words)
- **authors**: list of author names (just names, no affiliations/emails)
- **venue**: conference or journal abbreviation (e.g. NeurIPS, ICML, arXiv, JMLR, IEEE Trans. Autom. Control)
- **year**: publication year (4 digits)
- **abstract**: the abstract text (first 300 chars is fine)
- **confidence**: how confident you are (high/medium/low)

Respond ONLY with valid JSON in this exact format:
{{"title":"...","authors":["..."],"venue":"...","year":"...","abstract":"...","confidence":"..."}}

Do not include any explanation or markdown. Just the JSON.
"""


def call_llm(raw_text, year_hint=None, filename=None):
    """Call LLM with the raw text to extract metadata."""
    import socket
    import urllib.request

    # Build context with hint
    hint = f"[Filename hint: {filename}]" if filename else ""
    if year_hint:
        hint += f"\n[Year hint from filename: {year_hint}]"

    prompt = f"{LLM_PROMPT}\n\n{hint}\n\n---PDF TEXT---\n{raw_text[:4000]}\n---END---"

    # Try calling via OpenClaw local API or generic approach
    # We'll use a simple HTTP call to the local gateway if available
    try:
        import urllib.request, urllib.parse, json as json_lib

        payload = json_lib.dumps({
            "model": "minimax-portal/MiniMax-M2.7",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300,
            "temperature": 0.1,
        }).encode("utf-8")

        req = urllib.request.Request(
            "http://127.0.0.1:4892/v1/chat/completions",
            data=payload,
            headers={"Content-Type": "application/json", "Authorization": "Bearer local"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json_lib.load(resp)
            content = result["choices"][0]["message"]["content"].strip()
            # Parse JSON from response
            # Sometimes the model wraps it in ```json ... ```
            if content.startswith("```"):
                content = re.sub(r'^```(?:json)?\s*', '', content, flags=re.I).rstrip('` \n')
            return json_lib.loads(content)
    except Exception as e:
        return {"error": str(e)}


def run():
    if not os.path.exists(MANIFEST_IN):
        print(f"[ERROR] {MANIFEST_IN} not found. Run extract.py first.")
        return

    with open(MANIFEST_IN, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    print(f"Processing {len(manifest)} files with LLM...\n")

    for i, m in enumerate(manifest):
        print(f"[{i+1}/{len(manifest)}] {m['filename'][:60]}")
        raw_text = m.get("raw_text", "") or ""

        result = call_llm(raw_text, year_hint=m.get("year_hint"), filename=m["filename"])

        if "error" in result:
            print(f"  ERROR: {result['error']}")
            m["llm_error"] = result["error"]
            m["status"] = "llm_error"
        else:
            m["title"] = result.get("title")
            m["authors"] = result.get("authors", [])
            m["venue"] = result.get("venue")
            m["year"] = result.get("year") or m.get("year_hint")
            m["abstract"] = result.get("abstract", "")[:500]
            m["llm_confidence"] = result.get("confidence", "unknown")
            m["title_source"] = "llm"
            m["year_source"] = "llm" if result.get("year") else "filename"
            m["venue_source"] = "llm"
            m["status"] = "ready" if result.get("title") else "llm_failed"
            print(f"  title={m.get('title','')[:60]}")
            print(f"  venue={m.get('venue')} year={m.get('year')} confidence={m.get('llm_confidence')}")

        # Keep raw_text to avoid re-reading, but don't serialize all of it
        if len(raw_text) > 5000:
            m["raw_text"] = raw_text[:5000] + "\n[truncated]"

    with open(MANIFEST_OUT, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    ready = sum(1 for m in manifest if m.get("status") == "ready")
    print(f"\n[Done] {ready}/{len(manifest)} files ready. Output -> {MANIFEST_OUT}")


if __name__ == '__main__':
    folder = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    run()
