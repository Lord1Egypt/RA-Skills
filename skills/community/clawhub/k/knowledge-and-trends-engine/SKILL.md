---
name: knowledge-and-trends-engine
description: >
  Knowledge accumulation and tech trend analysis engine.
  Periodically summarizes learned concepts from user interactions,
  parses content from videos/articles/images shared by user,
  researches latest tech/news trends, and self-iterates.
  Triggers: "summarize what we discussed", "learn from this article",
  "analyze this video", "what's new in tech", "create a knowledge summary",
  or periodic scheduled reviews.
version: 1.0.0
metadata:
  openclaw:
    emoji: "📡"
    homepage: https://clawhub.ai/BusTes01/knowledge-and-trends-engine
    models:
      - gpt-4
      - deepseek-v4-flash
      - gemini-2.0-flash
      - claude-4-opus
    requires:
      skills:
        - complex-memory-manager
        - self-iteration-engine
---

# 📡 Knowledge & Trends Engine

Knowledge accumulation and tech trend analysis engine. Periodically summarizes learned concepts from user interactions, parses content from shared videos/articles/images, researches latest tech/news trends, and self-iterates via the shared component skills.

## Core Workflows

### Workflow 1: Concept Summarization (On-demand)

User says: "summarize what we've discussed recently" or "帮我总结最近聊过的概念"

**Step 1: Gather Memory Sources**
- Read `memory/tier1-public/` for all skill stats and public knowledge entries
- Read `memory/concepts/` for concept files stored from previous sessions
- Read recent daily notes: `memory/YYYY-MM-DD.md` (last 7 days)

**Step 2: Identify Distinct Concepts**
Scan all sources and extract unique concepts. For each concept, determine:
- **Category**: AI/ML, Finance, Development, Tools, Business, Science, etc.
- **Maturity**: new / explored / mastered
- **Related concepts**: cross-links to other learned concepts
- **Source**: conversation, article, video, image, or self-discovered

**Step 3: Generate Summary**
```markdown
# 📡 Knowledge Summary · YYYY-MM-DD

## 🆕 New This Period
### Concept A
- Source: conversation about financial modeling
- Key points: {3-5 bullet points}
- Related: Concept B, Concept C
- Status: explored ✓

## 📚 Concepts in Progress
### Concept D
- Last discussed: YYYY-MM-DD
- Progress: understand basics, need deeper dive
- Suggested next: look into {related topic}

## 🏆 Mastered Concepts
### Concept E
- Sessions covered: 5
- Last reviewed: YYYY-MM-DD
- Confident: yes
```

**Step 4: Store**
Use `complex-memory-manager` to store the summary:
- T1: `memory/tier1-public/concepts-summary-YYYY-MM.md` (concept names, relationships, categories)
- T2: `memory/tier2-internal/concepts-detail-YYYY-MM.md` (detailed notes, sources, encrypted if personal)

### Workflow 2: Parse External Content (On-demand)

User shares content: "watch this video", "read this article", "analyze this image", "这个概念你记住"

**Step 1: Content Analysis**
- For **articles** (`web_fetch` URL): extract key concepts, arguments, data points
- For **videos** (if URL to YouTube/transcript): extract main thesis, examples, conclusions
- For **images**: describe visual content, extract any text, identify key concepts
- For **direct concept explanation**: parse the user's textual explanation

**Step 2: Concept Structuring**
For each extracted concept, create a structured note:
```yaml
# memory/concepts/<concept-slug>.md
concept:
  name: "<concept name>"
  category: "<category>"
  source:
    type: article | video | image | conversation
    url: "<source URL if applicable>"
    date: "<YYYY-MM-DD>"
  summary: "<2-3 sentence explanation>"
  key_points:
    - "<point 1>"
    - "<point 2>"
  related_concepts: ["<concept A>", "<concept B>"]
  practical_applications: "<how this can be used>"
```

**Step 3: Cross-Link**
- Check memory for existing related concepts
- Add links in both directions
- If concept already exists, merge/update rather than duplicate

### Workflow 3: Trend Research (Periodic / On-demand)

User says: "what's new in tech" or "调研最新的技术趋势"

**Step 1: Define Research Scope**
- If user specified: use those keywords
- If not: use recent concept categories from memory as seed topics
- Always include: AI/ML, developer tools, security, finance tech

**Step 2: Search & Gather**
- Use `web_search` with targeted queries for each scope
- Priority sources: tech blogs (TechCrunch, ArsTechnica), research papers (arXiv), release notes (GitHub), financial news (Bloomberg, Reuters)
- Limit to last 7 days of content unless user specifies otherwise

**Step 3: Trend Analysis**
For each trend found:
```yaml
trend:
  title: "<trend name>"
  category: "<category>"
  significance: high | medium | low
  description: "<1-2 sentence description>"
  impact: "<who/what this affects>"
  source: "<URL>"
  relation_to_existing: "<how this relates to known concepts>"
```

