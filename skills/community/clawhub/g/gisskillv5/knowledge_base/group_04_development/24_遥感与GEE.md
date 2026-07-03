# 遥感影像处理与LiDAR | 关联：25_三维GIS与数字孪生.md 21_Python_GIS生态.md | 来源：旧第十八篇

# 第十八篇：遥感影像处理与解译

> 来源：ArcGIS Pro Image Analyst 影像分类向导 + 豆包GIS专家知识框架
> 最后更新：2026-05-23 | 核心要点：预处理→增强→分类→精度评估→变化检测全流程

---

## 18.1 遥感影像基础概念

### 18.1.1 影像数据模型

| 概念 | 说明 | GIS 对应 |
|------|------|---------|
| **波段（Band）** | 特定电磁波范围的数据层 | 栅格数据集中的单个波段 |
| **像元（Pixel/Cell）** | 影像最小单元 | 栅格单元格 |
| **空间分辨率** | 单个像元覆盖的地面尺寸 | Cellsize（如 0.5m/10m/30m） |
| **光谱分辨率** | 波段数量和宽度 | 多光谱(4-10波段) vs 高光谱(100+波段) |
| **辐射分辨率** | 传感器对电磁辐射的敏感度 | 位深度（8bit/16bit） |
| **时间分辨率** | 重访周期 | 天/周/月 |

### 18.1.2 常见遥感数据源

| 卫星/传感器 | 空间分辨率 | 波段数 | 重访周期 | 典型应用 |
|-------------|-----------|--------|---------|---------|
| **Landsat 8/9** | 15m(全色)/30m(多光谱) | 11 | 16天 | 土地利用/植被/水体 |
| **Sentinel-2** | 10m/20m/60m | 13 | 5天 | 农业监测/灾害评估 |
| **高分系列(GF)** | 0.8m~50m | 4~8 | 不定 | 国产数据/国土监测 |
| **WorldView-3** | 0.31m(全色)/1.24m | 16 | <1天 | 城市规划/精细制图 |
| **无人机航拍** | 0.02m~0.1m | RGB/多光谱 | 按需 | 测绘/农业/巡检 |

---

## 18.2 影像预处理流程

### 18.2.1 标准预处理六步法

```
原始影像
  → 1. 辐射定标（DN值 → 辐射亮度/反射率）
  → 2. 大气校正（去除大气散射/吸收影响）
  → 3. 正射校正（消除地形+传感器倾斜变形）
  → 4. 几何配准（多时相影像对齐）
  → 5. 影像融合（全色+多光谱 → 高分多光谱）
  → 6. 镶嵌与裁剪（多景拼接+研究区提取）
```

### 18.2.2 辐射定标与大气校正

**辐射定标**：将 DN 值转换为物理量（辐射亮度/表观反射率）。

```python
# ArcPy 辐射定标（Apparent Reflectance）
import arcpy
arcpy.ia.ApplyRadiometricCalibration(
    in_raster="LC08_L1TP.tif",
    out_raster="LC08_TOA.tif",
    calibration_type="REFLECTANCE"  # 或 "RADIANCE"
)
```

**大气校正**：FLAASH（Fast Line-of-sight Atmospheric Analysis of Spectral Hypercubes）或 QUAC（Quick Atmospheric Correction）：

```python
# ArcGIS Pro 大气校正（需 Spatial Analyst + Image Analyst）
arcpy.ia.ApplyAtmosphericCorrection(
    in_raster="LC08_TOA.tif",
    out_raster="LC08_SurfaceRef.tif",
    correction_method="QUAC",  # 快速；FLAASH 需更多参数
    atmospheric_model="TROPICAL",
    aerosol_model="RURAL"
)
```

### 18.2.3 影像融合（Pansharpening）

将高分辨率全色波段与低分辨率多光谱融合：

| 方法 | 原理 | 优点 | 缺点 |
|------|------|------|------|
| **IHS** | 色彩空间变换 | 简单快速 | 光谱失真 |
| **Brovey** | 波段比值 | 增强对比度 | 仅3波段 |
| **Gram-Schmidt** | 正交变换 ⭐ | 光谱保真度高 | 计算量大 |
| **NNDiffuse** | 最近邻扩散 ⭐ | 速度快+保真 | ArcGIS Pro 支持 |
| **PCA** | 主成分替换 | 信息量集中 | 物理意义弱 |

