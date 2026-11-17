# LinkedIn Content & Ads / 领英 内容 & 广告

Base URL: `https://www.aconfig.cn` · Auth: `Authorization: Bearer $MAXHUB_API_KEY`

## 本文件覆盖
帖子详情、评论、回复、点赞反应、转发、帖子搜索、群组信息与帖子、广告搜索与详情。含 Web 和 Web V2 双版本。**post_id 多在本文件首步产出**。

## 端点索引 (Endpoint Index)

### Web API

| ID | 推荐度 | 一句话用途 | Method | Path | Risk |
|----|-------|----------|--------|------|------|
| web_get_post_detail | ⭐⭐⭐ 首选 | 用 post_id 取帖子详情（**链式起点**） | GET | /api/v1/linkedin/web/get_post_detail | low |
| web_get_post_comments | ⭐⭐⭐ 首选 | 用 post_id 取帖子评论 | GET | /api/v1/linkedin/web/get_post_comments | low |
| web_get_post_reactions | ⭐⭐ 条件 | 用 post_id 取点赞反应 | GET | /api/v1/linkedin/web/get_post_reactions | low |
| web_get_post_reposts | ⭐⭐ 条件 | 用 post_id 取转发 | GET | /api/v1/linkedin/web/get_post_reposts | low |
| web_get_comments_replies | ⭐⭐ 条件 | 用 post_id+comment_id 取回复 | GET | /api/v1/linkedin/web/get_comments_replies | low |
| web_search_posts | ⭐⭐⭐ 首选 | 搜索帖子（**内容冷启动入口**） | GET | /api/v1/linkedin/web/search_posts | low |
| web_get_group_info | ⭐⭐ 条件 | 用 group_id 取群组信息 | GET | /api/v1/linkedin/web/get_group_info | low |
| web_get_group_posts | ⭐⭐ 条件 | 用 group_id 取群组帖子 | GET | /api/v1/linkedin/web/get_group_posts | low |
| web_search_ads | ⭐⭐ 条件 | 搜索广告 | GET | /api/v1/linkedin/web/search_ads | low |
| web_get_ad_detail | ⭐⭐ 条件 | 用 ad_id 取广告详情 | GET | /api/v1/linkedin/web/get_ad_detail | low |

### Web V2 API

| ID | 推荐度 | 一句话用途 | Method | Path | Risk |
|----|-------|----------|--------|------|------|
| v2_get_post_detail | ⭐⭐⭐ 首选 | 用 url 取帖子详情（V2，**推荐**） | GET | /api/v1/linkedin/web_v2/get_post_detail | low |

## 链式调用图谱 (Chain Recipes)

| 用户目标 | 链路 | 字段流 | 中间步失败时的容错 |
|---------|------|-------|-------------------|
| 看帖子+评论 | web_get_post_detail → web_get_post_comments | `$.data.post_id` → `post_id` | 第 1 步失败：STOP；第 2 步失败：返回详情+"评论暂不可取" |
| 看评论+回复 | web_get_post_comments → web_get_comments_replies | `$.data.comments[].comment_id` → `comment_id` | 第 2 步失败：返回已有评论 |
| 搜索帖子→详情 | web_search_posts → web_get_post_detail | `$.data.posts[].post_id` → `post_id` | 第 1 步空：STOP |
| 帖子→作者 | web_get_post_detail → user.md 的 web_get_user_profile | `$.data.author.username` → `username` | 跨文件链路 |
| 广告搜索→详情 | web_search_ads → web_get_ad_detail | `$.data.ads[].ad_id` → `ad_id` | 第 1 步空：STOP |

## 跨 reference 链路 (In-Chain)
- **流入本文件**：`user.md` 的 `web_get_user_posts` 输出 `post_id` → 本文件
- **流入本文件**：`company.md` 的 `web_get_company_posts` 输出 `post_id` → 本文件
- **流入本文件**：`user.md` 的 `web_get_user_interests_groups` 输出 `group_id` → 本文件 `web_get_group_info`
- **流出本文件**：`web_get_post_detail` 输出 `$.data.author.username` → `user.md`
- **流出本文件**：`web_get_post_comments` 输出评论者 username → `user.md`

## 错误处理契约 (Error Contract)

