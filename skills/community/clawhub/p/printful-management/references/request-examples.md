# Printful request examples

Use these as starting payloads. Adjust fields to match the exact endpoint and product model you are targeting.

For product reporting/export, use the built-in helper instead of hand-formatting responses:

```powershell
python scripts/printful_api.py export-products --store-id 12345 --format markdown --output-file report.md
python scripts/printful_api.py export-products --store-id 12345 --format csv --output-file products.csv
python scripts/printful_api.py export-products --store-id 12345 --format json --output-file products.json
```

## Create manual/API store product

```json
{
  "sync_product": {
    "external_id": "example-product-001",
    "name": "Example product title",
    "thumbnail": "https://example.com/thumb.jpg"
  },
  "sync_variants": [
    {
      "external_id": "example-variant-001",
      "variant_id": 4011,
      "retail_price": "24.99",
      "files": [
        {
          "url": "https://example.com/artwork-front.png"
        }
      ]
    }
  ]
}
```

## Update connected-store sync variant

```json
{
  "retail_price": "27.99",
  "sku": "MY-SKU-123",
  "files": [
    {
      "type": "front",
      "url": "https://example.com/new-art.png"
    }
  ]
}
```

## Create order draft

```json
{
  "external_id": "order-1001",
  "shipping": "STANDARD",
  "recipient": {
    "name": "John Smith",
    "address1": "19749 Dearborn St",
    "city": "Chatsworth",
    "state_code": "CA",
    "country_code": "US",
    "zip": "91311"
  },
  "items": [
    {
      "sync_variant_id": 123456789,
      "quantity": 1
    }
  ]
}
```

## Add file to file library

```json
{
  "url": "https://example.com/design.png",
  "filename": "design.png",
  "visible": true
}
```

## Set webhooks

```json
{
  "url": "https://example.com/printful/webhook",
  "types": [
    "package_shipped",
    "order_created",
    "order_updated",
    "product_synced",
    "stock_updated"
  ]
}
```

## Create mockup task

```json
{
  "variant_ids": [4011],
  "format": "jpg",
  "files": [
    {
      "placement": "front",
      "image_url": "https://example.com/design.png"
    }
  ]
}
```

## Shipping rate estimate

```json
{
  "recipient": {
    "country_code": "US",
    "state_code": "CA"
  },
  "items": [
    {
      "variant_id": 4011,
      "quantity": 1
    }
  ]
}
```

## Tax rate estimate

```json
{
  "recipient": {
    "country_code": "US",
    "state_code": "CA",
    "zip": "91311"
  },
  "retail_costs": {
    "currency": "USD",
    "subtotal": "24.99",
    "shipping": "4.99"
  }
}
```
