# Output rules

**`USER_WORDING.md`**, **`LOCALIZATION.md`**.

## Public open vessels (V)

- State **Total: N** per **`FULL_LIST_POLICY.md`**.
- **Laycan / OPEN window**: one line `Laycan: yyyy/MM/dd~yyyy/MM/dd` when dates present (`openDate`~`openEndDate`).
- **Each row must show record `id`** (for later contact fetch).
- **Default list (no contact request yet)** — completeness:
  - Treat **`VESSEL_SEARCH_API.md` → `data[]` field catalog** as the checklist.
  - For **each** returned row, show **all non-empty, non-sensitive** fields (size, age, flag, draught, holds, gear, OPEN region/port/dates, ETA/destination, tags, MMSI/IMO/callsign, builder, match hints, `purchased` / `requireUnLock`, etc.).
  - Prefer a readable block per vessel (multi-line key: value), not a single truncated headline that drops fields.
  - Omit only: null / `""` / `"-"` / empty arrays; **`emailBody`** when redacted; internal `userId` when useless.
  - **Do not** show phone / email / WeChat / sender names, or expand `******`. Plain company strings (`operator` / `registeredOwner` / `shipManager`) may be shown when **not** masked; they are still **not** full contacts.
- **After contact fetch** (`CONTACT_API.md`): mark **（已获取联系方式）**; show **deduped** contact fields (`references/charter_contact_unlock.md` § Contact dedup).
- Vessel names, ports: **verbatim** (no translation).
- **Footer after list** (when contacts not yet fetched): brief line inviting user to give **record id** or ask for **all** contacts — **no “unlock” wording**.
- Optional site footer: `💡 **More open tonnage:** https://mytonnages.hifleet.com`

## Public cargo (G)

- **Total: N**; full list; each row **`id`** visible.
- Laycan one line from `laycanStart`~`laycanEnd`.
- **Default**: cargo type, quantity, load/discharge ports, laycan, distance, tags — **not** charterer/phone/email if masked.
- **After contact fetch**: show charterer / contact / email / phone from **deduped** unlock response.
- Sort by distance when user asked and API provides `dischargingDist`.

## Enrich bundle

When **`ENRICH_OPENTONNAGES.md`** was used, append archive/tags/distance under each row. Enrich does **not** replace contact fetch.

## Never (user-facing)

- Say **「解锁」** / unlock / decrypt / typeCode.
- Treat `******` from list API as real contact data.
- Omit **record id** from list rows.
