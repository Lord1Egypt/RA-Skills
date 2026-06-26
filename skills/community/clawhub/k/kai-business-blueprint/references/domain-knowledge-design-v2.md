# Business Blueprint Skill: Domain-Knowledge 实体扩展设计 v2

**日期**: 2026-04-28
**状态**: 取代 v1（`domain-knowledge-entities-extension-design.md`）
**核心转变**: 从"schema 扩展"重新定位为"质量驱动"

---

## 一、为什么需要 v2

v1 设计把"高质量业务方案蓝图"当成了 schema 和渲染问题来解，但用户绘制蓝图的真实瓶颈不在表达能力，而在三个未解决的痛点：

1. **AI 不真懂业务**：v1 用关键词频率检测 blueprintType，"优化 ROI 策略"会被误判
2. **用户讲不清需求**：v1 一次性出图，用户只能改 JSON——但用户不会改 JSON
3. **没有迭代精炼**：v1 没有"草稿→反馈→修订"循环，第一版必然粗糙却没有进化路径

v1 投入分布也失衡：Phase 2/3 大量篇幅在循环依赖检测、关系语义校验、容错降级——这是防御性工程，对用户绘制质量几乎零增益。

v2 的核心论点：**蓝图质量 = 思考深度 × 迭代轮次 × 表达准确性**。schema 只影响第三项，而前两项才是杠杆。

---

## 二、操作化定义"高质量蓝图"

一份高质量业务方案蓝图必须满足：

| 维度 | 定义 | v2 是否解决 |
|------|------|-----------|
| **覆盖完整** | 业务关键维度都有体现（痛点/策略/规则/指标/实践/误区，或架构层） | ✅ hints + 必填检查 |
| **粒度合适** | 不过粗（笼统）也不过细（琐碎） | ✅ 自检反问 |
| **逻辑闭环** | 痛点↔策略↔指标三角对齐；规则约束策略 | ✅ 自检反问 + relations 必填 |
| **反映真实业务** | 实体名称与用户真实场景吻合 | ⚠️ 部分（澄清回合改善，根本依赖 LLM 能力） |
| **可用于沟通** | 视觉清晰，受众能快速理解 | ✅ 6 类基础渲染样式 |
| **支持迭代** | 用户能基于第一版继续改进 | ✅ --refine 命令 |

v2 不强求解决"反映真实业务"——这是 LLM 的语义理解能力，无法靠 skill 设计补全；只能通过澄清回合让用户主动校准。

---

## 三、核心策略：v1 vs v2 对照

| 维度 | v1 | v2 |
|------|----|----|
| 目标定位 | schema 扩展 | 质量驱动 |
| 第一性问题 | 实体表达力不足 | 用户思考深度不足 |
| 主要机制 | 6 类实体 + 关系类型 + validator + 渲染 | **澄清 + 自检 + 修订** 三件套 |
| blueprintType 检测 | 关键词频率匹配 | 意图抽取（自然语言摘要） |
| validator 重点 | 强校验关系完整性、循环依赖、语义合理性 | 强校验**用户思考完整性**（clarifyRequests 非空） |
| 渲染重点 | 容错降级、性能上限 | 自检状态可视化（让用户看见薄弱点） |
| 投入分布 | Phase 1: 4-6h / Phase 2: 6-10h / Phase 3: 7-11h | Phase 0: 6-8h（核心）/ Phase 1: 3-4h / Phase 2: 2-3h |
| 验收方式 | "准确率 >80%、渲染评分 >8/10"（占位） | 五个事后可量化代理指标 + 真实场景 |

---

## 四、三大质量驱动机制（Phase 0）

### 1. AI 澄清回合（Clarification Turn）

#### 设计目标

强制 AI 在第一轮提取后**暴露不确定性**，让用户主动校准，把"一次性出图"改为"对话式精炼"。

#### 数据流

```
[用户原始需求] 
    ↓
[AI 第一轮提取] → blueprint v1 + clarifyRequests[≥3]
    ↓
[用户回答] → context.clarifications
    ↓
[AI 第二轮提取] → blueprint v2（基于澄清细化）
```

#### Schema 变化

