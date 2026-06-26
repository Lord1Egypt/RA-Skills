# 20_GIS资源共享 | 关联：21_Python_GIS生态.md 23_WebGIS开发.md 31_学习路径与认证资源.md

> **V4.2 新建模块** | 开源数据、在线服务、API接口、中国特有资源一站式索引
> ⚠️ 本模块为资源索引，不保证所有链接持续有效。最后更新：2026-06-04

---

## 一、开源 GIS 数据源

### 1.1 全球基础地理数据

| 数据源 | 类型 | 覆盖 | 分辨率 | 许可 |
|--------|------|------|--------|------|
| **Natural Earth** | 矢量+栅格 | 全球 | 1:10m/1:50m/1:110m | 公共领域 |
| **OpenStreetMap (OSM)** | 矢量 | 全球 | 街道级 | ODbL |
| **GADM** | 行政区划 | 全球 | 0~5级 | 免费非商业 |
| **Global Administrative Areas** | 边界 | 全球 | 国家级/省/市 | CC-BY |
| **GeoNames** | 地名 | 全球 | 点 | CC-BY |
| **SRTM** | DEM | 全球(60°N-56°S) | 30m/90m | 公共领域 |
| **ASTER GDEM** | DEM | 全球(83°N-83°S) | 30m | 免费 |
| **ALOS AW3D30** | DEM | 全球 | 30m | 注册免费 |
| **Copernicus DEM (GLO-30)** | DEM | 全球 | 30m | 免费 |
| **LandSat** | 遥感影像 | 全球 | 15-30m | 公共领域 |
| **Sentinel-2** | 遥感影像 | 全球 | 10-60m | 免费 |
| **OpenTopography** | LiDAR/点云 | 全球 | 亚米级 | CC-BY |

### 1.2 中国特有数据

| 数据源 | 类型 | 说明 | 获取方式 |
|--------|------|------|----------|
| **全国地理信息资源目录服务系统** | 矢量/影像 | 1:100万/1:25万基础地理数据 | data.ngcc.cn 免费下载 |
| **资源环境科学与数据中心** | 专题 | 土地利用/土壤/气象/生态 | resdc.cn |
| **地理空间数据云** | DEM/影像 | ASTER GDEM/LandSat/MODIS | gscloud.cn |
| **国家地球系统科学数据中心** | 多学科 | 地质/海洋/极地/大气 | geodata.cn |
| **天地图 (Tianditu)** | 在线地图 | 国家地理信息公共服务平台 | tianditu.gov.cn |
| **OpenStreetMap 中国** | 矢量 | 中国区域 OSM 数据 | download.geofabrik.de/asia/china.html |
| **国家统计局** | 统计 | 行政区划/人口/经济普查 | stats.gov.cn |
| **北京大学开放研究数据平台** | 研究数据 | 社会经济/环境/健康 | opendata.pku.edu.cn |

### 1.3 省市级别数据

| 数据源 | 覆盖 | 类型 |
|--------|------|------|
| 各省自然资源厅 | 本省 | 基础测绘成果 |
| 各市规划和自然资源局 | 本市 | 规划/土地/建筑 |
| 省市公共数据开放平台 | 本省市 | 政务/交通/环境 |

---

## 二、在线地图服务

### 2.1 中国常用底图服务

| 服务商 | 服务类型 | URL模板 | 坐标系统 |
|--------|----------|--------|----------|
| **天地图 (Tianditu)** | WMTS/XYZ | `https://t{0-7}.tianditu.gov.cn/{layer}/wmts` | CGCS2000 (EPSG:4490) |
| **高德地图** | XYZ | `https://webrd0{1-4}.is.autonavi.com/appmaptile` | GCJ-02 |
| **百度地图** | XYZ | `https://online{0-3}.map.bdimg.com/tile` | BD-09 |
| **腾讯地图** | XYZ | `https://rt{0-3}.map.gtimg.com/tile` | GCJ-02 |

### 2.2 国际底图服务

| 服务商 | 服务类型 | URL |
|--------|----------|-----|
| **Esri World Imagery** | XYZ | `https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}` |
| **Google Maps** | XYZ | `https://mt{0-3}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}` |
| **Bing Maps** | XYZ | `https://t.ssl.ak.dynamic.tiles.virtualearth.net/comp/ch/{quadkey}` |
| **CartoDB** | XYZ | `https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png` |
| **Stamen** | XYZ | `http://tile.stamen.com/terrain/{z}/{x}/{y}.png` |
| **Mapbox** | XYZ | `https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/{z}/{x}/{y}` |

### 2.3 WMS/WMTS/WFS 公共服务

