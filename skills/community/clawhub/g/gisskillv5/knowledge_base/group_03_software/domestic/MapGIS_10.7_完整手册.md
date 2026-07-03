<!-- wm:坤图_GIS:V5.0 -->
---
knowledge_id: GIS-KB-G03-012
group: 3
group_name: "软件工具"
category: "software"
title: "MapGIS 10.7 完整实操手册（国产GIS三大支柱之一）"
software_versions: ["MapGIS 10.7"]
gb_standards: []
keywords: ["MapGIS", "中地数码", "MapGIS IGServer", "国产GIS", "二三维一体化", "麒麟统信适配", "达梦数据库", "人大金仓"]
risk_level: "high"
version: "V5.0"
last_updated: "2026-06-23"
---

# MapGIS 10.7 完整实操手册（V5.0 新建）

> MapGIS由武汉中地数码科技有限公司开发，是中国最早（1991年）的国产GIS平台之一，
> 与SuperMap（超图）、南方CASS/iData并称中国GIS三大支柱。
> 本手册为V5.0全新独立文档，对标ArcGIS Pro、SuperMap iDesktopX、QGIS等竞品。

---

## 一、MapGIS产品体系全览

### 1.1 产品矩阵

| 产品 | 定位 | 对标产品 | 核心能力 |
|------|------|----------|----------|
| **MapGIS 10.7 Desktop** | 桌面GIS | ArcGIS Pro / QGIS | 数据管理/制图/分析 |
| **MapGIS IGServer** | 服务端GIS | ArcGIS Server / GeoServer | 地图发布/空间服务 |
| **MapGIS Mobile** | 移动GIS | ArcGIS Field Maps | 外业采集/GPS定位 |
| **MapGIS 3D Scene** | 三维数字孪生 | Cesium / ArcGIS Earth | 三维可视化/分析 |
| **MapGIS Objects SDK** | 二次开发 | ArcObjects / PyQGIS | .NET/Python/Java API |
| **MapGIS Cloud** | 云GIS平台 | ArcGIS Online | 资源共享/在线制图 |
| **MapGIS SDE** | 空间数据引擎 | ArcGIS SDE | 空间数据库中间件 |
| **MapGIS Workflow** | 流程引擎 | FME Server | 自动化ETL流水线 |

### 1.2 版本历史

| 版本 | 年份 | 里程碑 |
|------|------|--------|
| MapGIS 6.x | 2000s | DOS→Windows转型 |
| MapGIS 7.x | 2008-2012 | 组件化GIS、空间数据引擎 |
| MapGIS K9 | 2009 | SOA架构、分布式部署 |
| MapGIS 10 | 2014 | 云GIS、大数据、三维一体化 |
| MapGIS 10.3 | 2017 | 全空间智能GIS |
| MapGIS 10.5 | 2019 | 深度学习集成、BIM+GIS |
| **MapGIS 10.7** | **2023+** | 信创全栈适配、地质AI、实景三维 |

### 1.3 国产三大GIS对标矩阵

| 维度 | MapGIS 10.7 | SuperMap 2026 | 南方CASS/iData |
|------|------------|---------------|----------------|
| 核心优势 | 地质矿产 | 通用GIS+大数据 | 测绘建库 |
| 桌面平台 | Desktop | iDesktopX | CASS(基于CAD) |
| 服务端 | IGServer | iServer | 无 |
| 移动端 | Mobile | iMobile | 外业精灵 |
| 三维 | 3D Scene | 三维GIS | 三维测图 |
| 二次开发 | Objects SDK(.NET/Python/Java) | iObjects(.NET/Java/Python) | 无 |
| 国产OS | 麒麟/统信 √ | 麒麟/统信 √ | 仅Windows |
| 国产DB | 达梦/金仓 √ | 达梦/金仓 √ | 无 |
| 行业特色 | 地质/矿产/国土 | 智慧城市/BIM | 测绘/地籍 |

---

## 二、MapGIS核心功能速览

### 2.1 数据管理

