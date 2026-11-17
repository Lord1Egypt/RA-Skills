---
name: gmail-filter-architect
description: "Design, verify and import a complete Gmail filter system: a small emoji label taxonomy, urgent mail starred, bills/finance/infra/codes labelled, marketing and social auto-archived, forwarded accounts tagged by source. Built from a 90-day sender census of your own mailbox, every rule is checked against your real mail for misfires before import, and every archiving rule carries a shared protection group so bills, codes and security alerts are never hidden. Use for: cleaning up Gmail filters, bills landing in promotions, important mail getting archived, 'set up the best Gmail filters', labelling mail forwarded from other accounts. 中文:整理 Gmail 过滤器、账单被当营销收走、重要邮件看不到、转发来的邮件标记来源账号、要一套最好的过滤规则。"
license: MIT
compatibility: "Census and verification need a Gmail connector with read access (label creation optional). Import via browser automation (Claude in Chrome), gmailctl, or manual XML upload in Gmail settings."
metadata:
  version: "1.0.0"
---

# Gmail Filter Architect

Goal: nothing important is missed, noise is archived automatically, and every message shows at a glance what it is and which account it came from.

The generator is `scripts/build_filters.py`. Your personal settings live in `profiles/<you>.json` (start from `profiles/TEMPLATE.json`, or `profiles/example.zh-CN.json` for Chinese labels and keywords). Never commit a real profile to a public repo.

## 0. Five rules (breaking any of them causes real damage)

1. **Every archiving filter carries the same protection group** (`protect`). Gmail has no "move back to inbox" action and there is no "stop processing"; every matching filter runs. If any one filter archives a message, nothing can bring it back. The protection group excludes subjects about codes, security, login, passwords, bills, receipts, invoices, statements, overdue, renewal, suspension, abuse, tickets, "action required", plus critical senders (Apple, cloud providers, account security).
2. **CJK keywords only inside `subject:`**. Gmail matches Chinese/Japanese/Korean as substrings, so a body match on 优惠 ("discount") also hits bank mail about 优惠利率 ("preferential rate"). In the first real run, body keyword filters had silently archived 85 transactional mails (hosting bills, credit card overdue notices, broker agreement updates, anti-fraud notices).
3. **Never use `unsubscribe` to detect marketing.** Bank payment reminders, broker login alerts, receipts and GitHub notifications all have it in the footer. Use `category:promotions` / `category:social` (the plural form works in search; the singular returned 0) plus a known marketing sender list.
4. **No `is:`, `label:`, `in:` or dates in filters.** New mail has none of those states, so they never match.
5. **One user label per filter**, and keep each query under ~1,400 characters (Gmail rejects around 1,470–1,490 with "The specified filter is too long").

## 1. Sender census (read-only)

With the Gmail connector (`search_threads`, metadata view, page size 50):
- Page through `newer_than:90d` (archived mail included). Group by sender address/domain: thread count, whether most sit in the inbox, one or two example subjects.
- Put each sender in one bucket: urgent candidates (security, login, failed payment, suspension, abuse report, review rejection) · bills · infrastructure (cloud, VPS, CDN, DNS, registrar, GitHub, email delivery) · Apple / app stores · finance (**list transactional and marketing addresses separately**) · verification codes · own business · marketing / social / cold outreach · real people.
- Check specifically: do banks, cards, brokers and exchanges send marketing from different addresses than statements and alerts? (Usually yes, which lets you separate them exactly.) Which transactional mails have "discount / coupon / % off" or local-language equivalents in the subject?
- On a large mailbox, give this to a background agent and ask for ready-to-paste `from:{...}` groups and subject keyword groups.

## 2. Write the profile, generate

Fill `profiles/<you>.json`: `labels`, `protect`, `urgent`, `bill`, `infra`, `apple`, `fin` (txn / mkt / exclude_compact / archive_rules), `otp`, `biz`, `mkt` (brand groups, social, cold, subject keywords), `extra_rules` (e.g. `deliveredto:` rules for forwarded accounts).

```bash
python3 scripts/build_filters.py profiles/<you>.json out/ --gmailctl
```

