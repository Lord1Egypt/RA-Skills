---
name: ProClaw-Partner-insight
description: 识别伴侣格局类型（丫鬟型/妃子型/皇后型），分析行为信号与误判点，提供关系影响评估与决策建议；当用户需要判断伴侣关系模式、分析伴侣是否拖垮或成就自己、制定关系决策时使用
author: ProClaw
website: www.proclaw.top
contact: wechat:Mr-zifang
version: 1.1
---

# 伴侣洞察

## 作者信息
- **作者**: ProClaw
- **网站**: www.proclaw.top
- **联系方式**: wechat:Mr-zifang

## 任务目标
- 本 Skill 用于:识别伴侣的核心格局类型（丫鬟型/妃子型/皇后型），通过行为信号判断伴侣是否在成就或拖垮用户，提供关系决策参考
- 能力包含:三种格局类型的定义、行为信号识别、常见误判点、结构化评估、动态跟踪、风险预警、决策支持
- 触发条件:用户询问伴侣类型、描述伴侣行为模式、表达关系困惑或需要关系决策建议时

## 前置准备
- 无特殊依赖
- 需要用户提供伴侣的具体行为描述、互动案例或关系现状

## 核心概念

### 格局类型定义

**丫鬟型**
- 核心特征:勤勤恳恳、任劳任怨、为家庭牺牲自我（传统"贤妻良母"）
- 心理驱动:恐惧失去、安全感不足、需要通过拉低伴侣来维持心理平衡
- 典型表现:抱怨陪伴时间、阻拦风险决策、控制欲增强

**妃子型**
- 核心特征:疯狂提升竞争力（颜值、身材、情商、社交、包装），精致展示
- 心理驱动:择偶竞争思维，宁愿在强者身边做妾也不陪弱者平庸一生
- 典型表现:完美展示无真实、关注利益交换、制造危机感

**皇后型**
- 核心特征:不可替代的战略价值，情绪稳定、社交调度、资源链接、判断力和定盘能力
- 心理驱动:接受现实和强者的复杂人性，不靠牺牲隐忍换位置
- 典型表现:共情解决问题、独立价值判断、校准方向能力

## 工具体系

### 脚本工具（scripts/）

#### 结构化评估脚本（assess_partner.py）
**功能**:根据六个维度打分，计算综合得分，判定类型和风险等级

**使用方法**:
```bash
python scripts/assess_partner.py --emotional [分数] --growth [分数] --independence [分数] --anchor [分数] --crisis [分数] --match [分数]
```

**参数说明**:
- emotional:情绪稳定性（1-10）
- growth:成长支持度（1-10）
- independence:价值独立性（1-10）
- anchor:自我价值锚点（1-10）
- crisis:危机应对能力（1-10）
- match:长期匹配度（1-10）

**输出**:综合得分、类型判定、风险等级、短板维度、改进建议

**评分标准**:见 [assets/tables/assessment-table.md](assets/tables/assessment-table.md)

#### 风险扫描脚本（scan_risk.py）
**功能**:根据危险信号清单扫描，判定风险等级

**使用方法**:
```bash
python scripts/scan_risk.py --red [数量] --orange [数量] --yellow [数量] --score [评估得分]
```

**参数说明**:
- red:红色信号数量（0-5）
- orange:橙色信号数量（0-5）
- yellow:黄色信号数量（0-5）
- score:评估得分（可选，0-10）

**输出**:风险等级、危险信号详情、应对策略、行动项

**危险信号清单**:见 [references/risk-warning-system.md](references/risk-warning-system.md)

#### 混合特征分析脚本（analyze_hybrid.py）
**功能**:根据特征权重分析混合类型，预测长期趋势

**使用方法**:
```bash
python scripts/analyze_hybrid.py --y [丫鬟型权重] --c [妃子型权重] --h [皇后型权重]
```

**参数说明**:
- y:丫鬟型权重（0-10）
- c:妃子型权重（0-10）
- h:皇后型权重（0-10）

**输出**:混合类型、主特征、副特征、长期趋势预测、改进可能性、切换触发条件

#### 决策支持脚本（support_decision.py）
**功能**:根据五维度数据匹配决策矩阵，输出决策建议

