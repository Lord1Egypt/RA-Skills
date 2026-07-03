<!-- wm:坤图_GIS:V5.0 -->
# GIS_SKILL V5.0 全局唯一知识ID映射表

> 格式：GIS-KB-G{群组}-{子类}-{序号}
> 子类编码：01-理论 02-标准 03-软件 04-开发 05-实战 06-现代技术 07-自进化 08-附录

## 群组一：基础底座 (GIS-KB-G01)

| 知识ID | 文件名 | 子类 | 关键词 | 国标关联 | 风险等级 |
|--------|--------|------|--------|----------|----------|
| GIS-KB-G01-001 | 01_基础理论与学科定位.md | 理论 | GIS定义,学科定位,发展历程,系统组成,地理本体论 | - | low |
| GIS-KB-G01-002 | 02_坐标系统与投影.md | 理论 | 椭球体,基准面,GCS,PCS,高斯-克吕格,UTM,投影 | GB/T 35644-2017 | high |
| GIS-KB-G01-003 | 03_数据模型与格式.md | 理论 | 矢量,栅格,TIN,点云,GeoParquet,COG,PMTiles | GB/T 30319-2013 | medium |
| GIS-KB-G01-004 | 04_中国三大坐标系实战.md | 理论 | 北京54,西安80,CGCS2000,七参数,四参数,三参数 | GB/T 35644-2017 | high |

## 群组二：标准与规范 (GIS-KB-G02)

| 知识ID | 文件名 | 子类 | 关键词 | 国标关联 | 风险等级 |
|--------|--------|------|--------|----------|----------|
| GIS-KB-G02-001 | 05_国家测绘标准体系.md | 标准 | GB/T,CH/T,行业标准,标准编号速查,国标OGC映射 | GB/T 13923, GB/T 20258 | high |
| GIS-KB-G02-002 | 06_数据生产流程规范.md | 标准 | DLG,DEM,DOM,DSM,SOP,生产流程 | GB/T 18316 | high |
| GIS-KB-G02-003 | 07_质量检查与验收标准.md | 标准 | 二级检查,一级验收,质量元素,质量评定,抽样方案 | GB/T 24356, GB/T 33176 | high |
| GIS-KB-G02-004 | 08_成果汇交与归档规范.md | 标准 | 成果汇交,命名规则,图幅编号,元数据,归档 | CH/T 1007 | medium |
| GIS-KB-G02-005 | 09_新型基础测绘实体规范.md | 标准 | 地理实体,实景三维,17级网格,空间身份编码 | 新型基础测绘系列 | high |
| GIS-KB-G02-006 | 10_测绘建库行业标准流程图集.md | 标准 | Mermaid流程图,建库流程,国土空间,地籍,管线 | 多国标综合 | medium |

## 群组三：软件工具 (GIS-KB-G03)

| 知识ID | 文件名 | 子类 | 关键词 | 软件版本 | 风险等级 |
|--------|--------|------|--------|----------|----------|
| GIS-KB-G03-001 | 12_ArcGIS_Pro.md | 软件 | ArcGIS Pro,ArcPy,ModelBuilder,GDB,拓扑 | 3.6 | high |
| GIS-KB-G03-002 | 13_QGIS.md | 软件 | QGIS,PyQGIS,Processing,GRASS,SAGA | 3.40 LTR | high |
| GIS-KB-G03-003 | 14_CASS11.0.md | 软件 | CASS,南方数码,编码,XDATA,SOUTH | 11.0 | high |
| GIS-KB-G03-004 | 15_iData_数据工厂.md | 软件 | iData,数据工厂,南方数码,质检引擎 | 4.x | medium |
| GIS-KB-G03-005 | 16_SuperMap_iDesktopX.md | 软件 | SuperMap,超图,iDesktopX,AgentX,空间智能体 | 2026 | high |
| GIS-KB-G03-006 | 17_GlobalMapper.md | 软件 | GlobalMapper,LiDAR,地形分析,GMScript | v26.2 | medium |
| GIS-KB-G03-007 | 18_FME_Form与Flow.md | 软件 | FME,ETL,Workbench,Transformer,REST API | 2025.1 | high |
| GIS-KB-G03-008 | 19_多源数据融合.md | 软件 | 坐标统一,ICP配准,多源融合,CAD-GIS-BIM | - | high |
| GIS-KB-G03-009 | 20_GIS资源共享.md | 软件 | 数据源,WMS,WMTS,API,开源SHP,学习社区 | - | low |
| GIS-KB-G03-010 | 36_LiDAR360_点云处理软件.md | 软件 | LiDAR360,点云,PTD,CSF,地面滤波,AI分类 | V9.0 | high |
| GIS-KB-G03-011 | 38_ArcGIS_Pro_3.7_新功能详解.md | 软件 | ArcGIS Pro 3.7,File KG,Embeddings,Analyze Map | 3.7(差异) | high |

