---
name: linkfox-1688-search-by-image
description: 通过图片 URL 在 1688 平台以图搜图，检索外观相似或同款货源的商品数据。

# 1688 以图搜图（1688 Image-Based Product Search）

本技能通过图片 URL 在 1688 平台进行以图搜图，帮助跨境卖家找到外观相似或同款的 1688 货源商品。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 通过图片 URL、Base64 或 imageId 在 1688 平台进行视觉检索，返回外观相似或同款的货源商品。
- 提供商品标题、批发价、一件代发价、月销量、起批量、复购率、交易评分、商家身份等核心数据。
- 支持按价格区间、过滤条件（1688 严选、认证工厂、发货时效、品质退款率等）、排序（价格/月销/复购率）、分页查询。

### ❌ 边界与限制

- **图片来源**：`imageUrl`/`imageBase64`/`imageId` 三选一必填；`imageUrl` 须为可公开访问的公网链接。
- **图片格式**：仅支持 png/jpg/jpeg，不支持 webp/gif 等格式。
- **Base64 格式**：`imageBase64` 必须为纯编码内容，不能包含 `data:image/jpeg;base64,` 前缀。
- **分页上限**：每页最多 50 条；`page > 1` 时建议回传 `imageId` 以加速查询。
- **数据时效**：结果为实时搜索，不入库，无法进行二次 SQL 或 `_dataQuery_executeDynamicQuery` 处理。
- **筛选/排序限制**：仅支持预设的过滤条件与排序字段；用户请求未列出的排序或过滤条件时，不要调用其他工具或逻辑兜底，应告知支持的选项。
- **本地图片**：本工具需要可公开访问的图片 URL；用户提供本地文件路径时，须先调用上传脚本获取公网 URL（见下方「本地图片上传」）。
- **不在范围内**：基于关键词的 1688 文本搜索（用店雷达-1688 选品库）；1688 商品排行/趋势（用店雷达-1688 商品榜单）；Amazon 以图搜图（用亚马逊前端-以图搜图）；图片生成或编辑；商品评论分析；价格历史或趋势分析。

## 核心概念

1688 以图搜图基于视觉识别，在 1688 批发平台查找外观相似的商品，返回供应商商品数据，包括标题、价格、起批量、月销量、复购率、交易评分及商家身份标识。

**默认行为**：第 1 页、每页 20 条，按月销量降序（`sort` 默认 `{"monthSold":"desc"}`）。

## 调用方式

- **API 端点**：`POST /alibaba1688/imageSearch`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/alibaba1688_image_search.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-1688-search-by-image-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 本地图片上传

本工具需要**可公开访问的图片 URL**。若用户提供本地图片文件路径，须先上传以获取公网 URL。

运行上传脚本：
```bash
python scripts/upload_image.py /path/to/local/image.png
```

脚本会返回一个公网 URL（有效期 24 小时），可作为 `imageUrl` 参数使用。

## 使用示例

**1. 基础以图搜图**
```
在1688搜索与图片相似的商品，图片地址为 https://m.media-amazon.com/images/I/719mRAn2VrL._AC_SL1500_.jpg
```

**2. 带筛选条件**
```
在1688搜索与图片相似的商品，图片地址为 https://m.media-amazon.com/images/I/719mRAn2VrL._AC_SL1500_.jpg，查询第1页，筛选1688严选，并按价格从高到低排序
```

**3. 按排序查询**
```
在1688搜索与图片相似的商品，图片地址为 https://example.com/product.jpg，按价格从高到低排序
```

**4. 分页查询**
```
在1688搜索与图片相似的商品，图片地址为 https://example.com/product.jpg，查询第2页，每页50条
```

**5. 价格区间筛选**
```
在1688搜索与图片相似的商品，图片地址为 https://example.com/product.jpg，价格区间10-100元
```

## 展示规则

1. **清晰呈现数据**：以结构化表格展示关键列——商品图片、标题、批发价、代发价、月销量、起批量、复购率、商家身份。
2. **图片展示**：返回 `imageUrl` 时内联展示商品图片，便于直观对比。
3. **价格格式**：价格统一以人民币（¥）格式展示。
4. **商家标识**：突出展示商家身份（超级工厂/实力商家/诚信通会员）与商品标（严选）。
5. **结果计数**：始终告知总结果数及当前页/总页数。
6. **分页提示**：还有更多页时，提示用户可继续翻页。
7. **筛选/排序限制**：用户请求未支持的排序或过滤条件时，不要尝试任何兜底，告知其支持的选项即可。
8. **不做二次处理**：结果为实时搜索数据，不入库，无法进行二次 SQL 或数据处理。

