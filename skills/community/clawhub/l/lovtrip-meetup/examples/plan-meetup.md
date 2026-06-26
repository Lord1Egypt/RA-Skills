# 多人聚会规划示例

## 场景：3 人周末咖啡聚会

### 用户输入

> 我在中关村，小明在望京，小红在西单，这周六下午想找个咖啡馆坐坐，人均不超过 80 元

### 规划流程

**第 1 步 — 解析时间**

```
→ parse_schedule({ text: "这周六下午" })
← { start: "2026-03-14T13:00:00", end: "2026-03-14T18:00:00", type: "afternoon" }
```

**第 2 步 — 推荐地点**

```
→ amap_find_optimal_venue({
    members: [
      { name: "我", location: "中关村" },
      { name: "小明", location: "望京" },
      { name: "小红", location: "西单" }
    ],
    activity_type: "咖啡馆",
    preferences: { budget: { max_price: 80 }, sort_by: "balanced" },
    city: "北京"
  })
← {
    recommended: [
      {
        name: "% Arabica 三里屯店",
        score: 0.87,
        rating: 4.5,
        commute_times: { "我": "35min", "小明": "25min", "小红": "20min" }
      },
      ...
    ]
  }
```

**第 3 步 — 检查天气**

```
→ check_weather({ location: { lng: 116.45, lat: 39.93 }, city: "北京", date: "2026-03-14" })
← { weather: "多云", temperature: "12-18°C", suggestion: "适合户外活动" }
```

**第 4 步 — 生成方案**

```
→ generate_plan({
    time_slot: { start: "2026-03-14T14:00:00", end: "2026-03-14T17:00:00" },
    venue: { name: "% Arabica 三里屯店", address: "...", location: { lng: 116.45, lat: 39.93 } },
    activities: ["咖啡"],
    members: ["我", "小明", "小红"]
  })
```

**第 5 步 — 生成链接**

```
→ generate_map_links({
    venue: { name: "% Arabica 三里屯店", address: "...", location: { lng: 116.45, lat: 39.93 } },
    members: [
      { name: "我", location: { lng: 116.32, lat: 39.98 } },
      { name: "小明", location: { lng: 116.47, lat: 40.00 } },
      { name: "小红", location: { lng: 116.37, lat: 39.91 } }
    ]
  })
```

### 最终输出

> **周六咖啡聚会方案**
>
> 📍 % Arabica 三里屯店
> 🕐 14:00 - 17:00
> 🌤 多云 12-18°C
>
> **各位的通勤时间：**
> - 我（中关村）→ 地铁 35 分钟
> - 小明（望京）→ 地铁 25 分钟
> - 小红（西单）→ 地铁 20 分钟
>
> **地图链接：**
> - [高德地图](https://uri.amap.com/marker?...)
> - [Apple 地图](https://maps.apple.com/?...)
