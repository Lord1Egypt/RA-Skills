---
title: 知识库 SCHEMA — 给 LLM 图书馆员的工作守则
type: schema
audience: llm-librarian
last_updated: bootstrap
---

# 知识库 SCHEMA — LLM 图书馆员的工作守则

> 这份文件**给 LLM 看**。每次 ingest / compile / ask / lint 时，librarian 必须先读完本文件，再按下面的规范操作 wiki/。
>
> 目标：让 wiki 长得像 Wikipedia——**原子条目 + 强双链 + 有出处 + 可被 lint**。

---

## 0. 三层架构（不要混淆）

```
raw/      ← 原始素材（不可改，只读）
wiki/     ← 你（LLM）维护的百科条目（可写）
SCHEMA.md ← 本文件（你的工作守则；很少改）
```

**raw/ 永远只读**。如果原始素材有错，标注在 wiki/ 里，不改 raw/。

---

## 1. 条目原子化原则

**一个 wiki 页 = 一个概念**，不是一篇原始文章。

- ❌ `2026-04-23-某博客全文整理.md`（多个概念塞一起）
- ✅ `Karpathy-Wiki-Pattern.md`、`Cross-Reference.md`、`No-RAG-Approach.md`（一篇文章拆成 N 页概念）

**规模指引**：单页 200-1500 字。<200 字考虑合并，>2000 字考虑拆分。

**一个新 raw 文档应该影响 5-15 个现有 wiki 页**——大部分是更新（加交叉引用），少部分是新建。

---

## 2. 文件命名

- **概念页**：`<英文标题或 kebab-case>.md`，如 `LLM-Wiki-Pattern.md`、`obsidian-sync.md`
- **人物页**：`Andrej-Karpathy.md`（保留人名原写法）
- **特殊页**：`index.md`（目录）/ `log.md`（日志）/ `SCHEMA.md`（本文件）/ `graph.mermaid`（自动生成）

**禁忌**：文件名不要有空格、不要有 `/`、中文标题用单独的 `title:` frontmatter 字段表达。

---

## 3. Frontmatter 规范

每个条目必须有：

```yaml
---
title: 条目可读标题（中文/英文皆可）
type: concept | person | paper | article | tutorial | reference
concepts: [关键词1, 关键词2, 关键词3]
sources:
  - url: https://...
    ingested: 2026-04-23
  - file: raw/2026-04-23/xxx.md
last_updated: 2026-04-23
status: stub | draft | stable
confidence: 0.85           # v2.7+，0.0-1.0，见 §3.1
relations:                 # v2.7+，typed graph 边，见 §4.1
  uses: [Page-A]
  depends-on: [Page-B]
  contradicts: [Page-C]
  supersedes: [old-Page-D]
---
```

- `type` 必填，枚举值见上
- `concepts` 必填，3-5 个标签，用于 index 分组
- `sources` **至少一条**——这是图书馆员的"引用癖"，**没有出处的断言不可信**
- `status: stub` 表示"被链接但还没写完"，需要补全；`stable` 表示已经过校对
- `confidence` v2.7+ 推荐填（缺省按 0.5 处理；见 §3.1）
- `relations` v2.7+ 选填，有 typed 关系时必写（见 §4.1）

### 3.1 Confidence + Supersession（v2.7+）

`confidence` 是 0.0–1.0 浮点，按下表赋值：

| 区间 | 含义 | 配套 status |
|---|---|---|
| `0.9 – 1.0` | 多源交叉验证；经过实践 | 必须 `stable` |
| `0.7 – 0.9` | 单一权威源（论文/官方文档/作者本人） | `stable` 或 `draft` |
| `0.5 – 0.7` | 单次提及 / 二手转述 | `draft` |
| `< 0.5` | 推测、未核实、待考证 | 正文必须有 `<!-- TODO: 待核实 -->` 注释 |

**Supersession（取代关系）**：当新事实推翻旧事实时，**不删旧条目**，而是：

