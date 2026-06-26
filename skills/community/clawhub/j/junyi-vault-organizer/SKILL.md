---
name: junyi-vault-organizer
version: 2.0.0
description: "自动归档 — A two-domain knowledge management system: Business domain (事业域, customizable name, organized by function) and Life & Learning domain (生活学习域, three-layer Inbox→Cognition→Guidebook). Stores to Obsidian vault. Triggers when user mentions 自动归档, 归档, 享育心塾萃取器, 萃取器, or asks to save/store/organize any information — articles, reading notes, class notes, children's words, conversations, ideas, reflections, quotes, or any content they want to keep. Also triggers on save this, remember this, file this away, put this in my notes, store this for later, 记下来, 存一下, 帮我记, 存到知识库."
---

# 自动归档 (Two-Domain Knowledge Vault)

A two-domain knowledge management system. Turns the flood of daily information into
organized, retrievable, and reusable wisdom.

**Two domains:**
- **事业域** (`{business_name}/`) — Business content organized by function
- **生活学习域** (`生活学习/`) — Personal growth organized by three layers (收集层→认知层→指南层)

## Design Principles

- Low-friction capture, traceable distillation, cautious upgrades, long-term maintainability
- Only text content; images/video out of scope
- Storage: Obsidian physical files (not memory — survives Gateway restarts)

## Configuration

The following must be configured per user (via workspace files, e.g. TOOLS.md or MEMORY.md):

| Key | Description | Example |
|-----|-------------|---------|
| `vault_path` | Obsidian vault root directory (absolute path) | `/Users/someone/Documents/MyVault` |
| `business_name` | Business domain directory name (user-defined) | `享育心塾` |

**If not configured:** Ask user to provide both values before first use. Never hardcode paths or names.

## Top-Level Decision Flow

### Step 0: Business or Life & Learning?

**This is always the first routing decision.**

| Route to | Signal | Examples |
|----------|--------|----------|
| **事业域** `{business_name}/` | Directly related to user's business, clients, products, operations, commercial activities | 课程设计、运营策略、客户报告、活动复盘、商业学习笔记、营销素材、周会记录、方法论产品 |
| **生活学习域** `生活学习/` | Personal growth, family, spiritual practice, hobbies, general learning, children, daily life | 育儿观察、修行笔记、个人感悟、读书心得(非商业)、家庭记录、兴趣爱好 |

**Ambiguous cases:**
- Content about a topic that serves both business and personal growth → Ask user which domain
- Learning content: "Is this learning FOR the business or FOR personal growth?" — if clearly business-related (e.g., marketing course for the business), route to `{business_name}/学习笔记/`; if general personal development, route to `生活学习/`

---

# 事业域 (`{business_name}/`)

Business content organized by **function**, no three-layer nesting.

## Directory Structure

```
{business_name}/
├── 课程/              ← Course design, curricula, teaching materials, class notes
├── 运营/              ← Marketing strategies, growth plans, funnel analysis, metrics
├── 方法论产品/        ← SOPs, templates, prompts designed FOR clients to use
├── 客户报告/          ← Reports, assessments, analyses produced FOR clients
├── 活动档案/          ← Event records, recaps, attendee feedback, photos notes
├── 周会/              ← Meeting notes, agendas, action items
├── 素材/              ← Marketing copy, social media content, design briefs
└── 学习笔记/          ← External learning relevant to the business (courses, articles, peers)
```

## Business Domain Routing Rules

| Content type | Route to | Signal words |
|-------------|----------|-------------|
| Course design, curricula, lesson plans, teaching materials | `{business_name}/课程/` | 课程、课件、大纲、教案、回放 |
| Marketing, growth, operations strategy | `{business_name}/运营/` | 运营、增长、转化、漏斗、复购、私域 |
| SOPs/templates/prompts for clients | `{business_name}/方法论产品/` | SOP、模板、prompt、工具包、给家长用 |
| Reports/assessments for clients | `{business_name}/客户报告/` | 报告、评估、分析、成长规划 |
| Event records and recaps | `{business_name}/活动档案/` | 活动、沙龙、工作坊、公开课、复盘 |
| Meeting notes | `{business_name}/周会/` | 周会、会议、议程、行动项 |
| Marketing copy, social content | `{business_name}/素材/` | 海报、文案、朋友圈、推文、宣传 |
| Business-related external learning | `{business_name}/学习笔记/` | XX的分享、行业报告、商业课程、同行案例 |

