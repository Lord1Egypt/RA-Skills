# Xiaohongshu PGY / 小红书蒲公英创作者数据

Base URL: `https://www.aconfig.cn` · Auth: `Authorization: Bearer $MAXHUB_API_KEY`

## 本文件覆盖

蒲公英（PGY）创作者数据分析平台端点：博主核心数据、数据概览、博主详情、粉丝增长历史、粉丝画像、粉丝概览、博主列表（选号）、笔记明细、笔记转化率、笔记详情。**全部为 POST 端点**，围绕"蒲公英博主选号 + 笔记效果分析"全部读取入口。**user_id / brand_user_id / note_id 是最常见的链式输入**。

> 本文件 10 个端点全部为 `method: POST` + `risk: high` + `requires_user_confirmation: true` + `write_operation: true`。
> 调用前 **必须** 显式向用户确认参数与意图，未确认禁止调用。
> 参数通过 request body（JSON）传递，**不是** query string。

## 安全声明 (Security Statement)

1. **POST 写入语义**：蒲公英接口在上游对应 POST 写入式查询（创建分析任务 / 触发数据计算），归为 `write_operation: true`。每次调用都会消耗蒲公英账户侧的查询额度。
2. **授权前置**：调用前必须显式向用户确认："即将以 user_id=xxx 调用 PGY <端点名>，是否继续？"未获明确确认禁止调用。
3. **凭证保护**：本文件端点不直接需要 cookie；如某些端点上游异常返回 401/403 提示需要 cookie，**禁止**自行编造，应让用户去 https://www.aconfig.cn 控制台配置。
4. **数据合规**：返回的粉丝画像 / 笔记转化率等数据可能涉及博主隐私，禁止写入未授权数据库或公开发布。

## 端点索引 (Endpoint Index)

| ID | 推荐度 | 一句话用途 | Method | Path | Risk |
|----|-------|----------|--------|------|------|
| pgy_get_blogger_core_data | ⭐⭐⭐ 首选 | 用 user_id 取蒲公英博主核心数据 | POST | /api/v1/xiaohongshu/pgy/get_blogger_core_data | high |
| pgy_get_blogger_data_summary | ⭐⭐⭐ 首选 | 用 user_id 取蒲公英博主数据概览 | POST | /api/v1/xiaohongshu/pgy/get_blogger_data_summary | high |
| pgy_get_blogger_detail | ⭐⭐⭐ 首选 | 用 user_id 取蒲公英博主详情 | POST | /api/v1/xiaohongshu/pgy/get_blogger_detail | high |
| pgy_get_blogger_fans_history | ⭐⭐ 条件 | 用 user_id 取博主粉丝增长历史 | POST | /api/v1/xiaohongshu/pgy/get_blogger_fans_history | high |
| pgy_get_blogger_fans_profile | ⭐⭐ 条件 | 用 user_id 取博主粉丝画像 | POST | /api/v1/xiaohongshu/pgy/get_blogger_fans_profile | high |
| pgy_get_blogger_fans_summary | ⭐⭐ 条件 | 用 user_id 取博主粉丝概览 | POST | /api/v1/xiaohongshu/pgy/get_blogger_fans_summary | high |
| pgy_get_blogger_list | ⭐⭐ 条件 | 用 brand_user_id 取蒲公英博主列表（选号） | POST | /api/v1/xiaohongshu/pgy/get_blogger_list | high |
| pgy_get_blogger_notes | ⭐⭐ 条件 | 用 user_id 取博主笔记明细 | POST | /api/v1/xiaohongshu/pgy/get_blogger_notes | high |
| pgy_get_blogger_notes_rate | ⭐⭐ 条件 | 用 user_id 取博主笔记转化率 | POST | /api/v1/xiaohongshu/pgy/get_blogger_notes_rate | high |
| pgy_get_note_detail | ⭐⭐ 条件 | 用 note_id 取蒲公英笔记详情 | POST | /api/v1/xiaohongshu/pgy/get_note_detail | high |

## 链式调用图谱 (Chain Recipes · 本文件内 + 跨文件)