**复用现有字段**（`context.clarifyRequests` 在 common/seed.json 已存在），扩展其结构：

```json
{
  "context": {
    "clarifyRequests": [
      {
        "id": "clr-001",
        "targetEntityId": "pain-001",
        "question": "我把 'ROI 不稳' 识别为顶层痛点(level=1)，但你提的是症状还是根因？如果是症状，真正的根因可能是什么？",
        "options": [
          "症状 - 根因待补充",
          "根因 - 已是最深层"
        ],
        "rationale": "顶层痛点应是根因；如果是症状，建议追溯到根因后重新分层"
      }
    ],
    "clarifications": [
      {
        "clarificationId": "clr-001",
        "answer": "ROI 不稳是症状，根因是创意疲劳和受众饱和"
      }
    ]
  }
}
```

#### 强制规则

- **domain-knowledge 蓝图**：第一轮输出必须有 ≥3 条 `clarifyRequests`，否则 validator 报 error
- **每条 clarifyRequest 必须**：
  - `targetEntityId` 指向具体实体（非泛问）
  - `question` 必须包含具体内容（非"还有什么补充？"）
  - `rationale` 解释为什么问这个

#### 反问触发模式

AI 提取时按以下优先级生成 clarifyRequests：

1. **层级歧义**：识别为 level=1 的痛点/策略 → 反问"是否是根因/最高优先级"
2. **关系不完整**：strategy 没有对应 painPoint（缺 solves） → 反问"这条策略对应哪个痛点"
3. **指标缺失**：strategy 没有对应 metric（缺 measures） → 反问"怎么衡量它有效"
4. **行业 hints 未触发**：industryHints.knowledgeHints.checklist 中某主题未提取出实体 → 反问"是否需要补充 X 主题"
5. **粒度可疑**：实体名称过短（<4 字）或过长（>30 字） → 反问"是否合适"

最少触发 3 条，最多 5 条（避免轰炸）。

---

### 2. 实体自检反问（Self-Check）

#### 设计目标

对每个提取的实体附带"AI 的自我怀疑"，让用户在视觉上看见**哪些实体还没想清楚**。

#### Schema 变化

实体内增加可选 `_selfCheck` 字段（user-defined 字段，validator 不强制结构）：

```json
{
  "id": "pain-001",
  "name": "ROI 不稳",
  "entityType": "painPoint",
  "_selfCheck": {
    "passed": ["可观测", "受影响方明确"],
    "questions": [
      "是症状还是根因？— 待用户确认",
      "严重度判断依据是什么？"
    ]
  }
}
```

- `passed`：AI 已确认通过的检查项
- `questions`：AI 仍存疑的问题（非空 → 渲染时高亮）

#### 反问清单（写入 `references/knowledge-self-check.md`）

| Entity Type | 反问 |
|------|------|
| **painPoint** | 1. 是症状还是根因？<br>2. 严重度判断依据是什么（数据/感受/对标）？<br>3. 受影响的角色/部门是谁？ |
| **strategy** | 1. 对应哪个具体痛点（必须有 solves 关系）？<br>2. 执行前提是什么（资源/能力/时机）？<br>3. 怎么衡量它有效（必须有 measures 关系）？ |
| **rule** | 1. 规则来源是什么（平台/法规/内部）？<br>2. 违反后果具体是什么？<br>3. 约束哪些策略（必须有 enforces 关系）？ |
| **metric** | 1. 计算方式或基准值是什么？<br>2. 衡量哪个策略（必须有 measures 关系）？<br>3. 阈值的业务依据是什么？ |
| **practice** | 1. 频率/周期是多少？<br>2. 支撑哪个策略（必须有 requires 反向关系）？<br>3. 成功的衡量信号是什么？ |
| **pitfall** | 1. 导致什么痛点（必须有 causes 关系）？<br>2. 避免方式是什么？<br>3. 真实案例或数据支撑？ |

#### 渲染规则

- `_selfCheck.questions` 非空 → 实体节点加**黄色边框**（stroke: #F59E0B, width: 3）
- 角标加 "?"图标（位于实体右上角）
- 鼠标悬浮显示 questions 列表
- 视觉目的：让用户一眼看见"这几个还没想清楚"

