# LLM Wiki 规范

## 领域定义

本 wiki 覆盖目标公司投资价值分析，服务于股东和潜在投资者。

**核心受众：** 股东、机构投资者、分析师

## 命名规范

```
文件命名：拼音连字符.md
示例：
- chuang-xin-yin-qing-创新引擎.md
- chan-pin-a-产品A.md
- ren-wu-a-人物A.md

链接格式：[[页面名]] 或 [[目录/页面名]]
```

## 前置字段（必需）

```yaml
---
title: 页面标题
created: YYYY-MM-DD
updated: YYYY-MM-DD
valid_until: YYYY-MM-DD | null  # 事实有效期，null表示当前有效
type: entity | concept | announcement | financial | governance
tags: [tag1, tag2, tag3]
sources: [raw/yyyy-mm-dd/source.md]
---
```

### valid_until 字段说明

用于处理**事实时效性**问题——同一事实随着时间推移可能变化（如"唯一"→"首个"→出现竞品）。

| 值 | 含义 |
|----|------|
| `YYYY-MM-DD` | 该页面内容有效至该日期截止 |
| `null` | 内容为当前有效状态（默认） |

**使用规则：**
- 年报/公告中的事实性描述应记录 `valid_until`（通常为下一份年报发布日期）
- 旧版描述保留但标注失效，新版描述作为当前有效
- AI 回答默认引用 `valid_until: null` 或未过期的内容
- 已失效内容不得作为当前市场判断的依据

## 双语规范

> **核心原则：中英文资料是对等翻译关系，内容一致。**
> 资料本身的错误由来源解决，知识库中的记录不需要因为"中英文不一致"而做特殊处理。

### 文档语言标识

所有入 `sources/` 的文档标明语言：

```yaml
---
language: zh | en 
title: 文档标题
document_date: YYYY-MM-DD
document_type: annual_report | interim_report | announcement | news | esg_report | other
sources: [raw/yyyy-mm-dd/filename.ext]
---
```

### 配对检测（Ingest Step 0）

| 规则 | 触发条件 | 动作 |
|------|---------|------|
| 规则A | 同名不同语言 | 自动配对 |
| 规则B | 同日期+同类型 | 人工确认后配对 |

配对成功 → 记录 `bilingual_pair_id`；无配对 → `bilingual_pair_id: null`

### 问答语言路由

| 用户语言 | 搜索范围 | 回答语言 |
|---------|---------|---------|
| `zh` | 中文知识库 | 简体中文 |
| `zh-TW/zh-HK` | 繁体中文（如有）→简体转换 | 繁体中文 |
| `en` | 英文知识库 | 英文 |

**注：** 中英文内容等价，按用户语言路由即可，不需要在知识库层面处理"差异"。

---

## 标签分类

> 标签类别通用，具体标签值根据目标公司行业自定义。

| 标签 | 用途 | 行业自定义示例 |
|------|------|--------------|
| **公司** | 公司主体 | 医药：集团/子公司；科技：母公司/事业部 |
| **战略** | 战略方向 | 医药：创新引擎；科技：产品路线图 |
| **产品** | 具体产品/业务 | 医药：创新药/管线；科技：SaaS/硬件 |
| **财务** | 业绩、营收、利润、研发投入 | — |
| **治理** | ESG、董事会、薪酬、关联交易 | — |
| **股东** | 分红、派息、股东回报 | — |
| **市场** | 市场准入、竞争格局 | 医药：医保/集采；科技：牌照/认证 |

## 页面阈值

| 操作 | 条件 |
|------|------|
| 创建实体页 | 2+ 来源提及，或单一来源的核心内容 |
| 创建概念页 | 战略、治理、财务等抽象话题 |
| 更新页面 | 有新的相关信息时 |
| 不创建页面 | 仅一次性提及的次要细节 |

## 实体页面要求

