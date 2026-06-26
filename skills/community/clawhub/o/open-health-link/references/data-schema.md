# 数据结构定义

本文档定义 Open Health Link 当前接入的 breo Scalp5 头皮检测报告与护理方案数据模型。

---

## 头皮检测报告

### 报告列表项 (ReportSummary)

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| reportId | string | 是 | 报告唯一标识 |
| detectTime | string (ISO 8601) | 是 | 检测时间 |
| overallScore | number (0-100) | 是 | 头皮综合评分 |
| schemeName | string | 否 | 对应护理方案名（用于联动远程方案知识库） |
| summary | string | 否 | 报告摘要文字 |
| thumbnailUrl | string (URL) | 否 | 缩略图 URL |

### 报告详情 (ReportDetail)

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| reportId | string | 是 | 报告唯一标识 |
| detectTime | string (ISO 8601) | 是 | 检测时间 |
| deviceModel | string | 是 | 设备型号（应为 "Scalp5"） |
| overallScore | number (0-100) | 是 | 头皮综合评分 |
| schemeName | string | 否 | 对应护理方案名 |
| dimensions | DimensionMap | 是 | 各维度评估指标 |
| images | ImageItem[] | 否 | 检测图片列表 |
| aiAnalysis | string | 否 | AI 分析建议文字 |

### 维度指标 (DimensionMap)

包含以下子维度，每个维度结构相同：

| 维度 key | 中文名称 | 说明 |
|----------|----------|------|
| oilLevel | 头皮油脂 | 油脂分泌水平 |
| sensitivity | 头皮敏感度 | 皮肤敏感程度 |
| follicleHealth | 毛囊健康 | 毛囊活力与健康状态 |
| keratinLevel | 头皮角质 | 角质层厚度与状态 |
| hairDensity | 头发密度 | 单位面积毛发数量 |

每个维度的值为 DimensionScore 结构：

| 字段 | 类型 | 说明 |
|------|------|------|
| score | number (0-100) | 该维度得分 |
| status | string | 状态标签（如"正常""偏高""需关注"） |
| description | string | 详细说明 |

### 检测图片 (ImageItem)

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| imageId | string | 是 | 图片标识 |
| imageUrl | string (URL) | 是 | 完整图片 URL |
| region | string | 否 | 检测区域（如"头顶""前额""左侧"） |
| description | string | 否 | 图片描述 |

---

## 头皮护理方案（远程知识库映射）

当前后端无独立护理方案接口。护理方案数据来源为：

1. 报告列表接口返回的 `schemeName`
2. 远程知识库 CSV：`https://breo-obs.obs.cn-south-1.myhuaweicloud.com/agents/plan-catalog.csv`

### 方案列表项 (PlanSummary)

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| planId | string | 是 | 方案唯一标识 |
| createdAt | string (ISO 8601) | 是 | 方案生成时间 |
| basedOnReport | string | 是 | 关联的检测报告 ID |
| title | string | 是 | 方案标题 |
| summary | string | 否 | 方案摘要 |

### 方案详情 (PlanDetail)

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| planId | string | 是 | 方案唯一标识 |
| createdAt | string (ISO 8601) | 是 | 方案生成时间 |
| basedOnReport | string | 是 | 关联的检测报告 ID |
| title | string | 是 | 方案标题 |
| targetIssues | string[] | 是 | 针对的头皮问题列表 |
| steps | CareStep[] | 是 | 护理步骤列表 |
| recommendedProducts | Product[] | 否 | 推荐产品列表 |
| precautions | string[] | 否 | 注意事项 |
| nextCheckSuggestion | string | 否 | 下次检测建议 |

### 护理步骤 (CareStep)

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| order | number | 是 | 步骤序号 |
| name | string | 是 | 步骤名称 |
| frequency | string | 是 | 建议频率（如"每周3次"） |
| method | string | 是 | 具体操作方法 |
| duration | string | 否 | 建议时长 |
| notes | string | 否 | 补充说明 |

### 推荐产品 (Product)

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 产品名称 |
| usage | string | 否 | 使用方法 |

---

## 评分等级参考

供 agent 在解读报告时使用的评分区间参考：

| 分数区间 | 等级 | 描述 |
|----------|------|------|
| 90-100 | 优秀 | 头皮状态非常健康 |
| 75-89 | 良好 | 头皮整体健康，个别指标可改善 |
| 60-74 | 一般 | 存在需要关注的问题 |
| 40-59 | 需改善 | 多项指标异常，建议加强护理 |
| 0-39 | 需就医 | 建议咨询专业皮肤科医生 |