```python
arcpy.ia.Pansharpen(
    in_raster="MultiSpec_4band.tif",
    panchromatic_image="PAN_0.5m.tif",
    out_raster="Pansharpened.tif",
    pansharpening_type="Gram-Schmidt",
    sensor="UNKNOWN"
)
```

### 18.2.4 几何配准（Georeferencing）

多时相影像对齐的关键步骤：

```python
# 自动配准（需控制点图层或参考影像）
arcpy.ia.AutoRegister(
    in_raster="待配准影像.tif",
    reference_raster="基准影像.tif",
    out_raster="配准后影像.tif",
    transformation_type="POLYORDER1",  # 一阶多项式(平移+旋转+缩放)
    max_rms="0.5"
)
```

---

## 18.3 影像增强与指数计算

### 18.3.1 常用遥感指数

| 指数 | 公式 | 用途 |
|------|------|------|
| **NDVI** | (NIR - Red) / (NIR + Red) | 植被覆盖度 [-1, 1] |
| **NDWI** | (Green - NIR) / (Green + NIR) | 水体提取 |
| **NDBI** | (SWIR - NIR) / (SWIR + NIR) | 建筑用地提取 |
| **SAVI** | (NIR - Red) / (NIR + Red + L) × (1+L) | 土壤调节植被指数 |
| **EVI** | 2.5×(NIR-Red)/(NIR+6×Red-7.5×Blue+1) | 增强植被指数（高植被区） |
| **TVI** | √(NDVI + 0.5) | 变换植被指数（放大低值） |

```python
# ArcPy 指数计算
# NDVI
arcpy.ia.BandArithmetic(
    in_raster="影像.tif",
    method="NDVI",
    band_indexes="NIR 5;Red 4",  # 指定对应波段索引
    out_raster="NDVI.tif"
)

# 自定义波段运算
arcpy.ia.RasterCalculator(
    expression="(NIR - Red) / (NIR + Red)",
    layers={"NIR": "Band5", "Red": "Band4"},
    out_raster="Custom_NDVI.tif"
)
```

### 18.3.2 主成分分析（PCA）

降维压缩，去冗余：

```python
arcpy.ia.PrincipalComponents(
    in_raster="多波段影像.tif",
    out_multiband_raster="PCA_Bands.tif",
    number_of_components=3,  # 前3个主成分通常含95%+信息
    output_route_file="PCA_Stats.txt"
)
```

---

## 18.4 影像分类

### 18.4.1 ArcGIS Pro 影像分类向导 10 步流程

```
步骤1：配置影像 → 选择分类影像 + 定义波段组合
步骤2：分割影像 → 可选，生成影像对象(Segment)提高分类精度
步骤3：选择分类方法 → 监督/非监督
步骤4：选择分类器 → ISO聚类/KNN/最大似然/随机森林/SVM
步骤5：创建训练样本 → 交互式绘制 + 实地采样导入
步骤6：评估训练样本 → 直方图/散点图检查可分离性
步骤7：训练分类器 → 执行分类
步骤8：合并类 → 归并相似类别
步骤9：精度评估 → 混淆矩阵/Kappa
步骤10：后处理 → 众数滤波/边界清理/面积阈值
```

### 18.4.2 五种分类器对比

| 分类器 | 类型 | 原理 | 样本需求 | 速度 | 精度 | 适用场景 |
|--------|------|------|---------|------|------|---------|
| **ISO聚类** | 非监督 | 迭代自组织 | 无需样本 | 慢 | 一般 | 快速概览/先验知识不足 |
| **KNN**（K近邻） | 监督 | 距离投票 | 适量 | 慢 | 较高 | 非线性可分数据 |
| **最大似然** | 监督(参数) | 概率密度函数 | 较多(需正态分布) | 中等 | 中等 | 正态分布数据 |
| **随机森林** ⭐ | 监督(机器学习) | 多决策树投票 | 适量 | 中等 | 高 | **推荐首选**，稳健性好 |
| **SVM**（支持向量机） | 监督(机器学习) | 最优超平面 | 可较少 | 慢(大样本) | 很高 | 高维数据/小样本场景 |

