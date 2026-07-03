# R 语言 GIS 生态 | 关联：21_Python_GIS生态.md 28_项目案例集.md 33_空间分析与统计.md | 群组六：现代GIS技术栈

> R 语言 GIS 完整技术栈：矢量(sf) → 栅格(terra) → 专题制图(tmap) → 交互Web(leaflet) → 空间统计 → 建模发布
> 面向科研/统计建模/出版级制图场景，覆盖安装、操作、场景速查，可直接复制运行

---

## 一、R vs Python：GIS场景定位对比

### 1.1 核心定位差异

| 维度 | R | Python |
|------|-----|--------|
| **核心受众** | 统计学家、生态学家、地理学家、公共卫生研究者 | 软件工程师、数据工程师、DevOps、通用开发者 |
| **GIS优势场景** | 空间统计建模(GLM/GWR/地统计)、出版级专题制图、探索性空间数据分析(ESDA) | 大规模生产级管道、Web服务集成、深度学习(GIS+CV)、自动化ETL |
| **矢量引擎** | sf (基于GDAL/GEOS/PROJ, Simple Features标准) | GeoPandas/Shapely/Fiona (同样基于GDAL底层) |
| **栅格引擎** | terra (C++底层, 替换raster包) | Rasterio/rioxarray (同样基于GDAL底层) |
| **交互可视化** | tmap(view模式) + leaflet(htmlwidgets) | Folium/ipyleaflet/keplergl |
| **空间统计** | spdep/spatstat/gstat/spGAM — 生态最完整 | PySAL — 功能接近但生态不如R |
| **出版系统** | RMarkdown/knitr/Quarto — 可重复研究黄金标准 | Jupyter + nbconvert — 灵活性高但不如R | 
| **包管理** | CRAN (19,000+包, 严格审核) + R-Universe | PyPI/conda-forge (更松散) |
| **学习曲线** | 统计思维门槛高，但tidyverse语法一致性好 | 通用编程范式，入门更平滑 |

### 1.2 何时选择 R

- ★★☆ 需要做空间广义线性模型(GLM)、GWR地理加权回归、Kriging插值
- ★★☆ 需要生成学术论文级别的专题地图（配色/图例/比例尺/指北针一体化）
- ★★★ 需要进行探索性空间数据分析(ESDA): Moran's I、LISA、空间滞后模型
- ★★☆ 生态学/物种分布模型(SDM): MaxEnt替代、Biomod2、ENMeval
- ★☆☆ 需要可重复研究报告：RMarkdown + knitr → PDF/Word/HTML自动生成
- ★☆☆ 人口健康地理、环境流行病学、犯罪地理等经典统计地理学领域

### 1.3 核心生态架构图

```
┌─────────────────────────────────────────────────┐
│            R GIS 生态系统 (四层架构)              │
├─────────────────────────────────────────────────┤
│  出版与交互层                                    │
│  tmap(专题图) leaflet(Web) mapview(速览)         │
│  ggplot2+ggspatial(科学图) shiny(dash)           │
├─────────────────────────────────────────────────┤
│  建模与统计层                                    │
│  spdep(Moran/I) gstat(Kriging) spatstat(点模式)  │
│  spGAM(GAM) nlme(空间混合效应) dismo/biomod2(SDM)│
├─────────────────────────────────────────────────┤
│  核心数据处理层                                  │
│  sf(矢量) terra(栅格) stars(多维)                │
│  exactextractr(快速区域统计) qgisprocess(QGIS)   │
├─────────────────────────────────────────────────┤
│  底层引擎层 (C/C++编译)                          │
│  GDAL / GEOS / PROJ / NetCDF / SQLite            │
└─────────────────────────────────────────────────┘
```

### 1.4 安装环境配置

```r
# 推荐：R >= 4.2.0，使用 pre-compiled binaries
# Windows: 安装 Rtools42+ (必须，包含GDAL/PROJ编译链)
# macOS: brew install gdal geos proj udunits
# Linux: sudo apt install libgdal-dev libgeos-dev libproj-dev libudunits2-dev

# 核心GIS包安装
install.packages(c("sf", "terra", "tmap", "leaflet", "mapview"))
install.packages(c("stars", "exactextractr", "qgisprocess"))
install.packages(c("spdep", "spatstat", "gstat", "dismo"))
install.packages(c("tidygeocoder", "whitebox", "r5r"))

# 从GitHub安装开发版（可选）
remotes::install_github("r-spatial/sf")
remotes::install_github("rspatial/terra")
```

---

## 二、核心库深度解析

### 2.1 sf —— Simple Features 矢量引擎（必学 ★★★）

sf 是 R GIS 生态的绝对基础。底层连接 GDAL（读写）、GEOS（几何运算）、PROJ（坐标转换）、S2（球面几何）。

#### 2.1.1 数据读写

```r
library(sf)

# 读取 — 支持 90+ 格式
roads <- st_read("data/roads.shp")                    # Shapefile（注意：字段名截断10字符）
parks <- st_read("data/parks.geojson")                # GeoJSON
admin <- st_read("data/admin.gpkg", layer = "districts")  # GeoPackage 指定图层
pipes <- st_read("PG:dbname=utility host=localhost",  # PostGIS 直连
                 query = "SELECT * FROM pipes WHERE status='active'")

# 写入
st_write(roads, "output/roads_clean.gpkg", layer = "roads", delete_layer = TRUE)
st_write(parks, "output/parks.geojson")
# GeoPackage 性能最优推荐大数据量，Shapefile 仅用于协作交换（注意字段名限制！）

# 列出可用的驱动和图层
st_drivers() |> subset(grepl("GPKG|GeoJSON|ESRI|PostgreSQL", long_name))
st_layers("data/regions.gpkg")  # 查看GeoPackage内图层列表
```

#### 2.1.2 坐标系处理 —— 核心反模式警告

```r
# 查询当前CRS
st_crs(roads)  # 输出: WGS 84 / EPSG:4326

# 坐标系转换
roads_utm <- st_transform(roads, crs = 32736)  # 转UTM Zone 36S

# 查找合适UTM带号（自动）
lon_center <- st_coordinates(st_centroid(st_union(roads)))[1, 1]
utm_zone <- floor((lon_center + 180) / 6) + 1
epsg_utm <- ifelse(mean(st_coordinates(roads)[, 2]) > 0,
                   32600 + utm_zone, 32700 + utm_zone)

# ★★★ 关键模式：always_xy 修复坐标列顺序
# 问题：sf默认Y/X顺序，GeoJSON标准是X/Y，容易混淆
pt <- data.frame(lon = 116.39, lat = 39.91)
pt_sf <- st_as_sf(pt, coords = c("lon", "lat"), crs = 4326)  # 明确X(col1)=lon

# ★★★ 反模式：绝对不要在EPSG:4326上做距离/面积运算!!
# 错误：st_buffer(roads, dist = 100)    # 100度≈11100km，完全错误
# 正确：
roads_utm <- st_transform(roads, 32736)
roads_buffered <- st_buffer(roads_utm, dist = 100)  # 100米缓冲区（正确）
```

#### 2.1.3 空间操作

```r
# 空间查询
intersects_idx <- st_intersects(points, polygons, sparse = TRUE)     # 返回索引列表
contains_idx <- st_contains(polygons, points)
within_idx <- st_within(points, polygons)

# 空间联接 — 用空间关系Join属性
joined <- st_join(points, admin, join = st_intersects)  # 默认左连接

# 空间聚合 — 按行政区分组合并几何
admin_stats <- census_blocks |>
  group_by(county_id) |>
  summarise(total_pop = sum(population, na.rm = TRUE))  # 自动做 st_union

# 几何运算
roads_geom <- st_geometry(roads)        # 提取几何列
buffered <- st_buffer(roads_geom, 500)  # 500米缓冲区
intersection <- st_intersection(roads, flood_zone)  # 裁剪
diff_area <- st_difference(admin, water_bodies)     # 擦除水域

# 距离矩阵（关键：必须在投影坐标系下运行！）
dist_mat <- st_distance(st_transform(points, 32736))  # 输出 meters

# 有效性修复
invalid_fixed <- st_make_valid(bad_geometry)
```

#### 2.1.4 sf 速查表

| 函数 | 用途 | 注意 |
|------|------|------|
| `st_read()` / `st_write()` | 矢量读写 | GPKG>GeoJSON>SHP |
| `st_crs()` / `st_transform()` | CRS查询/转换 | 先统一CRS再做空间操作 |
| `st_intersects()` / `st_contains()` / `st_within()` | 空间关系 | sparse=TRUE返回索引 |
| `st_join()` | 空间连接 | left=TRUE保留左侧所有行 |
| `st_union()` / `st_combine()` | 几何合并 | union去重复/combine不去重 |
| `st_buffer()` | 缓冲区 | **必须投影坐标系！** |
| `st_area()` / `st_length()` | 面积/长度 | 地理坐标系返回球面面积(平米) |
| `st_centroid()` | 中心点 | 使用 S2 球面计算 |
| `st_make_valid()` | 修复无效几何 | 使用前检查 st_is_valid() |
| `st_coordinates()` | 提取坐标矩阵 | 返回 (X, Y, L1, L2) 矩阵 |
| `st_intersection()` | 空间裁剪 | 相当于ArcGIS Clip工具 |
| `st_difference()` | 空间擦除 | 相当于ArcGIS Erase工具 |

