# OGC 国际标准速查手册 | V5.0 | 群组六：现代GIS技术栈

> Open Geospatial Consortium 标准体系完整收录。
> 本文件覆盖 60+ OGC 标准，聚焦 Web 服务、数据格式、坐标轴陷阱、许可合规、国标映射六大核心维度。
> 编写依据：OGC 官方文档 + awesome-gis 索引 + open-gis 实战经验 + GB/T 国标交叉验证。
> ←→ 关联文件：`05_国家测绘标准体系.md`、`03_数据模型与格式.md`、`23_WebGIS开发.md`、`41_现代GIS数据处理管道.md`

---

## 一、OGC 组织与标准体系概览

### 1.1 OGC 是什么

| 维度 | 说明 |
|------|------|
| **全称** | Open Geospatial Consortium（开放地理空间信息联盟） |
| **成立** | 1994年（前身 OGF，1994年更名 OGC） |
| **性质** | 非营利性国际标准化组织 |
| **成员** | 500+ 组织（政府机构、企业、大学、研究机构） |
| **总部** | 美国弗吉尼亚州阿灵顿 |
| **核心使命** | 制定地理空间数据与服务的互操作标准，使不同厂商的 GIS 系统能够无缝协作 |
| **中文关联** | 对等 ISO/TC211，对等中国 TC230（全国地理信息标准化技术委员会） |

### 1.2 标准生命周期

```
讨论稿 (Discussion Paper) → 最佳实践 (Best Practice) → 候选标准 (Candidate Standard) → 采纳标准 (Adopted Standard)
     ↓                           ↓                            ↓                              ↓
   概念探索阶段              社区验证&反馈             投票与互操作测试               正式发布，维护中
```

| 阶段 | 状态标记 | 说明 |
|------|---------|------|
| **讨论稿** | OGC DP | 早期概念，征求社区意见 |
| **最佳实践** | OGC BP | 已验证可用的实践方案，但非强制 |
| **候选标准** | OGC CS | 进入投票阶段，等待成员批准 |
| **采纳标准** | OGC AS | 正式标准，具有约束力 |

### 1.3 与 ISO/TC 211 的关系

OGC 与 ISO/TC 211 存在紧密的合作关系。许多 OGC 标准通过 ISO/TC 211 上升为国际标准（ISO 191xx 系列）：

```
OGC 制定 → ISO/TC 211 采纳 → 发布为 ISO 191xx 标准
                                   ↓
                            中国 TC230 采标
                                   ↓
                          发布为 GB/T 国标系列
```

**关键事实**：
- OGC 负责制定技术规范，ISO 负责将其转化为国际标准
- 约 **40%** 的 ISO 19100 系列标准源自 OGC 标准
- OGC 标准的更新速度通常快于 ISO 标准（OGC 平均每 2-3 年修订，ISO 平均每 5 年）

### 1.4 标准分类架构

```
OGC 标准体系（60+ 标准）
├── A. 数据服务标准（11 项）
│   ├── WMS (Web Map Service)
│   ├── WFS (Web Feature Service)
│   ├── WCS (Web Coverage Service)
│   ├── WPS (Web Processing Service)
│   ├── WMTS (Web Map Tile Service)
│   ├── CSW (Catalog Service for Web)
│   ├── SOS (Sensor Observation Service)
│   ├── SPS (Sensor Planning Service)
│   ├── SensorThings API
│   └── OGC API 系列 (Features / Tiles / Records / Maps / Processes / EDR)
│
├── B. 数据编码标准（15 项）
│   ├── GML (Geography Markup Language)
│   ├── KML (Keyhole Markup Language)
│   ├── GeoPackage
│   ├── GeoJSON (RFC 7946)
│   ├── CityGML (城市三维模型)
│   ├── IndoorGML (室内空间)
│   ├── WaterML (水文数据)
│   ├── PipelineML (管道数据)
│   ├── LandInfra / InfraGML (基础设施)
│   ├── LAS / COPC (点云)
│   ├── netCDF (多维数据)
│   ├── GeoParquet
│   └── FlatGeobuf
│
├── C. 三维标准（6 项）
│   ├── 3D Tiles (Cesium 提出，OGC 社区标准)
│   ├── i3s (Indexed 3D Scene Layer, Esri 提出)
│   ├── CityGML 3.0
│   ├── IndoorGML
│   └── 3D Portrayal Service
│
├── D. 元数据与目录标准（5 项）
│   ├── ISO 19115 元数据
│   ├── ISO 19139 元数据XML实现
│   ├── CSW (目录服务)
│   ├── GeoSPARQL (语义查询)
│   └── OGC API Records
│
├── E. 传感器与观测标准（6 项）
│   ├── SensorML (传感器模型语言)
│   ├── Observations & Measurements (O&M)
│   ├── SWE Common
│   ├── SOS / SPS
│   ├── SensorThings API
│   └── TimeseriesML
│
├── F. 分析与处理标准（4 项）
│   ├── WPS (Web Processing Service)
│   ├── OGC API Processes
│   ├── Web Coverage Processing Service (WCPS)
│   └── Moving Features
│
├── G. 安全与权限标准（2 项）
│   ├── GeoXACML (地理空间访问控制)
│   └── OGC Security
│
├── H. 样式与可视化标准（4 项）
│   ├── SLD/SE (Styled Layer Descriptor / Symbology Encoding)
│   ├── WMS 样式
│   └── Portrayal (描绘)
│
└── I. 新兴标准与最佳实践（10+ 项）
    ├── STAC (SpatioTemporal Asset Catalog)
    ├── COG (Cloud Optimized GeoTIFF)
    ├── COPC (Cloud Optimized Point Cloud)
    ├── PMTiles
    ├── FlatGeobuf
    ├── GeoParquet
    ├── Zarr
    └── OGC API EDR (Environmental Data Retrieval)
```

### 1.5 完整标准目录表（60+ 标准速查）

| 标准名称 | 缩写 | 版本 | ISO 等效 | 状态 | 本手册覆盖 |
|----------|------|------|----------|------|-----------|
| Web Map Service | WMS | 1.3.0 | ISO 19128 | 正式 | 深度覆盖 |
| Web Feature Service | WFS | 2.0.2 | ISO 19142 | 正式 | 深度覆盖 |
| Web Coverage Service | WCS | 2.1 | — | 正式 | 概要 |
| Web Processing Service | WPS | 2.0 | — | 正式 | 概要 |
| Web Map Tile Service | WMTS | 1.0 | — | 正式 | 深度覆盖 |
| Catalog Service for Web | CSW | 2.0.2 | ISO 19115/19139 | 正式 | 深度覆盖 |
| Sensor Observation Service | SOS | 2.0 | — | 正式 | 概要 |
| Sensor Planning Service | SPS | 2.0 | — | 正式 | 概要 |
| SensorThings API | STA | 1.1 | — | 正式 | 概要 |
| OGC API Features | — | 1.0 | — | 正式 | 深度覆盖 |
| OGC API Tiles | — | 1.0 | — | 正式 | 深度覆盖 |
| OGC API Records | — | 1.0 | — | 正式 | 深度覆盖 |
| OGC API Maps | — | 1.0 | — | 草案 | 概要 |
| OGC API Processes | — | 1.0 | — | 正式 | 概要 |
| OGC API EDR | — | 1.1 | — | 正式 | 概要 |
| Geography Markup Language | GML | 3.2.1 | ISO 19136 | 正式 | 深度覆盖 |
| Keyhole Markup Language | KML | 2.2 | — | 正式 | 概要 |
| GeoPackage | GPKG | 1.3 | ISO 19165 | 正式 | 深度覆盖 |
| GeoJSON | — | RFC 7946 | — | IETF/OGC | 深度覆盖 |
| Styled Layer Descriptor | SLD | 1.1 | — | 正式 | 概要 |
| Symbology Encoding | SE | 1.1 | — | 正式 | 概要 |
| Filter Encoding | FE | 2.0 | ISO 19143 | 正式 | 概要 |
| CityGML | — | 3.0 | — | 正式 | 概要 |
| IndoorGML | — | 1.0 | — | 正式 | 概要 |
| WaterML 2.0 | — | 2.0 | — | 正式 | 概要 |
| SensorML | — | 2.0 | ISO 19156 | 正式 | 概要 |
| Observations & Measurements | O&M | 2.0 | ISO 19156 | 正式 | 概要 |
| GeoSPARQL | — | 1.0 | — | 正式 | 概要 |
| NetCDF | — | — | — | OGC 采纳 | 概要 |
| 3D Tiles | — | 1.1 | — | 社区标准 | 概要 |
| i3s | — | 1.3 | — | 社区标准 | 概要 |
| STAC | — | 1.0 | — | 社区标准 | 深度覆盖 |
| COG | — | — | — | 最佳实践 | 深度覆盖 |
| COPC | — | 1.0 | — | 社区标准 | 深度覆盖 |
| GeoParquet | — | 1.1 | — | 社区标准 | 深度覆盖 |
| FlatGeobuf | — | 1.0 | — | 最佳实践 | 深度覆盖 |
| PMTiles | — | 3.x | — | 最佳实践 | 深度覆盖 |
| Zarr | — | 2.x | — | 社区标准 | 概要 |
| TimeseriesML | — | 1.0 | — | 正式 | 概要 |
| Moving Features | — | 1.0 | — | 正式 | 概要 |
| PipelineML | — | 1.0 | — | 正式 | 概要 |
| LandInfra / InfraGML | — | 1.0 | — | 正式 | 概要 |
| GeoXACML | — | 1.0 | — | 正式 | 概要 |