### 18.4.3 训练样本创建策略

| 策略 | 方法 | 优点 | 注意事项 |
|------|------|------|---------|
| **分层随机采样** | 按类别比例随机抽取 | 统计代表性强 | 需先验类面积比例 |
| **均匀网格采样** | 规则网格选点 | 空间覆盖均匀 | 可能忽略小类别 |
| **交互式绘制** | 目视解译勾画 | 灵活精准 | 主观性、耗时长 |
| **GPS/野外采集** | 实地采样+GPS坐标 | 最准确 | 成本高、范围受限 |

**样本数量要求**：各类别至少 **10~30 倍波段数** 的训练样本。例如 4 波段影像，每类至少 40 个像元。

### 18.4.4 影像分割（Segmentation）

在分类前将影像分割为同质对象（超像元），可大幅提升分类精度：

```python
# Segment Mean Shift 分割
arcpy.ia.SegmentMeanShift(
    in_raster="影像.tif",
    out_raster="Segments.tif",
    spectral_detail=15.0,   # 光谱细节权重 (1.0~20.0)
    spatial_detail=15.0,    # 空间细节权重 (1.0~20.0)
    min_segment_size=20,    # 最小分割对象(像元数)
    band_indexes="1 2 3 4"
)
```

### 18.4.5 分类执行（ArcPy）

```python
# 随机森林分类
arcpy.ia.TrainRandomTreesClassifier(
    in_raster="Segments.tif",
    in_training_features="TrainSamples.shp",
    out_classifier_definition="RF_Classifier.ecd",
    max_num_trees=100,
    max_tree_depth=30,
    sample_size_mode="ALL"
)

arcpy.ia.ClassifyRaster(
    in_raster="Segments.tif",
    in_classifier_definition="RF_Classifier.ecd",
    out_raster="Classified.tif"
)
```

---

## 18.5 精度评估

### 18.5.1 混淆矩阵（Confusion Matrix）

核心工具，横轴 = 预测类，纵轴 = 实际类：

```
             预测A  预测B  预测C  合计
实际A        45      3      2     50
实际B         5     38      7     50
实际C         2      4     44     50
```

| 指标 | 公式 | 含义 |
|------|------|------|
| **总体精度(OA)** | 对角线总和 / 总样本 | 整体正确率 → (45+38+44)/150 = 84.7% |
| **生产者精度(PA)** | 对角值 / 列合计 | 某类被正确分类的比例（漏分误差 = 1-PA） |
| **用户精度(UA)** | 对角值 / 行合计 | 分类结果中某类实际正确的比例（错分误差 = 1-UA） |
| **Kappa 系数** | (OA - Pe) / (1 - Pe) | 消除随机一致后的分类精度 |

**Kappa 系数评价标准**：
| Kappa | 一致性程度 |
|-------|-----------|
| < 0 | 差 |
| 0.0 ~ 0.20 | 轻微 |
| 0.21 ~ 0.40 | 一般 |
| 0.41 ~ 0.60 | 中等 |
| 0.61 ~ 0.80 | 实质 |
| 0.81 ~ 1.00 | 几乎完美 |

### 18.5.2 验证样本与训练样本分离

**黄金法则**：验证样本与训练样本必须严格分离（禁止重叠）。

```python
# 子集划分：70%训练 / 30%验证
arcpy.management.SubsetFeatures(
    in_features="AllSamples.shp",
    out_training_feature_class="TrainSamples_70.shp",
    out_test_feature_class="ValidateSamples_30.shp",
    subset_size_units="PERCENTAGE_OF_INPUT",
    subset_size=70  # 训练集比例
)

# 计算混淆矩阵
arcpy.ia.ComputeConfusionMatrix(
    in_accuracy_points="ValidateSamples_30.shp",
    in_classified_raster="Classified.tif",
    out_confusion_matrix="Confusion_Matrix.dbf"
)
```

---

## 18.6 变化检测

### 18.6.1 方法分类

