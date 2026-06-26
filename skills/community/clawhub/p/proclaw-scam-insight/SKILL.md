---
name: ProClaw-Scam-insight(骗局洞察者)
description: 基于不确定性与风险转移理论，识别金融骗局模式、分析收割机制、提供反收割策略；当用户需要判断投资是否靠谱、分析骗局原理或学习如何避免被收割时使用
author: ProClaw
website: www.proclaw.top
contact: wechat:Mr-zifang
---

# 骗局洞察

## 任务目标
- 本 Skill 用于：识别金融骗局模式、分析收割机制的本质结构、提供反收割决策框架
- 能力包含：底层公理理解、骗局系统拆解、风险结构分析、反收割策略执行
- 触发条件：用户询问投资是否靠谱、分析某项目是否骗局、学习如何避免被收割、理解骗局背后的机制

## 前置准备
- 依赖说明：
  - python: pandas==2.0.0, numpy==1.24.0, matplotlib==3.7.0
- 认知准备：接受"不确定性是底层常量"这一核心公理

## 操作步骤

### 标准流程

#### 步骤1：识别需求缺口（最隐蔽但最致命）
判断对方是否在制造"需求缺口"：
- 是否在放大你对不确定性的恐惧？（银行不安全、通胀、错过机会）
- 是否在制造焦虑？（不投就后悔、机会流失）
- 是否在暗示"你是少数幸运儿"？

如果存在以上信号，说明你被当作"韭菜"定位了。

#### 步骤2：分析确定性叙事（核心判断点）
对方提供的"确定性解决方案"是否包含以下关键词：
- "稳定收益" "年化固定" "保本" "可预测"
- "低风险高回报" "内部渠道" "专家背书"
- "不用懂""跟着就行""别人已经赚了"

只要出现这些词，**已经违背金融本质**。

#### 步骤3：拆解风险结构（必须回答五个问题）
对于任何投资机会，你必须强制自己回答：
1. **收益从哪里来？**（是谁亏的钱？还是透支未来？）
2. **风险在哪里？**（识别被包装、被隐藏的部分）
3. **谁在承担风险？**（如果你不知道，那一定是你）
4. **最坏情况是什么？**（会不会让你出局？）
5. **如果我错了，代价是多少？**（单次错误是否致命？）

任何一个问题答不出来，说明你在被利用。

#### 步骤4：识别收割节点（检查是否进入收割路径）
对照收割系统的七个节点判断当前状态：
- 节点1：需求缺口是否被制造
- 节点2：确定性方案是否被提供
- 节点3：认知门槛是否被降低（"不用懂"）
- 节点4：信任闭环是否建立（小收益→复利幻觉→加大投入）
- 节点5：资金是否开始聚集
- 节点6：风险是否在悄悄转移
- 节点7：流动性是否濒临断裂

如果已经进入节点4-7，说明收割正在发生。

#### 步骤5：执行反收割决策（基于五个控制变量）
基于以下五个变量做出决策：
1. **不确定性承受能力**：能不能接受波动？不能则不入场
2. **认知深度**：是否看懂了收益来源和风险结构？看不懂则不入局
3. **时间维度**：是短期情绪驱动还是长期结构主导？短期不参与
4. **资金位置**：你赚的是谁的钱？不知道则是对手盘
5. **决策来源**：是自主判断还是接受叙事？后者立即撤退

反收割行动：
- 不追求"确定性"，追求"正期望"
- 不"All in"，控制仓位确保单次错误不出局
- 不听故事，只看结构和对手盘
- 不追涨杀跌，反人性执行

### 量化工具调用

#### 凯利公式计算器
**用途**：计算最优投资仓位比例

**调用示例**：
```bash
# 对称盈亏（胜率60%，盈利100%，亏损100%）
python scripts/kelly_criterion.py --win-rate 0.6 --win-amount 100 --loss-amount 100

# 非对称盈亏（胜率40%，盈利50%，亏损10%）
python scripts/kelly_criterion.py --win-rate 0.4 --win-amount 50 --loss-amount 10 --conservative 0.25
```

#### 风险指标计算器
**用途**：计算夏普比率、最大回撤、VaR、索提诺比率

**调用示例**：
```bash
# 使用价格序列计算所有指标
python scripts/risk_metrics.py --prices '[100,105,110,108,112,115,113,118]'

# 使用收益率序列计算
python scripts/risk_metrics.py --returns '[0.05,0.0476,-0.0182,0.037,0.0268,-0.0174,0.0442]'
```

