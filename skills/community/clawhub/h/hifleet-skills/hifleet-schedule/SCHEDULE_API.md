# Liner schedule API (hifleet-schedule)

This skill queries **HiFleet liner schedules** only (general/bulk, Ro-Ro, container). Not for mailbox tonnage or ETA pre-arrival.

---

## Distribution

1. Data from **`api.hifleet.com`** via HTTPS; never substitute mail/SQLite or fabricated rows.
2. **Full list mandatory**: **`FULL_LIST_POLICY.md`**.
3. Key: `hifleet_api_key` / `HIFLEET_API_KEY`; never expose full key in chat.

## Schedule types (user wording)

| Category | User may say |
|----------|----------------|
| General / bulk | breakbulk, general cargo liner, 散杂货船期 |
| Ro-Ro | car carrier, PCTC, Ro-Ro, 滚装船期 |
| Container | container line, feeder, 集装箱船期 |

Same API endpoints for all; filter by ports/dates in `params`. If API returns a vessel/line type field, show it **as returned** (do not translate names).

---

## Config

| Item | Default |
|------|---------|
| `{base}` | `https://api.hifleet.com/openclaw/vessel/charter/liner` |

Resolve: `hifleet_liner_api_base` -> `HIFLEET_LINER_API_BASE` -> default.

---

## 1. Port suggest

**`GET {base}/ports/suggest`**

Full URL: **`https://api.hifleet.com/openclaw/vessel/charter/liner/ports/suggest`**

Also documented in **`references/charter_port_suggest.md`**. **Do not** use `portguide/getPort/token` for schedule portid.

| | |
|--|--|
| Header `api_key` | user key |
| Query `keyword` | **English** port name (`Shanghai`, not 上海) |
| Query `from` | `0` |
| Query `size` | `1` |
| Query `api_key` | same as header |

Take **`data[0].portId`** for load/discharge. If user names two ports, call section 1 **twice** and pass both IDs in one `POST /schedules` (see section 2).

**Do not** filter results by port name string after fetch.

---

## 2. Schedule list

**`POST {base}/schedules?sk={url-encoded api_key}`**

Content-Type: `application/json`

### Request body

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `offset` | Yes | number | Page offset (1-based) |
| `limit` | Yes | number | Page size |
| `filterLabels` | Yes | object | Filter criteria; keys with values filter data, empty keys mean no filter |
| `params` | Yes | object | Query parameters |

### `filterLabels` fields

| Field | Type | Description |
|-------|------|-------------|
| `filterLabels.type` | array[string] | Vessel type filter |
| `filterLabels.LENGTH` | array[string] | Vessel length filter |
| `filterLabels.sjdraught` | array[string] | Draught filter |
| `filterLabels.dwt` | array[string] | Deadweight filter |
| `filterLabels.holdCapacityCbm` | array[string] | Hold capacity (cbm) filter |
| `filterLabels.tradingArea` | array[string] | Trading area / route filter |
| `filterLabels.openDateDays` | array[string] | Open date days from today (negative = past, positive = future) |
| `filterLabels.openEndDateDays` | array[string] | Open end date days from today |
| `filterLabels.openPort` | array[string] | Open port filter |
| `filterLabels.dischargingPort` | array[string] | Discharging port filter |

### `params` fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `params.portid` | Yes | string | Load port ID from section 1 |
| `params.dischargingPortid` | No | string | Discharge port ID when user asked both ports |
| `params.isPublic` | No | boolean | e.g. `true` |
| `params.dataId` | No | string | Query single record by dataId |
| `params.openPort` | No | string | Open port name filter |
| `params.keyword` | No | string | Keyword search: vessel name / callsign / MMSI / IMO (Chinese or English) |
| `params.sortcolumn` | No | string | Sort column name |
| `params.sorttype` | No | string | Sort order: `asc` or `desc` |

### Request example

```json
{
  "offset": 1,
  "limit": 10,
  "filterLabels": {},
  "params": {
    "portid": "27999",
    "dischargingPortid": "25523",
    "isPublic": true
  }
}
```

**Recent**: wide window from tomorrow if user did not specify dates.

Each item in `data` must have top-level **`id`** for unlock (`dataId`).

### Response

| Field | Type | Description |
|-------|------|-------------|
| `total` | number | Total record count |
| `data` | array | Schedule list (see fields below) |
| `stat` | object | Filter statistics for sidebar (see below) |

