# Temu 以图搜同款 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/geekbi/temu/goodsImageSearch`
- **请求方式**：POST，`Content-Type: application/json`
- **认证方式**：Header `Authorization: <api_key>`；api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，回退到兼容键 `LINKFOXAGENT_API_KEY`
- **User-Agent**：`LinkFox-Skill/2.0`
- **透传头**：`SESSION_ID`、`MESSAGE_ID`、`MODE_ID`、`APP_NAME`（未设置时为空串）
- **超时**：150s

> 业务入口脚本默认仅缓存成功响应 24 小时，成功的空结果也可缓存；HTTP 或业务失败不缓存。`--inline` 不绕过缓存；`--no-cache` 跳过缓存读写并强制真实请求，可能再次消耗 150 算力。

> `${LINKFOX_TOOL_GATEWAY}` 未设置时，脚本回退到 `https://tool-gateway.linkfox.com`。客户端只调用 LinkFox 工具网关，不直接调用上游数据服务。

## 请求参数

POST Body 为 JSON 对象，只包含以下已验证字段：

| 参数 | 类型 | 必填 | 约束 | 说明 |
|---|---|---:|---|---|
| `imageUrl` | string | 是 | 非空；最大 2048 字符；必须是 LinkFox OSS 临时图片目录中的资源 URL | 用于视觉相似商品检索的源图 |
| `contentType` | string | 否 | 最大 100 字符；仅 `image/jpeg`、`image/png`、`image/gif`、`image/webp`、`image/bmp` | 图片 MIME 类型；传入时必须同时与 OSS 响应类型和图片实际字节格式一致 |

服务端下载后的图片不得超过 10 MB，且实际字节必须是 JPEG、PNG、GIF、WebP 或 BMP。省略 `contentType` 时，服务端从 OSS 响应和图片字节识别类型。

以下请求会被拒绝：

- `{}` 或缺少 `imageUrl`：HTTP 400，`imageUrl 为必填参数`
- 任意外部图片 URL：HTTP 400，要求使用配置好的 OSS 资源
- 图片超过 10 MB、格式不受支持，或 `contentType` 与 OSS 响应/实际字节不一致：HTTP 400

该端点的已验证请求契约不包含 Base64、分页、每页数量、排序、筛选、关键词或站点字段。不要从同族商品搜索接口复制这些参数。

## 图片上传

本地图片或外部图片必须先通过 `scripts/upload_image.py` 上传。辅助脚本执行以下流程：

1. 向 `POST ${LINKFOX_TOOL_GATEWAY}/oss/file/presignedPut` 提交图片的 `contentType` 与 `fileExtension`，获取预签名 PUT URL。
2. 使用相同 `Content-Type` 和 `x-oss-object-acl: public-read` 将本地图片 PUT 到该 URL。
3. 去除预签名 URL 的查询参数，并由 `upload_image.py` 输出包含公开 `url` 和 `contentType`、不含签名参数的结果 JSON。

辅助脚本只使用 Python 标准库，支持 `jpg`、`jpeg`、`png`、`gif`、`webp`、`bmp`。不要在日志、反馈或面向用户输出中泄露 API Key 或预签名 URL 的查询参数。`/oss/file/presignedPut` 图片上传接口不扣算力。

## 响应结构

| 字段 | 类型 | 真实值 / 说明 |
|---|---|---|
| `errcode` | integer | 成功为 `200` |
| `errmsg` | string | 成功为 `ok` |
| `total` | integer | 返回的相似商品行数；随源图变化，可为 `0` |
| `items` | array | 相似商品行；成功响应也可能为空数组，不得假设固定为 100 行 |
| `columns` | array | 渲染列定义 |
| `title` | string | 实测 `Temu 图搜同款` |
| `sourceType` | string | 实测 `temu` |
| `sourceTool` | string | 实测 `geekbi_temu` |
| `type` | string | 实测 `tableListWorkbenches` |

真实成功响应未包含 `page`、`size` 或 `regionId`；不要在文档中虚构分页字段。

### `items[]` 商品字段

业务字段都可能缺失或为 `null`，不得按必填字段解析。

| 字段组 | 字段与含义 |
|---|---|
| 标识与标题 | `goodsId`, `mallId`, `goodsName`, `goodsNameCn`, `goodsNameEn`, `brand`, `thumbnail` |
| 品类 | `catIds`; `catItems[]` 含 `catId`, `catName`, `catLevel`, `parentCatId`, `isLeaf` |
| 累计指标 | `sold` 历史销量，`sales` 历史销售额，`quantity` 库存，`mallSold` 店铺销量 |
| 周期销量 | `daySold`, `weekSold`, `monthSold`, `daySoldRate`, `weekSoldRate`, `monthSoldRate` |
| 周期销售额 | `daySales`, `weekSales`, `monthSales`, `daySalesRate`, `weekSalesRate`, `monthSalesRate` |
| 价格 | `minPrice`, `maxPrice`（站点当地货币） |
| 供货价 | `supplyPrice`, `minSupplyPrice`, `medianSupplyPrice`, `maxSupplyPrice`（上游供货价字段） |
| 评价 | `goodsScore`, `reviewNum` |
| 状态 | `hostingMode`（1=全托管，2=半托管）, `status`（1=正常，2=缺货，3=下架）, `isAd`, `isCustom`, `isPresale` |
| 时间 | `onSaleTime`, `mallOpenTime`, `createTime`, `updateTime` |
| 其他 | `similarNum`; `sku` 可能是 JSON 编码字符串 |

