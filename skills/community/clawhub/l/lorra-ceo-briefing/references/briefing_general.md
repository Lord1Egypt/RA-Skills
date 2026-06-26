# 🌄 Daily Morning Briefing Instructions (CEO Edition)

> **INPUT**: JSON object containing `global_scan`, `hn_ai`, `github_trending`, `insights` sections.
> **OUTPUT**: A single professional Markdown briefing report.

---

## ⚠️ Anti-Laziness Protocol (STRICT)

1. **Volume Target**: Aim for **18-22 total items**, NEVER invent items.
2. **No Aggregation**: One news item = One section. Never combine.
3. **Real Items Only**: Only use items that exist in the JSON input.

---

## 📋 Report Structure (3 Parts)

---

### Part 0: 📌 今日要点 (Executive Summary)

> **MANDATORY — Top of Report**
> Write 3-5 bullet points summarizing the most important themes TODAY.
> These are NOT about individual news items — they are **thematic conclusions**.
> Format: `- [主题]: 一句话判断 + 背后的原因/数据支撑`

**Example**:
```
- [AI 模型竞争]: 开源模型能力逼近闭源，DeepSeek/R1 成为开发者新基准
- [开源生态]: Rust 在系统级项目占比突破 30%，内存安全成主流选择
- [地缘政治]: 欧洲 tech 就业市场收缩，亚太高增长
```

---

### Part 1: 🌍 全网要闻 (Global Highlights)

**Goal**: Cover the 8-12 most important news items, grouped by **theme**, not by source rank.

**Grouping Themes** (pick 3-5 that fit today's news):
- AI & 模型进展 (AI & Model Progress)
- 产品与发布 (Products & Launches)
- 开源与工具 (Open Source & Tools)
- 市场与资本 (Market & Funding)
- 政策与监管 (Policy & Regulation)
- **🗞️ 社会与政治 (Society & Politics)** ← 强制包含！来自 Jacobin, Social Europe, China Digital Times 等左翼媒体源
- **🌍 中国观察 (China Watch)** ← 强制包含！来自 China Digital Times 等来源的中国社会内容

**Format per Theme**:
```markdown
#### 🤖 AI & 模型进展

##### [标题 (中文)](原始链接)
- **来源**: 源名 | **时间**: X小时前
- **Summary**: 一句话说明这是什么。
- **Impact**: 💡 为什么重要 + 接下来会怎样。（不是技术细节，是商业/行业影响）
```

**Rules**:
- ❌ 删除热度数字（不要"🔥 198 replies"、"热度: High"）
- ✅ 改用文字影响级别："重磅 / 值得关注 / 小进展"
- ✅ 每条 Deep Dive 结尾加 `[HN讨论]` 链接（如果有）
- ✅ 每个主题至少 1 条，最多 4 条

---

### Part 2: 🦄 AI 深度读 (AI Deep Dive)

**Goal**: 5-8 items focused on **technical AI/LLM discussions**.

**Format**:
```markdown
##### [标题](链接)
- **来源**: Hacker News | **时间**: X小时前
- **Summary**: 一句话技术摘要。
- **Technical Insight**: 💡 技术突破点 / 争议点 / 为什么开发者应该关注。
```

**Selection**: Pick items with technical depth — "Show HN", launches, technical analysis, model comparisons.

---

### Part 3: 🐙 开源精选 (Open Source Spotlight)

**Goal**: 6-10 most interesting GitHub projects, **prioritize new tools over established ones**.

**Format**:
```markdown
##### [Repo/项目名](链接)
- **语言**: Python | **星标**: 🌟 N
- **解决的问题**: 一句话。
- **为什么值得关注**: 💡 竞品对比 / 适用场景 / #标签
```

---

### Part 4: 🗞️ 社会与政治 (Society & Politics)

**Goal**: 3-5 items from left-wing / independent media sources.
**Sources**: Jacobin, Social Europe, China Digital Times, The Next Recession.

> **⚠️ MANDATORY**: If any items from these sources appear in `global_scan`, you **MUST** include at least 2 of them here, even if it exceeds your 18-22 item target.

**Format**:
```markdown
##### [标题](链接)
- **来源**: 源名 | **时间**: X小时前
- **Summary**: 一句话说明。
- **Why It Matters**: 💡 这件事反映了什么趋势/矛盾/值得关注的信号。
```

---

## 🎨 Tone & Style

| ✅ Do | ❌ Don't |
|-------|---------|
| 简洁有力的中文 | 翻译腔 / 废话 |
| "这意味着..." | "这篇报道讲述了..." |
| 影响 + 预判 | 单纯描述 |
| 按主题分组 | 排行榜式罗列 |
| 真实数据说话 | 夸大其词 |

**Style**: Professional, Insightful, "Tech Magazine" vibe — like a smart friend who reads everything and tells you only what matters.

**Language**: Simplified Chinese throughout.

---

## ❓ 读后思考题 (Post-Briefing Questions)

> **MANDATORY — After writing the full report, add 1-3 reflective questions at the bottom of the briefing.**

These questions should:
- Push the reader to connect multiple news items across sections
- Be **provocative**, not factual-recall questions
- Be answerable but not obvious

**Format**:
```markdown
---

## 💭 读后思考

1. [一个问题，把今天最矛盾的两件事放在一起问]
2. [一个预测性问题，让读者赌一个判断]
3. [一个行动性问题，引导读者决定下一步]
```

**Examples**:
- "如果 AI 编程真的无法承担长期任务，那为什么 Claude Code 的生态还在爆发式增长？"
- "开源模型占领 OpenRouter 头部位置，这对 Anthropic/OpenAI 的定价策略意味着什么？"
- "Habermas 去世和美俄制裁松动之间，有没有共同的叙事逻辑？"