| 方法 | 原理 | 输出 | 适用 |
|------|------|------|------|
| **差值法** | 后-前（单波段/指数） | 变化幅度图 | 简单快速，单一指标 |
| **比值法** | 后/前 | 相对变化 | 消除光照差异 |
| **分类后比较** ⭐ | 两期分类结果逐像元对比 | 变化矩阵（From→To） | **标准方法**，信息丰富 |
| **变化向量分析(CVA)** | 多维空间中变化方向和幅度 | 变化强度+方向 | 多波段同时变化检测 |
| **PCA差值** | 两期PCA成分相减 | 变化分量 | 多维变化压缩 |

### 18.6.2 分类后比较（推荐方法）

```python
# 两期影像分别分类
# 假设已有 Classified_2020.tif 和 Classified_2025.tif

# 变化检测：From-To 矩阵
arcpy.ia.ComputeChange(
    in_raster_from="Classified_2020.tif",
    in_raster_to="Classified_2025.tif",
    out_raster="ChangeDetect.tif",
    compute_transition=1,  # 使用颜色映射
    from_classes="CLASS_2020",
    to_classes="CLASS_2025",
    filter_method="NONE"
)
```

**变化矩阵（From→To）**：

```
From\To    建筑    水体   植被   裸地
建筑      80%     2%    10%    8%    ← 8%的建筑变为裸地(拆迁)
水体       5%    88%     5%    2%
植被      15%     3%    75%    7%    ← 15%的植被变为建筑(开发)
裸地      30%     1%    20%   49%
```

### 18.6.3 后处理

```python
# 众数滤波 - 消除椒盐噪声
arcpy.ia.MajorityFilter(
    in_raster="Classified.tif",
    out_raster="Classified_Cleaned.tif",
    number_of_neighbors="FOUR",  # 或 EIGHT
    majority_definition="HALF"   # 半数替换
)

# 边界清理 - 规整分类边界
arcpy.ia.BoundaryClean(
    in_raster="Classified.tif",
    out_raster="Classified_Cleaned.tif",
    sort_type="DESCENDING",
    number_of_runs="TWO_WAY"
)
```

---

## 18.7 完整影像分类工作流

```
1. 数据准备
   ├ 影像预处理（辐射定标/大气校正/正射）
   ├ 波段组合选择（真彩色/标准假彩色/CIR）
   └ 研究区裁剪（按边界/掩膜）

2. 样本创建
   ├ 交互式绘制训练样本（每类 40+ 像元）
   ├ 独立创建验证样本（训练集不重叠）
   └ 检查样本可分离性（直方图/散点图）

3. 分类执行
   ├ 可选：影像分割（Segment Mean Shift）
   ├ 选择分类器 → 随机森林（推荐首选）
   └ 执行分类 → 输出分类栅格

4. 精度评估
   ├ 混淆矩阵 → 总体精度/Kappa
   ├ 各类用户精度/生产者精度
   └ 精度不达标 → 回步骤2增加样本

5. 后处理
   ├ 众数滤波（去椒盐噪声）
   ├ 边界清理（规整斑块）
   ├ 面积阈值过滤（删除碎斑 < 最小制图单元）
   └ 栅格转矢量（分类面shp）

6. 变化检测（如有需求）
   ├ 两期分别分类
   ├ 分类后比较 → From-To矩阵
   └ 变化图输出
```

> **神经连接**：影像预处理工具参数 → 第十一篇 ArcGIS Pro 数据管理（`arcpy.ia` 模块）。分类精度评估 → 第十三篇 质量检查验收标准。NDVI/指数计算 → 第七篇 ArcGIS Pro 核心分析功能。

> **推荐学习资源**：
> - ArcGIS Pro Image Classification Wizard 文档：`pro.arcgis.com/zh-cn/pro-app/latest/help/analysis/image-analyst/the-image-classification-wizard.htm`
> - USGS Landsat 系列 `landsat.usgs.gov` — 免费遥感数据下载
> - ESA Sentinel 系列 `scihub.copernicus.eu` — 哨兵卫星免费数据
> - Richard & Jia《Remote Sensing Digital Image Analysis》— 遥感教材经典

---

## 18.8 LiDAR点云处理与Python生态

