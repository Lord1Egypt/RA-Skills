# 字段汇总表

## S1 输出字段

| 字段 | 来源 skill | 用途 |
|------|-----------|------|
| productTitle | linkfox-amazon-product-detail | S2/S3 所有检测的标题参数 |
| imageUrl | linkfox-amazon-product-detail | S2/S3 图片类检测的图片参数 |
| aboutItemFivePoint | linkfox-amazon-product-detail | 拼接为 productText 和 productDescription |
| brand | linkfox-amazon-product-detail | S2 文字商标预筛 + S4 报告产品信息 |
| price | linkfox-amazon-product-detail | S5 报告产品信息 |
| rating | linkfox-amazon-product-detail | S5 报告产品信息 |

## S2 输出字段（AIGC 预筛）

| 检测项 | skill | 关键输出字段 |
|--------|-------|-------------|
| 外观专利 | linkfox-aigc-textgen | verdict, reasoning, confidence |
| 实用新型专利 | linkfox-aigc-textgen | verdict, reasoning, confidence |
| 版权 | linkfox-aigc-textgen | verdict, reasoning, confidence |
| 图形商标 | linkfox-aigc-textgen | verdict, reasoning, confidence |
| 文字商标 | linkfox-aigc-textgen | verdict, reasoning, confidence |
| 政策合规 | linkfox-aigc-textgen | verdict, reasoning, confidence |

汇总字段：

| 字段 | 说明 |
|------|------|
| prescreen_results.*.verdict | RISK / CLEAN / AMBIGUOUS |
| prescreen_results.*.reasoning | AIGC 推理摘要 |
| prescreen_results.*.confidence | 置信度 0-100 |
| ambiguous_items | 需要进入 S3 专业检测的项列表 |
| risk_items | AIGC 判定为 RISK 的项列表 |
| clean_items | AIGC 判定为 CLEAN 的项列表 |

## S3 输出字段（仅模糊项，专业检测 JSON）

| 检测项 | skill | 关键输出字段 |
|--------|-------|-------------|
| 文字商标 | ruiguan-text-trademark-detection | textTrademarkRadar, blacklistTrademarks, data[].highestModeScore |
| 图形商标 | ruiguan-trademark-graphic-detection | radarResult, boundingBoxCount, data[].similarity |
| 实用新型专利 | ruiguan-utility-patent-detection | data[].similarity, data[].patentValidity, data[].troCase |
| 外观设计专利 | ruiguan-detection-patent-design | data[].radarResult.same, data[].similarity, data[].troCase |
| 版权 | ruiguan-copyright-detection | data[].similarity, data[].subRadarResult, data[].troCase |
| 政策合规 | ruiguan-gun-parts-search | data[] length |

## S4 输出字段

| 字段 | 说明 |
|------|------|
| aigc_prescreen.summary.total | 预筛总项数 (6) |
| aigc_prescreen.summary.risk | AIGC 判定 RISK 的项数 |
| aigc_prescreen.summary.clean | AIGC 判定 CLEAN 的项数 |
| aigc_prescreen.summary.ambiguous | AIGC 判定 AMBIGUOUS 的项数 |
| aigc_prescreen.credits_saved | 因 AIGC 预筛跳过的专业检测数量 |
| overall_risk.level | HIGH / MODERATE / LOW / CLEAN |
| detection_results.*.risk_level | 每项检测的风险等级 |
| detection_results.*.source | aigc_prescreen 或 professional |
| detection_results.*.summary | 每项检测的摘要 |
| detection_results.*.aigc_reasoning | AIGC 预筛推理摘要 |
| detection_results.design_patent.critical_finding | 外观专利疑似侵权详情 |
