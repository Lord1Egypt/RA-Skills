# 认知图谱构建协议 (Cognitive Graph Protocol)

> 本文档定义了如何从文本中抽取实体、概念、关系，构建结构化知识图谱。

---

## 1. 抽取 Prompt 模板

### 基础抽取

```
你是一个认知本体引擎，请从以下文本中提取知识三元组。

【输入文本】
{input_text}

【领域上下文】
{domain_context}

请提取以下内容并返回 JSON：

1. 实体（entities）：文本中出现的关键实体
   - id: 唯一标识符（e001, e002...）
   - name: 实体名称
   - type: 实体类型（见下方分类体系）
   - attributes: 额外属性（别名、分类、数值等）

2. 概念（concepts）：抽象概念或分类
   - id: 唯一标识符（c001, c002...）
   - name: 概念名称
   - description: 概念定义
   - examples: 具体示例

3. 关系（relations）：实体/概念之间的关联
   - source: 源实体/概念 ID
   - target: 目标实体/概念 ID
   - type: 关系类型（见下方关系类型）
   - weight: 置信度（0.0-1.0）
   - evidence: 支持该关系的原文证据

4. 元信息（metadata）
   - source_text: 原文摘要
   - domain: 识别到的领域
   - confidence: 整体抽取置信度

返回格式：
```json
{
  "entities": [...],
  "concepts": [...],
  "relations": [...],
  "metadata": {...}
}
```
```

### 增量抽取（已有图谱时）

```
你是一个认知本体引擎，需要在已有知识图谱基础上进行增量更新。

【已有图谱摘要】
实体数量：{entity_count}
关键实体：{top_entities}

【新输入文本】
{input_text}

请执行以下操作：

1. 新增：从新文本中识别已有图谱中不存在的新实体和关系
2. 补充：为新/旧实体补充新发现的属性
3. 关联：建立新实体与已有实体之间的关联
4. 冲突：如发现与已有知识矛盾的信息，标记为 conflict 并说明

返回增量更新 JSON：
```json
{
  "add_entities": [...],
  "add_relations": [...],
  "update_entities": [...],
  "conflicts": [...]
}
```
```

---

## 2. 实体类型分类体系

### 通用类型（适用于所有领域）

| 类型 | 说明 | 示例 |
|------|------|------|
| `organization` | 组织机构 | 公司、政府机构、研究机构 |
| `person` | 人物 | 个人、角色 |
| `product` | 产品/服务 | 软件、硬件、服务方案 |
| `technology` | 技术 | 技术栈、方法论、工具 |
| `concept` | 抽象概念 | 商业模式、管理理念 |
| `event` | 事件 | 会议、发布、里程碑 |
| `document` | 文档 | 报告、政策、论文 |
| `location` | 地点 | 城市、地区、园区 |
| `metric` | 指标 | KPI、数值、比例 |
| `role` | 角色/职能 | 岗位、职责 |

### 领域扩展类型

**能源领域：**
| 类型 | 说明 | 示例 |
|------|------|------|
| `energy_source` | 能源类型 | 光伏、风电、储能 |
| `market_mechanism` | 市场机制 | 电力现货、容量补偿 |
| `policy` | 政策法规 | 补贴政策、准入规则 |
| `equipment` | 能源设备 | PCS、BMS、变压器 |

**医疗领域：**
| 类型 | 说明 | 示例 |
|------|------|------|
| `disease` | 疾病 | 炎症性肠病、糖尿病 |
| `treatment` | 治疗手段 | FMT、药物治疗 |
| `biomarker` | 生物标志物 | 肠道菌群多样性 |
| `institution` | 医疗机构 | 医院、诊所 |

**AI 领域：**
| 类型 | 说明 | 示例 |
|------|------|------|
| `model` | AI 模型 | GPT-4、Claude、GLM |
| `algorithm` | 算法 | Transformer、RAG |
| `dataset` | 数据集 | 训练集、基准测试 |

---

## 3. 关系类型定义

### 核心关系类型

