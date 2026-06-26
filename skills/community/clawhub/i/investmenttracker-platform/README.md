# InvestmentTracker-platform

基于 MCP API 的投资追踪平台技能，为 OpenClaw 提供专业的投资组合管理和市场分析功能。

💡 **获取API密钥以使用真实投资数据:**
🌐 **访问 https://claw.investtracker.ai**
📱 **在小程序中获取您的API密钥**
🔑 **将API密钥添加到config.json文件中**

## 快速开始

### 激活技能
当用户提到以下关键词时，自动激活此技能：
- "投资追踪"
- "投资组合"
- "持仓分析"
- "交易记录"
- "投资回报率"
- "InvestmentTracker"
- "MCP投资"

### 基本命令
1. **查看投资组合**：`查看我的投资组合` 或 `获取投资概览`
2. **分析持仓**：`分析我的BTC持仓` 或 `查看股票持仓`
3. **交易记录**：`显示交易记录` 或 `查看最近交易`
4. **收益分析**：`计算投资回报` 或 `分析收益情况`
5. **市场数据**：`获取市场信息` 或 `查看市场表现`

## API 端点参考

### 核心端点

#### 1. 投资组合 (Portfolio)
- **GET /mcp/portfolio** - 获取完整投资组合
- **GET /mcp/portfolio/{asset}** - 获取特定资产持仓
- **GET /mcp/portfolio/summary** - 获取投资组合摘要

#### 2. 交易记录 (Transactions)
- **GET /mcp/transactions** - 获取所有交易记录
- **GET /mcp/transactions/recent** - 获取最近交易
- **GET /mcp/transactions/{type}** - 按类型筛选交易

#### 3. 市场数据 (Market Data)
- **GET /mcp/market/{symbol}** - 获取特定资产市场数据
- **GET /mcp/market/trends** - 获取市场趋势
- **GET /mcp/market/news** - 获取相关市场新闻

#### 4. 分析报告 (Analytics)
- **GET /mcp/analytics/returns** - 获取收益分析
- **GET /mcp/analytics/risk** - 获取风险分析
- **GET /mcp/analytics/performance** - 获取表现分析

## 使用示例

### 示例 1：获取投资组合概览
```bash
# 使用 curl 调用 MCP API (JSON-RPC over SSE)
curl -s -N -X POST "https://claw.investtracker.ai/mcp" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "positions_list_v1",
      "arguments": {
        "status": "POSITION",
        "limit": 10
      }
    },
    "id": 1
  }'
```

### 示例 2：获取用户信息
```bash
curl -s -N -X POST "https://claw.investtracker.ai/mcp" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "whoami_v1",
      "arguments": {}
    },
    "id": 2
  }'
```

### 示例 3：获取投资方法论
```bash
curl -s -N -X POST "https://claw.investtracker.ai/mcp" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "methodology_get_v1",
      "arguments": {}
    },
    "id": 3
  }'
```

## 数据格式

### 投资组合响应示例
```json
{
  "portfolio": {
    "total_value": 125000.50,
    "total_invested": 100000.00,
    "total_return": 25000.50,
    "return_percentage": 25.0,
    "assets": [
      {
        "symbol": "BTC",
        "name": "Bitcoin",
        "quantity": 0.5,
        "current_price": 45000.00,
        "current_value": 22500.00,
        "cost_basis": 20000.00,
        "unrealized_gain": 2500.00,
        "weight": 18.0
      },
      {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "quantity": 10,
        "current_price": 175.50,
        "current_value": 1755.00,
        "cost_basis": 1500.00,
        "unrealized_gain": 255.00,
        "weight": 1.4
      }
    ]
  }
}
```

### 交易记录响应示例
```json
{
  "transactions": [
    {
      "id": "txn_001",
      "date": "2026-02-15T10:30:00Z",
      "type": "BUY",
      "symbol": "BTC",
      "quantity": 0.1,
      "price": 42000.00,
      "total": 4200.00,
      "fee": 10.50
    },
    {
      "id": "txn_002",
      "date": "2026-02-14T14:20:00Z",
      "type": "SELL",
      "symbol": "AAPL",
      "quantity": 5,
      "price": 180.00,
      "total": 900.00,
      "fee": 2.25
    }
  ]
}
```

## 配置说明

### config.json
```json
{
  "mcpServers": {
    "investmenttracker": {
      "url": "https://claw.investtracker.ai/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY",
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json"
      },
      "timeout": 30,
      "retry_attempts": 3,
      "cache_enabled": true,
      "cache_ttl": 300
    }
  },
  "cache_settings": {
    "enabled": true,
    "ttl": 300,
    "max_size": 100
  },
  "notifications": {
    "price_alerts": true,
    "portfolio_updates": true,
    "daily_summary": true
  }
}
```

## 开发指南

### 添加新功能
1. 在 `scripts/` 目录下创建新的 Python 脚本
2. 更新 `SKILL.md` 中的功能描述
3. 添加相应的使用示例
4. 测试 API 调用和错误处理

### 错误处理
```python
try:
    response = requests.get(api_url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
except requests.exceptions.RequestException as e:
    logger.error(f"API请求失败: {e}")
    return {"error": "无法连接到投资追踪服务"}
```

### 性能优化
1. 实现数据缓存减少 API 调用
2. 使用异步请求提高响应速度
3. 批量处理相关数据请求
4. 压缩传输数据减少带宽

## 故障排除

### 常见问题
1. **API 连接失败**：检查网络连接和 API 密钥
2. **数据不更新**：清除缓存或增加更新频率
3. **权限错误**：验证 API 密钥是否有足够权限
4. **响应缓慢**：检查网络延迟或启用缓存

### 调试模式
启用调试日志查看详细请求信息：
```bash
export INVESTMENT_TRACKER_DEBUG=true
```

## 安全建议
1. 定期轮换 API 密钥
2. 使用环境变量存储敏感信息
3. 限制 API 调用频率
4. 监控异常访问模式
5. 定期审计访问日志

## 贡献指南
欢迎提交 Pull Request 或 Issue 来改进此技能。