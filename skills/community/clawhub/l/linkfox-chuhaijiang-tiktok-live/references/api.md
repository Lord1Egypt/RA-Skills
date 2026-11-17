# TikTok 直播带货情报 API 参考

## 调用规范

- **请求地址（直播搜索）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/lives/search`
- **请求地址（直播详情）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/lives/detail`
- **请求地址（关联商品）**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/lives/related-products`
- **请求方式**：POST，`Content-Type: application/json`
- **认证方式**：Header `Authorization: <api_key>`；api_key 优先从环境变量 `LINKFOX_AGENT_API_KEY` 读取，兼容回退 `LINKFOXAGENT_API_KEY`
- **User-Agent**：`LinkFox-Skill/2.0`
- **透传头**：`SESSION_ID`、`MESSAGE_ID`、`MODE_ID`、`APP_NAME`（未设置时为空串）
- **超时**：150s

`${LINKFOX_TOOL_GATEWAY}` 未设置时，入口脚本回退到 `https://tool-gateway.linkfox.com`。

## 入口脚本与算力

| 能力 | 脚本 | 算力/次 |
|---|---|---:|
| 直播搜索 | `chuhaijiang_live_search.py` | 18 |
| 直播详情 | `chuhaijiang_live_detail.py` | 9 |
| 直播关联商品 | `chuhaijiang_live_related_products.py` | 18 |

三个业务入口脚本默认缓存成功响应 24 小时。缓存按当前工作目录、调用身份、网关、端点和完整请求参数隔离；相同组合命中时输出 `Cache hit`，不会发起新的付费请求。HTTP 或业务失败不写入缓存；业务成功的空结果可以缓存。`--inline` 不绕过缓存；`--no-cache` 会跳过缓存读写并强制发起真实请求，可能再次消耗算力，仅在用户明确同意额外消耗或调试时使用。

## 公共约定

- 网关请求字段使用 camelCase。Java 服务会把这些字段映射到上游 snake_case 参数；脚本调用方不得直接发送 snake_case 别名。
- `country` 为必填小写国家码：`br,de,es,fr,gb,id,it,jp,mx,my,ph,sg,th,us,vn`。
- `id` 是 19 位直播或商品标识时必须以 JSON 字符串传递，避免数值精度损失。
- 金额字段通常为 `{ "unit": "US", "value": 2015752.25 }`。保留原始 `unit` 和 `value`，不要自行换算。

### 公共成功响应

2026-08-29 的真实网关调用中，三个端点均返回 HTTP 200、`errcode=200`、`errmsg=ok` 和非空业务数据：

| 字段 | 类型 | 说明 |
|---|---|---|
| `errcode` | integer | 200 表示成功 |
| `errmsg` | string | 成功时为 `ok` |
| `request_id` | string | 请求追踪 ID |
| `data` | object | 端点业务数据，形状按端点区分 |

入口脚本保留完整原始 JSON，不移除未知业务字段。

## 直播搜索

### 接口信息

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/lives/search`
- **脚本**：`chuhaijiang_live_search.py`
- **成功数据**：`data.items[]`，总数为 `data.total_count`

### 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---:|---|---|
| `country` | string | 是 | - | 小写国家码 |
| `page` | integer | 否 | 1 | 页码，最小 1 |
| `pageSize` | integer | 否 | - | 每页数量，最大 10；Java 路由未声明默认值 |
| `keyword` | string | 否 | - | 搜索关键词 |
| `category` | string | 否 | - | 直播分类 |
| `productCategory` | string | 否 | - | 商品分类 |
| `isLiving` | boolean | 否 | - | 是否正在直播 |
| `isCommercial` | boolean | 否 | - | 是否带货 |
| `minSold` / `maxSold` | number | 否 | - | 最低/最高销量 |
| `minGmv` / `maxGmv` | number | 否 | - | 最低/最高 GMV |
| `minAudience` / `maxAudience` | number | 否 | - | 最低/最高观众数 |
| `sort` | string | 否 | `gmv:desc` | `field:asc` 或 `field:desc`；`gmv:desc` 已真实验证 |

```bash
python scripts/chuhaijiang_live_search.py '{"country":"us","isCommercial":true,"sort":"gmv:desc","page":1,"pageSize":3}'
```

### 响应字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `data.total_count` | integer | 匹配总数 |
| `data.items[].id` | string | 直播房间 ID；详情和关联商品继续使用此值 |
| `title` / `room_link` | string | 直播标题 / 公共直播链接 |
| `user_id` / `user_unique_id` / `user_nickname` | string | 主播 ID、账号和昵称 |
| `user_category_label` | string | 主播分类标签 |
| `country_code` | string | 记录实际国家代码 |
| `start_time` / `end_time` | integer | 毫秒时间戳 |
| `cover` | object | `url` 与 `thumb_url` |
| `product_count` / `total_sold_count` | integer | 商品数 / 总销量 |
| `total_user` / `max_user_count` | integer | 总观众 / 峰值观众 |
| `new_follow_count` | integer | 新增粉丝数 |
| `gmv` / `gpm` | object | 带 `unit`、`value` 的 GMV / GPM |
| `opm` | number | 每千观众订单数 |
| `most_product_category_label` | string | 主要商品分类标签 |

字段可能缺失或为 `null`；脚本保留完整原始 JSON。

## 直播详情

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/lives/detail`
- **脚本**：`chuhaijiang_live_detail.py`
- **成功数据**：基础信息为 `data.items[]`；请求 `include=core` 时另有 `data.core.items[]`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `country` | string | 是 | 小写国家码 |
| `id` | string | 是 | 直播房间 ID |
| `include` | string | 否 | 可选扩展 `core`；多个值时用英文逗号分隔 |

