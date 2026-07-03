# GlobalMapper | 关联：17_GlobalMapper.md 18_FME_Form与Flow.md 12_ArcGIS_Pro.md | 最新验证：2026年6月

> v26.2（2025年10月发布）：万能数据格式转换器 + 地形分析 + LiDAR处理专家
> 数据来源：bluemarblegeo.com / reachsoft.com.cn（官方中文代理）/ 行业评测

---

## 一、软件定位

| 项目 | 内容 |
|------|------|
| **开发商** | Blue Marble Geographics（美国） |
| **中国代理** | 北京睿思创科（reachsoft.com.cn） |
| **授权** | 标准版 / Pro版（LiDAR扩展）|
| **核心定位** | 通用 GIS 数据查看/转换/分析工具，300+格式支持 |
| **策略定位** | "万能数据转换器" + "快速地形分析工具" |
| **最新版本** | v26.2 (2025.10) |
| **上一代** | v25.x → v26.1(2025.05) → v26.2(2025.10) |
| **下载** | https://www.bluemarblegeo.com/global-mapper/（14天免费试用） |

### v26.2 关键新特性

| 特性 | 说明 |
|------|------|
| **UI重构** | 用户驱动的界面改进，更直观的操作面板 |
| **动画工具** | 支持时空数据可视化动画 |
| **LiDAR着色器缩放** | 更直观的直方图调节，优化点云渲染 |
| **智能数字化** | 增强的矢量化/数字化辅助功能 |
| **脚本工具栏** (v26.1) | 内置脚本运行工具，支持 Global Mapper Script 自动化 |

---

## 二、数据格式支持（核心竞争力）

### 2.1 支持格式统计

```
矢量格式：SHP/GeoJSON/KML/GML/DXF/DWG/TAB/MIF/MID/GPKG/FileGDB ...
栅格格式：GeoTIFF/IMG/JP2/ECW/MrSID/HDF/NetCDF ...
高程格式：DEM/DTED/SRTM/ASTER GDEM/LAS/LAZ ...
在线源：  天地图/Google Earth/OSM/Bing Maps/WMS/WMTS ...
```

> 总数超过 350 种格式（业内最全）

### 2.2 最常用转换场景

| 源格式 | 目标格式 | 典型场景 |
|--------|---------|---------|
| .dwg (CAD) | .shp / .gpkg | CAD→GIS 转换 |
| .las / .laz | .tif / .dem | LiDAR→DEM |
| .ecw / .jp2 | .tif (GeoTIFF) | 影像格式转换 |
| .kml / .kmz | .shp / .dxf | Google Earth→GIS |
| .txt / .csv (含坐标) | .shp / .gpkg | 表格数据→空间数据 |

---

## 三、核心功能模块

### 3.1 数据查看与浏览

| 功能 | 操作 |
|------|------|
| **多格式叠加** | 直接拖放文件到窗口，自动识别格式 |
| **在线底图** | 加载天地图/OSM/Google Earth 作为底图 |
| **3D视图** | 切换为3D视图，DEM拉升地形 |
| **属性查询** | 点击要素查看属性，支持属性筛选和统计 |

### 3.2 数据转换（特色功能）

```
操作流程：
1. 加载源数据（支持拖放/File→Open）
2. 右键图层 → Layer → Export
3. 选择目标格式（下拉列表覆盖所有支持格式）
4. 配置选项：
   - 坐标系投影（可选择/定义/从源继承）
   - 属性字段选择
   - 几何类型过滤
   - 编码设置
5. 导出
```

**批量转换**：File → Batch Convert/Reproject → 添加多个文件 → 统一设置 → 一键批量执行

### 3.3 地形分析（Pro版核心）

| 工具 | 功能 | 应用 |
|------|------|------|
| **等高线生成** | DEM → 等高线矢量 | 地形图生产 |
| **坡度/坡向分析** | Slope / Aspect | 选址/水土保持 |
| **通视分析** | Viewshed / Line of Sight | 军事/通信/规划 |
| **流域分析** | Watershed / Flow Accumulation | 水文分析 |
| **体积计算** | Cut & Fill Volume | 土方量计算 |
| **地形剖面** | Path Profile | 路线设计 |
| **山体阴影** | Hillshade | 制图渲染 |

### 3.4 LiDAR 点云处理（Pro版专属）

| 功能 | 说明 |
|------|------|
| **点云加载** | LAS/LAZ/ZLAS 高效加载和渲染 |
| **点云分类** | 自动地面点分类（噪声/地面/植被/建筑） |
| **点云过滤** | 按分类码/高程/回波次数/强度过滤 |
| **DEM/DSM提取** | 从点云提取数字高程/表面模型 |
| **点云编辑** | 手动重分类、剖面浏览、点选编辑 |
| **着色器** | 按高程/分类/强度/LiDAR属性着色（v26.2增强） |

