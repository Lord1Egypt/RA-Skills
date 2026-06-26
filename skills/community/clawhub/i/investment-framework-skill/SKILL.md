---
name: investment-framework
version: 4.0.0
author: 燃冰 + 小蚂蚁
created: 2026-03-12
updated: 2026-04-07
skill_type: 核心🔴
allowed-tools: [Bash, Read, Write, Exec, WebSearch]
related_skills: [problem-mapper, risk-assessor, sentiment-analyzer]
tags: [投资框架，价值分析，资产配置，决策支持，风险管理]
description: ［何时使用］当用户需要进行投资价值分析时；当用户询问"这家公司值得投资吗"时；当用户需要资产配置建议时；当用户想做投资决策但需要检查逻辑时；当用户想识别长期趋势和机会时；当用户需要评估市场经济专利时；当需要行业专用指标分析时
---
  - value-analyzer: 个股价值分析（格雷厄姆标准）
  - moat-evaluator: 护城河评估（巴菲特标准）
  - intrinsic-value-calculator: 内在价值计算
  - decision-checklist: 决策检查（芒格多元思维 + 投资十诫）
  - asset-allocator: 资产配置（马尔基尔生命周期）
  - future-forecaster: 未来趋势预测（KK 方法论）
  - market-patent-evaluator: 市场经济专利评估（林森池《投资王道》）
  - industry-specialist: 行业分析专家（行业特解指标库）
  - thousand-mile-horse-screener: 千里马筛选器（七准则选股）
  - risk-assessor: 独立风险评估（波动率/下行风险/集中度）⭐ 2026-04-07 新增
  - sentiment-analyzer: 市场情绪分析（新闻/社交/分析师评级）⭐ 2026-04-07 新增
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": [] },
        "install": [],
      },
  }
---

# 投资框架 Skill 包 📈

> 基于 5 本经典投资书籍 + 凯文·凯利未来预测方法论的实战工具箱。

**基于经典**：
- 《聪明的投资者》格雷厄姆 - 安全边际、市场先生
- 《证券分析》格雷厄姆 & 多德 - 内在价值、财务分析
- 《巴菲特致股东的信》巴菲特 - 护城河、能力圈
- 《穷查理宝典》芒格 - 多元思维、逆向思考
- 《漫步华尔街》马尔基尔 - 指数基金、资产配置
- 《必然》《失控》凯文·凯利 - 未来预测方法论
- **《投资王道》林森池 - 市场经济专利、千里马筛选、行业特解** ⭐ 新增

---

## 📋 功能描述

**核心功能**：提供完整的投资决策支持系统，从趋势识别到价值分析到资产配置。

**适用场景**：
- 个股投资价值分析（"这家公司值得投资吗"）
- 资产配置方案制定（"我应该如何配置资产"）
- 投资决策前检查（"帮我检查这个投资逻辑"）
- 长期趋势识别（"AI 是趋势还是泡沫"）
- 投资学习和能力提升

**边界条件**：
- ❌ 不提供具体买卖建议（需用户自主决策）
- ❌ 不预测短期股价波动
- ❌ 不替代深入研究和尽职调查
- ✅ 提供分析框架和决策支持
- ✅ 帮助避免常见投资错误

**免责声明**（所有输出必须包含）：
> ⚠️ 本文内容仅供参考，不构成任何投资建议。市场有风险，投资需谨慎。请独立判断并自行承担风险。

---

## 🎯 技能架构

### 技能关系图（2026-04-07 更新）