**Custom sub-directories:** Within each function directory, organize by sub-topic or date as needed:
- Single event, 1 file → `YYYY-MM-DD 主题描述.md`
- Single event, multiple files → `YYYY-MM-DD 活动名/` sub-directory
- Cross-day event → `YYYY-MM 活动名/` sub-directory

## Business Domain Naming Rules

- Files: `YYYY-MM-DD 主题描述.md` (with date) or `主题名.md` (for evergreen docs like SOPs)
- Sub-directories: `YYYY-MM-DD 活动名/` or topic-based names
- Follow the universal naming rules below (no person names in titles, use `——` separator, etc.)

---

# 生活学习域 (`生活学习/`)

Personal and family content organized by the **three-layer** system.

```
生活学习/
├── 收集层/        → Raw capture, organized by scene
│     ↓ AI distills (when warranted)
├── 认知层/        → Refined insights by 5 dimensions
│     ↓ Proven patterns emerge
└── 指南层/        → Verified reusable guides, methods, checklists
```

## Layer 1: 收集层 (Inbox)

Zero-friction entry point. Raw records organized by **scene**.

**Default scenes:**

| Scene | What goes here |
|-------|---------------|
| 学习成长 | Class notes, reading highlights, lectures, courses, podcasts (non-business) |
| 童言童语 | Children's actual words, questions, expressions — preserved verbatim |
| 育儿观察 | Parents' observations of children — milestones, patterns, growth moments |
| 灵感闪现 | Sudden ideas, one-line thoughts, "what if..." moments |
| 对话收获 | Key takeaways from conversations with others |
| 生活记录 | Daily life events and feelings |

**Custom scenes:** When user proposes a new scene, confirm name once, then auto-create directory.

**Repeating content types** (journals, weekly reviews, etc.) get their own scene directory — don't stuff them into 学习成长.

## Layer 2: 认知层 (Cognition)

Distilled knowledge organized by five dimensions:

| Dimension | Directory name (exact) | The test | Examples |
|-----------|----------------------|----------|---------|
| **What I Learn** | `认知层/What I Learn/` | "I learned this from someone/something else" | Book insights, article takeaways, lecture notes |
| **What I Think** | `认知层/What I Think/` | "I figured this out / observed this myself" | Personal reflections, parenting discoveries, patterns noticed |
| **What I Create** | `认知层/What I Create/` | "I made/wrote/built this" | Articles, presentations, systems designed |
| **What I Collect** | `认知层/What I Collect/` | "I want to keep this as-is" | Quotes, golden lines, sparks |
| **Who We Are** | `认知层/Who We Are/` | "This defines who we are as a family" | Values, philosophy, long-term goals |

**IMPORTANT: Use exact directory names above (with spaces, title case). Never convert to lowercase-hyphen format like `what-i-think`.**

**🔴 分类防线（必须执行）：**

1. **来源测试（分类前必做）**：这个知识/观点是谁产出的？
   - 从他人/外部来源学到的 → **What I Learn**（即使内容包含"对我的启发""素材整理"，来源是他人就是 Learn）
   - 用户自己悟到/观察到的 → **What I Think**
   - 信号词：标题含他人名字、"XX的框架""XX分享" → 大概率 Learn

2. **重复类型第一次就建独立目录**：早间日报、周报、日志等定期产出物，第一次归档时就在收集层建独立场景目录，不塞进「学习成长」

3. **同一活动/事件的多条内容 → 先建活动子目录**：识别信号是同一天、同一来源、同一主题的多条内容，先建 `YYYY-MM-DD 活动名` 子目录再逐条归入

4. **What I Think 按主题域建子目录**：
   - 子目录示例：AI理念、教育理念、修行理念、事业理念
   - 写入前先检查是否有匹配的子目录，没有则考虑新建
   - 避免根目录堆积

5. **What I Learn 按主题域建子目录**：
   - 子目录示例：AI与技术、商业与创业、修行与心法、育儿与教育
   - 写入前先检查是否有匹配的子目录，没有则考虑新建
   - 避免根目录堆积

