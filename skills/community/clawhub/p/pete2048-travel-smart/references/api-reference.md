# TravelSmart API 参考

## 基础信息

- 端口：`5188`
- 基础 URL：`http://localhost:5188`

## 接口列表

### 1. 高速出口推荐

```
POST /api/travel-smart/highway
```

**请求体：**
```json
{
  "highway": "G4",
  "lng": 116.397,
  "lat": 39.909,
  "destination": "北京"
}
```

**响应：**
```json
{
  "scene": "highway",
  "highway": "G4",
  "exits": [
    {
      "name": "前门出口(南二环东向)",
      "distance": 3200,
      "detour": 800,
      "rating": 4.8,
      "score": 94.8,
      "dining_pois": [
        {"name": "麦当劳(前门店)"},
        {"name": "肯德基"}
      ]
    }
  ]
}
```

### 2. 住宿推荐

```
POST /api/travel-smart/hotel
```

**请求体：**
```json
{
  "lng": 116.397,
  "lat": 39.909,
  "budget": 300,
  "people": 2,
  "nextLng": 116.404,
  "nextLat": 39.915
}
```

### 3. 打车点推荐

```
POST /api/travel-smart/taxi
```

**请求体：**
```json
{
  "lng": 116.397,
  "lat": 39.909,
  "destLng": 116.404,
  "destLat": 39.915
}
```

### 4. 地理编码

```
POST /api/travel-smart/geocode
```

**请求体：**
```json
{ "address": "北京天安门" }
```

**响应：**
```json
{
  "lng": 116.397,
  "lat": 39.909,
  "formatted": "北京市东城区天安门"
}
```

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `AMAP_KEY` | **必填** | 高德地图 Web API Key（申请：https://console.amap.com/dev/key/app） |
| `MINIMAX_API_KEY` | 可选 | MiniMax LLM（自然语言路由用） |
| `FEISHU_APP_ID` | 可选 | 飞书推送用 |
| `FEISHU_APP_SECRET` | 可选 | 飞书推送用 |