**Step 4: Learn & Store**
- Store each significant new concept using Workflow 2 format
- Update `memory/tier1-public/trends-DATE.md` with all findings
- Use `self-iteration-engine` to log the research activity

### Workflow 4: Periodic Self-Review (Cron-driven)

When triggered by schedule (default weekly):

1. **Review accumulated concepts** from `memory/concepts/`
2. **Run trend research** (Workflow 3) on categories where concepts are stored
3. **Generate combined summary** (Workflow 1) including new trends
4. **Identify knowledge gaps** — concepts mentioned in trends that have no existing entry
5. **Log iteration** via `self-iteration-engine`
6. **Propose learning topics** for next week based on gaps

## Memory Structure

```
memory/
├── tier1-public/
│   ├── concepts-summary-YYYY-MM.md     # Monthly concept overview (T1)
│   └── trends-YYYY-MM-DD.md            # Trend research results (T1)
├── tier2-internal/
│   └── concepts-detail-YYYY-MM.md      # Detailed encrypted notes (T2)
├── concepts/
│   ├── <concept-slug>.md               # Individual concept files
│   └── INDEX.md                        # Master index of all concepts
└── usage-logs/
    └── knowledge-and-trends-engine.md  # Delegated to self-iteration-engine
```

## Query Examples

```
"最近我们聊过什么来着？" → Workflow 1 (concept summarization)
"看看这篇https://...  帮我提炼核心概念" → Workflow 2 (content parse)
"最近AI领域有什么新动向" → Workflow 3 (trend research)
"定期总结" → Workflow 4 (periodic review)
"这个概念你记住" + explanation → Workflow 2, Step 2-3 (direct store)
```

---

# 📡 知识趋势引擎

知识积累与技术趋势分析引擎。定期总结与用户讨论过的概念，解析用户分享的视频/文章/图片内容，调研最新技术与新闻热点，并通过共享组件技能实现自迭代。

## 核心工作流

### 工作流1：概念总结（按需）

用户说："总结最近聊过的概念"

**第一步：收集记忆源**
- 读取 `memory/tier1-public/` 中的技能统计和公开知识
- 读取 `memory/concepts/` 中的概念文件
- 读取最近7天的每日笔记

**第二步：识别独立概念**
扫描所有源提取唯一概念，判断：类别、成熟度、关联概念、来源

**第三步：生成总结**
按以下结构输出：
- 🆕 本期新概念
- 📚 进行中的概念
- 🏆 已掌握的概念

**第四步：存储**
委托 `complex-memory-manager` 存储总结

### 工作流2：解析外部内容（按需）

用户分享内容时：文章URL、视频URL、图片、或直接概念解释

**第一步：内容分析**
- 文章 → `web_fetch` 提取关键概念、论据、数据
- 视频 → 如有文字稿则提取主旨、示例、结论
- 图片 → 描述视觉内容，提取文字，找出关键概念
- 直接解释 → 解析用户的文字说明

**第二步：概念结构化**
每个概念创建结构化笔记，包括名称、类别、来源、摘要、要点、关联概念、实际应用

**第三步：交叉链接**
检查已有概念，双向链接；若已存在则合并/更新而非重复

### 工作流3：趋势调研（定期/按需）

用户说："最近有什么技术热点"

**第一步：确定调研范围**
使用用户指定关键词或已有概念类别作为种子

**第二步：搜索收集**
`web_search` 定向搜索，优先来源：TechCrunch、ArsTechnica、arXiv、GitHub、Bloomberg、Reuters

**第三步：趋势分析**
对每个趋势记录：标题、类别、重要性、描述、影响、来源、与现有概念的关系

**第四步：学习与存储**
使用工作流2格式存储新概念，更新趋势文件

### 工作流4：定期自审（Cron驱动）

默认每周执行：
1. 审查 `memory/concepts/` 中的积累概念
2. 在有概念存储的类别上运行趋势调研
3. 生成包含新趋势的合并总结
4. 识别知识盲区
5. 通过 `self-iteration-engine` 记录迭代
6. 基于盲区提出下周学习主题

## 记忆结构

```
memory/
├── tier1-public/
│   ├── concepts-summary-YYYY-MM.md     # 月度概念概览（公开）
│   └── trends-YYYY-MM-DD.md            # 趋势调研结果（公开）
├── tier2-internal/
│   └── concepts-detail-YYYY-MM.md      # 详细加密笔记（内部）
├── concepts/
│   ├── <概念slug>.md                    # 独立概念文件
│   └── INDEX.md                        # 概念总索引
└── usage-logs/
    └── knowledge-and-trends-engine.md  # 由self-iteration-engine管理
```

## 查询示例

```
"最近我们聊过什么来着？" → 工作流1（概念总结）
"看看这篇https://...  帮我提炼核心概念" → 工作流2（内容解析）
"最近AI领域有什么新动向" → 工作流3（趋势调研）
"定期总结" → 工作流4（定期自审）
"这个概念你记住" + 解释 → 工作流2（直接存储）