**Classification rules:**
- External source primarily → What I Learn
- Self-observation/reflection primarily → What I Think
- Finished output → What I Create
- Fragment to keep as-is → What I Collect
- Family identity/values/rules → Who We Are
- Mixed content → classify by primary source; if both parts are important, split into two cognition entries

## Layer 3: 指南层 (Guidebook)

Proven, reusable methods that answer "how to do X" concretely.

**Admission criteria (strict):**
- User explicitly says "已验证", "反复有效", "用了较长时间", or similar
- OR original text contains clear validation evidence (e.g., "执行两个月有效")
- Methods that don't meet validation criteria stay in Cognition, not Guidebook
- Mark as "待验证" only if user wants to track an unvalidated method

**Directory rules:**
- Organized by project/domain sub-directories (e.g., `指南层/写作系统/`, `指南层/孩子教育/`)
- No loose files in 指南层 root — every file must be in a topic sub-directory

## Life & Learning Decision Flow

After routing to 生活学习域, follow these steps:

### Step 1: Determine user intent
- User says "就存一下 / 先记下来 / 不用总结" → Only write `收集层`, stop
- Normal record → Write `收集层`, then evaluate distillation (Step 3)
- Explicitly validated method/process → Write `收集层` + `认知层` + evaluate `指南层`

### Step 2: Determine scene
- Scene is clear → Route to corresponding `收集层/` directory
- Scene is ambiguous but close → Pick closest match, preserve original context in content
- Scene truly unclear → **Ask user**, do not guess

### Step 3: Determine whether to distill to 认知层

**Distill when:**
- Content has clear viewpoints, patterns, insights, or conclusions
- Content has long-term reuse value
- Content is a quote/fragment worth collecting
- Content is from articles/lectures/courses that can be distilled

**Do NOT distill when:**
- Pure memo or reminder
- Pure diary/stream-of-consciousness with no extractable insight
- User explicitly asked not to summarize
- Content only suitable for raw preservation

**Short content exception:** Short reflections (<200 chars) or single quotes can skip 收集层 and go directly to 认知层 — the raw text IS the refined version, no need for duplicate storage.

### Step 4: Determine whether to enter 指南层
- Has executable steps + validated effectiveness → 指南层
- Just an idea, principle, or feeling → Stay in 认知层
- Unvalidated method → Stay in 认知层, upgrade later when validated

---

# Universal Rules (Both Domains)

## File Management Rules

### When to create new file
- New topic
- First record of the day under a new topic
- Content significantly different from existing notes
- Content belongs to a different layer/dimension/function

### When to merge into existing file
- Same day AND same scene/topic
- New content supplements existing content (not a new topic)
- Append with a separator (`---`) and timestamp

### When to update existing file
- Guidebook: prefer updating original file over creating new ones; refresh "更新日期"
- Cognition: if supplementing the same insight, add a "补充观察" section
- Never overwrite raw content for cosmetic reasons

## 🔴 标题命名规则（必须执行）

### 通用规则

1. **不含人名**：标题聚焦概念/主题本身，人名放在文件内部 metadata（来源字段）
   - ❌ `黄有璨的AI焦虑三分法` → ✅ `AI焦虑三分法`
   - ❌ `韩叙：一人公司框架` → ✅ `一人公司框架`
   - ❌ `刘思毅：深圳AI嘉年华` → ✅ `深圳AI嘉年华——观察与三个判断`
2. **分隔符统一用 `——`**（中文破折号），不用 `：`、`-`、`:`
3. **标题要精准直接**：描述内容核心，不用口语化/吸引眼球的表达
   - ❌ `你的小龙虾可能悄悄出卖了你` → ✅ `AI Agent安全隐患与防护`
4. **产品名用正式名称**：`龙虾` → `OpenClaw`

### 收集层标题（生活学习域）

- 格式：`YYYY-MM-DD 主题描述.md`
- 子目录内文件可省略日期前缀（如 `简版.md`、`详细版.md`）
- 活动子目录：`YYYY-MM-DD 活动名/` 或 `YYYY-MM 活动名/`

### 认知层标题（生活学习域）

- 格式：`标题.md`（无日期前缀，认知按主题组织不按时间）
- 从提炼内容中提取核心概念作为标题

