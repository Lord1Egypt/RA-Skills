# Enrich public listings (value-add bundle)

Optional **`enrich-row`** on public vessel/cargo rows — **ship archive**, **tags**, **port distance** — billed via **`hifleet_api_key`**.

**Separate from contact fetch**: enrich does not return owner phone/email; use **`CONTACT_API.md`** for contacts.

---

## Endpoint

**`POST https://api.hifleet.com/openclaw/vessel/charter/enrich-row?api_key={密钥}`**

(Config: `charter_enrich_url` — same URL.)

Resolve base: `charter_enrich_url` → `hifleet_charter_api_base` + `/enrich-row` → default public URL.

---

## When to call

| User intent | Action |
|-------------|--------|
| “Show tags / ship profile / distance” on public list | After **`vessels/search`** or **`cargo/search`**, call enrich-row per row (or batch policy below) |
| Plain list only | **Skip** enrich (saves points) |

---

## Request body (vessel row)

Map API list row → parse-schema-like object (minimum **`船名`**, **`载重吨`**, **`OPEN位置`**, **`IMO`** if present):

```json
{
  "kind": "vessel",
  "row": {
    "船名": "MV EXAMPLE",
    "IMO": "9123456",
    "载重吨": 58000,
    "OPEN位置": "SINGAPORE",
    "船型": "Bulk Carrier"
  },
  "query_port": "Tianjin"
}
```

| Field | Purpose |
|-------|---------|
| `kind` | `vessel` or `cargo` |
| `row` | Fields from public `data[]` mapped to Chinese keys where possible |
| `query_port` | Optional — user’s port of interest for **distance** enrichment |

**Response** (typical): `imo`, `mmsi`, `tags`, `archive` / ship profile fields, `portid`, distance hints — merge into user display **without translating** ship/port names.

---

## Request body (cargo row)

```json
{
  "kind": "cargo",
  "row": {
    "货物种类": "COAL",
    "装货港": "NEWCASTLE",
    "卸货港": "QINGDAO",
    "货物数量": 70000
  },
  "query_port": "Qingdao"
}
```

---

## Agent rules

1. List first; contacts only when user asks (**`CONTACT_API.md`**).
2. Enrich adds **archive/tags/distance**, not contact decryption.
3. If enrich fails for one row, still show the public list row; note partial enrich failure briefly.
4. Batch: for large **`total`**, enrich only rows the user asked about, or first page if they said “with full ship info”.
5. **Contacts**: never from enrich — use **`CONTACT_API.md`**.

---

## Reference

Detailed enrich semantics align with **`hifleet-mytonnages/CHARTER_ENRICH_API.md`** (portid decoupling, archive columns) — reuse field names when merging into replies.
