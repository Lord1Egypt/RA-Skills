# 🛒 Amazon Best Sellers Scraper — No Code, No Manual Work

Scrape Amazon best sellers (title, price, rating, review count, product URL) and export them into a formatted Word report, **fully automated**.

> **Record once → generate a Python script → replay instantly with no LLM, no tokens, no hallucinations.**

---

## What This Scraper Does

| Field | Example |
|-------|---------|
| Product Title | Women's Classic T-Shirt |
| Price | $19.99 |
| Star Rating | 4.5 |
| Review Count | 4,532 |
| Product URL | https://www.amazon.com/dp/B09XXXXX |

Output: a Word (`.docx`) table appended to your Desktop, timestamped at query time.

---

## Why OpenClaw-RPA for Amazon?

Amazon is a heavily JavaScript-rendered site. Traditional scrapers rely on hardcoded CSS selectors that break whenever Amazon updates its DOM. OpenClaw-RPA takes a different approach:

1. **Live DOM analysis (`data_groups`)** — on every recording run, `snapshot` scans the real page and auto-detects repeating product card containers and their child field selectors. No guessing, no training-knowledge selectors.
2. **`page.evaluate` for URLs** — product links are `href` attributes, not text. The scraper uses `el.querySelector('a[href*="/dp/"]')?.href` to get full absolute URLs. `extract_text` cannot do this.
3. **Row-aligned extraction** — all fields for one product are extracted from the same DOM container in a single JS pass, preventing zip-mismatch bugs across fields.
4. **Scroll-to-load** — Amazon lazy-loads cards; the script scrolls incrementally until ≥ N items appear.

---

## Step 1: Install

```bash
openclaw skills install openclaw-rpa
# or manually:
git clone https://github.com/laziobird/openclaw-rpa.git ~/.openclaw/workspace/skills/openclaw-rpa
cd ~/.openclaw/workspace/skills/openclaw-rpa && ./scripts/install.sh
```

Recommended model: **Gemini Pro 3.0 / Claude Sonnet 4.6 / Minimax 2.7**

---

## Step 2: Send the Prompt

Open an OpenClaw chat and paste:

```text
#RPA
AmazonBestSeller
E

[var]
query_time = ### current time, format MM月DD日HH时mm分 ###
output_path = '~/Desktop/amazon.docx'

[do]
1. Open https://www.amazon.com/s?k=Clothing%2C+Shoes+%26+Jewelry&language=zh
2. Extract the first 40 products: title, price, rating, review count, product URL
3. Table headers: Title | Price | Rating | Reviews | URL — add ${query_time} above
4. Append to ${output_path} (create if not exists)
```

> - Line 1 `#RPA` — trigger  
> - Line 2 `AmazonBestSeller` — task name → generates `rpa/amazonbestseller.py`  
> - Line 3 `E` — capability code: browser + Word

---

## Step 3: How the Agent Records

| Step | Action | What happens |
|------|--------|--------------|
| 1 | `goto` | Opens the Amazon search page |
| 2 | `snapshot` | `data_groups` detects `[data-component-type="s-search-result"]` as the product card container; samples `title`, `price`, `rating`, `reviews`, `href` selectors from the live DOM |
| 3 | `scroll` | Scrolls until ≥ 40 product cards are loaded |
| 4 | `python_snippet` | `page.evaluate()` JS extracts all five fields row-aligned using selectors from `data_groups` (no guessing); writes `rows.json` |
| 5 | `word_write` | Reads `rows.json`, appends formatted table to `amazon.docx` |

---

## Step 4: End Recording & Replay

Send `#end` → script is synthesized at `rpa/amazonbestseller.py`.

```bash
# Replay — zero token cost, runs in seconds
python3 rpa_manager.py run AmazonBestSeller
# or directly:
python3 rpa/amazonbestseller.py
```

---

## Already Have It? Run Directly Without Re-recording

The script `amazonbestseller.py` is already registered in [`registry.json`](../registry.json):

```json
"amazonbestseller": "amazonbestseller.py"
```

You can discover and run it without any recording step:

**In OpenClaw chat:**

```
#rpa-list
```

You'll see `amazonbestseller` in the list. Then run it in a new chat:

```
#rpa-run:amazonbestseller
```

**Or via CLI:**

```bash
python3 rpa_manager.py list          # confirm amazonbestseller is registered
python3 rpa_manager.py run amazonbestseller
```

The script runs standalone — no model, no tokens, no re-recording needed.

---

## Customize

| What to change | How |
|----------------|-----|
| Category | Change `k=` in the URL (e.g. `k=Electronics`) |
| Item count | Change `40` in the task description |
| Output format | Use `excel_write` for `.xlsx` instead of `word_write` |
| Extra fields | Add `seller`, `image_url` via extra `el.querySelector(...)` in the JS |
| Schedule | `cron` + `python3 rpa_manager.py run AmazonBestSeller` |

---

## Reference Script

[`rpa/amazonbestseller.py`](../rpa/amazonbestseller.py) — standalone, ready to run without AI.

Uses `sync_playwright` with `data-cy` semantic selectors, `/dp/` URL extraction, and Word hyperlink formatting.

---

## Compliance Note

Amazon's Terms of Service restrict automated scraping. Use this tool only for personal research or in ways permitted by Amazon's policies.
