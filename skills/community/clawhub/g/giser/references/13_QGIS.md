# QGIS | 关联：12_ArcGIS_Pro.md 16_SuperMap_iDesktopX.md 21_Python_GIS生态.md | 最新验证：2026年6月

> QGIS 3.40 LTR / 3.42 稳定版 —— 开源GIS首选，全球最大GIS开源社区
> 数据来源：qgis.org / docs.qgis.org / GitHub

---

## 一、软件定位

| 项目 | 内容 |
|------|------|
| **开发商** | QGIS 开源社区（核心团队+全球贡献者） |
| **授权** | GPL v2（完全免费、无版权限制） |
| **版本策略** | LTS（长期支持，3年维护）+ 稳定版（每4个月） |
| **当前 LTS** | **QGIS 3.40.x**（截至2026年6月最新LTS） |
| **当前稳定版** | QGIS 3.42.x |
| **上一代 LTS** | QGIS 3.34（2023-2026维护） |
| **平台** | Windows / macOS / Linux / FreeBSD / Android |
| **下载** | https://qgis.org/download/ 或 https://www.osgeo.cn/qgis/（中文镜像） |

### 版本差异速查

| 特性 | 3.34 LTS | 3.40 LTS（当前） | 说明 |
|------|---------|-----------------|------|
| 点云支持 | 基础 | 增强（原生GPU加速渲染） | 明显提升 |
| 3D视图性能 | 一般 | 大幅提升 | — |
| Temporal Controller | 无 | ✅ 新增 | 时空数据时间轴控制 |
| 高程剖面工具 | 无 | ✅ 新增 | — |
| 传感器数据处理 | 无 | ✅ | — |
| 标注引擎 | 旧版 | 重构版（性能+质量） | — |

---

## 二、安装与中文配置

### 2.1 安装方式

**方式一：官方安装包（推荐）**
```
1. 访问 https://qgis.org/download/
2. 选择 "Long Term Release" → 下载对应系统安装包
3. 双击安装 → 全部默认选项 → 完成
```

**方式二：OSGeo4W 网络安装（Windows高级用户）**
```
运行 osgeo4w-setup.exe → 选择 "Advanced Install"
→ 搜索 qgis-ltr → 安装（可同时安装GRASS/SAGA/GDAL）
```

### 2.2 中文界面配置

```
Settings → Options → General
  → ☑ Override system locale
  → User interface translation: 简体中文
  → 重启 QGIS 生效
```

### 2.3 坐标系默认配置

```
Settings → Options → CRS Handling
  → CRS for new projects: EPSG:4490 - CGCS2000
  → ☑ Ask for datum transformation when no default is defined
```

---

## 三、核心功能模块

### 3.1 数据管理与加载

| 功能 | 操作 |
|------|------|
| **矢量加载** | Layer → Add Layer → Add Vector Layer（支持SHP/GeoJSON/GPKG/GDB/KML等） |
| **栅格加载** | Layer → Add Layer → Add Raster Layer（GeoTIFF/IMG/HDF/NetCDF等） |
| **在线底图** | XYZ Tiles → 添加天地图/OSM/Google底图 |
| **数据库连接** | Browser面板 → 右键PostGIS → New Connection |
| **WMS/WFS** | Layer → Add Layer → Add WMS/WMTS Layer |
| **拖放加载** | 直接拖拽文件到QGIS窗口（最快捷方式） |

### 3.2 地图制图

| 功能 | 操作路径 |
|------|---------|
| **符号化** | 图层右键 → Properties → Symbology（Single/Graduated/Categorized/Rule-based） |
| **标注** | 图层右键 → Properties → Labels（支持表达式和条件规则） |
| **布局出图** | Project → New Print Layout（添加地图/图例/比例尺/指北针/表格） |
| **地图集** | Print Layout → Atlas Generation（按图幅/行政区自动批量出图） |
| **样式管理** | Settings → Style Manager（导入/导出 .qml 样式文件） |

