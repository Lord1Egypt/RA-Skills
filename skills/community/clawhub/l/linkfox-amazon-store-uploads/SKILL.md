---
name: linkfox-amazon-store-uploads
description: 亚马逊 SP-API 通用文件上传。用于为 A+ Content、Messaging 等业务创建 upload destination，计算 contentMD5，并将图片或附件上传到返回的预签名地址。用户提到亚马逊文件上传、A+ 图片上传、Messaging 附件、createUploadDestinationForResource、upload destination、contentMD5、预签名上传、Uploads API、SP-API 上传文件时触发。即使未明确说“Uploads API”，只要其他亚马逊 SP-API 操作需要先获得可引用的上传资源地址，也应触发此技能；Feed 文档上传使用 linkfox-amazon-store-feeds 的专用流程。
---

# Amazon 店铺 Uploads（文件上传）

本 skill 专用于 **向 Amazon 申请上传目的地并上传文件**，与 **`linkfox-amazon-store-auth`** 同系列：依赖 **`linkfox-amazon-store-auth`** 选店（`sellerId`+`region`）；直接 **`POST /spApi/developerProxy`** 传入 `sellerId`+`region` 调用 **createUploadDestinationForResource**，最后用 **`upload_to_destination.py`** 对返回的 URL 执行 **PUT**（不经网关）。

> 这是 **Uploads API**，不是 Orders 订单接口。订单见 **`linkfox-amazon-store-orders`**；批量 Feed 文件见 **`linkfox-amazon-store-feeds`**。

## 调用方式

- **API 端点**：`POST /spApi/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（可用脚本见上文脚本一览）
- **成本约束**：本工具会消耗算力；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-store-uploads-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
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

## 官方参考

[createUploadDestinationForResource](https://developer-docs.amazon.com/sp-api/reference/createuploaddestinationforresource) · [Create an upload destination](https://developer-docs.amazon.com/sp-api/docs/create-an-upload-destination)

---

## Prerequisites

1. 依赖 **`linkfox-amazon-store-auth`**。
2. **`resource`** 须与下游 API 文档一致（例如 A+：`aplus/2020-11-01/contentDocuments`；Messaging 为对应 messages 资源路径）。
3. **`contentMD5`** 为待上传文件内容的 **Base64 MD5 摘要**；传 **`filePath`** / **`content`** 时脚本可自动计算。

---

## 工作流

```text
create_upload_destination_for_resource  →  uploadDestination { uploadDestinationId, url, headers }
upload_to_destination (PUT url + headers)  →  在 A+/Messaging 等 API 中引用 uploadDestinationId
```

---

## Scripts

| 脚本 | 说明 |
|------|------|
| `create_upload_destination_for_resource.py` | POST `uploads/2020-11-01/uploadDestinations/{resource}` |
| `upload_to_destination.py` | PUT 到返回的 `url`（带 `headers`） |
| `_spapi_uploads_common.py` | 内部公共模块 |

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

# 1) 创建上传目的地（自动根据 filePath 计算 contentMD5）
python scripts/create_upload_destination_for_resource.py '{
  "sellerId":"A1...",
  "region":"NA",
  "resource":"aplus/2020-11-01/contentDocuments",
  "marketplaceId":"ATVPDKIKX0DER",
  "filePath":"/path/to/banner.jpg",
  "contentType":"image/jpeg"
}'

# 2) 上传文件（将上一步 stdout 中的 uploadDestination 传入）
python scripts/upload_to_destination.py '{
  "uploadDestination": { "url": "...", "headers": { } },
  "filePath": "/path/to/banner.jpg"
}'
```

---

## Display Rules

1. 成功创建目的地常为 **HTTP 201**；先看 **`developerProxy`**，再看 **`uploadDestination`**。
2. **`resource`** 传未编码的下游资源路径；可带或不带前导 `/`，生成 path 时保留内部 `/`（greedy path），不得预编码成 `%2F`。
3. 网关需放行 **`uploads/2020-11-01/`** 前缀。

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

**Feedback：** `skillName`：`linkfox-amazon-store-uploads`。

---
*更多跨境 skill：[LinkFox Skills](https://skill.linkfox.com/)*