```
                              problem-mapper（元技能）
                              ↓ 问题定义与成功标准
                              investment-framework（主技能）
                                       ↓
              ┌────────────────────────┼────────────────────────┐
              ↓                        ↓                        ↓
        价值分析端                决策支持端                趋势预测端
              ↓                        ↓                        ↓
       ┌──────┴──────┐         ┌──────┴──────┐         ┌──────┴──────┐
       │value-       │         │decision-    │         │future-      │
       │analyzer     │         │checklist    │         │forecaster   │
       └──────┬──────┘         └──────┬──────┘         └──────┬──────┘
              │                       │                       │
              │  ┌────────────────────┼────────────────────┐  │
              │  ↓                    ↓                    ↓  │
              │  │moat-          │intrinsic-value-   │market-    │
              │  │evaluator      │calculator         │patent-    │
              │  └─────────┬─────┘└────────┬─────────┘evaluator  │
              │            │               │            │         │
              │            ↓               ↓            ↓         │
              │      ┌─────┴───────────────┴────────────┴─┐      │
              │      │industry-                           │      │
              │      │specialist                          │      │
              │      └─────────────┬──────────────────────┘      │
              │                    ↓                              │
              │            ┌───────┴───────┐                      │
              │            │thousand-mile- │                      │
              │            │horse-screener │                      │
              │            └───────────────┘                      │
              │                                                   │
              └───────────────────────┬───────────────────────────┘
                                      ↓
                              asset-allocator（资产配置）
                                       ↓
              ┌────────────────────────┼────────────────────────┐
              ↓                        ↓                        ↓
        risk-assessor          sentiment-analyzer        (其他技能)
        (风险评估)              (情绪分析)
```

**新增技能说明**（2026-04-07）：
- **risk-assessor**：独立风险评估（波动率/下行风险/集中度分析，输出风险评分 + 仓位上限）
- **sentiment-analyzer**：市场情绪分析（新闻情绪/社交媒体/分析师评级，输出情绪评分 + 趋势判断）

**新增技能说明**（2026-04-06）：
- **market-patent-evaluator**：林森池市场经济专利评估（两类生意分类、专利强度评分、可持续性评估）
- **industry-specialist**：行业分析专家（6+ 大行业特解指标库、行业专利地图、周期定位）
- **thousand-mile-horse-screener**：千里马筛选器（七准则选股、历史业绩回溯、恒指成份股参考）

### CFA 财富管理流程整合

基于《新财富管理》（CFA 财富管理流程）的完整框架：

```
CFA 四流程                    investment-framework 映射
┌─────────────────┐
│ (1) 客户关系    │ → decision-checklist（客户沟通 + 适当性）
│ (2) 客户定位    │ → asset-allocator（目标/风险/约束评估）
│ (3) 投资策略    │ → asset-allocator（IPS 生成 + 配置）
│ (4) 执行监督    │ → fund-tracker + value-analyzer（绩效归因）
└─────────────────┘
```

**核心增强**：
- ✅ **生命周期资产负债表** - 人力资本→金融资本动态模型
- ✅ **投资者适当性管理** - 风险容忍度 vs 风险承受能力区分
- ✅ **IPS 模板** - 标准化投资政策说明书
- ✅ **行为偏差诊断** - 20 种认知/情感偏差识别 + 干预
- ✅ **五年现金流策略** - 6 个月 -2 年储备金管理
- ✅ **3P 基金经理筛选** - 理念/流程/人员优先于业绩

### 技能说明

| 技能 | 类型 | 核心功能 | 触发场景 |
|------|------|----------|----------|
| **problem-mapper** | 元技能🔵 | 问题定义与成功标准设定 | "这笔投资该不该做"（前置） |
| **value-analyzer** | 核心🔴 | 格雷厄姆标准价值分析 | "分析这只股票" |
| **moat-evaluator** | 核心🔴 | 巴菲特护城河评估 | "这家公司有护城河吗" |
| **intrinsic-value-calculator** | 核心🔴 | 内在价值和安全边际计算 | "计算内在价值" |
| **decision-checklist** | 核心🔴 | 芒格多元思维决策检查 + 投资十诫 | "帮我检查投资逻辑" |
| **asset-allocator** | 核心🔴 | 生命周期资产配置 | "如何配置资产" |
| **future-forecaster** | 通用🟡 | KK 未来趋势预测 | "这是趋势还是泡沫" |
| **market-patent-evaluator** | 核心🔴 | 市场经济专利评估（林森池框架） | "这家公司有市场经济专利吗" |
| **industry-specialist** | 核心🔴 | 行业特解指标库（6+ 大行业） | "这个行业值得投资吗" |
| **thousand-mile-horse-screener** | 通用🟡 | 千里马七准则筛选 | "哪些公司值得长期持有" |
| **risk-assessor** ⭐ | 核心🔴 | 独立风险评估（波动率/下行风险/集中度） | "这只股票风险有多大" |
| **sentiment-analyzer** ⭐ | 核心🔴 | 市场情绪分析（新闻/社交/分析师评级） | "市场怎么看这家公司" |

**⭐ 2026-04-07 新增技能**

---