#### 骗局风险评分系统
**用途**：计算CRS（骗局风险）、LRS（流动性风险）和综合风险评分

**调用示例**：
```bash
# 高风险案例
python scripts/scam_risk_scorer.py --revenue-source 0 --risk-identification 0 --cognitive-threshold 0 --liquidity 0 --information 0 --withdrawal-difficulty 0 --lock-period 0 --order-depth 0 --slippage 0

# 中风险案例
python scripts/scam_risk_scorer.py --revenue-source 1 --risk-identification 1 --cognitive-threshold 1 --liquidity 1 --information 1 --withdrawal-difficulty 1 --lock-period 2 --order-depth 2 --slippage 2
```

#### 决策矩阵评估
**用途**：评估骗局风险判断矩阵和投资机会评估矩阵

**调用示例**：
```bash
# 骗局风险矩阵评估
python scripts/decision_matrix.py --matrix-type scam --scores '{"revenue_source":0,"risk_identification":0,"cognitive_threshold":0,"trust_building":0,"liquidity":0,"information_transparency":0}'

# 投资机会矩阵评估
python scripts/decision_matrix.py --matrix-type investment --scores '{"expected_value":4,"risk_control":3,"liquidity":4,"information_transparency":3,"time_match":4}'
```

#### 流动性分析工具
**用途**：分析订单簿、流动性需求和供给、流动性风险

**调用示例**：
```bash
# 基本订单簿分析
python scripts/liquidity_analyzer.py --bid-price 10.00 --ask-price 10.05 --bid-volume 10000 --ask-volume 5000

# 完整流动性分析
python scripts/liquidity_analyzer.py --bid-price 10.00 --ask-price 10.05 --bid-volume 10000 --ask-volume 5000 --panic-sell-volume 30000 --normal-volume 5000 --available-funds 10000
```

#### 可视化工具
**用途**：生成风险热力图、骗局网络拓扑图、资金流向追踪图、决策树可视化

**调用示例**：
```bash
# 风险热力图
python scripts/visualization.py --type risk-heatmap --data '{"risks":{"high":80,"medium":15,"low":5}}' --output risk_heatmap.png

# 网络拓扑图
python scripts/visualization.py --type network-topology --data '{"nodes":["A","B","C","D"],"edges":[["A","B"],["B","C"],["C","D"]]}' --output network_topology.png
```

#### 数据处理工具
**用途**：数据清洗、数据分析、批量评分、报告生成

**调用示例**：
```bash
# 批量评分
python scripts/data_processor.py --input data.csv --task batch-score --output report.html
```

### 可选分支
- **当需要深度理解底层理论**：阅读 [references/underlying-principles.md](references/underlying-principles.md)（底层公理与核心轴）
- **当需要拆解具体骗局系统**：阅读 [references/scam-system-model.md](references/scam-system-model.md)（完整收割模型）
- **当需要构建反收割系统**：阅读 [references/anti-scam-framework.md](references/anti-scam-framework.md)（执行框架）
- **当需要理解规则与定价权**：阅读 [references/power-and-pricing-layer.md](references/power-and-pricing-layer.md)（规则设计与定价权）
- **当需要顶层玩家路径**：阅读 [references/top-player-path.md](references/top-player-path.md)（实操与进化）
- **当需要量化模型与算法**：阅读 [references/quantitative-core.md](references/quantitative-core.md)（凯利公式、夏普比率、VaR等）
- **当需要理解行为心理学**：阅读 [references/behavioral-psychology.md](references/behavioral-psychology.md)（损失厌恶、前景理论、锚定效应）
- **当需要定价与估值**：阅读 [references/pricing-and-valuation.md](references/pricing-and-valuation.md)（DCF、相对估值、梅特卡夫定律）
- **当需要理解流动性危机**：阅读 [references/liquidity-and-crisis.md](references/liquidity-and-crisis.md)（订单簿、滑点、崩盘前兆）
- **当需要决策工具**：阅读 [references/decision-tools.md](references/decision-tools.md)（决策树、判断矩阵、检查清单）
- **当需要识别骗局类型**：阅读 [references/scam-taxonomy.md](references/scam-taxonomy.md)（金融/技术/社交/商业骗局完整图谱）
- **当需要实战案例分析**：阅读 [references/scam-case-studies.md](references/scam-case-studies.md)（e租宝、麦道夫、PlusToken等案例拆解）
- **当需要理解社交工程**：阅读 [references/social-engineering-algorithms.md](references/social-engineering-algorithms.md)（信任构建、群体传播、信息操纵）
- **当需要博弈论应用**：阅读 [references/game-theory-applications.md](references/game-theory-applications.md)（纳什均衡、博弈树、多轮博弈）
- **当需要防御策略**：阅读 [references/defense-strategies.md](references/defense-strategies.md)（分类型防御、多层级防御、应急响应）
- **当需要复杂系统量化**：阅读 [references/complex-systems-quantification.md](references/complex-systems-quantification.md)（网络效应、相变点、黑天鹅）
- **当需要实战演练**：阅读 [references/interactive-training.md](references/interactive-training.md)（交互式案例、场景训练、错误分析）
- **当需要历史演化分析**：阅读 [references/historical-evolution.md](references/historical-evolution.md)（从古代到现代的骗局演化）

