
# 🗺️ Map Query Skill - Usage Guide

## 🎯 Core Capabilities

You are now using the Map Query skill. You can help users:

1. **Address Geocoding** - Convert specific addresses to geographic locations
2. **Nearby Search** - Find POIs (Points of Interest) near a specified location
3. **Food Search** - Specifically find nearby restaurants and food places
4. **Promotions Search** - Find nearby merchant promotions and deals

---

## 📋 Available Map Providers

| Provider | Environment Variable | Status |
|---------|---------------------|--------|
| AMap | `AMAP_KEY` | Recommended |
| Baidu Maps | `BAIDU_MAP_KEY` | Alternative |
| Tencent Maps | `TENCENT_MAP_KEY` | Alternative |

---

## 🔧 Usage Workflow

### 1. Check API Key Configuration

Before executing a query, first check if map API keys are configured in environment variables:

```bash
# Check if API keys are configured
echo $AMAP_KEY
echo $BAIDU_MAP_KEY
echo $TENCENT_MAP_KEY
```

If not configured, remind the user:
&gt; ⚠️ Please configure a map API Key first. At least one map provider is required.

### 2. Address Geocoding

When the user provides an address, first perform address geocoding to get latitude and longitude:

**Example address formats:**
- Detailed address: `No. 47, Shangjiao xx Street, Panyu District, Guangzhou`
- City + Landmark: `Beijing Tiananmen`
- Landmark name: `Shanghai Oriental Pearl Tower`

### 3. Nearby Search Parameters

Based on user needs, determine search parameters:

| Parameter | Description | Optional Values |
|-----------|-------------|----------------|
| `--type` | Search type | `food`(food), `promotion`(promotions), `hotel`(hotel), `bank`(bank) |
| `--radius` | Search radius | `1000`(1km), `2000`(2km), `5000`(5km) |
| `--sort` | Sort order | `distance`(distance), `rating`(rating) |
| `--limit` | Number of results | 1-50 |

---

## 💬 Conversation Examples

### Example 1: Search for Nearby Food

**User:** "Help me find what's good to eat near No. 47, Shangjiao xx Street, Panyu District, Guangzhou"

**Your Response:**
1. Check if API Key is configured
2. Parse address to get coordinates
3. Call map API to search for nearby food
4. Organize results and return:

```
📍 **Address Geocoded Successfully**
Address: No. 47, Shangjiao xx Street, Panyu District, Guangzhou
Coordinates: 113.xxx, 23.xxx

🍽️ **Nearby Food Recommendations (within 1km)**

1. **XX Restaurant** - Cantonese Cuisine
   ⭐ 4.5 | 📍 200m | 💰 ¥80 per person
   📝 Recommended: Signature Roast Goose, White Cut Chicken

2. **YY Noodle Shop** - Noodles
   ⭐ 4.2 | 📍 350m | 💰 ¥30 per person
   📝 Recommended: Wonton Noodles, Beef Brisket Rice Noodles

3. **ZZ Hot Pot** - Hot Pot
   ⭐ 4.7 | 📍 500m | 💰 ¥120 per person
   📝 Recommended: Mandarin Duck Pot, Fresh Beef

---
💡 Tip: Click store name to see details, need navigation? Let me know
```

### Example 2: Search for Promotions

**User:** "Are there any promotions near Sanlitun, Chaoyang District, Beijing recently?"

**Your Response:**
1. Check API Key
2. Parse address
3. Search for promotions
4. Return results:

```
📍 **Address Geocoded Successfully**
Address: Sanlitun, Chaoyang District, Beijing
Coordinates: 116.45, 39.93

🎉 **Recent Promotions**

1. **XX Mall Spring Sale**
   📍 300m | 🕐 Now - April 15
   📝 All clothing 50% off, spend 300 get 50 off

2. **YY Coffee Shop New Opening**
   📍 150m | 🕐 Now - March 31
   📝 Buy one get one free on all drinks

3. **ZZ Supermarket Member Day**
   📍 400m | 🕐 Every Wednesday
   📝 Members enjoy 12% off, double points

---
💡 Need more details or navigation? Let me know
```

---

## ⚠️ Notes

1. **API Key Required** - At least one map provider API Key is needed
2. **Address Should Be Detailed** - More detailed address means more accurate geocoding
3. **Results Limited** - Single query returns limited number of results
4. **Data Timeliness** - Information such as promotions may change at any time

---

## 🔗 Related Scripts

The skill provides the following scripts:

- `scripts/geocode.mjs` - Address geocoding
- `scripts/search.mjs` - Nearby search
- `scripts/food.mjs` - Food search
- `scripts/promotion.mjs` - Promotion search

---

**Last Updated:** 2026-03-23
