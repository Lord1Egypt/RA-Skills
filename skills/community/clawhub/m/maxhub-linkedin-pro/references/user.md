# LinkedIn User & People / 领英 用户 & 人脉

Base URL: `https://www.aconfig.cn` · Auth: `Authorization: Bearer $MAXHUB_API_KEY`

## 本文件覆盖
用户资料、帖子、评论、联系信息、推荐信、工作经历、技能、教育背景、出版物、认证、荣誉、兴趣、点赞反应、志愿者经历、粉丝/连接统计、人脉搜索。含 Web 和 Web V2 双版本。**username 与 urn 多在本文件首步产出**，是其他链式调用的常见起点。

## 端点索引 (Endpoint Index)

### Web API

| ID | 推荐度 | 一句话用途 | Method | Path | Risk |
|----|-------|----------|--------|------|------|
| web_get_user_profile | ⭐⭐⭐ 首选 | 用 username 取用户资料（**链式起点，产出 urn**） | GET | /api/v1/linkedin/web/get_user_profile | low |
| web_get_user_posts | ⭐⭐ 条件 | 用 urn 取用户帖子 | GET | /api/v1/linkedin/web/get_user_posts | low |
| web_get_user_comments | ⭐⭐ 条件 | 用 urn 取用户评论 | GET | /api/v1/linkedin/web/get_user_comments | low |
| web_get_user_recommendations | ⭐⭐ 条件 | 用 urn 取推荐信 | GET | /api/v1/linkedin/web/get_user_recommendations | low |
| web_get_user_videos | ⭐ 条件 | 用 urn 取用户视频 | GET | /api/v1/linkedin/web/get_user_videos | low |
| web_get_user_images | ⭐ 条件 | 用 urn 取用户图片 | GET | /api/v1/linkedin/web/get_user_images | low |
| web_get_user_about | ⭐ 条件 | 用 urn 取用户简介 | GET | /api/v1/linkedin/web/get_user_about | low |
| web_get_user_follower_and_connection | ⭐⭐ 条件 | 用 username 取粉丝/连接数 | GET | /api/v1/linkedin/web/get_user_follower_and_connection | low |
| web_get_user_experience | ⭐⭐ 条件 | 用 urn 取工作经历 | GET | /api/v1/linkedin/web/get_user_experience | low |
| web_get_user_skills | ⭐⭐ 条件 | 用 urn 取技能 | GET | /api/v1/linkedin/web/get_user_skills | low |
| web_get_user_educations | ⭐⭐ 条件 | 用 urn 取教育背景 | GET | /api/v1/linkedin/web/get_user_educations | low |
| web_get_user_publications | ⭐ 条件 | 用 urn 取出版物 | GET | /api/v1/linkedin/web/get_user_publications | low |
| web_get_user_certifications | ⭐ 条件 | 用 urn 取认证 | GET | /api/v1/linkedin/web/get_user_certifications | low |
| web_get_user_honors | ⭐ 条件 | 用 urn 取荣誉奖项 | GET | /api/v1/linkedin/web/get_user_honors | low |
| web_get_user_interests_groups | ⭐ 条件 | 用 urn 取感兴趣的群组 | GET | /api/v1/linkedin/web/get_user_interests_groups | low |
| web_get_user_interests_companies | ⭐ 条件 | 用 urn 取感兴趣的公司 | GET | /api/v1/linkedin/web/get_user_interests_companies | low |
| web_get_user_reactions | ⭐ 条件 | 用 urn 取点赞反应 | GET | /api/v1/linkedin/web/get_user_reactions | low |
| web_get_user_volunteers | ⭐ 条件 | 用 urn 取志愿者经历 | GET | /api/v1/linkedin/web/get_user_volunteers | low |
| web_search_people | ⭐⭐⭐ 首选 | 搜索用户（**username→urn 入口**） | GET | /api/v1/linkedin/web/search_people | low |
| web_search_location | ⭐⭐ 辅助 | 搜索地理位置（辅助搜索） | GET | /api/v1/linkedin/web/search_location | low |
| web_search_schools | ⭐⭐ 辅助 | 搜索学校（辅助搜索） | GET | /api/v1/linkedin/web/search_schools | low |

### Web V2 API

| ID | 推荐度 | 一句话用途 | Method | Path | Risk |
|----|-------|----------|--------|------|------|
| v2_get_user_profile | ⭐⭐⭐ 首选 | 用 url 取用户主页（V2，**推荐**） | GET | /api/v1/linkedin/web_v2/get_user_profile | low |
| v2_get_user_posts | ⭐⭐⭐ 首选 | 用 url 取用户帖子（V2） | GET | /api/v1/linkedin/web_v2/get_user_posts | low |

## 链式调用图谱 (Chain Recipes)

