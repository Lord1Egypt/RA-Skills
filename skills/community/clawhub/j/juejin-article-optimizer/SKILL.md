---
name: Juejin Article Optimizer
slug: juejin-article-optimizer
description: Optimize technical articles for the Juejin community: improve rankings, readability, and developer engagement.
tags: [juejin, article, optimization, seo, writing, dev-community, china, technical-blog]
version: 1.0.0
license: MIT-0
---

# Juejin Article Optimizer (掘金技术文章优化助手)

Take your technical draft from "just another post" to a high-ranking, high-engagement Juejin article. Analyze structure, readability, and SEO against platform best practices — then get a fully optimized version ready to publish.

## Core Capabilities

- **Article diagnostic scoring**: Rate your draft across 6 dimensions (title, structure, code/text ratio, readability, SEO, engagement hooks) with specific improvement targets
- **Title optimization**: Generate 3 high-CTR title variants based on Juejin's top-performing title patterns
- **Structure reorganization**: Recommend optimal heading hierarchy, paragraph length, and code/text balance for Juejin's mobile-first reading experience
- **SEO enhancement**: Keyword density analysis, internal link suggestions, tag optimization, and TOC anchor generation
- **Code block improvement**: Annotate code blocks with explanatory comments, add syntax highlighting language tags, suggest split/merge for readability
- **Visual suggestion engine**: Identify which sections would benefit from diagrams, screenshots, or GIFs — with placement recommendations
- **Engagement boost**: Add discussion-bait questions, practical takeaways, and community interaction hooks
- **Publishing optimization**: Tag strategy, best publish day/time, and cross-platform promotion snippets

## Workflow (8 Steps)

### Step 1: Article Ingestion
**Input**: User provides:
- **Article draft**: Markdown file, pasted text, or URL of existing Juejin article
- **Goal**: `optimize-new` (optimize before first publish) | `rescue-existing` (improve a low-performing published article) | `translate-adapt` (adapt English tech blog for Juejin)
- **Target audience** (optional): Beginner / Intermediate / Advanced

**Output**: Parsed article with structural metadata (word count, heading count, code block count, image count, reading time).

### Step 2: Diagnostic Scoring
**Input**: Parsed article.
**Action**: Score on 6 dimensions (1-10 scale):

| Dimension | What We Measure | Weight |
|-----------|----------------|--------|
| **Title Power** | CTR potential. Does it use Juejin-proven patterns (numbered lists, practical value, curiosity gap)? | 20% |
| **Structure** | Heading hierarchy, paragraph length, first-screen content value, section balance | 15% |
| **Code/Text Ratio** | Is there enough explanation around code? Standard: 60% text, 40% code. Too much code → low readability. | 15% |
| **Readability** | Sentence length, terminology explanation, Chinese readability score, mobile readability | 20% |
| **SEO & Discoverability** | Keyword density, tag relevance, title keyword placement, internal linking | 15% |
| **Engagement Design** | Discussion hooks, practical takeaways, call-to-action, comment-bait questions | 15% |

**Output**: Radar chart (text/Mermaid) + overall score + breakdown. Comparison to Juejin's top-article benchmarks.

### Step 3: Juejin Trend Analysis
**Input**: Article topic + Juejin category.
**Action**: Scrape Juejin's relevant category/channel for top-performing articles (last 30 days, >500 likes):
- Extract common title patterns (e.g., "一文搞懂...", "XXX最佳实践", "面试官问XXX")
- Analyze optimal article length (character count distribution of top articles)
- Code/text ratio benchmarks in the category
- Tag usage patterns (which tag combos get most exposure)
- Time-of-day posting patterns (extracted from publish times of trending articles)

**Output**: Category benchmark report with actionable patterns.

### Step 4: Gap Analysis
**Input**: Article diagnostic score + category benchmarks.
**Action**: Compare article metrics against category benchmarks:

| Dimension | Your Article | Category Average | Top 10% | Gap |
|-----------|-------------|------------------|---------|-----|
| Title Power | 5/10 | 6.5 | 8.2 | 🔴 -3.2 |
| Structure | 7/10 | 6.8 | 8.5 | ≈ |
| Code/Text Ratio | 55% code | 35% | 28% | 🔴 Too much code |
| Readability | 6/10 | 7.2 | 8.8 | 🟡 -2.8 |
| SEO | 4/10 | 6.0 | 8.0 | 🔴 -4.0 |
| Engagement | 3/10 | 5.5 | 7.5 | 🔴 -4.5 |

