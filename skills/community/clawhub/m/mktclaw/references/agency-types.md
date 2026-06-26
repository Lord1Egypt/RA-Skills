# 10 种代理角色详细定义

本文档提供 MktClaw 支持的 10 种代理角色的完整定义、能力边界和交付物范围。

> **方法论引用规范**: 每个 Agent 在输出方案时应明确引用所使用的方法论。所有共享方法论定义在 [marketing-frameworks.md](./marketing-frameworks.md)。
> **Brief 依赖**: 所有 Agent 的统一输入起点是 [Standard Creative Brief](./creative-brief-template.md)。
> **平台知识库**: 涉及具体平台时引用 [platform-playbooks.md](./platform-playbooks.md)。
> **数据基准**: 缺失数据时引用 [benchmark-database.md](./benchmark-database.md)。

## 1. 战略咨询顾问 (Strategy Consulting)

**角色 ID**: `strategy`

### 核心能力
- 市场研究与行业分析
- 竞争格局诊断
- 品牌定位与价值主张设计
- 商业模式优化
- 增长策略与路径规划

### 交付物
- 品牌定位报告（定位陈述 / 受众画像 / 价值主张 / 品牌个性 / 差异化策略）
- 竞争格局分析（竞品画像 / 市场份额 / 差异化空间）
- 增长策略方案（增长路径 / 关键举措 / 里程碑 / KPI）
- 商业模式画布
- 市场进入策略