---

## 二、核心 Web 服务标准（深度详解）

### 2.1 WMS — Web Map Service（网络地图服务）

#### 2.1.1 基本概念

WMS 是最基础的 OGC Web 服务，用于**请求地图图像**。返回的是渲染好的图片（PNG、JPEG、GIF），不是数据本身。

```
客户端 → GetCapabilities (服务器能力描述)
客户端 → GetMap (获取地图图像)
客户端 → GetFeatureInfo (点击查询属性) — 可选
```

#### 2.1.2 版本差异：1.1.1 vs 1.3.0 ⚠

这是整个 OGC 标准体系中**最常见的事故来源**。两个版本在坐标参数和轴顺序上存在不兼容的差异。

| 特性 | WMS 1.1.1 | WMS 1.3.0 |
|------|-----------|-----------|
| 坐标系参数名 | `SRS` | `CRS` |
| EPSG:4326 轴序 | **(lon, lat)** | **(lat, lon)** |
| CRS:84 轴序 | 不存在 | **(lon, lat)** |
| BBOX 格式 | `minx,miny,maxx,maxy` | `minx,miny,maxx,maxy`（但值含义变了） |
| 异常报告 | `ServiceExceptionReport` | `ServiceExceptionReport` |
| 样式支持 | 类似 | 增强了 SLD 支持 |

**WMS 1.1.1 请求示例**：
```
http://server/wms?service=WMS&version=1.1.1&request=GetMap
  &layers=roads,buildings
  &styles=,
  &srs=EPSG:4326
  &bbox=-122.5,37.7,-122.3,37.8         ← (lon_min, lat_min, lon_max, lat_max)
  &width=800&height=600
  &format=image/png
```

**WMS 1.3.0 请求示例（EPSG:4326）⚠**：
```
http://server/wms?service=WMS&version=1.3.0&request=GetMap
  &layers=roads,buildings
  &styles=,
  &crs=EPSG:4326
  &bbox=37.7,-122.5,37.8,-122.3         ← (lat_min, lon_min, lat_max, lon_max) — 注意顺序翻转!
  &width=800&height=600
  &format=image/png
```

**WMS 1.3.0 安全写法（CRS:84）**：
```
http://server/wms?service=WMS&version=1.3.0&request=GetMap
  &layers=roads,buildings
  &styles=,
  &crs=CRS:84
  &bbox=-122.5,37.7,-122.3,37.8         ← (lon_min, lat_min, lon_max, lat_max) — 与编程习惯一致
  &width=800&height=600
  &format=image/png
```

> ⚠ **黄金法则**：在 WMS 1.3.0 中使用 `CRS:84` 代替 `EPSG:4326`，避免轴序问题。`CRS:84` 始终使用 (lon, lat) 顺序。

#### 2.1.3 GetCapabilities 响应解读

```xml
<WMS_Capabilities version="1.3.0">
  <Service>
    <Name>WMS</Name>
    <Title>My GeoServer</Title>
    <OnlineResource xlink:href="http://server/geoserver/wms"/>
  </Service>
  <Capability>
    <Request>
      <GetCapabilities>...</GetCapabilities>
      <GetMap>
        <Format>image/png</Format>
        <Format>image/jpeg</Format>
        <DCPType><HTTP><Get>
          <OnlineResource xlink:href="http://server/geoserver/wms?"/>
        </Get></HTTP></DCPType>
      </GetMap>
      <GetFeatureInfo>...</GetFeatureInfo>
    </Request>
    <Layer>
      <Name>topp:states</Name>
      <Title>USA States</Title>
      <CRS>EPSG:4326</CRS>
      <CRS>CRS:84</CRS>
      <BoundingBox CRS="EPSG:4326" minx="-124.73" miny="24.96" maxx="-66.97" maxy="49.37"/>
      <!-- ⚠ 注意：1.3.0 下此 BBOX 实际含义是 (lat_min, lon_min, lat_max, lon_max) -->
    </Layer>
  </Capability>
</WMS_Capabilities>
```

#### 2.1.4 GetFeatureInfo

获取地图上指定像素点的属性信息：

```
http://server/wms?service=WMS&version=1.3.0&request=GetFeatureInfo
  &layers=states
  &crs=CRS:84
  &bbox=-124.73,24.96,-66.97,49.37
  &width=800&height=600
  &query_layers=states
  &i=400&j=300          ← 点击像素坐标
  &info_format=application/json
```

返回 GeoJSON 格式的属性数据（如果服务器支持）。

#### 2.1.5 常见 WMS 服务器

| 服务器 | 语言 | WMS 版本 | 特点 |
|--------|------|---------|------|
| **GeoServer** | Java | 1.1.1 / 1.3.0 | 最成熟，功能全，企业级 |
| **MapServer** | C | 1.1.1 / 1.3.0 | 高性能，CGI 模式 |
| **QGIS Server** | C++/Python | 1.3.0 | 直接发布 QGIS 项目 |
| **pygeoapi** | Python | 1.3.0 | 轻量级，OGC API 优先 |
| **deegree** | Java | 1.1.1 / 1.3.0 | 完整 OGC 标准栈 |

#### 2.1.6 WMS 请求调试清单

| 问题 | 排查项 |
|------|--------|
| 地图显示为空白 | 检查 `crs`/`srs` 参数是否与服务器支持的 CRS 匹配 |
| 地图位置偏移 | ⚠ 检查 WMS 版本 → 1.3.0+EPSG:4326 = 经纬度互换 |
| 图层未加载 | 检查 `layers` 名称是否与 GetCapabilities 中一致 |
| 样式不生效 | WMS 1.1.1 使用 `styles=`，1.3.0 可加 SLD 参数 |
| 跨域错误 | 服务器需要设置 CORS 头（GeoServer 默认不开启） |

---

### 2.2 WFS — Web Feature Service（网络要素服务）

#### 2.2.1 基本概念

WFS 返回**实际的地理数据**（矢量），与 WMS 返回图片不同。支持查询、过滤、增删改操作。

**WFS 操作类型**：

| 操作 | 说明 | WFS 1.1.0 | WFS 2.0 |
|------|------|-----------|---------|
| GetCapabilities | 获取服务能力描述 | √ | √ |
| DescribeFeatureType | 获取要素类型结构 | √ | √ |
| GetFeature | 查询要素 | √ | √ |
| GetPropertyValue | 获取单个属性值 | — | √ |
| LockFeature | 锁定要素（事务前置） | √ | — |
| Transaction | 增删改事务 | √ | — |
| CreateStoredQuery | 创建已存查询 | — | √ |
| DropStoredQuery | 删除已存查询 | — | √ |
| ListStoredQueries | 列出已存查询 | — | √ |

#### 2.2.2 分页参数

WFS 2.0 支持服务端分页：

```
http://server/wfs?service=WFS&version=2.0.0&request=GetFeature
  &typeNames=roads
  &count=100            ← 每页返回条数
  &startIndex=200       ← 起始索引（从 0 开始）
```

> ⚠ **注意**：`count` 和 `startIndex` 是 WFS 2.0 专有参数，WFS 1.1.0 不支持。1.1.0 使用 `MAXFEATURES` 限制数量但无偏移。

#### 2.2.3 输出格式：GeoJSON vs GML ⚠

WFS 可以返回多种格式，其中 GeoJSON 和 GML 的坐标轴顺序不同：

| 输出格式 | outputFormat 参数 | EPSG:4326 轴序 |
|----------|-------------------|---------------|
| **GML 3.2** | `application/gml+xml; version=3.2` | **(lat, lon)** — 遵循服务 CRS 的权威顺序 |
| **GeoJSON** | `application/json` | **(lon, lat)** — GeoJSON 规范强制 lon,lat |
| **GML 2** | `text/xml; subtype=gml/2.1.2` | 取决于服务器实现 |

```
# 请求 GeoJSON（轴序始终 lon,lat）
http://server/wfs?service=WFS&version=2.0.0&request=GetFeature
  &typeNames=roads
  &outputFormat=application/json

# 请求 GML（轴序取决于 CRS — EPSG:4326 = lat,lon）
http://server/wfs?service=WFS&version=2.0.0&request=GetFeature
  &typeNames=roads
  &outputFormat=application/gml+xml; version=3.2
```

