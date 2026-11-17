# 交易信息 — 11 个接口

> 本文件由 `tools/generate_catalog.py` 从 OpenAPI 规范自动生成，请勿手工编辑。

## daily_quote_latest — 股票最新日行情

`GET /api/v1/data/daily_quote_latest`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string |  |
| `market_code` | 否 | 交易市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `trade_date` | 否 | 交易日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_name` | string | 证券简称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `trade_date` | string/date | 交易日期；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `exchange` | string | 交易所；默认返回 |
| `prev_close` | number | 昨收盘；默认返回 |
| `open_price` | number | 开盘价；默认返回 |
| `volume` | number | 成交数量；默认返回 |
| `high_price` | number | 最高价；默认返回 |
| `low_price` | number | 最低价；默认返回 |
| `last_price` | number | 最近成交价；默认返回 |
| `total_trades` | number | 总笔数；默认返回 |
| `change` | number | 涨跌；默认返回 |
| `change_ratio` | number | 涨跌幅；默认返回 |
| `turnover` | number | 成交金额；默认返回 |
| `turnover_rate` | number | 换手率；默认返回 |
| `amplitude` | number | 振幅；默认返回 |
| `total_shares` | number | 公司总股本；默认返回 |
| `issued_shares` | number | 发行总股本；默认返回 |
| `float_shares` | number | 流通股本；默认返回 |
| `sec_name_en` | string | 证券简称（英文）；默认返回 |
| `exchange_en` | string | 交易所（英文）；默认返回 |
| `bid_volume` | number | 叫买揭示；默认返回 |
| `ask_volume` | number | 叫卖揭示；默认返回 |
| `pe_ratio` | number | 市盈率；默认返回 |
| `remark` | string | 备注 |

## daily_quote_hist — 股票历史日行情

`GET /api/v1/data/daily_quote_hist`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `trade_date` | 是 | 交易日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_name` | string | 证券简称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `trade_date` | string/date | 交易日期；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `exchange` | string | 交易所；默认返回 |
| `prev_close` | number | 昨日收盘价；默认返回 |
| `open_price` | number | 今日开盘价；默认返回 |
| `volume` | number | 成交数量；默认返回 |
| `high_price` | number | 最高成交价；默认返回 |
| `low_price` | number | 最低成交价；默认返回 |
| `last_price` | number | 最近成交价；默认返回 |
| `total_trades` | number | 总笔数；默认返回 |
| `change` | number | 涨跌；默认返回 |
| `change_ratio` | number | 涨跌幅；默认返回 |
| `turnover` | number | 成交金额；默认返回 |
| `turnover_rate` | number | 换手率；默认返回 |
| `amplitude` | number | 振幅；默认返回 |
| `total_shares` | number | 公司总股本；默认返回 |
| `issued_shares` | number | 发行总股本；默认返回 |
| `float_shares` | number | 流通股本；默认返回 |
| `sec_name_en` | string | 证券简称（英文）；默认返回 |
| `exchange_en` | string | 交易所（英文）；默认返回 |
| `bid_volume` | number | 叫买揭示；默认返回 |
| `ask_volume` | number | 叫卖揭示；默认返回 |
| `pe_ratio` | number | 市盈率1；默认返回 |
| `remark` | string | 备注 |

## block_trade — 公司大宗交易