| 用户目标 | 链路 | 字段流 | 中间步失败时的容错 |
|---------|------|-------|-------------------|
| 用户名→完整资料 | web_get_user_profile → 各子节端点 | `$.data.urn` → `urn` | 第 1 步失败：STOP |
| 用户名→帖子 | v2_get_user_posts（直接用 url） | url 复用 | 失败：降级 web_get_user_posts（需先取 urn） |
| 搜索人→资料 | web_search_people → web_get_user_profile | `$.data.people[].public_identifier` → `username` | 第 1 步空：STOP |
| 搜索位置→搜索职位 | web_search_location → web_search_jobs | `$.data.locations[].geocode` → `geocode` | 第 1 步失败：用户可手动提供位置 |
| 用户帖子→帖子详情 | web_get_user_posts → content.md 的 web_get_post_detail | `$.data.posts[].post_id` → `post_id` | 跨文件链路 |

## 跨 reference 链路 (In-Chain)
- **流入本文件**：`content.md` 的 `web_get_post_detail` 输出 `$.data.author.username` → 本文件 user 系端点
- **流入本文件**：`company.md` 的 `web_get_company_people` 输出用户 username → 本文件
- **流出本文件**：`web_get_user_posts` / `v2_get_user_posts` 输出 `post_id` → `content.md`
- **流出本文件**：`web_get_user_interests_groups` 输出 `group_id` → `content.md` 的 `web_get_group_info`
- **流出本文件**：`web_get_user_interests_companies` 输出公司信息 → `company.md`

## 错误处理契约 (Error Contract)

