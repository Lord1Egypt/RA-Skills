# Python GIS 开源生态 | 关联：12_ArcGIS_Pro.md 18_FME_Form与Flow.md 13_QGIS.md | 来源：旧第十七篇Python部分 + 新纲要Part2.4

> Python GIS 完整技术栈：矢量(GDAL/OGR) → 分析与几何(Shapely/GeoPandas) → 空间统计(PySAL) → 高级应用(PDAL/Rasterio)
> 安装/操作/场景速查，可直接复制运行

---

## 一、Python GIS 技术栈（三层架构）

```
┌──────────────────────────────────┐
│  高级应用层（一站式）            │
│  GeoPandas / xarray              │
├──────────────────────────────────┤
│  领域库层                        │
│  Shapely(几何) / Rasterio(栅格)   │
│  Pyproj(投影) / Fiona(读写)       │
│  PySAL(统计) / Folium(可视化)     │
│  PDAL(点云) / laspy(LiDAR)        │
├──────────────────────────────────┤
│  底层引擎层                      │
│  GDAL / OGR / PROJ / GEOS        │
└──────────────────────────────────┘
```

---

## 二、核心库速查（2026年6月 最新验证）

### 2.1 GDAL/OGR —— 万能读写引擎

| 命令/API | 说明 |
|---------|------|
| `gdalwarp -t_srs EPSG:4490 input.tif output.tif` | 栅格重投影 |
| `gdal_translate -projwin xmin ymax xmax ymin input.tif output.tif` | 按范围裁剪 |
| `gdal_merge.py -o merged.tif *.tif` | 多幅栅格合并 |
| `ogr2ogr -f "GPKG" output.gpkg input.shp` | 矢量格式转换 |
| `ogr2ogr -t_srs EPSG:4490 output.shp input.shp` | 矢量投影转换 |
| `gdal2tiles.py -z 10-18 input.tif output_folder/` | 生成瓦片金字塔 |

### 2.2 GeoPandas —— 矢量数据分析

```python
import geopandas as gpd

# 读取数据（支持SHP/GeoJSON/GPKG/PostGIS）
gdf = gpd.read_file(r"D:\data\roads.shp", encoding="utf-8")
# 中文GBK乱码时：gdf = gpd.read_file("file.shp", encoding="gbk")

# 坐标系统一
gdf = gdf.to_crs("EPSG:4490")  # CGCS2000

# 空间筛选
aoi = gpd.read_file("aoi.shp")
roads_in_aoi = gpd.sjoin(gdf, aoi, predicate="intersects")

# 缓冲区
gdf["buffer_100m"] = gdf.buffer(100)

# 面积计算（必须先转为等面积投影！）
area_m2 = gdf.to_crs("EPSG:102025").area  # Albers等积投影

# 写入
gdf.to_file("output.gpkg", driver="GPKG", encoding="utf-8")
# 性能优化：大数据量用 Parquet 中间存储
gdf.to_parquet("intermediate.parquet")
```

### 2.3 Shapely —— 几何运算

| 功能 | 代码 |
|------|------|
| 创建几何 | `from shapely.geometry import Point, LineString, Polygon` |
| 面积/长度 | `polygon.area` / `line.length` |
| 判断相交 | `geom1.intersects(geom2)` |
| 求交集 | `geom1.intersection(geom2)` |
| 几何简化 | `geom.simplify(tolerance)` |
| 修复无效几何 | `from shapely.validation import make_valid` |
| 凸包 | `geom.convex_hull` |
| 缓冲区 | `geom.buffer(distance)` |
| Voronoi | `shapely.ops.voronoi_diagram(points)` |
| Delaunay三角 | `shapely.ops.triangulate(geom)` |

### 2.4 Rasterio —— 栅格数据处理

```python
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

# 打开栅格
with rasterio.open("dem.tif") as src:
    dem = src.read(1)  # 读取第一个波段
    profile = src.profile
    bounds = src.bounds
    crs = src.crs

# 裁剪到范围
from rasterio.mask import mask
with rasterio.open("input.tif") as src:
    out_image, out_transform = mask(src, [aoi.geometry], crop=True)

# 重投影
dst_crs = "EPSG:4490"
transform, width, height = calculate_default_transform(
    src.crs, dst_crs, src.width, src.height, *src.bounds)
reproject(source=dem, destination=output_array, ...)

# 分块处理（避免内存溢出）
for window in src.block_windows(1):
    block = src.read(1, window=window)
```

### 2.5 Pyproj —— 坐标转换

```python
from pyproj import Transformer, CRS

# 检查EPSG信息
crs = CRS.from_epsg(4490)
print(crs.name)  # "CGCS2000"

# 创建坐标转换器
transformer = Transformer.from_crs("EPSG:4326", "EPSG:4490")
lon, lat = 116.39, 39.91
x, y = transformer.transform(lat, lon)  # 注意：输入(lat,lon)，输出(x,y)
```

