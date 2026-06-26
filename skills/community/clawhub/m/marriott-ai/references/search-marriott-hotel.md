# search-marriott-hotel ref

## Marriott Hotel Search (search-marriott-hotel)

### Parameters

- **--dest-name** (required): Destination name (country, province, city, district)
- **--key-words** (optional): Search keywords (hotel name, brand)
- **--poi-name** (optional): Nearby POI name
- **--hotel-bed-types** (optional): Hotel bed types (multiple selection, separated by commas)
  - Values: `大床房` (king bed) · `双床房` (twin beds) · `多床房` (multiple beds)
- **--max-price** (optional): Maximum price in RMB
- **--sort** (optional): Sorting rule
  - Values: `distance_asc` (distance priority) · `rate_desc` (rating priority) · `price_asc` (low price priority) · `price_desc` (high price priority) · `no_rank` (default)
- **--check-in-date** (optional): Check-in date (yyyy-MM-dd format)
- **--check-out-date** (optional): Check-out date (yyyy-MM-dd format)

### Examples

```bash
flyai search-marriott-hotel --dest-name "杭州"
flyai search-marriott-hotel --dest-name "上海" --sort "rate_desc"
```

### Output Example

```
{
  "data": {
    "itemList": [
      {
        "brandName": "...", // Hotel brand
        "address": "...", // Hotel address
        "star": "...", // Hotel star rating
        "shid": "...", // Hotel unique identifier
        "latitude": "...", // Hotel address latitude
        "nearbyPoi": "...", // Nearby POI
        "decorationTime": "...", // Hotel renovation time
        "price": "...", // Hotel reference price, guide users to booking page for actual price with possible discounts
        "name": "...", // Hotel name
        "mainPic": "https://...jpg", // Hotel main image
        "detailUrl": "https:...", // Booking link
        "longitude": "..." // Hotel address longitude
      }
    ]
  },
  "message": "success",
  "status": 0
}
```