### 3.3 空间分析（Processing 工具箱）

| 分析类型 | 核心工具 | 引擎 |
|---------|---------|------|
| **矢量分析** | Buffer/Clip/Intersect/Dissolve/Difference/Spatial Join | QGIS原生 / GRASS / SAGA |
| **栅格分析** | Raster Calculator/Slope/Aspect/Hillshade/Reclassify | GDAL / SAGA |
| **插值** | IDW/TIN/Kriging | SAGA / GRASS |
| **网络分析** | Shortest Path/Service Area | QGIS原生（需安装插件） |
| **水文分析** | Fill Sinks/Flow Accumulation/Watershed | SAGA / GRASS |
| **地形分析** | Slope/Aspect/Ruggedness Index/Relief | GDAL / SAGA |

### 3.4 三维视图（原生3D）

```
View → New 3D Map View
  └── 可叠加 DEM（地形）+ 影像（底图）+ 矢量（建筑矢量拉升3D）
      + 倾斜模型 (.obj) + 点云 (.las/.laz)
```

### 3.5 插件生态

| 插件 | 功能 | 安装 |
|------|------|------|
| **QuickMapServices** | 一键加载多种在线底图 | Plugins → Manage → 搜索安装 |
| **Semi-Automatic Classification** | 遥感影像监督分类 | 同上 |
| **qgis2web** | 一键发布交互式Web地图 | 同上（输出Leaflet/OpenLayers网页） |
| **Profile Tool** | 地形剖面工具 | 同上 |
| **OpenLayers Plugin** | 在线地图加载 | 同上 |

---

## 四、PyQGIS 自动化（核心优势）

### 4.1 Python 控制台

```python
# 打开控制台：Plugins → Python Console
# 获取当前活动图层
layer = iface.activeLayer()

# 遍历要素
for feature in layer.getFeatures():
    print(feature["字段名"])

# 创建缓冲区
import processing
result = processing.run("native:buffer", {
    'INPUT': layer,
    'DISTANCE': 100,
    'OUTPUT': 'memory:'
})
```

### 4.2 独立 PyQGIS 脚本

```python
# 独立脚本（需设置QGIS环境变量）
import sys
sys.path.append(r"C:\Program Files\QGIS 3.40\apps\qgis-ltr\python")
from qgis.core import *

# 初始化
QgsApplication.setPrefixPath(r"C:\Program Files\QGIS 3.40\apps\qgis-ltr", True)
qgs = QgsApplication([], False)
qgs.initQgis()

# 加载图层
layer = QgsVectorLayer(r"D:\data\roads.shp", "roads", "ogr")
if not layer.isValid():
    print("图层加载失败")

# 执行分析...

qgs.exitQgis()
```

### 4.3 Processing 脚本

```python
# 批量投影转换
import processing, os

input_dir = r"D:\data\shp"
output_dir = r"D:\data\output"
target_crs = "EPSG:4490"

for file in os.listdir(input_dir):
    if file.endswith(".shp"):
        result = processing.run("native:reprojectlayer", {
            'INPUT': os.path.join(input_dir, file),
            'TARGET_CRS': QgsCoordinateReferenceSystem(target_crs),
            'OUTPUT': os.path.join(output_dir, file)
        })
        print(f"✅ {file}")
```

---

## 五、QGIS 数据处理工作流

### 工作流 1：OSM 数据分析

```
1. QuickOSM 插件 → 下载研究区 OSM 数据
2. 数据筛选：按标签（amenity/highway/building）
3. 坐标系统一 → EPSG:4490
4. 空间分析：缓冲区/网络分析/密度分析
5. 制图输出 + 数据导出为 GeoPackage
```

### 工作流 2：遥感影像分类

```
1. 加载多光谱影像
2. Semi-Automatic Classification 插件
3. 创建训练样本（ROI）
4. 选择分类器（最大似然/随机森林/SVM）
5. 执行分类 → 精度评估 → 后处理（过滤碎斑）
```