> ⚠ **黄金法则**：解析 WFS 返回的 GML 时，**必须**根据 CRS 确定坐标轴顺序；解析 GeoJSON 时，**始终**假设 (lon, lat)。

#### 2.2.4 WFS 2.0 vs 1.1.0 主要差异

| 特性 | WFS 1.1.0 | WFS 2.0 |
|------|-----------|---------|
| 分页 | 无（仅 `MAXFEATURES` 限制） | `count` + `startIndex` |
| 查询方式 | 仅 Ad-hoc | Ad-hoc + StoredQuery |
| 命名空间 | XML 命名空间 | 简化命名空间 |
| 坐标参考 | 服务默认 CRS | 支持按请求指定 `srsName` |
| 过滤语言 | Filter 1.1 | Filter 2.0 (更强大) |
| Join 查询 | 不支持 | 支持跨表连接 |

#### 2.2.5 StoredQuery（已存查询）vs Ad-hoc 查询

**StoredQuery（已存查询）** — WFS 2.0 新增：

```
# 列出可用查询
http://server/wfs?service=WFS&version=2.0.0&request=ListStoredQueries

# 执行特定已存查询
http://server/wfs?service=WFS&version=2.0.0&request=GetFeature
  &storedQuery_id=urn:ogc:def:query:OGC-WFS::GetFeatureById
  &ID=roads.123
```

**优势**：
- 预编译查询更快
- 参数化查询防止注入
- 简化客户端代码

**Ad-hoc 查询**：

```xml
<GetFeature service="WFS" version="2.0.0">
  <Query typeNames="roads">
    <Filter>
      <PropertyIsGreaterThan>
        <ValueReference>traffic_count</ValueReference>
        <Literal>1000</Literal>
      </PropertyIsGreaterThan>
    </Filter>
  </Query>
</GetFeature>
```

---

### 2.3 WMTS — Web Map Tile Service（网络地图瓦片服务）

#### 2.3.1 基本概念

WMTS 解决 WMS 的性能问题——将地图预渲染为瓦片并缓存。与 WMS 每次动态渲染不同，WMTS 返回预生成的瓦片，适合高并发场景。

#### 2.3.2 瓦片矩阵集 (TileMatrixSet)

WMTS 的瓦片矩阵集定义了瓦片的坐标参考系、原点、分辨率等参数。**不能假设所有 WMTS 都使用 Web Mercator**。

```
瓦片矩阵集定义结构：
TileMatrixSet
├── CRS (坐标参考系)
├── TileMatrix (每个缩放级别)
│   ├── ScaleDenominator (比例分母)
│   ├── TopLeftCorner (左上角坐标)
│   ├── TileWidth (瓦片宽度，通常 256)
│   ├── TileHeight (瓦片高度，通常 256)
│   ├── MatrixWidth (矩阵宽度=瓦片列数)
│   └── MatrixHeight (矩阵高度=瓦片行数)
```

**常见瓦片矩阵集**：

| 矩阵集标识 | CRS | 瓦片大小 | 典型用途 |
|-----------|-----|---------|---------|
| `WebMercatorQuad` | EPSG:3857 | 256×256 | Web 地图（OpenStreetMap 兼容） |
| `WGS84` | EPSG:4326 | 256×256 | 全球经纬度网格 |
| `GoogleMapsCompatible` | EPSG:3857 | 256×256 | Google Maps 兼容 |
| 自定义矩阵集 | 任意投影 | 任意 | 国家/地方投影 |

> ⚠ **关键规则**：构造 WMTS 瓦片 URL 之前，**必须先读取 GetCapabilities 获取 TileMatrixSet 定义**。不能假设使用 Web Mercator 或 XYZ 方案。

#### 2.3.3 WMTS 请求流程

```
1. GetCapabilities
   → 获取 TileMatrixSet 定义、图层列表、支持的格式

2. 解析 TileMatrixSet
   → 获取 CRS、原点、分辨率、矩阵维度

3. 构造瓦片 URL
   GET /wmts?service=WMTS&version=1.0.0&request=GetTile
     &layer=roads
     &style=default
     &format=image/png
     &TileMatrixSet=EPSG:4326
     &TileMatrix=EPSG:4326:10           ← 缩放级别
     &TileRow=512                       ← 瓦片行号
     &TileCol=256                       ← 瓦片列号
```

#### 2.3.4 WMTS 与 XYZ/TMS 瓦片方案的关系

| 特性 | WMTS (OGC) | XYZ (Google/OSM) | TMS (OSGeo) |
|------|-----------|------------------|-------------|
| 标准 | OGC 07-057r7 | 事实标准 | OSGeo 规范 |
| 行列编号 | TileCol/TileRow | x/y/z（y 从北到南） | x/y/z（y 从南到北） |
| 原点 | 矩阵集定义的左上角 | 地图左上角(西北) | 地图左下角(西南) |
| Y轴方向 | 向下 | 向下 | 向上（与XYZ相反） |
| 瓦片大小 | 可变 | 256×256 | 256×256 |
| 支持的CRS | 任意 | 仅 Web Mercator | 多数投影 |

**XYZ ↔ WMTS 转换公式**（WebMercatorQuad）：
```
WMTS z = XYZ z
WMTS TileCol = XYZ x
WMTS TileRow = (2^z - 1) - XYZ y     ← 注意 Y 轴翻转
```

**XYZ ↔ TMS 转换公式**：
```
XYZ y = TMS y (数值相同，但方向相反 — TMS 的 y=0 在南极)
实际转换：XYZ y = (2^z - 1) - TMS y
```

#### 2.3.5 WMTS vs WMS 性能对比

| 场景 | WMS | WMTS |
|------|-----|------|
| 每次请求响应时间 | 100-500ms（动态渲染） | 5-20ms（预生成瓦片） |
| 服务器负载 | 高（每次重新渲染） | 低（直接返回文件） |
| 适用场景 | 动态数据、少量请求 | 静态底图、高并发 |
| 存储需求 | 低（不缓存瓦片） | 高（全级别瓦片可达 TB 级） |
| 数据更新 | 实时 | 需重新生成瓦片 |

---

### 2.4 OGC API — 现代 RESTful 标准

#### 2.4.1 OGC API 系列概述

OGC API 是 OGC 的**现代 Web 标准栈**，采用 RESTful 架构，使用 JSON、OpenAPI 等行业标准。目的是逐步替代传统的 W*S 服务。

| OGC API | 替代标准 | 说明 |
|---------|---------|------|
| **OGC API Features** | WFS | 矢量要素查询和访问 |
| **OGC API Tiles** | WMTS | 瓦片服务 |
| **OGC API Maps** | WMS | 地图渲染 |
| **OGC API Records** | CSW | 目录/元数据查询 |
| **OGC API Processes** | WPS | 空间处理 |
| **OGC API EDR** | WCS | 环境数据检索（栅格/时间序列） |

#### 2.4.2 OGC API Features（替代 WFS）

**接口设计**：

```
# Landing page（入口）
GET / → { title, description, links }

# Conformance（合规声明）
GET /conformance → { conformsTo: [...] }

# Collections（数据集合列表）
GET /collections → { collections: [...], links }

# 单个集合
GET /collections/{collectionId} → { id, title, extent, crs, links }

# 查询要素
GET /collections/{collectionId}/items → { type: "FeatureCollection", features: [...], links, numberMatched, numberReturned }

# 单个要素
GET /collections/{collectionId}/items/{featureId} → { type: "Feature", id, geometry, properties, links }
```

**分页**：
```
GET /collections/roads/items?limit=100&offset=200
```

**空间过滤**：
```
GET /collections/roads/items?bbox=120.0,30.0,122.0,32.0
```

**属性过滤**：
```
GET /collections/roads/items?type=highway
```

**CRS 支持** — 默认 EPSG:4326 CRS:84 ortho 顺序，但可请求其他 CRS：
```
GET /collections/roads/items?bbox=500000,4200000,520000,4220000&crs=http://www.opengis.net/def/crs/EPSG/0/3857
```

#### 2.4.3 OGC API Tiles（替代 WMTS）

```
# 获取瓦片集合
GET /collections/{collectionId}/tiles → { tileMatrixSetLinks, links }

# 获取瓦片矩阵集信息
GET /tileMatrixSets/{tileMatrixSetId}

# 获取具体瓦片
GET /collections/{collectionId}/tiles/{tileMatrixSetId}/{tileMatrix}/{tileRow}/{tileCol}
```

#### 2.4.4 OGC API Records（替代 CSW）

```
# 搜索记录
GET /collections/metadata/items?q=land+cover&bbox=120,30,122,32&type=dataset
```

#### 2.4.5 支持的服务器

