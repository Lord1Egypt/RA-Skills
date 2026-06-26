# Business Blueprint Skill 优化方案

## 问题诊断

### 现状分析

**现有skill定位**：系统架构蓝图生成器
- 实体类型：capabilities（能力）、actors（角色）、flowSteps（流程）、systems（系统）
- 输出形式：架构分层图、泳道流程图、系统支撑关系图
- 适用场景：售前方案设计、IT系统规划、业务流程梳理

**缺失需求**：业务领域know-how知识图谱
- 痛点挑战、关键策略、平台规则、数据指标、最佳实践、常见误区
- 用于展示"我们懂这个领域"的专业度
- 客户pitch时需要业务洞察，而非技术架构

### 根本原因

skill设计时将"业务蓝图"等同于"系统架构蓝图"，实体定义固化在IT系统视角：
- `systems` 实体强制映射到技术架构层（客户端层、网关层、业务服务层）
- 缺失"策略要素"、"行业规则"、"数据基准"等业务洞察实体
- AI只能按IT架构思维提取实体，无法生成领域知识图谱

---

## 设计方案对比

### 方案A：扩展实体类型（最小改动）

**改造思路**：
在现有`library`中新增实体类型：
```json
{
  "library": {
    "capabilities": [],
    "actors": [],
    "flowSteps": [],
    "systems": [],
    // 新增实体类型
    "painPoints": [
      {"id": "pain-001", "name": "ROI不稳", "description": "广告投放ROI波动大，缺乏稳定增长路径", "severity": "high"}
    ],
    "strategies": [
      {"id": "str-001", "name": "测款节奏", "description": "3天测款周期，预算分配策略", "applicableCapabilityIds": ["cap-004"]}
    ],
    "platformRules": [
      {"id": "rule-001", "name": "Facebook政策红线", "description": "禁止误导性宣传、过度夸大效果", "riskLevel": "critical"}
    ],
    "metrics": [
      {"id": "met-001", "name": "ROAS基准", "value": ">3.0", "unit": "ratio", "benchmarkContext": "欧美市场"}
    ],
    "bestPractices": [
      {"id": "bp-001", "name": "素材迭代周期", "description": "每7天测试新素材版本，避免疲劳"}
    ],
    "pitfalls": [
      {"id": "pit-001", "name": "过度依赖单一平台", "description": "Facebook封号后业务瘫痪风险", "impact": "critical"}
    ]
  }
}
```

**优点**：
- 兼容现有JSON schema和export逻辑，改动最小
- 一个蓝图可以同时包含架构和know-how

**缺点**：
- 实体职责混淆，一个JSON既要画架构图又要画知识图谱
- 导出视图选择复杂化（需要判断显示哪些实体类型）
- 与现有schema文档的"实体概览表"冲突（需要重新编写schema文档）

---

### 方案B：引入蓝图类型区分（路由层改造）

**改造思路**：
在SKILL.md中引入显式的蓝图类型参数：
```bash
python scripts/business_blueprint/cli.py --plan blueprint.json --type architecture
python scripts/business_blueprint/cli.py --plan blueprint.json --type domain-knowledge
```

两种类型使用不同的schema和hints：
- `--type architecture`：使用现有实体体系（capabilities/actors/flowSteps/systems）
- `--type domain-knowledge`：使用新的实体体系（painPoints/strategies/rules/metrics/practices/pitfalls）

**优点**：
- 职责清晰，互不干扰
- 每种类型有独立的hints模板和导出视图
- schema文档可以分别编写

**缺点**：
- 需要用户显式指定类型（增加使用门槛）
- 需要双倍维护成本（两套schema、两套模板、两套导出逻辑）
- 不符合skill的"渐进式披露"设计原则（AI应该自动判断意图）

---

### 方案C：轻量级schema扩展（推荐方案）

**改造思路**：
保持核心schema不变，新增可选的`knowledge`块：

```json
{
  "version": "1.0",
  "meta": {
    "title": "...",
    "industry": "retail",
    "blueprintType": "architecture",  // 新增字段：默认"architecture"，可选"domain-knowledge"或"hybrid"
    "revisionId": "...",
    "lastModifiedAt": "...",
    "lastModifiedBy": "ai"
  },
  "context": {...},
  "library": {
    // 保留现有实体（架构类）
    "capabilities": [],
    "actors": [],
    "flowSteps": [],
    "systems": [],
    // 新增可选块（know-how类）
    "knowledge": {
      "painPoints": [],
      "strategies": [],
      "rules": [],
      "metrics": [],
      "practices": [],
      "pitfalls": []
    }
  },
  "relations": [],
  "views": [],
  "editor": {...},
  "artifacts": {}
}
```

