# Google Sheets default
Use the host's Sheets connector/skill when available; authenticated browser editing is a fallback under applicable provider rules. Missing access -> deliver a CSV/draft, not a fictitious live URL.

## Design
Prefer one row per intended contribution/claim with opaque slot_id and claim_id. Columns: category, contribution, portions, contributor display name (consented), status, updated_at; keep capacity/target definitions in an organizer-controlled Slots tab if using multiple claims per category. Attendance is a separate measure.
Freeze headers, wrap descriptions, add status validation and filter views. Protect formulas/ID definitions from accidental edits where possible. Protection/hidden tabs aren't privacy boundaries: all shared file contents must be guest-safe. Keep private contacts/notes/gifts in a different unshared file.
Use actual discovered spreadsheet ID, tab names and explicit A1 ranges. Don't overwrite a reference workbook; copy if it wasn't authorized for editing. Share only to the intended audience; creating a file doesn't authorize public-link access.

## Writes and concurrency
Use RAW for untrusted guest text in API value writes; a leading '=' must not become a formula. For CSV/manual paste, encode formula-like prefixes as literal text and verify actual stored type. Keep generated formulas in known controlled columns; never execute a formula supplied by a guest.
Read current cells/formulas, compare with the expected old values, write the smallest range, then re-read. Batch formatting/structural operations can be grouped; atomic batch application is NOT a row claim lock or compare-and-swap against concurrent human edits. Detect conflicts and ask/reconcile instead of overwriting. A shared editable Sheet cannot promise exclusive slots: surface duplicate/overfilled claims for organizer resolution. If strict capacity is essential, choose a provider with enforced capacity or build a separately authorized transactional form service.

## Synchronization
An API read omits trailing empty rows/columns: reconstruct using headers/IDs, not row length alone. An incomplete/filtered read cannot prove cancellations. Don't sort/delete entire ranges to make the display tidy. Record snapshot time and whether the full relevant table was read. Verify saved cells and permissions before reporting delivery. No Apps Script deployment needed for this version.
