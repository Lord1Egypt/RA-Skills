---
name: linkfox-echotik-product-video
description: 查询TikTok商品的带货视频数据，包括播放、互动、视频销量及GMV，用于分析视频营销与达人带货效果。
---

# EchoTik - TikTok 商品视频

本技能用于查询 TikTok Shop 商品关联的带货视频数据，帮助卖家分析视频营销表现，识别有效的达人内容策略。参数与响应字段详见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 查询指定 TikTok 商品的关联带货视频列表。
- 展示视频互动指标（播放、点赞、评论、分享、收藏）、估算销量与 GMV、视频元数据（时长、分辨率、发布日期）以及创作者（达人）ID。
- 支持按播放量、点赞数、分享数、视频销量、视频 GMV、发布时间排序。
- 支持按达人 ID、发布时间区间筛选。

### ❌ 边界与限制

- **必填输入**：必须提供 `productId`。商品 ID 可从 `linkfox-echotik-product-search` 或 `linkfox-echotik-new-product-rank` 获取。
- **分页上限**：`pageSize` 须为 10 的倍数，最大 100；后端按每页 10 条分批拉取后合并。
- **估算数据**：视频销量与 GMV 为估算值，非精确统计。
- **播放地址时效**：`playAddr` 字段可能快速过期，分享优先使用 `officialUrl`。
- **不在范围内**：商品搜索（用 `linkfox-echotik-product-search`）；TikTok 新品排名（用 `linkfox-echotik-new-product-rank`）；达人档案分析（粉丝数、简介、整体表现）；TikTok 直播数据；视频内容创作或剪辑建议；TikTok 广告/广告活动管理；非 TikTok 平台视频数据。

## 核心概念

本工具检索与特定 TikTok 商品关联的带货视频列表。每条视频记录包含互动指标（播放、点赞、评论、分享、收藏）、估算销量归因（视频销量与 GMV）、视频元数据（时长、分辨率、发布日期）及创作者（达人）ID，帮助卖家理解哪些视频为商品带来了最多销量、哪些内容模式最有效。

- **排序字段**：可按播放量（1）、点赞数（2）、分享数（3）、视频销量（4）、视频 GMV（5）、发布时间（6）排序。
- **分页**：`pageSize` 须为 10 的倍数，最大 100；后端按每页 10 条分批拉取后合并。

## 调用方式

- **API 端点**：`POST /echotik/listProductVideo`（完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/echotik_list_product_video.py '<JSON 参数>' [--inline]`
- **成本约束**：本工具会消耗积分；同一会话同一参数组合默认只调用一次，脚本带 24h 本地缓存。失败/空结果不得自动换关键词、翻页或改邮编连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-echotik-product-video-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

**1. 查询某商品播放量最高的视频**
```json
{
  "productId": "1729382310407603945",
  "productVideoSortField": 1,
  "sortType": 1,
  "pageSize": 20
}
```

**2. 查找转化最高的视频（按视频销量）**
```json
{
  "productId": "1729382310407603945",
  "productVideoSortField": 4,
  "sortType": 1,
  "pageSize": 20
}
```

**3. 查询某商品下指定达人的视频**
```json
{
  "productId": "1729382310407603945",
  "userId": "7234567890123456789",
  "productVideoSortField": 1,
  "sortType": 1
}
```

**4. 查询时间区间内的视频（按 GMV 排序）**
```json
{
  "productId": "1729382310407603945",
  "minCreateTime": 1717200000,
  "maxCreateTime": 1719792000,
  "productVideoSortField": 5,
  "sortType": 1
}
```

**5. 按发布时间排序（最新优先）**
```json
{
  "productId": "1729382310407603945",
  "productVideoSortField": 6,
  "sortType": 1,
  "pageSize": 50
}
```

## 展示规则

1. **以表格呈现数据**：展示视频描述（过长截断）、播放量、点赞、评论、分享、视频销量、视频 GMV、发布日期、达人 ID。
2. **附原始链接**：`officialUrl` 可用时提供，便于用户在 TikTok 观看视频。
3. **估算值提示**：视频销量与 GMV 为估算值，提醒用户这些是近似数据。
4. **封面图**：存在 `coverUrl` 时提及，告知用户视频缩略图可用。
5. **时长格式化**：将 `duration`（秒）转为可读格式（如 90 秒显示为 "1:30"）。
6. **话题标签**：存在 `hashTag` 时展示，帮助用户理解内容主题。
7. **播放地址时效**：`playAddr` 字段可能快速过期；分享优先使用 `officialUrl`。

## 用户表达与场景速查

**适用** —— TikTok 商品带货视频查询：

| 用户说 | 场景 |
|--------|------|
| "看看这个 TikTok 商品的带货视频" | 按 productId 查询视频 |
| "哪些视频给这个商品带来最多销量" | 按视频销量排序（字段 4） |
| "有哪些达人在推这个商品" | 通用视频列表查询 |
| "看某位达人推这个商品的视频" | 按 userId 筛选 |
| "这个商品最近的带货视频" | 按时间区间筛选或按发布时间排序 |
| "这个 TikTok 商品 GMV 最高的视频是哪些" | 按视频 GMV 排序（字段 5） |
| "分析这个商品的视频营销表现" | 综合视频列表查询 |

不适用场景见上方【能力边界】。

当用户提到"TikTok 视频"时，需判断其想要的是某具体商品关联的视频（本技能适用）还是通用的 TikTok 视频分析（不适用）。若用户提到商品 ID 或询问"有哪些视频在推商品 X"，则适用本技能；若仅泛泛询问热门视频而无商品上下文，则不适用。

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

# EchoTik-TikTok商品视频 API 参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/echotik/listProductVideo`
- **请求方式**：POST，Content-Type: application/json
- **认证方式**：Header `Authorization: <api_key>`，api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）