## 🔄 投资决策完整流程

### 流程一：重大投资决策（problem-mapper 前置）

```
1. problem-mapper → 定义投资问题与成功标准
   - 第 0 层：问题淬炼（这是真问题吗？）
   - 第 1 层：问题定义（投资目标/范围/约束）
   - 第 2 层：成功标准（年化收益/风险承受/时间周期）
   - 第 3 层：风险评估（最大亏损/流动性风险/黑天鹅）
   ↓
2. value-analyzer / moat-evaluator → 价值与护城河分析
   ↓
3. intrinsic-value-calculator → 内在价值计算
   ↓
4. decision-checklist → 决策逻辑检查
   ↓
5. asset-allocator → 资产配置建议
```

**适用场景**：
- 大额投资（>总资产 10%）
- 重大决策（首次投资某行业/市场）
- 复杂情境（多方案选择）

**调用示例**：
```
@ant 帮我分析一下这笔投资该不该做：[投资情境]
```

### 流程二：常规投资分析（直接使用六大技能）

```
1. value-analyzer → 价值分析
2. moat-evaluator → 护城河评估
3. intrinsic-value-calculator → 内在价值
4. decision-checklist → 决策检查
```

**适用场景**：
- 常规投资分析
- 已有明确投资目标
- 问题定义清晰

---

## 🔄 组合使用流程

### 流程 1：个股深度分析（推荐）

```
【适用场景】分析具体公司是否值得投资

Step 1: value-analyzer → 初步筛选（是否符合格雷厄姆标准）
        输入：公司财务数据
        输出：防御型/积极型评估、安全边际初判

Step 2: moat-evaluator → 护城河评估（是否有持续竞争优势）
        输入：商业模式、竞争格局
        输出：护城河类型、强度评分、持续性

Step 3: intrinsic-value-calculator → 价值计算（内在价值和安全边际）
        输入：财务数据（资产/盈利/现金流）
        输出：多种方法估值、安全边际、买卖建议

Step 4: decision-checklist → 决策检查（避免认知偏差）
        输入：投资想法、分析结果
        输出：能力圈评估、认知偏差检查、最终建议

【输出】完整投资价值分析报告
```

### 流程 3：《投资王道》框架分析（2026-04-06 新增）

```
【适用场景】用林森池市场经济专利框架深度分析

Step 1: market-patent-evaluator → 专利评估
        输入：公司商业模式、竞争格局
        输出：生意类型分类、专利类型、强度评分、可持续性

Step 2: industry-specialist → 行业分析
        输入：行业名称、公司数据
        输出：行业专利强度、专用指标评估、周期定位

Step 3: thousand-mile-horse-screener → 千里马筛选
        输入：公司财务数据、历史业绩
        输出：七准则符合数、历史回溯、同业对比、星级评级

Step 4: value-analyzer（八步法）→ 价值分析
        输入：财务数据
        输出：八步分析结果、现金流质量、股权摊薄检查

Step 5: intrinsic-value-calculator → 内在价值
        输入：现金流预测、估值假设
        输出：DCF 估值、安全边际

Step 6: decision-checklist（投资十诫）→ 决策检查
        输入：投资想法、分析结果
        输出：投资十诫检查、最终建议

【输出】《投资王道》框架完整分析报告
```

### 流程 2：趋势驱动型投资

```
【适用场景】识别和把握长期趋势（如 AI、新能源）

Step 1: future-forecaster (trend-scanner) → 识别长期趋势
        输入：观察到的现象/新词汇/技术
        输出：趋势分类、爆发时点、投资启示

Step 2: future-forecaster (layer-analyzer) → 判断变化层级
        输入：趋势描述
        输出：流行/技术/基础设施层判定

Step 3: moat-evaluator → 评估相关公司护城河
        输入：候选公司列表
        输出：护城河强度排序

Step 4: value-analyzer → 筛选价值标的
        输入：护城河强的公司
        输出：符合格雷厄姆标准的标的

Step 5: intrinsic-value-calculator → 计算合理价格
        输入：筛选出的公司
        输出：内在价值、安全边际

Step 6: decision-checklist → 检查认知偏差
        特别注意：FOMO、从众心理、锚定效应

Step 7: asset-allocator → 配置到组合
        输入：投资标的、当前组合
        输出：配置比例、仓位建议

【输出】趋势驱动型投资完整方案
```

