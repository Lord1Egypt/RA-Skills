# Primary-source research when the search layer is degraded

If `web_search` (SearXNG) returns an empty `results` array AND `web_extract` errors out, do **not** conclude the open web is unreachable and do **not** keep retrying search or falling back to the browser. The metasearch layer is what's down; direct primary-source endpoints and feed readers usually still respond. Use these instead — they are direct HTTP to authoritative hosts, not metasearch, so they survive SearXNG / DuckDuckGo / Bing degradation.

## 1. SEC EDGAR — authoritative public-company filings (no key, no search)
For any US-listed company: verify exactly what was filed and when. This is the gold-standard check for an "8-K burst" risk flag, going-concern / restatement / departure items, or dating a catalyst — far better than inferring from a headline.

Step A — ticker → CIK (10-digit, zero-padded):
```python
import json, urllib.request
# SEC requires a descriptive User-Agent or it 403s
H = {"User-Agent": "<agent-name> <agent-handle>@gmail.com"}
d = json.loads(urllib.request.urlopen(
    urllib.request.Request("https://www.sec.gov/files/company_tickers.json", headers=H),
    timeout=30).read())
m = {v["ticker"]: f'{v["cik_str"]:010d}' for v in d.values()}
# m["NVDA"] -> "0001045810"
```

Step B — recent filings + item types:
```python
import json, urllib.request
cik = m["NVDA"]
u = f"https://data.sec.gov/submissions/CIK{cik}.json"
d = json.loads(urllib.request.urlopen(
    urllib.request.Request(u, headers=H), timeout=30).read())
r = d["filings"]["recent"]
# r["form"], r["filingDate"], r["items"], r["accessionNumber"] are parallel arrays
# 8-K "items" field carries exhibit/item codes: 1.01, 2.02, 5.02, 8.01, 9.01 ...
eights = [(f, dt, it) for f, dt, it in zip(r["form"], r["filingDate"], r["items"]) if f.startswith("8-K")]
```
Routine 8-Ks (governance 5.02/5.07, Reg-FD 7.01/9.01, earnings 2.02) are NOT adverse events; only items like 1.01 (bankruptcy), 2.03/2.04 (off-balance-sheet/triggered defaults), 3.01 (delisting), 4.02 (accounting/AO departure) signal real distress.

## 2. Google News RSS — recent coverage without a search engine
```

> **Google News RSS requires redirect-following.** Without `-L` the endpoint
> answers **HTTP 302 with zero items**, which reads as "no results" rather than
> "you did not follow the redirect". Measured 2026-08-17.
>
> ```bash
> curl -sL 'https://news.google.com/rss/search?q=<query>'   # -L is required
> ```

https://news.google.com/rss/search?q=<urlencoded query>&hl=en-US&gl=US&ceid=US:en
```
Parse with `xml.etree.ElementTree` (each `<item>` → `<title>` + `<pubDate>`). Rate-limit-friendly and clean compared to DDG/Bing HTML scraping. Best for "is there a catalyst / meme-pump in the last ~2 weeks?" — filter by `pubDate`.

## 3. Jina Reader — clean markdown for any specific URL
```
curl -s "https://r.jina.ai/<TARGET_URL>"
```
Returns `Title:` + clean Markdown. Confirmed working on this profile even when the `web_extract` backend (SearXNG) is broken. Use as the direct read fallback for a known page.

## Ordering vs. other fallbacks
- `references/ddg_html_fallback.md` — tier 0: try DuckDuckGo HTML first (fast, no key).
- This file — tier 1: when DDG is also rate-limiting (common from datacenter IPs) or `web_extract` is down, go straight to the direct endpoints above.
- `sift.fetch` Jina fallback and `sift.webwright` remain for reading/automating a specific JS-heavy page.