### Response `data[]` fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | number | Record ID (for unlock) |
| `ShipName` | string | Vessel name |
| `tradingArea` | string | Trading area / route |
| `openPort` | string | Load port name (English) |
| `dischargingPort` | string | Discharge port name (English) |
| `dischargingPortid` | string | Discharge port ID |
| `portid` | string | Load port ID |
| `openDate` | string | Open date (yyyy-MM-dd) |
| `openEndDate` | string | Cancel date (yyyy-MM-dd) |
| `openDateDays` | number | Days from today to open date |
| `openEndDateDays` | number | Days from today to cancel date |
| `openPortEta` | string | Next port ETA (yyyy-MM-dd) |
| `dischargingPortEta` | string | Discharge port ETA (yyyy-MM-dd) |
| `eta` | string | ETA |
| `portRegion` | string | Port region |
| `destination` | string | Destination |
| `dist` | number | Distance |
| `dischargingDist` | number | Discharge distance |
| `dwtLabel` | string | Deadweight label |
| `holdCapacityCbm` | string/null | Hold capacity (cbm) |
| `hatchSize` | string/null | Hatch size |
| `holdsCount` | string/null | Number of holds |
| `hatchCoverType` | string/null | Hatch cover type |
| `craneType` | string/null | Crane type |
| `craneCount` | string/null | Crane count |
| `isGeared` | string | Geared status |
| `deckStrength` | string/null | Deck strength |
| `sprinklerSystem` | string | Sprinkler system |
| `dgApproved` | string | DG approved |
| `reeferPlugs` | string/null | Reefer plugs |
| `fuelType` | string/null | Fuel type |
| `speedKnots` | string/null | Speed (knots) |
| `vesselAge` | string/null | Vessel age |
| `imo` | string/null | IMO number |
| `mmsi` | string | MMSI |
| `flagcode` | string | Flag code |
| `flagname` | string | Flag name |
| `flagnameCN` | string | Flag name (Chinese) |
| `vesselOwner` | string | Vessel owner (masked if locked) |
| `registeredOwner` | string | Registered owner (masked if locked) |
| `shipManager` | string | Ship manager (masked if locked) |
| `operator` | string | Operator (masked if locked) |
| `Shipbuilder` | string | Shipbuilder (masked if locked) |
| `particularShipName` | string | Particular ship name (masked if locked) |
| `userId` | string | User ID |
| `senderFlag` | string | Sender flag |
| `senderName` | string | Sender name (masked if locked) |
| `senderEmail` | string | Sender email (masked if locked) |
| `telephone` | string | Telephone (masked if locked) |
| `instantMessaging` | string | Instant messaging (masked if locked) |
| `senderInfoList` | array | Contact info list (masked if locked) |
| `senderInfoList[].senderName` | string | Contact name |
| `senderInfoList[].senderEmail` | string | Contact email |
| `senderInfoList[].telephone` | string | Contact phone |
| `senderInfoList[].instantMessaging` | string | Contact IM |
| `senderInfoList[].receivedTime` | string | Received time |
| `emailBody` | string | Email body (masked if locked) |
| `receivedTime` | string | Record received time (yyyy-MM-dd HH:mm) |
| `isPublic` | number | Public flag (1 = public) |
| `isOwner` | boolean | Is owner |
| `isDuplicate` | boolean | Is duplicate |
| `purchased` | boolean | Is purchased |
| `requireUnLock` | boolean | Requires unlock (true = contact masked) |
| `openType` | string | Open type (e.g. LINE) |
| `duration` | string/null | Duration |
| `tags` | array | Tags |
| `matchCount` | number | Match count |
| `matcheIds` | array | Matched IDs |
| `shipCargoMatchBo` | object | Cargo match info |
| `shipCargoMatchBo.matched` | boolean | Cargo matched |
| `shipCargoMatchBo.count` | number | Match count |
| `shipCargoMatchBo.ids` | array/null | Matched IDs |
| `imoEquipmentClass` | string/null | IMO equipment class |
| `cargoEquipment` | string/null | Cargo equipment |
| `dwt` | string/null | Deadweight |

### Response `stat` fields

The `stat` object contains filter statistics for the sidebar. Each key corresponds to a `filterLabels` field:

| Stat key | Label | Description |
|----------|-------|-------------|
| `stat.openPort` | 装货港 | Open port statistics |
| `stat.dischargingPort` | 卸货港 | Discharging port statistics |
| `stat.openDateDays` | 受载日 | Open date days statistics |
| `stat.openEndDateDays` | 解约日 | Cancel date days statistics |
| `stat.type` | 船型 | Vessel type statistics |
| `stat.LENGTH` | 船长 | Vessel length statistics |
| `stat.sjdraught` | 吃水 | Draught statistics |
| `stat.dwt` | 载重吨 | Deadweight statistics |
| `stat.holdCapacityCbm` | 舱容 | Hold capacity statistics |
| `stat.tradingArea` | 航线意向 | Trading area statistics |

Each stat entry contains:

| Field | Type | Description |
|-------|------|-------------|
| `stat.{key}.label` | string | Display label |
| `stat.{key}.total` | number | Total count |
| `stat.{key}.statistics[]` | array | Filter options |
| `stat.{key}.statistics[].label` | string | Option label |
| `stat.{key}.statistics[].count` | number | Count for this option |
| `stat.{key}.statistics[].filter` | boolean | Whether this option is currently filtered |
| `stat.{key}.statistics[].countFilter` | number | Count after filter applied |

