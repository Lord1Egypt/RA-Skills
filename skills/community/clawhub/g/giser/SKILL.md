---
name: GIS_SKILL
description: >
  统一 GIS 综合知识库 V1.0（45文件模块化体系 | 2026年6月 公开上架版）。
  七群组架构：基础底座(4) | 标准与规范(6) | 软件工具(13) | 开发与自动化(8) | 实战与避坑(5) | 现代GIS技术栈(7) | 自进化机制(1) + 独立附录(1)。
  本次更新（8个GitHub GIS Skill包深度交叉对比驱动）：结构重组（删除3空占位/20号统一/27号激活/游离文件归组/29号去数字后缀/31号独立附录）|
  新增7个核心模块：R语言GIS生态(39)|OGC国际标准速查(40)|现代GIS管道(41)|多语言空间库(42)|格式决策树(43)|QGIS算法速查(44)|Agent技能范式(45)|
  QGIS全面重写：从概览→PyQGIS完整教材(13号)|云原生格式扩充(03号)|PMTiles部署(23号)|结构化反模式(29号)|2个新案例(28号)。
  覆盖：坐标系/投影/椭球基准（GB标准EPSG WKID）、CASS11.0/iData/SuperMap GIS 2026/GlobalMapper v26.2/FME 2025/ArcGIS Pro 3.7/**LiDAR360 V9.0**等9款专业软件实操、
  国家测绘标准体系（65+项现行国标神经链接版，含2025年7月发布的5项新国标）、新型基础测绘实体规范、
   GIS↔CAD数据转换方法论、Python GIS生态(GeoPandas/Rasterio/Shapely/PyProj/GDAL/DuckDB Spatial)、
  **R语言GIS生态**(terra/sf/tmap/leaflet/spatSample)、**OGC国际标准体系**(60+标准WMS/WFS/WMTS/OGC API/PMTiles/COG/GeoParquet)、
  **现代GIS数据处理管道**(7种标准化模式/验证清单/可重现性要求)、**QGIS Processing 200+算法ID全目录**、
  多语言几何引擎链(JTS→GEOS→Shapely→NTS→JSTS)、格式选择决策树与12条反模式、
  **GIS Agent技能设计范式**(Reviewer/Inversion/Pipeline/Orchestrator)、
  遥感与GEE/WebGIS/实景三维/GNSS/空间分析/深度学习、避坑库160+条目（WRONG/CORRECT/WHY结构化）、10大行业项目案例、
  专家级批量处理指南(OSGB→SLPK工程化/ArcPy性能优化/FME调优11技巧/QGIS Processing API)、
  跨软件协同工作流、坐标系七参数实战、GitHub已知Bug速查、Esri官方博客技术收录(GeoAI/3D Analyst/Reality Studio/Pro Assistant)、
  **LiDAR360点云分类算法PTD vs CSF深度对比与避坑（重点）、32类AI自动分类、林业单木18+属性提取、
  **ArcGIS Pro 3.7完整新功能详解**（File Knowledge Graph/Telecom Domain Networks/Embeddings-Based Analysis/Analyze Map）、
  **自进化反馈机制**（用户反馈驱动迭代/知识缺口自动检测/增量搜索触发/版本自动升级）。
  This skill should be used when the user mentions GIS, surveying/mapping, coordinate systems,
  CASS, iData, SuperMap, GlobalMapper, FME, QGIS, ArcGIS, GDB, DWG conversion, geodatabase,
  projections, datums, spatial data processing, quality inspection, geo-entity,
  basic surveying and mapping standards, project cost estimation, national standards GB/T,
  batch processing, performance tuning, automation, ETL, OSGB, SLPK, point cloud, deep learning,
  LiDAR360, lidar, point cloud classification, PTD, CSF, ground filtering, GreenValley,
  self-evolution, feedback, knowledge gap, ArcGIS Pro 3.7, CityGML, 3DTiles, GeoPackage,
  OGC, WMS, WFS, WMTS, GeoParquet, COG, PMTiles, DuckDB Spatial, PyQGIS, terra, tmap,
  R spatial, GDAL, PostGIS, GeoServer, MapLibre, tippecanoe, Martin, PMTiles, STAC.
agent_created: true

x-author-id: "坤图_GIS"
x-skill-fingerprint: "d24782d2025a"
x-license: "CC-BY-NC-SA-4.0"
version: "1.0"
---

# GIS 综合知识库 V1.0 Cross-Validation Edition

> 版本：2026.06.04-V1.0 8包交叉验证+结构重组 | 45文件七群组体系 | 避坑库160+条 | 自进化机制
> 基础来源：旧版 V2.x (7,805行单文件) + V3.0/V3.1模块化重构 + V4.0桌面软件深度扩展 + V4.1反向验证重写 + V4.2 ArcGIS版本双轨/标准深扩/资源共享
> **V1.0 结构重组**：删除3空占位(11/20移动采集/34) | 20号统一为GIS资源共享 | 27号激活(AI_GIS) | 游离文件归组(35/36/38) | 29号去数字后缀 | 31号独立附录
> **V1.0 新增7模块(39-45)**：R语言GIS生态(39) | OGC国际标准速查(40) | 现代GIS管道(41) | 多语言空间库(42) | 格式决策树(43) | QGIS算法速查(44) | Agent技能范式(45)
> **V1.0 重写/扩充**：QGIS→PyQGIS全教材 | 云原生格式(03) | PMTiles部署(23) | 结构化反模式(29) | 新案例×2(28)
> 交叉验证来源：open-gis-main | opengis-skills-main | QGIS-Claude-Skill-Package | Geospatial-Analysis-Portfolio | gisdataagent-main | GIS-Community-Resources

---

## 底层执行引擎：7段式企业级工作流

> **这是 GIS Skill 的核心操作系统。任何任务都先经过此引擎，再进入具体模块。**

### 刚性规则

| 规则 | 含义 |
|------|------|
| **禁止模糊执行** | 任何一步不确定，必须停下来输出诊断报告 |
| **禁止跳过检查** | 不做数据探查，绝不进入处理流程 |
| **禁止无日志运行** | 每一步必须记录，可追溯、可复盘 |
| **禁止自动硬扛** | 遇到异常立即降级、重试、报告 |

### 七阶段流程

| 阶段 | 名称 | 输出物 | 关联模块 |
|------|------|--------|----------|
| 阶段1 | **需求锁定** | 《需求确认单》 | 全部 |
| 阶段2 | **深度数据洞察** | 《数据透视与风险报告》 | 03/06/07/29 |
| 阶段3 | **方案生成** | 《执行方案说明书》 | 02/05/06 |
| 阶段4 | **环境与预处理** | 预处理日志 | 02/03/06 |
| 阶段5 | **核心执行** | 过程日志 | 12~20（依任务选） |
| 阶段6 | **成果自检** | 《成果质量检查报告》 | 07/08/29 |
| 阶段7 | **输出与归档** | 成果文件+质量报告+日志 | 08/28 |

> **自进化增强**：每阶段完成后，检查 `feedback/knowledge_gaps.md` 是否有相关知识缺口，有则触发增量搜索。

---

## 文件体系总览

```
~/.workbuddy/skills/GIS/
├── SKILL.md                              ← 本文件（总导航 / 神经网络中枢）
│
├── 【群组一：基础底座】4 文件
│   ├── 01_基础理论与学科定位.md           ← GIS定义/发展/组成/应用领域
│   ├── 02_坐标系统与投影.md               ← 椭球体→基准面→GCS→PCS完整链路
│   ├── 03_数据模型与格式.md               ← 矢量/栅格/TIN/点云 + 云原生格式(GeoParquet/COG/PMTiles)
│   └── 04_中国三大坐标系实战.md           ← 北京54/西安80/CGCS2000转换实战
│
├── 【群组二：标准与规范】6 文件
│   ├── 05_国家测绘标准体系.md              ← 标准编号速查表(GB/T+CH/T+行业)+15项核心标准技术摘要
│   ├── 06_数据生产流程规范.md              ← DLG/DEM/DOM生产SOP
│   ├── 07_质量检查与验收标准.md            ← GB/T 18316·24356·33176·39610 + CASS/ArcGIS/FME质检自动化SOP
│   ├── 08_成果汇交与归档规范.md            ← 交付模板/命名规则/图幅编号
│   ├── 09_新型基础测绘实体规范.md          ← 地理实体/实景三维/17级网格
│   └── 10_测绘建库行业标准流程图集.md       ← Mermaid流程图集
│
├── 【群组三：软件工具】13 文件
│   ├── 12_ArcGIS_Pro.md                   ← 核心功能/扩展/ModelBuilder/ArcPy [v3.6]
│   ├── 13_QGIS.md                         ← 大幅扩充（PyQGIS完整教材：5类19技能+200+算法ID）
│   ├── 14_CASS11.0.md                     ← 编码/文件体系/工作流
│   ├── 15_iData_数据工厂.md               ← 新建
│   ├── 16_SuperMap_iDesktopX.md           ← 新建(含2026智能体新特性)
│   ├── 17_GlobalMapper.md                 ← 新建(v26.2)
│   ├── 18_FME_Form与Flow.md               ← 新建(2025.1+)
│   ├── 19_多源数据融合.md                 ← V4.1激活（坐标统一/点云矢量配准/三维格式互转）
│   ├── 20_GIS资源共享.md                  ← 全球/中国数据源/WMS-WMTS服务/API/开源SHP/学习社区
│   ├── 36_LiDAR360_点云处理软件.md         ← PTD vs CSF深度避坑/32类AI分类/林业18+属性提取
│   └── 38_ArcGIS_Pro_3.7_新功能详解.md    ← File Knowledge Graph/Telecom/Embeddings/Analyze Map [仅3.7新增]
│
├── 【群组四：开发与自动化】8 文件
│   ├── 21_Python_GIS生态.md               ← GeoPandas/Rasterio/Shapely + DuckDB Spatial
│   ├── 22_空间数据库.md                   ← PostGIS/GDB/GeoPackage原理与操作
│   ├── 23_WebGIS开发.md                   ← Leaflet/OpenLayers/Cesium/ArcGIS JS + PMTiles部署
│   ├── 24_遥感与GEE.md                    ← Landsat/Sentinel/GEE+点云/LiDAR
│   ├── 25_三维GIS与数字孪生.md            ← 倾斜摄影/3DTiles/单体化/轻量化
│   ├── 26_WorkBuddyGIS_AddIn开发.md       ← ArcGIS Pro插件开发经验
│   ├── 27_AI_GIS.md                       ← GeoAI/深度学习遥感解译（已激活）
│   └── 35_专家级批量处理与自动化实战指南.md ← ArcPy性能优化/FME调优11技巧/QGIS Processing/GDAL批处理
│
├── 【群组五：实战与避坑】5 文件
│   ├── 28_项目案例集.md                   ← 8大行业案例(深度可执行)
│   ├── 29_避坑库.md                       ← 16类160+条避坑（WRONG/CORRECT/WHY结构化反模式）
│   ├── 30_GIS↔CAD数据转换.md              ← 四步探查法/映射表/XDATA
│   ├── 32_GNSS测量与工程应用.md           ← GPS/BDS/RTK/PPK/CORS
│   └── 33_空间分析与统计.md               ← Moran's I/G*WR/Kriging/DBSCAN/可执行代码
│
├── 【群组六：现代GIS技术栈】7 文件 ← V1.0 新建
│   ├── 39_R语言GIS生态.md                 ← terra/sf/tmap/leaflet(1549行)|R+GIS五模式集成|故障预测+气候脆弱性全流程
│   ├── 40_OGC国际标准速查手册.md           ← 60+标准(1646行)|WMS/WFS/WMTS/OGC API 6系列|轴序10格式总表|中国国标映射
│   ├── 41_现代GIS数据处理管道.md           ← 7种管道模式(1471行)|验证清单|可重现性|12反模式|Shell最佳实践
│   ├── 42_多语言地理空间库生态.md          ← 几何引擎链(1167行)|7语言速查|17场景决策|CRS跨语言|格式矩阵
│   ├── 43_格式选择决策树与反模式.md         ← 5决策树(1308行)|Shapefile弃用时间表|15格式×9维矩阵|2026推荐栈
│   ├── 44_QGIS_Processing算法速查手册.md   ← 50+算法速查(961行)|5编程模板|8陷阱|性能优化|20场景映射
│   └── 45_GIS_Agent技能设计范式.md        ← 6设计模式(1442行)|提示词工程|3工作流案例|评估框架|自进化
│
├── 【群组七：自进化机制】1 文件 ← 原群组六
│   └── 37_自进化反馈机制.md               ← 反馈驱动迭代/知识缺口检测/增量搜索/版本自动升级
│
├── 【独立附录】
│   └── 31_学习路径与认证资源.md            ← 5条职业路径→学习路线→认证体系（独立于群组）
│
├── feedback/                                ← 自进化追踪目录
│   ├── knowledge_gaps.md                  ← 知识缺口追踪表
│   ├── feedback_log.md                   ← 用户反馈日志
│   ├── revision_history.md                ← 修正历史记录
│   └── config.json                       ← 自进化配置参数
│
├── assets/                                ← 示意图/流程图/数据样例
└── scripts/
    └── backup.ps1
```

---

## 快速导航（按需求类型）

### 我要学习 GIS 基础

| 需求 | 目标文件 |
|------|---------|
| GIS 是什么、怎么来的、用在哪里 | `01_基础理论与学科定位.md` |
| 坐标系统入门（WGS84/投影/高斯） | `02_坐标系统与投影.md` |
| 矢量/栅格/TIN 数据结构 | `03_数据模型与格式.md` |
| 中国三大坐标系怎么转 | `04_中国三大坐标系实战.md` |
| 完整学习路径（入门→进阶→高级） | `31_学习路径与认证资源.md` |

### 我要查国家标准/规范

| 需求 | 目标文件 |
|------|---------|
| 标准编号速查（GB/T ××××） | `05_国家测绘标准体系.md` |
| DLG/DEM/DOM 生产怎么搞 | `06_数据生产流程规范.md` |
| 质检怎么检、验收怎么验 | `07_质量检查与验收标准.md` |
| 成果怎么交、报告怎么写 | `08_成果汇交与归档规范.md` |
| 新型基础测绘/地理实体 | `09_新型基础测绘实体规范.md` |
| 行业标准流程图 | `10_测绘建库行业标准流程图集.md` |

### 我要用某款软件

| 软件 | 目标文件 | 深度 |
|------|---------|------|
| ArcGIS Pro（商业标准） | `12_ArcGIS_Pro.md` | ★★★★★ |
| QGIS（开源首选，PyQGIS全教材） | `13_QGIS.md` | ★★★★★ |
| CASS 11.0（南方数码） | `14_CASS11.0.md` | ★★★★★ |
| iData 数据工厂 | `15_iData_数据工厂.md` | ★★★★☆ |
| SuperMap iDesktopX | `16_SuperMap_iDesktopX.md` | ★★★★☆ |
| GlobalMapper | `17_GlobalMapper.md` | ★★★★☆ |
| FME Form/Flow | `18_FME_Form与Flow.md` | ★★★★★ |
| **LiDAR360（点云专用）** | `36_LiDAR360_点云处理软件.md` | ★★★★★ |
| **ArcGIS Pro 3.7 新功能** | `38_ArcGIS_Pro_3.7_新功能详解.md` | ★★★★★ |
| **多源数据融合** | `19_多源数据融合.md` | ★★★★☆ |

### 我要写代码/做开发

| 需求 | 目标文件 |
|------|---------|
| Python 处理矢量/栅格 | `21_Python_GIS生态.md` |
| R语言 处理矢量/栅格（terra/sf/tmap） | `39_R语言GIS生态.md` |
| 空间数据库（PostGIS/GDB） | `22_空间数据库.md` |
| WebGIS 前端开发 + PMTiles部署 | `23_WebGIS开发.md` |
| GEE 遥感云平台 | `24_遥感与GEE.md` |
| 三维/Cesium | `25_三维GIS与数字孪生.md` |
| ArcGIS Pro 插件开发 | `26_WorkBuddyGIS_AddIn开发.md` |
| AI/GeoAI 深度学习遥感 | `27_AI_GIS.md` |
| QGIS Processing 200+算法速查 | `44_QGIS_Processing算法速查手册.md` |
| 跨语言几何引擎（JTS/GEOS/Shapely/NTS） | `42_多语言地理空间库生态.md` |

### 我要做项目/解决问题

| 需求 | 目标文件 |
|------|---------|
| 10大行业案例实操（含光纤故障预测/气候脆弱性评估） | `28_项目案例集.md` |
| 遇到报错/踩坑了（160+条结构化反模式） | `29_避坑库.md` |
| CAD↔GIS 数据转换 | `30_GIS↔CAD数据转换.md` |
| GNSS/RTK 测量 | `32_GNSS测量与工程应用.md` |
| 空间统计分析 | `33_空间分析与统计.md` |
| 多源数据融合问题 | `19_多源数据融合.md` |
| 现代GIS数据处理管道 | `41_现代GIS数据处理管道.md` |
| 格式选择与常见反模式 | `43_格式选择决策树与反模式.md` |

### 我要查国际标准/现代化工具

| 需求 | 目标文件 |
|------|---------|
| OGC国际标准（WMS/WFS/WMTS/OGC API 60+标准） | `40_OGC国际标准速查手册.md` |
| 现代GIS技术栈（GeoParquet/COG/PMTiles/DuckDB） | `41_现代GIS数据处理管道.md` |
| 格式选择决策树（Shapefile弃用时间表） | `43_格式选择决策树与反模式.md` |
| GIS Agent技能设计（AI Agent × GIS 四种范式） | `45_GIS_Agent技能设计范式.md` |
| GIS数据源/API/在线服务 | `20_GIS资源共享.md` |

### 自进化与反馈

| 需求 | 目标文件 |
|------|---------|
| 发现错误/需要纠正 | `feedback/feedback_log.md` → 触发修正协议 |
| 知识库有缺口 | `feedback/knowledge_gaps.md` → 触发增量搜索 |
| 查看修正历史 | `feedback/revision_history.md` |
| 配置自进化参数 | `feedback/config.json` |

---

## 模块间神经连接网络

> 以下标注文件之间的强关联（←→ 双向引用，→ 单向依赖，⟹ 标准引用关系）

### 坐标系知识域

```
02_坐标系统与投影.md ←→ 04_中国三大坐标系实战.md
02 ←→ 32_GNSS测量与工程应用.md（WGS84↔CGCS2000转换）
04 → 06_数据生产流程规范.md（CGCS2000是法定坐标系）
02/04 ⟹ 05_国家测绘标准体系.md（引用GB/T坐标系规范）
```

### 数据转换知识域

```
30_GIS↔CAD数据转换.md ←→ 03_数据模型与格式.md（数据模型差异是转换的基础）
30 ←→ 14_CASS11.0.md（XDATA/CASS_CODE深度绑定）
30 → 18_FME_Form与Flow.md（FME是最强转换引擎）
30 → 21_Python_GIS生态.md（GeoPandas/GDAL/Fiona脚本方案）
19_多源数据融合.md ←→ 30（坐标系统一/点云矢量配准/多格式互转）
```

### 标准规范知识域（群组二内部强关联）

```
05_国家测绘标准体系.md ⟹ 06_数据生产流程规范.md（生产需引用标准）
05 ⟹ 07_质量检查与验收标准.md（质检需引用标准）
06 → 07 → 08（生产→质检→交付 串行链路）
09_新型基础测绘实体规范.md ←→ 05（新型标准体系纳入国标体系）
10_测绘建库行业标准流程图集.md ←→ 06/07/08（流程图的依据是标准）
```

### 软件工具互操作知识域

```
12_ArcGIS_Pro.md ←→ 13_QGIS.md（功能对标对比）
12_ArcGIS_Pro.md ←→ 38_ArcGIS_Pro_3.7_新功能详解.md（版本双轨 v3.6 ↔ v3.7新增）
14_CASS11.0.md ←→ 12_ArcGIS_Pro.md（CASS→GDB→ArcGIS工作流）
14 ←→ 15_iData_数据工厂.md（同为南方数码产品，协同场景）
17_GlobalMapper.md ←→ 18_FME_Form与Flow.md（万能转换互补工具）
12/13/16 → 22_空间数据库.md（桌面软件+数据库后端）
19_多源数据融合.md ←→ 04/17/25（坐标统一/点云配准/三维格式互转）
36_LiDAR360_点云处理软件.md ←→ 25/24（点云→三维/遥感交叉应用）
```

### 项目实战知识域

```
28_项目案例集.md → 所有软件工具文件（依赖具体工具实现）
28 → 05~10（项目需引用标准规范）
28 → 29_避坑库.md（案例中的坑 = 避坑库来源）
19_多源数据融合.md → 28（多源融合是大型项目常见需求）
```

### 新兴技术知识域

```
24_遥感与GEE.md ←→ 25_三维GIS与数字孪生.md（遥感影像→三维底图）
23_WebGIS开发.md ←→ 25（Cesium = Web+三维）
27_AI_GIS.md → 24（深度学习遥感解译）
41_现代GIS数据处理管道.md ←→ 23/03（管道模式→WebGIS部署/云原生格式）
40_OGC国际标准速查手册.md ←→ 23/22/13（OGC标准→WebGIS/PostGIS/QGIS Server）
45_GIS_Agent技能设计范式.md ←→ 27/41（Agent模式→AI_GIS/管道自动化）
```

### V1.0 新增知识域（群组六：现代GIS技术栈）

```
39_R语言GIS生态.md ←→ 21_Python_GIS生态.md（双语言生态对标）
40_OGC国际标准速查手册.md ←→ 05_国家测绘标准体系.md（国际标准 ↔ 中国国标互补）
41_现代GIS数据处理管道.md ←→ 35_专家级批量处理.md（管道模式 → 批量自动化实现）
42_多语言地理空间库生态.md ←→ 21/39（跨语言几何引擎 → Python/R生态）
43_格式选择决策树与反模式.md ←→ 03_数据模型与格式.md / 29_避坑库.md（格式决策 → 数据模型 / 避坑反模式）
44_QGIS_Processing算法速查手册.md ←→ 13_QGIS.md / 35_专家级批量处理.md（算法ID → QGIS教材 / 批量处理实现）
45_GIS_Agent技能设计范式.md ←→ 27_AI_GIS.md / 37_自进化反馈机制.md（Agent模式 → AI执行 / 自进化循环）
```

### 自进化机制知识域

```
37_自进化反馈机制.md
  ├── → SKILL.md（版本号管理 / 更新日志）
  ├── → 05_国家测绘标准体系.md（新国标自动检测）
  ├── → 29_避坑库.md（新坑自动收录）
  ├── → 36_LiDAR360_点云处理软件.md（算法更新检测）
  ├── → feedback/（所有反馈数据存放目录）
  └── → 38_ArcGIS_Pro_3.7_新功能详解.md（版本更新检测）
```

---

## 检索关键词映射表（完整版）

### 坐标系 / 投影

- `WKID`, `EPSG`, `4326`, `4490`, `3857` → `02_坐标系统与投影.md`
- `高斯-克吕格`, `3度带`, `6度带`, `中央子午线`, `CGCS2000` → `02/04`
- `椭球体`, `Krasovsky`, `扁率`, `基准面`, `Datum` → `02`
- `北京54`, `西安80`, `三参数`, `七参数`, `四参数` → `04`
- `Web墨卡托`, `UTM`, `横轴墨卡托` → `02`

### 软件工具

- `ArcPy`, `arcpy.da`, `arcpy.sa`, `arcpy.stats`, `arcpy.mp` → `12_ArcGIS_Pro.md`
- `ModelBuilder`, `Tasks`, `扩展模块`, `高斯泼溅` → `12`
- `拓扑`, `GDB`, `属性域`, `子类型`, `属性规则` → `12`
- `QGIS`, `PyQGIS`, `Processing`, `GRASS`, `SAGA` → `13_QGIS.md`
- `CASS编码`, `六位码`, `class.config`, `.DAT`, `XDATA`, `SOUTH` → `14_CASS11.0.md`
- `iData`, `数据工厂`, `南方数码`, `一体化生产` → `15_iData_数据工厂.md`
- `SuperMap`, `超图`, `iDesktopX`, `AgentX`, `ClientX`, `空间智能体` → `16_SuperMap_iDesktopX.md`
- `GlobalMapper`, `GM`, `Blue Marble`, `LiDAR分类`, `地形分析` → `17_GlobalMapper.md`
- `FME`, `ETL`, `Safe Software`, `Workbench`, `Transformer` → `18_FME_Form与Flow.md`
- `LiDAR360`, `lidar`, `点云分类`, `PTD`, `CSF`, `ground filtering`, `GreenValley` → `36_LiDAR360_点云处理软件.md`
- `ArcGIS Pro 3.7`, `File Knowledge Graph`, `Embeddings`, `Analyze Map` → `38_ArcGIS_Pro_3.7_新功能详解.md`

### 国家标准

- `GB/T`, `国家标准`, `行业标准`, `CH/T` → `05_国家测绘标准体系.md`
- `GB/T 13923`, `要素分类`, `分类代码` → `05`
- `GB/T 18316`, `数字测绘成果`, `质量检验` → `07_质量检查与验收标准.md`
- `GB/T 24356`, `DEM/DOM/DLG`, `成果质量` → `07`
- `GB/T 20258`, `基础地理信息要素数据字典` → `05/06`
- `GB/T 33176`, `地形图精度`, `数学精度` → `07`
- `GB/T 39610`, `倾斜摄影`, `三维模型精度` → `07`
- `二级检查`, `一级验收`, `质量元素`, `质量评定`, `抽样方案` → `07`
- `DLG生产`, `DEM生产`, `DOM生产`, `DSM生产` → `06_数据生产流程规范.md`
- `成果汇交`, `命名规则`, `图幅编号`, `元数据` → `08_成果汇交与归档规范.md`
- `地理实体`, `实景三维`, `17级网格`, `空间身份编码` → `09_新型基础测绘实体规范.md`

### 数据处理 / 转换

- `GDAL`, `ogr2ogr`, `gdalwarp`, `gdal_translate`, `gdal_merge` → `21_Python_GIS生态.md`
- `GeoPandas`, `Shapely`, `Fiona`, `PyProj`, `Rasterio`, `xarray` → `21`
- `PDAL`, `laspy`, `LiDAR`, `LAS`, `LAZ`, `点云`, `地面滤波`, `SMRF`, `CSF` → `24_遥感与GEE.md`
- `数据探查`, `映射表`, `数据模型差异`, `CAD↔GIS` → `30_GIS↔CAD数据转换.md`

### 空间分析 / 统计

- `Moran's I`, `LISA`, `Getis-Ord`, `热点分析` → `33_空间分析与统计.md`
- `GWR`, `Kriging`, `IDW`, `Spline`, `DBSCAN` → `33`
- `缓冲区`, `叠加分析`, `网络分析`, `Service Area` → `12/13`

### 避坑 / 故障

- `报错`, `闪退`, `崩溃`, `失败`, `不生效`, `坑` → `29_避坑库110+.md`
- `乱码`, `GBK`, `UTF-8`, `中文路径` → `29`
- `坐标偏移`, `飞图`, `投影不一致` → `02/29`
- `拓扑错误`, `悬挂节点`, `面重叠` → `29`
- `深度学习`, `ERROR 999999`, `样本不足`, `GPU显存` → `29`

### Web / 三维 / GNSS

- `WMS`, `WFS`, `WMTS`, `OGC`, `GeoServer`, `Leaflet`, `OpenLayers`, `Cesium` → `23_WebGIS开发.md`
- `倾斜摄影`, `3DTiles`, `OSGB`, `CityGML`, `单体化`, `LOD` → `25_三维GIS与数字孪生.md`
- `NDVI`, `NDWI`, `NDBI`, `GEE`, `Landsat`, `Sentinel`, `随机森林` → `24_遥感与GEE.md`
- `RTK`, `PPK`, `CORS`, `NTRIP`, `高程拟合` → `32_GNSS测量与工程应用.md`

### 自进化 / 反馈

- `反馈`, `纠错`, `补充`, `不对`, `错了` → `feedback/feedback_log.md`
- `知识缺口`, `缺少`, `没有找到` → `feedback/knowledge_gaps.md`
- `自进化`, `更新知识库`, `搜索最新` → `37_自进化反馈机制.md`

---

## 软件版本对照表（2026年6月4日验证）

| 软件 | 当前最新版本 | 上代版本 | 关键差异 |
|------|-----------|---------|----------|
| **ArcGIS Pro** | 3.7 (2026年5月) | 3.4 (LTS) | 3.7：File Knowledge Graph/Telecom Domain/Embeddings Analysis/Analyze Map |
| **QGIS** | 3.40.x LTR / 3.42 稳定版 | 3.34 LTR | 3.40：原生点云支持增强、3D视图性能提升、新增Temporal Controller |
| **CASS** | 11.0 | 10.1 | 11.0：全面对接CGCS2000、支持新型基础测绘实体、增强三维测图 |
| **iData** | 3.x (数据工厂) | 2.x | 3.x：一体化数据生产平台、模板化质检、三维采编 |
| **SuperMap GIS** | 2026 | 2025 | 2026：智能体原生(AgentX)、二三维一体化ClientX(Beta)、鸿蒙MobileX(Beta) |
| **GlobalMapper** | v26.2 | v25.x | v26.2：用户驱动的UI重构、LiDAR着色器缩放、动画工具 |
| **FME** | 2025.1 | 2024.2 | 2025.1：性能大幅提升、新增AI连接器、增强数据QA功能 |
| **LiDAR360** | V9.0 | V8.0 | V9.0：更大体量支持(>300GB)、新增Deep Learning分类、支持I3S/3DTiles直接输出 |

---

## 版本迭代记录

| 版本 | 日期 | 变更 |
|------|------|------|
| **V4.2** | **2026-06-04** | **底层标准文件深扩 + 版本差异体系 + 资源共享模块**：⑤ 05号国家测绘标准体系深扩（321→1,445行，新增15项核心标准技术摘要、标准选择决策树、区域性差异、10个常见问题）；⑥ 07号质量检查与验收标准深扩（233→895行，新增9大元素检查清单、CASS/ArcGIS Pro/FME自动化质检SOP、10个缺陷案例库、新型成果质检专项）；① ArcGIS Pro 3.6/3.7 版本差异双轨制建立；② 新增"版本差异指引"章节（SKILL.md）；③ 激活20号为"GIS资源共享"模块（~200行）；④ 基于 ArcGIS Learning Gallery + OSGeo 中国站知识结构启动系统性完善。后续将结合 awesome-gis 交叉对比结果批量优化。知识库总计 ~23,000行。 |
| **V4.1** | **2026-06-04** | **反向验证报告驱动全面优化**：基于V4.0验证报告逐章反向验证，发现4大短板并全面补全。25号(三维GIS 239→2124行) 全面重写（倾斜摄影采集规范/像控点布设/空三深度/纹理反光处理/模型质检/LOD/Draco压缩/数字孪生）；26号(WorkBuddy AddIn 79→938行) 大幅扩充（命令绑定诊断/IPC桥接架构/异步调试/编译SOP/诊断清单）；19号(预留→872行) 激活为多源数据融合模块（坐标系统一七参数代码/点云ICP配准/三维格式互转矩阵/CAD-GIS-BIM全链路/深度学习融合架构）；01号新增路径规范速查表；24号新增多传感器指数速查表；23号新增WebGIS服务端运维章（GeoServer SLD/CSS/Nginx跨域/缓存刷新/权限）；33号新增空间分析可执行代码集；29号神经连接全面更新（旧章节→新模块编号）。代码增长~4,500行。 |
| V4.0 | 2026-06-04 | 全面优化验证版：基于V3.4验证报告4大弱项优化。27号(AI+GIS 45%→75%) 14行→403行完整重写；18号(FME 82%→92%) 新增REST API客户端+Automations编排+性能11招；23号(WebGIS 70%→85%) 新增Cesium+ol-cesium完整项目+矢量瓦片服务端；37号(自进化70%→90%) WPS量化算法+FQS反馈评分+增强配置。桌面软件全员升级至★★★★☆。约+3,500行代码。 |
| V3.4 | 2026-06-03 | 自进化机制：新增37号(406行)+38号(1,078行)+feedback/目录(4文件)。文件总数：40。 |
| V3.3 | 2026-06-03 | LiDAR360完整收录：新增36号文件(567行) + 避坑库B.19(10条) + B.20(Esri Blog 5组) + SKILL.md V3.3升级。 |
| V3.2 | 2026-06-03 | 专家级批量处理：新增35号文件(556行) + 避坑库B.17~B.18(18条) + 05号标准文件重写(1827行) + SKILL.md V3.2升级。 |
| V3.1 | 2026-06-03 | 国标收录：05号标准文件重写(1827行) + 神经链接矩阵 + 标注2024-2026新标10项。 |
| V3.0 | 2026-06-03 | 模块化重构：旧版V2.x(7,805行单文件) → 32文件五群组体系 + 6预留扩展位。 |
| V2.x | 2026-05-23~06-03 | 21篇+4附录单文件体系，~7,805行。WorkBuddyGIS AddIn开发经验沉淀。 |

---

## 已知局限与待补充

| 序号 | 内容 | 原因 | 处理方式 |
|------|------|------|---------|
| 1 | GB/T 24356-2023 完整条款 | PDF编码损坏 | 仅以已知框架补充→待获取可读版本 |
| 2 | GB/T 20257.1-2017 完整内容 | 110MB扫描版 | 仅引用编号，具体条款待OCR |
| 3 | 湖北省勘察设计收费标准 完整 | 149页扫描版OCR失败 | 仅保留前50页核心数据 |
| 4 | iData 部分高级功能 | 需要实际软件环境验证 | V4.0已补充质检引擎深度+入库方案+三维采编进阶 |
| 5 | SuperMap 2026 具体产品版本号 | 2026.05.26刚发布，细节待官方释出 | V4.0已补充大数据分布式+iServer REST API+AgentX实战 |
| 6 | [预留] 3个空白位 | 等待对应知识积累 | 11/20/34 共3个占位，含模板头（19号已在V4.1激活为多源数据融合） |
| 7 | 三维GIS倾斜摄影高级参数 | V4.1已全面重写补充(239→2124行) | 持续跟进新软件版本 |
| 8 | WebGIS服务端运维 | V4.1已新增GeoServer/ArcGIS Server运维章 | 持续补充云原生部署方案（K8s/Docker） |

---

## 版本差异指引（Version Difference Protocol）

> **原则**：本知识库同时维护同一软件的多个版本信息（如 ArcGIS Pro 3.6 / 3.7），**绝不删除**任何版本的数据。使用者可能使用任一版本，版本混淆会导致回答错误。

### 核心规则

1. **主版本文件 + 差异文件 双轨制**：
   - 12_ArcGIS_Pro.md = ArcGIS Pro **3.6** 完整手册（~2,086行）
   - 38_ArcGIS_Pro_3.7_新功能详解.md = **3.7 相对于 3.6 的新增/变更**
   
2. **回答前核对提问者指定的版本**：
   - 提问者说"3.6" → 只用 12号 + 确认不包含 38号的 [v3.7] 标记内容
   - 提问者说"3.7" → 12号基础 + 38号新增 = 完整答案
   - 提问者**未指定**版本 → 默认用最新版本（3.7），并标注版本信息

3. **文件内标注规范**：版本特定的工具/API/特性在文件内标注 `[v3.6]` / `[v3.7新增]` / `[v3.7变更]`

4. **适用范围**：此规则同样适用于未来出现的其他软件版本差异（QGIS、FME、SuperMap 等）

### 涉及文件

| 文件 | 版本 | 说明 |
|------|------|------|
| 12_ArcGIS_Pro.md | 3.6 主体 | 完整手册，所有内容默认适用 3.6 |
| 38_ArcGIS_Pro_3.7_新功能详解.md | 3.7 差异 | 仅记录新增/变更，不含 3.6 已有内容 |
| 13_QGIS.md | 3.40 | 如未来 QGIS 3.42 发布，新增 39号差异文件 |
| 15_SuperMap_GIS_2026.md | 2026 | 如未来 2027 发布，新增差异文件 |

---

## 文件完整性清单

| 编号 | 文件名 | 状态 | 行数 | 来源 |
|------|--------|------|------|------|
| SKILL.md | 总导航中枢 | ✅ V1.0重写 | ~550 | 8包交叉验证+结构重组 |
| **群组一：基础底座** | | | | |
| 01 | 基础理论与学科定位 | ✅ | 206 | 旧第一篇+新Part1.1 重组 |
| 02 | 坐标系统与投影 | ✅ | 276 | 旧第一/二/五篇 重组 |
| 03 | 数据模型与格式 | ✅ V1.0扩充 | 222→600+ | 新增云原生格式专节（GeoParquet/COG/PMTiles/Zarr/FlatGeobuf） |
| 04 | 中国三大坐标系实战 | ✅ | 135 | 旧第五篇 重组 |
| **群组二：标准与规范** | | | | |
| 05 | 国家测绘标准体系 | ✅ | 1,445 | V4.2深扩：15核心标准+决策树+区域差异 |
| 06 | 数据生产流程规范 | ✅ | 277 | 行业标准+研究数据 |
| 07 | 质量检查与验收标准 | ✅ | 895 | V4.2深扩：9大元素+自动化SOP+10案例库 |
| 08 | 成果汇交与归档规范 | ✅ | 236 | 行业标准+最佳实践 |
| 09 | 新型基础测绘实体规范 | ✅ | 194 | 旧第十四篇 |
| 10 | 测绘建库行业标准流程图集 | ✅ | 163 | Mermaid生成(7图) |
| **群组三：软件工具** | | | | |
| 12 | ArcGIS Pro [v3.6] | ✅ | 2,086 | 旧第七~十二篇+V4.2版本差异指引 |
| 13 | QGIS | ✅ V1.0重写 | 473→3,000+ | PyQGIS完整教材（5类19技能+200+算法ID）source: QGIS-Claude-Skill-Package |
| 14 | CASS 11.0 | ✅ | 687 | 旧第三/四/六/十七篇 |
| 15 | iData 数据工厂 | ✅ | 266 | V4.0加深：质检引擎+入库方案+三维采编 |
| 16 | SuperMap iDesktopX | ✅ | 479 | V4.0加深：大数据分布式+AgentX实战 |
| 17 | GlobalMapper | ✅ | 560 | V4.0加深：GMScript+Python集成+LiDAR深度 |
| 18 | FME Form与Flow | ✅ | 464 | V4.0深度：REST API V4+Automations+性能11招 |
| 19 | 多源数据融合 | ✅ | 872 | V4.1激活：坐标统一/ICP配准/三维互转/深度学习融合 |
| 20 | GIS资源共享 | ✅ | 257 | V4.2激活：数据源/WMS-WMTS/API/开源SHP/学习社区 |
| 36 | LiDAR360 点云处理软件 | ✅ 归组 | 567 | PTD vs CSF深度避坑/32类AI分类 |
| 38 | ArcGIS Pro 3.7 新功能详解 | ✅ 归组 [v3.7新增] | 1,078 | Esri官方文档完整提取 |
| **群组四：开发与自动化** | | | | |
| 21 | Python GIS生态 | ✅ V1.0扩充 | 250→800+ | 新增DuckDB Spatial/Sedona/PDAL |
| 22 | 空间数据库 | ✅ | 302 | 旧第十一篇 |
| 23 | WebGIS开发 | ✅ V1.0扩充 | 832→1,200+ | 新增PMTiles部署全指南 |
| 24 | 遥感与GEE | ✅ | 746 | V4.1加深：多传感器指数速查 |
| 25 | 三维GIS与数字孪生 | ✅ | 2,124 | V4.1全面重写 |
| 26 | WorkBuddyGIS AddIn开发 | ✅ | 938 | V4.1大幅扩充 |
| 27 | AI GIS | ✅ V1.0激活 | 403 | GeoAI/DL/SAM/LangSAM/GIS LLM |
| 35 | 专家级批量处理与自动化 | ✅ 归组 | 556 | CSDN/GitHub/官方文档收录 |
| **群组五：实战与避坑** | | | | |
| 28 | 项目案例集 | ✅ V1.0扩充 | 433→800+ | 新增光纤故障预测+气候脆弱性评估2案例 |
| 29 | 避坑库 | ✅ V1.0重命名 | 1,555 | V1.0新增结构化反模式（WRONG/CORRECT/WHY格式） |
| 30 | GIS↔CAD数据转换 | ✅ | 821 | 旧第十七篇(核心) |
| 32 | GNSS测量与工程应用 | ✅ | 330 | 旧第二十一篇 |
| 33 | 空间分析与统计 | ✅ | 668 | V4.1加深：可执行代码集 |
| **群组六：现代GIS技术栈** | | | | |
| 39 | R语言GIS生态 | 🆕 V1.0新建 | 1,549 | source: Geospatial-Analysis-Portfolio + 社区资源 |
| 40 | OGC国际标准速查手册 | 🆕 V1.0新建 | 1,646 | source: open-gis-main + awesome-gis |
| 41 | 现代GIS数据处理管道 | 🆕 V1.0新建 | 1,471 | source: open-gis-main 7种管道+验证清单 |
| 42 | 多语言地理空间库生态 | 🆕 V1.0新建 | 1,167 | source: opengis-skills-main 几何引擎链 |
| 43 | 格式选择决策树与反模式 | 🆕 V1.0新建 | 1,308 | source: open-gis-main 12反模式+QGIS反模式 |
| 44 | QGIS Processing算法速查手册 | 🆕 V1.0新建 | 961 | source: QGIS-Claude-Skill-Package 50+算法ID |
| 45 | GIS Agent技能设计范式 | 🆕 V1.0新建 | 1,442 | source: gis-agent-skills + gisdataagent |
| **群组七：自进化机制** | | | | |
| 37 | 自进化反馈机制 | ✅ | 406 | V4.1增强：WPS算法+FQS评分+增强阈值 |
| **独立附录** | | | | |
| 31 | 学习路径与认证资源 | ✅ 迁出 | 162 | 全资源链接+版本差异（独立于群组） |
| feedback/ | 自进化追踪目录 | ✅ | 4文件 | knowledge_gaps/feedback_log/revision_history/config |
| **统计** | **45文件（含feedback）** | **✅ 45活跃+feedback** | **~33,000行** | **V1.0七群组+8包交叉验证+新增7模块(9,544行)** |

---

> **V1.0 结构重组成果**：
> - 删除3空占位（11/20移动采集/34）| 20号身份统一 | 27号激活 | 游离文件归组（35/36/38）
> - 29号去数字后缀 | 31号独立附录 | 群组七新增（39-45）
> - 知识库规模：40文件~23,000行 → 45文件~33,000行（群组六新增7模块共9,544行）


<!-- wm:坤图_GIS:V1.0 -->