## 群组四：开发与自动化 (GIS-KB-G04)

| 知识ID | 文件名 | 子类 | 关键词 | 风险等级 |
|--------|--------|------|--------|----------|
| GIS-KB-G04-001 | 21_Python_GIS生态.md | 开发 | GeoPandas,Rasterio,Shapely,DuckDB,PDAL,GDAL | high |
| GIS-KB-G04-002 | 22_空间数据库.md | 开发 | PostGIS,GDB,GeoPackage,DuckDB,TimescaleDB | high |
| GIS-KB-G04-003 | 23_WebGIS开发.md | 开发 | Leaflet,OpenLayers,Cesium,MapLibre,PMTiles,GeoServer | high |
| GIS-KB-G04-004 | 24_遥感与GEE.md | 开发 | Landsat,Sentinel,GEE,NDVI,NDWI,随机森林 | high |
| GIS-KB-G04-005 | 25_三维GIS与数字孪生.md | 开发 | 倾斜摄影,3DTiles,单体化,数字孪生,BIM+GIS | high |
| GIS-KB-G04-006 | 26_WorkBuddyGIS_AddIn开发.md | 开发 | ArcGIS Pro插件,AddIn,C#,WPF,开发经验 | medium |
| GIS-KB-G04-007 | 27_AI_GIS.md | 开发 | GeoAI,深度学习,SAM,LangSAM,空间大模型,LLM | high |
| GIS-KB-G04-008 | 35_专家级批量处理与自动化实战指南.md | 开发 | 批量处理,ArcPy性能,FME调优,QGIS Processing | high |
| GIS-KB-G04-009 | 39_R语言GIS生态.md | 开发 | terra,sf,tmap,leaflet,R+GIS,气候模拟 | medium |

## 群组五：实战与避坑 (GIS-KB-G05)

| 知识ID | 文件名 | 子类 | 关键词 | 风险等级 |
|--------|--------|------|--------|----------|
| GIS-KB-G05-001 | 28_项目案例集.md | 实战 | 行业案例,城市规划,国土,遥感,地籍,管线 | medium |
| GIS-KB-G05-002 | 29_避坑库.md | 实战 | WRONG/CAUSE/SOLUTION/CODE,反模式,报错,闪退 | high |
| GIS-KB-G05-003 | 30_GIS↔CAD数据转换.md | 实战 | CAD,DWG,DXF,CASS编码,XDATA,四步探查法 | high |
| GIS-KB-G05-004 | 32_GNSS测量与工程应用.md | 实战 | RTK,PPK,CORS,NTRIP,高程拟合,BDS+GPS | high |
| GIS-KB-G05-005 | 33_空间分析与统计.md | 实战 | Moran,GWR,Kriging,IDW,DBSCAN,热点分析 | high |

## 群组六：现代GIS技术栈 (GIS-KB-G06)

| 知识ID | 文件名 | 子类 | 关键词 | 风险等级 |
|--------|--------|------|--------|----------|
| GIS-KB-G06-001 | 40_OGC国际标准速查手册.md | 现代技术 | OGC,WMS,WFS,WMTS,OGC API,STAC,COPC | medium |
| GIS-KB-G06-002 | 41_现代GIS数据处理管道.md | 现代技术 | ETL,管道,云原生,容器化,可复现,增量更新 | medium |
| GIS-KB-G06-003 | 42_多语言地理空间库生态.md | 现代技术 | JTS,GEOS,Shapely,NTS,几何引擎,跨语言 | medium |
| GIS-KB-G06-004 | 43_格式选择决策树与反模式.md | 现代技术 | Shapefile弃用,GeoParquet,FlatGeobuf,COG,PMTiles | medium |
| GIS-KB-G06-005 | 44_QGIS_Processing算法速查手册.md | 现代技术 | Processing,算法ID,QGIS,批量调用,参数 | medium |
| GIS-KB-G06-006 | 45_GIS_Agent技能设计范式.md | 现代技术 | Agent,AI,GIS Agent,提示词,多智能体,编排 | high |