| 用户目标 | 链路 | 字段流 (json_path → 下游参数) | 中间步失败时的容错 |
|---------|------|-------|-------------------|
| 选号 → 博主详情 → 核心数据 | pgy_get_blogger_list → pgy_get_blogger_detail → pgy_get_blogger_core_data | `$.data.list[].user_id` → `user_id` 复用 | 第 1 步空数据：返回"暂无候选博主" |
| 博主详情 → 数据概览 + 粉丝概览 | pgy_get_blogger_detail → pgy_get_blogger_data_summary + pgy_get_blogger_fans_summary | user_id 复用 | 第 2 步失败：返回详情 + "粉丝数据暂不可取" |
| 博主详情 → 粉丝画像 + 增长历史 | pgy_get_blogger_detail → pgy_get_blogger_fans_profile + pgy_get_blogger_fans_history | user_id 复用 | 第 2 步失败：返回详情 + "粉丝画像暂不可取" |
| 博主笔记明细 → 单篇笔记详情 | pgy_get_blogger_notes → pgy_get_note_detail | `$.data.notes[].note_id` → `note_id` | 第 1 步空数据：返回"暂无笔记" |
| 博主核心数据 → 笔记转化率 | pgy_get_blogger_core_data → pgy_get_blogger_notes_rate | user_id 复用 | 第 2 步失败：返回核心数据 + "转化率暂不可取" |

## 跨 reference 链路 (In-Chain)

- **流入本文件**：`search.md` 的 `search_users` 输出 `$.data.users[].user_id` → 本文件博主系端点（PGY 端点 user_id 必须为蒲公英注册博主，搜索命中的普通用户可能不在蒲公英库中）
- **流入本文件**：`user.md` 的 `get_user_info` / `fetch_user_info` 输出 `$.data.user_id` → 本文件博主系端点
- **流出本文件**：`pgy_get_blogger_notes` 的 `$.data.notes[].note_id` → `note.md` 多端点（取小红书原站笔记详情）或本文件 `pgy_get_note_detail`（取蒲公英侧笔记分析详情）
- **流出本文件**：`pgy_get_blogger_list` 的 `$.data.list[].user_id` → 本文件全部博主系端点复用

## 错误处理契约 (Error Contract · 本文件全端点共享)