每个实体页面必须包含：
- 基本信息表格
- 关键数据
- 关联实体（至少 2 个 [[wikilinks]]）
- 来源引用

## 概念页面要求

每个概念页面必须包含：
- 定义/解释
- 当前状态
- 关联实体 [[wikilinks]]
- 来源引用

## 更新政策

当新信息与现有内容矛盾时：
1. 检查日期 — 新来源通常覆盖旧来源
2. 如果确实矛盾，注明双方并标注日期
3. 矛盾处标注在前置字段：`contradictions: [related-page]`
4. 在 lint 报告中标记

## 归档政策

内容完全被替代时：
1. 移动到 `_archive/` 目录
2. 从 index.md 移除
3. 将相关页面的 [[wikilinks]] 替换为纯文本
4. 记录到 log.md

## 目录结构

```
wiki/
├── index.md           ← 页面索引
├── log.md            ← 操作日志
├── SCHEMA.md         ← 本规范
├── raw/              ← 原始资料（只读）
│   └── YYYY-MM-DD/   ← 按日期归档
├── concepts/         ← 概念页面
├── entities/         ← 实体页面
│   ├── products/     ← 产品实体
│   └── people/       ← 人物实体
├── timeline/         ← 事件时间轴
│   └── [entity_id]/  ← 按实体分目录
└── _archive/        ← 已归档页面
```

## Lint 检查项

### 通用检查

1. **孤立页面** — 没有被任何 [[wikilinks]] 引用的页面
2. **断链** — 指向不存在页面的 [[wikilinks]]
3. **索引完整性** — 每个页面都应在 index.md 中
4. **前置验证** — 必须有 title/created/updated/type/tags/sources
5. **陈旧内容** — updated 日期超过 90 天
6. **矛盾内容** — 同一话题有不同说法的页面
7. **页面大小** — 超过 200 行则建议拆分
8. **标签审计** — 检查使用的标签是否在 taxonomy 中

### 双语配对检查

| 检查项 | 严重程度 | 说明 |
|--------|---------|------|
| `bilingual_pair_missing` | 中 | 有配对文档但未登记 bilingual_pair_id |

**注：** 中英文资料对等，内容差异来自资料本身（会修复），知识库不需要标注或处理"语言不一致"。

---

# 事件溯源架构（Event Sourcing）

> **背景：** 投资标的关键事实会随时间大幅变化（产品生命周期、监管状态、市场独占性等）。传统"最新快照优先"模式无法回答"站在某个时间点看，当时的逻辑是什么"这类时间旅行问题。
>
> **解决思路：** 每份文档入知识库时，提取其中的**事件**（event），存入时间轴（timeline）。实体页面聚合最新状态，日常问答读快照，深度分析读时间轴。

## 事件类型分类（event_type）

| event_type | 含义 | 触发条件 |
|------------|------|---------|
| `产品里程碑` | 产品获批/上市/扩展 | 公告/新闻稿 |
| `财务更新` | 业绩发布/财务数据 | 年报/季报 |
| `战略公告` | 分拆/并购/重大合作 | 公告 |
| `市场准入` | 监管批准/市场变化 | 监管公告 |
| `ESG事件` | 评级变化/重大ESG事件 | 评级机构公告 |
| `治理变化` | 高管变动/关联交易/股权变动 | 公告/通函 |
| `管线进展` | 进入临床/终止/对外授权 | 公告/新闻稿 |
| `法规政策` | 重大政策影响评估 | 政策文件 |

> 根据行业特点，可扩展或替换事件类型。

## 事件记录格式（Timeline Entry）