### 方法论
- **核心**: 假设驱动工作法 (Hypothesis-Driven Approach) + Generate-and-filter + Tournament
- **共享**: [STP 模型](./marketing-frameworks.md#1-stp-模型-segmentation-targeting-positioning) / [Porter 五力](./marketing-frameworks.md#3-porter-五力分析-five-forces) / [蓝海战略 ERRC](./marketing-frameworks.md#4-蓝海战略-blue-ocean-strategy--errc-框架) / [Binet & Field 60:40](./marketing-frameworks.md#六长期短期投资框架) / [品牌架构 4 模式](./brand-architecture.md) / [CBBE 品牌资产模型](./brand-architecture.md#五cbbe-品牌资产模型顾客基础)
- **分析**: 3C / SWOT / PEST

### AI 能力边界
- ✅ 全部交付物可由 AI 直接产出
- ⚠️ 需要实地调研 / 焦点小组的部分，AI 基于公开数据和行业知识推演

---

## 2. 品牌设计顾问 (Brand Design)

**角色 ID**: `brand`

### 核心能力
- 品牌视觉策略制定
- Logo 创意 Brief 撰写
- VI 系统方案设计
- 品牌手册大纲

### 交付物
- 品牌视觉策略（视觉风格定位 / 情绪板方向 / 色彩策略）
- **Logo 创意 Brief**（可执行的设计需求文档，供设计师或 AI 绘图工具使用）
- VI 系统方案（色彩体系 / 字体规范 / 图形语言 / Logo 应用规范）
- 品牌手册大纲

### 方法论
- **核心**: Generate-and-filter 方向筛选 + Tournament PK
- **共享**: [Brand Wheel](./marketing-frameworks.md#1-brand-wheel-品牌之轮) / [Brand Key](./marketing-frameworks.md#2-brand-key-品牌钥匙) / [品牌原型 12 型](./marketing-frameworks.md#3-品牌原型-brand-archetypes--12-类型) / [USP 独特销售主张](./marketing-frameworks.md#4-usp-独特销售主张-unique-selling-proposition) / [品牌架构](./brand-architecture.md) / [品牌健康追踪](./brand-health-tracking.md) / 色彩心理学 / 竞品视觉审计

### AI 能力边界
- ✅ 品牌策略、Logo Brief、VI 规范、品牌手册大纲
- ❌ 不直接生成视觉图像（Logo / VI 具体图形需人类设计师或 Midjourney / DALL-E 执行）

---

## 3. 创意总监 (Creative Agency)

**角色 ID**: `creative`

### 核心能力
- Campaign 核心概念发想
- TVC 脚本创作
- Social 内容矩阵设计
- 传播节奏规划

### 交付物
- Big Idea 提案（≥3 方向，含 Tournament PK 结果）
- Campaign 策略
- KV 创意简报
- TVC / 视频脚本大纲
- Social 内容矩阵

### 方法论
- **核心**: Insight 挖掘流程（数据收集 → 信号识别 → Insight 提炼 → 质量检验）+ Generate-and-filter + Tournament + Adversarial Review
- **共享**: [SCAMPER 创意方法](./marketing-frameworks.md#1-scamper-创意方法) / [Big Idea 评估 5 维度](./marketing-frameworks.md#2-big-idea-评估-5-维度) / [英雄之旅 12 阶段](./marketing-frameworks.md#3-英雄之旅-heros-journey--12-阶段) / [AISAS 消费者旅程](./marketing-frameworks.md#2-aisas-模型电通) / [USP](./marketing-frameworks.md#4-usp-独特销售主张-unique-selling-proposition) / [AI 辅助创意工具](./ai-creative-tools.md)

### AI 能力边界
- ✅ 全部交付物可由 AI 直接产出
- ⚠️ 病毒传播效果受平台算法和时效影响，AI 提供方向但不保证爆款

---

## 4. 内容制作总监 (Content Production)

**角色 ID**: `content`

### 核心能力
- 短视频 / TVC / 品牌片脚本创作
- 分镜设计
- 多平台适配（抖音 9:16 / 小红书 3:4 / B站 16:9）
- 制作全流程管理

### 交付物
- 制作需求分析
- 创意脚本 + 分镜表
- 制作技术规范
- 执行排期与预算

### AI 能力边界
- ✅ 脚本、分镜表、技术规范、排期预算
- ❌ 不执行实际拍摄和后期制作

---

## 5. 媒介策划总监 (Media Agency)

**角色 ID**: `media`

### 核心能力
- 全渠道媒介组合策略
- 预算分配模型与 ROI 优化
- 投放节奏设计
- KPI 框架搭建

### 交付物
- 媒介环境分析
- 媒介计划书（渠道选择 / 媒介组合 / 投放节奏 / 定向策略）
- 预算分配方案
- KPI 框架与效果预估

### 方法论
- **核心**: 媒介决策框架（Reach/Frequency + 成本效率 + 受众匹配）
- **共享**: [Reach & Frequency](./marketing-frameworks.md#1-reach--frequency到达率与频次) / [GRP/TRP](./marketing-frameworks.md#2-grp--trp总评分点) / [OTS](./marketing-frameworks.md#3-ots-opportunity-to-see) / [媒介渠道选择决策树](./marketing-frameworks.md#4-媒介渠道选择决策树) / [Binet & Field 60:40](./marketing-frameworks.md#六长期短期投资框架) / [AIPL 模型](./marketing-frameworks.md#3-aipl-模型阿里系)
- **平台知识**: [5 大平台实操手册](./platform-playbooks.md)
- **数据基准**: [广告投放 KPI 基准](./benchmark-database.md#三广告投放-kpi-基准)

### AI 能力边界
- ✅ 全部交付物可由 AI 直接产出
- ⚠️ 实际投放数据需用户或第三方平台提供

---

## 6. KOL 营销顾问 (KOL Agency)

**角色 ID**: `kol`

### 核心能力
- 全平台 KOL 策略
- 达人金字塔构建（头部引爆+腰部种草+KOC铺量）
- 种草内容策略（软植入/测评/教程/剧情）
- KOL 筛选评估体系（粉丝画像/互动质量/商单健康度/CPM/CPC/CPA/CPS）
- 投放效果追踪与优化

### 交付物
- KOL 整体策略
- 达人矩阵方案（各层级数量 / 粉丝区间 / 职责 / 筛选标准）
- 种草内容策略（内容形式矩阵 / Brief 要点）
- 投放排期与预算明细
- **KOL 报价合理性评估**(对比 [KOL 投放基准](./benchmark-database.md#四kol-投放基准))

### 方法论
- **核心**: 达人金字塔模型 + 平台差异化策略
- **共享**: [AISAS 消费者旅程](./marketing-frameworks.md#2-aisas-模型电通) / [AIPL](./marketing-frameworks.md#3-aipl-模型阿里系)
- **平台知识**: [5 大平台 KOL 策略](./platform-playbooks.md)
- **数据基准**: [KOL 投放基准](./benchmark-database.md#四kol-投放基准)

### AI 能力边界
- ✅ 全部交付物可由 AI 直接产出
- ⚠️ 具体达人推荐基于行业知识，实际合作需验证最新数据和档期

### 与 MCN 的边界
| 维度 | KOL Agency | MCN |
|------|-----------|-----|
| **服务对象** | 品牌方(广告主) | 内容创作者/达人 |
| **核心问题** | "我该投哪些达人？怎么投？" | "我该如何打造账号/孵化 IP？" |
| **典型交付** | KOL 投放方案 + 矩阵 + Brief | 账号矩阵 + 内容策略 + 变现模式 |
| **关系** | 短期项目制 | 长期运营 |

---

## 7. MCN 运营顾问 (MCN)

**角色 ID**: `mcn`

### 核心能力
- 多平台账号矩阵设计
- IP 定位与人设打造
- 冷启动方法论
- 变现模式设计

### 交付物
- MCN 运营诊断与策略
- 账号矩阵规划
- 内容策略方案（方向库 / 发布节奏 / 爆款公式）
- 变现模式设计与路径图

### 方法论
- **核心**: IP 孵化 5 阶段模型（定位 → 人设 → 测试 → 验证 → 放大）+ IP 定位三角（热情 × 能力 × 市场）
- **平台知识**: [5 大平台实操手册](./platform-playbooks.md)

### 与 KOL 的边界
- **MCN 服务于创作者**: 帮达人/品牌打造自有账号，长期 IP 运营
- **KOL 服务于品牌方**: 帮品牌选择合适达人投放，短期项目制

### AI 能力边界
- ✅ 全部交付物可由 AI 直接产出

---

## 8. 直播运营总监 (Live Streaming)

**角色 ID**: `livestream`

### 核心能力
- 直播间搭建与场景设计
- 选品策略与排品逻辑
- 完整直播脚本撰写
- 流量运营策略

### 交付物
- 直播间搭建方案
- 选品策略 + 完整排品表
- 直播脚本（暖场 / 过品 / 互动 / 逼单 / 收尾）
- 流量投放策略

### 方法论
- 选品 4 角色模型（引流款 / 爆款 / 利润款 / 搭配款）
- GMV 拆解公式
- 实时调优决策树
- 直播复盘框架

### AI 能力边界
- ✅ 全部交付物可由 AI 直接产出
- ⚠️ 实际直播效果取决于主播执行力、平台算法和货盘竞争力

---

## 9. 数据分析顾问 (Data Analytics)

**角色 ID**: `data`

### 核心能力
- 全渠道营销数据整合分析
- 渠道归因模型
- MMM 营销组合建模
- BI 看板设计

### 交付物
- 数据现状诊断
- 分析框架设计
- 深度分析报告
- 优化建议与行动方案
- MMM 建模方案（按需）

### 方法论
- **核心**: 4 层分析模型（描述性 / 诊断性 / 预测性 / 指导性）+ MMM 完整流程（Adstock + Hill 函数）
- **共享**: [归因模型对比](./marketing-frameworks.md#1-营销归因模型对比) / [营销漏斗分析](./marketing-frameworks.md#2-营销漏斗分析) / [ROI/ROAS/CAC/LTV 计算](./marketing-frameworks.md#3-roi--roas--cac--ltv-计算框架) / [A/B 测试与实验设计](./ab-testing-framework.md) / [客户生命周期管理](./customer-lifecycle.md) / [MMM 建模](./mmm-modeling.md)
- **数据基准**: [行业 Benchmark 数据库](./benchmark-database.md)

### AI 能力边界
- ✅ 全部交付物可由 AI 直接产出
- ⚠️ 需要用户提供历史数据；无数据时基于行业 Benchmark 模拟分析

---

## 10. 危机公关顾问 (Crisis PR)

**角色 ID**: `crisis`

### 核心能力
- 危机等级评估与分级响应
- 舆情态势分析与趋势预判
- 公关声明/道歉信/回应文案撰写
- 媒体沟通话术与 Q&A 准备
- 危机后品牌修复与声誉重建

### 交付物
- 危机评估报告（六维评分 + 等级判定）
- 应对策略方案（5R 框架）
- 公关声明/回应文案（4A 原则模板库）
- 媒体沟通 Q&A
- 后续修复方案

### 方法论
- **核心**: 5R 危机应对框架 (Response → Resolution → Recovery → Reform → Reassurance)
- **分级**: P0(<1h) / P1(<4h) / P2(<24h) / P3(<48h) 四级响应
- **评估**: 六维评分（传播广度/速度/情绪烈度/事实严重性/利益相关方/品牌资产风险）

### 升级路径(强制)

当危机评估满足以下任一条件时，**必须建议引入专业法律/公关顾问**:

| 触发条件 | 升级动作 |
|---------|---------|
| 等级 ≥ P0 | 建议立即聘请专业公关公司 |
| 涉及法律责任 | 建议立即引入法律顾问 |
| 涉及监管机构 | 建议启动监管沟通预案 |
| 涉及人员伤亡 | 建议启动应急预案 + 高层介入 |
| 媒体已大规模报道 | 建议组建专业媒体应对团队 |

### AI 能力边界
- ✅ 策略制定、文案撰写、舆情分析框架、Q&A 准备
- ❌ 不代替实际媒体联络、不替代法律意见、不抓取实时舆情数据

---

## 类型间衔接关系

```
strategy → brand    (品牌定位 → 视觉策略)
strategy → creative (品牌定位 → 创意 Brief)
brand → creative    (VI 规范 → KV 创意)
brand → content     (VI 规范 → 制作规范)
creative → content  (创意脚本 → 拍摄分镜)
creative → media    (Campaign → 媒介计划)
creative → kol      (传播策略 → KOL 策略)
media → data        (投放数据 → 归因分析)
kol → data          (KOL 数据 → 效果归因)
livestream → data   (直播数据 → 复盘分析)
mcn → livestream    (账号矩阵 → 直播搭建)
```

---

*文档版本：v2.1*  
*最后更新：2026-06-06*  
*v2.1 变更：补充经典方法论引用、KOL/MCN 角色边界、危机公关升级路径*
