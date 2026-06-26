# Okki go API 完整参考文档

**Version:** 1.0.0
**Base URL:** `https://go.okki.ai`
**认证方式:** `Authorization: ApiKey sk-your-key-here`
**Skill 归因 Headers:** `X-Okki-Install-Id`、`X-Okki-Skill-Version`、`X-Okki-Skill-Runtime`
**错误格式:** RFC 7807 Problem Details
**速率限制:** 60 次/分钟（所有鉴权接口共享）

---

## 通用请求 Headers

所有 Skill 发起的 API 请求都应携带以下非敏感归因 headers，便于服务端统计 `SkillUsed`、`SkillFirstUsed`、`ActivationAchieved` 等事件。不要把 API Key、邮箱、邮件正文放入这些 headers。

```http
Authorization: ApiKey sk-your-key-here
X-Okki-Install-Id: <anonymous install id>
X-Okki-Skill-Version: 1.3.2
X-Okki-Skill-Runtime: <agent runtime>
```

本地安装器会复用 `${XDG_CONFIG_HOME:-$HOME/.config}/okki-go/install-id`。设置 `OKKIGO_ANALYTICS_DISABLED=1` 可关闭安装器与本地 resolver 的 best-effort analytics。

---

## 目录

1. [查询积分与 EDM 余额](#1-查询积分与-edm-余额)
2. [搜索公司（高级画像搜索）](#2-搜索公司高级画像搜索)
3. [解锁公司](#3-解锁公司)
4. [查看公司 Profile](#4-查看公司-profile)
5. [获取公司联系人邮件](#5-获取公司联系人邮件)
6. [搜索联系人](#6-搜索联系人)
7. [发送批量开发信](#7-发送批量开发信)
8. [发送个性化开发信](#8-发送个性化开发信)
9. [查询邮件任务列表](#9-查询邮件任务列表)
10. [查询邮件任务详情](#10-查询邮件任务详情)
11. [查询邮件发送记录列表](#11-查询邮件发送记录列表)
12. [查看单封邮件详情](#12-查看单封邮件详情)
13. [计费规则汇总](#13-计费规则汇总)
14. [错误码速查表](#14-错误码速查表)

---

## 1. 查询积分与 EDM 余额

**GET** `/api/v1/credit/balance`

- 认证：必须
- 计费：免费

### 响应示例

```json
{
  "userId": "12345",
  "monthlyPoints": 80,
  "monthlyEdm": 200,
  "monthlyExpiresAt": "2026-04-30T23:59:59.000Z",
  "addonPoints": 400,
  "addonEdm": 2000
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `monthlyPoints` | integer | 当月套餐剩余搜索积分（过期则为 0） |
| `monthlyEdm` | integer | 当月套餐剩余 EDM 配额 |
| `monthlyExpiresAt` | string (ISO 8601) | 月度配额到期时间 |
| `addonPoints` | integer | 加购包剩余搜索积分（永不过期） |
| `addonEdm` | integer | 加购包剩余 EDM 配额（永不过期） |

> 实际可用积分 = `monthlyPoints + addonPoints`，扣费优先消耗 monthly，不足再扣 addon。

---

## 2. 搜索公司（高级画像搜索）

**POST** `/api/v1/companies/search-advanced`

- 认证：必须
- 计费：**免费**（不扣积分）
- 基于企业画像的多维搜索，返回公司列表；`domain` 仅供内部解锁使用，不展示给用户

`search-advanced supports only` the request fields listed below. Do not invent filters such as `employee_range`, `decision_roles`, `website`, `homepage`, `url`, `contacts`, or `limit`. Unsupported dimensions must be handled locally or in later workflow stages.

### 请求体

```json
{
  "companyTypeKeywords": ["digital printing equipment manufacturer"],
  "productKeywords": ["DTF printer"],
  "industryKeywords": ["manufacturing"],
  "includeCountry": ["US", "CN"],
  "excludeCountry": ["RU"],
  "withEmails": 1,
  "crossFieldOperator": "AND",
  "from": 0,
  "size": 10
}
```

### 请求参数说明

At least one of `companyTypeKeywords`, `productKeywords`, or `industryKeywords` must be non-empty. Geography fields such as `includeCountry` and `excludeCountry` are filters only and cannot be used as a keywordless search.

| 参数 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| `companyTypeKeywords` | string[] | 条件必填 | 三个关键词字段至少一个非空 | 公司类型关键词 |
| `productKeywords` | string[] | 条件必填 | 三个关键词字段至少一个非空 | 产品关键词 |
| `industryKeywords` | string[] | 条件必填 | 三个关键词字段至少一个非空 | 行业关键词 |
| `includeCountry` | string[] | 否 | ISO 3166-1 alpha-2 | 包含的国家代码 |
| `excludeCountry` | string[] | 否 | ISO 3166-1 alpha-2 | 排除的国家代码 |
| `withEmails` | integer | 否 | `0` / `1` | 是否只返回有邮箱的公司 |
| `crossFieldOperator` | string | 否 | `"AND"` / `"OR"` | 跨字段匹配逻辑 |
| `from` | integer | 否 | 默认 0 | 分页偏移量 |
| `size` | integer | 否 | 默认 10，最大 50 | 每页数量 |

### 响应示例

```json
{
  "total": 215,
  "list": [
    {
      "company_type": ["digital printing equipment manufacturer"],
      "email_count": 4,
      "founding_time": "1996",
      "industry": ["manufacturing - printing equipment"],
      "main_products": ["UV flatbed printer", "dye sublimation printer"],
      "country_code": "CN",
      "whatsapp_count": 0,
      "company_profile": "Company description...",
      "domain": "example.com",
      "company_name": "Example Corp",
      "id": "uuid-here",
      "employees_count": "201-500"
    }
  ]
}
```

> `domain` is an internal key owned by wrapper scripts and saved batch/raw files. Normal skill usage should rely on compact rows and opaque `selection_handle`/unlock plans; do not display `domain`, website, homepage, URL, or link fields in free company-search results.

---

## 3. 解锁公司

**POST** `/api/v1/companies/unlock`

- 认证：必须
- 计费：**首次解锁扣 1 积分**，同一 domain 30 天内重复解锁免费
- 用途：将 domain 解析为 `companyHashId`，后续用于查询 profile/detail/profileEmails

### 请求体

```json
{
  "domain": "epson.com",
  "countryCode": "US"
}
```

### 请求参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `domain` | string | 是 | 公司域名，来自 search-advanced 结果 |
| `countryCode` | string | 是 | ISO 3166-1 alpha-2 国家代码 |

### 响应示例（200 OK）

```json
{
  "companyHashId": "00a718fdc83311638eca442bb591bef2",
  "companyName": "epson.com",
  "charged": true,
  "alreadyViewed": false
}
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `companyHashId` | string | 公司唯一标识，用于后续 profile/detail/profileEmails 查询 |
| `companyName` | string | 公司名称（可能为 domain） |
| `charged` | boolean | 本次是否扣费 |
| `alreadyViewed` | boolean | 是否 30 天内已解锁过 |

### 错误响应

- **404**: domain + countryCode 无匹配公司（不扣费）
- **402**: 余额不足

> `companyHashId` is required for all subsequent company queries. Always obtain it via this endpoint first.

---

## 4. 查看公司 Profile

**GET** `/api/v1/companies/:companyHashId/profile`

- 认证：必须
- 计费：**免费**（纯查询，不扣积分）
- 前置条件：必须先通过 `/companies/unlock` 获取 `companyHashId`

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `companyHashId` | string | 是 | 来自 `/companies/unlock` 响应的公司唯一标识 |

### 响应示例

```json
{
  "companyHashId": "abc123hash",
  "name": "TechCorp GmbH",
  "country": "DE",
  "industry": "Electronics",
  "employeeCount": 350,
  "website": "https://techcorp.de",
  "description": "Leading manufacturer of industrial electronics...",
  "tradeData": [
    {
      "hsCode": "851712",
      "value": 250000,
      "date": "2025-06-15",
      "direction": "import"
    }
  ]
}
```

---

## 5. 获取公司联系人邮件

**GET** `/api/v1/companies/:companyHashId/profileEmails`

- 认证：必须
- 计费：**免费**（纯查询，不扣积分）
- 前置条件：必须先通过 `/companies/unlock` 获取 `companyHashId`
- 可与多家公司的 profileEmails 请求并行调用

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `companyHashId` | string | 是 | 公司唯一标识 |

### 查询参数

| 参数 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| `keyword` | string | 否 | — | 按职位/姓名关键词筛选联系人 |
| `page` | integer | 否 | 正整数 | 分页页码 |
| `pageSize` | integer | 否 | 最大 100 | 每页数量 |

### 响应示例

```json
{
  "emails": [
    {
      "name": "Hans Mueller",
      "title": "Procurement Manager",
      "email": "hans@techcorp.de",
      "linkedin": "https://linkedin.com/in/hansmueller"
    }
  ],
  "total": 3,
  "page": 1
}
```

> 若 `emails` 为空数组（`[]`），表示该公司暂无可用联系人邮件。

---

## 6. 搜索联系人

**POST** `/api/v1/contacts/search`

- 认证：必须
- 计费：**每次请求扣 1 积分**（无论结果数量）
- 独立于公司搜索，可直接按姓名/邮箱/职位跨公司搜索

### 请求体

```json
{
  "name": "Alice Wang",
  "title": "Procurement Manager",
  "company_name": "Acme Corp",
  "country_codes": "US",
  "has_email": 1,
  "has_linkedin": 1,
  "employees_min": 50,
  "employees_max": 500,
  "size": 20,
  "page": 1
}
```

### 请求参数说明

| 参数 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| `name` | string | 否 | — | 联系人姓名（支持邮箱搜索，配合 `contact_match`）|
| `contact_match` | string | 否 | `"email"` | 指定 `name` 字段按邮箱匹配 |
| `title` | string | 否 | — | 职位关键词 |
| `title_type` | string | 否 | — | 职位类型分类 |
| `company_name` | string | 否 | — | 所属公司名称 |
| `working_company` | string | 否 | — | 工作单位 |
| `description` | string | 否 | — | 描述信息 |
| `primary_industry_name` | string | 否 | — | 主行业名称 |
| `country_codes` | string | 否 | ISO alpha-2 | 国家代码，多个用逗号分隔 |
| `industry_codes` | string | 否 | — | 行业代码 |
| `has_email` | integer | 否 | `0` / `1` | 是否有邮箱 |
| `has_phone` | integer | 否 | `0` / `1` | 是否有电话 |
| `has_linkedin` | integer | 否 | `0` / `1` | 是否有 LinkedIn |
| `has_facebook` | integer | 否 | `0` / `1` | 是否有 Facebook |
| `has_company_name` | integer | 否 | `0` / `1` | 是否有公司名 |
| `employees_min` | integer | 否 | — | 所属公司最小员工数 |
| `employees_max` | integer | 否 | — | 所属公司最大员工数 |
| `size` | integer | 否 | 最大 100，默认 20 | 每页数量 |
| `page` | integer | 否 | 默认 1 | 页码 |

### 响应示例

```json
{
  "list": [
    {
      "id": "contact_001",
      "name": "Alice Wang",
      "email": "alice@acme.com",
      "phone": "+1-555-0123",
      "linkedin": "https://linkedin.com/in/alicewang",
      "title": "Procurement Manager",
      "company": "Acme Corp",
      "country": "US"
    }
  ],
  "total": 8,
  "page": 1,
  "size": 20
}
```

---

## 7. 发送批量开发信

**POST** `/api/v1/emails/send/batch`

- 认证：必须
- 计费：**每封收件人消耗 1 个 EDM 配额**
- 限制：单次请求最多 100 个收件人

### 请求体

```json
{
  "content": "Dear company_name, we would love to partner with you.",
  "body_format": "html",
  "recipients": [
    {
      "email": "alice@acme.com",
      "subject": "Partnership Opportunity",
      "nickname": "Alice",
      "variables": { "company_name": "Acme Corp" }
    }
  ]
}
```

### 请求参数说明

| 参数 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| `content` | string | 是 | ≤50000 字符 | 邮件正文模板，可包含变量名（直接写变量名，不加 `{{}}`）|
| `body_format` | string | 是 | `"text"` / `"html"` | 正文格式 |
| `recipients` | array | 是 | 1–100 个 | 收件人列表 |
| `recipients[].email` | string | 是 | 有效邮箱格式 | 收件人邮箱 |
| `recipients[].subject` | string | 是 | ≤200 字符 | 邮件主题 |
| `recipients[].nickname` | string | 否 | — | 收件人称谓 |
| `recipients[].variables` | object | 否 | key 仅含 `\w+` | 模板变量替换，value 为 string |

### 响应示例（201 Created）

```json
{ "task_id": 1001, "total": 50, "status": "pending" }
```

> 发送为异步处理。记录 `task_id` 用于后续通过 EDM skill 查询发送进度（参见 okki-edm skill）。

---

## 8. 发送个性化开发信

**POST** `/api/v1/emails/send/personalized`

- 认证：必须
- 计费：**每封邮件消耗 1 个 EDM 配额**
- 限制：单次请求最多 100 封

### 请求体

```json
{
  "emails": [
    {
      "content": "Hi Alice, Acme Corp has been leading the textile industry...",
      "body_format": "html",
      "email": "alice@acme.com",
      "subject": "Custom Proposal for Acme Corp",
      "nickname": "Alice",
      "variables": { "company_name": "Acme Corp" }
    }
  ]
}
```

### 请求参数说明

| 参数 | 类型 | 必填 | 约束 | 说明 |
|------|------|------|------|------|
| `emails` | array | 是 | 1–100 个 | 邮件列表 |
| `emails[].content` | string | 是 | ≤50000 字符 | 该封邮件的独立正文 |
| `emails[].body_format` | string | 是 | `"text"` / `"html"` | 正文格式 |
| `emails[].email` | string | 是 | 有效邮箱格式 | 收件人邮箱 |
| `emails[].subject` | string | 是 | ≤200 字符 | 邮件主题 |
| `emails[].nickname` | string | 否 | — | 收件人称谓 |
| `emails[].variables` | object | 否 | key 仅含 `\w+` | 模板变量，value 为 string |

### 响应示例（201 Created）

```json
{
  "total": 2,
  "tasks": [
    { "task_id": 1002, "mail_id": 2001, "email": "alice@acme.com" },
    { "task_id": 1003, "mail_id": 2002, "email": "bob@globex.com" }
  ]
}
```

---

## 9. 查询邮件任务列表

**GET** `/api/v1/emails/tasks`

- 认证：必须
- 计费：免费
- 适用场景：用户发送邮件后想查看历史任务列表和整体发送情况

### 查询参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `task_ids` | string | — | 逗号分隔任务 ID，如 `1001,1002` |
| `subject` | string | — | 邮件主题模糊匹配 |
| `statuses` | string | — | 逗号分隔状态，可选值：`pending`/`requested`/`completed`/`partial`/`failed` |
| `recipient_email` | string | — | 收件人邮箱精确匹配 |
| `recipient_nickname` | string | — | 收件人昵称模糊匹配 |
| `created_from` | ISO 8601 | — | 任务创建时间起 |
| `created_to` | ISO 8601 | — | 任务创建时间止 |
| `page` | integer | `1` | 页码 |
| `page_size` | integer | `20` | 每页条数（1–100）|
| `sort_by` | `created_at` \| `task_id` | `created_at` | 排序字段 |
| `sort_order` | `asc` \| `desc` | `desc` | 排序方向 |

### 任务状态说明

| 状态 | 含义 |
|------|------|
| `pending` | 已创建，等待提交 EDM |
| `requested` | 已提交 EDM，等待回调 |
| `completed` | 全部发送成功 |
| `partial` | 部分成功、部分失败 |
| `failed` | 全部失败 |

### 响应示例（200 OK）

```json
{
  "data": [
    {
      "taskId": 1001,
      "totalCount": 50,
      "status": "completed",
      "sentCount": 48,
      "failedCount": 2,
      "createdAt": "2026-03-20T08:00:00.000Z",
      "completedAt": "2026-03-20T08:05:32.000Z"
    }
  ],
  "total": 12,
  "page": 1,
  "page_size": 20
}
```

---

## 10. 查询邮件任务详情

**GET** `/api/v1/emails/tasks/:taskId`

- 认证：必须
- 计费：免费
- 适用场景：用户想查看某次群发任务中每封邮件的具体送达情况，或排查失败原因

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `taskId` | integer | 是 | 任务 ID，来自发送接口响应的 `task_id` |

### 响应示例（200 OK）

```json
{
  "taskId": 1001,
  "totalCount": 50,
  "status": "partial",
  "sentCount": 48,
  "failedCount": 2,
  "createdAt": "2026-03-20T08:00:00.000Z",
  "completedAt": "2026-03-20T08:05:32.000Z",
  "content": "Dear company_name, we have a great product for you.",
  "bodyFormat": "html",
  "mails": [
    {
      "mailId": 2001,
      "taskId": 1001,
      "recipientEmail": "alice@acme.com",
      "recipientNickname": "Alice",
      "subject": "Partnership Opportunity",
      "status": "sent",
      "sentAt": "2026-03-20T08:01:15.000Z",
      "callbackReceivedAt": "2026-03-20T08:02:30.000Z",
      "failureReason": null
    },
    {
      "mailId": 2002,
      "taskId": 1001,
      "recipientEmail": "bob@globex.com",
      "recipientNickname": "Bob",
      "subject": "Partnership Opportunity",
      "status": "failed",
      "sentAt": null,
      "callbackReceivedAt": null,
      "failureReason": "Invalid email address"
    }
  ]
}
```

> `callbackReceivedAt` 非空表示 EDM 服务已回调确认送达。`failureReason` 非空时说明该封邮件失败原因。404 表示任务不存在或不属于当前用户。

---

## 11. 查询邮件发送记录列表

**GET** `/api/v1/emails/mails`

- 认证：必须
- 计费：免费
- 适用场景：跨任务查询特定收件人、时间段或状态的邮件记录

### 查询参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `task_ids` | string | — | 逗号分隔任务 ID |
| `mail_ids` | string | — | 逗号分隔邮件 ID |
| `subject` | string | — | 主题模糊匹配 |
| `statuses` | string | — | 逗号分隔状态，可选值：`pending`/`requested`/`sent`/`failed` |
| `recipient_email` | string | — | 收件人邮箱精确匹配 |
| `recipient_nickname` | string | — | 收件人昵称模糊匹配 |
| `sent_from` | ISO 8601 | — | 发送时间起 |
| `sent_to` | ISO 8601 | — | 发送时间止 |
| `received_from` | ISO 8601 | — | 回调送达时间起 |
| `received_to` | ISO 8601 | — | 回调送达时间止 |
| `page` | integer | `1` | 页码 |
| `page_size` | integer | `20` | 每页条数（1–100）|
| `sort_by` | `sent_at` \| `callback_received_at` \| `mail_id` \| `status` | `sent_at` | 排序字段 |
| `sort_order` | `asc` \| `desc` | `desc` | 排序方向 |

### 响应示例（200 OK）

```json
{
  "data": [
    {
      "mailId": 2001,
      "taskId": 1001,
      "recipientEmail": "alice@acme.com",
      "recipientNickname": "Alice",
      "subject": "Partnership Opportunity",
      "status": "sent",
      "sentAt": "2026-03-20T08:01:15.000Z",
      "callbackReceivedAt": "2026-03-20T08:02:30.000Z",
      "failureReason": null
    }
  ],
  "total": 48,
  "page": 1,
  "page_size": 20
}
```

---

## 12. 查看单封邮件详情

**GET** `/api/v1/emails/mails/:mailId`

- 认证：必须
- 计费：免费
- 适用场景：查看某封邮件的完整正文内容及送达状态

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `mailId` | integer | 是 | 邮件 ID，来自发送接口响应或任务详情中的 `mail_id` |

### 响应示例（200 OK）

```json
{
  "mailId": 2001,
  "taskId": 1001,
  "recipientEmail": "alice@acme.com",
  "recipientNickname": "Alice",
  "subject": "Partnership Opportunity",
  "status": "sent",
  "sentAt": "2026-03-20T08:01:15.000Z",
  "callbackReceivedAt": "2026-03-20T08:02:30.000Z",
  "failureReason": null,
  "content": "Dear Acme Corp, we have a great product for you.",
  "bodyFormat": "html"
}
```

> `bodyFormat` 字段（`"text"` 或 `"html"`）决定如何向用户展示正文内容。404 表示邮件不存在或不属于当前用户。

---

## 13. 计费规则汇总

| 接口 | 扣费类型 | 扣费规则 |
|------|---------|---------|
| `POST /companies/search-advanced` | 无 | 完全免费 |
| `POST /companies/unlock` | Points | 首次解锁扣 1 积分，同一 domain 30 天内重复免费 |
| `GET /companies/:id/profile` | 无 | 完全免费（纯查询） |
| `GET /companies/:id/profileEmails` | 无 | 完全免费（纯查询） |
| `POST /contacts/search` | Points | 每次请求扣 1 积分（与结果数量无关） |
| `POST /emails/send/batch` | EDM 配额 | 每个收件人扣 1 配额；余额不足则全部退还并返回 402 |
| `POST /emails/send/personalized` | EDM 配额 | 每封邮件扣 1 配额；中途不足则退还已扣并返回 402 |
| `GET /emails/tasks` | 无 | 完全免费 |
| `GET /emails/tasks/:taskId` | 无 | 完全免费 |
| `GET /emails/mails` | 无 | 完全免费 |
| `GET /emails/mails/:mailId` | 无 | 完全免费 |
| `GET /credit/balance` | 无 | 完全免费 |

**双桶扣费顺序：**
1. 优先扣 `monthlyPoints` / `monthlyEdm`（月度配额）
2. 月度配额不足时，自动扣 `addonPoints` / `addonEdm`（加购包）
3. 两者均不足时返回 402

**余额不足时的购买引导：**
- 升级套餐或购买加购包：[go.okki.ai/pricing](https://go.okki.ai/pricing)
- 加购包规格：400 积分 + 2000 封 EDM，$39.99，永不过期

---

## 14. 错误码速查表

| HTTP 状态码 | type 字段（RFC 7807） | 常见原因 | 处理建议 |
|-------------|----------------------|---------|---------|
| 400 | `bad-request` | 参数格式错误（邮箱格式、超出数量限制等） | 检查请求体参数 |
| 401 | `unauthorized` | API Key 无效、未配置或已吊销 | 检查 `OKKIGO_API_KEY` |
| 402 | `insufficient-credits` | 搜索积分或 EDM 配额不足 | 引导用户购买套餐/加购包 |
| 403 | `forbidden` | Free 套餐无 EDM 发送权限 | 引导升级套餐 |
| 404 | `not-found` | companyHashId 或资源不存在 | 确认 ID 来自搜索结果 |
| 429 | `rate-limit` / `quota-exceeded` | 速率超限（60次/分钟）或月/日配额超限 | 等待后重试；配额超限需等下月重置或购买加购包 |
| 502 | `upstream-error` | EDM 第三方服务异常 | 稍后重试，已扣配额自动退还 |

**错误响应标准格式：**

```json
{
  "type": "https://go.okki.ai/errors/insufficient-credits",
  "title": "Payment Required",
  "status": 402,
  "detail": "Insufficient points balance. Required: 1, Available: 0",
  "instance": "/api/v1/contacts/search"
}
```
