# 场外指数基金信息查询 — 接口字段权威参考

> 编写脚本前必读：数据路径、字段名、单位均以本文件为准。
>
> 说明：
> - 本文所有路径都是 JSON 路径。
> - `$` 表示返回 JSON 的根节点。
> - 默认按 catalog 中的路径取值；只有路径失败、字段缺失或结构可疑时，才先查看真实响应结构再继续。
> - 如果按 catalog 取值失败，不要跨接口猜路径。必须先请求该接口，检查根节点有哪些 key、`data` 是对象/数组/空值，以及列表真实位于哪一层。

---

## 公共请求头

所有接口请求均需携带以下请求头：

```
# 认证格式：Authorization: Bearer <API_KEY>
# 请求来源标识：X-Caller-Type: external
```

---

## `POST /skill/v1/search/oef` — 关键词搜索场外基金

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 是 | 支持基金名称、代码模糊搜索 |
| page | integer | 否 | 页码，从1开始，默认1 |
| pageSize | integer | 否 | 每页条数，建议10-100，默认10 |

**最终数据路径**：`$.data.data[]`（⚠️ 不是 `$.data.list[]`）

| 字段 | 类型 | 说明 |
|------|------|------|
| fundCode | string | 场外基金代码，6位数字 |
| fundName | string | 产品名称（全称） |
| fundSht | string | 产品简称 |
| indexCode | string | 跟踪指数代码（不带后缀） |
| indexName | string | 跟踪指数名称 |
| indexType | string | 跟踪指数类型 |
| pubDt | string | 净值数据发布日期，yyyy-MM-dd |
| unitNav | number | 单位净值（元） |
| fundScale | number | 基金规模（**元**，÷1e8=亿）⚠️ 与 oef/detail 的 rptFundScale 同单位同值 |
| navPctChg1D | number | 日涨跌幅（%） |
| eodPctChg1W/1M/3M/TY/1Y/3Y/5Y | number | 各周期涨跌幅（%） |
| excessReturn1Y | number | 近1年超额收益（%） |
| unitAccBonus | number | 单位累计分红（元） |
| accBonusCount | integer | 累计分红次数（次） |
| currBonusDt | string | 最近分红权益登记日，yyyy-MM-dd |
| dividendYield | number | 指数股息率（%） |
| PETtm | number | PE-TTM（倍）⚠️ 注意大小写 |
| PETtm5Y | number | PE近5年分位（%） |
| PBLf | number | PB-LF（倍）⚠️ 注意大小写 |
| PBLf5Y | number | PB近5年分位（%） |
| PSTtm | number | PS-TTM（倍）⚠️ 注意大小写 |
| PSTtm5Y | number | PS近5年分位（%） |
| fundManageComp | string | 基金管理人 |
| fundManagerCurrent | array | 基金经理信息 |
| establishDt | string | 成立日，yyyy-MM-dd |
| mgtFee | number | 管理费（%） |
| trstFee | number | 托管费（%） |
| salesServiceFee | number | 销售服务费（%）（注意：search/oef 是 `salesServiceFee`，oef/detail 是 `saleServiceFee`） |
| relatedETF | array | 相关ETF产品信息 |
| maxDown1W/1M/3M/6M/1Y/3Y/5Y/10Y/TY/Bgn | number | 各周期最大回撤（%） |

`relatedETF[]` 内字段：
| 字段 | 类型 | 说明 |
|------|------|------|
| fundCode | string | 相关ETF代码 |
| relatedETFCode | string | 相关ETF代码 |
| relatedETFSht | string | 相关ETF简称 |

> 跟踪误差读取规则：`search/oef` 不提供年化跟踪误差；需要跟踪误差时请求 `oef/detail`，读取 `annTrackError1Y`。

**分页信息路径**：`$.data.totalNum`、`$.data.pageNum`、`$.data.pageSize`

---

## `POST /skill/v1/oef/detail` — 批量场外基金详情

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| fundCodes | array | 是 | 场外基金代码列表，最多10个 |

**最终数据路径**：`$.data[]`（数组，每个元素对应一只基金）

外层字段：
| 字段 | 类型 | 说明 |
|------|------|------|
| fundCode | string | 基金代码 |
| availabilityStatus | string | 有数据/未找到该基金/代码类型不匹配/查询失败 |
| detail | object | 详情对象，仅 availabilityStatus="有数据" 时存在 |

