---
name: china-ifind
description: |
  同花顺 iFinD (51ifind.com) 金融数据查询。支持 A 股/基金/债券/期货/指数的实时行情、历史行情、财务指标、宏观经济数据等 18 个 API 接口。
  Chinese financial data query skill powered by THS iFinD (51ifind.com) API. Covers real-time quotes, historical data, financial indicators, macro economics, fund valuation, and more across 18 API endpoints for A-shares, funds, bonds, futures, and indices.
metadata:
  author: sinabs
  version: "1.0.0"
  openclaw:
    requires:
      env:
        - IFIND_REFRESH_TOKEN
---

# iFinD 金融数据查询

基于同花顺 iFinD ([51ifind.com](https://www.51ifind.com)) 量化数据接口，覆盖 A 股、基金、债券、期货、指数等全品类金融数据。

## 运行机制

1. **Token 获取**：使用用户提供的 `IFIND_REFRESH_TOKEN` 向 iFinD 官方 API 获取 `access_token`，缓存在本地 `.data/access_token`（24 小时 TTL）。
2. **API 调用**：携带 `access_token` 调用 `quantapi.51ifind.com` 量化数据接口，返回 JSON 结果。
3. **自动重试**：当 token 过期（errorcode -1302）时自动刷新并重试一次。
4. **日志**：调用记录写入 `.data/ifind.log`（滚动日志，1MB 上限）。

本脚本仅与 iFinD 官方 API（`quantapi.51ifind.com`）通信，不连接任何第三方服务。

## 支持的 API

| # | API | Endpoint | 用途 |
|---|-----|----------|------|
| 1 | 基础数据 | `basic_data_service` | 财务指标、基本面数据 |
| 2 | 日期序列 | `date_sequence` | 按时间序列获取指标数据 |
| 3 | 历史行情 | `cmd_history_quotation` | 日K/周K等历史行情 |
| 4 | 高频序列 | `high_frequency` | 分钟级高频数据 + 技术指标 |
| 5 | 实时行情 | `real_time_quotation` | 最新价、涨跌幅、成交量 |
| 6 | 日内快照 | `snap_shot` | 逐笔/分钟级日内盘口快照 |
| 7 | 经济数据库 | `edb_service` | 宏观经济指标 (GDP、CPI 等) |
| 8 | 专题报表 | `data_pool` | REITs、龙虎榜等专题数据 |
| 9 | 组合管理 | `portfolio_manage` | 组合新建/导入/交易/监控 |
| 10 | 智能选股 | `smart_stock_picking` | 按条件筛选股票 |
| 11 | 基金估值(分钟) | `fund_valuation` | 基金实时分钟级估值 |
| 12 | 基金估值(日) | `final_fund_valuation` | 基金日终估值 |
| 13 | 日期查询 | `get_trade_dates` | 查询交易日历 |
| 14 | 日期偏移 | `get_trade_dates` | 基于基准日前推/后推 |
| 15 | 数据量查询 | `get_data_volume` | 查询账号已用数据量 |
| 16 | 错误信息查询 | `get_error_message` | 查询错误码含义 |
| 17 | 代码转换 | `get_thscode` | 证券代码转同花顺代码 |
| 18 | 公告查询 | `report_query` | 上市公司公告检索下载 |

## 首次使用

每次调用 API 前，先按 [API_REFERENCE.md](references/API_REFERENCE.md) 中「Token 配置」章节检查并配置 `IFIND_REFRESH_TOKEN`。

如果未配置，**停止执行**，向用户提示：

> 使用 iFinD 金融数据查询需要你的 refresh_token。获取方式：
> - **还没有账号**：访问 https://ft.10jqka.com.cn 申请 iFinD 量化数据终端
> - **已有账号**：打开 iFinD 超级命令客户端 → 工具 → refresh_token 查询；或登录 https://quantapi.51ifind.com 在账号信息中查看
>
> 请把你的 refresh_token 发给我，我帮你配置好。

## 参考资料

- [API_REFERENCE.md](references/API_REFERENCE.md) - Token 配置、调用方式、18 个 API 完整参数和示例
