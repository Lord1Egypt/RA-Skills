# Printify tools via Agiexa (25)

Preview only - these become available to the agent after Agiexa launches (November 2026) and the merchant connects Printify and turns the tools on. They cannot be called today.

Interactive explorer: https://agiexa.com/integrations/printify

| Tool | What it does |
| --- | --- |
| `PRINTIFY_ARCHIVE_UPLOAD` | Irreversibly archive an image in the connected merchant's Printify media library |
| `PRINTIFY_CALCULATE_ORDER_SHIPPING` | Calculate available shipping-cost estimates for proposed line items and a destination |
| `PRINTIFY_CREATE_PRODUCT` | Create a new product draft in a Printify shop |
| `PRINTIFY_CREATE_WEBHOOK` | Create a persistent webhook subscription for a Printify shop |
| `PRINTIFY_DELETE_PRODUCT` | Permanently delete a product from a Printify shop |
| `PRINTIFY_DELETE_WEBHOOK` | Permanently delete a Printify webhook subscription so future events are no longer delivered |
| `PRINTIFY_GET_BLUEPRINT` | Get the full catalog record for one Printify product blueprint, including its description and images |
| `PRINTIFY_GET_ORDER` | Get complete details for one Printify order, including its recipient address, line items, status, shipping method, shipments, and timestamps |
| `PRINTIFY_GET_PRODUCT` | Get the complete Printify record for one product in a shop, including variants, print areas, images, visibility, and sales-channel properties |
| `PRINTIFY_GET_SHIPPING_DETAILS` | Get per-variant shipping costs and handling-time ranges for one advertised V2 shipping method |
| `PRINTIFY_LIST_BLUEPRINT_PRINT_PROVIDERS` | List print providers that can fulfill a specific Printify blueprint |
| `PRINTIFY_LIST_BLUEPRINT_VARIANTS` | List purchasable variants and print placeholders for a blueprint and print provider |
| `PRINTIFY_LIST_ORDERS` | Return one page of orders in a Printify shop, optionally filtered by provider status or exact SKU |
| `PRINTIFY_LIST_PRODUCTS` | Return one page of products in a Printify shop |
| `PRINTIFY_LIST_SHIPPING_METHODS` | List the V2 shipping methods actually available for a Printify blueprint and print provider |
| `PRINTIFY_LIST_SHOPS` | List shops available to the connected Printify merchant account |
| `PRINTIFY_LIST_UPLOADS` | Return one page of images in the connected merchant's Printify media library |
| `PRINTIFY_LIST_WEBHOOKS` | List webhook subscriptions configured for a Printify shop |
| `PRINTIFY_PUBLISH_PRODUCT` | Start asynchronous publication of one or more fields selected in fields_to_publish from Printify to the shop's connected sales channel |
| `PRINTIFY_SEARCH_BLUEPRINTS` | Search Printify's product blueprint catalog by case-insensitive text in title, brand, or model |
| `PRINTIFY_SIMULATE_WEBHOOK` | Ask Printify to send a simulated event to an existing webhook's external callback URL |
| `PRINTIFY_UNPUBLISH_PRODUCT` | Notify Printify that a product has been unpublished from the connected sales channel |
| `PRINTIFY_UPDATE_PRODUCT` | Update selected fields of an existing Printify product |
| `PRINTIFY_UPDATE_WEBHOOK` | Replace the callback URL of an existing Printify webhook subscription |
| `PRINTIFY_UPLOAD_IMAGE` | Add an image to the connected merchant's Printify media library from either a public HTTP(S) URL or base64 content |