**Output**: Prioritized improvement list: "Top 3 fixes: 1. Add engagement hooks (gain +2.5) 2. Improve SEO (gain +2.5) 3. Optimize title (gain +2.0)."

### Step 5: Title Optimization
**Input**: Original title + category patterns.
**Action**: Generate 3 optimized title variants using Juejin-proven patterns:
1. **Numbered List Pattern**: "XXX 的 5 个最佳实践，第 3 个最容易被忽略"
2. **Practical Value Pattern**: "用了 XXX 这么久，90% 的人不知道这个技巧"
3. **Curiosity Gap Pattern**: "为什么你的 XXX 总是慢 3 倍？一个被忽视的配置"

**Output**: 3 title variants with CTR potential scores and rationale. User selects or combines.

### Step 6: Content Optimization
**Input**: Original article + gap analysis + selected title.
**Action**: Apply optimizations:
- **Opening hook**: Rewrite first 3 paragraphs — start with problem statement, data point, or relatable scenario (not "本文介绍了...")
- **Structure adjustment**: Ensure H2 level is scannable (reader can understand the article by reading only H2s). Add a TOC at top for articles >2000 chars.
- **Code block enrichment**: Add a "What this code does" comment before every code block. Add expected output example. Suggest language tag if missing.
- **Paragraph trimming**: Max 4 sentences per paragraph. Break walls of text. Add bold highlights to key sentences.
- **Visual insertion points**: Mark `[💡 建议配图: XXX架构图]` at 3-5 strategic locations.
- **Practical takeaways**: End each major section with "💡 要点总结" (1-2 sentences).

**Output**: Optimized markdown article. Diff available on request.

### Step 7: SEO & Discoverability Enhancement
**Input**: Optimized article.
**Action**:
- **Keyword optimization**: Identify primary keyword (1) and secondary keywords (3-5). Ensure primary keyword appears in title, first paragraph, at least 2 H2s, and naturally 5-8 times in body.
- **Tag strategy**: Recommend 5 tags: 1 primary category tag + 2-3 topic tags + 1 traffic tag. Explain why each tag is chosen.
- **TOC generation**: Auto-generate linked table of contents for articles >5 H2 sections.
- **Internal linking**: Suggest 2-3 places to link to your own previous articles (if applicable).
- **Description/summary**: Write a 2-3 sentence article description for the Juejin feed preview.

**Output**: SEO optimization report + applied changes.

### Step 8: Publishing Strategy
**Input**: Optimized article + category benchmarks.
**Action**: Generate publishing recommendations:
- **Best publish time**: Day of week + hour window based on category data (e.g., "周三 10:00–11:00 or 周四 14:00–15:00, 前端类文章最佳发布窗口")
- **Cross-promotion snippets**: 1 WeChat Moments share text, 1 tech community (V2EX/Zhihu) cross-post hook, 1 Twitter/X thread starter
- **First-hour engagement plan**: How to respond to first 5-10 comments to boost algorithm ranking (acknowledge, extend, ask follow-up)
- **Series potential**: If article is part of a broader topic, suggest a 3-article series plan to build follower momentum

**Output**: Publishing playbook with timeline + promotional copy.

## Sample Prompts

### Prompt 1: Pre-Publish Optimization
**User**: "我写了一篇关于Go并发编程的文章，帮我在发布前优化一下 [paste article]"
**Expected Output**: Diagnostic score → title variants ×3 → optimized article with improved structure, annotated code blocks, visual suggestions, SEO enhancements, and publishing strategy.

### Prompt 2: Low-Performing Article Rescue
**User**: "这篇文章在掘金只有200阅读，帮我诊断为什么，然后优化 [URL: juejin.cn/post/...]"
**Expected Output**: Diagnostic report identifying specific issues (e.g., "标题缺少搜索关键词，首屏信息密度太低，代码块无注释") → optimized version with before/after comparison table → re-publishing strategy.