### 流程 3：趋势陷阱规避

```
【适用场景】判断是否为趋势陷阱（避免追高）

Step 1: future-forecaster (layer-analyzer) → 判断层级
        关键问题：这是流行趋势还是技术变革？

Step 2A: 若为流行趋势 → 避免重大投资
         future-forecaster 输出警示

Step 2B: 若为技术变革 → 进入深度分析流程
         继续流程 2 的后续步骤

【输出】趋势陷阱判断报告
```

### 流程 4：资产配置方案

```
【适用场景】制定或调整资产配置方案

Step 1: asset-allocator → 设计配置方案
        输入：年龄、风险偏好、投资目标
        输出：资产类别配置比例

Step 2: value-analyzer → 选择具体标的
        输入：配置比例
        输出：各资产类别的具体基金/股票

Step 3: decision-checklist → 最终决策检查
        输入：配置方案、标的选择
        输出：配置逻辑检查、风险确认

【输出】完整资产配置方案
```

### 流程 5：能力圈扩展

```
【适用场景】扩展投资能力圈（学习新领域）

Step 1: future-forecaster (mindset-checker) → 检查认知捆绑
        关键问题：我是否被过时认知限制？

Step 2: 识别过时认知 → 主动学习新领域
        future-forecaster 输出学习建议

Step 3: 扩大能力圈 → 纳入投资框架分析
        使用 value-analyzer/moat-evaluator 分析新领域

【输出】能力圈扩展计划
```

---

## ⚠️ 常见错误

### 错误 1：跳过深度分析直接决策
```
失败案例：
• 2021 年追高某热门股，未做价值分析
• 只听消息买入，未检查护城河
• 结果：亏损 50%+

正确做法：
✓ 至少完成 value-analyzer + moat-evaluator
✓ 计算内在价值和安全边际
✓ 用 decision-checklist 检查逻辑

预防清单：
- [ ] 是否分析了护城河？
- [ ] 是否计算了内在价值？
- [ ] 安全边际是否>30%？
- [ ] 是否在能力圈内？
```

### 错误 2：混淆趋势层级
```
失败案例：
• 把流行趋势当技术变革（如某些元宇宙概念）
• 用长期逻辑投资短期热点
• 结果：趋势退潮后深套

正确做法：
✓ 用 future-forecaster (layer-analyzer) 判断层级
✓ 流行趋势层：保持距离，不重仓
✓ 技术层：核心关注，识别爆发点
✓ 基础设施层：长期持有

预防清单：
- [ ] 这是流行/技术/基础设施？
- [ ] 变化速度是年/3-5 年/10 年 +？
- [ ] 投资周期是否匹配？
```

### 错误 3：忽视认知偏差
```
失败案例：
• 过度自信重仓单一股票
• 确认偏误只看利好信息
• 损失厌恶死扛亏损股
• 结果：重大损失

正确做法：
✓ 每次决策前用 decision-checklist
✓ 特别检查：过度自信/确认偏误/从众心理
✓ 寻找反面证据平衡观点

预防清单：
- [ ] 是否只看了利好信息？
- [ ] 是否找了反面证据？
- [ ] 仓位是否过度集中？
- [ ] 是否因亏损而不愿卖出？
```

### 错误 4：机械套用格雷厄姆标准
```
失败案例：
• 用同一标准评估所有行业
• 忽视科技行业特殊性
• 错过优质成长股

正确做法：
✓ 防御型标准适合传统行业
✓ 科技行业需调整标准（更关注护城河）
✓ 结合 moat-evaluator 综合判断

预防清单：
- [ ] 行业类型是什么？
- [ ] 格雷厄姆标准是否适用？
- [ ] 护城河是否足够强？
- [ ] 是否需调整估值方法？
```

### 错误 5：资产配置僵化
```
失败案例：
• 机械套用"100-年龄"公式
• 忽视个人风险承受能力差异
• 结果：配置与实际不匹配

正确做法：
✓ 用 asset-allocator 综合评估
✓ 考虑年龄/收入/目标/经验
✓ 定期再平衡但不机械

预防清单：
- [ ] 是否评估了风险承受能力？
- [ ] 配置是否符合投资目标？
- [ ] 是否有应急资金？
- [ ] 再平衡频率是否合理？
```

