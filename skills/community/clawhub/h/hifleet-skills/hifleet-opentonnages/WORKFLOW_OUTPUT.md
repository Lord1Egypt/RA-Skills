# Output rules

**`USER_WORDING.md`**, **`LOCALIZATION.md`**.

## Public open vessels (V)

- State **Total: N** per **`FULL_LIST_POLICY.md`**.
- **Laycan / OPEN window**: one line `Laycan: yyyy/MM/dd~yyyy/MM/dd` when dates present.
- **Each row must show record `id`** (for later contact fetch).
- **Default list (no contact request yet)**:
  - Show: vessel name (if plain), DWT, type, OPEN port, OPEN/Laycan window, IMO, tags, route hints, etc.
  - **Do not** show owner, company, phone, email, WeChat, or expand `******`.
- **After contact fetch** (`CONTACT_API.md`): mark **（已获取联系方式）**; show plaintext contact fields from unlock response.
- Vessel names, ports: **verbatim** (no translation).
- **Footer after list** (when contacts not yet fetched): brief line inviting user to give **record id** or ask for **all** contacts — **no “unlock” wording**.
- Optional site footer: `💡 **More open tonnage:** https://mytonnages.hifleet.com`

## Public cargo (G)

- **Total: N**; full list; each row **`id`** visible.
- Laycan one line from `laycanStart`~`laycanEnd`.
- **Default**: cargo type, quantity, load/discharge ports, laycan, distance, tags — **not** charterer/phone/email if masked.
- **After contact fetch**: show charterer / contact / email / phone from unlock response.
- Sort by distance when user asked and API provides `dischargingDist`.

## Enrich bundle

When **`ENRICH_OPENTONNAGES.md`** was used, append archive/tags/distance under each row. Enrich does **not** replace contact fetch.

## Never (user-facing)

- Say **「解锁」** / unlock / decrypt / typeCode.
- Treat `******` from list API as real contact data.
- Omit **record id** from list rows.
