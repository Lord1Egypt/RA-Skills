# Zhihu Pins / 知乎 想法

Base URL: `https://www.aconfig.cn` · Auth: `Authorization: Bearer $MAXHUB_API_KEY`

## 本文件覆盖
知乎想法（Pin）详情与评论区 —— 围绕"想法"的全部读取入口。**pin_id 多在本文件首步产出**（fetch_pin_detail 是已知 pin_id 时的链式入口，可链式到 fetch_pin_comments 拉评论区）。

## 端点索引 (Endpoint Index)
| ID | 推荐度 | 一句话用途 | Method | Path | Risk |
|----|-------|----------|--------|------|------|
| web_fetch_pin_detail | ⭐⭐⭐ 首选 | 用 pin_id 取想法详情 | GET | /api/v1/zhihu/web/fetch_pin_detail | low |
| web_fetch_pin_comments | ⭐⭐ 条件 | 用 pin_id 取想法评论区 | GET | /api/v1/zhihu/web/fetch_pin_comments | low |

## 链式调用图谱 (Chain Recipes)

| 用户目标 | 链路 | 字段流 | 容错 |
|---------|------|-------|------|
| 想法详情 → 评论区 | web_fetch_pin_detail → web_fetch_pin_comments | `pin_id` 复用 | 第 2 步失败：返回详情 + "评论暂不可取" |
| 用户想法 → 想法详情 | user.md web_fetch_user_pins → web_fetch_pin_detail | `$.data.data[].id` → `pin_id` | 跨文件链路 |

## 跨 reference 链路 (In-Chain)
- **流入本文件**：`user.md` 的 `web_fetch_user_pins` 输出 `pin_id` → 本文件
- **流出本文件**：`web_fetch_pin_comments` 输出评论作者标识 → `user.md` user 系端点

## 错误处理契约

> **完整 HTTP 状态码语义与决策表见 [`param-mappings.md` § 3](./param-mappings.md#3-全-skill-错误处理总览-error-handling-overview)**

### 通用规则
- 404/410 → 防臆造自检后 STOP
- 400/422 → 防臆造自检后修正重试 ≤1 次
- 401/402/403 → STOP
- 429 → 退避重试 ≤2 次
- 5xx → 等 3s 重试 ≤1 次
- 业务 code≠0 → 读 message_zh，不重试

---

## 端点详情

### web_fetch_pin_detail — 获取知乎想法详情

**Full path:** `/api/v1/zhihu/web/fetch_pin_detail`
**Method:** GET · **Risk:** low

#### 用途
获取指定知乎想法（Pin）的完整详情。**pin 系链式调用的常见起点**。

> ⚠️ 注意：本端点 id 在白名单中为 `web_fetch_pin_detail`（带 `web_` 前缀），调用前需按白名单逐字符核对。

#### 何时使用 / 不使用
- ✅ 已知 pin_id，想查看想法正文、作者、互动数据
- ❌ 想看用户全部想法列表 → 用 `user.md` 的 `web_fetch_user_pins`

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| pin_id | string | yes | — | 想法 ID |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| id | `$.data.id` | 想法 ID（回显） | web_fetch_pin_comments |
| author.url_token | `$.data.author.url_token` | 作者用户标识 | user.md |

#### 错误处理 (ERR)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 404 | 想法不存在 | STOP | 0 | — |
| 5xx | 上游故障 | 等 3s 重试 | ≤1 次 | 无替代 |

---

### web_fetch_pin_comments — 获取知乎想法评论区

**Full path:** `/api/v1/zhihu/web/fetch_pin_comments`
**Method:** GET · **Risk:** low

#### 用途
获取指定知乎想法（Pin）的评论列表。常配合 `web_fetch_pin_detail` 使用。

#### 输入 (IN)
| name | type | required | constraints | 说明 |
|------|------|----------|-------------|------|
| pin_id | string | yes | — | 想法 ID（从 web_fetch_pin_detail 或 web_fetch_user_pins 获取） |
| order_by | string | no | — | 排序方式（如 score=最热，ts=最新） |
| limit | string | no | — | 每页评论数量 |
| offset | string | no | — | 偏移量/页码 |

#### 输出可链式字段 (OUT)
| 字段 | json_path | 语义 | 下游端点 |
|------|-----------|------|---------|
| data[].author.url_token | `$.data.data[].author.url_token` | 评论者标识 | user.md |

#### 错误处理 (ERR)
| code | 含义 | 行动 | 重试 | 降级/替换 |
|------|------|------|------|----------|
| 404 | 想法不存在或无评论 | STOP | 0 | — |
| 5xx | 上游故障 | 等 3s 重试 | ≤1 次 | 无替代 |
