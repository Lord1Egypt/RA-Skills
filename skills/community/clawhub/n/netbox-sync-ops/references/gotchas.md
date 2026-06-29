# Gotchas — NetBox/UniFi API quirks (read for churn or 400s)

These cause either perpetual re-PATCH ("churn", not idempotent) or HTTP 400.

## Idempotency / churn

- **`vcpus` round-trips as float.** NetBox returns `2.0`, Proxmox gives `2`;
  string comparison thinks they differ and patches every run. Compare numerically.
- **`assigned_object_type` has no readable top-level field.** When re-linking an IP
  to an interface, comparing/patching that field always looks "missing" → re-PATCH
  forever. Skip the assignment fields when the IP is already on the target object.
- **Listing endpoints return shallow nested objects.** The `dcim/mac-addresses`
  listing's embedded `assigned_object` omits `custom_fields`. Re-fetch the
  interface before comparing CFs, or CF patches fire every run.
- **Don't append to shared text fields from two writers.** Two sync passes editing
  the same `description` will fight. Give each writer its own field (e.g. structured
  custom fields) instead of concatenating into one string.

## HTTP 400

- **VirtualDisks own the VM `disk` value.** Once a VM has VirtualDisks, NetBox sets
  `disk` to their aggregate and rejects mismatched PATCHes. Never set `disk` on the
  VM directly when disks are also synced.
- **VMInterface `bridge` is a reference to another interface, not free text.** Use
  `description` for the host bridge name.
- **Interface type strings are exact.** `10gbase-x` is invalid; use
  `10gbase-x-sfpp` for SFP+, `1000base-t` for copper GbE.
- **`wireless_lans` (M2M) exists only on `dcim.interface`, not on
  `virtualization.vminterface`.** Model wireless endpoints as DCIM devices if they
  must hold WLAN membership.

## Cabling

- NetBox cables are point-to-point. A trunk/aggregation port serving many endpoints
  can't be cabled to all of them — only cable genuine 1:1 physical links. Skip
  creating a cable if either interface already reports a `cable`.

## UniFi API

- The **Integration API does not expose WLANs/SSIDs**; the **legacy private REST
  API** does (`/proxy/network/api/s/<site>/rest/wlanconf`, `/rest/networkconf`,
  `/stat/sta`, `/stat/device`) and accepts the same API key. The legacy site is
  usually `default`, not the Integration site UUID.
- Copy every field you need out of `stat/sta` into your snapshot explicitly (e.g.
  `ip`) — it's easy to drop one and silently lose downstream data.
