# 重大事项 — 6 个接口

> 本文件由 `tools/generate_catalog.py` 从 OpenAPI 规范自动生成，请勿手工编辑。

## penalty — 公司受处罚记录

`GET /api/v1/data/penalty`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000002` |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date-time |  |
| `penalty_type_code` | 否 | 处罚类型编码 | string | 045001=公开谴责；045002=罚款；045003=警告；045004=通报批评；045005=市场禁入；045006=责令整改；045007=行政处罚；045008=刑事处罚；045009=非行政处罚-出具监管关注函；045010=非行政处罚-出具监管工作函；045011=警示函；045012=非行政处罚-问询函；045013=非行政处罚-监管警示；045014=公开认定不适合担任相关职务；045999=其他 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `company_name` | string | 公司名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `announcement_date` | string/date-time | 公告日期；默认返回 |
| `penalty_type_code` | string | 处罚类型编码；默认返回 |
| `penalty_type` | string | 处罚类型；默认返回 |
| `penalty_reason` | string | 处罚原因 |
| `penalty_department` | string | 处罚部门；默认返回 |
| `penalty_target` | string | 处罚对象；默认返回 |
| `penalty_content` | string | 处罚内容 |
| `penalty_amount` | number | 处罚金额；默认返回 |
| `remark` | string | 备注 |
| `market_code` | string | 市场编码；默认返回 |
| `penalty_target_en` | string | 处罚对象英文翻译；默认返回 |
| `institution_fine_amount` | number | 对机构罚款金额；默认返回 |
| `individual_fine_amount` | number | 对个人罚款金额；默认返回 |

## arbitration — 公司仲裁

`GET /api/v1/data/arbitration`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000006` |
| `market_code` | 否 | 交易市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date-time |  |
| `company_position_code` | 否 | 公司所处地位编码 | string | 047001=原告；047002=被告；047003=申请方；047004=被申请方；047005=第三方 |
| `case_cause_code` | 否 | 案由编码 | string | 066001=借款纠纷；066002=担保纠纷；066003=股权纠纷；066004=往来款纠纷；066005=合同纠纷；066999=其他原因 |
| `progress_status_code` | 否 | 进展状态编码 | string | 067001=和解；067002=执行；067003=未执行；067004=提起诉讼；067005=已裁决 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `company_name` | string | 公司名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `announcement_date` | string/date-time | 公告日期；默认返回 |
| `applicant` | string | 申请方；默认返回 |
| `respondent` | string | 被申请方；默认返回 |
| `arbitration_matter` | string | 仲裁事项；默认返回 |
| `company_position_code` | string | 公司所处地位编码；默认返回 |
| `company_position` | string | 公司所处地位；默认返回 |
| `case_cause_code` | string | 案由编码；默认返回 |
| `case_cause` | string | 案由；默认返回 |
| `involved_amount` | number | 涉及金额；默认返回 |
| `currency_code` | string | 币种编码；默认返回 |
| `currency` | string | 币种；默认返回 |
| `subject_matter` | string | 标的；默认返回 |
| `hearing_date` | string/date | 开庭日期；默认返回 |
| `arbitration_institution` | string | 仲裁机构；默认返回 |
| `ruling_content` | string | 裁决内容 |
| `ruling_execution_status` | string | 裁决执行情况 |
| `impact_on_company` | string | 对本公司的影响；默认返回 |
| `arbitration_cost` | number | 仲裁费用；默认返回 |
| `progress_status_code` | string | 进展状态编码；默认返回 |
| `progress_status` | string | 进展状态；默认返回 |
| `remark` | string | 备注 |
| `market_code` | string | 市场编码；默认返回 |

## litigation — 公司诉讼

`GET /api/v1/data/litigation`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `market_code` | 否 | 交易市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date-time |  |
| `company_position_code` | 否 | 公司所处地位编码 | string | 047001=原告；047002=被告；047003=申请方；047004=被申请方；047005=第三方 |
| `case_cause_code` | 否 | 案由编码 | string | 066001=借款纠纷；066002=担保纠纷；066003=股权纠纷；066004=往来款纠纷；066005=合同纠纷；066999=其他原因 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `announcement_date` | string/date-time | 公告日期；默认返回 |
| `plaintiff` | string | 原告；默认返回 |
| `defendant` | string | 被告；默认返回 |
| `litigation_matter` | string | 诉讼事项；默认返回 |
| `company_position_code` | string | 公司所处地位编码；默认返回 |
| `company_position` | string | 公司所处地位；默认返回 |
| `case_cause_code` | string | 案由编码；默认返回 |
| `case_cause` | string | 案由；默认返回 |
| `involved_amount` | number | 涉及金额；默认返回 |
| `currency_code` | string | 币种编码；默认返回 |
| `currency` | string | 币种；默认返回 |
| `subject_matter` | string | 标的；默认返回 |
| `hearing_date` | string/date | 开庭日期；默认返回 |
| `first_instance_court` | string | 诉讼一审机构；默认返回 |
| `second_instance_court` | string | 诉讼二审机构；默认返回 |
| `appeal_court` | string | 诉讼申诉机构；默认返回 |
| `first_instance_ruling` | string | 一审裁决情况 |
| `second_instance_ruling` | string | 二审裁决情况 |
| `appeal_status` | string | 申诉情况 |
| `judgment_execution_status` | string | 判决执行情况 |
| `impact_on_company` | string | 对本公司的影响；默认返回 |
| `litigation_cost` | number | 诉讼费用；默认返回 |
| `repayment_amount` | number | 偿还金额；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `market_name` | string | 市场名称；默认返回 |
| `remark` | string | 备注 |
| `is_first_instance_appealed` | string | 一审_是否上诉；默认返回 |
| `progress_status` | string | 进展情况 |
| `latest_announcement_date` | string/date | 最新公告日期；默认返回 |

