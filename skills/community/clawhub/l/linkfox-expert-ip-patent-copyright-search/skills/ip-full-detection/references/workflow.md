# 业务流程

## 业务目标
输入一个亚马逊 ASIN，先用 AIGC 多模态大模型零积分预筛 6 项知识产权风险，仅对模糊项调用睿观专业检测消耗积分，汇总风险评级并生成 HTML 报告。

## 核心策略
AIGC 预筛 → 模糊项精准兜底 → 汇总报告

| AIGC 预筛结论 | 处理方式 | 积分消耗 |
|---------------|---------|---------|
| 明确有风险 (RISK) | 直接标记风险，跳过专业工具 | 零 |
| 明确无风险 (CLEAN) | 直接放行，跳过专业工具 | 零 |
| 模棱两可 (AMBIGUOUS) | 进入第二层专业工具检测 | 消耗 |

## 输入参数
- asin（必填）：亚马逊 ASIN
- region（可选，默认 US）：检测区域

## 步骤拆解

| 编号 | 动作 | 上下游 | 所需字段 |
|------|------|--------|---------|
| S1 | 调 amazon-product-detail 拉取产品详情 | 下游 S2 | asin, region → productTitle, imageUrl, aboutItemFivePoint |
| S2 | 并行调 linkfox-aigc-textgen 对 6 项 IP 风险做零积分预筛 | 上游 S1，下游 S3 | productTitle, imageUrl, productText, brand, region → 6 项三态判定 |
| S3 | 仅对 S2 判定 AMBIGUOUS 的项并行调睿观 IP 检测 | 上游 S2，下游 S4 | productTitle, imageUrl, productText, productDescription, region + ambiguous_items |
| S4 | 合并 AIGC 预筛 + 专业检测结果，计算风险评级 | 上游 S3，下游 S5 | S2 预筛结果 + S3 JSON 文件路径 |
| S5 | 调 linkfox-report-generator 生成 HTML 报告 | 上游 S4 | S4 输出的结构化 data 对象 |

## 报告诉求
HTML 报告，含 AIGC 预筛概览、风险矩阵概览、6 项检测详情（区分 AIGC/专业来源）、高风险标注、积分节省统计、综合建议。

## 已知局限
- AIGC 预筛基于大模型推理，不访问实时专利/商标数据库
- 实用新型专利检测仅支持 US
- 各专业检测有积分消耗，24h 缓存
- 不构成法律意见
