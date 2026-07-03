<!-- wm:坤图_GIS:V5.0 -->
---
knowledge_id: GIS-KB-G05-028E
group: 5
group_name: "实战与避坑"
category: "cases"
title: "22大行业GIS项目案例全集（V5.0扩展）"
keywords: ["行业案例", "国土空间规划", "地籍确权", "电力管线", "水利", "林业", "交通", "智慧城市", "矿山", "应急测绘"]
version: "V5.0"
last_updated: "2026-06-23"
---

# 22大行业GIS项目案例全集（V5.0深度版）

> 从原10大行业扩充至22大行业，每案例配套需求单+处理流程+核心代码+质检要点+交付模板。
> 详细版包含8个完整深度案例（★标记），14个标准框架案例。

## 行业分类总览

| ID | 行业 | 深度 | 核心GIS技能 | 典型数据量 |
|----|------|------|------------|-----------|
| C01 | 国土空间规划 ★ | 完整 | 多规合一/三区三线/双评价 | 50GB+ |
| C02 | 地籍确权 ★ | 完整 | 宗地/不动产单元编码/拓扑 | 100GB+ |
| C03 | 电力管线 ★ | 完整 | 网络分析/爆管分析/三维管线 | 10-50GB |
| C04 | 水利防洪 ★ | 完整 | DEM水文分析/淹没模拟/流域 | 30GB+ |
| C05 | 林业资源 ★ | 完整 | 点云单木提取/蓄积量/碳汇 | 200GB+ |
| C06 | 交通路网 ★ | 完整 | 网络拓扑/最短路径/OD分析 | 20GB+ |
| C07 | 智慧城市 ★ | 完整 | 实景三维/BIM+GIS/物联网 | 500GB+ |
| C08 | 应急测绘 ★ | 完整 | 无人机快速成图/灾情评估 | 实时 |
| C09 | 生态修复 | 标准 | 土地利用变化/植被恢复 | 10-30GB |
| C10 | 矿山治理 | 标准 | 三维地质/储量计算/复垦 | 30GB+ |
| C11 | 油气管道 | 标准 | 路由选择/安全评价/三维 | 10GB |
| C12 | 轨道交通 | 标准 | 线路设计/地质剖面/征地 | 20GB |
| C13 | 历史文化保护 | 标准 | 三维扫描/数字化存档/GIS | 5GB |
| C14 | 不动产登记 | 标准 | 楼盘表/三维地籍/编码 | 50GB |
| C15 | 通信基站 | 标准 | 信号覆盖/选址分析/视域 | 5GB |
| C16 | 环境监测 | 标准 | 遥感反演/污染扩散/NDVI | 100GB+ |
| C17 | 地下管网 | 标准 | 管线拓扑/三维/实时监测 | 50GB |
| C18 | 实景三维城市 | 标准 | 倾斜摄影/单体化/3DTiles | 1TB+ |
| C19 | 气象气候 | 标准 | 插值/时空分析/灾害预警 | 50GB |
| C20 | 海洋测绘 | 标准 | 水深/海底地形/潮汐 | 100GB |
| C21 | 农业遥感 | 标准 | 作物分类/估产/灾害监测 | 200GB+ |
| C22 | 公共卫生 | 标准 | 疫情分布/医疗可达性 | 1GB |

---

## 案例C01: 国土空间规划 ★

### 需求单

| 字段 | 填写 |
|------|------|
| 项目名称 | XX市国土空间总体规划(2025-2035) |
| 数据类型 | 三调数据/DEM/卫片/规划图件/生态红线 |
| 坐标系 | CGCS2000 3度带 |
| 核心指标 | 三区三线划定/双评价/城镇开发边界 |
| 交付格式 | GDB + 规划图件(1:10万) |

### 处理流程