**AI意图判断逻辑**（写在SKILL.md）：
```
用户需求关键词匹配：
- "架构图"、"系统设计"、"IT规划" → blueprintType = "architecture"，只填充library核心实体
- "know-how"、"领域知识"、"业务洞察"、"最佳实践"、"行业玩法" → blueprintType = "domain-knowledge"，只填充knowledge块
- 混合需求（同时提到架构和策略） → blueprintType = "hybrid"，同时填充两类实体
```

**导出视图路由逻辑**（在export_routes.py中）：
```python
if blueprintType == "architecture":
    使用现有视图模板（poster/swimlane/freeflow）
elif blueprintType == "domain-knowledge":
    使用新的knowledge视图模板（knowledge-graph/knowledge-cards）
elif blueprintType == "hybrid":
    分页渲染（第一页架构图，第二页知识图谱）
```

**优点**：
- 不破坏现有架构蓝图能力（向后兼容）
- AI自动判断意图，无需用户显式参数（符合渐进式披露）
- 同一个JSON schema，不同视图模板（维护成本低）
- 可以支持混合蓝图（架构+know-how并存）

**缺点**：
- 需要新增knowledge块的schema文档
- 需要开发新的导出视图模板

---

## 推荐方案C的详细设计

### 一、schema扩展设计

#### 1. meta字段扩展

```json
{
  "meta": {
    "blueprintType": "architecture"  // 新增，枚举值：architecture | domain-knowledge | hybrid
  }
}
```

#### 2. library.knowledge实体定义

新增`knowledge`块，包含6类know-how实体：

| 实体类型 | 定义 | 示例数量 | 必填字段 |
|---------|------|---------|---------|
| **painPoints** | 痛点挑战 | 3-8 | id, name, description, severity |
| **strategies** | 关键策略 | 3-10 | id, name, description, applicableCapabilityIds |
| **rules** | 平台/政策规则 | 3-8 | id, name, description, riskLevel |
| **metrics** | 数据指标/基准 | 3-10 | id, name, value, unit, benchmarkContext |
| **practices** | 最佳实践 | 3-10 | id, name, description |
| **pitfalls** | 常见误区 | 3-8 | id, name, description, impact |

#### 3. knowledge实体字段详细定义

**painPoints（痛点）**
```json
{
  "id": "pain-001",
  "name": "ROI不稳",
  "description": "广告投放ROI波动大，缺乏稳定增长路径",
  "severity": "high",  // 枚举：low | medium | high | critical
  "relatedCapabilityIds": ["cap-004", "cap-005"]  // 可选，关联到能力
}
```

**strategies（策略）**
```json
{
  "id": "str-001",
  "name": "测款节奏策略",
  "description": "3天测款周期，预算分配70%测款+30%放量",
  "applicableCapabilityIds": ["cap-004"],  // 可选，应用到哪些能力
  "prerequisites": ["数据分析能力"]  // 可选，前置条件
}
```

**rules（规则）**
```json
{
  "id": "rule-001",
  "name": "Facebook广告政策红线",
  "description": "禁止误导性宣传、过度夸大效果、虚假折扣",
  "riskLevel": "critical",  // 枚举：low | medium | high | critical
  "platform": "Facebook Ads",  // 可选，适用平台
  "penalty": "账户封禁"  // 可选，违规后果
}
```

**metrics（指标）**
```json
{
  "id": "met-001",
  "name": "ROAS基准",
  "value": ">3.0",
  "unit": "ratio",
  "benchmarkContext": "欧美市场，电商类目",
  "calculationMethod": "GMV / Ad Spend"  // 可选，计算公式
}
```

**practices（最佳实践）**
```json
{
  "id": "bp-001",
  "name": "素材迭代周期",
  "description": "每7天测试新素材版本，CTR下降10%时立即更换",
  "frequency": "weekly",  // 可选，执行频率
  "successMetric": "CTR提升15%"  // 可选，成功指标
}
```

**pitfalls（误区）**
```json
{
  "id": "pit-001",
  "name": "过度依赖单一平台",
  "description": "只投放Facebook，平台封号后业务瘫痪",
  "impact": "critical",  // 枚举：low | medium | high | critical
  "avoidanceStrategy": "多平台分散投放，预算占比不超过60%"  // 可选，规避建议
}
```

---

### 二、hints模板扩展

#### 1. 行业hints增加know-how checklist

修改`templates/{industry}/seed.json`：

```json
{
  "industryHints": {
    "title": "零售行业蓝图关注点",
    "checklist": [...],  // 现有的架构类hints
    "knowledgeHints": {  // 新增块
      "title": "零售行业know-how关注点",
      "checklist": [
        "痛点：库存积压、客流下滑、会员流失、POS效率低",
        "策略：会员分层运营、智能补货、导购赋能、全渠道融合",
        "规则：食品安全合规、价格欺诈风险、数据隐私法规",
        "指标：坪效基准、客单价目标、会员复购率、员工人效",
        "最佳实践：陈列迭代周期、促销节奏、会员召回时机",
        "误区：过度依赖促销、忽视会员运营、数据孤岛"
      ]
    }
  }
}
```