---

### 2.2 terra —— 现代栅格引擎（必学 ★★★）

terra 由 Robert Hijmans 开发，C++底层，替换已废弃的 raster 包。内存管理优秀，支持超过内存大小的栅格计算。

#### 2.2.1 栅格读取

```r
library(terra)

# 读取栅格
dem <- rast("data/dem_30m.tif")                   # 单波段GeoTIFF
landsat <- rast("data/LC08_2023.tif")              # 多波段（自动堆叠）
climate <- rast("data/era5_2020.nc")               # NetCDF多维（时间序列）

# 查看元数据
crs(dem)        # 坐标系
ext(dem)        # 范围
res(dem)        # 分辨率
nlyr(climate)   # 图层数（NetCDF时间维度有365/12层）
names(climate)  # 图层名称

# 波段选择
dem_1 <- dem[[1]]                                 # 选择第1波段
precip <- climate[["tp"]]                         # 按名称选择
jun_aug <- climate[[6:8]]                         # 按月索引选择
```

#### 2.2.2 多时相 NetCDF 处理 —— 核心模式

```r
# 读取 ERA5/CMIP6 多时相NetCDF
# 文件结构: [longitude, latitude, time] — 典型183层(半年逐日)
climate_nc <- rast("data/era5_seasia_2020.nc")

# 多时相平均值（最常用）
# app() 按层应用函数，并行高效
temp_mean <- app(climate_nc, fun = mean, na.rm = TRUE)    # 所有时次平均
temp_max  <- app(climate_nc, fun = max, na.rm = TRUE)     # 所有时次最大值
temp_min  <- app(climate_nc, fun = min, na.rm = TRUE)     # 所有时次最小值
temp_sd   <- app(climate_nc, fun = sd, na.rm = TRUE)      # 时间变异系数

# 按时间段分组统计
# 如果 NetCDF 有月度数据 (36个月 = 3年)
# 创建索引向量标记每个层属于哪一年
year_idx <- rep(1:3, each = 12)  # 第1-12月=year1, 13-24=year2, 25-36=year3
annual_mean <- tapp(climate_nc, index = year_idx, fun = mean)

# 季节平均（按月分组）
month_idx <- rep(1:12, times = 3)  # 12个月循环
seasonal <- tapp(climate_nc, index = month_idx, fun = mean)
season_names <- c("Jan","Feb","Mar","Apr","May","Jun",
                  "Jul","Aug","Sep","Oct","Nov","Dec")
names(seasonal) <- season_names
```

#### 2.2.3 栅格对齐与重采样

```r
# 多源栅格对齐 —— 所有栅格必须同范围、同分辨率、同CRS才能叠置分析
# 核心三步：project() → crop() → resample()

# 步骤1：统一投影
dem_proj <- project(dem, "EPSG:32736", method = "bilinear")  # 连续数据用bilinear
lc_proj  <- project(landcover, "EPSG:32736", method = "near")  # 分类数据用near

# 步骤2：裁剪到研究区
ref_grid <- rast(extent = ext(478000, 498000, 9158000, 9178000),
                 resolution = c(30, 30), crs = "EPSG:32736")
dem_clip <- crop(dem_proj, ref_grid)
lc_clip  <- crop(lc_proj, ref_grid)

# 步骤3：重采样到参考栅格（关键步骤）
dem_aligned <- resample(dem_clip, ref_grid, method = "bilinear")
lc_aligned  <- resample(lc_clip, ref_grid, method = "near")

# 现在 dem_aligned 和 lc_aligned 可以叠置 stack
env_stack <- c(dem_aligned, lc_aligned)
```

#### 2.2.4 地形分析

```r
# Horne (1981) 8邻域算法 — 地学界标准
slope <- terrain(dem, v = "slope", unit = "degrees", neighbors = 8)
aspect <- terrain(dem, v = "aspect", unit = "degrees", neighbors = 8)
tpi <- terrain(dem, v = "TPI", neighbors = 8)       # 地形位置指数
tri <- terrain(dem, v = "TRI", neighbors = 8)       # 地形粗糙度指数
roughness <- terrain(dem, v = "roughness", neighbors = 8)

# 山体阴影
hillshade <- shade(slope, aspect, angle = 45, direction = 315)

# 流向与汇流
flowdir <- terrain(dem, v = "flowdir")              # 流向（D8算法）
```

#### 2.2.5 重分类

```r
# 使用3列矩阵：from, to, becomes
# 海拔分级：0-200=1, 200-500=2, 500-1000=3, 1000-2000=4, 2000+=5
m <- matrix(c(
  0,   200, 1,
  200, 500, 2,
  500, 1000, 3,
  1000, 2000, 4,
  2000, 9000, 5
), ncol = 3, byrow = TRUE)

dem_class <- classify(dem, rcl = m, include.lowest = TRUE)

# 两值分类（二值化：海拔>1500m的区域）
high_elevation <- classify(dem, cbind(-Inf, 1500, 0), others = 1)
```

#### 2.2.6 值提取与采样

```r
# 提取栅格值到点
faults_vect <- vect(faults_sf)                     # sf转SpatVector
env_values <- extract(env_stack, faults_vect)       # 提取所有栅格层的值
# 返回 data.frame: ID + 每层一列值

# 空间随机采样 — 背景点生成（用于物种分布/故障预测建模 ★★★）
# 关键：在环境变量栅格上随机采样，避开已知点
set.seed(42)  # 可重复性
n_background <- nrow(faults_vect) * 3              # 3倍正样本数量
bkg_points <- spatSample(env_stack, size = n_background,
                         method = "random", na.rm = TRUE, as.points = TRUE)

# 排除与正样本重叠的背景点
bkg_dist <- distance(bkg_points, faults_vect)
bkg_valid <- bkg_points[bkg_dist[, 1] > 500]       # 500米外

# 提取背景点环境值
bkg_values <- extract(env_stack, bkg_valid)

# 区域统计（平均值/总和）
# exactextractr 更快（备选方案）
zonal_mean <- extract(dem, admin_vect, fun = mean, na.rm = TRUE)
zonal_sum  <- extract(pop_rast, admin_vect, fun = sum, na.rm = TRUE)
```

#### 2.2.7 栅格运算

```r
# 逐像元数学运算（矢量化，高效）
ndvi <- (nir - red) / (nir + red)                  # NDVI计算

# 多图层叠置（所有图层已对齐的前提下）
stack <- c(dem_aligned, slope, aspect, landcover_aligned)

# 条件运算
flood_risk <- ifel(dem < 10 & landcover != 80, 1, 0)  # ifelse栅格版

# 移动窗口（卷积/滤波）
dem_focal_mean <- focal(dem, w = 3, fun = mean, na.rm = TRUE)
dem_focal_sd   <- focal(dem, w = 5, fun = sd, na.rm = TRUE)

# NA值填充 — focal填补法
filled <- focal(incomplete_raster, w = 3, fun = mean,
                na.policy = "only", na.rm = TRUE)
# na.policy="only": 只填充NA值，已有值的像元不变
```

#### 2.2.8 terra 速查表

| 函数 | 用途 | 注意 |
|------|------|------|
| `rast()` | 读取栅格 | 支持GeoTIFF/NetCDF/HDF/IMG等 |
| `crs()` / `crs()<-` | 查询/设置CRS | 设置时不变换，用project()变换 |
| `ext()` / `res()` / `nlyr()` | 元数据查询 | ext返回SpatExtent对象 |
| `project()` | 投影转换 | method: bilinear(连续)/near(分类) |
| `crop()` / `mask()` | 裁剪/掩膜提取 | crop裁剪范围，mask内外赋值NA |
| `resample()` | 重采样对齐 | 关键：多源数据对齐统一 |
| `app()` | 按层应用函数 | 多时相均值的核心函数 |
| `tapp()` | 按索引分组应用 | 年度/季节汇总 |
| `terrain()` | 地形因子 | slope/aspect/TPI/TRI/roughness/flowdir |
| `shade()` | 山体阴影 | 需要 slope + aspect 输入 |
| `classify()` | 重分类 | rcl=3列矩阵(from,to,becomes) |
| `ifel()` | 像元条件判断 | ifelse 栅格版 |
| `extract()` | 提取值到点/面 | 面用 fun=mean/sum |
| `spatSample()` | 空间随机采样 | method: random/regular/stratified |
| `focal()` | 移动窗口计算 | na.policy="only"仅填充NA |
| `distance()` | 栅格距离 | 像元中心到最近非NA的距离 |
| `freq()` | 频数统计 | 分类栅格各类别像元数 |
| `global()` | 全局统计量 | 全部像元统计mean/sd/min/max |

