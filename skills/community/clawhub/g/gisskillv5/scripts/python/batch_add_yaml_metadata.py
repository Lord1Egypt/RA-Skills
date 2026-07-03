<!-- wm:坤图_GIS:V5.0 -->
#!/usr/bin/env python3
"""
GIS_SKILL V5.0 批量YAML元数据头注入脚本
为所有43个reference文件添加标准化YAML frontmatter
"""
import os
import re
from datetime import datetime

# 全局知识ID映射 (knowledge_id -> metadata)
KNOWLEDGE_MAP = {
    # 群组一：基础底座
    "01_基础理论与学科定位.md": {
        "knowledge_id": "GIS-KB-G01-001",
        "group": 1,
        "group_name": "基础底座",
        "category": "theory",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["GIS定义", "学科定位", "发展历程", "系统组成", "地理本体论", "时空GIS", "数字孪生", "测绘保密"],
        "related_modules": ["02_坐标系统与投影.md", "03_数据模型与格式.md"],
        "risk_level": "low",
        "update_cycle": "annual",
    },
    "02_坐标系统与投影.md": {
        "knowledge_id": "GIS-KB-G01-002",
        "group": 1,
        "group_name": "基础底座",
        "category": "theory",
        "gb_standards": ["GB/T 35644-2017"],
        "software_versions": [],
        "keywords": ["椭球体", "基准面", "GCS", "PCS", "高斯-克吕格", "UTM", "CGCS2000", "EPSG", "WKID", "3度带", "6度带", "中央子午线", "投影", "大地水准面"],
        "related_modules": ["04_中国三大坐标系实战.md", "32_GNSS测量与工程应用.md", "05_国家测绘标准体系.md"],
        "risk_level": "high",
        "update_cycle": "annual",
    },
    "03_数据模型与格式.md": {
        "knowledge_id": "GIS-KB-G01-003",
        "group": 1,
        "group_name": "基础底座",
        "category": "theory",
        "gb_standards": ["GB/T 30319-2013"],
        "software_versions": [],
        "keywords": ["矢量", "栅格", "TIN", "点云", "GeoParquet", "COG", "PMTiles", "Zarr", "GeoArrow", "COPC", "3DTiles", "CityGML", "I3S", "STAC", "FlatGeobuf"],
        "related_modules": ["30_GIS↔CAD数据转换.md", "25_三维GIS与数字孪生.md", "43_格式选择决策树与反模式.md"],
        "risk_level": "medium",
        "update_cycle": "annual",
    },
    "04_中国三大坐标系实战.md": {
        "knowledge_id": "GIS-KB-G01-004",
        "group": 1,
        "group_name": "基础底座",
        "category": "theory",
        "gb_standards": ["GB/T 35644-2017"],
        "software_versions": [],
        "keywords": ["北京54", "西安80", "CGCS2000", "七参数", "四参数", "三参数", "坐标转换", "地方独立坐标系", "北斗", "RTK", "高程异常"],
        "related_modules": ["02_坐标系统与投影.md", "32_GNSS测量与工程应用.md", "06_数据生产流程规范.md"],
        "risk_level": "high",
        "update_cycle": "annual",
    },
    # 群组二：标准与规范
    "05_国家测绘标准体系.md": {
        "knowledge_id": "GIS-KB-G02-001",
        "group": 2,
        "group_name": "标准与规范",
        "category": "standards",
        "gb_standards": ["GB/T 13923", "GB/T 20257", "GB/T 20258", "GB/T 18316", "GB/T 24356", "GB/T 33176", "CH/T系列"],
        "software_versions": [],
        "keywords": ["GB/T", "CH/T", "测绘标准", "标准编号速查", "国标", "OGC映射", "地方规范", "新型基础测绘", "实景三维"],
        "related_modules": ["06_数据生产流程规范.md", "07_质量检查与验收标准.md", "40_OGC国际标准速查手册.md"],
        "risk_level": "high",
        "update_cycle": "quarterly",
    },
    "06_数据生产流程规范.md": {
        "knowledge_id": "GIS-KB-G02-002",
        "group": 2,
        "group_name": "标准与规范",
        "category": "standards",
        "gb_standards": ["GB/T 18316", "GB/T 20258"],
        "software_versions": [],
        "keywords": ["DLG", "DEM", "DOM", "DSM", "SOP", "生产流程", "航测", "实景三维", "点云", "管网BIM"],
        "related_modules": ["05_国家测绘标准体系.md", "07_质量检查与验收标准.md", "08_成果汇交与归档规范.md"],
        "risk_level": "high",
        "update_cycle": "annual",
    },
    "07_质量检查与验收标准.md": {
        "knowledge_id": "GIS-KB-G02-003",
        "group": 2,
        "group_name": "标准与规范",
        "category": "standards",
        "gb_standards": ["GB/T 24356", "GB/T 33176", "GB/T 39610"],
        "software_versions": [],
        "keywords": ["二级检查", "一级验收", "质量元素", "质量评定", "抽样方案", "质检自动化", "实景三维质检", "点云质检"],
        "related_modules": ["06_数据生产流程规范.md", "08_成果汇交与归档规范.md"],
        "risk_level": "high",
        "update_cycle": "annual",
    },
    "08_成果汇交与归档规范.md": {
        "knowledge_id": "GIS-KB-G02-004",
        "group": 2,
        "group_name": "标准与规范",
        "category": "standards",
        "gb_standards": ["CH/T 1007"],
        "software_versions": [],
        "keywords": ["成果汇交", "命名规则", "图幅编号", "元数据", "归档", "加密"],
        "related_modules": ["07_质量检查与验收标准.md", "28_项目案例集.md"],
        "risk_level": "medium",
        "update_cycle": "annual",
    },
    "09_新型基础测绘实体规范.md": {
        "knowledge_id": "GIS-KB-G02-005",
        "group": 2,
        "group_name": "标准与规范",
        "category": "standards",
        "gb_standards": ["新型基础测绘系列标准"],
        "software_versions": [],
        "keywords": ["地理实体", "实景三维", "17级网格", "空间身份编码", "时序更新", "实体关联", "语义化", "多尺度表达"],
        "related_modules": ["05_国家测绘标准体系.md", "25_三维GIS与数字孪生.md"],
        "risk_level": "high",
        "update_cycle": "quarterly",
    },
    "10_测绘建库行业标准流程图集.md": {
        "knowledge_id": "GIS-KB-G02-006",
        "group": 2,
        "group_name": "标准与规范",
        "category": "standards",
        "gb_standards": ["多国标综合"],
        "software_versions": [],
        "keywords": ["Mermaid", "流程图", "建库流程", "国土空间", "地籍", "管线", "林业", "生态"],
        "related_modules": ["06_数据生产流程规范.md", "07_质量检查与验收标准.md", "08_成果汇交与归档规范.md"],
        "risk_level": "medium",
        "update_cycle": "annual",
    },
    # 群组三：软件工具
    "12_ArcGIS_Pro.md": {
        "knowledge_id": "GIS-KB-G03-001",
        "group": 3,
        "group_name": "软件工具",
        "category": "software",
        "gb_standards": [],
        "software_versions": ["ArcGIS Pro 3.6"],
        "keywords": ["ArcGIS Pro", "ArcPy", "ModelBuilder", "GDB", "拓扑", "属性域", "地图系列", "扩展模块"],
        "related_modules": ["13_QGIS.md", "38_ArcGIS_Pro_3.7_新功能详解.md", "26_WorkBuddyGIS_AddIn开发.md"],
        "risk_level": "high",
        "update_cycle": "biannual",
    },
    "13_QGIS.md": {
        "knowledge_id": "GIS-KB-G03-002",
        "group": 3,
        "group_name": "软件工具",
        "category": "software",
        "gb_standards": [],
        "software_versions": ["QGIS 3.40 LTR"],
        "keywords": ["QGIS", "PyQGIS", "Processing", "GRASS", "SAGA", "QGIS Server", "矢量瓦片", "COG"],
        "related_modules": ["12_ArcGIS_Pro.md", "44_QGIS_Processing算法速查手册.md", "23_WebGIS开发.md"],
        "risk_level": "high",
        "update_cycle": "biannual",
    },
    "14_CASS11.0.md": {
        "knowledge_id": "GIS-KB-G03-003",
        "group": 3,
        "group_name": "软件工具",
        "category": "software",
        "gb_standards": [],
        "software_versions": ["CASS 11.0"],
        "keywords": ["CASS", "南方数码", "编码", "XDATA", "SOUTH", "CGCS2000", "三维测图", "新型基础测绘"],
        "related_modules": ["15_iData_数据工厂.md", "30_GIS↔CAD数据转换.md", "12_ArcGIS_Pro.md"],
        "risk_level": "high",
        "update_cycle": "biannual",
    },
    "15_iData_数据工厂.md": {
        "knowledge_id": "GIS-KB-G03-004",
        "group": 3,
        "group_name": "软件工具",
        "category": "software",
        "gb_standards": [],
        "software_versions": ["iData 4.x"],
        "keywords": ["iData", "数据工厂", "南方数码", "质检引擎", "一体化生产", "三维采编"],
        "related_modules": ["14_CASS11.0.md", "06_数据生产流程规范.md"],
        "risk_level": "medium",
        "update_cycle": "biannual",
    },
    "16_SuperMap_iDesktopX.md": {
        "knowledge_id": "GIS-KB-G03-005",
        "group": 3,
        "group_name": "软件工具",
        "category": "software",
        "gb_standards": [],
        "software_versions": ["SuperMap GIS 2026"],
        "keywords": ["SuperMap", "超图", "iDesktopX", "AgentX", "空间智能体", "分布式", "鸿蒙", "ClientX"],
        "related_modules": ["12_ArcGIS_Pro.md", "23_WebGIS开发.md", "25_三维GIS与数字孪生.md"],
        "risk_level": "high",
        "update_cycle": "annual",
    },
    "17_GlobalMapper.md": {
        "knowledge_id": "GIS-KB-G03-006",
        "group": 3,
        "group_name": "软件工具",
        "category": "software",
        "gb_standards": [],
        "software_versions": ["GlobalMapper v26.2"],
        "keywords": ["GlobalMapper", "LiDAR", "地形分析", "GMScript", "格式转换", "Python"],
        "related_modules": ["18_FME_Form与Flow.md", "36_LiDAR360_点云处理软件.md"],
        "risk_level": "medium",
        "update_cycle": "annual",
    },
    "18_FME_Form与Flow.md": {
        "knowledge_id": "GIS-KB-G03-007",
        "group": 3,
        "group_name": "软件工具",
        "category": "software",
        "gb_standards": [],
        "software_versions": ["FME 2025.1"],
        "keywords": ["FME", "ETL", "Workbench", "Transformer", "REST API", "Automations", "AI连接器"],
        "related_modules": ["17_GlobalMapper.md", "19_多源数据融合.md", "35_专家级批量处理与自动化实战指南.md"],
        "risk_level": "high",
        "update_cycle": "annual",
    },
    "19_多源数据融合.md": {
        "knowledge_id": "GIS-KB-G03-008",
        "group": 3,
        "group_name": "软件工具",
        "category": "software",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["坐标统一", "ICP配准", "多源融合", "CAD-GIS-BIM", "点云矢量配准", "三维格式互转"],
        "related_modules": ["04_中国三大坐标系实战.md", "25_三维GIS与数字孪生.md", "30_GIS↔CAD数据转换.md"],
        "risk_level": "high",
        "update_cycle": "annual",
    },
    "20_GIS资源共享.md": {
        "knowledge_id": "GIS-KB-G03-009",
        "group": 3,
        "group_name": "软件工具",
        "category": "software",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["数据源", "WMS", "WMTS", "API", "开源SHP", "学习社区", "矢量瓦片", "COG"],
        "related_modules": ["40_OGC国际标准速查手册.md", "23_WebGIS开发.md"],
        "risk_level": "low",
        "update_cycle": "quarterly",
    },
    "36_LiDAR360_点云处理软件.md": {
        "knowledge_id": "GIS-KB-G03-010",
        "group": 3,
        "group_name": "软件工具",
        "category": "software",
        "gb_standards": [],
        "software_versions": ["LiDAR360 V9.0"],
        "keywords": ["LiDAR360", "点云", "PTD", "CSF", "地面滤波", "AI分类", "林业", "电力", "单木提取"],
        "related_modules": ["25_三维GIS与数字孪生.md", "24_遥感与GEE.md"],
        "risk_level": "high",
        "update_cycle": "annual",
    },
    "38_ArcGIS_Pro_3.7_新功能详解.md": {
        "knowledge_id": "GIS-KB-G03-011",
        "group": 3,
        "group_name": "软件工具",
        "category": "software",
        "gb_standards": [],
        "software_versions": ["ArcGIS Pro 3.7(差异文档)"],
        "keywords": ["ArcGIS Pro 3.7", "File Knowledge Graph", "Embeddings", "Analyze Map", "Telecom"],
        "related_modules": ["12_ArcGIS_Pro.md"],
        "risk_level": "high",
        "update_cycle": "annual",
    },
    # 群组四：开发与自动化
    "21_Python_GIS生态.md": {
        "knowledge_id": "GIS-KB-G04-001",
        "group": 4,
        "group_name": "开发与自动化",
        "category": "development",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["GeoPandas", "Rasterio", "Shapely", "GDAL", "DuckDB", "PDAL", "Sedona", "PyProj", "Fiona"],
        "related_modules": ["39_R语言GIS生态.md", "22_空间数据库.md", "42_多语言地理空间库生态.md"],
        "risk_level": "high",
        "update_cycle": "quarterly",
    },
    "22_空间数据库.md": {
        "knowledge_id": "GIS-KB-G04-002",
        "group": 4,
        "group_name": "开发与自动化",
        "category": "development",
        "gb_standards": [],
        "software_versions": ["PostGIS 3.5"],
        "keywords": ["PostGIS", "GDB", "GeoPackage", "DuckDB", "TimescaleDB", "空间索引", "分布式"],
        "related_modules": ["21_Python_GIS生态.md", "23_WebGIS开发.md"],
        "risk_level": "high",
        "update_cycle": "annual",
    },
    "23_WebGIS开发.md": {
        "knowledge_id": "GIS-KB-G04-003",
        "group": 4,
        "group_name": "开发与自动化",
        "category": "development",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["Leaflet", "OpenLayers", "Cesium", "MapLibre", "PMTiles", "GeoServer", "矢量瓦片", "K8s"],
        "related_modules": ["25_三维GIS与数字孪生.md", "40_OGC国际标准速查手册.md", "41_现代GIS数据处理管道.md"],
        "risk_level": "high",
        "update_cycle": "quarterly",
    },
    "24_遥感与GEE.md": {
        "knowledge_id": "GIS-KB-G04-004",
        "group": 4,
        "group_name": "开发与自动化",
        "category": "development",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["Landsat", "Sentinel", "GEE", "NDVI", "NDWI", "NDBI", "随机森林", "土地利用", "变化检测"],
        "related_modules": ["27_AI_GIS.md", "25_三维GIS与数字孪生.md"],
        "risk_level": "high",
        "update_cycle": "annual",
    },
    "25_三维GIS与数字孪生.md": {
        "knowledge_id": "GIS-KB-G04-005",
        "group": 4,
        "group_name": "开发与自动化",
        "category": "development",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["倾斜摄影", "3DTiles", "单体化", "数字孪生", "BIM+GIS", "空三", "像控", "LOD", "Draco"],
        "related_modules": ["24_遥感与GEE.md", "23_WebGIS开发.md", "36_LiDAR360_点云处理软件.md"],
        "risk_level": "high",
        "update_cycle": "annual",
    },
    "26_WorkBuddyGIS_AddIn开发.md": {
        "knowledge_id": "GIS-KB-G04-006",
        "group": 4,
        "group_name": "开发与自动化",
        "category": "development",
        "gb_standards": [],
        "software_versions": ["ArcGIS Pro AddIn"],
        "keywords": ["ArcGIS Pro插件", "AddIn", "C#", "WPF", "开发经验", "IPC桥接"],
        "related_modules": ["12_ArcGIS_Pro.md"],
        "risk_level": "medium",
        "update_cycle": "annual",
    },
    "27_AI_GIS.md": {
        "knowledge_id": "GIS-KB-G04-007",
        "group": 4,
        "group_name": "开发与自动化",
        "category": "development",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["GeoAI", "深度学习", "SAM", "LangSAM", "空间大模型", "LLM", "RAG", "遥感解译", "提示词工程"],
        "related_modules": ["24_遥感与GEE.md", "45_GIS_Agent技能设计范式.md", "41_现代GIS数据处理管道.md"],
        "risk_level": "high",
        "update_cycle": "quarterly",
    },
    "35_专家级批量处理与自动化实战指南.md": {
        "knowledge_id": "GIS-KB-G04-008",
        "group": 4,
        "group_name": "开发与自动化",
        "category": "development",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["批量处理", "ArcPy性能", "FME调优", "QGIS Processing", "GDAL", "分布式调度"],
        "related_modules": ["41_现代GIS数据处理管道.md", "44_QGIS_Processing算法速查手册.md"],
        "risk_level": "high",
        "update_cycle": "annual",
    },
    "39_R语言GIS生态.md": {
        "knowledge_id": "GIS-KB-G04-009",
        "group": 4,
        "group_name": "开发与自动化",
        "category": "development",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["terra", "sf", "tmap", "leaflet", "R+GIS", "气候模拟", "空间统计", "地统计插值"],
        "related_modules": ["21_Python_GIS生态.md", "33_空间分析与统计.md", "42_多语言地理空间库生态.md"],
        "risk_level": "medium",
        "update_cycle": "annual",
    },
    # 群组五：实战与避坑
    "28_项目案例集.md": {
        "knowledge_id": "GIS-KB-G05-001",
        "group": 5,
        "group_name": "实战与避坑",
        "category": "practice",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["行业案例", "城市规划", "国土", "遥感", "地籍", "管线", "选址", "航测", "不动产"],
        "related_modules": ["06_数据生产流程规范.md", "07_质量检查与验收标准.md", "29_避坑库.md"],
        "risk_level": "medium",
        "update_cycle": "annual",
    },
    "29_避坑库.md": {
        "knowledge_id": "GIS-KB-G05-002",
        "group": 5,
        "group_name": "实战与避坑",
        "category": "practice",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["WRONG", "CAUSE", "SOLUTION", "CODE", "反模式", "报错", "闪退", "ERROR 999999", "GDAL错误码"],
        "related_modules": ["全部"],
        "risk_level": "high",
        "update_cycle": "monthly",
    },
    "30_GIS↔CAD数据转换.md": {
        "knowledge_id": "GIS-KB-G05-003",
        "group": 5,
        "group_name": "实战与避坑",
        "category": "practice",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["CAD", "DWG", "DXF", "CASS编码", "XDATA", "四步探查法", "批量转换", "BIM", "Revit"],
        "related_modules": ["14_CASS11.0.md", "03_数据模型与格式.md", "19_多源数据融合.md"],
        "risk_level": "high",
        "update_cycle": "annual",
    },
    "32_GNSS测量与工程应用.md": {
        "knowledge_id": "GIS-KB-G05-004",
        "group": 5,
        "group_name": "实战与避坑",
        "category": "practice",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["RTK", "PPK", "CORS", "NTRIP", "高程拟合", "BDS+GPS", "静态控制网", "平差"],
        "related_modules": ["02_坐标系统与投影.md", "04_中国三大坐标系实战.md"],
        "risk_level": "high",
        "update_cycle": "annual",
    },
    "33_空间分析与统计.md": {
        "knowledge_id": "GIS-KB-G05-005",
        "group": 5,
        "group_name": "实战与避坑",
        "category": "practice",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["Moran", "GWR", "Kriging", "IDW", "DBSCAN", "热点分析", "空间插值", "时空序列"],
        "related_modules": ["21_Python_GIS生态.md", "39_R语言GIS生态.md"],
        "risk_level": "high",
        "update_cycle": "annual",
    },
    # 群组六：现代GIS技术栈
    "40_OGC国际标准速查手册.md": {
        "knowledge_id": "GIS-KB-G06-001",
        "group": 6,
        "group_name": "现代GIS技术栈",
        "category": "modern",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["OGC", "WMS", "WFS", "WMTS", "OGC API", "STAC", "COPC", "GeoParquet", "CityGML 3.0"],
        "related_modules": ["05_国家测绘标准体系.md", "23_WebGIS开发.md", "43_格式选择决策树与反模式.md"],
        "risk_level": "medium",
        "update_cycle": "quarterly",
    },
    "41_现代GIS数据处理管道.md": {
        "knowledge_id": "GIS-KB-G06-002",
        "group": 6,
        "group_name": "现代GIS技术栈",
        "category": "modern",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["ETL", "管道", "云原生", "容器化", "可复现", "增量更新", "分布式", "Docker", "K8s"],
        "related_modules": ["35_专家级批量处理与自动化实战指南.md", "23_WebGIS开发.md", "45_GIS_Agent技能设计范式.md"],
        "risk_level": "medium",
        "update_cycle": "quarterly",
    },
    "42_多语言地理空间库生态.md": {
        "knowledge_id": "GIS-KB-G06-003",
        "group": 6,
        "group_name": "现代GIS技术栈",
        "category": "modern",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["JTS", "GEOS", "Shapely", "NTS", "几何引擎", "跨语言", "C++", "Java", "Go", "JS"],
        "related_modules": ["21_Python_GIS生态.md", "39_R语言GIS生态.md"],
        "risk_level": "medium",
        "update_cycle": "annual",
    },
    "43_格式选择决策树与反模式.md": {
        "knowledge_id": "GIS-KB-G06-004",
        "group": 6,
        "group_name": "现代GIS技术栈",
        "category": "modern",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["Shapefile弃用", "GeoParquet", "FlatGeobuf", "COG", "PMTiles", "格式矩阵", "决策树"],
        "related_modules": ["03_数据模型与格式.md", "40_OGC国际标准速查手册.md"],
        "risk_level": "medium",
        "update_cycle": "quarterly",
    },
    "44_QGIS_Processing算法速查手册.md": {
        "knowledge_id": "GIS-KB-G06-005",
        "group": 6,
        "group_name": "现代GIS技术栈",
        "category": "modern",
        "gb_standards": [],
        "software_versions": ["QGIS 3.40"],
        "keywords": ["Processing", "算法ID", "QGIS", "批量调用", "参数", "性能优化", "陷阱"],
        "related_modules": ["13_QGIS.md", "35_专家级批量处理与自动化实战指南.md"],
        "risk_level": "medium",
        "update_cycle": "annual",
    },
    "45_GIS_Agent技能设计范式.md": {
        "knowledge_id": "GIS-KB-G06-006",
        "group": 6,
        "group_name": "现代GIS技术栈",
        "category": "modern",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["Agent", "AI", "GIS Agent", "提示词", "多智能体", "编排", "协同", "评估框架"],
        "related_modules": ["27_AI_GIS.md", "37_自进化反馈机制.md", "41_现代GIS数据处理管道.md"],
        "risk_level": "high",
        "update_cycle": "quarterly",
    },
    # 群组七：自进化机制
    "37_自进化反馈机制.md": {
        "knowledge_id": "GIS-KB-G07-001",
        "group": 7,
        "group_name": "自进化机制",
        "category": "evolution",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["反馈", "知识缺口", "增量搜索", "版本升级", "GeoEvolve", "自进化", "灰度发布"],
        "related_modules": ["29_避坑库.md", "05_国家测绘标准体系.md", "45_GIS_Agent技能设计范式.md"],
        "risk_level": "high",
        "update_cycle": "monthly",
    },
    # 独立附录
    "31_学习路径与认证资源.md": {
        "knowledge_id": "GIS-KB-APP-001",
        "group": 99,
        "group_name": "独立附录",
        "category": "appendix",
        "gb_standards": [],
        "software_versions": [],
        "keywords": ["学习路径", "认证", "培训", "考试", "职业发展", "ArcGIS认证", "GISP"],
        "related_modules": ["01_基础理论与学科定位.md"],
        "risk_level": "low",
        "update_cycle": "annual",
    },
}

