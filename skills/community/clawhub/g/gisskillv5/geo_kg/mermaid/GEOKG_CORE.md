<!-- wm:坤图_GIS:V5.0 -->

# GeoKG 地理知识图谱核心关联图

> 全局唯一知识ID: GIS-KG-MERMAID-001
> 版本: V5.0
> 关联模块: 全部知识群组
> 风险等级: 低

---

## 一、总览：五大实体域全关联图

```mermaid
graph TB
    subgraph 坐标系域["坐标系域 (CRS)"]
        CGCS2000["CGCS2000\nGIS-KG-CRS-001"]
        WGS84["WGS84\nGIS-KG-CRS-002"]
        BJ54["北京54\nGIS-KG-CRS-003"]
        XA80["西安80\nGIS-KG-CRS-004"]
        LOCAL["地方独立坐标系\nGIS-KG-CRS-005"]
    end

    subgraph 软件域["软件域 (SW)"]
        ArcGIS["ArcGIS Pro\nGIS-KG-SW-001"]
        QGIS["QGIS\nGIS-KG-SW-002"]
        CASS["CASS\nGIS-KG-SW-003"]
        SuperMap["SuperMap\nGIS-KG-SW-004"]
        FME["FME\nGIS-KG-SW-005"]
        LiDAR["LiDAR360\nGIS-KG-SW-006"]
        GlobalM["GlobalMapper\nGIS-KG-SW-007"]
        iData["iData\nGIS-KG-SW-008"]
        MapGIS["MapGIS\nGIS-KG-SW-009"]
    end

    subgraph 标准域["标准域 (STD)"]
        GBT["GB/T国标\nGIS-KG-STD-001"]
        CHT["CH/T行标\nGIS-KG-STD-002"]
        OGC["OGC国际\nGIS-KG-STD-003"]
        LOCAL_STD["地方测绘规范\nGIS-KG-STD-004"]
    end

    subgraph 格式域["格式域 (FMT)"]
        VECTOR["矢量格式\nGIS-KG-FMT-001"]
        RASTER["栅格格式\nGIS-KG-FMT-002"]
        POINTCLOUD["点云格式\nGIS-KG-FMT-003"]
        THREED["三维格式\nGIS-KG-FMT-004"]
        TIMESERIES["时序格式\nGIS-KG-FMT-005"]
    end

    subgraph 算法域["算法域 (ALG)"]
        TRANSFORM["坐标转换\nGIS-KG-ALG-001"]
        TOPO["拓扑修复\nGIS-KG-ALG-002"]
        SPATIAL["空间分析\nGIS-KG-ALG-003"]
        DL["深度学习\nGIS-KG-ALG-004"]
        INTERP["插值算法\nGIS-KG-ALG-005"]
    end

    %% 坐标系 ↔ 软件
    CGCS2000 -->|"法定基准"| ArcGIS
    CGCS2000 -->|"法定基准"| QGIS
    CGCS2000 -->|"法定基准"| CASS
    CGCS2000 -->|"法定基准"| SuperMap
    CGCS2000 -->|"法定基准"| MapGIS
    WGS84 -->|"GPS基准"| ArcGIS
    WGS84 -->|"GPS基准"| QGIS
    BJ54 -->|"历史兼容"| CASS
    XA80 -->|"历史兼容"| CASS

    %% 坐标系 ↔ 标准
    CGCS2000 -->|"GB/T 39612-2020"| GBT
    CGCS2000 -->|"自然资源规范"| CHT

    %% 软件 ↔ 格式
    ArcGIS --> VECTOR
    ArcGIS --> RASTER
    ArcGIS --> THREED
    QGIS --> VECTOR
    QGIS --> RASTER
    QGIS --> POINTCLOUD
    FME --> VECTOR
    FME --> RASTER
    FME --> THREED
    LiDAR --> POINTCLOUD
    LiDAR --> THREED

    %% 标准 ↔ 软件
    GBT -->|"质检依据"| ArcGIS
    GBT -->|"质检依据"| QGIS
    CHT -->|"生产规范"| CASS
    OGC -->|"Web服务"| QGIS
    OGC -->|"Web服务"| ArcGIS

    %% 算法 ↔ 软件
    TRANSFORM -->|"ArcPy实现"| ArcGIS
    TRANSFORM -->|"PyQGIS实现"| QGIS
    TOPO -->|"拓扑引擎"| ArcGIS
    DL -->|"SAM/UNet"| ArcGIS
    DL -->|"GEE"| QGIS
```

## 二、坐标系统知识域深层关联

