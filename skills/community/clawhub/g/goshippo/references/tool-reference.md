<!--
  ⚠️  DO NOT EDIT, auto-generated from skills/shippo/references/tool-reference.md by scripts/build-clawhub-bundle.js
  Edits here will be overwritten on the next sync.
  To change this content, edit the canonical source and re-run the sync script.
-->

# Shippo MCP Tool Reference

Complete list of MCP tools provided by the Shippo server, grouped by category. Includes required/optional parameters, data types, and async behavior.

**Data type note:** Dimensions (length, width, height) and weight values must be passed as **strings**, not numbers (e.g., `"12"` not `12`). This applies to parcels, customs items, and all weight/dimension fields.

---

## Addresses

### `CreateAddress` (preferred)
Create and validate a new address using v2 field names. Returns validation results.
- **Required:** `name` (string), `address_line_1` (string), `city_locality` (string), `country_code` (string, ISO 3166-1 alpha-2)
- **Optional:** `address_line_2` (string), `address_line_3` (string), `state_province` (string), `postal_code` (string), `phone` (string), `email` (string), `company` (string), `is_residential` (boolean)

### `ValidateAddress`
Validate an existing address by object ID using v2 field names.
- **Required:** `address_id` (string)

### `ParseAddress`
Parse a freeform address string into structured components. Returns v2 field names (no country).
- **Required:** `address_string` (string, freeform address text)

### `ValidateAddressByID` (legacy)
Validate an existing address by object ID using v1 field names.
- **Required:** `address_id` (string)

### `GetAddress`
Retrieve a previously created address by ID.
- **Required:** `address_id` (string)

### `ListAddresses`
List all stored addresses. Supports pagination.
- **Optional:** `page` (integer), `results` (integer, page size)

---

## Shipments

### `CreateShipment`
Create a new shipment and retrieve available rates. **Async:** if `async` is true (default), returns immediately and rates must be polled via `GetShipment` or `ListShipmentRates`.
- **Required:** `address_from` (object or string ID, v1 field names for inline), `address_to` (object or string ID, v1 field names for inline), `parcels` (array of parcel objects or string IDs)
- **Optional:** `customs_declaration` (string, object ID), `extra` (object, for signature, insurance, etc.), `metadata` (string), `async` (boolean, default true), `carrier_accounts` (array of carrier account IDs to filter rates)
- **Note:** Inline address objects use v1 names: `name`, `street1`, `city`, `state`, `zip`, `country`

### `GetShipment`
Retrieve a shipment by ID. Use to poll for rates after async creation.
- **Required:** `shipment_id` (string)

### `ListShipments`
List all shipments. Supports pagination.
- **Optional:** `page` (integer), `results` (integer, page size)

### `ListShipmentRates`
Retrieve rates for an existing shipment by ID.
- **Required:** `shipment_id` (string)

---

## Rates

### `GetRate`
Retrieve a specific rate by ID.
- **Required:** `rate_id` (string)

### `ListShipmentRatesByCurrencyCode`
Retrieve shipment rates filtered to a specific currency.
- **Required:** `shipment_id` (string), `currency_code` (string, ISO 4217 e.g., `USD`)
- **Optional:** `page` (integer), `results` (integer)

### `CreateLiveRate`
Generate live rates for a checkout flow with line items and address.
- **Required:** `address_to` (object), `line_items` (array), `parcel` (object or template)
- **Optional:** `address_from` (object), `carrier_accounts` (array)

### `GetDefaultParcelTemplate`
Show the current default parcel template for checkout rates. No parameters.

### `DeleteDefaultParcelTemplate`
Clear the current default parcel template. No parameters.

### `UpdateDefaultParcelTemplate`
Update the default parcel template for checkout rates.
- **Required:** `object_id` (string, parcel template ID)

---

## Transactions (Labels)

### `CreateTransaction`
Purchase a shipping label from an existing rate. **Async:** returns immediately with status `QUEUED`; poll via `GetTransaction` until status is `SUCCESS` or `ERROR`.
- **Required:** `rate` (string, rate object_id)
- **Optional:** `label_file_type` (string, e.g., `PDF_4x6`, `PNG`, `ZPLII`), `async` (boolean, default true), `metadata` (string)
- **Response includes:** `label_url`, `tracking_number`, `tracking_url_provider` when status is `SUCCESS`

### `GetTransaction`
Retrieve a transaction (label) by ID. Use to poll async label purchases.
- **Required:** `transaction_id` (string)

### `ListTransactions`
List all transactions. Supports filtering and pagination.
- **Optional:** `page` (integer), `results` (integer), `object_status` (string), `tracking_status` (string)

---

## Tracking

### `GetTrack`
Get current tracking status for a carrier + tracking number.
- **Required:** `carrier` (string, carrier token e.g., `usps`, `ups`, `fedex`, `dhl_express`), `tracking_number` (string)

### `CreateTrack`
Register a shipment for tracking webhook notifications.
- **Required:** `carrier` (string), `tracking_number` (string)
- **Optional:** `metadata` (string)

---

## Batches

