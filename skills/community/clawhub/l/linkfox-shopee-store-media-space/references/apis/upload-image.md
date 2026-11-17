# upload_image

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/upload_image.py` |
| LinkFox 端点 | POST `/shopee/uploadMediaSpaceImage` |
| 上游 Method / path | POST `api/v2/media_space/upload_image` |
| 官方文档 | [upload_image](https://open.shopee.com/documents/v2/v2.media_space.upload_image?module=91&type=1) |
| 用途 | Upload image; pass body (image file/url per official spec) |

经 **`POST /shopee/uploadMediaSpaceImage`** 专用端点转发；依赖 **`linkfox-shopee-store-auth`** 选店。Skill 读取本地图片并发送 Base64，服务端解码后构造 Shopee 所需的 multipart/form-data。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 是 | 已授权店铺 ID |
| `filePath` | string | 是 | 本地 JPEG、PNG 或 WebP 图片路径 |
| `contentType` | string | 否 | 默认按文件扩展名识别 |

- 单张图片最大 10MB；最终限制以 Shopee 官方要求为准。
- 不要传 OSS 外链或自行构造 multipart；`add_item` 使用上传后返回的 `imageId`。
- token、multipart boundary 和上游签名均由服务端处理。

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/upload_image.py '{"shopId":"67890","filePath":"/path/to/product.jpg"}'

# 通用入口
python scripts/media_space_api.py '{"api":"upload_image","shopId":"67890","filePath":"/path/to/product.jpg"}'
```

---

## 响应要点

1. 先看 **`uploadMediaSpaceImage.httpStatus`**、`success` 和 `error`
2. 成功后读取 **`uploadMediaSpaceImage.imageId`**；如上游提供，也可读取 `imageUrl`
3. `imageId` 用于 Product `add_item` 的图片字段；本接口没有 `developerProxy` 响应层