**使用方法**:
```bash
python scripts/support_decision.py --score [评估得分] --duration [关系时长月数] --improvement [改进可能性] --cost [沉没成本] --risk [风险等级]
```

**参数说明**:
- score:评估得分（0-10）
- duration:关系时长（月）
- improvement:改进可能性（1-10）
- cost:沉没成本（1-10）
- risk:风险等级（1-4，1=低，2=中，3=高，4=极高）

**输出**:决策类型、场景策略、执行策略、综合建议

**决策矩阵**:见 [references/decision-matrix.md](references/decision-matrix.md)

### 参考文档（references/）

#### 结构化评估模型（assessment-model.md）
**用途**:多维度量化评估伴侣格局

**包含内容**:
- 六个评估维度的详细定义
- 1-10分评分标准
- 综合得分计算方法
- 类型判定标准
- 风险等级判定

**何时读取**:需要量化评估时，参考评分标准

#### 交互式决策树（decision-tree.md）
**用途**:场景化问题导航

**包含内容**:
- 六大路径（初期识别、现有关系评估、伪装验证、对比决策、危机决策、混合特征分析）
- 场景化问题节点
- 可操作的下一步建议

**何时读取**:不确定如何开始分析时

#### 动态跟踪框架（tracking-framework.md）
**用途**:系统性行为跟踪，识别变化趋势

**包含内容**:
- 四个跟踪维度
- 月度记录模板
- 趋势分析方法
- 三级预警机制

**何时读取**:需要跟踪关系变化时

#### 混合特征识别器（hybrid-identifier.md）
**用途**:识别混合类型伴侣

**包含内容**:
- 四种混合类型定义
- 特征权重分析方法
- 切换触发条件
- 长期趋势预测框架

**何时读取**:伴侣行为复杂不符合单一类型时

#### 风险预警系统（risk-warning-system.md）
**用途**:危险信号扫描和风险等级判定

**包含内容**:
- 15个危险信号（红色5个、橙色5个、黄色5个）
- 风险等级判定标准
- 扫描方法
- 应对策略

**何时读取**:需要扫描危险信号时

#### 决策支持矩阵（decision-matrix.md）
**用途**:多维度、场景化的决策参考

**包含内容**:
- 五个决策维度
- 决策矩阵
- 五种决策类型
- 场景化策略

**何时读取**:需要做关系决策时

### 静态资源（assets/）

#### 记录模板（templates/）

**月度记录模板**（monthly-record.md）
- 每月记录关键事件和行为模式
- 包含评估得分、风险扫描、决策建议
- 为动态跟踪框架提供数据支持

**季度对比模板**（quarterly-comparison.md）
- 每3个月对比分析关系变化趋势
- 识别改进或退化
- 临界点识别和趋势预测

#### 评估表格（tables/）

**评估打分表**（assessment-table.md）
- 六个维度的详细评分标准
- 综合得分计算方法
- 类型判定和风险等级判定

**信号对照表**（signal-checklist.md）
- 三种类型的行为信号对照
- 误判点区分标准
- 快速识别指南

#### 常见问题（faq/）

**常见问题FAQ**（common-questions.md）
- 36个常见问题与解答
- 覆盖基础概念、工具使用、决策相关、具体场景等多个方面

## 使用流程

### 场景1:新伴侣类型判断
1. 观察伴侣行为3-6个月
2. 对照行为信号识别（见signal-checklist.md）
3. 使用评估脚本打分（见assess_partner.py）
4. 若表现完美担心伪装，使用动态跟踪框架观察

### 场景2:现有关系评估
1. 使用评估脚本打分（见assess_partner.py）
2. 使用风险扫描脚本（见scan_risk.py）
3. 根据得分决定是否改进或止损
4. 若改进，使用月度记录模板跟踪

### 场景3:混合特征分析
1. 识别各类型特征出现频率
2. 使用混合特征分析脚本（见analyze_hybrid.py）
3. 分析切换触发条件
4. 预测长期趋势

### 场景4:关系决策
1. 收集五维度数据（评估得分、关系时长、改进可能性、沉没成本、风险等级）
2. 使用决策支持脚本（见support_decision.py）
3. 参考决策矩阵场景策略
4. 制定执行计划

