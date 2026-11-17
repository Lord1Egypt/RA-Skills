# Douyin Douplus / 抖音 DOU+ 推广

Base URL: `https://www.aconfig.cn` · Auth: `Authorization: Bearer $MAXHUB_API_KEY`

## 本文件覆盖

抖音 DOU+ 推广数据分析：成本预估、投放数据明细/趋势图/概览（账号/视频/直播）、可推广作品列表、已投放账号、sec_token 获取、达人分类与按类搜索、用户主页作品、视频详情、DOU+ 视频排行榜、直播间搜索、DOU+ 用户搜索（V1/V2）、视频搜索。**全部 16 个端点均为 POST 方法，risk:high；含 `cookie` 参数的端点仅在用户明确授权后使用。**

> 🔒 **安全**：所有请求将 `MAXHUB_API_KEY` 和查询数据传输至 `https://www.aconfig.cn`。禁止在日志、提示词或客户端存储中暴露 API Key。含 `cookie` 参数的端点仅在用户明确授权后使用。

---

## 端点索引 (Endpoint Index)

### Douplus 端点（POST，risk:high）

| ID | 推荐度 | 一句话用途 | Method | Path | Risk |
|----|-------|----------|--------|------|------|
| douplus_calculate_cost | ⭐⭐⭐ 首选 | DOU+ 成本预估（**链式起点**） | POST | /api/v1/douyin/douplus/calculate_cost | **high** |
| douplus_fetch_analyse_detail | ⭐⭐ 条件 | 投放数据明细 | POST | /api/v1/douyin/douplus/fetch_analyse_detail | **high** |
| douplus_fetch_analyse_graph | ⭐⭐ 条件 | 投放数据趋势图 | POST | /api/v1/douyin/douplus/fetch_analyse_graph | **high** |
| douplus_fetch_analyse_overview | ⭐⭐⭐ 首选 | 投放数据概览（账号/视频/直播） | POST | /api/v1/douyin/douplus/fetch_analyse_overview | **high** |
| douplus_fetch_promotable_item_list | ⭐⭐ 条件 | 获取可推广作品列表（含点赞评论量） | POST | /api/v1/douyin/douplus/fetch_promotable_item_list | **high** |
| douplus_fetch_promoted_accounts | ⭐⭐ 条件 | 获取投放过的账号 | POST | /api/v1/douyin/douplus/fetch_promoted_accounts | **high** |
| douplus_fetch_talent_categories | ⭐ 条件 | 获取达人分类 | POST | /api/v1/douyin/douplus/fetch_talent_categories | **high** |
| douplus_fetch_talents_by_category | ⭐⭐ 条件 | 按分类搜索达人 | POST | /api/v1/douyin/douplus/fetch_talents_by_category | **high** |
| douplus_fetch_user_posts | ⭐⭐ 条件 | 获取用户主页作品 | POST | /api/v1/douyin/douplus/fetch_user_posts | **high** |
| douplus_fetch_video_detail | ⭐⭐ 条件 | 获取视频详情（按 ID 或链接） | POST | /api/v1/douyin/douplus/fetch_video_detail | **high** |
| douplus_fetch_video_ranking | ⭐⭐ 条件 | 获取 DOU+ 视频排行榜 | POST | /api/v1/douyin/douplus/fetch_video_ranking | **high** |
| douplus_search_live_room | ⭐⭐ 条件 | 搜索直播间（抖音号/昵称） | POST | /api/v1/douyin/douplus/search_live_room | **high** |
| douplus_search_user | ⭐⭐ 条件 | 搜索 DOU+ 用户 | POST | /api/v1/douyin/douplus/search_user | **high** |
| douplus_search_user_v2 | ⭐⭐⭐ 首选 | 搜索用户 V2（支持 scope） | POST | /api/v1/douyin/douplus/search_user_v2 | **high** |
| douplus_search_video | ⭐⭐ 条件 | 搜索视频（按标题） | POST | /api/v1/douyin/douplus/search_video | **high** |

---

## 链式调用图谱 (Chain Recipes)