---

### 2.3 tmap —— 出版级专题制图（★★★）

tmap (thematic map) 是 R 中最强大的专题地图绘制包，语法类似 ggplot2 的图层叠加方式。支持静态图("plot")和交互图("view")双模式。

#### 2.3.1 基础语法

```r
library(tmap)

# 模式切换
tmap_mode("plot")   # 静态地图（PDF/PNG输出，出版用）
tmap_mode("view")   # 交互地图（Leaflet引擎，探索用）

# 基本图层语法：tm_shape(数据) + tm_*(图层)
tm_shape(dem) +
  tm_raster(title = "Elevation (m)", palette = terrain.colors(10)) +
  tm_shape(admin_boundary) +
  tm_borders(col = "grey40", lwd = 1.5) +
  tm_shape(faults) +
  tm_symbols(col = "red", size = 0.3, shape = 21)

# 多面板地图（Faceted maps）
tm_shape(annual_precip) +
  tm_raster(title = "Precipitation") +
  tm_facets(ncol = 3)  # 每年一个面板
```

#### 2.3.2 专题图层类型

| 图层函数 | 数据/几何类型 | 典型用途 |
|----------|--------------|----------|
| `tm_raster()` | SpatRaster | DEM、温度、降水等连续栅格 |
| `tm_polygons()` | sf POLYGON | 行政区、土地利用、分区面 |
| `tm_borders()` | sf (边界) | 叠加行政边界 |
| `tm_lines()` | sf LINESTRING | 道路、河流、断层线 |
| `tm_symbols()` | sf POINT | 采样点、设施点、站点 |
| `tm_dots()` | sf POINT | 密度点图（大数据量点） |
| `tm_text()` | sf + text字段 | 地名标注 |
| `tm_basemap()` | 瓦片底图 | OSM/卫星图底图 |
| `tm_grid()` | 格网线 | 经纬网 |
| `tm_scalebar()` | 比例尺 | 地图比例尺 |
| `tm_compass()` | 指北针 | 指北针（type: 4star/arrow/rose） |
| `tm_credits()` | 数据来源 | 地图底部数据来源文字 |
| `tm_minimap()` | 小地图 | 位置索引小地图 |

#### 2.3.3 完整出版级布局

```r
# 出版物级别的多图层地图
map_final <- tm_shape(dem, bbox = study_area_bbox) +
  # 栅格层：海拔
  tm_raster(title = "Elevation (m)",
            palette = "-RdYlGn",            # RColorBrewer调色板，"-"反转
            style = "quantile", n = 9,       # 分位数分类
            alpha = 0.85) +
  # 面层：行政区边界
  tm_shape(districts) +
  tm_borders(col = "grey30", lwd = 1) +
  # 线层：断层
  tm_shape(fault_lines) +
  tm_lines(col = "red", lwd = 1.5, lty = "dashed") +
  # 点层：故障点
  tm_shape(fault_points) +
  tm_symbols(col = "type", size = 0.15, shape = 21,
             title.col = "Fault Type",
             palette = "Set1") +
  # 标签
  tm_shape(cities) +
  tm_text("name", size = 0.8, col = "black",
          fontface = "bold", shadow = TRUE) +
  # 布局组件
  tm_layout(
    title = "TTCL Network Fault Distribution and Terrain Analysis",
    title.position = c("left", "top"),
    title.size = 1.2,
    legend.position = c("right", "bottom"),
    legend.title.size = 0.9,
    legend.text.size = 0.7,
    legend.outside = FALSE,
    frame = TRUE,
    inner.margins = c(0.02, 0.02, 0.02, 0.02)
  ) +
  tm_scalebar(position = c("left", "bottom"), text.size = 0.6) +
  tm_compass(position = c("right", "top"), type = "arrow", size = 1.2) +
  tm_credits("Data: USGS SRTM | Analysis: R v4.3 + terra + tmap",
             position = c("left", "bottom"), size = 0.6) +
  tm_grid(labels.inside.frame = FALSE, lines = TRUE, alpha = 0.2)

# 渲染
print(map_final)

# 高分辨率导出
tmap_save(map_final, filename = "output/fault_map.png",
          width = 10, height = 8, dpi = 300, units = "in")
tmap_save(map_final, filename = "output/fault_map.pdf",
          width = 10, height = 8, units = "in")
```

#### 2.3.4 配色方案

```r
# RColorBrewer 调色板（CRAN标准）
# Sequential: Blues BuGn BuPu GnBu Greens Greys Oranges OrRd PuBu
#             PuBuGn PuRd Purples RdPu Reds YlGn YlGnBu YlOrBr YlOrRd
# Diverging: BrBG PiYG PRGn PuOr RdBu RdGy RdYlBu RdYlGn Spectral
# Qualitative: Accent Dark2 Paired Pastel1 Pastel2 Set1 Set2 Set3

# 使用示例
tm_shape(pop) + tm_polygons(col = "density", palette = "YlOrRd", style = "jenks")
tm_shape(landcover) + tm_raster(palette = "Set2")  # 分类数据用Qualitative
tm_shape(temp_anomaly) + tm_raster(palette = "-RdBu")  # 发散：暖冷色

# viridis配色（色盲友好，推荐）
tm_shape(dem) + tm_raster(palette = viridis::viridis(10))
tm_shape(dem) + tm_raster(palette = viridis::magma(10, direction = -1))
```

---

### 2.4 leaflet + htmlwidgets —— 交互式Web地图（★★☆）

#### 2.4.1 基础交互地图

```r
library(leaflet)
library(leafem)     # 扩展：栅格图例
library(leaflet.extras)  # 扩展：热力图/搜索等

# 基础地图
m <- leaflet() |>
  addProviderTiles(providers$CartoDB.Positron) |>  # 浅色底图
  setView(lng = 39.28, lat = -6.82, zoom = 11) |>
  addPolygons(data = districts,
              fillColor = ~colorQuantile("YlOrRd", pop_density)(pop_density),
              fillOpacity = 0.7, weight = 1, color = "#444",
              highlightOptions = highlightOptions(weight = 3, color = "#666",
                                                  bringToFront = TRUE),
              label = ~paste0(name, ": ", round(pop_density), " ppl/km²"),
              group = "Population") |>
  addPolygons(data = flood_zones,
              fillColor = "blue", fillOpacity = 0.3, color = "navy", weight = 1,
              group = "Flood Risk") |>
  addLegend(pal = colorQuantile("YlOrRd", districts$pop_density),
            values = districts$pop_density, position = "bottomright",
            title = "Population Density (quantile)")

print(m)
```

#### 2.4.2 栅格叠加到 Leaflet

```r
# terra栅格 到 leaflet
# 注意：大栅格需先aggregate降低分辨率
dem_lowres <- aggregate(dem, fact = 3, fun = mean)  # 3倍聚合

# 自定义调色板
pal_dem <- colorNumeric(
  palette = viridis::viridis(100),
  domain = values(dem_lowres, na.rm = TRUE),
  na.color = "transparent"
)

m <- leaflet() |>
  addProviderTiles(providers$OpenStreetMap.Mapnik) |>
  addRasterImage(dem_lowres, colors = pal_dem, opacity = 0.7,
                 group = "Elevation") |>
  addLegend(pal = pal_dem, values = values(dem_lowres, na.rm = TRUE),
            title = "Elevation (m)", position = "topright", group = "Elevation")
```

#### 2.4.3 多图层控制 + 多图例模式

