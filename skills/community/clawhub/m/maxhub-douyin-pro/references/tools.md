# Douyin Tools / 抖音工具

Base URL: `https://www.aconfig.cn` · Auth: `Authorization: Bearer $MAXHUB_API_KEY`

## 本文件覆盖

ID 提取工具（sec_user_id / aweme_id / webcast_id）、短链接转换。**本文件是 ID 提取的入口**——当用户只有分享链接/URL 时，需先通过 ID 提取端点获取 sec_user_id / aweme_id / webcast_id，再链式调用 video.md / user.md / live.md 的业务端点。

> 🔒 **安全**：所有请求将 `MAXHUB_API_KEY` 和查询数据传输至 `https://www.aconfig.cn`。禁止在日志、提示词或客户端存储中暴露 API Key。

---

## 端点索引 (Endpoint Index)

### App 跳转

| ID | 推荐度 | 一句话用途 | Method | Path | Risk |
|----|-------|----------|--------|------|------|
| app_v3_open_douyin_app_to_video_detail | ⭐⭐ 条件 | 生成 Deep-Link 跳转到视频详情页 | GET | /api/v1/douyin/app/v3/open_douyin_app_to_video_detail | low |
| app_v3_open_douyin_app_to_user_profile | ⭐⭐ 条件 | 生成 Deep-Link 跳转到用户主页 | GET | /api/v1/douyin/app/v3/open_douyin_app_to_user_profile | low |
| app_v3_open_douyin_app_to_keyword_search | ⭐⭐ 条件 | 生成 Deep-Link 跳转到搜索结果页 | GET | /api/v1/douyin/app/v3/open_douyin_app_to_keyword_search | low |

### ID 提取工具

| ID | 推荐度 | 一句话用途 | Method | Path | Risk |
|----|-------|----------|--------|------|------|
| web_get_sec_user_id | ⭐⭐⭐ 首选 | 从 URL 提取 sec_user_id（**链式起点**） | GET | /api/v1/douyin/web/get_sec_user_id | low |
| web_get_aweme_id | ⭐⭐⭐ 首选 | 从 URL 提取 aweme_id（**链式起点**） | GET | /api/v1/douyin/web/get_aweme_id | low |
| web_get_webcast_id | ⭐⭐⭐ 首选 | 从 URL 提取 webcast_id（**链式起点**） | GET | /api/v1/douyin/web/get_webcast_id | low |

### 其他工具

| ID | 推荐度 | 一句话用途 | Method | Path | Risk |
|----|-------|----------|--------|------|------|
| web_handler_shorten_url | ⭐⭐ 条件 | 短链接转换（长链接→短链接） | GET | /api/v1/douyin/web/handler_shorten_url | low |

---

## 链式调用图谱 (Chain Recipes)

> 当单个端点无法直接产出用户所需数据时，按下面链路组合调用。`字段流`列指明字段如何从上一步流向下一步，避免 Agent 臆造字段名。

| 用户目标 | 链路 | 字段流 (json_path → 下游参数) | 中间步失败时的容错 |
|---------|------|-------|-------------------|
| 从分享链接获取用户信息 | web_get_sec_user_id → user.md | `$.data.sec_user_id` → `sec_user_id` | 第 1 步失败：STOP，提示 URL 无效；第 2 步失败：返回 sec_user_id + "用户详情暂不可取" |
| 从分享链接获取视频详情 | web_get_aweme_id → video.md | `$.data.aweme_id` → `aweme_id` | 第 1 步失败：STOP，提示 URL 无效；第 2 步失败：返回 aweme_id + "视频详情暂不可取" |
| 从直播链接获取直播信息 | web_get_webcast_id → live.md | `$.data.webcast_id` → `webcast_id`（→ `web_webcast_id_2_room_id`） | 第 1 步失败：STOP，提示 URL 无效；第 2 步失败：返回 webcast_id + "直播信息暂不可取" |

---

## 跨 reference 链路 (In-Chain)

- **流出本文件**：`web_get_sec_user_id` 输出 `$.data.sec_user_id` → `user.md` 全部 user 系端点的 `sec_user_id`
- **流出本文件**：`web_get_aweme_id` 输出 `$.data.aweme_id` → `video.md` 全部 video 系端点的 `aweme_id`
- **流出本文件**：`web_get_webcast_id` 输出 `$.data.webcast_id` → `live.md` 的 `web_webcast_id_2_room_id` 的 `webcast_id`

---

## 错误处理契约 (Error Contract · 本文件全端点共享)

