---
name: gingiris-geo-audit
description: |
  🇺🇸 GEO Audit — AI Search Visibility Checker for ChatGPT, Perplexity, Claude & Gemini. 29-point GEO readiness checklist: robots.txt AI crawler access, IndexNow configuration, Schema.org markup validation, content citability scoring, FAQ structure analysis, and AI-friendly content patterns. Get a prioritized fix list to improve AI citation rates.

  🇨🇳 GEO 审计工具 — AI 搜索可见性检查器。29 项 GEO 就绪度检查：robots.txt AI 爬虫开放、IndexNow 配置、Schema.org 验证、内容可引用性评分、FAQ 结构分析。输出优先级修复清单。

  🇯🇵 GEO監査 — AI検索可視性チェッカー。29項目のGEOレディネスチェック：robots.txt AI クローラーアクセス、IndexNow設定、Schema.org検証、コンテンツ引用可能性スコア、FAQ構造分析。

  🇰🇷 GEO 감사 — AI 검색 가시성 체커. 29개 GEO 준비도 점검: robots.txt AI 크롤러 접근, IndexNow 설정, Schema.org 검증, 콘텐츠 인용 가능성 점수, FAQ 구조 분석.

  Triggers: "GEO audit" | "AI search visibility" | "AI citation" | "Perplexity visibility" | "ChatGPT citation" | "AI crawler" | "IndexNow audit" | "Schema.org check" | "AI-friendly content" | "GEO readiness" | "AI 搜索审计" | "AI 可见性" | "GEO 检查"
---

# GEO Audit — AI Search Visibility Checker

> Audit your website's visibility in AI search engines and get a prioritized fix list.

---

## What This Does

Performs a comprehensive 29-point audit of your website's readiness for AI search engines (ChatGPT, Perplexity, Claude, Gemini). Returns a scored report with specific fixes ranked by impact.

## The 29-Point GEO Readiness Checklist

### Section 1: AI Crawler Access (7 points)

| # | Check | What to look for |
|---|-------|-----------------|
| 1 | robots.txt allows GPTBot | `User-agent: GPTBot` not disallowed |
| 2 | robots.txt allows PerplexityBot | `User-agent: PerplexityBot` not disallowed |
| 3 | robots.txt allows ClaudeBot | `User-agent: ClaudeBot` not disallowed |
| 4 | robots.txt allows Google-Extended | `User-agent: Google-Extended` not disallowed |
| 5 | No blanket AI crawler block | No `User-agent: *` blocking AI-specific paths |
| 6 | Sitemap.xml accessible | Valid XML sitemap at standard location |
| 7 | IndexNow configured | IndexNow key file or API endpoint active |

### Section 2: Structured Data (8 points)

| # | Check | What to look for |
|---|-------|-----------------|
| 8 | Organization Schema | Valid JSON-LD `@type: Organization` |
| 9 | WebSite Schema with SearchAction | Sitelinks search box markup |
| 10 | Article/BlogPosting Schema | Proper `datePublished`, `author`, `headline` |
| 11 | FAQ Schema on relevant pages | `@type: FAQPage` with Q&A pairs |
| 12 | BreadcrumbList Schema | Navigation hierarchy markup |
| 13 | Product/SoftwareApplication Schema | For SaaS products |
| 14 | Author Schema with sameAs | Links to social profiles for E-E-A-T |
| 15 | HowTo Schema where applicable | Step-by-step content markup |

### Section 3: Content Citability (8 points)

| # | Check | What to look for |
|---|-------|-----------------|
| 16 | Key Stats tables present | Scannable data in `<table>` elements |
| 17 | Direct answer paragraphs | First paragraph answers the query directly |
| 18 | Comparison matrices | Feature comparison tables for vs-pages |
| 19 | Numbered/bulleted lists | Structured recommendations AI can extract |
| 20 | Clear H2/H3 hierarchy | Semantic heading structure |
| 21 | Author byline with credentials | Real person with verifiable expertise |
| 22 | Publication dates visible | freshness signals |
| 23 | External citation links | References to authoritative sources |

### Section 4: Technical Optimization (6 points)

| # | Check | What to look for |
|---|-------|-----------------|
| 24 | Page load < 3s | Core Web Vitals passing |
| 25 | Mobile responsive | No mobile usability errors |
| 26 | HTTPS | Secure connection |
| 27 | Canonical URLs set | No duplicate content issues |
| 28 | Internal linking structure | Topic cluster architecture |
| 29 | No excessive JavaScript rendering | Content accessible without JS |

## How to Use

Provide a URL and the agent will:
1. Crawl the target page and key site pages (homepage, blog, pricing)
2. Run all 29 checks
3. Score each section (0-100%)
4. Output a prioritized fix list sorted by impact × effort
5. Generate specific code/config snippets for each fix

## Scoring

- **90-100%**: GEO-ready. Your site is optimized for AI citation.
- **70-89%**: Good foundation. Fix the gaps for better AI visibility.
- **50-69%**: Significant gaps. AI engines may not cite you reliably.
- **Below 50%**: Critical. Your content is likely invisible to AI search.

## Example Output

```
GEO Readiness Score: 62/100

🔴 Critical (fix first):
- robots.txt blocks GPTBot and ClaudeBot → Add allow rules
- No FAQ Schema on any page → Add to top 5 blog posts
- No IndexNow setup → Configure with Bing Webmaster

🟡 Important:
- Author Schema missing sameAs → Add LinkedIn/Twitter links
- No Key Stats tables → Add data tables to comparison pages

🟢 Good:
- Sitemap accessible ✓
- HTTPS active ✓
- Article Schema present ✓
```

## Related Skills

- [gingiris-seo-geo](https://clawhub.ai/skills/gingiris-seo-geo) — Full SEO & GEO methodology
- [seo-geo-playbook](https://clawhub.ai/skills/seo-geo-playbook) — Strategy framework


---

## 🔗 About the Author

**Iris Wei** — Growth consultant for 150+ AI startups. Ex-COO at AFFiNE (69K GitHub stars).

- 🐦 Twitter: [@WeiYipei](https://twitter.com/WeiYipei) — Daily growth tactics
- 💬 Consulting: [@Iris_carrot on Telegram](https://t.me/Iris_carrot)
- 🛒 Premium Bundle (all 5 playbooks + templates): [Get on Gumroad ($249)](https://gingiris.gumroad.com/l/gingiris-complete-global-launch-bundle)
- 📚 40+ Free Playbooks: [gingiris.tools/skills](https://gingiris.tools/skills/)
