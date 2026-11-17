# 财务信息 — 16 个接口

> 本文件由 `tools/generate_catalog.py` 从 OpenAPI 规范自动生成，请勿手工编辑。

## perf_forecast — 公司业绩预告

`GET /api/v1/data/perf_forecast`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `market_code` | 否 | 市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date-time |  |
| `report_year` | 否 | 报告年度，YYYY-03-31为一季度，YYYY-06-30为中报，YYYY-09-30为三季报，YYYY-12-31为年报；操作符：between（逗号分隔两个边界） | string/date |  |
| `performance_type_code` | 否 | 业绩类型编码 | string | 035001=业绩大幅上升；035002=业绩大幅下降；035003=业绩预增；035004=业绩预降；035005=业绩预盈；035006=业绩预亏；035007=业绩持平；035008=预计扭亏；035009=预计减亏；035010=不确定；035011=取消预测；035013=无大幅变动；035014=大幅减亏 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_name` | string | 证券简称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `announcement_date` | string/date-time | 公告日期；默认返回 |
| `report_year` | string/date | 报告年度；默认返回 |
| `performance_type_code` | string | 业绩类型编码；默认返回 |
| `performance_type` | string | 业绩类型；默认返回 |
| `performance_forecast_content` | string | 业绩预告内容 |
| `performance_change_reason` | string | 业绩变化原因 |
| `latest_record_flag` | string | 报告期最新记录标识；默认返回 |
| `period_net_profit_min` | number | 本期净利润下限；默认返回 |
| `period_net_profit_max` | number | 本期净利润上限；默认返回 |
| `period_net_profit_change_min` | number | 本期净利润增减幅下限；默认返回 |
| `period_net_profit_change_max` | number | 本期净利润增减幅上限；默认返回 |
| `remark` | string | 备注 |
| `market_code` | string | 市场编码；默认返回 |
| `period_adjusted_net_profit_min` | number | 本期扣非后净利润下限；默认返回 |
| `period_adjusted_net_profit_max` | number | 本期扣非后净利润上限；默认返回 |
| `period_adjusted_net_profit_change_min` | number | 本期扣非后净利润增减幅下限；默认返回 |
| `period_adjusted_net_profit_change_max` | number | 本期扣非后净利润增减幅上限；默认返回 |

## perf_express — 公司业绩快报

`GET /api/v1/data/perf_express`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `market_code` | 否 | 市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `start_date` | 否 | 开始日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_name` | string | 证券简称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `start_date` | string/date | 开始日期；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `report_source_code` | string | 报表来源编码；默认返回 |
| `report_source` | string | 报表来源；默认返回 |
| `net_profit` | number | 净利润；默认返回 |
| `total_assets` | number | 总资产；默认返回 |
| `shareholders_equity` | number | 股东权益（不含少数股东权益）；默认返回 |
| `eps` | number | 每股收益；默认返回 |
| `roe` | number | 净资产收益率；默认返回 |
| `roe_weighted` | number | 净资产收益率-加权；默认返回 |
| `net_assets_per_share` | number | 每股净资产；默认返回 |
| `remark` | string | 备注 |
| `market_code` | string | 市场编码；默认返回 |

## fin_indicators — 上市公司财务指标

`GET /api/v1/data/fin_indicators`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `market_code` | 否 | 市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `start_date` | 否 | 开始日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `report_year` | 否 | 报告年度，YYYY-03-31为一季度，YYYY-06-30为中报，YYYY-09-30为三季报，YYYY-12-31为年报；操作符：between（逗号分隔两个边界） | string/date |  |
| `consolidation_type_code` | 否 | 合并类型编码 | string | 071001=合并本期；071002=合并上期 |
| `data_source_code` | 否 | 数据来源编码 | string | 033001=招募说明书；033002=上市公告书；033003=定期报告；033004=业绩快报；033006=转让说明书；033008=预披露公告；033012=换股报告书；033013=其他；033014=重新上市报告书；033016=更正或补充；033017=特殊来源；033020=审计报告；033022=重新上市-转让说明书；033024=减持进展公告 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `start_date` | string/date | 开始日期；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `report_year` | string/date | 报告年度；默认返回 |
| `consolidation_type_code` | string | 合并类型编码；默认返回 |
| `consolidation_type` | string | 合并类型；默认返回 |
| `data_source_code` | string | 数据来源编码；默认返回 |
| `data_source` | string | 数据来源；默认返回 |
| `eps` | number | 每股收益；默认返回 |
| `basic_eps` | number | 基本每股收益；默认返回 |
| `diluted_eps` | number | 稀释每股收益；默认返回 |
| `eps_excl_non_recurring` | number | 扣除非经常性损益每股收益；默认返回 |
| `undistributed_profit_per_share` | number | 每股未分配利润；默认返回 |
| `net_assets_per_share` | number | 每股净资产；默认返回 |
| `adj_net_assets_per_share` | number | 调整后每股净资产；默认返回 |
| `capital_reserve_per_share` | number | 每股资本公积金；默认返回 |
| `operating_profit_margin` | number | 营业利润率；默认返回 |
| `operating_tax_rate` | number | 营业税金率；默认返回 |
| `operating_cost_rate` | number | 营业成本率；默认返回 |
| `investment_yield` | number | 投资收益率；默认返回 |
| `roa` | number | 总资产报酬率；默认返回 |
| `net_profit_margin` | number | 净利润率；默认返回 |
| `general_admin_expense_ratio` | number | 管理费用率；默认返回 |
| `finance_expense_ratio` | number | 财务费用率；默认返回 |
| `cost_to_profit_ratio` | number | 成本费用利润率；默认返回 |
| `three_expenses_ratio` | number | 三费比重；默认返回 |
| `receivable_turnover` | number | 应收帐款周转率；默认返回 |
| `inventory_turnover` | number | 存货周转率；默认返回 |
| `working_capital_turnover` | number | 运营资金周转率；默认返回 |
| `asset_turnover` | number | 总资产周转率；默认返回 |
| `fixed_asset_turnover` | number | 固定资产周转率；默认返回 |
| `accounts_receivable_days` | number | 应收帐款周转天数；默认返回 |
| `inventory_days` | number | 存货周转天数；默认返回 |
| `current_asset_turnover` | number | 流动资产周转率；默认返回 |
| `current_asset_days` | number | 流动资产周转天数；默认返回 |
| `total_asset_days` | number | 总资产周转天数；默认返回 |
| `shareholder_equity_turnover` | number | 股东权益周转率；默认返回 |
| `current_asset_ratio` | number | 流动资产比率；默认返回 |
| `cash_funds_ratio` | number | 货币资金比率；默认返回 |
| `trading_financial_asset_ratio` | number | 交易性金融资产比率；默认返回 |
| `inventory_ratio` | number | 存货比率；默认返回 |
| `fixed_asset_ratio` | number | 固定资产比率；默认返回 |
| `debt_structure_ratio` | number | 负债结构比；默认返回 |
| `debt_to_equity` | number | 产权比率；默认返回 |
| `net_asset_ratio` | number | 净资产比率；默认返回 |
| `debt_to_asset_ratio` | number | 资产负债比率；默认返回 |
| `current_ratio` | number | 流动比率；默认返回 |
| `quick_ratio` | number | 速动比率；默认返回 |
| `cash_ratio` | number | 现金比率；默认返回 |
| `interest_coverage_ratio` | number | 利息保障倍数；默认返回 |
| `working_capital` | number | 营运资金；默认返回 |
| `non_current_liability_ratio` | number | 非流动负债比率；默认返回 |
| `current_liability_ratio` | number | 流动负债比率；默认返回 |
| `conservative_quick_ratio` | number | 保守速动比率；默认返回 |
| `cash_to_debt_ratio` | number | 现金到期债务比率；默认返回 |
| `tangible_asset_debt_ratio` | number | 有形资产净值债务率；默认返回 |
| `revenue_growth_rate` | number | 营业收入增长率；默认返回 |
| `net_profit_growth_rate` | number | 净利润增长率；默认返回 |
| `net_asset_growth_rate` | number | 净资产增长率；默认返回 |
| `fixed_asset_growth_rate` | number | 固定资产增长率；默认返回 |
| `total_asset_growth_rate` | number | 总资产增长率；默认返回 |
| `investment_income_growth_rate` | number | 投资收益增长率；默认返回 |
| `operating_profit_growth_rate` | number | 营业利润增长率；默认返回 |
| `cash_flow_per_share` | number | 每股现金流量；默认返回 |
| `operating_cash_flow_per_share` | number | 每股经营现金流量；默认返回 |
| `operating_cash_to_current_debt` | number | 经营净现金比率（短期债务）；默认返回 |
| `operating_cash_to_total_debt` | number | 经营净现金比率（全部债务）；默认返回 |
| `ocf_to_net_profit_ratio` | number | 经营活动现金净流量与净利润比率；默认返回 |
| `revenue_cash_ratio` | number | 营业收入现金含量；默认返回 |
| `total_asset_cash_recovery` | number | 全部资产现金回收率；默认返回 |
| `roe_deducting_non_recurring` | number | 净资产收益率(扣除非经常性损益)；默认返回 |
| `roe_weighted` | number | 净资产收益率-加权；默认返回 |
| `roe_weighted_deducting_non_recurring` | number | 净资产收益率-加权(扣除非经常性损益)；默认返回 |
| `org_name_en` | string | 机构名称（英文）；默认返回 |
| `consolidation_type_en` | string | 合并类型（英文）；默认返回 |
| `data_source_en` | string | 报表来源(英文)；默认返回 |
| `sec_name_en` | string | 证券简称（英文）；默认返回 |
| `net_profit_deducting_non_recurring` | number | 扣除非经常性损益的净利润（本年）；默认返回 |
| `non_recurring_profit_loss` | number | 非经常性损益合计；默认返回 |
| `gross_profit_margin` | number | 毛利率；默认返回 |
| `period_expense_ratio` | number | 期间费用率；默认返回 |
| `cash_conversion_cycle` | number | 现金转换周期；默认返回 |
| `roe` | number | 净资产收益率；默认返回 |
| `net_profit_cash_content` | number | 净利含金量 |
| `non_recurring_profit_loss_ratio` | number | 非经常性损益占比；默认返回 |
| `period_expense_growth_rate` | number | 期间费用增长率；默认返回 |
| `basic_earning_power` | number | 基本获利能力；默认返回 |
| `accounts_receivable_ratio` | number | 应收账款占比；默认返回 |
| `inventory_proportion` | number | 存货占比；默认返回 |
| `annualized_expense_to_gross_profit` | number | 年化期间费用毛利比；默认返回 |
| `operating_revenue` | number | 营业收入；默认返回 |
| `operating_cost` | number | 营业成本；默认返回 |
| `selling_expense` | number | 销售费用；默认返回 |
| `general_admin_expense` | number | 管理费用；默认返回 |
| `finance_expense` | number | 财务费用；默认返回 |
| `three_expenses_total` | number | 三费合计；默认返回 |
| `fair_value_change_income` | number | 公允价值变动净收益；默认返回 |
| `investment_income` | number | 投资收益；默认返回 |
| `operating_profit` | number | 营业利润；默认返回 |
| `subsidy_income` | number | 补贴收入；默认返回 |
| `non_operating_net_income` | number | 营业外收支净额；默认返回 |
| `total_profit` | number | 利润总额；默认返回 |
| `net_profit` | number | 净利润；默认返回 |
| `net_profit_attributable_to_parent` | number | 归属于母公司所有者的净利润；默认返回 |
| `net_profit_deducting_non_recurring_2007` | number | 扣除非经常性损益后的净利润(2007版)；默认返回 |
| `non_recurring_profit_loss_2007` | number | 非经常性损益合计(2007版)；默认返回 |
| `net_operating_cash_flow` | number | 经营活动现金流量净额；默认返回 |
| `net_investing_cash_flow` | number | 投资活动现金流量净额；默认返回 |
| `net_financing_cash_flow` | number | 筹资活动现金流量净额；默认返回 |
| `net_increase_in_cash` | number | 现金及现金等价物净增加额；默认返回 |
| `currency_funds` | number | 货币资金；默认返回 |
| `trading_financial_assets` | number | 交易性金融资产；默认返回 |
| `accounts_receivable` | number | 应收账款；默认返回 |
| `inventory` | number | 存货；默认返回 |
| `total_current_assets` | number | 流动资产合计；默认返回 |
| `investment_property` | number | 投资性房地产；默认返回 |
| `goodwill` | number | 商誉；默认返回 |
| `fixed_assets` | number | 固定资产；默认返回 |
| `total_non_current_assets` | number | 非流动资产合计；默认返回 |
| `total_assets` | number | 资产总计；默认返回 |
| `total_current_liabilities` | number | 流动负债合计；默认返回 |
| `total_non_current_liabilities` | number | 非流动负债合计；默认返回 |
| `total_liabilities` | number | 负债合计；默认返回 |
| `share_capital` | number | 股本；默认返回 |
| `capital_reserve` | number | 资本公积；默认返回 |
| `surplus_reserve` | number | 盈余公积；默认返回 |
| `treasury_stock` | number | 库存股；默认返回 |
| `retained_earnings` | number | 未分配利润；默认返回 |
| `minority_interest` | number | 少数股东权益；默认返回 |
| `total_shareholders_equity` | number | 股东权益合计；默认返回 |
| `remark` | string | 备注 |
| `equity_attributable_to_parent` | number | 归属于母公司所有者权益；默认返回 |
| `rd_expense` | number | 研发费用；默认返回 |
| `rd_expense_ratio` | number | 研发费用率；默认返回 |
| `selling_expense_ratio` | number | 销售费用率；默认返回 |
| `four_expenses_ratio` | number | 四费费用率；默认返回 |
| `four_expenses_ratio_yoy_change` | number | 四费费用率同比变化值；默认返回 |
| `three_expenses_ratio_yoy_change` | number | 三费费用率同比变化值；默认返回 |
| `finance_expense_ratio_yoy_change` | number | 财务费用率同比变化值；默认返回 |
| `admin_expense_ratio_yoy_change` | number | 管理费用率同比变化值；默认返回 |
| `selling_expense_ratio_yoy_change` | number | 销售费用率同比变化值；默认返回 |
| `rd_expense_ratio_yoy_change` | number | 研发费用率同比变化值；默认返回 |
| `gross_margin_yoy_change` | number | 毛利率同比变化值；默认返回 |
| `net_profit_excl_non_recurring_yoy_growth` | number | 扣除非经常性损益后的净利润同比变化率；默认返回 |
| `parent_net_profit_yoy_growth` | number | 归属于母公司所有者的净利润同比变化率；默认返回 |
| `operating_cash_flow_yoy_growth` | number | 经营活动产生的现金流净额同比变化率；默认返回 |

