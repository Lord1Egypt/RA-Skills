# HTML 报告合同

## 目标

使用 `assets/report-template.html` 和 `scripts/render_report.py` 把同一轮 `decision_result.v1` 与决策输入渲染成自包含、响应式、可打印的 HTML。模板只负责展示，不能重新计算或覆盖动作、基金、金额、目标权重、回撤、换手或审计哈希。

## 唯一入口

```bash
python3 scripts/render_report.py \
  --decision-result work/decision-result.json \
  --decision-input work/decision-input.json \
  --diagnostic-result work/diagnostic-result.json \
  --output work/fund-position-report.html
```

`--diagnostic-result` 可省略。诊断结果只能显示为研究候选，不能覆盖正式结果。不要复制旧报告后手工替换数字，也不要让模型直接拼接另一份 HTML。

## 输入约束

- 正式结果必须是 `decision_result.v1`；
- 决策输入必须含 `quant_strategy_context.v2`、`investor_policy.v1`、同日现金、交易活动和 `ai_investment_view.v1`；
- 正式结果、上下文、政策版本和日期必须一致；
- `ACTIVE` 之外不得出现 `amountCny`；无交易动作不得携带金额；
- 有效 ACTIVE 交易必须使用资金内核输出的正金额；
- 基金代码与名称必须和同轮持仓目录一致；
- 目标权重合计必须为 100%；
- 正式结果必须含 `canonicalOutputHash`。

任一约束失败时，脚本以非零状态退出并输出 `REPORT_BLOCKED`，不得回退到模型手写金额或静态旧报告。

## 展示规则

渲染器必须直接从结构化数据生成：

- 唯一动作、方向、基金和金额；
- 数据、政策与 critic 门禁；
- 全账户资产分布；
- 战略目标与战术目标；
- 逐基金 MCP 因子、AI 袖套方向和失效条件；
- 证据事实、AI 推断、情景概率和独立反方审查；
- 基金子组合回撤与政策有效回撤；
- 普通换手、保护性卖出和风险后再入场分桶；
- 下一次复核路径与机器审计入口。

所有文本进行 HTML 转义。已知基金名称或代码在正文出现时，渲染器统一扩展为“基金原名（6位代码）”。机器审计链接必须写明 JSON 不是程序源码。首屏不得出现工具轨迹、内部阻断码或第二笔引擎之外的交易建议。

用户可见正文必须把内部枚举翻译成自然中文，例如：

- `broad_downtrend` → “宽基指数整体处于下行趋势”；
- `OVERWEIGHT / NEUTRAL / UNDERWEIGHT` → “建议提高 / 维持 / 降低权重”；
- `HOLD / BLOCKED` → “保持不动 / 暂不执行”；
- `PASS_WITH_LIMITS` → “通过，但仍有约束”；
- `STATIC_CASH_PROXY_V1` → “静态现金代理法”；
- `MA20 / MA60` → “20日均线 / 60日均线”。

不要在普通投资者正文显示原始英文枚举。它们只保留在机器审计 JSON 中。

证据必须按日期分层：

- `asOfDate` 等于报告日期的材料显示在“当日证据”；
- 早于报告日期的材料只能折叠显示为“中期背景证据”，并明确说明不是今日新增消息；
- 没有同日可信资讯时必须直说，不得用旧公告、旧财报或旧研报填充“今日新闻”位置；
- 报告日期、发布日期和来源必须同时可见，旧材料不得排在同日证据之前。

## 交互与可访问性

- “仅看结论”只隐藏深度研究区，不改变动作；
- “打印报告”只调用浏览器打印；
- 使用原生 `details` 展开基金与审计数据；
- 保留键盘焦点、跳转正文、WCAG AA 对比、减少动态效果、窄屏和打印样式；
- 不加载远程字体、脚本、图片或分析服务；报告离线可读。

## 交付校验

生成后至少执行：

```bash
python3 -m unittest discover -s scripts/tests -p 'test_*.py'
```

再在桌面与窄屏各打开一次，确认：

- 首屏动作、基金和金额与 `decision_result.v1` 一致；
- SHADOW、BLOCKED、HOLD 不泄漏影子金额；
- 每一处基金引用同时显示名称和代码；
- 用户可见正文没有未解释的内部英文枚举、状态码或算法名；
- 证据正文被转义，没有脚本注入；
- JSON 按钮打开机器审计数据，不被描述为源码；
- 结论视图、展开、打印和移动端布局可用。