---

### 3. 修订命令（Refine）

#### 设计目标

把"二轮深化"做成显式产品功能，而不是隐式期望。用户写自然语言反馈，AI 输出结构化 diff，用户逐条 accept/reject。

#### CLI 接口

```bash
python -m business_blueprint.cli refine \
  --blueprint /path/to/blueprint.json \
  --feedback "策略部分太浅，缺少出价策略；ROI 不稳应该拆成 ROAS 波动和获客成本上升两个具体痛点"
```

#### 输出 diff 结构

```json
{
  "diffId": "diff-20260428-001",
  "baseBlueprintRevisionId": "rev-20260428-01",
  "operations": [
    {
      "op": "modify",
      "path": "library.knowledge.painPoints[0].name",
      "old": "ROI 不稳",
      "new": "ROAS 波动"
    },
    {
      "op": "add",
      "path": "library.knowledge.painPoints[]",
      "value": {
        "id": "pain-002",
        "name": "获客成本上升",
        "entityType": "painPoint",
        "description": "..."
      }
    },
    {
      "op": "add",
      "path": "library.knowledge.strategies[]",
      "value": {
        "id": "str-003",
        "name": "动态出价策略",
        "entityType": "strategy"
      }
    },
    {
      "op": "delete",
      "path": "library.knowledge.pitfalls[2]"
    }
  ],
  "rationale": "用户反馈策略部分薄弱、痛点粒度过粗。拆分 ROI 不稳为两个具体痛点，新增动态出价策略以覆盖出价相关思考。"
}
```

#### 用户工作流

1. 用户跑 `refine` 得到 diff JSON
2. viewer 加载 diff（新视图模板 `views/diff-review.html`，**Phase 0 不做 viewer，先用 CLI 输出文本**）
3. 用户逐条 `accept` / `reject`
4. 应用通过的 operations，输出 `blueprint.v2.json`

#### Phase 0 范围限定

- ✅ CLI `refine` 命令
- ✅ AI prompt 设计（输出 diff JSON）
- ✅ diff 结构定义
- ✅ 应用 diff 的 patcher 逻辑
- ❌ Web viewer 集成（推迟）

---

## 五、Schema 极简扩展（Phase 1）

### 1. meta 字段

```json
{
  "meta": {
    "blueprintType": "domain-knowledge",
    "detectedIntent": "用户想了解跨境电商广告投放领域的 know-how，重点是痛点和策略，用于客户 pitch",
    "industry": "cross-border-ecommerce",
    "revisionId": "rev-20260428-01"
  }
}
```

- `blueprintType`：枚举 `architecture | domain-knowledge`，默认 `architecture`
- `detectedIntent`：**自然语言意图摘要**（≤80 字），AI 必填，用户可见可改

### 2. library.knowledge 块

```json
{
  "library": {
    "capabilities": [],
    "actors": [],
    "flowSteps": [],
    "systems": [],
    "knowledge": {
      "painPoints": [],
      "strategies": [],
      "rules": [],
      "metrics": [],
      "practices": [],
      "pitfalls": []
    }
  }
}
```

**约束**：
- `knowledge` 块在 `architecture` 蓝图中应为空或不存在
- `knowledge` 块在 `domain-knowledge` 蓝图中至少包含 1 个实体
- `domain-knowledge` 蓝图允许同时填充 architecture 实体（用于跨类型关联）
- 6 类预定义数组都可选；用户自定义实体类型数组允许（不校验数组名称）

### 3. 实体核心字段（强校验）

| 字段 | 类型 | 必填 | 校验规则 |
|------|------|------|----------|
| `id` | string | ✅ | 唯一，格式 `{prefix}-{seq}`（如 `pain-001`） |
| `name` | string | ✅ | 非空 |
| `entityType` | string | ✅ | 非空字符串（不强制 camelCase） |

### 4. 实体可选字段（不校验，纯文档建议）

- `description`、`severity`、`level`、`relatedCapabilityIds`、`platform`、`value`、`unit`、`frequency` 等
- 用户自定义字段一律放行

