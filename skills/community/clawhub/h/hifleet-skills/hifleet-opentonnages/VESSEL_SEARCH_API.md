# Public open vessel search (route V)

HiFleet **public open tonnage** — list via **`POST /vessels/search`**; **contact details on demand** via **`CONTACT_API.md`** (`POST {liner}/unlock`, `typeCode=product_vessel_charter`).

---

## Distribution

1. Data from **`api.hifleet.com`** only; never substitute mailbox/SQLite or fabricated rows.
2. **`hifleet_api_key`** required; Query **`api_key`** — do not paste full key in chat.
3. Default filters: **`params.isPublic: true`**, **`params.isDuplicate: false`** unless user asks otherwise.
4. **Full list**: **`FULL_LIST_POLICY.md`**.

---

## Base URL

| Item | Default |
|------|---------|
| `{base}` | `https://api.hifleet.com/openclaw/vessel/charter` |

Resolve: `hifleet_charter_api_base` → `HIFLEET_CHARTER_API_BASE` → default.

---

## Port ID (when user names a port)

Before filtering by open/load/discharge port, resolve **`params.portid`** (and cargo **`params.dischargingPortid`**) via **`GET {liner}/ports/suggest`** only — see **`references/charter_port_suggest.md`**.

**Do not** use `portguide/getPort/token` for this skill.

Put resolved **`portId`** in **`params.portid`** / **`params.dischargingPortid`**. Text port name in **`params.openPort`** only when API accepts name filter without id.

---

## Search

**`POST {base}/vessels/search?api_key={密钥}`**

- **Header**: `Content-Type: application/json`

**Body example**:

```json
{
  "offset": 1,
  "limit": 200,
  "params": {
    "isPublic": true,
    "isDuplicate": false,
    "keyword": "",
    "openPort": "",
    "portid": "",
    "shiptype": "",
    "shipagemin": "",
    "shipagemax": "",
    "openDateStart": "2026-06-01",
    "openDateEnd": "2026-06-30"
  },
  "filterLabels": {
    "dwt": ["0~5k", "5k~10k"],
    "sjdraught": ["0~5"]
  }
}
```

| Field | Required | Notes |
|-------|----------|--------|
| `offset` | yes | Page start (usually **1**) |
| `limit` | yes | Page size; use max allowed; paginate per **`FULL_LIST_POLICY.md`** |
| `params` | yes | Filters |
| `params.isPublic` | yes | **`true`** for this skill |
| `params.isDuplicate` | yes | **`false`** default (deduped public rows) |
| `params.keyword` | no | Vessel name / callsign / MMSI / IMO (CN or EN) |
| `params.mmsi` / `params.imo` | no | Exact identifiers |
| `params.openPort` | no | OPEN port text filter |
| `params.portid` | no | Port ID from port guide |
| `params.shiptype` | no | Vessel type |
| `params.shipflag` | no | Flag |
| `params.shipagemin` / `shipagemax` | no | Age bounds |
| `params.openDateStart` / `openDateEnd` | no | OPEN window (`yyyy-MM-dd`) |
| `filterLabels` | no | Label filters from response **`stat`** (values mean **exclude** that bucket — see destination API pattern) |

**Response**: **`total`**, **`stat`**, **`data[]`**.

### Response envelope

| Field | Meaning |
|-------|---------|
| `total` | Matches after filters (must paginate until all rows fetched — **`FULL_LIST_POLICY.md`**) |
| `stat` | Facet buckets for UI filters / `filterLabels` (see below) |
| `data[]` | Vessel rows — **every non-empty, non-masked field must be showable** (full catalog below) |

### `stat` dimensions (use labels for `filterLabels`)

Each key has `total`, `label` (or `grouplabel`), and `statistics[]` with `label` / `count` / `countFilter` / `filter`.

| Key | Meaning |
|-----|---------|
| `dwt` | DWT buckets |
| `vesselAge` | Age buckets |
| `sjdraught` | Design draught buckets |
| `portRegion` | OPEN region |
| `openDateDays` | OPEN date windows |
| `type` | Ship type |
| `holdCapacityCbm` | Hold capacity (m³) |
| `openType` | Fixture type (SPOT / TCT / PERIOD / …) |
| `tags` | Tag labels (Geared, Gearless, MPP, …) |