| 功能 | MapGIS实现 | 与ArcGIS/SuperMap差异 |
|------|-----------|----------------------|
| 原生格式 | HDF(层级数据格式) | 封闭二进制，需专用API读写 |
| GDB兼容 | 读取ESRI GDB(有限) | 不支持GDB创建/编辑 |
| SHP兼容 | 完整读写SHP | 字段名限10字符(同ArcGIS) |
| GeoPackage | 支持读取 | 写入有限 |
| 空间数据库 | SDE → Oracle/达梦/金仓/PostgreSQL | ArcGIS SDE只支持商业DB |
| 栅格 | IMG/TIF/GRD | 多波段支持弱于ArcGIS |
| 大数据 | 分布式文件系统(DFS) | SuperMap iServer分布式更有优势 |

### 2.2 制图与符号化

```
MapGIS符号库体系 (.sym格式):
├── 地形图符号库 (GB/T 20257.1-4 全套)
│   ├── 1:500/1000/2000 大比例尺
│   ├── 1:5000/10000 中比例尺
│   └── 1:25000/50000/100000 小比例尺
├── 地质图符号库 (DZ/T 0179 全套)
│   ├── 地质体花纹(沉积岩/火成岩/变质岩)
│   ├── 构造符号(断层/褶皱/节理)
│   └── 矿产符号(矿种/规模/开采方式)
├── 管线符号库 (CJJ 61 全套)
│   ├── 给水/排水/燃气/热力/电力/通信
│   └── 管点(阀门/检查井/消防栓)
├── 土地利用符号库 (GB/T 21010)
│   ├── 农用地/建设用地/未利用地
│   └── 12大类+73小类
└── 规划符号库 (CJJ/T 85)
    ├── 用地分类(居住/商业/工业/绿地)
    └── 设施符号(学校/医院/市政)

制图能力比较:
  地图整饰: MapGIS(★★★) ArcGIS(★★★★★) QGIS(★★★★)
  符号编辑: MapGIS(★★★) ArcGIS(★★★★) QGIS(★★★)
  标注引擎: MapGIS(★★★) ArcGIS(★★★★★) QGIS(★★★★)
  专题图模板: MapGIS(★★) ArcGIS(★★★★) QGIS(★★★)
```

### 2.3 拓扑编辑

```
MapGIS内置拓扑规则引擎 (与ArcGIS Topology Engine对标):

面拓扑规则:
├── 不重叠 (Must Not Overlap)
├── 无缝隙 (Must Not Have Gaps)
├── 必须被覆盖 (Must Be Covered By)
├── 边界必须被覆盖 (Boundary Must Be Covered By)
└── 包含点 (Contains Point)

线拓扑规则:
├── 不重叠 (Must Not Overlap)
├── 不交叉 (Must Not Intersect)
├── 无悬挂 (Must Not Have Dangles)
├── 端点必须被其他要素覆盖 (Endpoint Must Be Covered By)
└── 不自相交 (Must Not Self-Intersect)

网络拓扑:
├── 连通性 (Connectivity)
├── 流向 (Flow Direction)
└── 权重累计 (Weight Accumulation)

容差设置:
  - 默认拓扑容差: 0.001 地图单位
  - 高精度模式: 0.0001
  - 快速模式: 0.01
```

### 2.4 空间分析

| 分析类型 | MapGIS实现 | 对标评估 |
|----------|-----------|----------|
| 缓冲区分析 | 单环/多环/可变距离 | ★★★★★ |
| 叠加分析 | 相交/联合/擦除/标识 | ★★★★★ |
| 网络分析 | 最短路径/服务区/OD矩阵 | ★★★★ |
| 栅格分析 | 重分类/栅格计算/坡度坡向 | ★★★ |
| 三维分析 | 通视/剖面/填挖方/阴影 | ★★★★ |
| 地质分析 | 钻孔插值/地层建模/储量计算 | ★★★★★ (独有) |
| 地形分析 | DEM/等高线/TIN构建 | ★★★★ |
| 统计图表 | 柱状图/饼图/散点图 | ★★★ |

---

## 三、MapGIS行业应用深度

### 3.1 地质矿产（核心优势领域 ★★★★★）