> 来源：PDAL官方文档 + laspy API参考 + gis-mcp/PDAL MCP 生态勘探 + SuperPoint项目实战
> 最后更新：2026-05-29 | 核心要点：laspy→PDAL→Open3D三层工具链、管道体系、地面滤波算法对比

### 18.8.1 点云数据格式对比

| 格式 | 扩展名 | 压缩 | 标准 | 典型场景 |
|------|--------|------|------|---------|
| **LAS** | `.las` | 无 | ASPRS 标准 | LiDAR行业交换格式，含分类/强度/回波 |
| **LAZ** | `.laz` | 有（LASzip） | ASPRS 标准 | LAS无损压缩版，文件体积约1/10 |
| **PLY** | `.ply` | 无 | 斯坦福标准 | 通用3D点云/三角网，含颜色/法向量 |
| **PCD** | `.pcd` | 有 | PCL原生 | ROS/PCL生态，支持有序点云 |
| **XYZ** | `.xyz/.txt` | 无 | 无标准 | 纯文本坐标，无元数据 |
| **E57** | `.e57` | 有 | ASTM E2807 | 地面激光扫描交换格式 |

#### LAS 点分类编码（ASPRS Standard 1.4）

| 分类码 | 类别 | 说明 |
|:---:|------|------|
| 0 | Created, Never Classified | 未分类 |
| 1 | Unclassified | 处理过但未分类 |
| 2 | Ground | 地面点 |
| 3 | Low Vegetation | 低矮植被 (0~1.5m) |
| 4 | Medium Vegetation | 中等植被 (1.5~5m) |
| 5 | High Vegetation | 高植被 (>5m) |
| 6 | Building | 建筑物 |
| 7 | Low Point (Noise) | 低噪点 |
| 8 | Model Key/Reserved | 模型关键点 |
| 9 | Water | 水体 |
| 10 | Rail | 铁路 |
| 11 | Road Surface | 路面 |
| 12 | Overlap/Reserved | 重叠点 |
| 13-31 | Reserved | ASPRS保留 |

### 18.8.2 Python点云处理库全景对比

| 库 | 定位 | 核心能力 | 安装 | 适用场景 |
|---|------|---------|------|---------|
| **laspy** | LAS/LAZ读写 | 快速读写LAS、点云过滤、分类修改 | `pip install laspy` | 数据探查、批量格式处理 |
| **PDAL** | 专业点云管道 | 管道式处理、格式转换、地面滤波、分类 | `pip install pdal` | 生产级点云处理流水线 |
| **Open3D** | 3D数据处理 | 点云配准、ICP、体素化、可视化 | `pip install open3d` | SLAM/三维重建/可视化 |
| **pylas** | 纯Python LAS | 纯Python实现，无C++依赖 | `pip install pylas` | 轻量级LAS操作 |
| **PCL (python-pcl)** | PCL Python绑定 | 滤波/分割/特征提取 | `conda install -c conda-forge pcl` | 学术研究/算法原型 |

#### 工具链选择策略

```
快速探查 → laspy（读写快，API简洁）
    ↓ 需要管道处理
生产流水线 → PDAL（C++底层，JSON管道，一键全链路）
    ↓ 需要3D分析
三维可视化/配准 → Open3D（可视化、ICP、体素降采样）
```

### 18.8.3 PDAL管道体系详解

PDAL 的核心概念是 **Pipeline（管道）**，JSON格式定义处理链路：

```
{Reader} → {Filter 1} → {Filter 2} → ... → {Writer}
```

#### 管道三要素

| 要素 | 说明 | 数量限制 |
|------|------|---------|
| **Reader** | 数据源读取（LAS/LAZ/PLY/TXT等） | 至少1个 |
| **Filter** | 中间处理步骤（滤波/分类/重投影/采样等） | 0~N个 |
| **Writer** | 输出目标（文件/数据库/终端） | 至少1个 |

#### 完整管道示例：地面滤波 + 分类 + 输出