| 服务 | 类型 | URL | 说明 |
|------|------|-----|------|
| **GeoServer 演示** | WMS/WFS | `https://demo.geo-solutions.it/geoserver/ows` | GeoServer 官方演示 |
| **USGS 国家地图** | WMS | `https://basemap.nationalmap.gov/arcgis/services/USGSTopo/MapServer/WMSServer` | 美国地质调查 |
| **NASA GIBS** | WMTS | `https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/wmts.cgi` | NASA 地球观测 |
| **NOAA** | WMS | `https://nowcoast.noaa.gov/arcgis/services/nowcoast/analysis_meteohydro_sfc_ndfd_time/MapServer/WMSServer` | 海洋大气 |

### 2.4 QGIS 中加载在线服务的典型配置

**天地图 WMTS 示例**：
```
连接 URL: https://t0.tianditu.gov.cn/img_w/wmts?tk=YOUR_KEY
图层名称: img
坐标系: EPSG:3857
瓦片矩阵集: w
```

**ArcGIS Pro 中加载 XYZ 底图**：
```
数据源类型: Web Tile Layer
URL模板: https://{subDomain}.tianditu.gov.cn/DataServer?T=vec_w&x={col}&y={row}&l={level}&tk=YOUR_KEY
```

---

## 三、常用 API 与 SDK

### 3.1 地图 JavaScript API

| API/库 | 类型 | 免费/开源 | 中国适用性 |
|--------|------|:--:|:--:|
| **Leaflet.js** | 轻量地图库 | ✅ 开源 | ✅ 需注意 GCJ-02 偏移 |
| **OpenLayers** | 完整 WebGIS | ✅ 开源 | ✅ 支持各种服务 |
| **MapLibre GL JS** | 矢量瓦片 | ✅ 开源 | ✅ 性能优秀 |
| **Cesium.js** | 3D 地球 | ✅ 开源 | ✅ 需处理坐标系 |
| **ArcGIS Maps SDK for JavaScript** | 企业级 | 免费开发 | ✅ |
| **高德地图 JS API** | 中国本地化 | 免费（限额度） | ✅ 原生支持 GCJ-02 |
| **百度地图 JS API** | 中国本地化 | 免费（限额度） | ✅ 原生支持 BD-09 |
| **腾讯地图 JS API** | 中国本地化 | 免费（限额度） | ✅ 原生支持 GCJ-02 |

### 3.2 地理编码/逆地理编码 API

| 服务 | 免费额度 | 覆盖 | 特色 |
|------|:--:|------|------|
| **高德地理编码** | 5000次/天 | 中国 | GCJ-02，POI丰富 |
| **百度地图** | 5000次/天 | 中国 | BD-09，地址信息详实 |
| **腾讯位置服务** | 10000次/天 | 中国 | GCJ-02 |
| **天地图** | 注册使用 | 中国 | CGCS2000，官方权威 |
| **Nominatim (OSM)** | 无限制（有频率限制） | 全球 | 开源，WGS-84 |

### 3.3 路径规划 API

| 服务 | 出行方式 | 覆盖 | 免费额度 |
|------|----------|------|:--:|
| 高德路径规划 | 驾车/步行/骑行/公交 | 中国 | 5000次/天 |
| 百度路线规划 | 驾车/步行/骑行/公交 | 中国 | 5000次/天 |
| OSRM | 驾车/步行/骑行 | 全球 | ✅ 开源自部署 |
| GraphHopper | 驾车/步行/骑行 | 全球 | ✅ 开源自部署 |
| Valhalla | 多模式 | 全球 | ✅ 开源自部署 |

---

## 四、开源 SHP / GeoJSON / GeoPackage 数据

### 4.1 通用数据集

| 数据集 | 格式 | 覆盖 | 下载 |
|--------|------|------|------|
| Natural Earth Quick Start Kit | SHP | 全球 | naturalearthdata.com |
| OSM 导出服务 | SHP/GeoJSON | 按区域 | export.hotosm.org |
| World Bank Data | SHP/GeoJSON | 全球 | data.worldbank.org |
| UN OCHA HDX | SHP/GeoJSON/KML | 人道主义区域 | data.humdata.org |
| DIVA-GIS | SHP | 全球 | diva-gis.org/gdata |

### 4.2 中国 SHP 资源获取途径

1. **全国地理信息资源目录服务系统** (data.ngcc.cn)：1:100万/1:25万矢量
2. **资源环境科学与数据中心** (resdc.cn)：行政区划/土地利用/土壤
3. **中国科学院地理科学与资源研究所**：学术研究数据
4. **各省自然资源厅公开数据目录**：地方基础测绘成果（部分需申请）
5. **GitHub/Gitee** 搜索 "china shp" ：社区整理的开源数据