### `CreateBatch`
Create a new batch of shipments. **Async:** returns immediately with status `VALIDATING`; poll via `GetBatch` until status is `VALID` or `INVALID`.
- **Required:** `default_carrier_account` (string, carrier account ID), `default_servicelevel_token` (string), `batch_shipments` (array of batch shipment objects)
- **Optional:** `label_filetype` (string), `metadata` (string), `label_size` (string)
- **Each batch shipment object requires:** `shipment` (object with `address_from`, `address_to`, `parcels`, and optionally `customs_declaration`)

### `GetBatch`
Retrieve a batch by ID. Includes status and per-shipment results.
- **Required:** `batch_id` (string)

### `PurchaseBatch`
Purchase labels for all valid shipments in a batch. **Async:** triggers purchase; poll `GetBatch` until status is `PURCHASED`.
- **Required:** `batch_id` (string)

### `AddShipmentsToBatch`
Add shipments to an existing batch (before purchase only).
- **Required:** `batch_id` (string), `body` (array of batch shipment objects)

### `RemoveShipmentsFromBatch`
Remove shipments from an existing batch (before purchase only).
- **Required:** `batch_id` (string), `shipment_ids` (array of string IDs)

---

## Customs

### `CreateCustomsDeclaration`
Create a customs declaration for international shipments.
- **Required:** `certify` (boolean, must be true), `certify_signer` (string), `contents_type` (string), `non_delivery_option` (string), `items` (array of customs item object_ids)
- **Optional:** `contents_explanation` (string, required if contents_type is OTHER), `exporter_reference` (string), `importer_reference` (string), `invoice` (string), `license` (string), `certificate` (string), `notes` (string), `eel_pfc` (string), `incoterm` (string), `b13a_filing_option` (string), `metadata` (string)

### `GetCustomsDeclaration`
Retrieve a customs declaration by ID.
- **Required:** `customs_declaration_id` (string)

### `ListCustomsDeclarations`
List all customs declarations. Supports pagination.
- **Optional:** `page` (integer), `results` (integer)

### `CreateCustomsItem`
Create a customs item (individual line item within a declaration).
- **Required:** `description` (string), `quantity` (integer), `net_weight` (string), `mass_unit` (string), `value_amount` (string), `value_currency` (string), `origin_country` (string)
- **Optional:** `tariff_number` (string), `sku_code` (string), `eccn_ear99` (string), `metadata` (string)

### `GetCustomsItem`
Retrieve a customs item by ID.
- **Required:** `customs_item_id` (string)

### `ListCustomsItems`
List all customs items. Supports pagination.
- **Optional:** `page` (integer), `results` (integer)

---

## Manifests

### `CreateManifest`
Create an end-of-day manifest (SCAN form) for carrier pickup. **Async:** returns with status `QUEUED`; poll via `GetManifest`.
- **Required:** `carrier_account` (string, carrier account ID), `shipment_date` (string, ISO 8601 date), `address_from` (object or string ID)
- **Optional:** `transactions` (array of transaction IDs; if omitted, includes all eligible), `async` (boolean)

### `GetManifest`
Retrieve a manifest by ID.
- **Required:** `manifest_id` (string)

### `ListManifests`
List all manifests. Supports pagination.
- **Optional:** `page` (integer), `results` (integer)

---

## Parcels

### `CreateParcel`
Create a new parcel object.
- **Required:** `length` (string), `width` (string), `height` (string), `distance_unit` (string: `in`, `cm`, `ft`, `m`, `mm`, `yd`), `weight` (string), `mass_unit` (string: `lb`, `kg`, `g`, `oz`)
- **Optional:** `template` (string, carrier parcel template token), `metadata` (string)

### `GetParcel`
Retrieve an existing parcel by ID.
- **Required:** `parcel_id` (string)

### `ListParcels`
List all parcels. Supports pagination.
- **Optional:** `page` (integer), `results` (integer)

---

## Parcel Templates

### `ListCarrierParcelTemplates`
List all carrier-provided parcel templates (e.g., USPS Flat Rate). Filterable by carrier.
- **Optional:** `carrier` (string, carrier token), `include` (string)

### `GetCarrierParcelTemplate`
Retrieve a specific carrier parcel template.
- **Required:** `carrier_parcel_template_id` (string)

### `ListUserParcelTemplates`
List all user-created parcel templates. No required parameters.

### `CreateUserParcelTemplate`
Create a new user parcel template.
- **Required:** `name` (string), `length` (string), `width` (string), `height` (string), `distance_unit` (string), `weight` (string), `mass_unit` (string)
- **Optional:** `template` (string)

### `GetUserParcelTemplate`
Retrieve a user parcel template by ID.
- **Required:** `user_parcel_template_id` (string)

### `UpdateUserParcelTemplate`
Update an existing user parcel template.
- **Required:** `user_parcel_template_id` (string)
- **Optional:** Same fields as create

### `DeleteUserParcelTemplate`
Delete a user parcel template.
- **Required:** `user_parcel_template_id` (string)

---

## Carrier Accounts