### 工作流 3：批量制图

```
1. 准备分幅图层（网格面/图幅索引）
2. Print Layout → Atlas → 选择 Coverage Layer
3. 配置地图项 → 动态标题/图名/图号
4. Export Atlas → 批量输出PDF/PNG
```

---

## 六、PyQGIS 高级自动化 ⭐ V4.0深度扩充

### 6.1 Processing Framework 批量处理

```python
# 批量执行所有矢量图层的缓冲区分析
import processing
from qgis.core import QgsProject

layers = QgsProject.instance().mapLayers().values()
results = []
for layer in layers:
    if layer.type() == layer.VectorLayer:
        result = processing.run("native:buffer", {
            'INPUT': layer,
            'DISTANCE': 100,
            'SEGMENTS': 20,
            'OUTPUT': 'memory:BUFFER_' + layer.name()
        })
        results.append(result['OUTPUT'])
```

| Processing 引擎 | 特点 | 适用场景 |
|----------------|------|---------|
| QGIS Native | 内置，无需额外安装 | 基础矢量/栅格分析 |
| GDAL | 栅格处理能力强 | 栅格转换/投影/拼接 |
| GRASS GIS 7/8 | 完整GIS分析套件 | 水文/地形/景观生态 |
| SAGA GIS | 栅格分析+地统计 | DEM分析/插值/地貌分类 |

### 6.2 自定义 Processing 算法

```python
from qgis.core import (QgsProcessingAlgorithm, QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterNumber, QgsProcessingParameterFeatureSink,
                       QgsProcessing, QgsFeatureSink, QgsProcessingFeedback)
from PyQt5.QtCore import QVariant

class MultiBufferAlgorithm(QgsProcessingAlgorithm):
    """多距离缓冲区分析算法"""
    
    INPUT = 'INPUT'
    DISTANCES = 'DISTANCES'
    OUTPUT = 'OUTPUT'
    
    def initAlgorithm(self, config):
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT, '输入图层', [QgsProcessing.TypeVectorAnyGeometry]))
        self.addParameter(QgsProcessingParameterNumber(
            self.DISTANCES, '缓冲距离(米)',
            QgsProcessingParameterNumber.Double, 100))
        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT, '输出图层'))
    
    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        distance = self.parameterAsDouble(parameters, self.DISTANCES, context)
        
        (sink, dest_id) = self.parameterAsSink(
            parameters, self.OUTPUT, context,
            source.fields(), source.wkbType(), source.sourceCrs())
        
        feedback.pushInfo(f'处理 {source.featureCount()} 个要素...')
        
        for feature in source.getFeatures():
            geom = feature.geometry()
            buffer_geom = geom.buffer(distance, 20)
            new_feature = feature
            new_feature.setGeometry(buffer_geom)
            sink.addFeature(new_feature, QgsFeatureSink.FastInsert)
        
        return {self.OUTPUT: dest_id}
```

| 自定义算法关键类 | 作用 |
|----------------|------|
| QgsProcessingAlgorithm | 算法基类，重写 initAlgorithm 和 processAlgorithm |
| QgsProcessingParameter* | 定义输入参数（矢量源/数值/字符串/范围等） |
| QgsProcessingParameterFeatureSink | 定义输出图层 |
| QgsProcessingFeedback | 反馈进度/日志信息 |

### 6.3 Virtual Layers（虚拟图层）

```sql
-- 跨图层空间查询，无需物理合并
SELECT a.*, b.population
FROM districts a
JOIN population_data b
ON ST_Intersects(a.geometry, b.geometry)
```

```sql
-- 虚拟图层：按行政区统计POI数量
SELECT a.id, a.name, a.geometry, COUNT(b.id) as poi_count
FROM admin_units a
LEFT JOIN poi_points b
ON ST_Contains(a.geometry, b.geometry)
GROUP BY a.id
```

