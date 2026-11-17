# 股权与治理 — 15 个接口

> 本文件由 `tools/generate_catalog.py` 从 OpenAPI 规范自动生成，请勿手工编辑。

## actual_controller — 公司实际控制人

`GET /api/v1/data/actual_controller`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `control_type_code` | 否 | 控制类型编码 | string | 069001=单独控制；069002=实际控制人；069003=一致行动人；069004=家族控制 |
| `data_source_code` | 否 | 数据来源编码 | string | 033001=招募说明书；033002=上市公告书；033013=其他 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `change_date` | string/date | 变动日期；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `direct_holder_name` | string | 直接持有人名称 |
| `actual_controller_name` | string | 实际控制人名称；默认返回 |
| `controlling_shares` | number | 控股数量；默认返回 |
| `controlling_ratio` | number | 控股比例；默认返回 |
| `control_type_code` | string | 控制类型编码；默认返回 |
| `control_type` | string | 控制类型；默认返回 |
| `is_latest` | string | 最新标识；默认返回 |
| `direct_controller_name` | string | 直接控制人名称 |
| `actual_controller_type` | string | 实际控制人类型；默认返回 |
| `hierarchy_level` | string | 层级数；默认返回 |
| `remark` | string | 备注 |
| `direct_holder_name_en` | string | 直接持有人名称_英文 |
| `actual_controller_name_en` | string | 实际控制人名称_英文 |
| `direct_controller_name_en` | string | 直接控制人名称_英文 |
| `actual_controller_type_en` | string | 实际控制人类型_英文；默认返回 |
| `hierarchy_level_en` | string | 层级数_英文；默认返回 |
| `holder_relationship_en` | string | 持有人关联关系_英文 |
| `data_source_code` | string | 数据来源编码；默认返回 |
| `data_source` | string | 数据来源；默认返回 |

## capital_chg — 公司股本变动

`GET /api/v1/data/capital_chg`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `change_reason_code` | 否 | 变动原因编码 | string | 015001=A股上市；015002=B股上市；015003=H股上市；015004=增发新股上市；015005=配股上市；015006=职工股上市；015007=外资法人股上市；015008=转配股上市；015009=配售股份上市；015010=送股；015011=转增；015012=可转债转股；015013=股权转让；015014=股东性质变更；015015=吸收合并；015016=股份回购；015018=个人股上市；015019=定期报告；015020=股权分置；015021=股权分置受限股份上市；015022=权证行权；015023=配股除权；015025=股权激励；015026=招股说明书；015027=限售股份上市；015029=超额配售；015031=缩股；015032=分立上市；015033=D股上市；015034=重新上市；015035=GDR上市；015045=转板上市；015990=高管股限售；015992=期权行权；015995=报价转让；015997=承诺限售；015998=激励股份解禁；015999=其他 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `org_name_en` | string | 机构名称（英文）；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `change_date` | string/date | 变动日期；默认返回 |
| `change_reason_code` | string | 变动原因编码；默认返回 |
| `change_reason` | string | 变动原因；默认返回 |
| `change_reason_en` | string | 变动原因（英文）；默认返回 |
| `total_shares` | number | 总股本；默认返回 |
| `non_tradable_shares` | number | 未流通股份；默认返回 |
| `sponsor_shares` | number | 发起人股份；默认返回 |
| `state_shares` | number | 国家持股；默认返回 |
| `state_legal_entity_shares` | number | 国有法人持股；默认返回 |
| `domestic_legal_entity_shares` | number | 境内法人持股；默认返回 |
| `foreign_legal_entity_shares` | number | 境外法人持股；默认返回 |
| `individual_shares` | number | 自然人持股；默认返回 |
| `private_placement_legal_entity_shares` | number | 募集法人股；默认返回 |
| `internal_employee_shares` | number | 内部职工股 |
| `transfer_shares` | number | 转配股；默认返回 |
| `other_restricted_shares` | number | 其他流通受限股份；默认返回 |
| `preferred_shares` | number | 优先股；默认返回 |
| `other_non_tradable_shares` | number | 其他未流通股；默认返回 |
| `tradable_shares` | number | 已流通股份；默认返回 |
| `rmb_common_shares` | number | 人民币普通股；默认返回 |
| `b_shares` | number | 境内上市外资股（B股）；默认返回 |
| `h_shares` | number | 境外上市外资股（H股）；默认返回 |
| `executive_shares` | number | 高管股；默认返回 |
| `other_tradable_shares` | number | 其他流通股；默认返回 |
| `restricted_shares` | number | 流通受限股份；默认返回 |
| `placement_legal_entity_shares` | number | 配售法人股；默认返回 |
| `strategic_investor_shares` | number | 战略投资者持股；默认返回 |
| `securities_fund_shares` | number | 证券投资基金持股；默认返回 |
| `general_legal_entity_shares` | number | 一般法人持股；默认返回 |
| `state_shares_restricted` | number | 国家持股（受限）；默认返回 |
| `state_legal_entity_shares_restricted` | number | 国有法人持股（受限）；默认返回 |
| `other_domestic_shares_restricted` | number | 其他内资持股（受限）；默认返回 |
| `domestic_legal_entity_shares_restricted` | number | 其中：境内法人持股；默认返回 |
| `domestic_individual_shares_restricted` | number | 其中：境内自然人持股；默认返回 |
| `foreign_shares_restricted` | number | 外资持股（受限）；默认返回 |
| `foreign_legal_entity_shares_restricted` | number | 其中：境外法人持股；默认返回 |
| `foreign_individual_shares_restricted` | number | 其中：境外自然人持股；默认返回 |
| `restricted_executive_shares` | number | 其中：限售高管股；默认返回 |
| `restricted_b_shares` | number | 其中：限售B股；默认返回 |
| `restricted_h_shares` | number | 其中：限售H股；默认返回 |
| `controlling_shareholder_actual_controller_restricted` | number | 控股股东、实际控制人(受限)；默认返回 |
| `executive_shares_restricted` | number | 高管股份(受限)；默认返回 |
| `key_employee_shares_restricted` | number | 核心员工(受限)；默认返回 |
| `individual_or_fund_shares_restricted` | number | 个人或基金(受限)；默认返回 |
| `other_legal_entity_shares_restricted` | number | 其他法人(受限)；默认返回 |
| `other_shares_restricted` | number | 其他(受限)；默认返回 |
| `is_latest` | string | 最新记录标识；默认返回 |
| `remark` | string | 备注 |
| `others` | number | 其他；默认返回 |
| `controlling_shareholder_actual_controller` | number | 控股股东、实际控制人；默认返回 |

