# Relation Ontology

关系是知识图谱的骨架。当前关系只有 `type` + `target_id`，语义太薄。本文定义关系的完整语义结构、核心关系类型目录、以及三元关系的处理策略。

## 1. 关系的语义属性

扩展后的关系结构：

```json
{
  "type": "works_at",
  "target_id": "org-00002",
  "direction": "forward",
  "cardinality": "N:1",
  "temporal": {"start": "2019-01", "end": null},
  "evidence": "doc-00123",
  "confidence": "high"
}
```

各属性语义：

| 属性 | 值域 | 语义 | 默认值 |
|------|------|------|--------|
| `type` | 关系类型名 | 关系的语义标签，英文动词或动词短语 | (必需) |
| `target_id` | 实体 ID | 关系指向的目标实体 | (必需) |
| `direction` | forward / reverse / bidirectional | forward: 主语→宾语（张三 works_at 蓝天信息）；reverse: 宾语→主语（从 target 看回来）；bidirectional: 双向对等（partner_of） | forward |
| `cardinality` | 1:1 / 1:N / N:1 / N:M | 从源实体到目标实体的基数约束。N:1 表示多个源可指向同一目标（多人可 works_at 同一公司） | N:M |
| `temporal` | `{start, end}` | 关系有效期。start/end 为 ISO 日期或 null。null start = 起始不详，null end = 当前有效 | null（无时间信息） |
| `evidence` | 实体 ID | 支撑该关系的来源实体（通常是 Document 或 Event），用于溯源 | null |
| `confidence` | high / medium / low | 关系可信度。high = 文档明确记载；medium = 从上下文推断；low = 间接证据或过时信息 | medium |

**向后兼容**：所有新增字段均可选（null = 未知）。旧数据中只有 type + target_id 的关系继续有效，视为 direction=forward, confidence=medium, 其余 null。

**示例**（真实数据）：

```json
// per-00001 张三 在蓝天信息工作
{
  "type": "works_at",
  "target_id": "org-00002",
  "direction": "forward",
  "cardinality": "N:1",
  "temporal": {"start": null, "end": null},
  "confidence": "high"
}

// org-00002 蓝天信息 是星辰集团国际的子公司
{
  "type": "subsidiary_of",
  "target_id": "org-00001",
  "direction": "forward",
  "cardinality": "N:1",
  "temporal": {"start": "2020-09", "end": null},
  "evidence": "evt-00001",
  "confidence": "high"
}
```

## 2. 核心关系类型目录

按源实体类型分组，列出最常见的关系。

### Person 相关

| 关系 | 方向 | 目标 | 基数 | 时间性 | 示例 |
|------|------|------|------|--------|------|
| `works_at` | Person → Org | Organization | N:1 | 有（在职期间） | 张三 works_at 蓝天信息 |
| `leads` | Person → Org | Organization | N:1 | 有 | 李四 leads 蓝天信息 |
| `member_of` | Person → Org | Organization | N:M | 有 | 孙九 member_of 市场业务部 |
| `participates_in` | Person → Project | Project | N:M | 有 | 陈七 participates_in 某IT系统项目 |
| `manages` | Person → Project | Project | 1:N | 有 | 王五 manages 某升级项目 |
| `authored` | Person → Document | Document | 1:N | 无 | 张三 authored 某战略项目战略报告 |
| `knows` | Person → Person | Person | N:M | 无（双向） | 同事/合作关系 |

### Organization 相关

| 关系 | 方向 | 目标 | 基数 | 时间性 | 示例 |
|------|------|------|------|--------|------|
| `subsidiary_of` | Org → Org | Organization | N:1 | 有 | 蓝天信息 subsidiary_of 星辰集团 |
| `partner_of` | Org ↔ Org | Organization | N:M | 有（双向） | 蓝天信息 partner_of 某机场 |
| `competitor_of` | Org ↔ Org | Organization | N:M | 无（双向） | 蓝天信息 competitor_of CompetitorA |
| `customer_of` | Org → Org | Organization | N:M | 有 | 某航空公司 customer_of 蓝天信息 |
| `regulates` | Org → Org | Organization | 1:N | 无 | IATA regulates 星辰集团 |

### Project 相关

| 关系 | 方向 | 目标 | 基数 | 时间性 | 示例 |
|------|------|------|------|--------|------|
| `contracted_by` | Project → Org | Organization | N:1 | 有 | 某IT系统项目 contracted_by 某国际机场 |
| `delivered_to` | Project → Org | Organization | N:M | 有 | 某AI产品 delivered_to 中小企业客户群 |
| `uses_methodology` | Project → Methodology | domain type | N:M | 无 | 某战略项目 uses_methodology BLM |