### 错误 6：能力圈外投资
```
失败案例：
• 投资完全不理解的行业（如生物医药）
• 只听"专家"推荐不做研究
• 结果：无法判断真假，亏损离场

正确做法：
✓ 用 decision-checklist 检查能力圈
✓ 能力圈外坚决不投（或先学习）
✓ 用 future-forecaster 扩展认知

预防清单：
- [ ] 我是否理解这个商业模式？
- [ ] 能否预测 10 年后行业格局？
- [ ] 是否有相关专业知识？
- [ ] 是否投资过类似公司？
```

### 错误 7：忽视安全边际
```
失败案例：
• 好公司但价格过高时买入
• 忽视安全边际的重要性
• 结果：好公司也亏钱

正确做法：
✓ 用 intrinsic-value-calculator 计算价值
✓ 安全边际<30% 不买入
✓ 等待好价格

预防清单：
- [ ] 内在价值是多少？
- [ ] 安全边际是否>30%？
- [ ] 当前价格是否合理？
- [ ] 是否可等待更好价格？
```

---

## 📊 输入参数

### 主技能输入（路由到子技能）

```json
{
  "request_type": {
    "type": "string",
    "enum": ["个股分析", "趋势分析", "资产配置", "决策检查", "能力圈扩展"],
    "required": true,
    "description": "请求类型，路由到对应子技能"
  },
  "company_name": {
    "type": "string",
    "required": false,
    "description": "公司名称（个股分析时必填）"
  },
  "financial_data": {
    "type": "object",
    "required": false,
    "description": "财务数据（个股分析时提供）"
  },
  "trend_observation": {
    "type": "string",
    "required": false,
    "description": "趋势观察描述（趋势分析时必填）"
  },
  "investor_profile": {
    "type": "object",
    "properties": {
      "age": {"type": "number"},
      "risk_tolerance": {"type": "string"},
      "investment_goal": {"type": "string"}
    },
    "required": false,
    "description": "投资者画像（资产配置时必填）"
  },
  "investment_idea": {
    "type": "string",
    "required": false,
    "description": "投资想法描述（决策检查时必填）"
  }
}
```

---

## 📤 输出格式

### 统一输出结构

```json
{
  "status": "success",
  "data": {
    "request_type": "个股分析 | 趋势分析 | 资产配置 | 决策检查",
    "skills_used": ["value-analyzer", "moat-evaluator", "..."],
    "analysis_result": {},
    "recommendation": "强烈推荐 | 推荐 | 观察 | 谨慎 | 避免",
    "key_risks": [],
    "action_items": [],
    "next_steps": []
  }
}
```

### 各技能输出详见子技能文档

- `value-analyzer/SKILL.md` - 价值分析输出
- `moat-evaluator/SKILL.md` - 护城河评估输出
- `intrinsic-value-calculator/SKILL.md` - 估值输出
- `decision-checklist/SKILL.md` - 决策检查输出
- `asset-allocator/SKILL.md` - 资产配置输出
- `future-forecaster/SKILL.md` - 趋势预测输出
- `risk-assessor/SKILL.md` - 风险评估输出 ⭐ 新增
- `sentiment-analyzer/SKILL.md` - 情绪分析输出 ⭐ 新增

### 标准化输出 Schema ⭐

所有技能遵循统一输出标准：`signal + confidence + reasoning`

详见：`OUTPUT_SCHEMA.md` - 完整 Schema 定义和字段说明

---

## 🧪 使用示例

### 示例 1：个股深度分析（腾讯控股）

**用户输入**：
```
分析腾讯控股是否值得投资
```

**处理流程**：
```
1. value-analyzer → 格雷厄姆标准评估
2. moat-evaluator → 护城河评估
3. intrinsic-value-calculator → 内在价值计算
4. decision-checklist → 决策检查
```

**输出**：
```
【腾讯控股投资价值分析】

【价值分析】（value-analyzer）
- 投资者类型：积极型
- 符合标准：5/7（规模/财务/盈利/分红/增长✓，P/B/P/E✗）
- 初评：不符合防御型标准，适合积极型投资者

【护城河评估】（moat-evaluator）
- 护城河类型：网络效应（5/5）、转换成本（5/5）、品牌（4/5）
- 综合评分：18/25 分（强）
- 趋势：稳定

【内在价值】（intrinsic-value-calculator）
- 多种方法估值：¥350-450
- 当前价格：¥380
- 安全边际：10-20%（不足）

【决策检查】（decision-checklist）
- 能力圈评分：17/20（能力圈内）
- 认知偏差：2/8（低）
- 逻辑完整性：4/5

【综合建议】
建议：观察
理由：
1. 护城河强（18/25 分）
2. 但安全边际不足（10-20%）
3. 建议等待更好价格（<¥300）

【行动项】
1. 加入观察列表
2. 设定理想买入价：¥280-300
3. 持续跟踪护城河变化
```