### 指南层标题（生活学习域）

- 格式：`主题名.md`（无日期前缀）
- 面向行动：回答"怎么做X"

### 事业域标题

- 带日期的记录：`YYYY-MM-DD 主题描述.md`
- 常青文档（SOP、模板等）：`主题名.md`

## Content Templates

### 事业域文件

```markdown
# [Title]

> 日期：YYYY-MM-DD
> 类别：[function directory name, e.g., 课程/运营/方法论产品]
> 来源：[source if applicable]

---

[Content — structured appropriately for the function type]
```

### 收集层 (生活学习域)

```markdown
# [Title]

> 日期：YYYY-MM-DD
> 场景：[scene name]
> 来源：[source if applicable]

---

[Original content — keep close to original, minimal formatting]
```

### 认知层 (生活学习域)

```markdown
# [Title]

> 日期：YYYY-MM-DD
> 维度：[dimension name]
> 来源：[source — article name, conversation, experience, etc.]
> 源文件：[corresponding inbox filename, e.g., 生活学习/收集层/学习成长/2026-03-13 蒙特梭利.md]
> 标签：#tag1 #tag2

---

[Refined content — distilled, structured, insightful]

## 核心要点
- Point 1
- Point 2
```

Note: When content skips 收集层 (short reflections/quotes), 源文件 field is "用户即时输入".

### 指南层 (生活学习域)

```markdown
# [Title]

> 更新日期：YYYY-MM-DD
> 适用场景：[when to use this guide]
> 验证状态：[已验证 / 待验证]
> 来源：[corresponding cognition or inbox filename]

---

[Step-by-step guide, checklist, or methodology]
```

**Field defaults:**
- 来源 missing → "用户即时输入"
- Tags: 2-3 max, prefer topic/person/method keywords
- Preserve original attribution for articles/lectures/books

## Source Traceability

- Every 认知层 entry must trace back to a 收集层 file or "用户即时输入"
- Every 指南层 entry must trace back to 认知层 or 收集层
- 事业域 files should note their source in the 来源 field
- No orphaned conclusions without traceable context

## Long Text Handling

| Size | Strategy |
|------|----------|
| < 30,000 chars | Write directly |
| ≥ 30,000 chars | Chunked write (≤20K per chunk, break at paragraph boundaries) |

**Never use `obsidian-cli create --content`** — truncation bug.

After every write, verify:
```bash
ls -la "<file>"     # exists and reasonable size
tail -5 "<file>"    # content is complete
```

## 🔴 乱码检查（每次写入后必须执行）

```bash
python3 -c "c=open('<file_path>').read(); n=c.count('\ufffd'); print(f'{n}个乱码') if n else print('✅')"
```

Found U+FFFD (�) → infer correct character from context, fix with edit, re-verify.

## Searching and Retrieval

- `obsidian-cli search-content "<keyword>"` — search note content
- `obsidian-cli search "<note name>"` — search note titles
- `find` + `grep` — precise filesystem search

## 🔴 目录构建规则（必须执行）

### 事业域目录规则

1. **顶层按功能分8个目录**：课程、运营、方法论产品、客户报告、活动档案、周会、素材、学习笔记
2. **功能目录内部按需建子目录**：
   - 单次活动1个文件 → 直接放 `YYYY-MM-DD 主题描述.md`
   - 单次活动多个文件 → 建 `YYYY-MM-DD 活动名/` 子目录
   - 跨日活动 → 建 `YYYY-MM 活动名/` 子目录
   - 系列内容 → 建主题子目录（如 `课程/公开课系列/`）
3. **新的功能类型**：如果内容不匹配现有8个目录，先考虑归入最近似的；确实需要新目录时，向用户确认后新建

### 生活学习域——收集层目录规则

1. **顶层按场景分目录**：学习成长、童言童语、育儿观察、灵感闪现、对话收获、生活记录等
2. **重复类型独立建目录**：日报、周报、日志等定期产出物，不塞进「学习成长」，直接在收集层建独立场景目录
3. **学习成长/内部的子目录规则**：
   - 单次活动1个文件 → 直接放 `YYYY-MM-DD 主题描述.md`
   - 单次活动多个文件 → 建 `YYYY-MM-DD 活动名/` 子目录
   - 跨日活动（禅七、大会等）→ 建 `YYYY-MM 活动名/` 子目录