### 4.3 Shapefile 注意事项

- 字段名限制：最多 10 个字符（DBF 格式限制），中文字段名会被截断
- 编码问题：推荐 UTF-8 编码的 .cpg 文件配合使用
- 文件完整性：一个完整的 Shapefile = .shp + .shx + .dbf + .prj（至少需要前三个）
- 大小限制：单个 .shp 文件 ≤ 2GB

---

## 五、数据格式转换在线工具

| 工具 | 功能 | 限制 |
|------|------|------|
| **ogr2ogr Web** | SHP↔GeoJSON↔KML↔GPKG | 基于 GDAL，支持所有 OGR 格式 |
| **mapshaper.org** | SHP/GeoJSON/TopoJSON 简化/转换 | 浏览器处理，无数据上传 |
| **geojson.io** | GeoJSON 编辑/可视化 | 浏览器编辑 |
| **MyGeodata Converter** | 30+格式互转 | 免费 ≤ 5MB |
| **QGIS** | 全格式支持 | 桌面软件，无限制 |

---

## 六、学习资源与社区

### 6.1 中文社区

| 社区 | 类型 | 链接 | 特点 |
|------|------|------|------|
| OSGeo 中国 | 综合 | osgeo.cn | 开源 GIS 教程/文档/翻译 |
| 麻辣 GISer | 论坛 | malagis.com | 作业/考试/技术问答 |
| GIS 帝国 | 论坛 | gisempire.com | 老牌社区 |
| CSDN GIS 专栏 | 博客 | csdn.net | 海量技术文章 |
| 知乎 GIS 话题 | 问答 | zhihu.com | 深度讨论 |

### 6.2 国际社区

| 社区 | 特点 |
|------|------|
| GIS StackExchange | 专业问答，排名系统 |
| r/gis (Reddit) | 社区讨论，新闻 |
| r/QGIS | QGIS 专属社区 |
| GIS Discord 服务器 | 实时讨论 |
| Esri Community | Esri 官方社区 |

### 6.3 开源 GIS 书籍

| 书名 | 链接 | 语言 |
|------|------|:--:|
| QGIS Training Manual | docs.qgis.org | EN/多语言 |
| Python GDAL/OGR Cookbook | pcjericks.github.io | EN |
| Geocomputation with R | geocompr.robinlovelace.net | EN |
| Geographic Data Science with Python | geographicdata.science/book | EN |
| Open Geospatial Textbook | opengislab.com | EN |
| OSGeo 中国站 教程合辑 | osgeo.cn/docs | 中文 |

---

## 七、数据可视化平台（零代码）

| 平台 | 适用场景 | 免费版 |
|------|----------|:--:|
| **Kepler.gl** | 大规模地理数据可视化 | ✅ 开源 |
| **QGIS** | 桌面 GIS | ✅ 开源 |
| **Datawrapper** | 地图图表 | ✅ 免费版 |
| **Flourish** | 动态地图 | ✅ 免费版 |
| **ArcGIS StoryMaps** | 故事地图 | ✅ |
| **Mapbox Studio** | 自定义底图 | ✅ 免费版 |
| **Google Earth Studio** | 卫星动画 | ✅ 免费 |

---

## 八、未来集成资源（TODO）

### 8.1 待收录

- [ ] 中国1:1万基础地理数据库（涉密，需审批后使用）
- [ ] 全球实时气象数据 API（OpenWeatherMap/和风天气）
- [ ] FlightAware 航班轨迹数据
- [ ] AIS 船舶轨迹数据
- [ ] 各城市共享单车/公交实时数据
- [ ] OpenStreetMap 历史数据归档
- [ ] 中国土地利用/覆盖变化数据集（LUCC）

### 8.2 贡献指南

如果您有优质的 GIS 数据资源或在线服务想要收录，请在以下区域补充：

```
### 新增资源
| 资源名称 | 类型 | URL | 免费/付费 | 备注 |
|----------|------|-----|:--------:|------|
|          |      |     |          |      |
```

---

> **神经连接**：
> - 21_Python_GIS生态.md（Python 数据获取库：geopandas/owslib/requests）
> - 23_WebGIS开发.md（前端加载在线服务：Cesium/Leaflet/OpenLayers）
> - 02_坐标系统与投影.md（WGS-84/GCJ-02/BD-09/CGCS2000 坐标系差异）
> - 05_国家测绘标准体系.md（基础测绘成果管理规定/涉密数据审批流程）

> **V4.2 版本标识** | 新建模块 | 持续集成


<!-- wm:坤图_GIS:V1.0 -->