## 请求参数

POST Body（JSON）：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| productId | string | 是 | 商品ID。最大长度 1000 |
| userId | string | 否 | 达人ID，用于筛选特定达人的带货视频。最大长度 1000 |
| productVideoSortField | integer | 否 | 排序字段：1=播放量、2=点赞数、3=分享数、4=视频销量、5=视频销售GMV、6=发布时间。默认 `1` |
| sortType | integer | 否 | 排序方式：0=升序、1=降序。默认 `1` |
| minCreateTime | integer | 否 | 视频发布时间区间-开始（秒级时间戳） |
| maxCreateTime | integer | 否 | 视频发布时间区间-结束（秒级时间戳） |
| pageNum | integer | 否 | 分页页码。默认 `1` |
| pageSize | integer | 否 | 分页条数（须为10的倍数，最大100；官方接口单页上限10，内部按10每页多次拉取后合并）。默认 `50` |

## 响应结构

| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 记录数 |
| data | array | 视频列表（见下方视频对象） |
| columns | array | 渲染的列 |
| type | string | 渲染的样式 |
| costToken | integer | 消耗token |

### 视频对象

| 字段 | 类型 | 说明 |
|------|------|------|
| videoId | string | 视频ID |
| productId | string | 商品ID |
| userId | string | 达人ID |
| videoDesc | string | 视频描述 |
| officialUrl | string | TikTok官方视频地址 |
| covet | integer | 分享数 |
| totalFavoritesCnt | integer | 收藏数 |
| totalVideoSaleCnt | integer | 视频销量（估算） |
| totalVideoSaleGmvAmt | integer | 视频销售GMV（估算） |
| hashTag | string | 话题标签 |
| createDate | string (date) | 视频发布日期 |
| region | string | 区域代码 |
| sourceTool | string | 来源工具 |
| sourceType | string | 商品来源 |

## 错误码

正常情况下，接口的 HTTP 状态码均为 200，业务的成功与否通过响应体中的 errorCode 字段区分（errorCode = 200 表示成功，其他值表示业务错误）。当遇到未授权等情况时，HTTP 状态码为 401，且对应的 errorCode 也是 401。

| errcode | 含义 | 处理建议 |
|---------|------|----------|
| 200 | 成功 | 正常解析业务字段 |
| 401 | 认证失败 | HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 402 | 积分不足 | HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。|
| 其他非200值 | 业务异常 | 参考 `errmsg` 字段获取具体错误原因 |

错误响应示例：

```json
{
    "errcode": 401,
    "errmsg": "authorized error"
}
```

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/echotik/listProductVideo \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "productId": "1729382310407603945",
    "productVideoSortField": 1,
    "sortType": 1,
    "pageSize": 20
  }'
```
