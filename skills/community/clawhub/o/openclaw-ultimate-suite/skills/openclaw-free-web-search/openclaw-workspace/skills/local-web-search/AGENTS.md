# Agent Injection Rules — Local Free Web Search v4.1

> **Model-agnostic.** These rules apply to any LLM acting as the OpenClaw commander:
> Claude, GPT-4, Gemini, Mistral, Llama, DeepSeek, Qwen, or any other model.
> No model-specific behavior is assumed. All tools are standard Python scripts.

---

## When to use this skill

Activate this skill when:
- The user asks about current events, latest news, recent releases, or real-time information
- The built-in `web_search` tool is unavailable or not configured
- The user explicitly asks to search the web
- The task requires verifying facts with up-to-date sources
- The user asks to fact-check a specific claim

---

## Step 1 — Search

Run the search script with the appropriate intent:

```bash
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/search_local_web.py \
  --query "<user query>" \
  --intent <factual|news|research|tutorial|comparison|privacy|general> \
  --limit 5
```

Choose intent based on query type:
- Current events / news → `--intent news --freshness day`
- Technical docs / facts → `--intent factual`
- Academic / GitHub → `--intent research`
- How-to / examples → `--intent tutorial`
- A vs B questions → `--intent comparison`
- Sensitive queries → `--intent privacy`

---

## Step 2 — Browse top results

For each result with Score > 50 or marked `[cross-validated]`:

```bash
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/browse_page.py \
  --url "<result URL>" \
  --max-words 600
```

If a page is JS-heavy or behind anti-bot protection, retry with:

```bash
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/browse_page.py \
  --url "<result URL>" \
  --mode stealth
```

---

## Step 3 — Verify key facts (for factual claims)

When the answer contains specific facts (dates, names, numbers, events), verify before asserting:

```bash
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/verify_claim.py \
  --claim "<specific factual claim>" \
  --sources 5
```

Or, if you already have relevant URLs from Step 1:

```bash
python3 ~/.openclaw/workspace/skills/local-web-search/scripts/verify_claim.py \
  --claim "<specific factual claim>" \
  --urls <url1> <url2> <url3>
```

---

## Step 4 — Answer rules

- `HIGH` confidence from `browse_page.py` → safe to answer from this page
- `MEDIUM` confidence → answer with caveat, suggest checking another source
- `LOW` confidence → do NOT use this page as a sole source; try the next URL or retry with `--mode stealth` / `--mode dynamic`
- `VERIFIED` or `LIKELY_TRUE` from `verify_claim.py` → assert the claim confidently with citation
- `UNCERTAIN` → tell the user the evidence is mixed; do not assert
- `LIKELY_FALSE` or `UNVERIFIABLE` → tell the user the claim could not be verified
- **NEVER** fabricate content when all sources fail — tell the user the search returned no usable results
- **ALWAYS** cite the URL and published date when answering factual questions
- **PREFER** `[cross-validated]` results over single-engine results for factual claims
- **NEVER** state facts from snippets alone — always browse the full page first

---

## Fallback behaviour

If local SearXNG is unavailable, both scripts automatically fall back to `searx.be`.
If all sources fail, output:

```
Search unavailable. To start local SearXNG:
cd "$(cat ~/.openclaw/workspace/skills/local-web-search/.project_root)" && ./start_local_search.sh
```

---

## Notes for non-Claude models

- **GPT-4 / GPT-4o**: Use the `tool_call` interface to run shell commands. The script outputs plain text and JSON — both are easy to parse.
- **Gemini**: The `--json` flag on all three scripts produces structured output that is easier to process programmatically.
- **Mistral / Llama / local models**: If the model has limited context, use `--max-words 300` in `browse_page.py` to reduce output size.
- **All models**: The `--json` flag is available on all three tools for structured, machine-readable output.