## 使用示例

### 示例1:量化评估
**场景**:在一起1年，想量化评估关系健康度

**步骤**:
1. 使用评估打分表（assessment-table.md）对照评分
2. 执行脚本:
```bash
python scripts/assess_partner.py --emotional 7 --growth 8 --independence 7 --anchor 8 --crisis 7 --match 8
```

**结果**:综合得分7.45分，皇后型，低风险

**建议**:珍惜关系，深化战略伙伴关系

### 示例2:风险扫描
**场景**:感觉关系不对劲，识别危险信号

**步骤**:
1. 对照危险信号清单（risk-warning-system.md）
2. 发现1个红色信号（极端控制行为）、2个橙色信号（频繁情绪爆发、阻拦发展）
3. 执行脚本:
```bash
python scripts/scan_risk.py --red 1 --orange 2 --yellow 0 --score 4.5
```

**结果**:极高风险，建议立即止损

### 示例3:混合特征分析
**场景**:伴侣行为复杂，有时支持有时控制

**步骤**:
1. 识别特征权重:丫鬟型5分、妃子型3分、皇后型2分
2. 执行脚本:
```bash
python scripts/analyze_hybrid.py --y 5 --c 3 --h 2
```

**结果**:丫鬟型与妃子型混合，长期趋势暴露为丫鬟型

**建议**:使用动态跟踪框架观察6个月，参考决策支持矩阵

### 示例4:决策支持
**场景**:在一起18个月，评估得分4.5分，不知道该继续还是止损

**步骤**:
1. 收集数据:评估得分4.5分、关系时长18个月、改进可能性5分、沉没成本6分、风险等级3分
2. 执行脚本:
```bash
python scripts/support_decision.py --score 4.5 --duration 18 --improvement 5 --cost 6 --risk 3
```

**结果**:积极改进

**建议**:深度沟通，明确改进目标和边界，使用动态跟踪框架记录

## 资源索引

### 脚本工具
- 见 [scripts/assess_partner.py](scripts/assess_partner.py)(用途:结构化评估，参数:六个维度得分1-10)
- 见 [scripts/scan_risk.py](scripts/scan_risk.py)(用途:风险扫描，参数:危险信号数量+评估得分)
- 见 [scripts/analyze_hybrid.py](scripts/analyze_hybrid.py)(用途:混合特征分析，参数:三种类型权重)
- 见 [scripts/support_decision.py](scripts/support_decision.py)(用途:决策支持，参数:五维度数据)

### 参考文档
- 见 [references/assessment-model.md](references/assessment-model.md)(何时读取:需要量化评估时)
- 见 [references/decision-tree.md](references/decision-tree.md)(何时读取:不确定如何开始分析时)
- 见 [references/tracking-framework.md](references/tracking-framework.md)(何时读取:需要跟踪关系变化时)
- 见 [references/hybrid-identifier.md](references/hybrid-identifier.md)(何时读取:伴侣行为复杂时)
- 见 [references/risk-warning-system.md](references/risk-warning-system.md)(何时读取:需要扫描危险信号时)
- 见 [references/decision-matrix.md](references/decision-matrix.md)(何时读取:需要做关系决策时)

### 静态资源
- 见 [assets/templates/monthly-record.md](assets/templates/monthly-record.md)(用途:每月记录模板)
- 见 [assets/templates/quarterly-comparison.md](assets/templates/quarterly-comparison.md)(用途:季度对比模板)
- 见 [assets/tables/assessment-table.md](assets/tables/assessment-table.md)(用途:评估打分表)
- 见 [assets/tables/signal-checklist.md](assets/tables/signal-checklist.md)(用途:信号对照表)
- 见 [assets/faq/common-questions.md](assets/faq/common-questions.md)(用途:常见问题解答)

## 注意事项
- 本 Skill 提供洞察框架和识别标准，不替代专业心理咨询
- 所有判断基于用户提供的行为描述，需具体场景具体分析
- 格局类型不是固定标签，可能存在混合特征和阶段变化
- 时间维度是关键验证指标，短期表现可能存在伪装
- 脚本工具需要基于长期观察数据，避免过早下结论
- 最终决策权在用户，Skill 仅提供结构化分析工具
