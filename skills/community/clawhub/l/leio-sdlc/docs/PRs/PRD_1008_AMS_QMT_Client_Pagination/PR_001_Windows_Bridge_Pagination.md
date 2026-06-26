status: closed

# PR-001: Windows Bridge Pagination Support

## 1. Objective
Modify the Windows QMT Bridge (`server.py`) to support chunked data retrieval for the `/api/bulk_quote` endpoint, preventing timeouts when fetching the entire A-share market.

## 2. Scope & Implementation Details
- `server.py`: Update `/api/bulk_quote` to accept `chunk_size` (default 500) and `chunk_index` (default 0) query parameters.
- Fetch the full stock list using `xtdata.get_stock_list_in_sector('a_shares')`.
- Calculate `start` and `end` indices based on `chunk_size` and `chunk_index`.
- Slice the stock list and fetch full ticks only for that slice via `xtdata.get_full_tick(slice)`.
- Return a JSON response structured as `{"data": {...}, "total_stocks": <total_count>, "chunk_index": <index>, "chunk_size": <size>}`.

## 3. TDD & Acceptance Criteria
- Write a unit test simulating a request to `/api/bulk_quote?chunk_size=100&chunk_index=0` and verify the payload contains exactly 100 stocks.
- Verify the response includes `total_stocks`, `chunk_index`, and `data` fields.
- Ensure requests outside the bounds (e.g., `chunk_index` very high) return an empty `data` dict without throwing exceptions.