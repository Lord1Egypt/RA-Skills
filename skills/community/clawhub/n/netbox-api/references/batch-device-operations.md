# Batch device operations — verified recipe (4.6.8)

Full workflow run against a self-hosted NetBox (4.6.8) in one session: relocate 21
storage-cluster nodes between racks/sites, normalize hostnames, set description
tags, and delete 68 stale 25G cables. All via API with pre-verify + read-back.

## The 5 rules that matter
1. **PRE-VERIFY ids → names with GET before any write batch.** Build the move
   plan from a fresh fetch, match every planned object by name, abort if any
   mismatch. Never patch by id from a plan written before the fetch.
2. **READ BACK after every batch.** Re-fetch and diff against the source
   document (rack, position, site, name, description). Count mismatches;
   don't trust the 200 responses alone.
3. **Site/location consistency is enforced on rack moves** (400 errors):
   `Rack X does not belong to site Y` and `Location Z does not belong to site Y`.
   Fix by PATCHing `site` + `location: null` + `rack` + `position` in ONE call.
4. **Wrong field names are SILENT no-ops**, not errors: sending `rack_unit`
   returns 200 and changes nothing. The field is `position` (float) + `face`.
   Verify with a read-back or you will report success on a no-op.
5. **Batch writes = one Python script, not N tool calls.** A single script that
   loops GET-verify → PATCH/DELETE → read-back is faster, survives timeouts,
   and produces an auditable per-object log. Reusable CLI: `../scripts/netbox_api.py`.

## Relocation (cross-site)
```
PATCH /api/dcim/devices/{id}/
{"site": {"id": <target_site_id>}, "location": null,
 "rack": {"id": <rack_id>}, "position": <u_int>}
```
- `location: null` is REQUIRED when the device's current location belongs to the
  old site — omitting it is the second 400 wave after fixing the site error.
- Racks: `GET /api/dcim/racks/` (name → id, note `site` per rack).
- If devices have no `device_type`, U heights aren't validated — the document's
  positions are trusted as-is; check gap-free fit manually.

## Renames
- `PATCH /api/dcim/devices/{id}/ {"name": "new"}` — run a **collision check**
  over the computed new-name set first.
- NetBox device names are free-form; FQDNs in names are common
  (e.g. `ceph-a2-09.example.com`). Normalize per the user's declared schema.

## Description tags
- `PATCH /api/dcim/devices/{id}/ {"description": "<SERVICE-TAG>"}` (e.g. an asset/order number).
- **Check for EXISTING descriptions first**: if non-empty and the tag absent,
  append (don't clobber). If a *different-looking* tag already exists (typo
  variant), flag it to the user and replace only on confirmation — one such
  case appeared mid-session (an extra digit in the tag for two nodes).

## Cable sweep (delete stale cabling)
1. Fetch all interfaces with pagination (`limit=500` + follow `next`; the 1000/page cap applies).
2. Select target interfaces (e.g. device in cluster AND name matches `GbE-25G-*` AND `cable` set).
3. For each distinct `cable.id`, `GET /api/dcim/cables/{id}/` and resolve BOTH
   ends via `a_terminations` / `b_terminations` (each: `object_type`,
   `object_id`, `object.{name,device.name}`).
4. Assert: exactly one end is the target node, the other end is an EXPECTED
   peer set (e.g. the two switch device names). Any unexpected peer → ABORT.
5. `DELETE /api/dcim/cables/{id}/` per cable; expect 200/204.
6. Read back: re-fetch interfaces, assert zero cabled interfaces in the target set.

## Gotchas seen in practice
- `GET /api/dcim/interfaces/?limit=2000` silently returns only 1000 rows — always paginate.
- `?name=exact-string` on `/api/dcim/devices/` returned 0 hits on this build
  (exact-match semantics) — fetch the full list, filter client-side.
- `fields=` trimming works on list endpoints; note `device` comes back nested
  `{"id":…, "name":…}` (unhashable dict — use `.get('id')`).
- 42U racks: U positions counted from 1; "RU 1 → 2" style docs = 2U nodes at
  starting units 1, 3, 5, ….
- TLS: internal cert — the script verifies certificates by default; for
  self-signed CAs export `NETBOX_INSECURE_TLS=1` (equivalent to `curl -k`).
- Keep tokens in the script/session only; do NOT write them into skill files or
  reference notes (this file intentionally has none).