### Prompt 3: English-to-Juejin Adaptation
**User**: "这篇英文技术博客写的不错，帮我改写成适合掘金发布的中文版 [paste or URL]"
**Expected Output**: Localized article: not direct translation but culturally adapted — Chinese dev community references, relevant Chinese tech stack context, Juejin-appropriate humor/examples, SEO keywords in Chinese.

### Prompt 4: Article Series Planning
**User**: "我想写一个'微服务入门到实战'的系列，帮我规划前5篇的选题和结构"
**Expected Output**: 5-article series plan: title per article, key takeaways, progression logic (foundation → practice → optimization → pitfalls → advanced), cross-linking strategy, estimated publishing cadence.

### Prompt 5: Title A/B Test
**User**: "这几个标题哪个在掘金最可能火？1) Go并发编程入门 2) 用了3年Go，才知道goroutine可以这样用 3) Go并发：从理论到实战的5个关键技巧"
**Expected Output**: Per-title CTR potential analysis: pattern match, keyword power, emotion trigger, curiosity gap. Ranked recommendation with reasoning. "Title 2 has highest potential: curiosity gap + experience authority + practical value."

### Prompt 6: Full Audit & Rewrite
**User**: "把我最近的5篇文章都审计一遍，按优化优先级排序，然后从最差的那篇开始重写"
**Expected Output**: Audit report ranking all 5 by optimization potential (estimated score gain) → full rewrite of the weakest article with all optimizations applied.

## Real Task Examples

### Example 1: First-Time Juejin Author
**Scenario**: Senior developer writing first Juejin article, unfamiliar with platform norms.
**Input**: "写了篇微服务监控的文章，帮我看看在掘金能不能火 [paste draft: ~3000 chars, heavy code, light explanation]"
**Steps**:
1. Diagnostic: Title 4/10 (generic), Code/Text 65% code (too much), Engagement 2/10 (no hooks), Readability 5/10.
2. Category benchmark: Backend category top articles average 45% code ratio, 4000-8000 chars.
3. Gap: need +25% text, engagement hooks, better title, visual suggestions.
4. Title: Generate 3 variants → user picks "微服务监控踩坑实录：这5个指标救了我3次".
5. Optimize: restructure with problem-first opening, add "why this matters" before each code block, add practical takeaways, insert 4 visual suggestion markers.
6. SEO: tags (微服务, 监控, Prometheus, 后端, 架构), primary keyword "微服务监控".
**Output**: Optimized article (5200 chars, 42% code). Projected score improvement: 4.8/10 → 7.5/10. Publishing at Thursday 10:30.

### Example 2: Company Tech Blog Pipeline
**Scenario**: Company DevRel team needs to publish 4 articles/month on Juejin to build employer brand.
**Input**: "这是我们团队本月要发的4篇草稿，帮我统一优化，风格要专业但不枯燥 [upload: 4 drafts]"
**Steps**:
1. Per-article diagnostic scoring.
2. Cross-article consistency: ensure complementary topics, no overlap, coherent series if applicable.
3. Per-article optimization with shared tag strategy (build company tag presence).
4. Internal linking: cross-reference between articles where relevant.
5. Publishing calendar: stagger across 4 weeks with optimal days/times.
**Output**: 4 optimized articles + publishing calendar + engagement plan + team author bio templates.

### Example 3: Viral Article Reverse-Engineering
**Scenario**: User wants to understand why a competitor's article went viral and apply lessons.
**Input**: "这篇文章在掘金有5000赞，帮我分析它为什么火 [URL], 然后按同样的套路优化我的文章 [paste my draft]"
**Steps**:
1. Analyze viral article: title pattern (numbered list + practical value), structure (problem → why it happens → solution → code → results), engagement hooks (3 discussion questions, 2 relatable scenarios), length (6200 chars, 38% code).
2. Extract replicable patterns → apply to user's draft.
3. Optimize: adopt same structure pattern, similar hook placement, comparable length.
**Output**: "Viral pattern decoded: ① Hook with relatable pain point ② Show don't tell (benchmark data) ③ 'I wish I knew this earlier' framing. Applied to your article: [optimized version]. Estimated CTR uplift: +80%."

