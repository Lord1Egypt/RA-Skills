# 市场分析 skills

**7 个 skill**，5 维度分析编排（市场初步 / 竞品 / 评论 / 关键词 / 合规）+ HTML 报告渲染 + 产品方案生成。

**归属 agent（重要）**：本桶 **7 个全部只在 `linkfox-market-analysis-agent`**，`default` **不包含**。

**用什么 agent**：
- 要跑完整 5 维度市场调研 / 生成 HTML 报告 / 产品方案 → **必须** `--model linkfox-market-analysis-agent`
- 只是查数据（不做多维编排）→ 用 `default` + 亚马逊 / 跨平台桶的 skill（见 [`skills-amazon.md`](skills-amazon.md) / [`skills-third-platforms.md`](skills-third-platforms.md)）

## Skills

| skill | 分析维度 | 用途 | 入参（关键字段） | 返回摘要 |
|---|---|---|---|---|
| `linkfox-market-preliminary` | 市场初步 | 判断这个市场值不值得进（7 维：市场容量/趋势季节性/垄断程度/卖家类型分布/新品友好度/市场竞争/产品形态） | `keyword` 或 `category_node`（二选一）, `marketplace` | 落盘 `data/stage_preliminary.json` + HTML 报告路径 `<session_dir>/reports/*.html` |
| `linkfox-market-competitor` | 竞品 | 打哪几个对手、基本面/产品力/流量结构（6 维：竞品档案/Listing卖点/包装物流/规格定价/流量结构/视觉审美） | `asins`（1-5 个）或 `keyword`/`category_node`, `marketplace` | 落盘 `data/stage_competitor.json` + HTML 报告路径 |
| `linkfox-market-review` | 评论 | 用户在痛什么爱什么缺什么（4 维：差评聚类/好评聚类/客户画像/差异化机会清单） | `confirmed_asins`, `marketplace` | 落盘 `data/stage_review.json`（含 opportunities）+ HTML 报告路径 |
| `linkfox-market-keyword` | 关键词 | 靠哪些词获客、CPC 与竞争成本（4 维：词池构建/核心检索词/搜索量与趋势/竞争与广告成本） | `confirmed_asins`, `marketplace` | 落盘 `data/stage_keyword.json` + HTML 报告路径 |
| `linkfox-compliance-check` | 合规 | 产品是否存在 IP 侵权风险（6 类工具：外观专利/发明专利/文字商标/图形商标/版权/枪支合规） | `image_urls`, `product_title`, `product_description`, `check_type` | 落盘 `data/stage_compliance.json`（含风险等级+免责声明）+ HTML 报告路径 |
| `linkfox-market-html` | HTML 渲染 | 零 LLM 渲染器：扫描 session 内已有 `stage_*.json` 组装为带 ECharts 图表的 HTML | `session_dir` | HTML 报告文件路径 `<session_dir>/reports/<topic>-<ts>.html` |
| `linkfox-product-proposal` | 产品方案 | 基于四份已落盘分析产出 2-4 个可交工厂方案（含功能规格/材质/定价/Listing 草稿/AI 渲染图/IP 预检） | `session_id`, `marketplace`（依赖 `stage_review.json`） | 落盘 `data/stage_proposal.json` + `media/proposal_*.png` + HTML 报告路径 |