```r
# 完整交互地图：3个分析层 + 图层控制 + 分别图例
m <- leaflet() |>
  # 底图
  addProviderTiles(providers$CartoDB.Positron) |>
  
  # 图层1：洪水风险栅格
  addRasterImage(flood_risk, colors = pal_flood, opacity = 0.6,
                 group = "Flood Risk", project = TRUE) |>
  addLegend(pal = pal_flood, values = values(flood_risk, na.rm = TRUE),
            title = "Flood Risk Index", position = "bottomright",
            group = "Flood Risk") |>
  
  # 图层2：热风险栅格
  addRasterImage(heat_risk, colors = pal_heat, opacity = 0.6,
                 group = "Heat Risk", project = TRUE) |>
  addLegend(pal = pal_heat, values = values(heat_risk, na.rm = TRUE),
            title = "Heat Risk Index", position = "bottomleft",
            group = "Heat Risk") |>
  
  # 图层3：综合脆弱性
  addRasterImage(vulnerability, colors = pal_vuln, opacity = 0.7,
                 group = "Vulnerability", project = TRUE) |>
  addLegend(pal = pal_vuln, values = values(vulnerability, na.rm = TRUE),
            title = "Composite Vulnerability", position = "topright",
            group = "Vulnerability") |>
  
  # 面板图层（始终显示）
  addPolygons(data = admin_borders, fill = FALSE, color = "grey50",
              weight = 1.5, group = "Admin Boundaries") |>
  
  # 图层控制器
  addLayersControl(
    baseGroups = c("CartoDB.Positron", "OpenStreetMap"),
    overlayGroups = c("Flood Risk", "Heat Risk", "Vulnerability",
                      "Admin Boundaries"),
    options = layersControlOptions(collapsed = FALSE)
  ) |>
  hideGroup(c("Heat Risk", "Vulnerability"))  # 默认折叠

print(m)

# 保存为独立HTML（自包含，可离线使用）
htmlwidgets::saveWidget(m, file = "dar_vulnerability_map.html",
                        selfcontained = TRUE)
```

#### 2.4.4 地图小部件扩展

```r
# leafem — 增强栅格图例
library(leafem)
leaflet() |> addRasterImage(dem) |> addImageQuery(dem)

# leaflet.extras — 热力图/搜索/全屏
library(leaflet.extras)
leaflet(points) |>
  addProviderTiles(providers$CartoDB.Positron) |>
  addHeatmap(lng = ~lon, lat = ~lat, intensity = ~value,
             radius = 15, blur = 10, max = 1.0) |>
  addSearchOSM() |>
  addFullscreenControl()

# leafgl — WebGL加速点渲染（大数据量）
library(leafgl)
leaflet() |>
  addProviderTiles(providers$CartoDB.DarkMatter) |>
  addGlPoints(data = large_points_sf, group = "Points")
```

---

### 2.5 其他关键包

#### 2.5.1 tidygeocoder —— OSM Nominatim 批量地理编码

```r
library(tidygeocoder)

# 单条地址
result <- geo("Dar es Salaam City Center, Tanzania",
              method = "osm", limit = 1)

# 批量地理编码（逐条调用，注意速率限制）
addresses <- data.frame(
  addr = c("Ubungo, Dar es Salaam", "Kigamboni, Dar es Salaam",
           "Ilala, Dar es Salaam", "Kinondoni, Dar es Salaam")
)
geocoded <- addresses |>
  geocode(address = addr, method = "osm", limit = 1)

# 使用 Google Geocoding（需API Key）
geocoded_google <- addresses |>
  geocode(address = addr, method = "google",
          api_key = Sys.getenv("GOOGLE_GEOCODE_KEY"))
```

#### 2.5.2 mapview —— 快速交互预览

```r
library(mapview)

# 一键交互预览（调试神器！）
mapview(dem)                              # 栅格
mapview(districts, zcol = "population")   # 矢量面（按字段着色）
mapview(faults, zcol = "type") +           # 矢量点
  mapview(dem, alpha.regions = 0.5)        # 图层叠加

# 结合 terra/sf 对象的快速渲染
mapview(dem, col.regions = terrain.colors(256), legend = TRUE)
```

#### 2.5.3 whitebox —— 地形/水文分析（WhiteboxTools R接口）

```r
library(whitebox)

# 初始化（首次需下载 ~15MB 二进制文件）
install_whitebox()

# DEM预处理 — Breach Depressions（比填洼更科学）
wbt_breach_depressions(dem = "data/dem.tif",
                       output = "output/dem_breached.tif")

# 流向
wbt_d8_pointer(dem = "output/dem_breached.tif",
               output = "output/flow_direction.tif")

# 累积流量
wbt_d8_flow_accumulation(input = "output/flow_direction.tif",
                         output = "output/flow_accum.tif")

# 流域提取
wbt_watershed(d8_pntr = "output/flow_direction.tif",
              pour_pts = "data/outlets.shp",
              output = "output/watersheds.tif")

# 地形湿度指数 (TWI)
wbt_wetness_index(dem = "output/dem_breached.tif",
                  output = "output/twi.tif",
                  sca = "output/specific_catchment_area.tif")
```

#### 2.5.4 stars —— 时空数组（多维数据）

```r
library(stars)

# 读取NetCDF为4D数组 [x, y, band, time]
climate_stars <- read_stars("data/era5_monthly.nc")

# 沿时间维度聚合
annual_stars <- aggregate(climate_stars, by = "1 year", FUN = mean)

# 时空裁剪
croped <- climate_stars[study_area_bbox]
# stars与stars.proxy模式（延迟加载大文件）
climate_proxy <- read_stars("data/era5_monthly.nc", proxy = TRUE)
```

#### 2.5.5 空间统计包群

```r
# spdep — 空间自相关（Moran's I, LISA）
library(spdep)
nb <- poly2nb(admin_sf, queen = TRUE)              # 邻接关系
lw <- nb2listw(nb, style = "W")                     # 权重矩阵
moran.test(admin_sf$crime_rate, lw)                  # 全局 Moran's I
local_moran <- localmoran(admin_sf$crime_rate, lw)   # LISA 局部自相关

# gstat — 地统计（Kriging插值）
library(gstat)
variogram_model <- variogram(temperature ~ 1, data = weather_points,
                             cutoff = 50000, width = 5000)
fit_vgm <- fit.variogram(variogram_model, model = vgm("Sph"))
kriged <- krige(temperature ~ 1, weather_points, grid_points, fit_vgm)

# spatstat — 点模式分析
library(spatstat)
ppp_obj <- as.ppp(faults_points)                    # 转点模式对象
k_est <- Kest(ppp_obj, correction = "Ripley")       # Ripley's K函数
plot(k_est)                                          # 诊断聚集/分散
density_map <- density.ppp(ppp_obj, sigma = 1000)    # 核密度估计
```

#### 2.5.6 dismo / biomod2 —— 物种分布模型 (SDM)

```r
library(dismo)

# MaxEnt 工作流
presence <- read.csv("data/species_presence.csv")
env <- stack(list.files("data/climate/", pattern = ".tif$", full.names = TRUE))
maxent_model <- maxent(env, presence[, c("lon", "lat")])
prediction <- predict(maxent_model, env)
plot(prediction)

# biomod2 — 集成SDM框架
library(biomod2)
bm_data <- BIOMOD_FormatingData(resp.var = presence_vector,
                                expl.var = env_stack,
                                resp.name = "SpeciesX")
bm_options <- BIOMOD_ModelingOptions()
bm_out <- BIOMOD_Modeling(bm_data, models = c("GLM", "RF", "MAXENT"),
                          models.options = bm_options, NbRunEval = 5)
bm_em <- BIOMOD_EnsembleModeling(bm_out, models.chosen = "all",
                                 em.by = "all", eval.metric = "TSS")
```

#### 2.5.7 qgisprocess —— 从R调用QGIS处理工具

```r
library(qgisprocess)

# 列出所有可用QGIS工具
qgis_algorithms() |>
  subset(grepl("buffer|clip", algorithm, ignore.case = TRUE))

# 调用QGIS缓冲区工具
result <- qgis_run_algorithm(
  "native:buffer",
  INPUT = roads_sf,
  DISTANCE = 200,
  DISSOLVE = TRUE,
  OUTPUT = "output/buffer_200m.gpkg"
)
buffer_sf <- sf::read_sf(result$OUTPUT)

# 需要先安装QGIS并配置路径
# qgis_configure()  # 首次自动探测QGIS安装位置
```

#### 2.5.8 r5r —— 多模式交通可达性

```r
library(r5r)

# 构建交通网络
r5r_core <- setup_r5(data_path = "data/transport_network/")

# 计算等时圈（步行+公交）
isochrones <- isochrone(
  r5r_core,
  origins = facilities_points,
  mode = c("WALK", "TRANSIT"),
  departure_datetime = as.POSIXct("2024-01-15 08:00:00"),
  cutoffs = c(15, 30, 45, 60),  # 分钟
  sample_size = 0.8
)

# 计算OD出行时间矩阵
ttm <- travel_time_matrix(
  r5r_core,
  origins = origins_points,
  destinations = destinations_points,
  mode = c("WALK", "TRANSIT"),
  departure_datetime = as.POSIXct("2024-01-15 08:00:00")
)
```

---

## 三、完整工作流模式（含完整代码 ★★☆~★★★）

### 3.1 模式A：多源数据集成 + 预测建模 ★★★

基于电信网络故障预测(TTCL Network Fault Prediction)的完整工作流。

