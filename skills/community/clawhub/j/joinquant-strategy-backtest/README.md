# ClawHub — 聚宽策略回测代码生成框架

> 基于 Hermes Agent Skill 架构，自动生成可直接在聚宽平台运行的回测代码。

## 功能

- **六段式骨架模板**：统一的聚宽策略代码结构（initialize → before_trading_start → 信号模块 → handle_data → after_trading_end）
- **截面多因子选股**：使用聚宽原生API（get_fundamentals + attribute_history）获取因子数据，按多因子打分排序选股
- **时序技术指标择时**：基于EMA金叉/死叉的双均线择时策略
- **因子IC查询**：直接访问聚宽因子库页面 `https://www.joinquant.com/view/factorlib/list` 查看IC
- **API速查**：聚宽平台API快速参考（下单/数据/上下文/调度/代码格式）

## 目录结构

```
clawhub/
├── SKILL.md                              # 主技能文档（六段式骨架+截面/时序/因子推荐）
├── references/
│   └── joinquant-api-access-pitfalls.md  # 聚宽API访问陷阱与解决方案
└── templates/
    └── basic_strategy_template.py        # 基础六段式骨架模板
```

## 使用方式

1. 将 `SKILL.md` 加载为 Hermes Agent Skill
2. 告诉 Agent 你的策略需求（因子/标的/参数）
3. Agent 自动选择模板、填入参数、生成完整代码
4. 复制到聚宽平台运行回测

## 许可

MIT
