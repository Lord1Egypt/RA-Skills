# iFinD MCP API Reference

## 服务器端点

| 服务 | URL |
|------|-----|
| stock | https://api-mcp.51ifind.com:8643/ds-mcp-servers/hexin-ifind-ds-stock-mcp |
| fund | https://api-mcp.51ifind.com:8643/ds-mcp-servers/hexin-ifind-ds-fund-mcp |
| edb | https://api-mcp.51ifind.com:8643/ds-mcp-servers/hexin-ifind-ds-edb-mcp |
| news | https://api-mcp.51ifind.com:8643/ds-mcp-servers/hexin-ifind-ds-news-mcp |

## 认证

通过 HTTP Header 传递：
```
Authorization: Bearer <jwt_token>
```

## 调用示例

```bash
# 列出所有工具
mcporter list

# 调用股票查询
mcporter call hexin-ifind-stock.get_stock_summary query:"股票名称"

# 调用基金查询
mcporter call hexin-ifind-fund.search_funds query:"基金名称"
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| -32002 | 工具不允许 |
| 403 | 认证失败 |
| 500 | 服务器错误 |
