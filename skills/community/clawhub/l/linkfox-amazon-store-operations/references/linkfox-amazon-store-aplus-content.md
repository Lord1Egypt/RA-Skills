---
name: linkfox-amazon-store-aplus-content
description: 亚马逊店铺 A+ Content（增强图文页）管理。支持 A+ 页面检索、创建、更新、ASIN 关联验证、审核提交与暂停展示等 SP-API A+ 功能。
---

# Amazon 店铺 A+ Content 管理

本 skill 与 **`linkfox-amazon-store-auth`**、**`linkfox-amazon-store-listings`** 同属 Amazon Store 系列：使用 `POST /spApi/storeTokens` 取 `accessToken`，再经 `POST /spApi/developerProxy` 转发上游 SP-API A+ Content Management v2020-11-01。完整参数、响应与错误码见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- A+ 文档检索（`searchContentDocuments`）、创建（`createContentDocument`）、获取（`getContentDocument`）、更新（`updateContentDocument`）。
- ASIN 关联管理：列出（`listContentDocumentAsinRelations`）、全量替换（`postContentDocumentAsinRelations`）、校验（`validateContentDocumentAsinRelations`）。
- 发布记录查询（`searchContentPublishRecords`，按 ASIN）。
- 提交审核发布（`postContentDocumentApprovalSubmission`）、暂停前台展示（`postContentDocumentSuspendSubmission`）。

### ❌ 边界与限制

- **前置依赖**：须先安装并完成 **`linkfox-amazon-store-auth`** 授权；本 skill 不内置授权逻辑。运行 `python scripts/check_auth_dependency.py`，若 exit code **42** 且 stderr 含 `DEPENDENCY_MISSING:`，请先安装该依赖。
- **应用权限**：Seller Central 应用须具备 A+ Content 相关角色/权限，否则 **403**。
- **网关白名单**：`aplus/2020-11-01/` 须在网关 developerProxy 放行；`errcode=1005` 需运维配置。
- **内容结构**：`contentDocument` 结构复杂，须符合 Amazon 官方模型；本 skill 只做透传，不内置模板校验。
- **marketplaceId 单数**：A+ 接口 Query 使用单数 `marketplaceId`（与 Listings 的 `marketplaceIds` 不同）。
- **contentReferenceKey 非永久**：官方说明该 key 非永久链接，未来可能变化。
- **不在范围内**：店铺授权与令牌管理（用 `linkfox-amazon-store-auth`）；Listing 与商品管理（用 `linkfox-amazon-store-listings`）；A+ 模板设计与内容创作建议；图片素材制作。

## 执行流程

A+ 内容管理通常为多步编排，按需选择下列步骤。

### 步骤 1：前置依赖检查
- 【输入】本 skill 所在目录
- 【动作】运行 `python scripts/check_auth_dependency.py`，确认 `linkfox-amazon-store-auth` 已安装并完成授权
- 【输出】依赖通过则继续；exit code 42 则先安装依赖

### 步骤 2：获取 A+ 文档列表
- 【输入】`sellerId`、`region`、`marketplaceId`（可选 `pageToken`）
- 【动作】运行 `scripts/search_content_documents.py`，调用 `searchContentDocuments`
- 【输出】文档元数据列表，获取目标文档的 `contentReferenceKey`

### 步骤 3：获取或创建文档内容
- 【输入】`contentReferenceKey`（获取）或 `contentDocument` 对象（创建）
- 【动作】运行 `scripts/get_content_document.py`（含 `includedDataSet`：`CONTENTS`/`METADATA`）读取内容，或 `scripts/create_content_document.py` 新建
- 【输出】完整 A+ 文档内容与元数据

### 步骤 4：更新文档与 ASIN 关联
- 【输入】`contentReferenceKey`、更新后的 `contentDocument`；关联所需的 `asinSet`
- 【动作】按需运行 `scripts/update_content_document.py` 更新内容；`scripts/post_content_document_asin_relations.py` 全量替换关联 ASIN；`scripts/validate_content_document_asin_relations.py` 校验可用性
- 【输出】更新结果与 ASIN 校验结果

### 步骤 5：提交审核或暂停展示
- 【输入】`contentReferenceKey`
- 【动作】运行 `scripts/post_content_document_approval_submission.py` 提交审核发布，或 `scripts/post_content_document_suspend_submission.py` 暂停前台展示
- 【输出】提交结果；可用 `scripts/search_content_publish_records.py`（按 `asin`）查询发布记录

## 调用方式

