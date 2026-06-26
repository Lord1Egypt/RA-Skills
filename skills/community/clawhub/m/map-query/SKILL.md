
---
name: map-query
description: Map Query Skill - Query nearby food and promotions by address, supports AMap/Baidu/Tencent Maps
metadata:
  version: 1.0.0
  author: uynewnas
  category: location-services
  tags: [map, poi, food, location, amap, baidu, tencent]
  env:
    required:
      - name: AMAP_KEY
        description: AMap (高德地图) API Key
        required: false
      - name: BAIDU_MAP_KEY
        description: Baidu Maps API Key
        required: false
      - name: TENCENT_MAP_KEY
        description: Tencent Maps API Key
        required: false
    note: At least one map provider API key must be configured
---

# Map Query Skill

Query nearby restaurants, shops, promotions and other POI information by specific address.

## Core Features

- **Address Geocoding**: Convert detailed address to latitude and longitude coordinates
- **Nearby Search**: Query POIs (Points of Interest) around specified location
- **Multi-map Support**: Integrate AMap, Baidu Maps, Tencent Maps APIs
- **Food Search**: Specialized search for nearby restaurants and food places
- **Promotions Search**: Query nearby merchant promotions and deals

## Supported Map Providers

| Provider | Features | Notes |
|---------|---------|-------|
| AMap (高德) | ✅ Geocoding, POI Search, Food Search | API Key required |
| Baidu Maps | ✅ Geocoding, POI Search, Food Search | API Key required |
| Tencent Maps | ✅ Geocoding, POI Search, Food Search | API Key required |

## Main Functions

### 1. Address Geocoding
- Support detailed addresses: e.g., "No. 47, Shangjiao xx Street, Panyu District, Guangzhou"
- Support city + landmark: e.g., "Beijing Tiananmen"
- Auto-resolve and return coordinates

### 2. Nearby Search
- Search by type: food, hotel, bank, gas station, etc.
- Filter by distance: 1km, 2km, 5km, etc.
- Sort by rating: prioritize high-rated merchants
- Sort by distance: prioritize nearby merchants

### 3. Food Search
- Cuisine filter: Sichuan, Cantonese, Japanese, etc.
- Price range: per capita consumption range
- Business hours filter
- User rating filter

### 4. Promotions Search
- Find nearby merchant deals
- New store opening information
- Limited-time discount activities

## Dependencies

- Node.js &gt;= 18
- Map provider API Key (at least one configured)

## Quick Start

```bash
# Configure API Key
export AMAP_KEY=your_amap_api_key
export BAIDU_MAP_KEY=your_baidu_map_key
export TENCENT_MAP_KEY=your_tencent_map_key

# Search for food near address
node scripts/search.mjs "Sanlitun, Chaoyang District, Beijing" --type food

# Search for promotions
node scripts/search.mjs "Sanlitun, Chaoyang District, Beijing" --type promotion
```

---

## References

- 12306 Skill: https://github.com/kirorab/12306-skill
- AMap API: https://lbs.amap.com/
- Baidu Maps API: https://lbsyun.baidu.com/
- Tencent Maps API: https://lbs.qq.com/
