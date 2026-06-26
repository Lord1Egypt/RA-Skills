# Virtual Trading MCP API リファレンス

virtual-trading MCP で利用可能なツール群。実際のツール名は MCP 接続時に確認すること。

## 主要ツール

| ツール名 | 用途 |
|----------|------|
| `get_portfolio` | 保有資産一覧 (銘柄, 数量, 平均取得価格) |
| `get_prices` | 資産の現在価格一覧 |
| `get_balance` | 現金残高 |
| `place_order` | 買い/売り注文の発行 |
| `query_metrics` | PromQL でメトリクス時系列取得 |

## PromQL で価格トレンドを取得する例

7 日間の高値/安値を取得する PromQL:

```promql
# 過去 7 日の高値
max_over_time(asset_price{asset="BTC"}[7d])

# 過去 7 日の安値
min_over_time(asset_price{asset="BTC"}[7d])

# 現在価格
asset_price{asset="BTC"}
```

`query_metrics` ツールに上記クエリを渡し、レスポンスの value を使う。

## place_order パラメータ例

```json
{
  "asset": "BTC",
  "side": "buy",
  "quantity": 0.01,
  "order_type": "market"
}
```

- `side`: `"buy"` または `"sell"`
- `quantity`: 数量（通貨・株式の単位）
- `order_type`: `"market"` (成行) / `"limit"` (指値)

## エラー対処

- 残高不足: `get_balance` で現金を確認し、注文数量を調整する
- 保有不足（売り): `get_portfolio` で数量を確認し、保有量以下にする
- ツール名が合わない: MCP ツール一覧を `list_tools` 等で確認する
