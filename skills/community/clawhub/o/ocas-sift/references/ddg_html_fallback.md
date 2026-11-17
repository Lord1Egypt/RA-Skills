# DuckDuckGo HTML Fallback (when web_search returns an empty results array)

> **Status check first — this endpoint is currently BLOCKED from this host.**
> Measured 2026-08-17: `html.duckduckgo.com/html` answers **HTTP 202** with a
> challenge page and **zero** parseable result links. It returns a body, so a
> naive check sees "success" and an empty parse rather than an error.
>
> Re-verify before relying on it:
> ```bash
> curl -s -o /tmp/ddg.html -w '%{http_code}\n' \
>   -A 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0' \
>   'https://html.duckduckgo.com/html/?q=test'
> grep -c 'result__a' /tmp/ddg.html    # 0 means still blocked
> ```
> While it is blocked, skip to `primary_source_research.md`. Also check whether
> the real problem is upstream of DuckDuckGo: if `web_search` came back empty,
> confirm which engines SearXNG itself has working before assuming the topic is
> unfindable —
> `curl -s "$SEARXNG_URL/search?q=test&format=json" | jq '[.results[].engines[]] | unique'`



## When to use
`web_search` routes to the SearXNG plugin and normally works. But it can occasionally return an **empty `results` array inside a successful `success: true` payload** (no error, just zero hits) — usually when SearXNG is degraded or the query phrasing trips it. When that happens and you still need live web discovery, fall back to a direct fetch of the DuckDuckGo HTML endpoint, which returns parseable result links without an API key or CAPTCHA.

## Method
Fetch `https://html.duckduckgo.com/html/?q=<URL-encoded query>` and parse the `class="result__a"` anchors. On this profile `execute_code` is blocked in cron mode, so run the fetch from a `terminal` Python script (write with `write_file`, then `python3` it) rather than inline.

```python
import urllib.request, urllib.parse, re, ssl
from html import unescape
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
q = urllib.parse.quote("Honolulu Oahu events August 2026 festival")
html = urllib.request.urlopen(
    urllib.request.Request(f"https://html.duckduckgo.com/html/?q={q}", headers={'User-Agent': UA}),
    timeout=20, context=ctx).read().decode('utf-8','ignore')
for m in re.finditer(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html, re.S):
    link = m.group(1)
    link = urllib.parse.unquote(link.split('uddg=')[-1].split('&')[0]) if 'uddg=' in link else link
    print(re.sub(r'<[^>]+>','',m.group(2)).strip()[:90], '||', link)
```

## Notes
- The `uddg=` wrapper is DDG's redirector; strip it to get the real URL.
- For reading a specific result page, fetch it directly with `urllib` and strip tags (`re.sub(r'<[^>]+>',' ', html)` + `unescape` + collapse whitespace). This is the manual stand-in for `web_extract` when that backend is unavailable.
- This is a discovery + read technique, not a replacement for Sift's source-reputation model. Still cross-check dates/venues against 2+ sources before treating them as facts.
- Do NOT generalize "web_search is broken" from one empty payload — it's usually transient; this is just the recovery path.
