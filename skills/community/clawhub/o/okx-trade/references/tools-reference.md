# OKX Agent Trade Kit — 完整 Tools 參考

共 8 個 module，121 個 tools（以官方 GitHub 為準）。

## market — 行情數據（唔需要 API Key）

| Tool | 說明 |
|------|------|
| `market_get_ticker` | 單個合約 ticker（最新價、24h 量、bid/ask） |
| `market_get_tickers` | 某類型所有 ticker（SPOT/SWAP/FUTURES/OPTION） |
| `market_get_orderbook` | 訂單簿深度 |
| `market_get_candles` | K 線（最近 300 根） |
| `market_get_history_candles` | 歷史 K 線（2 天前，最多 3 個月） |
| `market_get_funding_rate` | 永續合約資金費率 |
| `market_get_funding_rate_history` | 歷史資金費率 |
| `market_get_mark_price` | 標記價格 |
| `market_get_open_interest` | 未平倉量 |
| `market_get_trades` | 最近成交記錄 |

## spot — 現貨交易

| Tool | 說明 |
|------|------|
| `spot_place_order` | 下現貨訂單（market/limit/post-only/FOK/IOC） |
| `spot_cancel_order` | 撤單 |
| `spot_amend_order` | 改價/改量 |
| `spot_batch_place_orders` | 批量下單（最多 20 筆） |
| `spot_batch_cancel_orders` | 批量撤單 |
| `spot_get_order` | 查詢單筆訂單 |
| `spot_get_open_orders` | 當前掛單列表 |
| `spot_get_order_history` | 歷史訂單（7 天內） |
| `spot_get_fills` | 成交記錄 |

## swap — 永續合約

| Tool | 說明 |
|------|------|
| `swap_place_order` | 下永續合約訂單 |
| `swap_cancel_order` | 撤單 |
| `swap_close_position` | 一鍵平倉 |
| `swap_get_positions` | 當前持倉 |
| `swap_set_leverage` | 設置槓桿 |
| `swap_get_leverage` | 查詢當前槓桿 |

## futures — 交割合約

| Tool | 說明 |
|------|------|
| `futures_place_order` | 下交割合約訂單 |
| `futures_get_positions` | 持倉查詢 |

## option — 期權

| Tool | 說明 |
|------|------|
| `option_place_order` | 下期權訂單（買/賣 call/put） |
| `option_get_instruments` | 期權鏈 |
| `option_get_greeks` | IV 同 Greeks（delta/gamma/theta/vega） |
| `option_get_positions` | 持倉（含 Greeks） |

## account — 帳戶管理

| Tool | 說明 |
|------|------|
| `account_get_balance` | 交易帳戶餘額 |
| `account_get_asset_balance` | 資金帳戶餘額 |
| `account_get_positions` | 全帳戶持倉 |
| `account_get_bills` | 帳單/流水（7 天） |
| `account_get_fee_rates` | 手續費率 |
| `account_set_leverage` | 設置槓桿 |

## bot — 交易機器人

### Grid Bot
| Tool | 說明 |
|------|------|
| `grid_create_order` | 建立 Grid Bot（現貨/合約/Moon Grid） |
| `grid_stop_order` | 停止 Grid Bot |
| `grid_get_orders` | 查看 Grid Bot 列表 |

### DCA Bot
| Tool | 說明 |
|------|------|
| `dca_create_order` | 建立 DCA（馬丁格爾）策略 |
| `dca_stop_order` | 停止 DCA 策略 |
| `dca_get_orders` | 查看 DCA 策略列表 |

---

最新完整列表：https://github.com/okx/agent-trade-kit