#### 2. 为跨境电商新建industry模板

新建`templates/cross-border-ecommerce/seed.json`：

```json
{
  "industryHints": {
    "title": "跨境电商广告投放know-how关注点",
    "checklist": [],  // 空列表，架构类hints可选
    "knowledgeHints": {
      "title": "跨境电商广告投放know-how",
      "checklist": [
        "痛点：ROI不稳、素材疲劳、平台封号、库存积压、汇率风险",
        "策略：测款节奏、出价策略、受众分层、再营销触发时机、预算动态分配",
        "规则：Facebook政策红线、Google Quality Score、TikTok审核要点、Amazon合规要求",
        "指标：ROAS基准(>3.0)、CPA阈值、CTR基准(>1.5%)、LTV测算",
        "最佳实践：素材迭代周期(7天)、测款预算分配(70%测款)、再营销触发时机(浏览>3次)",
        "误区：过度依赖单一平台、忽视合规风险、数据孤岛、盲目放量、忽视LTV"
      ]
    }
  }
}
```

---

### 三、导出视图设计

#### 1. 新增knowledge视图模板

新建`references/knowledge-view-templates/`目录：

**knowledge-graph.md**：知识图谱视图
- 布局：中心发散式，painPoints为核心节点
- 连线：painPoints → strategies → practices → metrics
- 视觉：按severity/riskLevel分级颜色（critical=红，high=橙，medium=黄，low=绿）
- 交互：点击节点展开详细描述卡片

**knowledge-cards.md**：卡片式视图
- 布局：分6列（痛点/策略/规则/指标/实践/误区）
- 每列内按severity排序
- 每个卡片显示name + description + 关联信息
- 支持导出为PPT单页

#### 2. export_routes.py路由逻辑

```python
def select_export_route(blueprint):
    blueprint_type = blueprint.get("meta", {}).get("blueprintType", "architecture")

    if blueprint_type == "architecture":
        # 现有路由逻辑
        return select_architecture_route(blueprint)
    elif blueprint_type == "domain-knowledge":
        # 新路由：knowledge优先
        return "knowledge-graph"  # 或 "knowledge-cards"
    elif blueprint_type == "hybrid":
        # 混合路由：双视图
        return "hybrid-view"
    else:
        # fallback
        return "freeflow"
```

---

### 四、SKILL.md改造

#### 1. AI意图判断指南

在SKILL.md的"How to Generate a Blueprint"章节前插入：

```markdown
## Blueprint Type Detection

AI must detect user intent before entity extraction:

| Intent keywords | Blueprint type | Entity focus |
|----------------|---------------|-------------|
| "架构图"、"系统设计"、"IT规划"、"技术蓝图" | `architecture` | capabilities, actors, flowSteps, systems |
| "know-how"、"领域知识"、"业务洞察"、"最佳实践"、"行业玩法"、"痛点"、"策略" | `domain-knowledge` | knowledge块（painPoints/strategies/rules/metrics/practices/pitfalls） |
| 混合需求（同时提到架构和策略） | `hybrid` | 两类实体同时提取 |

Default behavior:
- If unclear, default to `architecture` (backward compatibility)
- If industryHints contains `knowledgeHints`, hint AI to also extract knowledge entities
```

#### 2. Step 2改造

```markdown
### Step 2: Extract entities from source text

**If blueprintType = "architecture"**:
Using the user's source material AND the industry hints checklist, extract:
- capabilities, actors, flowSteps, systems
  - See `references/entities-schema.md` for definitions

**If blueprintType = "domain-knowledge"**:
Using the user's source material AND the knowledge hints checklist, extract:
- painPoints, strategies, rules, metrics, practices, pitfalls
  - See `references/knowledge-schema.md` for definitions

**If blueprintType = "hybrid"**:
Extract both architecture and knowledge entities
```

---

### 五、实施步骤

#### Phase 1：Schema扩展（向后兼容）

1. 修改`scripts/business_blueprint/templates/common/seed.json`，新增`meta.blueprintType`字段（默认值"architecture"）
2. 新建`references/knowledge-schema.md`，定义knowledge块6类实体
3. 修改`references/entities-schema.md`，在"实体概览表"中新增knowledge块说明
4. 修改JSON schema validator，允许`library.knowledge`可选块

#### Phase 2：Hints模板扩展

1. 修改所有industry seed.json（common/finance/manufacturing/retail），新增`industryHints.knowledgeHints`块
2. 新建`templates/cross-border-ecommerce/seed.json`（跨境电商专属模板）
3. 新建`templates/ad-tech/seed.json`（广告技术专属模板）

