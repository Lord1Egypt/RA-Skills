# CurseForge API 参考文档

## 基本信息

- **Base URL**: `https://api.curseforge.com/v1`
- **文档地址**: `https://docs.curseforge.com/`
- **认证**: 需要 API Key，通过 `X-API-Key` 请求头传递
- **国内可访问性**: ⚠️ 国内可能需要代理，超时建议 5 秒
- **游戏 ID（Minecraft Java Edition）**: `432`

---

## 1. 获取 Mod API Key

若用户提供了 `CF_API_KEY`，则优先使用 CurseForge。申请地址：
`https://console.curseforge.com/`

---

## 2. 搜索 Mod

### 端点

```
GET /games/432/mods/search
```

### 请求头

```http
X-API-Key: <你的API_KEY>
```

### 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `gameId` | integer | ✅ | Minecraft Java Edition = 432 |
| `searchFilter` | string | ❌ | 搜索关键词 |
| `classId` | integer | ❌ | Mod 类型，默认 6（Minecraft Mod） |
| `categoryId` | integer | ❌ | 分类 ID（需先获取分类列表） |
| `gameVersion` | string | ❌ | Minecraft 版本，如 `1.20.4` |
| `sortField` | integer | ❌ | 排序字段（见下表） |
| `sortOrder` | string | ❌ | `asc` 或 `desc` |
| `modLoaderType` | integer | ❌ | 加载器类型（见下表） |
| `gameVersionTypeId` | integer | ❌ | 版本类型（快照/正式版等） |
| `index` | integer | ❌ | 分页起始位置 |
| `pageSize` | integer | ❌ | 每页数量，默认 25，最大 50 |

### 排序字段（sortField）

| 值 | 含义 |
|----|------|
| 1 |  popularity（下载量） |
| 2 |  lastUpdated（最后更新时间） |
| 3 |  name（名称） |
| 4 |  totalDownloads（总下载量） |
| 5 |  featured（精选） |
| 7 |  rating（评分） |

### 加载器类型（modLoaderType）

| 值 | 加载器 |
|----|-------|
| 1 | Any |
| 2 | Forge |
| 3 | LiteLoader |
| 4 | Fabric |
| 5 | Rift |
| 6 | 未知 |

### 请求示例

```http
GET https://api.curseforge.com/v1/games/432/mods/search?gameId=432&searchFilter=sodium&gameVersion=1.20.4&modLoaderType=4&sortField=1&sortOrder=desc&pageSize=10
```

### 响应示例

```json
{
  "data": [
    {
      "id": 394298,
      "name": "Sodium",
      "slug": "sodium",
      "authors": [
        {
          "id": 186789,
          "name": "embeddedt",
          "url": "https://www.curseforge.com/members/embeddedt"
        }
      ],
      "logo": {
        "url": "https://media.forgecdn.net/avatars/...",
        "thumbnailUrl": "https://media.forgecdn.net/avatars/thumbnails/..."
      },
      "summary": "A Minecraft mod designed to improve frame rates...",
      "categories": [
        {
          "id": 4251,
          "name": "Modding Tools",
          "slug": "modding-tools",
          "avatarUrl": "...",
          "parentId": -1,
          "rootId": -1,
          "projectId": 394298,
          "gameId": 432
        }
      ],
      "classId": 6,
      "downloadCount": 78901234,
      "latestFiles": [
        {
          "id": 5678901,
          "gameVersion": ["1.20.4", "1.20.2"],
          "modLoader": 4,
          "fileDate": "2024-11-20T12:34:56Z",
          "fileName": "sodium-0.5.8+1.20.4.jar",
          "downloadUrl": "https://www.curseforge.com/minecraft/mc-mods/sodium/download/5678901",
          "fileLength": 2048576,
          "releaseType": 1
        }
      ],
      "dateModified": "2024-11-20T12:34:56Z",
      "dateCreated": "2020-12-28T14:36:43Z",
      "dateReleased": "2024-11-20T12:34:56Z",
      "status": 1,
      "userVote": 0,
      "externalUrl": "https://www.curseforge.com/minecraft/mc-mods/sodium",
      "primaryCategoryId": 4251,
      "popularityScore": 99999
    }
  ],
  "pagination": {
    "index": 0,
    "pageSize": 10,
    "resultCount": 10,
    "totalCount": 42
  }
}
```

---

## 3. 获取 Mod 详情

### 端点

```
GET /mods/<mod_id>
```

### 请求示例

```http
GET https://api.curseforge.com/v1/mods/394298
```

---

## 4. 获取 Mod 文件列表（含依赖）

### 端点

```
GET /mods/<mod_id>/files
```

### 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `gameVersion` | string | ❌ | Minecraft 版本 |
| `modLoaderType` | integer | ❌ | 加载器类型 |
| `index` | integer | ❌ | 分页起始位置 |
| `pageSize` | integer | ❌ | 每页数量 |

### 响应关键字段

```json
{
  "data": [
    {
      "id": 5678901,
      "displayName": "Sodium 0.5.8 for 1.20.4",
      "fileName": "sodium-0.5.8+1.20.4.jar",
      "gameVersions": ["1.20.4", "1.20.2"],
      "modLoader": 4,
      "releaseType": 1,
      "fileDate": "2024-11-20T12:34:56Z",
      "fileLength": 2048576,
      "downloadUrl": "https://www.curseforge.com/minecraft/mc-mods/sodium/download/5678901",
      "dependencies": [
        {
          "modId": 419700,
          "relationType": 3
        }
      ]
    }
  ]
}
```

**`relationType` 值说明：**

| 值 | 含义 |
|----|------|
| 1 | EmbeddedLibrary |
| 2 | OptionalDependency |
| 3 | RequiredDependency |
| 4 | Tool |
| 5 | Unmapped |
| 6 | Incompatible |
| 7 | Include |

---

## 5. 获取 Mod 分类

### 端点

```
GET /games/432/categories?classId=6
```

### 参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `gameId` | integer | ✅ | 432 |
| `classId` | integer | ❌ | 6 = Minecraft Mod |

### 常用分类 ID

| ID | 名称 |
|----|------|
| 406 | Biomes |
| 412 | Add-ons |
| 418 | Energy |
| 420 | Farming |
| 422 | Food |
| 426 | Hardware |
| 430 | Lucky Blocks |
| 431 | Magic |
| 435 | Management |
| 436 | Map & Information |
| 439 | Miscellaneous |
| 440 | Mobs |
| 445 | Optimization |
| 447 | Other |
| 448 | Physics |
| 453 | Player |
| 454 | QoL |
| 456 | Redstone |
| 457 | Server |
| 461 | Storage |
| 462 | Structures |
| 463 | Technology |
| 464 | Terraforming |
| 467 | Transportation |
| 470 | Tynai's Library |
| 475 | Vanilla+ |

---

## 6. 注意事项

- **API Key 优先级**：优先使用环境变量 `CF_API_KEY`，若未配置则跳过 CurseForge
- **超时设置**：建议 5 秒，CurseForge 响应较慢
- **分页处理**：使用 `index` 和 `pageSize` 进行分页，CurseForge 单次最多返回 50 条
- **版本过滤**：CurseForge 的 `gameVersion` 参数需精确匹配，不支持模糊版本
- **国内访问**：若连接超时，自动降级到 Modrinth
