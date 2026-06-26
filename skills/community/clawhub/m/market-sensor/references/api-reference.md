# MarketSensor Open API Reference

完整的 API 接口参考文档。

## Base URL

```
https://api.marketsensor.ai
```

## 认证

所有请求需要 `Authorization: Bearer <API_KEY>` header。

API Key 在 MarketSensor 网站的「设置 → API Keys」页面生成。

---

## 接口列表

### GET /api/open/watchlist

获取用户自选股列表。

**Response 200**:
```json
{
  "items": [
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "assetType": "stock",
      "mode": "daily"
    }
  ]
}
```

---

### POST /api/open/watchlist

添加自选股。

**Request Body**:
```json
{
  "symbol": "AAPL",
  "mode": "daily",
  "name": "Apple Inc."
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| symbol | string | 是 | 股票代码 |
| mode | string | 否 | `daily` 或 `intraday`，默认 `daily` |
| name | string | 否 | 显示名称，不传则自动解析 |

**Response 200**: 添加成功
**Response 409**: 已存在

---

### POST /api/open/watchlist/remove

移除自选股。

**Request Body**:
```json
{
  "symbol": "AAPL"
}
```

**Response 200**: 移除成功
**Response 404**: 未找到

---

### GET /api/open/analysis/status/:symbol

查询指定股票的分析状态。

**Path Parameters**: `symbol` — 股票代码

**Response 200**:
```json
{
  "status": "completed",
  "reportId": "abc123",
  "updatedAt": "2026-03-30T10:00:00Z"
}
```

status 可选值：`completed` | `generating` | `queued` | `none`

---

### POST /api/open/analyze

触发股票分析。

**Request Body**:
```json
{
  "symbol": "TSLA",
  "mode": "daily"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| symbol | string | 是 | 股票代码 |
| mode | string | 否 | `daily` 或 `intraday`，不传则自动判断 |

**Response 200**: `{ status, reportId? }`
**Response 429**: 额度不足

---

### GET /api/open/report/:reportId

获取分析报告。

**Path Parameters**: `reportId` — 报告 ID

**Query Parameters**:
| 参数 | 说明 |
|------|------|
| format | `markdown`（默认）或 `json` |

**Response 200**: Markdown 文本或 JSON 对象
**Response 404**: 报告不存在

---

### GET /api/open/quota

查询账户额度。

**Response 200**:
```json
{
  "short": {
    "remaining": 8,
    "total": 10
  },
  "intraday": {
    "remaining": 5,
    "total": 5
  }
}
```