**v2 决策**：v1 中的 soft-schema 校验（severity 枚举、level 整数等）**全部推迟**到 Phase 3。理由：当前阶段不知道用户会真用什么字段，过早约束反而限制探索。

### 5. Relations 类型

| type | from → to | 说明 |
|------|-----------|------|
| `solves` | strategy → painPoint | 策略解决痛点 |
| `prevents` | practice → pitfall | 实践规避误区 |
| `measures` | metric → strategy | 指标衡量策略 |
| `enforces` | rule → strategy | 规则约束策略 |
| `requires` | strategy → practice | 策略依赖实践 |
| `causes` | pitfall → painPoint | 误区导致痛点 |
| `impacts` | painPoint → capability | 痛点影响能力（跨类型） |
| `supports` | strategy → capability | 策略支撑能力（跨类型） |
| `enforcedBy` | rule → system | 规则约束系统（跨类型） |
| `measuredBy` | metric → system | 指标监控系统（跨类型） |

**v2 决策**：validator **只校验 `type` 在白名单内 + `from`/`to` ID 存在**。语义合理性（如 `measures` 必须 metric→strategy）**推迟**到 Phase 3——这是渲染期或导出期更适合做的友好提示，而不是阻塞性校验。

---

## 六、blueprintType 检测：意图抽取替代关键词

### v1 的问题

```
用户需求包含 "know-how"、"领域知识"、"策略"、"痛点" ≥2 个 → domain-knowledge
```

误判案例：
- "优化 ROI 策略" → 触发（"策略"），但用户实际想看架构
- "审视痛点和系统瓶颈" → 触发（"痛点"），但混合需求

### v2 方案

AI 第一步必须输出 `detectedIntent`（自然语言摘要 ≤80 字），然后基于 intent 选 `blueprintType`：

#### Prompt 模板（写入 SKILL.md）

```
Step 1 — Intent Extraction:
Read the user's request. Output a single-sentence summary (max 80 chars) of what they want.
Example: "用户想要跨境电商广告领域的 know-how 大图，用于客户 pitch"
Save to meta.detectedIntent.

Step 2 — Blueprint Type Selection:
Based on detectedIntent, choose blueprintType:
- If intent describes domain knowledge, market insights, strategies, best practices → "domain-knowledge"
- If intent describes system architecture, IT design, technical blueprint → "architecture"
- If ambiguous, ask the user before proceeding (do NOT default silently).

Step 3 — User Visibility:
detectedIntent and blueprintType are written to meta. User can override either.
```

### 优势

- 误判时用户能看见"AI 以为你想要 X"，黑盒变白盒
- 比关键词匹配更鲁棒（LLM 自己做语义抽取，不依赖人工关键词清单）
- 模糊需求时强制询问，避免静默选错

---

## 七、hints 诚实化

### 问题

v1 plan 中 `retail/finance/manufacturing/seed.json` 的 knowledgeHints 是模板填充凑出来的（凭空补的"安全库存预警"、"反洗钱合规"等）。AI 提取质量被 hints 质量卡死，但用户不知道 hints 不可靠。

### v2 方案

每份 industry seed.json 的 knowledgeHints 标注 `_status` 字段：

```json
{
  "industryHints": {
    "knowledgeHints": {
      "_status": "template-only-not-domain-validated",
      "_disclaimer": "本 hints 由模板生成，未经领域专家验证。建议用户根据实际业务场景增删。",
      "title": "零售行业 know-how 关注点",
      "checklist": [...]
    }
  }
}
```

- `cross-border-ecommerce`：`_status: "depth-validated"`（已深度调研，作为黄金标准）
- `retail/finance/manufacturing`：`_status: "template-only-not-domain-validated"`
- `common`：无 knowledgeHints

### SKILL.md 配套规则

AI 在使用 `template-only` 状态的 hints 时，**必须在 detectedIntent 后追加一句免责声明**：

```
detectedIntent: "用户想要零售行业的 know-how 大图"
disclaimer: "我用的是模板版 hints（未经领域验证），请重点检查痛点/策略是否符合你的实际业务"
```

### 长期演进

