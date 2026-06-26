---
name: grocy-inventory
description: "Manage Grocy inventory, shopping list, batteries, and barcodes. Use when user wants to: (1) Check what's in their fridge/pantry, (2) See expiring products, (3) Manage stock by barcode, (4) Add/Consume/Transfer products, (5) Track rechargeable batteries. Grocy is a self-hosted inventory management app running at http://localhost:14611"
---

# Grocy Inventory Skill

Check and manage your Grocy inventory, shopping list, and batteries. This skill connects to your local Grocy instance.

## Configuration

| Variable | Value |
|----------|-------|
| URL | `http://localhost:14611` |
| API Key | `mz43yGJzBKfwZdSOwG5EdnKPRrKnCbkGrEFbxXYv2JF61tQ9Mj` |

## Quick Commands

### Check Stock (Fridge/Pantry)
```bash
curl -s -H "GROCY-API-KEY: $API_KEY" "$URL/api/stock"
```

### Lookup Details by Barcode
```bash
curl -s -H "GROCY-API-KEY: $API_KEY" "$URL/api/stock/products/by-barcode/{barcode}" 
```

### Consume Stock by Barcode
```bash
curl -s -X POST -H "GROCY-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"amount": 1, "transaction_type": "consume"}' \
  "$URL/api/stock/products/by-barcode/{barcode}/consume"
```

### Mark Stock as Opened by Barcode
```bash
curl -s -X POST -H "GROCY-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"amount": 1}' \
  "$URL/api/stock/products/by-barcode/{barcode}/open"
```

### Transfer Stock by Barcode
```bash
curl -s -X POST -H "GROCY-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"amount": 1, "location_id_from": 6, "location_id_to": 2}' \
  "$URL/api/stock/products/by-barcode/{barcode}/transfer"
```

### Get All Batteries
```bash
curl -s -H "GROCY-API-KEY: $API_KEY" "$URL/api/batteries"
```

### Track Battery Charge
```bash
curl -s -X POST -H "GROCY-API-KEY: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"battery_id": 7}' \
  "$URL/api/batteries/7/charge"
```

## Common Tasks

| Task | Command |
|------|---------|
| Find product by barcode | GET `/api/stock/products/by-barcode/{barcode}` |
| Consume by barcode | POST `/api/stock/products/by-barcode/{barcode}/consume` |
| Open by barcode | POST `/api/stock/products/by-barcode/{barcode}/open` |
| Transfer by barcode | POST `/api/stock/products/by-barcode/{barcode}/transfer` |
| Check battery status | GET `/api/batteries` |
| Track battery charge | POST `/api/batteries/{id}/charge` |

## Tips

- Use `jq` for pretty JSON logs: `curl ... | jq`
- For barcodes, use the direct `/by-barcode/{barcode}` endpoints found in the `Stock "by-barcode"` tags.
- Full API docs: See `references/grocy-api.md`
