# Output rules

Use **`USER_WORDING.md`** and **`LOCALIZATION.md`**.

## Route C (pre-arrival)

- Full list per **`FULL_LIST_POLICY.md`**.  
- **Each row must show record `id`** (for contact fetch).
- Show distance, ETA, vessel names **as in API** (do not translate).
- **Default list (no contact request yet)**:
  - Show: ship name, IMO, MMSI, destination, ETA, distance, DWT, type, age, tags, etc.
  - **Do not** show owner, company, phone, email, WeChat, or expand `******`.
- **After contact fetch** (`CONTACT_API.md`): mark **（已获取联系方式）**; show plaintext from unlock response.
- **Footer after list** (contacts not yet fetched): invite user to give **record id** or ask for **all** contacts — no 「解锁」 wording.

## Route A (mailbox)

- Sender, time, subject + structured fields.  
- **Dedup**: **`WORKFLOW_2_MAIL.md` §2.5.1**.  
- Show **`联系电话` / `即时通讯`** when present in DB (from original-body extract).  
- Laycan one line for cargo / open windows.  
- **`preview_url`** on each row when mail preview server is running — link **「查看原邮件」** per **`MAIL_PREVIEW.md`**.
- **`reply_url`** / **`webmail_url`** for **reply** — **`MAIL_REPLY.md`** (webmail first, SMTP fallback).

## Liner schedule

Use skill **`hifleet-schedule`** and its **`WORKFLOW_OUTPUT.md`**.

## Fixed footer (route A)

`💡 **More tonnage/cargo:** https://mytonnages.hifleet.com`