Outputs `batchA.xml` (label only), `batchB.xml` (star / archive), `tests.json` (one search query per filter) and, with `--gmailctl`, `gmailctl.jsonnet`. The script checks length and bracket balance.

Recommended labels (about ten; the emoji prefix makes them easy to spot and sorts them first):

| Label | Actions | Inbox? |
|---|---|---|
| ⚠️ Action | star + important + never spam | yes (new mail only) |
| 💳 Bills / 🍎 Apple / 📈 Finance / 🔐 Codes / 🛠 Infra / 🏢 Business | label + never spam | yes |
| Marketing / Marketing/Social / Marketing/Cold | archive + mark read + never important | no |
| From/<account> | label only (`deliveredto:account@gmail.com`) | yes |

High-volume routine infra and finance mail (DNS change confirmations, Search Console reports, GitHub CI, daily broker statements) gets its own "label + archive" rule, still with the protection group. For infra senders use a **subject whitelist** (archive only the routine subjects). Archiving a whole infra sender also swallowed its login codes, "zone deleted" alerts and nameserver warnings in the first run.

## 3. Verify every rule against real mail (before importing)

Run each query in `tests.json` as `(<query>) newer_than:90d` and read the first 30 subjects:
- **Archiving rules**: any bill, renewal/expiry notice, security or login alert, code, failed payment, account warning, app review, cloud provider notice or human reply among the hits is a serious misfire. Add it to the protection group or exclude the sender.
- **Star rules**: estimate stars per week. If marketing gets starred, exclude that sender. One or two a day is the useful maximum.
- **Label rules**: fix obvious wrong categories.
- Coverage: search `in:inbox newer_than:21d` for marketing senders that no rule catches, and for important mail that no label covers.
- A background agent can do this read-only; ask for "rule | hits | misfires | concrete fix".

## 4. Import

Pick one:
- **Manual**: Gmail Settings → Filters and Blocked Addresses → Import filters → choose file → Open file → review → Create filters.
- **gmailctl**: merge `gmailctl.jsonnet` into your config, `gmailctl diff`, then `gmailctl apply`. gmailctl only affects new mail.
- **Browser automation** (only with the user's permission): find the file input, upload, read the checkbox state with JS, click Create.

Batch A: tick "Also apply filter to matching conversations" (it only adds labels, so old mail gets categorised). Batch B: **do not tick it** (old mail would be starred or archived en masse).

Create labels first if you can (Gmail connector `create_label`, with colours). Renaming an existing label is safe: filters reference labels by ID.

Three import pitfalls seen in practice:
- The "apply to matching conversations" checkbox **remembers its last state**. After importing batch A with it ticked, it is still ticked for batch B. Read it before every Create.
- Creation is **asynchronous**: a "Creating N filters" dialog runs for tens of seconds, then "Filter import completed". Until then the import panel is still open and its preview rows look like filters, so any row count is wrong. Reload the settings page before counting.
- After import, **the new filters stay selected** in the list. If you then tick old filters and bulk-delete, the new ones go too. Clear every checkbox first, tick only the targets, check with JS that the selected count equals the target count, then delete. Deleting while creation is still running queues and stalls.

## 5. Replace old filters

Import only adds; it never modifies existing filters. Save the old filters' text as a backup, then select the superseded ones by their criteria text (see pitfalls above) and bulk-delete.

## 6. Finish

- Move mail that the old filters wrongly archived back to the inbox (connector `label_thread` with `INBOX`).
- Take a screenshot of the inbox to confirm labels show.
- Report: total filters, actions per group, verification results, and anything deliberately left alone (e.g. senders the user blocked on purpose).
- Suggest a quarterly re-run of step 1 to catch new marketing and infra senders; a simple calendar or chat reminder is enough.

## Rollback

The old filters' text is in the backup; new filters can be selected by label and deleted. Archived mail is still under its label; add `INBOX` back with `label_thread`.

## References

- `references/research-2026-09.zh-CN.md`: survey of widely recommended Gmail filter practice with sources (in Chinese).
