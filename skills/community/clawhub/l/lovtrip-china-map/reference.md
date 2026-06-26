# 高德地图工具参数参考

## 坐标系统

高德地图使用 GCJ-02 坐标系（中国国标），与 WGS-84（GPS）有偏移。

**中国大陆坐标范围**:
- 经度: 73.5° ~ 135.0° E
- 纬度: 18.0° ~ 53.5° N

## POI 类型编码（常用）

| 编码 | 类型 |
|------|------|
| 050000 | 餐饮服务 |
| 060000 | 购物服务 |
| 080000 | 住宿服务 |
| 110000 | 景点 |
| 120000 | 商务住宅 |
| 150000 | 交通设施 |
| 160000 | 金融 |
| 170000 | 科教文化 |

## 路线规划模式

| 模式 | 说明 | 返回信息 |
|------|------|----------|
| `transit` | 公交/地铁 | 换乘方案、步行距离、票价 |
| `driving` | 驾车 | 距离、时长、收费、路况 |
| `walking` | 步行 | 距离、时长、路线 |

## generate_map_links 输出格式

```json
{
  "map_links": {
    "amap": { "link": "https://uri.amap.com/marker?..." },
    "tencent": { "link": "https://apis.map.qq.com/uri/v1/marker?..." },
    "baidu": { "link": "https://api.map.baidu.com/marker?..." },
    "apple": { "link": "https://maps.apple.com/?..." }
  },
  "navigation_links": [
    {
      "member": "Alice",
      "links": {
        "amap": { "link": "https://uri.amap.com/navigation?..." }
      }
    }
  ]
}
```

使用时应提取 URL 格式化为 Markdown 链接：`[高德地图](https://uri.amap.com/marker?...)`

## 缓存策略

| 操作 | TTL | 说明 |
|------|-----|------|
| 地理编码 | 24h | 地址很少变化 |
| 路线规划 | 6h | 交通状况变化较频繁 |
| 周边搜索 | 不缓存 | 结果实时性要求高 |