```yaml
---
event_id: EVT_001
event_type: 产品里程碑
entity_id: [entity_id]           # 关联实体
entity_name: [实体名称]

# 文档来源
document_source: sources/YYYY-MM-DD/[文件名]
document_title: [文档标题]
document_date: YYYY-MM-DD     # 文档发布日期
document_type: announcement    # announcement | annual_report | interim_report | news | regulatory

# 事件时间
announcement_date: YYYY-MM-DD  # 对外公告时间（可与document_date不同）
effective_date: ~YYYY-MM       # 事件生效时间（如不确定则填估算）

# 事件状态
is_current: true              # 是否仍有最新效力
superseded_by: null           # 被哪条事件取代（EVT_XXX）

# 事件性质
is_state_change: true         # 是否为状态变更（里程碑类必须为true）
is_data_update: false         # 是否仅为数据更新（财务类）
is_context: false             # 是否仅为背景参考（非事件性内容）

# 标签
tags: [产品, tag1, tag2]
sources: [sources/YYYY-MM-DD/[文件名]]
---

## 事件摘要

[事件概述]

## 关键内容

### 事件性质
- [状态变更/数据更新/背景参考]

### 核心数据
| 指标 | 数值 |
|------|------|
| ... | ... |

### 对投资判断的影响
[影响分析]

## 关联实体
- [[实体1]]（关系说明）
- [[实体2]]（关系说明）

## 引用
- [[原始文件名]]

---
*由 Ingest 流程自动生成 | event_id: EVT_001*
```

## 实体快照页格式（Entity Snapshot）

实体页面从"直接编辑"改为"由 timeline 聚合"，格式如下：

```yaml
---
entity_id: [entity_id]
entity_type: product | company | person
entity_name: [实体名称]

# 快照元数据
latest_event_id: EVT_003       # 指向最新事件
snapshot_date: YYYY-MM-DD       # 快照生成日期
last_updated: YYYY-MM-DD

# 当前状态（由最新事件填充）
current_stage: [当前阶段]
current_status: [当前状态描述]

tags: [tag1, tag2]
sources: [timeline/[entity_id]/EVT_003-事件.md]
---

## 当前快照（截至YYYY-MM-DD）

| 指标 | 数值 | 来源事件 |
|------|------|---------|
| ... | ... | EVT_XXX |

## 近期时间轴

→ 完整时间轴：[[timeline/[entity_id]/]]

| 时间 | 事件 | 性质 |
|------|------|------|
| YYYY-MM | 事件描述 | 事件类型 / EVT_XXX |

## 历史快照

[[timeline/[entity_id]/EVT_001-事件1.md]]
[[timeline/[entity_id]/EVT_002-事件2.md]]

---
*本页面由 timeline 聚合生成，请勿直接编辑 — 更新请通过 Ingest 流程*
```

## 实体快照规范

> 中英文资料对等，不需要为每种语言维护独立快照。

### 文件结构

```
entities/products/
├── [entity_id].md    ← 主快照（中文，回答时自动路由）
└── ...

entities/companies/
├── [entity_id].md    ← 主快照
└── ...
```

### 财务数字货币

| 来源 | 货币 |
|------|------|
| 中文年报/公告 | CNY（人民币） |
| 英文年报/公告 | USD（美元），回答时换算注明 |

换算汇率：1 USD ≈ 7.2 CNY（参考值，回答时注明"换算，仅供参考"）

---

## Ingest 流程（重构版）

> 每份文档入知识库时，必须经过以下判断流程。

### 总流程图

