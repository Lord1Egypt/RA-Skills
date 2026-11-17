# NetBox REST API quick reference

Verified against NetBox **4.6.8**. Use `Authorization: Bearer *** on every call.

## Discovery
- **OpenAPI schema:** `GET /api/schema/` — served as **YAML** (`content-type: application/vnd.oai.openapi`), NOT JSON. Parse with a YAML parser (`yaml.safe_load`), not `json.load` (that throws `JSONDecodeError: line 1 column 1`). ~308 paths.
- **Version:** `GET /api/status/` returns JSON with `netbox-version`, `django-version`, `python-version`, `plugins`, `rq-workers-running`.
- Unauthenticated `/api/` returns `{"detail":"Authentication credentials were not provided."}` — that's the token path working, not a block.

## Pitfall: no "Docs" app in 4.6.x
`/api/docs/*` (sections/pages/links) does NOT exist in 4.6.x — all 404, and there are no `docs` paths in the schema. Don't hunt for a documentation store. When a user says "change the documentation" in NetBox, they usually mean the **`description` / `comments` fields on existing objects** (devices, interfaces, IPs, sites, racks) — or relocating objects. Ask which objects before assuming a doc app exists.

## Field gotchas (the ones that cost debugging time)
- **U position is `position` (float), NOT `rack_unit`.** 4.x Device API: `position` + `face`. Sending `rack_unit` is silently ignored (200, no change) — always read back.
- **OOB IP is `Device.oob_ip`** (nullable), set by `PATCH /api/dcim/devices/{id}/ {"oob_ip": <ip_object_id>}`. There is **no** OOB boolean on the IPAddress schema.
- **`primary_ip4` / `primary_ip6` are nullable.** OOB-only management devices should normally have no primary IP: `PATCH ... {"primary_ip4": null}` (200) keeps `oob_ip` intact.
- **Unassigning a primary IP 400s** (`Cannot reassign IP address while it is designated as the primary IP`). Clear `primary_ip4` on the device first.
- **`assigned_object` brief has no `type` key** — keys are `id`/`url`/`display`/`device`/`name` (±`cable`, `_occupied`). Match `"/dcim/interfaces/" in assigned_object["url"]` and read `assigned_object["device"]["id"]`.
- **`?name=` on devices is exact-match (iexact)** — may return 0 hits. Fetch the full list, filter client-side.

## Common operations
- **Trim payloads:** append `&fields=name,rack,position,site` (comma list) to any list endpoint to reduce response size. Also `?limit=N&offset=M` for pagination; list responses carry `count`, `next`, `previous`.
- **List devices with rack context:**
  `GET /api/dcim/devices/?limit=100&fields=name,rack,position,site`
  `rack` comes back nested as `{"id":…, "name":…}` (or `None`); `position` is the U position (may be `null` instance-wide if nobody sets U placement — a pure rack reassignment then needs no unit math).
- **Relocate a device to a rack:**
  `PATCH /api/dcim/devices/{id}/` with `{"rack": <rack_id>, "position": <int|null>}` — the field is **`position`** (float), NOT `rack_unit` (that is silently ignored with a 200). Add `"face": "front"` when it matters.
  For cross-site moves also send `"site": {"id": <site_id>}` and `"location": null` in the SAME call, or you'll get 400s about rack/site and location/site consistency (`Rack X does not belong to site Y` / `Location Z does not belong to site Y`).
  Get `<rack_id>` from `GET /api/dcim/racks/?limit=100` first (name→id mapping). `PATCH` is a partial update — send only the fields you're changing.
- **Assign an IP to an interface:** `PATCH /api/ipam/ip-addresses/{id}/` with `{"assigned_object_type": "dcim.interface", "assigned_object_id": <iface_id>}` (the `assigned_object` object field is read-only). To unassign, send `null` for both — but **it 400s if the IP is a device's `primary_ip4`**; clear `primary_ip4` on the device first.
- **Management-IP migration pattern:** one device PATCH sets `oob_ip` **and** `primary_ip4` to the new IP, then a second PATCH unassigns the legacy IP object (unassign-first 400s).
- **Mapping IPs to devices from GET responses:** the `assigned_object` brief object carries only `id`/`url`/`display`/`device`/`name` — **no `type` key**. Match `"/dcim/interfaces/" in assigned_object["url"]` and read `assigned_object["device"]["id"]`; keying on `type == "dcim.interface"` matches nothing.
- **Verify IP assignments via the IP object** (`assigned_object_id`), not the interface list view — the interface `ip_address`/`ip_addresses` fields can come back empty/missing even when the IP is assigned.
- **Object counts / existence:** `GET /api/<app>/<model>/?limit=1` then read `.count` — cheap way to see if a collection (e.g. `ipam/prefixes`, `circuits/circuits`) is populated without pulling rows.

## Pagination
- Always follow `next`. `?limit=2000` **silently caps at 1000** (server `MAX_PAGE_SIZE` default; configurable in `configuration.py`).
- `scripts/netbox_api.py` `all` subcommand handles this by following `next` — use it instead of hand-stepping `offset`.

## Notes
- Racks live at `GET /api/dcim/racks/`; each has `id`, `name`, `site`, `location`, `u_height`.
- Some devices legitimately have `name: null` (unnamed placeholder devices) — guard `d.get("name") or ""` when filtering client-side.
- Never hardcode the API token in files/notes — reference it as a placeholder.
- Access may be IP-restricted at the reverse proxy (nginx `403 Forbidden` from outside the trusted network). If every call is 403 even with a valid token, that's an egress/allowlist issue, not an auth issue — confirm with the user before debugging the token.
