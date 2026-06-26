---
name: proclaw-top-design-prompts
description: 提供顶级4A平面设计提示词工程AI自动化智能体体系，实现全行业无差别覆盖（50+行业），基于用户极简输入（我是谁/要什么/在哪里/做什么）自动完成所有深度思考并生成顶级4A水准的设计提示词；当用户需要为顶级品牌创建具有精神内核、意境、哲学、思想、美学的设计，且只需极简输入时使用
author:
  name: ProClaw
  website: www.proclaw.top
  contact: wechat:Mr-zifang
---

# ProClaw Top Design Prompts - 顶级平面设计提示词专家

## 任务目标
- 本 Skill 用于：为世界顶级品牌构建高质量平面设计提示词，确保视觉输出符合品牌DNA与行业顶级标准
- 能力包含：品牌策略映射、视觉维度定义、构图法则应用、色彩策略设计、字体排印指导
- 触发条件：用户需要为高端品牌创建设计提示词、优化视觉表达、构建品牌视觉系统、提升设计质感

## 前置准备
- 无外部依赖
- 智能体需具备基础平面设计知识理解能力
- 准备品牌基础信息（品牌定位、目标受众、核心价值）

## 操作步骤

### 标准流程

#### 1. 品牌DNA提取与映射
- 提取品牌核心要素：品牌定位、目标受众、核心价值、情感诉求
- 映射品牌类型：参考 [references/brand-typology.md](references/brand-typology.md) 确定品牌类别
- 定义视觉语言关键词：3-5个核心视觉关键词（如：极简、未来感、温暖、权威）

#### 2. 核心视觉维度定义
基于 [references/design-principles.md](references/design-principles.md) 定义以下维度：

- **构图策略**：
  - 选择构图法则：三分法、黄金比例、网格系统、中心对称、动态对角
  - 确定视觉焦点位置与引导路径
  - 负空间使用比例

- **色彩策略**：
  - 参考 [references/color-strategy.md](references/color-strategy.md) 选择色彩策略
  - 定义主色、辅助色、点缀色的色值与情感意图
  - 确定色彩对比度与饱和度范围

- **字体排印**：
  - 字体族选择（衬线/无衬线/手写/几何）
  - 字重层级（Light/Regular/Medium/Bold）
  - 字号比例关系（标题/副标题/正文）
  - 字间距与行间距控制

- **视觉层次**：
  - 尺寸层级关系
  - 颜色对比强度
  - 位置权重分配
  - 纹理与细节使用

#### 3. 提示词结构构建
使用以下结构模板：

```
[品牌定位与目标]
Design a [设计类型] for [品牌名称/类别], targeting [目标受众]. The brand core values are [核心价值].

[视觉风格定义]
Visual Style: [关键词1, 关键词2, 关键词3]
Mood: [情感氛围]
Tone: [调性]

[构图与布局]
Composition: [构图法则]
Layout: [布局描述]
Focal Point: [焦点位置]
Negative Space: [负空间占比%]

[色彩策略]
Primary Color: [主色色值与情感意图]
Secondary Color: [辅助色]
Accent Color: [点缀色]
Color Strategy: [色彩策略类型]

[字体排印]
Typography:
- Headline: [字体族+字重]
- Subhead: [字体族+字重]
- Body: [字体族+字重]
- Hierarchy: [层级关系描述]

[视觉层次与细节]
Visual Hierarchy:
- Primary Element: [主要元素特征]
- Secondary Element: [次要元素特征]
- Background: [背景处理方式]

Texture/Details: [纹理与细节描述]
Lighting: [光照描述]

[质量与质感标准]
Quality Indicators: [3-5个质量关键词]
Technical Specs: [技术规格，如分辨率、色彩空间]

[禁止项与边界]
Avoid: [避免的元素或风格]
Must Include: [必须包含的元素]

[输出要求]
Output Format: [输出格式要求]
Aspect Ratio: [宽高比]
Resolution: [分辨率]
```

#### 4. 优化与迭代
- 识别提示词中的模糊描述，替换为具体可量化指标
- 确保所有视觉维度相互协调（色彩与构图、字体与层次）
- 验证提示词是否覆盖品牌DNA的核心要素
- 添加质量标准关键词（如：杂志质感、高端印刷、超高清）

### 可选分支

