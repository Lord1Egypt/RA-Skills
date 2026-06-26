# search-marriott-package ref

## Marriott Hotel Package Search (search-marriott-package)

### Parameters

- **--keyword** (optional): Search keyword
- **--hotel-name** (optional): Hotel name
- **--province-or-city** (optional): Province or city name
- **--sort-type** (optional): Sorting method
  - Values: `price_asc` (low price priority) · `price_desc` (high price priority) · `score_desc` (score priority)

### Validation Rules

- At least one of the following parameters must be provided: `--keyword`, `--hotel-name`, `--province-or-city`. They cannot all be empty at the same time.

### Examples

```bash
flyai search-marriott-package --keyword "通兑" --sort-type "price_asc"
flyai search-marriott-package --hotel-name "西溪喜来登" --province-or-city "杭州"
```

### Output Example

```
{
  "data": {
    "itemList": [
      {
        "picUrl": "https://...jpg", // Package image
        "itemId": "...", // Package unique identifier
        "sellPoint": "...", // Selling point
        "price": "...", // Reference price, guide users to booking page for actual price with possible discounts
        "detailUrl": "https://...", // Booking link
        "title": "...", // Package name
        "benefit": "..." // Member benefits
      }
    ]
  },
  "message": "success",
  "status": 0
}
```