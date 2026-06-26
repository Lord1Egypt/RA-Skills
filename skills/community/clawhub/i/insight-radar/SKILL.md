---
name: insight-radar
description: Dual-purpose news intelligence system - (1) AI self-evolution: extracts strategic patterns from news, writes to knowledge base. (2) User learning: generates CORE-analyzed news briefings tailored to user's interests. Supports customizable news categories. Use when scheduled daily news scanning or analyzing breaking trends.
dependencies:
  - core-prism
  - news-source-manager
permissions:
  filesystem:
    read:
      - USER.md  # User context for [E] Execution personalization
      - memory/news-sources.json  # News category config
    write:
      - memory/news-log/  # Daily news records
      - memory/knowledge-base/concepts.md  # High-bar concept entries
      - memory/knowledge-base/patterns/*.md  # Verified patterns only (rare, 3+ occurrence threshold)
  network:
    - WebSearch  # Search recent news via web search API
    - WebFetch  # Fetch article content for URL validation
  external_outputs:
    - none  # This skill generates briefings locally; delivery to Feishu is handled by the caller (HEARTBEAT-news.md), not this skill
  credentials:
    - none  # No API keys needed; web search uses agent's built-in tools
config:
  reads:
    - USER.md
    - memory/news-sources.json
  writes:
    - memory/news-log/
    - memory/knowledge-base/concepts.md
    - memory/knowledge-base/patterns/*.md
---

# Insight Radar (洞察雷达)

**Two modes, one skill:**

## 🧠 For AI Self-Evolution
扫描新闻，提取**概念与战略模式**，写入知识库:
- **Concepts** (主要) → `concepts.md`: 当前事件、技术发展、市场变化
- **Thinking Patterns** (偶尔) → `patterns/*.md`: 仅当新闻揭示可复用模式时

## 📰 For User Learning
CORE 分析的战略简报，不是新闻聚合:
- **[C] Core Logic**: 第一性原理（不是发生了什么，而是 WHY）
- **[O] Opportunity**: 价值流向，谁赢了？
- **[R] Risk**: 反共识，隐藏黑天鹅
- **[E] Execution**: 你今天该做什么？

**News categories**: 由 `news-source-manager` 管理，默认 AI/Tech。

---

## Workflow

### 1. Load News Config

调用 `news-source-manager` 获取用户的活跃新闻类别:

```json
{
  "active_categories": [{
    "name": "AI/Tech",
    "keywords": ["AI", "machine learning", "LLM", "AI agents", "semiconductor", "robotics"],
    "sources": ["TechCrunch", "MIT Tech Review"],
    "search_params": {"count": 5}
  }]
}
```

**If news-sources.json 不存在**: 触发 `news-source-manager` 初始化流程。
**Fallback**: 用户跳过配置时，默认 "AI/Tech" 类别。

---

### 2. Search Recent News

**搜索策略**: 宽泛扫描 + 智能补搜 + 中英双语。

**核心原则**: 不预定义固定 hints。越简单的 query 返回越全面的结果（测试验证：`"AI technology news March 2026"` 比精心设计的关键词组合覆盖度更高）。

**For each active category, 分两步**:

#### Step 2a: 宽泛扫描（每类别固定 2 次）

```
英文: "{category_name} news {current_month} {current_year}"
中文: "{类别中文名} 新闻 {current_year}"
count: 5

示例 (Finance/Crypto, 当前 March 2026):
  WebSearch("Finance Crypto news March 2026", count: 5)
  WebSearch("金融 加密货币 新闻 2026", count: 5)
```

**类别名称映射**:
| category_name | 类别中文名 |
|---------------|----------|
| AI/Tech | AI 科技 |
| Business Strategy | 商业战略 |
| Finance/Crypto | 金融 加密货币 |
| Health/Bio | 生物医药 数字健康 |
| Energy/Climate | 新能源 气候科技 |
| Policy/Regulation | AI监管 科技政策 |
| Product Design | 产品设计 用户体验 |

#### Step 2b: 覆盖度评估 + 智能补搜（每类别 0-2 次）

扫描 Step 2a 结果后，用 `news-sources.json` 中的 **keywords** 评估覆盖度:

```
1. 将该类别的 keywords 分为 3-4 个子领域簇
   例如 AI/Tech: [模型/Agent] [芯片/硬件] [安全/治理] [应用/商业]

2. 检查 Step 2a 结果覆盖了哪些簇
   例如: 结果中有 GPT-5.4、Agent 部署 → [模型/Agent] ✅
         结果中没有芯片相关 → [芯片/硬件] ❌

3. 对未覆盖的簇，生成 1 条补搜 query
   例如: WebSearch("AI chips semiconductor news March 2026", count: 3)

4. 最多补搜 2 次/类别（硬上限，防止无限膨胀）
```

**总调用量**: 3 类别 × 2 底线 + 0-6 补搜 = **6-12 次**（实际通常 8-9 次）。

#### Fallback

仅当某类别 Step 2a + 2b 合计 < 2 条结果时，将 `{current_month}` 改为上月重搜。

**If ALL categories fail**: 通知用户 "过去 24h 无重大新闻，建议扩展类别或时间范围。"

#### 后处理

**去重**: 合并所有类别结果，按 URL/title 去重，优先保留高权威来源（sources 中 priority: 1）。

**URL 验证**: 检查返回 URL 是否为具体文章。首页/分类页 → 用 web_fetch 提取具体链接。

**战略价值筛选** — 从去重结果中选 TOP 3-5 条:

高价值信号 (优先): 揭示行业本质变化 / 反共识观点 / 跨领域影响 / 基础设施机会
低价值信号 (跳过): 纯融资公告 / 常规产品发布 / 无新洞察的共识观点

**类别覆盖**: 选出的 3-5 条至少覆盖 2 个不同类别。如果都来自同一类别 → 补 1 条次要类别。

**输出格式**: 每条标注类别、时间、来源链接
```markdown
### 1️⃣ 中国AI Agent爆火 【AI/Tech】
📅 1 day ago (2026-03-22)
🔗 [Reuters](https://www.reuters.com/...)
```

---

### 3. Analyze with CORE Framework

对每条选中的新闻，调用 `core-prism` skill 进行 CORE 分析。传入 USER.md 中的用户上下文用于 [E] Execution 维度个性化。

---

### 4. Generate Strategic Briefing

**4 个 mandatory sections**:

1. **📰 核心资讯** (Core News)
   - 3-5 items with CORE analysis
   - 每条含: 类别标签【】, 时间 📅, 来源链接 🔗, C/O/R/E 分析

2. **🎯 战略简报** (Strategic Briefing)
   - 今日破局点: 这些故事**一起**揭示了什么？
   - So What? 给用户一个尖锐的可操作问题

3. **🧠 认知沉淀** (Cognitive Digest)
   - 今日关键事件摘要 (写入 news-log)
   - 候选概念 (如果今日新闻揭示了一个**全新的认知框架**，标记为候选，累积验证后才入 concepts.md)
   - 候选模式 (如果同一模式已在 3+ 条不同新闻中反复出现，才提炼入 patterns/*.md)
   - 判断力复盘 (哪些旧假设被验证/推翻？)

4. **🤔 盲区质询** (Blind Spot Questions)
   - 3-5 个挑战用户假设的思考题

---

### 5. Write to Knowledge Base — **三层架构**

**每日新闻和深度认知分层存储，避免知识库被新闻复述淹没。**

#### 三层写入规则

| 层级 | 文件 | 入库标准 | 频率 |
|------|------|---------|------|
| **Layer 1: 新闻日志** | `memory/news-log/YYYY-MM-DD.md` | 每条分析过的新闻 | 每天 |
| **Layer 2: 概念** | `memory/knowledge-base/concepts.md` | 真正的新认知框架，不是事件记录 | 每周 1-3 个 |
| **Layer 3: 思维模式** | `memory/knowledge-base/patterns/*.md` | 同一模式在 3+ 条不同新闻中反复出现 | 每月 1-2 个 |

#### Step 5.1: 写入新闻日志（每次必须）

创建/追加 `~/.openclaw/workspace/memory/news-log/YYYY-MM-DD.md`:

```markdown
# 资讯早报 - YYYY-MM-DD

## 1. [新闻标题] 【类别】
- **来源**: [链接]
- **CORE 摘要**: C: ... | O: ... | R: ... | E: ...
- **候选概念**: [如有，标记为候选] 或 "无"
- **关联旧模式**: [如能关联到 patterns/*.md 中已有模式] 或 "无"
```

#### Step 5.2: 概念入库（高门槛，非每日）

**入库条件**（必须同时满足）:
- ✅ 这是一个**新的认知框架**，不是事件/产品/公司名
- ✅ 具有**持久解释力**（6 个月后仍然有用）
- ✅ 无法用已有概念解释

**Bad**: "LightGen 光芯片"（这是一条新闻）
**Good**: "光计算范式"（这是一个持久概念，但需要更多数据点确认才入库）

暂不入库的标记为"候选概念"记录在 news-log 中，等累积验证。

#### Step 5.3: 思维模式入库（最高门槛）

**入库条件**: 同一模式在 **3+ 条不同日期的新闻中反复出现**。

在 news-log 中标记 "关联旧模式"，当累积到 3+ 条时，提炼入 `patterns/{id}.md`。

**写入格式必须与 cognitive-forge 一致**（YAML frontmatter + 7 字段正文）：

```markdown
---
id: {kebab-case-english}
name_zh: {中文名}
name_en: {English Name}
source: Insight Radar, {触发该模式的 3+ 条新闻来源概述}
category: {investing|startup|systems|ai-thinking|positioning|management|growth|cognitive-bias|influence|economics}
tags: [{3-5个中文标签}]
scenarios: [{3-5个应用场景}]
related_models: [{2-4个已有模型id}]
difficulty: {beginner|intermediate|advanced}
date: {YYYY-MM-DD}
---

**核心逻辑**: {模式的本质，一段话}

**思维框架**: {核心机制，一句话}

**决策原则**: {在XX场景下，应该XX而非XX}

**盲区警告**: {何时失效}

**反射弧**: {看到XX信号 → 联想到模型 → 行动}

**锚定案例**: {触发该模式的真实新闻案例}

**反共识**: {❌ "旧常识" → ✅ 新真相}
```

> **注意**：insight-radar 产出的模式 `source` 字段标注为 "Insight Radar, ..."（而非书籍来源），以区分来源渠道。

#### Step 5.4: 验证写入

写入后，用 Read 工具读取 news-log 文件确认条目存在。

**Completion Checkpoint**:
- □ news-log/YYYY-MM-DD.md 已写入？
- □ 概念入库？（仅当满足高门槛条件时）
- □ 思维模式入库？（仅当同一模式 3+ 次出现时）
- □ 用 Read 验证了写入？

---

### 6. Deliver Briefing

通过触发通道发送给用户。

**用户上下文个性化** (强制步骤):

1. **读取 USER.md** (`~/.openclaw/workspace/USER.md`):
   - 工作经历/现在 → profession
   - 兴趣/爱好 → interests
   - 当前焦虑/未来规划 → challenges
   - 不存在 → 使用通用第二人称

2. **映射到 [E] Execution**:
   - 引用职业: "如果你在做 AI 产品..."
   - 关联兴趣: "鉴于你对 fintech 的关注..."
   - 回应挑战: "对于你建立第二曲线的目标..."

3. **始终使用第二人称** ("你/你的")

---

## Configuration

| 优先级 | 来源 | 用途 |
|--------|------|------|
| 1 | `memory/news-sources.json` | 新闻类别 (由 news-source-manager 管理) |
| 2 | `USER.md` | 个性化 [E] Execution 维度 |
| 3 | 默认值 | AI/Tech 类别, 通用第二人称 |

**Knowledge base paths** (auto-created if missing):
- `~/.openclaw/workspace/memory/knowledge-base/concepts.md`
- `~/.openclaw/workspace/memory/knowledge-base/patterns/*.md`

---

## Quality Standards

**Forbidden**: 新闻聚合无分析 / 表面评论 / 重复新闻稿 / "AI is changing everything" 式空话 / 空 briefing

**Required**: 一针见血的洞察 / 反共识视角 / 可操作 / 跨文章找暗线 / 最少 2-3 条新闻 / 🧠 认知库更新 section is MANDATORY

---

## Execution Flow

```
Daily trigger
    ↓
1. Load news-source-manager config
    ↓
2. Search recent news (search_hints + fallback)
    ↓
3. Call core-prism for CORE analysis
    ↓
4. Generate briefing (4 mandatory sections)
    ↓
5. Write to knowledge base (MANDATORY)
    ├─ concepts.md
    ├─ patterns/*.md (if patterns found)
    └─ Verify with Read
    ↓
6. Deliver briefing (personalized via USER.md)
```

---

## References

- See [example-output.md](references/example-output.md) for output format
- See [category-config.md](references/category-config.md) for adding custom categories
- See `core-prism` skill for detailed CORE framework
- See `news-source-manager` skill for category management