def generate_yaml_frontmatter(meta):
    """生成YAML frontmatter字符串"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    yaml = "---\n"
    yaml += f"knowledge_id: {meta['knowledge_id']}\n"
    yaml += f"group: {meta['group']}\n"
    yaml += f"group_name: \"{meta['group_name']}\"\n"
    yaml += f"category: {meta['category']}\n"
    yaml += f"gb_standards: {meta['gb_standards']}\n"
    yaml += f"software_versions: {meta['software_versions']}\n"
    yaml += f"keywords: {meta['keywords']}\n"
    yaml += f"related_modules: {meta['related_modules']}\n"
    yaml += f"risk_level: {meta['risk_level']}\n"
    yaml += f"update_cycle: {meta['update_cycle']}\n"
    yaml += f"last_updated: \"{today}\"\n"
    yaml += f"version: \"V5.0\"\n"
    yaml += "---\n\n"
    return yaml

def add_yaml_to_file(filepath, meta):
    """为单个文件添加YAML frontmatter"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 如果已有YAML frontmatter，跳过
    if content.startswith('---'):
        print(f"  跳过(已有YAML): {os.path.basename(filepath)}")
        return False
    
    # 如果第一行是#标题，在标题前插入YAML
    yaml_header = generate_yaml_frontmatter(meta)
    new_content = yaml_header + content
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ 已添加YAML: {os.path.basename(filepath)}")
    return True

def main():
    ref_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "references")
    
    if not os.path.exists(ref_dir):
        print(f"错误：目录不存在 {ref_dir}")
        return
    
    success_count = 0
    skip_count = 0
    fail_count = 0
    
    for filename, meta in KNOWLEDGE_MAP.items():
        filepath = os.path.join(ref_dir, filename)
        if not os.path.exists(filepath):
            print(f"  ✗ 文件不存在: {filename}")
            fail_count += 1
            continue
        
        try:
            if add_yaml_to_file(filepath, meta):
                success_count += 1
            else:
                skip_count += 1
        except Exception as e:
            print(f"  ✗ 处理失败 {filename}: {e}")
            fail_count += 1
    
    print(f"\n=== 处理完成 ===")
    print(f"成功: {success_count} | 跳过: {skip_count} | 失败: {fail_count}")
    print(f"总计: {len(KNOWLEDGE_MAP)} 个文件")

if __name__ == "__main__":
    main()
