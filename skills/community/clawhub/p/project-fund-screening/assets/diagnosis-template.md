# 项目筛选诊断 — 输入模板与输出骨架

## 一、输入 JSON 模板（交给 scripts/diagnose.py --input）

```json
{
  "project_name": "项目公司名称",
  "stage": "A",                 // seed/angel | pre_a/A | B | C | PE/pre_ipo
  "screen_vc": true,            // 是否做 VC/PE 维度
  "screen_gov": true,           // 是否做政府基金维度
  "landing": {                  // 政府维度所需（只做 VC 时可省略）
    "city": "深圳",
    "sector_aligns_local_plan": true,   // 赛道是否对齐该城市重点投资领域清单
    "return_actions": 2,                // 可认定的返投动作数（本地子公司/研发中心/供应链/招商引荐）
    "intent_register": true,
    "intent_rd_center": true,
    "intent_tax": true,
    "intent_jobs": true
  },
  "facts": {
    "team": {"founders": 2, "key_roles": ["CEO","CTO"], "domain_years": 10, "completeness": "complete"},
    "market": {"tam_tier": 5, "sector": "半导体"},     // tam_tier: 1-5 市场天花板
    "validation": {"has_mvp": true, "pilot_users": 0, "waitlist": 0},
    "tech_barrier": "patent",                          // patent|knowhow|brand|none
    "pmf": {"retention": 0.7, "ndr": 1.2, "signal": true},
    "growth": {"mom": 0.3, "qoq": null},
    "unit_econ": {"ltv_cac": 3.0, "gross_margin": 0.6, "cac_payback_months": 12},
    "moat": "data",                                    // network|data|switching|brand|none
    "financials": {"burn_monthly": 800000, "runway_months": 18, "path_to_profit": "visible"},
    "governance": {"clean": true, "board": true, "audit": false},
    "compliance": {"clean": true},
    "exit": {"path": "ipo", "clear": true}
  }
}
```

> 字段全部可选：缺失项在报告中标记为"待核实"，引擎不会臆造分数。

## 二、输出报告骨架（Markdown）

```
# 项目初步筛选诊断报告：<project_name>
- 融资阶段：<stage>
- 拟落地城市：<city>

## 一、VC/PE 的 BP 阶段就绪度
**综合达标度：<pct>%** （<评级>）
| 准则 | 得分(0-5) | 权重 | 评级 |
🚩 红旗（被毙风险）：<flag ...>

## 二、政府引导/产投基金落地契合度
**综合达标度：<pct>%**
| 准则 | 得分 | 权重 | 评级 |
🚩 红旗：<flag ...>

## 三、综合结论与整改建议
1. <建议>
2. ...
> 免责声明（基于国办发〔2025〕1号 及 2025-2026 细则自动生成，不构成正式投资建议）
```