```
┌─────────────────────────────────────────────┐
│  Step 0: 双语配对检测                         │
│  · 识别文档语言（zh / en）                    │
│  · 查找配对文档（同名不同语言/同时同类）       │
│  · 建立 bilingual_pair_id                     │
│  · 如已有配对，更新双方 doc_id                │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│  Step 1: 读取原始文件                         │
│  · 识别文件类型（PDF/Word/Markdown/HTML）   │
│  · 提取文本内容                              │
│  · 记录来源：原文件名 + 文档日期             │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│  Step 2: 判断文档性质                         │
│                                             │
│  公告/新闻稿？    → Step 3A（事件提取）     │
│  年报/季报？      → Step 3B（数据+事件双提取）│
│  法规/政策文件？  → Step 3C（影响分析）      │
│  其他/背景资料？  → Step 3D（归档为上下文）  │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│  Step 4: 事件提取（Event Extraction）        │
│                                             │
│  识别：涉及哪些实体？事件类型是什么？         │
│  判断：is_state_change / is_data_update /    │
│        is_context                           │
│  关联：已有 timeline？是否需要创建新目录？    │
│  编号：自动分配 EVT_XXX                     │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│  Step 5: 写入 timeline/                     │
│                                             │
│  ① 原始文件归档 → sources/YYYY-MM-DD/       │
│  ② 事件记录写入 → timeline/[entity_id]/    │
│  ③ 判断是否需要更新 entity snapshot         │
│  ④ 更新 entity meta.md（事件索引）          │
│  ⑤ 更新 index.md                            │
│  ⑥ 记录 log.md                             │
└─────────────────────────────────────────────┘
```

### Step 0：双语配对检测

> 每份文档入 sources/ 前，必须先完成语言识别和配对检测。

**规则A — 文件名检测（最优先）：**
```
检测同一日期目录下：
- 一方含中文字符，另一方为英文直译 → 配对
- 命名规律：一方含中文字符，另一方为英文直译

配对成功 → 分配共同 bilingual_pair_id
```

**规则B — 内容相似度检测（辅助）：**
```
如文件名无明显规律但同时同类型：
- 同一日期的两份文档
- document_type 相同
- 文档长度差异 < 20%
→ 视为潜在配对，人工确认后建立 bilingual_pair_id
```

**规则C — 配对后的写入规则：**
```
新文档入 sources/ 时：
① 检测是否有配对文档
② 如有：
   - 双方 doc_id 相同 bilingual_pair_id
   - 各自独立的前置字段 language 标识
③ 如无：bilingual_pair_id = null
④ 如英文版为合同/协议等法律文本：
   - 标记 is_authoritative: true（原始法律文本为准）
   - 翻译版对应标记 is_authoritative: false
```

**Step 0 输出：**
```yaml
bilingual_pair_id: DOC_YYYY_TYPE  # 或 null
language: zh | en
is_authoritative: true | false  # 仅合同类需要
```

### Step 3A：公告/新闻稿处理

**触发条件：** 文件名为"公告"、"新闻稿"、"通函"或 `document_type: announcement`

```
① 提取事件要素：
   - 涉及实体（公司/产品/人物）
   - 事件类型（见 event_type 分类表）
   - 公告日期 vs 生效日期

② 判断 is_state_change：
   - 新产品获批 → TRUE（状态变更）
   - 分拆公告 → TRUE（状态变更）
   - 高管任命 → TRUE（状态变更）
   - 业绩发布 → FALSE（数据更新）
   - 新闻报道（无新事实）→ FALSE（is_context）

③ 如 is_state_change = TRUE：
   - 检查 timeline/[entity_id]/ 是否已有该事件
   - 如有，追加到同一实体目录，更新 superseded_by
   - 如无，创建新事件文件

④ 如 is_data_update = TRUE：
   - 写入对应 entity 的 timeline
   - 标记 is_data_update = TRUE

⑤ 如 is_context = TRUE：
   - 仅归档到 sources/，不写入 timeline
   - 在 entities 页的"关联背景"中引用
```

### Step 3B：年报/半年报处理（重点）

**特点：** 年报信息量大，需要同时提取**数据**和**事件**

```
① 识别年报覆盖期间（YYYY年度 / YYYY半年度等）

② 提取所有事实性描述，按实体+维度分类：
   - 财务数据（营收/利润/研发）→ 写入对应 entity timeline
   - 产品里程碑 → 识别是否已有事件，无则创建
   - 市场描述（"唯一""首个"）→ 需记录 valid_until
   - 战略描述 → 写入 concept 页，不入 timeline

③ 关键原则：
   - 年报中的"事实性数字"属于数据更新（is_data_update）
   - 年报中的"里程碑事件"属于状态变更
   - 年报中的"opinion/展望"不写入任何结构化数据

④ 特殊处理——"绝对性表述"历史对比：
   - 发现"唯一/首个/最强"等表述时：
     → 在 event 中记录该表述 + document_date
     → 在 entity snapshot 的 valid_until 标注
     → 如果新版年报表述变了，旧表述自动失效
```

