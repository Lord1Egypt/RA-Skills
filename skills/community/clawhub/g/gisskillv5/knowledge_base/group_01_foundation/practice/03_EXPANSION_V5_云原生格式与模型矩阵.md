<!-- wm:坤图_GIS:V5.0 -->
---
knowledge_id: GIS-KB-G01-003-EXP01
group: 1
group_name: "基础底座"
category: "theory"
title: "03号扩展：云原生格式·五大模型矩阵·BIM-GIS·STAC时序"
source_file: "03_数据模型与格式.md"
version: "V5.0"
last_updated: "2026-06-23"
---

# 03号模块 V5.0 扩展：云原生/三维/点云/时序格式全集

---

## 一、云原生空间格式全解析

### 1.1 矢量云原生

| 格式 | 标准 | 压缩率 | 查询性能 | 适用场景 | 工具支持 |
|------|------|--------|----------|----------|----------|
| **FlatGeobuf** | OGC(社区标准) | ★★★★ | ★★★★★(范围查询) | Web流式传输/API | GDAL 3.6+ |
| **GeoParquet** | OGC+Apache | ★★★★★(列式) | ★★★★(分析查询) | 大数据分析/DuckDB | GDAL 3.6+ |
| **GeoArrow** | Apache Arrow | ★★★★★(内存) | ★★★★★(零拷贝) | 高性能计算/WASM | GeoPandas 1.0+ |
| **GeoJSON** | IETF RFC7946 | ★★(文本) | ★★★ | Web API/轻量交换 | 全平台 |
| **PMTiles** | Protomaps | ★★★★(单文件) | ★★★★(HTTP Range) | 矢量瓦片托管 | MapLibre/Leaflet |

### 1.2 栅格云原生

| 格式 | 标准 | 压缩 | 流式读取 | 适用场景 |
|------|------|------|----------|----------|
| **COG(Cloud Optimized GeoTIFF)** | OGC | DEFLATE/LZW/ZSTD | HTTP Range | 遥感影像Web发布 |
| **Zarr** | Community | Blosc/ZSTD/LZ4 | 分块并行 | 科学数据/多维数组 |
| **STAC-GeoTIFF** | STAC+COTG | 外部概览 | HTTP | 时空资产目录 |
| **NetCDF4** | OGC | zlib/szip | 维度切片 | 气候/海洋/气象 |
| **TileDB** | Apache 2.0 | 多算法 | 分片查询 | 大规模多维分析 |

### 1.3 点云云原生

| 格式 | 标准 | 压缩 | 流式 | 适用场景 |
|------|------|------|------|----------|
| **COPC(Cloud Optimized Point Cloud)** | LAS 1.4 + LAZ | LASzip | HTTP Range | 点云Web发布 |
| **EPT(Entwine Point Tile)** | 开源 | LAZ | 八叉树流 | 海量点云渐进加载 |
| **3DTiles(pnts)** | OGC | Draco | 层次LOD | 三维Web可视化 |
| **Potree格式** | 开源 | LAZ | 八叉树 | 点云Web展示(传统) |

---

## 二、五大空间数据模型对比矩阵

### 2.1 综合对比

| 维度 | 矢量(Vector) | 栅格(Raster) | 点云(Point Cloud) | 三维Mesh | 时序(Temporal) |
|------|-------------|-------------|-------------------|---------|---------------|
| **几何基元** | 点/线/面 | 像元(Pixel) | X,Y,Z坐标+属性 | 三角面片/体素 | 时空坐标(x,y,z,t) |
| **精度** | 无限(矢量) | 分辨率限定 | mm级(激光扫描) | 纹理分辨率 | 时间间隔 |
| **数据类型** | 离散对象 | 连续场 | 抽样点集 | 表面模型 | 事件/序列 |
| **存储格式** | Shapefile/GDB/GeoPackage/GeoParquet | GeoTIFF/COG/NetCDF/Zarr | LAS/LAZ/COPC/EPT | OBJ/3DTiles/I3S/CityGML/glTF | NetCDF/GeoPackage/TimescaleDB |
| **数据量(GIS项目典型)** | MB-GB | GB-TB | TB-PB | GB-TB | GB-TB |
| **典型应用** | 地籍/管网/规划 | DEM/DOM/土地利用 | 地形测量/林业/电力线 | 城市三维/数字孪生/倾斜摄影 | NDVI/气象/轨迹/疫情 |
| **空间数据库** | PostGIS/SpatiaLite/GDB | PostGIS Raster/Rasterio | PostgreSQL+PDAL | Cesium ion/MongoDB | TimescaleDB/MobilityDB |
| **分析方法** | 叠加/缓冲/网络/拓扑 | 代数/卷积/分类/重分类 | 滤波/分割/分类/配准 | 可视域/阴影/体积/碰撞 | 变化检测/趋势/聚类 |

### 2.2 选型决策

```
你需要处理什么类型的数据？
├── 离散空间对象(建筑物/道路/管井/地块)
│   ├── 高精度编辑 → File GDB / PostGIS
│   ├── Web共享 → GeoPackage / GeoJSON
│   └── 大数据分析 → GeoParquet + DuckDB
├── 连续场数据(DEM/影像/气象)
│   ├── 桌面处理 → GeoTIFF
│   ├── Web发布 → COG
│   └── 多维科学 → Zarr / NetCDF
├── 三维场景(城市/BIM/地质)
│   ├── Web展示 → 3DTiles / glTF
│   ├── 企业级 → I3S(ArcGIS生态)
│   └── BIM集成 → CityGML + Revit插件
├── 点云(激光/摄影测量)
│   ├── 桌面 → LAS 1.4
│   ├── Web → COPC / EPT
│   └── AI处理 → LAS+PDAL管线
└── 时序数据(遥感/传感器/轨迹)
    ├── 时序影像 → STAC + COG
    ├── 传感器 → TimescaleDB
    └── 轨迹 → MobilityDB
```