实测同一 `goodsId` 可能重复出现且指标或时间不同；中文标题和 `sku` 内文本可能乱码；个别价格字段可能互相矛盾。调用方不得静默纠正、合并或补造。

### `columns[]` 结构

渲染列通常包含 `field`, `title`, `cellType`, `sortable`, `filterable`。实测返回 44 个列定义，覆盖上述商品字段；业务解析应以 `items[]` 实际存在的字段为准。

## 响应示例

以下示例只展示已由真实响应确认的层级，业务值已简化：

```json
{
  "errcode": 200,
  "errmsg": "ok",
  "total": 100,
  "items": [
    {
      "goodsId": "601100240999226",
      "mallId": "634418220884840",
      "goodsNameEn": "Men's thick-soled hiking shoes",
      "thumbnail": "https://img.kwcdn.com/product/fancy/example.jpg",
      "sold": 53000,
      "monthSold": 1494,
      "minPrice": 22.32,
      "goodsScore": 4.7,
      "reviewNum": 5070,
      "hostingMode": 1,
      "status": 1
    }
  ],
  "columns": [],
  "title": "Temu 图搜同款",
  "sourceType": "temu",
  "sourceTool": "geekbi_temu",
  "type": "tableListWorkbenches"
}
```

## 错误码

入口脚本会原样返回 HTTP JSON 错误；非 JSON 的 XML/文本错误体会包装为 `error` / `details`，不应以 Python 堆栈替代业务错误。

| HTTP / 业务码 | 含义 | 处理建议 |
|---|---|---|
| 200 且 `errcode=200` | 成功 | 解析 `items`；空数组也是有效结果，不要自动换图重试 |
| 400 | 参数或图片 URL 不合规 | 检查 `imageUrl` 是否非空且来自 LinkFox OSS；不要自动换图重试 |
| 401 | 认证失败 | 检查 `LINKFOX_AGENT_API_KEY` 或兼容键 `LINKFOXAGENT_API_KEY`，并按 `SKILL.md` 的认证引导处理 |
| 402 | 算力或余额不足 | 停止调用并按认证/算力引导处理 |
| 403 | 无权限 | 停止调用并联系工具管理员；不要按充值问题处理 |
| 429 | 请求过于频繁 | 停止连续调用，稍后再试 |
| 502 / 503 / 504 | 网关或上游异常 | 不自动重试；说明可能再次扣费并取得用户确认后，才可按原参数重试一次 |

已验证错误示例：

```xml
<ToolErrorResponse><errcode>400</errcode><errmsg>imageUrl 为必填参数</errmsg></ToolErrorResponse>
```

## curl 示例

```bash
LINKFOX_UPLOAD_RESULT="$(python scripts/upload_image.py ./product.jpg)"
LINKFOX_OSS_URL="$(printf '%s' "${LINKFOX_UPLOAD_RESULT}" | jq -r '.url')"
LINKFOX_CONTENT_TYPE="$(printf '%s' "${LINKFOX_UPLOAD_RESULT}" | jq -r '.contentType')"

curl --max-time 150 -X POST "${LINKFOX_TOOL_GATEWAY}/geekbi/temu/goodsImageSearch" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID}" \
  -H "MESSAGE_ID: ${MESSAGE_ID}" \
  -H "MODE_ID: ${MODE_ID}" \
  -H "APP_NAME: ${APP_NAME}" \
  -d "{\"imageUrl\":\"${LINKFOX_OSS_URL}\",\"contentType\":\"${LINKFOX_CONTENT_TYPE}\"}"
```

## Feedback API

> This endpoint is **separate** from the tool API above. Do not mix the two base URLs.

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type:** `application/json`

```json
{
  "skillName": "linkfox-geekbi-temu-search-by-image",
  "sentiment": "POSITIVE",
  "category": "OTHER",
  "content": "Results were accurate, user was satisfied."
}
```

**Field rules:**
- `skillName`: Use this skill's `name` from the YAML frontmatter (`linkfox-geekbi-temu-search-by-image`)
- `sentiment`: Choose ONE - `POSITIVE` (praise), `NEUTRAL` (suggestion without emotion), `NEGATIVE` (complaint or error)
- `category`: Choose ONE - `BUG` (malfunction or wrong data), `COMPLAINT` (user dissatisfaction), `SUGGESTION` (improvement idea), `OTHER`
- `content`: Include what the user said or intended, what actually happened, and why it is a problem or praise
