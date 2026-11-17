# Charter contact unlock (`POST /unlock`)

HiFleet charter list types share the **same unlock endpoint**; only **`typeCode`** differs.

**User-facing wording** (all skills): say **「获取联系方式」** / get contact details — **do not** say 「解锁」/ unlock.

---

## Endpoint

**`POST {liner}/unlock?dataId={id}&typeCode={code}&api_key={密钥}`**

| Item | Value |
|------|--------|
| `{liner}` | `https://api.hifleet.com/openclaw/vessel/charter/liner` |
| Resolve | `hifleet_liner_api_base` → `HIFLEET_LINER_API_BASE` → default |
| Body | Empty (query only), unless gateway requires otherwise |
| `dataId` | Top-level **`id`** from the list row (not nested `senderInfoList.id`) |

---

## typeCode by capability

| Capability | Skill | List API | `typeCode` |
|------------|-------|----------|------------|
| **班轮船期** Liner schedule | `hifleet-schedule` | `POST {liner}/schedules` | **`product_vessel_liner_charter`** |
| **公开船盘** Open vessel | `hifleet-opentonnages` | `POST {charter}/vessels/search` | **`product_vessel_charter`** |
| **公开货盘** Open cargo | `hifleet-opentonnages` | `POST {charter}/cargo/search` | **`product_cargo_charter`** |

Detail per skill:

- Schedule → **`hifleet-schedule/SCHEDULE_API.md`** §3  
- Open vessel / cargo → **`hifleet-opentonnages/CONTACT_API.md`**

---

## Agent flow

### 1. List (default)

1. Call the list API; show **full list** per each skill’s **`FULL_LIST_POLICY.md`**.
2. Each row **must show record `id`**.
3. **Do not** treat masked `******` as real contact data.
4. End with guidance: user may give **record id** or ask for **all** contacts (uses API points per row).

### 2. User asks for contacts

| User intent | Action |
|-------------|--------|
| One row by id / row number | `POST /unlock` with that row’s **`id`** and the correct **`typeCode`** |
| **全部** / all contacts | Loop **`dataId`** for **each** `id` from the last list (confirm points if many rows) |
| Ship name only, no id | Ask user to pick **record id** from the list already shown |

3. After success: **deduplicate contacts** (see § Contact dedup below); show deduped plaintext; mark **（已获取联系方式）**; do not repeat unlock for same `id` in session unless user asks again.

---

## Contact dedup (mandatory after unlock)

Applies to **schedule** and **open tonnage/cargo** — all skills that call **`POST /unlock`**.

After unlock (or when showing **`senderInfoList`** plaintext from list/unlock):

1. Treat each contact row as one record (email, phone, instant messaging / 即时通讯, date).  
2. **Merge** rows where **email, phone, and IM are all the same** (after trim; case-insensitive for email).  
3. When merging, **keep the row with the latest date** (`updatetime`, `updateTime`, `date`, etc. — field names vary by API).  
4. **Show only deduped rows** to the user; do not repeat identical contact triples.

CLI tools attach **`contacts_deduped`** on fetch-contacts output. Agents must apply the same rule when formatting unlock JSON manually.

---

## CLI (where provided)

| Skill | Command |
|-------|---------|
| Open vessel/cargo | `hifleet-opentonnages/scripts/opentonnages_tool.py fetch-contacts` |

Schedule: agent calls HTTP directly per **`SCHEDULE_API.md`** (no bundled CLI).

---

## Port ID (list queries)

Resolve **`portid`** via **`references/charter_port_suggest.md`** (`GET {liner}/ports/suggest`) — **not** `portguide/getPort/token`.
