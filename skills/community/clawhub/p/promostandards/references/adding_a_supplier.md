# Config shape, adding a supplier, adding a version

## Config shape

Configuration is a **per-service map**, not a base URL. A supplier does not
have "an endpoint" — it has an independently chosen URL *and* version per
service, and they do not move together. SanMar publishes Inventory at both
1.2.1 and 2.0.0, Product Data at 1.0.0 and 2.0.0, and PO only at 1.0.0, each
on its own path:

```json
{
  "supplier": "SanMar",
  "credentials": {
    "id": "${PS_SANMAR_ID}",
    "password": "${PS_SANMAR_PASSWORD}"
  },
  "services": {
    "INV": {
      "url": "https://ws.sanmar.com:8080/promostandards/InventoryServiceBindingV2final?WSDL",
      "wsVersion": "2.0.0",
      "testUrl": "https://edev-ws.sanmar.com:8080/promostandards/InventoryServiceBindingV2final?WSDL",
      "status": "Production"
    },
    "PO": {
      "url": "https://ws.sanmar.com:8080/promostandards/POServiceBinding?WSDL",
      "wsVersion": "1.0.0",
      "testUrl": "https://edev-ws.sanmar.com:8080/promostandards/POServiceBinding?WSDL"
    }
  }
}
```

| Field | Required | Notes |
| --- | --- | --- |
| `supplier` | yes | registry company code |
| `credentials` | yes | omitting it leaves nothing for the runtime to fill |
| `credentials.id` | no | when present, **must** be a `${ENV_VAR}` reference |
| `credentials.password` | no | also a reference; omitted if the supplier needs no password |
| `services.<CODE>.url` | yes | production endpoint |
| `services.<CODE>.wsVersion` | yes | exact version string from the registry |
| `services.<CODE>.testUrl` | no | required for test-mode PO submission |
| `services.<CODE>.status` | no | `Production` / `Deprecated`, informational |
| `services.<CODE>.namespaces` | no | prefix→URI overrides for non-compliant suppliers, merged over the adapter's defaults |

### Namespace overrides

Not every supplier honours the spec's namespace. Sampling live WSDLs found
3M serving Inventory 1.2.1 under its own:

```json
"INV": {
  "url": "https://...",
  "wsVersion": "1.2.1",
  "namespaces": {"ns": "http://inventoryservice.promostandards.mmm/"}
}
```

This affects the **request** side only — responses are parsed by local name
and ignore namespaces entirely, so a non-compliant reply parses either way.
Reach for an override only when a supplier rejects well-formed requests;
confirm by fetching their endpoint's WSDL and reading its
`targetNamespace`.

Service codes are the registry's, upper-cased: `INV`, `PRODUCT`, `PPC`,
`PO`, `OSN`, `ODRSTAT`, `INVC`, `MED`, `PDC`. Note the registry spells
Product Data as `Product`, not `PROD`; both spellings normalise to
`PRODUCT`.

A literal credential value inside the `credentials` block is **rejected at
load time**, so a working secret cannot be committed by accident.

### Delegated credentials

The config describes endpoints; identity always comes from the environment.
On a delegated agent-to-agent turn the platform injects the *calling*
agent's shared credentials into this process's environment under the same
`PS_<SUPPLIER>_ID` / `PS_<SUPPLIER>_PASSWORD` names the config already
references, for that turn only, before the script runs. So there is nothing
extra to configure in the file and nothing extra to pass on the command
line — the identical committed config serves every caller.

Credentials are never accepted on stdin, and a `credentials` object there is
rejected. The reason is not stylistic: on a delegated turn the values are
deliberately withheld from the agent's context, so the only party able to
compose such a payload is one that should never have seen them.

Isolation comes from the process boundary. Each invocation is its own
process reading its own environment, so a delegated identity cannot outlive
its turn or reach another caller's request.

`describe()` reports `credentials.source` as `environment` or `none`, so an
operator can confirm a call had an identity without ever printing one. It
cannot tell a host credential from a delegated one — both arrive as the same
env var, and the process is never told which filled it.

