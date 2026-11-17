---
name: linkfox-amazon-store-aplus-content
description: 亚马逊店铺 A+ Content（增强品牌内容）管理。用于查询、创建和更新 A+ 内容文档，关联或解除 ASIN，校验关联关系，查询发布记录，提交审核以及暂停展示等品牌详情页运营场景。用户提到亚马逊 A+ 页面、A+ Content、增强品牌内容、EBC、图文详情、A+ 审核、A+ 发布、ASIN 关联、contentReferenceKey、contentPublishRecords 时触发。即使未明确提及 A+ API，只要希望管理亚马逊商品详情页中的品牌图文模块，也应触发此技能。
---

# Amazon 店铺 A+ Content Management

本 skill 与 **`linkfox-amazon-store-auth`**、**`linkfox-amazon-store-listings`** 等同属 **Amazon Store** 系列：依赖 auth 选店（`sellerId`+`region`）；直接 **`POST /spApi/developerProxy`** 传入 `sellerId`+`region`，由服务端解析 token（勿传 `amzAccessToken`，除非兼容旧调用）。转发上游 **GET** 或 **POST**。

| 操作 | 官方参考 |
|------|----------|
| 搜索文档列表 | [searchContentDocuments](https://developer-docs.amazon.com/sp-api/reference/searchcontentdocuments) |
| 新建文档 | [createContentDocument](https://developer-docs.amazon.com/sp-api/reference/createcontentdocument) |
| 获取文档（内容/元数据） | [getContentDocument](https://developer-docs.amazon.com/sp-api/reference/getcontentdocument) |
| 更新文档 | [updateContentDocument](https://developer-docs.amazon.com/sp-api/reference/updatecontentdocument) |
| 列出 ASIN 关联 | [listContentDocumentAsinRelations](https://developer-docs.amazon.com/sp-api/reference/listcontentdocumentasinrelations) |
| 替换 ASIN 关联 | [postContentDocumentAsinRelations](https://developer-docs.amazon.com/sp-api/reference/postcontentdocumentasinrelations) |
| 校验文档与 ASIN | [validateContentDocumentAsinRelations](https://developer-docs.amazon.com/sp-api/reference/validatecontentdocumentasinrelations) |
| 按 ASIN 查发布记录 | [searchContentPublishRecords](https://developer-docs.amazon.com/sp-api/reference/searchcontentpublishrecords) |
| 提交审核/发布 | [postContentDocumentApprovalSubmission](https://developer-docs.amazon.com/sp-api/reference/postcontentdocumentapprovalsubmission) |
| 暂停前台展示 | [postContentDocumentSuspendSubmission](https://developer-docs.amazon.com/sp-api/reference/postcontentdocumentsuspendsubmission) |

---

## 调用方式

- **API 端点**：`POST /spApi/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`（可用脚本见上文脚本一览）
- **成本约束**：本工具会消耗算力；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-store-aplus-content-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录，在 Claude Code 里即当前项目目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；**禁止写入 /tmp**，当前目录不可写则报错）
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq`或`ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

---

## 解决认证和算力问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或余额不足**：消息含"算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

## Prerequisites（必须先读）

本 skill **依赖** **`linkfox-amazon-store-auth`**。

1. 运行 `python scripts/check_auth_dependency.py`；若 exit code **42** 且 stderr 含 `DEPENDENCY_MISSING:`，请先安装 **`linkfox-amazon-store-auth`**。
2. **不要**在本 skill 内绕过依赖实现授权或令牌逻辑。

---

## Current Capabilities

| 能力 | Path 要点 | 脚本 |
|------|-----------|------|
| 搜索 A+ 文档 | `aplus/2020-11-01/contentDocuments` + `marketplaceId` | `scripts/search_content_documents.py` |
| 创建 A+ 文档 | 同上 **POST** + body `contentDocument` | `scripts/create_content_document.py` |
| 获取单篇文档 | `.../contentDocuments/{contentReferenceKey}` + `includedDataSet`（必填，至少 1 项） | `scripts/get_content_document.py` |
| 更新文档 | 同上 **POST** + body | `scripts/update_content_document.py` |
| 列出关联 ASIN | `.../contentDocuments/{key}/asins` | `scripts/list_content_document_asin_relations.py` |
| 全量替换关联 ASIN | `.../asins` **POST** + body `asinSet` | `scripts/post_content_document_asin_relations.py` |
| 校验与 ASIN 的可用性 | `.../contentAsinValidations` **POST** | `scripts/validate_content_document_asin_relations.py` |
| 发布记录（按 ASIN） | `.../contentPublishRecords` + `asin` | `scripts/search_content_publish_records.py` |
| 提交审核 | `.../approvalSubmissions` **POST** | `scripts/post_content_document_approval_submission.py` |
| 暂停展示 | `.../suspendSubmissions` **POST** | `scripts/post_content_document_suspend_submission.py` |

**注意**：`postContentDocumentAsinRelations` 为 **全量替换** `asinSet`；从集合中移除 ASIN 会导致该 ASIN 上内容被 **suspend**（以 Amazon 行为为准）。详见 **`references/api.md`**。

---

## Quick Parameters

### 通用

| 字段 | 必填 | 说明 |
|------|------|------|
| sellerId | 是 | 已授权 Seller ID（与 `storeTokens` 一致） |
| region | 是 | `NA` / `EU` / `FE` |
| marketplaceId **或** marketplaceIds | 是 | 目标站点；数组时脚本仅取 **第一个** |

### contentReferenceKey

多数操作需要 **`contentReferenceKey`**（来自 `searchContentDocuments` 等）。官方说明该 key **非永久链接**、未来可能变化。

### getContentDocument

| 字段 | 必填 | 说明 |
|------|------|------|
| includedDataSet | 是 | 至少一项；**`CONTENTS`**、**`METADATA`**（可并存） |

### searchContentPublishRecords

| 字段 | 必填 | 说明 |
|------|------|------|
| asin | 是 | 长度 ≥ 10 |

---

## Scripts

- **`scripts/search_content_documents.py`**
- **`scripts/create_content_document.py`**
- **`scripts/get_content_document.py`**
- **`scripts/update_content_document.py`**
- **`scripts/list_content_document_asin_relations.py`**
- **`scripts/post_content_document_asin_relations.py`**
- **`scripts/validate_content_document_asin_relations.py`**
- **`scripts/search_content_publish_records.py`**
- **`scripts/post_content_document_approval_submission.py`**
- **`scripts/post_content_document_suspend_submission.py`**
- **`scripts/check_auth_dependency.py`**

示例：

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/search_content_documents.py '{"sellerId":"A1...","region":"NA","marketplaceId":"ATVPDKIKX0DER"}'

python scripts/get_content_document.py '{"sellerId":"A1...","region":"NA","marketplaceId":"ATVPDKIKX0DER","contentReferenceKey":"YOUR_KEY","includedDataSet":["CONTENTS","METADATA"]}'

python scripts/post_content_document_asin_relations.py '{"sellerId":"A1...","region":"NA","marketplaceId":"ATVPDKIKX0DER","contentReferenceKey":"YOUR_KEY","asinSet":["B0XXXXXXXXXX"]}'

python scripts/search_content_publish_records.py '{"sellerId":"A1...","region":"NA","marketplaceId":"ATVPDKIKX0DER","asin":"B0XXXXXXXXXX"}'

python scripts/post_content_document_approval_submission.py '{"sellerId":"A1...","region":"NA","marketplaceId":"ATVPDKIKX0DER","contentReferenceKey":"YOUR_KEY"}'
```

---

## Display Rules

1. 先展示网关 **`errcode` / `httpStatus`**；成功后再解析 **`developerProxy.body`** 或各脚本附带的 **`*Response`** 字段。
2. 说明 **`contentReferenceKey`** 与前台「A+ ID」不一定一致。
3. 写操作（创建/更新/关联/校验/提交/暂停）前确认用户意图；**替换 ASIN** 与 **暂停展示** 影响线上详情页。

---

## Important Limitations

- **应用权限**：Seller Central 应用须具备 A+ Content 相关 **角色/权限**；否则 **403**。
- **白名单**：`aplus/2020-11-01/` 须在网关 developerProxy 放行；**1005** 需运维配置。
- **`contentDocument`** 结构复杂，须符合 **Amazon 官方模型**；本 skill 只做透传，不内置模板校验。
- **marketplaceId**：A+ 接口 Query 使用单数 **`marketplaceId`**（与 Listings 的 `marketplaceIds` 不同）。

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

**Feedback：** 见 `references/api.md`，`skillName`：`linkfox-amazon-store-aplus-content`。

---
*更多跨境 skill：[LinkFox Skills](https://skill.linkfox.com/)*
