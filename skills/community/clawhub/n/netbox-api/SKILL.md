---
name: netbox-api
description: "Use when scripting or batch-driving a NetBox instance over the REST API — relocating/renaming devices, cables, IP assignment, OOB/primary IP, pre-verify + read-back."
category: devops
---

# NetBox REST API (using the instance, not administering it)

Operate an existing NetBox **through its REST API** — batch device moves, renames, cable sweeps, IP assignment. For **upgrading the instance, venv drift, rq worker crashes, or reverse-proxy/CSRF config**, use the sibling skill `netbox-upgrade` instead — this skill is only about *using* NetBox via the API.

Verified against NetBox **4.6.8** (`Authorization: Bearer <token>` on every call). Never hardcode the token in files — reference it as a placeholder. Access may be IP-restricted at the reverse proxy; if *every* call 403s with a valid token, that's an allowlist/egress issue, not auth.

## Golden rules for API work
1. **PRE-VERIFY ids → names with GET before any write batch.** Build the plan from a fresh fetch, match every planned object by name, abort on any mismatch. Never PATCH by id from a plan written before the fetch.
2. **READ BACK after every batch.** Re-fetch and diff against the source document (rack, position, site, name, description). A `200` is not proof the change landed.
3. **Batch writes = one Python script, not N tool calls.** A single loop (GET-verify → PATCH/DELETE → read-back) survives timeouts and gives an auditable per-object log. Reusable CLI: `scripts/netbox_api.py`.
4. **Wrong field names are SILENT no-ops, not errors** — see `position` below.

## The field gotchas (these cost real debugging time)
- **The U position field is `position` (float), NOT `rack_unit`.** NetBox 4.x uses `position` + `face` on the Device API. Sending `rack_unit` returns **200 and changes nothing** — always read back.
- **OOB IP is a *device* field, not an IP flag.** The GUI checkbox "Make this the out-of-band IP for the device" maps to `Device.oob_ip` (nullable `BriefIPAddress`). There is **no** boolean on the `IPAddress` schema. Set it via `PATCH /api/dcim/devices/{id}/` with `{"oob_ip": <ip_object_id>}`.
- **`primary_ip4` is nullable.** A device whose only IP is its OOB/management IP should normally have **no** primary IP: `PATCH /api/dcim/devices/{id}/ {"primary_ip4": null}` (200) keeps `oob_ip` intact. Use this when the IP is "only" the management/OOB IP.
- **A device's `primary_ip4` cannot be unassigned** — 400 `Cannot reassign IP address while it is designated as the primary IP`. Clear the device's `primary_ip4` first.
- **The `assigned_object` brief in GET responses has NO `type` key** — only `id`/`url`/`display`/`device`/`name` (±cable/`_occupied`). To map IPs → devices, match `"/dcim/interfaces/" in assigned_object["url"]` and read `assigned_object["device"]["id"]`. Keying on `type == "dcim.interface"` matches nothing.

## Common operations
- **Relocate a device to a rack:** `PATCH /api/dcim/devices/{id}/` with `{"rack": <rack_id>, "position": <int|null>}` (add `"face": "front"` when it matters). For a **cross-site** move, ALSO send `"site": {"id": <site_id>}` and `"location": null` in the **same** call, or you'll get 400s:
  - `Rack X does not belong to site Y`
  - `Location Z does not belong to site Y`
  Get `<rack_id>` from `GET /api/dcim/racks/?limit=100` (name→id, note each rack's `site`). `PATCH` is a partial update — send only the fields you're changing.
- **Assign an IP to an interface:** `PATCH /api/ipam/ip-addresses/{id}/` with `{"assigned_object_type": "dcim.interface", "assigned_object_id": <iface_id>}` (the `assigned_object` object field itself is read-only). To unassign, send `null` for both — but it **400s if the IP is a device's `primary_ip4`**; clear that first.
- **Management-IP migration pattern (move + OOB + unassign legacy):** one device PATCH sets `oob_ip` **and** `primary_ip4` to the new IP, then a second PATCH unassigns the legacy IP object. Doing the unassign first 400s while it's still primary.
- **Verify IP assignments via the IP object** (`assigned_object_id`), not the interface list view — the interface `ip_address`/`ip_addresses` fields can come back empty/missing even when assigned.
- **Trim payloads:** append `&fields=name,rack,position,site` to a list endpoint. Note nested objects come back as `{"id":…, "name":…}` (a dict — use `.get("id")`).
- **Object counts:** `GET /api/<app>/<model>/?limit=1` then read `.count` — cheap way to see if a collection is populated.

## Pagination (a real trap)
- List responses carry `count`, `next`, `previous`. **Always follow `next`** — never assume the last page.
- `GET .../?limit=2000` **silently caps at 1000** (server `MAX_PAGE_SIZE` default). Follow `next` to get the rest.
- `?name=exact-string` on `/api/dcim/devices/` uses **exact-match (iexact) semantics** and may return 0 hits for a name that exists with different casing/form — fetch the full list and filter client-side.
- `scripts/netbox_api.py` follows `next` correctly; use its `all` subcommand rather than hand-paging.

## Discovery
- **OpenAPI schema:** `GET /api/schema/` — served as **YAML**, not JSON. Parse with `yaml.safe_load`, not `json.load`.
- **Version/status:** `GET /api/status/` → JSON with `netbox-version`, `django-version`, `python-version`, `plugins`, `rq-workers-running`.
- **No "Docs" app in 4.6.x:** `/api/docs/*` all 404. When a user says "change the documentation" they usually mean the `description`/`comments` fields on existing objects (or relocating objects) — ask which objects.

## Verify after a batch
Re-fetch the affected objects and diff against the source document. Spot-check a known device's rack/position/name and an assigned IP's `assigned_object_id`. Don't close on 200s alone.

## Verifying API claims against upstream (no live box needed)
When you can't reach the running instance, check the tagged source instead: `raw.githubusercontent.com/netbox-community/netbox/v<VER>/netbox/...`.
- 4.6.x serializer layout is a **`serializers_/` package** — `serializers.py` at `dcim/api/` and `ipam/api/` only re-export from it. Device fields: `dcim/api/serializers_/devices.py`; nested (brief) forms: `dcim/api/serializers_/nested.py`; IP fields: `ipam/api/serializers_/ip.py`.
- Pagination defaults: `netbox/netbox/config/parameters.py` — `PAGINATE_COUNT` default **50**, `MAX_PAGE_SIZE` default **1000** (both overridable in `configuration.py`).
- Device validation error strings: `dcim/models/devices.py`; primary-IP unassign guard: `ipam/models/ip.py`.

## References
- `references/netbox-api.md` — field-level quick reference (all the field gotchas + common ops in one table-ish doc)
- `references/batch-device-operations.md` — full verified recipe: relocate 21 nodes, renames, description tags, 68-cable sweep (GET-verify → write → read-back)

## Sibling skill
- `netbox-upgrade` — major-version upgrades, venv/requirements drift, rq worker `ImportError: cannot import name 'Connection'`, and reverse-proxy CSRF 403s (`references/proxy-csrf-403-behind-reverse-proxy.md`). If the task is *fixing the instance* rather than *driving it via the API*, switch there.
