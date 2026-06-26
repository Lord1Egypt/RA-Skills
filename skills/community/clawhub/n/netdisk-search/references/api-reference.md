# 网盘搜索 API Reference

## Base URL

```
http://localhost:8888  # 默认本地
```

## Authentication

当 `AUTH_ENABLED=true` 时，需要 JWT Token。

```
Authorization: Bearer <token>
```

### POST /api/auth/login

获取 Token。

```json
// Request
{"username": "admin", "password": "admin123"}

// Response
{"token": "eyJhbGc...", "expires_at": 1234567890, "username": "admin"}
```

### POST /api/auth/verify

验证 Token 有效性。

### POST /api/auth/logout

退出登录（客户端删除 Token 即可）。

---

## Search API

### POST /api/search

搜索网盘资源。

**Request Body:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| kw | string | ✅ | 搜索关键词 |
| channels | string[] | 否 | TG频道列表，不提供则用默认配置 |
| conc | number | 否 | 并发数，默认自动计算 |
| refresh | boolean | 否 | 强制刷新缓存 |
| res | string | 否 | 结果类型: all / results / merge (默认) |
| src | string | 否 | 来源: all (默认) / tg / plugin |
| plugins | string[] | 否 | 指定插件列表 |
| cloud_types | string[] | 否 | 网盘类型过滤 |
| ext | object | 否 | 传递给插件的扩展参数 |
| filter | object | 否 | 过滤条件: {"include": [...], "exclude": [...]} |

**示例:**

```bash
curl -X POST http://localhost:8888/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "kw": "速度与激情",
    "cloud_types": ["baidu", "quark"],
    "filter": {"include": ["合集"], "exclude": ["预告"]}
  }'
```

**Response:**

```json
{
  "total": 15,
  "results": [
    {
      "message_id": "12345",
      "unique_id": "channel-12345",
      "channel": "tgsearchers3",
      "datetime": "2024-06-10T14:23:45Z",
      "title": "速度与激情全集1-10",
      "content": "...",
      "links": [
        {
          "type": "baidu",
          "url": "https://pan.baidu.com/s/1abcdef",
          "password": "1234",
          "work_title": "速度与激情全集1-10"
        }
      ]
    }
  ],
  "merged_by_type": {
    "baidu": [
      {
        "url": "https://pan.baidu.com/s/1abcdef",
        "password": "1234",
        "note": "速度与激情全集1-10",
        "datetime": "2024-06-10T14:23:45Z",
        "source": "tg:tgsearchers3"
      }
    ]
  }
}
```

### GET /api/search

同 POST，参数通过 URL query 传递。

---

## Link Check API

### POST /api/check/links

批量检测网盘链接有效性。

**Request Body:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| items | object[] | ✅ | 待检测链接数组 |
| items[].disk_type | string | ✅ | 网盘类型 |
| items[].url | string | ✅ | 分享链接 |
| items[].password | string | 否 | 提取码 |
| proxy_url | string | 否 | 本次检测使用的代理 |

**支持检测的网盘类型:**
baidu, aliyun, quark, tianyi, uc, mobile, 115, xunlei, 123

**示例:**

```bash
curl -X POST http://localhost:8888/api/check/links \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"disk_type": "quark", "url": "https://pan.quark.cn/s/abcdefg"},
      {"disk_type": "baidu", "url": "https://pan.baidu.com/s/1abcdef", "password": "1234"}
    ]
  }'
```

**Response:**

```json
{
  "results": [
    {
      "disk_type": "quark",
      "url": "https://pan.quark.cn/s/abcdefg",
      "state": "ok",
      "summary": "链接有效"
    },
    {
      "disk_type": "baidu",
      "url": "https://pan.baidu.com/s/1abcdef",
      "state": "bad",
      "summary": "链接失效"
    }
  ]
}
```

**状态说明:**

| state | 说明 |
|-------|------|
| ok | 链接有效 |
| bad | 链接失效 |
| locked | 需要提取码或密码错误 |
| unsupported | 暂不支持检测 |
| uncertain | 检测失败或不确定 |

---

## Health API

### GET /api/health

检查服务状态，无需认证。

**Response:**

```json
{
  "status": "ok",
  "auth_enabled": false,
  "plugins_enabled": true,
  "plugin_count": 80,
  "plugins": ["pansearch", "panta", "..."],
  "channels_count": 1,
  "channels": ["tgsearchers3"]
}
```

---

## Supported Cloud Types

| type | 中文名 |
|------|--------|
| baidu | 百度网盘 |
| aliyun | 阿里云盘 |
| quark | 夸克网盘 |
| guangya | 光鸭云盘 |
| tianyi | 天翼云盘 |
| uc | UC网盘 |
| mobile | 移动云盘 |
| 115 | 115网盘 |
| pikpak | PikPak |
| xunlei | 迅雷网盘 |
| 123 | 123网盘 |
| magnet | 磁力链接 |
| ed2k | 电驴链接 |
| others | 其他 |