`GET /api/v1/data/block_trade`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `trade_date` | 否 | 交易日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_name` | string | 证券简称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `trade_date` | string/date | 交易日期；默认返回 |
| `exchange` | string | 交易所；默认返回 |
| `seq_no` | number | 序号；默认返回 |
| `buyer_branch` | string | 买方营业部；默认返回 |
| `seller_branch` | string | 卖方营业部；默认返回 |
| `trade_price` | number | 成交价格；默认返回 |
| `trade_volume` | number | 成交量；默认返回 |
| `trade_amount` | number | 成交金额；默认返回 |
| `remark` | string | 备注 |

## abnormal_info — 沪深异动证券公开信息

`GET /api/v1/data/abnormal_info`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `trade_date` | 否 | 交易日期；操作符：between（逗号分隔两个边界） | string/date-time |  |
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string |  |
| `market_code` | 否 | 市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `info_type_code` | 否 | 信息类型编码 | string | 070001=涨幅偏离值达7%的证券；070002=跌幅偏离值达7%的证券；070003=振幅值达15%的证券；070004=换手率达20%的证券；070005=连续三个交易日内涨幅偏离值累计达20%的证券；070006=连续三个交易日内跌幅偏离值累计达20%的证券；070007=连续三个交易日内涨幅偏离值累计达15%的ST证券；070008=连续三个交易日内跌幅偏离值累计达15%的ST证券；070009=无价格涨跌幅限制；070010=连续三个交易日内的日均换手率与前五个交易日日均换手率的比值到达30倍,并且该股票封闭式基金连续三个交易日内累计换手率达到20%；070011=其它异常波动；070012=连续三个交易日收盘价达到涨幅限制价格的ST证券、*ST证券；070013=连续三个交易日收盘价达到跌幅限制价格的ST证券、*ST证券；070014=连续三日内，日均换手率与前五日比值达30倍，且累计达20%；070017=当日无价格涨跌幅限制盘中交易价格较当日开盘价上涨30％以上；070019=当日有涨跌幅限制的A股，连续2个交易日触及涨幅限制，在这2个交易日中同一营业部净买入股数占当日总成交股数的比重30％以上，且上市公司未有重大事项公告；070020=ST股票、*ST股票和S股连续三个交易日触及涨幅限制的；070021=ST股票、*ST股票和S股连续三个交易日触及跌幅限制的；070022=单只标的证券的当日融资买入数量达到当日该证券总交易量的50％以上；070023=单只标的证券的当日融券卖出数量达到当日该证券总交易量的50％以上；070025=当日有涨跌幅限制的A股，连续2个交易日触及跌幅限制，在这2个交易日中同一营业部净卖出股数占当日总成交股数的比重30％以上，且上市公司未有重大事项公告；070026=退市整理期；070027=涨幅达到15%的证券；070028=跌幅达到15%的证券；070029=振幅达到30%的证券；070030=换手率达到30%的证券；070031=连续三个交易日内收盘价格涨幅偏离值累计达到30%的证券；070032=连续三个交易日内收盘价格跌幅偏离值累计达到30%的证券；070035=北交所股票最近3个有成交的交易日以内收盘价涨跌幅偏离值累计达到+40%(-40%)；070036=上市首日可转债 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_name` | string | 证券简称；默认返回 |
| `trade_date` | string/date-time | 交易日期；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `info_type_code` | string | 信息类型编码；默认返回 |
| `info_type` | string | 信息类型；默认返回 |
| `trade_type` | string | 交易类型；默认返回 |
| `rank` | number | 排名；默认返回 |
| `branch_name` | string | 营业部(席位)名称；默认返回 |
| `buy_amount` | number | 买入金额；默认返回 |
| `sell_amount` | number | 卖出金额；默认返回 |
| `total_amount` | number | 交易金额；默认返回 |
| `remark` | string | 备注 |
| `abnormal_period` | string | 异常期间；默认返回 |
| `trade_volume` | number | 成交量；默认返回 |
| `trade_amount` | number | 成交金额；默认返回 |

## suspend_resume — 证券交易停复牌信息

`GET /api/v1/data/suspend_resume`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string |  |
| `market_code` | 否 | 交易市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `sec_category_code` | 否 | 证券类别编码 | string | 001001=A股；001002=B股；001004=股份报价；001013=CDR |
| `suspend_time` | 否 | 停牌时间；操作符：between（逗号分隔两个边界） | string/date-time |  |
| `resume_time` | 否 | 复牌时间；操作符：between（逗号分隔两个边界） | string/date-time |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_name` | string | 证券简称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_category` | string | 证券类别；默认返回 |
| `sec_category_code` | string | 证券类别编码；默认返回 |
| `suspend_time` | string/date-time | 停牌时间；默认返回 |
| `resume_time` | string/date-time | 复牌时间；默认返回 |
| `suspend_duration` | string | 停牌期限；默认返回 |
| `suspend_reason` | string | 停牌原因 |
| `market_code` | string | 交易市场编码；默认返回 |
| `market_name` | string | 交易市场；默认返回 |
| `remark` | string | 备注 |

## weekly_quote — 股票行情周报