| 服务器 | 支持的标准 | 语言 | 特点 |
|--------|-----------|------|------|
| **pygeoapi** | Features, Tiles, Maps, Records, Processes, EDR | Python | 最完整的 OGC API 实现 |
| **GeoServer** | Features, Tiles, Maps (通过社区模块) | Java | 同时支持传统 W*S 和 OGC API |
| **Martin** | Tiles (MVT) | Rust | 矢量瓦片专用，极高性能 |
| **pg_tileserv** | Tiles (MVT) | Go | PostgreSQL 矢量瓦片，轻量 |
| **ldproxy** | Features | Java | 参考实现 |
| **QGIS Server** | Features (通过插件) | C++ | QGIS 项目直接发布 |

#### 2.4.6 OpenAPI 文档

OGC API 标准要求每个服务提供 OpenAPI/Swagger 文档：

```
GET /api → OpenAPI 3.0 JSON 文档
GET /api.html → Swagger UI 交互式文档（如果服务器提供）
```

示例 OpenAPI 片段：

```json
{
  "openapi": "3.0.3",
  "info": { "title": "OGC API Features - Roads", "version": "1.0.0" },
  "paths": {
    "/collections/roads/items": {
      "get": {
        "parameters": [
          { "name": "bbox", "in": "query", "schema": { "type": "string" } },
          { "name": "limit", "in": "query", "schema": { "type": "integer", "default": 10, "maximum": 10000 } },
          { "name": "offset", "in": "query", "schema": { "type": "integer", "default": 0 } }
        ]
      }
    }
  }
}
```

---

### 2.5 CSW — Catalog Service for Web（网络目录服务）

#### 2.5.1 基本概念

CSW 是地理空间**元数据发现**协议。用于搜索、浏览和查询地理空间数据、服务和相关资源的元数据。

#### 2.5.2 核心操作

| 操作 | 说明 |
|------|------|
| GetCapabilities | 获取服务能力（支持的操作、约束） |
| DescribeRecord | 获取记录结构描述 |
| GetRecords | 搜索记录（主要查询接口） |
| GetRecordById | 通过 ID 获取记录 |
| GetDomain | 获取属性域值 |
| Transaction | 插入/更新/删除元数据记录 |
| Harvest | 从外部资源获取元数据 |

#### 2.5.3 GetRecords 查询示例

**基本搜索**：
```xml
<csw:GetRecords service="CSW" version="2.0.2" resultType="results" maxRecords="20">
  <csw:Query typeNames="csw:Record">
    <csw:ElementSetName>full</csw:ElementSetName>
    <csw:Constraint version="1.1.0">
      <Filter xmlns="http://www.opengis.net/ogc">
        <PropertyIsLike wildCard="*" singleChar="#" escapeChar="!">
          <PropertyName>csw:AnyText</PropertyName>
          <Literal>*land+cover*</Literal>
        </PropertyIsLike>
      </Filter>
    </csw:Constraint>
  </csw:Query>
</csw:GetRecords>
```

**空间搜索**：
```xml
<Filter>
  <And>
    <PropertyIsEqualTo>
      <PropertyName>dc:type</PropertyName>
      <Literal>dataset</Literal>
    </PropertyIsEqualTo>
    <BBOX>
      <PropertyName>ows:BoundingBox</PropertyName>
      <Envelope srsName="EPSG:4326">
        <lowerCorner>-125 24</lowerCorner>
        <upperCorner>-66 49</upperCorner>
      </Envelope>
    </BBOX>
  </And>
</Filter>
```

#### 2.5.4 ISO 19115/19139 元数据

CSW 主要使用 ISO 19115（地理信息元数据）和 ISO 19139（XML 实现）：

| ISO 标准 | 核心内容 | 中国对应 |
|----------|---------|----------|
| ISO 19115-1:2014 | 元数据基础 | GB/T 19710.1-2023 |
| ISO 19115-2 | 影像和格网扩展 | GB/T 19710.2-2016 |
| ISO 19139 | XML 编码实现 | GB/T 45790.1-2025 |

**核心元数据字段**：

| 字段 | 说明 | 示例 |
|------|------|------|
| `dc:title` | 数据集标题 | "全国土地利用数据2020" |
| `dc:abstract` | 摘要描述 | "基于 Landsat 8 生产的 30m ..." |
| `dc:type` | 资源类型 | dataset / service / application |
| `dc:format` | 格式 | GeoPackage / GeoTIFF |
| `dc:identifier` | 标识符 | DOI 或 UUID |
| `dc:date` | 日期 | 2020-06-30 |
| `ows:BoundingBox` | 空间范围 | EPSG:4326 下的 BBOX |
| `dc:subject` | 主题关键词 | 土地利用、遥感 |

#### 2.5.5 QGIS MetaSearch 集成

QGIS 内置 MetaSearch 插件可以连接 CSW 服务：

1. 安装 MetaSearch（默认已安装）
2. 添加 CSW 服务器 URL
3. 按关键词/空间范围搜索
4. 直接加载数据到 QGIS

**常用公共 CSW 端点**：
- INSPIRE Geoportal (欧洲)
- data.gov CSW (美国)
- GeoNetwork 实例（全球多个）
- 国家基础地理信息中心（中国）

---

## 三、数据格式标准（现代云原生）

### 3.1 GeoParquet — 云原生矢量分析

#### 3.1.1 为什么需要 GeoParquet

| 对比维度 | Shapefile | GeoPackage | GeoJSON | **GeoParquet** |
|----------|-----------|------------|---------|----------------|
| 文件大小限制 | 2GB | 无限制 | 无限制 | 无限制 |
| 列存储 | 否 | 否 | 否 | **是**（列存） |
| 压缩 | 无 | 可选 | 可选(gzip) | **内置多编解码** |
| 模式内嵌 | 弱(.dbf) | 是 | 否 | **是**（Parquet schema） |
| 读取性能 | 慢 | 中等 | 慢 | **极快**（谓词下推） |
| 云计算 | 不适合 | 有限 | 有限 | **端到端云原生** |
| SQL 查询 | 否 | 否（需QGIS） | 否 | **是**（DuckDB/Spark） |
| 写入 | 传统工具 | QGIS/GDAL | 所有语言 | GDAL 3.5+ |
| 编码 | 取决于.cpg | 可选 | UTF-8 | UTF-8 |

#### 3.1.2 DuckDB Spatial 直连查询

```sql
-- 本地文件
SELECT name, ST_Area(geom) AS area_sqm
FROM ST_Read('buildings.parquet')
WHERE ST_Within(geom, ST_GeomFromText('POLYGON((...))'));

-- S3 云端文件（无需提前下载）
SELECT COUNT(*), category
FROM ST_Read('s3://my-bucket/data/buildings.parquet')
GROUP BY category;

-- 多文件联合查询
SELECT a.name, b.population
FROM ST_Read('admin_boundaries.parquet') a
JOIN ST_Read('population_grid.parquet') b
  ON ST_Intersects(a.geom, b.geom);
```

#### 3.1.3 GeoParquet 核心要求

| 要求 | 说明 |
|------|------|
| **geometry 列** | 必须使用 `byte_array` 类型，编码为 WKB |
| **元数据** | 必须在文件级元数据中包含 `geo` 键 |
| **BBOX** | 强烈建议包含 bounding box 加速查询 |
| **CRS** | 推荐 PROJJSON 格式的 CRS 描述 |
| **版本** | 目前 GeoParquet 1.1.0（beta） |

**元数据示例**：

```json
{
  "version": "1.1.0",
  "primary_column": "geometry",
  "columns": {
    "geometry": {
      "encoding": "WKB",
      "geometry_types": ["Polygon", "MultiPolygon"],
      "bbox": [-180.0, -90.0, 180.0, 90.0, -500.0, 9000.0],
      "crs": {
        "$schema": "https://proj.org/schemas/v0.7/projjson.schema.json",
        "type": "GeographicCRS",
        "name": "WGS 84 (longitude, latitude)",
        "datum": { "type": "GeodeticReferenceFrame", "name": "World Geodetic System 1984", "ellipsoid": { "name": "WGS 84", "semi_major_axis": 6378137, "inverse_flattening": 298.257223563 } },
        "coordinate_system": { "subtype": "ellipsoidal", "axis": [{"name": "Longitude", "unit": "degree"}, {"name": "Latitude", "unit": "degree"}] },
        "id": { "authority": "OGC", "code": "CRS84" }
      }
    }
  }
}
```

#### 3.1.4 验证与生成

```bash
# 生成 GeoParquet
ogr2ogr -f Parquet output.parquet input.shp

# 带过滤生成
ogr2ogr -f Parquet \
  -where "population > 10000" \
  -sql "SELECT name, population, ST_SimplifyPreserveTopology(geometry, 0.001) AS geometry FROM cities" \
  cities_large.parquet cities.shp

# 验证 GeoParquet
gpq validate output.parquet
# 输出: ✔ BBOX metadata present, ✔ geometry encoding correct, ✔ CRS metadata present
```

---

### 3.2 COG — Cloud Optimized GeoTIFF（云优化栅格）

#### 3.2.1 核心原理

COG 是 GeoTIFF 的**内部组织优化**，而非新格式。三个关键技术：

