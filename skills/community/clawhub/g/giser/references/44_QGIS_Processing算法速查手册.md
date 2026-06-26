# 44 QGIS Processing 算法速查手册

> **CBK V5.0 | 群组六：现代GIS技术栈**
> **版本**: 1.0 | **日期**: 2026-06 | **维护**: GIS CBK Team
> **交叉引用**: ←→ 35_专家级批量处理与自动化实战指南.md、←→ 37_自进化反馈机制.md、←→ 26_WorkBuddyGIS_AddIn开发.md、←→ 13_QGIS.md、←→ 21_Python_GIS生态.md、←→ 33_空间分析与统计.md

---

## 目录

1. [Processing框架架构](#一processing框架架构)
2. [核心算法速查表](#二核心算法速查表)
3. [PyQGIS Processing 编程模板](#三pyqgis-processing-编程模板)
4. [Model Builder 与图形建模](#四model-builder-与图形建模)
5. [常见陷阱与反模式](#五常见陷阱与反模式)
6. [批量处理最佳实践](#六批量处理最佳实践)
7. [性能优化](#七性能优化)
8. [快速参考表](#八快速参考表)

---

## 一、Processing框架架构

### 1.1 架构总览

QGIS Processing Framework 是统一算法执行框架，核心理念："一个前端，多个后端"——所有算法通过统一的 GUI/Python/CLI 接口调用，底层封装 QGIS 原生、GDAL、GRASS、SAGA 等引擎。

```
┌──────────────────────────────────────────────────────────────┐
│                      Unified Frontend                        │
│  ┌──────────┐  ┌───────────┐  ┌───────────┐  ┌──────────┐  │
│  │ GUI      │  │  PyQGIS   │  │ qgis_     │  │ Graphical│  │
│  │ Toolbox  │  │  Python   │  │ process   │  │ Modeler  │  │
│  └────┬─────┘  └─────┬─────┘  └─────┬─────┘  └────┬─────┘  │
│       └──────────────┴─────────────┴──────────────┘         │
│                          │                                   │
│                  ProcessingRegistry                          │
│                          │                                   │
│  ┌────────┬───────┬──────┼──────┬──────┬───────┬──────┐     │
│  │ native │ qgis  │ gdal │ grass│ saga │  otb  │ pdal │     │
│  │ (C++)  │ (py)  │  ★   │  ★   │(弃用)│(需装) │ 3.32+│     │
│  └────────┴───────┴──────┴──────┴──────┴───────┴──────┘     │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 Provider 体系详解

| # | Provider ID | 底层引擎 | 算法数量 | 状态 | 关键用途 |
|---|-------------|---------|---------|------|---------|
| 1 | `native` | QGIS C++ 核心 | ~280+ | 活跃 | 矢量/栅格/分析核心 |
| 2 | `qgis` | QGIS Python 脚本 | ~40+ | 活跃 | 扩展工具、高级分析 |
| 3 | `gdal` | GDAL/OGR CLI | ~50+ | 活跃 | 投影/格式转换/COG |
| 4 | `grass` | GRASS GIS 8 | ~300+ | 活跃 | 水文/地形/地统计 |
| 5 | `saga` | SAGA GIS | ~200+ | QGIS 3.30+ 弃用 | 地形分析（建议迁移到 native） |
| 6 | `otb` | Orfeo ToolBox | ~100+ | 需额外安装 | 遥感分类/分割 |
| 7 | `pdal` | PDAL 点云 | ~20+ | QGIS 3.32+ | LAS/LAZ 点云处理 |
| 8 | `3d` | QGIS 3D 引擎 | ~10+ | QGIS 3.30+ | 3D 三角剖分/DEM赋Z |

### 1.3 Algorithm ID 命名规范

**格式**: `provider:algorithm_id`

```
native:buffer              # native provider的buffer算法
gdal:warpreproject         # gdal provider的投影算法
grass:r.slope.aspect       # grass provider（sub-module层级用点号）
saga:sagawetnessindex      # saga provider（扁平命名）
pdal:clip                  # pdal provider
3d:tessellate              # 3d provider
model:my_workflow          # 自定义Model
```

**命名规则**:
- `native:*` 和 `qgis:*` 使用小写下划线命名（`fixgeometries`, `joinbylocationsummary`）
- `gdal:*` 使用小写扁平命名（`warpreproject`, `clipvectorbypolygon`）
- `grass:*` 使用 `module.submodule` 层次结构（`r.slope.aspect`, `v.clean`）
- `saga:*` 使用小写扁平无分隔符（`sagawetnessindex`）

### 1.4 QGIS Python Console / Standalone Script 集成

**QGIS 内置 Python Console 中调用**（最常用）:
```python
import processing
result = processing.run("native:buffer", {
    'INPUT': '/path/to/input.shp',
    'DISTANCE': 100,
    'OUTPUT': '/path/to/output.shp'
})
```

**Standalone Script 方式**（无GUI环境）:
```python
import sys
sys.path.append('/usr/share/qgis/python/plugins')
from qgis.core import QgsApplication, QgsProcessingFeedback, QgsProcessingContext
from processing.core.Processing import Processing

QgsApplication.setPrefixPath('/usr', True)
qgs = QgsApplication([], False)
qgs.initQgis()

Processing.initialize()
import processing
result = processing.run("native:buffer", {'INPUT': 'in.shp', 'DISTANCE': 100, 'OUTPUT': 'out.shp'})

qgs.exitQgis()
```

**qgis_process CLI 方式**（CI/CD 友好）:
```bash
# 搜索算法
qgis_process list | grep buffer

# 查看参数
qgis_process help native:buffer

# 执行
qgis_process run native:buffer --INPUT=input.shp --DISTANCE=100 --OUTPUT=output.shp

# JSON 方式执行
qgis_process run native:buffer --json '{"INPUT":"input.shp","DISTANCE":100,"OUTPUT":"output.shp"}'
```

### 1.5 Processing 版本历史关键变更

| 版本 | 年份 | 关键变更 |
|------|------|---------|
| **QGIS 3.0** | 2018 | 全新 Processing 框架（C++重写），API 不兼容 2.x |
| **QGIS 3.4 LTR** | 2018 | 算法参数类型扩展，加入 QgsProcessingParameterEnum |
| **QGIS 3.10 LTR** | 2019 | `native:` provider 大幅扩展，引入 network analysis 算法 |
| **QGIS 3.16 LTR** | 2020 | 引入 3D provider，修复大量 algorithm ID |
| **QGIS 3.22 LTR** | 2021 | 加入 `native:dbscanclustering`、`native:kmeansclustering` |
| **QGIS 3.28 LTR** | 2022 | GRASS 8 集成，SAGA provider 标记弃用 |
| **QGIS 3.30** | 2023 | SAGA 正式移除改用插件，PDAL provider 稳定 |
| **QGIS 3.32** | 2023 | PDAL 点云算法补全，COG/STAC 支持增强 |
| **QGIS 3.34 LTR** | 2023 | 当前 LTR，算法稳定性修复，GDAL 3.8 集成 |
| **QGIS 3.36** | 2024 | 栅格分析性能优化，虚拟栅格 VRT 改进 |
| **QGIS 3.38** | 2024 | 最新版，3D tile 支持增强 |

> **提示**: 判断当前版本用 `QGIS.QgsApplication.QGIS_VERSION`，列出所有算法用 `qgis_process list`

---

## 二、核心算法速查表

### 2.1 矢量分析

| 算法ID | 名称 | 关键参数 | Python调用示例 |
|--------|------|---------|---------------|
| `native:buffer` | 缓冲区 | INPUT, DISTANCE, SEGMENTS(5), END_CAP_STYLE(0=Round), DISSOLVE(False) | `processing.run("native:buffer", {'INPUT': lyr, 'DISTANCE': 100, 'OUTPUT': 'memory:'})` |
| `native:clip` | 裁剪 | INPUT, OVERLAY, OUTPUT | `processing.run("native:clip", {'INPUT': lyr, 'OVERLAY': boundary, 'OUTPUT': 'clipped.shp'})` |
| `native:intersection` | 交集 | INPUT, OVERLAY, OUTPUT | 保留INPUT属性，取相交部分 |
| `native:union` | 并集 | INPUT, OVERLAY, OUTPUT | 合并区域，保留双方属性 |
| `native:difference` | 差集 | INPUT, OVERLAY, OUTPUT | INPUT减去OVERLAY区域 |
| `native:symmetricaldifference` | 对称差集 | INPUT, OVERLAY, OUTPUT | XOR区域（非重叠区） |
| `native:dissolve` | 融合 | INPUT, FIELD(可选), OUTPUT | 按字段融合相邻面 |
| `native:simplifygeometries` | 简化 | INPUT, METHOD(0=Douglas), TOLERANCE | Douglas-Peucker 简化 |
| `native:fixgeometries` | 修复几何 | INPUT, METHOD(1=Structure), OUTPUT | 修复无效拓扑 |
| `native:reprojectlayer` | 投影转换 | INPUT, TARGET_CRS, OUTPUT | 坐标系重投影 |
| `native:extractbyexpression` | 表达式提取 | INPUT, EXPRESSION, OUTPUT | `"area_km2" > 100` |
| `native:extractbyattribute` | 属性提取 | INPUT, FIELD, OPERATOR(0==), VALUE | 按字段值过滤 |
| `native:extractbylocation` | 位置提取 | INPUT, PREDICATE(0=intersects), INTERSECT | 空间关系过滤 |
| `native:joinattributestable` | 属性表连接 | INPUT, INPUT_2, FIELD, FIELD_2, OUTPUT | 一对一属性挂接 |
| `native:joinbylocationsummary` | 按位置汇总 | INPUT, JOIN, PREDICATE, SUMMARIES, OUTPUT | 面内点数统计 |
| `native:countpointsinpolygon` | 面内点计数 | POLYGONS, POINTS, WEIGHT, FIELD(NUMPOINTS) | 行政区POI密度 |

**buffer 端点样式编码**:
- 0 = Round (默认), 1 = Flat, 2 = Square

**extractbylocation 谓词编码**:
- 0=intersects, 1=contains, 2=equals, 3=touches, 4=overlaps, 5=within, 6=crosses

**joinbylocationsummary 汇总类型**:
- 0=count, 1=sum, 2=mean, 3=median, 4=stdev, 5=min, 6=max, 7=range, 8=minority, 9=majority

### 2.2 栅格分析

| 算法ID | 名称 | 关键参数 | 说明 |
|--------|------|---------|------|
| `native:fillnodata` | 填充NoData | INPUT, BAND(1), DISTANCE(10), ITERATIONS, OUTPUT | 周边像元插值填充空洞 |
| `gdal:warpreproject` | 投影/重采样 | INPUT, SOURCE_CRS, TARGET_CRS, RESAMPLING(0), OUTPUT | GDAL gdalwarp 封装 |
| `gdal:cliprasterbymasklayer` | 按面裁剪 | INPUT, MASK, CROP_TO_CUTLINE(True), OUTPUT | gdalwarp -cutline |
| `gdal:cliprasterbyextent` | 按范围裁剪 | INPUT, PROJWIN, OUTPUT | gdal_translate -projwin |
| `native:rastercalculator` | 栅格计算器 | INPUT, BAND(1), FORMULA, OUTPUT | `"dem@1" * 3.28084` |
| `gdal:rastercalculator` | GDAL栅格计算 | INPUT_A, BAND_A, INPUT_B, BAND_B, FORMULA | numpy 语法: `A+B` |
| `native:slope` | 坡度 | INPUT, BAND(1), Z_FACTOR(1), OUTPUT | 度/百分比（自动判断CRS） |
| `native:aspect` | 坡向 | INPUT, BAND(1), Z_FACTOR(1), OUTPUT | 0-360° |
| `native:hillshade` | 山体阴影 | INPUT, BAND(1), AZIMUTH(300), VERTICAL_ANGLE(40), OUTPUT | 常用: azimuth=315, altitude=45 |
| `native:reclassifybytable` | 重分类 | INPUT, BAND(1), TABLE, OUTPUT | TABLE=[min,max,newVal, ...] |
| `native:rasterlayerzonalstats` | 分区统计 | INPUT, BAND(1), ZONES, STATS | 按矢量/栅格分区统计 |
| `gdal:contour` | 等高线 | INPUT, BAND(1), INTERVAL(10), FIELD_NAME('ELEV') | DEM→等高线 |

**山体阴影常用参数**:

| 效果 | AZIMUTH | VERTICAL_ANGLE |
|------|---------|----------------|
| 标准日照 | 315 | 45 |
| 早晨效果 | 90 | 15 |
| 中午顶光 | 0 | 90 |

**重分类 TABLE 格式**: `[min1, max1, newVal1, min2, max2, newVal2, ...]`
```python
# 坡度重分类: 0-5°→1, 5-15°→2, 15-25°→3, 25-90°→4
TABLE = [0, 5, 1, 5, 15, 2, 15, 25, 3, 25, 90, 4]
```

**gdal:warpreproject RESAMPLING 编码**:
- 0=Nearest, 1=Bilinear, 2=Cubic, 3=CubicSpline, 4=Lanczos

### 2.3 数据处理

| 算法ID | 名称 | 关键参数 | 使用场景 |
|--------|------|---------|---------|
| `native:mergevectorlayers` | 合并图层 | LAYERS, CRS, OUTPUT | 多图幅拼接为一个图层 |
| `native:splitvectorlayer` | 按字段分割 | INPUT, FIELD, OUTPUT | 按行政区/类型拆分 |
| `native:randomextract` | 随机提取 | INPUT, METHOD(0), NUMBER(10), OUTPUT | 抽样验证/缩略图 |
| `native:randomextractwithinsubsets` | 分组随机提取 | INPUT, METHOD, NUMBER, FIELD | 分层抽样 |
| `native:creategrid` | 创建网格 | TYPE(0=Rectangle), EXTENT, HSPACING, VSPACING | 渔网/采样网格 |
| `native:pointsalonggeometry` | 沿几何生成点 | INPUT, DISTANCE, OUTPUT | 等距采样点 |
| `native:refactorfields` | 重构字段 | INPUT, FIELDS_MAPPING, OUTPUT | 批量改名/改类型/重排 |
| `native:addgeometryattributes` | 添加几何属性 | INPUT, CALCULATE_ALL(True), OUTPUT | 添加area/perimeter/x/y字段 |
| `native:fieldcalculator` | 字段计算器 | INPUT, FIELD_NAME, FIELD_TYPE, FORMULA | 最常用：计算面积/长度/条件 |
| `native:multiparttosingleparts` | 多部件拆分 | INPUT, OUTPUT | 一个多部件→多个单部件 |
| `native:deletefield` | 删除字段 | INPUT, NAME, OUTPUT | 移除指定列 |
| `native:retainfields` | 保留字段 | INPUT, FIELDS, OUTPUT | 只保留指定列 |

**creategrid TYPE 编码**: 0=Rectangle, 1=Diamond, 2=Hexagon

**字段类型编码 (FIELD_TYPE)**: 0=Integer, 1=Float, 2=String, 3=Integer64, 4=Date, 6=DateTime, 8=Boolean, 10=Decimal

### 2.4 GDAL/OGR 核心算法

| 算法ID | 对应CLI | 功能 | 典型用法 |
|--------|---------|------|---------|
| `gdal:warpreproject` | gdalwarp | 栅格投影/重采样 | WGS84→CGCS2000 |
| `gdal:translate` | gdal_translate | 格式转换/压缩 | TIF→COG, 加LZW压缩 |
| `gdal:cliprasterbymasklayer` | gdalwarp -cutline | 按矢量面裁剪 | 行政区裁剪DEM |
| `gdal:cliprasterbyextent` | gdal_translate -projwin | 按范围裁剪 | 批量分幅 |
| `gdal:contour` | gdal_contour | 等高线 | DEM→10m等高距 |
| `gdal:merge` | gdal_merge.py | 栅格拼接 | 多景影像拼接 |
| `gdal:buildvirtualraster` | gdalbuildvrt | 虚拟栅格 | 无需物理拼接即可处理 |
| `gdal:fillnodata` | gdal_fillnodata.py | 填充空洞 | 消除DEM空洞 |
| `gdal:convertformat` | ogr2ogr | 矢量格式转换 | SHP→GPKG |
| `gdal:clipvectorbypolygon` | ogr2ogr -clipdst | 按面裁剪矢量 | 行政区裁切 |
| `gdal:clipvectorbyextent` | ogr2ogr -spat | 按范围裁剪矢量 | 矩形范围裁切 |

**gdal:translate 压缩示例**:
```python
processing.run("gdal:translate", {
    'INPUT': 'input.tif',
    'OUTPUT': 'output.tif',
    'EXTRA': '-co COMPRESS=LZW -co TILED=YES -co BIGTIFF=YES -co PREDICTOR=2'
})
```

---

## 三、PyQGIS Processing 编程模板

### 模板1: 单次调用（含错误处理）

```python
import processing
from qgis.core import QgsProcessingException

def safe_buffer(layer, distance, output_path):
    """安全执行Buffer，含参数验证"""
    if not layer.isValid():
        raise ValueError(f"图层无效: {layer.name()}")
    try:
        result = processing.run("native:buffer", {
            'INPUT': layer,
            'DISTANCE': distance,
            'SEGMENTS': 5,
            'DISSOLVE': True,
            'OUTPUT': output_path
        })
        return result['OUTPUT']
    except QgsProcessingException as e:
        print(f"Buffer失败: {e}")
        # 尝试自动修复几何后重试
        fixed = processing.run("native:fixgeometries", {
            'INPUT': layer, 'OUTPUT': 'memory:fixed'
        })['OUTPUT']
        return processing.run("native:buffer", {
            'INPUT': fixed, 'DISTANCE': distance,
            'SEGMENTS': 5, 'OUTPUT': output_path
        })['OUTPUT']
```

### 模板2: 按字段值分组批量处理

```python
import processing
from qgis.core import QgsVectorLayer

def batch_by_field(input_path, field_name, output_dir):
    """按字段值分组，每组独立处理"""
    layer = QgsVectorLayer(input_path, 'input', 'ogr')
    unique_values = layer.uniqueValues(layer.fields().indexOf(field_name))
    
    for value in unique_values:
        # 提取当前组
        subset = processing.run("native:extractbyattribute", {
            'INPUT': layer,
            'FIELD': field_name,
            'OPERATOR': 0,  # =
            'VALUE': value,
            'OUTPUT': 'memory:subset'
        })['OUTPUT']
        
        # 对该组执行处理
        result = processing.run("native:buffer", {
            'INPUT': subset,
            'DISTANCE': 500,
            'OUTPUT': f'{output_dir}/buffer_{value}.shp'
        })
        print(f"  完成 {field_name}={value}")
```

### 模板3: 自定义Processing脚本（@alg decorator）

```python
from qgis.core import (QgsProcessingAlgorithm, QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterDistance, QgsProcessingParameterFeatureSink)
from qgis.PyQt.QtCore import QCoreApplication

class MultiBufferAlgorithm(QgsProcessingAlgorithm):
    """多环缓冲区算法示例"""
    
    INPUT = 'INPUT'
    DISTANCES = 'DISTANCES'
    OUTPUT = 'OUTPUT'
    
    def name(self): return 'multibuffer'
    def displayName(self): return '多环缓冲区'
    def group(self): return '自定义工具'
    
    def tr(self, string): return QCoreApplication.translate('Processing', string)
    
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSource(
            self.INPUT, '输入图层'))
        self.addParameter(QgsProcessingParameterDistance(
            self.DISTANCES, '缓冲区距离（逗号分隔）', defaultValue=100.0))
        self.addParameter(QgsProcessingParameterFeatureSink(
            self.OUTPUT, '输出图层'))
    
    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        distances = [float(d.strip()) for d in 
                     self.parameterAsString(parameters, self.DISTANCES, context).split(',')]
        
        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT, context,
            source.fields(), source.wkbType(), source.sourceCrs())
        
        for distance in distances:
            if feedback.isCanceled(): break
            feedback.pushInfo(f'处理距离: {distance}')
            temp = processing.run("native:buffer", {
                'INPUT': parameters[self.INPUT],
                'DISTANCE': distance, 'OUTPUT': 'memory:'
            }, context=context)['OUTPUT']
            for f in temp.getFeatures():
                sink.addFeature(f)
        
        return {self.OUTPUT: dest_id}
```

### 模板4: 运行Model

```python
# 加载并运行 .model3 模型文件
model_result = processing.run("model:SiteSelection", {
    'roads': 'roads.shp',
    'dem': 'elevation.tif',
    'landuse': 'landuse.shp',
    'buffer_distance': 500,
    'slope_threshold': 15,
    'Output': 'suitable_sites.gpkg'
})
```

### 模板5: 带日志的管道处理

```python
import processing
import time

def pipeline_with_logging(steps, log_path='pipeline.log'):
    """带时间戳日志的处理管道"""
    with open(log_path, 'w', encoding='utf-8') as log:
        log.write(f"Pipeline started at {time.ctime()}\n")
        
        for i, (alg_id, params, desc) in enumerate(steps):
            t0 = time.time()
            log.write(f"[Step {i+1}] {desc} ({alg_id})\n")
            try:
                result = processing.run(alg_id, params)
                elapsed = time.time() - t0
                log.write(f"  SUCCESS in {elapsed:.1f}s → {result.get('OUTPUT', 'N/A')}\n")
                yield result
            except Exception as e:
                log.write(f"  FAILED: {e}\n")
                raise
    
    print(f"日志已写入: {log_path}")

# 使用示例
for r in pipeline_with_logging([
    ("native:fixgeometries", {'INPUT':'raw.shp','OUTPUT':'memory:'}, "修复几何"),
    ("native:reprojectlayer", {'INPUT': r['OUTPUT'], 'TARGET_CRS': 'EPSG:4527', 'OUTPUT': 'final.gpkg'}, "投影转换"),
]):
    pass
```

---

## 四、Model Builder 与图形建模

### 4.1 使用场景与限制

| 场景 | 适合Model Builder? | 说明 |
|------|-------------------|------|
| 3-10个算法的线性流程 | 是 | 最佳场景 |
| 含条件分支的逻辑 | 部分支持 | QGIS 3.26+ 支持 condition 节点 |
| 含循环/迭代 | 否 | 建议用 PyQGIS 脚本 |
| 需要复用的工作流 | 是 | 保存为 .model3 文件分享 |
| 需要版本控制 | 是 | .model3 是XML，可 Git 管理 |
| 超大数据量 (>10GB) | 否 | 建议用 CLI/Python 分块处理 |
| 含自定义 Python 逻辑 | 否 | 用 @alg decorator |

**限制**:
- 不支持循环（需用 PyQGIS 脚本）
- 不支持异步/并行执行
- 复杂条件嵌套难以维护
- .model3 XML 手动编辑易出错

### 4.2 Python 创建/运行模型

**在 Python 中调用已有模型**:
```python
# 方式1: 直接运行（模型在 QGIS profile 的 models/ 目录）
result = processing.run("model:my_workflow", {
    'INPUT': 'data.shp',
    'DISTANCE': 100,
    'OUTPUT': 'output.shp'
})

# 方式2: 指定完整路径的模型文件
result = processing.run("model:C:/models/site_analysis.model3", {
    'INPUT': 'data.shp',
    'PARAM_X': 42,
    'OUTPUT': 'result.gpkg'
})
```

**将 Model 导出为 Python 脚本**:
- 在 Model Designer 中: Model → Export as Script → Python
- 导出后可在此基础上添加循环、条件、错误处理

### 4.3 Model 参数类型速查表

| 参数类型 | 用途 | GUI 设置方式 |
|---------|------|------------|
| Vector Layer | 输入矢量图层 | 添加输入 → Vector Layer |
| Raster Layer | 输入栅格图层 | 添加输入 → Raster Layer |
| Number | 数值参数 | 添加输入 → Number |
| String | 文本参数 | 添加输入 → String |
| Boolean | 开关选项 | 添加输入 → Boolean |
| Enum | 下拉选择 | 添加输入 → Enum |
| CRS | 坐标系选择 | 添加输入 → CRS |
| Extent | 空间范围 | 添加输入 → Extent |
| Point | 点坐标 | 添加输入 → Point |
| Field | 字段选择（动态关联图层） | 添加输入 → Field |
| Expression | QGIS 表达式 | 添加输入 → Expression |
| File | 文件路径 | 添加输入 → File |

**Model 设计最佳实践**:
1. 节点重命名：设置有意义的算法名称（如"缓冲区_500m"而非"Buffer"）
2. 只暴露必要参数：不把每个算法的所有参数都设为 Model 输入
3. 设置合理默认值：减少用户操作
4. 添加注释节点：说明关键步骤逻辑
5. 使用 condition 节点：处理空输入/异常情况
6. 中间结果可调试：关键步骤输出到 TEMPORARY_OUTPUT

---

## 五、常见陷阱与反模式

### 5.1 Algorithm ID 变化（版本升级坑）

| 旧ID (QGIS 3.10) | 新ID (QGIS 3.28+) | 说明 |
|-------------------|-------------------|------|
| `qgis:buffer` | `native:buffer` | 从 qgis provider 迁移到 native |
| `qgis:reprojectlayer` | `native:reprojectlayer` | 同上 |
| `qgis:intersection` | `native:intersection` | 同上 |
| `saga:slopeaspectcurvature` | `native:slope` + `native:aspect` | SAGA弃用，拆分为多个 native 算法 |
| `saga:ordinarykriging` | `grass:v.surf.rst` | 克里金插值替代方案 |

**防御措施**:
```python
# 运行时检查算法是否可用
from qgis.core import QgsApplication
alg = QgsApplication.processingRegistry().algorithmById("native:buffer")
if alg is None:
    # 降级到备选算法
    alg = QgsApplication.processingRegistry().algorithmById("qgis:buffer")
```

### 5.2 'memory:' 临时图层生命周期

```python
# 错误: memory: 图层仅在本脚本执行期间有效
result = processing.run("native:buffer", {
    'INPUT': layer, 'DISTANCE': 100, 'OUTPUT': 'memory:'
})
# 脚本结束后 memory: 图层被销毁

# 正确: 如果后续需要引用，显式保存到磁盘
result = processing.run("native:buffer", {
    'INPUT': layer, 'DISTANCE': 100, 'OUTPUT': 'intermediate.gpkg'
})
```

| OUTPUT 值 | 行为 | 生命周期 | 适用场景 |
|-----------|------|---------|---------|
| `'memory:'` | 内存图层 | 脚本生命周期 | 串联步骤的中间结果 |
| `'TEMPORARY_OUTPUT'` | QGIS管理临时文件 | QGIS session | GUI中使用 |
| `'/path/to/file.gpkg'` | 磁盘文件 | 永久 | 最终输出、大文件 |

### 5.3 坐标系不一致导致静默错误

```python
# 问题: 两个图层坐标系不同 → 结果错位但无报错
layer_a = QgsVectorLayer('wgs84.shp')  # EPSG:4326
layer_b = QgsVectorLayer('cgcs2000.shp')  # EPSG:4527

# 修复: 统一坐标系后再处理
def ensure_same_crs(layer1, layer2, target_crs='EPSG:4527'):
    """确保两个图层坐标系一致"""
    layers = []
    for lyr in [layer1, layer2]:
        if lyr.crs().authid() != target_crs:
            reprojected = processing.run("native:reprojectlayer", {
                'INPUT': lyr, 'TARGET_CRS': target_crs, 'OUTPUT': 'memory:'
            })['OUTPUT']
            layers.append(reprojected)
        else:
            layers.append(lyr)
    return layers[0], layers[1]
```

### 5.4 字段名/类型不匹配

```python
# 问题: GPKG 字段名小写，SHP 字段名大写/截断
# SHP 的 "AREA_KM2" → GPKG 的 "area_km2"

# 防御: 使用字段索引而非名称
layer = QgsVectorLayer(input_path, 'temp', 'ogr')
field_idx = layer.fields().indexFromName('area_km2')

# 通用字段查找（大小写不敏感）
def find_field(layer, name):
    for f in layer.fields():
        if f.name().lower() == name.lower():
            return f.name()
    return None
```

### 5.5 NULL 几何体导致处理中断

```python
# 处理前清除 NULL 几何要素
clean = processing.run("native:extractbyexpression", {
    'INPUT': layer,
    'EXPRESSION': '$geometry IS NOT NULL',
    'OUTPUT': 'memory:clean'
})['OUTPUT']

# 修复无效几何
fixed = processing.run("native:fixgeometries", {
    'INPUT': clean,
    'METHOD': 1,  # Structure方法（更彻底）
    'OUTPUT': 'memory:fixed'
})['OUTPUT']
```

### 5.6 Windows 路径编码问题

```python
# 问题: 中文路径导致 GDAL 命令失败
import os
input_path = 'D:/数据/道路.shp'  # 中文路径

# 修复1: 使用 forward slash
safe_path = input_path.replace('\\', '/')

# 修复2: GPKG 替代 SHP（UTF-8原生支持）
output = safe_path.replace('.shp', '.gpkg')

# 修复3: 使用 os.path 处理
output = os.path.join(output_dir, 'output.gpkg').replace('\\', '/')
```

### 5.7 大文件处理内存溢出

| 策略 | 适用场景 | 示例 |
|------|---------|------|
| 分块处理 | 千万级要素 | 按空间网格分批 |
| GDAL 命令行 | >1GB 栅格 | `gdalwarp -multi -wo NUM_THREADS=ALL_CPUS` |
| VRT 虚拟栅格 | 多文件栅格 | `gdalbuildvrt mosaic.vrt *.tif` |
| 内存图层限制 | 百万级矢量 | 使用 `'memory:' + layerName` 命名 |
| 字段精简 | 宽表矢量 | 先用 `retainfields` 只保留必要的列 |

```python
# 分块处理大矢量
def chunked_spatial_process(layer_path, algorithm_id, params, chunk_cols=10):
    extent = QgsVectorLayer(layer_path).extent()
    x_step = (extent.xMaximum() - extent.xMinimum()) / chunk_cols
    
    results = []
    for col in range(chunk_cols):
        xmin = extent.xMinimum() + col * x_step
        xmax = xmin + x_step
        chunk_extent = f"{xmin},{xmax},{extent.yMinimum()},{extent.yMaximum()}"
        
        chunk = processing.run("native:extractbyextent", {
            'INPUT': layer_path, 'EXTENT': chunk_extent, 'CLIP': True,
            'OUTPUT': 'memory:chunk'
        })['OUTPUT']
        
        params['INPUT'] = chunk
        params['OUTPUT'] = f'output_chunk_{col}.gpkg'
        results.append(processing.run(algorithm_id, params))
    
    # 合并结果
    processing.run("native:mergevectorlayers", {
        'LAYERS': [r['OUTPUT'] for r in results],
        'CRS': QgsCoordinateReferenceSystem('EPSG:4527'),
        'OUTPUT': 'final_merged.gpkg'
    })
```

### 5.8 后台处理 vs 前台处理差异

| 特性 | 前台 (`run()`) | 后台 (`runAndLoadResults()`) |
|------|---------------|------------------------------|
| 执行方式 | 同步阻塞 | 异步非阻塞 |
| 结果加载 | 不自动加载 | 自动添加到地图 |
| 进度反馈 | 脚本可控 | QGIS 任务管理器 |
| 内存管理 | 脚本控制 | QGIS 管理 |
| 适用场景 | Python 脚本/批处理 | GUI 交互操作 |
| 错误处理 | try/except | 信号/槽 |

---

## 六、批量处理最佳实践

### 6.1 按字段值分组批处理

```python
def batch_by_field_value(input_path, group_field, process_func, output_dir):
    """按字段分组执行批处理"""
    layer = QgsVectorLayer(input_path, 'input', 'ogr')
    values = list(layer.uniqueValues(layer.fields().indexOf(group_field)))
    
    for i, val in enumerate(values):
        print(f"[{i+1}/{len(values)}] {group_field}={val}")
        subset = processing.run("native:extractbyattribute", {
            'INPUT': layer, 'FIELD': group_field,
            'OPERATOR': 0, 'VALUE': val, 'OUTPUT': 'memory:'
        })['OUTPUT']
        process_func(subset, val, output_dir)
```

### 6.2 多文件批量处理

```python
import os, glob

def batch_process_files(pattern, algorithm_id, params_template, output_dir):
    """批量处理匹配文件"""
    files = glob.glob(pattern)
    for i, file_path in enumerate(files):
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        params = dict(params_template)
        params['INPUT'] = file_path
        params['OUTPUT'] = os.path.join(output_dir, f'{base_name}_processed.gpkg')
        
        try:
            processing.run(algorithm_id, params)
            print(f"[{i+1}/{len(files)}] OK: {base_name}")
        except Exception as e:
            print(f"[{i+1}/{len(files)}] FAIL: {base_name} - {e}")

# 使用
batch_process_files(
    'D:/data/counties/*.shp',
    'native:buffer',
    {'DISTANCE': 500, 'SEGMENTS': 5, 'DISSOLVE': False},
    'D:/output/buffered/'
)
```

### 6.3 进度条与日志集成

```python
from qgis.core import QgsProcessingFeedback

class LogFeedback(QgsProcessingFeedback):
    """自定义反馈类：记录日志+控制台输出"""
    def __init__(self, log_file=None):
        super().__init__()
        self.log = open(log_file, 'w') if log_file else None
    
    def setProgressText(self, text):
        print(f"  [进度] {text}")
        if self.log:
            self.log.write(f"[PROGRESS] {text}\n")
    
    def pushInfo(self, info):
        print(f"  [信息] {info}")
        if self.log:
            self.log.write(f"[INFO] {info}\n")
    
    def reportError(self, error):
        print(f"  [错误] {error}")
        if self.log:
            self.log.write(f"[ERROR] {error}\n")
    
    def __del__(self):
        if self.log:
            self.log.close()

# 使用自定义反馈
feedback = LogFeedback('processing.log')
context = QgsProcessingContext()
alg = QgsApplication.processingRegistry().algorithmById("native:buffer")
result = alg.run({'INPUT': layer, 'DISTANCE': 100, 'OUTPUT': 'out.gpkg'}, context, feedback)
```

### 6.4 并行处理注意事项

> **警告**: QGIS Processing 的 `run()` 不是线程安全的，不能在多线程中直接调用。

```python
# 正确: 使用 subprocess 调用 qgis_process 实现并行
import subprocess, concurrent.futures

def run_qgis_process_parallel(tasks, max_workers=4):
    """用 subprocess 并行执行 qgis_process"""
    def run_task(task):
        alg_id, params = task
        json_params = json.dumps(params)
        result = subprocess.run(
            ['qgis_process', 'run', alg_id, '--json', json_params],
            capture_output=True, text=True, timeout=600
        )
        return alg_id, result.returncode, result.stdout
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_task, t) for t in tasks]
        for f in concurrent.futures.as_completed(futures):
            alg_id, code, output = f.result()
            status = "OK" if code == 0 else f"FAIL({code})"
            print(f"[{status}] {alg_id}")
```

**并行处理核心原则**:
1. 不同进程处理不同文件（无共享状态）
2. 每个进程的输出写到不同路径
3. 并行数 ≤ CPU 核心数（栅格）或 ≤ 内存/4GB（矢量）
4. GDAL 有内置 `-multi` 多线程支持，单任务即可利用多核

---

## 七、性能优化

### 7.1 空间索引预热

```python
# QGIS 加载图层时默认创建空间索引
# 对于外部生成的数据，手动验证/创建
layer = QgsVectorLayer('data.gpkg', 'layer', 'ogr')
if not layer.spatialIndex():
    print("空间索引缺失，创建中...")

# GDAL: 创建 .qix 空间索引文件
import subprocess
subprocess.run(['ogrinfo', '-sql', 'CREATE SPATIAL INDEX ON layer_name', 'data.gpkg'])
```

### 7.2 先过滤再处理

```python
# 慢: 对全量数据做缓冲区
result = processing.run("native:buffer", {
    'INPUT': 'all_points.shp', 'DISTANCE': 100, 'OUTPUT': 'out.shp'
})

# 快: 先用空间范围过滤，再处理
subset = processing.run("native:extractbyextent", {
    'INPUT': 'all_points.shp',
    'EXTENT': '120.0,122.0,30.0,32.0',  # 只处理目标区域
    'CLIP': True, 'OUTPUT': 'memory:'
})['OUTPUT']

result = processing.run("native:buffer", {
    'INPUT': subset, 'DISTANCE': 100, 'OUTPUT': 'out.shp'
})
```

**过滤优先策略**:

| 步骤 | 方法 | 效率提升 |
|------|------|---------|
| 按范围过滤 | `extractbyextent` | 10-100x（取决于数据分布） |
| 按属性过滤 | `extractbyattribute` | 10-1000x（取决于筛选比例） |
| 按表达式过滤 | `extractbyexpression` | 灵活，效果取决于表达式 |
| 只保留必要字段 | `retainfields` | 20-50%（减少IO） |

### 7.3 适当使用简化

```python
# 高精度数据在可视化场景中可先简化
simplified = processing.run("native:simplifygeometries", {
    'INPUT': 'high_detail.gpkg',
    'METHOD': 0,  # Douglas-Peucker
    'TOLERANCE': 10,  # 米（仅在投影坐标系中有效）
    'OUTPUT': 'simplified.gpkg'
})
```

### 7.4 GDAL vs Native 算法性能对比

| 操作 | Native 算法 | GDAL 算法 | 推荐 | 原因 |
|------|------------|----------|------|------|
| 投影转换 | `native:reprojectlayer` | `gdal:warpreproject` | GDAL(栅格) | 多线程+更好的内存管理 |
| 按面裁剪 | `native:clip` | `gdal:cliprasterbymasklayer` | Native(矢量) | 自动处理属性 |
| 缓冲区 | `native:buffer` | — | Native | 无GDAL等效算法 |
| 格式转换 | — | `gdal:translate` / `gdal:convertformat` | GDAL | 压缩选项丰富 |
| 等高线 | — | `gdal:contour` | GDAL | 速度快、参数丰富 |
| 栅格计算 | `native:rastercalculator` | `gdal:rastercalculator` | GDAL(大栅格) | numpy后端+多波段 |
| 栅格填充 | `native:fillnodata` | `gdal:fillnodata` | GDAL(大栅格) | 迭代插值更优 |
| 融合 | `native:dissolve` | `gdal:dissolve` | Native(复杂几何) | 更好的拓扑处理 |

**选型口诀**: 大文件用 GDAL，复杂分析用 Native，矢量大文件优先 GDAL 的 `ogr2ogr`

---

## 八、快速参考表

### 8.1 "我需要做X，用什么算法？" 场景映射表

| # | 需求场景 | 推荐算法 | 备选方案 |
|---|---------|---------|---------|
| 1 | 两个图层求相交部分 | `native:intersection` | — |
| 2 | 按行政区裁剪数据 | `native:clip` | `native:extractbylocation` |
| 3 | 计算每个面的面积 | `native:fieldcalculator` (`$area`) | `native:addgeometryattributes` |
| 4 | WGS84 转 CGCS2000 | `native:reprojectlayer` | `gdal:warpreproject`(栅格) |
| 5 | 统计每个行政区内点数 | `native:countpointsinpolygon` | `native:joinbylocationsummary` |
| 6 | 生成 DEM 等高线 | `gdal:contour` | — |
| 7 | 生成坡度图 | `native:slope` | `grass:r.slope.aspect` |
| 8 | 生成山体阴影 | `native:hillshade` | — |
| 9 | 合并多个SHP为一个 | `native:mergevectorlayers` | `gdal:convertformat`(批量→GPKG) |
| 10 | 按属性筛选要素 | `native:extractbyattribute` | `native:extractbyexpression` |
| 11 | 修复无效几何 | `native:fixgeometries` | `grass:v.clean` |
| 12 | 栅格重采样/对齐 | `gdal:warpreproject` | `native:alignraster` |
| 13 | 按字段值拆分为多个图层 | `native:splitvectorlayer` | PyQGIS循环 `extractbyattribute` |
| 14 | 点生成 Voronoi 多边形 | `native:voronoipolygons` | — |
| 15 | 计算点到最近设施距离 | `native:distancetonearesthub` | `native:shortestline` |
| 16 | DEM填充空洞 | `native:fillnodata` | `gdal:fillnodata` |
| 17 | 模糊选址（多条件叠加） | `native:intersection` × N | Graphical Modeler |
| 18 | KDE热力图 | `native:heatmapkerneldensityestimation` | `grass:v.kernel` |
| 19 | 栅格转矢量面 | `native:polygonize` | `gdal:polygonize` |
| 20 | SHP转GPKG格式 | `gdal:convertformat` | — |

### 8.2 Algorithm ID 版本变更速查表

| 算法功能 | QGIS 3.10 | QGIS 3.22 | QGIS 3.28 LTR | QGIS 3.34 LTR | 迁移建议 |
|---------|-----------|-----------|---------------|---------------|---------|
| 缓冲区 | `qgis:buffer` | `native:buffer` | `native:buffer` | `native:buffer` | 始终使用 `native:` |
| 裁剪 | `qgis:clip` | `native:clip` | `native:clip` | `native:clip` | 同上 |
| 投影转换 | `qgis:reprojectlayer` | `native:reprojectlayer` | `native:reprojectlayer` | `native:reprojectlayer` | 同上 |
| 交集/并集 | `qgis:intersection/union` | `native:intersection/union` | 同左 | 同左 | 同上 |
| DBSCAN | — | `native:dbscanclustering` | 同左 | 同左 | 3.22+可用 |
| K-means | — | `native:kmeansclustering` | 同左 | 同左 | 3.22+可用 |
| SAGA地形分析 | `saga:*` | `saga:*` | 标记弃用 | 移除（需插件） | 迁移到 `native:` |
| GRASS | `grass7:*` | `grass7:*` | `grass:*` (v8) | `grass:*` (v8) | 注意ID前缀变化 |
| PDAL点云 | — | — | — | `pdal:*` (v3.32+) | 3.32+可用 |
| 3D处理 | — | `3d:*` | `3d:*` | `3d:*` | 3.30+增强 |
| 选区运算 | `qgis:extractbylocation` | `native:extractbylocation` | 同左 | 同左 | `selectbylocation`不输出 |

### 8.3 坐标系速查（PyQGIS）

```python
# 常用CRS创建方式
from qgis.core import QgsCoordinateReferenceSystem

# 方式1: EPSG代码
crs = QgsCoordinateReferenceSystem('EPSG:4527')   # CGCS2000 3度带 39

# 方式2: WKT
crs = QgsCoordinateReferenceSystem.fromWkt('PROJCS["CGCS2000 / 3-degree Gauss-Kruger zone 39",...]')

# 方式3: 从图层获取
layer = QgsVectorLayer('data.shp')
source_crs = layer.crs()

# 常用EPSG
EPSG_4326 = QgsCoordinateReferenceSystem('EPSG:4326')   # WGS84
EPSG_3857 = QgsCoordinateReferenceSystem('EPSG:3857')   # Web Mercator
EPSG_4490 = QgsCoordinateReferenceSystem('EPSG:4490')   # CGCS2000 地理
EPSG_4527 = QgsCoordinateReferenceSystem('EPSG:4527')   # CGCS2000 GK 39
```

### 8.4 输出格式速查（矢量）

| 格式 | 输出路径格式 | 适用场景 | 注意 |
|------|------------|---------|------|
| GeoPackage | `'output.gpkg'` | 推荐默认格式 | 单文件、UTF-8、无大小限制 |
| Shapefile | `'output.shp'` | 兼容旧系统 | 字段名10字符限制、GBK编码 |
| GeoJSON | `'output.geojson'` | Web交换 | 人可读、所有库支持 |
| 内存图层 | `'memory:'` | 中间步骤 | 仅当前脚本有效 |
| 临时输出 | `'TEMPORARY_OUTPUT'` | GUI环境 | QGIS自动管理生命周期 |
| PostGIS | `'postgres://...'` | 企业级 | 需数据库连接配置 |

---

## 附录: 常用 Algorithm ID 索引

### 矢量分析 Top 15
```
native:buffer              native:clip                 native:intersection
native:union               native:difference           native:dissolve
native:simplifygeometries  native:fixgeometries        native:reprojectlayer
native:extractbyexpression native:extractbylocation    native:fieldcalculator
native:mergevectorlayers   native:countpointsinpolygon native:joinattributestable
```

### 栅格分析 Top 10
```
gdal:warpreproject         native:slope                native:aspect
native:hillshade           native:rastercalculator     native:fillnodata
gdal:contour               native:reclassifybytable    gdal:cliprasterbymasklayer
gdal:translate
```

### 数据转换 Top 8
```
gdal:convertformat         gdal:translate              gdal:merge
native:polygonize          native:rasterize            native:multiparttosingleparts
gdal:buildvirtualraster    native:refactorfields
```

---

> **文档维护准则**: Algorithm ID 以 `qgis_process list` 实际输出为准。本文档基于 QGIS 3.34 LTR / 3.38 验证。发现错误或新增算法请通过 feedback 机制提交更新。
> **参考文档**: [QGIS Processing 官方文档](https://docs.qgis.org/latest/en/docs/user_manual/processing/)


<!-- wm:坤图_GIS:V1.0 -->
