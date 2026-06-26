---
name: mvp-idea-generator
description: 从Reddit挖掘真实痛点，快速生成可落地的MVP方案。当用户需要产品创意验证、市场痛点分析、MVP设计或创业方向评估时使用。
---

# MVP Idea Generator

## 任务目标

本Skill用于帮助独立开发者、SaaS创始人、跨境创业者和AI工具开发者从Reddit社区挖掘真实的用户痛点，并将其转化为可在7天内构建的最小可行产品(MVP)方案。

**核心能力:**
- 垂直社区定位与价值评估
- 高频痛点提取与优先级排序
- MVP核心功能设计与技术栈选型
- Reddit合规验证文案生成
- 商业化可行性评分

**触发条件:**
- 用户需要验证产品创意
- 用户寻找创业方向或市场机会
- 用户需要快速设计MVP方案
- 用户希望评估项目商业价值

## 目标用户

- 独立开发者(Indie Hackers)
- SaaS创始人
- 跨境创业者
- AI工具开发者
- 寻找产品市场契合度(PMF)的创业者

## 五阶段工作流程

### 阶段1: 垂直社区定位

**目标:** 找到高质量、高活跃度、有付费意愿的目标Subreddit

**执行步骤:**
1. 了解用户的目标领域或感兴趣的方向
2. 使用网络搜索研究相关Subreddit
3. 评估社区质量指标:
   - 订阅人数(>10k为佳)
   - 日活发帖量(>10帖/天)
   - 评论互动率(高 engagement)
   - 商业讨论氛围(是否允许推广)
4. 输出5-10个高价值Subreddit推荐及选择理由

**参考资源:** 详细社区评估方法见 [references/subreddit-discovery-guide.md](references/subreddit-discovery-guide.md)

### 阶段2: 痛点嗅探

**目标:** 从社区讨论中提取真实、高频、未被满足的用户需求

**执行步骤:**
1. 分析目标Subreddit的Top Posts(本周/本月/年度)
2. 识别重复出现的问题抱怨模式
3. 提取关键词:
   - "I wish there was..."
   - "Why doesn't anyone make..."
   - "Is there a tool that..."
   - "I'm frustrated with..."
   - "The current solution sucks because..."
4. 记录痛点证据:
   - 帖子链接
   - 出现频率
   - 点赞/评论数
   - 用户付费意愿信号
5. 按优先级排序痛点列表

**参考资源:** 痛点分析方法论见 [references/pain-point-analysis-framework.md](references/pain-point-analysis-framework.md)

### 阶段3: MVP生成

**目标:** 设计一个核心功能、极简技术栈、7天可构建的MVP方案

**核心原则:**
1. **单一核心功能** - 只解决一个痛点，不追求功能完整
2. **最小技术栈** - 使用熟悉的工具，避免学习成本
3. **快速验证** - 7天内必须发布，获取真实反馈

**输出内容:**
- 产品名称与一句话定位
- 核心功能描述(1个)
- 用户故事(User Story)
- 技术栈选型及理由
- 7天构建计划(每日里程碑)
- 成功指标定义

**参考资源:** MVP设计指南见 [references/mvp-design-principles.md](references/mvp-design-principles.md)

### 阶段4: 验证文案生成

**目标:** 生成符合Reddit社区规范的验证帖，获取真实用户反馈

**文案类型:**
1. **问题验证帖** - 验证痛点真实性和严重程度
2. **方案验证帖** - 展示MVP概念，测试兴趣度
3. **预发布帖** - 收集早期用户和反馈

**合规要点:**
- 遵守Subreddit规则(Read the rules first)
- 提供真实价值，不硬推销
- 披露身份(if required)
- 参与讨论，不只是发帖

**模板资源:** 直接使用 [assets/validation-post-templates.md](assets/validation-post-templates.md) 中的模板

### 阶段5: 商业化评分

**目标:** 客观评估项目的商业可行性，决定是否投入开发

**评分维度(每项10分，总分50分):**
1. **需求强度** (Demand Intensity)
   - 问题是否真实存在?
   - 用户是否愿意付费解决?
2. **市场规模** (Market Size)
   - 目标用户数量
   - 支付能力评估
3. **竞争格局** (Competition)
   - 现有解决方案数量
   - 差异化空间
4. **技术可行性** (Technical Feasibility)
   - 7天开发是否现实?
   - 技术门槛高低
5. **变现路径** (Monetization Path)
   - 清晰的商业模式
   - 定价策略可行性

**评分输出:**
- 各维度得分及理由
- 总分计算
- Go/No-Go建议
- 关键风险提示

**参考资源:** 详细评分标准见 [references/commercial-scoring-rubric.md](references/commercial-scoring-rubric.md)

## 资源索引

**参考文档:**
- [社区定位指南](references/subreddit-discovery-guide.md) - 如何找到高价值Subreddit
- [痛点分析框架](references/pain-point-analysis-framework.md) - 痛点提取方法论
- [MVP设计原则](references/mvp-design-principles.md) - 最小可行产品设计指南
- [商业化评分表](references/commercial-scoring-rubric.md) - 项目可行性评估标准

**输出资产:**
- [验证帖模板](assets/validation-post-templates.md) - Reddit合规发帖模板

## 注意事项

**研究阶段:**
- 仅在需要时读取参考文档，保持上下文简洁
- 优先使用网络搜索获取最新数据
- 记录所有信息来源，确保可追溯

**分析阶段:**
- 避免主观臆断，以数据为依据
- 关注用户行为而非用户语言
- 警惕"伪需求"(用户说想要但不付费)

**设计阶段:**
- 严格遵循"1个核心功能"原则
- 技术栈选择优先考虑开发速度
- 7天计划必须包含发布时间点

**验证阶段:**
- 遵守各Subreddit的具体规则
- 提供真实价值，避免纯推销
- 准备应对负面反馈的心理

**评分阶段:**
- 保持客观，不过度乐观
- 总分<30分建议放弃或调整方向
- 总分≥40分值得快速尝试

## 使用示例

**示例1: AI写作工具创意验证**
```
用户输入: "我想做一个AI写作工具，但不知道做什么方向"

执行流程:
1. 阶段1: 定位写作相关Subreddit(r/writing, r/freelanceWriters, r/selfpublish等)
2. 阶段2: 发现"小说家需要角色一致性检查工具"的高频痛点
3. 阶段3: 设计"Character Consistency Checker" MVP
4. 阶段4: 生成r/writing的验证帖
5. 阶段5: 评分38/50，建议尝试

总耗时: 约2小时研究+分析
```

**示例2: 跨境电商工具创意**
```
用户输入: "跨境电商卖家有什么痛点?"

执行流程:
1. 阶段1: 定位电商Subreddit(r/FulfillmentByAmazon, r/ecommerce等)
2. 阶段2: 发现"多平台库存同步困难"痛点
3. 阶段3: 设计"Simple Inventory Sync" MVP
4. 阶段4: 生成问题验证帖
5. 阶段5: 评分32/50，有需求但竞争激烈，建议细分

总耗时: 约3小时研究+分析
```

## 成功标准

完成本Skill后，用户将获得:
1. 5-10个目标Subreddit推荐列表(含评估理由)
2. 痛点优先级清单(含证据链接和频率数据)
3. 完整的MVP设计文档(核心功能+技术栈+7天计划)
4. 2-3篇Reddit验证帖草稿
5. 商业可行性评分报告(含Go/No-Go建议)

**核心价值:** 帮助用户在投入开发前，用最小成本验证产品创意是否值得做。
