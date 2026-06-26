# hotel-price-finder

Real-time hotel price comparison across Booking.com, Agoda, Trip.com & more. Find the cheapest OTA for any hotel, instantly. No API key required.

## What It Does

Search any city → Get hotel list with ratings → Compare real-time prices across OTAs → Find the best deal.

```
🏨 Hotel Search: Seoul
📅 Apr 10-12 (2 nights) | 👤 2 adults

1. Hotel Skypark Myeongdong 3 - ⭐ 4.7 (2,272 reviews)
   Trip.com: $292 | Agoda: $303 | Booking.com: $334
   → Trip.com saves you $42 vs Booking.com!
```

## Modes

| Mode | Requirement | What You Get |
|------|------------|--------------|
| **Free** (default) | None | Hotel list + real-time OTA price comparison via Xotelo |
| **Agoda Direct** | None | City lookup + Agoda search URL + area recommendations |
| **Apify** (optional) | `APIFY_API_KEY` | Agoda-specific deep search (22+ fields per hotel) |

## Install

```bash
npx clawhub@latest install hotel-price-finder
```

## Setup

### Free Mode (default)
No setup needed. Works immediately using Xotelo's free API.

### Apify Mode (optional)
```bash
export APIFY_API_KEY="your_apify_api_key_here"
```

## Usage Examples

- "Find hotels in Seoul for May 1-3"
- "Compare hotel prices in Bangkok under $50/night"
- "Which OTA is cheapest for Hotel Skypark Myeongdong?"
- "서울 명동 근처 호텔 5월 1일~3일 2명"
- "Show me the cheapest dates for this hotel" (heatmap)

## Data Sources

### Free Mode (Xotelo API)
- Hotel list: name, rating, review count, price range, GPS, image
- OTA price comparison: Booking.com, Agoda, Trip.com, Vio.com, Hotels.com, Expedia
- Price heatmap: cheapest dates visualization

### Agoda Direct
- City/area lookup via Agoda autocomplete API
- Pre-built search URLs with all filters

### Apify Mode
- 22+ fields: name, star rating, detailed pricing, facilities, photos, policies

## Supported Cities

25+ cities pre-mapped including Seoul, Tokyo, Osaka, Bangkok, Singapore, Bali, Hong Kong, Taipei, Paris, London, New York, and more. Any city searchable via Xotelo search API.

## License

MIT
