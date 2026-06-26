# PinchTab API 参考

完整 HTTP API 文档。

## 基础 URL

```
http://localhost:9867
```

## 认证

如果设置了 `BRIDGE_TOKEN`，所有请求需要：

```
Authorization: Bearer YOUR_TOKEN
```

## 端点

### POST /navigate

导航到 URL。

**请求：**
```json
{
  "url": "https://example.com",
  "blockImages": false,
  "stealth": true
}
```

**响应：**
```json
{
  "tabId": "TAB_123",
  "success": true
}
```

### GET /snapshot

获取页面可访问性树快照。

**参数：**
- `filter` - `interactive` 仅交互式元素
- `format` - `compact` 紧凑格式
- `diff` - `true` 仅变化
- `tabId` - 指定标签页

**响应：**
```json
{
  "refs": [...],
  "text": "...",
  "title": "..."
}
```

### POST /action

执行操作。

**请求：**
```json
{
  "kind": "click",
  "ref": "e5",
  "tabId": "TAB_123"
}
```

**操作类型：**
- `click` - 点击
- `type` - 输入文本
- `press` - 按键
- `focus` - 聚焦
- `hover` - 悬停
- `scroll` - 滚动

### GET /text

提取页面文本。

**参数：**
- `mode` - `readable` (默认) 或 `raw`
- `tabId` - 指定标签页

### POST /screenshot

截图。

**请求：**
```json
{
  "format": "jpeg",
  "quality": 80,
  "fullPage": true
}
```

### POST /tabs

创建新标签页。

**请求：**
```json
{
  "url": "https://example.com"
}
```

### POST /tabs/switch

切换标签页。

**请求：**
```json
{
  "tabId": "TAB_123"
}
```

### DELETE /tabs/{id}

关闭标签页。

### POST /eval

执行 JavaScript。

**请求：**
```json
{
  "script": "document.title",
  "tabId": "TAB_123"
}
```

### POST /tabs/{id}/pdf

导出 PDF。

**请求：**
```json
{
  "landscape": false,
  "printBackground": true,
  "headerTemplate": "<div>Header</div>",
  "footerTemplate": "<div>Footer</div>"
}
```
