---
name: industry-map
description: |
  生成完整产业图谱。支持深度调研（30+搜索）、自动发现一级分类、5-7层层级深度。
  触发场景：用户请求生成产业图谱、产业链分析、行业分类图谱、产业结构梳理等。
---

# Industry Map Generator

Generate comprehensive industry chain maps from any input head node with deep research.

## Usage

```
/industry-map <头节点名称> [--output <目录>] [--template <CSV模板路径>] [--no-md]
```

**Examples:**
```
/industry-map 航空航天
/industry-map 量子科技 --output D:\project\docs
/industry-map 新能源 --template D:\docs\新能源产业图谱_template.csv
/industry-map 人工智能
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| 头节点名称 | Yes | - | The head node name to generate map from |
| --output | No | ./docs/<头节点名称> | Output directory for generated files |
| --template | No | assets/default_template.csv | Reference CSV template file path |
| --no-md | No | false | Skip generating process record MD file |

## Output Requirements

### CSV File: `<头节点名称>产业图谱_full.csv`

**Structure:** 8 columns (id, name, level, parent_id, parent_name, path, classification, decision_basis)

**Flexible Scale (Based on Industry Complexity):**
| 指标 | 要求 | 说明 |
|------|------|------|
| 总行数 | **灵活** | 根据产业复杂度调整，一般400-1200行 |
| 最大层级 | 5-7层 | 深度细分到具体技术/产品 |
| 一级分类 | **通过调研发现** | 不预设数量，由产业内在结构决定 |
| 层级深度 | 渐进式 | 每层细分5-15个子节点 |

### MD File: `<头节点名称>产业图谱生成过程记录.md`

**Required Sections:**
1. 初始需求理解
2. 第一版设计方案（含一级分类发现过程）
3. 问题识别与调研过程
4. 关键节点划分依据
5. 完整参考来源列表（含URL）

## CSV Format

**Reference Template:** `assets/default_template.csv`（航空航天产业图谱完整样例）

这是一个标准参考样例，展示了完整的产业图谱结构，包括：
- 层级深度示例（1-7层）
- decision_basis 列的实际用法
- 节点命名规范
- ID 格式规范

**ID Format:** `1`, `1-1`, `1-1-1`, `1-1-1-1`, `1-1-1-1-1`, `1-1-1-1-1-1`

**Columns:**
| Column | Description |
|--------|-------------|
| id | 节点唯一标识，层级递进格式 |
| name | 节点名称，纯中文或中英文混合，不含标点 |
| level | 层级深度 (1-7) |
| parent_id | 父节点ID |
| parent_name | 父节点名称 |
| path | 完整路径，用/分隔 |
| classification | 分类类型（可选） |
| decision_basis | 决策依据/技术说明 |

**decision_basis Column Usage:**
- 添加技术说明（如：主流技术、下一代技术）
- 标注应用场景（如：航天应用、户用分布式）
- 记录分类依据（如：按技术原理分、按应用领域分）

## Execution Steps

### Step 1: Understand Requirements
- Parse head node name and parameters
- Load template (user-provided via `--template` or default at `assets/default_template.csv`)
- **Search for existing industry maps in project for reference**

### Step 2: Discover First-Level Categories (CRITICAL)

**Do NOT assume first-level categories. Discover them through research:**

1. **National Standards Research (2-3 searches)**
   - 国民经济行业分类
   - 产业在国家标准中的定义和范围
   - 相关行业代码归属

2. **Government Policy Research (3-5 searches)**
   - 国家级产业政策文件
   - "十五五"相关规划
   - 产业发展指导意见

3. **Industry Association Research (2-3 searches)**
   - 行业协会分类标准
   - 产业联盟组织结构
   - 学术界分类方法

4. **Market Structure Research (5-10 searches)**
   - 头部企业业务板块
   - 产业链上下游关系
   - 市场细分方式

**Output:** 基于调研确定的一级分类列表，每个分类需有权威来源支持

### Step 3: Deep Research Per Category (30+ searches total)

**For each discovered first-level category:**
1. 技术原理/产品大类调研
2. 关键零部件/材料调研
3. 应用场景/细分市场调研
4. 技术发展趋势调研

### Step 4: Design Classification
- Follow "what it is" first, then "where it's used"
- Principle: Same technical principle? Similar application environment? Unified industry standard?
- **Aim for comprehensive coverage, flexible node count**

### Step 5: Generate CSV
- Each node is an independent term (no commas/semicolons in name)
- Use standard industry terminology
- No specific company/institution/product names
- **Drill down to Level 5-7 for key categories**
- **Use decision_basis column for technical notes**

### Step 6: Generate MD Record
- Research process documentation
- First-level category discovery rationale
- Decision rationale for key nodes
- Complete reference list with URLs

## Critical Rules

### Node Representation Specification (CRITICAL)

#### 1. 节点名称格式规范

**基本格式：**
- 纯中文或中英文混合
- 不含标点符号（逗号、分号、顿号、引号等）
- 不含特殊字符（@、#、$、%等）
- 不含括号内容说明（如：电池(储能用) → 错误）

**正确示例：**
```
多晶硅、单晶硅片、TOPCon电池、IGBT模块、永磁同步电机
```

**错误示例：**
```
多晶硅（改良西门子法）、硅片,电池片、TOPCon/PERC电池、电机（高效）
```

#### 2. 节点内容类型（允许的节点类型）

| 节点类型 | 说明 | 示例 |
|----------|------|------|
| 技术原理 | 基础技术/工艺原理 | 直拉法、区熔法、气相沉积 |
| 产品类别 | 产品分类/型号 | 单晶硅片、多晶硅片、N型电池 |
| 零部件 | 组成部件 | 燃烧室、涡轮叶片、转子 |
| 材料 | 原材料/辅助材料 | 多晶硅、银浆、EVA胶膜 |
| 工艺方法 | 生产/加工工艺 | 改良西门子法、PECVD |
| 设备类型 | 生产设备分类 | 单晶炉、切片机、丝网印刷机 |
| 应用场景 | 应用领域（作为分类维度） | 集中式电站、分布式电站 |
| 系统类型 | 系统/子系统分类 | 飞控系统、导航系统 |
| 服务类型 | 服务分类 | 运维服务、检测服务 |

#### 3. 节点禁止内容（绝对禁止）

**3.1 禁止具体企业/品牌名称**
```
❌ 错误：华为逆变器、隆基绿能、宁德时代电池、比亚迪刀片电池
✅ 正确：组串式逆变器、单晶组件、磷酸铁锂电池、电池包
```

**3.2 禁止具体机构名称**
```
❌ 错误：中科院光伏所、清华大学研究院、国家电网
✅ 正确：光伏研究机构、高校研究院、电网运营商
```

**3.3 禁止具体产品型号/品牌产品名**
```
❌ 错误：HPBC电池、ABC电池、麒麟电池、4680电池
✅ 正确：背接触电池、无主栅电池、方形磷酸铁锂电池、圆柱电池
```

**3.4 禁止具体平台/系统名称**
```
❌ 错误：阿里云能源平台、华为云、特斯拉超级工厂
✅ 正确：能源管理平台、云服务平台、电池生产基地
```

**3.5 禁止营销性描述**
```
❌ 错误：高效电池、领先技术、核心零部件
✅ 正确：N型电池、TOPCon电池、关键零部件
```

**3.6 禁止含数量/参数的节点**
```
❌ 错误：210mm硅片、182mm硅片、1500V逆变器
✅ 正确：大尺寸硅片、常规尺寸硅片、高压逆变器
```

#### 4. 节点粒度控制

**粒度判断原则：**
- 同一层级的节点粒度应一致
- 子节点粒度应比父节点更细
- 最细粒度到具体技术/零件类型即可，不必到具体参数

**粒度层级参考：**

| 层级 | 粒度示例 | 说明 |
|------|----------|------|
| Level 2 | 太阳能光伏、风能发电 | 产业子领域 |
| Level 3 | 光伏材料、光伏电池 | 产品/技术大类 |
| Level 4 | 硅材料、薄膜材料 | 材料类型 |
| Level 5 | 多晶硅、单晶硅棒 | 具体材料 |
| Level 6 | 改良西门子法多晶硅、直拉法单晶硅 | 工艺/技术 |
| Level 7 | （如需细分）具体工艺参数 | 最细粒度 |

#### 5. 节点命名规范对照表

| 场景 | ❌ 错误命名 | ✅ 正确命名 |
|------|------------|------------|
| 企业产品 | 华为HiSilicon芯片 | 手机SoC芯片 |
| 品牌技术 | 隆基HPBC技术 | 背接触电池技术 |
| 型号规格 | 182mm硅片 | 大尺寸硅片 |
| 行业术语 | TOPCon（未翻译） | TOPCon电池（带分类词） |
| 缩写术语 | HJT（单独使用） | HJT异质结电池 |
| 复合概念 | 光伏组件及系统 | 光伏组件（拆分为独立节点） |
| 含说明 | 钙钛矿（新型材料） | 钙钛矿（说明放decision_basis） |
| 营销词 | 高效PERC电池 | PERC电池 |
| 时代词 | 第三代半导体 | 宽禁带半导体 |

#### 6. 特殊情况处理

**6.1 行业通用缩写**
- 广泛认知的缩写可直接使用：LED、IGBT、CPU
- 新兴/专业缩写需加说明词：HJT异质结电池、POE胶膜

**6.2 技术代际**
```
❌ 第一代光伏、第二代光伏、第三代光伏
✅ 晶硅电池、薄膜电池、钙钛矿电池（按技术类型分）
```

**6.3 尺寸/规格差异**
- 如果尺寸差异构成技术路线差异 → 可作为节点
- 如果仅是规格参数差异 → 不应作为节点

**6.4 中英文混合**
- 国际通用术语可保留英文：GaN器件、SiC模块
- 中文有标准译名的用中文：氮化镓器件、碳化硅模块

### Classification Principles
1. **"What it is" first**: Classify by technical/product nature
2. **"Where it's used" second**: Subdivide by application when needed
3. **Judgment criteria**:
   - Same technical principle? → Merge
   - Similar application environment? → Merge
   - Unified industry standard? → Merge

### First-Level Category Discovery

**CRITICAL: Do NOT use preset templates. Each industry has unique structure.**

**Discovery process:**
1. Start with broad searches: "<头节点> 产业链"、"<头节点> 分类"
2. Consult authoritative sources: GB/T 4754, government policies
3. Identify natural boundaries in the industry
4. Validate categories against multiple sources

**Common patterns (use as reference, NOT template):**
- 制造型产业: 研发设计 → 原材料 → 零部件 → 整机/系统 → 应用/服务
- 技术型产业: 基础研究 → 技术开发 → 产品化 → 应用场景
- 服务型产业: 基础设施 → 服务内容 → 服务对象 → 配套支撑

### Granularity Guidelines

**Progressive depth:**
- Level 2: 产业链环节/技术领域
- Level 3: 产品大类/技术分支
- Level 4: 具体产品/技术类型
- Level 5: 部件/工艺/材料
- Level 6: 零件/技术细节
- Level 7: 具体参数/工艺方法

**Use decision_basis at deeper levels:**
- Level 5-7 节点应填写 decision_basis
- 说明技术特点、应用场景、分类依据

## Research Sources Priority

1. **Official/Government**
   - National Bureau of Statistics (GB/T 4754)
   - NDRC, MIIT policies
   - Industry development plans

2. **Industry Associations**
   - China Federation of Industry
   - Sector-specific associations

3. **Research Institutions**
   - CAICT, CAE reports
   - Industry white papers

4. **Market Data**
   - Listed company reports
   - Industry analysis reports
   - Securities research

## Quality Checklist

Before completing:
- [ ] First-level categories discovered through research (not assumed)
- [ ] Each category has authoritative source support
- [ ] Node count reflects industry complexity
- [ ] Deep levels (5-7) have decision_basis notes
- [ ] No company/institution/product names
- [ ] Technical terminology is accurate
- [ ] Classification follows "what it is" first principle
- [ ] All sources documented with URLs

## Error Handling

- If head node is ambiguous, ask clarifying questions
- If template file not found, use default template at `assets/default_template.csv`
- If output directory doesn't exist, create it
- If research yields insufficient data, report limitations
- **If first-level categories unclear, conduct more research**

## Notes

- This skill generates ONE industry map at a time
- For batch generation, invoke multiple times
- Research depth is **comprehensive** (30+ searches)
- **First-level categories must be discovered, not assumed**
- All sources must be documented with URLs
- **Reference existing industry maps in project for depth guidance**
