---
name: gis-coord-transform
description: GIS 坐标转换工具，支持点/线/面数据在 WGS84（经纬度）和 Web Mercator（墨卡托/EPSG:3857）之间转换。处理 GeoJSON 格式，支持批量转换。Use when: (1) 需要转换 GIS 数据坐标系，(2) WebGIS 项目需要墨卡托投影，(3) 处理 GPS 数据转地图显示，(4) 转换 Shapefile/GeoJSON 等矢量数据。
license: MIT
---

# GIS 坐标转换 Skill

快速转换点、线、面数据的坐标系：**WGS84（经纬度）↔ Web Mercator（EPSG:3857）**

## 快速开始

### 转换 GeoJSON 到墨卡托
```bash
python3 ~/.openclaw/workspace/skills/gis-coord-transform/scripts/transform_coords.py input.geojson -t mercator -o output.geojson --pretty
```

### 转换墨卡托回经纬度
```bash
python3 ~/.openclaw/workspace/skills/gis-coord-transform/scripts/transform_coords.py input.geojson -t wgs84 -o output.geojson --pretty
```

## 支持的几何类型

| 类型 | 说明 |
|------|------|
| Point | 点 |
| LineString | 线 |
| Polygon | 面 |
| MultiPoint | 多点 |
| MultiLineString | 多线 |
| MultiPolygon | 多面 |
| Feature | GeoJSON 要素 |
| FeatureCollection | 要素集合 |

## 命令行参数

| 参数 | 说明 |
|------|------|
| `input` | 输入 GeoJSON 文件路径 |
| `-o, --output` | 输出文件路径（默认输出到 stdout） |
| `-t, --to` | 目标坐标系：`mercator` 或 `wgs84` |
| `--pretty` | 美化输出 JSON |

## 使用示例

### 示例 1：转换单个点
```json
// input.geojson
{
  "type": "Point",
  "coordinates": [116.4074, 39.9042]
}
```

```bash
python3 scripts/transform_coords.py input.geojson -t mercator
```

输出（墨卡托坐标）：
```json
{
  "type": "Point",
  "coordinates": [12958396.7, 4865942.3]
}
```

### 示例 2：转换 FeatureCollection
```bash
python3 scripts/transform_coords.py cities.geojson -t mercator -o cities_mercator.geojson --pretty
```

### 示例 3：批量转换
```bash
for file in *.geojson; do
  python3 scripts/transform_coords.py "$file" -t mercator -o "${file%.geojson}_mercator.geojson"
done
```

## 依赖安装

```bash
pip3 install pyproj
```

## 坐标系说明

| 坐标系 | EPSG 代码 | 用途 |
|--------|----------|------|
| WGS84 | EPSG:4326 | GPS、经纬度、地理坐标 |
| Web Mercator | EPSG:3857 | Web 地图（Google Maps、OpenStreetMap、Mapbox 等） |

## 常见问题

### 为什么转换后坐标数字变大了？
Web Mercator 使用米为单位，而 WGS84 使用度。墨卡托坐标通常在百万级别。

### 转换精度如何？
使用 pyproj 库，精度非常高，适合专业 GIS 应用。

### 支持其他坐标系吗？
当前版本仅支持 WGS84 ↔ Web Mercator。如需其他坐标系，可扩展 `pyproj.Transformer`。

## 扩展建议

需要添加其他坐标系转换时，修改脚本中的 Transformer 定义：

```python
# 例如：WGS84 → CGCS2000 (EPSG:4490)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:4490", always_xy=True)
```

## 相关文件

- `scripts/transform_coords.py` - 坐标转换主脚本