## Where the config comes from

`SupplierConfig.load` tries three sources and takes the first that answers:

1. **An explicit path** — used verbatim, so a config you manage yourself is
   never shadowed by anything bundled.
2. **A bundled override** — `assets/suppliers/<name>.json`.
3. **The bundled registry capture** — `from_registry()` runs the same
   `provision.build_config` path at call time.

Step 3 is the one that matters: ~575 of the registry's companies produce a
drivable config with nothing checked in, so adding a vendor is a name in a
payload, not a skill release. Env var names come out of the company code the
same way `provision.py` derives them, so credentials line up automatically.

Names are matched by slug — case, spaces and punctuation ignored — and the
override directory is resolved relative to the skill rather than the process
cwd, because a skill does not get to assume where the agent's `exec` runs it
from.

### Overrides must claim every name for their supplier

`_override_index()` keys each override by **both** its filename and the
`supplier` code inside it. That is not tidiness. The registry's code for
Cutter & Buck is `Cutter` while the file is named for the brand, so indexing
only the filename would let `{"config": "Cutter"}` fall through to step 3 and
silently return the endpoints the override exists to correct — the same
failure shape as the misordered `getFobPoints` request: a plausible answer,
no error, wrong data.

### When an override is warranted

Only when the registry is wrong or incomplete for that supplier, and it cannot
be fixed at the registry. Write the correction, and record its provenance in
the config's `_note` field — keys prefixed with `_` are ignored by the loader,
so the note travels with the config instead of rotting in a ticket.

```bash
python3 scripts/provision.py "Cutter & Buck" --bundle --validate
# wrote .../assets/suppliers/cutter.json
```

Then correct the generated file and commit it — a hosted agent's workspace
`skills/` directory is wiped and force-reinstalled from source on **every
boot**, so committing is what makes an override survive a restart. Overrides
hold `${ENV_VAR}` references and endpoints, never a credential value, so
committing them leaks nothing.

Pass `--bundle <name>` to choose the filename, or `-o <path>` for a config you
do not intend to ship.

## A vendor document beats the registry

The registry is a self-reported directory and it goes stale. Cutter & Buck's
bundled config is the worked example: the registry lists Product Data only at
1.0.0, while the vendor's own integration document specifies 2.0.0 at
`ProductData200.asmx` — and conversely the registry carries the PO **test**
endpoint (`qapi.cbcorporate.com`) that the vendor document mentions but never
gives a URL for. Neither source is complete. Provision from the registry, then
reconcile against whatever the supplier sent you, and record in the config's
`_note` field which endpoints came from where — keys prefixed with `_` are
ignored by the loader, so notes travel with the config instead of rotting in a
ticket.

## Adding a supplier

Data entry, not engineering:

```bash
python3 scripts/provision.py <CompanyCode> -o <supplier>.json --validate
export PS_<SUPPLIER>_ID=... PS_<SUPPLIER>_PASSWORD=...
python3 scripts/smoke_test.py --config <supplier>.json --product-id <a real style>
```

`provision.py` reads the captured registry dump, picks the newest version
of each service that has an adapter, and reports anything it skipped. If
the company code is unknown, refresh the dump:

```bash
python3 scripts/ps_registry.py dump -o assets/promostandards_endpoints.json
python3 scripts/ps_registry.py summary
```

The smoke test is read-only and never submits a PO. Treat its output as the
provisioning sign-off.

## Adding a service version

One new module, registered in one table. Never a branch inside an existing
request builder — the versions diverge far more than they appear to.

1. Fetch the WSDL for the version from `/json/services` (the `WSDL` field is
   a zip URL). **Extract it with Python's `zipfile`, not `unzip`** — several
   packages, Inventory 1.2.1 among them, are malformed in a way `unzip`
   rejects as overlapped components.
2. Read the request and response schemas and note four things: the target
   namespace, the request root element name, whether shared objects live in
   a second namespace, and the error channel (`ServiceMessageArray` vs a
   bare `errorMessage`).
3. Copy the closest existing adapter in `scripts/adapters/` and edit those
   four things plus the element spellings.