4. **功能性文件可直接放收集层根目录**：如待办池、清单等不属于特定场景的文件

### 生活学习域——认知层目录规则

1. **What I Learn 按知识领域分子目录**：如 AI与技术、修行与心法、育儿与教育
2. **What I Think 按理念主题分子目录**：如 AI理念、修行理念、教育理念
3. **What I Create 按产出类型分子目录**：如 公众号文章、觉知日记
4. **What I Collect 按素材类型分子目录**：如 金句库、选题库
5. **Who We Are 扁平存放**：身份文档数量少，不需要子目录
6. **🚫 禁止同名文件与目录共存**：如果存在 `事业理念/` 目录，就不能同时有 `事业理念.md` 文件。遇到这种情况，把 .md 文件移入目录并重命名

### 生活学习域——指南层目录规则

1. **顶层按项目/领域分目录**：如 写作系统、孩子教育、家庭OS系统、旅行规划
2. **根目录零散文件清零**：每个文件都必须归入一个主题目录
3. **项目目录内部按功能分子目录**：如 大纲/、成长规划报告/ 等

## 🔴 反模式清单（遇到必须修复）

| 反模式 | 正确做法 |
|--------|---------|
| 同名 .md 文件与目录共存 | 把文件移入目录并重命名 |
| 根目录散落文件（指南层/认知层） | 归入对应主题目录 |
| 标题含人名 | 去掉人名，放入 metadata |
| 分隔符混用（`：`、`-`、`——`） | 统一用 `——` |
| 同日期多文件未归入子目录 | 建活动子目录合并 |
| 口语化/营销化标题 | 改为精准直接的概念描述 |
| 产品俗称（龙虾） | 用正式名称（OpenClaw） |
| 重复类型内容塞进「学习成长」 | 在收集层建独立场景目录 |
| 事业内容放进生活学习域 | 路由到 `{business_name}/` 对应功能目录 |
| 个人成长内容放进事业域 | 路由到 `生活学习/` 对应层级 |
| 英文目录名（inbox/cognition/guidebook） | 用中文目录名（收集层/认知层/指南层） |

## Full Directory Structure Reference

```
[vault_path]/
├── {business_name}/                ← 事业域（用户自定义名称）
│   ├── 课程/
│   │   ├── 2026-03-15 公开课第一期/
│   │   └── 课程体系设计.md
│   ├── 运营/
│   │   ├── 2026-03 增长策略.md
│   │   └── 私域运营SOP.md
│   ├── 方法论产品/
│   │   └── 家庭AI实操指南.md
│   ├── 客户报告/
│   │   └── 2026-03-20 XX家庭成长规划.md
│   ├── 活动档案/
│   │   └── 2026-03-22 线下沙龙/
│   ├── 周会/
│   │   └── 2026-03-17 周会纪要.md
│   ├── 素材/
│   │   └── 朋友圈文案库.md
│   └── 学习笔记/
│       ├── 商业与创业/
│       └── 2026-03-10 一人公司框架.md
└── 生活学习/                       ← 生活学习域（固定名称）
    ├── 收集层/
    │   ├── 学习成长/
    │   │   ├── 2026-01 泉州禅七/
    │   │   └── 2026-03-13 SWIS学校讲座.md
    │   ├── 童言童语/
    │   ├── 育儿观察/
    │   ├── 灵感闪现/
    │   ├── 对话收获/
    │   └── 生活记录/
    ├── 认知层/
    │   ├── What I Learn/
    │   │   ├── AI与技术/
    │   │   ├── 修行与心法/
    │   │   └── 育儿与教育/
    │   ├── What I Think/
    │   │   ├── AI理念/
    │   │   ├── 修行理念/
    │   │   └── 教育理念/
    │   ├── What I Create/
    │   ├── What I Collect/
    │   └── Who We Are/
    └── 指南层/
        ├── 写作系统/
        ├── 孩子教育/
        ├── 家庭OS系统/
        └── 旅行规划/
```

**IMPORTANT: Use Chinese directory names for the three layers. English aliases (inbox/cognition/guidebook) are NOT used — they cause duplicate directories.**