```bash
python scripts/chuhaijiang_live_detail.py '{"country":"us","id":"7643101948819835678","include":"core"}'
```

### 基础详情 `data.items[]`

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | string | 直播房间 ID |
| `title` / `room_link` | string | 标题 / 公共链接 |
| `country_code` | string | 记录国家代码 |
| `start_time` / `end_time` | integer | 毫秒时间戳 |
| `cover` / `user_avatar` | object | `url` 与 `thumb_url` |
| `user_id` / `user_nickname` | string | 主播 ID / 昵称 |
| `user_follower_count` / `user_live_count` | integer | 主播粉丝数 / 直播场次 |
| `user_avg_audience_count` / `user_avg_max_audience_count` | number | 主播历史平均观众 / 平均峰值观众 |
| `most_product_category_label` | string | 主要商品分类标签 |

### 核心指标 `data.core.items[]`

`include=core` 的真实响应包含 `id`、`core_room_id`、`core_country_code`、`core_gmv`、`core_gpm`、`core_avg_price`、`core_product_count`、`core_sold_product_id_count`、`core_total_sold_count`、`core_total_user`、`core_avg_online_viewer`、`core_max_user_count`、`core_new_follow_count` 和 `core_follower_conversion_rate`。

`core_gmv`、`core_gpm`、`core_avg_price` 是金额对象；`core_follower_conversion_rate` 是小数比率，例如 `0.0007` 表示 `0.07%`。

## 直播关联商品

- **地址**：`${LINKFOX_TOOL_GATEWAY}/chuhaijiang/lives/related-products`
- **脚本**：`chuhaijiang_live_related_products.py`
- **成功数据**：`data.items[]`，总数为 `data.total_count`

### 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|---|---|---:|---|---|
| `country` | string | 是 | - | 小写国家码 |
| `id` | string | 是 | - | 直播房间 ID |
| `page` | integer | 否 | 1 | 页码，最小 1 |
| `pageSize` | integer | 否 | - | 每页数量，最大 10；Java 路由未声明默认值 |

```bash
python scripts/chuhaijiang_live_related_products.py '{"country":"us","id":"7643101948819835678","page":1,"pageSize":3}'
```

### 响应字段 `data.items[]`

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` / `tiktok_live_detail_product_id` | string | 商品 ID |
| `tiktok_live_detail_product_title` | string | 商品标题 |
| `tiktok_live_detail_product_images` | object | 商品图 `url` / `thumb_url` |
| `tiktok_live_detail_product_country_code` | string | 商品国家代码 |
| `tiktok_live_detail_product_floor_price` / `ceiling_price` | object | 最低/最高价，含 `unit`、`value` |
| `tiktok_live_detail_product_sold_count` | integer | 直播关联销量 |
| `tiktok_live_detail_product_gmv` | object | 直播关联 GMV，含 `unit`、`value` |
| `tiktok_live_detail_product_commission_rate_num` | number | 佣金率小数；字段可能缺失 |
| `tiktok_live_detail_product_conversion_rate` | number | 转化率小数 |
| `tiktok_live_detail_product_seller_id` / `seller_name` | string | 卖家 ID / 名称 |
| `tiktok_live_detail_product_seller_avatar` | object | 卖家头像 |
| `tiktok_live_detail_product_seller_info` | array | 卖家说明文本 |
| `tiktok_live_detail_product_l1_category` / `l2_category` / `l3_category` | string | 商品分类标签 |
| `tiktok_live_detail_product_seller_category_name_label` | string | 卖家分类标签 |

## 错误码

| `errcode` / HTTP | 含义 | 处理建议 |
|---|---|---|
| 200 | 成功 | 按当前端点的 `data` 结构解析 |
| 401 | 认证失败 | 按 `SKILL.md` 的“解决认证和算力问题”处理 |
| 402 | 算力或余额不足 | 停止重试并引导用户处理余额 |
| 501 | 参数校验失败 | 根据 `errmsg` 修正字段；不得自动连续试探付费接口 |
| 其他非 200 | 业务异常 | 回显 `errmsg` 并停止；需要重试时先向用户说明可能再次计费并取得同意 |

入口脚本会把 HTTP 错误和网关 JSON 错误作为结构化内容回显，不应出现未处理的 Python 堆栈。

## curl 示例

```bash
curl -X POST "${LINKFOX_TOOL_GATEWAY}/chuhaijiang/lives/search" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY:-$LINKFOXAGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -H "SESSION_ID: ${SESSION_ID}" \
  -H "MESSAGE_ID: ${MESSAGE_ID}" \
  -H "MODE_ID: ${MODE_ID}" \
  -H "APP_NAME: ${APP_NAME}" \
  -d '{"country":"us","isCommercial":true,"sort":"gmv:desc","page":1,"pageSize":3}'
```

---

## Feedback API

此端点独立于工具网关。仅在用户明确要求提交反馈，或发现问题后明确授权提交时调用。提交前应概括并脱敏，不得发送原始用户消息、无关任务上下文、手机号或任何凭证。

- **POST** `https://skill-api.linkfox.com/api/v1/public/feedback`
- **Content-Type**：`application/json`

```json
{
  "skillName": "linkfox-chuhaijiang-tiktok-live",
  "sentiment": "NEUTRAL",
  "category": "SUGGESTION",
  "content": "Describe the user intent, actual behavior, and improvement clearly."
}
```

`sentiment` 取 `POSITIVE`、`NEUTRAL` 或 `NEGATIVE`；`category` 取 `BUG`、`COMPLAINT`、`SUGGESTION` 或 `OTHER`。