1. **内部瓦片化** → 将栅格分成小块（默认 512×512）
2. **内部概览** → 多级分辨率金字塔
3. **HTTP Range 请求支持** → 仅下载需要的瓦片，而非整个文件

```
传统 GeoTIFF 访问模式：
  请求整个 10GB 文件 → 下载 10GB → 提取 512×512 瓦片

COG 访问模式：
  HTTP Range 请求 → 仅下载 512×512 瓦片(~64KB) → 显示
                    → 客户端根据 zoom 选择对应概览级别
```

#### 3.2.2 生成与验证

```bash
# 转为 COG（最常用命令）
gdal_translate -of COG \
  -co COMPRESS=DEFLATE \
  -co PREDICTOR=2 \
  -co BLOCKSIZE=512 \
  input.tif output_cog.tif

# 验证 COG
rio cogeo validate output_cog.tif
# 检查项：内部瓦片、概览、HTTP range 兼容性

# 从多个瓦片构建 COG
gdalbuildvrt mosaic.vrt tile_*.tif
gdal_translate -of COG mosaic.vrt full_cog.tif

# 补建概览
gdaladdo -r average input.tif 2 4 8 16 32
```

#### 3.2.3 COG 核心参数

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `-of COG` | 输出格式 | 必选 |
| `-co COMPRESS` | 压缩算法 | DEFLATE / LZW / ZSTD |
| `-co PREDICTOR` | 预测器 | 2（水平差分）/ 3（浮点） |
| `-co BLOCKSIZE` | 瓦片大小 | 256 / 512 |
| `-co RESAMPLING` | 概览重采样 | average / bilinear |
| `-co OVERVIEWS` | 概览策略 | AUTO / NONE / 自定义 |

---

### 3.3 PMTiles — 现代瓦片容器

#### 3.3.1 核心概念

PMTiles 是**单一文件包含所有缩放级别的瓦片归档**。基于 HTTP Range 请求按需读取，无需瓦片服务器。

```
传统瓦片部署：
  数百万个独立文件 → 需要瓦片服务器 → CDN → 客户端
  （百万文件×每个4KB = 4GB+，部署复杂）

PMTiles 部署：
  1个 .pmtiles 文件 → S3/R2/任意静态托管 + 支持Range请求 → CDN → 客户端
  （1个文件，部署如上传普通文件）
```

#### 3.3.2 生成 PMTiles

```bash
# 从 GeoJSON 生成（基本用法）
tippecanoe -o output.pmtiles \
  --maximum-zoom=14 --minimum-zoom=4 \
  -l layer_name \
  input.geojson

# 从 GeoParquet 通过管道生成
ogr2ogr -f GeoJSONSeq /vsistdout/ buildings.parquet | \
  tippecanoe -o buildings.pmtiles -l buildings -zg --drop-densest-as-needed

# 智能 zoom 选择和密度控制（推荐）
tippecanoe -o output.pmtiles \
  -zg --drop-densest-as-needed \
  --extend-zooms-if-still-dropping \
  --simplification=4 \
  --detect-shared-borders \
  -l buildings \
  buildings.geojson

# MBTiles → PMTiles 转换
pmtiles convert input.mbtiles output.pmtiles
```

#### 3.3.3 MapLibre 中使用 PMTiles

```javascript
// 注册 pmtiles:// 协议
const protocol = new pmtiles.Protocol();
maplibregl.addProtocol("pmtiles", protocol.tile);

const map = new maplibregl.Map({
  container: 'map',
  style: {
    version: 8,
    sources: {
      buildings: {
        type: 'vector',
        url: 'pmtiles://https://your-cdn.example.com/buildings.pmtiles',
      }
    },
    layers: [{
      id: 'buildings-fill',
      type: 'fill',
      source: 'buildings',
      'source-layer': 'buildings',
      paint: { 'fill-color': '#888', 'fill-opacity': 0.6 }
    }]
  },
  center: [120.15, 30.25],
  zoom: 13
});
```

#### 3.3.4 PMTiles 部署陷阱 ⚠

| 陷阱 | 说明 | 解决方案 |
|------|------|---------|
| **CDN 不缓存 Range 请求** | Cloudflare 等 CDN 默认不缓存 206 响应 | 配置 Page Rules 或 Cache Rules 显式缓存 |
| **CORS 未配置** | 跨域请求被浏览器阻止 | 设置 `Access-Control-Allow-Origin: *` |
| **Python http.server 不兼容** | Python 内置 HTTP 服务器不支持 Range 请求 | 使用 `npx serve` / `caddy file-server` / `RangeHTTPServer` |
| **eTag/缓存头丢失** | 无 `Content-Range` 响应头 | 确保 HTTP 服务器正确返回 206 和 Content-Range |

**PMTiles 本地测试检查清单**：
```
1. 打开 HTML 页面的 DevTools → Network 标签
2. 查找 .pmtiles 请求 → 确认返回 206 Partial Content
3. 如果返回 200 → 服务器不支持 Range 请求 → 换服务器
4. 如果请求卡住 → 检查 CORS 头是否包含 GET 和 HEAD
```

#### 3.3.5 文件检查

```bash
# 查看 PMTiles 元数据
pmtiles show output.pmtiles
# 输出: bounds, min/max zoom, layers, tile size, compression

# 提取子区域
pmtiles extract input.pmtiles output.pmtiles \
  --bbox=120.0,30.0,122.0,32.0
```

---

### 3.4 GeoPackage (.gpkg) — SQLite 交换格式

#### 3.4.1 核心特性

| 特性 | 说明 |
|------|------|
| **基础** | 基于 SQLite 3 数据库 |
| **多数据合一** | 矢量 + 栅格 + 瓦片存于单个文件 |
| **OGC 标准** | 2014 年正式采纳 |
| **QGIS 默认** | QGIS 3.0+ 默认存储格式 |
| **跨平台** | 所有主流 GIS 软件原生支持 |
| **扩展机制** | 通过 Extension 注册新功能 |

#### 3.4.2 使用场景

| 场景 | 推荐 GeoPackage | 原因 |
|------|----------------|------|
| 桌面 GIS 数据交换 | ✅ 推荐 | QGIS/ArcGIS 原生支持，单文件便携带 |
| 多图层项目归档 | ✅ 推荐 | 一个文件包含所有图层 |
| 离线地图应用 | ✅ 推荐 | 瓦片+矢量一体 |
| **云原生大数据分析** | ❌ 不推荐 | 无列存、无谓词下推、不适合 S3 |
| **流式传输** | ❌ 不推荐 | SQLite 不适合 HTTP Range 分块读取 |

#### 3.4.3 基本操作

```bash
# 创建 GeoPackage
ogr2ogr -f GPKG output.gpkg input.shp -nln layer_name

# 添加多个图层
ogr2ogr -f GPKG output.gpkg roads.shp -nln roads
ogr2ogr -f GPKG output.gpkg buildings.shp -nln buildings -update

# 列出图层
ogrinfo output.gpkg

# 导出为其他格式
ogr2ogr -f Parquet layer.parquet output.gpkg roads
```

#### 3.4.4 云环境限制

GeoPackage 的 SQLite 底层设计决定了它在云环境中存在问题：

- **无列存**：不能只读需要的列
- **无谓词下推**：必须读取整个数据库文件才能过滤
- **写入锁**：SQLite 不支持并行写入
- **HTTP Range 不友好**：不能只读取文件的特定部分

**结论**：GeoPackage 适合桌面/局域网数据交换，但应**逐步转向 GeoParquet** 用于云环境。

---

### 3.5 FlatGeobuf — 流式 HTTP 矢量

#### 3.5.1 核心优势

FlatGeobuf 专为 **HTTP 流式传输**设计。文件内部包含基于 Hilbert R 树的空间索引。

```
FlatGeobuf 架构：
 ┌─────────────────────────────────────┐
 │ Header (魔数 + 索引偏移)            │
 ├─────────────────────────────────────┤
 │ Hilbert R-tree 索引                 │ ← 空间索引（无需全量扫描）
 ├─────────────────────────────────────┤
 │ 数据块 1 (100 条要素)              │
 │ 数据块 2 (100 条要素)              │
 │ 数据块 3 (100 条要素)              │
 │ ...                                 │
 └─────────────────────────────────────┘
```

特点：
- 单文件，无需索引文件
- 空间查询先查索引 → 仅读取相关数据块
- 适合 Web 客户端直接读取（无需 GeoServer/PostGIS）
- 串流读取，内存友好

#### 3.5.2 使用方式

```bash
# 生成 FlatGeobuf
ogr2ogr -f FlatGeobuf output.fgb input.shp

# GDAL/OGR 直接读取
ogr2ogr -f Parquet output.parquet input.fgb
```

---

### 3.6 COPC — Cloud Optimized Point Cloud

#### 3.6.1 设计原理

COPC 是 LASzip 编码的点云数据，以 COG 方式组织——内部带空间索引和八叉树。

