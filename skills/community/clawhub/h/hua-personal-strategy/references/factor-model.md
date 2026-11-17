# 多因子模型与交叉检查

本 skill 是个人场外基金策略，不做股票选股，不做自动交易。因子只用于形成可审计的研究信号；交易仍需用户确认。

## 因子分层

### 核心收益因子

只使用官方净值、真实持仓和服务端组合历史可审计的数据：

- `a_share_market_regime`：A股整体模式，不等同于持仓模式。至少覆盖上证指数、沪深300或中证A500、创业板、科创50；优先同时看日线、周线、月线/年线。若只能取到日线或实时点，必须标注缺失周期，不能用单一周期推断整体牛熊。
- `growth_style_regime`：成长风格模式。覆盖科创50、创业板、半导体ETF、AI/科技代表指数、恒生科技、纳指100/KOSPI。用于判断科技/成长是普通回调、杀拥挤、杀估值还是趋势破坏。
- `decline_type`：下跌性质分类。取值为 `leverage_flush`（杀杠杆/杀拥挤）、`valuation_reset`（杀估值）、`bull_washout`（牛市洗盘）、`systemic_bear`（系统性熊市）、`unknown`。必须由跌幅、量能/资金流、跨市场同步性、消息反证和修复质量共同决定。
- `market_regime`：**多指数加权基准**（科创50/半导体ETF/纳指100/韩国KOSPI/恒生科技/沪深300按持仓权重加权），不只用沪深300。沪深300代表不了科技/半导体持仓。
- `cross_market_factor`：**跨市场联动因子**——A股半导体与全球供应链深度绑定，但只能作为辅助确认，不能替代基金级净值、夜盘和风控：
  - 韩国KOSPI（三星/SK海力士）：大A盘中实时指标（时区仅差1小时），A股半导体领先指标
  - 纳指100期货NQF：纳指/美股科技相关 QDII 和 A股科技风险偏好的辅助实时指标
  - 恒生科技HSTECH：港股科技实时指标
  - **KOSPI-A股半导体背离信号**：KOSPI涨但A股半导体跌 = 均值回归机会（70-80%时间联动，偶尔脱钩是买点）
- `absolute_momentum`：基金 R20/R60/R120/R250，分别约代表近 1 月、近 3 月、近 6 月、近 1 年。日常轮动判断必须同时看四个窗口，不得只看近 6 月和近 1 年。
- `relative_momentum`：同 `direction` 或跨方向的动量百分位。
- `rotation_acceleration`：近 1 月相对近 3 月月均的加速度（`R20 - R60/3`）和近 3 月相对近 6 月月均的加速度（`R60 - R120/2`）。用于判断板块是否正在加速、失速或只是旧趋势惯性。
- `mean_reversion`：BIAS5/BIAS20，用于震荡市回归和极端偏离判断。
- `trend_quality`：基金 MA20/MA60、cross_down、是否仍在中期趋势上。
- `fund_risk`：单基金官方净值计算的最大回撤、年化波动、净值覆盖率和有效点数。不得用组合回撤替代。
- `portfolio_risk`：服务端真实组合最大回撤、波动、覆盖率和缺失警告。
- `portfolio_execution_risk`：盘中执行回撤估算。官方当前回撤 + 按持仓权重加总的 A 股实时估值/QDII 夜盘冲击，只用于风控门禁、停止新增、暂停高波动定投和防守判断；不得计入真实收益、组合净值、官方最大回撤或快照里的官方收益。
- `fund_multifactor_score`：每只真实持仓的 0–100 综合评分。分项至少包含价格趋势、BIAS/均值回归、单基金风险、实时/QDII 执行、消息情绪证据、申购流动性和数据质量。该分数是动作主轴，但不能绕过硬风控门禁。
- `opportunity_direction_score`：候选方向的 R20/R60/R120/R250、轮动加速度、趋势质量、估值分位、资金流、拥挤度和当前组合暴露。近 1 月和近 3 月权重高于近 6 月和近 1 年。

### 风控与执行因子

这些因子只允许阻断、降级或限制金额，不直接制造收益信号：

