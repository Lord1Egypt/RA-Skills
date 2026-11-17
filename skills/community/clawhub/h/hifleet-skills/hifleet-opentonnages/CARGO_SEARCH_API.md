# Public cargo search (route G)

HiFleet **public cargo** listings — **`POST /cargo/search`**; contacts on demand via **`CONTACT_API.md`** (`typeCode=product_cargo_charter`).

---

## Distribution

1. Data from **`api.hifleet.com`** only.
2. **`hifleet_api_key`** required.
3. Default: **`params.isPublic: true`**, **`params.isDuplicate: false`**.
4. **Full list**: **`FULL_LIST_POLICY.md`**.

---

## Base URL

`{base}` = `https://api.hifleet.com/openclaw/vessel/charter` (same resolution as **`VESSEL_SEARCH_API.md`**).

---

## Port IDs

Resolve load/discharge port names **only** via **`GET {liner}/ports/suggest`** → **`params.portid`** / **`params.dischargingPortid`**. See **`references/charter_port_suggest.md`**.

**Do not** use `portguide/getPort/token`.

When user asks “cargo near X” or sort by distance, set sort fields per API (e.g. **`dischargingDist`**) after **portid** is known.

---

## Search

**`POST {base}/cargo/search?api_key={密钥}`**

```json
{
  "offset": 1,
  "limit": 200,
  "params": {
    "isPublic": true,
    "isDuplicate": false,
    "portid": "",
    "dischargingPortid": "",
    "keyword": "",
    "laycanStart": "2026-06-01",
    "laycanEnd": "2026-06-30"
  },
  "filterLabels": {}
}
```

| Field | Notes |
|-------|--------|
| `params.isPublic` | **`true`** |
| `params.isDuplicate` | **`false`** default |
| `params.portid` | Load port ID |
| `params.dischargingPortid` | Discharge port ID |
| `params.keyword` | Cargo / charterer keyword |
| `laycanStart` / `laycanEnd` | Laycan window inside `params` if required by API |
| `filterLabels` | Optional; keys from response **`stat`** |

**Response**: **`total`**, **`stat`**, **`data[]`**. Typical fields: cargo type, quantity, ports, laycan, `dischargingDist`, `tags`, **`id`**; charterer/contact often **masked** in list.

**Output**: per **`WORKFLOW_OUTPUT.md`**; contact plaintext only after **`CONTACT_API.md`**.

**Sort**: when user cares about distance to a discharge area, use API-supported sort (e.g. by `dischargingDist` descending) after portid resolution.

---

## Optional enrich

**`ENRICH_OPENTONNAGES.md`** → `enrich-row` for **tags** (cargo) and related metadata.

---

## CLI

```bash
python scripts/opentonnages_tool.py search-cargo --limit 200
python scripts/opentonnages_tool.py search-cargo --load-port "Tianjin"
```

---

## Errors

Localized short message; never fabricate cargo rows.