```
MapGIS在地矿领域的独特优势:
  1. 地质数据库国家标准原生支持
     - 全国矿产资源潜力评价数据库
     - 全国重要矿产资源数据库
     - 全国矿业权实地核查数据库
  2. 地矿行业专用工具
     - 钻孔柱状图自动生成
     - 勘探线剖面图自动绘制
     - 储量估算(断面法/块段法/Kriging)
     - 矿体三维建模+资源量计算
  3. 地矿符号库(DZ/T 0179) 业界最完整
```

### 3.2 国土空间规划（★★★★★）

```
国土"一张图"建库流程(MapGIS版本):
  数据收集 → 数据标准化 → 坐标系统一(CGCS2000)
      ↓
  三区三线划定
      ├── 生态保护红线
      ├── 永久基本农田
      └── 城镇开发边界
      ↓
  规划成果编制 → 质检 → 汇交(自然资源部格式)

MapGIS优势: 自然资源部国产化替代政策直接受益者
```

### 3.3 管网/管线（★★★★）

```
管线信息化(MapGIS IGServer):
  管线探测数据 → MapGIS建库 → IGServer发布服务
      ├── 爆管分析(关阀搜索)
      ├── 横断面/纵断面生成
      ├── 三维管线可视化(3D Scene)
      └── 实时监测对接(SCADA/物联网)

对标: SuperMap管线模块 功能相似度85%
```

### 3.4 实景三维（★★★★）

```
MapGIS实景三维中国方案:
  倾斜摄影 → 空三解算(ContextCapture/Metashape)
      ↓
  MapGIS 3D Scene
      ├── OSGB导入→纹理优化
      ├── 单体化(矢量切割/纹理映射)
      ├── 3DTiles/I3S导出
      └── 与BIM数据融合(Revit/IFC导入)
```

---

## 四、MapGIS PyObject二次开发完整速查

### 4.1 基础数据操作

```python
# MapGIS Objects Python SDK 完整操作示例
from mapgis import (
    DataSource, FeatureClass, Map, Geometry,
    SpatialReference, CoordinateTransform, RasterLayer
)

# ===== 1. 数据源与要素类 =====
ds = DataSource()
ds.open("C:/data/mapgis10/Hubei_LandUse.hdf")

# 列出所有要素类
for fc_name in ds.list_feature_classes():
    fc = ds.get_feature_class(fc_name)
    print(f"{fc_name}: {fc.count} 要素, 类型={fc.geometry_type}")

# ===== 2. 属性查询与过滤 =====
fc = ds.get_feature_class("LANDUSE_POLYGON")
# 简单条件
result = fc.search("地类编码 LIKE '01%' AND 面积 > 5000")
# SQL空间查询
result = fc.spatial_query(
    search_geom=some_polygon,
    spatial_rel="INTERSECT",
    where_clause="面积 > 1000"
)

# ===== 3. 创建新要素类 =====
schema = {
    "fields": [
        {"name": "ID", "type": "INTEGER"},
        {"name": "NAME", "type": "TEXT", "length": 50},
        {"name": "AREA", "type": "DOUBLE"}
    ],
    "geometry_type": "POLYGON",
    "spatial_reference": "CGCS2000_GK_CM_114E"
}
new_fc = ds.create_feature_class("NEW_LAYER", schema)

# ===== 4. 坐标转换 =====
from mapgis import CoordinateTransform
src_crs = "Xian1980_GK_CM_117E"
tgt_crs = "CGCS2000_GK_CM_117E"
# 七参数
params = {"dx": -23.5, "dy": 128.7, "dz": 56.2,
          "rx": -0.21, "ry": 0.56, "rz": -0.88,
          "scale": 6.89}
transform = CoordinateTransform(src_crs, tgt_crs, params)
# 全库转换
transformed_fc = transform.apply(fc, output_name="LANDUSE_CGCS2000")

# ===== 5. 拓扑检查 =====
from mapgis import TopologyValidator
topo = TopologyValidator(fc)
# 添加规则
topo.add_rule("Must Not Overlap")
topo.add_rule("Must Not Have Gaps")
# 执行检查
errors = topo.validate(tolerance=0.001)
print(f"发现 {len(errors)} 个拓扑错误")

# ===== 6. 栅格分析 =====
raster = ds.open_raster("DEM_30m.tif")
# 坡度计算
slope = raster.slope(output_unit="degree")
# 重分类
reclass_dict = {(-9999, 100): 1, (100, 500): 2, (500, 1000): 3, (1000, 9999): 4}
reclassed = raster.reclassify(reclass_dict)
```

