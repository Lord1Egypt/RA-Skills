<!-- @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-08 -->

# OPC智脑 - Skill参考手册

## 概述

OPC智脑包含5个核心Skill，每个Skill对应五阶段模型的一个阶段。本文档是所有Skill的完整参考手册。

## Skill总览

| Skill ID | 名称 | 适用阶段 | 核心能力 |
|----------|------|---------|---------|
| skill1-idea-feasibility | Idea可行性研判 | 构思期 | 需求真伪校验、个人匹配度测评、竞品分析 |
| skill2-mvp-design | MVP精益设计 | 原型期 | MVP裁剪、三层产品体系、交付成本测算 |
| skill3-opc-compliance | OPC合规落地 | 实体期 | 主体选型、新公司法合规、财税规划 |
| skill4-seed-coldstart | 种子用户冷启动 | 验证期 | 低成本获客、招募策略、商业闭环验证 |
| skill5-scale-growth | 规模化增长 | 规模化期 | 业务自动化、产品升级、渠道规模化 |

---

## Skill1：Idea可行性研判

### 基本信息

| 属性 | 值 |
|------|-----|
| **Skill ID** | skill1-idea-feasibility |
| **名称** | Idea可行性研判 |
| **适用阶段** | 构思期（IDEA） |
| **版本** | 1.0.0 |
| **Prompt文件** | src/prompts/skill1.md |

### 输入参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| projectInfo | ProjectInfo | 是 | 项目基本信息 |
| demandDescription | string | 是 | 需求描述 |
| competitorInfo | string | 否 | 竞品信息 |
| personalSkills | string[] | 是 | 个人技能清单 |
| budget | number | 是 | 可用预算（元） |
| availableTime | number | 是 | 可投入时间（小时/周） |

### 输出结构

| 字段 | 类型 | 说明 |
|------|------|------|
| demandValidation | object | 需求真伪校验结果 |
| personalMatch | object | 个人匹配度测评 |
| competitorAnalysis | array | 竞品格局分析 |
| feasibilityLevel | string | 可行性等级 |
| summary | string | 可行性研判总结 |
| alternativeTracks | array | 替代赛道建议 |
| nextStep | string | 下一步行动建议 |

### 可行性等级

| 等级 | 英文 | 含义 |
|------|------|------|
| 高度可行 | highly_feasible | 刚需+匹配度高+竞争有空间 |
| 可行 | feasible | 改善型需求+匹配度中等+有差异化点 |
| 有挑战 | challenging | 需求存疑或匹配度低或竞争激烈 |
| 不可行 | not_feasible | 伪需求或严重不匹配或红海无空间 |

### 前置条件

1. 有明确的创业Idea描述
2. 需求描述清晰，能说明目标用户和痛点
3. 已了解自身技能和可用资源

---

## Skill2：MVP精益设计

### 基本信息

| 属性 | 值 |
|------|-----|
| **Skill ID** | skill2-mvp-design |
| **名称** | MVP精益设计 |
| **适用阶段** | 原型期（MVP） |
| **版本** | 1.0.0 |
| **Prompt文件** | src/prompts/skill2.md |

### 输入参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| projectInfo | ProjectInfo | 是 | 项目基本信息 |
| validatedDemand | string | 是 | 已验证的需求（来自Skill1输出） |
| coreFeatures | string[] | 是 | 核心功能列表 |
| expectedPricing | string | 否 | 预期定价 |
| deliveryMethod | string | 否 | 交付方式 |

### 输出结构

| 字段 | 类型 | 说明 |
|------|------|------|
| mvpScope | object | MVP极简裁剪方案 |
| productLayers | object | 三层产品体系 |
| deliveryCost | object | 单人交付成本测算 |
| firstOrderPlan | object | 首单冷交付方案 |
| summary | string | MVP设计总结 |
| nextStep | string | 下一步行动建议 |

### 三层产品体系

| 层级 | 名称 | 定价策略 | 目的 |
|------|------|---------|------|
| 第一层 | 引流款 | 低/免费 | 获取用户信任和线索 |
| 第二层 | 利润款 | 中高 | 核心收入来源 |
| 第三层 | 被动产品 | 中低 | 自动化交付，边际成本趋零 |

### 前置条件

1. 需求已通过可行性验证（Skill1输出feasibility≥feasible）
2. 核心功能列表已明确
3. 有明确的交付方式设想

---

## Skill3：OPC合规落地

### 基本信息

| 属性 | 值 |
|------|-----|
| **Skill ID** | skill3-opc-compliance |
| **名称** | OPC合规落地规划 |
| **适用阶段** | 实体期（ENTITY） |
| **版本** | 1.0.0 |
| **Prompt文件** | src/prompts/skill3.md |