---

## 三、BIM与GIS互通格式

### 3.1 BIM↔GIS数据流

```
BIM软件                  中间格式                GIS平台
Revit ────→ IFC 2x3/4 ────→ FME ────→ GDB/PostGIS
Navisworks → NWD/NWC ─────→ ArcGIS Pro ──→ Multipatch
Bentley ───→ DGN ─────────→ GlobalMapper ──→ Shapefile
Tekla ─────→ IFC ─────────→ QGIS ──→ GeoPackage

三维轻量化:
Revit ──→ glTF/OBJ ──→ 3DTiles/Cesium ion
IFC ────→ CityGML 3.0 ──→ 3D City Database(PostGIS)
```

### 3.2 BIM-GIS关键格式

| 格式 | 用途 | BIM精度 | GIS分析 | 文件大小 |
|------|------|---------|---------|----------|
| **IFC 4.x** | BIM交换标准 | ★★★★★(建筑构件级) | ★★(需解析) | 大(MB-GB) |
| **CityGML 3.0** | 城市级数字孪生 | ★★★★(LOD0-LOD4) | ★★★★★(语义+拓扑) | 大(MB-GB) |
| **3DTiles 1.1** | Web三维瓦片 | ★★★(三角网格) | ★★★(属性查询) | 中(经压缩) |
| **I3S(ESRI)** | ArcGIS三维服务 | ★★★(三角网格+点) | ★★★★★(ArcGIS全分析) | 中 |
| **glTF 2.0** | 3D Web/移动端 | ★★★(外观) | ★(无空间参考) | 小(KB-MB) |

---

## 四、STAC时空资产目录

### 4.1 STAC规范体系

```
STAC (SpatioTemporal Asset Catalog)
├── STAC Item: 单个时空资产(如一幅Sentinel-2影像)
│   ├── geometry: 覆盖范围(GeoJSON Polygon)
│   ├── bbox: 外包矩形
│   ├── datetime: 采集时间
│   └── assets: 关联文件(B02.tif, B03.tif, ...)
├── STAC Catalog: 资产集合目录
└── STAC Collection: 同类资产集合+公共元数据
```

### 4.2 STAC在GIS中的应用

```python
# 使用pystac-client搜索Sentinel-2影像
from pystac_client import Client
import planetary_computer

catalog = Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace
)

search = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=[114.0, 30.0, 115.0, 31.0],     # 武汉区域
    datetime="2025-01-01/2025-06-30",
    query={"eo:cloud_cover": {"lt": 10}}   # 云量<10%
)

items = search.item_collection()
print(f"找到{len(items)}景符合条件的影像")

# 批量下载COG格式
for item in items:
    b04_url = item.assets["B04"].href  # 红波段
    b08_url = item.assets["B08"].href  # 近红外
    # HTTP Range读取指定区域，无需下载整景!
```

---

## 五、格式选择——2026年推荐栈

### 5.1 各场景首选格式

| 场景 | 首选格式 | 备选格式 | 淘汰/慎用 |
|------|----------|----------|----------|
| 矢量存储 | **GeoPackage** | GeoParquet | Shapefile(2026停止推荐) |
| 矢量大数据 | **GeoParquet** | FlatGeobuf | GDB(企业版外) |
| 栅格存储 | **COG** | Zarr | 传统GeoTIFF(非云优化) |
| 多维栅格 | **Zarr** | NetCDF4 | HDF5(已停止推荐) |
| 点云 | **COPC** | LAS 1.4 | LAS 1.2(旧) |
| 三维 | **3DTiles 1.1** | I3S | OSGB(废弃) |
| 矢量瓦片 | **PMTiles** | MBTiles | GeoServer缓存 |
| Web API | **GeoJSON** | FlatGeobuf | KML(新项目不推荐) |
| CAD交换 | **DWG 2018** | DXF | DXF(属性丢失) |
| BIM交换 | **IFC 4.3** | CityGML 3.0 | IFC 2x3(旧) |
| 时序资产 | **STAC** | GeoPackage | 文件夹散落影像 |

### 5.2 Shapefile淘汰路线图

```
2024 → 开始警告：新项目不推荐Shapefile
2025 → 默认禁止：工具默认输出GeoPackage
2026 → 完全停止推荐：仅保留读取兼容
2027 → 归档模式：读取兼容也标记为Legacy
```

**Shapefile致命缺陷**：
- 10项硬限制（字段名≤10字节/ 2GB/ 不支持NULL/ 无拓扑/ 多文件散落）
- `.dbf` 编码混乱（GBK/UTF-8/Latin1不可测）
- 性能：属性查询需全表扫描
- 替代方案：GeoPackage(单文件/无大小限制/全类型支持)

---

> **V5.0 新增内容说明**：云原生格式(Zarr/GeoArrow/COPC/STAC/PMTiles/FlatGeobuf)全解析、五大模型对比矩阵(矢量/栅格/点云/三维/时序)、BIM-GIS互通格式(IFC/CityGML/3DTiles/glTF)、2026年推荐格式栈+Shapefile淘汰路线图。原03号模块基础数据模型内容不变。