## 使用示例

### 示例1：判断"年化8%稳定收益"项目
- **场景/输入**：有人推荐"年化8%稳定收益，保本保息"
- **预期产出**：识别这是典型的确定性幻觉骗局
- **关键要点**：
  1. 识别叙事关键词："稳定""保本保息" - 违背金融本质
  2. 回答五个问题：收益来源？谁承担风险？答不出→骗局
  3. 对照收割节点：确定性方案已提供，认知门槛被降低
  4. 反收割决策：拒绝，因为追求确定性是被收割的前置条件

### 示例2：分析某P2P爆雷事件
- **场景/输入**：用户询问"某某P2P为什么会爆雷？我亏了钱"
- **预期产出**：拆解完整的收割路径，解释风险转移机制
- **关键要点**：
  1. 回溯收割链路：需求缺口（通胀恐惧）→确定性方案（稳定收益）→降低门槛（不用懂）→信任建立（小收益）→资金聚集→风险转移→流动性断裂
  2. 分析收益来源：本质上是用新资金兑付旧收益（庞氏结构）
  3. 风险转移风险从设计者转移到参与者
  4. 真相：用户不是"投资"，而是"买安心感"

### 示例3：学习反收割策略
- **场景/输入**：用户表示"我总是被骗，想知道如何避免"
- **预期产出**：提供五步强制判断流程和四个策略
- **关键要点**：
  1. 五步强制判断：每次决策前必须回答五个核心问题
  2. 概率思维：不问"能不能赚钱"，问"长期正期望吗"
  3. 仓位系统：设计"允许犯错的系统"，单次错误不出局
  4. 反叙事能力：问"这个故事如果是假的，骗点在哪里"
  5. 进化路径：从"被收割者"→"认知觉醒"→"结构理解"→"策略执行"→"结构利用"

### 示例4：从防守到进攻（进阶）
- **场景/输入**：用户表示"我已经能避免被骗了，如何升级到顶层玩家"
- **预期产出**：提供从参与者到设计者的升级路径
- **关键要点**：
  1. 理解定价权：解释权 = 定价权 = 收益分配权
  2. 掌握三大权力：定价权、流量控制权、规则定义权
  3. 构建信息优势：深度调研、人脉网络、系统化思考
  4. 设计规则结构：成为规则的一部分，而不是参与者
  5. 升级路径：防守（不被收割）→理解（拆解结构）→进攻（主动设计）

### 示例5：量化评估投资机会（专业级）
- **场景/输入**：用户询问"年化30%的项目，值得投吗？"
- **预期产出**：使用量化模型系统化评估
- **关键要点**：
  1. 使用凯利公式脚本计算仓位：`python scripts/kelly_criterion.py --win-rate 0.5 --win-amount 3 --loss-amount 1`
  2. 使用风险指标脚本评估风险：`python scripts/risk_metrics.py --returns '[0.3,0.25,-0.15,0.35,0.2]'`
  3. 使用骗局风险评分：`python scripts/scam_risk_scorer.py --revenue-source 1 --risk-identification 1 ...`
  4. 综合分析量化结果，做出决策

### 示例6：流动性危机识别（实战级）
- **场景/输入**：某平台提现困难，用户询问"是否会爆雷？"
- **预期产出**：使用流动性分析工具评估
- **关键要点**：
  1. 使用流动性分析脚本：`python scripts/liquidity_analyzer.py --bid-price 10.00 --ask-price 10.50 --bid-volume 1000 --ask-volume 10000 --panic-sell-volume 30000 --normal-volume 5000 --available-funds 5000`
  2. 分析输出中的流动性需求和供给
  3. 检查风险警告（critical/severe/moderate）
  4. 根据整体风险评级做出决策

## 资源索引

