# 融资分配 — 8 个接口

> 本文件由 `tools/generate_catalog.py` 从 OpenAPI 规范自动生成，请勿手工编辑。

## margin_trade — 公司融资融券

`GET /api/v1/data/margin_trade`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `trade_date` | 否 | 交易日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `target_security_code` | 是 | 标的证券代码 | string | `000001` |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `target_security_name` | string | 标的证券简称；默认返回 |
| `trade_date` | string/date | 交易日期；默认返回 |
| `target_security_code` | string | 标的证券代码；默认返回 |
| `margin_balance` | number | 本日融资余额；默认返回 |
| `margin_buy_amount` | number | 本日融资买入额；默认返回 |
| `margin_repayment_amount` | number | 本日融资偿还额；默认返回 |
| `short_outstanding_volume` | number | 本日融券余量；默认返回 |
| `short_sell_volume` | number | 本日融券卖出量；默认返回 |
| `short_repayment_volume` | number | 本日融券偿还量；默认返回 |
| `short_outstanding_amount` | number | 融券余量金额；默认返回 |
| `margin_trading_balance` | number | 融资融券余额；默认返回 |
| `data_source` | string | 数据来源；默认返回 |
| `sec_category_code` | string | 证券类别编码；默认返回 |
| `sec_category` | string | 证券类别；默认返回 |
| `remark` | string | 备注 |

## pledge_ratio — 单一股票质押比例

