---
name: gis
description: Helps with GIS concepts, spatial data formats, projections, and spatial analysis. Use when the user works with shapefiles, GeoJSON, coordinate reference systems, spatial indexes, or needs to design spatial queries and analysis workflows.
---

# GIS（地理信息系统）

本 Skill 聚焦于 **GIS / 空间数据**：数据格式、坐标参考系（CRS）、投影转换、空间索引与查询、以及常见 GIS 分析工作流。与 `map` Skill 偏重可视化与经纬度基础不同，`gis` 更侧重“数据与分析”。

---

## 何时使用

当用户提到或需要：

- Shapefile、GeoJSON、KML、GeoPackage 等空间数据格式
- 坐标参考系（CRS）、EPSG 代码、投影转换（如 WGS84 ↔ Web Mercator）
- 在数据库中进行空间查询（如 PostGIS、SpatiaLite 等）
- 做缓冲区（buffer）、叠加（overlay）、裁剪（clip）、相交（intersect）等空间分析
- 设计 GIS 数据处理/分析管线与最佳实践

---

## 空间数据格式（概念）

- **Shapefile**：一组相关文件（.shp/.shx/.dbf/...），存储矢量数据（点/线/面）及属性，广泛支持但有字段/字符集等限制。
- **GeoJSON**：基于 JSON 的矢量数据格式，适合 Web 与 API；注意 `coordinates` 顺序通常为 `[lon, lat]`。
- **KML/KMZ**：多用于地标/轨迹展示（与地球浏览器配合）。
- **GeoPackage（.gpkg）**：基于 SQLite 的容器，可同时存储矢量与栅格，逐渐成为现代通用格式。

回答时说明哪种更适合用户场景（Web 展示、分析作业、跨系统交换等），避免过深实现细节。

---

## 坐标参考系与投影

- 使用 **EPSG 代码** 标识 CRS（如 WGS84: EPSG:4326；Web Mercator: EPSG:3857）。
- 回答中明确：\n  - 源 CRS（数据当前所用 CRS）。\n  - 目标 CRS（分析/展示所需 CRS）。\n- 对于投影转换，建议使用专业库/工具：\n  - 桌面：QGIS、ArcGIS。\n  - 编程：proj/proj4、GDAL/OGR、常用语言的 GIS 包（如 Python 的 `pyproj`、`geopandas`）。\n\n不要手写复杂投影公式；给出“应调用的库与大致调用方式”，并强调坐标顺序与单位（度/米）。

---

## 空间数据库与查询

- 常见：PostGIS（PostgreSQL 扩展）、SpatiaLite（SQLite 扩展）、部分 NoSQL/搜索引擎的地理扩展。
- 回答要点：\n  - 使用几何列（如 `geometry` 或 `geography`）。\n  - 借助空间索引（如 GIST/BRIN），提高查询性能。\n  - 常用函数：`ST_Distance`、`ST_Intersects`、`ST_Within`、`ST_Buffer`、`ST_Union` 等（以 PostGIS 为例）。\n\n具体 SQL 示例要与用户使用的数据库匹配，不混用不同系统的语法。

---

## 常见 GIS 分析操作（概念）

- **Buffer**：以要素为中心生成一定距离的缓冲区（如道路两侧 500m 范围）。\n- **Clip**：用一个面要素裁剪另一个图层，只保留重叠部分。\n- **Intersect / Union / Difference**：图层之间的空间叠加分析。\n- **Dissolve**：按属性合并几何（如按行政区合并多个多边形）。\n\n回答时可说明使用哪些工具/库执行这些操作（如 QGIS 的菜单路径、GeoPandas/PostGIS 的函数），不必展开所有参数细节。

---

## 与 `map` Skill 的关系

- **`map`**：经纬度、距离、瓦片、Web/移动地图展示与交互。\n- **`gis`**：空间数据格式、CRS/投影、空间查询与分析工作流。\n\n当问题偏“画地图/显示点/算简单距离”时优先用 `map`；当偏“如何存空间数据/做 buffer/叠加分析/CRS 转换”时用 `gis`。

---

## 使用原则

- 在回答中明确 **坐标系、单位与坐标顺序**，避免默认假设产生误导。\n- 遇到需要高精度或特定标准的 GIS 任务时，建议结合官方文档与专门工具，而不是单纯依赖手算或近似公式。\n- 关注性能：对大规模空间数据建议引入空间索引和批处理/分块处理策略。