### 4.2 IGServer REST API

```python
# MapGIS IGServer 服务发布与调用
import requests

# --- 发布地图服务 ---
IGSERVER_URL = "http://localhost:8089/igs/rest"

# 发布HDF为地图服务
resp = requests.post(
    f"{IGSERVER_URL}/services/publish",
    json={
        "source_type": "HDF",
        "source_path": "/data/Hubei_BaseMap.hdf",
        "service_name": "HubeiBaseMap",
        "service_type": "MapServer",
        "crs": "EPSG:4490"  # CGCS2000
    }
)

# --- 查询要素 ---
resp = requests.get(
    f"{IGSERVER_URL}/services/HubeiBaseMap/MapServer/0/query",
    params={
        "where": "NAME LIKE '%武汉%'",
        "returnGeometry": "true",
        "outFields": "NAME, AREA, CODE",
        "f": "geojson"
    }
)
features = resp.json()

# --- WMS/WMTS ---
# MapGIS IGServer自动支持OGC WMS/WMTS
wms_url = f"{IGSERVER_URL}/services/HubeiBaseMap/MapServer/WMSServer"
wms_params = {
    "service": "WMS",
    "version": "1.3.0",
    "request": "GetMap",
    "layers": "0",
    "crs": "EPSG:4490",
    "bbox": "112.0,30.0,115.0,32.0",
    "width": 800,
    "height": 600,
    "format": "image/png"
}
map_image = requests.get(wms_url, params=wms_params)
```

### 4.3 三维场景开发

```python
# MapGIS 3D Scene Python API
from mapgis.threed import Scene, Layer3D, Camera

scene = Scene()
scene.open("C:/projects/Wuhan_RealityModel.m3d")

# 加载OSGB倾斜摄影
osgb_layer = Layer3D.open_osgb("C:/data/osgb/tiles/")
scene.add_layer(osgb_layer)

# 加载3DTiles
tiles_layer = Layer3D.open_3dtiles("C:/data/tiles/tileset.json")
scene.add_layer(tiles_layer)

# 相机控制
camera = scene.camera
camera.fly_to(lon=114.30, lat=30.59, alt=500, duration=2)
camera.set_view(direction=45, pitch=-30)

# 单体化
building_layer = scene.select_by_attribute("BUILDING_ID = 'B0012'")
building_layer.highlight(color=(255, 0, 0, 0.3))
```

---

## 五、MapGIS与ArcGIS完整迁移方案

### 5.1 数据迁移矩阵

| 源格式(ArcGIS) | 目标(MapGIS) | 迁移工具 | 完整度 |
|---------------|-------------|----------|--------|
| File GDB | HDF | FME/自定义脚本 | 85% |
| SHP | HDF子类 | MapGIS导入工具 | 95% |
| TIF/IMG | HDF栅格子类 | MapGIS导入工具 | 98% |
| 镶嵌数据集 | 栅格目录 | FME | 60% |
| 拓扑规则 | MapGIS拓扑规则 | 手动重建 | 70% |
| 网络数据集 | MapGIS网络 | 手动重建 | 50% |
| .style符号库 | .sym符号库 | 逐个映射 | 40% |
| ArcPy脚本 | MapGIS Objects SDK | 逻辑等价重写 | N/A |
| .lyrx图层文件 | .mlayer | 手动重建 | 70% |
| .aprx工程文件 | MapGIS工程 | 手动重建 | 30% |

### 5.2 国产化迁移路线图