## asset_freeze — 公司资产冻结

`GET /api/v1/data/asset_freeze`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000007` |
| `market_code` | 否 | 交易市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date-time |  |
| `freeze_start_date` | 否 | 冻结起始日；操作符：between（逗号分隔两个边界） | string/date |  |
| `freeze_end_date` | 否 | 冻结截止日；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `company_name` | string | 公司名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `announcement_date` | string/date-time | 公告日期；默认返回 |
| `frozen_unit` | string | 被冻结单位；默认返回 |
| `frozen_asset_type_code` | string | 冻结资产类型编码；默认返回 |
| `frozen_asset_type` | string | 冻结资产类型；默认返回 |
| `frozen_asset` | string | 冻结资产 |
| `frozen_asset_amount` | number | 冻结资产金额；默认返回 |
| `freeze_unit` | string | 冻结单位；默认返回 |
| `freeze_reason` | string | 冻结原因；默认返回 |
| `freeze_start_date` | string/date | 冻结起始日；默认返回 |
| `freeze_end_date` | string/date | 冻结截止日；默认返回 |
| `post_frozen_explanation` | string | 事后说明 |
| `application_freeze_unit` | string | 申请冻结单位；默认返回 |
| `remark` | string | 备注 |
| `market_code` | string | 市场编码；默认返回 |

## external_guarantee — 公司对外担保

`GET /api/v1/data/external_guarantee`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000002` |
| `market_code` | 否 | 交易市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date-time |  |
| `guarantee_type_code` | 否 | 担保类别编码 | string | 068001=保证额度；068002=保证；068003=抵押；068004=质押；068005=互保；068006=反担保 |
| `related_party_relationship_code` | 否 | 双方关联关系编码 | string | 039001=实际控制人；039002=控股股东；039003=一般股东；039004=受同一股东控制；039005=控股子公司；039006=参股公司；039007=孙公司；039999=其他 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `announcement_date` | string/date-time | 公告日期；默认返回 |
| `guarantor` | string | 担保方；默认返回 |
| `guaranteed_party` | string | 被担保方；默认返回 |
| `guarantee_matter` | string | 担保事项；默认返回 |
| `guarantee_type_code` | string | 担保类别编码；默认返回 |
| `guarantee_type` | string | 担保类别；默认返回 |
| `agreement_signing_date` | string/date | 协议签署日期；默认返回 |
| `is_related_transaction` | string | 是否关联交易；默认返回 |
| `related_party_relationship_code` | string | 双方关联关系编码；默认返回 |
| `related_party_relationship` | string | 双方关联关系；默认返回 |
| `guarantee_amount` | number | 担保金额；默认返回 |
| `currency_code` | string | 币种编码；默认返回 |
| `currency` | string | 币种；默认返回 |
| `guarantee_period` | number | 担保期限；默认返回 |
| `loan_start_date` | string/date | 借款开始日期；默认返回 |
| `loan_end_date` | string/date | 借款结束日期；默认返回 |
| `loan_annual_rate` | number | 借款年利率；默认返回 |
| `collateral` | string | 抵押或质押物；默认返回 |
| `creditor` | string | 债权人；默认返回 |
| `post_period_related_matters` | string | 期后相关事项 |
| `guarantee_exemption_date` | string/date | 担保免除日期；默认返回 |
| `guarantee_progress` | string | 担保进程；默认返回 |
| `guarantee_start_date` | string/date | 担保开始日期；默认返回 |
| `guarantee_end_date` | string/date | 担保截止日期；默认返回 |
| `is_shareholder_meeting_reviewed` | string | 是否经股东大会审议；默认返回 |
| `shareholder_meeting_resolution_date` | string/date | 股东大会决议公告日；默认返回 |
| `is_related_party_guarantee` | string | 是否为关联方担保；默认返回 |
| `total_external_guarantee_amount` | number | 公司及控股子公司对外担保总额；默认返回 |
| `announcement_internal_code` | string | 公告内部编码 |
| `market_code` | string | 市场编码；默认返回 |
| `market_name` | string | 市场名称；默认返回 |
| `remark` | string | 备注 |

## related_party_trade — 公司日常关联交易

`GET /api/v1/data/related_party_trade`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000008` |
| `market_code` | 否 | 交易市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板 |
| `announcement_date` | 否 | 公告日期；操作符：between（逗号分隔两个边界） | string/date-time |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `company_name` | string | 公司名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `announcement_internal_code` | string | 公告内部编码 |
| `announcement_date` | string/date-time | 公告日期；默认返回 |
| `related_transaction_type` | string | 关联交易类别；默认返回 |
| `related_party_name` | string | 关联方名称；默认返回 |
| `contract_amount_or_estimated_amount` | number | 合同签订金额或预计金额；默认返回 |
| `related_transaction_year` | number | 关联交易年度；默认返回 |
| `is_adjusted_announcement` | string | 是否调整公告；默认返回 |
| `remark` | string | 备注 |