1. 新条目 frontmatter 加 `relations.supersedes: [old-page]`
2. 旧条目 frontmatter 加 `relations.superseded-by: [new-page]` + `confidence` 调低到 ≤ 0.3
3. 旧条目正文顶部加 `> ⚡ 已被 [[new-page]] 取代，请优先看新条目`
4. kb-lint 会自动校验双向一致性（`supersedes` ↔ `superseded-by` 必须互指）

**为什么不删旧条目**：保留历史 = 保留证据链 = 让人能看到"我们以前是这么以为的，后来发现不对"。这是 wiki vs RAG 的关键差异。

---

## 4. 双链规范（核心）

**任何提到其他条目的地方都要 `[[双括号]]`**。这是 wiki 的命脉。

- 条目里第一次提到一个概念时必须 `[[Cross-Reference]]`
- 同一段反复出现可以省略，避免视觉噪音
- 链接目标必须是**已存在的 wiki 文件名（不带 .md）**或 stub
- 如果引用了未来要写的概念，建一个 stub：仅包含 frontmatter + 一句话占位，`status: stub`

**不要"裸引"**：不要写 "Karpathy 提出..."，要写 "[[Andrej-Karpathy]] 提出..."。

### 4.1 Typed Relations（v2.7+）

正文里的 `[[]]` 保持**原文可读**（Wikipedia 风格，不污染阅读体验）。**关系类型放 frontmatter `relations:` 字段**，由机器使用（kb-graph 着色 / kb-lint 校验 / 推理）。

**允许的关系类型**（封闭枚举）：

| 类型 | 含义 | 何时用 |
|---|---|---|
| `uses` | 使用了某概念/工具 | "本概念在实现里用到 X" |
| `depends-on` | 强依赖 | "没有 X 本概念无法成立" |
| `extends` | 在父概念基础上扩展 | "本概念是 X 的延伸/特例" |
| `part-of` | 是更大概念的子部件 | "本概念是 X 的一个组成部分" |
| `contradicts` | 与某条结论冲突 | "本条与 X 主张相反" — kb-lint 会报警 |
| `supersedes` | 取代某旧条目 | 见 §3.1 |
| `superseded-by` | 被某新条目取代 | 通常自动维护，见 §3.1 |
| `related` | 通用关联 | 其他都不合适时的兜底 |

**示例**：

```yaml
relations:
  uses: [Karpathy-Wiki-Pattern, Obsidian]
  depends-on: [obsidian-cli]
  contradicts: [RAG-Pipeline]
  supersedes: [old-knowledge-base-design]
  related: [LLM-as-Librarian]
```

**重要规则**：

- frontmatter `relations.<type>` 列出的页**必须**也用 `[[]]` 在正文里出现至少一次，反过来不强制（正文里有 `[[X]]` 但没列 `relations:` 视为 `related`）
- `contradicts` 双向：A `contradicts: [B]` 时，建议 B 也 `contradicts: [A]`（kb-lint 给 warning 不强制）
- `supersedes` ↔ `superseded-by` **强制双向**（kb-lint 强制 error）

---

## 5. 标准段落结构

每个概念页推荐分段（按需取舍，不强制全有）：

```markdown
# 标题

## 一句话定义
（一行；让人秒懂"这是什么"）

## 详解
（核心展开，引用其他条目用 [[]]）

## 与相关概念的关系
- 与 [[X]] 的区别：...
- 与 [[Y]] 的协作：...

## 出处
- [文章标题](原始 URL) — 2026-04-23 ingest
- raw/2026-04-23/xxx.md（本地素材）

## 待办
- [ ] 待补：xxx
```

---

## 6. ingest 时 librarian 必须做的事

当用户喂一个新 raw 文档时：

