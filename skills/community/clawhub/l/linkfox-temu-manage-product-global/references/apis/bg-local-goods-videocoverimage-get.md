# 视频封面 — `bg.local.goods.videocoverimage.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_manage_videocoverimage_get.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=2a343c65a03d42d380e9ad835aa7b54b |
| **网关** | `POST /temu/proxy`，`type`=`bg.local.goods.videocoverimage.get`，业务载荷放在 Body 的 `params` |

**Description:** Obtain cover image of video frame（按视频 `vid` 批量获取视频封面图）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── vidList[]              ← 视频 vid 列表
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| vidList | STRING[] | 否 | vid list for video（待查询封面的视频 vid 列表） |

> 实际调用时通常传入至少一个 `vid`；`vid` 来自商品详情或视频上传接口返回，勿与规格属性值 `vid` 混淆（以 Partner 上下文为准）。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "request": {
    "vidList": ["video-vid-001", "video-vid-002"]
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "request": {
    "vidList": ["58224724203874"]
  }
}
```

> **勿**使用旧字段 `videoUrl`；官方入参为 **`request.vidList`**。

---

## Response（Temu `body` 解析后）

```text
response
├── result
│   └── videoInfoMap          ← MAP: vid → 视频详情
│       └── [vid]
│           └── coverImage
├── success
├── errorCode
└── errorMsg
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| result | OBJECT | 业务结果对象 |
| success | BOOLEAN | success（当前请求是否成功） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| videoInfoMap | MAP | Video Information（视频信息映射） |

### `result.videoInfoMap`（MAP 键值）

| 键 / 值 | 类型 | 说明 |
|---------|------|------|
| `$key`（vid） | STRING | vid（视频 ID，与入参 `vidList` 中元素对应） |
| `$value` | OBJECT | Video Details（该视频详情） |

#### `videoInfoMap.$value`

| 参数 | 类型 | 说明 |
|------|------|------|
| coverImage | STRING | Video Cover image（视频封面图 URL） |

> 批量查询时遍历 **`result.videoInfoMap`**，以 **key（vid）** 与入参对照；某 `vid` 无 key 或 `coverImage` 为空时，表示该视频暂无封面或查询失败（以实网返回为准）。

### 响应示例（结构示意）

```json
{
  "success": true,
  "errorCode": 0,
  "errorMsg": "",
  "result": {
    "videoInfoMap": {
      "video-vid-001": {
        "coverImage": "https://cdn.example.com/cover1.jpg"
      },
      "video-vid-002": {
        "coverImage": "https://cdn.example.com/cover2.jpg"
      }
    }
  }
}
```

---

## 示例

```bash
python scripts/global_manage_videocoverimage_get.py '{
  "accessToken": "TOKEN",
  "request": {
    "vidList": ["video-vid-001"]
  }
}'
```
