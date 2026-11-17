# PromoStandards registry — Step 1 findings

Captured from the live WebServiceRepository on 2026-08-12 via
`scripts/ps_registry.py`. Raw dump: `assets/promostandards_endpoints.json`.

## Service codes (verified — supersedes prior assumptions)

18 entries at `/json/services`:

| Code | Service | Versions (status) |
| --- | --- | --- |
| `Product` | Product Data | 1.0.0, 2.0.0 |
| `MED` | Media Content | 1.0.0 *(Deprecated)*, 1.1.0 |
| `PPC` | Product Pricing and Configuration | 1.0.0 |
| `INV` | Inventory | 1.0.0 *(Deprecated)*, 1.2.1, 2.0.0 |
| `ODRSTAT` | Order Status | 1.0.0, 2.0.0 |
| `PO` | Purchase Order | 1.0.0 |
| `OSN` | Order Shipment Notification | 1.0.0, 2.0.0, 2.1.0 |
| `INVC` | Invoice | 1.0.0 |
| `PDC` | Product Compliance | 1.0.0 |
| *(empty)* | Company Data | 1.0.0 |
| *(empty)* | Remittance Advice | 1.0.0 |

Three corrections worth carrying forward:

- **Product Data's code is `Product`**, mixed-case — not `PROD`. The registry
  path `/companies/{code}/endpoints/types/{serviceTypeCode}` takes this string,
  so casing matters at the wire. This repo normalises to upper-case `PRODUCT`
  as the *internal* canonical key; the raw string stays in the dump.
- **`PDC` (Product Compliance)** exists and was previously unaccounted for.
- **Company Data and Remittance Advice have an empty-string `Code`.** Any
  code-keyed lookup needs a name fallback or it will collide these two.

## Adoption

1873 companies read (18 failed, recorded in the dump's `errors` map).
Of those: 1013 Supplier, ~660 Distributor, ~195 Service Provider.

Only **601 companies publish any endpoint at all** — 578 of them Suppliers,
plus 23 Distributors/Service Providers. Percentages against the full 1873
understate adoption by ~3x, so the meaningful denominator is 601.

| Service | Companies | % of 601 | Version split (endpoint count) |
| --- | ---: | ---: | --- |
| `PRODUCT` | 540 | 89.9% | 2.0.0: 502, 1.0.0: 494 |
| `MED` | 527 | 87.7% | 1.1.0: 521, 1.0.0: 6 |
| `PPC` | 513 | 85.4% | 1.0.0: 513 |
| `PO` | 468 | 77.9% | 1.0.0: 470 |
| `INV` | 201 | 33.4% | 2.0.0: 155, 1.2.1: 139, 1.0.0: 12 |
| `ODRSTAT` | 164 | 27.3% | 1.0.0: 156, 2.0.0: 29 |
| `OSN` | 146 | 24.3% | 1.0.0: 135, 2.0.0: 36, 2.1.0: 4 |
| `INVC` | 69 | 11.5% | 1.0.0: 69 |
| `PDC` | 9 | 1.5% | 1.0.0: 9 |

Endpoint counts can exceed company counts: a company may register the same
service at two versions (SanMar registers both INV 1.2.1 and 2.0.0), and a
few register the same service/version twice.

## What this implies for the design

**Adapter count is driven by two services, not all nine.** Most services are
single-version and need exactly one adapter each:

| Service | Adapters needed | Why |
| --- | --- | --- |
| `PPC`, `PO`, `INVC`, `PDC` | 1 each | only one version exists |
| `MED` | 1 (1.1.0) | 1.0.0 is Deprecated and has 6 users |
| `PRODUCT` | **2** | 502 / 494 — an even split, neither droppable |
| `INV` | **2** | 155 / 139 — likewise even; 1.0.0 (12, Deprecated) skippable |
| `ODRSTAT` | 2 | 1.0.0 dominates 156/29, but v2 is 18% of users |
| `OSN` | 2 | 1.0.0 dominates 135/36; 2.1.0 (4 users) not worth an adapter yet |

For the brief's priority set (INV, PRODUCT, PPC, PO) that is **six adapters**,
not four — Product Data and Inventory each need both versions on day one.
Shipping only the newest version of either strands roughly half the suppliers.

**`INV` adoption is 33%, well below PRODUCT/MED/PPC/PO (78–90%).** Inventory
is a reasonable first build for being self-contained, but it is not the
widest-reach service. PRODUCT + PPC + PO cover far more suppliers.

**Namespaces do not track service versions.** From the WSDLs:

| | INV 1.2.1 | INV 2.0.0 |
| --- | --- | --- |
| Target namespace | `.../WSDL/InventoryService/1.0.0/` | `.../WSDL/Inventory/2.0.0/` |
| Request root | `Request` | `GetInventoryLevelsRequest` |
| Product field | `productID` + required `productIDtype` | `productId`, optional `Filter` |
| Shared objects | inline, single namespace | separate `SharedObjects/` namespace |

Inventory **1.2.1 declares namespace `InventoryService/1.0.0`**. The namespace
must therefore be a constant owned by each adapter — never interpolated from
the configured `wsVersion`. Deriving it would silently break all 139 suppliers
on 1.2.1.

`password` is `minOccurs="0"` in both versions: optional per spec despite being
the auth mechanism. Treat it as optional-but-usually-required and let the
supplier's response say otherwise.

## Operational notes

- SanMar's registered test host is **`edev-ws.sanmar.com`**, not the
  `test-ws.sanmar.com` hardcoded in BaconCo's `utils/sanmar.py:31`. Reconcile
  before any PO work.
- The **INV 1.2.1 WSDL zip is malformed** — `unzip` rejects it as having
  overlapped components; Python's `zipfile` reads it fine. Any fixture-fetching
  script must not shell out to `unzip`.
- 18 companies return errors on their endpoints call. They are recorded rather
  than skipped so provisioning can distinguish "no endpoints" from "unreadable".