```json
{
  "pipeline": [
    {
      "type": "readers.las",
      "filename": "input.las",
      "spatialreference": "EPSG:4546"
    },
    {
      "type": "filters.smrf",
      "cell": 1.0,
      "threshold": 0.5,
      "scalar": 1.2,
      "slope": 0.15,
      "window": 18
    },
    {
      "type": "filters.range",
      "limits": "Classification[2:2]",
      "tag": "ground"
    },
    {
      "type": "filters.hag",
      "tag": "height"
    },
    {
      "type": "filters.ferry",
      "dimensions": "HeightAboveGround=>Z"
    },
    {
      "type": "writers.las",
      "filename": "output_classified.las",
      "extra_dims": "all",
      "compression": "laszip"
    }
  ]
}
```

#### 核心 Filter 类型速查

| Filter | 功能 | 关键参数 |
|--------|------|---------|
| `filters.smrf` | Simple Morphological Filter 地面滤波 | cell, threshold, slope, window |
| `filters.pmf` | Progressive Morphological Filter | max_window_size, slope, initial_distance |
| `filters.csf` | Cloth Simulation Filter 布料模拟 | cloth_resolution, rigidness, time_step |
| `filters.hag` | 计算点距地面高度(Height Above Ground) | — |
| `filters.outlier` | 统计离群点移除 | mean_k, multiplier |
| `filters.range` | 按维度值过滤 | limits="Classification[2:2]" |
| `filters.reprojection` | 坐标系重投影 | out_srs, in_srs |
| `filters.decimation` | 点云抽稀 | step, count |
| `filters.ferry` | 维度值传递/复制 | dimensions="HAG=>Z" |
| `filters.assign` | 赋值维度 | value, condition |
| `filters.crop` | 按范围/多边形裁剪 | bounds, polygon |

### 18.8.4 PDAL CLI命令速查

| 命令 | 功能 | 示例 |
|------|------|------|
| `pdal info` | 查看点云元数据 | `pdal info data.las --all` |
| `pdal translate` | 格式转换/简单过滤 | `pdal translate in.las out.laz --filter smrf` |
| `pdal pipeline` | 执行JSON管道 | `pdal pipeline pipeline.json` |
| `pdal merge` | 合并多个点云 | `pdal merge *.las merged.las` |
| `pdal split` | 按点容量/瓦片分割 | `pdal split in.las tiles/tile_#.las capacity 1000000` |
| `pdal tile` | 生成正方形瓦片 | `pdal tile in.las tiles/tile_#.las --buffer 50` |
| `pdal tindex` | 创建瓦片索引 | `pdal tindex index.sqlite tiles/*.las` |

#### pdal info 元数据速查

```bash
pdal info data.las --all
# 输出: 点数、边界范围、CRS、维度列表、分类统计
# 关键字段:
#   num_points: 点数
#   maxx/minx/maxy/miny/maxz/minz: 边界
#   srs.wkt: 坐标系
#   stats.classification.counts: 分类统计
```

### 18.8.5 laspy 实战操作

#### 基本读写

```python
import laspy
import numpy as np

# 读取
las = laspy.read("input.las")
print(f"点数: {len(las.points)}")
print(f"维度: {list(las.point_format.dimension_names)}")
print(f"分类统计: {np.unique(las.classification, return_counts=True)}")

# 提取XYZ
xyz = np.vstack((las.x, las.y, las.z)).T

# 分类过滤 - 提取地面点
ground_mask = las.classification == 2
ground_points = las.points[ground_mask]

# 修改分类
las.classification[地面点索引] = 2  # 标记为地面

# 写入
las.write("output.las")
```

#### 常用过滤与统计

```python
# 按范围过滤
x_min, x_max = 500000, 501000
y_min, y_max = 3400000, 3401000
mask = (las.x >= x_min) & (las.x <= x_max) & \
       (las.y >= y_min) & (las.y <= y_max)
subset = las.points[mask]

# 按回波过滤 - 仅保留首次回波
first_return = las.points[las.return_number == 1]

# 强度统计
print(f"强度范围: {las.intensity.min():.0f} ~ {las.intensity.max():.0f}")
print(f"强度均值: {las.intensity.mean():.1f}")

# 高程统计
z = np.array(las.z)
print(f"Z范围: {z.min():.2f} ~ {z.max():.2f}")
print(f"平均高度: {z.mean():.2f}")
```

#### 自适应采样（SuperPoint核心需求）

