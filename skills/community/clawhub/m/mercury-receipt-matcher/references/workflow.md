# Receipt matcher workflow

## Purpose
Match card transactions to real merchant receipts, forward valid receipts to `receipts@mercury.com`, and preserve a complete audit trail.

## Inputs
- transaction CSV export
- connected Gmail accounts
- matching rules
- SQLite database

## Batch workflow
1. Import any new CSV rows into `transactions`.
2. Keep each wake small. Default batch size is **3 rows maximum**.
3. Select the next N transactions with status `pending` or other not-yet-triaged states first. Revisit/error states should be processed only after the fresh queue has been worked through.
4. For each transaction:
   - search every connected Gmail account
   - record every search attempt
   - record candidate messages considered
   - truncate candidate material before reasoning over it: keep subject, from, to, date, the line(s) containing total/amount, and at most the first ~1000 characters of useful body text
   - drop HTML, signatures, footers, and quoted thread history whenever possible
   - prefer a valid original merchant receipt with exact amount match
   - if no exact match exists but there is a strong close match, use the best close match and keep the row in revisit state
5. If a valid receipt is found:
   - create a forward attempt record
   - forward to `receipts@mercury.com`
   - mark transaction `forwarded` on success
   - if the forwarded receipt is a close match, set a reconciliation status like `forwarded_close_match` or `forwarded_amount_mismatch` and keep `actionable_status = revisit`
6. If no valid receipt is found:
   - mark `not_found`, `skipped_no_receipt_expected`, or `needs_review`
7. Wrap each row's SQLite writeback in a **single transaction** so a mid-wake abort leaves that row fully updated or fully untouched.
8. Emit a short best-effort summary.

## Rules
- Search all connected Gmail accounts before declaring `not_found`.
- Never fabricate a forward with a composed email.
- Never use a human-forwarded copy when the original merchant email can be found.
- Exact amount match is preferred, not mandatory.
- When a strong close match is forwarded, record the mismatch clearly and keep the row out of the fully-done state.
- Prioritize fresh, not-yet-triaged rows before revisit rows.
- Revisit/error rows should be processed last, after the pending/new queue has been exhausted or when explicitly requested.
- When revisit rows are eventually processed, try forwarding again by default if a best valid candidate now exists.
- Do not carry prior-run summaries in prompt context. Each wake should derive state from `/workspace/receipts.db`.
- Keep prompt/context lean: read `SKILL.md` and `references/workflow.md` from disk only when needed instead of inlining them into the wake prompt.
