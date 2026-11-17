---
name: linkfox-amazon-store-feeds
description: 亚马逊店铺 Feed 批量数据提交与处理状态管理。用于创建 Feed 文档、向预签名地址上传 Feed 内容、提交库存或 Listing 等批量文件、查询或列出 Feed、获取结果文档以及取消 Feed。用户提到亚马逊 Feed、批量更新库存或商品、提交 Listing Feed、POST_FLAT_FILE、feedType、feedDocumentId、feedId、Feed 处理状态、Feed 结果、取消 Feed、Feeds API 时触发。即使未明确说“Feed”，只要希望通过亚马逊 SP-API 批量提交结构化商品或库存数据，也应触发此技能；单个 Listing 的增删改查使用 linkfox-amazon-store-listings。
---

# Amazon 店铺 Feeds

本 skill 与 **`linkfox-amazon-store-auth`** 等同属 **Amazon Store** 系列：依赖 **`linkfox-amazon-store-auth`** 选店（`sellerId`+`region`）；直接 **`POST /spApi/developerProxy`** 传入 `sellerId`+`region`，由服务端解析 token（勿传 `amzAccessToken`，除非兼容旧调用）。转发 **GET / POST / DELETE**。

## 调用方式

- **API 端点**：`POST /spApi/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（可用脚本见上文脚本一览）
- **成本约束**：本工具会消耗算力；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-store-feeds-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 解决认证和算力问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或余额不足**：消息含"算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

## 官方参考索引

| 能力 | 文档 |
|------|------|
| createFeedDocument | [createFeedDocument](https://developer-docs.amazon.com/sp-api/reference/createfeeddocument) |
| getFeedDocument | [getFeedDocument](https://developer-docs.amazon.com/sp-api/reference/getfeeddocument) |
| createFeed | [createFeed](https://developer-docs.amazon.com/sp-api/reference/createfeed) |
| getFeed | [getFeed](https://developer-docs.amazon.com/sp-api/reference/getfeed) |
| getFeeds | [getFeeds](https://developer-docs.amazon.com/sp-api/reference/getfeeds) |
| cancelFeed | [cancelFeed](https://developer-docs.amazon.com/sp-api/reference/cancelfeed) |

---

## Prerequisites

1. 依赖 **`linkfox-amazon-store-auth`**；运行 `python scripts/check_auth_dependency.py`，exit **42** 时需先安装授权 skill。
2. 应用需具备 **Feeds** 相关角色；`feedType` 须与上传文件格式匹配（见 Amazon Feed Type Values 文档）。

---

## 典型工作流

1. **`create_feed_document.py`** → 得到 `feedDocumentId` 与 **`url`**（上传地址）。
2. **`upload_feed_document.py`** → 对 `url` **PUT** 上传 feed 文件（**不经** developerProxy）。
3. **`create_feed.py`** → 传入 `inputFeedDocumentId`、`feedType`、`marketplaceIds`。
4. **`get_feed.py`** / **`get_feeds.py`** → 轮询 `processingStatus`（如 IN_QUEUE、IN_PROGRESS、DONE、FATAL）。
5. 处理完成后用 **`get_feed_document.py`** 下载 **resultFeedDocumentId** 对应文档（再按返回 URL 自行下载结果文件）。

---

## Current Capabilities

| 能力 | path | method | 脚本 |
|------|------|--------|------|
| createFeedDocument | `feeds/2021-06-30/documents` | POST | `create_feed_document.py` |
| getFeedDocument | `feeds/2021-06-30/documents/{feedDocumentId}` | GET | `get_feed_document.py` |
| createFeed | `feeds/2021-06-30/feeds` | POST | `create_feed.py` |
| getFeed | `feeds/2021-06-30/feeds/{feedId}` | GET | `get_feed.py` |
| getFeeds | `feeds/2021-06-30/feeds` | GET | `get_feeds.py` |
| cancelFeed | `feeds/2021-06-30/feeds/{feedId}` | DELETE | `cancel_feed.py` |
| 上传文档内容 | createFeedDocument 返回的 URL | PUT | `upload_feed_document.py` |

共享模块：**`_spapi_feeds_common.py`**。

---

## Scripts 示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/create_feed_document.py '{"sellerId":"A1...","region":"NA","contentType":"text/tab-separated-values; charset=UTF-8"}'

python scripts/upload_feed_document.py '{"uploadUrl":"<from createFeedDocument>","contentType":"text/tab-separated-values; charset=UTF-8","filePath":"./inventory.tsv"}'

python scripts/create_feed.py '{"sellerId":"A1...","region":"NA","feedType":"POST_FLAT_FILE_INVLOADER_DATA","marketplaceIds":["ATVPDKIKX0DER"],"inputFeedDocumentId":"<feedDocumentId>"}'
```