```python
def adaptive_sampling(las, min_spacing=0.5, max_spacing=2.0):
    """基于曲率/高程变化的自适应点云采样"""
    from scipy.spatial import KDTree
    
    points = np.vstack((las.x, las.y, las.z)).T
    tree = KDTree(points[:, :2])  # 2D KDTree
    
    # 计算局部高程标准差作为复杂度指标
    k = 15
    complexity = np.zeros(len(points))
    for i in range(0, len(points), 10000):  # 分批处理
        end = min(i + 10000, len(points))
        dists, idxs = tree.query(points[i:end, :2], k=k)
        neighbors_z = points[idxs, 2]
        complexity[i:end] = np.std(neighbors_z, axis=1)
    
    # 复杂度映射到采样间距
    c_min, c_max = complexity.min(), complexity.max()
    spacing = min_spacing + (max_spacing - min_spacing) * \
              (1 - (complexity - c_min) / (c_max - c_min))
    
    return spacing
```

### 18.8.6 地面滤波算法对比

| 算法 | 原理 | 优点 | 缺点 | 适用场景 |
|------|------|------|------|---------|
| **SMRF** (Simple Morphological Filter) | 形态学开运算 | 速度快、参数少 | 陡坡可能漏分 | 城市/平原 |
| **PMF** (Progressive Morphological Filter) | 渐进窗口形态学 | 适应不同坡度 | 参数多、需调优 | 山区/丘陵 |
| **CSF** (Cloth Simulation Filter) | 物理模拟布料覆盖 | 理论优美、效果稳定 | 速度中等 | 混合地形 |
| **ATIN** (Adaptive TIN) | 迭代三角网加密 | 点级别精度 | 速度慢、大内存 | 精细地形 |

#### SuperPoint 推荐方案

```
首选 CSF → 布料模拟参数少、效果好
备选 SMRF → 城市区域速度快
```

#### PDAL 管道执行

```python
import pdal
import json

pipeline_json = {
    "pipeline": [
        {"type": "readers.las", "filename": "input.las"},
        {
            "type": "filters.csf",
            "rigidness": 3,         # 布硬度(1:平缓, 3:山区)
            "cloth_resolution": 1.0 # 布料分辨率(m)
        },
        {"type": "filters.hag"},    # 计算高度
        {"type": "writers.las", "filename": "ground.las",
         "extra_dims": "all"}
    ]
}

pipeline = pdal.Pipeline(json.dumps(pipeline_json))
pipeline.execute()
print(f"处理点数: {pipeline.arrays[0].shape[0]}")
```

> **神经连接**：坐标系选择→第一篇(坐标系基础)+第五篇(中国坐标系实战)。地面滤波→ArcGIS 3D Analyst（第七篇7.19）。点云分类编码→ASPRS标准（本表）。点云→三维建模 ← 第二十篇 实景三维（3D Tiles/LOD体系优化）。分类精度评估 → 第十三篇 质量检查验收标准。遥感避坑 → 附录B B.6 遥感/倾斜摄影篇。PDAL管道→GIS开源工具链（第十七篇17.7）。

---

### 18.9 多传感器指数速查表 ⭐ V4.1 新增

> 按传感器分类列示各指数波段对应，避免波段错误（B.6.7避坑根因）。

#### 18.9.1 Landsat 8/9 (OLI) 波段对照

| 波段 | 名称 | 波长(μm) | 指数应用 |
|------|------|---------|---------|
| Band 2 | Blue | 0.45-0.51 | NDWI (McFeeters) |
| Band 3 | Green | 0.53-0.59 | NDWI替代 |
| **Band 4** | **Red** | 0.64-0.67 | **NDVI, EVI, SAVI** |
| **Band 5** | **NIR** | 0.85-0.88 | **NDVI, EVI, MNDWI** |
| **Band 6** | **SWIR1** | 1.57-1.65 | **NDBI, NDMI, NBR** |
| Band 7 | SWIR2 | 2.11-2.29 | NBR2, NDMI |

#### 18.9.2 Sentinel-2 (MSI) 波段对照