## major_sh — 主要股东持股

`GET /api/v1/data/major_sh`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `shareholder_type` | 否 | 股东类别 | string |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `shareholder_name` | string | 股东名称；默认返回 |
| `shareholder_sec_code` | string | 股东股票代码；默认返回 |
| `shareholder_type` | string | 股东类别；默认返回 |
| `shareholding_amount` | number | 持股数量；默认返回 |
| `shareholding_ratio` | number | 持股比例；默认返回 |
| `share_property` | string | 股份性质；默认返回 |
| `remark` | string | 备注 |

## sh_count — 公司股东人数

`GET /api/v1/data/sh_count`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `data_source_code` | 否 | 数据来源编码 | string | 033002=上市公告书；033003=定期报告；033013=其他 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `org_name_en` | string | 机构名称（英文）；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `short_name_en` | string | 英文简称；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `total_shareholders` | number | 股东总户数；默认返回 |
| `a_shareholders` | number | Ａ股户数；默认返回 |
| `b_shareholders` | number | Ｂ股户数；默认返回 |
| `h_shareholders` | number | Ｈ股户数；默认返回 |
| `avg_shares_per_household` | number | 户均持股；默认返回 |
| `avg_shareholding_ratio` | number | 户均持股比例；默认返回 |
| `remark` | string | 备注 |
| `shareholder_change_rate` | number | 股东人数变动幅度；默认返回 |
| `data_source_code` | string | 数据来源编码；默认返回 |
| `data_source` | string | 数据来源；默认返回 |

## top10_circulating_sh — 十大流通股东持股变化