4. Register it in `scripts/adapters/__init__.py` under `ADAPTERS`.
5. Record a response fixture in `assets/fixtures/` and add a test to
   `scripts/_selftest.py`. Include a sparse variant — a supplier that omits
   every optional field — because that is what breaks parsers in practice.

### The namespace is not derivable from the version

The single most important rule. `NAMESPACES` is a hardcoded constant on each
adapter and must never be built by interpolating `wsVersion`:

| Service | Version | Target namespace |
| --- | --- | --- |
| Inventory | 1.2.1 | `.../WSDL/InventoryService/1.0.0/` |
| Inventory | 2.0.0 | `.../WSDL/Inventory/2.0.0/` |
| Product Data | 1.0.0 | `.../WSDL/ProductDataService/1.0.0/` |
| Product Data | 2.0.0 | `.../WSDL/ProductDataService/2.0.0/` |
| Pricing | 1.0.0 | `.../WSDL/PricingAndConfiguration/1.0.0/` |
| Purchase Order | 1.0.0 | `.../WSDL/PO/1.0.0/` |

Inventory 1.2.1 declares `InventoryService/**1.0.0**` and changes the path
segment as well. Interpolating the version would break all 139 suppliers
running it, and would do so silently: the request would be well-formed and
the response would parse to nothing.

## Why hand-built XML and not a WSDL client

Requests are built as strings with the exact namespaces each schema
declares; responses are searched by **local name only**, ignoring namespace
URIs. Strict out, lenient in.

A WSDL client was considered and rejected. PromoStandards services are
almost all .NET-generated, and their published WSDLs frequently import
schemas over dead links, disagree with what the service actually accepts, or
ship as broken archives. A WSDL client also fetches and parses a remote
document at call time, which converts a supplier's slow or broken web server
into our outage. Hand-building costs a few lines per operation and makes the
bytes on the wire exactly what the adapter says — diffable in a fixture, and
immune to a supplier's broken WSDL. The same approach is already proven in
BaconCo's `utils/sanmar.py`.

## Known-flaky and structural issues

Established from the registry capture, the WSDL packages, and an
unauthenticated sample of live supplier endpoints. No authenticated call
has been made yet, so **operation-level** flakiness (timeouts, partial
data, rate limits) is still unknown — populate that from smoke-test runs as
suppliers are onboarded.

| Issue | Where | Impact |
| --- | --- | --- |
| TLS connection reset from unregistered IPs | SanMar | every endpoint resets the handshake ~6s in; SanMar requires the calling server's IP to be allowlisted, so the smoke test cannot run from an unregistered host regardless of credentials |
| Non-standard service namespace | 3M | serves Inventory 1.2.1 as `http://inventoryservice.promostandards.mmm/`; needs a `namespaces` override |
| Wrong WSDL served at registered URLs | company `114083` | its PPC and Product Data endpoints both return the *OrderStatus* WSDL; the registered URLs appear misconfigured |
| Endpoints on non-standard ports | 34 of 3617 URLs (0.9%) | ports 8080, 7443, 444, plain-HTTP 80; fine here but blocked by egress policies that permit only 443 |
| 18 companies error on their endpoints call | registry-wide | recorded in the dump's `errors` map; provisioning those codes fails until the registry recovers |
| Inventory 1.2.1 WSDL zip is malformed | spec package | `unzip` refuses it; use Python `zipfile` |
| Registered test host differs from documentation | SanMar | registry says `edev-ws.sanmar.com`; BaconCo's `utils/sanmar.py:31` hardcodes `test-ws.sanmar.com` |
| Two services carry an empty service code | Company Data, Remittance Advice | code-keyed lookups collide; both are skipped by capability introspection |
| `MED` 1.0.0 and `INV` 1.0.0 are Deprecated | registry | 6 and 12 suppliers respectively still publish them |
| Endpoint URLs are WSDL URLs | most suppliers | the registry's `url` usually ends `?WSDL`; posting SOAP to it works for the suppliers checked, but a supplier that rejects it needs the query stripped in config |
