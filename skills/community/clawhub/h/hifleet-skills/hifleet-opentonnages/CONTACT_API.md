# Contact details API (route V / G)

List APIs (`vessels/search`, `cargo/search`) return **masked** owner/charterer/contact fields by default.  
When the user **asks for contact details**, call **`POST /unlock`** with the row **`id`** as **`dataId`**.

**User-facing wording**: say **「获取联系方式」** / **get contact details** — **do not** say 「解锁」/ unlock (see **`USER_WORDING.md`**).

**All charter unlock types** (schedule, open vessel, open cargo): **`references/charter_contact_unlock.md`**.

---

## Endpoint

**`POST {liner}/unlock?dataId={id}&typeCode={code}&api_key={密钥}`**

| Item | Value |
|------|--------|
| `{liner}` | `https://api.hifleet.com/openclaw/vessel/charter/liner` |
| Resolve | `hifleet_liner_api_base` → `HIFLEET_LINER_API_BASE` → default |
| Body | Empty (query only), unless your gateway requires otherwise |
| Header | `api_key` same as query (align with **`hifleet-schedule/SCHEDULE_API.md`** §3) |

---

## typeCode (internal — do not read aloud to user)

| Route | Listing API | `typeCode` |
|-------|-------------|------------|
| **V** Open vessel | `POST {charter}/vessels/search` | **`product_vessel_charter`** |
| **G** Open cargo | `POST {charter}/cargo/search` | **`product_cargo_charter`** |
| **B** Liner schedule | `POST {liner}/schedules` | **`product_vessel_liner_charter`** (`hifleet-schedule/SCHEDULE_API.md` §3) |

`{charter}` = `hifleet_charter_api_base` (same as search).

---

## Agent flow

### 1. List (default)

1. User e.g. “open bulkers from Shanghai” → **`VESSEL_SEARCH_API.md`** (resolve port → `POST /vessels/search`).
2. Show **full list** per **`FULL_LIST_POLICY.md`**.
3. Each row **must include record `id`** (label: **记录 id** / record id).
4. **Do not** show masked `******` as real data; **do not** show owner/phone/email/WeChat from list if masked.
5. **End with guidance** (localized):

   > Need contact details for a vessel? Tell me the **record id** (e.g. `12345`), or say **all** to fetch contacts for every row in this list (uses API points per row).

### 2. User asks for contacts

| User intent | Action |
|-------------|--------|
| One row: “contact for id 12345” / “第 2 条” | `POST /unlock?dataId=12345&typeCode=product_vessel_charter` (or cargo code) |
| All rows: “contacts for all” / “全部联系方式” | Loop **`dataId`** for **each** `id` from the last list (confirm points if many rows) |
| By ship name without id | Ask user to pick **record id** from the list you already showed |

3. After success: **deduplicate** per **`references/charter_contact_unlock.md`** § Contact dedup; show deduped plaintext; mark row **（已获取联系方式）** / *(contacts retrieved)*.
4. **Do not** call unlock again for the same `id` in the same session unless user asks.

---

## CLI

```bash
# Single row (vessel)
python scripts/opentonnages_tool.py fetch-contacts --kind vessel --id 12345

# Single row (cargo)
python scripts/opentonnages_tool.py fetch-contacts --kind cargo --id 67890
```

---

## Errors

Short localized message (`LOCALIZATION.md`); never paste full `api_key`.
