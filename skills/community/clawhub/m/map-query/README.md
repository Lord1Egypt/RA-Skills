
# 🗺️ Map Query Skill - OpenClaw Skill

Query nearby restaurants, shops, promotions and other POI information by specific address. Supports AMap, Baidu Maps, Tencent Maps.

## ✨ Core Features

- **📍 Address Geocoding** - Convert detailed address to latitude and longitude coordinates
- **🍽️ Food Search** - Find nearby restaurants and food places
- **🎉 Promotions Search** - Query nearby merchant promotions and deals
- **🏪 POI Search** - Search nearby points of interest by type
- **🔀 Multi-map Support** - AMap/Baidu/Tencent Maps APIs

## 🚀 Quick Start

### 1. Get API Key

Need to configure at least one map provider API Key:

- **AMap**: https://lbs.amap.com/ (Recommended)
- **Baidu Maps**: https://lbsyun.baidu.com/
- **Tencent Maps**: https://lbs.qq.com/

### 2. Configure Environment Variables

```bash
# AMap (Recommended)
export AMAP_KEY=your_amap_api_key

# Baidu Maps
export BAIDU_MAP_KEY=your_baidu_map_key

# Tencent Maps
export TENCENT_MAP_KEY=your_tencent_map_key
```

### 3. Install the Skill

```powershell
# Windows
xcopy /E /I map-query %USERPROFILE%\.openclaw\skills\map-query

# Linux/Mac
cp -r map-query ~/.openclaw/skills/map-query
```

### 4. Restart OpenClaw

```bash
openclaw restart
```

## 💬 Usage Examples

### Search for Nearby Food

**You ask:** "Help me find what's good to eat near No. 47, Shangjiao xx Street, Panyu District, Guangzhou"

**AI responds:**
```
📍 Address geocoded successfully: No. 47, Shangjiao xx Street, Panyu District, Guangzhou

🍽️ Nearby food recommendations (within 1km):

1. Yue Xiang Ge - Cantonese Cuisine ⭐4.8 (280m)
   Recommended: Signature Roast Goose, White Cut Chicken

2. Old Shanghai Wonton Shop - Snacks ⭐4.5 (150m)
   Recommended: Fresh Pork Wontons

...
```

### Search for Promotions

**You ask:** "Are there any promotions near Sanlitun, Beijing recently?"

**AI responds:**
```
📍 Address geocoded successfully: Sanlitun, Chaoyang District, Beijing

🎉 Recent promotions:

1. Taikoo Li Spring Fashion Week (Now - April 10)
   Spring clothing 50% off, spend 1000 get 200 off

2. Starbucks New Store Opening (Now - March 31)
   Buy one get one free on all drinks

...
```

## 📁 Directory Structure

```
map-query/
├── SKILL.md      # Skill definition
├── CLAUDE.md      # Core instructions (auto-injected)
├── README.md     # This file
├── INSTALL.md    # Detailed installation guide
├── EXAMPLES.md   # Usage examples
└── scripts/      # (Reserved) Query scripts directory
```

## 🛠️ Available Scripts

- `scripts/geocode.mjs` - Address geocoding
- `scripts/search.mjs` - Nearby search
- `scripts/food.mjs` - Food search
- `scripts/promotion.mjs` - Promotion search

## 🔗 Reference Project

- 12306 Skill: https://github.com/kirorab/12306-skill

---

**New skill created successfully!** 🎉

📝 Review Note:
- Please check if skill functionality meets expectations
- API Key configuration needs to be set by the user
- Confirm before putting into production use