| 波段 | 波段号 | 波长(nm) | 指数应用 |
|------|--------|---------|---------|
| Red | Band 4 | 665 | NDVI, EVI, SAVI |
| **NIR** | **Band 8** | 842 | **NDVI, NDWI, MNDWI** |
| SWIR1 | Band 11 | 1610 | NDBI, NDMI, NBR |
| SWIR2 | Band 12 | 2190 | NBR2 |
| Red Edge | Band 5-7 | 705/740/783 | NDRE |

#### 18.9.3 高分系列 (GF/国产卫星) 波段对照

| 卫星 | 波段(Blue/Green/Red/NIR) | 分辨率 | NDVI公式 |
|------|--------------------------|--------|---------|
| GF-1/GF-6 WFV | 0.45-0.52 / 0.52-0.59 / 0.63-0.69 / 0.77-0.89 | 16m | (B4-B3)/(B4+B3) |
| GF-2 PMS | Blue/Green/Red/NIR | 4m | (B4-B3)/(B4+B3) |
| GF-3 SAR | C波段 5.6cm (雷达) | 1-500m | 后向散射系数 |
| GF-4 | VNIR+MWIR (静止轨道) | 50m/400m | 持续监测 |

#### 18.9.4 常用指数公式速查

| 指数 | 通用公式 | Landsat 8/9 | Sentinel-2 | GF-1/6 |
|------|---------|------------|-----------|--------|
| **NDVI** | (NIR-Red)/(NIR+Red) | (B5-B4)/(B5+B4) | (B8-B4)/(B8+B4) | (B4-B3)/(B4+B3) |
| **EVI** | 2.5×(NIR-Red)/(NIR+6×Red-7.5×Blue+1) | B5/B4/B2公式 | B8/B4/B2公式 | 同Landsat |
| **SAVI** | (NIR-Red)×1.5/(NIR+Red+0.5) | (B5-B4)×1.5/(B5+B4+0.5) | (B8-B4)×1.5/(B8+B4+0.5) | 同 |
| **NDWI** | (Green-NIR)/(Green+NIR) | (B3-B5)/(B3+B5) | (B3-B8)/(B3+B8) | (B2-B4)/(B2+B4) |
| **MNDWI** | (Green-SWIR1)/(Green+SWIR1) | (B3-B6)/(B3+B6) | (B3-B11)/(B3+B11) | — |
| **NDBI** | (SWIR1-NIR)/(SWIR1+NIR) | (B6-B5)/(B6+B5) | (B11-B8)/(B11+B8) | — |
| **NDMI** | (NIR-SWIR1)/(NIR+SWIR1) | (B5-B6)/(B5+B6) | (B8-B11)/(B8+B11) | — |
| **NBR** | (NIR-SWIR2)/(NIR+SWIR2) | (B5-B7)/(B5+B7) | (B8-B12)/(B8+B12) | — |
| **NDRE** | (NIR-RedEdge)/(NIR+RedEdge) | — | (B8-B5)/(B8+B5) | — |

#### 18.9.5 GEE 自动传感器识别代码

```javascript
// 关键提醒：Landsat C2 L2 使用 SR_B* 命名，非 TOA 的 B*
var image = ee.Image('LANDSAT/LC08/C02/T1_L2/LC08_123032_20230601');
var ndvi = image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI');

// Sentinel-2
var s2 = ee.Image('COPERNICUS/S2_SR_HARMONIZED/...');
var ndvi_s2 = s2.normalizedDifference(['B8', 'B4']).rename('NDVI');
```

> ⚠️ **B.6.7 避坑根因**：Landsat Collection 2 Level-2 使用 `SR_B*` 命名（地表反射率），TOA Collection 1 用 `B*`。混淆将导致零值或异常指数。

---

### 18.8.7 补充参考：点云常用开源数据集

| 数据集 | 描述 | 规模 | 获取 |
|--------|------|------|------|
| **AHN3/4** | 荷兰全国LiDAR | TB级/全境 | `geotiles.nl` |
| **USGS 3DEP** | 美国全国LiDAR | PB级 | `usgs.gov/3dep` |
| **ISPRS Benchmark** | 点云分类基准 | 多场景 | `isprs.org` |
| **OpenTopography** | 全球LiDAR开源 | 多源 | `opentopography.org` |

---


<!-- wm:坤图_GIS:V1.0 -->