| 虚拟图层特性 | 说明 |
|------------|------|
| 数据源 | 可引用项目中已加载的任何图层 |
| SQL引擎 | 基于 SQLite/SpatiaLite |
| 空间函数 | ST_Intersects, ST_Contains, ST_Distance, ST_Buffer 等 |
| 更新方式 | 源数据变化时自动更新查询结果 |
| 持久化 | 可导出为普通矢量图层 |

### 6.4 Field Calculator 高级表达式

```sql
-- Case when 条件赋值
CASE 
    WHEN "area" > 10000 THEN '大型'
    WHEN "area" > 5000 THEN '中型'
    ELSE '小型'
END

-- 几何函数
$area          -- 面积(m²)
$perimeter     -- 周长(m)
$x / $y        -- 几何中心坐标
$length        -- 线段长度
$x_at(0)       -- 几何体第一个节点X坐标
num_points($geometry)  -- 节点数

-- 聚合函数
aggregate(
    layer:='districts',
    aggregate:='sum',
    expression:="population",
    filter:=intersects($geometry, geometry(@parent))
)
```

**自定义 Python 函数：**

```python
from qgis.utils import qgsfunction

@qgsfunction(args='auto', group='Custom')
def land_use_class(value, feature, parent):
    """土地利用分类函数"""
    code_map = {'01': '耕地', '02': '园地', '03': '林地', '04': '草地'}
    return code_map.get(value, '其他')
```

### 6.5 Model Designer 自动化建模

```text
Processing → Graphical Modeler → 新建模型

典型建模工作流（批量缓冲区+裁剪）：
Input Layer → Buffer Tool → Clip Tool → Output
              ↑                ↑
         Distance参数      Clip Layer输入(第二输入)

模型特性：
├── 可视化编排：拖拽工具箱工具并连线
├── 可迭代：支持对多要素/多图层的批量处理
├── 可导出：导出为Python脚本再编辑
├── 可共享：.model3 文件可直接分享
└── 可参数化：参数可暴露给最终用户
```

### 6.6 QGIS Server + QWC2 企业发布

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1. 部署 QGIS Server | `sudo apt install qgis-server` (Linux) 或 OSGeo4W (Windows) | 作为 Apache/Nginx 的 FastCGI 模块运行 |
| 2. 准备项目文件 | 在 QGIS Desktop 中配置符号化/标注/可见范围，保存 .qgs 项目 | 项目文件即服务配置文件 |
| 3. 发布 WMS/WFS | 项目放在 QGIS Server 读取路径 → 自动获得 WMS/WFS/WMTS/WCS 能力 | URL: `http://server/qgisserver?MAP=/path/project.qgs&SERVICE=WMS` |
| 4. 部署 QWC2 | 下载 QGIS Web Client 2，配置 themesConfig.json | 轻量级 WebGIS 前端，不依赖数据库 |
| 5. 权限控制 | QGIS Server 支持 WMS 图层级别的访问控制 | 通过 .qgs 项目配置图层可见性和权限 |

### 6.7 性能调优

| 优化项 | 方法 | 效果 |
|--------|------|------|
| 空间索引 | 矢量图层属性 → Source → Create Spatial Index | 查询/选择速度提升 10-100 倍 |
| 缩放可见范围 | 图层右键 → Properties → Rendering → Scale dependent visibility | 避免小比例尺加载大量要素 |
| 几何简化 | 图层右键 → Properties → Rendering → ☑ Simplify geometry | 边渲染边简化，不影响原始数据 |
| 数据库视图 | 用 PostGIS 视图替代重复生成的文件 | 零冗余，始终为最新数据 |
| 渲染缓存 | Settings → Options → Rendering → Render cache | 平移/缩放无延迟 |
| 并行渲染 | Settings → Options → Rendering → Render layers in parallel | 多核心充分利用 |
| 属性表索引 | 图层属性 → Attributes Form → 对常用字段建索引 | 属性查询加速 |
| GeoPackage | 替代 Shapefile 作为工作格式 | 单文件、多图层、无字段名长度限制 |

