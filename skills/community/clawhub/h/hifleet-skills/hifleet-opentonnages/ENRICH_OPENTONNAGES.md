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

### 标准格式（与 `CHARTER_ENRICH_API.md` / 邮件解析 2.4 一致）

**`source` 固定 `parse_schema`**，`row` 用中文键；**`IMO` 可 null**（后端用 `api_key` 按船名+载重吨 lookup）。

```json
{
  "kind": "vessel",
  "source": "parse_schema",
  "include_archive": true,
  "row": {
    "船名": "ZHONG XING MEN",
    "IMO": null,
    "载重吨": 55408,
    "船型": "杂货船",
    "OPEN位置": "Singapore",
    "是否有船吊": 1,
    "吊机数量": 4,
    "是否可装危险品": 0,
    "租船类型": "OPEN"
  }
}
```

**Query**：`?api_key={密钥}`（必填，用于 IMO lookup 与 ship-archive）。

**不要**在 `row.IMO` 或顶层 `imo` 填占位/错误 IMO（如 `9123456`）——后端会直接用该 IMO 查档案与 tags，查不到则返回：

```json
{
  "ok": true,
  "partial": true,
  "imo": "9123456",
  "data": { "tags": "", "dwt": null, "YearOfBuild": null, "shiptype": null, "minotype": null },
  "warnings": [{ "step": "archive", "detail": "ship-archive unavailable or empty" }]
}
```

行内 **无 IMO** 且 **Query 带 api_key** 时，才会按 `船名`+`载重吨` 自动补齐真实 IMO。

**船名**：去掉 **`MV` / `M.V.` / `MT`** 前缀后再传入（skill 自动处理，如 `MV WILSON NEWPORT` → `WILSON NEWPORT`）。

### 公开船盘列表行（C/D 路由）

若 `row` 来自 `vessels/search` 的 `data[]`（英文字段），须映射后再调 enrich，或由 CLI 自动映射：

| Public API field | Maps to `row` |
|------------------|---------------|
| `ShipName` | `船名` |
| `imo` | `row.IMO`（须为真实 7 位 IMO，勿用占位符） |
| `dwt` | `载重吨` |
| `type` | `船型` |
| `openPort` / `destination` | `OPEN位置` |

CLI：`opentonnages_tool.py enrich --kind vessel --file row.json`

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

Enrich semantics: portid decoupling and archive column names — reuse field names when merging into replies.

