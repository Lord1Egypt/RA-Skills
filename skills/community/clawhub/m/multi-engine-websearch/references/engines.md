# Engine Notes & Troubleshooting

## Engine Reliability (as of 2026)

| Engine | Reliability | Bot Detection | Best For |
|---|---|---|---|
| DuckDuckGo | ⭐⭐⭐⭐⭐ | Very Low | General, privacy |
| Bing | ⭐⭐⭐⭐ | Low | News, recent |
| Brave | ⭐⭐⭐⭐ | Low | Independent results |
| Mojeek | ⭐⭐⭐⭐ | Very Low | Unbiased index |
| Yahoo | ⭐⭐⭐ | Medium | General |
| Startpage | ⭐⭐⭐ | Medium | Google results + privacy |
| Yandex | ⭐⭐⭐ | Medium | European/Russian |
| Google | ⭐⭐ | High | Best quality (when works) |
| Ask | ⭐⭐ | Medium | Question queries |
| Baidu | ⭐⭐ | Medium | Chinese content |

## If Google Blocks

Google aggressively blocks scrapers. If results are empty from Google, use:
```bash
python3 search.py "query" --engines duckduckgo,bing,brave,startpage
```
Startpage proxies Google results with privacy — use it as a Google fallback.

## Rate Limiting

If you run many searches quickly, some engines may temporarily block you.
Wait 30-60 seconds between heavy search sessions.

## Ranking Logic

Results are ranked by cross-engine frequency:
- A result appearing in 5 engines scores higher than one appearing in 1
- This filters spam/SEO-gamed results naturally
- First-party, authoritative sources tend to rank higher