`detail{}` 内字段：
| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | 交易代码 |
| fundName | string | 基金展示名（短产品名，OEF对外展示优先使用此字段） |
| chiName | string | 基金全称（法律全称） |
| indexCode | string | 标的指数代码 |
| indexName | string | 指数名称 |
| indexSht | string | 指数简称 |
| firstClass | string | 指数一级分类 |
| secondClass | string | 指数二级分类 |
| establishDt | string | 成立日，yyyy-MM-dd |
| mgtFee | number | 管理费（%） |
| trstFee | number | 托管费（%） |
| saleServiceFee | number | 销售服务费（%） |
| fundManageComp | string | 基金管理人全称 |
| fundManageSht | string | 基金管理人简称 |
| rptDt | string | 报告日期 |
| rptFundScale | number | 产品规模（报告日期）（**元**，÷1e8=亿） |
| unitNav | number | 单位净值（元） |
| accuUnitNav | number | 累计单位净值（元） |
| navPctChg1D | number | 日涨跌幅（%） |
| navPctChg1W/1M/3M/6M/1Y/3Y/5Y/TY/Bgn | number | 各周期净值涨跌幅（%） |
| annTrackError1Y | number | 近1年年化跟踪误差（%） |
| excessReturn1Y | number | 近1年超额收益（%） |
| maxDown1Y/3Y/5Y/Bgn | number | 最大回撤（%） |
| riskLevel | string | 风险等级 |
| unitAccBonus | number | 单位累计分红（元） |
| accBonusCount | number | 累计分红次数（次） |
| currBonusDt | string | 最近分红日期（可能是 yyyy-MM-dd 或毫秒时间戳字符串） |
| fundManagerCurrent | array | 现任基金经理 |
| fundManagerFormer | array | 历任基金经理 |
| relatedETF | array | 相关ETF（底层ETF信息） |
| relatedShareFunds | array | 相关份额基金 |
| benchMark | string | 业绩比较基准 |

`relatedETF[]` 内字段：
| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | 底层ETF代码 |
| fundSht | string | 底层ETF简称 |
| fundType | string/null | 基金类型 |
| fundScale | number/null | 基金规模（元） |
| navPctChg1Y | number/null | 近1年涨跌幅（%） |
| navPctChg1D | number/null | 日涨跌幅（%） |

> 跟踪误差读取规则：年化跟踪误差读取 `annTrackError1Y`。

---

## `POST /skill/v1/oef/holdings` — 批量场外基金持仓

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| fundCodes | array | 是 | 场外基金代码列表，最多10个 |
| date | string | 否 | 持仓日期 yyyy-MM-dd，不传返回最新报告期 |

**最终数据路径**：`$.data[]`（数组）

外层字段：
| 字段 | 类型 | 说明 |
|------|------|------|
| fundCode | string | 基金代码 |
| availabilityStatus | string | 有数据/未找到该基金/代码类型不匹配/无持仓数据/查询失败 |
| holdingItems | array | 持仓明细，仅 availabilityStatus="有数据" 时存在 |

`holdingItems[]` 内字段：
| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | 基金交易代码 |
| endDt | string | 报告期截止日期，yyyy-MM-dd |
| stockCode | string | 股票代码（6位） |
| secuSht | string | 股票简称 |
| holdNavRat | number | 占净值比例（%） |
| sInfoWindcode | string | 基金Wind代码 |
| stockWindcode | string | 股票Wind代码 |

---

## `POST /skill/v1/oef/return` — 批量场外基金区间收益率

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| codes | array | 是 | 场外基金代码数组，最多10只 |
| timeMode | string | 是 | PERIOD（预设周期）或 RANGE（自定义区间） |
| period | string | PERIOD时必填 | 1D/1W/1M/3M/6M/1Y/3Y/5Y/10Y/TY（今年以来）/INCE（成立以来） |
| startDate | string | RANGE时必填 | yyyy-MM-dd |
| endDate | string | RANGE时必填 | yyyy-MM-dd |
| boundaryMatchMode | string | 否 | STRICT/FLEXIBLE（默认FLEXIBLE） |

**最终数据路径**：`$.data[]`（数组）

| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | 基金代码 |
| indexCode | string | 跟踪指数代码 |
| startDate | string | 实际区间开始日期 |
| endDate | string | 实际区间结束日期 |
| returnRate | number | 区间收益率（%）⚠️ 见下方说明 |
| availabilityStatus | string | 有数据/API接口无数据/历史查询无数据/不支持的期间/API调用异常/系统异常 |

