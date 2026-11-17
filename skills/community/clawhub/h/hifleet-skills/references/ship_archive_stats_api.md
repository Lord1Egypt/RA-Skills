# 船舶档案统计 API / Ship Archive Statistics API

用于查询船舶档案的**日批快照**：一组 `ads_*` 预聚合统计表，以及 `dwd_ship_profile_current` 船舶档案明细表。适合回答船旗、船型、公司船队、建造年份、载重吨、船厂、证书到期和登记国等维度的“多少艘、如何分布、有哪些船”问题。

这不是实时 AIS 数据，也不是单船完整档案接口；查单船档案应使用 [archive_api.md](archive_api.md)。所有接口需通过 OpenClaw 权限校验；按本技能统一方式配置并使用 `api_key`。

**API 基址**：`{base}` 默认是 `https://api.hifleet.com`，可由 `HIFLEET_API_BASE` 覆盖，且不含末尾 `/`。详见 [api_base.md](api_base.md)。

统一前缀：`{base}/api/openclaw/ship-archive/stats`

## 批次选择规则

三个接口均可通过 `statDate` 或 `batchNo` 定位快照：

1. 传入 `batchNo` 时，按批次号查询，优先级最高。
2. 未传 `batchNo`、传入 `statDate` 时，按该日最近成功批次查询；日期必须是 `yyyy-MM-dd`。
3. 两者都不传时，取最近一次成功的全量刷新批次（`shipStatsFullRefresh`）。

因此，同一轮分析应复用响应中的 `statDate` 和 `batchNo`。若返回“无成功批次”或“无法解析批次”，应如实说明当前没有可用快照，不要将其解释为统计值为 0。

## 统一响应

成功：

```json
{
  "status": "1",
  "msg": "SUCCESS",
  "data": {}
}
```

失败：

```json
{
  "status": "0",
  "msg": "Missing intent"
}
```

错误消息会随 `i18n` 语言设置变化。`status="0"` 时没有可用业务数据。

---

## 1. 聚合统计：`POST /query`

**URL**：`POST {base}/api/openclaw/ship-archive/stats/query`

按 `intent` 查询对应的 `ads_*` 预聚合表。`intent` 是必填项，大小写不敏感。`rows` 是数据表的原始行，因统计类型不同字段不同；不要假设所有统计都有同一组字段。

### 请求体

| 字段 | 必填 | 类型 | 说明 |
|---|---:|---|---|
| `intent` | 是 | string | 统计主题，见下表 |
| `statDate` | 否 | string | 统计日期，格式 `yyyy-MM-dd` |
| `batchNo` | 否 | string | 批次号；传入时优先于 `statDate` |
| `filters` | 否 | object | 依 `intent` 使用的精确匹配筛选条件 |

### intent、作用与 filters

| intent | 作用 | 可用 `filters` |
|---|---|---|
| `FLAG_SHIP_COUNT` | 各船旗的船舶数量统计 | `flagName` |
| `FLAG_SHIPTYPE_DIST` | 船旗与四级船型的交叉分布 | `flagName`, `shiptypeLevel4` |
| `SHIPTYPE_PROFILE` | 四级船型档案统计 | `shiptypeLevel4` |
| `NEWBUILD_TREND_YEAR` | 按建造年份的新增船舶趋势 | `buildYear`（整数） |
| `COMPANY_FLEET_SUMMARY` | 公司/角色维度的船队汇总 | `companyRole`, `companyName`, `companyCode` |
| `COMPANY_AGE_BUCKET` | 公司船队的船龄分段分布 | `companyRole`, `companyName`, `ageBucket` |
| `DWT_RANGE_COUNT` | 按四级船型和 DWT 区间的数量分布 | `shiptypeLevel4`, `dwtBucket` |
| `SHIPBUILDER_DELIVERY_SUMMARY` | 船厂和建造国维度的交付统计 | `shipbuilder`, `countryOfBuild` |
| `CERT_EXPIRY_SUMMARY` | 证书分类、到期窗口统计 | `certificateCategory`, `windowType` |
| `REGISTRY_COUNTRY_SUMMARY` | 船籍登记国统计 | `registryCountry` |

除 `buildYear` 外，筛选字段均为非空字符串时才生效，且都是精确匹配；没有通用模糊匹配或分页参数。`NEWBUILD_TREND_YEAR` 的结果按 `build_year` 升序返回。

### 示例：利比里亚船旗的数量统计

```json
{
  "intent": "FLAG_SHIP_COUNT",
  "filters": {
    "flagName": "Liberia"
  }
}
```

### 成功响应

```json
{
  "status": "1",
  "msg": "SUCCESS",
  "data": {
    "intent": "FLAG_SHIP_COUNT",
    "statDate": "2026-07-16",
    "batchNo": "batch-xxx",
    "rows": [
      {
        "stat_date": "2026-07-16",
        "batch_no": "batch-xxx"
      }
    ]
  }
}
```

