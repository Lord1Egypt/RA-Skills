# 船舶事故事件 API / Vessel Casualty & Events API

按 IMO 查询船舶事故/事件列表，再按 `eventId` 查详情（概览、描述、位置、船舶、航次、货物、关联事件）。**需配置 `api_key`**。

**API 基址**：默认 `https://api.hifleet.com`（`{base}`）；其它部署可设 **`HIFLEET_API_BASE`**（无末尾 `/`）。见 [api_base.md](api_base.md)。

数据来源：Maritime Portal 事故事件库（与网站船舶档案页「事故和事件」一致）。**勿与** MSA 事故报告、海盗事件接口混用。

---

## 1. 事故事件列表 / List by IMO

### 请求

| 项目 | 值 |
|------|-----|
| 请求 URL | `{base}/casualty/list/token` |
| 请求方式 | `GET` 或 `POST` |

### Query 参数

| 参数名 | 示例值 | 必选 | 类型 | 说明 |
|--------|--------|------|------|------|
| api_key | (从配置读取) | 是 | string | 接口授权 `api_key`（也可放请求头 `x-api-key`） |
| imo | 1042823 | 是 | string | IMO 号（通常 7 位） |

### 成功响应

- `status`: `"1"` 表示成功
- `msg`: `"SUCCESS"`
- `data`: 数组，按 `startDate` **倒序**；无记录时为空数组 `[]`

#### data 项字段

| 字段 | 类型 | 说明 |
|------|------|------|
| eventId | int | 事件 ID，用于详情接口 |
| imo | string | IMO |
| shipName | string | 事故发生时船名 |
| eventType | string | 事件类型（如 Collision、Grounding） |
| eventGroup | string | 事件分组 |
| detail | string | 详情摘要 |
| significance | string | 严重性 |
| startDate | string | 开始日期 `yyyy-MM-dd` |
| endDate | string | 结束日期 `yyyy-MM-dd` |
| totalLoss | string | 是否全损 |
| pollution | string | 是否污染 |
| summaryText | string | 概要文本 |

---

## 2. 事故事件详情 / Detail by eventId

### 请求

| 项目 | 值 |
|------|-----|
| 请求 URL | `{base}/casualty/detail/token` |
| 请求方式 | `GET` 或 `POST` |

### Query 参数

| 参数名 | 示例值 | 必选 | 类型 | 说明 |
|--------|--------|------|------|------|
| api_key | (从配置读取) | 是 | string | 接口授权 `api_key` |
| eventId | 914215 | 是 | int | 事件 ID，**取自列表项 `eventId`** |

### 成功响应

- `status`: `"1"` 表示成功
- `msg`: `"SUCCESS"`；若事件不存在则为 `"event not found"` 且 `data` 为 `null`
- `data`: 对象，结构如下

| 键 | 类型 | 说明 |
|----|------|------|
| overview | object | 同列表项结构 |
| descriptionText | string | 详细描述文本（可为空） |
| data | object/array/string/null | 结构化详情（服务端已解析 JSON） |
| location | object/array/null | 位置信息 |
| ship | object/array/null | 船舶信息 |
| voyage | object/array/null | 航次信息 |
| cargo | object/array/null | 货物信息 |
| related | array | 关联事件列表 |

#### related 项字段

| 字段 | 说明 |
|------|------|
| relatedEventId | 关联事件 ID（可再调详情） |
| shipName | 船名 |
| eventType | 类型 |
| detail | 详情 |
| significance | 严重性 |
| startDate | 开始日期 |
| relationship | 关联关系 |

---

## 调用流程（Agent）

1. 检查 `api_key`（环境变量 `HIFLEET_API_KEY`）；无则提示并终止。
2. **仅有船名/关键字**：先 `GET {base}/position/shipSearch?shipname=...&api_key=...`，从结果取 **IMO**（`imonumber`）；多条时请用户确认。
3. **已有 IMO**：`GET {base}/casualty/list/token?imo={imo}&api_key=...`，展示列表（Event ID、类型、详情、严重性、日期）。
4. 用户要看某条详情：取该条 **`eventId`** → `GET {base}/casualty/detail/token?eventId={id}&api_key=...`。
5. 无记录或 `event not found` 时如实说明，勿伪造事故内容。

---

## 错误与权限

- `status` 非 `"1"`：如实展示 `msg`。
- `api_key` 无效或未授权能力 `vessel.casualty.list` / `vessel.casualty.detail`：提示检查 Key 是否开通事故事件接口。
- 本能力为增值数据，无权限时勿与档案/PSC 等混答为「无事故」。