---

## 四、脚本自动化

### 4.1 Global Mapper Script (.gms)

```
// 示例：批量将SHP转换为KML
GLOBAL_MAPPER_SCRIPT VERSION=1.00

// 设置工作目录
DIR_LOOP_START DIRECTORY="D:\data\shp" FILENAME_MASKS="*.shp"
  IMPORT FILENAME="%FNAME_W_DIR%"
  EXPORT_VECTOR FILENAME="D:\data\kml\%FNAME_WO_EXT%.kml" TYPE="KML"
  UNLOAD_ALL
DIR_LOOP_END
```

### 4.2 常用脚本命令

| 命令 | 功能 |
|------|------|
| `IMPORT` | 加载数据 |
| `EXPORT_VECTOR` | 导出矢量 |
| `EXPORT_RASTER` | 导出栅格 |
| `EXPORT_ELEVATION` | 导出高程数据 |
| `GENERATE_CONTOURS` | 生成等高线 |
| `GENERATE_WATERSHEDS` | 流域分析 |
| `DIR_LOOP_START` / `DIR_LOOP_END` | 批量循环 |
| `UNLOAD_ALL` | 清空工作区 |

---

## 五、与其他工具的协同

### 5.1 GlobalMapper vs FME 定位差异

| 维度 | GlobalMapper | FME |
|------|-------------|-----|
| 核心定位 | 数据查看器+转换器 | 专业ETL引擎 |
| 格式支持 | 350+ (侧重查看) | 450+ (侧重流程) |
| 空间分析 | 强（地形/LiDAR/视域） | 弱（需配合GIS） |
| 图形界面 | 地图为中心 | 流程为中心(Workbench) |
| 自动化 | 脚本 (.gms) | 工作流 (.fmw) |
| 价格 | 中 | 高 |
| **最佳搭配** | 快速格式转换+地形分析 | 复杂ETL+数据流处理 |

### 5.2 典型协同场景

```
GlobalMapper → 快速格式转换 → ArcGIS Pro / QGIS 深度分析
GlobalMapper → LiDAR→DEM → FME → 数据入库
AutoCAD DWG → GlobalMapper → GeoPackage → QGIS 制图
```

---

## 六、Global Mapper Script 高级编程 ⭐ V4.0深度扩充

### 6.1 脚本变量与循环

```
// Global Mapper Script 变量系统
GLOBAL_MAPPER_SCRIPT VERSION=1.00

// 定义变量
DEFINE_VAR NAME="INPUT_DIR" VALUE="D:\YourGISData\raw"
DEFINE_VAR NAME="OUTPUT_DIR" VALUE="D:\YourGISData\processed"

// 数值变量与数学运算
DEFINE_VAR NAME="BUFFER_DIST" VALUE="100"
DEFINE_VAR NAME="SCALE_FACTOR" VALUE="1.5"

// 条件判断（通过预设变量和 MASK 匹配实现）
DIR_LOOP_START DIRECTORY="%INPUT_DIR%" FILENAME_MASKS="*.shp"
  IMPORT FILENAME="%FNAME_W_DIR%"
  // 根据 GISPACE 变量选择不同导出坐标系
  EXPORT_VECTOR FILENAME="%OUTPUT_DIR%\%FNAME_WO_EXT%.gpkg" TYPE="GPKG"
  UNLOAD_ALL
DIR_LOOP_END
```

```
脚本变量说明：
  %FNAME_W_DIR%     → 完整文件路径（含目录）
  %FNAME_WO_EXT%    → 文件名（不含扩展名）
  %FNAME_W_EXT%     → 文件名（含扩展名）
  %GISPACE%         → 当前工作空间路径
  %DATE%            → 当前日期
  DEFINE_VAR        → 自定义变量定义
```

### 6.2 地形分析批处理脚本