---

## Display Rules

1. 先看 **`developerProxy.errcode` / `httpStatus`**；createFeedDocument 常为 **201**，createFeed 常为 **202**。
2. **getFeeds** 分页：仅用上一页 **`nextToken`** 作为下一请求的 **`paginationToken` 参数名在 Amazon 侧为 `nextToken`**（脚本字段名 `nextToken`）。
3. **upload** 失败与 SP-API 网关无关，检查 `uploadUrl` 是否过期、**Content-Type** 是否与 createFeedDocument 一致。
4. 网关 path 白名单需包含 **`feeds/2021-06-30/`** 前缀。

---

## Important Limitations

- 本 skill **不**代替 Amazon 侧 feed 文件 schema 校验；`feedType`、TSV/XML 格式以官方为准。
- 下载 **getFeedDocument** 返回的 **url** 内容需另行 HTTP GET（与 upload 类似，不经 developerProxy）。
- 详见 **`references/api.md`**。

## Amazon SP-API 接口保护与重试指引

同一店铺连续收到 Amazon SP-API 的 400、403、404 或 429 时，网关会返回 450、453、454 或 459 并短暂冷却。这些自定义状态码不是 Amazon 原生状态，也不表示封号；目的是避免持续异常或高频调用扩大店铺风险。

| 状态与 message | 范围 | 触发与冷却 | 处理 |
|---|---|---|---|
| `450`：`400，请求异常，请优化您的参数` | 店铺+接口 | 60 秒内超过 3 次：5 分钟；10 分钟内超过 4 次：20 分钟 | 停止原参数重试，检查必填字段、marketplace、ID、日期和请求体 |
| `453`：`403，店铺未授权，请先授权` | 店铺全部接口 | 60 秒内超过 2 次：5 分钟；10 分钟内超过 4 次：30 分钟 | 停止该店铺调用，检查授权、权限、店铺归属和区域 |
| `454`：`404，资源不存在，请优化您的参数` | 店铺+接口 | 60 秒内超过 3 次：5 分钟；10 分钟内超过 4 次：30 分钟 | 确认资源 ID、所属店铺/站点、资源状态和接口路径 |
| `459`：`429限流中，请降低频率` | 店铺+接口 | 首次：15 秒；2 分钟内超过 2 次：30 秒；3 分钟内超过 4 次：2 分钟 | 降低并发、分页和轮询频率并逐级退避 |

- 立即停止自动或并发重试，不得通过换脚本或重复创建任务绕过保护；优先遵循 `retryAfter`、`blockedUntil`，没有时按表中时长说明。
- 450/453/454 必须先修正参数、授权或资源标识，冷却后最多谨慎重试一次；再次触发则停止调用。453 期间停止该店铺全部 SP-API。
- 保留已有 `reportId`、`feedId` 等任务 ID；写操作结果不确定时先查询状态，不直接重放。
- 向用户先说明店铺保护，再给原因、处理和等待时间。可回复：“为保护您的亚马逊店铺安全，检测到 Amazon SP-API 连续返回{原因}，当前已进入短暂保护。请先{处理动作}，预计{等待时间}后再试；这不代表封号，也不是套餐或算力限制。”不要只说“LinkFox 限流”或“服务器繁忙”。

## 算力消耗规则

不消耗算力。

**Feedback：** `skillName`：`linkfox-amazon-store-feeds`。

---
*更多跨境 skill：[LinkFox Skills](https://skill.linkfox.com/)*

