# Contact details API (route C — pre-arrival)

List API **`POST {charter}/destination/search`** returns vessel facts; **owner/contact fields are masked** by default (`******`).

When the user **asks for contact details**, call **`POST {liner}/unlock`** with the row **`id`** as **`dataId`** and **`typeCode=product_will_arrive_charter`**.

**User-facing wording**: **「获取联系方式」** — **do not** say 「解锁」/ unlock (see **`USER_WORDING.md`**).

**Shared rules** (all four charter unlock types): **`references/charter_contact_unlock.md`**.

---

## Endpoint

**`POST {liner}/unlock?dataId={id}&typeCode=product_will_arrive_charter&api_key={密钥}`**

| Item | Value |
|------|--------|
| `{liner}` | `https://api.hifleet.com/openclaw/vessel/charter/liner` |
| Resolve | `hifleet_liner_api_base` → `HIFLEET_LINER_API_BASE` → default |
| `{charter}` | Same as **`DESTINATION_SEARCH_API.md`** (search only) |

## List response hints (pre-arrival)

| Field | Agent use |
|-------|-----------|
| **`id`** | **`dataId`** for unlock (top-level; often MMSI string) |
| `purchased` | `true` → account may already have contacts; prefer showing `senderInfoList` if plaintext |
| `requireUnLock` | When `true`, user request for contacts → call unlock |
| `senderInfoList` | Contact objects when unlocked/purchased; **do not** use nested ids as `dataId` |
| `hasSenderInfoList` | `有` / `未知` — list filter only; not a substitute for unlock |

If user asks for contacts and row is not yet purchased / `senderInfoList` empty or masked → **`POST /unlock`** with top-level **`id`**.

---

### 1. List (default)

1. User asks pre-arrival at a port → **`DESTINATION_SEARCH_API.md`**.
2. Show **full list** per **`FULL_LIST_POLICY.md`**.
3. Each row **must include record `id`** (label: **记录 id**).
4. **Do not** show masked owner/phone/email as real data.
5. **Footer** (localized): invite user to give **record id** or say **全部** for all rows in this list.

### 2. User asks for contacts

| User intent | Action |
|-------------|--------|
| One row: id / 「第 N 条」 | `POST /unlock?dataId={id}&typeCode=product_will_arrive_charter` |
| **全部联系方式** | Loop every **`id`** from the last pre-arrival list |
| By ship name without id | Ask user to pick **record id** from the list |

3. After success: show plaintext from unlock response; mark **（已获取联系方式）**.
4. Do not call unlock again for the same `id` in the same session unless user asks.

---

## CLI

```bash
# Port suggest → portId
python scripts/destination_tool.py ports-suggest --keyword Tianjin

# Pre-arrival search
python scripts/destination_tool.py search --portid 15843

# Single row contacts
python scripts/destination_tool.py fetch-contacts --id 352005839

# All ids from last search JSON
python scripts/destination_tool.py fetch-contacts --all-from-file result.json
```

---

## Errors

Short localized message (`LOCALIZATION.md`); never paste full `api_key`.
