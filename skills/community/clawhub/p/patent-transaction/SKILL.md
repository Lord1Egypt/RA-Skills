---
name: patent-transaction
description: Patent marketplace via trade.9235.net (listings, deals, open license, procurement, Excel export).
version: 1.0.0
metadata:
  openclaw:
    emoji: "🏪"
    homepage: https://trade.9235.net
    primaryEnv: TRADE_API_TOKEN
    requires:
      env:
        - TRADE_API_TOKEN
      bins:
        - python3
    envVars:
      - name: TRADE_API_TOKEN
        required: true
        description: Trade skill API token for https://trade.9235.net/api/skill
      - name: TRADE_API_BASE_URL
        required: false
        description: Optional trade API base URL override
    install:
      - kind: uv
        package: requests
---

# 专利交易 · Patent Transaction

## 概述 | Overview

| | |
|---|---|
| **中文** | 对接 `https://trade.9235.net/api/skill`：在售专利、详情、卖家、成交、开放许可、采购需求、Excel 导出。与 **patent-search** 联用做尽调。 |
| **English** | Trade skill API for patent listings, sellers, deal history, open licensing, procurement, Excel export. Pair with **patent-search** for due diligence. |

**凭证 Credentials**: `TRADE_API_TOKEN` 或 `skills.entries.patent-transaction.apiKey`

触发词：专利交易、转让、许可、在售专利、开放许可、采购需求、patent listing、licensing。

---

## 工具命令

| command | 说明 |
|---------|------|
| `search` | 在售专利搜索（表格展示） |
| `export` | 导出当前检索结果为 **Excel** 下载 |
| `export_orders` | 导出成交记录 Excel |
| `detail` / `sellers` / `orders` / `open` / `demand` | 详情与其它查询 |

## 配置

```json
{
  "api_base_url": "https://trade.9235.net/api/skill",
  "token": "YOUR_TRADE_SKILL_TOKEN"
}
```

或环境变量：

```bash
export TRADE_API_TOKEN="your_token"
export TRADE_API_BASE_URL="https://trade.9235.net/api/skill"
```

### 获取 Token

1. 运维设置 `TRADE_SKILL_TOKENS`
2. 或 `go run scripts/gen_skill_token.go -client mchat`

备用：无 token 时可设 `TRADE_API_BASE_URL=https://trade.9235.net/nbapi`

## CLI

```bash
python3 main.py search 锂电池
python3 main.py detail CN112968234A
python3 main.py orders
python3 main.py open 石墨烯
python3 main.py demand 电池
python3 main.py info
```

## API 端点

| 功能 | 路径 |
|------|------|
| 在售搜索 | `GET /api/skill/product/search?keyWord=&page=&pageSize=` |
| 交易详情 | `GET /api/skill/product/detail/{an}` |
| 卖家 | `GET /api/skill/product/sellers/{an}` |
| 成交记录 | `GET /api/skill/orders` |
| 成交详情 | `GET /api/skill/order/detail/{an}` |
| 开放许可 | `GET /api/skill/openPatent/search` |
| 采购需求 | `GET /api/skill/demand/search` |

所有请求需 `t=<token>&v=1` 或头 `X-Token`。

## 与 patent-search 协作

尽调流程：

1. `patent-search` 查法律状态、权利要求、相似专利
2. `patent-transaction` 查是否挂牌、价格、成交记录
3. 输出尽调摘要（见 [due-diligence.md](due-diligence.md)）

## 错误码

| code | 含义 |
|------|------|
| 201 | token 为空 |
| 202 | 非法 token |
| 209 | 版本号 v 缺失 |
| 203 | 服务异常 |