### 输入参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| projectInfo | ProjectInfo | 是 | 项目基本信息 |
| businessType | string | 是 | 业务类型（service/product/hybrid） |
| expectedMonthlyRevenue | number | 否 | 预计月营收 |
| hasEmployees | boolean | 否 | 是否有员工（默认false） |
| city | string | 否 | 所在城市 |

### 输出结构

| 字段 | 类型 | 说明 |
|------|------|------|
| entityRecommendation | object | 主体选型建议 |
| businessScope | object | 经营范围推荐 |
| compliancePoints | object | 2024新公司法合规要点 |
| taxPlanning | object | 初创财税规划 |
| templates | array | 商用模板清单 |
| preparationChecklist | array | 前期筹备清单 |
| summary | string | 合规规划总结 |
| nextStep | string | 下一步行动建议 |

### 主体类型

| 类型 | 英文 | 适用场景 |
|------|------|---------|
| 个体工商户 | individual_business | 月营收<5万，无融资需求，维护成本最低 |
| 一人有限公司 | one_person_company | 需要有限责任保护，品牌形象重要 |

### 前置条件

1. MVP已设计完成（Skill2输出）
2. 业务类型已明确（服务/产品/混合）
3. 有明确的营收预期

---

## Skill4：种子用户冷启动

### 基本信息

| 属性 | 值 |
|------|-----|
| **Skill ID** | skill4-seed-coldstart |
| **名称** | 种子用户冷启动 |
| **适用阶段** | 验证期（VALIDATION） |
| **版本** | 1.0.0 |
| **Prompt文件** | src/prompts/skill4.md |

### 输入参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| projectInfo | ProjectInfo | 是 | 项目基本信息 |
| productDescription | string | 是 | 产品/MVP描述 |
| currentPricing | string | 是 | 当前定价 |
| existingUsers | number | 否 | 已有用户数（默认0） |
| channelPreference | string[] | 否 | 获客渠道偏好 |

### 输出结构

| 字段 | 类型 | 说明 |
|------|------|------|
| acquisitionChannels | array | 低成本获客渠道方案 |
| seedUserStrategy | object | 种子用户招募策略 |
| feedbackFramework | object | 用户反馈拆解框架 |
| pricingDiagnosis | object | 定价诊断与调价方案 |
| businessLoop | object | 最小商业闭环验证 |
| summary | string | 冷启动方案总结 |
| nextStep | string | 下一步行动建议 |

### 前置条件

1. MVP已可交付
2. 合规主体已就绪（或至少在办理中）
3. 产品定价已有初步方案

---

## Skill5：规模化增长

### 基本信息

| 属性 | 值 |
|------|-----|
| **Skill ID** | skill5-scale-growth |
| **名称** | 规模化增长 |
| **适用阶段** | 规模化期（SCALE） |
| **版本** | 1.0.0 |
| **Prompt文件** | src/prompts/skill5.md |

### 输入参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| projectInfo | ProjectInfo | 是 | 项目基本信息 |
| currentMonthlyRevenue | number | 是 | 当前月营收 |
| currentUserCount | number | 是 | 当前用户数 |
| revenueSources | string[] | 是 | 主要营收来源 |
| bottlenecks | string[] | 是 | 当前痛点/瓶颈 |

### 输出结构

| 字段 | 类型 | 说明 |
|------|------|------|
| businessDecomposition | object | 业务拆解（可AI自动化/可外包/必须亲自做） |
| productLineUpgrade | object | 产品线升级路径 |
| channelScale | object | 渠道规模化方案 |
| riskWarning | array | 经营风险预警 |
| longTermLayout | object | 长期布局 |
| summary | string | 规模化增长总结 |
| nextStep | string | 下一步行动建议 |

### 前置条件

1. 已有稳定付费用户（验证期通过）
2. 月营收>0且相对稳定
3. 交付流程可复用
4. 有明确的增长瓶颈

---

## 通用类型定义

### ProjectInfo

| 字段 | 类型 | 说明 |
|------|------|------|
| projectName | string | 项目/业务名称 |
| description | string | 项目描述 |
| industry | string | 所属行业 |
| targetUsers | string | 目标用户群体 |
| valueProposition | string | 核心价值主张 |
| founderBackground | string | 创业者背景/技能 |
| budget | number | 可用预算（元，可选） |
| availableTime | number | 可投入时间（小时/周，可选） |

### SkillResult

| 字段 | 类型 | 说明 |
|------|------|------|
| skillId | string | 执行的Skill ID |
| success | boolean | 执行是否成功 |
| data | object | 结果数据 |
| prompt | string | Prompt文本（可直接传给大模型） |
| error | string | 错误信息（如果失败） |

## 使用流程

```
1. 采集用户5项核心信息
2. 映射为五维度评分
3. 调用classifyStage()判定阶段
4. 根据阶段调用对应Skill的execute函数
5. 将生成的Prompt发送给大模型
6. 解析大模型返回的结构化结果
7. 按三维输出模板呈现给用户
```