P3 阶段提供 `--contribute-hints` 反向沉淀命令：用户产出蓝图后，可将本次提取的实体写回 hints 模板，形成"用户驱动的 hints 演进"。本文档不展开。

---

## 八、Validator 极简（Phase 2）

### v2 校验范围（核心字段，严格）

1. `meta.blueprintType` 在 `["architecture", "domain-knowledge"]`
2. `meta.detectedIntent` 必填且为字符串（domain-knowledge 蓝图）
3. `architecture` 蓝图：`library.knowledge` 应为空或不存在
4. `domain-knowledge` 蓝图：`library.knowledge` 至少 1 个实体
5. `domain-knowledge` 蓝图：`context.clarifyRequests` 至少 3 条
6. 每条 `clarifyRequest` 必须有 `targetEntityId` 指向 library 中存在的实体
7. 每个 knowledge 实体必须有 `id`、`name`、`entityType`
8. `id` 全局唯一
9. `relations` 中 `from`/`to` ID 必须存在
10. `relations.type` 必须在白名单内

### v2 不做的校验（推迟到 Phase 3）

- ❌ severity / level 数据类型校验
- ❌ entityType camelCase 命名规范
- ❌ 循环依赖检测
- ❌ 关系语义合理性（如 measures 必须 metric→strategy）
- ❌ 用户自定义字段类型校验

### 理由

这些是"用户已经在产出大量蓝图、需要稳定性"才有价值的工程。当前阶段还在"用户能不能产出有用蓝图"的验证期，不投。

---

## 九、Render 极简（Phase 2）

### v2 渲染范围

1. **6 类基础样式**（颜色 + 形状 + 图标），定义见 v1 设计第六章——保留
2. **自检状态可视化**（新增）：
   - `_selfCheck.questions` 非空 → 黄色边框 + ?角标
   - 鼠标悬浮显示 questions
3. **关系连线**：solves/prevents/measures 等 8-10 类关系的基础样式（实线/虚线/颜色）

### v2 不做的渲染（推迟到 Phase 3）

- ❌ entityType-based clustering 布局算法（用现有 freeflow 自由布局）
- ❌ 性能上限（>50 简化、>100 分页）
- ❌ 嵌套字段降级（>3 层显示为 `{...}`）
- ❌ 未知 entityType 的容错样式（用默认灰色样式即可，不算容错只算 fallback）
- ❌ severity 分级渲染（无 soft-schema 校验，severity 字段是用户自由文本）

### 理由

- 当前阶段实体数量少（10-30 个），现有 freeflow 自由布局够用
- 性能优化是真出现性能问题再做
- 容错降级是真出现崩溃再做

---

## 十、Phase 3 推迟清单（不在本设计范围）

| 项 | 触发条件 |
|----|---------|
| validator 关系语义合理性校验 | 用户报告"关系误用导致渲染异常" ≥3 次 |
| validator 循环依赖检测 | 用户报告"循环关系导致死循环" ≥1 次 |
| validator severity/level soft schema | 用户自定义字段普及，约 5+ 用户使用 |
| 渲染性能优化（>50 实体） | 实测渲染 >5s 或用户报告卡顿 |
| 渲染容错降级（嵌套 >3） | 实测崩溃或显示异常 |
| entityType-based clustering 布局 | 用户反馈"实体多了看不懂" |
| Web viewer 的 diff review 视图 | --refine 命令使用率 >30% |
| --contribute-hints 反向沉淀 | 跨境电商之外的行业有 5+ 真实蓝图 |

每项推迟工程，除非触发条件满足，否则不做。

---

## 十一、风险评估（与 v1 评审报告对照）

### v1 评审捕获的高危问题，v2 处理

| v1 问题编号 | v1 修复方式 | v2 处理 |
|---|---|---|
| 问题 1（关键词检测脆弱） | 加判断优先级 + 手动覆盖 | **重做为意图抽取**——根本解决 |
| 问题 4（混合蓝图缺失） | "可选添加 architecture 实体" | 保留 v1 修复，但澄清回合让用户主动选 |
| 问题 7（决策矛盾） | 同上 | 同上 |
| 问题 9（schema-first 兼容性） | 检查现有 validator | v2 新增字段全是 optional，向后兼容自动满足 |
| 问题 14（Phase 2 工时低估） | 调整估算 6-9h | **删掉了 v1 Phase 2 的复杂功能**——工时降到 2-3h |

