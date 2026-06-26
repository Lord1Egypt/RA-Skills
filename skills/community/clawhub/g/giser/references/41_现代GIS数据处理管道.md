# 现代GIS数据处理管道

> 来源：open-gis-main 项目（processing / validation-and-ops / analytics 三文档综合）
> 最后更新：2026-06-04 | 验证级别：专家级（Expert）
> 群组归属：群组六 — 现代GIS技术栈
> 交叉引用：←→ 03_数据模型与格式.md、←→ 22_空间数据库.md、←→ 23_WebGIS开发.md、←→ 33_空间分析与统计.md、←→ 35_专家级批量处理与自动化实战指南.md

---

## 目录

1. [现代GIS技术栈（2026）](#一现代gis技术栈2026)
2. [七大标准处理管道模式](#二七大标准处理管道模式)
3. [处理工具选型矩阵](#三处理工具选型矩阵)
4. [输出验证清单](#四输出验证清单)
5. [CRS与几何门禁检查](#五crs与几何门禁检查)
6. [可复现性要求](#六可复现性要求data-manifestjson)
7. [12大反模式（Anti-Patterns）](#七12大反模式anti-patterns)
8. [Shell脚本最佳实践](#八shell脚本最佳实践)

---

## 一、现代GIS技术栈（2026）

### 1.1 完整技术栈架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                      现代GIS技术栈全景                            │
├──────────┬──────────┬──────────┬────────────┬──────────────────┤
│  数据源   │   处理    │   存储    │   服务     │     可视化        │
│  Data    │Process   │ Storage  │  Serving   │  Visualization    │
├──────────┼──────────┼──────────┼────────────┼──────────────────┤
│Overture  │DuckDB    │GeoParquet│Martin      │MapLibre GL JS    │
│  Maps    │  Spatial │          │            │                  │
│Sentinel  │xarray +  │Cloud     │TiTiler     │Deck.gl           │
│  STAC    │  dask    │Optimized │            │                  │
│OpenStr...│PostGIS   │GeoTIFF   │            │                  │
│  Map PBF │          │(COG)     │pg_tileserv │Leaflet           │
│Global    │PDAL      │PMTiles   │Static S3   │OpenLayers        │
│  DEM/DSM │          │          │            │                  │
│WorldPop  │Apache    │FlatGeo...│MapLibre    │Three.js / Cesium │
│/GHSL     │  Sedona  │          │GL Native   │                  │
│OGC API   │r5py /    │PostGIS   │Static COG  │Kepler.gl         │
│Features  │  Valhalla│          │            │                  │
└──────────┴──────────┴──────────┴────────────┴──────────────────┘
```

### 1.2 传统栈 vs 现代栈 全面对比

| 维度 | 传统栈（2015） | 现代栈（2026） |
|------|---------------|---------------|
| **矢量格式** | Shapefile (.shp/.dbf/.shx) | GeoParquet (.parquet) |
| **栅格格式** | GeoTIFF（单文件） | Cloud Optimized GeoTIFF (COG) |
| **瓦片格式** | MBTiles (.mbtiles) | PMTiles (.pmtiles) |
| **空间数据库** | ArcGIS Geodatabase / Oracle Spatial | DuckDB Spatial / PostGIS |
| **分析引擎** | ArcGIS Desktop / ArcPy | DuckDB + GeoPandas + xarray |
| **地图服务** | ArcGIS Server + ArcGIS REST API | Martin / TiTiler / 静态S3 |
| **前端渲染** | ArcGIS JavaScript API / OpenLayers 3 | MapLibre GL JS / Deck.gl |
| **批量处理** | ModelBuilder / Python (arcpy) | SQL + Makefile + shell 脚本 |
| **分发方式** | 文件拷贝 / ArcGIS Online | Cloud-Native (HTTP Range Requests) |
| **许可模式** | 商业许可 | 开源 + SaaS |
| **可复现性** | 手动记录（或无记录） | data-manifest.json + 固定版本 |

### 1.3 为什么这场迁移至关重要

| 驱动力 | 说明 |
|--------|------|
| **云原生（Cloud-Native）** | COG/PMTiles/GeoParquet 支持 HTTP Range Requests，无需下载全文件即可按需读取 |
| **成本** | 开源工具栈消除 ArcGIS Server 许可费用；静态文件托管比 GeoServer 运维成本低 10-50 倍 |
| **可复现性** | 纯代码管线 + 固定版本 + manifest.json，任何人都可重跑（←→ 35_专家级批量处理.md） |
| **可扩展性** | DuckDB 单机处理 5000 万条记录；Apache Sedona 可扩展到数十亿条 |
| **互操作性** | OGC 标准格式（GeoParquet/COG/STAC）可在任何工具间流转，无厂商锁定 |
| **性能** | DuckDB Spatial 在空间连接上比传统工具快 10-100 倍；PMTiles 单文件即服务 |

### 1.4 工具选择心智模型

**核心原则：CLI 用于一次性任务，DuckDB 用于分析，PostGIS 用于服务，Python 用于粘合层和 ML。**

| 任务场景 | 首选工具 |
|---------|---------|
| 单次格式转换/重投影 | GDAL/OGR CLI（gdalwarp, ogr2ogr） |
| 迭代分析，<5000 万条记录 | DuckDB Spatial（Notebook 或脚本中） |
| 生产级查询层，多用户 | PostGIS |
| 多波段栅格时序，lazy/dask 支持 | xarray + rioxarray + odc-stac |
| Python 中的矢量处理 | GeoPandas（Shapely 2.x 后端） |
| 真正分布式（>1 亿条记录，多节点） | Apache Sedona |
| 点云处理 | PDAL pipelines |
| 网络/可达性分析 | r5py / Valhalla |
| 地形/水文分析 | WhiteboxTools / GRASS / gdaldem |

---

## 二、七大标准处理管道模式

### 管道 1：Source → DuckDB → Analysis → Tiles ★★★

**适用场景**：从 Overture Maps 等云数据源提取、分析并发布矢量瓦片。

**完整流程**：

```
Overture S3 GeoParquet
    ↓ DuckDB 查询（bbox 过滤 + CRS 转换）
    ↓ ST_AsMVT 或写出 GeoParquet → tippecanoe
    ↓ PMTiles
    ↓ Martin / 静态 S3
    ↓ MapLibre GL JS
```

**步骤 1：设置 DuckDB 环境**

```sql
INSTALL spatial; LOAD spatial;
INSTALL httpfs; LOAD httpfs;
INSTALL h3 FROM community; LOAD h3;
```

**步骤 2：从 Overture S3 读取数据**

```sql
-- 读取 Overture 建筑物数据，利用 bbox 列做谓词下推
-- 注意：必须固定 OVERTURE_RELEASE 版本号，禁止使用 "latest"
SELECT id, names.primary AS name,
       ST_Transform(geometry, 'OGC:CRS84', 'EPSG:3301', always_xy := true) AS geom_3301
FROM read_parquet(
  's3://overturemaps-us-west-2/release/2025-01-22.0/theme=buildings/type=building/*.parquet'
)
WHERE bbox.xmin > 24.5 AND bbox.xmax < 25.0
  AND bbox.ymin > 59.3 AND bbox.ymax < 59.5;
```

**步骤 3：空间分析与聚合**

```sql
-- 在度量 CRS 中做距离/面积计算
WITH buildings AS (
  SELECT id, name,
    ST_Transform(geometry, 'OGC:CRS84', 'EPSG:3301', always_xy := true) AS geom
  FROM read_parquet('buildings.parquet')
),
roads AS (
  SELECT id,
    ST_Transform(geometry, 'OGC:CRS84', 'EPSG:3301', always_xy := true) AS geom
  FROM read_parquet('roads.parquet')
)
SELECT b.id, b.name, b.geom,
       count(r.id) AS nearby_roads,
       ST_Area(b.geom) AS area_m2
FROM buildings b
LEFT JOIN roads r ON ST_DWithin(b.geom, r.geom, 200)
GROUP BY b.id, b.name, b.geom;
```

**步骤 4：导出为 GeoParquet**

```sql
COPY (SELECT id, name, ST_Transform(geom, 'EPSG:3301', 'EPSG:4326', always_xy := true) AS geometry
      FROM analysis_result)
TO 'result.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);
```

**步骤 5：转换为 PMTiles**

```bash
tippecanoe -o output.pmtiles \
  -Z 10 -z 16 \
  -l buildings \
  --drop-densest-as-needed \
  --coalesce-densest-as-needed \
  result.parquet
```

**步骤 6：服务与渲染**

```bash
# 方式 A：Martin 动态服务
martin output.pmtiles

# 方式 B：静态 S3 + MapLibre
# 上传 output.pmtiles 到 S3，前端通过 PMTiles 协议直接读取
```

```javascript
// MapLibre 前端配置
const protocol = new pmtiles.Protocol();
maplibregl.addProtocol('pmtiles', protocol.tile);

const map = new maplibregl.Map({
  container: 'map',
  style: {
    sources: {
      buildings: {
        type: 'vector',
        url: 'pmtiles://https://my-bucket.s3.amazonaws.com/output.pmtiles'
      }
    }
  }
});
```

> **关键提示**：Overture 公共桶仅保留最近几个 release。如需长期可复现，必须镜像（mirror）所需 release 版本。

---

### 管道 2：Sentinel STAC → xarray → COG → Tiles ★★★★

**适用场景**：从 Sentinel-2 STAC 目录搜索影像，计算植被/水体指数，生成时间序列分析产品。

**完整流程**：

```
pystac-client 搜索（cloud<20%）
    ↓ odc.stac.load（lazy, dask 支持）
    ↓ 计算指数（NDVI, NDWI, NDBI 等）
    ↓ 时间维归约
    ↓ rio-cogeo 写出
    ↓ TiTiler 动态切片 OR 预切至 PMTiles
```

**步骤 1：STAC 搜索**

```python
from pystac_client import Client
import planetary_computer

client = Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)

items = client.search(
    collections=["sentinel-2-l2a"],
    bbox=[24.5, 59.3, 25.0, 59.5],
    datetime="2025-06-01/2025-08-31",
    query={"eo:cloud_cover": {"lt": 20}},
).item_collection()

print(f"找到 {len(items)} 景影像")
```

**步骤 2：lazy load + 云掩膜**

```python
import odc.stac

ds = odc.stac.load(
    items,
    bands=["B03", "B04", "B08", "B11", "SCL"],
    chunks={"x": 1024, "y": 1024},
    resolution=10,
    crs="EPSG:3301",
    bbox=[24.5, 59.3, 25.0, 59.5],
)

# SCL 云掩膜：排除 NoData/Saturated/CloudShadow/CloudMedium/CloudHigh/ThinCirrus
mask = ~ds.SCL.isin([0, 1, 3, 8, 9, 10])
clean = ds.where(mask)
```

**步骤 3：计算多指数**

```python
# 植被指数
ndvi = (clean.B08 - clean.B04) / (clean.B08 + clean.B04)

# 水体指数（McFeeters）
ndwi = (clean.B03 - clean.B08) / (clean.B03 + clean.B08)

# 城市水体指数（urban-resistant）
mndwi = (clean.B03 - clean.B11) / (clean.B03 + clean.B11)

# 植被水分指数（Gao）
ndmi = (clean.B08 - clean.B11) / (clean.B08 + clean.B11)

# 建筑指数
ndbi = (clean.B11 - clean.B08) / (clean.B11 + clean.B08)
```

**步骤 4：时间归约 + 写出 COG**

```python
# 最大值合成（常用）
ndvi_max = ndvi.max(dim="time").compute()

# 中值合成（抗云）
ndvi_median = ndvi.median(dim="time").compute()

# 写出 Cloud Optimized GeoTIFF
ndvi_max.rio.to_raster(
    "ndvi_max_2025_summer.tif",
    driver="COG",
    compress="DEFLATE",
    overview_resampling="average"
)

ndvi_median.rio.to_raster(
    "ndvi_median_2025_summer.tif",
    driver="COG",
    compress="DEFLATE",
    overview_resampling="average"
)
```

**步骤 5：验证 COG**

```bash
rio cogeo validate ndvi_max_2025_summer.tif
gdalinfo ndvi_max_2025_summer.tif
```

**步骤 6：动态服务（TiTiler）**

```bash
# 启动 TiTiler 服务
uvicorn titiler.application.main:app --host 0.0.0.0 --port 8000

# 前端通过 URL 参数动态请求瓦片
# /cog/tiles/{z}/{x}/{y}?url=file:///path/to/ndvi_max_2025_summer.tif
```

**备选：预切为静态 PMTiles**

```bash
# TiTiler 可生成静态栅格 PMTiles
# 或使用 rio-tiler 直接生成
```

---

### 管道 3：OSM → PostGIS → Application ★★★

**适用场景**：从 OpenStreetMap 提取完整路网/建筑物/POI 数据，建立生产级 PostgreSQL 空间数据库。

**完整流程**：

```
Geofabrik PBF 下载
    ↓ osm2pgsql --slim -G 导入
    ↓ 创建 GIST 空间索引
    ↓ 应用 SQL 查询分析
    ↓ 可选：MVT 矢量瓦片（Martin 或 pg_tileserv）
```

**步骤 1：下载 OSM 数据**

```bash
# 以爱沙尼亚为例
wget https://download.geofabrik.de/europe/estonia-latest.osm.pbf -P data/

# 记录下载时间戳（用于可复现性）
stat data/estonia-latest.osm.pbf > data/source_timestamp.txt
```

**步骤 2：导入 PostGIS**

```bash
osm2pgsql \
  --slim \
  --drop \
  --create \
  --database=gis \
  --username=postgres \
  --host=localhost \
  --style=openstreetmap-carto.style \
  --multi-geometry \
  --hstore \
  --tag-transform-script=style.lua \
  data/estonia-latest.osm.pbf
```

关键参数说明：

| 参数 | 说明 |
|------|------|
| `--slim` | 存储中间表，支持增量更新 |
| `--multi-geometry` | 统一为 MULTI* 类型 |
| `--hstore` | 所有 tags 存入 hstore 列 |
| `-G` | 使用 flex 模式输出并创建 GIST 索引 |

**步骤 3：构建空间索引**

```sql
-- osm2pgsql 会自动创建基础 GIST 索引
-- 手动补充业务索引

-- 建筑物在 3301 投影下的索引（用于距离查询）
CREATE INDEX idx_buildings_geom_3301 ON planet_osm_polygon
  USING GIST (ST_Transform(way, 3301))
  WHERE building IS NOT NULL;

-- 道路名称全文搜索
CREATE INDEX idx_roads_name ON planet_osm_line
  USING GIN (to_tsvector('english', name))
  WHERE name IS NOT NULL;

-- BRIN 索引：超大表的廉价索引
CREATE INDEX idx_points_brin ON planet_osm_point
  USING BRIN (way) WITH (pages_per_range = 32);
```

**步骤 4：测试索引有效性**

```sql
-- 验证索引是否被使用
EXPLAIN ANALYZE
SELECT osm_id, name, building
FROM planet_osm_polygon
WHERE building IS NOT NULL
  AND ST_Intersects(
    way,
    ST_MakeEnvelope(24.5, 59.3, 25.0, 59.5, 4326)
  );
-- 期望输出中看到 "Index Scan using idx_planet_osm_polygon_way"
```

**步骤 5：应用分析查询**

```sql
-- 空间连接：每个建筑物属于哪个行政区
SELECT b.osm_id, b.name AS building_name,
       d.name AS district_name
FROM planet_osm_polygon b
JOIN planet_osm_polygon d
  ON ST_Within(b.way, d.way)
WHERE b.building IS NOT NULL
  AND d.admin_level = '8';
```

**步骤 6：矢量瓦片生成（Martin）**

```bash
# 方式 A：Martin 直接连接 PostGIS
martin \
  --postgresql-dsn "postgresql://postgres@localhost/gis" \
  --listen-addresses 0.0.0.0:3000

# 前端请求：http://localhost:3000/public.planet_osm_polygon/{z}/{x}/{y}
```

**SQL 内联瓦片生成**（供高级定制）：

```sql
SELECT ST_AsMVT(tile, 'buildings', 4096, 'geom')
FROM (
  SELECT osm_id, name,
         ST_AsMVTGeom(
           ST_Transform(way, 3857),
           ST_TileEnvelope(14, 9600, 6000),
           4096, 64, true
         ) AS geom
  FROM planet_osm_polygon
  WHERE building IS NOT NULL
    AND way && ST_Transform(ST_TileEnvelope(14, 9600, 6000), 4326)
) AS tile;
```

---

### 管道 4：Point Cloud → Classification → Products ★★★★

**适用场景**：从 LiDAR 点云提取数字地形模型(DTM)、数字表面模型(DSM)和冠层高度模型(CHM)，并计算建筑物高度。

**完整流程**：

```
1. 检查：pdal info input.laz --stats
2. 地面分类：PDAL filters.smrf
3. 提取 DTM：地面点 → 栅格最小值/TIN
4. 提取 DSM：全部回波 → 栅格最大值
5. 计算 CHM：DSM - DTM
6. 按要素高度：CHM 区域统计
```

**步骤 1：点云质量检查**

```bash
pdal info input.laz             # 基本元数据
pdal info input.laz --stats     # 统计信息
pdal info input.laz --all       # 完整元数据
```

**步骤 2：地面分类（SMRF 算法）**

编写 `ground-classify.json`：

```json
{
  "pipeline": [
    "input.laz",
    {
      "type": "filters.smrf",
      "scalar": 1.2,
      "slope": 0.2,
      "threshold": 0.45,
      "window": 16.0
    },
    {
      "type": "writers.las",
      "filename": "classified.laz",
      "extra_dims": "all"
    }
  ]
}
```

```bash
pdal pipeline ground-classify.json
```

SMRF 参数调优指南：

| 参数 | 含义 | 城市环境推荐 | 山地/森林推荐 |
|------|------|-------------|-------------|
| scalar | 高程阈值缩放 | 1.2 | 1.5 |
| slope | 地形坡度阈值 | 0.2 | 0.5 |
| threshold | 初始高程阈值(m) | 0.45 | 0.8 |
| window | 形态学窗口大小(m) | 16.0 | 30.0 |

**步骤 3：提取 DTM（地面点栅格化）**

编写 `dtm-pipeline.json`：

```json
{
  "pipeline": [
    "classified.laz",
    {
      "type": "filters.range",
      "limits": "Classification[2:2]"
    },
    {
      "type": "writers.gdal",
      "filename": "dtm.tif",
      "resolution": 1.0,
      "output_type": "min",
      "data_type": "float32",
      "nodata": -9999,
      "gdaldriver": "COG"
    }
  ]
}
```

**步骤 4：提取 DSM（全部回波最大值）**

编写 `dsm-pipeline.json`：

```json
{
  "pipeline": [
    "classified.laz",
    {
      "type": "writers.gdal",
      "filename": "dsm.tif",
      "resolution": 1.0,
      "output_type": "max",
      "data_type": "float32",
      "nodata": -9999,
      "gdaldriver": "COG"
    }
  ]
}
```

```bash
pdal pipeline dtm-pipeline.json
pdal pipeline dsm-pipeline.json
```

**步骤 5：计算 CHM（冠层高度模型）**

```bash
gdal_calc.py -A dsm.tif -B dtm.tif \
  --outfile=chm.tif \
  --calc="A-B" \
  --type=Float32 \
  --NoDataValue=-9999 \
  --co="COMPRESS=DEFLATE" \
  --co="TILED=YES"
```

**步骤 6：建筑物高度提取**

```bash
# 使用 exactextract 计算每个建筑轮廓内的 CHM 中值
exactextract \
  -p buildings.gpkg \
  -r chm.tif \
  -s "median(chm)" \
  -o buildings_with_height.gpkg
```

```python
# Python 等效
from exactextract import exact_extract
import geopandas as gpd

buildings = gpd.read_file("buildings.gpkg")
result = exact_extract(
    "chm.tif",
    buildings,
    ops=["median", "min", "max", "stdev"],
    output="pandas",
)
buildings = buildings.join(result)
buildings.to_file("buildings_with_height.gpkg", driver="GPKG")
```

---

### 管道 5：Mobility / Accessibility Analysis ★★★★

**适用场景**：分析"某类设施在 N 分钟步行/交通可达范围内覆盖了多少人口"。

**完整流程**：

```
1. 人口栅格（WorldPop 或 GHSL）
2. 设施点位（Overture places，分类过滤）
3. r5py 多模式等时圈
4. 合并等时圈，栅格化至人口网格
5. 统计内/外部人口
```

**步骤 1：加载人口与设施数据**

```python
import geopandas as gpd
import rasterio
import numpy as np

# 人口栅格（如 WorldPop 2020）
pop = rasterio.open("est_pop_2020.tif")

# 设施点位（从 Overture 或 OSM）
facilities = gpd.read_file("healthcare_facilities.gpkg")
facilities_3301 = facilities.to_crs("EPSG:3301")
```

**步骤 2：生成等时圈（r5py）**

```python
import r5py

# 初始化 r5py（需要 GTFS + OSM PBF）
transport_network = r5py.TransportNetwork(
    "data/estonia-latest.osm.pbf",
    ["data/tallinn_gtfs.zip"]
)

# 为每个设施生成 15 分钟步行等时圈
isochrones = []
for idx, facility in facilities_3301.iterrows():
    try:
        iso = r5py.DetailedItinerariesComputer(
            transport_network,
            origins=r5py.TransportMode.WALK,
            destinations=gpd.GeoSeries([facility.geometry], crs="EPSG:3301"),
            max_trip_duration=15
        )
        isochrones.append(iso)
    except Exception as e:
        print(f"跳过设施 {idx}: {e}")
```

**步骤 3：使用 Per-POI 等时圈（推荐方案）**

对于步行/自行车可达性审计，**Per-POI 等时圈模式远优于 origin×target 矩阵**：

```
1. K = 所有类别的 POI 总数（通常 1000+ — 规模可控）
2. for each POI: POST /isochrone {time:N, costing:pedestrian}
   → 存储多边形，标注类别
3. DuckDB / PostGIS 空间连接：
   建筑 centroid 落在某个类别的任意等时圈内 → has_<category> = 1
4. 综合得分 = sum(has_<category>)
```

**为什么不用矩阵？**
- 矩阵复杂度 O(起点×终点)，10000 个建筑 × 4200 个 POI = 4200 万次计算
- 等时圈多边形天然编码覆盖信息，一次空间连接即可得到布尔结果
- 等时圈同时作为"缺口地图"的可视化图层

**步骤 4：栅格化等时圈并统计人口**

```python
# 合并所有等时圈
all_iso = gpd.GeoSeries(unary_union(all_isochrone_polys), crs="EPSG:3301")

# 栅格化
from rasterio.features import rasterize
iso_raster = rasterize(
    [(geom, 1) for geom in all_iso],
    out_shape=pop.shape,
    transform=pop.transform,
    fill=0
)

# 统计覆盖人口
covered_pop = np.sum(pop.read(1)[iso_raster == 1])
total_pop = np.sum(pop.read(1))
coverage_pct = covered_pop / total_pop * 100

print(f"15分钟步行覆盖: {coverage_pct:.1f}% 人口")
```

---

### 管道 6：Geocoding + Address Standardization ★★★

**适用场景**：批量将非结构化地址文本转换为空间坐标（参考坦桑尼亚 TTCL 项目经验）。

**完整流程**：

```
1. 加载 CSV → 清洗地址（正则检测 PO Box）
2. tidygeocoder::geocode(method='osm') 批量地理编码
3. 过滤失败的编码，手动修正
4. 转换为空间对象 + 重投影到本地 UTM
5. 导出 GeoPackage
```

**步骤 1：地址清洗**

```r
library(tidyverse)
library(janitor)

# 加载原始数据
df <- read_csv("ttcl_subscribers.csv") %>%
  clean_names() %>%
  mutate(
    # 检测 PO Box 地址（无法地理编码）
    is_pobox = str_detect(
      tolower(address),
      "p\\.?\\s*o\\.?\\s*box|post office box|box\\s+no"
    ),
    # 清洗无关字符
    clean_address = address %>%
      str_replace_all("\\s+", " ") %>%
      str_trim()
  )

# 分类：可编码 vs 不可编码
pobox <- df %>% filter(is_pobox)
geocodable <- df %>% filter(!is_pobox)
```

**步骤 2：批量地理编码**

```python
import pandas as pd
import requests
import time

# 自托管 Nominatim（推荐方式）
NOMINATIM_URL = "http://localhost:8080/search"

def geocode_address(address):
    """批量地理编码，带速率控制"""
    time.sleep(1.1)  # Nominatim 公共 API 限速 1 req/s
    try:
        r = requests.get(
            NOMINATIM_URL,
            params={
                "q": address,
                "format": "json",
                "limit": 1,
                "countrycodes": "tz",  # 限定坦桑尼亚
            },
            timeout=10
        )
        data = r.json()
        if data:
            return pd.Series({
                "lat": float(data[0]["lat"]),
                "lon": float(data[0]["lon"]),
                "display_name": data[0]["display_name"],
                "osm_type": data[0]["osm_type"],
            })
    except Exception:
        pass
    return pd.Series({"lat": None, "lon": None, "display_name": None, "osm_type": None})

# 执行批量编码
results = df["clean_address"].apply(geocode_address)
df = pd.concat([df, results], axis=1)
```

**步骤 3：过滤失败 + 手动修正**

```python
# 识别失败的编码
failed = df[df["lat"].isna()]
success = df[df["lat"].notna()]

print(f"成功: {len(success)}, 失败: {len(failed)}")
print(f"成功率: {len(success)/len(df)*100:.1f}%")

# 导出失败列表供人工处理
failed[["clean_address"]].to_csv("failed_geocodes.csv", index=False)
```

**步骤 4：转换为空间数据 + 导出**

```python
import geopandas as gpd
from shapely.geometry import Point

# 构造几何列
geometry = [Point(lon, lat) for lon, lat in zip(success["lon"], success["lat"])]
gdf = gpd.GeoDataFrame(success, geometry=geometry, crs="EPSG:4326")

# 重投影到本地 UTM（坦桑尼亚 EPSG:21037）
gdf_utm = gdf.to_crs("EPSG:21037")

# 导出 GeoPackage
gdf_utm.to_file("ttcl_geocoded.gpkg", driver="GPKG")
```

---

### 管道 7：Climate Risk Modeling ★★★★★

**适用场景**：综合气候、地形和人口数据，生成多因子叠置的脆弱性/风险指数地图（参考达累斯萨拉姆脆弱性项目）。

**完整流程**：

```
1. 加载 NetCDF 气候数据 + DEM + 人口
2. 统一 CRS 到本地投影
3. 多年时间均值：app(x, mean)
4. 网格对齐：resample() 到参考栅格
5. 归一化 + 加权叠置
6. NA 填充：focal(w=3, mean, na.policy="only")
7. Leaflet 交互式输出
```

**步骤 1：加载多源数据**

```r
library(terra)
library(sf)

# 气候数据（NetCDF）
precip <- rast("precip_annual.nc")
temp_max <- rast("tmax_annual.nc")
drought_index <- rast("spei_12.nc")

# DEM 与人口
dem <- rast("dar_dem_30m.tif")
population <- rast("dar_population_2020.tif")

# 研究区边界
aoi <- vect("dar_es_salaam_boundary.gpkg")
```

**步骤 2：统一 CRS**

```r
# 确定目标 CRS：达累斯萨拉姆使用 UTM Zone 37S (EPSG:32737)
target_crs <- "EPSG:32737"

# 统一重投影
precip <- project(precip, target_crs)
temp_max <- project(temp_max, target_crs)
drought_index <- project(drought_index, target_crs)
dem <- project(dem, target_crs)
population <- project(population, target_crs)
```

**步骤 3：时间维归约**

```r
# 计算多年平均值
precip_mean <- app(precip, mean, na.rm = TRUE)
temp_max_mean <- app(temp_max, mean, na.rm = TRUE)
drought_mean <- app(drought_index, mean, na.rm = TRUE)
```

**步骤 4：网格对齐**

```r
# 以 DEM 为目标参考栅格对齐所有图层
reference <- dem

precip_aligned <- resample(precip_mean, reference, method = "bilinear")
temp_aligned <- resample(temp_max_mean, reference, method = "bilinear")
drought_aligned <- resample(drought_mean, reference, method = "bilinear")
pop_aligned <- resample(population, reference, method = "bilinear")
```

**步骤 5：归一化到 0-1 区间**

```r
normalize_01 <- function(r) {
  r_min <- global(r, "min", na.rm = TRUE)[1, 1]
  r_max <- global(r, "max", na.rm = TRUE)[1, 1]
  (r - r_min) / (r_max - r_min)
}

# 注意：干旱指数越低越严重，需反转
precip_norm <- 1 - normalize_01(precip_aligned)  # 低降水 → 高脆弱
temp_norm <- normalize_01(temp_aligned)           # 高温 → 高脆弱
drought_norm <- 1 - normalize_01(drought_aligned) # 负 SPEI → 高脆弱
dem_norm <- normalize_01(dem)                     # 低洼 → 高脆弱（洪水）
pop_norm <- normalize_01(pop_aligned)             # 密集 → 高暴露
```

**步骤 6：加权叠置**

```r
# 权重分配（根据领域专家确定）
weights <- c(
  precip = 0.30,      # 降水 30%
  temp = 0.15,        # 温度 15%
  drought = 0.15,     # 干旱 15%
  dem = 0.15,         # 地形 15%
  population = 0.25    # 人口暴露 25%
)

# 加权叠置
vulnerability <- precip_norm * weights["precip"] +
  temp_norm * weights["temp"] +
  drought_norm * weights["drought"] +
  dem_norm * weights["dem"] +
  pop_norm * weights["population"]

# 根据数据情况是否处理 NA
```

**步骤 7：NA 填充（focal 移动窗口）**

```r
# 3×3 窗口均值填充仅 NA 像素
vulnerability_filled <- focal(
  vulnerability,
  w = 3,
  fun = mean,
  na.policy = "only",
  na.rm = TRUE
)
```

**步骤 8：输出与可视化**

```r
# 写入 COG
writeRaster(
  vulnerability_filled,
  "dar_vulnerability_index.tif",
  filetype = "COG",
  gdal = c("COMPRESS=DEFLATE", "OVERVIEWS=AUTO"),
  overwrite = TRUE
)

# 分类输出
vuln_class <- classify(vulnerability_filled, c(
  0, 0.2, 1,  # 低风险
  0.2, 0.4, 2, # 中低风险
  0.4, 0.6, 3, # 中风险
  0.6, 0.8, 4, # 中高风险
  0.8, 1.0, 5  # 高风险
))

writeRaster(vuln_class, "dar_vulnerability_classes.tif",
            filetype = "COG", overwrite = TRUE)
```

```r
# Leaflet 交互式地图
library(leaflet)
library(leafem)

pal <- colorNumeric("RdYlBu", values(vulnerability_filled),
                    na.color = "transparent", reverse = TRUE)

leaflet() %>%
  addProviderTiles("CartoDB.Positron") %>%
  addRasterImage(vulnerability_filled, colors = pal, opacity = 0.8,
                 project = TRUE) %>%
  addLegend(pal = pal, values = values(vulnerability_filled),
            title = "气候脆弱性指数") %>%
  addPolygons(data = st_as_sf(aoi), fill = FALSE, color = "#333", weight = 2)
```

---

## 三、处理工具选型矩阵

### 3.1 按数据量与工具选型

| 任务 | < 5000 万条 | 5000 万 - 1 亿条 | > 1 亿条 |
|------|-----------|---------------|---------|
| **矢量转换** | DuckDB Spatial | DuckDB Spatial | Apache Sedona |
| **矢量空间连接** | DuckDB / GeoPandas | DuckDB Spatial | Apache Sedona |
| **单幅栅格** | GDAL CLI | xarray + dask | xarray + dask (cluster) |
| **栅格时间序列** | xarray | xarray + dask | xarray + dask |
| **点云处理** | PDAL | PDAL（分批） | PDAL + Spark |
| **Web 地图服务** | PMTiles 静态 / Martin | Martin + PostGIS | SaaS (MapTiler/Mapbox) |
| **网络分析** | pgRouting / r5py | r5py / Valhalla | SaaS (Google/HERE) |

### 3.2 路由引擎对比

| 引擎 | 优势 | 劣势 |
|------|------|------|
| **OSRM** | 最快汽车路由，简洁 HTTP API，成熟 Docker 镜像 | 单实例单一模式 |
| **Valhalla** | 多模式，内置等时圈，动态成本选项，tile-based 架构 | 配置较复杂 |
| **GraphHopper** | 多模式，强公交支持 | 内存消耗大 |
| **OpenRouteService** | 托管 + 自托管，多模式，等时圈，矩阵 | 托管有速率限制 |
| **pgRouting** | 内置于 PostGIS，与数据库集成 | 大规模图速度慢于专用引擎 |
| **r5py** | 多模式可达性（公交+步行+自行车），科研级 | Java 运行环境，批处理导向 |

### 3.3 重采样方法选择

| 数据类型 | 推荐方法 |
|---------|---------|
| 连续型（高程、温度、反射率） | `bilinear`（默认）、`cubic`、`cubicspline`、`lanczos` |
| 分类型（土地覆盖、掩膜） | `near` 或 `mode` |
| 聚合型（高分辨率 → 低分辨率连续型） | `average` |

> **关键警告**：绝不要在分类型数据上使用 `bilinear`——它会"发明"不存在的插值类别值。

---

## 四、输出验证清单

### 4.1 按输出类型的完整验证

| 输出类型 | 验证命令 | 关键检查项 |
|---------|---------|-----------|
| **GeoParquet** | `gpq validate output.parquet` | 几何列名、CRS 元数据、bbox 元数据、行数 |
| **STAC** | `stac-validator item.json` | 条目和目录与 schema 的符合性 |
| **GeoPackage** | `ogrinfo -al -so output.gpkg` | 图层名、几何类型、CRS、要素数量 |
| **COG** | `rio cogeo validate output.tif` | 内部切片、overviews、压缩、NoData 值 |
| **栅格（通用）** | `gdalinfo output.tif` | scale/offset、dtype、NoData、波段顺序、分辨率、CRS、bounds |
| **PMTiles** | `pmtiles show output.pmtiles` | bounds、min/max zoom、矢量图层名、元数据 |
| **PostGIS** | 自定义 SQL | SRID、GIST 索引、行数、ST_IsValid、EXPLAIN ANALYZE |
| **Web 地图** | 浏览器加载 | 网络请求、source-layer 名称、属性标注、图例、移动端视口 |

### 4.2 具体验证命令

```bash
# GeoParquet
gpq validate buildings.parquet

# COG
rio cogeo validate ndvi.tif
gdalinfo ndvi.tif  # 确认 overviews/tiling/compression

# GeoPackage
ogrinfo -al -so output.gpkg
ogrinfo -so output.gpkg layer_name  # 单层摘要

# PMTiles
pmtiles show output.pmtiles

# 栅格质量
gdalinfo input.tif             # 完整元数据
gdalinfo -stats input.tif      # 含计算统计量
gdalinfo -mm input.tif         # 仅 min/max（更快）

# PostGIS 内
SELECT Find_SRID('public', 'buildings', 'geom');
SELECT count(*) FROM buildings;
SELECT count(*) FROM buildings WHERE NOT ST_IsValid(geom);
SELECT count(*) FROM buildings WHERE geom IS NULL;
```

### 4.3 环境基线检查

在调试数据问题前，务必执行以下版本和环境检查：

```bash
gdalinfo --version
ogrinfo --formats | grep -E 'Parquet|GPKG|FlatGeobuf'
projinfo EPSG:3301
duckdb -c "INSTALL spatial; LOAD spatial; SELECT duckdb_proj_version();"
python -c "import geopandas, shapely, pyproj, rasterio; print(geopandas.__version__)"
```

---

## 五、CRS与几何门禁检查

### 5.1 生产管道前的强制检查（MANDATORY）

任何生产级数据处理管道必须执行以下五项检查，无一例外：

| 序号 | 检查项 | 命令/方法 | 说明 |
|------|-------|----------|------|
| 1 | **断言输入 CRS** | `st_crs()` / `gdalinfo` | 绝不要假设 CRS；有时 Shapefile 的 .prj 文件不存在或配置错误 |
| 2 | **重投影到度量 CRS** | 使用本地 UTM 或等同投影 | 距离/面积/缓冲区/聚类/密度分析必须在度量坐标系下进行 |
| 3 | **运行 ST_MakeValid** | `ST_MakeValid()` / `st_make_valid()` | 导入、重投影、叠置、融合、简化之后必须修复几何体 |
| 4 | **重新投影到目标 CRS** | EPSG:4326（存储）或 EPSG:3857（Web 渲染） | 根据下游用途选择合适的 CRS |
| 5 | **CRS 标签一致性** | 写入前统一 CRS 标签 | DuckDB Spatial 1.5+ 会将 EPSG:4326 和 OGC:CRS84 视为不同 CRS |

### 5.2 DuckDB Spatial EPSG:4326 vs OGC:CRS84 陷阱

这是 DuckDB Spatial 1.5+ 中最关键的注意事项：

```
相同坐标，不同标签 → 空间连接失败！
```

- GeoJSON 读取的数据标注为 **OGC:CRS84**（RFC 7946 默认）
- GeoParquet 读取的数据可能标注为 **EPSG:4326**
- Shapefile `.prj` 保持原始标注

**解决方案：读取时统一标注**

```sql
-- 选项 A：统一为 OGC:CRS84
SELECT ST_SetCRS(geometry, 'OGC:CRS84') AS geom FROM ST_Read('input.gpkg');

-- 选项 B：统一为 EPSG:4326
SELECT ST_SetCRS(geometry, 'EPSG:4326') AS geom FROM ST_Read('input.gpkg');

-- 强制指定：使用 ST_Transform 时必须保持标签一致
SELECT ST_Transform(geom, 'OGC:CRS84', 'EPSG:3301', always_xy := true)
FROM ST_Read('input.geojson');
```

### 5.3 通用几何体修复流程

```sql
-- PostGIS
UPDATE my_table
SET geom = ST_MakeValid(geom)
WHERE NOT ST_IsValid(geom);

-- 修复后验证
SELECT count(*) FROM my_table WHERE NOT ST_IsValid(geom);
-- 期望输出：0
```

```python
# GeoPandas / Shapely
import geopandas as gpd
gdf = gpd.read_file("input.gpkg")
gdf["geometry"] = gdf["geometry"].make_valid()
gdf.to_file("output.gpkg", driver="GPKG")
```

---

## 六、可复现性要求（data-manifest.json）

### 6.1 Manifest 模板

每一个可复现管道必须记录以下 JSON 数据清单：

```json
{
  "sources": [
    {
      "name": "Overture buildings",
      "release": "2025-01-22.0",
      "url": "s3://overturemaps-us-west-2/release/2025-01-22.0/theme=buildings/type=building/*.parquet",
      "license": "CDLA Permissive v2.0"
    }
  ],
  "crs": {
    "storage_crs": "EPSG:4326",
    "analysis_crs": "EPSG:3301"
  },
  "environment": {
    "gdal": "3.8.5",
    "duckdb": "1.1.0",
    "python": "3.12",
    "geopandas": "1.0.1"
  },
  "outputs": [
    {
      "path": "buildings.pmtiles",
      "format": "PMTiles",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "validated": true,
      "attribution": "© OpenStreetMap contributors, Overture Maps Foundation"
    }
  ]
}
```

### 6.2 可复现性规则（必须遵守）

| 编号 | 规则 | 说明 |
|------|------|------|
| 1 | **固定 Overture release 版本** | 禁止使用 "latest"；公共桶仅保留最近几个 release |
| 2 | **固定 STAC item ID** | 卫星影像必须记录具体 item ID 而非搜索条件 |
| 3 | **记录 Geofabrik 文件时间戳** | `stat file.osm.pbf > timestamp.txt` |
| 4 | **镜像 Overture release** | 超出公共保留窗口的数据必须自行镜像 |
| 5 | **使用 conda-forge 环境或容器** | 避免纯 pip 环境（GDAL/PROJ 原生依赖难以复现） |
| 6 | **固定 DuckDB 版本** | Homebrew CLI 和 PyPI wheel 可能 patch 版本不同，`ST_SetCRS` 行为可能变化 |
| 7 | **提交 environment.yml / pixi.toml / Dockerfile** | 将环境定义纳入版本控制 |

### 6.3 DuckDB 版本固定注意事项

```bash
# Homebrew 安装的 DuckDB 与 PyPI wheel 可能不是同一补丁版本
# 确认版本一致
duckdb --version
python -c "import duckdb; print(duckdb.__version__)"

# 在 requirements.txt 中固定版本
duckdb==1.1.0

# 测试脚本：确保 Python 连接和 CLI 的 SQL 行为一致
duckdb -c "INSTALL spatial; LOAD spatial; SELECT ST_SetSRID(ST_MakePoint(24.75, 59.44), 'EPSG:4326');"
```

---

## 七、12大反模式（Anti-Patterns）

以下来自 open-gis-main 项目总结的关键反模式。每一个都可能摧毁生产管道的正确性、可维护性或可复现性。

| 编号 | 反模式 | 严重性 | 说明与正确做法 |
|------|-------|-------|--------------|
| **1** | **Shapefile 作为新输出格式** | 🔴 严重 | 列名截断（10 字符）、2GB 上限、无 UTF-8、多文件分散。应使用 GeoParquet 或 GeoPackage |
| **2** | **在 EPSG:4326 上计算距离/面积/缓冲区** | 🔴 严重 | 经纬度单位是度（degrees），不是米（meters）。必须先重投影到本地度量 CRS |
| **3** | **Web Mercator 用于面积/距离计算** | 🔴 严重 | Web Mercator 是非等积投影。使用本地 UTM 或等同投影 |
| **4** | **Python 循环做空间连接** | 🟠 重要 | DuckDB/PostGIS 一行 SQL 替代千百行 Python for 循环 |
| **5** | **下载整个数据集** | 🟠 重要 | STAC + cloud-native 格式支持按需懒加载。善用 bbox 过滤和 COG 的 Range Requests |
| **6** | **全球尺度本地处理取数/查表** | 🟠 重要 | 全球查询/搜索问题不应在本地处理。使用自托管 geocoding 或 Overture 云端查询 |
| **7** | **默认使用 MBTiles** | 🟡 建议 | PMTiles 是现代默认选择：单文件、零服务器、支持 HTTP Range Requests |
| **8** | **写 GeoTIFF 而非 COG** | 🟡 建议 | 仅需一个 `-of COG` 标志。COG 自动生成内部切片和 overviews |
| **9** | **静默混合 CRS** | 🔴 严重 | 每次空间连接前必须断言 CRS 匹配 |
| **10** | **手写路由或地理编码** | 🟠 重要 | OSRM/Valhalla/Nominatim 一个 `docker pull` 即可部署。手写路由引擎是"重新发明轮子" |
| **11** | **固定数据为 "latest"** | 🔴 严重 | 可复现管道中禁止使用 "latest"。必须固定具体版本/日期 |
| **12** | **混淆 EPSG:4326 和 OGC:CRS84** | 🔴 严重 | 两者坐标值相同，但 DuckDB Spatial 1.5+ 视为不同 CRS，导致连接失败 |

### 反模式具体案例

#### 反模式 #2：在 EPSG:4326 上做缓冲

```python
# ❌ 错误：在经纬度上做 500"度"的缓冲
buildings_4326["buffer"] = buildings_4326.geometry.buffer(500)

# ✅ 正确：重投影到度量 CRS 再做缓冲
buildings_3301 = buildings_4326.to_crs("EPSG:3301")
buildings_3301["buffer"] = buildings_3301.geometry.buffer(500)  # 500 米
buildings_4326_with_buffer = buildings_3301.to_crs("EPSG:4326")
```

#### 反模式 #4：Python 循环空间连接

```python
# ❌ 错误：嵌套循环 O(n*m)
for idx_p, point in points.iterrows():
    for idx_d, district in districts.iterrows():
        if district.geometry.contains(point.geometry):
            result.append({...})

# ✅ 正确：一行 sjoin（R-tree 索引自动使用）
result = gpd.sjoin(points, districts, how="left", predicate="within")
```

#### 反模式 #9：静默混合 CRS

```sql
-- ❌ 错误：未断言 CRS 一致性
SELECT b.* FROM buildings b
JOIN districts d ON ST_Within(b.geom, d.geom);
-- 如果 buildings 是 EPSG:3301，districts 是 EPSG:4326，结果全空但无报错！

-- ✅ 正确：先统一 CRS
SELECT Find_SRID('public', 'buildings', 'geom');
SELECT Find_SRID('public', 'districts', 'geom');
-- 确认一致后再做连接，或使用 ST_Transform 统一
```

---

## 八、Shell脚本最佳实践

### 8.1 核心原则

| 原则 | 说明 |
|------|------|
| **单独 .py 文件，由 shell 调用** | 不要在 shell 脚本中嵌入 Python heredoc |
| **heredoc 仅用于短 SQL 或无引号风险的简单 Python** | 引号冲突和调试困难是常见陷阱 |
| **每个脚本以 `set -euo pipefail` 开头** | `-e` 遇错退出；`-u` 未定义变量报错；`-o pipefail` 管道中任一命令失败则失败 |

### 8.2 示例模板

```bash
#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# Pipeline: Overture Buildings → PMTiles
# Date: 2026-06-04
# Manifest: data/data-manifest.json
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${SCRIPT_DIR}/../data"
OUTPUT_DIR="${SCRIPT_DIR}/../output"

mkdir -p "${DATA_DIR}" "${OUTPUT_DIR}"

echo "[1/4] 从 Overture 提取建筑数据..."
.venv/bin/python scripts/extract_buildings.py \
  --release 2025-01-22.0 \
  --bbox 24.5,59.3,25.0,59.5 \
  --output "${DATA_DIR}/buildings.parquet"

echo "[2/4] 验证 GeoParquet..."
gpq validate "${DATA_DIR}/buildings.parquet"

echo "[3/4] 转换为矢量瓦片..."
tippecanoe -o "${OUTPUT_DIR}/buildings.pmtiles" \
  -Z 10 -z 16 \
  -l buildings \
  --drop-densest-as-needed \
  "${DATA_DIR}/buildings.parquet"

echo "[4/4] 验证 PMTiles..."
pmtiles show "${OUTPUT_DIR}/buildings.pmtiles"

echo "完成。输出：${OUTPUT_DIR}/buildings.pmtiles"
```

### 8.3 错误示例

```bash
# ❌ 错误：Python heredoc 中包含单引号
python3 << 'PY'
import requests
print('处理中...')  # 单引号在 heredoc 中可能引发问题
PY

# ✅ 正确：拆分到单独文件
# scripts/process.py 包含所有 Python 逻辑
.venv/bin/python scripts/process.py
```

---

## 附录：工具速查

### GDAL/OGR 常用操作

```bash
# 格式转换
ogr2ogr -f Parquet output.parquet input.gpkg

# 重投影
ogr2ogr -t_srs EPSG:3301 output.gpkg input.gpkg

# 空间裁剪
ogr2ogr -spat 24.5 59.3 25.0 59.5 -spat_srs EPSG:4326 output.gpkg input.gpkg

# 属性过滤
ogr2ogr -where "amenity IN ('cafe','restaurant')" output.gpkg input.gpkg

# 批量导入 PostGIS（使用 COPY 协议，速度显著快于 INSERT）
ogr2ogr -f PostgreSQL "PG:host=localhost dbname=gis user=postgres" \
  input.gpkg -nln target_table -lco GEOMETRY_NAME=geom \
  -nlt PROMOTE_TO_MULTI -lco UNLOGGED=ON --config PG_USE_COPY YES
```

### GDAL 栅格操作

```bash
# 重投影 + 重采样
gdalwarp -t_srs EPSG:3301 -tr 10 10 -r bilinear input.tif output.tif

# 按多边形裁剪
gdalwarp -cutline aoi.gpkg -crop_to_cutline input.tif clipped.tif

# 构建虚拟镶嵌（不拷贝数据）
gdalbuildvrt mosaic.vrt tile_*.tif
gdal_translate -of COG mosaic.vrt mosaic_cog.tif

# 直接合并为 COG
gdalwarp -of COG -co COMPRESS=DEFLATE tile_*.tif mosaic.tif
```

### DuckDB 常用 SQL

```sql
-- 环境初始化
INSTALL spatial; LOAD spatial;
INSTALL httpfs; LOAD httpfs;

-- 本地/远程读取
SELECT * FROM ST_Read('input.gpkg');
SELECT count(*), ST_Extent(ST_Extent_Agg(geometry))
FROM read_parquet('buildings.parquet');

-- 空间连接（DWithin）
WITH b AS (
  SELECT id, ST_Transform(geometry, 'EPSG:4326', 'EPSG:3301', always_xy := true) AS geom
  FROM buildings
)
SELECT b.* FROM b JOIN roads r
  ON ST_DWithin(b.geom, r.geom, 200);

-- H3 聚合
SELECT h3_latlng_to_cell(ST_Y(ST_Centroid(geom)), ST_X(ST_Centroid(geom)), 9) AS h3,
       count(*) AS n
FROM places GROUP BY h3;

-- 持久化数据库
-- duckdb my_gis.duckdb  # 命令行启动即创建
```

### PDAL 常用操作

```bash
# 格式转换
pdal translate input.las output.laz
pdal translate input.laz output.copc.laz

# 元数据查看
pdal info input.laz
pdal info input.laz --stats
pdal info input.laz --all

# 执行管道
pdal pipeline pipeline.json
```

### 性能提醒

| 事项 | 说明 |
|------|------|
| GIST/R-tree 索引 | 超过 ~10,000 条要素必须创建索引 |
| 查询下推 | 将连接和聚合推到数据库（DuckDB/PostGIS），不要拉回 Python |
| 栅格分块 | 应匹配 COG 内部 block 大小（默认 512×512） |
| Overture S3 查询 | `bbox` struct 列支持谓词下推，务必在 WHERE 中过滤 |
| 物化视图 | PostGIS 中为昂贵的重复查询创建物化视图 |
| dask chunk 大小 | 每块 50-500 MB 为最佳区间——太小浪费调度开销，太大耗尽内存 |
| GeoParquet 回读 | DuckDB 写入的 GeoParquet 回读后列类型为 GEOMETRY 而非 BLOB，不要再用 ST_GeomFromWKB 包装 |
| OSM tags 引用 | OSM tags（如 `natural`、`cross`、`addr:street`、`garden:type`）在 SQL 中必须双引号包裹 |

### H3 分辨率速查

| 分辨率 | 平均六边形面积 | 平均边长 | 典型用途 |
|--------|-------------|---------|---------|
| 6 | ~36 km² | ~3.7 km | 区域网格 |
| 7 | ~5.2 km² | ~1.4 km | 城市片区 |
| 8 | ~0.74 km² | ~531 m | 社区 |
| 9 | ~0.105 km² | ~201 m | 街区/设施服务范围 |
| 10 | ~0.015 km² | ~76 m | 地块级筛选 |

### OSM POI 去重参考

| 类别 | 度量 CRS 网格大小 |
|------|-------------------|
| 学校 | 100 m（校园级） |
| 幼儿园 | 80 m |
| 药店 | 30 m |
| 杂货店 | 30 m |
| 医疗机构 | 50 m |
| 公交站点 | 30 m |

---

> **交叉引用**：本文档应配合以下文档阅读：
> - ←→ 03_数据模型与格式.md — 理解 GeoParquet/COG/PMTiles 格式详情
> - ←→ 22_空间数据库.md — PostGIS 建库与运维实践
> - ←→ 23_WebGIS开发.md — MapLibre/Deck.gl 前端渲染与瓦片服务
> - ←→ 33_空间分析与统计.md — 空间统计、聚类与热点分析方法
> - ←→ 35_专家级批量处理与自动化实战指南.md — ArcGIS Pro/FME 批处理对比
>
> **文档版本**：V1.0 | 2026-06-04 | open-gis-main 三文档综合


<!-- wm:坤图_GIS:V1.0 -->