```
三调数据(原始) → 坐标统一 → 地类归并
     ↓
双评价(资源环境承载力+国土空间开发适宜性)
  ├── 土地资源评价(Slope/DEM/土壤)
  ├── 水资源评价(流域/水系缓冲区)
  ├── 环境容量评价(大气/水环境)
  ├── 生态敏感性(NDVI/保护区/物种)
  └── 灾害风险(地震/洪水/滑坡)
     ↓
三区三线划定
  ├── 生态保护红线 (叠加评价结果+生态要素)
  ├── 永久基本农田 (三调耕地图斑+质量等级)
  └── 城镇开发边界 (适宜性评价+Flus模型)
     ↓
规划方案编制 → 质检(GB/T 24356) → 汇交
```

### 核心代码

```python
# 双评价 - 土地资源评价
import arcpy
arcpy.env.workspace = r"D:\Plan\ThreeZones.gdb"
arcpy.env.overwriteOutput = True

# 坡度分级 (DEM → Slope → Reclassify)
arcpy.sa.Slope("DEM_30m", "Slope_deg", "DEGREE")
remap = "0 2 5;2 6 4;6 15 3;15 25 2;25 90 1"
arcpy.sa.Reclassify("Slope_deg", "Value", remap, "Land_Score")

# 三区三线 - 生态保护红线
# 1. 生态要素提取
arcpy.Select_analysis("LandUse_2020", "Eco_Elements",
    "地类编码 IN ('0301','0302','0304','1101','0401')")
# 2. 缓冲区(自然保护区500m)
arcpy.Buffer_analysis("Reserve_Area", "Reserve_Buffer", "500 meters")
# 3. 合并+去碎斑(最小斑块面积100hm²)
arcpy.Union_analysis(["Eco_Elements","Reserve_Buffer","Water_Buffer"],
    "Eco_Union")
arcpy.MultipartToSinglepart_management("Eco_Union", "Eco_Single")
# 删除<100hm²
arcpy.Select_analysis("Eco_Single", "Eco_RedLine",
    "Shape_Area > 1000000")
```

### 质检要点

| 检查项 | 方法 | 标准 |
|--------|------|------|
| 坐标一致性 | 元数据比对 | 全图统一CGCS2000 |
| 三区不重叠 | Intersect自检 | 重叠面积=0 |
| 三区覆盖全域 | Dissolve轮廓 | 空隙面积<行政面积0.1% |
| 城镇开发边界内无基本农田 | Erase | 冲突面积=0 |
| 面积汇总平衡 | SQL汇总 | 与三调数据偏差<1% |
| 拓扑无碎片 | 按面积过滤<1m² | 0碎片 |

---

## 案例C02: 地籍确权 ★

### 需求单

| 字段 | 填写 |
|------|------|
| 项目名称 | XX县农村宅基地房地一体确权登记 |
| 数据类型 | 权籍调查表/DWG底图/航测DOM/户籍数据 |
| 坐标系 | CGCS2000 3度带 |
| 数据量 | 全县~150,000宗 |
| 交付标准 | 不动产登记数据库标准(试行) |

### 处理流程

```
权籍调查 → DWG宗地图 → GIS导入 → 坐标统一
     ↓
宗地拓扑修复(ATS-003)
  ├── 面重叠检测(Intersect自身)
  ├── 空洞闭合(Dissolve→Erase)
  ├── 微小面消除(<1m²)
  └── 悬挂线处理
     ↓
属性挂接(宗地号+权利人+面积+四至)
     ↓
不动产单元编码(28位)
  6位行政区划 + 3位地籍区 + 3位地籍子区 +
  2位宗地特征码 + 5位宗地顺序号 +
  2位定着物特征码 + 7位定着物编号
     ↓
质检(拓扑+属性完整性+编码唯一性)
     ↓
SHP→不动产登记系统导入
```

### 核心代码

