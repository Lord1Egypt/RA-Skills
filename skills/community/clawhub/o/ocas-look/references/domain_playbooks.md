# Look Domain Playbooks

## Events
Strong grounding required for venue and timezone. EXIF capture location is weak signal only. Strong grounding: QR/URL to canonical event page, full street address that geocodes, venue name with official confirmation. Draft types: calendar_hold (ungrounded), calendar_event (grounded), ticket_purchase.

## Food Macros
Use context and nearby location to identify restaurant. Apply vegetarian constraint before clarification. Infer portion size. Produce macro range with confidence. Draft type: health_macros.

## Places
OCR signage, use EXIF GPS for candidate resolution, dedupe against try-list. Draft type: maps_to_try.

## Products
Barcode dominates when present. Otherwise OCR brand/model. Fetch offers from preferred retailers. Reduce to cheapest vs fastest. Draft types: product_pricing, product_order.

## Civic Issues
Determine jurisdiction from GPS. Validate geofence if configured. Description stays factual. Draft type: civic_report_311.

## Receipts
Extract merchant, date, subtotal, tax, tip, total. Categorize via merchant type. Route to ledger per config. Draft type: expense_entry.

## Documents
Classify, OCR, generate searchable PDF. Propose drive folder and filename. Draft type: drive_file_document.
