# Charter contact unlock (`POST /unlock`)

Four HiFleet charter list types share the **same unlock endpoint**; only **`typeCode`** differs.

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
| **预抵船舶** Pre-arrival | `hifleet-mytonnages` (route C) | `POST {charter}/destination/search` | **`product_will_arrive_charter`** |

Detail per skill:

- Schedule → **`hifleet-schedule/SCHEDULE_API.md`** §3  
- Open vessel / cargo → **`hifleet-opentonnages/CONTACT_API.md`**  
- Pre-arrival → **`hifleet-mytonnages/CONTACT_API.md`**

---

## Agent flow (all four)

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

3. After success: show plaintext fields; mark **（已获取联系方式）**; do not repeat unlock for same `id` in session unless user asks again.

---

## CLI (where provided)

| Skill | Command |
|-------|---------|
| Open vessel/cargo | `hifleet-opentonnages/scripts/opentonnages_tool.py fetch-contacts` |
| Pre-arrival | `hifleet-mytonnages/scripts/destination_tool.py fetch-contacts` |

Schedule: agent calls HTTP directly per **`SCHEDULE_API.md`** (no bundled CLI).
