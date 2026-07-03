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
| `{charter}`（租船 OpenClaw 根） | `https://api.hifleet.com/openclaw/vessel/charter` |
| `{liner}`（港口联想 + unlock） | `https://api.hifleet.com/openclaw/vessel/charter/liner` |

**解析顺序**：`hifleet_charter_api_base` / `hifleet_liner_api_base`（config）→ `HIFLEET_CHARTER_API_BASE` / `HIFLEET_LINER_API_BASE` → 上表默认。

---

## 0. 港口 ID（`portid`）

预抵列表 **必选** **`params.portid`**（港口 id 字符串，如 `"15843"`）。用户说中文或英文港名时，须先解析 portid 再调 §1。

**推荐：`GET {liner}/ports/suggest`**（与班轮船期相同，详见 **`hifleet-schedule/SCHEDULE_API.md`** §1）

| | |
|--|--|
| Header `api_key` | 用户密钥 |
| Query `keyword` | **英文**港名（如 `Tianjin`，勿用中文） |
| Query `from` | `0` |
| Query `size` | `1`（多条命中时增至 `5` 让用户选） |
| Query `api_key` | 与 Header 相同 |

取命中项 **`data[0].portId`**（或列表项中的 `portId` 字段）写入 **`params.portid`**。

**备选**：`GET https://api.hifleet.com/portguide/getPort/token?api_key=…&portName=…` → 若响应含可与现网对齐的港口 id 字段则采用；**以 `ports/suggest` 的 `portId` 为准**。

多条命中时向用户确认主港，**不得**臆造 portid。

**CLI**：`python scripts/destination_tool.py ports-suggest --keyword Tianjin`

---

## 1. 预抵列表查询

**`POST {charter}/destination/search?api_key={密钥}`**

- **Header**：`Content-Type: application/json`  
- **Body 示例**：

```json
{
  "offset": 1,
  "limit": 200,
  "params": {
    "sortcolumn": "dist",
    "sorttype": "asc",
    "portid": "15843",
    "isPublic": true
  },
  "filterLabels": {
    "type": ["杂货船"],
    "sjdraught": ["0~5"],
    "dwt": ["5k~10k"],
    "holdCapacityCbm": ["0~5k"],
    "vesselAge": ["0~3"],
    "etaDays": ["07.03~07.06"],
    "tags": ["未知"],
    "hasSenderInfoList": ["有"]
  }
}
```

| 字段 | 必选 | 说明 |
|------|------|------|
| `offset` | 是 | 分页起始（现网多为从 **1** 起） |
| `limit` | 是 | 单页条数；全量拉取见 **`FULL_LIST_POLICY.md`** |
| `params` | 是 | 查询与排序 |
| `params.portid` | **是** | 港口 id（§0 自 `ports/suggest` 取得） |
| `params.isPublic` | **是** | 默认 **`true`** |
| `params.sortcolumn` | 否 | 排序字段，如 `dist` |
| `params.sorttype` | 否 | `asc` / `desc` |
| `filterLabels` | 是 | 统计维过滤；键名与响应 **`stat`** 对应 |
| `filterLabels.type` | 否 | 船型，如 `["杂货船"]` |
| `filterLabels.sjdraught` | 否 | 设计吃水 |
| `filterLabels.dwt` | 否 | 载重吨 |
| `filterLabels.holdCapacityCbm` | 否 | 舱容（立方米） |
| `filterLabels.vesselAge` | 否 | 船龄 |
| `filterLabels.etaDays` | 否 | 预抵时间窗（标签来自 `stat.etaDays`） |
| `filterLabels.tags` | 否 | 标签 |
| `filterLabels.hasSenderInfoList` | 否 | 是否有联系人，如 `["有"]` / `["未知"]` |

**`filterLabels` 含义**：传入某 **`label`** 表示**过滤掉**该标签对应的数据（「有该值代表需要过滤掉」）；取值须来自当次或上次响应 **`stat.*.statistics[].label`**。

---

## 1.1 成功响应

含 **`total`**、**`stat`**（各维度统计）、**`data[]`**（船舶明细）。

**典型 `data[]` 字段**（以现网为准，勿臆造）：

| 字段 | 说明 |
|------|------|
| `ShipName`、`imo`、`mmsi`、`type`、`dwt`、`destination`、`eta`、`dist`、`vesselAge`、`tags` | 船货与预抵事实 |
| **`id`** | **记录 id**（常为 MMSI 字符串）；unlock 的 **`dataId`** |
| `senderInfoList` | 联系人列表；列表阶段多为 `[]` 或脱敏，明文见 **`CONTACT_API.md`** |
| `hasSenderInfoList` | `有` / `未知`（与 `stat.hasSenderInfoList` 对应） |
| `purchased` | 当前账号是否已购买该条联系方式 |
| `requireUnLock` | 是否仍需 unlock 才能看联系人（以现网为准） |

**输出规则**：

- 展示全部非敏感字段 + **记录 `id`**（见 **`WORKFLOW_OUTPUT.md`** 路由 C）。
- **不得**把脱敏或空的联系人当完整联系方式展示。
- 列表末尾引导用户按 **记录 id** 或 **全部** 获取联系方式 — **`CONTACT_API.md`**。

**分页**：须拉齐 **`total`** 后再向用户输出，禁止只展示第一页。

---

## 2. 与用户对话的触发说法（示例）

- 「**预抵**天津的船」「**即将到港**」「**ETA**」「**目的地**是某港的船」  
- 「某港**附近**将要到达的船舶」  

若用户说「**我邮件里**」→ **路由 A**，不是 C。

---

## 3. CLI

```bash
# 港口联想 → portId
python scripts/destination_tool.py ports-suggest --keyword Tianjin

# 预抵列表（须已知 portid）
python scripts/destination_tool.py search --portid 15843 --sorttype asc

# 带 filterLabels JSON 文件
python scripts/destination_tool.py search --portid 15843 --filter-labels-file filters.json
```

---

## 4. 输出用词

向用户展示时遵守 **`WORKFLOW_OUTPUT.md`**「路由 C（预抵）」及 **`USER_WORDING.md`**：**禁止**对用户说 workflow、schema、SQLite、`portid` 等内部术语。
