---
name: invoice-sorter
description: Sort, rename, and organize invoices, receipts, bills, statements, and related PDF or image files into a predictable folder structure. Use when asked to clean up finance documents, batch-organize invoice folders, standardize filenames, separate vendors or months, or prepare records for bookkeeping and reimbursement workflows.
---

# Invoice Sorter

Organize finance documents conservatively. Prefer inspection and a rename/move plan before making file changes.

## Workflow

1. Scan the target folder and identify likely invoice-like files.
2. Infer a practical structure from filenames and metadata first.
3. If document content must be read to classify correctly, sample a few files before doing broad changes.
4. Propose a naming and folder rule.
5. Execute batch renames or moves only after the rule is clear.
6. Produce a summary of what was moved, renamed, skipped, or flagged.

## Good default folder structures

Choose the simplest structure that matches the collection:

### By year and month
- `YYYY/MM`
- good for mixed bills and receipts

### By vendor
- `Vendor/YYYY`
- good for recurring suppliers

### By document type
- `invoices/`, `receipts/`, `statements/`, `contracts/`
- good when files are heterogeneous

## Good filename patterns

Prefer stable, sortable names such as:
- `YYYY-MM-DD_vendor_amount_invoice.pdf`
- `YYYY-MM_vendor_invoice-number.pdf`
- `vendor_YYYY-MM_statement.pdf`

Use lowercase and hyphens/underscores consistently.

## Safety rules

- Avoid deleting originals unless the user explicitly asks.
- If metadata is ambiguous, move uncertain files into a `review/` folder instead of guessing.
- Preserve file extensions exactly.
- For very large batches, do a dry-run summary first.

## Output pattern

Report using:
- **Detected files**
- **Proposed structure**
- **Planned renames/moves**
- **Ambiguous items**
- **Completed changes**

Keep the plan auditable so the user can spot mistakes quickly.