### `ListCarrierAccounts`
List all carrier accounts. Supports pagination and filtering.
- **Optional:** `page` (integer), `results` (integer), `carrier` (string), `account_id` (string)

### `CreateCarrierAccount`
Create a new carrier account.
- **Required:** `carrier` (string), `account_id` (string), `parameters` (object, carrier-specific)

### `GetCarrierAccount`
Retrieve a carrier account by ID.
- **Required:** `carrier_account_id` (string)

### `UpdateCarrierAccount`
Update a carrier account.
- **Required:** `carrier_account_id` (string)
- **Optional:** `account_id` (string), `parameters` (object)

### `GetCarrierRegistrationStatus`
Get carrier registration status.
- **Required:** `carrier` (string)

### `InitiateOauth2Signin`
Connect a carrier account using OAuth 2.0.
- **Required:** `carrier_account_id` (string), `redirect_url` (string)

---

## Orders

### `CreateOrder`
Create a new order.
- **Required:** `to_address` (object), `line_items` (array), `placed_at` (string, ISO 8601), `order_number` (string), `order_status` (string), `shipping_cost` (string), `shipping_cost_currency` (string)
- **Optional:** `from_address` (object), `weight` (string), `weight_unit` (string), `notes` (string), `shipping_method` (string)

### `GetOrder`
Retrieve an order by ID.
- **Required:** `order_id` (string)

### `ListOrders`
List all orders. Supports pagination.
- **Optional:** `page` (integer), `results` (integer), `order_status` (array of strings), `shop_app` (string)

### Packing slip (known gap)
There is no packing-slip tool in the catalog. To retrieve a packing slip for an order, fall back to the REST API: `GET /orders/{order_id}/packingslip`.

---

## Refunds

### `CreateRefund`
Create a refund (void a label). Must be requested within 30 days of purchase for most carriers.
- **Required:** `transaction` (string, transaction object_id)
- **Optional:** `async` (boolean)

### `GetRefund`
Retrieve a refund by ID.
- **Required:** `refund_id` (string)

### `ListRefunds`
List all refunds. Supports pagination.
- **Optional:** `page` (integer), `results` (integer)

---

## Pickups

### `CreatePickup`
Schedule a carrier pickup.
- **Required:** `carrier_account` (string), `location` (object with address and building info), `transactions` (array of transaction IDs), `requested_start_time` (string, ISO 8601), `requested_end_time` (string, ISO 8601)
- **Optional:** `is_test` (boolean)

---

## Service Groups

### `ListServiceGroups`
List all service groups. No required parameters.

### `CreateServiceGroup`
Create a new service group.
- **Required:** `name` (string), `description` (string), `flat_rate` (string), `flat_rate_currency` (string), `service_levels` (array)

### `UpdateServiceGroup`
Update an existing service group.
- **Required:** `service_group_id` (string)
- **Optional:** Same fields as create

### `DeleteServiceGroup`
Delete a service group.
- **Required:** `service_group_id` (string)

---

## Webhooks

### `createWebhook`
Create a new webhook subscription.
- **Required:** `url` (string), `event` (string, e.g., `track_updated`, `transaction_created`, `batch_created`)
- **Optional:** `is_test` (boolean), `active` (boolean)

### `getWebhook`
Retrieve a specific webhook.
- **Required:** `webhook_id` (string)

### `listWebhooks`
List all webhooks. No required parameters.

### `updateWebhook`
Update an existing webhook.
- **Required:** `webhook_id` (string)
- **Optional:** `url` (string), `event` (string), `is_test` (boolean), `active` (boolean)

### `deleteWebhook`
Delete a webhook.
- **Required:** `webhook_id` (string)

---

## Shippo Accounts

### `ListShippoAccounts`
List all Shippo accounts. Supports pagination.
- **Optional:** `page` (integer), `results` (integer)

### `CreateShippoAccount`
Create a Shippo account.
- **Required:** `email` (string), `first_name` (string), `last_name` (string), `company_name` (string)

### `GetShippoAccount`
Retrieve a Shippo account.
- **Required:** `shippo_account_id` (string)

### `UpdateShippoAccount`
Update a Shippo account.
- **Required:** `shippo_account_id` (string)
- **Optional:** `email` (string), `first_name` (string), `last_name` (string), `company_name` (string)

---

## Async Tools Summary

These tools return immediately and require polling to get final results:

| Tool | Initial Status | Poll With | Final Status |
|---|---|---|---|
| `CreateShipment` (async=true) | `QUEUED` | `GetShipment` | rates populated |
| `CreateTransaction` | `QUEUED` | `GetTransaction` | `SUCCESS` or `ERROR` |
| `CreateBatch` | `VALIDATING` | `GetBatch` | `VALID` or `INVALID` |
| `PurchaseBatch` | `PURCHASING` | `GetBatch` | `PURCHASED` |
| `CreateManifest` | `QUEUED` | `GetManifest` | `SUCCESS` or `ERROR` |
| `CreateRefund` (async=true) | `QUEUED` | `GetRefund` | `SUCCESS` or `ERROR` |