#### Phase 3：导出视图开发

1. 新建`references/knowledge-view-templates/knowledge-graph.md`（知识图谱模板设计文档）
2. 新建`references/knowledge-view-templates/knowledge-cards.md`（卡片式模板设计文档）
3. 修改`business_blueprint/export_routes.py`，增加knowledge路由判断
4. 开发knowledge视图渲染器（HTML/SVG输出）

#### Phase 4：SKILL.md改造

1. 在SKILL.md开头新增"Blueprint Type Detection"章节
2. 修改"Step 2: Extract entities"章节，增加分支逻辑
3. 新增"Export Formats"章节的knowledge视图说明
4. 新增"Industry Selection"表的跨境电商、广告技术行业

---

## 改造清单

### 必须改造的文件

| 文件 | 改动内容 | 优先级 |
|------|---------|--------|
| `scripts/business_blueprint/templates/common/seed.json` | 新增meta.blueprintType字段 | P0 |
| `references/entities-schema.md` | 新增knowledge块说明 | P0 |
| 新建 `references/knowledge-schema.md` | 定义knowledge实体字段 | P0 |
| `SKILL.md` | 新增Blueprint Type Detection章节 | P0 |
| `scripts/business_blueprint/templates/retail/seed.json` | 新增knowledgeHints块 | P1 |
| `scripts/business_blueprint/templates/finance/seed.json` | 新增knowledgeHints块 | P1 |
| `scripts/business_blueprint/templates/manufacturing/seed.json` | 新增knowledgeHints块 | P1 |
| 新建 `templates/cross-border-ecommerce/seed.json` | 跨境电商专属模板 | P1 |
| 新建 `references/knowledge-view-templates/knowledge-graph.md` | 知识图谱视图设计 | P2 |
| 新建 `references/knowledge-view-templates/knowledge-cards.md` | 卡片式视图设计 | P2 |
| `scripts/business_blueprint/export_routes.py` | 新增knowledge路由逻辑 | P2 |

### 可选改造（后续迭代）

- 新建 `templates/ad-tech/seed.json`（广告技术行业模板）
- 新建 `templates/logistics/seed.json`（物流行业模板）
- 开发混合视图渲染器（architecture + knowledge并存）
- 开发知识图谱交互式编辑器（点击节点展开详情）

---

## 验证测试用例

### 测试1：向后兼容性

输入：
```
生成企业管理系统的架构蓝图
```

预期：
- blueprintType = "architecture"
- 只填充library核心实体（capabilities/actors/flowSteps/systems）
- 导出视图为现有模板（poster/swimlane/freeflow）
- JSON schema验证通过

### 测试2：纯knowledge蓝图

输入：
```
生成跨境电商广告投放的领域know-how大图，包含痛点、策略、平台规则、数据指标
```

预期：
- blueprintType = "domain-knowledge"
- 只填充library.knowledge块（painPoints/strategies/rules/metrics/practices/pitfalls）
- 导出视图为knowledge-graph或knowledge-cards
- industry自动选择"cross-border-ecommerce"

### 测试3：混合蓝图

输入：
```
生成跨境电商广告投放方案，既要系统架构，又要业务策略know-how
```

预期：
- blueprintType = "hybrid"
- 同时填充architecture实体和knowledge实体
- 导出视图为双页（第一页架构图，第二页知识图谱）
- 或者单页分区域显示

---

## 风险评估

### 低风险

- schema向后兼容（默认blueprintType="architecture"，现有调用不受影响）
- hints模板扩展不影响现有行业模板
- AI意图判断写在SKILL.md，不修改Python代码逻辑

### 中风险

- 导出视图路由逻辑需要修改export_routes.py（需要测试回归）
- knowledge实体字段定义可能与capabilities产生混淆（需要在schema文档中明确区分）

### 高风险

- 无（方案C避免了双schema的维护成本，也没有破坏性改动）

---

## 时间估算

- Phase 1（Schema扩展）：2-3小时
- Phase 2（Hints模板）：3-4小时
- Phase 3（导出视图）：8-10小时（需要开发新渲染器）
- Phase 4（SKILL.md改造）：1-2小时

总计：14-19小时（约2-3个工作日）

---

## 后续迭代建议

1. **知识图谱编辑器**：让用户可以在HTML viewer中点击节点，展开详情卡片，添加新的know-how节点
2. **行业know-how库**：沉淀各行业的know-how模板库（例如跨境电商的常见痛点、策略清单）
3. **know-how版本管理**：支持know-how的演化记录（例如Facebook政策规则的历史变更）
4. **know-how与架构联动**：在架构图中标注对应know-how（例如某个系统旁边显示"规避XX风险的最佳实践"）