`GET /api/v1/data/top10_circulating_sh`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `change_ratio` | number | 增减情况（比例）；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `shareholder_rank` | number | 股东名次；默认返回 |
| `shareholder_name` | string | 股东名称；默认返回 |
| `shareholder_type` | string | 股东类别；默认返回 |
| `shareholding_amount` | number | 持股数量；默认返回 |
| `total_shares_ratio` | number | 占总股本比例；默认返回 |
| `tradable_shares_ratio` | number | 占流通股本比例；默认返回 |
| `period_change` | number | 本期增减；默认返回 |
| `change_rate` | number | 增减幅；默认返回 |
| `change_status` | string | 变动状态；默认返回 |
| `share_property` | string | 股份性质；默认返回 |
| `b_shares_amount` | number | 持有B股数量；默认返回 |
| `h_shares_amount` | number | 持有H股数量；默认返回 |
| `other_shares_amount` | number | 持有其他股数量；默认返回 |
| `remark` | string | 备注 |

## top10_sh — 十大股东持股变化

`GET /api/v1/data/top10_sh`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `change_ratio` | number | 增减情况（比例）；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `shareholder_rank` | number | 股东名次；默认返回 |
| `shareholder_name` | string | 股东名称；默认返回 |
| `shareholder_type` | string | 股东类别；默认返回 |
| `shareholding_amount` | number | 持股数量；默认返回 |
| `total_shares_ratio` | number | 占总股本比例；默认返回 |
| `tradable_shares_ratio` | number | 占流通股本比例；默认返回 |
| `share_property` | string | 股份性质；默认返回 |
| `pledged_frozen_shares` | number | 股份质押冻结数量；默认返回 |
| `pledged_shares` | number | 股份质押数量；默认返回 |
| `frozen_shares` | number | 股份冻结数量；默认返回 |
| `shareholder_relationship` | string | 股东关联关系 |
| `restricted_shares_amount` | number | 持限售(未流通)股数量；默认返回 |
| `concerted_persons_group` | string | 一致行动人关系组；默认返回 |
| `tradable_shares_amount` | number | 持流通股数量；默认返回 |
| `remark` | string | 备注 |

## major_sh_chg — 大股东增（减）持情况

`GET /api/v1/data/major_sh_chg`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date-time |  |
| `change_type` | 否 | 增（减）持类型 | string | B=增持；S=减持 |
| `sec_category_code` | 否 | 证券类别编码 | string | 001001=A股；001002=B股；001012=优先股；001013=CDR；001014=GDR |
| `trading_method_code` | 否 | 交易方式编码 | string | 026008=大宗交易；026010=竞价交易；026011=大宗交易和竞价交易；026012=询价转让；026999=其他 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `announcement_date` | string/date-time | 公告日期；默认返回 |
| `change_deadline` | string/date | 增（减）持截止日；默认返回 |
| `change_type` | string | 增（减）持类型；默认返回 |
| `shareholder_name` | string | 股东名称；默认返回 |
| `change_amount` | number | 变动数量；默认返回 |
| `change_ratio_to_total` | number | 变动数量占总股本比例；默认返回 |
| `post_change_ratio` | number | 变动后占比；默认返回 |
| `price_upper_limit` | string | 增（减）持价格上限；默认返回 |
| `sec_category_code` | string | 证券类别编码；默认返回 |
| `sec_category` | string | 证券类别；默认返回 |
| `trading_method_code` | string | 交易方式编码；默认返回 |
| `trading_method` | string | 交易方式；默认返回 |
| `remark` | string | 备注 |
| `post_change_holding_amount` | number | 变动后持股数量；默认返回 |
| `post_change_tradable_amount` | number | 变动后持有流通股数量；默认返回 |
| `market_code` | string | 市场编码；默认返回 |

## sh_freeze — 公司股东股份冻结