### 基础理论
- 参考：见 [references/underlying-principles.md](references/underlying-principles.md)（何时读取：需要理解底层公理、核心轴、收益来源时）
- 参考：见 [references/scam-system-model.md](references/scam-system-model.md)（何时读取：需要拆解完整骗局系统、理解收割机制时）
- 参考：见 [references/behavioral-psychology.md](references/behavioral-psychology.md)（何时读取：需要理解人性弱点、骗局心理学时）

### 反收割框架
- 参考：见 [references/anti-scam-framework.md](references/anti-scam-framework.md)（何时读取：需要构建反收割执行系统、学习具体策略时）
- 参考：见 [references/decision-tools.md](references/decision-tools.md)（何时读取：需要使用决策树、判断矩阵、检查清单时）

### 进阶能力
- 参考：见 [references/power-and-pricing-layer.md](references/power-and-pricing-layer.md)（何时读取：需要理解规则设计、定价权、从参与者升级到设计者时）
- 参考：见 [references/top-player-path.md](references/top-player-path.md)（何时读取：需要学习策略模型执行、资金配置、信息优势构建、从防守到进攻的完整路径时）

### 量化模型
- 参考：见 [references/quantitative-core.md](references/quantitative-core.md)（何时读取：需要使用凯利公式、夏普比率、最大回撤、VaR等量化模型时）
- 参考：见 [references/pricing-and-valuation.md](references/pricing-and-valuation.md)（何时读取：需要使用DCF、相对估值、梅特卡夫定律等定价方法时）
- 参考：见 [references/liquidity-and-crisis.md](references/liquidity-and-crisis.md)（何时读取：需要理解流动性危机、订单簿、崩盘前兆时）

### 脚本工具
- 脚本：见 [scripts/kelly_criterion.py](scripts/kelly_criterion.py)（用途：计算最优投资仓位比例，支持对称和非对称盈亏，提供保守策略建议）
- 脚本：见 [scripts/risk_metrics.py](scripts/risk_metrics.py)（用途：计算夏普比率、最大回撤、VaR、索提诺比率等风险指标）
- 脚本：见 [scripts/scam_risk_scorer.py](scripts/scam_risk_scorer.py)（用途：计算CRS骗局风险评分、LRS流动性风险评分和综合风险评分）
- 脚本：见 [scripts/decision_matrix.py](scripts/decision_matrix.py)（用途：评估骗局风险判断矩阵和投资机会评估矩阵）
- 脚本：见 [scripts/liquidity_analyzer.py](scripts/liquidity_analyzer.py)（用途：分析订单簿、流动性需求和供给、流动性风险）

### 骗局识别与防御
- 参考：见 [references/scam-taxonomy.md](references/scam-taxonomy.md)（何时读取：需要识别金融/技术/社交/商业等骗局类型、了解骗局特征时）
- 参考：见 [references/scam-case-studies.md](references/scam-case-studies.md)（何时读取：需要学习e租宝、麦道夫、PlusToken等经典骗局案例、理解收割路径时）
- 参考：见 [references/social-engineering-algorithms.md](references/social-engineering-algorithms.md)（何时读取：需要理解信任构建、群体传播、心理操控等社交工程算法时）
- 参考：见 [references/game-theory-applications.md](references/game-theory-applications.md)（何时读取：需要理解纳什均衡、博弈树、多轮博弈等博弈论应用时）
- 参考：见 [references/defense-strategies.md](references/defense-strategies.md)（何时读取：需要学习分类型防御策略、多层级防御体系、应急响应机制时）

## 注意事项

- 接受"不确定性"是入场门票，追求"确定性"是进入收割轨道
- 前期收益不是能力证明，只是"诱饵成本"
- 不懂的不碰，看不懂的不入，这比亏钱更安全
- 所有被收割的人，本质是在用钱购买"安心感"
- 市场只奖励敢面对不确定性且有能力管理它的人

## 进阶能力

从防守到进攻的升级路径：

### 阶段1：不被收割（防守）
- 目标：识别骗局，避免被收割
- 能力：五步判断、概率思维、仓位控制
- 参考：anti-scam-framework.md

### 阶段2：理解结构（过渡）
- 目标：理解市场运行机制，拆解收割系统
- 能力：系统思维、结构分析、风险识别
- 参考：underlying-principles.md、scam-system-model.md

### 阶段3：主动设计（进攻）
- 目标：掌握定价权，设计规则，控制流量
- 能力：资源整合、规则设计、影响力
- 参考：power-and-pricing-layer.md、top-player-path.md

### 核心升级关键
- 从"接受规则"到"设计规则"
- 从"被动反应"到"主动定价"
- 从"跟随流量"到"控制流量"