## bs — 上市公司资产负债表

`GET /api/v1/data/bs`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000002` |
| `market_code` | 否 | 交易市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date-time |  |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `report_year` | 否 | 报告年度，YYYY-03-31为一季度，YYYY-06-30为中报，YYYY-09-30为三季报，YYYY-12-31为年报；操作符：between（逗号分隔两个边界） | string/date |  |
| `consolidation_type_code` | 否 | 合并类型编码 | string | 071001=合并本期；071002=合并上期；071003=母公司本期；071004=母公司上期 |
| `report_source_code` | 否 | 报表来源编码 | string | 033001=招募说明书；033002=上市公告书；033003=定期报告；033005=临时公告；033008=预披露公告；033012=换股报告书；033014=重新上市报告书；033016=更正或补充；033021=转板上市公告书 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `announcement_date` | string/date-time | 公告日期；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `report_year` | string/date | 报告年度；默认返回 |
| `consolidation_type_code` | string | 合并类型编码；默认返回 |
| `consolidation_type` | string | 合并类型；默认返回 |
| `report_source_code` | string | 报表来源编码；默认返回 |
| `report_source` | string | 报表来源；默认返回 |
| `currency_funds` | number | 货币资金；默认返回 |
| `trading_financial_assets` | number | 交易性金融资产；默认返回 |
| `notes_receivable` | number | 应收票据 |
| `accounts_receivable` | number | 应收账款；默认返回 |
| `prepayments` | number | 预付款项；默认返回 |
| `other_receivables` | number | 其他应收款；默认返回 |
| `receivables_from_related_parties` | number | 应收关联公司款；默认返回 |
| `interest_receivable` | number | 其中：应收利息；默认返回 |
| `dividend_receivable` | number | 其中：应收股利；默认返回 |
| `inventory` | number | 存货；默认返回 |
| `biological_assets` | number | 其中：消耗性生物资产；默认返回 |
| `non_current_assets_due_within_one_year` | number | 一年内到期的非流动资产；默认返回 |
| `other_current_assets` | number | 其他流动资产；默认返回 |
| `total_current_assets` | number | 流动资产合计；默认返回 |
| `available_for_sale_financial_assets` | number | 可供出售金融资产；默认返回 |
| `held_to_maturity_investments` | number | 持有至到期投资；默认返回 |
| `long_term_receivables` | number | 长期应收款；默认返回 |
| `long_term_equity_investments` | number | 长期股权投资；默认返回 |
| `investment_property` | number | 投资性房地产；默认返回 |
| `fixed_assets` | number | 固定资产；默认返回 |
| `construction_in_progress` | number | 在建工程；默认返回 |
| `construction_materials` | number | 工程物资；默认返回 |
| `fixed_assets_disposal` | number | 固定资产清理；默认返回 |
| `productive_biological_assets` | number | 生产性生物资产；默认返回 |
| `oil_and_gas_assets` | number | 油气资产；默认返回 |
| `intangible_assets` | number | 无形资产；默认返回 |
| `development_expenditure` | number | 开发支出；默认返回 |
| `goodwill` | number | 商誉；默认返回 |
| `long_term_prepaid_expenses` | number | 长期待摊费用；默认返回 |
| `deferred_tax_assets` | number | 递延所得税资产；默认返回 |
| `other_non_current_assets` | number | 其他非流动资产；默认返回 |
| `total_non_current_assets` | number | 非流动资产合计；默认返回 |
| `total_assets` | number | 资产总计；默认返回 |
| `short_term_borrowings` | number | 短期借款；默认返回 |
| `trading_financial_liabilities` | number | 交易性金融负债；默认返回 |
| `notes_payable` | number | 应付票据 |
| `accounts_payable` | number | 应付账款；默认返回 |
| `advances_from_customers` | number | 预收款项；默认返回 |
| `employee_benefits_payable` | number | 应付职工薪酬；默认返回 |
| `taxes_payable` | number | 应交税费；默认返回 |
| `interest_payable` | number | 其中：应付利息；默认返回 |
| `dividend_payable` | number | 其中：应付股利；默认返回 |
| `other_payables` | number | 其他应付款；默认返回 |
| `payables_to_related_parties` | number | 应付关联公司款；默认返回 |
| `non_current_liabilities_due_within_one_year` | number | 一年内到期的非流动负债；默认返回 |
| `other_current_liabilities` | number | 其他流动负债；默认返回 |
| `total_current_liabilities` | number | 流动负债合计；默认返回 |
| `long_term_borrowings` | number | 长期借款；默认返回 |
| `bonds_payable` | number | 应付债券；默认返回 |
| `long_term_payables` | number | 长期应付款；默认返回 |
| `special_payables` | number | 专项应付款；默认返回 |
| `provisions` | number | 预计负债；默认返回 |
| `deferred_tax_liabilities` | number | 递延所得税负债；默认返回 |
| `other_non_current_liabilities` | number | 其他非流动负债；默认返回 |
| `total_non_current_liabilities` | number | 非流动负债合计；默认返回 |
| `total_liabilities` | number | 负债合计；默认返回 |
| `share_capital` | number | 实收资本（或股本）；默认返回 |
| `capital_reserve` | number | 资本公积；默认返回 |
| `surplus_reserve` | number | 盈余公积；默认返回 |
| `special_reserve` | number | 专项储备；默认返回 |
| `treasury_stock` | number | 减：库存股；默认返回 |
| `general_risk_reserve` | number | 一般风险准备；默认返回 |
| `retained_earnings` | number | 未分配利润；默认返回 |
| `equity_attributable_to_parent` | number | 归属于母公司所有者权益；默认返回 |
| `minority_interest` | number | 少数股东权益；默认返回 |
| `foreign_currency_translation_difference` | number | 外币报表折算价差；默认返回 |
| `non_operating_income_adjustment` | number | 非正常经营项目收益调整；默认返回 |
| `total_equity` | number | 所有者权益（或股东权益）合计；默认返回 |
| `total_liabilities_and_equity` | number | 负债和所有者（或股东权益）合计；默认返回 |
| `other_comprehensive_income` | number | 其他综合收益；默认返回 |
| `deferred_income_non_current` | number | 递延收益-非流动负债；默认返回 |
| `settlement_reserve` | number | 结算备付金；默认返回 |
| `placements_with_bank_fin_inst` | number | 拆出资金；默认返回 |
| `loans_and_advances_current` | number | 发放贷款及垫款-流动资产；默认返回 |
| `derivative_financial_assets` | number | 衍生金融资产；默认返回 |
| `premiums_receivable` | number | 应收保费；默认返回 |
| `reinsurance_receivables` | number | 应收分保账款；默认返回 |
| `reinsurance_contract_reserves` | number | 应收分保合同准备金；默认返回 |
| `financial_assets_purchased_under_agreements_to_resell` | number | 买入返售金融资产；默认返回 |
| `assets_held_for_sale` | number | 划分为持有待售的资产；默认返回 |
| `loans_and_advances_non_current` | number | 发放贷款及垫款-非流动资产；默认返回 |
| `borrowings_from_central_bank` | number | 向中央银行借款；默认返回 |
| `deposits_and_interbank_deposits` | number | 吸收存款及同业存放；默认返回 |
| `placements_from_bank_fin_inst` | number | 拆入资金；默认返回 |
| `derivative_financial_liabilities` | number | 衍生金融负债；默认返回 |
| `financial_assets_sold_under_agreement_to_repurchase` | number | 卖出回购金融资产款；默认返回 |
| `fees_commissions_payable` | number | 应付手续费及佣金；默认返回 |
| `reinsurance_payables` | number | 应付分保账款；默认返回 |
| `insurance_contract_reserves` | number | 保险合同准备金；默认返回 |
| `securities_brokering` | number | 代理买卖证券款；默认返回 |
| `securities_underwriting` | number | 代理承销证券款；默认返回 |
| `liabilities_held_for_sale` | number | 划分为持有待售的负债；默认返回 |
| `provisions_current` | number | 预计负债-流动负债；默认返回 |
| `deferred_income_current` | number | 递延收益-流动负债；默认返回 |
| `preferred_stock_non_current_liabilities` | number | 其中：优先股-非流动负债；默认返回 |
| `perpetual_bonds_non_current_liabilities` | number | 永续债-非流动负债；默认返回 |
| `long_term_employee_benefits_payable` | number | 长期应付职工薪酬；默认返回 |
| `other_equity_instruments` | number | 其他权益工具；默认返回 |
| `preferred_stock_equity` | number | 其中：优先股-所有者权益；默认返回 |
| `perpetual_bonds_equity` | number | 永续债-所有者权益；默认返回 |
| `notes_and_accounts_receivable` | number | 应收票据及应收账款 |
| `contract_assets` | number | 合同资产；默认返回 |
| `debt_investments` | number | 债权投资；默认返回 |
| `other_debt_investments` | number | 其他债权投资；默认返回 |
| `other_equity_investments` | number | 其他权益工具投资；默认返回 |
| `other_non_current_financial_assets` | number | 其他非流动金融资产；默认返回 |
| `notes_and_accounts_payable` | number | 应付票据及应付账款 |
| `contract_liabilities` | number | 合同负债；默认返回 |
| `receivables_financing` | number | 应收款项融资；默认返回 |
| `right_of_use_assets` | number | 使用权资产；默认返回 |
| `lease_liabilities` | number | 租赁负债；默认返回 |
| `remark` | string | 备注 |
| `non_current_assets_special_items` | number | 非流动资产-特殊报表项目汇总；默认返回 |
| `insurance_contract_reserves_current` | number | 保险合同准备金-流动负债；默认返回 |
| `current_liabilities_special_items` | number | 流动负债-特殊报表项目汇总；默认返回 |
| `non_current_liabilities_special_items` | number | 非流动负债-特殊报表项目汇总；默认返回 |
| `special_equity_items` | number | 所有者权益-特殊报表项目汇总；默认返回 |

## is — 上市公司利润表

`GET /api/v1/data/is`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000002` |
| `market_code` | 否 | 交易市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date-time |  |
| `start_date` | 否 | 开始日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `report_year` | 否 | 报告年度，YYYY-03-31为一季度，YYYY-06-30为中报，YYYY-09-30为三季报，YYYY-12-31为年报；操作符：between（逗号分隔两个边界） | string/date |  |
| `consolidation_type_code` | 否 | 合并类型编码 | string | 071001=合并本期；071002=合并上期；071003=母公司本期；071004=母公司上期 |
| `report_source_code` | 否 | 报表来源编码 | string | 033001=招募说明书；033002=上市公告书；033003=定期报告；033005=临时公告；033008=预披露公告；033012=换股报告书；033014=重新上市报告书；033016=更正或补充；033021=转板上市公告书 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `announcement_date` | string/date-time | 公告日期；默认返回 |
| `start_date` | string/date | 开始日期；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `report_year` | string/date | 报告年度；默认返回 |
| `consolidation_type_code` | string | 合并类型编码；默认返回 |
| `consolidation_type` | string | 合并类型；默认返回 |
| `report_source_code` | string | 报表来源编码；默认返回 |
| `report_source` | string | 报表来源；默认返回 |
| `total_operating_revenue` | number | 一、营业总收入；默认返回 |
| `operating_revenue` | number | 其中：营业收入；默认返回 |
| `total_operating_cost_old` | number | 二、营业总成本-旧规则；默认返回 |
| `operating_cost` | number | 其中：营业成本；默认返回 |
| `taxes_and_surcharges` | number | 税金及附加；默认返回 |
| `selling_expense` | number | 销售费用；默认返回 |
| `general_admin_expense` | number | 管理费用；默认返回 |
| `exploration_expense` | number | 堪探费用；默认返回 |
| `finance_expense` | number | 财务费用；默认返回 |
| `asset_impairment_loss` | number | 资产减值损失；默认返回 |
| `fair_value_change_income` | number | 加：公允价值变动净收益；默认返回 |
| `investment_income` | number | 投资收益；默认返回 |
| `investment_income_from_associates` | number | 其中：对联营企业和合营企业的投资收益；默认返回 |
| `exchange_gain` | number | 汇兑收益；默认返回 |
| `other_operating_profit_items` | number | 影响营业利润的其他科目；默认返回 |
| `operating_profit` | number | 三、营业利润；默认返回 |
| `subsidy_income` | number | 加：补贴收入；默认返回 |
| `non_operating_income` | number | 营业外收入；默认返回 |
| `non_operating_expense` | number | 减：营业外支出；默认返回 |
| `disposal_of_non_current_asset_loss` | number | 其中：非流动资产处置损失；默认返回 |
| `other_total_profit_items` | number | 加：影响利润总额的其他科目；默认返回 |
| `total_profit` | number | 四、利润总额；默认返回 |
| `income_tax` | number | 减：所得税；默认返回 |
| `other_net_profit_items` | number | 加：影响净利润的其他科目；默认返回 |
| `net_profit` | number | 五、净利润；默认返回 |
| `net_profit_attributable_to_parent` | number | 归属于母公司所有者的净利润；默认返回 |
| `minority_profit_loss` | number | 少数股东损益；默认返回 |
| `basic_eps` | number | （一）基本每股收益；默认返回 |
| `diluted_eps` | number | （二）稀释每股收益；默认返回 |
| `other_comprehensive_income` | number | 七、其他综合收益；默认返回 |
| `total_comprehensive_income` | number | 八、综合收益总额；默认返回 |
| `tci_attributable_to_parent` | number | 其中：归属于母公司；默认返回 |
| `tci_attributable_to_minority` | number | 其中：归属于少数股东；默认返回 |
| `interest_income` | number | 利息收入；默认返回 |
| `earned_premium` | number | 已赚保费；默认返回 |
| `commission_income` | number | 手续费及佣金收入；默认返回 |
| `interest_expense` | number | 利息支出；默认返回 |
| `commission_expense` | number | 手续费及佣金支出；默认返回 |
| `cash_surrender_value` | number | 退保金；默认返回 |
| `claims_expense_net` | number | 赔付支出净额；默认返回 |
| `insurance_contract_reserves_net` | number | 提取保险合同准备金净额；默认返回 |
| `policyholder_dividend_expense` | number | 保单红利支出；默认返回 |
| `reinsurance_expense` | number | 分保费用；默认返回 |
| `disposal_of_non_current_asset_gain` | number | 其中：非流动资产处置利得；默认返回 |
| `other_income` | number | 其他收益；默认返回 |
| `asset_disposal_income` | number | 资产处置收益；默认返回 |
| `net_profit_from_continuing_operations` | number | 持续经营净利润；默认返回 |
| `net_profit_from_discontinued_operations` | number | 终止经营净利润；默认返回 |
| `rd_expense` | number | 研发费用；默认返回 |
| `credit_impairment_loss` | number | 信用减值损失；默认返回 |
| `net_hedge_income` | number | 净敞口套期收益；默认返回 |
| `total_operating_cost` | number | 二、营业总成本；默认返回 |
| `included_interest_expense` | number | 其中：利息费用；默认返回 |
| `included_interest_income` | number | 其中：利息收入；默认返回 |
| `credit_impairment_loss_2019` | number | 信用减值损失（2019格式）；默认返回 |
| `asset_impairment_loss_2019` | number | 资产减值损失（2019格式）；默认返回 |
| `oci_parent_after_tax` | number | 其中：归属母公司所有者的其他综合收益的税后净额；默认返回 |
| `oci_minority_after_tax` | number | 其中：归属于少数股东的其他综合收益的税后净额；默认返回 |
| `remark` | string | 备注 |
| `other_operating_revenue_items` | number | 影响营业总收入的其他科目；默认返回 |
| `other_total_operating_cost_items` | number | 影响营业总成本的其他科目；默认返回 |