## 用户表达与场景速查

**适用** —— 1688 平台以图找货源场景：

| 用户说 | 场景 |
|--------|------|
| "1688以图搜图" / "用图片找1688货源" | 基础以图搜图 |
| "帮我在1688找这个图片的同款" | 找同款商品 |
| "跨境找工厂，图片是..." | 跨境供应商找货 |
| "这个Amazon产品在1688有没有货源" | 由 Amazon 图片反查 1688 货源 |
| "筛选1688严选的相似商品" | 带筛选的以图搜图 |
| "按月销量排序找相似货源" | 带排序的以图搜图 |
| "查看第2页结果" | 分页查询 |

不适用场景见上方【能力边界】。

**边界判断**：当用户说"找货源"或"找同款"时，若其提供了图片 URL 且意图是在 1688 上找外观相似商品，则适用本技能；若需基于关键词搜索或排行数据，改用店雷达工具。

## 解决认证和积分问题

发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用skill内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个skill并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个skill。

---

# 1688-以图搜图 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/alibaba1688/imageSearch`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，回退 `LINKFOXAGENT_API_KEY`（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）
- **User-Agent**：`LinkFox-Skill/1.0`
- **超时**：150s

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| imageUrl | string | 条件必填 | - | 图片URL地址，请确保图片URL有效且可公开访问。最大长度：1000。仅支持 png/jpg/jpeg 格式，不支持 webp/gif 等。imageUrl/imageBase64/imageId 三选一必填 |
| imageBase64 | string | 条件必填 | - | 图片 Base64 编码字符串，为纯编码内容，不包含 `data:image/jpeg;base64,` 前缀。仅支持 png/jpg/jpeg 格式（imageUrl为空时使用） |
| imageId | string | 条件必填 | - | 图片ID（1688图片ID），以图搜图查询结果中也会返回，建议当分页 page>1 查询时带 imageId，加快响应速度 |
| page | int | 否 | 1 | 页码，从1开始 |
| pageSize | int | 否 | 20 | 每页返回的商品数量，最大不超过50 |
| priceStart | string | 否 | - | 价格筛选起始值（人民币），如 10 |
| priceEnd | string | 否 | - | 价格筛选结束值（人民币），如 100 |
| filter | string | 否 | - | 过滤条件，多个条件用逗号分隔。有效值见下方「支持的过滤条件」 |
| sort | string | 否 | {"monthSold":"desc"} | 排序条件，JSON格式 {排序字段: 排序方式}。有效字段：price、rePurchaseRate、monthSold；方式：asc/desc |
| keyword | string | 否 | - | 关键词，在结果中搜索 |
| productCollectionId | string | 否 | - | 货盘ID，单选。有效值见下方「支持的货盘ID」 |

### 支持的过滤条件

多个条件用逗号分隔，如 `1688Selection,totalEpScoreLv1,qrr0`。

| 值 | 说明 |
|----|------|
| 1688Selection | 1688严选 |
| certifiedFactory | 认证工厂 |
| totalEpScoreLv1 | 综合体验分5星 |
| totalEpScoreLv2 | 综合体验分4星 |
| totalEpScoreLv3 | 综合体验分3星 |
| totalEpScoreLv4 | 综合体验分2星 |
| qrr0 | 无品质退款 |
| qrr1 | 品质退款率<1% |
| qrr5 | 品质退款率<5% |
| qrr10 | 品质退款率<10% |
| shipInToday | 当日发货 |
| shipIn24Hours | 24小时发货 |
| shipIn48Hours | 48小时发货 |
| noReason7DReturn | 7天无理由退货 |
| isOnePsale | 一件代发 |
| isOnePsaleFreePost | 一件代发包邮 |
| new7 | 7天内新品 |
| new30 | 30天内新品 |
| isQqyx | 全球严选 |
| JPFL | 日本专线 |
| USFL | 美国专线 |
| KRFL | 韩国专线 |
| VNFL | 越南专线 |
| SAFL | 沙特专线 |
| RUFL | 俄罗斯专线 |
| KZFL | 哈萨克斯坦专线 |
| HKFL | 香港专线 |
| MOFL | 澳门专线 |
| TWFL | 台湾专线 |