- **API 端点**：`POST /spApi/developerProxy`（不同操作通过请求体区分；完整参数/响应/错误码见 `references/api.md`）。
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`。
- **成本约束**：本工具会消耗积分；失败/空结果不得自动换关键词、翻页或连续试探；需要继续检索时先向用户说明会产生额外消耗。

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-store-aplus-content-<timestamp>.json`（`<cwd>` 为脚本执行时的工作目录；`<session>` 取自环境变量 `SESSION_ID`，按用户任务自动聚合；禁止写入 /tmp，当前目录不可写则报错）。
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout。
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）。
- 加 `--inline` 强制全量打印到 stdout（同样落盘）。

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。

## 使用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

# 搜索 A+ 文档列表
python scripts/search_content_documents.py '{"sellerId":"A1...","region":"NA","marketplaceId":"ATVPDKIKX0DER"}'

# 获取单篇文档（含内容与元数据）
python scripts/get_content_document.py '{"sellerId":"A1...","region":"NA","marketplaceId":"ATVPDKIKX0DER","contentReferenceKey":"YOUR_KEY","includedDataSet":["CONTENTS","METADATA"]}'

# 全量替换关联 ASIN
python scripts/post_content_document_asin_relations.py '{"sellerId":"A1...","region":"NA","marketplaceId":"ATVPDKIKX0DER","contentReferenceKey":"YOUR_KEY","asinSet":["B0XXXXXXXXXX"]}'

# 按 ASIN 查发布记录
python scripts/search_content_publish_records.py '{"sellerId":"A1...","region":"NA","marketplaceId":"ATVPDKIKX0DER","asin":"B0XXXXXXXXXX"}'

# 提交审核发布
python scripts/post_content_document_approval_submission.py '{"sellerId":"A1...","region":"NA","marketplaceId":"ATVPDKIKX0DER","contentReferenceKey":"YOUR_KEY"}'
```

## 展示规则

1. 先展示网关 `errcode` / `httpStatus`；成功后再解析 `developerProxy.body` 或各脚本附带的 `*Response` 字段。
2. 说明 `contentReferenceKey` 与前台「A+ ID」不一定一致。
3. 写操作（创建/更新/关联/校验/提交/暂停）前确认用户意图；替换 ASIN 与暂停展示影响线上详情页。
4. `postContentDocumentAsinRelations` 为全量替换 `asinSet`，从集合中移除 ASIN 会导致该 ASIN 上内容被 suspend，须提示用户。

## 用户表达与场景速查

**适用** —— 亚马逊店铺 A+ Content 管理：

| 用户说 | 场景 |
|--------|------|
| "查一下我店铺的 A+ 页面"、"A+ 文档列表" | 搜索 A+ 文档 |
| "新建一个 A+ 页面"、"创建 A+ Content" | 创建文档 |
| "看下这个 A+ 的内容"、"获取 A+ 详情" | 获取文档 |
| "更新 A+ 页面"、"修改 A+ Content" | 更新文档 |
| "这个 A+ 关联了哪些 ASIN"、"给 A+ 加 ASIN" | ASIN 关联管理 |
| "校验 A+ 能不能用这些 ASIN" | ASIN 校验 |
| "这个 ASIN 的 A+ 发布记录" | 发布记录查询 |
| "提交 A+ 审核"、"发布 A+ Content" | 提交审核 |
| "暂停这个 A+ 的展示" | 暂停展示 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题

发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应 401 或 402 状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用 skill 内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个 skill 并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个 skill。

---

# Amazon 店铺 A+ Content Management API 参考（v2020-11-01）

本文档描述通过 **LinkFox 店铺网关** 调用 Selling Partner API **A+ Content Management v2020-11-01**：`searchContentDocuments`、`createContentDocument`、`getContentDocument`、`updateContentDocument`、`listContentDocumentAsinRelations`、`postContentDocumentAsinRelations`、`validateContentDocumentAsinRelations`、`searchContentPublishRecords`、`postContentDocumentApprovalSubmission`、`postContentDocumentSuspendSubmission`。流程与 **`linkfox-amazon-store-report`** / **`linkfox-amazon-store-listings`** 一致：先 **`POST /spApi/storeTokens`**，再 **`POST /spApi/developerProxy`** 转发上游 **GET** 或 **POST**。

> 官方参考：[searchContentDocuments](https://developer-docs.amazon.com/sp-api/reference/searchcontentdocuments) · [createContentDocument](https://developer-docs.amazon.com/sp-api/reference/createcontentdocument) · [getContentDocument](https://developer-docs.amazon.com/sp-api/reference/getcontentdocument) · [updateContentDocument](https://developer-docs.amazon.com/sp-api/reference/updatecontentdocument) · [listContentDocumentAsinRelations](https://developer-docs.amazon.com/sp-api/reference/listcontentdocumentasinrelations) · [postContentDocumentAsinRelations](https://developer-docs.amazon.com/sp-api/reference/postcontentdocumentasinrelations) · [validateContentDocumentAsinRelations](https://developer-docs.amazon.com/sp-api/reference/validatecontentdocumentasinrelations) · [searchContentPublishRecords](https://developer-docs.amazon.com/sp-api/reference/searchcontentpublishrecords) · [postContentDocumentApprovalSubmission](https://developer-docs.amazon.com/sp-api/reference/postcontentdocumentapprovalsubmission) · [postContentDocumentSuspendSubmission](https://developer-docs.amazon.com/sp-api/reference/postcontentdocumentsuspendsubmission)

> ⚠️ **依赖**：需已安装 **`linkfox-amazon-store-auth`** 并完成店铺授权。

---

## 调用规范

| 项 | 说明 |
|----|------|
| **Base URL** | `${LINKFOX_TOOL_GATEWAY}`（可用 `STORE_API_BASE_URL` 或 `SPAPI_BASE_URL` 覆盖） |
| **网关认证** | Header `Authorization: <api_key>`，环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY`（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理） |
| **店铺令牌** | `POST /spApi/storeTokens`，Body：`{"sellerId":"...","region":"NA\|EU\|FE"}` → `accessToken` |
| **SP-API 转发** | `POST /spApi/developerProxy` |