### 示例 2：趋势分析（AI 投资）

**用户输入**：
```
AI 现在是趋势还是泡沫？
```

**处理流程**：
```
1. future-forecaster (layer-analyzer) → 判断层级
2. future-forecaster (trend-scanner) → 扫描趋势
3. moat-evaluator → 评估相关公司
```

**输出**：
```
【AI 趋势分析】

【层级判断】（future-forecaster）
- 变化层级：技术层（3-5 年大变化）
- 非流行趋势（有实质技术突破）
- 爆发时点：2023-2028

【趋势扫描】（future-forecaster）
- 思维模型：新词挖掘（AIGC/大模型/Agent）
- 边缘主流：GPU 从游戏到 AI
- 富人下沉：AI 助理从高端到普及

【相关公司护城河】（moat-evaluator）
- 英伟达：CUDA 生态（转换成本 5/5）
- 微软：生态 + 数据（网络效应 4/5）
- 谷歌：数据 + 人才（品牌 4/5）

【投资建议】
建议：趋势确认，但需精选标的
理由：
1. 技术层变革（非泡沫）
2. 护城河强的公司有限
3. 估值普遍偏高，需等待

【行动项】
1. 关注护城河强的公司
2. 等待安全边际>30% 的价格
3. 用 decision-checklist 避免 FOMO
```

### 示例 3：资产配置方案

**用户输入**：
```
我 35 岁，平衡型风险偏好，如何配置资产？
```

**处理流程**：
```
1. asset-allocator → 设计配置方案
2. value-analyzer → 选择具体标的
3. decision-checklist → 最终检查
```

**输出**：
```
【35 岁平衡型资产配置方案】

【风险承受评估】（asset-allocator）
- 年龄：35 岁（中年）
- 风险偏好：平衡
- 投资期限：25 年 +（退休）
- 综合风险等级：平衡

【资产配置】（asset-allocator）
| 资产类别 | 比例 | 金额（假设 100 万） |
| 股票 | 70% | 70 万 |
| 债券 | 25% | 25 万 |
| 现金 | 5% | 5 万 |

股票细分：
- 国内指数：50%（35 万，沪深 300ETF）
- 国际指数：50%（35 万，标普 500ETF）

【具体标的】（value-analyzer）
- 沪深 300ETF：符合指数投资标准
- 标普 500ETF：符合指数投资标准
- 国债 ETF：低风险配置

【决策检查】（decision-checklist）
- 配置逻辑：✓ 符合生命周期理论
- 风险认知：✓ 理解波动风险
- 长期承诺：✓ 准备持有 25 年 +

【再平衡策略】
- 频率：每年 1 次（建议年初）
- 阈值：偏离>5% 时调整
- 方法：卖出高估，买入低估

【定投计划】
假设每月可投资 1 万：
- 沪深 300ETF：¥3500
- 标普 500ETF：¥3500
- 国债 ETF：¥2000
```

---

## 📚 核心理念

### 投资第一性原理

```
好投资 = 好公司 × 好价格 × 长期持有

好公司：moat-evaluator（护城河强）
好价格：intrinsic-value-calculator（安全边际>30%）
长期持有：asset-allocator（生命周期匹配）
```

### 格雷厄姆安全边际

```
用 4 毛钱买 1 块钱的东西

核心公式：
安全边际 = (内在价值 - 当前价格) / 内在价值 × 100%

建议：
- 防御型：安全边际>30%
- 积极型：安全边际>50%
```

### 巴菲特护城河

```
护城河是结构性优势，不是短期优势

5 大护城河：
1. 品牌优势（用户愿付溢价）
2. 网络效应（用户越多价值越大）
3. 转换成本（用户更换困难）
4. 规模优势（规模带来成本优势）
5. 特许经营权（政府授权/专利）

真正的护城河必须能持续 10 年+
```

