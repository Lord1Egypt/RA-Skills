# 海事行政处罚 API / Maritime Administrative Penalty API

查询中国海事局公示的**行政处罚**记录（案号、案由、处罚对象、处罚结果等）。数据存于 `public_opinion`（`content_type=行政处罚`）及 `public_opinion_detail`，由调度任务从海事局公示爬取。**需配置 `api_key`**。

**API 基址**：默认 `https://api.hifleet.com`（`{base}`）；其它部署可设 **`HIFLEET_API_BASE`**（无末尾 `/`）。见 [api_base.md](api_base.md)。

与 PSC、事故事件、制裁不同：本能力为**国内海事行政处罚公示**，勿混用。

---

## 请求

| 项目 | 值 |
|------|-----|
| 请求 URL | `{base}/maritime/penalty/list/token` |
| 请求方式 | `GET` 或 `POST` |

### Query 参数

| 参数名 | 示例值 | 必选 | 类型 | 说明 |
|--------|--------|------|------|------|
| api_key | (从配置读取) | 是 | string | 接口授权 `api_key`（也可放请求头 `x-api-key`） |
| mmsi | 412345678 | 否* | string | MMSI；与 shipName / 时间 至少一组有值 |
| shipName | 远航 | 否* | string | 船名或违法主体名（模糊匹配 `cn_names` / `en_names` / `title`） |
| startTime | 2024-01-01 | 否* | string | 决定日期起 `yyyy-MM-dd`（字段 `triggertime`） |
| endTime | 2024-12-31 | 否* | string | 决定日期止 `yyyy-MM-dd` |
| page | 1 | 否 | int | 页码，默认 1 |
| pageSize | 20 | 否 | int | 每页条数，默认 20，最大 100 |

\* **至少提供**：`mmsi`、`shipName`、或 `startTime`/`endTime` 之一。查某船优先传 **shipName**（库内主体名多为中文船名）；有 MMSI 关联时也可传 `mmsi`。

---

## 成功响应

- `status`: `"1"`
- `msg`: `"SUCCESS"`
- `data`:

| 字段 | 类型 | 说明 |
|------|------|------|
| total | int | 总条数 |
| page | int | 当前页 |
| pageSize | int | 每页大小 |
| list | array | 处罚记录 |

### list 项字段

| 字段 | 说明 |
|------|------|
| id | 主键 |
| title | 标题/当事人 |
| content | 内容摘要 |
| website | 作出机关 |
| websiteId | 公示 ID |
| mmsis | 关联 MMSI（可能为空） |
| cnNames / enNames | 中/英文船名或主体名 |
| triggertime | 决定日期 |
| contentType | 一般为 `行政处罚` |
| details | 明细数组 |

### details[] 字段

| 字段 | 说明 |
|------|------|
| caseNo | 案号 |
| caseReasonName | 案由 |
| decisionDateText | 决定日期 |
| orgName | 作出机关 |
| punishObjName | 处罚对象 |
| illegalClause | 违法条款 |
| punishReference | 处罚依据 |
| punishResult | 处罚结果 |

---

## 调用流程（Agent）

1. 检查 `api_key`（`HIFLEET_API_KEY`）。
2. 用户给船名：可直接 `shipName=...`；若需统一船名再 `shipSearch`。
3. 用户给 MMSI：可传 `mmsi`（仅当库内已关联 MMSI 时有命中；无命中时可改用船名再查）。
4. `GET {base}/maritime/penalty/list/token?shipName=...&api_key=...`（可加时间与分页）。
5. 展示案号、案由、机关、处罚结果；无记录如实说明。勿伪造公示内容。

---

## 错误与权限

- 未传任何筛选条件：返回参数错误提示。
- `api_key` 无效或未授权 `vessel.maritime.penalty.list`：提示开通相关能力。
