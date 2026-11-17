# Quick VPS Search Cheat Sheet

When running from VPS/cloud environments where browser-based search is CAPTCHA-blocked.

## Primary — SearXNG (localhost:8888, no CAPTCHA)

```bash
curl -s "http://localhost:8888/search?q=QUERY&format=json" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for r in d.get('results',[])[:10]:
    print(r['title']); print(r['url']); print(r['content'][:200]); print()
"
```

## Fallback — CSAPI (check quota first)

```bash
python3 ~/.hermes/skills/ocas-sift/scripts/csapi_quota.py check
```

## Anti-bot fetch fallback — donsetch

When `sift.fetch` returns bot-wall / 403 / empty / CAPTCHA:

```bash
/usr/local/bin/donsetch fetch <url>
```

Exit codes: `0` success · `1` permanent error · `2` transient (retry) · `3` walled (escalate to `sift.webwright`).
