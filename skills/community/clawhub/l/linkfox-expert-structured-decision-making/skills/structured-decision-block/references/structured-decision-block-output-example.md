# Structured Decision Block — Output Example (v0.2)

This is the **standardized output** the decision module must produce.

It is designed to be:
- Human-readable (for reports)
- Machine-parseable (for automation, QA, downstream agents)
- Explicit about evidence + counter-evidence

---

## 决策块

**最终判定**: 🟢 推荐进入（中高优先级）  
**综合得分**: 82 / 100  
**置信度**: 0.81 (数据完整率 87%，反证条件较清晰)

### 维度得分与档位

| 维度 | 当前值 | 模块评分 (0-10) | 权重 | 档位 | 主要驱动证据 |
|------|--------|------------------|------|------|-------------|
| 市场增长潜力 | 38% YoY | 8.5 | 20 | 🟢 | Google Trends +52%, ABA 改善 31% |
| 竞争集中度 (CR3) | 42% | 6.8 | 18 | 🟡 | 前台搜索 + 卖家精灵聚合 |
| 新品友好度 | 18% 成功率 | 7.9 | 15 | 🟢 | 极目 + 前台新品分布 |
| 利润空间（零广告策略） | 28.5% 净利润率 | 8.7 | 25 | 🟢 | S6 Keepa + 1688 货源核算 |
| 进入门槛（评论/上架） | 平均 1200 评论，14 个月 | 6.5 | 12 | 🟡 | Keepa + 前台 |
| 货源与供应链风险 | 3 个可验证货源 | 8.0 | 10 | 🟢 | 1688 匹配 + AIGC 验证 |

**加权总分计算说明**：使用 business_context.weights（利润 25、增长 20 等）。一票否决未触发。

### 一票否决项
- 无（所有硬约束满足）

### 主要支持证据（Top 3）
1. **利润健康**：Top ASIN 按零广告策略核算净利润率 28.5%，高于稳健型 25% 门槛（S6.4-C + Keepa 正常 Buybox 价）。
2. **增长真实**：Google Trends 年度增长 52% + ABA 排名改善 31%，社媒验证触发且找到真实讨论驱动因素。
3. **新品窗口存在**：新品成功率 18%，近 6 月上架且进入 Top 50 的占比高于类目均值。

### 反证条件（什么情况下结论会失效）
1. **趋势反转**：Google Trends 或 ABA 最近 8 周连续恶化超过 15%（连续 4 周以上）。
2. **成本假设崩盘**：真实 FBA 费用或退货率比模型高 30% 以上，或 1688 实际起批量 ≥ 当前预估的 2 倍且无更优货源。
3. **竞争强度突变**：SIF sponsoredProductsKeywordCount 显著上升（头部品牌突然加投），或 CR3 快速升至 55%+。
4. **数据新鲜度失效**：距离本次扫描超过 14 天且未重新跑决策模块（尤其是趋势类维度）。

**如何使用反证**：建议为每个高优先级维度设置监控（定时任务），一旦反证条件命中，自动触发重新扫描或降级告警。

### 推荐动作（已排序）
**优先级 1（立即可执行）**
- 锁定 Top 3 差异化切入方向（标题/主图/卖点），基于当前低分高销量竞品的痛点（S5 商业洞察 + 前台低分商品）。
- 准备 3–5 个变体，广告预算控制在日均 X 元，跑 7–10 天真实转化测试（重点观察自然流量占比）。

**优先级 2（本周内）**
- 对 Top ASIN 做 1688 货源二次验证（起批量、质量、稳定供货能力）。
- 建立基础监控：SIF 曝光结构 + Google Trends 周数据 + 主要竞品广告强度。

**优先级 3（观察期）**
- 如果测试 7 天后转化率 > 目标且 ACOS < 市场均值，升级为中高预算主推。
- 每 14 天自动复扫一次（使用 linkfox-task-scheduler），对比反证条件。

### 数据质量与局限
- 数据完整率：87%
- 主要局限：
  - ABA 为周维度，非实时
  - 1688 货源匹配仍需人工确认实际起批量与质量
  - 前台搜索样本为 3 页（约 150 个非广告商品），代表性有限
- 建议：利润核算部分必须在真实上架前用当前真实 FBA 费 + 佣金 + 头程重新跑一次。

---

**JSON 版本**（供自动化消费）
```json
{
  "verdict": "🟢",
  "verdict_text": "推荐进入（中高优先级）",
  "overall_score": 82,
  "confidence": 0.81,
  "dimensions": [...],
  "vetoes": [],
  "counter_evidence": [
    "Google Trends 或 ABA 最近8周连续恶化 >15%",
    "真实 FBA/退货率比模型高30%+",
    ...
  ],
  "recommended_actions": [
    {"priority": 1, "action": "..."},
    ...
  ],
  "data_limitations": [...]
}
```

---

## Usage Notes for Consumers

- Always surface **反证条件** to the user.
- The decision block should be the **last major section** of the report (after all data-source chapters and S6 deep analysis).
- Automation can key off `verdict` and `overall_score` to decide next steps (create task, schedule re-scan, escalate, etc.).
- When risk_preference changes, re-run the decision module on the same upstream payload for different verdicts.