---

## `POST /spApi/developerProxy`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| region | string | 是 | `NA` / `EU` / `FE` |
| path | string | 是 | **不含**主机名；本 API 统一前缀 **`aplus/2020-11-01/...`**（见各节） |
| method | string | 是 | **`GET`** 或 **`POST`**（A+ 的创建/更新/校验/关联/提交均为 **POST**） |
| amzAccessToken | string | 是 | `storeTokens` 返回的 `accessToken` |
| queryString | string | 视操作 | **无 `?` 前缀**；Query 键名与官方一致（注意单数 **`marketplaceId`**） |
| body | string | 视操作 | **POST** 且带 JSON body 时，为 JSON 字符串；**GET** 不传 |
| contentType | string | 视操作 | 有 body 时建议 **`application/json`** |

**网关响应**（与其它店铺 skill 一致）：解析 **`errcode`**、**`httpStatus`**，再将 **`body`** 字符串 `JSON.parse`。

### 白名单

`path` 须在网关 **`sp-api.developer-proxy.allowed-path-prefixes`** 内。若 **`errcode=1005`**，需运维放行前缀（常见）：**`aplus/2020-11-01/`**。

### 速率（文档默认值）

各操作文档默认多为 **10 req/s**，burst **10**；以响应头 `x-amzn-RateLimit-Limit` 及账号实际配额为准。

### 错误码

- **401**：HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。
- **402**：HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。

---

## 路径与 Query 总览

| 操作 | Method | `developerProxy.path` 模板 |
|------|--------|---------------------------|
| searchContentDocuments | GET | `aplus/2020-11-01/contentDocuments` |
| createContentDocument | POST | `aplus/2020-11-01/contentDocuments` |
| getContentDocument | GET | `aplus/2020-11-01/contentDocuments/{contentReferenceKey}` |
| updateContentDocument | POST | `aplus/2020-11-01/contentDocuments/{contentReferenceKey}` |
| listContentDocumentAsinRelations | GET | `aplus/2020-11-01/contentDocuments/{contentReferenceKey}/asins` |
| postContentDocumentAsinRelations | POST | `aplus/2020-11-01/contentDocuments/{contentReferenceKey}/asins` |
| validateContentDocumentAsinRelations | POST | `aplus/2020-11-01/contentAsinValidations` |
| searchContentPublishRecords | GET | `aplus/2020-11-01/contentPublishRecords` |
| postContentDocumentApprovalSubmission | POST | `aplus/2020-11-01/contentDocuments/{contentReferenceKey}/approvalSubmissions` |
| postContentDocumentSuspendSubmission | POST | `aplus/2020-11-01/contentDocuments/{contentReferenceKey}/suspendSubmissions` |

**Path 编码**：`contentReferenceKey` 等路径段须 **百分号编码**（脚本已处理）。

---

## searchContentDocuments（GET）

| Query | 必填 | 说明 |
|-------|------|------|
| marketplaceId | 是 | 目标站点 id |
| pageToken | 否 | 分页 |

返回文档列表（**元数据**为主）；完整内容需 **`getContentDocument`**。

---

## createContentDocument（POST）

| Query | 必填 | 说明 |
|-------|------|------|
| marketplaceId | 是 | 目标站点 id |

| Body JSON | 必填 | 说明 |
|-----------|------|------|
| contentDocument | 是 | A+ 文档对象（结构以 Amazon 模型为准） |

---