```r
# ============================================================
# 故障预测建模完整工作流
# 场景：预测电网/通信网故障的空间分布概率
# 难度：★★★
# ============================================================
library(sf)
library(terra)
library(tmap)
library(leaflet)
library(pROC)

# --- 步骤1：多源数据加载 ---
# 矢量：历史故障点
faults <- st_read("data/ttcl_faults.gpkg", layer = "faults_2023")  # n=287故障
# 栅格：SRTM 30m DEM
dem <- rast("data/n11_e039_3arc_v2.tif")
# 栅格：ERA5气候多时相 NetCDF（12个月×8变量）
climate_nc <- rast("data/era5_tanzania_2023.nc")
# 栅格：WorldPop人口密度 100m
population <- rast("data/tza_ppp_2020.tif")
# 矢量：保护区边界（掩膜用）
admin <- st_read("data/tanzania_admin.gpkg", layer = "regions")

# --- 步骤2：坐标系统一 ---
target_crs <- 32736  # WGS 84 / UTM zone 36S (Tanzania)

dem_proj <- project(dem, paste0("EPSG:", target_crs), method = "bilinear")
pop_proj <- project(population, paste0("EPSG:", target_crs), method = "bilinear")
# NetCDF：逐层投影到UTM
climate_proj <- project(climate_nc, paste0("EPSG:", target_crs), method = "bilinear")
faults_proj <- st_transform(faults, target_crs)
admin_proj <- st_transform(admin, target_crs)

# --- 步骤3：多时相气候降维 ---
# 从月度NetCDF提取年度均值（8个变量各自年度平均）
precip_mean <- app(climate_proj[[grep("tp", names(climate_proj))]],
                   fun = mean, na.rm = TRUE)
temp_mean <- app(climate_proj[[grep("t2m", names(climate_proj))]],
                 fun = mean, na.rm = TRUE)
wind_mean <- app(climate_proj[[grep("u10|v10", names(climate_proj))]],
                 fun = function(x) sqrt(mean(x[, 1], na.rm = TRUE)^2 +
                                        mean(x[, 2], na.rm = TRUE)^2))

# --- 步骤4：创建参考栅格并对齐 ---
ref_grid <- rast(extent = ext(dem_proj), resolution = c(100, 100),
                 crs = paste0("EPSG:", target_crs))

dem_100m <- resample(dem_proj, ref_grid, method = "bilinear")
pop_100m <- resample(pop_proj, ref_grid, method = "bilinear")
precip_100m <- resample(precip_mean, ref_grid, method = "bilinear")
temp_100m <- resample(temp_mean, ref_grid, method = "bilinear")
wind_100m <- resample(wind_mean, ref_grid, method = "bilinear")

# 衍生地形变量
slope_100m <- terrain(dem_100m, v = "slope", unit = "degrees", neighbors = 8)
aspect_100m <- terrain(dem_100m, v = "aspect", unit = "degrees", neighbors = 8)
tpi_100m <- terrain(dem_100m, v = "TPI", neighbors = 8)

# 距离变量（到最近道路/城市的距离）
roads_proj <- st_transform(roads, target_crs)
dist_roads <- distance(dem_100m, vect(roads_proj))
names(dist_roads) <- "dist_roads"

# --- 步骤5：环境变量叠置 ---
env_stack <- c(dem_100m, slope_100m, aspect_100m, tpi_100m,
               precip_100m, temp_100m, wind_100m,
               pop_100m, dist_roads)
names(env_stack) <- c("elevation", "slope", "aspect", "tpi",
                      "precip", "temp", "wind", "pop_density", "dist_roads")

# --- 步骤6：背景点采样 ---
# spatSample 在环境栅格上随机采样背景点（避开故障点）
set.seed(2024)
n_presence <- nrow(faults_proj)
bkg_pts <- spatSample(env_stack, size = n_presence * 3,
                      method = "random", na.rm = TRUE, as.points = TRUE)

# 排除与故障点过近的背景点（>500m）
bkg_dist <- distance(bkg_pts, vect(faults_proj))
bkg_valid <- bkg_pts[bkg_dist[, 1] > 500]

# --- 步骤7：提取环境值并构建训练数据集 ---
# 故障点环境值
fault_env <- extract(env_stack, vect(faults_proj))
fault_env$presence <- 1  # 标记为正样本

# 背景点环境值
bkg_env <- extract(env_stack, bkg_valid)
bkg_env$presence <- 0    # 标记为背景

# 合并并去除ID列
training <- rbind(fault_env, bkg_env)
training <- training[, -1]  # 移除extract产生的ID列
training <- na.omit(training)
training$presence <- as.factor(training$presence)

# --- 步骤8：广义线性模型 (GLM) ---
model <- glm(presence ~ ., data = training, family = binomial(link = "logit"))
summary(model)

# --- 步骤9：模型验证 (ROC/AUC) ---
pred_prob <- predict(model, training, type = "response")
roc_obj <- roc(training$presence, pred_prob)
auc_value <- auc(roc_obj)
cat(sprintf("AUC = %.4f\n", auc_value))  # 期望 > 0.75

# 绘图
plot(roc_obj, main = sprintf("ROC Curve — AUC = %.3f", auc_value))
abline(a = 0, b = 1, lty = 2, col = "grey50")

# --- 步骤10：全空间预测 ---
# 栅格预测
pred_surface <- predict(env_stack, model, type = "response")
# predict() 返回 SpatRaster — 每个像元一个故障概率值

# --- 步骤11：热点提取（Top 5%高风险区）---
hotspot_threshold <- quantile(values(pred_surface, na.rm = TRUE), 0.95, na.rm = TRUE)
hotspots <- pred_surface > hotspot_threshold
hotspots_poly <- as.polygons(hotspots, dissolve = TRUE)
hotspots_sf <- st_as_sf(hotspots_poly)
hotspots_sf <- hotspots_sf[hotspots_sf$lyr.1 == 1, ]  # 仅保留高风险区

# --- 步骤12：多模式可视化 ---
# 静态出版图
tmap_mode("plot")
risk_map <- tm_shape(pred_surface) +
  tm_raster(title = "Fault Probability",
            palette = "YlOrRd", style = "quantile", n = 7) +
  tm_shape(faults_proj) +
  tm_symbols(col = "black", size = 0.05, alpha = 0.5) +
  tm_shape(hotspots_sf) +
  tm_borders(col = "red", lwd = 2) +
  tm_shape(admin_proj) +
  tm_borders(col = "grey40") +
  tm_layout(title = "Network Fault Prediction — GLM Model",
            legend.position = c("right", "bottom"),
            frame = TRUE) +
  tm_scalebar() + tm_compass(position = c("left", "top"))
tmap_save(risk_map, "output/fault_prediction_map.png", dpi = 300)

# 交互Web地图
risk_pal <- colorNumeric("YlOrRd", values(pred_surface, na.rm = TRUE), na.color = "transparent")
leaflet() |>
  addProviderTiles(providers$CartoDB.Positron) |>
  addRasterImage(pred_surface, colors = risk_pal, opacity = 0.7, group = "Risk") |>
  addPolygons(data = hotspots_sf, color = "red", fill = FALSE, weight = 3,
              group = "Hotspots (Top 5%)") |>
  addCircleMarkers(data = faults_proj, radius = 2, color = "black",
                   fillOpacity = 0.6, group = "Faults") |>
  addLegend(pal = risk_pal, values = values(pred_surface, na.rm = TRUE),
            title = "Fault Probability") |>
  addLayersControl(overlayGroups = c("Risk", "Hotspots (Top 5%)", "Faults"))
```

### 3.2 模式B：气候脆弱性综合评估 ★★☆

基于达累斯萨拉姆城市气候脆弱性(Dar es Salaam Urban Climate Vulnerability)项目的完整工作流。