### 芒格多元思维

```
好决策 = 能力圈内 × (1 - 认知偏差) × 逻辑完整性

关键原则：
1. 能力圈外坚决不投
2. 认知偏差是最大敌人
3. 逆向思考（反过来想）
4. 清单是思考工具不是形式
```

### 马尔基尔资产配置

```
长期稳健收益 = 资产配置 × 定期定额 × 再平衡

核心原则：
1. 定期定额投资（不择时）
2. 分散化（不要把所有鸡蛋放一个篮子）
3. 低成本（选择低费率指数基金）
4. 再平衡（每年调整一次）
5. 长期思维（忽略短期波动）
```

### KK 未来预测

```
把握趋势 = 识别信号 × 理解层级 × 保持开放

三思维模型：
1. 富人下沉法（高端服务→大众市场）
2. 边缘主流法（边缘创新→主流应用）
3. 新词挖掘法（新词汇→新趋势）

四变化层级：
- 流行趋势（年变）→ 避免追逐
- 技术（3-5 年变）→ 核心关注
- 基础设施（10 年 + 不变）→ 长期持有
- 气候地质（世纪变）→ 超长期参考
```

### 健康公式

```
投资成功 = 能力圈 × 安全边际 × 护城河 × 长期思维 × (1 - 认知偏差)

关键变量：
- 能力圈：只投理解的
- 安全边际：价格<价值 30%+
- 护城河：结构性优势 10 年 +
- 长期思维：持有期 5 年 +
- 认知偏差：越少越好
```

---

## 🔗 相关资源

### 渐进式披露结构

**核心文档**（本文件）：
- 投资框架总览和组合使用流程

**子技能文档**：
- `value-analyzer/SKILL.md` - 价值分析详情
- `moat-evaluator/SKILL.md` - 护城河评估详情
- `intrinsic-value-calculator/SKILL.md` - 估值计算详情
- `decision-checklist/SKILL.md` - 决策检查详情
- `asset-allocator/SKILL.md` - 资产配置详情
- `future-forecaster/SKILL.md` - 趋势预测详情

**参考资料**（references/）：
- `references/graham-principles.md` - 格雷厄姆核心原则
- `references/buffett-moat.md` - 巴菲特护城河理论
- `references/munger-models.md` - 芒格多元思维模型
- `references/malkiel-allocation.md` - 马尔基尔资产配置
- `references/kk-prediction.md` - KK 未来预测方法论

**示例集合**（examples/）：
- `examples/tech-company-analysis.md` - 科技公司分析示例（腾讯/阿里）
- `examples/consumer-company-analysis.md` - 消费公司分析示例（茅台/伊利）
- `examples/trend-analysis.md` - 趋势分析示例（AI/新能源）
- `examples/allocation-cases.md` - 资产配置案例（不同年龄段）

**模板文件**（templates/）：
- `templates/investment-report-template.md` - 投资分析报告模板
- `templates/decision-checklist-template.md` - 决策清单模板
- `templates/allocation-plan-template.md` - 配置方案模板

---

## 🔗 相关文件

### 子技能文件路径

```
investment-framework/
├── SKILL.md（本文件）
├── value-analyzer/
│   └── SKILL.md
├── moat-evaluator/
│   └── SKILL.md
├── intrinsic-value-calculator/
│   └── SKILL.md
├── decision-checklist/
│   └── SKILL.md
├── market-patent-evaluator/       # ⭐ 新增 - 市场经济专利评估
│   └── SKILL.md
├── industry-specialist/           # ⭐ 新增 - 行业分析专家
│   └── SKILL.md
├── thousand-mile-horse-screener/  # ⭐ 新增 - 千里马筛选器
│   └── SKILL.md
├── asset-allocator/
│   └── SKILL.md
└── future-forecaster/
    └── SKILL.md
```

### 组合使用指南

- `APPLICATION_GUIDE.md` - 完整应用指南
- `THEORY.md` - 理论基础详解
- `ADVANCED_SKILLS.md` - 高级技能组合
- `USAGE.md` - 使用手册

---

## 更新日志