### 2.6 PySAL —— 空间统计

```python
import pysal
from pysal.lib import weights
from pysal.explore import esda

# 空间权重矩阵
w = weights.KNN.from_dataframe(gdf, k=8)

# Moran's I 空间自相关
moran = esda.Moran(gdf["字段"], w)
print(f"I={moran.I:.4f}, p={moran.p_sim:.4f}")

# LISA 局部自相关
lisa = esda.Moran_Local(gdf["字段"], w)

# Getis-Ord Gi* 热点分析
gi_star = esda.G_Local(gdf["字段"], w)
```

### 2.7 Fiona —— 轻量矢量读写

```python
import fiona

# 查看图层信息
with fiona.open("data.shp", encoding="utf-8") as src:
    print(src.schema)   # 字段结构
    print(src.crs)      # 坐标系
    print(len(src))     # 要素数量
```

### 2.8 Folium —— 交互式地图可视化

```python
import folium

m = folium.Map(location=[39.91, 116.39], zoom_start=12)
folium.GeoJson(gdf).add_to(m)
m.save("map.html")
```

### 2.9 xarray + rioxarray —— 多维栅格

```python
import xarray as xr
import rioxarray

# 打开多维NetCDF数据
ds = xr.open_dataset("climate.nc")
ds.rio.set_spatial_dims("lon", "lat")
ds.rio.write_crs("EPSG:4326")

# 时间序列分析
temp_annual = ds["temperature"].groupby("time.year").mean()
```

### 2.10 PDAL —— 点云处理

```python
import pdal
import json

pipeline = [
    {"type": "readers.las", "filename": "cloud.las"},
    {"type": "filters.smrf"},  # 地面滤波
    {"type": "writers.las", "filename": "classified.las",
     "extra_dims": "all"}
]
pdal.Pipeline(json.dumps(pipeline)).execute()
```

---

## 三、GDAL CLI 命令速查

| 命令 | 功能 | 示例 |
|------|------|------|
| `gdalwarp` | 栅格重投影/裁剪/重采样 | `gdalwarp -t_srs EPSG:4490 -tr 30 30 in.tif out.tif` |
| `gdal_translate` | 格式转换/按范围裁剪 | `gdal_translate -of GTiff -projwin xmin ymax xmax ymin in.jp2 out.tif` |
| `gdal_merge.py` | 多幅栅格合并 | `gdal_merge.py -o merged.tif tile*.tif` |
| `gdal_calc.py` | 栅格计算器 | `gdal_calc.py -A dem.tif --calc="A>100" --outfile mask.tif` |
| `gdaldem` | 山体阴影/坡度/坡向 | `gdaldem hillshade dem.tif shade.tif` |
| `gdal_contour` | DEM生成等高线 | `gdal_contour -i 10 dem.tif contour.shp` |
| `gdal2tiles.py` | 生成XYZ瓦片 | `gdal2tiles.py -z 10-18 map.tif tiles/` |
| `ogr2ogr` | 矢量格式/坐标系转换 | `ogr2ogr -f "GPKG" -t_srs EPSG:4490 out.gpkg in.shp` |

---

## 四、环境配置

```bash
# 推荐：使用 conda 或 mamba 创建专用环境
conda create -n gis python=3.11
conda activate gis

# 核心库
pip install geopandas shapely fiona pyproj rasterio
pip install xarray rioxarray netcdf4

# 可选
pip install folium pysal laspy pdal
pip install earthengine-api  # GEE
```

> **注意**：ArcPy 必须使用 ArcGIS Pro 自带 Python 解释器（`C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3`），不兼容 conda 环境。

---

## 五、常见错误与解决

| 错误 | 原因 | 解决 |
|------|------|------|
| `ImportError: DLL load failed` | GDAL/Rasterio 依赖缺失 | 安装 OSGeo4W 或使用 conda |
| `UnicodeDecodeError` | Shapefile编码非UTF-8 | `gpd.read_file("f.shp", encoding="gbk")` |
| `MemoryError`（大栅格） | 一次性读取整个影像 | 使用 `rasterio.windows` 分块读取 |
| GeoPandas buffer 单位错误 | 地理坐标系下直接计算 | 先 `to_crs()` 到投影坐标系 |
| `CRSError: Invalid projection` | EPSG代码错误 | 用 `pyproj.CRS.from_epsg()` 验证 |

---

> 关联阅读：`12_ArcGIS_Pro.md` 第十二篇（ArcPy完整参考） | `18_FME_Form与Flow.md`（FME Python脚本替代） | `24_遥感与GEE.md`（PDAL/Rasterio/点云处理完整章节）


<!-- wm:坤图_GIS:V1.0 -->
