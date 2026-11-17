# S4b: ABA TOP3反查（标杆评分数据准备）

> 仅对S4通过重合度过滤的核心候选执行，控制ABA调用成本。

## 输入
- core_candidates: S4输出的核心候选（overlap≥0.80的ASIN）
- target_asin: 目标ASIN

## 依赖
S4

## 操作
1. 合并目标ASIN + 核心候选ASIN列表
2. 对每个ASIN调用linkfox-aba-intelligent-query反查
   - analysisDescription: "筛选美国站最近一周被点击ASIN为{asin}的数据，返回搜索词searchTerm、点击排名clickShareRank、点击占比clickShare、转化占比conversionShare字段，按点击排名升序排列"
3. 统计每个ASIN的ABA指标:
   - aba_kw_count: ABA TOP3上榜词总数
   - rank1_count: 排名#1的词数
   - rank2_count: 排名#2的词数
   - rank3_count: 排名#3的词数
4. 判断是否核心词ABA #1（目标ASIN最大流量词是否排在ABA #1）

## 输出
- aba_data: {asin: {aba_kw_count, rank1_count, rank2_count, rank3_count, is_core_kw_rank1: bool}}
- 目标ASIN的aba_kw_count作为标杆评分基线

## 用途
被S5消费（标杆头部5维模型中"ABA统治力"维度20%权重的数据来源）