> ⚠️ **returnRate 异常值处理**：
> - status≠有数据时，returnRate 字段**完全缺失**（非 null），必须用 `.get('returnRate')`
> - status=有数据 但 returnRate=-888.89 时，为 API 哨兵值，表示该基金历史不足以计算此周期，需过滤：`if returnRate is not None and returnRate > -100`

---

## `POST /skill/v1/oef/dividends` — 批量场外基金历史分红

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| fundCodes | array | 是 | 场外基金代码数组，最多10只 |
| startDate | string | 否 | 查询开始日期，不传从最早记录 |
| endDate | string | 否 | 查询结束日期，不传到最新记录 |

**最终数据路径**：`$.data[]`（数组）

外层字段：
| 字段 | 类型 | 说明 |
|------|------|------|
| fundCode | string | 基金代码 |
| availabilityStatus | string | 有数据/无历史分红/未找到该基金/代码类型不匹配/查询失败 |
| dividendItems | array | 分红明细，按分红时间倒序排列 |

`dividendItems[]` 内字段：
| 字段 | 类型 | 说明 |
|------|------|------|
| trdCode | string | 交易代码 |
| eqyRecordDt | string | 权益登记日，yyyy-MM-dd |
| dvdBenDt | string | 分红计算基准日，yyyy-MM-dd |
| cashDvdPerShTax | number | 每份分红金额（元） |
| payDt | string | 红利发放日（场内），场外基金此字段通常为 null |
| divPayDt | string | 红利发放日（场外），yyyy-MM-dd |

---

## 单位速查

| 字段 | 接口 | 单位 | 换算 |
|------|------|------|------|
| rptFundScale | oef/detail.detail | 元 | ÷1e8=亿 |
| fundScale | `$.data.data[]`（search/oef） | 元（与rptFundScale同值同单位） | ÷1e8=亿 |
| holdNavRat | oef/holdings.holdingItems[] | % | 直接展示 |
| cashDvdPerShTax | oef/dividends.dividendItems[] | 元/份 | 直接展示 |
| annTrackError1Y | oef/detail.detail | % | 直接展示；搜索接口没有该字段时先查 detail |

## 名称字段使用规则

| 接口 | 对外展示名 | 说明 |
|------|------------|------|
| oef/detail | `detail.fundName` | OEF detail 的 `fundName` 是短产品名，`chiName` 是法律全称 |
| search/oef | `$.data.data[].fundSht` 或 `fundName` | 搜索列表有 `fundSht`，样本中通常与 `fundName` 一致；如为空再使用 `fundName` |
| oef/detail.relatedETF | `relatedETF[].fundSht` | 底层 ETF 信息里的简称字段是 `fundSht` |

## 代码格式速查

| 场景 | 正确格式 | 常见错误 |
|------|----------|----------|
| 场外基金代码入参 | `006748`（6位数字） | `006748.OF`、`006748.SH`、`006748.SZ` |
| 批量场外基金代码 | `["006748", "110003"]` | 带 `.OF` 或交易所后缀 |

## 数据路径速查

| 接口 | 结果路径 | 常见错误 |
|------|---------|---------|
| search/oef | `$.data.data[]` | 误用 `$.data.list[]` |
| oef/detail | `$.data[]` → `[i].detail{}` | 忘记检查 availabilityStatus |
| oef/holdings | `$.data[]` → `[i].holdingItems[]` | 同上 |
| oef/return | `$.data[]` → `[i].returnRate` | status≠有数据时 returnRate 字段可能**缺失**，需用 `.get('returnRate')` |
| oef/dividends | `$.data[]` → `[i].dividendItems[]` | oef的 `payDt` 通常为 `null`，用 `divPayDt` |

## OEF vs ETF 关键差异

| 维度 | ETF (etf/detail) | OEF (oef/detail) |
|------|-----------------|-----------------|
| 规模字段名 | fundScale（元，÷1e8=亿） | rptFundScale（元，÷1e8=亿） |
| 规模报告日期字段 | 无 | rptDt |
| 销售服务费 | 无 | saleServiceFee |
| 溢折率/实时行情 | ETF skill 不展示实时行情字段 | 无（场外无溢折率） |
| 场内分红发放日 | payDt | payDt（通常null） |
| 场外分红发放日 | divPayDt | divPayDt |
| 上市日 | lstDt | 无 |
| 风险等级 | 无 | riskLevel |