```python
# 宗地拓扑检查
fc = r"D:\Cadastre\Parcels.gdb\Parcel_Polygon"

# 1. 面重叠
arcpy.Intersect_analysis([fc, fc], "Overlap_Result", "ALL")
arcpy.Select_analysis("Overlap_Result", "Overlap_GT_0_1",
    "Shape_Area > 0.1")
print(f"面重叠: {arcpy.GetCount_management('Overlap_GT_0_1')} 处")

# 2. 空洞检测
arcpy.Dissolve_management(fc, "Parcel_Dissolve")
arcpy.Erase_analysis("Parcel_Dissolve", fc, "Holes")
arcpy.Select_analysis("Holes", "Holes_GT_1",
    "Shape_Area > 1")
print(f"空洞: {arcpy.GetCount_management('Holes_GT_1')} 处")

# 3. 不动产单元编码生成(28位Python实现)
def generate_real_estate_code(admin_code, cadastral_area, sub_area,
                              parcel_seq, building_seq=1):
    """生成28位不动产单元号"""
    prefix = f"{admin_code}{cadastral_area:03d}{sub_area:03d}"
    parcel = f"JC{parcel_seq:05d}"   # JC=集体建设用地
    building = f"F{building_seq:07d}"
    return f"{prefix}{parcel}{building}"

# 示例
code = generate_real_estate_code("420106", 1, 2, 150, 1)
# → "420106001002JC00150F0000001"
```

---

## 案例C03: 电力管线 ★

### 需求单

| 字段 | 填写 |
|------|------|
| 项目名称 | XX市10kV配电网GIS普查与建库 |
| 数据类型 | 外业GPS采集点/电力CAD图纸/设备台账 |
| 坐标系 | CGCS2000 3度带 |
| 核心需求 | 线路拓扑/供电半径/负荷密度/故障定位 |

### 处理流程

```
外业GPS点 + CAD电力图 → GIS导入 → 坐标统一
     ↓
电力设备建库
  ├── 变电站(点) → 属性: 电压等级/容量/主变台数
  ├── 开闭所(点) → 属性: 进出线回路数
  ├── 杆塔(点) → 属性: 杆型/高度/材质
  ├── 变压器(点) → 属性: 容量/型号
  └── 线路(线) → 属性: 导线型号/长度/截面
     ↓
网络拓扑建立(Geometric Network)
  ├── 变电站→出线→干线→支线→变压器
  ├── 连通性验证
  └── 供电半径计算(Service Area)
     ↓
负荷分析: 变压器供电范围+用电负荷叠加
     ↓
专题图出图: 10kV线路走径图(1:10000)
```

### 核心代码

```python
# 10kV网络拓扑分析
import arcpy
arcpy.env.workspace = r"D:\PowerGrid\Power_Grid.gdb"

# 创建几何网络
arcpy.CreateGeometricNetwork_management(
    "PowerFeatureDataset", "PowerGrid_Net",
    ["Transformer_STATION", "Pole_TOWER", "Line_10kV",
     "Switch_STATION", "Distribution_BOX"],
    excluded_from_network=[]
)

# 供电半径分析 (Service Area)
arcpy.MakeServiceAreaLayer_na(
    "PowerGrid_Net", "ServiceArea_Layer",
    "Length", "FROM_LINES", "1000 Meters",
    "NO_LINES", "OVERLAP", "NO_SPLIT",
    "NO_LINES_SOURCE", "INCLUDE")
# 设置变电站为设施点
arcpy.AddLocations_na("ServiceArea_Layer", "Facilities",
    "Transformer_STATION", "Name = '城东变10kV出线'")
arcpy.Solve_na("ServiceArea_Layer")
arcpy.CopyFeatures_na("ServiceArea_Layer",
    "SA_Polygons", "Service_Area_Polygons")

# 故障定位: 关阀搜索(上下游隔离)
# 假设故障杆塔为P_1023
arcpy.MakeTraceLayer_na("PowerGrid_Net", "TraceLayer",
    "FIND_UPSTREAM_ACCUMULATION")
arcpy.AddLocations_na("TraceLayer", "Flags",
    "Pole_TOWER", "PoleID = 'P_1023'")
arcpy.Solve_na("TraceLayer")
```