When applying `filterLabels`, values mean **exclude** that bucket (same pattern as destination search).

### `data[]` field catalog (show all non-empty unless marked sensitive)

**Mandatory identity** (always surface when present):

| Field | Notes |
|-------|--------|
| **`id`** | Record id — required for contact fetch; never omit |
| `ShipName` / `particularShipName` | Vessel name(s); prefer `ShipName`, show both if differ |
| `imo` / `mmsi` / `callsign` | Identifiers |
| `type` / `minotype` / `dwtLabel` | Type / subtype / DWT class label |
| `dwt` / `GrossTonnage` / `LENGTH` / `width` / `sjdraught` | Size & draught |
| `YearOfBuild` / `vesselAge` | Build year / age |
| `flagname` / `flagnameCN` / `flagcode` | Flag |
| `tags[]` | `{label, color}` — show **labels**; color optional |
| `openPort` / `portname` / `cnportname` / `portRegion` / `portid` | OPEN position (text + ids when present) |
| `openDate` / `openEndDate` / `openDateDays` / `openEndDateDays` / `openType` / `duration` | OPEN / laycan window |
| `eta` / `destination` / `openPortEta` | ETA / AIS destination hints |
| `lat` / `lon` / `countrycodelrf` | Position / LRF country when present |
| `dist` / `dischargingDist` / `dischargingPortid` | Distance / discharge filters when present |
| `holdCapacityCbm` / `holdsCount` / `hatchSize` / `hatchCoverType` | Holds / hatch |
| `isGeared` / `craneType` / `craneCount` / `craneCapacityTon` / `cargoEquipment` / `deckStrength` / `reeferPlugs` / `sprinklerSystem` / `dgApproved` / `imoEquipmentClass` / `fuelType` / `speedKnots` | Gear & outfit |
| `tradingArea` / `group` | Trading / group |
| `Shipbuilder` | Yard |
| `isPublic` / `isDuplicate` / `isOwner` / `senderFlag` | Listing meta |
| `purchased` / `requireUnLock` | Contact entitlement flags (drive unlock UX; do **not** say 「解锁」) |
| `receivedTime` | Source mail time |
| `matchCount` / `matcheIds` / `shipCargoMatchBo` | Cargo-match hints when non-empty |
| `operator` / `registeredOwner` / `shipManager` / `vesselOwner` | Company names — show only if **not** masked (`******`); still **not** a substitute for contact unlock |

**Sensitive / contact-related** (list API often returns `******` or redacted HTML — **do not** treat as real values; show after **`CONTACT_API.md`** only):

| Field | Notes |
|-------|--------|
| `senderName` / `senderEmail` | Masked until unlock |
| `senderInfoList[]` | `senderName`, `senderEmail`, `telephone`, `instantMessaging`, `receivedTime`, `id`, `userId` — masked until unlock |
| `emailBody` | Often asterisk / redacted HTML — omit when empty or only `*` / noise |
| `userId` | Internal; omit unless debugging |

**Nested structures**:

- `tags`: list of `{ "label": "Gearless", "color": "#FFDBEE" }` → display labels.
- `shipCargoMatchBo`: `{ count, ids, matched }` → show when useful (`count` / `matched`).
- `senderInfoList`: contacts; default list = masked.

**Output rules** (see also **`WORKFLOW_OUTPUT.md`**):

- Show **every non-empty, non-sensitive field** from the catalog above + **record `id`**. Do **not** summarize down to only name/DWT/OPEN and drop the rest.
- Null / `"-"` / empty string / empty arrays may be omitted.
- **Do not** present masked owner/phone/email/`******` as real data.
- After list, **guide** user to request contacts by **record id** or **all** — see **`CONTACT_API.md`**.

---

## Optional enrich (sold bundle)

After listing (or for top-N rows user cares about), call **`ENRICH_OPENTONNAGES.md`** → `POST {base}/enrich-row` for **IMO / tags / ship archive / port distance**.

---

## CLI

```bash
python scripts/opentonnages_tool.py search-vessels --limit 200
python scripts/opentonnages_tool.py search-vessels --keyword "PACIFIC" --open-port "Singapore"
```

---

## Errors

Short localized message (`LOCALIZATION.md`); no stack traces or full `api_key`.