`GET /api/v1/data/sh_freeze`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000006` |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `frozen_share_nature_code` | 否 | 被冻结股份性质编码 | string | 025001=境内法人股；025002=境外法人股；025003=自然人持股；025006=其他未流通股；025007=流通A股；025011=国家股；025012=国有法人股；025015=股权分置受限股份；025016=流通受限股份 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `frozen_party` | string | 被冻结当事人；默认返回 |
| `freeze_matter` | string | 冻结事项 |
| `frozen_share_nature_code` | string | 被冻结股份性质编码；默认返回 |
| `frozen_share_nature` | string | 被冻结股份性质；默认返回 |
| `frozen_quantity` | number | 冻结数量；默认返回 |
| `total_shares_ratio` | number | 占总股份比例；默认返回 |
| `freeze_applicant` | string | 冻结申请人；默认返回 |
| `freeze_executor` | string | 冻结执行人；默认返回 |
| `freeze_start_date` | string/date | 冻结起始日；默认返回 |
| `freeze_end_date` | string/date | 冻结终止日；默认返回 |
| `unfreeze_date` | string/date | 解冻日期；默认返回 |
| `cumulative_unfrozen_quantity` | number | 累计解冻数量；默认返回 |
| `unfreeze_explanation` | string | 解冻处理说明 |
| `remark` | string | 备注 |

## sh_pledge — 公司股东股份质押

`GET /api/v1/data/sh_pledge`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000002` |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date-time |  |
| `pledged_share_property_code` | 否 | 质押股份性质编码 | string | 025001=境内法人股；025002=境外法人股；025003=自然人持股；025005=转配股；025006=其他未流通股；025007=流通A股；025009=境外可流通股；025011=国家股；025012=国有法人股；025015=股权分置受限股份；025016=流通受限股份 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `announcement_date` | string/date-time | 公告日期；默认返回 |
| `pledgor` | string | 出质人；默认返回 |
| `pledgee` | string | 质权人；默认返回 |
| `pledge_matter` | string | 质押事项；默认返回 |
| `pledged_share_property_code` | string | 质押股份性质编码；默认返回 |
| `pledged_share_property` | string | 质押股份性质；默认返回 |
| `pledged_quantity` | number | 质押数量；默认返回 |
| `total_shares_ratio` | number | 占总股本比例；默认返回 |
| `pledge_start_date` | string/date | 质押起始日；默认返回 |
| `pledge_end_date` | string/date | 质押终止日；默认返回 |
| `pledge_release_date` | string/date | 质押解除日；默认返回 |
| `released_quantity` | number | 质押解除数量；默认返回 |
| `release_explanation` | string | 解除质押说明 |
| `is_pledged_repurchase_transaction` | string | 是否质押式回购交易；默认返回 |
| `remark` | string | 备注 |
| `this_pledge_ratio_of_holding` | number | 本次质押占其所持股份比例；默认返回 |
| `cumulative_pledged_shares` | number | 累计质押股数；默认返回 |
| `cumulative_pledge_ratio_of_holding` | number | 累计质押占所持股份比例；默认返回 |
| `cumulative_pledge_ratio_of_total` | number | 累计质押占总股本比例；默认返回 |
| `holding_shares` | number | 持有公司股份；默认返回 |
| `holding_ratio` | number | 持股比例(%)；默认返回 |
| `announcement_internal_code` | string | 公告内部编码 |

## holding_concentration — 股东持股集中度

`GET /api/v1/data/holding_concentration`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `statistical_item` | string | 统计项目；默认返回 |
| `shareholding_amount` | number | 股东持股数量；默认返回 |
| `shareholding_ratio` | number | 股东持股比例；默认返回 |
| `shareholding_ratio_change` | number | 股东持股比例比上报告期增减；默认返回 |
| `remark` | string | 备注 |

## mgmt_holding — 上市公司管理层持股及报酬

`GET /api/v1/data/mgmt_holding`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `data_source_code` | 否 | 数据来源编码 | string | 033001=招募说明书；033002=上市公告书；033003=定期报告；033004=业绩快报；033005=临时公告；033008=预披露公告；033009=增发；033010=配股 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `name` | string | 姓名；默认返回 |
| `executive_name` | string | 董监高姓名；默认返回 |
| `executive_position` | string | 董监高职务；默认返回 |
| `relationship_with_executive` | string | 变动人与董监高关系；默认返回 |
| `opening_shares` | number | 期初持股数量；默认返回 |
| `closing_shares` | number | 期末持股数量；默认返回 |
| `change_amount` | number | 变动数量；默认返回 |
| `change_ratio` | number | 变动比例；默认返回 |
| `average_price` | number | 成交均价；默认返回 |
| `closing_market_value` | number | 期末市值；默认返回 |
| `change_reason` | string | 持股变动原因；默认返回 |
| `data_source` | string | 数据来源；默认返回 |
| `remark` | string | 备注 |
| `annual_salary` | number | 年薪；默认返回 |
| `data_source_code` | string | 数据来源编码；默认返回 |
| `position_code` | string | 董监高职务编码；默认返回 |