| 关系 | 方向 | 说明 | 示例 |
|------|------|------|------|
| `is_a` | 单向 | 继承/分类 | BMS → is_a → 电池管理系统 |
| `part_of` | 单向 | 组成关系 | 电芯 → part_of → 电池包 |
| `includes` | 单向 | 包含关系 | 储能系统 → includes → PCS |
| `related_to` | 双向 | 关联关系 | 储能 → related_to → 电力现货 |
| `depends_on` | 单向 | 依赖关系 | EMS → depends_on → 数据采集 |
| `causes` | 单向 | 因果关系 | 政策补贴 → causes → 市场增长 |
| `contradicts` | 双向 | 矛盾关系 | 高成本 → contradicts → 快速普及 |
| `similar_to` | 双向 | 相似关系 | 磷酸铁锂 → similar_to → 三元锂 |
| `regulated_by` | 单向 | 监管关系 | 储能项目 → regulated_by → 电力条例 |
| `located_in` | 单向 | 位置关系 | 储能电站 → located_in → 浙江省 |

### 关系强度（weight）

| 权重范围 | 含义 | 判断标准 |
|----------|------|---------|
| 0.9-1.0 | 确定性 | 文本直接陈述，无歧义 |
| 0.7-0.8 | 高置信 | 文本强烈暗示，有逻辑支撑 |
| 0.5-0.6 | 中等置信 | 推断得到，需进一步验证 |
| 0.3-0.4 | 低置信 | 间接关联，不确定性高 |
| 0.1-0.2 | 待验证 | 仅基于假设或弱关联 |

---

## 4. 图谱构建流程

```
输入文本
  │
  ▼
┌─────────────┐
│ 预处理       │  清洗、分句、领域识别
└─────┬───────┘
      ▼
┌─────────────┐
│ 实体识别     │  基于 entity types 体系识别
└─────┬───────┘
      ▼
┌─────────────┐
│ 关系抽取     │  基于 relation types 体系建立连接
└─────┬───────┘
      ▼
┌─────────────┐
│ 增量合并     │  与已有图谱去重合并
└─────┬───────┘
      ▼
┌─────────────┐
│ 置信度评估   │  为每条关系打分
└─────┬───────┘
      ▼
输出知识图谱 JSON
```

---

## 5. 质量检查清单

构建图谱后，逐项检查：

- [ ] 实体是否有唯一 ID 且无重复
- [ ] 关系的 source/target 是否对应已存在的实体
- [ ] 每条关系是否有 evidence（原文证据）
- [ ] 关系方向是否正确（causes 是有向的，related_to 是双向的）
- [ ] weight 是否合理（直接陈述 > 推断 > 假设）
- [ ] 是否有孤立实体（没有任何关系连接的实体）
- [ ] 增量更新时是否标记了冲突

---

## 6. 输出格式规范

### 最小化输出（快速分析）

```json
{
  "entities": [
    {"id": "e001", "name": "储能系统", "type": "concept"}
  ],
  "relations": [
    {"source": "e001", "target": "e002", "type": "includes", "weight": 0.9}
  ]
}
```

### 完整输出（深度分析）

```json
{
  "version": "1.0.0",
  "domain": "energy_storage",
  "updated_at": "2026-03-30T16:00:00+08:00",
  "entities": [
    {
      "id": "e001",
      "name": "储能系统",
      "type": "concept",
      "attributes": {
        "category": "能源基础设施",
        "aliases": ["ESS", "Energy Storage System"],
        "subtypes": ["电化学储能", "机械储能", "热储能"]
      }
    }
  ],
  "relations": [
    {
      "source": "e001",
      "target": "e002",
      "type": "includes",
      "weight": 0.9,
      "evidence": "储能系统主要由电池组、PCS、BMS和EMS组成",
      "timestamp": "2026-03-30T16:00:00+08:00"
    }
  ],
  "metadata": {
    "total_entities": 23,
    "total_relations": 34,
    "source_text_hash": "abc123",
    "session_id": "sess_001"
  }
}
```
