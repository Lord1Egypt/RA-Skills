# Modrinth API 参考文档

## 基本信息

- **Base URL**: `https://api.modrinth.com/v2`
- **文档地址**: `https://docs.modrinth.com/api-specification/`
- **认证**: 不需要 API Key（公开接口）
- **国内可访问性**: ✅ 可裸连，无需代理

---

## 1. 搜索 Mod

### 端点

```
GET /search
```

### 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `query` | string | ✅ | 搜索关键词 |
| `index` | string | ❌ | 排序字段：`relevance`（默认）/ `downloads` / `updated` / `newest` / `name` |
| `filters` | string | ❌ | 过滤表达式，格式：`categories="shader" AND versions="1.20.4"` |
| `limit` | integer | ❌ | 返回数量，默认 20，最大 100 |
| `offset` | integer | ❌ | 分页偏移量 |

### 过滤表达式格式

```
categories="shader" AND versions="1.20.4" AND loaders="fabric"
categories="technology" OR categories="utility"
NOT categories="addons"
```

### 请求示例

```http
GET https://api.modrinth.com/v2/search?query=sodium&limit=10&filters=categories="optimization" AND versions="1.20.4" AND loaders="fabric"
```

### 响应示例

```json
{
  "hits": [
    {
      "slug": "sodium",
      "title": "Sodium",
      "description": "A Minecraft mod designed to improve frame rates...",
      "categories": ["optimization", "fabric", "liteloader"],
      "client_side": "optional",
      "server_side": "required",
      "project_id": "AANobbMI",
      "author": "embeddedt",
      "downloads": 78901234,
      "icon_url": "https://cdn.modrinth.com/data/AANobbMI/icon.png",
      "latest_version": "0.5.8",
      "date_created": "2020-12-28T14:36:43.512000Z",
      "date_modified": "2024-11-20T12:34:56.789000Z"
    }
  ],
  "offset": 0,
  "limit": 10,
  "total_hits": 156
}
```

---

## 2. 获取 Mod 详情

### 端点

```
GET /project/<slug_or_id>
```

### 请求示例

```http
GET https://api.modrinth.com/v2/project/sodium
```

### 响应关键字段

```json
{
  "id": "AANobbMI",
  "slug": "sodium",
  "title": "Sodium",
  "description": "...",
  "categories": ["optimization", "fabric", "liteloader"],
  "client_side": "optional",
  "server_side": "required",
  "downloads": 78901234,
  "followers": 123456,
  "latest_version": "0.5.8",
  "license": "LGPL-3.0",
  "author": "embeddedt",
  "versions": ["0.5.8", "0.5.7", ...],
  "game_versions": ["1.20.4", "1.20.2", "1.20.1", "1.19.4"],
  "loaders": ["fabric", "quilt"],
  "icon_url": "https://cdn.modrinth.com/data/AANobbMI/icon.png",
  "date_published": "2024-01-15T10:00:00.000000Z",
  "date_modified": "2024-11-20T12:34:56.789000Z",
  "approved": true,
  "repository_url": "https://github.com/CaffeineMC/sodium-fabric",
  "issues_url": "https://github.com/CaffeineMC/sodium-fabric/issues",
  "wiki_url": "https://github.com/CaffeineMC/sodium-fabric/wiki"
}
```

---

## 3. 获取 Mod 版本列表

### 端点

```
GET /project/<slug_or_id>/version
```

### 请求示例

```http
GET https://api.modrinth.com/v2/project/sodium/version?game_version=1.20.4
```

### 响应关键字段

```json
[
  {
    "id": "...",
    "version_number": "0.5.8",
    "loaders": ["fabric", "quilt"],
    "game_versions": ["1.20.4", "1.20.2", "1.20.1"],
    "date_published": "2024-11-20T12:34:56.789000Z",
    "downloads": 123456,
    "files": [
      {
        "url": "https://cdn.modrinth.com/data/AANobbMI/versions/...",
        "filename": "sodium-0.5.8+1.20.4.jar",
        "size": 2048576,
        "sha1": "..."
      }
    ]
  }
]
```

---

## 4. 获取 Mod 依赖

### 端点

```
GET /project/<slug_or_id>/dependencies
```

### 请求示例

```http
GET https://api.modrinth.com/v2/project/sodium/dependencies
```

### 响应关键字段

```json
[
  {
    "version_id": "...",
    "project_id": "...",
    "dependency_type": "required",
    "project": {
      "slug": "fabric-api",
      "title": "Fabric API",
      "categories": ["library"],
      "downloads": 123456789
    }
  }
]
```

**`dependency_type` 值说明：**

| 值 | 含义 |
|----|------|
| `required` | 必需依赖，不安装会导致崩溃 |
| `optional` | 可选依赖 |
| `incompatible` | 与当前 Mod 不兼容 |
| `embedded` | 内嵌依赖（已打包在 Mod 中） |

---

## 5. 搜索分类列表

### 端点

```
GET /tag/category
GET /tag/game_version
GET /tag/loader
```

### 常用 Loader

| Loader | 说明 |
|--------|------|
| `forge` | Forge 加载器 |
| `fabric` | Fabric 加载器 |
| `quilt` | Quilt 加载器 |
| `rift` | Rift 加载器（1.13-1.18） |

### 常用分类

`optimization`, `technology`, `adventure`, `cursed`, `decoration`, `equipment`, `food`, `fun`, `gameplay`, `library`, `magic`, `misc`, `mobs`, `music`, `nature`, `news`, `organization`, `photography`, `creation`, `economy`, `roleplay`, `server`, `storage`, `transportation`, `utility`

---

## 6. 常见问题

**Q: 如何判断 Mod 支持哪个 Minecraft 版本？**
A: 查看 `game_versions` 数组，包含所有兼容的版本号。

**Q: 如何判断是客户端还是服务端 Mod？**
A: 查看 `client_side` 和 `server_side` 字段，值可为 `required` / `optional` / `unsupported` / `unknown`。

**Q: Modrinth 支持模糊搜索吗？**
A: 支持，`query` 参数会自动进行模糊匹配。

**Q: 单次请求超时设置？**
A: 建议设置为 8 秒。Modrinth 服务器响应较快，正常情况下 2-3 秒内返回。