```
// 批量DEM生成等高线+坡度+山体阴影
GLOBAL_MAPPER_SCRIPT VERSION=1.00
DIR_LOOP_START DIRECTORY="D:\DEM" FILENAME_MASKS="*.tif"
  IMPORT FILENAME="%FNAME_W_DIR%" TYPE="AUTO"

  // 生成等高线（10米间距）
  GENERATE_CONTOURS ELEV_INTERVAL=10 \
    ELEV_UNITS="METERS" \
    MIN_ELEV="AUTO" MAX_ELEV="AUTO" \
    GEN Spicer_ELEV_FILE="D:\Output\Contours\%FNAME_WO_EXT%_contour.shp"

  // 生成坡度图
  CALC_SLOPE \
    SLOPE_UNITS="DEGREES" \
    SLOPE_DIR="D:\Output\Slope\%FNAME_WO_EXT%_slope.tif"

  // 生成山体阴影
  HILLSHADE AZIMUTH=315 ALTITUDE=45 \
    SHADOW_FILE="D:\Output\Hillshade\%FNAME_WO_EXT%_hillshade.tif"

  UNLOAD_ALL
DIR_LOOP_END
```

```
常用地形分析脚本命令：
  GENERATE_CONTOURS     → 等高线生成
  CALC_SLOPE            → 坡度计算（DEGREES/PERCENT）
  CALC_SLOPE_DIR        → 坡向计算
  HILLSHADE             → 山体阴影
  GENERATE_WATERSHEDS   → 流域分析
  CALC_VOLUME           → 体积计算（土方量）
  PATH_PROFILE          → 地形剖面
  VIEW_SHED             → 通视分析
  COMBINE_TERRAIN       → 地形数据合并
```

### 6.3 Python + Global Mapper 集成

```python
import subprocess
import json
import os

# 方法一：subprocess 调用 Global Mapper 脚本
def run_gms_script(script_path):
    """执行 Global Mapper Script 文件"""
    gm_path = r"C:\Program Files\GlobalMapper\global_mapper64.exe"
    result = subprocess.run(
        [gm_path, script_path],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    if result.returncode != 0:
        raise RuntimeError(f"Script failed: {result.stderr}")
    return result.stdout

# 方法二：生成并执行动态脚本
def batch_convert(input_dir, output_dir, target_format="KML"):
    """动态生成转换脚本并执行"""
    script_lines = [
        "GLOBAL_MAPPER_SCRIPT VERSION=1.00",
        f'DIR_LOOP_START DIRECTORY="{input_dir}" FILENAME_MASKS="*.shp"',
        '  IMPORT FILENAME="%FNAME_W_DIR%"',
        f'  EXPORT_VECTOR FILENAME="{output_dir}\\%FNAME_WO_EXT%.{target_format.lower()}" TYPE="{target_format}"',
        '  UNLOAD_ALL',
        'DIR_LOOP_END'
    ]
    script_content = '\n'.join(script_lines)

    script_file = os.path.join(output_dir, "_temp_convert.gms")
    with open(script_file, 'w') as f:
        f.write(script_content)

    return run_gms_script(script_file)

# 使用示例
batch_convert(r"D:\YourGISData\shp", r"D:\YourGISData\kml", "KML")
```

```
参数传递技巧：
  - 复杂参数通过动态生成 .gms 脚本传入（而非命令行参数）
  - 临时脚本用完后及时清理，避免残留
  - 大批量任务建议分批执行（每批≤500文件），避免内存溢出

结果解析：
  - 检查 returncode 判断成功/失败
  - 捕获 stderr 获取错误详情
  - 导出结果文件检查：校验文件大小 > 0 && 格式可读
```

---

## 七、LiDAR 点云深度处理 ⭐ V4.0新增

### 7.1 点云自动分类参数调优

```
点云自动分类配置（Global Mapper Pro）：

地面点分类核心参数：
  ┌────────────────────────────────────────────────────┐
  │ 参数                  │ 推荐值       │ 说明        │
  ├────────────────────────────────────────────────────┤
  │ Max Ground Point Spacing │ 15m       │ 地面点最大间距  │
  │ Bin Size（网格大小）      │ 5m        │ 分类网格分辨率  │
  │ Terrain Slope Threshold  │ 30°       │ 地形坡度阈值    │
  │ Iterations               │ 50-100    │ 迭代次数       │
  │ Thin Point Reduction      │ 开启       │ 降采样加速     │
  └────────────────────────────────────────────────────┘

建筑物/植被分类：
  - 高度阈值：建筑物 > 3m，植被 > 0.5m
  - 点密度阈值：建筑物点密度 > 植被
  - 回波次数：植被多回波，建筑物少回波
  - 推荐流程：先地面点分类 → 再按高程分层 → 最后按密度/回波细分

噪声点识别与去除：
  - 离群点检测（Isolated Point Removal）
  - 阈值：邻域半径内点数 < 3 视为噪声
  - 高度异常点：超出统计范围（均值±3σ）标记为噪声
```

### 7.2 点云→DEM 精细流程