```mermaid
graph LR
    subgraph CRS_KNOWLEDGE["坐标系知识域"]
        K02["02_坐标系统与投影\nGIS-KB-01-020"]
        K04["04_中国三大坐标系实战\nGIS-KB-01-040"]
        K32["32_GNSS测量\nGIS-KB-05-320"]
        K02EXP["V5扩展: 坐标系码表\nGIS-KB-01-02E"]
        K04EXP["V5扩展: 地方坐标\nGIS-KB-01-04E"]
    end

    K02 <-->|"双向引用"| K04
    K02 -->|"WGS84↔CGCS2000"| K32
    K02EXP -->|"扩充EPSG全集"| K02
    K02EXP -->|"扩充中央子午线"| K02
    K04EXP -->|"扩充七/四/三参数"| K04
    K04EXP -->|"扩充北斗RTK"| K32
    K04 -->|"坐标系选择"| K06["06_数据生产流程\nGIS-KB-02-060"]
    K02 -->|"投影方法"| K03["03_数据模型\nGIS-KB-01-030"]
```

## 三、标准规范知识域链路

```mermaid
graph TB
    subgraph STD_CHAIN["标准规范链路"]
        K05["05_国标体系\nGIS-KB-02-050"]
        K06["06_数据生产流程\nGIS-KB-02-060"]
        K07["07_质量检查\nGIS-KB-02-070"]
        K08["08_成果汇交\nGIS-KB-02-080"]
        K09["09_新型基础测绘\nGIS-KB-02-090"]
        K10["10_流程图集\nGIS-KB-02-100"]
        K40["40_OGC标准\nGIS-KB-06-400"]
    end

    K05 -->|"引用标准号"| K06
    K05 -->|"引用标准号"| K07
    K06 -->|"生产→质检"| K07
    K07 -->|"质检→汇交"| K08
    K09 -->|"新标准体系"| K05
    K05 <-->|"国标↔OGC映射"| K40
    K10 -->|"流程图依据"| K06
    K10 -->|"流程图依据"| K07
    K10 -->|"流程图依据"| K08
```

## 四、软件互操作知识域

```mermaid
graph TB
    subgraph SW_INTEROP["软件互操作域"]
        K12["12_ArcGIS Pro v3.6\nGIS-KB-03-120"]
        K13["13_QGIS 3.40LTR\nGIS-KB-03-130"]
        K14["14_CASS 11.0\nGIS-KB-03-140"]
        K15["15_iData\nGIS-KB-03-150"]
        K16["16_SuperMap 2026\nGIS-KB-03-160"]
        K17["17_GlobalMapper v26\nGIS-KB-03-170"]
        K18["18_FME 2025\nGIS-KB-03-180"]
        K19["19_多源融合\nGIS-KB-03-190"]
        K36["36_LiDAR360 V9\nGIS-KB-03-360"]
        K38["38_ArcGIS Pro 3.7\nGIS-KB-03-380"]
        MAPGIS["MapGIS 10.7\nGIS-KB-03-MG"]
    end

    K12 <-->|"功能对标"| K13
    K12 <-->|"版本双轨"| K38
    K14 -->|"CASS→GDB"| K12
    K14 <-->|"南方数码协同"| K15
    K17 <-->|"万能转换互补"| K18
    K19 -->|"坐标统一"| K12
    K19 -->|"点云配准"| K36
    MAPGIS <-->|"国产对标"| K16
    MAPGIS <-->|"国产对标"| CASS["南方系"]
```

## 五、AI与智能体知识域

```mermaid
graph LR
    subgraph AI_DOMAIN["AI智能体域"]
        K27["27_AI_GIS\nGIS-KB-04-270"]
        K27EXP["V5扩展: GeoAI工程化\nGIS-KB-04-27E"]
        K45["45_Agent范式\nGIS-KB-06-450"]
        AGENT["agents/orchestrator\nAGENT_ENGINE.py"]
    end

    K27 -->|"SAM/遥感/GIS LLM"| K27EXP
    K27EXP -->|"LangSAM+本地RAG"| K45
    K45 -->|"范式实现"| AGENT
    AGENT -->|"5类Agent调度"| K27
```

## 六、自进化闭环

```mermaid
graph TB
    subgraph EVO["GeoEvolve自进化闭环"]
        FEEDBACK["反馈采集层\n采集用户反馈+报错"]
        CRAWLER["情报抓取层\n国标/软件/OGC监控"]
        FIXER["知识修正层\nLLM校验+补全"]
        REBUILD["索引重建层\n向量+图谱增量刷新"]
        MONITOR["监控看板\n4指标量化"]
    end

    FEEDBACK -->|"知识缺口"| FIXER
    CRAWLER -->|"版本更新"| FIXER
    FIXER -->|"增量包"| REBUILD
    REBUILD -->|"状态回写"| MONITOR
    MONITOR -->|"触发"| FEEDBACK
    MONITOR -->|"触发"| CRAWLER
```

---

<!-- wm:坤图_GIS:V5.0 -->
