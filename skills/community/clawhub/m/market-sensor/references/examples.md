# 使用示例

## 示例 1：完整分析流程

用户说：「帮我看看英伟达现在什么情况」

```bash
# 1. 先查状态
curl -s -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  https://api.marketsensor.ai/api/open/analysis/status/NVDA

# 返回: { "status": "none" }

# 2. 触发分析
curl -s -X POST -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "NVDA"}' \
  https://api.marketsensor.ai/api/open/analyze

# 返回: { "status": "generating" }

# 3. 等待 30s 后轮询状态
sleep 30
curl -s -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  https://api.marketsensor.ai/api/open/analysis/status/NVDA

# 返回: { "status": "completed", "reportId": "abc123" }

# 4. 获取报告
curl -s -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  https://api.marketsensor.ai/api/open/report/abc123
```

## 示例 2：管理自选列表

```bash
# 查看当前自选
curl -s -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  https://api.marketsensor.ai/api/open/watchlist

# 添加美股
curl -s -X POST -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL"}' \
  https://api.marketsensor.ai/api/open/watchlist

# 添加 A 股（茅台）
curl -s -X POST -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "600519"}' \
  https://api.marketsensor.ai/api/open/watchlist

# 添加加密货币
curl -s -X POST -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "BTCUSD"}' \
  https://api.marketsensor.ai/api/open/watchlist

# 移除
curl -s -X POST -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL"}' \
  https://api.marketsensor.ai/api/open/watchlist/remove
```

## 示例 3：盘中分析（Intraday）

```bash
# 盘中触发实时分析
curl -s -X POST -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "TSLA", "mode": "intraday"}' \
  https://api.marketsensor.ai/api/open/analyze
```

## 示例 4：额度管理

```bash
# 查看剩余额度
curl -s -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  https://api.marketsensor.ai/api/open/quota

# 返回:
# {
#   "short": { "remaining": 3, "total": 10 },
#   "intraday": { "remaining": 5, "total": 5 }
# }
```

## 示例 5：JSON 格式报告

```bash
# 获取 JSON 格式（适合程序处理）
curl -s -H "Authorization: Bearer $MARKETSENSOR_API_KEY" \
  "https://api.marketsensor.ai/api/open/report/abc123?format=json"
```