- `equity_beta_budget`：权益总仓位和高 Beta 仓位预算。熊市/强防守模式下，高 Beta 权益方向必须先降权；宽基只是低 Beta 权益，不得被写成避险资产。
- `defensive_asset_preference`：现金、货基、短债、纯债、黄金、红利低波等防守方向优先级。没有高置信防守方向时，现金/货基优先于强行迁入新权益板块。
- `post_trade_exposure`：在途买卖确认后的预计暴露。若 MCP 暂未直接返回预计暴露，Agent 只能定性说明，不得自行在报告中伪造精确风险下降幅度。
- `direction_concentration`：单方向超过 45% 时触发再平衡提示。
- `fund_loss_review`：单只持有收益率低于 -15% 时强制检视，不自动止损。
- `fund_drawdown_review`：单基金历史最大回撤或年化波动异常时降级新增；数据缺失时禁止可执行新增。
- `fee_liquidity`：申购状态、限购额度、确认天数。
- `realtime_execution`：当日估值、盘中涨跌、板块资金流和 QDII 夜盘估算，只修正执行时机和仓位强度；面向用户时称为“盘中/夜盘执行过滤”。QDII 普通估值只用于解释官方/估算归属收益，今天申赎更看夜盘接口。
- `qdii_readiness`：QDII 夜盘数据是否 ready、是否包含估算涨跌幅、是否 fresh、覆盖率是否足够、汇率是否可用、对应交易夜盘是否匹配当前执行窗口。
- `qdii_attribution_quality`：QDII/T+N 官方收益是否有可靠 G 日证据。缺少 `displayDate/publish_date/lastNavPublishDate/estimateVsActual.publish_date` 时，不得把官方涨跌计入“今天收益”，只能标注“未可靠归属”。
- `qdii_holdings_breakdown`：夜盘接口中的重仓个股涨跌、汇率、覆盖率、缺失成分和贡献拆解。它是夜盘估算解释因子，不是持有收益因子；单个股票大涨/大跌不得直接等同为基金涨跌。
- `data_quality`：持仓同步时间、净值覆盖、资讯时间、组合历史覆盖。

### 消息面因子

消息面是独立确认/否决层，不直接单独触发买入：

- `news_policy`：政策、监管、产业规划、会议口径。
- `news_company`：基金重仓方向相关公司的公告、业绩预告、订单、减持、处罚。
- `news_research`：东财研报、券商观点和行业跟踪，只能作为观点证据，不能替代价格因子。
- `news_event`：突发事件、地缘、供需扰动、产品发布。
- `news_recency`：默认只接受今天或最近 36 小时；非交易日可扩展到最近一个交易日。

规范输出：

- `news_factor.status`: `supportive` / `neutral` / `negative` / `stale` / `unknown`
- `news_factor.strength`: `strong` / `medium` / `weak`
- `news_factor.sources`: 至少包含来源、发布时间、标题或摘要。
- `news_factor.veto`: 重大反证时为 true。

### 情绪面因子

情绪面是风险温度计，不是收益核心因子。只使用东财 skill 或 HuahuaDaily 市场接口中的公开市场数据，不使用花花社区/喵舍数据：

- `sentiment_flow`：东财资金流、板块资金流、基金资金流的连续性和方向。
- `sentiment_rank_heat`：东财阶段涨跌幅、成交/关注热度、公开市场排名热度。
- `sentiment_news_tone`：东财资讯中的一致预期、风险偏好和主题热度。
- `sentiment_extreme`：过热、恐慌、拥挤交易迹象。

规范输出：

- `sentiment_factor.status`: `risk_on` / `neutral` / `risk_off` / `crowded` / `unknown`
- `sentiment_factor.strength`: `strong` / `medium` / `weak`
- `sentiment_factor.veto`: 极端拥挤、单日异常或明显反向资金流时为 true。
- `sentiment_factor.note`: 简短说明。

情绪分必须按策略场景解释，不能机械同向加分：

- 趋势确认：`risk_on` 可增强趋势信号；`risk_off` 不能增强追随信号，只能轻微降级。
- 逆向低吸：`risk_off` 可增强恐慌测试或震荡回归信号；`crowded` 降级。
- 减仓避险：`negative`、`risk_off`、`crowded` 增强减仓紧迫度；`risk_on/supportive` 降低减仓紧迫度。

### 证据与否决因子

这些因子不进入收益公式，只做解释、交叉验证或风险否决：

- `eastmoney_numeric`：行业涨跌幅、资金流、公告/研报中的可核验数值。
- `eastmoney_news`：近期政策、公告、事件催化和反证。
- `serenity_chain`：产业链位置、瓶颈、公开证据链、反方理由。
- `public_rank_heat`：东财或公开市场阶段排名热度，仅作情绪温度，不作核心收益因子。
- 花花社区、喵舍、弹幕、用户持有人排行和社区关注不得进入任何因子；如用户主动询问，只能作为产品内样本偏差背景说明。