### v1 评审中危问题，v2 处理

| v1 问题 | v2 处理 |
|---|---|
| 问题 2（扩展字段放行） | 推迟 soft-schema 到 Phase 3，承认风险 |
| 问题 3（freeflow 布局） | 推迟到 Phase 3 |
| 问题 6（relations 完整性） | 保留 ID 引用 + 类型白名单校验，**删掉**循环依赖、语义合理性 |
| 问题 10（entityType 命名） | 推迟，不强制 |
| 问题 15（Phase 3 难度） | **整个 Phase 3 推迟**，不在本设计范围 |
| 问题 16（向后兼容测试覆盖） | 测试设计（见独立文档）有完整回归测试 |

### v2 新增风险

| 风险 | 应对 |
|------|------|
| 澄清回合质量差，用户嫌烦 | L3 eval 五指标之一"澄清击中率 ≥60%"；不达标改设计 |
| 自检反问清单不全/过浅 | 反问表写入 references/，迭代版本号；用户反馈驱动更新 |
| --refine diff 不准确，用户拒绝率高 | L3 eval"修订接受率 ≥70%"；不达标说明 prompt 设计有问题 |
| LLM 不稳定，跨次提取差异大 | L2 eval 设计 fixture 测试；接受 ±10% 波动 |

---

## 十二、向后兼容保证

v2 所有新增字段都是 **optional**：

- `meta.blueprintType` 缺失 → 默认 `architecture`
- `meta.detectedIntent` 缺失 → 仅 domain-knowledge 蓝图必填
- `library.knowledge` 缺失 → architecture 蓝图正常
- `context.clarifyRequests` 缺失 → architecture 蓝图正常
- 实体的 `_selfCheck` 缺失 → 渲染时不加黄色边框，正常显示

**回归测试**：遍历 demos/ 下所有现有 architecture 蓝图，validator 必须 0 error，导出 SVG 与基线 diff 通过。详见测试设计文档。

---

## 十三、与 v1 设计文档的关系

- v1 设计文档（`domain-knowledge-entities-extension-design.md`）保留作为历史参考
- v1 评审报告（`domain-knowledge-design-adversarial-review.md`）保留
- v2 设计**取代** v1，本文档为 single source of truth
- v1 plan 文档（`plans/2026-04-28-domain-knowledge-entities-extension.md`）作废，由 v2 plan 取代

---

## 十四、设计审查清单

### Placeholder 扫描
- ✅ 无"TBD"/"TODO"/不完整章节

### 内部一致性
- ✅ 三件套设计 ↔ Schema 扩展 ↔ Validator 校验 一致
- ✅ Phase 0/1/2 边界清晰
- ✅ Phase 3 推迟项每项都有触发条件

### Scope 检查
- ✅ 设计聚焦质量驱动，砍掉所有未触发条件的复杂工程
- ✅ Phase 3 推迟清单显式列出，不偷偷塞回 Phase 0-2

### Ambiguity 检查
- ✅ "高质量蓝图"有操作化定义
- ✅ 三件套数据流明确
- ✅ blueprintType 检测从模糊关键词改为明确 intent 抽取

### 质量验证机制
- ✅ 不依赖主观打分，全部用代理指标（详见测试设计文档）
- ✅ Ship Gate 显式定义在 Phase 0 完工节点

---

## 十五、下一步

1. 用户审查本设计
2. 批准后阅读 v2 plan：`plans/2026-04-28-domain-knowledge-v2.md`
3. 阅读测试与 Eval 设计：`references/domain-knowledge-test-eval-design.md`
4. 按 Phase 0 → Phase 1 → Phase 2 顺序实施
5. Phase 0 完工后跑 L3 eval，五指标达门槛才进 Phase 1（否则改设计）

---

**设计完成日期**: 2026-04-28
**版本**: v2.0
**取代**: v1（`domain-knowledge-entities-extension-design.md`）