1. **读 raw**，识别 5-15 个核心概念
2. **扫 wiki/**（看 index.md 和文件名列表），判断哪些概念已存在
3. 对**已存在的概念**：在它们的页里追加内容 + 加 `[[新建概念]]` 反链
4. 对**新概念**：建新 wiki 页（按上面规范）
5. **写 log.md**：追加 `## [日期] ingest | <raw 文件名> | 影响 N 页`
6. **更新 index.md**：把新建/更新的概念加到对应分组

---

## 7. 查询（kb-ask）时 librarian 必须做的事

当用户问问题时：

1. 在 wiki/ 里**先 grep 关键词**，再读相关页全文（**不要只看摘要**）
2. 综合答案，**每个事实性断言都要带 `[[页名]]` 引用**
3. 如果发现了 wiki 里没记录的洞察 → 提示用户用 `kb-ask --save` 把答案归档为新条目
4. 如果发现 wiki 有矛盾或过时 → 在答案里标注，并写一条 lint TODO

---

## 8. lint 守则

定期跑 `kb-lint`。重点关注：

- **断链**（[[X]] 但 X.md 不存在）→ 要么建 stub 要么改链接
- **孤儿**（没人链入它的条目）→ 要么从相关条目加反链，要么考虑合并/删除
- **stub 累积**（status: stub 太多）→ 优先补全
- **stale**（last_updated 超 90 天 + status:draft）→ 重读、更新或归档
- **缺出处**（sources: 为空）→ 危险信号，可能是 LLM 自己编的
- **supersession 不对称**（A `supersedes: [B]` 但 B 没 `superseded-by: [A]`）→ 修双向（v2.7+）
- **未声明的 contradicts**（两页都 `confidence ≥ 0.7` 但内容矛盾）→ 二次审阅，决定 supersession 或都改 confidence（v2.7+）
- **未知关系类型**（`relations:` 用了枚举外的 key）→ 改成兜底的 `related`（v2.7+）
- **低信度高声调**（`confidence < 0.5` 但正文里全是断言句，无 TODO 标记）→ 加 `<!-- TODO: 待核实 -->`（v2.7+）

---

## 9. 一切的目的

> "instead of just retrieving from raw documents at query time, the LLM **incrementally builds and maintains a persistent wiki**" — Karpathy

人类策划素材、提问；**你（LLM）做剩下所有事**：摘要、交叉引用、一致性维护、log 记录。
人类的判断仍然是核心，你只是执行者。

---

## 10. 与本系统的扩展约定

- **scope**：本 wiki 可能是 `agent`（私有）或 `shared`（跨 Agent）。两者结构相同，规范相同。
- **Obsidian 同步**：同步到 `vault/知识库/<scope>/`，所以你的双链格式必须和 Obsidian 兼容（标准 `[[文件名]]`）。
- **不要在 wiki 里写 child_process、shell 注入、密钥**：这个库可能被同步到云端 / 公司 KB。

---

## 11. wiki 子目录组织（v2.8.0 推荐 / 不强制）

Karpathy 原方案把 wiki/ 按内容性质分 4 个子目录。**v2.8 引入概念但不强制**——
旧的平铺 wiki 仍然能用；新条目优先按下面规则路由，让 Bases / Graph / index 更清晰：

```
wiki/
├── entities/    人 / 组织 / 产品（type: person | organization | product）
├── concepts/    想法 / 框架 / 理论（type: concept | pattern | method）
├── sources/     每个原始入库源的摘要页（type: source | paper | article）
└── synthesis/   跨切面分析 / 比较 / 推论（type: synthesis | analysis）
```

**LLM 创建新条目时的路由判断**：

| frontmatter `type` | 放哪 |
|---|---|
| `person` / `organization` / `product` | `entities/` |
| `concept` / `pattern` / `method` / `tutorial` / `reference` | `concepts/` |
| `source` / `paper` / `article` | `sources/`（一篇 raw 文档 = 一个 source 摘要页） |
| `synthesis` / `analysis` / `comparison` | `synthesis/`（kb-ask --save 默认归档到这里） |

**双链 `[[Page-Name]]` 不需要带子目录前缀**——Obsidian 自动按文件名解析，wikilink 跨子目录依然有效。

**已有平铺 wiki 怎么办**：
- 旧条目继续平铺也合规（lint 不会报警）
- 新条目优先按子目录创建
- 一次性迁移：未来版本可能提供 `kb-migrate-tree` 工具
- Obsidian Bases (`知识库-by-type.base`) 不依赖子目录——按 frontmatter `type` 字段就能分组