当前策略不设默认防御基金，也不设防御底仓比例。016858、023299 不能被默认视为防御资产；如用户未来指定防御资产，也只作为普通基金参与统一信号规则，不享有“不能加减仓”的特殊规则。

## 方向迁移

迁移决策分三层，不能跳层：

1. **组合层**：先判断真实组合是否允许新增或轮动。若回撤阈值、数据质量、申购状态或用户资金门禁不通过，只能输出只复盘，不给可执行交易。
2. **方向层**：再判断哪些方向继续持有、降低暴露、优先研究迁入或暂不纳入。方向必须经过价格、估值、资金流、消息、情绪、Serenity 和拥挤度交叉验证。
3. **基金层**：当前不做自然语言全市场选基。只有用户点名基金代码、基金已在持仓/自选中，或未来存在专用结构化筛选接口时，才做单基金比较。

候选方向结论：

- `PRIORITY_RESEARCH`：优先研究迁入，不等于买入。
- `WATCH`：候选跟踪。
- `AVOID`：暂不纳入。

方向评分不能替代真实持仓风控。即使某个方向评分高，只要组合回撤门禁、QDII 夜盘、申购状态或消息反证不通过，也不能生成可执行新增金额。

熊市或强防守模式下，方向迁移必须先给资产级结论，再给基金级动作：

1. 降低高 Beta 权益方向：科创、半导体、AI、创业板、军工、海外科技。
2. 判断低 Beta 权益是否仅保留观察仓：沪深300、中证A500、红利低波。
3. 判断真防守仓：现金/货基/短债/纯债/黄金。
4. 若没有稳定迁入方向，明确写“现金等待”，不要强行推荐基金。

## 冲突处理

- 价格因子给出 ADD，但服务端真实组合回撤超过 `get_quant_strategy_context.portfolio.risk.configuredMaxDrawdownLimitPct`，或盘中执行回撤估算接近/超过该阈值，或降级路径中 `get_records.strategyPreferences.maxDrawdownLimitPct` 触发，且该阈值大于 0：降级为 `CONDITIONAL_ADD`，金额为 0。阈值为 0 表示未启用，不得自行假定 10%。
- 价格因子给出 ADD，但 Serenity 或东财出现强反证：降级为 `CONDITIONAL_ADD` 或 `HOLD`。
- 价格因子给出 ADD，但 `news_factor.veto=true` 或 `sentiment_factor.veto=true`：降级为 `CONDITIONAL_ADD`，金额为 0。
- 没有价格因子支持时，即使消息面强利好或情绪 risk_on，也不得单独生成 ADD。
- 情绪 risk_off 只在恐慌测试或均值回归语境中提供逆向加分；不得在趋势追随语境中鼓励追高。
- 近 6 月或近 1 年强，但近 1 月、近 3 月明显失速时，不得仅凭长期收益给出新增；应降级为继续持有或轮动风险提示。
- 近 1 月突然转强但近 3 月、近 6 月仍弱时，不得直接追涨；必须结合 BIAS、实时估值、资金流、消息和申购状态，最多先进入优先研究或小额跟踪。
- 实时大涨不是机械禁止买入：趋势市且中期趋势、方向动量、资金流或消息面同时确认时，可以保留趋势追随，但金额降档并提示追高风险。
- 实时大涨在震荡市或缺少确认时，ADD 必须降级为等待回落，不给可执行新增金额。
- 实时大跌不是机械禁止卖出：若 MA20/MA60 破坏、资金流转负或消息面反证，进入降低暴露；若中期趋势未坏且处于恐慌/超跌语境，只允许小额逆向测试。
- 大跌日不能直接按“跌多了就低吸”。低吸必须同时满足：市场未进入 `valuation_reset/systemic_bear`、主线资金流出收敛、实时跌幅不再扩大、同方向强势标的先修复、组合回撤门禁允许。
- `leverage_flush` 中可以战术减仓但保留核心底仓；`valuation_reset` 中应提高现金/短债权重；`bull_washout` 中只允许等待反包确认后分批恢复；`systemic_bear` 中禁止主动加高 Beta 权益。
- QDII 夜盘涨跌必须纳入执行层。普通估值接口的 QDII 涨跌可解释官方/估算归属收益，但不能替代夜盘作为今天加减仓参考；夜盘数据缺失、过期、覆盖率弱、汇率缺失或交易日不匹配时，不允许形成可执行新增。
- 板块迁移不是追热点：方向涨幅过大且拥挤度高时，即使消息面强，也只能标为候选跟踪或等待回落。
- 用户点名基金与现有持仓重合度高于 60% 时，必须说明它是“替代比较”还是“重复暴露”；没有回撤、波动、跟踪质量、申购流动性或管理优势时不得提高研究优先级。费率只作背景，不单独触发买卖。
- 价格因子给出 REDUCE，但用户偏好“卖飞负效用高”：牛市中不得只因 BIAS 高自动卖出，只能转为不动或暂不调出。
- 市场模式在 1.8%–2.2% 缓冲区：只保持同方向的上次 BULL/BEAR；方向变化、上次 RANGE 或无历史状态时按 RANGE。
- 数据覆盖不足：禁止可执行新增金额；允许输出只复盘结论和下一步需要的数据。