## 群组七：自进化机制 (GIS-KB-G07)

| 知识ID | 文件名 | 子类 | 关键词 | 风险等级 |
|--------|--------|------|--------|----------|
| GIS-KB-G07-001 | 37_自进化反馈机制.md | 自进化 | 反馈,知识缺口,增量搜索,版本升级,GeoEvolve | high |

## 独立附录 (GIS-KB-APP)

| 知识ID | 文件名 | 子类 | 关键词 | 风险等级 |
|--------|--------|------|--------|----------|
| GIS-KB-APP-001 | 31_学习路径与认证资源.md | 附录 | 学习路径,认证,培训,考试,职业发展 | low |

## ID编码规则说明

```
GIS-KB-G{群组编号}-{子类编号}-{序号}

群组编号:
  G01 = 基础底座 (01-04)
  G02 = 标准与规范 (05-10)
  G03 = 软件工具   (12-20, 36, 38)
  G04 = 开发与自动化 (21-27, 35, 39)
  G05 = 实战与避坑 (28-33)
  G06 = 现代GIS技术栈 (39-45中的新建模块)
  G07 = 自进化机制 (37)
  APP = 独立附录 (31)

子类编号:
  01 = 理论 / 02 = 标准 / 03 = 软件 / 04 = 开发
  05 = 实战 / 06 = 现代技术 / 07 = 自进化 / 08 = 附录

序号: 该群组内从001递增

总文件数: 43个活跃知识文件 + feedback/目录(4文件)
```

## 跨文件关联关系（双向引用图）

### 坐标系知识域
```
GIS-KB-G01-002(坐标系统) ↔ GIS-KB-G01-004(三大坐标系实战)
GIS-KB-G01-002 ↔ GIS-KB-G05-004(GNSS测量)
GIS-KB-G01-004 → GIS-KB-G02-002(数据生产)
GIS-KB-G01-002/004 → GIS-KB-G02-001(标准体系)
```

### 标准规范知识域
```
GIS-KB-G02-001 → GIS-KB-G02-002 → GIS-KB-G02-003
GIS-KB-G02-003 → GIS-KB-G02-004 (质检→交付)
GIS-KB-G02-005 ↔ GIS-KB-G02-001 (新型基础测绘)
GIS-KB-G02-006 ↔ GIS-KB-G02-002/003/004 (流程图引用)
```

### 软件工具互操作知识域
```
GIS-KB-G03-001(ArcGIS Pro) ↔ GIS-KB-G03-002(QGIS)
GIS-KB-G03-001 ↔ GIS-KB-G03-011(Pro 3.7差异)
GIS-KB-G03-003(CASS) ↔ GIS-KB-G03-001(ArcGIS)
GIS-KB-G03-006(GlobalMapper) ↔ GIS-KB-G03-007(FME)
GIS-KB-G03-010(LiDAR360) ↔ GIS-KB-G04-005(三维)
```

### 实战知识域
```
GIS-KB-G05-001(案例集) → 所有软件工具文件
GIS-KB-G05-001 → GIS-KB-G02-001~004 (标准引用)
GIS-KB-G05-002(避坑库) → 全部 (通用故障知识)
GIS-KB-G05-003(CAD-GIS) ↔ GIS-KB-G03-003(CASS)
```

### 自进化知识域
```
GIS-KB-G07-001(自进化) → GIS-KB-G02-001(国标更新)
GIS-KB-G07-001 → GIS-KB-G05-002(避坑增量)
GIS-KB-G07-001 → GIS-KB-G03-011(版本检测)
GIS-KB-G07-001 → feedback/ (反馈数据)
```

> **V5.0新增**：此映射表替代V1.0纯文本注释式关联，支持GraphRAG知识图谱检索。
> 后续通过geo_kg/mermaid/目录生成Mermaid双向关联图。