> **完整 HTTP 状态码语义与决策表见 [`param-mappings.md` § 3](./param-mappings.md#3-全-skill-错误处理总览-error-handling-overview)**

- 通用错误处理见 param-mappings.md
- **特别注意**：Web 版用 `post_id`（数字 ID），V2 版用 `url`（帖子 URL），不可混用
- `web_get_comments_replies` 需要 3 个必填参数：`post_id` + `comment_id` + `previous_replies_token`
- `web_search_ads` 的 `keyword` 和 `advertiser_name` 至少提供一个

---

## 端点详情

### web_get_post_detail — 获取帖子详情 (Web)

**Full path:** `/api/v1/linkedin/web/get_post_detail`
**Method:** GET · **Risk:** low

#### 用途
用 post_id 获取 LinkedIn 帖子详情。**链式起点**——产出作者信息供后续 user 系端点使用。

#### 何时使用 / 不使用
- ✅ 已知 post_id（纯数字）
- ✅ 链式起点：post_id → 评论/反应/转发
- ❌ 有帖子 URL → 用 V2 版 `v2_get_post_detail`

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| post_id | string | yes | — | 帖子 ID（纯数字） |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| post_id | `$.data.post_id` | 帖子 ID（回显） | web_get_post_comments / web_get_post_reactions / web_get_post_reposts |
| author.username | `$.data.author.username` | 作者用户名 | user.md |

---

### v2_get_post_detail — 获取帖子详情 (V2)

**Full path:** `/api/v1/linkedin/web_v2/get_post_detail`
**Method:** GET · **Risk:** low

#### 用途
用 url 获取帖子详情（V2 版本，**推荐**）。支持多种 URL 格式。

#### 何时使用 / 不使用
- ✅ 已知帖子 URL（**推荐**）
- ✅ 链式起点：url → 详情
- ❌ 有纯数字 post_id → 用 Web 版 `web_get_post_detail`

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| url | string | yes | — | 帖子 URL |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| author | `$.data.author` | 作者信息 | user.md |

---

### web_search_posts — 搜索帖子 (Web)

**Full path:** `/api/v1/linkedin/web/search_posts`
**Method:** GET · **Risk:** low

#### 用途
按关键词搜索 LinkedIn 帖子。**内容冷启动入口**——用户没有具体 post_id 时，可从此端点采集。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| keyword | string | yes | — | 搜索关键词 |
| page | string | no | — | 页码（默认 1） |
| date_posted | string | no | enum: past_month, past_week, past_24h | 发布时间过滤 |
| sort_by | string | no | enum: date_posted, relevance | 排序方式 |
| from_member | string | no | — | 按成员过滤（逗号分隔） |
| from_company | string | no | — | 按公司过滤（逗号分隔） |
| content_type | string | no | enum: videos, photos, jobs, live_videos, documents, collaborative_articles | 内容类型 |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| posts[].post_id | `$.data.posts[].post_id` | 帖子 ID | web_get_post_detail |

---

### 其他端点（简要）

#### Web 版

| 端点 ID | 路径 | 必填参数 | 可选参数 | 用途 |
|---------|------|---------|---------|------|
| web_get_post_comments | /api/v1/linkedin/web/get_post_comments | post_id | page, sort_order(relevance/recent), post_type(activity/ugc) | 取帖子评论 |
| web_get_post_reactions | /api/v1/linkedin/web/get_post_reactions | post_id | page, type(all/like/praise/empathy/appreciation/interest) | 取点赞反应 |
| web_get_post_reposts | /api/v1/linkedin/web/get_post_reposts | post_id | page, pagination_token | 取转发 |
| web_get_comments_replies | /api/v1/linkedin/web/get_comments_replies | post_id, comment_id, previous_replies_token | — | 取评论回复 |
| web_get_group_info | /api/v1/linkedin/web/get_group_info | group_id | — | 取群组信息 |
| web_get_group_posts | /api/v1/linkedin/web/get_group_posts | group_id | page | 取群组帖子 |
| web_search_ads | /api/v1/linkedin/web/search_ads | — | keyword, advertiser_name, country, date, pagination_token | 搜索广告 |
| web_get_ad_detail | /api/v1/linkedin/web/get_ad_detail | ad_id | — | 取广告详情 |
