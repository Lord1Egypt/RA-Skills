# init_video_upload

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/init_video_upload.py` |
| Method / path | POST `api/v2/media/init_video_upload` |
| 官方文档 | [init_video_upload](https://open.shopee.com/documents/v2/v2.media.init_video_upload?module=130&type=1) |
| 用途 | Init chunked video upload session; pass body |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |

- Method：**POST**
- POST：传 `body` / `requestBody`，或把 `body_fields` 列在 JSON 顶层
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：Init chunked video upload session; pass body

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/init_video_upload.py '{"shopId": "67890"}'

# 通用入口
python scripts/media_api.py '{"api": "init_video_upload", "shopId": "67890"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`initVideoUpload`**（Shopee `response` 解析结果）
3. 字段以官方文档为准