- **v3.2.0 (2026-04-06): 整合《投资王道》框架** ⭐ 新增
  - 新增 `market-patent-evaluator`：市场经济专利评估（两类生意分类、专利强度评分）
  - 新增 `industry-specialist`：行业分析专家（6+ 大行业特解指标库）
  - 新增 `thousand-mile-horse-screener`：千里马筛选器（七准则选股）
  - 增强 `decision-checklist`：加入投资十诫检查清单
  - 增强 `moat-evaluator`：加入专利可持续性评估
  - 增强 `value-analyzer`：加入八步分析法流程
  - 增强 `intrinsic-value-calculator`：加入资源股储量折现法、有期限 DCF
  - 更新技能关系图和使用流程

- v3.1.0 (2026-03-23): 集成 problem-mapper 作为元技能
  - 更新技能关系图，problem-mapper 作为前置工具
  - 添加投资决策完整流程（problem-mapper 前置）
  - 区分重大投资决策和常规投资分析流程
  - 强调问题定义优先（重大投资前先用 problem-mapper）

- v3.0.0 (2026-03-19): 按照 SKILL-STANDARD-v2.md 深度重构

| 问题 | 检查项 |
|------|--------|
| 不触发 | description 是否包含触发词？ |
| 运行失败 | 脚本有执行权限吗？(`chmod +x`) |
| 用错技能 | 多个技能 description 是否太相似？ |

- v3.0.0 (2026-03-19): 按照 SKILL-STANDARD-v2.md 深度重构
  - 添加完整 Front Matter（version/author/skill_type/related_skills）
  - description 改为触发说明式
  - 添加技能关系图和组合流程
  - 添加 7 个常见错误（从失败案例提炼）
  - 添加渐进式披露结构（references/examples/templates）
  - 标准化输入输出格式（JSON Schema）
  - 添加 3 个完整使用示例
  - 优化核心理念和健康公式

- v1.1.0 (2026-03-16): 新增 future-forecaster 技能

- v1.0.0 (2026-03-12): 初始版本，包含 5 个核心技能

---

*投资是认知的变现。用框架提升认知，用纪律保护资本，用时间换取复利。* 📈

---

## 📚 《投资王道》整合说明（2026-04-06）

### 核心理念

**市场经济专利**：市场给予的、难以复制的竞争优势（非政府授予）
- 六大类型：地理位置、规模成本、消费习惯、利基市场、品牌心智、网络效应
- 两类生意：过度竞争 vs 拥有专利（只投资后者）

**千里马七准则**：
1. 经济环境：处于经济高速增长期
2. 专利要求：产品/服务无可取代
3. 需求特性：重复性且有增无减
4. 竞争格局：存在竞争但非割喉式
5. 行业稳定性：前景稳定，受周期影响轻微
6. 增长能力：纯利及营业额增幅 > 经济增速
7. 资本回报：ROE ≥ 12%（双位数）

**投资十诫**（增强 decision-checklist）：
戒短线、戒狂潮、戒贪婪恐惧、戒新股、戒衍生工具、戒流言、戒过度分散、戒落后股、戒收购合并、戒刀仔锯大树

### 行业特解指标

| 行业 | 核心指标 | 估值方法 |
|------|----------|----------|
| 电力 | EV/EBITDA、煤价传导、现金流/Capex | DCF |
| 银行 | 坏账率、贷款增长、ROE、成本收入比 | P/B |
| 石油 | 储量替代率、开采成本、实现价 | 储量折现 |
| 电讯 | ARPU、纯利率、折旧占比、现金流 | DCF |
| 保险 | 内含价值、新业务价值 | EV/P |
| 公路 | 剩余年限、车流量、加价能力 | 有期限 DCF |

### 完整框架对比

| 维度 | 原有框架 | 《投资王道》 | 整合后 |
|------|----------|--------------|--------|
| 护城河 | 巴菲特五类型 | 市场经济专利六类型 | 合并使用，交叉验证 |
| 选股 | 格雷厄姆定量 | 千里马七准则 | 定量 + 定性 |
| 分析 | 通用财务分析 | 八步法 + 行业特解 | 通用 + 专用 |
| 纪律 | 认知偏差检查 | 投资十诫 | 合并增强 |
| 估值 | 通用 DCF/PE/PB | 储量折现/有期限 DCF | 补充专业方法 |

### 参考文档

- 整合方案：`docs/investment-framework/wangdao-integration.md`
- 读书笔记：飞书文档 `JwaddKbsroATO0xx0e2cI3mjnvg`

---