### 支持的排序字段

| 字段 | 说明 |
|------|------|
| price | 价格 |
| monthSold | 月销量 |
| rePurchaseRate | 复购率 |

排序方式：`asc`（升序）、`desc`（降序）。格式示例：`{"price":"asc"}`

### 支持的货盘ID

| ID | 说明 |
|----|------|
| 262105288 | 跨境货盘 |
| 262105286 | 跨境货盘 |
| 262105253 | 跨境货盘 |
| 262105281 | 跨境货盘 |
| 262105280 | 跨境货盘 |
| 262105277 | 跨境货盘 |
| 262105276 | 跨境货盘 |
| 262105274 | 跨境货盘 |
| 262105269 | 跨境货盘 |
| 262185282 | 跨境货盘 |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| imageId | string | 上传后的图片ID（分页查询时回传可加速） |
| total | integer | 本页商品数量 |
| totalPage | integer | 总页数 |
| sourceType | string | 来源类型（固定值 "1688"） |
| type | string | 渲染样式（固定值 "productWorkbenches"） |
| columns | array | 渲染列定义 |
| costToken | integer | 消耗 token |
| products | array | 商品列表（详见下方商品字段） |

### 商品字段

| 字段 | 类型 | 说明 |
|------|------|------|
| offerId | string | 商品ID |
| asin | string | 商品编号（同 offerId） |
| imageUrl | string | 商品图片 |
| title | string | 商品标题 |
| price | number | 批发价（元） |
| consignPrice | number | 一件代发价（元） |
| salesQuantity | integer | 月销售件数 |
| estimatedSalesAmount | number | 预估销售额 |
| asinUrl | string | 商品链接 |
| isOnePsale | string | 是否一件代发（是/否） |
| isJxhy | string | 是否精选货源（是/否） |
| sellerIdentities | string | 商家身份（超级工厂/实力商家/诚信通会员） |
| offerIdentities | string | 商品标（严选） |
| repurchaseRate | string | 复购率 |
| tradeScore | string | 商品交易评分 |
| compositeServiceScore | string | 综合服务体验分 |
| sendGoodsAddressText | string | 发货地 |
| deliveryTime | string | 发货时间（24/48小时） |
| quantityBegin | integer | 起批量 |
| hasPromotion | string | 是否有营销活动（是/否） |
| promotionType | string | 营销类型 |
| isPatentProduct | string | 是否专利商品（是/否） |
| isSelect | string | 跨境select货盘标识 |
| currency | string | 币种（固定值 "¥"） |
| sourceType | string | 来源类型（固定值 "1688"） |
| sourceTool | string | 来源工具（固定值 "1688以图搜图"） |
| dataType | string | 数据类型（固定值 "monthlyData"） |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。 |
| 其他非200值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

### 基础以图搜图

```bash
curl -X POST https://tool-gateway.linkfox.com/alibaba1688/imageSearch \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/1.0" \
  -d '{
    "imageUrl": "https://m.media-amazon.com/images/I/719mRAn2VrL._AC_SL1500_.jpg",
    "page": 1,
    "pageSize": 20
  }'
```

### 带筛选和排序

```bash
curl -X POST https://tool-gateway.linkfox.com/alibaba1688/imageSearch \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/1.0" \
  -d '{
    "imageUrl": "https://m.media-amazon.com/images/I/719mRAn2VrL._AC_SL1500_.jpg",
    "page": 1,
    "pageSize": 20,
    "filter": "1688Selection,totalEpScoreLv1,qrr0",
    "sort": "{\"price\":\"desc\"}"
  }'
```

### 分页查询（使用 imageId）

```bash
curl -X POST https://tool-gateway.linkfox.com/alibaba1688/imageSearch \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/1.0" \
  -d '{
    "imageId": "abc123456",
    "page": 2,
    "pageSize": 20
  }'
```

### 价格区间筛选

```bash
curl -X POST https://tool-gateway.linkfox.com/alibaba1688/imageSearch \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/1.0" \
  -d '{
    "imageUrl": "https://m.media-amazon.com/images/I/719mRAn2VrL._AC_SL1500_.jpg",
    "page": 1,
    "pageSize": 20,
    "priceStart": "10",
    "priceEnd": "100"
  }'
```