## management — 公司管理人员情况

`GET /api/v1/data/management`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_org_name` | string | 证券机构名称；默认返回 |
| `org_name_en` | string | 机构名称（英文）；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `stock_short_name_en` | string | 股票简称(英文)；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `name` | string | 姓名；默认返回 |
| `name_en` | string | 姓名（英文）；默认返回 |
| `appointment_date` | string/date | 任职日期；默认返回 |
| `resignation_date` | string/date | 离职日期；默认返回 |
| `position_name` | string | 职务名称；默认返回 |
| `position_name_en` | string | 职务名称（英文）；默认返回 |
| `gender` | string | 性别；默认返回 |
| `education` | string | 教育程度；默认返回 |
| `birth_date` | string | 出生年月日；默认返回 |
| `nationality` | string | 国籍；默认返回 |
| `position_category_code` | string | 职务类别编码；默认返回 |
| `position_category` | string | 职务类别；默认返回 |
| `position_category_en` | string | 职务类别（英文）；默认返回 |
| `position_code` | string | 职务编码；默认返回 |
| `highest_degree` | string | 最高学历；默认返回 |
| `resume` | string | 个人简历 |
| `is_active` | string | 是否在职；默认返回 |
| `resignation_reason` | string | 离职原因；默认返回 |
| `remark` | string | 备注 |

## employee — 公司员工情况

`GET /api/v1/data/employee`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `end_date` | 否 | 截止日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `company_name` | string | 公司名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `end_date` | string/date | 截止日期；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `total_staff` | number | 员工总数；默认返回 |
| `is_latest` | string | 最新记录标识；默认返回 |
| `remark` | string | 备注 |
| `phd_count` | number | 博士人数；默认返回 |
| `master_count` | number | 硕士人数；默认返回 |
| `bachelor_count` | number | 本科人数；默认返回 |
| `college_count` | number | 大专人数；默认返回 |
| `high_school_below_count` | number | 高中及以下人数（其它）；默认返回 |
| `production_staff` | number | 生产人员；默认返回 |
| `sales_staff` | number | 销售人员；默认返回 |
| `technical_staff` | number | 技术人员；默认返回 |
| `finance_staff` | number | 财务人员；默认返回 |
| `admin_staff` | number | 行政人员；默认返回 |
| `other_staff` | number | 其它人员；默认返回 |

## restricted_release_date — 受限股份实际解禁日期

`GET /api/v1/data/restricted_release_date`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `restriction_reason_code` | 否 | 限售原因编码 | string | 100001=股改限售；100002=发行限售；100003=高管限售；100005=股权激励；100006=承诺限售；100007=网下配售（增发）；100008=网下配售（首发）；100009=非公开发行限售；100010=配股限售；100011=战略投资者配售（首发）；100013=增持限售；100014=IPO-老股东转让股份；100016=重新上市限售；100017=转板上市限售；100099=其它 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `shareholder_name` | string | 股东名称；默认返回 |
| `actual_lifting_date` | string/date | 实际解除限售日期；默认返回 |
| `actual_lifting_amount` | number | 实际解除限售数量；默认返回 |
| `actual_lifting_ratio` | number | 实际解除限售比例；默认返回 |
| `restriction_reason` | string | 限售原因；默认返回 |
| `restriction_reason_code` | string | 限售原因编码；默认返回 |
| `actual_tradable_amount` | number | 实际可流通数量；默认返回 |
| `seq_no` | number | 序号；默认返回 |
| `remark` | string | 备注 |
| `market_code` | string | 市场编码；默认返回 |

## restricted_listing_date — 受限股份流通上市日期

`GET /api/v1/data/restricted_listing_date`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `announcement_date` | string/date | 公告日期；默认返回 |
| `shareholder_name` | string | 股东名称；默认返回 |
| `estimated_lifting_date` | string/date | 预计解除限售日期；默认返回 |
| `estimated_lifting_amount` | number | 预计解除限售数量；默认返回 |
| `restriction_reason` | string | 限售原因；默认返回 |
| `restriction_reason_code` | string | 限售原因编码；默认返回 |
| `seq_no` | number | 序号；默认返回 |
| `remark` | string | 备注 |
| `market_code` | string | 市场编码；默认返回 |
