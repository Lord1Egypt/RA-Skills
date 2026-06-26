# Grocy API Reference

## Base URL
```
http://localhost:14611
```

## Authentication
Header: `GROCY-API-KEY: your-api-key`

## Stock "by-barcode" API

Grocy **does** feature specialized endpoints to manage stock via barcode directly!

### Get Product Details by Barcode
```bash
GET /api/stock/products/by-barcode/{barcode}
```
Returns a `ProductDetailsResponse` object.

### Add Product to Stock by Barcode
```bash
POST /api/stock/products/by-barcode/{barcode}/add
```
```json
{
  "amount": 1,
  "best_before_date": "2026-06-01",
  "transaction_type": "purchase",
  "price": 1.99,
  "location_id": 3
}
```

### Consume Product by Barcode
```bash
POST /api/stock/products/by-barcode/{barcode}/consume
```
```json
{
  "amount": 1,
  "transaction_type": "consume",
  "spoiled": false,
  "location_id": 3,
  "exact_amount": false
}
```

### Transfer Product by Barcode
```bash
POST /api/stock/products/by-barcode/{barcode}/transfer
```
```json
{
  "amount": 1,
  "location_id_from": 1,
  "location_id_to": 2
}
```

### Inventory (Audit) Product by Barcode
```bash
POST /api/stock/products/by-barcode/{barcode}/inventory
```
```json
{
  "new_amount": 5,
  "best_before_date": "2026-06-01",
  "location_id": 3,
  "price": 1.99
}
```

### Mark Product as Opened by Barcode
```bash
POST /api/stock/products/by-barcode/{barcode}/open
```
```json
{
  "amount": 1
}
```

---

## Battery API

### Get All Batteries
```bash
GET /api/batteries
```

### Get Battery Definition
```bash
GET /api/objects/batteries
```

### Track Battery Charge
```bash
POST /api/batteries/track
```
```json
{
  "battery_id": 1,
  "tracked_time": "2026-03-04T05:50:00"
}
```

---

## Example: Consume Milk via Barcode
```bash
curl -s -X POST -H "GROCY-API-KEY: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"amount": 1, "transaction_type": "consume", "location_id": 6}' \
  "http://localhost:14611/api/stock/products/by-barcode/8998009010620/consume"
```