## 交叉检查清单

每次输出前检查：

- MCP manifest 是否包含 `get_quant_strategy_context`、`run_portfolio_backtest`、`save_quant_snapshot`、`get_quant_snapshot_review`；降级路径再检查 `get_portfolio_nav_history`、`get_batch_fund_nav_history`。
- 当前持仓总市值是否来自 `get_quant_strategy_context.portfolio.totalMarketValue`；降级路径是否用 `get_records` 和 `get_summary` 交叉核对。
- 组合回撤阈值是否来自 `get_quant_strategy_context.portfolio.risk.configuredMaxDrawdownLimitPct`；降级路径是否来自 `get_records.strategyPreferences.maxDrawdownLimitPct`；阈值为 0 时是否明确标注未启用。
- 官方组合回撤是否来自 `get_quant_strategy_context.portfolio.risk` 或降级路径中的 `get_portfolio_nav_history`，而不是 Agent 自行拼接。
- 盘中执行回撤估算是否单独标注：它可由实时估值/QDII 夜盘按权重估算，用于交易门禁；但不得写成官方真实回撤。
- 基金历史指标是否来自 `get_quant_strategy_context.portfolio.holdings[].metrics`；降级路径是否来自 `get_batch_fund_nav_history`，且逐基金检查 `complete/coverageStart/coverageEnd/baselineDate`。
- 基金和方向动量是否同时展示近 1 月、近 3 月、近 6 月、近 1 年和轮动加速度；若只展示近 6 月/近 1 年，报告不合格。
- 单基金最大回撤和年化波动是否来自官方净值历史或服务端指标；缺失时是否明确标注“不可计算/本次未取到”。
- 市场模式是否输出 `gap`、双阈值规则、上次模式来源。
- 每个 ADD/REDUCE/ROTATE_REVIEW 是否能追溯到至少一个核心价格因子和所有阻断项。
- 消息面和情绪面是否独立输出 `news_factor` / `sentiment_factor`，且没有脱离价格因子单独触发 ADD。
- Serenity 和东财是否只作为证据/否决或置信度调节，不作为收益分数。
- 是否完全排除了花花社区/喵舍/弹幕/用户持有人排行等产品内偏样本数据。
- 是否展示盘中/夜盘执行过滤：估值/夜盘时间、涨跌幅、执行判断和对金额的修正。
- 是否输出 A股整体模式、成长风格模式、持仓加权模式；若缺任一层，是否明确标注数据缺失。
- 是否明确下跌性质：杀杠杆/杀拥挤、杀估值、牛市洗盘、系统性熊市或 unknown；不得只写“市场较弱”。
- 是否把宽基误写为避险资产；宽基只能是低 Beta 权益，真正防守是现金/货基/短债/纯债/黄金/红利低波。
- 是否执行防踏空卖出审查：卖弱腿还是卖核心、是否保留同方向强腿、卖出后是否仍有反弹参与。
- QDII 是否明确区分 D 日、G 日、普通估值接口与夜盘接口：官方收益按 G 日归属，普通估值解释归属/估值，夜盘接口用于今天申赎时点判断。
- QDII 夜盘是否使用 `estimatedChangePercent`、`freshness`、`coverage/breakdown`、`fx` 和 `reason/availability`，而不是只检查 `ready`。
- 持有收益、累计收益、组合市值是否标注不含盘中估算和 QDII 夜盘。
- 板块迁移是否只输出方向池结论，不把自然语言选基包装成基金推荐。
- 用户点名基金比较是否明确标注来源，不写成系统筛选。
- 机会池是否只输出研究优先级，没有直接输出交易指令。
- snapshot 是否不含建议金额、建议份额、虚拟现金、虚拟收益或交易动作。

## 回测措辞

`run_portfolio_backtest` 和组合回放使用 HuahuaDaily 服务端权威口径，但数据基准是 `official_final`，不能宣称严格 point-in-time。报告中使用“服务端历史试算”“基于官方终值净值的回放”，不要写成“无前视实盘收益”。