> **完整 HTTP 状态码语义与决策表见 [`param-mappings.md` § 3](./param-mappings.md#3-全-skill-错误处理总览-error-handling-overview)**

### 路径错误（404 / 410）
- 必须先做防臆造自检（详见 [`param-mappings.md` § 3.1 (A)](./param-mappings.md#a-收到-404-时的自检清单-️-防路径臆造)）
- 自检通过后 STOP 并报告"资源不存在"
- 禁止：改路径段 / 切换版本前缀 / 拼接新路径

### 参数错误（400 / 422）
- 必须先做防臆造自检（详见 [`param-mappings.md` § 3.1 (B)](./param-mappings.md#b-收到-400--422-时的自检清单-️-防参数臆造)）
- **特别注意**：Web 版用 `urn` / `username`，V2 版用 `url`，不可混用
- 自检通过后修正参数重试 ≤ 1 次

### 鉴权 / 余额 / 权限 / 限流 / 上游故障 / 网络超时 / 业务错误
- 通用处理见 [`param-mappings.md` § 3](./param-mappings.md#3-全-skill-错误处理总览-error-handling-overview)

---

## 端点详情

### web_get_user_profile — 获取用户资料 (Web)

**Full path:** `/api/v1/linkedin/web/get_user_profile`
**Method:** GET · **Risk:** low

#### 用途
用 username 获取 LinkedIn 用户资料。**链式起点**——产出 `urn` 供后续 Web 版子节端点使用。

#### 何时使用 / 不使用
- ✅ 已知 username，需取完整资料或 urn
- ✅ 链式起点：username → urn
- ❌ 只需粉丝数 → 用 `web_get_user_follower_and_connection`（更轻量）
- ❌ 已知 urn 且只需子节 → 直接调子节端点
- ❌ 推荐用 V2 版 `v2_get_user_profile`（字段更丰富，用 url）

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| username | string | yes | — | LinkedIn 用户名（URL slug） |
| include_follower_and_connection | string | no | — | 包含粉丝/连接数（+1 请求） |
| include_experiences | string | no | — | 包含工作经历（+1 请求） |
| include_skills | string | no | — | 包含技能（+1 请求） |
| include_certifications | string | no | — | 包含认证（+1 请求） |
| include_publications | string | no | — | 包含出版物（+1 请求） |
| include_educations | string | no | — | 包含教育背景（+1 请求） |
| include_volunteers | string | no | — | 包含志愿者经历（+1 请求） |
| include_honors | string | no | — | 包含荣誉奖项（+1 请求） |
| include_interests | string | no | — | 包含兴趣（+1 请求） |
| include_bio | string | no | — | 包含个人简介（+1 请求） |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| urn | `$.data.urn` | 用户 URN | Web 版全部 urn 系端点 |
| public_identifier | `$.data.public_identifier` | 用户名（回显） | 本文件 username 系端点 |

#### 错误处理 (ERR)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 404 | 用户不存在 | STOP | 0 | — |
| 5xx | 上游故障 | 等 3s 重试 | ≤1 次 | 降级 v2_get_user_profile |

---

### web_search_people — 搜索用户 (Web)

**Full path:** `/api/v1/linkedin/web/search_people`
**Method:** GET · **Risk:** low

#### 用途
按姓名/职位/公司/学校等条件搜索 LinkedIn 用户。**username→urn 入口**。

#### 何时使用 / 不使用
- ✅ 用户给出人名但不知 username
- ✅ 链式起点：搜索 → username → profile
- ❌ 已知 username → 直接 web_get_user_profile
- ❌ 搜索公司 → company.md

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| name | string | no | — | 搜索关键词 |
| first_name | string | no | — | 名 |
| last_name | string | no | — | 姓 |
| title | string | no | — | 职位 |
| company | string | no | — | 公司 |
| school | string | no | — | 学校 |
| page | string | no | — | 页码（默认 1） |
| geocode_location | string | no | — | 地理位置代码（从 web_search_location 获取） |
| current_company | string | no | — | 当前公司 ID |
| profile_language | string | no | — | 资料语言 |
| industry | string | no | — | 行业 ID |
| service_category | string | no | — | 服务类别 ID |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| people[].public_identifier | `$.data.people[].public_identifier` | 用户名 | web_get_user_profile |

#### 错误处理 (ERR)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 空结果 | 未命中 | STOP，告知用户 | 0 | — |

---

### v2_get_user_profile — 获取用户主页 (V2)

**Full path:** `/api/v1/linkedin/web_v2/get_user_profile`
**Method:** GET · **Risk:** low

#### 用途
用 url 获取 LinkedIn 用户主页资料（V2 版本，**推荐优先使用**）。支持 include 参数一次性附带多个子节。

#### 何时使用 / 不使用
- ✅ 已知用户 URL，需取完整资料（**推荐**）
- ✅ 需要一次性获取多个子节（通过 include 参数）
- ❌ 只需单个子节 → 用 Web 版专用端点（如 web_get_user_experience）

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| url | string | yes | — | LinkedIn 用户主页 URL |
| include_follower_and_connection | string | no | — | 附带粉丝/连接数（+1 请求） |
| include_experiences | string | no | — | 附带工作经历 |
| include_skills | string | no | — | 附带技能 |
| include_certifications | string | no | — | 附带认证 |
| include_publications | string | no | — | 附带出版物 |
| include_educations | string | no | — | 附带教育背景 |
| include_volunteers | string | no | — | 附带志愿者经历 |
| include_honors | string | no | — | 附带荣誉奖项 |
| include_interests | string | no | — | 附带兴趣 |
| include_bio | string | no | — | 附带简介 |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| profile | `$.data.profile` | 主资料对象 | 仅展示 |
| 各 include 子节 | `$.data.<section>` | 子节数据块 | 仅展示 |

#### 错误处理 (ERR)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 404 | 用户不存在 | STOP | 0 | — |
| 5xx | 上游故障 | 等 3s 重试 | ≤1 次 | 降级 web_get_user_profile |

---

### 其他 Web 版子节端点（简要）

以下端点均用 `urn`（从 `web_get_user_profile` 获取）作为必填参数，`page` 为可选分页参数：

| 端点 ID | 路径 | 用途 |
|---------|------|------|
| web_get_user_posts | /api/v1/linkedin/web/get_user_posts | 用 urn 取用户帖子 |
| web_get_user_comments | /api/v1/linkedin/web/get_user_comments | 用 urn 取用户评论 |
| web_get_user_recommendations | /api/v1/linkedin/web/get_user_recommendations | 用 urn 取推荐信（可选 type: received/given） |
| web_get_user_videos | /api/v1/linkedin/web/get_user_videos | 用 urn 取用户视频 |
| web_get_user_images | /api/v1/linkedin/web/get_user_images | 用 urn 取用户图片 |
| web_get_user_about | /api/v1/linkedin/web/get_user_about | 用 urn 取用户简介 |
| web_get_user_experience | /api/v1/linkedin/web/get_user_experience | 用 urn 取工作经历 |
| web_get_user_skills | /api/v1/linkedin/web/get_user_skills | 用 urn 取技能 |
| web_get_user_educations | /api/v1/linkedin/web/get_user_educations | 用 urn 取教育背景 |
| web_get_user_publications | /api/v1/linkedin/web/get_user_publications | 用 urn 取出版物 |
| web_get_user_certifications | /api/v1/linkedin/web/get_user_certifications | 用 urn 取认证 |
| web_get_user_honors | /api/v1/linkedin/web/get_user_honors | 用 urn 取荣誉奖项 |
| web_get_user_interests_groups | /api/v1/linkedin/web/get_user_interests_groups | 用 urn 取感兴趣的群组 |
| web_get_user_interests_companies | /api/v1/linkedin/web/get_user_interests_companies | 用 urn 取感兴趣的公司 |
| web_get_user_reactions | /api/v1/linkedin/web/get_user_reactions | 用 urn 取点赞反应 |
| web_get_user_volunteers | /api/v1/linkedin/web/get_user_volunteers | 用 urn 取志愿者经历 |

### 辅助搜索端点

| 端点 ID | 路径 | 用途 |
|---------|------|------|
| web_get_user_follower_and_connection | /api/v1/linkedin/web/get_user_follower_and_connection | 用 username 取粉丝/连接数 |
| web_search_location | /api/v1/linkedin/web/search_location | 用 keyword 搜索地理位置 |
| web_search_schools | /api/v1/linkedin/web/search_schools | 用 keyword 搜索学校 |