```r
# ============================================================
# 城市气候脆弱性评估
# 场景：多灾种加权叠加 → 人口暴露度 → 综合脆弱性分级
# 难度：★★☆
# ============================================================
library(sf)
library(terra)
library(leaflet)
library(leafem)

# --- 步骤1：多源数据加载 ---
# 矢量：达累斯萨拉姆5个市辖区
dar_districts <- st_read("data/dar_boundaries.gpkg", layer = "districts")
# DEM：SRTM 30m
dem <- rast("data/dar_dem.tif")
# 人口：WorldPop 100m
worldpop <- rast("data/tza_ppp_2020_UNadj.tif")
# 气候NetCDF
precip_nc <- rast("data/chirps_dar_2020.nc")   # 逐日降水
temp_nc <- rast("data/era5_dar_2020.nc")        # 逐小时温度
# 土地利用
landcover <- rast("data/esa_lc_dar_2019.tif")
# 土壤
soil <- rast("data/isric_soil_dar.tif")         # 0-30cm黏土含量

# --- 步骤2：投影到UTM ---
crs_utm <- 32737  # WGS 84 / UTM zone 37S (Dar es Salaam)
dem <- project(dem, paste0("EPSG:", crs_utm), method = "bilinear")
worldpop <- project(worldpop, paste0("EPSG:", crs_utm), method = "bilinear")
landcover <- project(landcover, paste0("EPSG:", crs_utm), method = "near")

# --- 步骤3：年度气候因子计算 ---
annual_precip <- app(precip_nc, fun = sum, na.rm = TRUE)  # 年总降水
annual_precip <- project(annual_precip, paste0("EPSG:", crs_utm), method = "bilinear")

# 高温日数（>35°C天数统计）
extreme_heat <- app(temp_nc, fun = function(x) sum(x > 307.15, na.rm = TRUE))  # 307.15K=34°C
extreme_heat <- project(extreme_heat, paste0("EPSG:", crs_utm), method = "near")

# --- 步骤4：栅格对齐 ---
ref <- rast(extent = ext(dem), resolution = c(100, 100), crs = paste0("EPSG:", crs_utm))
dem <- resample(dem, ref, method = "bilinear")
worldpop <- resample(worldpop, ref, method = "bilinear")
annual_precip <- resample(annual_precip, ref, method = "bilinear")
extreme_heat <- resample(extreme_heat, ref, method = "bilinear")
landcover <- resample(landcover, ref, method = "near")
soil <- resample(soil, ref, method = "bilinear")

# --- 步骤5：归一化函数 ---
normalize <- function(x) {
  xmin <- global(x, min, na.rm = TRUE)[1, 1]
  xmax <- global(x, max, na.rm = TRUE)[1, 1]
  (x - xmin) / (xmax - xmin)
}

# --- 步骤6：洪水风险子模型 ---
# 坡度反转：平坦 = 高洪水风险
slope <- terrain(dem, v = "slope", unit = "degrees")
slope_inv <- 1 - normalize(slope)           # 坡度越小，风险越高

# 降水因子
precip_norm <- normalize(annual_precip)

# 土壤因子：黏土含量高 → 排水差 → 洪水风险高
soil_norm <- normalize(soil)

# 洪水风险 = 加权叠加
flood_risk <- 0.50 * precip_norm + 0.35 * slope_inv + 0.15 * soil_norm

# --- 步骤7：热风险子模型 ---
# 高温日数
heat_days_norm <- normalize(extreme_heat)

# 城市热岛（简化：建成区=1, 水域=0, 植被=中）
# ESA CCI Land Cover: 190=Urban, 80=Water, 10-120=Vegetation
builtup <- classify(landcover, cbind(190, 1), others = 0)
greenness <- classify(landcover, cbind(c(10, 20, 30, 40, 50, 60, 70, 80,
                                         90, 100, 110, 120, 130), 1), others = 0)
veg_norm <- 1 - normalize(greenness)  # 植被少=热岛效应强

heat_risk <- 0.55 * heat_days_norm + 0.30 * builtup + 0.15 * veg_norm

# --- 步骤8：多灾种综合 ---
multi_hazard <- 0.55 * flood_risk + 0.45 * heat_risk

# --- 步骤9：人口暴露度 ---
pop_norm <- normalize(worldpop)

# 综合脆弱性 = 多灾种 × 人口暴露
vulnerability <- multi_hazard * pop_norm

# --- 步骤10：NA值处理 ---
vulnerability <- focal(vulnerability, w = 3, fun = mean,
                       na.policy = "only", na.rm = TRUE)

# --- 步骤11：脆弱性分级 ---
vuln_class <- classify(vulnerability,
  rcl = matrix(c(
    0,    0.10, 1,   # 低脆弱性
    0.10, 0.25, 2,   # 中低
    0.25, 0.50, 3,   # 中
    0.50, 0.75, 4,   # 中高
    0.75, 1.00, 5    # 高脆弱性
  ), ncol = 3, byrow = TRUE))

class_labels <- c("Low", "Mod-Low", "Moderate", "Mod-High", "High")
vuln_class <- as.factor(vuln_class)
levels(vuln_class) <- data.frame(ID = 1:5, class = class_labels)

# --- 步骤12：分区统计 ---
district_vuln <- extract(vulnerability, vect(dar_districts), fun = mean, na.rm = TRUE)
dar_districts$vuln_mean <- district_vuln[, 2]

# --- 步骤13：Leaflet 3层交互地图 ---
vuln_pal <- colorNumeric("RdYlBu", values(vulnerability, na.rm = TRUE),
                         na.color = "transparent", reverse = TRUE)
flood_pal <- colorNumeric("Blues", values(flood_risk, na.rm = TRUE))
heat_pal <- colorNumeric("Reds", values(heat_risk, na.rm = TRUE))

m <- leaflet() |>
  addProviderTiles(providers$CartoDB.Positron, group = "CartoDB Light") |>
  addProviderTiles(providers$OpenStreetMap.Mapnik, group = "OSM") |>

  addRasterImage(vulnerability, colors = vuln_pal, opacity = 0.7,
                 group = "Vulnerability", project = TRUE) |>
  addRasterImage(flood_risk, colors = flood_pal, opacity = 0.6,
                 group = "Flood Risk", project = TRUE) |>
  addRasterImage(heat_risk, colors = heat_pal, opacity = 0.6,
                 group = "Heat Risk", project = TRUE) |>

  addPolygons(data = dar_districts, fill = FALSE, color = "black",
              weight = 2, group = "Districts",
              label = ~paste(name, ":", round(vuln_mean, 3))) |>

  addLegend(pal = vuln_pal, values = values(vulnerability, na.rm = TRUE),
            title = "Composite Vulnerability", position = "topright",
            group = "Vulnerability") |>
  addLegend(pal = flood_pal, values = values(flood_risk, na.rm = TRUE),
            title = "Flood Risk", position = "bottomright",
            group = "Flood Risk") |>
  addLegend(pal = heat_pal, values = values(heat_risk, na.rm = TRUE),
            title = "Heat Risk", position = "bottomleft",
            group = "Heat Risk") |>

  addLayersControl(
    baseGroups = c("CartoDB Light", "OSM"),
    overlayGroups = c("Vulnerability", "Flood Risk", "Heat Risk", "Districts"),
    options = layersControlOptions(collapsed = FALSE)
  ) |>
  hideGroup(c("Flood Risk", "Heat Risk"))

print(m)

htmlwidgets::saveWidget(m, "output/dar_vulnerability_interactive.html",
                        selfcontained = TRUE)
```

---

## 四、反模式与陷阱

### 4.1 坐标系统类

| 反模式 | 问题 | 正确做法 |
|--------|------|----------|
| `st_buffer(roads, 100)` 在EPSG:4326上 | 100度≈11100km，缓冲区远超预期 | 先 `st_transform(roads, UTM_zone)` |
| `st_distance()` 在EPSG:4326上 | 返回度数距离，非米 | `st_distance(st_transform(x, proj_crs))` |
| sf对象手动修改coord列（`st_coordinates()[,]`） | X/Y列顺序混淆 | 用 `st_as_sf(coords=c("lon","lat"))` + `st_crs()` |
| 不同CRS对象做空间连接 | 结果不可预测或报错 | `assertthat::assert_that(identical(st_crs(a), st_crs(b)))` |
| `terra::project()` 分类数据用bilinear | 分类值被插值为非整数 | 分类数据始终用 `method="near"` |

### 4.2 包选择类

| 反模式 | 问题 | 正确做法 |
|--------|------|----------|
| 使用 `raster` 包 (已废弃) | 2023年后不再维护，性能差 | 永远用 `terra`，API类似 |
| 使用 `sp` 包 (已废弃) | sp::Spatial* 类已被sf取代 | 永远用 `sf`，`st_as_sf()`可转换旧数据 |
| 使用 `rgdal` (已于2023年10月退役) | CRAN已移除 | 永远用 `sf::st_read/st_write` |
| 使用 `maptools` | CRAN已移除 | 用 `sf` + `tmap` |
| 在 `ggplot2` 中用 `geom_polygon()` 处理空间数据 | 繁琐且易出错 | 用 `geom_sf()` |

### 4.3 数据与性能类

| 反模式 | 问题 | 正确做法 |
|--------|------|----------|
| NetCDF逐层for循环求均值 | 极其缓慢（1826层=5分钟） | `app(x, mean)` 一次完成（5秒） |
| `readAll()` 大栅格（terra） | 强制加载到内存，可能溢出 | terra默认延迟加载，按需使用 |
| 用Shapefile存大数据（>2GB） | 字段名截断、性能差、无索引 | 使用 GeoPackage (.gpkg) |
| 多源栅格未 resample() 就叠加 | 范围/分辨率不一致导致报错 | 先 crop → resample 到ref grid |
| `extract()` 大量点未用exactextractr | sf::extract较慢（千万级点） | 使用 `exactextractr::exact_extract()` |
| 叶子地图大栅格(>10000px边) | Leaflet性能崩溃 | 用 `aggregate(fact=3)` 降低分辨率 |

### 4.4 统计建模类

