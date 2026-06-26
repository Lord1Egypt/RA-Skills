# Current Availability

## Market Module Capability Status

| Capability | Status | Notes |
|---|---|---|
| Snapshot / Latest Quote | Ready | 已验证，可用于港股 / 美股快照查询 |
| Market State | Ready | 已验证，可返回市场状态文本 |
| Intraday | Ready | 已验证，支持 detail mode，默认最多展示最近 10 条 |
| Kline | Ready | 已验证 `get_cur_kline` 与 `get_cur_kline_date` 主路径可用；detail mode 已支持 |
| Capital Flow | Ready | 已验证，支持 detail mode；尾部 0 值占位记录已处理 |
| Basic Info | Ready | 已验证，可返回上市日期、每手股数、退市状态等 |
| CN Name Parsing | Partial | 已支持部分常见名称和歧义澄清；目前仍以本地映射为主，未接入正式搜索接口 |
| HK / US Ambiguity Clarification | Ready | 已支持阿里巴巴、百度、京东、哔哩哔哩、蔚来、小鹏、理想等双市场名称澄清 |
| IPO List | Ready | 已验证 `/quote/get_ipo_list` 可用 |
| Rank | Ready | 已按 `references/enum.yaml#/QuoteSortField` 严格取枚举值验证通过 |
| Finance HK / US | Ready | 已验证 `/infos/get_finance_hk_infos` 与 `/infos/get_finance_us_infos` 可用；调用时需使用 `DateTypeConvertUtil` 的 `x-enum-varnames`（如 `DT4`） |
| Shareholder Inc/Red Hold | Ready | 已验证 `/infos/shareholder_inc_red_hold` 与 `/infos/shareholder_inc_red_hold_by_ucode` 可用；调用时需使用 `ShareholderRedHoldEnum` 的 `x-enum-varnames`（如 `EVENT_DATE`） |
| Wealth Balance List | Routed | 已接入 `/wealth/balance_list`，等待统一联调验证 |
| Wealth Cash Total Asset | Routed | 已接入 `/wealth/cash_total_asset`，等待统一联调验证 |
| Wealth Fixed Income | Routed | 已接入 `/wealth/fixed_income`，等待统一联调验证 |
| Wealth Private Contract Asset List | Routed | 已接入 `/wealth/query_private_contract_asset_list`，等待统一联调验证 |
| Wealth Total Asset | Routed | 已接入 `/wealth/total_asset`，等待统一联调验证 |

## Notes

- `Ready`：当前环境已验证可用。
- `Partial`：已有部分能力，但仍受当前环境、标的或名称解析策略限制。
- `Unsupported in current env`：接口存在，但当前环境未正式开放或直接返回错误。

## Product Rules Already Applied

当前 market 模块已落地的产品规则包括：
- 默认优先摘要输出，不直接倾倒原始 JSON
- 用户要求“最近几条 / 明细 / 逐条”时进入 detail mode
- detail mode 默认最多展示最近 10 条记录
- 中文名称存在港股 / 美股歧义时先澄清，不默认猜测
- 资金流向尾部全 0 占位记录会自动忽略

## Related Files

- `references/edge-cases.md`
- `references/known-limitations.md`
- `references/usage-guide.md`
