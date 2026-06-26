# 行程规划工具参数参考

## generate_travel_itinerary 完整参数

```json
{
  "destination": "成都",
  "days": 5,
  "start_date": "2026-03-15",
  "budget": 6000,
  "preferences": {
    "interests": ["food", "culture", "nature"],
    "pace": "moderate",
    "accommodation_type": "mid-range",
    "prefer_public_transport": true
  },
  "mapProvider": "auto"
}
```

### interests 选项

| 值 | 含义 | 倾向 |
|----|------|------|
| `nature` | 自然风光 | 公园、山水、湖泊 |
| `culture` | 文化历史 | 博物馆、古迹、寺庙 |
| `food` | 美食 | 当地特色餐厅、小吃街 |
| `shopping` | 购物 | 商圈、夜市、特产 |
| `nightlife` | 夜生活 | 酒吧街、夜景 |
| `adventure` | 冒险 | 户外运动、徒步 |

### pace 选项

| 值 | 景点/天 | 适合人群 |
|----|---------|----------|
| `relaxed` | 2-3 | 老人、亲子、度假 |
| `moderate` | 3-4 | 大多数旅行者 |
| `fast` | 4-5 | 时间紧凑、年轻人 |

### accommodation_type 选项

| 值 | 价格区间（参考） |
|----|------------------|
| `budget` | ¥100-300/晚 |
| `mid-range` | ¥300-800/晚 |
| `luxury` | ¥800+/晚 |

### mapProvider 选项

| 值 | 说明 |
|----|------|
| `auto` | 默认，国内用高德，国际自动切换 |
| `amap` | 强制使用高德（中国大陆） |
| `google` | 强制使用 Google Maps（需 API Key） |

## search_attractions 完整参数

```json
{
  "city": "北京",
  "keywords": "博物馆",
  "types": ["历史", "文化"],
  "min_rating": 4.0,
  "max_results": 10,
  "sort_by": "rating"
}
```

## calculate_travel_budget 完整参数

```json
{
  "destination": "成都",
  "days": 5,
  "budget_total": 6000,
  "accommodation_cost": 1500,
  "transportation_cost": 1000,
  "daily_food_budget": 200,
  "activities": [
    { "name": "大熊猫基地门票", "price": 55 },
    { "name": "武侯祠门票", "price": 50 },
    { "name": "青城山门票", "price": 80 }
  ]
}
```

不提供具体费用时，工具会根据目的地自动估算。

## search_hotels 完整参数

```json
{
  "city": "成都",
  "check_in": "2026-03-15",
  "check_out": "2026-03-20",
  "guests": 2,
  "min_price": 200,
  "max_price": 500,
  "star_rating": 4,
  "location_preference": "市中心"
}
```

## search_flights 完整参数

```json
{
  "origin": "北京",
  "destination": "成都",
  "departure_date": "2026-03-15",
  "return_date": "2026-03-20",
  "passengers": 2,
  "cabin_class": "economy",
  "max_price": 2000,
  "direct_only": false
}
```

## optimize_daily_route 完整参数

```json
{
  "start_point": "成都春熙路酒店",
  "end_point": "成都春熙路酒店",
  "waypoints": [
    { "name": "宽窄巷子", "location": "成都市青羊区宽窄巷子", "duration": 90 },
    { "name": "人民公园", "location": "成都市青羊区少城路12号", "duration": 60 },
    { "name": "武侯祠", "location": "成都市武侯区武侯祠大街231号", "duration": 90, "priority": 5 },
    { "name": "锦里", "location": "成都市武侯区武侯祠大街231号附1号", "duration": 60 }
  ],
  "start_time": "09:00",
  "travel_mode": "transit",
  "city": "成都"
}
```

求解 TSP（旅行商问题）的变体，找到最优访问顺序。支持时间窗口和优先级约束。