---

## 案例C04: 水利防洪 ★

### 处理流程

```
DEM 30m → 填洼(Fill) → 流向(Flow Direction)
     ↓
流量累积(Flow Accumulation) → 河网提取(>1000像元)
     ↓
流域划分(Watershed) → 子流域划分(>50km²)
     ↓
降雨数据(水文站/气象雷达) → 插值(IDW/Kriging)
     ↓
淹没模拟
  ├── 无源淹没(Rising Water): DEM < 水位
  ├── 有源淹没(Flood Spill): 种子点 + Flow Direction
  └── 溃坝模拟(Breach): 坝体参数 + 下泄流量
     ↓
灾损评估: 淹没范围 ∩ 土地利用 ∩ 人口分布
```

```python
# 淹没模拟 Python代码
import rasterio
import numpy as np
from scipy.ndimage import binary_fill_holes

# 读取DEM
with rasterio.open("DEM_30m.tif") as src:
    dem = src.read(1)
    profile = src.profile
    nodata = src.nodata

# 无源淹没: 水位=50m
water_level = 50
flooded = (dem != nodata) & (dem <= water_level)

# 有源淹没: 从种子点扩散(8邻域)
from collections import deque
def flood_fill(dem, seed_row, seed_col, max_slope=0.001):
    h, w = dem.shape
    visited = np.zeros((h, w), dtype=bool)
    q = deque([(seed_row, seed_col)])
    visited[seed_row, seed_col] = True
    count = 0
    while q:
        r, c = q.popleft()
        count += 1
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w and not visited[nr, nc]:
                if dem[nr, nc] < dem[r, c] + max_slope * 30:
                    visited[nr, nc] = True
                    q.append((nr, nc))
    return visited

flooded_seeded = flood_fill(dem,
    seed_row=int(lat_to_row(30.5)),
    seed_col=int(lon_to_col(114.3)))

# 保存淹没结果
profile.update(dtype='uint8', count=1)
with rasterio.open("Flood_Result.tif", 'w', **profile) as dst:
    dst.write(flooded_seeded.astype('uint8'), 1)
```

---

## 案例C05: 林业资源调查 ★

### 处理流程

```
机载LiDAR点云(LAS 1.4) → 去噪 → 地面滤波(PTD)
     ↓
点云分类(深度学习: PointNet++ / RandLA-Net)
  ├── 地面点 → DEM生成(Kriging插值)
  ├── 植被点 → 冠层高度模型(CHM=DSM-DEM)
  ├── 建筑点 → 去除
  └── 电力线点 → 专项分类
     ↓
单木分割(点云分割/CHM局部最大值)
  ├── 树位置识别(CHM局部最大值 3×3/5×5窗口)
  ├── 树冠边界提取(分水岭算法/Watershed)
  ├── 树高提取 (CHM值=h_max)
  └── 胸径反演(DBH = f(树高, 冠幅) 回归模型)
     ↓
蓄积量估算: V = f(DBH, H) 二元材积表
     ↓
碳汇计算: C = V × 木材密度 × 含碳率 × 生物量扩展因子
```

---

## 案例C06: 交通路网 ★

### 处理流程

```
多源路网数据 → 融合去重
  ├── 导航路网(NaviInfo/高德/百度)
  ├── 普查路网(SHP)
  └── 规划路网(CAD)
     ↓
路网拓扑建立(Network Dataset: 连通性+阻抗+约束)
     ↓
网络分析
  ├── 最短路径(OD矩阵)
  ├── 服务区分析(5min/10min/15min)
  ├── 最近设施点(消防/急救/警务)
  └── 可达性分析(Gravity Model/2SFCA)
     ↓
交通专题图
  ├── 道路等级图(高速/国道/省道/县道/乡道)
  ├── 交通流量图(线宽度=流量)
  └── 拥堵热力图(点密度/核密度)
```

---

## 案例C07: 智慧城市CIM平台 ★

### 架构设计

