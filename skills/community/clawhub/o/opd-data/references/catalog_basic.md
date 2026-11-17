# 基本信息 — 6 个接口

> 本文件由 `tools/generate_catalog.py` 从 OpenAPI 规范自动生成，请勿手工编辑。

## co_info — 公司基本信息

`GET /api/v1/data/co_info`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `market_code` | 否 | 市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `est_date` | 否 | 成立日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `listing_status_code` | 否 | 上市状态编码 | string | 013001=正常上市；013004=ST；013005=*ST；013006=已发行未上市；013008=未过会；013009=发行失败；013011=暂缓发行 |
| `province` | 否 | 所属省份 | string | `广东` |
| `city` | 否 | 所属城市 | string | `深圳市` |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `market_code` | string | 市场编码；默认返回 |
| `en_name` | string | 英文名称；默认返回 |
| `en_short_name` | string | 英文简称；默认返回 |
| `legal_rep` | string | 法人代表；默认返回 |
| `reg_address` | string | 注册地址 |
| `office_address` | string | 办公地址 |
| `zip_code` | string | 邮政编码；默认返回 |
| `reg_capital` | number | 注册资金；默认返回 |
| `currency_code` | string | 货币编码；默认返回 |
| `currency_name` | string | 货币名称；默认返回 |
| `est_date` | string/date | 成立日期；默认返回 |
| `website` | string | 机构网址 |
| `email` | string | 电子信箱；默认返回 |
| `phone` | string | 联系电话；默认返回 |
| `fax` | string | 联系传真；默认返回 |
| `main_business` | string | 主营业务；默认返回 |
| `business_scope` | string | 经营范围 |
| `profile` | string | 机构简介/公司成立概况 |
| `board_secretary` | string | 董事会秘书；默认返回 |
| `secretary_phone` | string | 董秘联系电话；默认返回 |
| `secretary_fax` | string | 董秘联系传真；默认返回 |
| `secretary_email` | string | 董秘电子邮箱；默认返回 |
| `sec_rep` | string | 证券事务代表；默认返回 |
| `listing_status_code` | string | 上市状态编码；默认返回 |
| `listing_status` | string | 上市状态；默认返回 |
| `province_code` | string | 所属省份编码；默认返回 |
| `province` | string | 所属省份；默认返回 |
| `city_code` | string | 所属城市编码；默认返回 |
| `city` | string | 所属城市；默认返回 |
| `csrc_ind_l1_code` | string | 证监会一级行业编码；默认返回 |
| `csrc_ind_l1_name` | string | 证监会一级行业名称；默认返回 |
| `csrc_ind_l2_code` | string | 证监会二级行业编码；默认返回 |
| `csrc_ind_l2_name` | string | 证监会二级行业名称；默认返回 |
| `sw_ind_l1_code` | string | 申万行业分类一级编码；默认返回 |
| `sw_ind_l1_name` | string | 申万行业分类一级名称；默认返回 |
| `sw_ind_l2_code` | string | 申万行业分类二级编码；默认返回 |
| `sw_ind_l2_name` | string | 申万行业分类二级名称；默认返回 |
| `sw_ind_l3_code` | string | 申万行业分类三级编码；默认返回 |
| `sw_ind_l3_name` | string | 申万行业分类三级名称；默认返回 |
| `accounting_firm` | string | 会计师事务所；默认返回 |
| `law_firm` | string | 律师事务所；默认返回 |
| `chairman` | string | 董事长；默认返回 |
| `general_manager` | string | 总经理；默认返回 |
| `indep_director` | string | 公司独立董事(现任)；默认返回 |
| `index_list` | string | 入选指数 |
| `report_appointment_date` | string | 最新报告预约日期；默认返回 |
| `sponsor` | string | 保荐机构；默认返回 |
| `lead_underwriter` | string | 主承销商；默认返回 |
| `remark` | string | 备注 |
| `country` | string | 注册国家；默认返回 |
| `credit_code` | string | 统一社会信用代码；默认返回 |
| `convertible_bond` | string | 可转债；默认返回 |
| `cdr` | string | CDR；默认返回 |
| `company_scale` | string | 企业规模；默认返回 |

## industry_chg — 公司行业归属的变动

`GET /api/v1/data/industry_chg`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `change_date` | 否 | 变更日期；操作符：between（逗号分隔两个边界） | string/date |  |
| `std_code` | 否 | 分类标准编码 | string | 008001=中国上市公司协会上市公司行业分类标准；008002=巨潮行业分类标准；008003=申银万国行业分类标准；008004=新财富行业分类标准；008008=全球行业分类标准（GICS）；008009=证监会行业分类标准（2001）；008013=巨潮行业分类标准(旧)；008014=中证行业分类标准；008016=恒生行业分类；008018=申银万国行业分类标准(旧)；008019=中证行业分类标准(旧)；008021=证监会行业分类标准（2012） |
| `ind_gate` | 否 | 行业门类 | string | `信息技术` |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `change_date` | string/date | 变更日期；默认返回 |
| `std_code` | string | 分类标准编码；默认返回 |
| `std_name` | string | 分类标准；默认返回 |
| `ind_code` | string | 行业编码；默认返回 |
| `ind_gate` | string | 行业门类；默认返回 |
| `ind_subclass` | string | 行业次类；默认返回 |
| `ind_major` | string | 行业大类；默认返回 |
| `ind_medium` | string | 行业中类；默认返回 |
| `is_latest` | string | 最新记录标识；默认返回 |
| `remark` | string | 备注 |

## security_info — 证券信息