## cf — 上市公司现金流量表

`GET /api/v1/data/cf`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000002` |
| `market_code` | 否 | 交易市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date-time |  |
| `start_date` | 否 | 开始日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `report_year` | 否 | 报告年度，YYYY-03-31为一季度，YYYY-06-30为中报，YYYY-09-30为三季报，YYYY-12-31为年报；操作符：between（逗号分隔两个边界） | string/date |  |
| `consolidation_type_code` | 否 | 合并类型编码 | string | 071001=合并本期；071002=合并上期；071003=母公司本期；071004=母公司上期 |
| `report_source_code` | 否 | 报表来源编码 | string | 033001=招募说明书；033002=上市公告书；033003=定期报告；033005=临时公告；033008=预披露公告；033012=换股报告书；033014=重新上市报告书；033016=更正或补充；033021=转板上市公告书 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `announcement_date` | string/date-time | 公告日期；默认返回 |
| `start_date` | string/date | 开始日期；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `report_year` | string/date | 报告年度；默认返回 |
| `consolidation_type_code` | string | 合并类型编码；默认返回 |
| `consolidation_type` | string | 合并类型；默认返回 |
| `report_source_code` | string | 报表来源编码；默认返回 |
| `report_source` | string | 报表来源；默认返回 |
| `cash_from_sales` | number | 销售商品、提供劳务收到的现金；默认返回 |
| `tax_refunds` | number | 收到的税费返还；默认返回 |
| `other_operating_cash_inflow` | number | 收到其他与经营活动有关的现金；默认返回 |
| `total_operating_cash_inflow` | number | 经营活动现金流入小计；默认返回 |
| `cash_paid_for_goods` | number | 购买商品、接受劳务支付的现金；默认返回 |
| `cash_paid_to_employees` | number | 支付给职工以及为职工支付的现金；默认返回 |
| `taxes_paid` | number | 支付的各项税费；默认返回 |
| `other_operating_cash_outflow` | number | 支付其他与经营活动有关的现金；默认返回 |
| `total_operating_cash_outflow` | number | 经营活动现金流出小计；默认返回 |
| `net_operating_cash_flow` | number | 经营活动产生的现金流量净额；默认返回 |
| `cash_from_investment_recovery` | number | 收回投资收到的现金；默认返回 |
| `cash_from_investment_income` | number | 取得投资收益收到的现金；默认返回 |
| `cash_from_productive_assets_disposal` | number | 处置固定资产、无形资产和其他长期资产收回的现金净额；默认返回 |
| `cash_from_subsidiary_disposal` | number | 处置子公司及其他营业单位收到的现金净额；默认返回 |
| `other_investing_cash_inflow` | number | 收到其他与投资活动有关的现金；默认返回 |
| `total_investing_cash_inflow` | number | 投资活动现金流入小计；默认返回 |
| `cash_paid_for_productive_assets` | number | 购建固定资产、无形资产和其他长期资产支付的现金；默认返回 |
| `cash_paid_for_investment` | number | 投资支付的现金；默认返回 |
| `net_increase_in_pledged_loans` | number | 质押贷款净增加额；默认返回 |
| `cash_paid_for_subsidiary_acquisition` | number | 取得子公司及其他营业单位支付的现金净额；默认返回 |
| `other_investing_cash_outflow` | number | 支付其他与投资活动有关的现金；默认返回 |
| `total_investing_cash_outflow` | number | 投资活动现金流出小计；默认返回 |
| `net_investing_cash_flow` | number | 投资活动产生的现金流量净额；默认返回 |
| `cash_from_capital_contribution` | number | 吸收投资收到的现金；默认返回 |
| `cash_from_borrowing` | number | 取得借款收到的现金；默认返回 |
| `cash_from_bond_issuance` | number | 发行债券收到的现金；默认返回 |
| `other_financing_cash_inflow` | number | 收到其他与筹资活动有关的现金；默认返回 |
| `total_financing_cash_inflow` | number | 筹资活动现金流入小计；默认返回 |
| `cash_for_debt_repayment` | number | 偿还债务支付的现金；默认返回 |
| `cash_for_dividends_interest` | number | 分配股利、利润或偿付利息支付的现金；默认返回 |
| `other_financing_cash_outflow` | number | 支付其他与筹资活动有关的现金；默认返回 |
| `total_financing_cash_outflow` | number | 筹资活动现金流出小计；默认返回 |
| `net_financing_cash_flow` | number | 筹资活动产生的现金流量净额；默认返回 |
| `effect_of_exchange_rate_changes` | number | 四、汇率变动对现金的影响；默认返回 |
| `effect_of_other_factors_on_cash` | number | 四(2)、其他原因对现金的影响；默认返回 |
| `net_increase_in_cash` | number | 五、现金及现金等价物净增加额；默认返回 |
| `beginning_cash_balance` | number | 期初现金及现金等价物余额；默认返回 |
| `ending_cash_balance` | number | 期末现金及现金等价物余额；默认返回 |
| `net_profit` | number | 净利润；默认返回 |
| `provision_for_asset_impairment` | number | 加：资产减值准备；默认返回 |
| `depreciation_depletion` | number | 固定资产折旧、油气资产折耗、生产性生物资产折旧；默认返回 |
| `amortization_of_intangible_assets` | number | 无形资产摊销；默认返回 |
| `amortization_of_long_term_prepaid_expenses` | number | 长期待摊费用摊销；默认返回 |
| `loss_on_asset_disposal` | number | 处置固定资产、无形资产和其他长期资产的损失；默认返回 |
| `loss_on_asset_scrapping` | number | 固定资产报废损失；默认返回 |
| `loss_on_fair_value_change` | number | 公允价值变动损失；默认返回 |
| `finance_expense` | number | 财务费用；默认返回 |
| `investment_loss` | number | 投资损失；默认返回 |
| `decrease_in_deferred_tax_assets` | number | 递延所得税资产减少；默认返回 |
| `increase_in_deferred_tax_liabilities` | number | 递延所得税负债增加；默认返回 |
| `decrease_in_inventory` | number | 存货的减少；默认返回 |
| `decrease_in_operating_receivables` | number | 经营性应收项目的减少；默认返回 |
| `increase_in_operating_payables` | number | 经营性应付项目的增加；默认返回 |
| `others` | number | 其他；默认返回 |
| `net_operating_cash_flow_2` | number | 经营活动产生的现金流量净额2；默认返回 |
| `conversion_of_debt_to_capital` | number | 债务转为资本；默认返回 |
| `convertible_bonds_due_within_one_year` | number | 一年内到期的可转换公司债券；默认返回 |
| `finance_lease_assets` | number | 融资租入固定资产；默认返回 |
| `ending_cash_balance_excl_equivalents` | number | 现金的期末余额；默认返回 |
| `beginning_cash_balance_excl_equivalents` | number | 减：现金的期初余额；默认返回 |
| `ending_cash_equivalents` | number | 加：现金等价物的期末余额；默认返回 |
| `beginning_cash_equivalents` | number | 减：现金等价物的期初余额；默认返回 |
| `effect_of_other_factors_on_cash_2` | number | 加：其他原因对现金的影响2；默认返回 |
| `net_increase_in_cash_2` | number | 现金及现金等价物净增加额2；默认返回 |
| `net_increase_in_deposits` | number | 客户存款和同业存放款项净增加额；默认返回 |
| `net_increase_in_borrowings_from_central_bank` | number | 向中央银行借款净增加额；默认返回 |
| `net_increase_in_interbank_borrowings` | number | 向其他金融机构拆入资金净增加额；默认返回 |
| `cash_from_premiums` | number | 收到原保险合同保费取得的现金；默认返回 |
| `net_cash_from_reinsurance` | number | 收到再保险业务现金净额；默认返回 |
| `net_increase_in_policyholder_deposits` | number | 保户储金及投资款净增加额；默认返回 |
| `net_increase_from_disposal_of_trading_financial_assets` | number | 处置以公允价值计量且其变动计入当期损益的金融资产净增加额；默认返回 |
| `cash_from_interest_commissions` | number | 收取利息、手续费及佣金的现金；默认返回 |
| `net_incr_placements_from_bank_fin_inst` | number | 拆入资金净增加额；默认返回 |
| `net_increase_in_repurchases` | number | 回购业务资金净增加额；默认返回 |
| `net_increase_in_loans` | number | 客户贷款及垫款净增加额；默认返回 |
| `net_increase_in_deposits_with_banks` | number | 存放中央银行和同业款项净增加额；默认返回 |
| `cash_for_claims` | number | 支付原保险合同赔付款项的现金；默认返回 |
| `cash_for_interest_commissions` | number | 支付利息、手续费及佣金的现金；默认返回 |
| `cash_for_policyholder_dividends` | number | 支付保单红利的现金；默认返回 |
| `cash_from_minority_shareholders_investment` | number | 其中：子公司吸收少数股东投资收到的现金；默认返回 |
| `cash_paid_to_minority_shareholders` | number | 其中：子公司支付给少数股东的股利、利润；默认返回 |
| `depreciation_of_investment_property` | number | 投资性房地产的折旧及摊销；默认返回 |
| `credit_impairment_loss` | number | 信用减值损失；默认返回 |
| `depreciation_of_right_of_use_assets` | number | 使用权资产折旧；默认返回 |
| `remark` | string | 备注 |
| `other_items_affecting_operating_inflow` | number | 影响经营活动现金流入的其他科目；默认返回 |
| `net_increase_in_funds_lent` | number | 拆出资金净增加额；默认返回 |
| `other_items_affecting_operating_outflow` | number | 影响经营活动现金流出的其他科目；默认返回 |
| `other_items_affecting_investing_inflow` | number | 影响投资活动现金流入的其他科目；默认返回 |
| `other_items_affecting_investing_outflow` | number | 影响投资活动现金流出的其他科目；默认返回 |
| `other_items_affecting_financing_inflow` | number | 影响筹资活动现金流入的其他科目；默认返回 |
| `other_items_affecting_financing_outflow` | number | 影响筹资活动现金流出的其他科目；默认返回 |
| `other_items_affecting_net_operating_cash_flow_supplementary` | number | 影响经营活动现金流量净额的其他科目-补充资料；默认返回 |

## bs_fin — 金融类上市公司资产负债表

`GET /api/v1/data/bs_fin`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 股票代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `market_code` | 否 | 市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `report_year` | 否 | 报告年度，YYYY-03-31为一季度，YYYY-06-30为中报，YYYY-09-30为三季报，YYYY-12-31为年报；操作符：between（逗号分隔两个边界） | string/date |  |
| `consolidation_type_code` | 否 | 合并类型编码 | string | 071001=合并本期；071002=合并上期；071003=母公司本期；071004=母公司上期 |
| `report_source_code` | 否 | 报表来源编码 | string | 033001=招募说明书；033002=上市公告书；033003=定期报告；033008=预披露公告；033012=换股报告书；033016=更正或补充 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 股票代码；默认返回 |
| `sec_name` | string | 股票简称；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `report_year` | string/date | 报告年度；默认返回 |
| `consolidation_type_code` | string | 合并类型编码；默认返回 |
| `consolidation_type` | string | 合并类型；默认返回 |
| `report_source_code` | string | 报表来源编码；默认返回 |
| `report_source` | string | 报表来源；默认返回 |
| `interbank_deposits` | number | 存放同业款项；默认返回 |
| `currency_funds` | number | 货币资金；默认返回 |
| `client_funds_deposits` | number | 其中：客户资金存款；默认返回 |
| `cash_and_central_bank_deposits` | number | 现金及存放中央银行款项；默认返回 |
| `settlement_reserve` | number | 结算备付金；默认返回 |
| `client_reserve` | number | 其中：客户备付金；默认返回 |
| `precious_metals` | number | 贵金属；默认返回 |
| `placements_with_bank_fin_inst` | number | 拆出资金；默认返回 |
| `trading_financial_assets` | number | 交易性金融资产；默认返回 |
| `derivative_financial_assets` | number | 衍生金融资产；默认返回 |
| `financial_assets_purchased_under_agreements_to_resell` | number | 买入返售金融资产；默认返回 |
| `interest_receivable` | number | 应收利息；默认返回 |
| `premiums_receivable` | number | 应收保费；默认返回 |
| `subrogation_receivables` | number | 应收代位追偿款；默认返回 |
| `reinsurance_receivables` | number | 应收分保帐款；默认返回 |
| `reinsurance_unearned_premium_reserves` | number | 应收分保未到期责任准备金；默认返回 |
| `reinsurance_outstanding_claims_reserves` | number | 应收分保未决赔款准备金；默认返回 |
| `reinsurance_life_reserves` | number | 应收分保寿险责任准备金；默认返回 |
| `reinsurance_long_term_health_reserves` | number | 应收分保长期健康险责任准备金；默认返回 |
| `policyholder_loans` | number | 保户质押贷款；默认返回 |
| `time_deposits` | number | 定期存款；默认返回 |
| `loans_and_advances` | number | 发放贷款及垫款；默认返回 |
| `margins_paid` | number | 存出保证金；默认返回 |
| `agency_assets` | number | 代理业务资产；默认返回 |
| `receivables_investments` | number | 应收款项类投资；默认返回 |
| `prepayments` | number | 预付款项；默认返回 |
| `available_for_sale_financial_assets` | number | 可供出售金融资产；默认返回 |
| `held_to_maturity_investments` | number | 持有至到期投资；默认返回 |
| `long_term_equity_investments` | number | 长期股权投资；默认返回 |
| `margin_financing` | number | 融出资金；默认返回 |
| `capital_guarantee_deposits` | number | 存出资本保证金；默认返回 |
| `investment_property` | number | 投资性房地产；默认返回 |
| `inventory` | number | 存货；默认返回 |
| `fixed_assets` | number | 固定资产；默认返回 |
| `construction_in_progress` | number | 在建工程；默认返回 |
| `intangible_assets` | number | 无形资产；默认返回 |
| `trading_seat_fees` | number | 其中：交易席位费；默认返回 |
| `long_term_prepaid_expenses` | number | 长期待摊费用；默认返回 |
| `fixed_assets_disposal` | number | 固定资产清理；默认返回 |
| `separate_account_assets` | number | 独立帐户资产；默认返回 |
| `deferred_tax_assets` | number | 递延所得税资产；默认返回 |
| `other_assets` | number | 其他资产；默认返回 |
| `total_assets` | number | 资产总计；默认返回 |
| `borrowings_from_central_bank` | number | 向中央银行借款；默认返回 |
| `deposits_from_banks` | number | 同业及其他金融机构存放款项；默认返回 |
| `short_term_borrowings` | number | 短期借款；默认返回 |
| `pledged_borrowings` | number | 其中：质押借款；默认返回 |
| `placements_from_bank_fin_inst` | number | 拆入资金；默认返回 |
| `trading_financial_liabilities` | number | 交易性金融负债；默认返回 |
| `derivative_financial_liabilities` | number | 衍生金融负债；默认返回 |
| `financial_assets_sold_under_agreement_to_repurchase` | number | 卖出回购金融资产款；默认返回 |
| `customer_deposits` | number | 吸收存款；默认返回 |
| `securities_brokering` | number | 代理买卖证券款；默认返回 |
| `securities_underwriting` | number | 代理承销证券款；默认返回 |
| `accounts_payable` | number | 应付帐款；默认返回 |
| `notes_payable` | number | 应付票据 |
| `advances_from_customers` | number | 预收款项；默认返回 |
| `premiums_received_in_advance` | number | 预收保费；默认返回 |
| `fees_commissions_payable` | number | 应付手续费及佣金；默认返回 |
| `payables_to_reinsurers` | number | 应付分保帐款；默认返回 |
| `employee_benefits_payable` | number | 应付职工薪酬；默认返回 |
| `taxes_payable` | number | 应交税费；默认返回 |
| `interest_payable` | number | 应付利息；默认返回 |
| `agency_liabilities` | number | 代理业务负债；默认返回 |
| `provisions` | number | 预计负债；默认返回 |
| `claims_payable` | number | 应付赔付款；默认返回 |
| `policyholder_dividends_payable` | number | 应付保单红利；默认返回 |
| `policyholder_deposits` | number | 保户储金及投资款；默认返回 |
| `unearned_premium_reserves` | number | 未到期责任准备金；默认返回 |
| `outstanding_claims_reserves` | number | 未决赔款准备金；默认返回 |
| `life_insurance_reserves` | number | 寿险责任准备金；默认返回 |
| `long_term_health_reserves` | number | 长期健康险责任准备金；默认返回 |
| `long_term_borrowings` | number | 长期借款；默认返回 |
| `bonds_payable` | number | 应付债券；默认返回 |
| `independent_account_liabilities` | number | 独立帐户负债；默认返回 |
| `deferred_tax_liabilities` | number | 递延所得税负债；默认返回 |
| `other_liabilities` | number | 其他负债；默认返回 |
| `total_liabilities` | number | 负债合计；默认返回 |
| `share_capital` | number | 实收资本（或股本）；默认返回 |
| `capital_reserve` | number | 资本公积；默认返回 |
| `treasury_stock` | number | 减：库存股；默认返回 |
| `surplus_reserve` | number | 盈余公积；默认返回 |
| `general_risk_reserve` | number | 一般风险准备；默认返回 |
| `equity_attributable_to_parent` | number | 归属于母公司所有者权益；默认返回 |
| `retained_earnings` | number | 未分配利润；默认返回 |
| `minority_interest` | number | 少数股东权益；默认返回 |
| `currency_translation_difference` | number | 外币报表折算差额；默认返回 |
| `total_equity` | number | 所有者权益（或股东权益）合计；默认返回 |
| `total_liabilities_and_equity` | number | 负债和所有者权益（或股东权益）总计；默认返回 |
| `preferred_stock_liability` | number | 其中：优先股-负债；默认返回 |
| `receivables` | number | 应收款项；默认返回 |
| `other_equity_instruments` | number | 其他权益工具；默认返回 |
| `preferred_stock_equity` | number | 其中：优先股-权益；默认返回 |
| `perpetual_bonds_equity` | number | 永续债-权益；默认返回 |
| `other_comprehensive_income` | number | 其他综合收益；默认返回 |
| `goodwill` | number | 商誉；默认返回 |
| `short_term_financing_bonds` | number | 应付短期融资款；默认返回 |
| `payables` | number | 应付款项；默认返回 |
| `contract_assets` | number | 合同资产；默认返回 |
| `assets_held_for_sale` | number | 持有待售资产；默认返回 |
| `debt_investments` | number | 债权投资；默认返回 |
| `other_debt_investments` | number | 其他债权投资；默认返回 |
| `other_equity_investments` | number | 其他权益工具投资；默认返回 |
| `contract_liabilities` | number | 合同负债；默认返回 |
| `liabilities_held_for_sale` | number | 持有待售负债；默认返回 |
| `right_of_use_assets` | number | 使用权资产；默认返回 |
| `lease_liabilities` | number | 租赁负债；默认返回 |
| `remark` | string | 备注 |
| `perpetual_bonds_liability` | number | 其中：永续债-负债；默认返回 |
| `insurance_contract_liabilities` | number | 保险合同负债；默认返回 |
| `reinsurance_contract_liabilities` | number | 分出再保险合同负债；默认返回 |
| `special_liabilities_items` | number | 负债-特殊报表项目汇总；默认返回 |
| `special_equity_items` | number | 所有者权益-特殊报表项目汇总；默认返回 |

## is_fin — 金融类上市公司利润表

`GET /api/v1/data/is_fin`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 股票代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `market_code` | 否 | 市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `start_date` | 否 | 开始日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `report_year` | 否 | 报告年度；操作符：between（逗号分隔两个边界） | string/date |  |
| `consolidation_type_code` | 否 | 合并类型编码 | string | 071001=合并本期；071002=合并上期；071003=母公司本期；071004=母公司上期 |
| `report_source_code` | 否 | 报表来源编码 | string | 033001=招募说明书；033002=上市公告书；033003=定期报告；033008=预披露公告；033012=换股报告书；033016=更正或补充 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 股票代码；默认返回 |
| `sec_name` | string | 股票简称；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `start_date` | string/date | 开始日期；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `report_year` | string/date | 报告年度；默认返回 |
| `consolidation_type_code` | string | 合并类型编码；默认返回 |
| `consolidation_type` | string | 合并类型；默认返回 |
| `report_source_code` | string | 报表来源编码；默认返回 |
| `report_source` | string | 报表来源；默认返回 |
| `total_operating_revenue` | number | 一、营业收入；默认返回 |
| `net_interest_income` | number | 利息净收入；默认返回 |
| `included_interest_income` | number | 其中:利息收入；默认返回 |
| `included_interest_expense` | number | 其中:利息支出；默认返回 |
| `net_fees_commission_income` | number | 手续费及佣金净收入；默认返回 |
| `included_fees_commission_income` | number | 其中:手续费及佣金收入；默认返回 |
| `included_fees_commission_expense` | number | 其中:手续费及佣金支出；默认返回 |
| `net_income_from_brokerage` | number | 其中：代理买卖证券业务净收入；默认返回 |
| `net_income_from_underwriting` | number | 其中:证券承销业务净收入；默认返回 |
| `net_income_from_asset_management` | number | 其中:委托客户管理资产业务净收入；默认返回 |
| `earned_premium` | number | 已赚保费；默认返回 |
| `insurance_business_income` | number | 保险业务收入；默认返回 |
| `reinsurance_income` | number | 其中：分保费收入；默认返回 |
| `ceded_premium` | number | 减：分出保费；默认返回 |
| `provision_for_unexpired_risk` | number | 提取未到期责任准备金；默认返回 |
| `investment_income` | number | 投资收益；默认返回 |
| `investment_income_from_associates` | number | 其中：对联营企业和合营企业的投资收益；默认返回 |
| `fair_value_change_income` | number | 公允价值变动收益；默认返回 |
| `exchange_gain` | number | 汇兑收益；默认返回 |
| `other_business_income` | number | 其他业务收入；默认返回 |
| `total_operating_expenses` | number | 二、营业支出；默认返回 |
| `cash_surrender_value` | number | 退保金；默认返回 |
| `claims_expense` | number | 赔付支出；默认返回 |
| `recovery_of_claims` | number | 减：摊回赔付支出；默认返回 |
| `provision_for_insurance_reserves` | number | 提取保险责任准备金；默认返回 |
| `recovery_of_insurance_reserves` | number | 减：摊回保险责任准备金；默认返回 |
| `policyholder_dividend_expense` | number | 保单红利支出；默认返回 |
| `reinsurance_expense` | number | 分保费用；默认返回 |
| `taxes_and_surcharges` | number | 税金及附加；默认返回 |
| `commission_expense_2` | number | 手续费及佣金支出2；默认返回 |
| `business_and_admin_expenses` | number | 业务及管理费；默认返回 |
| `recovery_of_reinsurance_expense` | number | 减：摊回分保费用；默认返回 |
| `asset_impairment_loss` | number | 资产减值损失；默认返回 |
| `other_business_cost` | number | 其他业务成本；默认返回 |
| `operating_profit` | number | 三、营业利润；默认返回 |
| `subsidy_income` | number | 加：补贴收入；默认返回 |
| `non_operating_income` | number | 营业外收入；默认返回 |
| `non_operating_expense` | number | 减：营业外支出；默认返回 |
| `other_total_profit_items` | number | 加：影响利润总额的其他科目；默认返回 |
| `total_profit` | number | 四、利润总额；默认返回 |
| `income_tax` | number | 减：所得税；默认返回 |
| `other_net_profit_items` | number | 加：影响净利润的其他科目；默认返回 |
| `net_profit` | number | 五、净利润；默认返回 |
| `net_profit_attributable_to_parent` | number | （一）归属于母公司所有者的净利润；默认返回 |
| `minority_profit_loss` | number | （二）少数股东损益；默认返回 |
| `basic_eps` | number | （一）基本每股收益；默认返回 |
| `diluted_eps` | number | （二）稀释每股收益；默认返回 |
| `other_comprehensive_income` | number | 七、其他综合收益；默认返回 |
| `total_comprehensive_income` | number | 八、综合收益总额；默认返回 |
| `tci_attributable_to_parent` | number | 其中：归属于母公司；默认返回 |
| `tci_attributable_to_minority` | number | 其中：归属于少数股东；默认返回 |
| `other_income` | number | 其他收益；默认返回 |
| `asset_disposal_income` | number | 资产处置收益；默认返回 |
| `net_profit_from_continuing_operations` | number | 持续经营净利润；默认返回 |
| `net_profit_from_discontinued_operations` | number | 终止经营净利润；默认返回 |
| `credit_impairment_loss` | number | 信用减值损失；默认返回 |
| `net_hedge_income` | number | 净敞口套期收益；默认返回 |
| `oci_parent_after_tax` | number | 其中：归属母公司所有者的其他综合收益的税后净额；默认返回 |
| `oci_minority_after_tax` | number | 其中：归属于少数股东的其他综合收益的税后净额；默认返回 |
| `remark` | string | 备注 |
| `insurance_service_income` | number | 保险服务收入；默认返回 |
| `interest_income` | number | 利息收入；默认返回 |
| `commission_income` | number | 手续费及佣金收入；默认返回 |
| `derecognition_gain_amortized_cost` | number | 其中：以摊余成本计量的金融资产终止确认产生的收益；默认返回 |
| `other_operating_revenue_items` | number | 影响营业总收入的其他科目；默认返回 |
| `insurance_service_expenses` | number | 保险服务费用；默认返回 |
| `allocation_of_ceded_premium` | number | 分出保费的分摊；默认返回 |
| `recovery_of_insurance_service_expenses` | number | 减：摊回保险服务费用；默认返回 |
| `underwriting_financial_loss` | number | 承保财务损失；默认返回 |
| `reinsurance_financial_income` | number | 减：分出再保险财务收益；默认返回 |
| `interest_expense` | number | 利息支出；默认返回 |
| `other_operating_expense_items` | number | 影响营业总支出的其他科目；默认返回 |

## cf_fin — 金融类上市公司现金流量表

`GET /api/v1/data/cf_fin`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 股票代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `market_code` | 否 | 市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `start_date` | 否 | 开始日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `report_year` | 否 | 报告年度，YYYY-03-31为一季度，YYYY-06-30为中报，YYYY-09-30为三季报，YYYY-12-31为年报；操作符：between（逗号分隔两个边界） | string/date |  |
| `consolidation_type_code` | 否 | 合并类型编码 | string | 071001=合并本期；071002=合并上期；071003=母公司本期；071004=母公司上期 |
| `report_source_code` | 否 | 报表来源编码 | string | 033001=招募说明书；033002=上市公告书；033003=定期报告；033008=预披露公告；033012=换股报告书；033016=更正或补充 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 股票代码；默认返回 |
| `sec_name` | string | 股票简称；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `start_date` | string/date | 开始日期；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `report_year` | string/date | 报告年度；默认返回 |
| `consolidation_type_code` | string | 合并类型编码；默认返回 |
| `consolidation_type` | string | 合并类型；默认返回 |
| `report_source_code` | string | 报表来源编码；默认返回 |
| `report_source` | string | 报表来源；默认返回 |
| `net_decrease_in_loans` | number | 客户贷款及垫款净减少额；默认返回 |
| `net_increase_in_deposits` | number | 客户存款和同业存放款项净增加额；默认返回 |
| `net_increase_in_borrowings_from_central_bank` | number | 向中央银行借款净增加额；默认返回 |
| `net_decrease_in_deposits_with_banks` | number | 存放中央银行和同业款项净减少额；默认返回 |
| `net_increase_in_interbank_borrowings` | number | 向其他金融机构拆入资金净增加额；默认返回 |
| `cash_from_interest_commissions` | number | 收取利息、手续费及佣金的现金；默认返回 |
| `net_increase_from_disposal_trading_assets` | number | 处置交易性金融资产净增加额；默认返回 |
| `net_incr_placements_from_bank_fin_inst` | number | 拆入资金净增加额；默认返回 |
| `net_increase_in_repurchases` | number | 回购业务资金净增加额；默认返回 |
| `cash_from_sales` | number | 销售商品、提供劳务收到的现金；默认返回 |
| `tax_refunds` | number | 收到的税费返还；默认返回 |
| `cash_from_premiums` | number | 收到原保险合同保费取得的现金；默认返回 |
| `net_cash_from_reinsurance` | number | 收到再保业务现金净额；默认返回 |
| `net_increase_in_policyholder_deposits` | number | 保户储金及投资款净增加额；默认返回 |
| `other_operating_cash_inflow` | number | 收到其他与经营活动有关的现金；默认返回 |
| `total_operating_cash_inflow` | number | 经营活动现金流入小计；默认返回 |
| `net_increase_in_loans` | number | 客户贷款及垫款净增加额；默认返回 |
| `net_decrease_in_customer_deposits` | number | 客户存放及同业存放款项净减少额；默认返回 |
| `net_increase_in_deposits_with_banks` | number | 存放中央银行和同业款项净增加额；默认返回 |
| `net_decrease_in_central_bank_borrowings` | number | 向中央银行借款净减少额；默认返回 |
| `net_increase_in_interbank_funds_lent` | number | 向其他金融机构拆出资金净增加额；默认返回 |
| `net_increase_in_trading_assets` | number | 购入交易性金融资产净增加额；默认返回 |
| `net_decrease_in_repo_funds` | number | 回购业务资金净减少额；默认返回 |
| `cash_paid_for_interest_commissions` | number | 支付利息、手续费及佣金的现金；默认返回 |
| `cash_paid_for_goods` | number | 购买商品、提供劳务支付的现金；默认返回 |
| `net_cash_paid_for_reinsurance` | number | 支付再保业务现金净额；默认返回 |
| `net_decrease_in_policyholder_deposits` | number | 保户储金及投资款净减少额；默认返回 |
| `cash_for_claims` | number | 支付原保险合同赔付款项的现金；默认返回 |
| `cash_for_policyholder_dividends` | number | 支付保单红利的现金；默认返回 |
| `cash_paid_to_employees` | number | 支付给职工以及为职工支付的现金；默认返回 |
| `taxes_paid` | number | 支付的各项税费；默认返回 |
| `other_operating_cash_outflow` | number | 支付其他与经营活动有关的现金；默认返回 |
| `total_operating_cash_outflow` | number | 经营活动现金流出小计；默认返回 |
| `net_operating_cash_flow` | number | 经营活动产生的现金流量净额；默认返回 |
| `cash_from_investment_recovery` | number | 收回投资收到的现金；默认返回 |
| `cash_from_investment_income` | number | 取得投资收益收到的现金；默认返回 |
| `other_investing_cash_inflow` | number | 收到其他与投资活动有关的现金；默认返回 |
| `cash_from_productive_assets_disposal` | number | 处置固定资产、无形资产和其他长期资产所收回的现金；默认返回 |
| `total_investing_cash_inflow` | number | 投资活动现金流入小计；默认返回 |
| `cash_paid_for_investment` | number | 投资支付的现金；默认返回 |
| `net_increase_in_pledged_loans` | number | 质押贷款净增加额；默认返回 |
| `cash_paid_for_productive_assets` | number | 购建固定资产、无形资产和其他长期资产支付的现金；默认返回 |
| `other_investing_cash_outflow` | number | 支付其他与投资活动有关的现金；默认返回 |
| `total_investing_cash_outflow` | number | 投资活动现金流出小计；默认返回 |
| `net_investing_cash_flow` | number | 投资活动产生的现金流量净额；默认返回 |
| `cash_from_capital_contribution` | number | 吸收投资收到的现金；默认返回 |
| `cash_from_bond_issuance` | number | 发行债券收到的现金；默认返回 |
| `cash_from_borrowing` | number | 取得借款收到的现金；默认返回 |
| `other_financing_cash_inflow` | number | 收到其他与筹资活动有关的现金；默认返回 |
| `total_financing_cash_inflow` | number | 筹资活动现金流入小计；默认返回 |
| `cash_for_debt_repayment` | number | 偿还债务支付的现金；默认返回 |
| `cash_for_dividends_interest` | number | 分配股利、利润或偿付利息支付的现金；默认返回 |
| `other_financing_cash_outflow` | number | 支付其他与筹资活动有关的现金；默认返回 |
| `total_financing_cash_outflow` | number | 筹资活动现金流出小计；默认返回 |
| `net_financing_cash_flow` | number | 筹资活动产生的现金流量净额；默认返回 |
| `effect_of_exchange_rate_changes` | number | 四、汇率变动对现金的影响；默认返回 |
| `effect_of_other_factors_on_cash` | number | 四(2)、其他原因对现金的影响；默认返回 |
| `net_increase_in_cash` | number | 五、现金及现金等价物净增加额；默认返回 |
| `beginning_cash_balance` | number | 期初现金及现金等价物余额；默认返回 |
| `ending_cash_balance` | number | 期末现金及现金等价物余额；默认返回 |
| `net_profit` | number | 净利润；默认返回 |
| `provision_for_asset_impairment` | number | 加：资产减值准备；默认返回 |
| `depreciation_depletion` | number | 固定资产折旧、油气资产折耗、生产性生物资产折旧；默认返回 |
| `amortization_of_intangible_assets` | number | 无形资产摊销；默认返回 |
| `amortization_of_long_term_prepaid_expenses` | number | 长期待摊费用摊销；默认返回 |
| `loss_on_asset_disposal` | number | 处置固定资产、无形资产和其他长期资产的损失；默认返回 |
| `loss_on_asset_scrapping` | number | 固定资产报废损失；默认返回 |
| `loss_on_fair_value_change` | number | 公允价值变动损失；默认返回 |
| `finance_expense` | number | 财务费用；默认返回 |
| `investment_loss` | number | 投资损失；默认返回 |
| `decrease_in_deferred_tax_assets` | number | 递延所得税资产减少；默认返回 |
| `increase_in_deferred_tax_liabilities` | number | 递延所得税负债增加；默认返回 |
| `decrease_in_inventory` | number | 存货的减少；默认返回 |
| `decrease_in_operating_receivables` | number | 经营性应收项目的减少；默认返回 |
| `increase_in_operating_payables` | number | 经营性应付项目的增加；默认返回 |
| `others` | number | 其他；默认返回 |
| `net_operating_cash_flow_2` | number | 经营活动产生的现金流量净额2；默认返回 |
| `conversion_of_debt_to_capital` | number | 债务转为资本；默认返回 |
| `convertible_bonds_due_within_one_year` | number | 一年内到期的可转换公司债券；默认返回 |
| `finance_lease_assets` | number | 融资租入固定资产；默认返回 |
| `ending_cash_balance_excl_equivalents` | number | 现金的期末余额；默认返回 |
| `beginning_cash_balance_excl_equivalents` | number | 减：现金的期初余额；默认返回 |
| `ending_cash_equivalents` | number | 加：现金等价物的期末余额；默认返回 |
| `beginning_cash_equivalents` | number | 减：现金等价物的期初余额；默认返回 |
| `effect_of_other_factors_on_cash_2` | number | 加：其他原因对现金的影响2；默认返回 |
| `depreciation_of_investment_property` | number | 投资性房地产的折旧及摊销；默认返回 |
| `net_decrease_in_margin_financing` | number | 融出资金净减少额；默认返回 |
| `net_cash_from_securities_brokerage` | number | 代理买卖证券收到的现金净额；默认返回 |
| `net_increase_in_margin_financing` | number | 融出资金净增加额；默认返回 |
| `net_cash_for_securities_brokerage` | number | 代理买卖证券支付的现金净额；默认返回 |
| `net_decrease_in_interbank_borrowings` | number | 拆入资金净减少额；默认返回 |
| `credit_impairment_loss` | number | 信用减值损失；默认返回 |
| `remark` | string | 备注 |
| `cash_from_issued_contract_premiums` | number | 收到签发保险合同保费取得的现金；默认返回 |
| `net_cash_from_reinsurance_contracts` | number | 收到分入再保险合同的现金净额；默认返回 |
| `net_increase_in_liabilities_for_trading` | number | 为交易目的而持有的金融负债净增加额；默认返回 |
| `cash_paid_for_contract_claims` | number | 支付签发保险合同赔款的现金；默认返回 |
| `net_cash_paid_for_reinsurance_contracts` | number | 支付分出再保险合同的现金净额；默认返回 |
| `net_increase_in_policy_loans` | number | 保单质押贷款净增加额；默认返回 |
| `net_increase_in_buy_back_operating_outflow` | number | 返售业务资金净增加额-经营流出；默认返回 |
| `net_increase_in_buy_back_investing_outflow` | number | 返售业务资金净增加额-投资流出；默认返回 |
| `net_increase_in_repo_financing_inflow` | number | 回购业务资金净增加额-筹资流入；默认返回 |

## rev_by_product — 分产品主营业务收入

`GET /api/v1/data/rev_by_product`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `market_code` | 否 | 交易市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `start_date` | 否 | 开始日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `end_date` | 否 | 截止日期，YYYY-03-31为一季度，YYYY-06-30为中报，YYYY-09-30为三季报，YYYY-12-31为年报；操作符：between（逗号分隔两个边界） | string/date |  |
| `report_source_code` | 否 | 报表来源编码 | string | 033003=定期报告 |
| `consolidation_type_code` | 否 | 合并类型编码 | string | 071001=合并本期 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `start_date` | string/date | 开始日期；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `seq_no` | number | 序号；默认返回 |
| `business_category` | string | 业务类别；默认返回 |
| `business_content` | string | 业务内容 |
| `industry_segment_code` | string | 产业细分编码；默认返回 |
| `business_revenue` | number | 业务收入；默认返回 |
| `business_cost` | number | 业务成本；默认返回 |
| `business_gross_profit` | number | 业务毛利；默认返回 |
| `gross_profit_margin` | number | 毛利率；默认返回 |
| `report_source` | string | 报表来源；默认返回 |
| `report_source_code` | string | 报表来源编码；默认返回 |
| `standard_business_content` | string | 标准业务内容 |
| `remark` | string | 备注 |
| `consolidation_type_code` | string | 合并类型编码；默认返回 |
| `consolidation_type` | string | 合并类型；默认返回 |

## rev_by_industry — 分行业主营业务收入

`GET /api/v1/data/rev_by_industry`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `market_code` | 否 | 交易市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `start_date` | 否 | 开始日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `end_date` | 否 | 截止日期，YYYY-03-31为一季度，YYYY-06-30为中报，YYYY-09-30为三季报，YYYY-12-31为年报；操作符：between（逗号分隔两个边界） | string/date |  |
| `report_source_code` | 否 | 报表来源编码 | string | 033003=定期报告；033008=预披露公告 |
| `consolidation_type_code` | 否 | 合并类型编码 | string | 071001=合并本期 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `start_date` | string/date | 开始日期；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `seq_no` | number | 序号；默认返回 |
| `business_content` | string | 业务内容 |
| `industry_sector_code` | string | 行业门类编码；默认返回 |
| `industry_sector_name` | string | 行业门类名称；默认返回 |
| `industry_group_code` | string | 行业大类编码；默认返回 |
| `industry_group_name` | string | 行业大类名称；默认返回 |
| `main_business_revenue` | number | 主营业务收入；默认返回 |
| `main_business_cost` | number | 主营业务成本；默认返回 |
| `main_business_gross_profit` | number | 主营业务毛利；默认返回 |
| `gross_profit_margin` | number | 毛利率；默认返回 |
| `remark` | string | 备注 |
| `main_revenue_ratio` | number | 占主营业务收入比重；默认返回 |
| `production_sales_ratio` | number | 主营业务产销率；默认返回 |
| `business_content_en` | string | 业务内容（英文） |
| `report_source` | string | 报表来源；默认返回 |
| `report_source_code` | string | 报表来源编码；默认返回 |
| `consolidation_type_code` | string | 合并类型编码；默认返回 |
| `consolidation_type` | string | 合并类型；默认返回 |

## rev_by_region — 分地区主营业务收入

`GET /api/v1/data/rev_by_region`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `market_code` | 否 | 交易市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `start_date` | 否 | 开始日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `report_year` | 否 | 报告年度；操作符：between（逗号分隔两个边界） | string/date |  |
| `report_source_code` | 否 | 报表来源编码 | string | 033003=定期报告 |
| `consolidation_type_code` | 否 | 合并类型编码 | string | 071001=合并本期 |
| `end_date` | 否 | 截止日期，YYYY-03-31为一季度，YYYY-06-30为中报，YYYY-09-30为三季报，YYYY-12-31为年报；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `start_date` | string/date | 开始日期；默认返回 |
| `report_year` | string/date | 报告年度；默认返回 |
| `report_source` | string | 报表来源；默认返回 |
| `report_source_code` | string | 报表来源编码；默认返回 |
| `region_name` | string | 地区名称；默认返回 |
| `operating_revenue` | number | 营业收入；默认返回 |
| `operating_cost` | number | 营业成本；默认返回 |
| `gross_profit_margin` | number | 毛利率；默认返回 |
| `standard_region_name` | string | 地区标准名称；默认返回 |
| `remark` | string | 备注 |
| `consolidation_type_code` | string | 合并类型编码；默认返回 |
| `consolidation_type` | string | 合并类型；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |

## audit_opinion — 定期报告审计意见

`GET /api/v1/data/audit_opinion`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `market_code` | 否 | 市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `report_year` | 否 | 报告年度，YYYY-03-31为一季度，YYYY-06-30为中报，YYYY-09-30为三季报，YYYY-12-31为年报；操作符：between（逗号分隔两个边界） | string/date |  |
| `domestic_audit_opinion_code` | 否 | 境内会计师事务所审计意见类型编码 | string | 042001=无保留意见；042002=保留意见；042003=保留意见与解释性说明；042004=否定意见；042005=拒绝表示意见；042006=解释性说明；042007=无法表示意见；042008=带强调事项段的无保留意见 |
| `overseas_audit_opinion_code` | 否 | 境外审计报告会计师事务所审计意见类型编码 | string | 042001=无保留意见；042002=保留意见；042003=保留意见与解释性说明；042005=拒绝表示意见；042006=解释性说明；042007=无法表示意见 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_name` | string | 证券简称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `report_year` | string/date | 报告年度；默认返回 |
| `is_audited` | string | 是否经审计；默认返回 |
| `domestic_auditor_name` | string | 境内会计师事务所名称；默认返回 |
| `domestic_signing_cpa` | string | 境内会计师事务所签名注册会计师；默认返回 |
| `domestic_audit_opinion_code` | string | 境内会计师事务所审计意见类型编码；默认返回 |
| `domestic_audit_opinion_type` | string | 境内会计师事务所审计意见类型；默认返回 |
| `non_standard_opinion_content` | string | 非标准审计意见的事项内容 |
| `overseas_auditor_name` | string | 境外会计师事务所名称；默认返回 |
| `board_explanation_on_opinion` | string | 董事会对会计师事务所出具的有保留意见书、解释说明 |
| `overseas_non_standard_opinion_content` | string | 境外审计意见非标准的事项说明 |
| `overseas_audit_opinion_type` | string | 境外审计报告会计师事务所审计意见类型；默认返回 |
| `overseas_audit_opinion_code` | string | 境外审计报告会计师事务所审计意见类型编码；默认返回 |
| `overseas_signing_cpa` | string | 境外会计师事务所签名注册会计师；默认返回 |
| `supervisory_board_opinion` | string | 监事会对董事会就上述事项的说明所表示的意见 |
| `remark` | string | 备注 |
| `market_code` | string | 市场编码；默认返回 |