`GET /api/v1/data/weekly_quote`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string |  |
| `start_date` | 否 | 开始日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `exchange` | 否 | 交易所 | string | 上交所=；深交所=；北交所= |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_name` | string | 证券简称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `start_date` | string/date | 开始日期；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `exchange` | string | 交易所；默认返回 |
| `trading_days` | number | 交易天数；默认返回 |
| `prev_week_close` | number | 上周收盘；默认返回 |
| `week_open` | number | 本周开盘；默认返回 |
| `volume` | number | 成交数量；默认返回 |
| `week_high` | number | 最高成交；默认返回 |
| `week_low` | number | 最低成交；默认返回 |
| `last_price` | number | 最近成交；默认返回 |
| `total_trades` | number | 总笔数；默认返回 |
| `float_shares` | number | 流通股本；默认返回 |
| `change` | number | 涨跌；默认返回 |
| `change_ratio` | number | 涨跌幅；默认返回 |
| `turnover` | number | 成交金额；默认返回 |
| `turnover_rate` | number | 换手率；默认返回 |
| `trading_week` | string | 交易周；默认返回 |
| `week_amplitude` | number | 周振幅；默认返回 |
| `remark` | string | 备注 |
| `total_shares` | number | 公司总股本；默认返回 |
| `issued_shares` | number | 发行总股本；默认返回 |
| `sec_name_en` | string | 证券简称（英文）；默认返回 |
| `exchange_en` | string | 交易所（英文）；默认返回 |
| `bid_volume` | number | 叫买揭示；默认返回 |
| `ask_volume` | number | 叫卖揭示；默认返回 |
| `pe_ratio` | number | 市盈率1；默认返回 |

## monthly_quote — 股票行情月报

`GET /api/v1/data/monthly_quote`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string |  |
| `start_date` | 否 | 开始日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `exchange` | 否 | 交易所 | string | 上交所=；深交所=；北交所= |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_name` | string | 证券简称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `start_date` | string/date | 开始日期；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `exchange` | string | 交易所；默认返回 |
| `trading_days` | number | 交易天数；默认返回 |
| `prev_month_close` | number | 上月收盘；默认返回 |
| `month_open` | number | 本月开盘；默认返回 |
| `volume` | number | 成交数量；默认返回 |
| `month_high` | number | 最高成交；默认返回 |
| `month_low` | number | 最低成交；默认返回 |
| `last_price` | number | 最近成交；默认返回 |
| `total_trades` | number | 总笔数；默认返回 |
| `float_shares` | number | 流通股本；默认返回 |
| `change` | number | 涨跌；默认返回 |
| `change_ratio` | number | 涨跌幅；默认返回 |
| `turnover` | number | 成交金额；默认返回 |
| `turnover_rate` | number | 换手率；默认返回 |
| `trading_month` | string | 交易月；默认返回 |
| `month_amplitude` | number | 月振幅；默认返回 |
| `remark` | string | 备注 |
| `total_shares` | number | 公司总股本；默认返回 |
| `issued_shares` | number | 发行总股本；默认返回 |
| `sec_name_en` | string | 证券简称（英文）；默认返回 |
| `exchange_en` | string | 交易所（英文）；默认返回 |
| `bid_volume` | number | 叫买揭示；默认返回 |
| `ask_volume` | number | 叫卖揭示；默认返回 |
| `pe_ratio` | number | 市盈率1；默认返回 |

## special_notice — 证券交易特别提示

`GET /api/v1/data/special_notice`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string |  |
| `market_code` | 否 | 交易市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `sec_category_code` | 否 | 证券类别编码 | string | 001001=A股；001002=B股；001013=CDR；002001=国债；002028=私募债；003001=封闭式基金；003002=开放式基金；003008=QDII |
| `event_type` | 否 | 事件种类 | string | `首发新股上市日` |
| `event_date` | 否 | 发生日期；操作符：between（逗号分隔两个边界） | string/date-time |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_name` | string | 证券简称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `sec_category` | string | 证券类别；默认返回 |
| `sec_category_code` | string | 证券类别编码；默认返回 |
| `event_type_code` | string | 事件种类编码；默认返回 |
| `event_type` | string | 事件种类；默认返回 |
| `event_date` | string/date-time | 发生日期；默认返回 |
| `event_content` | string | 事件内容 |
| `remark` | string | 备注 |

## multi_market_daily — 多市场交易日报

`GET /api/v1/data/multi_market_daily`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `exchange_code` | 否 | 交易所编码 | string | 012001=上交所；012002=深交所主板；012006=港交所主板；012007=港交所创业板；012008=股份报价系统 |
| `exchange_name` | 否 | 交易所 | string | 上交所=；深交所=；港交所主板=；港交所创业板=；股份报价系统= |
| `trade_date` | 否 | 交易日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `exchange_code` | string | 交易所编码；默认返回 |
| `exchange_name` | string | 交易所；默认返回 |
| `trade_date` | string/date | 交易日期；默认返回 |
| `subject_code` | string | 科目编码；默认返回 |
| `subject_name` | string | 科目名称；默认返回 |
| `subject_data` | number | 科目数据；默认返回 |
| `unit` | string | 单位；默认返回 |
| `remark` | string | 备注 |

## weekly_acct_stats — 一周股票账户情况统计

`GET /api/v1/data/weekly_acct_stats`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `start_date` | 否 | 开始日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `announcement_date` | string/date | 公告日期；默认返回 |
| `start_date` | string/date | 开始日期；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `weekly_account_stats_category` | string | 一周股票账户情况统计类别；默认返回 |
| `weekly_account_stats_category_code` | string | 一周股票账户情况统计类别编码；默认返回 |
| `sh_account_count` | number | 市场户数（沪）；默认返回 |
| `sz_account_count` | number | 市场户数（深）；默认返回 |
| `total` | number | 合计；默认返回 |
| `remark` | string | 备注 |

## ipo_approval — 新股过会情况

`GET /api/v1/data/ipo_approval`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `meeting_date` | 否 | 上会日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `announcement_date` | 否 | 审核公告日；操作符：between（逗号分隔两个边界） | string/date |  |
| `market_code` | 否 | 市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `company_name` | string | 公司名称；默认返回 |
| `review_type_code` | string | 审核类型编码；默认返回 |
| `review_type` | string | 审核类型；默认返回 |
| `meeting_date` | string/date | 上会日期；默认返回 |
| `review_content` | string | 审议内容 |
| `review_result` | string | 审核结果；默认返回 |
| `announcement_date` | string/date | 审核公告日；默认返回 |
| `remark` | string | 备注 |
| `market_code` | string | 市场编码；默认返回 |