```
COPC 文件结构：
 ├── LAS 头 + VLR (变长记录)
 ├── COPCD 索引 VLR ← 八叉树空间索引
 ├── 点数据，COG 方式组织（分块+索引）
```

#### 3.6.2 生成与使用

```bash
# LAS → LAZ → COPC
pdal translate input.las output.laz
pdal translate input.laz output.copc.laz \
  --writers.copc.filename=output.copc.laz

# 直接转换
pdal translate input.las output.copc.laz

# 验证 COPC
pdal info output.copc.laz
```

#### 3.6.3 EPT vs COPC

| 特性 | EPT | COPC |
|------|-----|------|
| 格式 | 多文件（八叉树目录） | 单文件 |
| 部署 | 困难（需要服务器） | 简单（任意HTTP） |
| 趋势 | 逐渐被替代 | 新标准，推荐 |
| 互操作 | PDAL / Cesium | PDAL / GDAL 3.8+ / QGIS |

---

### 3.7 其他关键格式速查

#### 3.7.1 Zarr / NetCDF

| 格式 | 适用场景 | 特点 |
|------|---------|------|
| **NetCDF (.nc)** | 气候/海洋数据，多维度科学数据 | 成熟生态（CDO、xarray），自描述 |
| **Zarr** | 云原生 n 维数组 | 分块存储，S3 友好，并行读/写 |

```python
# xarray 读取 NetCDF
import xarray as xr
ds = xr.open_dataset('temperature.nc')
# 或 Zarr
ds = xr.open_zarr('s3://bucket/temperature.zarr')
```

#### 3.7.2 GeoJSON / GeoJSONSeq

| 格式 | 文件扩展名 | 适用场景 |
|------|-----------|---------|
| **GeoJSON** | .geojson / .json | API 响应、< 几 MB 的数据、调试查看 |
| **GeoJSONSeq** | .geojsonl | 流式管道传输、大批量数据 |

```bash
# GeoJSONSeq 用于管道流式转换
ogr2ogr -f GeoJSONSeq /vsistdout/ large.gpkg | \
  tippecanoe -o tiles.pmtiles -zg
```

#### 3.7.3 STAC — SpatioTemporal Asset Catalog

STAC 是**栅格数据发现协议**，不是数据格式本身。

```
STAC 层级结构：
   Catalog (目录)
     └── Collection (集合：如 Landsat 8)
           └── Item (项：单景影像)
                ├── 元数据 (时间、空间范围、波段)
                ├── 缩略图链接
                └── Asset 链接 (COG/GeoTIFF 文件 URL)
```

```json
{
  "stac_version": "1.0.0",
  "type": "Feature",
  "stac_extensions": ["eo", "proj"],
  "id": "LC08_L1TP_042034_20200301_20200301_01_RT",
  "geometry": { "type": "Polygon", "coordinates": [[...]] },
  "properties": {
    "datetime": "2020-03-01T18:57:29Z",
    "platform": "landsat-8",
    "eo:cloud_cover": 2.3
  },
  "assets": {
    "B4": { "href": "s3://bucket/LC08/.../B4.tif", "type": "image/tiff; application=geotiff" },
    "B8": { "href": "s3://bucket/LC08/.../B8.tif", "type": "image/tiff; application=geotiff" }
  }
}
```

**STAC API 端点**：
- `/stac` — Landing page
- `/collections` — 集合列表
- `/collections/{id}/items` — 集合内项列表
- `/search` — 空间/时间/属性搜索

---

## 四、坐标轴顺序陷阱 ⚠（本章必读）

### 4.1 问题根源

OGC 标准遵循 ISO 19111 的**"坐标参考系权威定义"**——即 EPSG:4326 的权威定义顺序是 (latitude, longitude)。但这与 GIS 行业惯例和 GeoJSON 规范（始终 lon,lat）冲突。

```
ISO/OGC 定义: EPSG:4326 = (lat, lon)  ← 权威顺序
行业惯例:     EPSG:4326 = (lon, lat)  ← 编程习惯
GeoJSON 强制: 始终 (lon, lat)         ← RFC 7946 明确规定
```

### 4.2 各种标准/格式的轴序总表

| 标准/格式 | CRS | 轴序 | 备注 |
|-----------|-----|------|------|
| **WMS 1.1.1** | EPSG:4326 | **(lon, lat)** | bbox = (lon_min, lat_min, lon_max, lat_max) |
| **WMS 1.3.0** | EPSG:4326 | ⚠ **(lat, lon)** | bbox = (lat_min, lon_min, lat_max, lon_max) |
| **WMS 1.3.0** | CRS:84 | **(lon, lat)** | 安全替代方案 |
| **WFS GML** | EPSG:4326 | ⚠ **(lat, lon)** | 遵循服务 CRS 的权威顺序 |
| **WFS GeoJSON** | EPSG:4326 | **(lon, lat)** | GeoJSON 规范强制 |
| **WMTS** | WebMercatorQuad (EPSG:3857) | **(x, y)** | 与 XYZ 方案一致 |
| **WMTS** | WGS84 矩阵集 (EPSG:4326) | ⚠ **取决于矩阵集定义** | 必须先读 Capabilities |
| **GeoJSON (RFC 7946)** | 默认 CRS84 | **(lon, lat)** | 强制 lon,lat，不允许其他 CRS |
| **GeoPackage** | 任意 | **取决于存储的 CRS** | SQLite 元数据中定义 |
| **GeoParquet** | 默认 OGC:CRS84 | **(lon, lat)** | 推荐 CRS84 |
| **Shapefile .prj** | 任意 | **由 .prj 文件定义** | 旧数据可能缺 .prj |

### 4.3 DuckDB Spatial CRS 严格性 ⚠

DuckDB Spatial 1.5+ 存在一个**极度容易触发**的陷阱：

```sql
-- 这会报错！"geometries of different CRS: EPSG:4326 vs OGC:CRS84"
SELECT COUNT(*) FROM
  ST_Read('data1.geojson') a           -- 自动标记为 OGC:CRS84
  JOIN ST_Read('data2.parquet') b        -- 可能标记为 EPSG:4326
  ON ST_Intersects(a.geom, b.geom);
```

**同样的坐标值，不同的 CRS 标签 → 连接失败！**

**修复方案**：
```sql
-- 统一所有输入到同一个 CRS 标签
SELECT ST_SetSRID(geom, 'OGC:CRS84') AS geom FROM ST_Read('data.geojson');

-- 或统一到 EPSG:4326
SELECT ST_SetSRID(geom, 'EPSG:4326') AS geom FROM ST_Read('data.parquet');

-- 管道中始终使用相同的标签
-- 推荐 OGC:CRS84 因为 GeoJSON 默认此标签
```

### 4.4 pyproj 的 always_xy ⚠

```python
from pyproj import Transformer

# ❌ 错误：pyproj 默认使用权威轴序 (lat, lon)
t = Transformer.from_crs("EPSG:4326", "EPSG:3857")
x, y = t.transform(30.5, 120.5)   # pyproj 理解成 (lat, lon) → 结果错误!

# ✅ 正确：强制 always_xy=True
t = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
x, y = t.transform(120.5, 30.5)   # 输入 (lon, lat) → 正确!
```

> ⚠ **黄金法则**：始终使用 `always_xy=True`，除非你明确需要权威轴序。

### 4.5 诊断表："如果看到 X，检查 Y"

| 症状 | 可能原因 | 检查项 |
|------|---------|--------|
| 地图数据偏移到另一半球 | 经纬度互换 | lon∈[-180,180], lat∈[-90,90] → 如果 lon 在 [-90,90] 说明互换了 |
| WMS 图层错位 | WMS 1.3.0 + EPSG:4326 轴序 | 切换为 CRS:84 或手动翻转 bbox |
| WFS GML 坐标与 GeoJSON 不一致 | GML 返回 (lat,lon)，GeoJSON 是 (lon,lat) | 检查 outputFormat，做坐标翻转 |
| DuckDB 连接失败 | CRS 标签不匹配 | 用 ST_SetSRID 统一所有输入的 CRS 标签 |
| pyproj 转换结果异常 | 未使用 always_xy=True | 添加 always_xy=True |
| WMTS 瓦片显示混乱 | 使用了错误的 Y 轴方向 | 检查矩阵集定义 → Y 轴是向下还是向上 |
| QGIS 加载 OGC 图层位置错误 | QGIS 自动处理了轴序但处理错误 | 检查 QGIS 项目 CRS 设置 |

### 4.6 安全编码实践

```python
# WMS 请求安全模板
def build_wms_url(base_url, layer, bbox_lonlat, width, height, version="1.3.0"):
    if version == "1.3.0":
        # 使用 CRS:84 避免轴序问题
        params = {
            "service": "WMS",
            "version": "1.3.0",
            "request": "GetMap",
            "layers": layer,
            "crs": "CRS:84",           # ← 安全的 (lon, lat) 顺序
            "bbox": ",".join(map(str, bbox_lonlat)),  # lon_min,lat_min,lon_max,lat_max
            "width": width,
            "height": height,
            "format": "image/png"
        }
    else:
        params = {
            "service": "WMS",
            "version": "1.1.1",
            "request": "GetMap",
            "layers": layer,
            "srs": "EPSG:4326",         # 1.1.1 中 EPSG:4326 = (lon, lat)
            "bbox": ",".join(map(str, bbox_lonlat)),
            "width": width,
            "height": height,
            "format": "image/png"
        }
    return f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
```