## Scripts

| Path | Description |
|------|-------------|
| `scripts/optimizer.sh` | Main CLI script — diagnose, title optimization, tags, publishing strategy |
| `schemas/input.schema.json` | JSON Schema for workflow input (title, task, tags) |
| `schemas/output.schema.json` | JSON Schema for workflow output (scores, variants, publishing) |
| `references/category_benchmarks.json` | Juejin category benchmarks for article patterns |

### CLI Usage

```bash
# Diagnose article title
bash scripts/optimizer.sh --title "Go并发编程入门" --task diagnose

# Generate optimized title variants
bash scripts/optimizer.sh --title "微服务监控实战" --task title

# Tag and SEO recommendations
bash scripts/optimizer.sh --title "Kubernetes教程" --task tags --tags "后端,Kubernetes"

# Publishing strategy
bash scripts/optimizer.sh --title "React性能优化指南" --task publish

# Full pipeline
bash scripts/optimizer.sh --title "Go并发编程入门" --task full --tags "后端,Go语言"
```

## 🚀 First-Success Path (3 Steps)

1. **Step 1**: Run `bash scripts/optimizer.sh --title "你的文章标题" --task diagnose`
2. **Step 2**: Review the diagnostic scores and run `bash scripts/optimizer.sh --title "你的文章标题" --task title` for title variants
3. **Step 3**: Run `bash scripts/optimizer.sh --title "你的文章标题" --task full --tags "标签"` to receive the complete optimization report within 30 seconds

```bash
# Quick start
bash scripts/optimizer.sh --title "Go并发编程入门" --task diagnose
```

## Boundary Conditions

| Condition | Behavior |
|-----------|----------|
| Article <500 characters | Flag as too short for Juejin (min 1000 chars recommended); suggest expanding |
| Article >15,000 characters | Warn: "Very long — consider splitting into 2-part series for better engagement" |
| Pure code dump (>80% code) | Flag: "This reads like a gist, not an article. Add explanations and context." |
| Non-technical content | Warn: "Juejin is a technical community. Entertainment/general content performs poorly." |
| Article already published | Offer "rescue" mode — analyze existing performance + suggest improvements for re-publish or next article |
| URL unreachable (Juejin blocks scrape) | Request user to paste article text manually |
| Category has <10 reference articles | Broaden to adjacent categories for pattern analysis |
| User requests guaranteed viral result | Redirect: "Optimization improves probability, not guarantees. Even top authors have articles that underperform." |

## Error Handling

| Error Code | Scenario | Handling |
|-----------|----------|----------|
| E-SCRAPE-BLOCKED | Juejin anti-scraping triggered | Use cached benchmark data; flag staleness; suggest manual category input |
| E-CATEGORY-UNKNOWN | Article topic doesn't match any Juejin category | Ask user to specify closest category; use general tech benchmark |
| E-LOW-DATA | Insufficient reference articles for pattern analysis | Broaden time range or adjacent categories; flag lower confidence |
| E-ARTICLE-UNREADABLE | Can't parse article format (corrupted markdown, special chars) | Offer plain text mode; warn formatting may be simplified |
| E-TITLE-REJECTED | All 3 title variants rejected by user | Generate 3 more with different patterns (try: controversy, question, how-to) |
| E-OVER-OPTIMIZATION | Too many optimization suggestions overwhelm user | Offer priority-ranked top-5 mode; defer others to "advanced optimization" |

## Security Requirements

- **Original content only**: The optimizer enhances YOUR content. It does not generate content that plagiarizes existing Juejin articles. If pattern analysis detects high similarity to a specific published article, flag it.
- **No automated posting**: This tool generates optimized drafts and publishing advice. It does not post to Juejin on the user's behalf. User controls all publishing decisions.
- **Article privacy**: Draft content processed in-session only. Not stored or used for any other purpose.
- **Juejin ToS compliance**: All scraping is read-only and rate-limited. Do not circumvent Juejin's anti-scraping measures.
- **Attribution integrity**: If the user's article references external sources, ensure proper attribution is preserved and enhanced.
- **Content safety**: Reject optimization requests for content that violates Chinese internet regulations or Juejin community guidelines.