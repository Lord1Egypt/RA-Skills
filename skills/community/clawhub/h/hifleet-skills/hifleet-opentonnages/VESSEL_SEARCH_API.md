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

Before filtering by load/open port:

1. **Port guide** (recommended): `GET https://api.hifleet.com/portguide/getPort/token?api_key=...&portName=...` → **`portCode`** / list `piuid` as needed (see `hifleet-skills/references/port_api.md`).
2. **Liner suggest** (fallback): `GET {liner}/ports/suggest` from **`hifleet-schedule`** if port guide misses.

Put resolved ID in **`params.portid`** or **`params.openPort`** per API behaviour.

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

**Response**: **`total`**, **`stat`**, **`data[]`**. Typical fields: ship name, DWT, type, OPEN port/dates, `imo`, `tags`, **`id`**, owner/contact (often **masked** in list).

**Output rules**:

- Show **all non-empty non-sensitive** fields + **record `id`** per **`WORKFLOW_OUTPUT.md`**.
- **Do not** present masked owner/phone/email as real data.
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