### Step 3C：法规/政策文件

```
① 识别政策性质（利好/利空/中性）
② 识别受影响实体
③ 写入对应 entity timeline，event_type = 法规政策
④ 判断影响写入 concept 页
```

### Step 3D：背景资料

```
① 仅归档到 sources/，不写入 timeline
② 在相关 entity/concept 页的"关联背景"节引用
③ 用于回答"请介绍XX的背景"类问题
```

### 事件 ID 分配规则

```
前缀：EVT_
编号：三位数字，从001开始，按 entity 分别计数
示例：
- EVT_001（实体A）= 实体A的第一个事件
- EVT_001（实体B）= 实体B的第一个事件

entity_id 与 event_id 组合 = 全局唯一
```

### 冲突处理规则

**同一实体、同一时间有多份文件？**
- 优先级：公告 > 年报 > 新闻报道
- 保留优先级最高的，其余归档为背景引用

**同一事件被多份文件描述？**
- 以最早发布的官方文件为准
- 后续文件引用同一事件，仅更新 event 中的 `additional_sources`

**矛盾表述？**
- 写入 event 时，在 `discrepancy` 字段注明
- entity snapshot 取最新描述，保留历史版本供参考

## QA 问答流程（适配事件溯源）

### 默认回答路径（快速查询）

```
① 识别实体 + 问题时间范围
② 读取 entity snapshot（当前状态）
③ 如问题涉及具体时间点 → 读取 timeline/ 下对应事件
④ 综合 snapshot + 时间轴事件，回答问题
⑤ 引用时标注来源事件 ID
```

### 时间旅行查询（历史视角）

用户问题示例：
- "站在某年年报发布时，市场对某业务的估值逻辑是什么？"
- "某产品在某年中有哪些已获批的适应症？"

```
① 确定时间锚点：某份具体年报/公告的日期
② 筛选 timeline 中 document_date <= 锚点的所有事件
③ 重建"当时"的实体状态
④ 回答时明确说明："以XXXX公告/报告发布时为准"
```

### 差异对比查询

用户问题示例：
- "某事件前后，市场对某业务的估值方法有什么变化？"

```
① 确定时间节点：关键事件日
② 聚类锚点前后各一个时间窗口的事件
③ 对比 snapshot 或计算关键指标变化
④ 输出结构化对比表
```

## 迁移指南（从旧架构升级）

已有知识库迁移至事件溯源架构的步骤：

```
Phase 1: 建立目录结构
- 创建 timeline/[entity_id]/ 目录
- 创建 entity.latest.md 快照

Phase 2: 事件抽取（批量）
- 遍历 sources/ 中所有文件
- 按 entity 归类，提取事件
- 生成历史事件文件（EVT_XXX_历史.md）

Phase 3: 生成实体快照
- 基于最新事件聚合生成 entity snapshot
- 将原有 entity.md 内容转为快照的一部分

Phase 4: 清理旧引用
- 将不再准确的内容移入 _archive/
- 更新所有 [[wikilinks]] 指向新结构

Phase 5: 验证
- 跑 lint 检查断链和孤立页面
- 抽样测试时间旅行查询
```

**迁移原则：**
- sources/ 原始文件不动
- 存量 entity 页内容转为历史快照保留
- timeline/ 的事件编号从 EVT_001 开始，与历史无关
- 迁移完成后，旧的"直接编辑 entity"流程废除，统一走 Ingest

---

*事件溯源架构 v1.0*
