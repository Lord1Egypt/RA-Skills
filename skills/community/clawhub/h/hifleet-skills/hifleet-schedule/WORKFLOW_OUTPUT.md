# Output rules

Follow **`USER_WORDING.md`**. Use **`LOCALIZATION.md`** for system/error text language.

## Schedule list

- **Full list**: `total` = N → show N entries.  
- **Each row must show record `id`** (for contact fetch).
- **Laycan (one line)**: `Laycan: yyyy/MM/dd~yyyy/MM/dd` (combine load/cancel windows on one line).  
- **Empty fields**: omit.  
- **Locked (default list)**: show Laycan, load/discharge port, record id, service line; **do not** show masked `******` as real contact data.  
- **Footer** (contacts not fetched): invite user to give **record id** or ask for **all** contacts.  
- **After contact fetch**: show **deduped** plaintext from unlock (`references/charter_contact_unlock.md` § Contact dedup); mark **（已获取联系方式）**.

## Business data

Keep **verbatim**: port names, line names, vessel names, company names from API — **do not translate**.
