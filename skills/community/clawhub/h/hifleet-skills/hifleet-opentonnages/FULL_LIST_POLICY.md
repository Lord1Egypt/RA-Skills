# Full list policy (routes V + G)

**Public open vessel** and **public cargo** list APIs: paginate until **`total`** is collected; show **all** rows to the user.

Does **not** apply to optional single-row **`enrich-row`** calls.

## Algorithm

1. `POST` with `offset` / `limit` (see **`VESSEL_SEARCH_API.md`** or **`CARGO_SEARCH_API.md`**).
2. Read **`total`** from the first response; merge all pages until count ≥ **`total`**.
3. Reply with **Total: N** and every record (per **`WORKFLOW_OUTPUT.md`**).
4. **Do not** sample, truncate, or “show 3 examples” unless the user explicitly asks for a short preview.

## Offset

Follow each API doc (typically **`offset` starts at 1**). Increase by page size or per response `data.length` until complete.