```
LAS → 地面点过滤 → DEM插值 → 空洞填补 → DEM平滑 → 导出

各步骤参数建议和常见问题：

Step 1: 地面点过滤
  - 工具：LiDAR → Filter by Classification → Ground Points Only
  - 或自动分类后提取分类码=2的点（ASPRS标准）
  - 常见问题：陡坡区域地面点被误分类为非地面
    → 解决：降低 Terrain Slope Threshold（从30°降至45°）

Step 2: DEM插值
  - 插值方法：TIN / IDW / Kriging
  - 推荐地形平缓区：TIN（精度最高）
  - 推荐地形复杂区：IDW（搜索半径=点间距2-3倍）
  - 分辨率：建议原始点密度的1/2~1/3（如点间距1m → DEM 1-2m）

Step 3: 空洞填补
  - 工具：Analysis → Fill Gaps in Elevation Grid
  - 小空洞（<5个像元）：线性插值自动填补
  - 大空洞：邻近采样 + 趋势面拟合
  - 常见问题：水域空洞
    → 解决：先提取水域范围，单独处理（设为固定高程/拉平）

Step 4: DEM平滑
  - 工具：Analysis → Elevation Grid Filter
  - 低通滤波核大小：3×3 或 5×5
  - 注意：不要过度平滑，保留地形细节
  - 仅对插值区域平滑，原始高程保持不变

Step 5: 导出
  - 格式：GeoTIFF（推荐）/ SRTM / IMG / BIL
  - 坐标系：确保元数据正确写入（CRS Profile）
  - 精度：Float32（推荐）或 Float64
```

### 7.3 剖面分析与体积计算

```
任意路径剖面提取：
  工具：3D Viewer → Path Profile
  操作：
    1. 在3D视图中用数字化工具画一条路径
    2. 自动生成剖面图（高程 vs 距离）
    3. 可同时显示多个地形的叠加剖面
  导出：File → Export → Profile to CSV/XY

土方量计算（设计面 vs 现状面）：
  工具：Analysis → Cut and Fill Volume
  步骤：
    1. 加载现状面 DEM（survey surface）
    2. 加载设计面 DEM（design surface）或定义平面高程
    3. 计算结果：
       - Cut Volume（挖方量）
       - Fill Volume（填方量）
       - Net Volume（净方量）
    4. 导出土方量报告：CSV/图像

蓄水容积计算：
  工具：Analysis → Volume Calculation → Water Volume
  操作：
    1. 加载湖盆/水库底部 DEM
    2. 定义最高水位高程
    3. 自动计算每个高程对应的面积和容积
    4. 生成 高程-面积-容积 曲线（导出 CSV）
```

### 7.4 多期点云变化检测

```
两期DEM差异分析：
  工具：Analysis → Compare Elevation Grids
  步骤：
    1. 加载两期 DEM（需统一坐标系和分辨率）
    2. 计算 DEM_diff = DEM_T2 - DEM_T1
    3. 正值 = 沉积/堆积，负值 = 侵蚀/下切
    4. 按阈值分类：微小变化（<0.1m）/ 显著变化（>0.5m）

变化区域自动提取：
  步骤：
    1. DEM差异图 → 设定变化阈值（如 |差值| > 0.5m）
    2. 栅格转矢量：变化区域 → 多边形提取
    3. 统计变化面积：按变化类型分类汇总
    4. 输出：变化区域矢量图 + 统计报表

报告生成：
  - 变化检测结果 → 导出 GeoTIFF（差异图）
  - 变化区域多边形 → 导出 Shapefile
  - 统计数据 → 导出 CSV
  - 最终整合为完整的变化检测报告
```

---

## 八、坐标转换实战 ⭐ V4.0新增

### 8.1 批量坐标系转换

```
三参数/七参数配置：
  - 工具：Tools → Projection → Coordinate System Setup
  - 三参数：DX, DY, DZ（平移）
  - 七参数：DX, DY, DZ, RX, RY, RZ, Scale（平移+旋转+缩放）
  - 常用中国区域参数（示例，需实测校正）：

    CGCS2000 → WGS84 七参数（局部区域）：
      DX: -24.0  DY: 123.0  DZ: 94.0
      RX: -0.000003  RY: -0.000003  RZ: 0.000006
      Scale: 0.0000015

转换参数文件导入：
  - 支持格式：.gtx（NTv2 格式）/ .gsb（NTv1 格式）
  - 导入路径：Tools → Projection → Datum Shift Grid
  - 常用：中国境内 CGCS2000→WGS84 换带表
  - 注意：参数精度取决于区域，离参数测量点越远误差越大

批量重投影脚本：
  GLOBAL_MAPPER_SCRIPT VERSION=1.00
  DIR_LOOP_START DIRECTORY="D:\data\CGCS2000" FILENAME_MASKS="*.shp"
    IMPORT FILENAME="%FNAME_W_DIR%"
    // 设置目标坐标系
    SET_PROJ PROJ_NAME="EPSG:4326"
    EXPORT_VECTOR FILENAME="D:\data\WGS84\%FNAME_WO_EXT%.shp" TYPE="SHP"
    UNLOAD_ALL
  DIR_LOOP_END
```