`GET /api/v1/data/security_info`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `market_code` | 否 | 交易市场编码 | string | 012001=上交所；012002=深交所主板；012015=深交所创业板；012029=上交所科创板；012046=北交所 |
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |
| `sec_category_code` | 否 | 证券类别编码 | string | 001001=A股；001002=B股；001013=CDR；002001=国债；002002=政策性金融债；002003=央行票据；002005=企业债；002006=可转债；002007=一般金融债；002008=资产支持证券；002009=买断式回购；002010=质押式回购；002011=次级债；002012=短期融资券；002013=国际机构债券；002015=可分离可转债；002018=公司债；002019=集合债券；002020=中期票据；002021=地方政府债；002022=集合票据；002025=非银行金融债；002027=政府支持机构债券；002028=私募债；002029=小微企业扶持债；002030=可交换私募债；002033=可交换债；002034=外国主权政府人民币债券；002035=超短期融资债券；002036=项目收益票据；002037=资产支持票据；003001=封闭式基金；003003=LOF；003004=ETF；003012=不动产基金 |
| `list_date` | 否 | 上市日期；操作符：between（逗号分隔两个边界） | string/date |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `sec_type_id` | string | 证券大类编码；默认返回 |
| `sec_type_name` | string | 证券大类；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `credit_code` | string | 统一社会信用代码；默认返回 |
| `isin_code` | string | ISIN码；默认返回 |
| `sec_category_code` | string | 证券类别编码；默认返回 |
| `sec_category` | string | 证券类别；默认返回 |
| `market_code` | string | 交易市场编码；默认返回 |
| `market_name` | string | 交易市场；默认返回 |
| `currency_code` | string | 交易货币编码；默认返回 |
| `currency_name` | string | 交易货币；默认返回 |
| `list_date` | string/date | 上市日期；默认返回 |
| `delist_date` | string/date | 终止上市日期（到期日）；默认返回 |
| `pinyin_short_name` | string | 拼音简称；默认返回 |
| `en_short_name` | string | 英文简称；默认返回 |
| `remark` | string | 备注 |

## sector — 股票所属板块

`GET /api/v1/data/sector`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `std_code` | 否 | 分类标准编码 | string | 137001=市场分类；137002=中上协行业分类；137003=巨潮行业分类；137004=申银万国行业分类；137005=新财富行业分类；137006=地区省市分类；137007=指数成份股；137008=概念板块；137098=证监会行业分类（2001） |
| `sec_code` | 否 | 证券代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001.sz` |
| `sector_l1_name` | 否 | 板块一类名称 | string | `深市A股` |
| `sector_l2_name` | 否 | 板块二类名称 | string | `深市创业板` |
| `eff_date` | 否 | 生效日期；操作符：between（逗号分隔两个边界） | string/date-time |  |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `org_name` | string | 机构名称；默认返回 |
| `std_code` | string | 分类标准编码；默认返回 |
| `std_name` | string | 分类标准；默认返回 |
| `sec_code` | string | 证券代码；默认返回 |
| `sec_name` | string | 证券简称；默认返回 |
| `sector_code` | string | 板块编码；默认返回 |
| `sector_l1_name` | string | 板块一类名称；默认返回 |
| `sector_l1_code` | string | 板块一类编码；默认返回 |
| `sector_l2_name` | string | 板块二类名称；默认返回 |
| `sector_l2_code` | string | 板块二类编码；默认返回 |
| `sector_l3_name` | string | 板块三类名称；默认返回 |
| `sector_l3_code` | string | 板块三类编码；默认返回 |
| `sector_l4_name` | string | 板块四类名称；默认返回 |
| `sector_l4_code` | string | 板块四类编码；默认返回 |
| `sector_l5_name` | string | 板块五类名称；默认返回 |
| `sector_l5_code` | string | 板块五类编码；默认返回 |
| `eff_date` | string/date-time | 生效日期；默认返回 |
| `remark` | string | 备注 |

## background — 股票背景资料

`GET /api/v1/data/background`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `sec_code` | 是 | 股票代码；操作符：in（逗号拆分多值（如 2024-01-01,2024-01-02）） | string | `000001` |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `sec_name` | string | 股票简称；默认返回 |
| `sec_code` | string | 股票代码；默认返回 |
| `background` | string | 背景资料 |
| `market_data` | string | 行情信息 |
| `remark` | string | 备注 |

## intermediary — 中介机构

`GET /api/v1/data/intermediary`

> 数据为深交所镜像数据，更新频率为实时更新，节假日除外
> **调用说明**：版本：1.0；调用限频：每分钟 60 次；单次最大记录数：1000
> **鉴权**：请求头 `X-API-Key: opd_xxx`；需已订阅该接口，否则返回 BIZ_INTERFACE_FORBIDDEN。

**过滤参数**（`fields` 必填、`limit`/`offset` 分页为统一参数，见 SKILL.md）

| 参数 | 必填 | 说明 | 类型 | 示例 / 可选值 |
|---|---|---|---|---|
| `change_date` | 否 | 变更日期；操作符：between（逗号分隔两个边界） | string/date-time |  |
| `intermediary_type_code` | 否 | 中介机构类别编码 | string | 016001=境内会计师事务所；016002=境外会计师事务所；016003=律师事务所；016004=主办券商；016005=副主办券商 |

**返回字段**（`fields` 参数可选值；标注"默认返回"的字段在未指定时也会返回）

| 字段 | 类型 | 说明 |
|---|---|---|
| `company_name` | string | 公司名称；默认返回 |
| `change_date` | string/date-time | 变更日期；默认返回 |
| `intermediary_type_code` | string | 中介机构类别编码；默认返回 |
| `intermediary_type` | string | 中介机构类别；默认返回 |
| `intermediary_name` | string | 中介机构名称；默认返回 |
| `remark` | string | 备注 |
