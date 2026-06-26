# 🔍 GitHub Discoverability & SEO Plan

> **Goal**: Make `Mck-ppt-design-skill` findable via GitHub search and Google for queries like:
> "mckinsey ppt template", "AI presentation generator python", "consulting slide design skill", etc.

---

## ✅ Done — README Bilingual Rewrite

**Problem**: GitHub search weighs English README content heavily. Our all-Chinese README was invisible to English queries — the #1 issue.

**Solution**: README.md rewritten as **English-first** with Chinese in `<details>` collapse:
- All section headings, descriptions, and table contents now in English
- Added keyword-rich paragraph in Overview: "McKinsey PowerPoint template, consulting slide design, AI presentation generator, python-pptx automation..."
- Chinese documentation preserved in collapsible `<details>` block — no information lost
- AI agent compatibility table added (Claude, Cursor, GPT, Codebuddy)
- Stars badge added for social proof

---

## 📋 Action Items — Manual Steps Required

### 1️⃣ GitHub Repository Settings (5 min) ⭐ HIGHEST PRIORITY

Go to: **github.com/likaku/Mck-ppt-design-skill → Settings (gear icon on About section)**

#### Description (one line)
```
McKinsey-style PowerPoint design system for AI agents. 70 layout patterns, flat design, python-pptx. 麦肯锡风格PPT设计系统。
```
> ⚠️ GitHub indexes the repo description very heavily — this single line matters more than the entire README for search ranking.

#### Topics (tags)
Add ALL of these topics (click "Manage topics"):
```
mckinsey
powerpoint
pptx
python-pptx
presentation
slide-design
consulting
ai-skill
claude
cursor
pitch-deck
business-presentation
flat-design
data-visualization
chinese
ppt-template
ppt-generator
automation
design-system
```

> **Why these matter**: GitHub Topics are the primary mechanism for topic-based discovery. Someone browsing `github.com/topics/powerpoint` or `github.com/topics/mckinsey` will find you. Each topic also creates a backlink.

#### Website URL
```
https://github.com/likaku/Mck-ppt-design-skill
```
> Or if you have a demo site / blog post, use that instead.

---

### 2️⃣ Rename Repository (Optional but HIGH IMPACT)

**Current**: `Mck-ppt-design-skill`
**Recommended**: `mckinsey-ppt-design-skill`

**Why**:
- GitHub search does NOT do abbreviation expansion — "mckinsey" won't match "Mck"
- The query "mckinsey ppt" is 10x more common than "mck ppt"
- GitHub auto-redirects the old URL, so all existing links continue to work
- Git clone URLs also redirect — zero breakage

**How**: Settings → General → Repository name → `mckinsey-ppt-design-skill` → Rename

> If you want to keep the short name, add "mckinsey" to Topics instead (already listed above). But renaming is the single highest-impact change.

---

### 3️⃣ Google Search Console — Force Indexing (15 min)

Google's crawler visits small repos infrequently. Force it:

1. Go to [Google Search Console](https://search.google.com/search-console)
2. Add property: `https://github.com/likaku/Mck-ppt-design-skill`
   - Use "URL Prefix" method
   - Verify via "HTML tag" or "Google Analytics" (if applicable to your GitHub Pages)
3. **URL Inspection** → paste the repo URL → **Request Indexing**
4. Also request indexing for:
   - `https://github.com/likaku/Mck-ppt-design-skill/blob/main/README.md`
   - `https://github.com/likaku/Mck-ppt-design-skill/blob/main/SKILL.md`

> **Note**: Google can only index public pages. GitHub repos are public, so this works. Re-index after each major update.

#### Alternative: Google Indexing Ping

If Search Console verification is cumbersome, simply ping Google with:
```bash
curl "https://www.google.com/ping?sitemap=https://github.com/likaku/Mck-ppt-design-skill"
```

---

### 4️⃣ Create GitHub Pages Site (30 min, MEDIUM PRIORITY)

A GitHub Pages site gives Google a proper website to index (instead of relying on GitHub's own pages):

1. Settings → Pages → Source: "Deploy from a branch" → `main` / `docs/`
2. Create `docs/index.html` — a simple landing page with all keywords
3. Google indexes `.github.io` sites much more aggressively than raw repo pages

> This creates `likaku.github.io/Mck-ppt-design-skill/` — a fully crawlable website.

---

### 5️⃣ External Backlinks (Ongoing, HIGH IMPACT)

Google ranks pages by incoming links. Every external mention = +1 signal.

#### Quick wins:
| Platform | Action | Est. Time |
|----------|--------|-----------|
| **Hacker News** | Post "Show HN: McKinsey-style PPT design system for AI agents" | 5 min |
| **Reddit** | Post to r/Python, r/ChatGPT, r/artificial, r/consulting | 10 min |
| **Twitter/X** | Thread showing before/after slides with repo link | 15 min |
| **Dev.to** | Write "How I automated McKinsey-style presentations with AI" | 1 hr |
| **Medium** | Same article, different audience | 1 hr |
| **V2EX** | 发帖到 "分享发现" 或 "Python" 节点 | 5 min |
| **知乎** | 回答 "如何用 AI 生成专业 PPT" 类问题，附链接 | 15 min |
| **少数派** | 写一篇工具推荐文 | 30 min |
| **掘金** | 技术分享文章 | 30 min |
| **Product Hunt** | Launch as "McKinsey PPT Design Skill" | 15 min |
| **Awesome lists** | Submit PR to `awesome-python-pptx`, `awesome-claude`, `awesome-ai-tools` | 15 min |

#### Blog post template:
```markdown
Title: "I Built an AI Skill That Generates McKinsey-Style Presentations — Here's How"

- Problem: AI-generated PPTs look amateur
- Solution: Encoded McKinsey's design specification into a 268KB skill document
- Demo: Show 6 sample slides
- How it works: python-pptx + design rules + 70 layouts
- Link: github.com/likaku/Mck-ppt-design-skill
```

---

### 6️⃣ GitHub Releases (5 min)

Create a proper GitHub Release for each version:
1. Go to Releases → Draft New Release
2. Tag: `v1.10.3`
3. Title: `v1.10.3 — Title Line Spacing Optimization`
4. Body: Copy from CHANGELOG.md
5. Check "Set as the latest release"

> GitHub Releases are separately indexed by Google and show up in search results with rich snippets.

---

### 7️⃣ Add `awesome-` List Entries

Submit PRs to these curated lists:

- [`awesome-python`](https://github.com/vinta/awesome-python) — under Presentation/Document Generation
- [`awesome-ai-tools`](https://github.com/mahseema/awesome-ai-tools) — under Productivity
- Any `awesome-claude` or `awesome-cursor` lists that exist
- [`awesome-pptx`](https://github.com/search?q=awesome+pptx) — search for relevant lists

Each PR = a permanent backlink from a high-authority GitHub page.

---

## 📊 Expected Impact Timeline

| Timeframe | Expected Result |
|-----------|----------------|
| **Day 1** | README rewrite live ✅; Topics + Description set |
| **Week 1** | GitHub search starts returning repo for "mckinsey powerpoint python" |
| **Week 2** | Google re-indexes with new English content |
| **Month 1** | If repo renamed + blog posts published → appears in Google top 20 for "mckinsey ppt template python" |
| **Month 2-3** | Backlinks from blog posts + awesome lists → Google top 10 for niche queries |

---

## 🧪 How to Measure

1. **GitHub Traffic**: Insights → Traffic → check "Referring sites" and "Popular content"
2. **Google Search**: `site:github.com/likaku/Mck-ppt-design-skill` — see what's indexed
3. **Test queries** (incognito mode):
   - `mckinsey ppt python github`
   - `ai powerpoint generator skill`
   - `python-pptx mckinsey template`
   - `consulting slide design automation`

---

*Plan created 2026-03-18. Delete this file before committing if you don't want it in the repo.*