| 用户目标 | 链路 | 字段流 (json_path → 下游参数) | 中间步失败时的容错 |
|---------|------|-------|-------------------|
| 投放概览 + 明细 | douplus_fetch_analyse_overview → douplus_fetch_analyse_detail | `query` 复用 | 第 1 步失败：STOP |
| 投放概览 + 趋势图 | douplus_fetch_analyse_overview → douplus_fetch_analyse_graph | `query` 复用 | 第 2 步失败：返回概览 + "趋势图暂不可取" |
| 选可推广作品 → 成本预估 | douplus_fetch_promotable_item_list → douplus_calculate_cost | `$.data.item_list[].item_id` → `item_ids` | 第 1 步失败：STOP |
| 达人分类 → 按类搜索 | douplus_fetch_talent_categories → douplus_fetch_talents_by_category | `$.data.categories[].id` → `name`/`page` | 第 1 步失败：STOP |
| DOU+ 用户搜索 → 主页作品 | douplus_search_user_v2 → douplus_fetch_user_posts | `$.data.users[].sec_uid` → `sec_uid` | 第 1 步失败：STOP |
| DOU+ 视频搜索 → 视频详情 | douplus_search_video → douplus_fetch_video_detail | `$.data.videos[].aweme_id` → `video` | 第 1 步失败：STOP |
| 视频排行榜 → 视频详情 | douplus_fetch_video_ranking → douplus_fetch_video_detail | `$.data.ranking[].item_id` → `video` | 跨文件链路 |
| 投放过的账号 → 用户作品 | douplus_fetch_promoted_accounts → douplus_fetch_user_posts | `$.data.accounts[].sec_uid` → `sec_uid` | 第 1 步失败：STOP |

---

## 跨 reference 链路 (In-Chain)

- **流入本文件**：`user.md` 的用户端点输出 `sec_user_id` / `sec_uid` → 本文件 `douplus_calculate_cost`、`douplus_fetch_promotable_item_list`、`douplus_fetch_user_posts`
- **流入本文件**：`video.md` 的视频端点输出 `aweme_id` → 本文件 `douplus_fetch_video_detail` 的 `video` 参数
- **流入本文件**：`live.md` 的直播端点输出 `room_id` → 本文件 `douplus_search_live_room` 关联查询
- **流出本文件**：`douplus_fetch_user_posts` 的 `$.data.aweme_list[].aweme_id` → `video.md` 的视频详情端点
- **流出本文件**：`douplus_search_video` 的 `$.data.videos[].aweme_id` → `video.md` 的视频详情端点
- **流出本文件**：`douplus_search_user_v2` 的 `$.data.users[].sec_uid` → `user.md` 的用户资料端点

---

## 错误处理契约 (Error Contract · 本文件全端点共享)