---

## 3. Unlock contact

List API (`POST /schedules`) returns **masked** owner/charterer/contact fields by default.
When the user **asks for contact details**, call **`POST /unlock`** with the row **`id`** as **`dataId`**.

**User-facing wording**: say **「获取联系方式」** / **get contact details** — **do not** say 「解锁」/ unlock (see **`USER_WORDING.md`**).

**All four charter unlock types** (schedule, open vessel, open cargo, pre-arrival): **`references/charter_contact_unlock.md`**.

---

### Endpoint

**`POST {base}/unlock?dataId={id}&typeCode=product_vessel_liner_charter&api_key={密钥}`**

| Item | Value |
|------|--------|
| `{base}` | `https://api.hifleet.com/openclaw/vessel/charter/liner` |
| Resolve | `hifleet_liner_api_base` -> `HIFLEET_LINER_API_BASE` -> default |
| Body | Empty (query only), unless gateway requires otherwise |
| `dataId` | Top-level **`id`** from schedule list row (not nested `senderInfoList.id`) |
| `typeCode` | Fixed **`product_vessel_liner_charter`** |

---

### Agent flow

#### 1. List (default)

1. Call `POST /schedules`; show **full list** per **`FULL_LIST_POLICY.md`**.
2. Each row **must show record `id`** (label: **记录 id** / record id).
3. **Do not** treat masked `******` as real contact data.
4. End with guidance (localized):

   > Need contact details for a vessel? Tell me the **record id** (e.g. `12345`), or say **all** to fetch contacts for every row in this list (uses API points per row).

#### 2. User asks for contacts

| User intent | Action |
|-------------|--------|
| One row: "contact for id 12345" / "第 2 条" | `POST /unlock?dataId=12345&typeCode=product_vessel_liner_charter` |
| All rows: "contacts for all" / "全部联系方式" | Loop **`dataId`** for **each** `id` from the last list (confirm points if many rows) |
| By ship name without id | Ask user to pick **record id** from the list already shown |

3. After success: **deduplicate** per **`references/charter_contact_unlock.md`** section Contact dedup; show deduped plaintext; mark row **（已获取联系方式）** / *(contacts retrieved)*.
4. **Do not** call unlock again for the same `id` in the same session unless user asks.

---

### Contact dedup (mandatory after unlock)

After unlock (or when showing **`senderInfoList`** plaintext from list/unlock):

1. Treat each contact row as one record (email, phone, instant messaging / 即时通讯, date).
2. **Merge** rows where **email, phone, and IM are all the same** (after trim; case-insensitive for email).
3. When merging, **keep the row with the latest date** (`receivedTime`, `updateTime`, `date`, etc.).
4. **Show only deduped rows** to the user; do not repeat identical contact triples.

---

### Errors

Short localized message (`LOCALIZATION.md` / `scripts/i18n_messages.py`); never paste full `api_key`.

---

## 4. User-visible output

See **`WORKFLOW_OUTPUT.md`**: full list, Laycan one line, empty fields omitted, locked vs unlocked contact rules.

---

## 5. 目的港 / ETA / 当前位置（跨 skill 补充）

班轮 **`POST /schedules`** 列表已含部分字段（`destination`、`eta`、`openPortEta`、`dischargingPortEta`、`dist` 等），**优先展示列表返回值**。

用户追问某船的 **AIS 实时目的港、ETA、当前经纬度/航速**（或列表字段为空/过旧）时，用 **`hifleet-skills` 父 skill** 的船位接口（与班轮 **同一 `api_key`**）：

| 需求 | 父 skill 文档 | 接口（`{base}` 默认 `https://api.hifleet.com`） |
|------|----------------|--------------------------------------------------|
| 确定 MMSI | **`references/position_api.md`** §1 | `GET {base}/position/shipSearch?shipname=…` |
| 当前位置 + AIS 目的港 + ETA | **`references/position_api.md`** §2 | `GET {base}/position/position/get/token?mmsi=…` |
| 上一离港 / 当前停船（可选） | **`references/voyage_api.md`** | `lastdeparture/token`、`getstop/token` |

**推荐流程**：

1. 从船期行取 **`mmsi`**（或 **`ShipName`** → shipSearch 得 MMSI）。  
2. **`position/get/token`** → 展示 `destination` / `destinationIdentified`、`eta`、经纬度（`la`/`lo` ÷60）、`ti`（最后更新时间）。  
3. **勿**用 `portguide/getPort` 替代班轮 **`ports/suggest`** 的 portid。

脚本（可选）：父 skill **`scripts/get_position.py`**。

---

## Errors

On HTTP/API errors, show a **short** message in the **user locale** (`LOCALIZATION.md` / `scripts/i18n_messages.py`). Do not paste full `api_key` or stack traces.