### 6.8 QField 移动端采集

```text
项目 → 移动端工作流：
1. QGIS Desktop 配置外业项目（图层/表单/符号化）
2. QFieldSync 插件 → 打包项目到手机/平板
3. 外业采集（支持GPS定位/拍照/离线编辑）
4. 数据回传 → QFieldSync 同步回QGIS项目

关键配置：
├── 图层格式：GeoPackage（离线编辑必备）
├── 表单设计：图层属性 → Attributes Form → 拖放式控件布局
├── 照片关联：字段类型设为 "Attachment" → 自动关联拍照
├── 离线底图：使用 MBTiles 或 GeoPackage 栅格瓦片
├── 属性域：设置下拉列表/范围约束，减少外业录入错误
└── 可见性规则：根据属性条件控制字段显示/隐藏
```

| QField 能力 | 说明 |
|------------|------|
| 离线编辑 | GeoPackage 格式离线编辑，联网后同步 |
| 高精度GPS | 支持外接蓝牙GNSS接收器（厘米级） |
| 表单定制 | 拖放式表单设计，支持条件可见性 |
| 多媒体 | 照片/视频关联到要素属性 |
| 轨迹记录 | 后台GPS轨迹记录 |
| 云同步 | QFieldCloud 实现团队协作同步 |

---

## 七、QGIS ↔ ArcGIS Pro 功能对标

| 功能 | QGIS 实现 | ArcGIS Pro 实现 |
|------|----------|----------------|
| 地图制图 | Print Layout + Atlas | Layout + Map Series |
| 地理处理 | Processing Toolbox (GDAL/GRASS/SAGA) | Geoprocessing Tools |
| 模型构建 | Graphical Modeler | ModelBuilder |
| Python编程 | PyQGIS | ArcPy |
| 3D分析 | 3D Map View (原生) | Local Scene / Global Scene |
| 网络分析 | Shortest Path 插件 | Network Analyst |
| 空间统计 | Processing → 部分工具 | Spatial Statistics Toolbox |
| 栅格分析 | GDAL工具链 | Spatial Analyst |
| 数据管理 | Browser + Data Source Manager | Catalog |
| 格式支持 | 100+ | 100+ |
| 成本 | **免费** | 付费 |

---

## 八、常见问题

| 问题 | 原因 | 方案 |
|------|------|------|
| Shapefile 中文乱码 | 编码非 UTF-8 | 图层属性 → Source → Encoding → 选择 GBK/UTF-8 |
| 插件安装失败 | 网络问题 | 设置代理/手动下载 .zip 安装 |
| 处理大文件卡死 | 单线程处理 | 使用 Processing → 勾选 "Run in background" |
| 坐标偏移 | CRS不匹配 | 右键图层 → Set CRS → 选择正确坐标系 |
| 导出PDF中文不显示 | 字体缺失 | 安装中文字体 / 使用英文备用字体 |
| Processing 后台运行无响应 | 插件冲突或内存不足 | 查看 Processing → History 日志，关闭无关插件，增大处理内存 |
| PyQGIS 导入错误 | 环境变量未正确配置 | 确保 PYTHONPATH/PATH 指向 QGIS Python 目录，或使用 OSGeo4W Shell 启动 |
| 虚拟图层SQL错误 | 字段名大小写或引号问题 | 字段名需使用双引号包裹，检查字段名与SQL中一致（区分大小写） |

---

> V4.0 | 关联阅读：`12_ArcGIS_Pro.md`（对标产品） | `16_SuperMap_iDesktopX.md`（国产竞品） | `21_Python_GIS生态.md`（Python脚本生态）


<!-- wm:坤图_GIS:V1.0 -->