> 端点级 ERR 表仅列出特殊覆盖项；通用规则见此处。
> **完整 HTTP 状态码语义与决策表见 [`param-mappings.md` § 3](./param-mappings.md#3-全-skill-错误处理总览-error-handling-overview)**

### 路径错误（404 / 410）⚠️ 防臆造前置自检
- **第 1 步：必须先做防臆造自检**（详见 [`param-mappings.md` § 3.1 (A)](./param-mappings.md#a-收到-404-时的自检清单-️-防路径臆造)）
  - 注意 Douplus 路径统一为 `/api/v1/douyin/douplus/`，无 V1/V2 区分
- **第 2 步：自检通过后**才能判定"上游资源真的不存在" → **STOP**

### 参数错误（400 / 422）⚠️ 防臆造前置自检
- **第 1 步：必须先做防臆造自检**（详见 [`param-mappings.md` § 3.1 (B)](./param-mappings.md#b-收到-400--422-时的自检清单-️-防参数与传参方式臆造)）
  - 所有 Douplus 端点参数通过 **body**（JSON）传递
  - 含 `cookie` 参数的端点为强约束项（必填时不可省略）

### cookie 参数特化规则
- 本文件中标注 `cookie` 为必填或可选的端点均使用**用户抖音 DOU+ 后台 Cookie**
- **必须在用户明确授权后才可传递**
- 禁止 Agent 自行构造或缓存 cookie

### query 参数特化规则（仅 analyse 三端点）
- `douplus_fetch_analyse_detail` / `douplus_fetch_analyse_graph` / `douplus_fetch_analyse_overview` 的 `query` 参数为 **object 类型**，包含投放分析查询条件（如时间范围、投放目标、维度等）
- Agent 不得自行构造 query 内部字段，须依据用户输入或上游响应组装

### sec_uid 参数特化规则
- `douplus_calculate_cost`、`douplus_fetch_promotable_item_list`、`douplus_fetch_user_posts` 的 `sec_uid` 参数为抖音用户加密 ID（Base64 格式长字符串）
- 来源：`user.md` 端点的 `sec_user_id` 输出，或 `douplus_search_user_v2` 的 `$.data.users[].sec_uid`

### item_ids 参数特化规则（仅 calculate_cost）
- `douplus_calculate_cost` 的 `item_ids` 为作品 ID 列表，多个用逗号分隔
- 来源：`douplus_fetch_promotable_item_list` 的 `$.data.item_list[].item_id`

### video 参数特化规则（仅 fetch_video_detail）
- `douplus_fetch_video_detail` 的 `video` 参数支持视频 ID 或视频链接（短链/分享链接）

---

## 端点详情

---

### douplus_calculate_cost — DOU+ 成本预估

**Full path:** `/api/v1/douyin/douplus/calculate_cost`
**Method:** POST · **Risk:** **high**

#### 用途
预估 DOU+ 投放成本，按目标受众与作品给出预估消耗、曝光、互动等指标。**链式起点**，常与 `douplus_fetch_promotable_item_list` 组合使用。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| cookie | string | yes | — | 抖音 DOU+ 后台 Cookie（**需用户授权**） |
| sec_uid | string | yes | Base64 长字符串 | 用户加密 ID |
| item_ids | string | yes | 逗号分隔多个 ID | 作品 ID 列表（从 `douplus_fetch_promotable_item_list` 获取） |
| target_id | unknown | no | — | 投放目标 ID |

#### 输出可链式字段 (OUT)
终端数据（预估消耗、预估曝光、预估互动等指标），无下游链式调用。

#### 错误处理 (ERR)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 401 | cookie 无效/过期 | STOP，提示用户更新 cookie | 0 | — |
| 400 | sec_uid / item_ids 缺失 | 补全参数重试 | ≤1 次 | — |

---

### douplus_fetch_analyse_detail — 投放数据明细

**Full path:** `/api/v1/douyin/douplus/fetch_analyse_detail`
**Method:** POST · **Risk:** **high**

#### 用途
获取 DOU+ 投放数据明细，逐条展示投放记录的曝光、点击、互动、消耗等数据。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| cookie | string | yes | — | 抖音 DOU+ 后台 Cookie（**需用户授权**） |
| query | object | yes | — | 投放分析查询条件（时间范围、维度等） |

#### 输出可链式字段 (OUT)
终端数据（投放明细列表），无下游链式调用。

---

### douplus_fetch_analyse_graph — 投放数据趋势图

**Full path:** `/api/v1/douyin/douplus/fetch_analyse_graph`
**Method:** POST · **Risk:** **high**

#### 用途
获取 DOU+ 投放数据趋势图，按时间序列展示曝光、互动、消耗等指标的变化趋势。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| cookie | string | yes | — | 抖音 DOU+ 后台 Cookie（**需用户授权**） |
| query | object | yes | — | 投放分析查询条件 |

#### 输出可链式字段 (OUT)
终端数据（时间序列趋势数据），无下游链式调用。

---

### douplus_fetch_analyse_overview — 投放数据概览

**Full path:** `/api/v1/douyin/douplus/fetch_analyse_overview`
**Method:** POST · **Risk:** **high**

#### 用途
获取 DOU+ 投放数据概览，覆盖账号/视频/直播三类投放维度的总览指标。**链式起点**，常与 `douplus_fetch_analyse_detail`、`douplus_fetch_analyse_graph` 组合使用。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| cookie | string | yes | — | 抖音 DOU+ 后台 Cookie（**需用户授权**） |
| query | object | yes | — | 投放分析查询条件（账号/视频/直播维度） |

#### 输出可链式字段 (OUT)
终端数据（总览指标），无下游链式调用。

#### 错误处理 (ERR)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 401 | cookie 无效/过期 | STOP，提示用户更新 cookie | 0 | — |
| 400 | query 缺失 | 补全参数重试 | ≤1 次 | — |

---

### douplus_fetch_promotable_item_list — 获取可推广作品列表

**Full path:** `/api/v1/douyin/douplus/fetch_promotable_item_list`
**Method:** POST · **Risk:** **high**

#### 用途
获取指定用户可推广的作品列表，含点赞、评论量等指标，为 `douplus_calculate_cost` 提供 `item_ids` 输入。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| sec_uid | string | yes | Base64 长字符串 | 用户加密 ID |
| count | unknown | no | — | 每页数量 |
| target_id | unknown | no | — | 投放目标 ID |
| aim_ids | unknown | no | — | 指定作品 ID 列表 |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| item_list[].item_id | `$.data.item_list[].item_id` | 作品 ID | douplus_calculate_cost |

---

### douplus_fetch_promoted_accounts — 获取投放过的账号

**Full path:** `/api/v1/douyin/douplus/fetch_promoted_accounts`
**Method:** POST · **Risk:** **high**

#### 用途
获取当前账号投放 DOU+ 过的账号列表，支持分页。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| cookie | string | yes | — | 抖音 DOU+ 后台 Cookie（**需用户授权**） |
| limit | unknown | no | — | 每页数量 |
| cursor | unknown | no | — | 分页游标，首次不传 |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| accounts[].sec_uid | `$.data.accounts[].sec_uid` | 用户加密 ID | douplus_fetch_user_posts |
| cursor | `$.data.cursor` | 下一页游标 | 同端点翻页 |

---

### douplus_fetch_talent_categories — 获取达人分类

**Full path:** `/api/v1/douyin/douplus/fetch_talent_categories`
**Method:** POST · **Risk:** **high**

#### 用途
获取 DOU+ 达人分类列表，为 `douplus_fetch_talents_by_category` 提供分类 ID 输入。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| cookie | unknown | no | — | 抖音 DOU+ 后台 Cookie（可选，需用户授权后传递） |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| categories[].id | `$.data.categories[].id` | 分类 ID | douplus_fetch_talents_by_category |

---

### douplus_fetch_talents_by_category — 按分类搜索达人

**Full path:** `/api/v1/douyin/douplus/fetch_talents_by_category`
**Method:** POST · **Risk:** **high**

#### 用途
按分类搜索 DOU+ 达人，支持关键词、分页。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| cookie | unknown | no | — | 抖音 DOU+ 后台 Cookie（可选，需用户授权后传递） |
| name | unknown | no | — | 达人名称/关键词 |
| page | unknown | no | — | 页码 |
| limit | unknown | no | — | 每页数量 |

#### 输出可链式字段 (OUT)
终端数据（达人列表，含基础信息、粉丝数等），无下游链式调用。

---

### douplus_fetch_user_posts — 获取用户主页作品

**Full path:** `/api/v1/douyin/douplus/fetch_user_posts`
**Method:** POST · **Risk:** **high**

#### 用途
获取指定用户主页的作品列表，支持分页。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| cookie | unknown | no | — | 抖音 DOU+ 后台 Cookie（可选，需用户授权后传递） |
| sec_uid | string | yes | Base64 长字符串 | 用户加密 ID |
| cursor | unknown | no | — | 分页游标，首次不传 |
| count | unknown | no | — | 每页数量 |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| aweme_list[].aweme_id | `$.data.aweme_list[].aweme_id` | 作品 ID | video.md 视频详情端点 |
| cursor | `$.data.cursor` | 下一页游标 | 同端点翻页 |

---

### douplus_fetch_video_detail — 获取视频详情

**Full path:** `/api/v1/douyin/douplus/fetch_video_detail`
**Method:** POST · **Risk:** **high**

#### 用途
获取视频详情，支持按视频 ID 或视频链接（短链/分享链接）查询。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| cookie | unknown | no | — | 抖音 DOU+ 后台 Cookie（可选，需用户授权后传递） |
| video | string | yes | 视频 ID 或链接 | 视频 ID 或分享链接 |

#### 输出可链式字段 (OUT)
终端数据（视频详情，含播放、互动、作者等字段），无下游链式调用。

---

### douplus_fetch_video_ranking — 获取 DOU+ 视频排行榜

**Full path:** `/api/v1/douyin/douplus/fetch_video_ranking`
**Method:** POST · **Risk:** **high**

#### 用途
获取 DOU+ 视频排行榜，支持时间范围、标签、维度、广告主 ID 筛选。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| time_range | unknown | no | — | 时间范围 |
| tag_id | unknown | no | — | 标签 ID |
| dim_type | unknown | no | — | 维度类型 |
| adv_id | unknown | no | — | 广告主 ID |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| ranking[].item_id | `$.data.ranking[].item_id` | 作品 ID | douplus_fetch_video_detail / video.md |

---

### douplus_search_live_room — 搜索直播间

**Full path:** `/api/v1/douyin/douplus/search_live_room`
**Method:** POST · **Risk:** **high**

#### 用途
按抖音号或昵称搜索直播间，支持分页。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| cookie | unknown | no | — | 抖音 DOU+ 后台 Cookie（可选，需用户授权后传递） |
| keyword | string | yes | — | 搜索关键词（抖音号/昵称） |
| cursor | unknown | no | — | 分页游标，首次不传 |
| count | unknown | no | — | 每页数量 |

#### 输出可链式字段 (OUT)
终端数据（直播间列表），无下游链式调用。

---

### douplus_search_user — 搜索 DOU+ 用户

**Full path:** `/api/v1/douyin/douplus/search_user`
**Method:** POST · **Risk:** **high**

#### 用途
搜索 DOU+ 用户，支持分页。V1 版本，无 scope 筛选。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| keyword | string | yes | — | 搜索关键词 |
| count | unknown | no | — | 每页数量 |
| cursor | unknown | no | — | 分页游标，首次不传 |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| users[].sec_uid | `$.data.users[].sec_uid` | 用户加密 ID | douplus_fetch_user_posts |

---

### douplus_search_user_v2 — 搜索用户 V2

**Full path:** `/api/v1/douyin/douplus/search_user_v2`
**Method:** POST · **Risk:** **high**

#### 用途
搜索用户 V2，支持 scope 筛选，字段更丰富。**链式起点**，常与 `douplus_fetch_user_posts` 组合使用。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| cookie | unknown | no | — | 抖音 DOU+ 后台 Cookie（可选，需用户授权后传递） |
| keyword | string | yes | — | 搜索关键词 |
| cursor | unknown | no | — | 分页游标，首次不传 |
| count | unknown | no | — | 每页数量 |
| scope | unknown | no | — | 搜索范围筛选 |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| users[].sec_uid | `$.data.users[].sec_uid` | 用户加密 ID | douplus_fetch_user_posts / user.md |
| cursor | `$.data.cursor` | 下一页游标 | 同端点翻页 |

---

### douplus_search_video — 搜索视频

**Full path:** `/api/v1/douyin/douplus/search_video`
**Method:** POST · **Risk:** **high**

#### 用途
按标题搜索视频，支持分页。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| cookie | unknown | no | — | 抖音 DOU+ 后台 Cookie（可选，需用户授权后传递） |
| keyword | string | yes | — | 搜索关键词 |
| cursor | unknown | no | — | 分页游标，首次不传 |
| count | unknown | no | — | 每页数量 |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| videos[].aweme_id | `$.data.videos[].aweme_id` | 作品 ID | douplus_fetch_video_detail / video.md |
| cursor | `$.data.cursor` | 下一页游标 | 同端点翻页 |
