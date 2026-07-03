<!-- wm:坤图_GIS:V5.0 -->

# GeoKG 地理知识图谱索引

> 全局唯一知识ID: GIS-KG-INDEX-001
> 版本: V5.0
> 关联模块: 全部知识群组

| 实体类别 | 实体名称 | 全局ID | 关联文件 | 关联实体 |
|----------|----------|--------|----------|----------|
| **坐标系** | CGCS2000 | GIS-KG-CRS-001 | references/02, references/04, 02_EXPANSION | WGS84, BJ54, XA80 |
| **坐标系** | WGS84 | GIS-KG-CRS-002 | references/02, references/32 | CGCS2000, GPS, BDS |
| **坐标系** | 北京54 | GIS-KG-CRS-003 | references/04 | CGCS2000, 七参数 |
| **坐标系** | 西安80 | GIS-KG-CRS-004 | references/04 | CGCS2000 |
| **坐标系** | 地方独立系 | GIS-KG-CRS-005 | 04_EXPANSION | CGCS2000, RTK |
| **软件** | ArcGIS Pro | GIS-KG-SW-001 | references/12, references/38 | ArcPy, GDB, 拓扑 |
| **软件** | QGIS | GIS-KG-SW-002 | references/13, references/44 | PyQGIS, GRASS, SAGA |
| **软件** | CASS | GIS-KG-SW-003 | references/14 | DWG, XDATA, 南方 |
| **软件** | SuperMap | GIS-KG-SW-004 | references/16 | AgentX, 超图, 鸿蒙 |
| **软件** | FME | GIS-KG-SW-005 | references/18 | ETL, Transformer |
| **软件** | LiDAR360 | GIS-KG-SW-006 | references/36 | 点云, PTD, CSF |
| **软件** | GlobalMapper | GIS-KG-SW-007 | references/17 | 万能转换 |
| **软件** | iData | GIS-KG-SW-008 | references/15 | 南方数码, 质检引擎 |
| **软件** | MapGIS | GIS-KG-SW-009 | MapGIS_10.7_完整手册 | 中地数码, 国产 |
| **标准** | GB/T国标 | GIS-KG-STD-001 | references/05 | CH/T, OGC |
| **标准** | CH/T行标 | GIS-KG-STD-002 | references/05, references/06 | GB/T |
| **标准** | OGC国际 | GIS-KG-STD-003 | references/40 | WMS, WFS, WMTS |
| **标准** | 地方规范 | GIS-KG-STD-004 | STD_EXPANSION | 各省细则 |
| **格式** | 矢量格式 | GIS-KG-FMT-001 | references/03, references/43 | GDB, SHP, GeoJSON |
| **格式** | 栅格格式 | GIS-KG-FMT-002 | references/03 | GeoTIFF, COG, Zarr |
| **格式** | 点云格式 | GIS-KG-FMT-003 | references/03, 03_EXPANSION | LAS, LAZ, COPC |
| **格式** | 三维格式 | GIS-KG-FMT-004 | references/03, references/25 | 3DTiles, I3S, OSGB |
| **格式** | 时序格式 | GIS-KG-FMT-005 | references/03 | STAC, GeoParquet |
| **算法** | 坐标转换 | GIS-KG-ALG-001 | atomic_skills/coordinate_transform | 七参数, 四参数 |
| **算法** | 拓扑修复 | GIS-KG-ALG-002 | atomic_skills/topology_repair | 面重叠, 空洞 |
| **算法** | 空间分析 | GIS-KG-ALG-003 | references/33 | Moran, Kriging, DBSCAN |
| **算法** | 深度学习 | GIS-KG-ALG-004 | 27_EXPANSION | SAM, UNet, YOLO |
| **算法** | 插值算法 | GIS-KG-ALG-005 | references/33 | IDW, Spline, 克里金 |