### Task 相关

| 关系 | 方向 | 目标 | 基数 | 时间性 | 示例 |
|------|------|------|------|--------|------|
| `belongs_to` | Task → Project | Project | N:1 | 无 | 升级方案编制 belongs_to 某升级项目 |
| `assigned_to` | Task → Person | Person | N:1 | 有 | 某IT系统实施 assigned_to 周八 |
| `depends_on` | Task → Task | Task | N:M | 无 | 需求文档 depends_on 调研完成 |
| `blocks` | Task → Task | Task | N:M | 无 | 审批未过 blocks 开发启动 |

### Event 相关

| 关系 | 方向 | 目标 | 基数 | 时间性 | 示例 |
|------|------|------|------|--------|------|
| `related_to` | Event → Project/Org | any | N:M | 无 | 蓝天信息并入星辰集团国际 related_to 星辰集团国际 |
| `has_participant` | Event → Person | Person | N:M | 无 | 某行业大会 has_participant 张三 |
| `produces` | Event → Task/Doc/Note | any | 1:N | 无 | 评审会 produces 修改任务 |

### Document 相关

| 关系 | 方向 | 目标 | 基数 | 时间性 | 示例 |
|------|------|------|------|--------|------|
| `belongs_to` | Doc → Project | Project | N:1 | 无 | 战略报告 belongs_to 某战略项目 |
| `authored_by` | Doc → Person | Person | N:1 | 无 | 战略报告 authored_by 张三 |
| `references` | Doc → Doc | Document | N:M | 无 | 07号文档 references 技术底座方案 |
| `describes` | Doc → any | any | N:M | 无 | 公司介绍 describes 蓝天信息 |

### Goal 相关

| 关系 | 方向 | 目标 | 基数 | 时间性 | 示例 |
|------|------|------|------|--------|------|
| `set_by` | Goal → Org/Project | Org or Project | N:1 | 有 | 国际化目标 set_by 蓝天信息 |
| `owned_by` | Goal → Person | Person | N:1 | 有 | AI内训目标 owned_by 张三 |
| `measured_by` | Goal → Task | Task | 1:N | 无 | 份额提升 measured_by 客户拓展任务 |
| `driven_by` | Goal → Note/Event | Note or Event | N:M | 无 | 转型目标 driven_by 市场现状分析 |

### Note 相关

| 关系 | 方向 | 目标 | 基数 | 时间性 | 示例 |
|------|------|------|------|--------|------|
| `about` | Note → any | any | N:M | 无 | 业务占比数据 about 蓝天信息 |
| `extracted_from` | Note → Document | Document | N:1 | 无 | 核心劣势 extracted_from 公司介绍文档 |
| `authored_by` | Note → Person | Person | N:1 | 无 | 洞察 authored_by 张三 |

## 3. 三元关系处理

有些关系涉及第三方。例如：蓝天信息通过某IT系统合同向某机场提供IT服务。

**策略一：拆成二元关系 + 共享实体**

将三元关系 (A, 通过C, 服务B) 拆为：
- A → C: `signs`（蓝天信息签订 某IT系统合同）
- C → B: `serves`（合同服务于某机场）
- A → B: `delivered_to`（蓝天信息交付给某机场）

中间实体 C（合同/协议）可建模为 Document 或 Event。

**策略二：via 属性**

关系上加 `via` 字段，适合不想为中间实体单独建模的场景：

```json
{
  "type": "serves",
  "target_id": "org-00005",
  "via": "evt-00007",
  "confidence": "high"
}
```

含义：蓝天信息 serves 某国际机场，via 某IT系统合同签订事件。

**选择标准**：
- 中间实体有独立属性需要记录（金额、日期、条款）→ 策略一，建独立实体
- 中间实体只是关系的背景信息 → 策略二，用 via 属性
- 拿不准 → 先用策略二，后续需要时再升级为策略一

**示例**（真实场景）：

```json
// 策略二：张三通过某战略项目为蓝天信息制定AI战略
// per-00001 的 relations 中：
{
  "type": "advises",
  "target_id": "org-00002",
  "via": "task-00005",
  "confidence": "high"
}

// 策略一：蓝天信息通过外派协议为星辰集团国际提供某IT系统实施
// 外派协议建为 doc-NNNNN：
// org-00002 → doc-NNNNN: signs
// doc-NNNNN → org-00024: serves
// org-00002 → org-00024: delivered_to
```