## getContentDocument（GET）

| Query | 必填 | 说明 |
|-------|------|------|
| marketplaceId | 是 | 目标站点 id |
| includedDataSet | **是**（≥1） | 可重复键；取值：**`CONTENTS`**、**`METADATA`** |

---

## updateContentDocument（POST）

| Query | 必填 | 说明 |
|-------|------|------|
| marketplaceId | 是 | 目标站点 id |

| Body JSON | 必填 | 说明 |
|-----------|------|------|
| contentDocument | 是 | 更新后的 A+ 文档 |

---

## listContentDocumentAsinRelations（GET）

| Query | 必填 | 说明 |
|-------|------|------|
| marketplaceId | 是 | 目标站点 id |
| includedDataSet | 否 | 可选 **`METADATA`**；不传则通常仅返回关联 ASIN |
| asinSet | 否 | 可重复；筛选指定 ASIN |
| pageToken | 否 | 分页 |

---

## postContentDocumentAsinRelations（POST）

| Query | 必填 | 说明 |
|-------|------|------|
| marketplaceId | 是 | 目标站点 id |

| Body JSON | 必填 | 说明 |
|-----------|------|------|
| asinSet | 是 | **替换**该文档关联的全部 ASIN（官方语义为全量替换；移除 ASIN 会 suspend 该 ASIN 上的内容）。可为 **字符串数组**，或与官方 schema 一致的对象数组 |

---

## validateContentDocumentAsinRelations（POST）

| Query | 必填 | 说明 |
|-------|------|------|
| marketplaceId | 是 | 目标站点 id |
| asinSet | 否 | 可重复；待校验 ASIN 集合 |

| Body JSON | 必填 | 说明 |
|-----------|------|------|
| contentDocument | 是 | 待校验的 A+ 文档 |

---

## searchContentPublishRecords（GET）

| Query | 必填 | 说明 |
|-------|------|------|
| marketplaceId | 是 | 目标站点 id |
| asin | 是 | ASIN，文档要求 **length ≥ 10** |
| pageToken | 否 | 分页 |

---

## postContentDocumentApprovalSubmission（POST）

| Query | 必填 | 说明 |
|-------|------|------|
| marketplaceId | 是 | 目标站点 id |

**Body**：官方无必填 body；本仓库脚本 **不传** `developerProxy.body`。

---

## postContentDocumentSuspendSubmission（POST）

| Query | 必填 | 说明 |
|-------|------|------|
| marketplaceId | 是 | 目标站点 id |

请求暂停详情页可见 A+；**不删除**文档与 ASIN 关联。脚本 **不传** body。

---

## 脚本入参约定（JSON 一行）

各脚本均需 **`sellerId`**、**`region`**；站点 id 使用 **`marketplaceId`** 或 **`marketplaceIds`**（数组时仅取第一个，与其它店铺 skill 一致）。

| 脚本 | 额外必填 | 可选 |
|------|----------|------|
| `search_content_documents.py` | — | `pageToken` |
| `create_content_document.py` | `contentDocument` | — |
| `get_content_document.py` | `contentReferenceKey`, `includedDataSet` | — |
| `update_content_document.py` | `contentReferenceKey`, `contentDocument` | — |
| `list_content_document_asin_relations.py` | `contentReferenceKey` | `includedDataSet`, `asinSet`, `pageToken` |
| `post_content_document_asin_relations.py` | `contentReferenceKey`, `asinSet` | — |
| `validate_content_document_asin_relations.py` | `contentDocument` | `asinSet`（写入 Query） |
| `search_content_publish_records.py` | `asin` | `pageToken` |
| `post_content_document_approval_submission.py` | `contentReferenceKey` | — |
| `post_content_document_suspend_submission.py` | `contentReferenceKey` | — |

全局可选：**`skipDepCheck`: true**（跳过本地依赖探测，不建议常规使用）。

---

## curl 示例（网关层示意）

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

# 1) 取令牌（示意）
curl -sS -X POST "https://tool-gateway.linkfox.com/spApi/storeTokens" \
  -H "Authorization: $LINKFOXAGENT_API_KEY" -H "Content-Type: application/json" \
  -d '{"sellerId":"A1...","region":"NA"}'

# 2) 转发 searchContentDocuments（将 ACCESS_TOKEN 替换为上一步 accessToken）
curl -sS -X POST "https://tool-gateway.linkfox.com/spApi/developerProxy" \
  -H "Authorization: $LINKFOXAGENT_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "region":"NA",
    "path":"aplus/2020-11-01/contentDocuments",
    "method":"GET",
    "amzAccessToken":"ACCESS_TOKEN",
    "queryString":"marketplaceId=ATVPDKIKX0DER"
  }'
```
