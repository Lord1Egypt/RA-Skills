# GIS 格式规范速查手册

> KML/SHP/CAD 格式转换 V1.0 — 坤图_GIS

---

## 一、DWG (.dwg)

Autodesk 私有二进制格式，Python 生态无法原生读取。

| 属性 | 值 |
|------|-----|
| 格式类型 | 二进制 (Autodesk 私有) |
| 坐标系 | 无内建 CRS，依赖外部定义 |
| 属性存储 | 图层(Layer)、块(Block)、扩展数据(XDATA) |
| 转换方案 | ODA File Converter CLI → DXF 中转 |
| 版本标识 | 文件头 6 字节 (AC1018=2004, AC1024=2010, AC1032=2018) |

### ODA File Converter 命令行

```
ODAFileConverter.exe <input_dir> <output_dir> <version> <format> <recurse> <audit> <filter>
```

- **version**: ACAD2018 (常用), ACAD2013, ACAD2010
- **format**: DXF
- **recurse**: 0 (不递归), 1 (递归子目录)
- **audit**: 0 (不修复), 1 (自动修复)
- **filter**: `*.dwg`

---

## 二、DXF (.dxf)

AutoCAD Drawing Exchange Format — 开放式文本交换格式。

| 属性 | 值 |
|------|-----|
| 格式类型 | 文本 (ASCII) 或二进制 |
| 坐标系 | 无标准 CRS 字段，坐标数值存储 |
| 几何支持 | LWPOLYLINE, LINE, CIRCLE, ARC, POINT, INSERT, POLYLINE |
| 属性 | 仅图层名，无属性表 |
| 转换限制 | 属性全部丢失，仅保留几何和图层 |

### DXF → GIS 转换注意事项

1. CIRCLE 自动转为 Polygon(32边近似)
2. ARC 转为 LineString(16段/象限)
3. 闭合 LWPOLYLINE(4+点) → Polygon
4. 块引用(INSERT) → Point(插入点)
5. 按图层(layer)字段可在GIS中分层渲染

---

## 三、Shapefile (.shp)

ESRI 传统矢量格式（多文件组成）。

| 文件 | 作用 |
|------|------|
| `.shp` | 几何数据 |
| `.shx` | 空间索引 |
| `.dbf` | 属性表 (dBASE IV) |
| `.prj` | 坐标系定义 |
| `.cpg` | 编码标识 |

### 限制

- 字段名 ≤ 10 个英文字符（中文字段名可能截断）
- 单个文件 ≤ 2GB
- 不支持 NULL 值区分
- 日期/时间无标准支持
- 推荐替代：**GeoPackage (.gpkg)**

### 编码问题

Shapefile 不强制要求编码标准。中文数据常见 GBK/GB2312：
```bash
python gis_converter.py data.shp output.kml --encoding gbk
```

---

## 四、GeoJSON (.geojson)

WGS84 地理坐标的 JSON 格式。

| 属性 | 值 |
|------|-----|
| CRS | 固定 WGS84 (EPSG:4326) |
| 编码 | UTF-8 |
| 几何类型 | Point, LineString, Polygon, Multi*, GeometryCollection |
| 适用场景 | WebGIS 前端、API 交换 |

---

## 五、KML/KMZ (.kml / .kmz)

Google Earth / 奥维地图 原生格式。

| 属性 | 值 |
|------|-----|
| CRS | WGS84 (EPSG:4326)，经度/纬度/海拔顺序 |
| KMZ | KML 的 ZIP 压缩包 |
| 层级 | Document > Folder > Placemark |
| 注意 | KMZ 内可能有多个 KML，默认取第一个 |

---

## 六、奥维 OVKML (.ovkml)

奥维地图扩展 KML，坐标系为 **GCJ-02**。

| 属性 | 值 |
|------|-----|
| 坐标系 | GCJ-02 (火星坐标) |
| 与标准 KML 差异 | 坐标偏移 ~100-700m (相对于 WGS84) |
| 转换 | 读取时自动 GCJ-02 → WGS84 纠偏 |

---

## 七、奥维 OVJSN (.ovjsn)

奥维 JSON 格式 — 纯文本，便于程序读写。

| 属性 | 值 |
|------|-----|
| 对象类型 | Type=7(点), Type=8(轨迹), Type=9(线), Type=10(面) |
| 坐标系 | GCJ-02 (Gcj02=1 字段标识) |
| 结构 | ObjItems[] > Object > ObjectDetail > PointList[] |
| 转换 | 读写均自动 GCJ-02 纠偏 |

---

## 八、GuoPackage (.gpkg)

OGC 标准格式（Shapefile 推荐替代品）。

| 属性 | 值 |
|------|-----|
| 底层 | SQLite 数据库 |
| 编码 | UTF-8 原生 |
| 字段名 | 无长度限制 |
| 单文件 | 是（含所有图层和索引） |
| 空间索引 | 自动 R-Tree |
| 兼容 | QGIS, ArcGIS Pro, GeoPandas, GDAL |

---

## 九、GeoParquet (.parquet)

列式云原生格式。

| 属性 | 值 |
|------|-----|
| 压缩 | 列式压缩 (10:1 ~ 20:1) |
| 查询 | DuckDB, Pandas, GeoPandas 兼容 |
| 场景 | 大规模空间分析、云存储 |
| 元数据 | JSON GeoParquet metadata |

---

## 十、DJI WPML / WPMZ (.wpmz)

大疆无人机航线规划格式。

| 文件 | 作用 |
|------|------|
| `wpmz/template.kml` | 航线模板(航点坐标+无人机参数) |
| `wpmz/waylines.wpml` | 航线执行详情(动作/高度/速度) |

### DJI 枚举值

设备枚举必须使用 DJI 官方整数值，不能用型号字符串。本工具内置查找表自动映射。

---

## 十一、华测 KML

华测 LandStar GNSS 接收机导出格式。

| 属性 | 值 |
|------|-----|
| 坐标系 | WGS84 |
| 要素类型 | Point, LineString, Polygon |
| 优势 | 可直接导入奥维/Google Earth |

---

## 十二、坐标系对照速查

| 坐标系 | EPSG | 说明 |
|--------|------|------|
| WGS84 | 4326 | GPS 全球坐标系 |
| CGCS2000 | 4490 | 中国现行法定坐标系 |
| Web Mercator | 3857 | 网络地图瓦片 |
| Beijing 1954 | 4214 | 已废除(2008) |
| Xian 1980 | 4610 | 已废除(2018) |
| GCJ-02 | — | 中国火星坐标(无EPSG) |

### CGCS2000 3° 带常用 EPSG

| 中央经线 | EPSG | 覆盖区域 |
|---------|------|---------|
| 105°E | 4544 | 四川盆地 |
| 108°E | 4545 | 陕西南部/重庆 |
| 111°E | 4546 | 湖北/湖南/河南西部 |
| 114°E | 4547 | 河南东部/安徽/江西 |
| 117°E | 4548 | 河北/山东/江苏 |
| 120°E | 4549 | 辽宁/浙江/福建 |

---

<!-- wm:坤图_GIS -->
