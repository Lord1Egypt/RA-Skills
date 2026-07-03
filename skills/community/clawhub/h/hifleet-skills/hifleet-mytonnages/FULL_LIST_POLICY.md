# Full list policy (route C only)

**Pre-arrival** (`POST /destination/search`): paginate until **`total`** is collected; show **all** rows.

Does **not** apply to route A mailbox search.

## Algorithm

1. `POST` with `offset` / `limit` (see **`DESTINATION_SEARCH_API.md`**).  
2. Merge pages until count ≥ **`total`**.  
3. Reply with **Total: N** and every record.

**Liner schedules**: **`hifleet-schedule`** / **`FULL_LIST_POLICY.md`** there.
