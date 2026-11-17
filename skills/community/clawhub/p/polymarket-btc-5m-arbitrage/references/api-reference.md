# Polymarket API 只读参考

本 skill 只使用公开的 GET 接口。它不会调用 POST、PUT、PATCH 或 DELETE，也不需要钱包或交易凭据。

## Base URLs

    Gamma API: https://gamma-api.polymarket.com
    CLOB API:  https://clob.polymarket.com

## Gamma API

获取活跃市场：

    GET /markets?active=true&closed=false&limit=100

脚本读取的主要字段：

- id
- question
- slug
- clobTokenIds
- outcomes
- liquidity
- endDate

## CLOB API

获取某个 token 的订单簿：

    GET /book?tokenId={token_id}

读取价格或中间价时可使用：

    GET /price?tokenId={token_id}
    GET /midpoint?tokenId={token_id}

订单簿响应的 bids 和 asks 只用于展示与候选筛选：

    {
      "bids": [{"price": "0.50", "size": "100"}],
      "asks": [{"price": "0.51", "size": "50"}]
    }

## BTC 5分钟市场

- 系列：btc-up-or-down-5m
- 结果：Up 或 Down
- 分辨率：Chainlink BTC/USD

市场 slug 和返回字段可能随平台版本变化。脚本只在返回数据中确认 BTC/5m/updown 相关标识后再处理，不会猜测 token ID。

## 禁止范围

以下接口不属于本 skill 的权限范围：

- 任何下单、撤单、授权、转账或支付接口
- 任何第三方计费接口
