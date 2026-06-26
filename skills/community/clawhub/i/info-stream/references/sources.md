# Information Source Reference

## Source Selection Criteria

Sources must be:
1. **Authoritative** — Original publisher, not reposted content
2. **Regularly updated** — At least weekly
3. **Machine-readable** — Accessible via web_fetch (not JS-rendered only)

## Source Tiers

### Tier 1: Official Technical Blogs (Highest Authority)

| Source | URL | Coverage | Update Freq |
|--------|-----|----------|-------------|
| WebKit Blog | webkit.org/blog | Safari/WebKit engine updates | Weekly |
| V8 Blog | v8.dev/blog | Chrome JS engine, performance | Weekly |
| Mozilla Hacks | hacks.mozilla.org | Firefox, web standards, Wasm | Weekly |
| Web.dev | web.dev | Google web dev guidance | Weekly |
| Chromium Blog | blog.chromium.org | Chrome browser updates | Weekly |
| Android Developers | android-developers.googleblog.com | Android WebView, mobile web | Weekly |
| Chromium Blog | blog.chromium.org | Chrome browser updates | Weekly |

### Tier 2: Technical Media (Curated Analysis)

| Source | URL | Coverage | Update Freq |
|--------|-----|----------|-------------|
| InfoQ | infoq.cn | Enterprise tech, QCon talks | Daily |
| 36氪 | 36kr.com | Chinese tech industry, funding | Daily |
| APPSO | apps.sina.cn | AI product news, tools | Daily |
| 机器之心 | jiqizhixin.com | AI deep coverage | Daily |
| 量子位 | qbitai.com | AI industry dynamics | Daily |
| 虎嗅 | huxiu.com | Tech industry analysis | Daily |
| 雷科技 | leikeji.com | Consumer electronics, tech | Daily |
| The Register | theregister.com | Tech industry news, analysis | Daily |
| Ars Technica | arstechnica.com | Deep tech coverage | Daily |

### Tier 3: Community Aggregators (Trend Signal)

| Source | URL | Coverage | Update Freq |
|--------|-----|----------|-------------|
| Hacker News | news.ycombinator.com | Global tech community | Real-time |
| Lobste.rs | lobste.rs | Curated tech links | Daily |
| Slashdot | slashdot.org | Tech news discussion | Daily |

## Source → Category Mapping

| Category | Primary Sources | Secondary Sources |
|----------|----------------|-------------------|
| Browser Engine | WebKit Blog, V8 Blog, Chromium Blog | Hacker News |
| Web Standards | Web.dev, Mozilla Hacks, WHATWG | Hacker News |
| Firefox | Mozilla Hacks, Mozilla Blog | Hacker News |
| AI & Browser | InfoQ, 36氪, Hacker News | WebKit Blog, V8 Blog |
| Mobile/Android | Android Developers Blog | InfoQ |
| Regional Tech | 36氪, InfoQ | — |

## Anti-JS-Rendered Sources

Some major Chinese tech sites (机器之心, 部分36kr pages) are JS-rendered and cannot be fetched with simple HTTP requests. For these:

1. Try RSS feed if available
2. Use Tavily API which handles JS rendering
3. Skip if both fail — don't waste time

## Source Health Check

Periodically verify sources are still active:
- Check last post date (flag if >30 days old)
- Verify URL still resolves
- Check for domain changes or redirects