> 端点级 ERR 表仅列出特殊覆盖项。
> **完整 HTTP 状态码语义与决策表见 [`param-mappings.md` § 3](./param-mappings.md#3-全-skill-错误处理总览-error-handling-overview)**

### 路径错误（404 / 410）⚠️ 防臆造前置自检
- 详见 [`param-mappings.md` § 3.1 (A)](./param-mappings.md#a-收到-404-时的自检清单-️-防路径臆造)

### 参数错误（400 / 422）⚠️ 防臆造前置自检
- 详见 [`param-mappings.md` § 3.1 (B)](./param-mappings.md#b-收到-400--422-时的自检清单-️-防参数与传参方式臆造)
- **PGY 特化**：参数必须放在 request body（JSON），**不是** query string。把 user_id 放在 query string 会触发 400。

### 鉴权错误（401）→ STOP · 余额（402）→ STOP · 权限（403）→ STOP
### 限流（429）→ 读 Retry-After 退避，最多重试 2 次
### 上游故障（500/502/503/504）→ 等 3s 重试 1 次，仍失败走替换
### 网络超时 → STOP · 业务错误 → 读 message_zh，不重试

### PGY 特化错误

| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 403 + "未开通蒲公英" | 账户未开通蒲公英权限 | STOP，告知用户去 https://www.aconfig.cn 开通 | 0 | 无替代 |
| 404 + "博主不存在" | user_id 不在蒲公英博主库 | STOP，告知用户该博主未入驻蒲公英 | 0 | 可改用 `user.md` 的 `get_user_info` 取小红书原站资料 |
| 402 + "蒲公英额度不足" | 蒲公英侧查询额度耗尽 | STOP，告知用户充值 | 0 | 无替代 |
| 400 + "brand_user_id 无效" | brand_user_id 不是品牌账户 | STOP，告知用户检查品牌账户 ID | 0 | 无替代 |

---

## 端点详情

### pgy_get_blogger_core_data — 获取蒲公英博主核心数据

**Full path:** `/api/v1/xiaohongshu/pgy/get_blogger_core_data`
**Method:** POST · **Risk:** high · **requires_user_confirmation:** true · **write_operation:** true

#### 用途
获取蒲公英博主核心数据指标，包含互动率、CPE、CPM 等商业化分析字段。**博主商业化价值评估的首选入口**。

#### 何时使用 / 不使用
- ✅ 已知 user_id，想看博主商业化核心数据
- ✅ 链式起点：选号 → 详情 → 核心数据
- ❌ 只想看博主基础资料 → pgy_get_blogger_detail
- ❌ 想看粉丝画像 → pgy_get_blogger_fans_profile
- ❌ user_id 不是蒲公英博主 → STOP（PGY 库不收录）

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| user_id | string | yes | — | 蒲公英博主 user_id（24 位 hex），需先确认博主已入驻蒲公英 |
| note_type | integer | no | enum=`1, 2` | 笔记类型：1=图文, 2=视频，默认全部 |
| date_type | integer | no | enum=`1, 2, 3` | 时间范围：1=近 30 天, 2=近 90 天, 3=近 180 天，默认 1 |
| advertise_switch | integer | no | enum=`0, 1` | 是否包含广告笔记：0=否, 1=是，默认 0 |

> **请求体格式**：参数以 JSON 放在 request body 中，如 `{"user_id":"xxx","note_type":1,"date_type":1,"advertise_switch":0}`。

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| user_id | `$.data.user_id` | 博主 user_id（回显） | 本文件博主系端点复用 |
| note_id | `$.data.top_notes[].note_id` | 高互动笔记 ID | pgy_get_note_detail / note.md |

#### 错误处理 (ERR · 端点特化)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 404 | 博主不在蒲公英库 | STOP | 0 | 改用 `user.md` get_user_info 取原站资料 |

---

### pgy_get_blogger_data_summary — 获取蒲公英博主数据概览

**Full path:** `/api/v1/xiaohongshu/pgy/get_blogger_data_summary`
**Method:** POST · **Risk:** high · **requires_user_confirmation:** true · **write_operation:** true

#### 用途
获取蒲公英博主数据概览，包含近期笔记数、平均互动、最高互动等汇总指标。

#### 何时使用 / 不使用
- ✅ 已知 user_id，想快速了解博主整体数据水平
- ✅ 链式中间步：详情 → 概览 + 粉丝概览
- ❌ 想看核心商业化指标（CPE/CPM）→ pgy_get_blogger_core_data
- ❌ 想看具体笔记列表 → pgy_get_blogger_notes

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| user_id | string | yes | — | 蒲公英博主 user_id |

> **请求体格式**：`{"user_id":"xxx"}`。

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| user_id | `$.data.user_id` | 博主 user_id（回显） | 本文件博主系端点复用 |

#### 错误处理 (ERR)
同 pgy_get_blogger_core_data。

---

### pgy_get_blogger_detail — 蒲公英博主详情

**Full path:** `/api/v1/xiaohongshu/pgy/get_blogger_detail`
**Method:** POST · **Risk:** high · **requires_user_confirmation:** true · **write_operation:** true

#### 用途
获取蒲公英博主详情，包含博主标签、报价、合作历史等商业化资料。**博主选号链路的核心节点**。

#### 何时使用 / 不使用
- ✅ 已知 user_id，想看博主蒲公英详情页
- ✅ 链式起点：详情 → 数据概览 + 粉丝概览 + 核心数据
- ❌ 想看数据指标 → pgy_get_blogger_core_data / pgy_get_blogger_data_summary
- ❌ 想看粉丝画像 → pgy_get_blogger_fans_profile

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| user_id | string | yes | — | 蒲公英博主 user_id |

> **请求体格式**：`{"user_id":"xxx"}`。

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| user_id | `$.data.user_id` | 博主 user_id（回显） | 本文件博主系端点复用 |
| brand_user_id | `$.data.brand_user_id` | 关联品牌账户 ID | pgy_get_blogger_list（如需横向对比同品牌博主） |

#### 错误处理 (ERR)
同 pgy_get_blogger_core_data。

---

### pgy_get_blogger_fans_history — 获取博主粉丝增长历史

**Full path:** `/api/v1/xiaohongshu/pgy/get_blogger_fans_history`
**Method:** POST · **Risk:** high · **requires_user_confirmation:** true · **write_operation:** true

#### 用途
获取蒲公英博主粉丝增长历史曲线数据，用于评估博主粉丝增长趋势与异常波动。

#### 何时使用 / 不使用
- ✅ 已知 user_id，想分析粉丝增长趋势
- ✅ 链式中间步：详情 → 粉丝概览 + 粉丝增长历史 + 粉丝画像
- ❌ 想看粉丝总量 → pgy_get_blogger_fans_summary
- ❌ 想看粉丝画像分布 → pgy_get_blogger_fans_profile

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| user_id | string | yes | — | 蒲公英博主 user_id |
| date_type | integer | no | enum=`1, 2, 3` | 时间范围：1=近 30 天, 2=近 90 天, 3=近 180 天，默认 1 |

> **请求体格式**：`{"user_id":"xxx","date_type":1}`。

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| user_id | `$.data.user_id` | 博主 user_id（回显） | 本文件博主系端点复用 |

#### 错误处理 (ERR)
同 pgy_get_blogger_core_data。

---

### pgy_get_blogger_fans_profile — 获取博主粉丝画像

**Full path:** `/api/v1/xiaohongshu/pgy/get_blogger_fans_profile`
**Method:** POST · **Risk:** high · **requires_user_confirmation:** true · **write_operation:** true

#### 用途
获取蒲公英博主粉丝画像分布数据，包含性别、年龄、地域、兴趣等维度。

#### 何时使用 / 不使用
- ✅ 已知 user_id，想分析博主粉丝构成
- ✅ 链式中间步：详情 → 粉丝概览 + 粉丝画像 + 粉丝增长历史
- ❌ 想看粉丝总数与增长 → pgy_get_blogger_fans_summary / pgy_get_blogger_fans_history

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| user_id | string | yes | — | 蒲公英博主 user_id |

> **请求体格式**：`{"user_id":"xxx"}`。

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| user_id | `$.data.user_id` | 博主 user_id（回显） | 本文件博主系端点复用 |

#### 错误处理 (ERR)
同 pgy_get_blogger_core_data。

---

### pgy_get_blogger_fans_summary — 获取博主粉丝概览

**Full path:** `/api/v1/xiaohongshu/pgy/get_blogger_fans_summary`
**Method:** POST · **Risk:** high · **requires_user_confirmation:** true · **write_operation:** true

#### 用途
获取蒲公英博主粉丝概览数据，包含粉丝总量、新增、流失等汇总指标。

#### 何时使用 / 不使用
- ✅ 已知 user_id，想快速看粉丝总量与近期变化
- ✅ 链式中间步：详情 → 数据概览 + 粉丝概览
- ❌ 想看粉丝画像分布 → pgy_get_blogger_fans_profile
- ❌ 想看粉丝增长曲线 → pgy_get_blogger_fans_history

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| user_id | string | yes | — | 蒲公英博主 user_id |

> **请求体格式**：`{"user_id":"xxx"}`。

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| user_id | `$.data.user_id` | 博主 user_id（回显） | 本文件博主系端点复用 |

#### 错误处理 (ERR)
同 pgy_get_blogger_core_data。

---

### pgy_get_blogger_list — 获取蒲公英博主列表（选号）

**Full path:** `/api/v1/xiaohongshu/pgy/get_blogger_list`
**Method:** POST · **Risk:** high · **requires_user_confirmation:** true · **write_operation:** true

#### 用途
按品牌账户 ID 拉取蒲公英博主列表，支持粉丝数筛选与分页。**品牌方选号链路的入口端点**。

#### 何时使用 / 不使用
- ✅ 已知 brand_user_id，想批量拉取候选博主
- ✅ 链式起点：列表 → 详情 → 核心数据 → 粉丝画像
- ❌ 已知具体 user_id → 直接用 pgy_get_blogger_detail
- ❌ 想搜小红书原站用户 → search.md 的 search_users

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| brand_user_id | string | yes | — | 品牌账户 ID（蒲公英品牌方账号 ID） |
| page_num | integer | no | min=1, default=1 | 页码，从 1 开始 |
| page_size | integer | no | min=1, max=50, default=20 | 每页数量，最大 50 |
| fans_number_lower | string | no | — | 粉丝数下限（字符串数字），如 `"10000"` |
| fans_number_upper | string | no | — | 粉丝数上限（字符串数字），如 `"100000"` |

> **请求体格式**：`{"brand_user_id":"xxx","page_num":1,"page_size":20,"fans_number_lower":"10000","fans_number_upper":"100000"}`。
> **翻页说明**：page_num 从 1 开始递增。

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| list[].user_id | `$.data.list[].user_id` | 候选博主 user_id | 本文件全部博主系端点 |
| list[].nickname | `$.data.list[].nickname` | 博主昵称 | 用于核对身份避免误命中 |

#### 错误处理 (ERR · 端点特化)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 400 | brand_user_id 无效 | STOP，告知用户检查品牌账户 ID | 0 | 无替代 |
| 403 | 非品牌账户 | STOP，告知用户当前账户无品牌身份 | 0 | 无替代 |
| 空数据 | 暂无候选博主 | 返回"暂无候选博主" | 0 | — |

---

### pgy_get_blogger_notes — 获取博主笔记明细

**Full path:** `/api/v1/xiaohongshu/pgy/get_blogger_notes`
**Method:** POST · **Risk:** high · **requires_user_confirmation:** true · **write_operation:** true

#### 用途
获取蒲公英博主笔记明细列表，包含每篇笔记的互动数据与发布时间。**博主内容产出分析的入口**。

#### 何时使用 / 不使用
- ✅ 已知 user_id，想看博主全部笔记的商业化数据
- ✅ 链式起点：笔记明细 → 单篇笔记详情（pgy_get_note_detail）
- ❌ 只想看转化率指标 → pgy_get_blogger_notes_rate
- ❌ 想看小红书原站笔记详情 → note.md 的 get_image_note_detail / get_video_note_detail

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| user_id | string | yes | — | 蒲公英博主 user_id |
| page_number | integer | no | min=1, default=1 | 页码，从 1 开始 |
| page_size | integer | no | min=1, max=50, default=20 | 每页数量，最大 50 |
| note_type | integer | no | enum=`1, 2` | 笔记类型：1=图文, 2=视频，默认全部 |
| order_type | integer | no | enum=`1, 2, 3` | 排序：1=最新, 2=最热, 3=互动最高，默认 1 |
| advertise_switch | integer | no | enum=`0, 1` | 是否包含广告笔记：0=否, 1=是，默认 0 |

> **请求体格式**：`{"user_id":"xxx","page_number":1,"page_size":20,"note_type":1,"order_type":2,"advertise_switch":0}`。
> **翻页说明**：page_number 从 1 开始递增。

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| notes[].note_id | `$.data.notes[].note_id` | 笔记 ID | pgy_get_note_detail / note.md 多端点 |
| user_id | `$.data.user_id` | 博主 user_id（回显） | 本文件博主系端点复用 |

#### 错误处理 (ERR)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 404 | 博主不在蒲公英库 | STOP | 0 | 改用 `user.md` get_user_posted_notes 取原站笔记 |
| 空数据 | 暂无笔记 | 返回"暂无笔记" | 0 | — |

---

### pgy_get_blogger_notes_rate — 获取博主笔记转化率

**Full path:** `/api/v1/xiaohongshu/pgy/get_blogger_notes_rate`
**Method:** POST · **Risk:** high · **requires_user_confirmation:** true · **write_operation:** true

#### 用途
获取蒲公英博主笔记转化率数据，包含 CTR、互动率、收藏率等转化漏斗指标。

#### 何时使用 / 不使用
- ✅ 已知 user_id，想分析笔记转化效果
- ✅ 链式终点：核心数据 → 转化率
- ❌ 想看具体笔记列表 → pgy_get_blogger_notes
- ❌ 想看核心数据（CPE/CPM）→ pgy_get_blogger_core_data

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| user_id | string | yes | — | 蒲公英博主 user_id |
| note_type | integer | no | enum=`1, 2` | 笔记类型：1=图文, 2=视频，默认全部 |
| date_type | integer | no | enum=`1, 2, 3` | 时间范围：1=近 30 天, 2=近 90 天, 3=近 180 天，默认 1 |
| advertise_switch | integer | no | enum=`0, 1` | 是否包含广告笔记：0=否, 1=是，默认 0 |

> **请求体格式**：`{"user_id":"xxx","note_type":1,"date_type":1,"advertise_switch":0}`。

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| user_id | `$.data.user_id` | 博主 user_id（回显） | 本文件博主系端点复用 |

#### 错误处理 (ERR)
同 pgy_get_blogger_core_data。

---

### pgy_get_note_detail — 获取蒲公英笔记详情

**Full path:** `/api/v1/xiaohongshu/pgy/get_note_detail`
**Method:** POST · **Risk:** high · **requires_user_confirmation:** true · **write_operation:** true

#### 用途
获取蒲公英笔记详情，包含笔记的商业化数据（如该笔记是否为广告笔记、合作品牌等）。

#### 何时使用 / 不使用
- ✅ 已知 note_id，想看笔记在蒲公英侧的商业化数据
- ✅ 链式终点：博主笔记明细 → 单篇笔记详情
- ❌ 想看小红书原站笔记内容 → note.md 的 get_image_note_detail / get_video_note_detail / fetch_note_detail
- ❌ 不知 note_id → 先用 pgy_get_blogger_notes 取博主笔记列表

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| note_id | string | yes | — | 笔记 ID（24 位 hex） |

> **请求体格式**：`{"note_id":"xxx"}`。

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| note_id | `$.data.note_id` | 笔记 ID（回显） | note.md 多端点（取原站详情） |
| user_id | `$.data.user_id` | 笔记作者 user_id | 本文件博主系端点 |

#### 错误处理 (ERR · 端点特化)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 404 | 笔记不在蒲公英库 | STOP | 0 | 改用 `note.md` get_image_note_detail 取原站详情 |
| 空数据 | 笔记暂无可取商业化数据 | 返回"暂无可取商业化数据" | 0 | — |
