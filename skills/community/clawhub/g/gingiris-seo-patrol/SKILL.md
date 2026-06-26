---
name: gingiris-seo-patrol
description: |
  🇺🇸 SEO Patrol — Daily site health monitor & content decay tracker. Automated SEO monitoring: detect ranking drops, content decay, broken links, indexing issues, and Core Web Vitals regressions. IndexNow auto-push on content updates, competitor rank change alerts, and weekly SEO report generation. Built for SaaS teams without full-time SEO.

  🇨🇳 SEO 巡检 — 日常站点健康监控与内容衰退追踪器。自动化 SEO 监控：排名下降检测、内容衰退、死链、索引问题、Core Web Vitals 退化。IndexNow 自动推送、竞品排名变化预警、周度 SEO 报告。

  🇯🇵 SEOパトロール — 日次サイト健全性モニター＆コンテンツ劣化トラッカー。自動SEO監視：ランキング低下、コンテンツ劣化、リンク切れ、インデックス問題検出。IndexNow自動プッシュ、競合ランク変動アラート。

  🇰🇷 SEO 순찰 — 일일 사이트 건강 모니터 및 콘텐츠 감쇠 추적기. 자동화된 SEO 모니터링: 순위 하락, 콘텐츠 감쇠, 깨진 링크, 인덱싱 문제 감지. IndexNow 자동 푸시, 경쟁사 순위 변화 알림.

  Triggers: "SEO monitoring" | "SEO audit" | "site health" | "content decay" | "ranking drop" | "broken links" | "Core Web Vitals" | "IndexNow push" | "SEO report" | "SEO 监控" | "SEO 巡检" | "排名下降"
---

# SEO Patrol — Daily Site Health Monitor

> Automated SEO monitoring for teams who can't afford (or don't need) a full-time SEO specialist.

---

## What This Does

Continuous SEO health monitoring with automated alerts and fixes:

1. **Detect** — Find problems before they impact rankings
2. **Alert** — Prioritized notifications on critical issues
3. **Fix** — Auto-generate fix scripts or push changes via IndexNow
4. **Report** — Weekly summary for stakeholders

## Monitoring Checklist

### Daily Checks

| Check | What It Detects | Auto-Fix Available |
|-------|-----------------|-------------------|
| Sitemap validation | Missing/broken URLs in sitemap | ✅ Regenerate |
| robots.txt changes | Accidental blocks | ⚠️ Alert only |
| IndexNow push | New/updated content not pushed | ✅ Auto-push |
| 404 monitoring | Pages returning errors | ⚠️ Redirect suggestions |
| SSL certificate | Expiry within 30 days | ⚠️ Alert |

### Weekly Checks

| Check | What It Detects | Action |
|-------|-----------------|--------|
| Content freshness | Posts older than 6 months with declining traffic | Refresh list |
| Internal link audit | Orphan pages, broken internal links | Fix map |
| Core Web Vitals | LCP/CLS/INP regressions | Performance report |
| Schema validation | Broken or outdated structured data | Fix snippets |
| Competitor rank shifts | Keywords where competitors moved ±3 positions | Strategy update |

### Monthly Checks

| Check | What It Detects | Action |
|-------|-----------------|--------|
| Keyword cannibalization | Multiple pages targeting same keyword | Consolidation plan |
| Backlink profile | Lost links, toxic links | Outreach/disavow list |
| Content gap analysis | New competitor content you should match | Content calendar |
| AI citation check | Changes in AI engine citation frequency | GEO optimization |

## Content Decay Detection

Content decay = pages that once ranked well but are losing positions.

**Detection Signal:**
```
IF page_traffic(current_month) < page_traffic(3_months_ago) * 0.7
AND page_age > 6 months
THEN flag for refresh
```

**Refresh Priorities:**
| Priority | Condition | Action |
|----------|-----------|--------|
| P0 | Top 10 page dropped to page 2+ | Immediate update |
| P1 | Conversion page lost 30%+ traffic | Update within 1 week |
| P2 | Blog post declined 50%+ | Schedule for content refresh |
| P3 | Low-traffic page declining | Batch update monthly |

**Content Refresh Checklist:**
- [ ] Update title with current year
- [ ] Refresh statistics and data points
- [ ] Add new sections for recent developments
- [ ] Update screenshots/images
- [ ] Check and fix broken links
- [ ] Update FAQ with new questions
- [ ] Push via IndexNow after update

## IndexNow Auto-Push Setup

```javascript
// Trigger IndexNow push on any content change
// Works with: Next.js, WordPress, Hugo, Gatsby

const pushToIndexNow = async (urls) => {
  await fetch('https://api.indexnow.org/indexnow', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      host: 'yoursite.com',
      key: 'your-indexnow-key',
      urlList: urls
    })
  });
};
```

## Weekly Report Template

```markdown
# SEO Patrol Weekly Report — [Date]

## Summary
- Pages monitored: [N]
- Issues found: [N] (🔴 Critical: [N], 🟡 Warning: [N])
- Auto-fixed: [N]
- Requires attention: [N]

## Critical Issues
1. [Issue description] → [Recommended fix]

## Content Decay Alerts
| Page | Traffic Change | Current Rank | Action |
|------|---------------|--------------|--------|

## Competitor Movements
| Keyword | Our Position | Change | Competitor Action |
|---------|-------------|--------|-------------------|

## This Week's Wins
- [Positive ranking changes]
- [New indexed pages]

## Recommendations
1. [Priority action item]
```

## Related Skills

- [gingiris-seo-geo](https://clawhub.ai/skills/gingiris-seo-geo) — Full SEO & GEO strategy
- [gingiris-geo-audit](https://clawhub.ai/skills/gingiris-geo-audit) — One-time AI visibility audit
- [gingiris-blog-writer](https://clawhub.ai/skills/gingiris-blog-writer) — Content refresh/creation


---

## 🔗 About the Author

**Iris Wei** — Growth consultant for 150+ AI startups. Ex-COO at AFFiNE (69K GitHub stars).

- 🐦 Twitter: [@WeiYipei](https://twitter.com/WeiYipei) — Daily growth tactics
- 💬 Consulting: [@Iris_carrot on Telegram](https://t.me/Iris_carrot)
- 🛒 Premium Bundle (all 5 playbooks + templates): [Get on Gumroad ($249)](https://gingiris.gumroad.com/l/gingiris-complete-global-launch-bundle)
- 📚 40+ Free Playbooks: [gingiris.tools/skills](https://gingiris.tools/skills/)