```
第一梯队(核心替代 - 6个月内):
  桌面GIS:     ArcGIS Pro → MapGIS 10.7 Desktop
  服务发布:    ArcGIS Server → MapGIS IGServer
  数据存储:    SQL Server → 达梦DM8 / 人大金仓KingbaseES

第二梯队(配套替代 - 12个月内):
  操作系统:    Windows Server → 麒麟V10 / 统信UOS
  开发框架:    ArcPy → MapGIS Objects SDK Python绑定
  文档办公:    MS Office → WPS Office

第三梯队(生态替代 - 24个月内):
  移动外业:    ArcGIS Field Maps → MapGIS Mobile
  三维平台:    ArcGIS Earth → MapGIS 3D Scene
  BIM对接:     Revit → 国产BIM → MapGIS
  工作流:      ModelBuilder → MapGIS Workflow

风险提示:
  ⚠ 坐标系统内部编码差异，需逐个验证
  ⚠ 符号化需全部重建
  ⚠ 高级分析工具(地统计/空间统计)功能覆盖度有限
  ⚠ 用户培训成本高，建议分批迁移
```

### 5.3 常见迁移问题速查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 字段名乱码 | GBK/UTF-8编码不一致 | FME中转 → 设置编码为UTF-8 |
| 坐标系不识别 | WKID未在MapGIS注册 | 通过PRJ文件手动指定 |
| 面要素丢失 | 弧段超过MapGIS支持上限 | FME → Generalizer平滑 |
| 符号全部丢失 | .style无法直接转换 | 按国标重建符号库 |
| 注记化为点 | MapGIS不支持注记要素类 | 转为点要素+属性标注 |
| 3D符号消失 | ArcGIS 3D符号规范不兼容 | MapGIS 3D Scene重建 |

---

## 六、国产系统与数据库适配

### 6.1 操作系统适配

| 操作系统 | MapGIS 10.7 支持 | 注释 |
|----------|-----------------|------|
| Windows 10/11 | ✅ | 主要开发平台 |
| Windows Server 2019/2022 | ✅ | 服务器部署 |
| 麒麟V10(飞腾/鲲鹏) | ✅ | 国产化标准配置 |
| 统信UOS | ✅ | 国产化备选 |
| 中标麒麟 | ✅ | 军事/涉密环境 |

```bash
# 麒麟V10环境检查
uname -m          # 确认CPU架构: aarch64(鲲鹏/飞腾)
cat /etc/os-release | grep "Kylin"
# 安装MapGIS依赖
sudo yum install -y libX11 libXext libXi libXtst libstdc++
# MapGIS Desktop安装
sudo ./install_mapgis.sh --silent --accept-license
```

### 6.2 数据库适配

| 数据库 | MapGIS SDE支持 | 适用场景 |
|--------|---------------|----------|
| Oracle 19c | ✅ | 大型地矿数据库 |
| 达梦DM8 | ✅ | 信创首选 |
| 人大金仓KingbaseES V8 | ✅ | 信创备选 |
| PostgreSQL 15 + PostGIS | ✅ | 开源方案 |
| SQL Server 2019 | ✅ | 存量系统兼容 |

```sql
-- 达梦DM8空间数据初始化
CREATE TABLESPACE gis_data DATAFILE '/dm8/data/gis.dbf' SIZE 4096;
CREATE USER gis_admin IDENTIFIED BY "******" DEFAULT TABLESPACE gis_data;
GRANT DBA TO gis_admin;
-- 启用空间扩展
CALL SP_INIT_GEO_SYS(1);
```

---

## 七、MapGIS性能调优

| 优化项 | 方法 | 预期提升 |
|--------|------|----------|
| 数据存储 | HDF部署到SSD | 读写速度提升3-5倍 |
| 空间索引 | 创建R树索引 | 空间查询提升10-100倍 |
| 内存 | MapGIS内存缓存 >16GB | 大数据量操作流畅度提升 |
| 渲染 | 图层可见比例尺范围设置 | 平移缩放流畅度提升 |
| IGServer | 启用瓦片缓存 | 并发访问QPS提升10倍 |
| 分布式 | IGServer集群部署 | 并发支持500→5000 |
| 栅格 | 金字塔构建(overview) | 缩放显示提升100倍 |

---

> **V5.0新建说明**：本手册填补国产GIS三大支柱中MapGIS空白，对标ArcGIS Pro/SuperMap/QGIS。
> 原群组三无MapGIS独立文档，本手册为V5.0核心补充。
> 关联模块: references/13(QGIS), references/16(SuperMap), references/14(CASS), references/22(空间数据库), FUTURE_V5_云原生国产合规交付
