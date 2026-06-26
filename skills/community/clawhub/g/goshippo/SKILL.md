---
name: goshippo
description: "(Beta) A shipping and logistics skill for Shippo. Get multi-carrier rates (USPS, UPS, FedEx, DHL, 30+), buy domestic and international labels with customs, validate addresses, track packages with webhooks, and run bulk CSV batches, plus cost analysis, integration routing, and SDK-upgrade help. Runs through Shippo's hosted MCP with per-user OAuth (sign in once, nothing to copy or store). Uses Shippo's discounted carrier rates."
version: 1.4.0
license: MIT
metadata:
  openclaw:
    emoji: "📦"
    homepage: https://github.com/goshippo/ai
---

# Shippo Shipping Skill

## Setup

**MCP server:** Shippo's hosted MCP at `https://mcp.shippo.com`, with per-user Shippo OAuth. You authorize once through Shippo on first use, with nothing to copy or configure, and the client refreshes the token automatically.

Point your MCP client at the hosted server:

```json
{
  "mcpServers": {
    "shippo": {
      "type": "http",
      "url": "https://mcp.shippo.com"
    }
  }
}
```

On first use, your client runs the Shippo OAuth sign-in (in OpenClaw, `openclaw mcp login shippo`; in Claude Code, `/mcp`). No local Node process and nothing to store.

**Prerequisites:** A Shippo account and at least one carrier account (Shippo provides managed accounts for USPS, UPS, FedEx, DHL Express by default). See `references/tool-reference.md` for the full tool catalog.

**Purchases are live:** label purchases charge the authorized Shippo account for real. Confirm carrier, service, and cost with the user before any purchase.

**Response envelope:** The MCP wraps most API responses in a Speakeasy envelope shaped like `{"ContentType": "application/json", "StatusCode": <code>, "RawResponse": {}, "<PayloadName>": {...actual response...}}`. The payload field is named after the response schema on success (e.g. `ParsedAddress`, `AddressPaginatedList`, `AddressValidationResultV2`, `AddressWithMetadataResponse`, `Shipment`, `CarrierAccountPaginatedList`) and after the HTTP status code on some errors (e.g. `fourHundredAndNineApplicationJsonObject` for a 409, the body may be `{}`). To extract the payload, find the field whose key is not `ContentType`, `StatusCode`, or `RawResponse`, and branch on `StatusCode` for success vs error.

**Non-envelope errors:** Some failures bypass the envelope entirely and surface as an MCP-level error instead, the tool response has `isError: true` with a single text block containing a plaintext message like `Unexpected API response status or content-type: Status 404 Content-Type application/json Body: {"detail":"Not found."}`. Argument-validation failures come back as JSON-RPC error code `-32602`. Handle both paths when reporting errors to the user.

---

## Best Practices

Latest Shippo API version: **2018-02-08**. Send via the `Shippo-API-Version` header.

### Using the Shippo MCP

The hosted Shippo MCP at `https://mcp.shippo.com` exposes exactly **4 tools** (a meta-API), not the underlying operations directly:

- `shippo_list_tools`: discover which operation you need.
- `shippo_describe_tool`: get that operation's input schema.
- `shippo_read_execute_tool`: run a read (lists, gets, lookups).
- `shippo_write_execute_tool`: run a write or mutation (creates, purchases, voids).

Every operation name in this skill (`ValidateAddress`, `CreateShipment`, `CreateTransaction`, `GetTrack`, etc.) is invoked **through** these wrappers, never called as a tool on its own. Standard discovery pattern: `shippo_list_tools` to find the operation, then `shippo_describe_tool` for its schema, then `shippo_read_execute_tool` or `shippo_write_execute_tool` to run it. The read/write split lets approval policies gate mutations separately. In the Claude apps these 4 tools may be deferred (loaded on demand), so an initial "tool has not been loaded yet" is normal: discover via the wrappers rather than guessing operation names.

### Integration routing

| Building…                                          | Recommended primitive          | See                                                                                        |
|----------------------------------------------------|--------------------------------|--------------------------------------------------------------------------------------------|
| Checkout flow with live shipping rates             | Rates at Checkout              | Rate Shopping (+ `shippo/references/rate-shopping-guide.md`)                               |
| Single label purchase                              | Shipments + Transactions       | Label Purchase                                                                              |
| Bulk label generation from CSV                     | Batches + Manifests            | Batch Shipping (+ `shippo/references/csv-format.md`)                                        |
| Track packages across carriers                     | Tracking + webhooks            | Tracking                                                                                    |
| Validate user addresses before save                | Addresses v2                   | Address Validation (+ `shippo/references/address-formats.md`)                               |
| Analyze shipping spend / optimize carriers         | Shipments + Transactions list  | Shipping Analysis                                                                           |
| International shipments                            | Customs Items + Declarations   | Label Purchase (+ `shippo/references/customs-guide.md` + `shippo/references/international-shipping.md`) |

Read the relevant skill or reference before answering integration questions or writing code.

### Critical rules

- **Always validate addresses before purchasing labels.** Most "no rates" / "label failed" errors trace back to unvalidated addresses.
- **Label purchases charge your live Shippo account for real.** Always confirm carrier, service, and cost with the user before any purchase.
- **Always confirm purchase before `CreateTransaction`.** Show carrier/service/cost/eta and require explicit user confirmation.
- **Parcel dimensions and weight must be strings, not numbers.** Use `"10"`, never `10`.
- **Label URLs are S3 signed URLs.** Always display the complete URL, truncating breaks the signature.
- **Rates expire after 7 days.** Re-create the shipment for fresh rates.

### Response handling

The MCP wraps responses in a Speakeasy envelope. Some failures bypass the envelope. See `shippo/references/response-envelope.md` and `shippo/references/error-reference.md` for parsing logic and error-handling patterns.

### Connecting

The hosted MCP at `https://mcp.shippo.com` uses per-user Shippo OAuth. You authorize once through Shippo (in Claude Code, run `/mcp` and sign in), and the session refreshes automatically. There is nothing to copy or configure. Once you are connected, the workflow guidance below is unchanged.

- **Two 401 strings to recognize:**
  - `"Token does not exist"`: the credential is invalid, revoked, or for a different account. Re-authorize the Shippo OAuth session.
  - `"Authentication credentials were not provided"`: no credential reached Shippo. The OAuth session is not authorized yet, or it has expired. Re-authorize the Shippo OAuth session.