使用响应中的 `intent`、`statDate`、`batchNo` 说明统计口径。`rows` 的具体指标字段以该 intent 对应的 ADS 表实际返回为准。

---

## 2. 船舶档案明细：`POST /list`

**URL**：`POST {base}/api/openclaw/ship-archive/stats/list`

从 `dwd_ship_profile_current` 返回满足条件的船舶档案原始明细。适合用户要查看“符合条件的船有哪些”，而不是仅要聚合数字。

### 请求体

| 字段 | 必填 | 类型 | 说明 |
|---|---:|---|---|
| `statDate` | 否 | string | 统计日期，`yyyy-MM-dd` |
| `batchNo` | 否 | string | 批次号，优先级高于 `statDate` |
| `page` | 否 | integer | 页码，默认 `1`；小于 1 时也按 `1` 处理 |
| `pageSize` | 否 | integer | 每页条数，默认 `20`，最大 `200` |
| `filters` | 否 | object | 明细筛选条件，见下表 |

### filters

| 字段 | 类型 | 匹配方式 | 说明 |
|---|---|---|---|
| `imo` | integer | 精确 | IMO 号 |
| `mmsi` | string | 精确 | MMSI |
| `flagName` | string | 精确 | 船旗名称 |
| `shiptypeLevel3` | string | 精确 | 三级船型 |
| `shiptypeLevel4` | string | 精确 | 四级船型 |
| `registeredOwner` | string | 精确 | 注册船东 |
| `shipNameKeyword` | string | 包含匹配 | 船名关键字，等价于 SQL `LIKE %keyword%` |

结果固定按 `imo ASC` 排序。分页时应保留同一 `statDate` 与 `batchNo`，直到取完所需页面。

### 示例：检索利比里亚籍散货船

```json
{
  "page": 1,
  "pageSize": 20,
  "filters": {
    "flagName": "Liberia",
    "shiptypeLevel4": "Bulk Carrier"
  }
}
```

### 成功响应

```json
{
  "status": "1",
  "msg": "SUCCESS",
  "data": {
    "statDate": "2026-07-16",
    "batchNo": "batch-xxx",
    "total": 125,
    "page": 1,
    "pageSize": 20,
    "list": [
      {
        "imo": 1234567,
        "ship_name": "EXAMPLE STAR"
      }
    ]
  }
}
```

`total` 是所有符合当前条件的记录数，`list` 是当前页。明细行返回 DWD 表原始字段，字段存在性取决于实际数据。

---

## 3. 批次元信息：`GET/POST /meta`

**URL**：`GET {base}/api/openclaw/ship-archive/stats/meta` 或 `POST {base}/api/openclaw/ship-archive/stats/meta`

在查询统计前，用于确认当前可用快照、统计日期和批次。该接口的参数是 **Query 参数**，不是 JSON 请求体。

| 参数 | 必填 | 说明 |
|---|---:|---|
| `statDate` | 否 | 指定统计日期，`yyyy-MM-dd` |
| `batchNo` | 否 | 指定批次号，优先级高于 `statDate` |

示例：

```text
GET {base}/api/openclaw/ship-archive/stats/meta?statDate=2026-07-16
```

成功响应中的 `data`：

| 字段 | 说明 |
|---|---|
| `statDate` | 实际解析出的统计日期 |
| `batchNo` | 实际解析出的批次号 |
| `jobName` | 若有任务日志，通常为 `shipStatsFullRefresh` |
| `endTime` | 成功任务结束时间；可能缺失 |
| `affectedRows` | 任务影响行数；可能缺失 |
| `dwdSampleGeneratedAt` | DWD 表最大采样生成时间；可能缺失 |
| `adsFlagSummaryGeneratedAt` | 船旗汇总表最大采样生成时间；可能缺失 |

```json
{
  "status": "1",
  "msg": "SUCCESS",
  "data": {
    "statDate": "2026-07-16",
    "batchNo": "batch-xxx",
    "jobName": "shipStatsFullRefresh",
    "endTime": "2026-07-16 03:00:00",
    "affectedRows": 100000,
    "dwdSampleGeneratedAt": "2026-07-16 03:05:00",
    "adsFlagSummaryGeneratedAt": "2026-07-16 03:06:00"
  }
}
```

---

## Agent 使用规则

1. 先识别问题是**单船档案**、**聚合统计**还是**船舶明细**；不要用聚合接口伪造单船详细档案。
2. 未指定时间时，可先调用 `/meta`，并在回答中说明实际使用的 `statDate`、`batchNo`；跨查询比较时必须固定同一批次。
3. 聚合问题选择最小必要的 `intent` 和 `filters`。筛选值必须使用库中实际名称；空结果仅表示当前批次和条件没有命中，不等于该类船舶不存在。
4. 明细问题使用 `/list`；只展示当前页时，说明 `total`、页码和每页条数。用户要求完整列表时继续按页取数，但遵守每页最多 `200` 条的限制。
5. 无可用成功批次、批次号不存在或日期格式不合法时，如实展示接口错误并请用户更换日期/批次；不要将错误响应当作零值统计。
