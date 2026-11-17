# 竞品分析Agent — Skill依赖清单

## 自建Skill（需打包导入）

| Skill名称 | Tier | 路径 | 作用 |
|-----------|------|------|------|
| competitor-selector | Tier 2 | /root/.linkfox/.ce/skills/competitor-selector/ | 竞品筛选算法引擎：三路径分流(标品/非标品/混合) → 4道门槛 → 三模型评分 |
| competitor-research-pipeline | Tier 3 | /root/.linkfox/.ce/skills/competitor-research-pipeline/ | 竞品调研全流程SOP：筛选→数据采集→8维度对比→A+分析→报告 |

## 依赖的LinkFox公共Skill（需在Agent中挂载）

| Skill名称 | 用途 | 使用环节 |
|-----------|------|----------|
| linkfox-amazon-product-detail | 商品详情(五点/规格/变体/图片/A+) | S0商品类型判定, S4功能对比, S6c A+分析 |
| linkfox-amazon-search | 亚马逊前台搜索 | S2标品/混合路径候选池生成 |
| linkfox-amazon-search-by-image | 以图搜图 | S2非标品/混合路径候选池生成 |
| linkfox-keepa-product-request | Keepa历史数据(BSR/月销/评论/费用) | S3价格过滤+历史数据, S6b横向对比 |
| linkfox-sellersprite-traffic-keyword | 卖家精灵流量词反查(含翻页) | S1核心流量词识别, S3数据采集, S6首页词归因 |
| linkfox-aba-intelligent-query | ABA TOP3反查 | S4b标杆评分数据, S4 ABA反查, S7 ABA交叉对比 |
| linkfox-aigc-textgen | AIGC多模态(图片/文本理解) | S4功能/外观重合度对比, S6c A+与商品图分析 |
| linkfox-report-generator | HTML报告生成 | S9报告生成 |
| linkfox-voc-review-analysis | VOC评论分析(可选) | S5 VOC评论采集 |

## 自建Skill内部脚本

| 脚本 | 所属Skill | 作用 |
|------|-----------|------|
| competitor_selector.py | competitor-selector | 三模型评分引擎(直接竞品6维+潜力股5维+标杆5维) |
| keyword_overlap_analyzer.py | competitor-research-pipeline | 首页词归因分析(唯一vs重复) |
| aba_overlap_analyzer.py | competitor-research-pipeline | ABA TOP3交叉对比 |
| competitor_comparison_analyzer.py | competitor-research-pipeline | 8维度横向对比(销量/份额/Deal/稳定性/季节性/BSR动量/弹性/参数) |
| generate_report_fragment.py | competitor-research-pipeline | JSON→HTML片段自动生成器 |

## Agent创建配置建议

```
Agent名称: 竞品分析Agent
Agent ID: competitor-analysis-agent
描述: 输入ASIN+站点，端到端完成竞品筛选(三路径算法)→全量数据采集→8维度横向对比→A+与商品图分析→HTML深度报告

核心Skill:
  - competitor-selector (竞品筛选)
  - competitor-research-pipeline (全流程编排)

依赖Skill(需挂载):
  - linkfox-amazon-product-detail
  - linkfox-amazon-search
  - linkfox-amazon-search-by-image
  - linkfox-keepa-product-request
  - linkfox-sellersprite-traffic-keyword
  - linkfox-aba-intelligent-query
  - linkfox-aigc-textgen
  - linkfox-report-generator
  - linkfox-voc-review-analysis (可选)

积分消耗预估: 800-1200/次(含ABA反查)
报告输出: 11章HTML标准模板, ~18个ECharts图表
```