| 反模式 | 问题 | 正确做法 |
|--------|------|----------|
| 空间数据用普通GLM忽略自相关 | 伪显著、I型错误膨胀 | 检查Moran's I残差，必要时用SAR/SEM |
| 背景点采样不排除正样本区域 | 污染负样本 | `spatSample()` 后 `distance()` 过滤 |
| ROC评估不拆分训练/测试集 | 过度乐观的AUC | 分层抽样 `initial_split(strata=presence)` |
| 强制连续数据用 `style="equal"` 分类 | 极值主导，大部分区域同色 | 使用 `style="quantile"` 或 `"fisher"` |

---

## 五、R + GIS 集成模式

### 5.1 R + QGIS 集成

```r
# 方法1：qgisprocess 包 — 直接在R中调用QGIS Processing工具
library(qgisprocess)
library(sf)

# 确保QGIS已安装并配置
qgis_configure()

# 列出QGIS处理工具中带"distance"的工具
qgis_search_algorithms("distance") |> head(10)

# 调用QGIS的PyQGIS处理工具
result <- qgis_run_algorithm(
  "native:fixgeometries",    # 几何修复
  INPUT = broken_geom_sf,
  OUTPUT = "output/fixed.gpkg"
)

# 方法2：R as QGIS Processing Provider (Processing R Provider插件)
# 在QGIS中安装 "Processing R Provider" 插件
# 在QGIS工具箱中直接调用R脚本 → 结果渲染为QGIS图层
# 适用于：QGIS为主用户，偶尔需要R统计功能的场景
```

### 5.2 R + PostGIS 集成

```r
library(RPostgres)
library(DBI)
library(sf)

# 建立PostGIS连接
conn <- dbConnect(
  Postgres(),
  host = "localhost",
  port = 5432,
  dbname = "gis_db",
  user = Sys.getenv("PG_USER"),
  password = Sys.getenv("PG_PASSWORD")
)

# 方法1：SQL查询 + 空间结果转sf
sf_obj <- st_read(conn,
  query = "SELECT gid, name, ST_Buffer(geom, 500) as geom
           FROM admin_boundaries
           WHERE ST_Intersects(geom, ST_SetSRID(ST_MakePoint(39.2, -6.8), 4326))")

# 方法2：sf对象写入PostGIS
st_write(sf_obj, conn, "analysis_results", overwrite = TRUE)

# 方法3：执行原生PostGIS函数
dbGetQuery(conn,
  "SELECT ST_Area(ST_Transform(geom, 32737)) / 1000000 AS area_km2
   FROM admin_boundaries WHERE gid = 1")

dbDisconnect(conn)
```

### 5.3 R + GDAL CLI

```r
# gdalUtils 包 — R 接口调用 GDAL 命令行工具
library(gdalUtils)

# 栅格投影变换（等价于 gdalwarp）
gdalwarp(srcfile = "data/elev_wgs84.tif",
         dstfile = "output/elev_utm36.tif",
         t_srs = "EPSG:32736",
         tr = c(30, 30),
         r = "bilinear",
         overwrite = TRUE,
         verbose = TRUE)

# 格式转换（等价于 gdal_translate）
gdal_translate(src_dataset = "data/big.tif",
               dst_dataset = "output/big_cog.tif",
               of = "COG",           # Cloud Optimized GeoTIFF
               co = "COMPRESS=DEFLATE",
               verbose = TRUE)

# 矢量坐标转换（等价于 ogr2ogr）
ogr2ogr(src_datasource_name = "data/roads_wgs84.shp",
        dst_datasource_name = "output/roads_utm.gpkg",
        t_srs = "EPSG:32736",
        f = "GPKG")
```

### 5.4 R + Python (reticulate) 互通

```r
library(reticulate)

# 配置使用系统Python/conda环境
use_condaenv("gis", required = TRUE)  # 使用conda gis环境

# 导入 Python GIS 库
geopandas <- import("geopandas")
rasterio <- import("rasterio")
xarray <- import("xarray")

# Python → R：GeoDataFrame 转 sf
py_gdf <- geopandas$read_file("data/roads.gpkg")
r_sf <- sf::st_as_sf(py_gdf)

# R → Python：sf 转 GeoDataFrame
py_data <- r_to_py(roads_sf)
py_gdf <- geopandas$GeoDataFrame(py_data)

# 使用 Python 函数（例如 GEE）
ee <- import("ee")
ee$Initialize()
# 直接调用 Python GEE API
landsat_col <- ee$ImageCollection("LANDSAT/LC08/C02/T1_L2")
```

---

## 六、出版与报表

### 6.1 RMarkdown —— 可重复研究报告

```r
# 典型的GIS分析 RMarkdown 文档结构（.Rmd 文件）

# --- YAML 头 ---
# ---
# title: "Urban Heat Island Analysis — Dar es Salaam 2020"
# author: "GIS Analysis Team"
# date: "`r Sys.Date()`"
# output:
#   html_document:
#     toc: true
#     toc_float: true
#     theme: flatly
#   pdf_document:
#     toc: true
#   word_document: default
# params:
#   city: "Dar es Salaam"
#   year: 2020
# ---

# 代码块中使用 knitr 参数：
# `{r load-data, message=FALSE, warning=FALSE, cache=TRUE}
# library(sf); library(terra); library(tmap); library(ggplot2)
# `

# 内联输出：模型 AUC = `r round(auc_value, 3)`
# 地图直接嵌入：tm_shape(dem) + tm_raster() 自动渲染
```

### 6.2 ggplot2 + ggspatial —— 科学出版图

```r
library(ggplot2)
library(ggspatial)
library(sf)

# ggplot2 原生sf图层
ggplot() +
  # 栅格用 geom_raster (需先转data.frame)
  # geom_raster(data = as.data.frame(dem, xy = TRUE), aes(x, y, fill = z)) +
  # 矢量图层
  geom_sf(data = admin_sf, fill = "grey95", color = "grey40", size = 0.3) +
  geom_sf(data = faults_sf, aes(color = type), size = 0.5) +
  geom_sf(data = roads_sf, color = "grey50", size = 0.2, alpha = 0.5) +
  scale_color_brewer(palette = "Set1", name = "Fault Type") +
  # 比例尺和指北针
  annotation_scale(location = "bl", width_hint = 0.2) +
  annotation_north_arrow(location = "tr", which_north = "true",
                         style = north_arrow_fancy_orienteering) +
  labs(title = "Fault Distribution by Type",
       subtitle = "TTCL Network Infrastructure",
       caption = "Data source: TTCL 2023 | Projection: UTM 36S") +
  theme_minimal() +
  theme(panel.grid = element_line(color = "grey90", size = 0.2))

ggsave("output/fault_ggplot_map.pdf", width = 10, height = 8, dpi = 300)
```

### 6.3 Shiny + Leaflet —— 交互式GIS仪表盘

```r
library(shiny)
library(leaflet)
library(terra)
library(sf)
library(DT)

# Shiny 仪表盘框架
ui <- fluidPage(
  titlePanel("GIS Vulnerability Dashboard — Dar es Salaam"),
  sidebarLayout(
    sidebarPanel(
      selectInput("scenario", "Climate Scenario:",
                  choices = c("SSP2-4.5" = "ssp245", "SSP5-8.5" = "ssp585")),
      sliderInput("threshold", "Vulnerability Threshold:",
                  min = 0, max = 1, value = 0.5, step = 0.05),
      downloadButton("downloadMap", "Download Map (HTML)"),
      downloadButton("downloadData", "Download Stats (CSV)")
    ),
    mainPanel(
      leafletOutput("map", height = 600),
      br(),
      DTOutput("stats_table")
    )
  )
)

server <- function(input, output, session) {
  output$map <- renderLeaflet({
    leaflet() |>
      addProviderTiles(providers$CartoDB.Positron) |>
      setView(lng = 39.20, lat = -6.80, zoom = 11)
  })

  observe({
    # 根据用户选择动态更新地图图层
    leafletProxy("map") |>
      clearImages() |>
      addRasterImage(vulnerability_rasters[[input$scenario]],
                     colors = vuln_pal, opacity = 0.7,
                     group = "Vulnerability")
  })

  output$downloadMap <- downloadHandler(
    filename = "vulnerability_map.html",
    content = function(file) {
      htmlwidgets::saveWidget(
        leaflet() |> addRasterImage(vulnerability_raster, colors = vuln_pal),
        file)
    }
  )

  output$downloadData <- downloadHandler(
    filename = "district_vulnerability.csv",
    content = function(file) {
      write.csv(district_vuln_stats, file, row.names = FALSE)
    }
  )
}