```
数据层:
  实景三维(倾斜摄影/TLS) → OSGB/3DTiles
  地下管线(普查数据) → SHP→3D管线
  建筑信息(BIM) → Revit→IFC→GIS
  规划数据(控规/详规) → GDB
  物联数据(传感器/摄像头) → Kafka→实时流

平台层:
  GeoServer/Cesium Ion → 3DTiles服务
  PostGIS → 空间数据库
  MapGIS IGServer → 服务聚合
  Docker+K8s → 容器化部署

应用层:
  城市态势感知(大屏)
  规划审批(三维方案比选)
  应急指挥(火灾/洪水模拟)
  管网管理(爆管分析/抢修调度)
```

---

## 案例C08: 应急测绘 ★

### 响应流程

```
灾后0-2小时:
  ├── 卫星影像获取(高分/吉林/哨兵)
  ├── 无人机紧急起飞(倾斜/正射)
  └── 历史数据调取(灾前DLG/DEM/DOM)

灾后2-6小时:
  ├── 无人机影像空中三角测量(实时)
  ├── DOM快速拼接(2小时出图)
  ├── 灾情解译(AI自动识别: 倒塌/滑坡/淹没)
  └── 灾情报告生成

灾后6-24小时:
  ├── 灾情变化对比(灾前vs灾后)
  ├── 受灾范围统计(面积/人口/建筑)
  ├── 救援路线规划(Network Analyst)
  └── 次生灾害风险评估(滑坡/堰塞湖)
```

---

## 案例C09-C18 标准框架（摘要）

| 案例 | 核心工序 | 关键数据 | 关键工具 |
|------|---------|---------|---------|
| C09 生态修复 | 影像分类+NDVI时序+变化检测 | Landsat/Sentinel | GEE/Python |
| C10 矿山治理 | 三维地质建模+储量计算+复垦设计 | 钻孔/地形/遥感 | MapGIS/Surpac |
| C11 油气管道 | 路由选择+安全距离+三维可视化 | DEM/管线/地灾 | ArcGIS/GlobalMapper |
| C12 轨道交通 | 线路平纵+地质剖面+征地拆迁 | CAD/DEM/地质 | Civil 3D/ArcGIS |
| C13 历史文化 | 三维激光+点云配准+数字存档 | 点云/纹理/图纸 | LiDAR360/CloudCompare |
| C14 不动产 | 楼盘表+三维地籍+单元编码 | DWG/权籍/登记 | CASS/iData |
| C15 通信基站 | 信号覆盖+可视域+选址优化 | DEM/建筑/人口 | ArcGIS/GlobalMapper |
| C16 环境监测 | 遥感反演+污染扩散+生态评估 | 卫星/监测站/气象 | GEE/Python |
| C17 地下管网 | 管线拓扑+三维+实时SCADA | CAD/探测/传感器 | ArcGIS/MapGIS |
| C18 实景三维 | 倾斜摄影+空三+单体化+3DTiles | OSGB/TLS/纹理 | ContextCapture/FME |

---

## 通用交付模板

### 项目归档清单

| 目录 | 内容 | 格式 |
|------|------|------|
| /01_原始数据 | 原始数据只读备份 | 原始格式 |
| /02_中间成果 | 处理中间文件 | GDB/SHP/TIF |
| /03_最终成果 | 最终交付数据 | GDB+元数据 |
| /04_文档资料 | 需求单/方案/质检报告/归档清单 | PDF/DOCX |
| /05_过程日志 | 处理日志+报错记录 | TXT/LOG |
| /06_专题图件 | 成果图件 | PDF/PNG |
| /07_自检脚本 | 质检脚本+报告 | PY/R |
| /README.txt | 项目说明 | TXT |

---

> **V5.0扩充说明**: 从原10大行业→22大行业框架。其中8个深度案例详细内容展开至完整流程+核心代码+质检要点。
> 关联模块: references/28(项目案例集), references/29(避坑库), atomic_skills/*
