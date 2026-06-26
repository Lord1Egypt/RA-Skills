# 预抵船舶查询（路由 C）

本文件为 **hifleet-mytonnages** 中 **路由 C（预抵）** 的约定；**路由 A（本人邮箱）不适用本文**。

---

## 分发模式

1. 预抵数据由 **HiFleet `api.hifleet.com`** 提供；触发路由 C 时由助手发 **HTTPS** 请求，**不得**用邮件、本地船货盘库或臆造数据代替。  
2. **列表须全量返回**：**`FULL_LIST_POLICY.md`**（分页拉齐 **`total`**，查到多少展示多少）。  
3. 密钥：`hifleet_api_key` / `HIFLEET_API_KEY`；Query **`api_key`** = 该串，**勿在对话中完整暴露**。

---

## 配置与 API 基址

| 含义 | 默认值 |
|------|--------|
| `{base}`（租船 OpenClaw 根） | `https://api.hifleet.com/openclaw/vessel/charter` |

**解析顺序**：`hifleet_charter_api_base`（config）→ `HIFLEET_CHARTER_API_BASE` → 上表默认。

---

## 0. 港口五字码（portcode）

用户说中文或英文港名时，须先得到 **`params.portcode`**（五字码，如 `CNTIZ`）再调 §1：

1. **港口指南**（推荐）：`GET https://api.hifleet.com/portguide/getPort/token?api_key={密钥}&portName={港名}`，从命中列表取 **`portCode`**（见 `hifleet-skills/references/port_api.md`）。  
2. **班轮港口联想**（备选）：`GET {liner_base}/ports/suggest`（**`SCHEDULE_API.md` §1**）；若响应项含 **`portCode`** 则采用，否则仍用 §0.1。  
3. 多条命中时向用户确认主港，**不得**臆造 portcode。

---

## 1. 预抵列表查询

**`POST {base}/destination/search?api_key={密钥}`**

- **Header**：`Content-Type: application/json`  
- **Body**：

```json
{
  "offset": 1,
  "limit": 200,
  "params": {
    "portcode": "CNTIZ",
    "sortcolumn": "dist",
    "sorttype": "desc"
  },
  "filterLabels": {
    "vesselAge": ["0~3"]
  }
}
```

| 字段 | 必选 | 说明 |
|------|------|------|
| `offset` | 是 | 分页起始（现网多为从 1 起） |
| `limit` | 是 | 单页条数上限，全量拉取见 **`FULL_LIST_POLICY.md`** |
| `params.portcode` | 是 | 港口五字码（如 `CNTIZ`）；用户说中文港名时须先解析为 portcode |
| `params.sortcolumn` | 否 | 排序字段，如 `dist` |
| `params.sorttype` | 否 | `asc` / `desc` |
| `filterLabels` | 是 | 按统计项过滤；键名与响应 `stat` 中字段对应 |
| `filterLabels.vesselAge` | 否 | 船龄区间标签，如 `["0~3"]` |
| `filterLabels.type` | 否 | 船型 |
| `filterLabels.LENGTH` | 否 | 船长 |
| `filterLabels.sjdraught` | 否 | 设计吃水 |
| `filterLabels.dwt` | 否 | 载重吨 |
| `filterLabels.holdCapacityCbm` | 否 | 舱容（立方米） |

**`filterLabels` 含义**：传入某标签值表示**过滤掉**该标签对应的数据（与接口文档「有该值代表需要过滤掉」一致）；取值须来自当次或上次响应 `stat.*.statistics[].label`。

**成功响应**：含 **`total`**、**`stat`**（各维度统计）、**`data[]`**（船舶明细）。`data` 字段含 `ShipName`、`imo`、`mmsi`、`destination`、`eta`、`dist`、`dwt`、`type`、`vesselAge`、`tags` 等。

**分页**：须拉齐 **`total`** 后再向用户输出，禁止只展示第一页。

---

## 2. 与用户对话的触发说法（示例）

- 「**预抵**天津的船」「**即将到港**」「**ETA**」「**目的地**是某港的船」  
- 「某港**附近**将要到达的船舶」  

若用户说「**我邮件里**」→ **路由 A**，不是 C。

---

## 3. 输出用词

向用户展示时遵守 **`WORKFLOW_OUTPUT.md`**「路由 C（预抵）」及 **`USER_WORDING.md`**：**禁止**对用户说 workflow、schema、SQLite 等内部术语。