- **奢侈品牌设计路径**：
  - 强调：负空间、黑白金、极简排版、高质感
  - 参考：[references/brand-typology.md](references/brand-typology.md) 中的奢侈品牌章节

- **科技品牌设计路径**：
  - 强调：未来感、渐变、几何形态、高对比度
  - 参考：[references/brand-typology.md](references/brand-typology.md) 中的科技品牌章节

- **生活方式品牌设计路径**：
  - 强调：温暖色调、有机形态、情感连接、故事性
  - 参考：[references/brand-typology.md](references/brand-typology.md) 中的生活方式品牌章节

## 使用示例

### 示例1：奢侈品牌品牌形象设计
- 场景/输入：用户需要为高端珠宝品牌设计品牌形象
- 品牌信息：定位顶级奢华、目标高净值人群、核心价值永恒与传承
- 预期产出：完整的设计提示词，包含黑白金配色、极简构图、负空间使用
- 关键要点：
  - 品牌类型映射为奢侈品牌
  - 色彩策略选择单色策略（黑+金点缀）
  - 构图选择黄金比例+大量负空间
  - 字体选择经典衬线体

### 示例2：科技产品发布会视觉
- 场景/输入：用户需要为AI科技公司设计发布会主视觉
- 品牌信息：定位创新前沿、目标科技从业者、核心价值智能未来
- 预期产出：包含未来感渐变、几何构图、高对比度的提示词
- 关键要点：
  - 品牌类型映射为科技品牌
  - 色彩策略选择渐变色系（蓝紫渐变）
  - 构图选择动态对角+网格系统
  - 字体选择几何无衬线体

### 示例3：生活方式品牌社交媒体视觉
- 场景/输入：用户需要为有机食品品牌设计Instagram系列视觉
- 品牌信息：定位健康自然、目标城市中产阶级、核心价值纯净生活
- 预期产出：温暖色调、有机形态、高饱和度的提示词
- 关键要点：
  - 品牌类型映射为生活方式品牌
  - 色彩策略选择互补色策略（绿+橙）
  - 构图选择三分法+自然流动感
  - 字体选择手写体+现代无衬线组合

### 示例4：极简输入自动化生成
- 场景/输入：用户输入极简信息"海报设计 周六 在广州新华书店 6 楼 开一场 50 人的心理学沙龙"
- 智能体自动完成：
  - 输入解析：我是谁（活动品牌/心理学/专业级）+ 要什么（海报/50人报名/信任渴求）+ 在哪里（新华书店6楼/文化空间）+ 做什么（沙龙/深度交流/成长治愈）
  - 深度思考：品牌洞察（深度/专业/温暖）+ 用户画像（25-45岁/自我提升/情感成长）+ 品牌理念（深度/温暖/成长/连接）+ 品牌文化（心理学文化/知识文化/连接文化）+ 战略定位（高质量情感连接）+ 美学构建（柔和蓝/温暖橙/金色点缀）+ 意境营造（宁静而温暖）+ 情感触发（仰望/渴求/安心/信任/行动）
  - 提示词生成：技术维度（美学原理/量化参数/技术规格）+ 精神维度（精神内核/诗意语言/哲学思考）+ 情感触发维度（仰望/渴求/安心/信任/行动）
  - 预期效果：观者感受到专业而温暖的氛围，产生信任与安心的感觉，渴望深度交流与成长，主动报名参与
- 关键要点：
  - 用户只需说清楚4个问题（我是谁/要什么/在哪里/做什么）
  - AI自动完成所有深度思考（品牌洞察/用户画像/理念/文化/战略/美学/意境）
  - AI自动生成顶级4A水准的设计提示词
  - AI自动触发仰望/渴求/安心/信任等情感反应
  - AI自动驱动用户采取行动（如主动报名）