### 8.2 自定义投影定义

```
自定义投影参数配置：
  工具：Tools → Configuration → Projection → Custom

常见地方坐标系配置要点：
  1. 选择基准面（Datum）：最接近的已知基准面
  2. 定义椭球参数（如需）：
     - Semi-Major Axis（长半轴）
     - Inverse Flattening（扁率倒数）
  3. 定义投影方法：
     - 横轴墨卡托（Transverse Mercator）—— 最常用
     - 兰伯特等角圆锥（Lambert Conformal Conic）—— 省级
     - 双标准纬线等角圆锥（Albers）—— 国家级
  4. 定义投影参数：
     - 中央经线（Longitude of Origin）
     - 原点纬度（Latitude of Origin）
     - 比例因子（Scale Factor）
     - 东偏/北偏（False Easting / False Northing）
```

### 8.3 常见转换问题

```
CGCS2000 → WGS84（全球 vs 中国区域）：
  ┌──────────────────────────────────────────────────────┐
  │ 情景           │ 误差量级    │ 说明                    │
  ├──────────────────────────────────────────────────────┤
  │ 直接 EPSG 等同   │ < 0.1m     │ 同一椭球，直接等同即可    │
  │ 中国境内三参数   │ 1-5m       │ 适用于小范围/低精度需求    │
  │ 中国境内七参数   │ 0.01-0.5m  │ 高精度，需实测参数         │
  │ 全球区域         │ 无通用参数   │ 建议使用大地水准面模型     │
  └──────────────────────────────────────────────────────┘

  注意：CGCS2000 与 WGS84 椭球参数几乎一致，
  在多数应用中可视为等同（差异<0.1m），
  坐标差异主要来自平移参数。

高斯3度带 → 6度带换带：
  方法一（GUI）：
    1. 加载数据 → 确认当前为3度带（如 EPSG:4547 = CGCS2000 3度带 39度）
    2. Tools → Projection → Assign Projection → 选择目标6度带
    3. File → Export → 导入到新坐标系

  方法二（脚本批量）：
    GLOBAL_MAPPER_SCRIPT VERSION=1.00
    IMPORT FILENAME="D:\data\zone39_3degree.shp"
    SET_PROJ PROJ_NAME="EPSG:4529"  // CGCS2000 / 6度带 39度
    EXPORT_VECTOR FILENAME="D:\data\zone39_6degree.shp" TYPE="SHP"

  换带对照表（部分）：
    3度带 → 6度带：
      带38 → 带38（不跨带）
      带39 → 带39（不跨带）
      带40 → 带40（不跨带）
      带41 → 带42（跨带！注意）
```

---

## 九、实用技巧

### 9.1 中文环境设置

```
Tools → Configuration → General → Language
如遇 Shapefile 中文乱码：
  Layer → Control Center → Options → 选择编码 → UTF-8 / GBK
```

### 9.2 快速配准扫描地图

```
1. 加载扫描地图（.tif/.jpg）
2. 右键图层 → Rectify (Georeference)
3. 在图上选取已知坐标点 → 输入坐标
4. 至少3个控制点 → 选择配准方法 → 导出
```

### 9.3 大范围DEM快速浏览

```
1. 加载DEM
2. 3D View → 开启3D地形渲染
3. Hillshade叠加：图层右键 → Shader Options → Hillshade
4. 调整垂直拉伸比例获得最佳视觉效果
```

---

## 十、常见问题 ⭐ V4.0更新

| 问题 | 原因 | 方案 |
|------|------|------|
| 加载大文件卡死 | 内存不足 | 64位版本 + 文件太大可先裁剪 |
| CAD文字转为矢量后乱码 | 字体映射 | 导出时设置正确的Shapefile编码 |
| DEM坐标系错误 | 坐标元数据缺失 | 手动设置：Layer → Projection |
| 点云显示不全 | 默认显示密度限制 | 3D Viewer → 增大显示点数上限 |

---

> 关联阅读：`18_FME_Form与Flow.md`（FME ETL 对标） | `24_遥感与GEE.md`（LiDAR章节） | `12_ArcGIS_Pro.md`（深度分析）


<!-- wm:坤图_GIS:V1.0 -->
