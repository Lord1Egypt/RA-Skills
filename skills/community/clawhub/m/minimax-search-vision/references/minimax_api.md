# MiniMax API 参考文档

## Token Plan MCP

MiniMax Token Plan 提供了两个专属工具：**网络搜索** 和 **图片理解**

### web_search

根据搜索查询词进行网络搜索，返回搜索结果和相关搜索建议。

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| query | string | ✓ | 搜索查询词 |

### understand_image

对图片进行理解和分析，支持多种图片输入方式。

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| prompt | string | ✓ | 对图片的提问或分析要求 |
| image_url | string | ✓ | 图片来源，支持 HTTP/HTTPS URL 或本地文件路径 |

**支持格式**：JPEG、PNG、GIF、WebP（最大 20MB）

## API 端点

MCP 服务地址：`https://api.minimaxi.com`

## 认证

使用 Bearer Token 认证：

```python
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
```

## 错误码

| 错误码 | 说明 |
|-------|------|
| 401 | API Key 无效或缺失 |
| 403 | 无权限访问 |
| 429 | 请求频率超限 |
| 500 | 服务器内部错误 |
| 503 | 服务暂时不可用 |

## 官方文档

- [Token Plan MCP 文档](https://platform.minimaxi.com/docs/guides/token-plan-mcp-guide.md)
- [API 概览](https://platform.minimaxi.com/docs/api-reference/api-overview.md)
- [Anthropic API 兼容](https://platform.minimaxi.com/docs/api-reference/text-anthropic-api.md)