`GET /api/v1/data/pledge_ratio`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `start_date` | 否 | 交易起始日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `end_date` | 否 | 交易截止日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_name` | string | 证券简称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `start_date` | string/date | 交易起始日期；默认返回 |
| `end_date` | string/date | 交易截止日期；默认返回 |
| `unrestricted_pledged_shares` | number | 无限售股份质押数量(万)；默认返回 |
| `restricted_pledged_shares` | number | 有限售股份质押数量(万)；默认返回 |
| `total_a_shares` | number | A股总股本(万)；默认返回 |
| `pledge_count` | number | 质押笔数；默认返回 |
| `pledge_ratio` | number | 质押比例；默认返回 |
| `remark` | string | 备注 |

## issuance_plan — 公司增发股票实施方案

`GET /api/v1/data/issuance_plan`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `market_code` | 否 | 市场编码 | string | 012001=上交所；012002=深交所主板；012008=股份报价系统；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date-time |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `announcement_date` | string/date-time | 公告日期；默认返回 |
| `stock_type_code` | string | 股票类别编码；默认返回 |
| `stock_type` | string | 股票类别；默认返回 |
| `total_issued_shares` | number | 总发行数量；默认返回 |
| `public_issued_shares` | number | 公开发行数量；默认返回 |
| `state_share_reduction` | number | 其中：国有股减持数量；默认返回 |
| `directed_institutional_shares` | number | 定向募集法人股；默认返回 |
| `directed_employee_shares` | number | 定向募集职工股；默认返回 |
| `other_issued_shares` | number | 其他发行数量；默认返回 |
| `par_value_per_share` | number | 每股面值；默认返回 |
| `issue_price_rmb` | number | 发行价格(人民币)；默认返回 |
| `issue_price_foreign` | number | 发行价格（外币）；默认返回 |
| `currency_code` | string | 币种编码；默认返回 |
| `currency` | string | 币种；默认返回 |
| `auction_upper_limit` | number | 竞价上限；默认返回 |
| `auction_lower_limit` | number | 竞价下限；默认返回 |
| `issue_pricing_method` | string | 发行定价方式；默认返回 |
| `old_shareholder_allotment_method` | string | 老股东配售方式；默认返回 |
| `old_shareholder_allotment_price` | number | 老股东配售价格；默认返回 |
| `old_shareholder_allotment_ratio` | number | 老股东配售比例；默认返回 |
| `weighted_issue_pe_ratio` | number | 加权发行市盈率；默认返回 |
| `diluted_issue_pe_ratio` | number | 摊薄发行市盈率；默认返回 |
| `net_assets_per_share_before_issue` | number | 发行前每股净资产；默认返回 |
| `net_assets_per_share_after_issue` | number | 发行后每股净资产；默认返回 |
| `estimated_raising_amount` | number | 预计募资金额；默认返回 |
| `actual_raising_amount` | number | 实际募资总额；默认返回 |
| `cash_amount` | number | 其中现金；默认返回 |
| `actual_raising_net_amount_rmb` | number | 实际募资净额（人民币）；默认返回 |
| `actual_raising_net_amount_foreign` | number | 实际募资净额（外币）；默认返回 |
| `total_issue_cost` | number | 发行费用总额；默认返回 |
| `underwriting_fee` | number | 承销费用；默认返回 |
| `issue_cost_per_share` | number | 每股发行费用；默认返回 |
| `issue_region` | string | 发行地区；默认返回 |
| `issue_region_code` | string | 发行地区编码；默认返回 |
| `issue_target` | string | 发行对象；默认返回 |
| `issue_method_code` | string | 发行方式编码；默认返回 |
| `issue_method` | string | 发行方式；默认返回 |
| `underwriting_method_code` | string | 承销方式编码；默认返回 |
| `underwriting_method` | string | 承销方式；默认返回 |
| `allocation_commitment` | string | 分配承诺；默认返回 |
| `is_ex_rights` | string | 是否除权；默认返回 |
| `share_registration_date` | string/date | 股权登记日；默认返回 |
| `ex_rights_date` | string/date | 除权日；默认返回 |
| `total_shares_before_issue` | number | 发行前总股本；默认返回 |
| `total_shares_after_issue` | number | 发行后总股本；默认返回 |
| `tradable_shares_before_issue` | number | 发行前流通股本；默认返回 |
| `tradable_shares_after_issue` | number | 发行后流通股本；默认返回 |
| `online_issue_date` | string/date | 网上发行日期；默认返回 |
| `offline_inquiry_start_date` | string/date | 网下询价配售开始日；默认返回 |
| `offline_inquiry_end_date` | string/date | 网下询价配售结束日；默认返回 |
| `other_issue_date` | string/date | 其他发行日期；默认返回 |
| `online_subscription_upper_limit` | number | 网上申购上限；默认返回 |
| `subscription_code_1` | string | 申购代码1；默认返回 |
| `subscription_name_1` | string | 申购简称1；默认返回 |
| `subscription_code_2` | string | 申购代码2；默认返回 |
| `subscription_name_2` | string | 申购简称2；默认返回 |
| `online_lottery_rate` | number | 网上发行中签率；默认返回 |
| `offline_lottery_rate` | number | 网下发行中签率；默认返回 |
| `subscription_multiple` | number | 起额认购倍数；默认返回 |
| `online_issue_shares` | number | 网上发行数量；默认返回 |
| `old_shareholder_allotment_shares` | number | 老股东配售数量；默认返回 |
| `offline_allotment_shares` | number | 网下配售数量；默认返回 |
| `underwriting_balance` | number | 承销余额；默认返回 |
| `clawback_shares` | number | 回拨数量；默认返回 |
| `clawback_method_code` | string | 回拨方式编码；默认返回 |
| `clawback_method` | string | 回拨方式；默认返回 |
| `online_valid_subscription_shares` | number | 网上有效申购股数；默认返回 |
| `online_valid_subscription_funds` | number | 网上有效申购资金；默认返回 |
| `online_valid_subscription_accounts` | number | 网上有效申购户数；默认返回 |
| `old_shareholder_valid_subscription_shares` | number | 老股东有效申购股数；默认返回 |
| `old_shareholder_valid_subscription_accounts` | number | 老股东有效申购户数；默认返回 |
| `old_shareholder_valid_subscription_funds` | number | 老股东有效申购资金；默认返回 |
| `offline_valid_subscription_accounts` | number | 网下有效申购户数；默认返回 |
| `offline_valid_subscription_shares` | number | 网下有效申购股数；默认返回 |
| `offline_valid_subscription_funds` | number | 网下有效申购资金；默认返回 |
| `corporate_subscription_shares` | number | 一般法人申购数量；默认返回 |
| `corporate_allotment_shares` | number | 一般法人配售数量；默认返回 |
| `corporate_allotment_accounts` | number | 一般法人配售户数；默认返回 |
| `securities_fund_subscription_shares` | number | 证券基金申购数量；默认返回 |
| `securities_fund_allotment_shares` | number | 证券基金配售数量；默认返回 |
| `securities_fund_allotment_accounts` | number | 证券基金配售户数；默认返回 |
| `strategic_investor_subscription_shares` | number | 战略投资者申购数量；默认返回 |
| `strategic_investor_allotment_shares` | number | 战略投资者配售数量；默认返回 |
| `strategic_investor_allotment_accounts` | number | 战略投资者配售户数；默认返回 |
| `listing_announcement_date` | string/date | 上市公告日期；默认返回 |
| `additional_share_listing_date` | string/date | 增发股上市日；默认返回 |
| `fund_arrival_date` | string/date | 资金到帐日；默认返回 |
| `estimated_issue_shares` | number | 预计发行股数；默认返回 |
| `online_preset_issue_ratio` | number | 网上预设发行数量比例；默认返回 |
| `offline_preset_issue_ratio` | number | 网下预设发行数量比例；默认返回 |
| `online_roadshow_start_date` | string/date | 网上路演起始日；默认返回 |
| `prospectus_website` | string | 招股意向书网址 |
| `original_shareholder_priority_date` | string/date | 原股东优先申购日；默认返回 |
| `original_shareholder_max_subscription_ratio` | number | 原股东最多认购数占发行数比例；默认返回 |
| `offline_subscription_lower_limit` | number | 网下申购数量下限；默认返回 |
| `offline_subscription_deposit` | number | 网下申购定金；默认返回 |
| `class_a_offline_subscription_ratio` | number | A 类投资者网下申购中签比例；默认返回 |
| `class_b_offline_subscription_ratio` | number | B 类投资者网下申购中签比例；默认返回 |
| `class_a_offline_subscription_unit` | number | A类投资者网下申购单位；默认返回 |
| `class_b_offline_subscription_unit` | number | B类投资者网下申购单位；默认返回 |
| `offline_subscription_upper_limit` | number | 网下申购数量上限；默认返回 |
| `class_a_subscription_lower_limit` | number | A类投资者认购下限；默认返回 |
| `class_b_subscription_lower_limit` | number | B类投资者认购下限；默认返回 |
| `class_a_lock_up_period` | number | A类锁定期；默认返回 |
| `offline_refund_date` | string/date | 网下资金退缴日；默认返回 |
| `online_subscription_lower_limit` | number | 网上申购数量下限；默认返回 |
| `online_subscription_unit` | number | 网上申购单位；默认返回 |
| `online_refund_date` | string/date | 网上资金退款日；默认返回 |
| `online_lottery_announcement_date` | string/date | 网上中签结果公告日；默认返回 |
| `unrestricted_shares_this_listing` | number | 本次上市的无流通限制及锁定安排的股份；默认返回 |
| `eps_after_issue` | number | 发行后每股收益；默认返回 |
| `trading_suspension_end_date` | string/date | 停牌截止日期；默认返回 |
| `trading_suspension_start_date` | string/date | 停牌起始日期；默认返回 |
| `offline_lottery_refund_date` | string/date | 网下中签率公布及退款日；默认返回 |
| `csdcc_online_fund_arrival_date` | string/date | CSDCC网上申购资金到帐日；默认返回 |
| `offline_deposit_arrival_date` | string/date | 网下申购定金到帐日；默认返回 |
| `remark` | string | 备注 |
| `subscription_name_1_en` | string | 申购简称1（英文）；默认返回 |
| `subscription_name_2_en` | string | 申购简称2（英文）；默认返回 |
| `coupon_rate` | number | 票面股息率；默认返回 |
| `capital_verification_date` | string/date | 验资日；默认返回 |

## rights_issue_plan — 公司配股实施方案

`GET /api/v1/data/rights_issue_plan`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `market_code` | 否 | 市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `stock_type_code` | string | 股票类别编码；默认返回 |
| `stock_type` | string | 股票类别；默认返回 |
| `rights_issue_ratio` | number | 配股比例；默认返回 |
| `rights_issue_price` | number | 配股价格；默认返回 |
| `estimated_rights_issue_shares` | number | 预计配股数量；默认返回 |
| `estimated_raising_funds` | number | 预计募集资金；默认返回 |
| `estimated_issue_cost` | number | 预计发行费用；默认返回 |
| `underwriting_method_code` | string | 承销方式编码；默认返回 |
| `underwriting_method` | string | 承销方式；默认返回 |
| `share_registration_date` | string/date | 股权登记日；默认返回 |
| `ex_rights_date` | string/date | 除权基准日；默认返回 |
| `rights_issue_payment_start_date` | string/date | 配股缴款起始日；默认返回 |
| `rights_issue_payment_end_date` | string/date | 配股缴款截止日；默认返回 |
| `actual_rights_issue_shares` | number | 实际配股数量；默认返回 |
| `underwriting_balance` | number | 承销余额；默认返回 |
| `actual_raising_amount` | number | 实际募资总额；默认返回 |
| `actual_raising_net_amount` | number | 实际募资净额；默认返回 |
| `total_issue_cost` | number | 发行费用总额；默认返回 |
| `underwriting_fee` | number | 承销费用；默认返回 |
| `fund_arrival_date` | string/date | 资金到账日；默认返回 |
| `total_shares_before_rights_issue` | number | 配股前总股本；默认返回 |
| `total_shares_after_rights_issue` | number | 配股后总股本；默认返回 |
| `tradable_shares_before_rights_issue` | number | 配股前流通股本；默认返回 |
| `tradable_shares_after_rights_issue` | number | 配股后流通股本；默认返回 |
| `state_shares_actual_subscription` | number | 国家股实配数量；默认返回 |
| `legal_person_shares_actual_subscription` | number | 法人股实配数量；默认返回 |
| `employee_shares_actual_subscription` | number | 职工股实配数量；默认返回 |
| `transfer_rights_shares_actual_subscription` | number | 转配股实配数量；默认返回 |
| `other_shares_actual_subscription` | number | 其他股份实配数量；默认返回 |
| `public_shares_actual_subscription` | number | 公众股实配数量；默认返回 |
| `major_shareholder_subscription_amount` | number | 大股东认购数量；默认返回 |
| `major_shareholder_subscription_method` | string | 大股东认购方式 |
| `transferable_rights_shares` | number | 可转配股数量；默认返回 |
| `legal_person_transfer_rights` | number | 法人获转配数量；默认返回 |
| `public_transfer_rights` | number | 公众获转配数量；默认返回 |
| `rights_transfer_fee_per_share` | number | 每股配权转让费；默认返回 |
| `public_rights_subscription_code` | string | 公众配售代码；默认返回 |
| `public_rights_subscription_name` | string | 公众配售简称；默认返回 |
| `other_rights_subscription_code` | string | 其他配售代码；默认返回 |
| `other_rights_subscription_name` | string | 其他配售简称；默认返回 |
| `listing_announcement_date` | string/date | 上市公告日期；默认返回 |
| `rights_issue_listing_date` | string/date | 配股上市日；默认返回 |
| `rights_warrant_trading_start_date` | string/date | 配股权证交易起始日；默认返回 |
| `rights_warrant_trading_end_date` | string/date | 配股权证交易截止日；默认返回 |
| `rights_issue_refund_date` | string/date | 配股失败，退还申购款日期；默认返回 |
| `trading_suspension_start_date` | string/date | 停牌起始日；默认返回 |
| `trading_suspension_end_date` | string/date | 停牌截止日；默认返回 |
| `rights_allotment_target` | string | 配售对象；默认返回 |
| `issue_method` | string | 发行方式；默认返回 |
| `rights_issue_result_announcement_date` | string/date | 配股发行结果公告日；默认返回 |
| `issue_method_code` | string | 发行方式编码；默认返回 |
| `entrusted_unit` | number | 委托单位；默认返回 |
| `remark` | string | 备注 |

## ipo — 公司首发股票

`GET /api/v1/data/ipo`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string |  |
| `market_code` | 否 | 市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `stock_type_code` | 否 | 股票类别编码 | string | 001001=A股；001002=B股；001013=CDR |
| `issue_method` | 否 | 发行方式 | string |  |
| `underwriting_method` | 否 | 承销方式 | string | 包销=；代销=；余额包销= |
| `issue_region` | 否 | 发行地区 | string |  |
| `clawback_method_code` | 否 | 回拨方式编码 | string | 050001=网下向网上回拨；050002=网上向网下回拨；050003=网上向二级市场回拨 |
| `listing_announcement_date` | 否 | 上市公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `ipo_stage_status_code` | 否 | IPO阶段进展状态编码 | string | 203001=正常发行；203003=暂缓发行；203005=恢复发行；203009=恢复上市进程 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `stock_type_code` | string | 股票类别编码；默认返回 |
| `stock_type` | string | 股票类别；默认返回 |
| `total_issued_shares` | number | 总发行数量；默认返回 |
| `public_issued_shares` | number | 公开发行数量；默认返回 |
| `state_share_reduction` | number | 其中：国有股减持数量；默认返回 |
| `directed_institutional_shares` | number | 定向募集法人股；默认返回 |
| `directed_employee_shares` | number | 定向募集职工股；默认返回 |
| `other_issued_shares` | number | 其他发行数量；默认返回 |
| `par_value_per_share` | number | 每股面值；默认返回 |
| `issue_price_rmb` | number | 发行价格（人民币）；默认返回 |
| `issue_price_foreign` | number | 发行价格（外币）；默认返回 |
| `foreign_currency_code` | string | 外币币种编码；默认返回 |
| `foreign_currency` | string | 外币币种；默认返回 |
| `weighted_issue_pe_ratio` | number | 加权发行市盈率；默认返回 |
| `diluted_issue_pe_ratio` | number | 摊薄发行市盈率；默认返回 |
| `net_assets_per_share_before_issue` | number | 发行前每股净资产；默认返回 |
| `net_assets_per_share_after_issue` | number | 发行后每股净资产；默认返回 |
| `issue_pricing_method` | string | 发行定价方式；默认返回 |
| `inquiry_upper_limit` | number | 询价上限；默认返回 |
| `inquiry_lower_limit` | number | 询价下限；默认返回 |
| `issue_target` | string | 发行对象；默认返回 |
| `issue_method_code` | string | 发行方式编码；默认返回 |
| `issue_method` | string | 发行方式；默认返回 |
| `underwriting_method_code` | string | 承销方式编码；默认返回 |
| `underwriting_method` | string | 承销方式；默认返回 |
| `issue_region` | string | 发行地区；默认返回 |
| `issue_region_code` | string | 发行地区编码；默认返回 |
| `main_sponsor` | string | 主要发起人；默认返回 |
| `allocation_commitment` | string | 分配承诺；默认返回 |
| `estimated_raising_funds` | number | 预计募集资金；默认返回 |
| `actual_raising_amount` | number | 实际募资总额；默认返回 |
| `actual_raising_net_amount_rmb` | number | 实际募资净额(人民币)；默认返回 |
| `actual_raising_net_amount_foreign` | number | 实际募资净额(外币)；默认返回 |
| `total_issue_cost` | number | 发行费用总额；默认返回 |
| `underwriting_fee` | number | 承销费用；默认返回 |
| `issue_cost_per_share` | number | 每股发行费用；默认返回 |
| `prospectus_announcement_date` | string/date | 招股公告日期；默认返回 |
| `market_value_calculation_date` | string/date | 市值计算日；默认返回 |
| `online_issue_date` | string/date | 上网发行日期；默认返回 |
| `secondary_market_allotment_date` | string/date | 二级市场配售日期；默认返回 |
| `offline_allotment_start_date` | string/date | 网下配售起始日；默认返回 |
| `offline_allotment_end_date` | string/date | 网下配售截止日；默认返回 |
| `other_issue_date` | string/date | 其他发行日期；默认返回 |
| `subscription_code_1` | string | 申购代码1；默认返回 |
| `subscription_name_1` | string | 申购简称1；默认返回 |
| `subscription_code_2` | string | 申购代码2；默认返回 |
| `subscription_name_2` | string | 申购简称2；默认返回 |
| `online_subscription_upper_limit` | number | 网上申购上限；默认返回 |
| `online_issue_shares` | number | 上网发行数量；默认返回 |
| `secondary_market_allotment_shares` | number | 二级市场配售数量；默认返回 |
| `offline_allotment_shares` | number | 网下配售数量；默认返回 |
| `clawback_shares` | number | 回拨数量；默认返回 |
| `clawback_method_code` | string | 回拨方式编码；默认返回 |
| `clawback_method` | string | 回拨方式；默认返回 |
| `underwriting_balance` | number | 承销余额；默认返回 |
| `online_issue_lottery_rate` | number | 上网发行中签率；默认返回 |
| `secondary_allotment_lottery_rate` | number | 二级市场配售发行中签率；默认返回 |
| `offline_allotment_lottery_rate` | number | 网下配售中签率；默认返回 |
| `oversubscription_multiple` | number | 超额认购倍数；默认返回 |
| `online_valid_subscription_shares` | number | 网上有效申购股数；默认返回 |
| `online_valid_subscription_accounts` | number | 网上有效申购户数；默认返回 |
| `online_valid_subscription_funds` | number | 网上有效申购资金；默认返回 |
| `secondary_allotment_valid_subscription_shares` | number | 二级配售有效申购股数；默认返回 |
| `secondary_allotment_valid_subscription_accounts` | number | 二级配售有效申购户数；默认返回 |
| `secondary_allotment_valid_subscription_funds` | number | 二级配售有效申购资金；默认返回 |
| `offline_valid_subscription_shares` | number | 网下有效申购股数；默认返回 |
| `offline_valid_subscription_accounts` | number | 网下有效申购户数；默认返回 |
| `offline_valid_subscription_funds` | number | 网下有效申购资金；默认返回 |
| `corporate_valid_subscription_shares` | number | 一般法人有效申购股数；默认返回 |
| `corporate_allotted_shares` | number | 一般法人获配数量；默认返回 |
| `corporate_allotted_accounts` | number | 一般法人获配户数；默认返回 |
| `strategic_valid_subscription_shares` | number | 战略投资者有效申购股数；默认返回 |
| `strategic_allotted_shares` | number | 战略投资者获配数量；默认返回 |
| `strategic_allotted_accounts` | number | 战略投资者获配户数；默认返回 |
| `securities_fund_valid_subscription_shares` | number | 证券基金有效申购数量；默认返回 |
| `securities_fund_allotted_shares` | number | 证券基金获配数量；默认返回 |
| `securities_fund_allotted_accounts` | number | 证券基金获配户数；默认返回 |
| `listing_announcement_date` | string/date | 上市公告日期；默认返回 |
| `fund_arrival_date` | string/date | 资金到帐日；默认返回 |
| `strategic_lock_up_period` | number | 战略投资者锁定期；默认返回 |
| `is_cumulative_inquiry` | string | 是否累计询价；默认返回 |
| `onsite_roadshow_start_date` | string/date | 现场推介起始日；默认返回 |
| `onsite_roadshow_end_date` | string/date | 现场推介截止日；默认返回 |
| `online_roadshow_start_date` | string/date | 网上路演起始日；默认返回 |
| `subscription_price_range` | string | 申购价格范围；默认返回 |
| `preliminary_inquiry_start_date` | string/date | 初步询价开始日期；默认返回 |
| `preliminary_inquiry_end_date` | string/date | 初步询价截止日期；默认返回 |
| `issue_price_range_announcement_date` | string/date | 发行价格区间公告日期；默认返回 |
| `offline_fund_refund_date` | string/date | 网下冻结资金返还日期；默认返回 |
| `online_fund_refund_date` | string/date | 网上冻结资金返还日期；默认返回 |
| `pricing_announcement_date` | string/date | 定价公告日期；默认返回 |
| `offline_lock_up_period` | number | 网下投资者锁定期；默认返回 |
| `estimated_issue_shares` | number | 预计发行股数；默认返回 |
| `online_preset_issue_ratio` | number | 网上预设发行数量比例；默认返回 |
| `offline_preset_issue_ratio` | number | 网下预设发行数量比例；默认返回 |
| `online_subscription_lower_limit` | number | 网上申购下限；默认返回 |
| `offline_subscription_upper_limit` | number | 网下申购上限；默认返回 |
| `offline_subscription_lower_limit` | number | 网下申购下限；默认返回 |
| `offline_subscription_unit` | number | 网下申购单位；默认返回 |
| `online_subscription_unit` | number | 网上申购单位；默认返回 |
| `offline_subscription_end_date` | string/date | 网下申购截止日；默认返回 |
| `prospectus_website` | string | 招股意向书网址 |
| `online_preset_issue_shares` | number | 网上预设发行数量；默认返回 |
| `offline_preset_issue_shares` | number | 网下预设发行数量；默认返回 |
| `offline_oversubscription_multiple` | number | 网下超额认购倍数；默认返回 |
| `strategic_issue_ratio` | number | 战略投资者发行量比例；默认返回 |
| `lottery_result_announcement_date` | string/date | 摇号结果公告日；默认返回 |
| `lottery_rate_announcement_date` | string/date | 中签率公告日；默认返回 |
| `is_over_allotment_exercised` | string | 是否行使超额配售权；默认返回 |
| `over_allotment_shares` | number | 超额配售数量；默认返回 |
| `preliminary_inquiry_oversubscription_multiple` | number | 初步询价超额认购倍数；默认返回 |
| `estimated_new_issue_upper_limit` | number | 预计新增发行数量上限；默认返回 |
| `estimated_old_shareholder_transfer_upper_limit` | number | 预计老股东转让数量上限；默认返回 |
| `estimated_strategic_allotment_upper_limit` | number | 预计战略配售数量上限；默认返回 |
| `strategic_investor_allotment_shares` | number | 战略投资者配售数量；默认返回 |
| `old_shareholder_transfer_shares` | number | 老股东转让数量；默认返回 |
| `total_issue_cost_2` | number | 发行费用总额2；默认返回 |
| `old_shareholder_transfer_issue_cost` | number | 老股东转让发行费用；默认返回 |
| `offline_subscription_rejection_ratio` | number | 网下申购剔除比例；默认返回 |
| `offline_subscription_rejection_lower_price` | number | 网下申购剔除价格下限；默认返回 |
| `ipo_stage_status` | string | IPO阶段进展状态；默认返回 |
| `ipo_stage_status_code` | string | IPO阶段进展状态编码；默认返回 |
| `remark` | string | 备注 |

## dividend_cap — 公司分红转增

`GET /api/v1/data/dividend_cap`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `dividend_year` | 否 | 分红年度：一季报:YYYY-03-31;中报:YYYY-06-30;三季报:YYYY-09-30;年报:YYYY-12-31；操作符：between（逗号分隔两个边界） | string/date |  |
| `share_base_year` | 否 | 股本基准年度；操作符：between（逗号分隔两个边界） | string/date |  |
| `market_code` | 否 | 交易市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `dividend_type` | 否 | 分红类型 | string | 年度分红=；中期分红=；季度分红=；重整转增=；特别分红=；承诺补偿=；股改分红=；其他= |
| `latest_announcement_date` | 否 | 最新公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `distribution_target_code` | 否 | 派发对象编码 | string | 243001=全体股东；243002=特定股东；243003=非原股东 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `org_name_en` | string | 机构名称（英文）；默认返回 |
| `currency` | string | 币种；默认返回 |
| `dividend_year` | string/date | 分红年度；默认返回 |
| `board_proposal_date` | string/date-time | 董事会预案公告日期；默认返回 |
| `board_proposal_description` | string | 董事会预案分红说明 |
| `shareholder_proposal_date` | string/date-time | 股东大会预案公告日期；默认返回 |
| `shareholder_proposal_description` | string | 股东大会预案分红说明 |
| `implementation_announcement_date` | string/date-time | 实施方案公告日期；默认返回 |
| `implementation_description` | string | 实施方案分红说明 |
| `allocation_share_base_actual` | number | 分配股本基数（实施）；默认返回 |
| `share_base_year` | string/date | 股本基准年度；默认返回 |
| `bonus_ratio` | number | 送股比例；默认返回 |
| `capitalization_ratio` | number | 转增比例；默认返回 |
| `dividend_ratio_rmb` | number | 派息比例(人民币)；默认返回 |
| `dividend_ratio_usd` | number | 派息比例（美元）；默认返回 |
| `dividend_ratio_hkd` | number | 派息比例（港币）；默认返回 |
| `bonus_shares` | number | 送股数量；默认返回 |
| `capitalization_shares` | number | 转增数量；默认返回 |
| `dividend_amount_rmb` | number | 派息金额(人民币)；默认返回 |
| `a_share_record_date` | string/date | A股股权登记日；默认返回 |
| `b_share_record_date` | string/date | B股股权登记日；默认返回 |
| `a_share_ex_rights_date` | string/date | A股除权日；默认返回 |
| `b_share_ex_rights_date` | string/date | B股除权基准日；默认返回 |
| `b_share_last_trading_date` | string/date | B股最后交易日；默认返回 |
| `dividend_payment_date_a` | string/date | 派息日(A)；默认返回 |
| `dividend_payment_date_b` | string/date | 派息日(B)；默认返回 |
| `a_share_bonus_shares_date` | string/date | A股送红股到帐日；默认返回 |
| `a_share_new_shares_listing_date` | string/date | A股新增股份上市日；默认返回 |
| `b_share_new_shares_listing_date` | string/date | B股新增股份上市日；默认返回 |
| `total_shares_before_transfer` | number | 送转前总股本；默认返回 |
| `total_shares_after_transfer` | number | 送转后总股本；默认返回 |
| `tradable_shares_before_transfer` | number | 送转前流通股本；默认返回 |
| `tradable_shares_after_transfer` | number | 送转后流通股本；默认返回 |
| `allocation_share_base_board` | number | 分配股本基数（董）；默认返回 |
| `allocation_share_base_shareholder` | number | 分配股本基数（股）；默认返回 |
| `plan_progress` | string | 方案进度；默认返回 |
| `cancellation_announcement_date` | string/date-time | 取消分红公告日期；默认返回 |
| `a_share_capitalization_shares_date` | string/date | A股转赠股份到帐日；默认返回 |
| `b_share_capitalization_shares_date` | string/date | B股转赠股份到帐日；默认返回 |
| `b_share_bonus_shares_date` | string/date | B股送红股到帐日；默认返回 |
| `exchange_rate` | number | 汇率；默认返回 |
| `remark` | string | 备注 |
| `market_code` | string | 交易市场编码；默认返回 |
| `dividend_type` | string | 分红类型；默认返回 |
| `latest_announcement_date` | string/date | 最新公告日期；默认返回 |
| `distribution_target_code` | string | 派发对象编码；默认返回 |
| `distribution_target` | string | 派发对象；默认返回 |

## ipo_review — 公司首发股票审核信息

`GET /api/v1/data/ipo_review`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `proposed_listing_board_code` | 否 | 拟上市板块编码 | string | 012001=上交所；012002=深交所主板；012003=深交所中小板；012015=深交所创业板；012029=上交所科创板；012046=北交所；012999=其他 |
| `review_progress_code` | 否 | 审核进度编码 | string | 149001=初审中；149002=落实反馈意见中；149003=已预披露；149004=已上发审会，暂缓表决；149005=已通过发审会；149006=中止审查；149007=终止审查；14900701=终止审查（撤回）；14900702=终止审查（审核不通过）；14900703=终止审查（未在规定时限内回复）；149008=已核准；149010=已受理；149011=已反馈；149012=预先披露更新；149013=已问询；149014=上市委会议通过；149015=提交注册；149019=注册生效；149020=不予注册；149021=已发行；149022=终止注册；149023=暂缓审议；149028=同意上市 |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `market_code` | 否 | 市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `approval_date` | 否 | 获批文日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `listing_type` | 否 | 上市类型 | string | IPO=；转板上市= |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `registered_location` | string | 注册地；默认返回 |
| `industry` | string | 所属行业或领域；默认返回 |
| `proposed_listing_board_code` | string | 拟上市板块编码；默认返回 |
| `proposed_listing_board` | string | 拟上市板块；默认返回 |
| `sponsor` | string | 保荐机构；默认返回 |
| `sponsor_representative` | string | 保荐代表人；默认返回 |
| `accounting_firm` | string | 会计师事务所；默认返回 |
| `signing_accountant` | string | 签字会计师；默认返回 |
| `law_firm` | string | 律师事务所；默认返回 |
| `signing_lawyer` | string | 签字律师；默认返回 |
| `review_progress_code` | string | 审核进度编码；默认返回 |
| `review_progress` | string | 审核进度；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `remark` | string | 备注 |
| `evaluation_agency` | string | 评估机构；默认返回 |
| `signing_evaluator` | string | 签字评估师；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `review_termination_date` | string/date | 终止审查决定时间；默认返回 |
| `approval_date` | string/date | 获批文日期；默认返回 |
| `listing_type` | string | 上市类型；默认返回 |
| `inquiry_date` | string/date | 已问询日期；默认返回 |
| `listing_committee_meeting_date` | string/date | 上市委会议日期；默认返回 |
| `registration_submission_date` | string/date | 提交注册日期；默认返回 |
| `csrc_submission_date` | string/date | 报送证监会日期；默认返回 |
| `registration_result_date` | string/date | 注册结果日期；默认返回 |
| `review_result_date` | string/date | 审核结果日期；默认返回 |
| `is_registration_system` | string | 是否注册制上市；默认返回 |

## underwriting — 股票发行中介机构及承销情况

`GET /api/v1/data/underwriting`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string |  |
| `market_code` | 否 | 市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `issue_start_date` | 否 | 发行起始日；操作符：between（逗号分隔两个边界） | string/date |  |
| `issue_type_code` | 否 | 发行类别编码 | string | 053001=首发新股；053002=增发新股；053003=配股；053010=权证发行 |
| `intermediary_type_code` | 否 | 中介机构类别编码 | string | 021001=上市推荐人；021002=发行协调人；021003=会计师事务所；021004=律师事务所；021005=主承销商；021006=副主承销商；021009=上市保荐人；021010=分销商；021011=财务审计机构；021012=资产评估机构；021013=土地评估机构；021014=国际发行协调人；021015=直销机构；021019=联席保荐人；021031=保荐人；021035=财务顾问；021050=联席主承销商；021051=独立财务顾问；021052=牵头主承销商；021053=承销商；021056=CDR存托人；021057=CDR托管人；021059=联席上市保荐人 |
| `change_date` | 否 | 变更日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `issue_start_date` | string/date | 发行起始日；默认返回 |
| `issue_type_code` | string | 发行类别编码；默认返回 |
| `issue_type` | string | 发行类别；默认返回 |
| `intermediary_type_code` | string | 中介机构类别编码；默认返回 |
| `intermediary_type` | string | 中介机构类别；默认返回 |
| `intermediary_name` | string | 中介机构名称；默认返回 |
| `underwriting_amount` | number | 承销数量；默认返回 |
| `underwriting_ratio` | number | 承销比例；默认返回 |
| `change_date` | string/date | 变更日期；默认返回 |
| `remark` | string | 备注 |