shinyApp(ui, server)
```

---

## 七、快速参考表

### 7.1 包 → 使用场景速查

| 包 | 用途 | 替代包 | 难度 |
|----|------|--------|------|
| sf | 矢量读写+空间操作 | (独一档) | ★★☆ |
| terra | 栅格读写+分析 | raster(废弃) | ★★☆ |
| tmap | 专题制图(静+动) | ggplot2+ggspatial | ★★☆ |
| leaflet | 交互Web地图 | mapview(速览) | ★★☆ |
| stars | 多维时空数组 | raster stack | ★★★ |
| spdep | 空间自相关/回归 | spGAM | ★★★ |
| gstat | 地统计(Kriging) | geoR | ★★★ |
| spatstat | 点模式分析 | — | ★★★ |
| dismo | 物种分布模型 | biomod2(集成) | ★★★ |
| tidygeocoder | 地理编码 | googleway | ★☆☆ |
| qgisprocess | R调用QGIS | — | ★★☆ |
| r5r | 交通可达性 | — | ★★☆ |
| whitebox | 地形/水文分析 | RSAGA | ★★★ |
| exactextractr | 快速区域统计 | terra::extract | ★★☆ |
| mapview | 快速交互预览 | tmap(view) | ★☆☆ |
| reticulate | R-Python互通 | — | ★★☆ |
| pROC | ROC曲线+AUC | — | ★☆☆ |
| mapedit | 交互式要素编辑 | — | ★★☆ |

### 7.2 空间函数速查 Top 50

| # | 函数(包) | 签名 | 用途 |
|---|----------|------|------|
| 1 | `sf::st_read()` | `(dsn, layer, query)` | 矢量读取 |
| 2 | `sf::st_write()` | `(obj, dsn, layer, ...)` | 矢量写入 |
| 3 | `sf::st_transform()` | `(x, crs)` | CRS转换 |
| 4 | `sf::st_crs()` | `(x)` | 查询CRS |
| 5 | `sf::st_buffer()` | `(x, dist)` | 缓冲区 |
| 6 | `sf::st_intersects()` | `(x, y, sparse)` | 相交判断 |
| 7 | `sf::st_join()` | `(x, y, join)` | 空间连接 |
| 8 | `sf::st_union()` | `(x)` | 几何合并 |
| 9 | `sf::st_intersection()` | `(x, y)` | 空间裁剪 |
| 10 | `sf::st_difference()` | `(x, y)` | 空间擦除 |
| 11 | `sf::st_area()` | `(x)` | 面积计算 |
| 12 | `sf::st_distance()` | `(x, y)` | 距离矩阵 |
| 13 | `sf::st_as_sf()` | `(x, coords, crs)` | 转sf |
| 14 | `sf::st_coordinates()` | `(x)` | 提取坐标 |
| 15 | `sf::st_make_valid()` | `(x)` | 修复几何 |
| 16 | `terra::rast()` | `(x)` | 读取栅格 |
| 17 | `terra::project()` | `(x, y, method)` | 栅格投影 |
| 18 | `terra::crop()` | `(x, y)` | 栅格裁剪 |
| 19 | `terra::mask()` | `(x, mask)` | 掩膜提取 |
| 20 | `terra::resample()` | `(x, y, method)` | 重采样对齐 |
| 21 | `terra::app()` | `(x, fun)` | 按层计算 |
| 22 | `terra::tapp()` | `(x, index, fun)` | 按索引分组计算 |
| 23 | `terra::terrain()` | `(x, v, neighbors)` | 地形分析 |
| 24 | `terra::classify()` | `(x, rcl)` | 重分类 |
| 25 | `terra::ifel()` | `(test, yes, no)` | 条件判断 |
| 26 | `terra::extract()` | `(x, y, fun)` | 值提取 |
| 27 | `terra::spatSample()` | `(x, size, method)` | 空间采样 |
| 28 | `terra::focal()` | `(x, w, fun)` | 移动窗口 |
| 29 | `terra::distance()` | `(x)` | 距离栅格 |
| 30 | `terra::global()` | `(x, fun)` | 全局统计 |
| 31 | `terra::predict()` | `(object, model)` | 模型预测 |
| 32 | `terra::aggregate()` | `(x, fact, fun)` | 栅格聚合 |
| 33 | `terra::as.polygons()` | `(x)` | 栅格转面 |
| 34 | `terra::vect()` | `(x)` | 创建矢量对象 |
| 35 | `terra::shade()` | `(slope, aspect)` | 山体阴影 |
| 36 | `tmap::tm_shape()` | `(shp)` | 图层起点 |
| 37 | `tmap::tm_raster()` | `(title, palette, style)` | 栅格图层 |
| 38 | `tmap::tm_polygons()` | `(col, title)` | 面图层 |
| 39 | `tmap::tm_symbols()` | `(col, size, shape)` | 点符号 |
| 40 | `tmap::tm_layout()` | `(title, legend.position)` | 地图布局 |
| 41 | `tmap::tmap_save()` | `(tm, filename, dpi)` | 导出地图 |
| 42 | `leaflet::leaflet()` | `()` | 创建地图 |
| 43 | `leaflet::addRasterImage()` | `(x, colors, group)` | 添加栅格 |
| 44 | `leaflet::addPolygons()` | `(data, ...)` | 添加面 |
| 45 | `leaflet::addLegend()` | `(pal, values, title)` | 添加图例 |
| 46 | `leaflet::addLayersControl()` | `(baseGroups, overlayGroups)` | 图层控制 |
| 47 | `spdep::poly2nb()` | `(pl, queen)` | 邻接矩阵 |
| 48 | `spdep::moran.test()` | `(x, listw)` | Moran's I |
| 49 | `gstat::variogram()` | `(formula, data)` | 变异函数 |
| 50 | `gstat::krige()` | `(formula, locations, newdata)` | Kriging插值 |

### 7.3 CRS 快速参考

| 场景 | EPSG | CRS名称 | st_crs() 参数 |
|------|------|---------|---------------|
| WGS84 全球 | 4326 | WGS 84 | `st_crs(4326)` |
| CGCS2000 中国 | 4490 | China Geodetic Coordinate System 2000 | `st_crs(4490)` |
| CGCS2000 GK 6度带 | 4491-4560 | 按带号选择 | `st_crs(4513)` (117°E) |
| Web Mercator | 3857 | WGS 84 / Pseudo-Mercator | `st_crs(3857)` |
| UTM N 31N | 32631 | WGS 84 / UTM zone 31N | `st_crs(32631)` |
| UTM S 36S (Tanzania) | 32736 | WGS 84 / UTM zone 36S | `st_crs(32736)` |
| UTM S 37S (Dar es Salaam) | 32737 | WGS 84 / UTM zone 37S | `st_crs(32737)` |
| Albers等积(非洲) | 102022 | Africa Albers Equal Area Conic | `st_crs("ESRI:102022")` |

```r
# 快速查找UTM EPSG
find_utm <- function(lon, lat) {
  zone <- floor((lon + 180) / 6) + 1
  ifelse(lat >= 0, 32600 + zone, 32700 + zone)
}
find_utm(39.2, -6.8)  # 返回 32736 (UTM 36S)
```

---

## 八、R 包版本与废弃状态 (2026年6月)

| 包 | 状态 | 替代方案 | 备注 |
|----|------|----------|------|
| raster | **已废弃** (2023) | terra | 接口几乎完全兼容，迁移成本低 |
| sp | **已废弃** | sf | `st_as_sf()` 可一键转换 |
| rgdal | **已退役** (CRAN移除, 2023.10) | sf | sf底层内置GDAL/PROJ |
| maptools | **已退役** (CRAN移除) | sf + tmap | — |
| rgeos | **已退役** | sf (内建GEOS) | — |
| mapproj | **不再需要** | sf::st_transform() 内建PROJ | — |
| sf | **活跃维护** (CRAN, v1.0+) | — | 当前R空间数据事实标准 |
| terra | **活跃维护** (CRAN, v1.7+) | — | 当前R栅格数据事实标准 |
| tmap | **活跃维护** (CRAN, v4.0+) | — | v4重大更新，语法变化 |
| leaflet | **活跃维护** (CRAN, v2.2+) | — | — |
| stars | **活跃维护** (CRAN, v0.6+) | — | 多维数组标准 |

---

> 关联阅读：`21_Python_GIS生态.md`（Python GIS横向对比） | `28_项目案例集.md`（实战项目完整代码） | `33_空间分析与统计.md`（空间统计理论与R实现） | `01_基础理论与学科定位.md`（GIS基础概念）

> 术语对照：sf = Simple Features | terra = 地球/土地（拉丁） | CRS = 坐标参考系统 | UTM = 通用横轴墨卡托 | NetCDF = 网络通用数据格式 | GLM = 广义线性模型 | SAR = 空间自回归模型 | SDM = 物种分布模型 | Kriging = 克里金插值 | TPI = 地形位置指数 | TRI = 地形粗糙度指数


<!-- wm:坤图_GIS:V1.0 -->