## pre_disclosure_date — 定期报告预披露时间

`GET /api/v1/data/pre_disclosure_date`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `market_code` | 否 | 市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `report_year` | 否 | 报告年度；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_name` | string | 证券简称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `report_year` | string/date | 报告年度；默认返回 |
| `scheduled_disclosure_date` | string/date | 预约披露日期；默认返回 |
| `change_date_1` | string/date | 变更日1；默认返回 |
| `change_date_2` | string/date | 变更日2；默认返回 |
| `change_date_3` | string/date | 变更日3；默认返回 |
| `actual_disclosure_date` | string/date | 实际批露日期；默认返回 |
| `remark` | string | 备注 |
| `market_code` | string | 市场编码；默认返回 |
| `change_date_4` | string/date | 变更日4；默认返回 |
| `change_date_5` | string/date | 变更日5；默认返回 |

## top5_suppliers — 公司前五大供应商信息表

`GET /api/v1/data/top5_suppliers`

> 数据来源于上市公司年报，定期更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 股票代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000002` |
| `end_date` | 否 | 统计截止日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_code` | string | 股票代码；默认返回 |
| `sec_name` | string | 股票简称；默认返回 |
| `end_date` | string/date | 统计截止日期；默认返回 |
| `rank` | number | 排名；默认返回 |
| `institution_name` | string | 供应商名称；默认返回 |
| `is_listed` | string | 是否上市公司；默认返回 |
| `business_symbol` | string | 公司股票代码；默认返回 |
| `is_related_company` | string | 是否上市公司关联公司；默认返回 |
| `related_symbol` | string | 关联上市公司股票代码；默认返回 |
| `purchase_amount` | number | 供应商采购额（元）；默认返回 |
| `proportion_of_total_value` | number | 供应商采购额占比（%）；默认返回 |
| `currency` | string | 币种；默认返回 |

## top5_customers — 公司前五大客户信息表

`GET /api/v1/data/top5_customers`

> 数据来源于上市公司年报，定期更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 股票代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000002` |
| `end_date` | 否 | 统计截止日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_code` | string | 股票代码；默认返回 |
| `sec_name` | string | 股票简称；默认返回 |
| `end_date` | string/date | 统计截止日期；默认返回 |
| `rank` | number | 排名；默认返回 |
| `institution_name` | string | 客户名称；默认返回 |
| `is_listed` | string | 是否上市公司；默认返回 |
| `business_symbol` | string | 公司股票代码；默认返回 |
| `is_related_company` | string | 是否上市公司关联公司；默认返回 |
| `related_symbol` | string | 关联上市公司股票代码；默认返回 |
| `sales_amount` | number | 客户销售额（元）；默认返回 |
| `proportion_of_total_value` | number | 客户销售额占比（%）；默认返回 |
| `currency` | string | 币种；默认返回 |