> 端点级 ERR 表仅列出特殊覆盖项；通用规则见此处。
> **完整 HTTP 状态码语义与决策表见 [`param-mappings.md` § 3](./param-mappings.md#3-全-skill-错误处理总览-error-handling-overview)**

### 路径错误（404 / 410）⚠️ 防臆造前置自检
- **第 1 步：必须先做防臆造自检**（详见 [`param-mappings.md` § 3.1 (A)](./param-mappings.md#a-收到-404-时的自检清单-️-防路径臆造)）
  - 路径是否在 [`endpoints_whitelist.yaml`](./endpoints_whitelist.yaml) 中？
  - Method、参数键名是否符合白名单？
  - 资源 ID（url/room_id/user_unique_id）是否来自合法响应字段？
- **第 2 步：自检通过后**才能判定"上游资源真的不存在" → **STOP**，向用户报告
- **禁止**：❌ 改路径段（app/v3→web 试探）❌ 切换平台前缀 ❌ 拼接新路径 ❌ 自行修改资源 ID 重试
- **替换**：参考 [`param-mappings.md`](./param-mappings.md) 的"端点替换矩阵"

### 参数错误（400 / 422）⚠️ 防臆造前置自检
- **第 1 步：必须先做防臆造自检**（详见 [`param-mappings.md` § 3.1 (B)](./param-mappings.md#b-收到-400--422-时的自检清单-️-防参数与传参方式臆造)）
  - 参数名是否逐字符匹配 IN 表？注意 `url` vs `target_url` 的区别
  - 必填项是否齐全？
  - 传参方式（query vs body）是否正确？Authorization 头是否正确？
  - **是否有 IN 表外的臆造参数**？
- **第 2 步：自检通过后**才能修正参数重试 → 最多重试 1 次 → 仍失败 STOP
- **禁止**：❌ 切换端点 ❌ 在 IN 表外凭空加参数

### 工具类端点特化规则
- **ID 提取端点**：输入的 `url` 必须是完整的抖音分享链接（含 `https://` 前缀），短链接需先通过 `web_handler_shorten_url` 还原
- **App Deep-Link 端点**：生成的链接需在移动端打开才能唤起抖音 App，PC 端无法直接使用

---

## 端点详情

---

### app_v3_open_douyin_app_to_video_detail — 生成跳转视频详情的 Deep-Link

**Full path:** `/api/v1/douyin/app/v3/open_douyin_app_to_video_detail`
**Method:** GET · **Risk:** low

#### 用途
生成抖音分享链接，唤起抖音 App 并跳转到指定视频详情页。

#### 何时使用 / 不使用
- ✅ 用户需要在手机端打开指定视频
- ✅ 已知 aweme_id
- ❌ 不知 aweme_id → 先通过 `web_get_aweme_id` 从 URL 提取，或从 `video.md` 获取
- ❌ 在 PC 端使用（Deep-Link 需移动端打开）

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| aweme_id | string | yes | — | 视频/作品 ID |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| — | — | 分享链接为终端数据，无下游链式调用 | — |

#### 错误处理 (ERR)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 400 | aweme_id 缺失 | 补全参数重试 | ≤1 次 | — |
| 404 | aweme_id 不存在 | STOP | 0 | 无 |

---

### app_v3_open_douyin_app_to_user_profile — 生成跳转用户主页的 Deep-Link

**Full path:** `/api/v1/douyin/app/v3/open_douyin_app_to_user_profile`
**Method:** GET · **Risk:** low

#### 用途
生成抖音分享链接，唤起抖音 App 并跳转到指定用户主页。

#### 何时使用 / 不使用
- ✅ 用户需要在手机端打开指定用户主页
- ✅ 已知 uid 和 sec_uid（**两者都必须有值**）
- ❌ 缺少 uid 或 sec_uid → 无法跳转
- ❌ 在 PC 端使用（Deep-Link 需移动端打开）

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| uid | string | yes | — | 用户 ID |
| sec_uid | string | yes | — | 用户 sec_uid |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| — | — | 分享链接为终端数据，无下游链式调用 | — |

#### 错误处理 (ERR)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 400 | uid 或 sec_uid 缺失 | 补全参数重试 | ≤1 次 | — |

---

### app_v3_open_douyin_app_to_keyword_search — 生成跳转搜索结果的 Deep-Link

**Full path:** `/api/v1/douyin/app/v3/open_douyin_app_to_keyword_search`
**Method:** GET · **Risk:** low

#### 用途
生成抖音分享链接，唤起抖音 App 并跳转到指定关键词搜索结果页。

#### 何时使用 / 不使用
- ✅ 用户需要在手机端搜索指定关键词
- ✅ 已知 keyword
- ❌ 在 PC 端使用（Deep-Link 需移动端打开）

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| keyword | string | yes | — | 搜索关键词 |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| — | — | 分享链接为终端数据，无下游链式调用 | — |

#### 错误处理 (ERR)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 400 | keyword 缺失 | 补全参数重试 | ≤1 次 | — |

---

### web_get_sec_user_id — 从 URL 提取 sec_user_id

**Full path:** `/api/v1/douyin/web/get_sec_user_id`
**Method:** GET · **Risk:** low

#### 用途
从抖音分享链接/URL 中提取 sec_user_id。**链式调用常见起点**——当用户只提供分享链接时，先提取 sec_user_id，再调用 user.md 的用户详情端点。

#### 何时使用 / 不使用
- ✅ 用户提供了抖音用户分享链接，需要提取 sec_user_id
- ✅ 链式起点：提取 sec_user_id 后调用 user.md 端点
- ❌ 已知 sec_user_id → 直接调用 user.md 端点
- ❌ URL 不是抖音用户链接 → 无法提取

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| url | string | yes | 需为完整抖音分享链接（含 `https://` 前缀） | 抖音用户分享链接 |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| sec_user_id | `$.data.sec_user_id` | 用户 sec_uid | user.md 全部 user 系端点 |

#### 错误处理 (ERR)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 400 | url 缺失或格式无效 | 校正 URL 重试 | ≤1 次 | — |
| 404 | URL 中无法提取 sec_user_id | STOP | 0 | 提示用户确认链接是否为用户主页 |

---

### web_get_aweme_id — 从 URL 提取 aweme_id

**Full path:** `/api/v1/douyin/web/get_aweme_id`
**Method:** GET · **Risk:** low

#### 用途
从抖音分享链接/URL 中提取 aweme_id。**链式调用常见起点**——当用户只提供分享链接时，先提取 aweme_id，再调用 video.md 的视频详情端点。

#### 何时使用 / 不使用
- ✅ 用户提供了抖音视频分享链接，需要提取 aweme_id
- ✅ 链式起点：提取 aweme_id 后调用 video.md 端点
- ❌ 已知 aweme_id → 直接调用 video.md 端点
- ❌ URL 不是抖音视频链接 → 无法提取

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| url | string | yes | 需为完整抖音分享链接（含 `https://` 前缀） | 抖音视频分享链接 |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| aweme_id | `$.data.aweme_id` | 视频/作品 ID | video.md 全部 video 系端点 |

#### 错误处理 (ERR)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 400 | url 缺失或格式无效 | 校正 URL 重试 | ≤1 次 | — |
| 404 | URL 中无法提取 aweme_id | STOP | 0 | 提示用户确认链接是否为视频页 |

---

### web_get_webcast_id — 从 URL 提取 webcast_id

**Full path:** `/api/v1/douyin/web/get_webcast_id`
**Method:** GET · **Risk:** low

#### 用途
从抖音直播分享链接/URL 中提取 webcast_id。**链式调用常见起点**——当用户只提供直播链接时，先提取 webcast_id，再调用 live.md 的 `web_webcast_id_2_room_id` 转换为 room_id。

#### 何时使用 / 不使用
- ✅ 用户提供了抖音直播分享链接，需要提取 webcast_id
- ✅ 链式起点：提取 webcast_id 后调用 live.md 端点
- ❌ 已知 room_id → 直接调用 live.md 端点
- ❌ URL 不是抖音直播链接 → 无法提取

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| url | string | yes | 需为完整抖音直播分享链接（含 `https://` 前缀） | 抖音直播分享链接 |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| webcast_id | `$.data.webcast_id` | 直播 webcast_id | live.md 的 `web_webcast_id_2_room_id` |

#### 错误处理 (ERR)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 400 | url 缺失或格式无效 | 校正 URL 重试 | ≤1 次 | — |
| 404 | URL 中无法提取 webcast_id | STOP | 0 | 提示用户确认链接是否为直播页 |

---

### web_handler_shorten_url — 短链接转换

**Full path:** `/api/v1/douyin/web/handler_shorten_url`
**Method:** GET · **Risk:** low

#### 用途
将长链接转换为短链接，或将短链接还原为长链接。

#### 何时使用 / 不使用
- ✅ 用户需要缩短链接
- ✅ ID 提取端点无法识别短链接 → 先还原为长链接再提取
- ❌ 已有完整长链接 → 无需转换

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| target_url | string | yes | 需为完整 URL（含 `https://` 前缀） | 目标链接 |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| — | — | 转换结果为终端数据，但还原后的长链接可作为 `web_get_*` 端点的 url 参数 | web_get_sec_user_id / web_get_aweme_id / web_get_webcast_id |

#### 错误处理 (ERR)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 400 | target_url 缺失或格式无效 | 校正 URL 重试 | ≤1 次 | — |
| 404 | 无法解析短链接 | STOP | 0 | 提示用户确认链接有效性 |

---