### Purchases are live

Label and batch purchases charge the authorized Shippo account for real money. Before any `CreateTransaction` or `PurchaseBatch`, show the carrier, service level, cost, and ETA, and get explicit user confirmation. Do not proceed without it.

### Key documentation

- [API Concepts](https://docs.goshippo.com/docs/api_concepts/apiversioning): request shapes, versioning, auth
- [Address Validation Guide](https://docs.goshippo.com/docs/addresses/address_validation): validation depth varies by country
- [Customs Reference](https://docs.goshippo.com/docs/exporting/internationalshipments): incoterms, contents types, HS codes
- [Carrier Accounts](https://docs.goshippo.com/docs/shipping/carrieraccounts): managed vs custom accounts
- [Webhooks](https://docs.goshippo.com/docs/tracking/webhooks): event types, signature verification

(Once Mintlify migration completes, `.md` URL suffixes will provide raw markdown access for AI agents.)

---

## Address Validation

### Address Field Format

The Shippo API uses **v1 field names** for address components in most endpoints (including `CreateShipment`). Always use:

| Field | Description | Example |
|---|---|---|
| `name` | Full name | `Jane Smith` |
| `street1` | Street address line 1 | `731 Market St` |
| `street2` | Street address line 2 (optional) | `Suite 200` |
| `city` | City | `San Francisco` |
| `state` | State or province | `CA` |
| `zip` | Postal code | `94103` |
| `country` | ISO 3166-1 alpha-2 country code | `US` |
| `email` | Email (required for international senders) | `jane@example.com` |
| `phone` | Phone (required for international senders) | `+1-555-123-4567` |

Note: `CreateAddress` and `ValidateAddress` take the v2 field names (`address_line_1`, `city_locality`, `state_province`, `postal_code`), but when passing addresses inline to `CreateShipment`, you must use the v1 names above.

---

### Validate a Structured Address

1. Collect at minimum: `street1`, `city`, `state`, `zip`, `country` (ISO 3166-1 alpha-2).
2. Call `CreateAddress` with the address fields. This creates the address and returns an object ID.
3. Call `ValidateAddress` with the address fields to get validation results. Note: this endpoint takes address fields as query parameters, not an object ID.
4. Check `analysis.validation_result.value` in the response. Values: `"valid"`, `"invalid"`, or `"partially_valid"` (address found with corrections applied). Check `analysis.validation_result.reasons` for details.
5. Report the standardized address back. Highlight any corrected fields (listed in `changed_attributes`). Note `analysis.address_type` (`"residential"`, `"commercial"`, or `"unknown"`) -- residential classification affects carrier surcharges.
6. If invalid: relay the reason descriptions. If the API returns a `recommended_address`, present it to the user.
7. If `partially_valid`: show what was corrected and ask the user to confirm the corrections are acceptable.

---

### Parse a Freeform Address

1. Call `ParseAddress` with the raw string (e.g., "123 Main St, Springfield IL 62704").
2. Review the structured output for completeness. The parse response uses v2 field names: `address_line_1`, `city_locality`, `state_province`, `postal_code`.
3. Note: the parse response does not include `country`. You must ask the user for the country or infer it, then add it before proceeding.
4. Validate the parsed result by passing the fields to `CreateAddress` then `ValidateAddress` (follow the structured address workflow above from step 2).

---

### International Addresses

- Always require the `country` field. Do not guess.
- Pass non-Latin characters as-is; the API handles encoding.
- Validation depth varies by country. US, CA, GB, AU, and major EU countries have deep validation. Others may only confirm structural completeness. Inform the user of this limitation.

---

### Bulk Address Validation

There is no batch validation endpoint. Call `CreateAddress` per address. Track results (row number, valid/invalid, corrections, errors, residential classification) and report a summary when done. For 50+ addresses, set expectations about processing time and provide progress updates.

---

### Re-validate an Existing Address

Call `ValidateAddress` with the address fields. This endpoint validates by address fields, not by object ID.

---

### Duplicate Addresses

If `CreateAddress` returns a "Duplicate address" error, the address already exists in the account. Retrieve it via `ListAddresses` or proceed directly to validation.

---

### Quick Reference

**Validate an address:**
`CreateAddress` (saves address) + `ValidateAddress` (validates with same fields)

**Parse then validate:**
`ParseAddress` -> add country -> `CreateAddress` + `ValidateAddress`

---

## Rate Shopping

### Get Rates for a Shipment

1. Collect: origin address, destination address, parcel (length, width, height, distance_unit, weight, mass_unit). All dimension and weight values must be **strings** (e.g., `"10"` not `10`).
2. Optionally validate both addresses with `ValidateAddress` (see Address Validation).
3. Call `CreateShipment` with `address_from`, `address_to` (as inline address objects using v1 field names -- `street1`, `city`, `state`, `zip`, `country` -- not object IDs), and `parcels`.
4. The response `rates` array contains available options. Present a table: carrier, service level, price, estimated days.
5. Note: the same carrier may return duplicate rates from multiple carrier accounts. Present the best rate per carrier/service combination.
6. Each rate carries an `object_id`. To buy a label, pass the chosen rate's `object_id` to the purchase flow (see Label Purchase); you do not re-send the address or parcel.

---

### Rate Expiration

Rates expire after 7 days. If a user tries to purchase a rate that was retrieved more than 7 days ago, create a new shipment to get fresh rates.

---

### Filter by Speed

Map user requests: "overnight" = estimated_days 1, "2-day" = estimated_days <= 2, "within N days" = estimated_days <= N. Filter the rates array accordingly. If nothing matches, show the fastest available option.

---

### International Rates

Some carriers may return international rates without a customs declaration, but others will not. If no rates are returned, try attaching a customs declaration to the shipment. Some carriers also require a phone number on the destination address for international rate retrieval. Inform the user that customs will be required at label purchase time regardless. See `references/customs-guide.md` for customs details.

---

### Checkout Rates (Line Items)

Call `CreateLiveRate` instead of `CreateShipment`. Accepts `address_from`, `address_to`, and `line_items` (each with title, quantity, total_price, currency, weight, weight_unit).

---

### Rates in a Specific Currency

Call `ListShipmentRatesByCurrencyCode` with the preferred ISO currency code (USD, EUR, GBP, CAD, etc.).

---

### Recommendation

Identify the cheapest (lowest `amount`), fastest (lowest `estimated_days`), and best-value options from the rates array. These are not API fields -- compute them by sorting the rates array yourself. State the trade-off: "Option A is $X cheaper but takes Y more days than Option B."

---

### Troubleshooting: No Rates

- Verify both addresses passed validation (most common cause).
- Confirm parcel dimensions are reasonable (not zero, not exceeding carrier limits).
- Shippo provides managed carrier accounts by default for major carriers. If no rates are returned, the issue is more likely address validation, unsupported route, or parcel dimensions -- not missing carrier accounts. You can verify with `ListCarrierAccounts` if needed.
- Rates expire after 7 days. If stale, create a new shipment to get fresh rates.

---

### Quick Reference

**Get rates:**
(optional) `ValidateAddress` (x2) -> `CreateShipment` (with inline addresses) -> read `rates` array

---

## Label Purchase

### Purchases Are Live

Label purchases charge the authorized Shippo account for real. **Before purchasing, explicitly state "this will charge your Shippo account" with the carrier, service, and cost, and require the user to acknowledge.** Do not purchase without that confirmation.

---

### Purchase Confirmation Gate

Before every call to `CreateTransaction`, summarize the following and ask the user for explicit confirmation:
- Carrier and service level
- Estimated cost
- Estimated delivery time
- Origin and destination

**Do not proceed without explicit user confirmation.**

---

### Domestic Label

1. Optionally validate both addresses with `ValidateAddress` (see Address Validation).
2. Call `CreateShipment` with `address_from`, `address_to` (as inline address objects using v1 field names -- `street1`, `city`, `state`, `zip`, `country`), `parcels`, and `async: false`.
3. Present rates to the user. Let them choose.
4. **Confirm purchase** (see Purchase Confirmation Gate above).
5. Call `CreateTransaction` with: `rate` (selected rate object_id), `label_file_type` (default `PDF_4x6`), `async: false`.
6. Check response `status`:
   - `SUCCESS`: return `tracking_number`, `label_url` (display the COMPLETE URL -- S3 signed URLs break if truncated), and `tracking_url_provider`.
   - `QUEUED`/`WAITING`: poll `GetTransaction` until resolved.
   - `ERROR`: report messages from the `messages` array.

---

### International Label

All domestic steps apply, plus customs handling before shipment creation. See `references/customs-guide.md` for the full customs workflow.

1. Optionally validate addresses with `ValidateAddress`. Sender must include `email` and `phone`. Ask if missing.
2. Create customs items: call `CreateCustomsItem` per item (description, quantity, net_weight, mass_unit, value_amount, value_currency, origin_country, tariff_number). Alternatively, you can skip this step and pass inline item objects directly in the declaration (step 3).
3. Create the customs declaration: call `CreateCustomsDeclaration` with contents_type, non_delivery_option, certify: true, certify_signer, and the items (either object_ids from step 2, or inline item objects). See `references/customs-guide.md` for field details.
4. Call `CreateShipment` with all standard fields plus `customs_declaration` (the declaration object_id).
5. Present rates, **confirm purchase** (see Purchase Confirmation Gate), then purchase label and return results as in the domestic flow.

#### Contents Type Decision Tree

Use this to determine the correct `contents_type` value:

| Scenario | Value |
|---|---|
| Selling to the recipient (commercial sale) | `MERCHANDISE` |
| Sending a free gift | `GIFT` |
| Sending a product sample | `SAMPLE` |
| Paper documents only | `DOCUMENTS` |
| Customer returning a purchased item | `RETURN_MERCHANDISE` |
| Charitable donation | `HUMANITARIAN_DONATION` |
| None of the above | `OTHER` (requires `contents_explanation`) |

#### Incoterms Decision Logic

The `incoterm` field on the customs declaration controls who pays duties and taxes:

- **B2C / e-commerce (default):** Use `DDU` (Delivered Duty Unpaid) -- recipient pays duties at delivery.
- **Seller prepays duties:** Use `DDP` (Delivered Duty Paid) -- seller covers all duties and taxes.
- **FedEx/DHL only:** `FCA` (Free Carrier) is available for advanced trade scenarios.

If the user does not specify, default to `DDU` for standard e-commerce shipments.

---

### Return Labels

To generate a return label, swap `address_from` and `address_to` so the original recipient becomes the sender and the original sender becomes the recipient. All other steps (shipment creation, rate selection, label purchase) remain the same.

---

### Label Format Options

Default to `PDF_4x6` unless the user specifies otherwise. Supported formats: `PDF_4x6`, `PDF_4x8`, `PDF_A4`, `PDF_A5`, `PDF_A6`, `PDF`, `PDF_2.3x7.5`, `PNG`, `PNG_2.3x7.5`, `ZPLII`.

---

### Label Customization Options

When purchasing a label via `CreateTransaction`, the following options may be set on the shipment or rate:

- **Signature confirmation**: set `signature_confirmation` on the shipment's `extra` field. Values: `STANDARD`, `ADULT`, `CERTIFIED`, `INDIRECT`, `CARRIER_CONFIRMATION`.
- **Insurance**: set `insurance` on the shipment's `extra` field with `amount`, `currency`, and `provider`.
- **Saturday delivery**: set `saturday_delivery` to `true` in the shipment's `extra` field. Only supported by certain carriers and service levels.
- **Reference fields**: pass `metadata` on the transaction for order numbers or internal references.

---

### Label from Existing Rate

If the user already has a rate object_id: optionally call `GetRate` to confirm details, then **confirm purchase** (see Purchase Confirmation Gate), then call `CreateTransaction` directly.

---

### Voiding a Label

Call `CreateRefund` with the transaction object_id.

**Refund limitations:** Void/refund eligibility depends on carrier and timing. Not all labels can be refunded after purchase. If `CreateRefund` fails, advise the user to contact Shippo support.

---

### Quick Reference

**Domestic label:**
(optional) `ValidateAddress` (x2) -> `CreateShipment` (with inline addresses) -> user picks rate -> confirm -> `CreateTransaction`

**International label:**
(optional) `ValidateAddress` (x2) -> `CreateCustomsItem` (per item) -> `CreateCustomsDeclaration` -> `CreateShipment` (with inline addresses + customs_declaration) -> user picks rate -> confirm -> `CreateTransaction`

**Return label:**
Same as domestic/international, but swap `address_from` and `address_to`.

**Order-to-label:**
`CreateOrder` -> `CreateShipment` (using order address/item data) -> user picks rate -> confirm -> `CreateTransaction` -> packing slip (REST fallback, see below)

---

### Orders and Packing Slips

Use orders to represent e-commerce fulfillment requests. An order captures the shipping address, line items, and totals -- then feeds into the standard label purchase workflow.

#### Tools

- **`CreateOrder`**: Create an order with line items, shipping address, and order details.
- **`GetOrder`**: Retrieve an order by its object_id.
- **`ListOrders`**: List all orders.
- **Packing slip (known gap):** Generate a packing slip PDF for an order. There is no packing-slip tool in the MCP catalog. The underlying REST endpoint exists at `GET /orders/{ORDER_ID}/packingslip/` (returns a 24-hour S3 PDF link). Fall back to a direct REST call, or advise the user to use the Shippo dashboard until the MCP gap is closed.

#### Workflow

1. Call `CreateOrder` with the shipping address, line items (title, quantity, sku, total_price, etc.), and order-level fields.
2. Use the order's address and item data to call `CreateShipment`, then follow the standard label purchase flow (rate selection, confirmation, `CreateTransaction`).
3. After purchasing the label, generate a packing slip via the REST fallback (see Tools above for the known MCP gap).

---

## Tracking

### Track by Number

1. Determine carrier and tracking number. Carrier must be a lowercase Shippo token (e.g., `usps`, `ups`, `fedex`, `dhl_express`). See `references/carrier-guide.md` for tracking number format hints per carrier. If uncertain, ask the user.
2. Call `GetTrack` with `carrier` and `tracking_number`.
3. Key response fields: `tracking_status` (status, status_details, status_date, location), `tracking_history`, `eta`.
4. Each tracking event includes a `substatus` object with `code`, `text`, and `action_required` (boolean). Include substatus details when presenting tracking history -- these provide more specific information about what happened at each step.
5. Present: current status, location, ETA, substatus details, and chronological event history (most recent first).

---

### Status Values

See `references/carrier-guide.md` for carrier-specific status nuances. Standard values:

| Status | Meaning |
|---|---|
| PRE_TRANSIT | Label created, carrier has not received the package |
| TRANSIT | Package is in transit |
| DELIVERED | Delivered |
| RETURNED | Being returned or returned to sender |
| FAILURE | Delivery failed |
| UNKNOWN | No tracking information from carrier |

The `eta` field is provided by most major carriers (USPS, UPS, FedEx, DHL Express) but availability is carrier-dependent, it may be `null` for regional carriers or for shipments before the carrier has finalized routing. Treat absence as informational, not as an error condition.

---

### Find Trackable Packages

Call `ListTransactions`. Filter for `object_status: SUCCESS`. Each successful transaction has `tracking_number` and carrier info. Then call `GetTrack` for selected items.

---

### Register a Tracking Webhook

1. Get the user's HTTPS webhook URL.
2. Call `createWebhook` with `url` and `event: track_updated`.
3. Optionally call `CreateTrack` with carrier and tracking number to register a specific shipment for push updates.

---

### Quick Reference

**Track a package:**
`GetTrack` with carrier + tracking number

**Find past shipment tracking:**
`ListTransactions` -> filter SUCCESS -> `GetTrack`

---

## Batch Shipping

### Purchases Are Live

Batch purchases charge the authorized Shippo account for real. Before `PurchaseBatch`, show the shipment count, carrier/service, and estimated total cost, and require explicit user confirmation.

---

### Purchase Confirmation Gate

Before every call to `PurchaseBatch`, summarize the following and ask the user for explicit confirmation:
- Total number of shipments to be purchased
- Carrier and service level (or selection rule if varied)
- Estimated total cost
- Number of domestic vs international shipments

**Do not proceed without explicit user confirmation.**

---

### CSV Batch Processing

See `references/csv-format.md` for the column specification.

1. Read and parse the CSV. Validate required columns are present. Report row count.
2. Validate each row for non-empty required fields. Report invalid rows with reasons.
3. Detect international rows (sender_country != recipient_country). Create customs declarations for those rows. See `references/customs-guide.md`. Use correct customs enum values: `RETURN_MERCHANDISE` (not `RETURN`) for returned goods, `HUMANITARIAN_DONATION` (not `HUMANITARIAN`) for charitable donations.
4. Build the `batch_shipments` array with inline address and parcel objects per row.
5. Call `CreateBatch` with the array.
6. Poll `GetBatch` until status changes from `VALIDATING` to `VALID`. See Polling Intervals below.
7. Review per-shipment validation results. Report failures before proceeding.
8. **Confirm purchase** (see Purchase Confirmation Gate above).
9. Call `PurchaseBatch` to buy labels for all valid shipments.
10. Poll `GetBatch` until status changes from `PURCHASING` to `PURCHASED`. See Polling Intervals below.
11. Report: total attempted, succeeded, failed. For successes: tracking_number and label_url (complete URL). For failures: error messages.

#### Batch Size Guidance

For batches over 500 shipments, consider splitting into multiple batches. Large batches take longer to validate and purchase, and a single failure can be harder to diagnose.

---

### Polling Intervals

- For batches under 100 shipments: poll every 3-5 seconds.
- For batches with 100+ shipments: poll every 5-10 seconds.
- Report progress to the user every 30 seconds.
- Stop after 60 retries and suggest the user check back later using `GetBatch` with the batch object_id.

---

### Batch with Rate Shopping

1. Call `CreateShipment` per shipment to get rate quotes (see Rate Shopping).
2. Present rates. User picks a service level rule (e.g., "cheapest for each" or a specific carrier/service).
3. Build `batch_shipments` with `servicelevel_token` per item.
4. Create, validate, **confirm purchase**, purchase, report as above.

---

### Managing an Existing Batch

- Add shipments: `AddShipmentsToBatch` (before purchase only). Note: adding an invalid shipment will change the entire batch status to `INVALID`. Check per-shipment statuses after adding.
- Remove shipments: `RemoveShipmentsFromBatch` (before purchase only).

---

### End-of-Day Manifest

1. Collect: `carrier_account` (object_id), `shipment_date` (YYYY-MM-DD, default today), `address_from` (pickup address).
2. Optionally collect specific transaction object_ids to scope the manifest. You must pass specific transaction object_ids -- there is no auto-include for a date range.
3. Call `CreateManifest`.
4. Poll `GetManifest` until status is `SUCCESS` or `ERROR`.
5. Return the manifest PDF URL(s) and shipment count.

---

### Quick Reference

**CSV batch:**
Parse CSV -> `CreateCustomsDeclaration` (international rows) -> `CreateBatch` -> poll `GetBatch` -> confirm -> `PurchaseBatch` -> poll `GetBatch`

**Manifest:**
`CreateManifest` (with transaction object_ids) -> poll `GetManifest`

---

## Shipping Analysis

### Geographic Cost Analysis

1. Confirm origin address, destination list (or use representative cities), and parcel details.
2. Call `ListCarrierAccounts` to see configured carriers.
3. Call `CreateShipment` per destination to collect rates. Creating shipments is free; only `CreateTransaction` costs money.
4. Write results to `analysis/` directory (markdown report + CSV). Columns: Route, Destination, Carrier, Service, Cost, Currency, EstimatedDays, Zone.

---

### Package Optimization

1. Confirm the route.
2. Define dimension profiles to test (or use user-provided ones).
3. Check `ListCarrierParcelTemplates` and `ListUserParcelTemplates` for flat-rate and saved templates. See `references/rate-shopping-guide.md` for dimensional weight and flat-rate guidance.
4. Call `CreateShipment` per profile on the same route.
5. Compare: cheapest rate, carrier options, fastest option per profile. Note where flat-rate templates beat custom dimensions and where dimensional weight causes price jumps. See `references/carrier-guide.md` for carrier-specific weight limits and surcharges.

---

### Carrier Comparison

1. Call `CreateShipment` for the route.
2. Group the `rates` array by `provider`.
3. Per carrier: cheapest service, fastest service, number of service levels, price range.

---

### Historical Cost Optimization

1. Call `ListShipments` and `ListTransactions` to get past activity.
2. Cross-reference: what the user paid vs. what alternatives were available.
3. Identify patterns: carrier concentration, service-level mismatch, consistent overpayment.
4. For a sample of shipments with tracking numbers, call `GetTrack` to check actual vs. estimated delivery times.
5. If fewer than 5 successful transactions exist (not just shipments -- shipments are rate quotes, transactions represent actual spend), redirect to forward-looking analysis.

---

### Output Conventions

Write reports to the `analysis/` directory. Create it if it does not exist. Include both markdown and CSV. CSV must have a header row. Markdown must include a timestamp and input parameters.

---

### Quick Reference

**Cost analysis:**
`ListCarrierAccounts` -> `CreateShipment` (per destination) -> read `rates` arrays -> write report

**Carrier comparison:**
`CreateShipment` -> group `rates` by `provider` -> summarize

**Historical review:**
`ListShipments` + `ListTransactions` -> cross-reference -> `GetTrack` (sample) -> write report

---

## Upgrades

The Shippo MCP is hosted at `https://mcp.shippo.com`. It is OAuth-only and auto-updates server-side, so there is nothing to install or upgrade on your side. This skill covers what stays your responsibility: API version awareness, webhook payload versioning, and troubleshooting the hosted session.

### API version handling

The current Shippo API version is **2018-02-08**. Shippo uses a single long-lived API version, and the hosted server manages it for you server-side. You do not set the `Shippo-API-Version` header yourself when going through the hosted MCP.

What backward-compatibility means in practice:

- Most changes are backward-compatible: new optional fields, new resources, additional webhook events. Existing calls keep working.
- Breaking changes are rare and announced via release notes.
- Because the server picks the version, you don't pin anything client-side. Your job is to handle new fields gracefully (see webhook versioning below) rather than to manage versions.

Shippo API changes are tracked in [the API changelog](https://docs.goshippo.com/changelog). As of 2026-06, no recent breaking changes affect the workflows covered by this skill set.

### Webhook event versioning

Webhook events can include new fields without bumping the API version. To handle them gracefully:

- Default to ignoring unknown fields in your webhook handler, never fail-closed on a field you don't recognize.
- Subscribe only to the specific event types you need (`track_updated`, `transaction_created`, `transaction_updated`, etc.).
- Verify webhook signatures using the `Shippo-Signature` header per [webhook docs](https://docs.goshippo.com/docs/tracking/webhooks).

### Troubleshooting the hosted MCP

#### `401` or `403` errors

The OAuth session has expired or is not authorized. Re-authorize the Shippo OAuth session: in Claude Code, run `/mcp` and sign in again.

#### Tools changed or missing after a server update

The hosted server auto-updates, so the tool catalog can shift without any action on your side. Re-list the current tools via `shippo_list_tools` to see what is available now.

#### "Not found" errors for objects you expect to exist

Most likely the object does not exist on the authorized account, or it belongs to a different account. Confirm you are signed in to the account that owns the object (re-authorize via `/mcp` if needed).

### Auditing an existing integration

Before making a change to a production integration:

1. Don't pin anything client-side. The hosted server manages the API version, so there's nothing to pin.
2. Verify webhook handlers ignore unknown fields.
3. Review the [API changelog](https://docs.goshippo.com/changelog) for any breaking changes.
4. Re-list tools via `shippo_list_tools` after an update to catch renamed or added operations.

---

## Support Ticket Builder

Turn a single shipment identifier into a complete, **classified**, well-structured
support package for the Shippo support team. The agent classifies the issue,
gathers every relevant fact from the Shippo MCP (running issue-type-specific
lookups, not just the lost-package set), computes the triage timeline, and emits
two things:

1. A **human copy-paste block** for the ticket body.
2. A **structured JSON block** tagged with a routing queue, so the ticket can be
   piped into the ticketing system and land in the right pipeline without a
   human re-classifying it.

This dual output is the point: completeness *and* correct routing are what kill
the back-and-forth.

Audience: Shippo support agents. Output uses Shippo terminology, object IDs, and
an internal routing tag. It is not customer-facing copy.

### When to use

Use this skill when someone wants to escalate or document a shipping problem and
asks for a support ticket / message to Shippo support, e.g. "package is stuck,"
"label was charged but never shipped," "why was I charged more than the rate I
saw," "refund this label I never used," "where is this delivery," "the address
looks wrong," "tracking updates aren't coming through," "can't get rates from
this carrier." It produces **text + JSON to copy and paste**; it does not open a
Jira ticket or send Slack/email itself.

### Step 1: Classify the issue (do this first)

Pick exactly one **canonical issue type** from the customer's description. The
issue type drives both the routing tag and which extra lookups you run in Step 4.
If the wording is ambiguous, ask one clarifying question before building.

| Issue type (canonical) | Triggers / signals | Routing tag |
|---|---|---|
| `lost_or_delayed` | stuck, late, no movement, "where is my package", lost | `queue:tracking-ops` |
| `unused_label_refund` | "never shipped", "refund this label", bought-but-unused | `queue:billing-refunds` |
| `billing_adjustment` | "charged more than the rate", surcharge, reweigh, dim-weight, address-correction fee | `queue:billing-adjustments` |
| `address_exception` | undeliverable, returned to sender, bad/invalid address, address correction | `queue:address-exceptions` |
| `customs_international` | customs hold, duties/taxes, missing HS code, commercial invoice, international | `queue:customs-intl` |
| `carrier_account` | "can't get rates from <carrier>", connection failed, registration pending | `queue:carrier-onboarding` |
| `tracking_webhook` | "tracking updates aren't coming through", webhook not firing | `queue:integrations` |
| `other` | anything that doesn't fit above | `queue:general-triage` |

> The routing tags above are **placeholders for Shippo's real support queue
> names**. Confirm the actual queue/label taxonomy and update this table once.
> The skill's value is producing a consistent, machine-parseable tag; the exact
> strings should match your ticketing system.

### Inputs accepted

The user may start from any **one** of these. Ask which one they have if it is
ambiguous; do not guess an ID type.

| Input | What it anchors |
|---|---|
| **Tracking number + carrier** | Drives `GetTrack` directly. Best for delivery/lost-package issues. |
| **Transaction (label) object ID** | Cleanest anchor: label creation time + tracking number + the rate/shipment link, all derivable. |
| **Shipment object ID** | Gives from/to addresses, requested `shipment_date`, and rates; tracking number comes from the purchased transaction. |

> **Resolving a tracking number to its label.** First detect the carrier and map
> it to the Shippo carrier *token* (see the note below), then call `GetTrack`.
> When the label was purchased through Shippo, the `GetTrack` response carries the
> transaction `object_id`; use that with `GetTransaction` to pull the label and
> billing facts. If the label was not bought through Shippo (no transaction comes
> back), there is nothing to resolve: build the ticket from `GetTrack` plus
> whatever the user supplied and mark the label fields "Not available."
> `ListTransactions` has no server-side `tracking_number` filter, so paging it to
> match by hand is a rarely-useful last resort, not the primary path.

> **Carrier token:** `GetTrack` expects a Shippo carrier *token*, not a display
> name, e.g. `usps`, `ups`, `fedex`, `dhl_express`, `dhl_ecommerce`,
> `canada_post`. If you only have a display name (often from a rate's
> `provider`), map it to the token. If unsure, ask the user for the carrier.

### Shippo MCP tools used

Discover/confirm with `shippo_list_tools` and `shippo_describe_tool`; execute
read-only lookups with `shippo_read_execute_tool`. **Everything this skill needs
is a `read` operation; never call a `write` tool (e.g. `CreateRefund`) from
this skill; the ticket only documents and recommends.**

Core reads (all issue types):

- `GetTransaction`: label creation time (`object_created`), `tracking_number`, `status`, `rate` reference, `eta`, `metadata` (order/internal reference)
- `GetShipment`: `address_from`, `address_to`, requested `shipment_date`, `parcels`, `rates`, `customs_declaration`, `extra` (added services + references), `messages`
- `GetTrack`: current `tracking_status`, full `tracking_history[]`, `eta`, and (for Shippo-purchased labels) the `transaction` object reference

Issue-type-specific reads (Step 4):

- `GetRate`: purchased `amount`, `currency`, `provider`, `servicelevel`, `estimated_days` (billing)
- `GetParcel`: declared `length/width/height`, `distance_unit`, `weight`, `mass_unit` (billing)
- `ListRefunds` / `GetRefund`: existing refund object + `status` (refund)
- `ValidateAddress` / `ValidateAddressByID`: `is_valid`, `messages`, residential flag (address)
- `GetCustomsDeclaration` / `GetCustomsItem`: `contents_type`, `incoterm`, `eel_pfc`, per-item `tariff_number` (HS code), `value_amount`, `origin_country` (customs)
- `ListCarrierAccounts` / `GetCarrierAccount` / `GetCarrierRegistrationStatus`: `active`, registration status (carrier-account)
- `listWebhooks` / `getWebhook`: `url`, `event`, `active` (webhook)

### Step 2: Resolve the anchor object

Always work toward having the four core objects: **transaction**, **shipment**,
**addresses**, and **tracking**. Stop early only when the issue genuinely needs
nothing more (e.g. a pure tracking-status question with no label on file).

- **Transaction ID** → `GetTransaction`. Read `object_created` (label creation
  time), `tracking_number`, `tracking_url_provider`, `status`, and the `rate`
  reference. Inspect for a `shipment` reference to get the shipment ID.
- **Shipment ID** → `GetShipment`. Read `address_from`, `address_to`,
  `shipment_date` (the **requested** ship date), `parcels`, `rates`,
  `customs_declaration`. Find the purchased rate/transaction for the tracking #.
- **Tracking number + carrier** → map the carrier to its token and call
  `GetTrack`. For a Shippo-purchased label the response carries the transaction
  `object_id`; follow it with `GetTransaction` to get the billing/label facts.

### Step 3: Pull the core facts

Pull the shipment (`GetShipment`) for `address_from`, `address_to`,
`shipment_date` if not already loaded, and tracking (`GetTrack` with carrier
token + tracking number) for `tracking_status`, `tracking_history[]`, and `eta`.

> From each address object capture only its `object_id` and coarse geography
> (`city`, `state`, `zip`, `country`) for the ticket, **not** `name`,
> `street1`, or `street2` (see PII minimization in guardrails).

- **First carrier scan** = the earliest `tracking_history` event representing
  physical acceptance by the carrier (the first `TRANSIT`/`DELIVERED`-class scan,
  or the carrier's "accepted/picked up" event). Pre-transit / "label created" /
  "shipment info received" pseudo-events do **not** count; call those out
  separately if present.
- **Added services and order reference (capture them):** surface the shipment's
  `extra` block (added services such as `signature_confirmation`, `insurance`,
  Saturday delivery, QR-code labels) and the customer's own order / internal
  reference number. That reference can live in two places depending on the
  integration: the transaction's `metadata` field (the documented home for order
  numbers) and/or the shipment `extra` reference fields. Capture it from wherever
  it actually appears, so the agent can tie the ticket back to the order without
  searching on an order number. The `extra` schema is nuanced and
  carrier/service-dependent, so **read the actual response fields rather than
  assuming names**: the `label-purchase` skill documents the common added-service
  options (signature, insurance, Saturday delivery) and
  `shippo/references/carrier-guide.md` covers per-carrier availability. Surface
  only what is actually present; omit the rest.
- **`messages` noise:** a shipment's `messages` array often carries routine
  "carrier doesn't support option" / "out of service area" entries. These are
  informational. Only surface messages tied to a carrier that actually appears
  in `rates`.
- **Read the actual response fields:** do not assume names. If a field is
  absent, record "Not available" rather than inventing a value.

### Step 4: Run the issue-type branch

After the core facts, run **only** the lookups for the classified issue type and
fill the matching section of the output. Skip branches that don't apply.

- **`lost_or_delayed`**: no extra reads; the core timeline carries it. Emphasize
  "last scan → now" and "overdue vs ETA."
- **`unused_label_refund`**: Was the label ever scanned? Re-check `GetTrack`: if
  there is a real carrier scan, the label is **used** (not eligible as an unused
  refund). Say so. Compute **label age** from `object_created` to now. Call
  `ListRefunds` (and `GetRefund`) to report any existing refund object + its
  `status`. Do **not** assert a specific eligibility window from memory; state
  the facts (used/unused, age, existing refund) and let the queue apply policy.
- **`billing_adjustment`**: `GetRate` for the purchased `amount`/`currency`;
  `GetParcel` (or shipment `parcels`) for **declared** dims/weight; compare the
  transaction's charged amount to the quoted rate. Flag the likely cause:
  dimensional-weight reweigh (declared vs billed dims), address-correction
  surcharge, or service upgrade. Report declared-vs-billed as the core evidence.
  Note: the reweigh/adjustment amount and the carrier's *billed* dims may not be
  exposed by these read ops; if so, record "Not available" rather than inferring.
- **`address_exception`**: run `ValidateAddress`/`ValidateAddressByID` on
  `address_to`; report `is_valid`, any validation `messages`, and the
  residential/commercial flag. Note whether validation was bypassed at purchase.
- **`customs_international`**: pull `GetCustomsDeclaration` + each
  `GetCustomsItem`. Check completeness: `contents_type`, `incoterm`,
  `eel_pfc`/AES exemption, and per item a `tariff_number` (HS code),
  `value_amount`, and `origin_country`. Flag missing HS codes / values, the
  usual cause of customs holds.
- **`carrier_account`**: `ListCarrierAccounts`, then `GetCarrierAccount` /
  `GetCarrierRegistrationStatus` for the relevant carrier. Report `active` and
  registration status; an incomplete registration is the usual "no rates" cause.
- **`tracking_webhook`**: `listWebhooks` + `getWebhook`. Report whether an
  `active` webhook exists for the relevant `track_updated`/tracking event and the
  configured `url`.

### Timeline to compute

These derived metrics pre-diagnose the issue so support doesn't have to:

- **Label created → first carrier scan**: how long the label sat before entering
  the network. A large gap is the classic "bought but never shipped" signature.
- **Requested `shipment_date` → first carrier scan**: picked up on/near intent?
- **First scan → last scan**: total time in transit so far.
- **Last scan → now**: days of silence; a long gap signals a stalled/lost parcel.
- **ETA vs. now**: is it overdue?

State each as an absolute date/time **and** a duration (e.g. "Label created
2026-06-01 14:02 UTC; first scan 2026-06-05 09:11 UTC, a 3d 19h gap"). Use UTC
and label it. In the JSON block, also emit each gap in whole hours.

### Output

Emit **both** blocks below, each as its own fenced block. Replace every `<...>`
placeholder; use "Not available" for anything you could not retrieve; never
invent values.

**Provenance (required).** Both blocks carry a generation stamp so support can
tell at a glance that the ticket was machine-assembled, and so ticket quality
can be tracked over time. Stamp:

- the **skill name** (`shippo-support-ticket`),
- the **source** (`Shippo MCP`),
- the **generation time in UTC** (ISO 8601).

Never alter or omit the stamp, and never present an auto-generated ticket as if
it were hand-written.

After the blocks, add a short plain-language **triage summary**
(1-3 sentences) naming the most likely problem based on the classification +
timeline, and list any data you could not retrieve.

#### Block A: Human ticket (copy-paste)

```
Subject: [<issue_type>] <one-line summary>, tracking <tracking_number>

ROUTING
  Issue type:      <canonical issue type>
  Routing tag:     <queue:...>
  Confidence:      <high | medium | low; note if classified from sparse info>

ISSUE
  Reported by:     <customer name / email, if known>
  Summary:         <2-3 sentence description in plain language>

SHIPMENT
  Shipment ID:     <shipment object_id>
  Transaction ID:  <transaction object_id>
  Carrier:         <carrier display name> (<carrier token>)
  Service level:   <servicelevel name>
  Tracking #:      <tracking_number>
  Tracking URL:    <tracking_url_provider>
  Parcel:          <declared dimensions + weight, if available>
  References:      <order/internal ref from transaction metadata or shipment extra, else "none">
  Added services:  <signature / insurance / QR code / etc. from extra, else "none">

ADDRESSES (no street-level PII; run GetAddress on an ID for full details)
  From address ID: <address_from object_id>
  From region:     <city> <state> <zip> <country>
  To address ID:   <address_to object_id>
  To region:       <city> <state> <zip> <country>

TIMELINE (all times UTC)
  Label created:           <object_created>
  Requested ship date:     <shipment_date>
  First carrier scan:      <status_date> @ <location>   (<status>)
  Last/most recent scan:   <status_date> @ <location>   (<status>)
  Current status:          <tracking_status>
  Carrier ETA:             <eta or "Not available">

  Label created → first scan:     <duration, e.g. 3d 19h>
  Requested ship → first scan:    <duration or note>
  First scan → last scan:         <duration>
  Last scan → now:                <duration>
  Overdue vs ETA:                 <yes/no + by how much>

ISSUE-SPECIFIC FINDINGS
  <Only the block for the classified issue type; examples:>
  [unused_label_refund]  Label used (scanned)? <yes/no>; Label age: <duration>;
                         Existing refund: <refund object_id + status or "none">
  [billing_adjustment]   Quoted rate: <amount> <ccy>; Charged: <amount> <ccy>;
                         Declared dims/wt: <...>; Likely cause: <reweigh/surcharge>
  [address_exception]    Address valid: <yes/no>; Validation messages: <...>;
                         Residential: <yes/no/unknown>
  [customs_international] Contents type: <...>; Incoterm: <...>;
                         Items missing HS code/value: <list or "none">
  [carrier_account]      Carrier: <...>; Active: <yes/no>; Registration: <status>
  [tracking_webhook]     Active webhook for tracking events: <yes/no>; URL: <...>

TRACKING HISTORY (most recent first)
  <status_date>  <status>  <location>  <substatus/text>
  <... one line per scan ...>

WHAT WE NEED FROM SUPPORT
  <the specific ask: locate package / refund label / explain charge / fix
   address / clear customs / complete carrier registration / fix webhook>

(Auto-generated by the "shippo-support-ticket" skill via the Shippo MCP on
  <generation time UTC>. Facts collected automatically; verify before acting.)
```

#### Block B: Structured JSON (for the pipeline)

```json
{
  "issue_type": "<canonical issue type>",
  "routing_tag": "<queue:...>",
  "classification_confidence": "<high|medium|low>",
  "reported_by": "<email or name or null>",
  "summary": "<one-line summary>",
  "identifiers": {
    "transaction_id": "<or null>",
    "shipment_id": "<or null>",
    "tracking_number": "<or null>",
    "carrier_token": "<or null>",
    "service_level": "<or null>",
    "order_reference": "<order/internal ref from transaction metadata or shipment extra, or null>"
  },
  "shipment_extra": {
    "<only the added-service `extra` fields actually present; e.g. signature_confirmation, insurance, qr_code>": ""
  },
  "addresses": {
    "from": { "address_id": "<or null>", "city": "", "state": "", "zip": "", "country": "" },
    "to":   { "address_id": "<or null>", "city": "", "state": "", "zip": "", "country": "" }
  },
  "timeline_utc": {
    "label_created": "<ISO8601 or null>",
    "requested_ship_date": "<ISO8601 or null>",
    "first_carrier_scan": "<ISO8601 or null>",
    "last_scan": "<ISO8601 or null>",
    "carrier_eta": "<ISO8601 or null>",
    "current_status": "<or null>"
  },
  "gaps_hours": {
    "label_to_first_scan": "<int or null>",
    "requested_ship_to_first_scan": "<int or null>",
    "first_to_last_scan": "<int or null>",
    "last_scan_to_now": "<int or null>",
    "overdue_vs_eta": "<int or null>"
  },
  "issue_findings": {
    "<keys depend on issue_type; e.g. label_used, label_age_hours, existing_refund_status, quoted_amount, charged_amount, declared_dims, address_is_valid, items_missing_hs_code, carrier_active, registration_status, webhook_active>": ""
  },
  "requested_action": "<the specific ask>",
  "data_gaps": ["<fields that could not be retrieved>"],
  "generated_by": {
    "skill": "shippo-support-ticket",
    "source": "shippo-mcp",
    "generated_at": "<ISO8601 UTC>"
  }
}
```

### Edge cases & guardrails

- **Read-only:** This skill never calls `write` operations. Recommend a refund;
  don't issue one.
- **Multiple matches** when paging `ListTransactions` as a fallback: list the
  candidates and ask the user to pick before building the ticket.
- **Stale objects:** objects older than 390 days aren't returned. If lookups fail
  for that reason, note it and build from whatever the user provided plus tracking.
- **Classification confidence:** if you classified from sparse wording, set
  confidence `low` and say why, so the queue knows to sanity-check the tag.
- **PII minimization (required):** Do **not** put recipient/sender **names** or
  **street lines** (`street1`/`street2`) in the ticket, not in the human block
  and not in the JSON. Reference the `address_from` / `address_to` `object_id`s
  instead; support can run `GetAddress` on an ID to retrieve full details and
  replicate the issue only when they actually need to. Coarse geography
  (city, state/province, ZIP/postal, country) **is** retained, since support
  needs it for zone/routing triage. Tracking-history `location` values
  (typically city/state) are fine. Don't pull in unrelated shipments, and don't
  include API tokens or raw object dumps beyond what the templates ask for.
- **Never invent** timestamps, statuses, addresses, IDs, or HS codes. Missing →
  "Not available" (human block) / `null` (JSON).

---

## Error Handling

- **Never guess** parcel dimensions, weight, customs values, HS codes, or signer names. Ask the user.
- **Do not auto-retry** transport, auth, or rate-limit errors. Report to user and stop.
- Parcel dimensions and weight must be **strings** (e.g., `"10"` not `10`).
- Label URLs are S3 signed URLs. **Always display the complete URL** -- truncating breaks the signature.
- Rates expire after 7 days. Create a new shipment for fresh rates.
- No rates? Validate addresses first, then check dimensions, then `carrier-accounts-list`.
- "Not found" errors: verify the authorized account's mode matches the data -- test and live have separate object IDs.

---

## Data Handling

- **Hosted MCP:** requests go to Shippo's hosted MCP at `https://mcp.shippo.com`, authenticated by your per-user Shippo OAuth token. The server forwards each call to `api.goshippo.com` on your behalf. Nothing runs or is stored locally.
- No data is stored by the skill itself; all persistence is handled by Shippo's API.
- Label and tracking data are subject to Shippo's data retention policies.