---

## 五、空间标识符标准

### 5.1 空间 ID 体系对比

| ID 体系 | 标识符格式 | 覆盖范围 | 用途 | 示例 |
|---------|-----------|---------|------|------|
| **UN/LOCODE** | 5字符码 (国家2+地点3) | 全球贸易/运输地点 | 物流、海关、航运 | `CN SHA` (上海) |
| **GeoNames ID** | 数字ID | 全球 1000万+ 地名 | 地名查找、地理编码 | `1796236` (上海) |
| **Wikidata QID** | Q+数字 | 全球实体（含地名） | 跨域知识图谱关联 | `Q8686` (上海) |
| **OpenStreetMap ID** | node/way/relation + 数字 | 全球地理要素 | 地图编辑、POI 关联 | `r913067` (上海关系ID) |
| **Who's On First ID** | 数字ID | 全球行政区划层级 | 地名层级体系 | `85669817` (上海) |
| **Open Location Code (Plus Code)** | 字母数字字符串 | 全球 | 无地址区域定位 | `8Q23JQ3C+XX` (上海某处) |

### 5.2 ID 使用原则

```
// 最佳实践：一个地点的多 ID 记录
{
  "name": "上海市",
  "country_code": "CN",
  "admin_path": "中国 > 上海",
  "osm_type": "relation",
  "osm_id": 913067,
  "wikidata_qid": "Q8686",
  "geonames_id": 1796236,
  "unlocode": "CN SHA",
  "open_location_code": "8Q23JQ3C+",
  "source": "OSM 2024-06-01",
  "source_version": "planet_20240601"
}
```

> ⚠ **重要**：不同提供商的 ID 不互通。跨系统关联需要映射表（crosswalk），并记录来源、匹配置信度和更新日期。

### 5.3 Open Location Code (Plus Code)

Google 推出的开放位置编码，用于在没有传统地址的地方提供全球地址：

```
格式: XXXX+XX 区域名称
示例: 8Q23JQ3C+V2 上海  → 约 14m×14m 精度
      8Q23JQ3C+     → 约 275m×275m 精度
```

**特点**：
- 开放标准，免费使用
- 全球覆盖，基于经纬度自动生成
- 不依赖任何政府地址数据库
- 通过缩短码长控制精度

---

## 六、许可标准与合规

### 6.1 主要数据许可类型

| 数据源 | 许可协议 | 关键限制 | 衍生数据许可 |
|--------|---------|---------|-------------|
| **OpenStreetMap** | ODbL (Open Database License) | **传染性** — 衍生数据必须也以 ODbL 发布 | ODbL |
| **Overture Maps** | CDLA-Permissive 2.0（主要） | 署名即可，无传染性 | 任意 |
| **Overture (FourSquare POI)** | Apache 2.0 | 署名 + 免责声明 | 任意 |
| **Overture (OSM 派生)** | ODbL | 传染性 — 与 OSM 相同 | ODbL |
| **Sentinel (ESA)** | 免费 + 署名 | 必须署名 ESA，使用条款有 PDF 文档 | 任意 |
| **Copernicus** | CC-BY 4.0 | 署名即可 | 任意 |
| **Landsat (USGS/NASA)** | 公共领域 | 无限制（鼓励署名） | 任意 |
| **Microsoft Building Footprints** | 公共领域 | 无限制，**但如使用 OSM 派生的版本则为 ODbL** | 取决于版本 |
| **Natural Earth** | 公共领域 | 无限制 | 任意 |
| **GADM** | 学术免费 / 商业需许可 | 商业使用需购买许可 | 取决于许可 |
| **GeoNames** | CC-BY 4.0 | 署名即可 | 任意 |

### 6.2 OSM ODbL 传染性详解 ⚠

ODbL 的核心是**"相同方式共享"(Share-Alike)**：

```
如果你使用了 OSM 数据：
✓ 可以：在地图上展示 OSM 数据（需署名 "© OpenStreetMap contributors"）
✓ 可以：下载并本地分析 OSM 数据
✓ 可以：将 OSM 数据与其他数据结合使用（前提是结合后的数据库继续以 ODbL 发布）
✗ 不可以：将 OSM 数据用于衍生工作后以专有许可发布
✗ 不可以：制作基于 OSM 的 POI 数据集并以商业许可出售
⚠ 灰色地带：使用 OSM 作为"训练数据"产生的模型是否受 ODbL 约束（法律争议中）
```

### 6.3 数据管道中的许可追踪

在生产系统中，配照追踪是必要的：

```python
# 为每个数据集维护许可元数据
dataset_licenses = {
    "buildings_osm": {
        "source": "OpenStreetMap",
        "license": "ODbL 1.0",
        "attribution_required": True,
        "share_alike": True,
        "derived_license": "ODbL 1.0",
        "download_date": "2024-06-01",
        "extract_url": "https://download.geofabrik.de/asia/china.html"
    },
    "buildings_microsoft": {
        "source": "Microsoft",
        "license": "Public Domain (ODbL if OSM-derived)",
        "attribution_required": False,
        "share_alike": False,
        "derived_license": "Any",
        "download_date": "2024-05-15"
    },
    "sentinel2_imagery": {
        "source": "ESA Sentinel-2",
        "license": "Free + Attribution",
        "attribution_required": True,
        "share_alike": False,
        "derived_license": "Any",
        "download_date": "2024-06-03"
    }
}
```

> ⚠ **管道设计原则**：在数据引入（ingestion）阶段标记许可信息，在数据发布（delivery）阶段强制署名检查。

### 6.4 署名模板

```
# OSM 署名（标准格式）
"© OpenStreetMap contributors"

# Overture 署名
"© Overture Maps Foundation"

# Sentinel 署名
"Contains modified Copernicus Sentinel data [YYYY], processed by ESA"

# 多源合成
"© OpenStreetMap contributors | Microsoft Building Footprints | Sentinel-2 (ESA)"
```

---

## 七、中国国家标准 ↔ OGC 标准映射

### 7.1 核心服务标准映射

| OGC 标准 | GB/T 对应 | 标准名称 | 采标关系 |
|----------|----------|---------|---------|
| WMS 1.3.0 (ISO 19128) | **GB/T 33189-2016** | 地理信息 网络地图服务接口 | MOD（修改采用） |
| WFS 2.0 (ISO 19142) | **GB/T 30319-2013** | 基础地理信息数据库规范 | 对应关系 |
| WMTS 1.0 | **GB/T 39609-2020** | 地理信息 地图瓦片服务 | MOD |
| CSW (ISO 19115/19119) | **GB/T 33188-2016** | 地理信息 网络要素服务 | MOD |
| OGC API Features | **GB/T 39608-2020** | 地理信息 要素服务 | 对应关系 |
| Simple Features (ISO 19125) | **GB/T 30319-2013** | 基础地理信息数据库基本规定 | MOD |
| GeoPackage (ISO 19165) | **GB/T 41449-2022** | 地理信息 GeoPackage | IDT（等同采用） |

### 7.2 元数据标准映射

| ISO/OGC 标准 | GB/T 对应 | 标准名称 |
|-------------|----------|---------|
| ISO 19115-1:2014 | **GB/T 19710.1-2023** | 地理信息 元数据 第1部分：基础 |
| ISO 19115-2 | **GB/T 19710.2-2016** | 地理信息 元数据 第2部分：影像和格网数据扩展 |
| ISO 19139 | **GB/T 45790.1-2025** | 地理信息 XML编码实现 |
| ISO 19157 (数据质量) | **GB/T 33176-2016** | 地理信息 数据质量评价 |

### 7.3 坐标参照系统映射

| 国际 CRS | 中国对应 | 坐标系统名称 |
|----------|---------|-------------|
| EPSG:4326 | CGCS2000 (EPSG:4490) | 2000国家大地坐标系（地理坐标） |
| EPSG:3857 | CGCS2000 对应高斯投影 | 2000国家大地坐标系（投影坐标） |
| EPSG:4479 | — | CGCS2000 地理 3D |
| EPSG:3857 | EPSG:4490 | 需使用局部投影 3°带/6°带 |

> ⚠ **重点项目必须使用 CGCS2000（EPSG:4490），不能使用 WGS84（EPSG:4326）**。

### 7.4 三维标准映射

| OGC 标准 | 中国对应 | 说明 |
|----------|---------|------|
| CityGML 3.0 | **CH/T 9024-2022** (实景三维数据规范) | 实景三维中国建设 |
| 3D Tiles 1.1 | **GB/T 41447-2022** (实景三维) | 三维瓦片流式传输 |
| IndoorGML | 智慧城市 BIM-GIS 融合标准 | 室内空间建模 |