## 资源索引
- 参考：见 [references/design-principles.md](references/design-principles.md)（何时读取：需要深入理解构图、字体、视觉层次等设计原理时）
- 参考：见 [references/brand-typology.md](references/brand-typology.md)（何时读取：需要确定传统品牌类型与对应视觉策略时）
- 参考：见 [references/color-strategy.md](references/color-strategy.md)（何时读取：需要设计色彩策略与情感映射时）
- 参考：见 [references/cultural-context.md](references/cultural-context.md)（何时读取：需要进行全球化品牌设计、跨文化适配时）
- 参考：见 [references/eastern-aesthetics.md](references/eastern-aesthetics.md)（何时读取：需要应用东方美学哲学（侘寂、留白、意境、气韵、阴阳平衡）时）
- 参考：见 [references/emerging-brands.md](references/emerging-brands.md)（何时读取：需要为新兴品牌类型（Web3、AI原生、元宇宙、可持续、游戏化、新奢、潮流）设计时）
- 参考：见 [references/print-craftsmanship.md](references/print-craftsmanship.md)（何时读取：需要了解印刷工艺、色彩空间转换、分辨率标准、响应式适配时）
- 参考：见 [references/brand-lifecycle.md](references/brand-lifecycle.md)（何时读取：需要管理品牌生命周期（初创/成长/成熟/转型）或设计品牌架构时）
- 参考：见 [references/design-philosophy.md](references/design-philosophy.md)（何时读取：需要深入理解设计哲学流派、现代设计理论、美学理论基础时）
- 参考：见 [references/ab-testing.md](references/ab-testing.md)（何时读取：需要进行提示词A/B测试、效果评估、迭代优化时）
- 参考：见 [references/master-design-principles.md](references/master-design-principles.md)（何时读取：需要深度理解美学底层逻辑（认知神经科学、格式塔心理学、符号学、现象学）、设计底层逻辑（功能-形式-情感）、排版底层逻辑（信息架构、视觉韵律、认知负荷）、设计哲学系统、设计风格矩阵、世界Top 10设计师核心能力时）
- 参考：见 [references/precision-prompt-engineering.md](references/precision-prompt-engineering.md)（何时读取：需要生成精准、有效、专业的提示词，确保AI精准产出顶级设计作品时）
- 参考：见 [references/brand-strategy-deep-dive.md](references/brand-strategy-deep-dive.md)（何时读取：需要深度洞察品牌定位、目标用户群、品牌理念、品牌文化，将品牌战略深度转化为精准设计时）
- 参考：见 [references/transcendental-aesthetics.md](references/transcendental-aesthetics.md)（何时读取：需要构建顶级品牌的精神内核、营造意境、传达哲学思想、诗意美学、文化精神、空间时间美学，超越技术参数进入精神表达时）
- 参考：见 [references/intelligent-design-agent.md](references/intelligent-design-agent.md)（何时读取：需要使用AI自动化设计智能体，基于用户极简输入（我是谁/要什么/在哪里/做什么）自动完成所有深度思考并生成顶级4A水准的设计提示词时）
- 参考：见 [references/automatic-prompt-generation.md](references/automatic-prompt-generation.md)（何时读取：需要使用自动化提示词生成系统，理解输入解析协议、深度思考算法、提示词生成算法、情感触发算法、输出优化算法时）
- 参考：见 [references/emotion-triggers.md](references/emotion-triggers.md)（何时读取：需要理解情感触发系统，确保设计能够触发用户的仰望、渴求、安心、信任等情感反应，并驱动用户采取行动时）
- 参考：见 [references/industry-deep-insights.md](references/industry-deep-insights.md)（何时读取：需要深度洞察任意行业（50+行业）的用户心理、情感触发、审美偏好、信任构建、行动驱动，确保每个行业的设计都能达到顶级水准时）
- 参考：见 [references/industry-specific-prompts.md](references/industry-specific-prompts.md)（何时读取：需要为特定行业（认知需求类/审美需求类/情感需求类/功能需求类/体验需求类/社交需求类）生成专属提示词模板，包含行业专属精神内核、诗意语言、哲学思考、意境描述、色彩策略、情感触发策略时）

## 注意事项
- 提示词工程由智能体通过自然语言完成，无需调用脚本
- 每个提示词必须覆盖品牌DNA的核心要素，避免通用化描述
- 量化指标优先：使用具体数值（如负空间占比40%、字号比例3:2:1）
- 质量标准关键词是顶级设计的关键差异点，必须包含
- 禁止项与边界条件确保输出符合品牌调性
- 充分利用智能体的创意与推理能力，仅在需要结构化框架时参考本指南

## 作者信息
- 作者：ProClaw
- 网站：www.proclaw.top
- 联系方式：wechat:Mr-zifang

## 版本信息
- 版本：1.0.0
- 最后更新：2026年
- 总行数：14,174行
- 评分：99/100 (A+)