---

## 八、快速决策表

### 8.1 "我想在 Web 上发布地图" → 协议选择决策树

```
开始
 │
 ├─ 数据是否频繁更新（每小时多次）？
 │   ├─ 是 → PostGIS + Martin/OGC API Tiles（实时矢量瓦片）
 │   └─ 否 ↓
 │
 ├─ 需要用户交互查询属性吗？
 │   ├─ 是 → OGC API Features（现代）或 WFS（传统）→ GeoJSON 返回
 │   └─ 否 ↓
 │
 ├─ 数据量 < 100MB 矢量？
 │   ├─ 是 → 转换为 GeoParquet → tippecanoe → PMTiles → 静态部署
 │   └─ 否 ↓
 │
 ├─ 需要动态样式/渲染？
 │   ├─ 是 → GeoServer/MapServer WMS 或 QGIS Server
 │   └─ 否 → PMTiles + MapLibre（矢量瓦片） / COG + TiTiler（栅格瓦片）
 │
 └─ 需要兼容传统 OGC 客户端？
     ├─ 是 → GeoServer（同时支持 WMS/WFS/WMTS + OGC API）
     └─ 否 → OGC API Features + Tiles + Maps（现代 REST）
```

### 8.2 "我需要存储地理数据" → 格式选择矩阵

| 场景 | 数据量 | 访问模式 | 云就绪 | 推荐格式 |
|------|--------|---------|--------|---------|
| 桌面分析 | < 1 GB | 本地文件 | — | GeoPackage (.gpkg) |
| QGIS 项目 | < 5 GB | 本地 + 局域网 | 否 | GeoPackage |
| 云分析 | 任意 | S3/对象存储 SQL | 是 | **GeoParquet** |
| Web 瓦片发布 | < 10 GB | HTTP Range | 是 | **PMTiles** |
| API 响应 | < 5 MB | HTTP | 是 | **GeoJSON** |
| 大文件流式传输 | 任意 | HTTP 流 | 是 | **FlatGeobuf** |
| 栅格云存储 | 任意 | HTTP Range | 是 | **COG** (GeoTIFF) |
| 点云云存储 | 任意 | HTTP Range | 是 | **COPC** |
| 多维科学数据 | 任意 | 分块并行 | 是 | **Zarr** / NetCDF |
| 遥感影像目录 | — | 发现 + 访问 | 是 | **STAC** + COG |
| 归档交换 | < 10 GB | 单文件 | 否 | GeoPackage |
| **永远不要用于新数据** | — | — | — | **Shapefile** |

### 8.3 "我构建 API" → OGC API vs 自定义 REST

| 对比维度 | OGC API (Features) | 自定义 REST |
|----------|-------------------|------------|
| **互操作性** | ✅ 任何 OGC 客户端可直接使用 | ❌ 需要自定义客户端 |
| **文档自动生成** | ✅ OpenAPI 3.0 自动生成 | ⚠ 需要手动维护 |
| **QGIS 支持** | ✅ 原生支持 | ❌ 需要编写插件 |
| **分页** | ✅ 标准 limit/offset | 自定义 |
| **空间过滤** | ✅ 标准 bbox 参数 | 自定义 |
| **CRS 处理** | ✅ 标准方式处理 | 自行实现 |
| **开发难度** | 中等（遵循规范） | 低（完全自由） |
| **性能** | 中等 | 可以极致优化 |
| **适用场景** | 需要与其他 GIS 系统互操作 | 内部系统、性能关键路径 |

### 8.4 "我需要为特定场景选择 OGC 标准"

| 我需要... | 使用标准 | 版本 | 现代替代 |
|-----------|---------|------|---------|
| 在 Web 上显示地图 | WMS | 1.3.0 | OGC API Maps |
| 在地图上点击查询属性 | WMS GetFeatureInfo | — | OGC API Features |
| 下载/编辑矢量数据 | WFS | 2.0 | OGC API Features |
| 高性能瓦片底图 | WMTS | 1.0 | OGC API Tiles / PMTiles |
| 搜索和发现地理数据 | CSW | 2.0.2 | OGC API Records / STAC |
| 空间分析处理 | WPS | 2.0 | OGC API Processes |
| 下载栅格数据 | WCS | 2.1 | OGC API EDR / COG 直读 |
| 发布三维模型 | 3D Tiles / i3s | 1.1 / 1.3 | — |
| 交换桌面 GIS 数据 | GeoPackage | 1.3 | GeoParquet (cloud) |
| 云环境大数据分析 | — | — | GeoParquet + DuckDB |
| 大规模影像发布 | COG | — | — |
| 矢量瓦片 Web 发布 | PMTiles | 3.x | — |
| 卫星影像时空搜索 | STAC | 1.0 | — |

---

## 九、OGC 标准实施与测试

### 9.1 一致性测试

OGC 提供 TEAM Engine 测试框架：

```bash
# TEAM Engine Docker 部署
docker run -d -p 8080:8080 ogccite/teamengine

# 通过 Web 界面运行 WMS 1.3.0 测试
# 访问 http://localhost:8080/teamengine/
# 选择 "WMS 1.3.0 Conformance Test Suite"
```

### 9.2 常见服务端点测试命令

```bash
# 测试 WMS GetCapabilities
curl "http://server/wms?service=WMS&version=1.3.0&request=GetCapabilities" | xmllint --format -

# 测试 WFS 过滤器
curl -X POST "http://server/wfs" \
  -H "Content-Type: application/xml" \
  -d '<GetFeature service="WFS" version="2.0.0" count="5">
        <Query typeNames="roads"/>
      </GetFeature>'

# 测试 OGC API Features Landing Page
curl "http://server/" | jq .

# 测试 OGC API Features Items
curl "http://server/collections/roads/items?limit=5" | jq '.features[0]'

# 测试 STAC 搜索
curl "https://earth-search.aws.element84.com/v1/search" \
  -H "Content-Type: application/json" \
  -d '{"collections":["sentinel-2-l2a"],"bbox":[120,30,122,32],"datetime":"2024-06-01T00:00:00Z/2024-06-03T23:59:59Z","limit":5}' | jq .
```

---

## 十、附录

### 10.1 OGC 官方资源

| 资源 | 地址 |
|------|------|
| OGC 官方网站 | https://www.ogc.org |
| OGC 标准列表 | https://www.ogc.org/standards/ |
| OGC API 文档 | https://ogcapi.ogc.org |
| TEAM Engine 测试 | https://cite.opengeospatial.org/teamengine/ |
| OGC GitHub | https://github.com/opengeospatial |

### 10.2 速记表：最常见 OGC 请求模式

```
# 获取地图（WMS 1.3.0 安全写法）
...?service=WMS&version=1.3.0&request=GetMap&layers=X&crs=CRS:84&bbox=lon_min,lat_min,lon_max,lat_max&width=800&height=600&format=image/png

# 获取矢量数据（WFS 2.0 GeoJSON）
...?service=WFS&version=2.0.0&request=GetFeature&typeNames=X&count=100&outputFormat=application/json

# 获取瓦片（OGC API Tiles）
.../collections/X/tiles/WebMercatorQuad/{z}/{y}/{x}

# 获取要素（OGC API Features）
.../collections/X/items?limit=100&bbox=lon_min,lat_min,lon_max,lat_max

# STAC 时空搜索
.../search -d '{"collections":["X"],"bbox":[...],"datetime":"..."}'
```

### 10.3 未来趋势

| 趋势 | OGC 老标准 | OGC 新标准 | 行业推动力 |
|------|-----------|-----------|-----------|
| RESTful API | W*S (SOAP/XML) | OGC API (REST/JSON/OpenAPI) | 开发者生态 |
| 云原生存储 | GeoPackage/Local | GeoParquet/COG/COPC/Zarr | 云计算 |
| 单一文件瓦片 | 目录式瓦片 | PMTiles | 部署简化 |
| 流式传输 | 全量下载 | FlatGeobuf/GeoJSONSeq | 网络效率 |
| 三维标准 | CityGML/GML 3 | 3D Tiles/i3s/glTF | 可视化需求 |
| 协议驱动发现 | CSW (SOAP) | STAC (REST + JSON) | 卫星数据爆炸 |

---

> **文件版本**：V5.0 初始版 | 发布日期：2026年6月4日
> **关联文件**：←→ `05_国家测绘标准体系.md` (国标与OGC映射) | ←→ `03_数据模型与格式.md` (格式详情) | ←→ `23_WebGIS开发.md` (Web全栈实践) | ←→ `25_三维GIS与数字孪生.md` (三维标准) | ←→ `41_现代GIS数据处理管道.md` (云原生管道)
> **后续计划**：OGC-ISO 双编号对照补充、OGC API EDR 深度覆盖扩展


<!-- wm:坤图_GIS:V1.0 -->
