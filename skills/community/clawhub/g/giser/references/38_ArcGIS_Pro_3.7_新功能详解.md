# 38_ArcGIS_Pro_3.7_新功能详解.md

> **来源**：Esri 官方文档（doc.esri.com）| 提取时间：2026-06-03
> **价值评级**：A级（完全新增，V3.3 知识库无此内容）
> **适用软件**：ArcGIS Pro 3.7（2026年5月发布）
> 
> **关联文件**：本文档仅涵盖 3.7 **相对于 3.6 的新增/变更内容**。完整功能指南请参阅 → **[12_ArcGIS_Pro.md](./12_ArcGIS_Pro.md)**（3.6 完整手册，2,080行）。
> ⚠️ **版本警示**：3.7 新增的功能/API 在 3.6 中**不可用**。若提问者指定 3.6 版本，切勿引用本文档内容。

---

## 一、亮点功能（Highlights）

### 1.1 按地图框控制图层可见性 ⭐⭐⭐⭐⭐

**功能描述**：
- 可在布局（Layout）中的**地图框（Map Frame）内独立开启/关闭图层**
- 不影响其他地图框或地图视图中的图层状态
- 启用方式：选择地图框 → **Map Frame** 功能区 → 点击 **Layer Visibility** 按钮

**价值**：
- 无需为不同图层组合创建多个地图
- 多个布局或多个地图框可指向同一地图但显示不同图层
- 大幅简化布局管理

**限制**：
- 仅适用于布局内容窗格中的可见性复选框
- 定义查询（Definition Query）或符号类可见性无法按地图框单独设置

---

### 1.2 Analyze Map（地图性能分析）⭐⭐⭐⭐⭐

**功能描述**：
- 新增 **Analyze Map** 窗格，用于评估地图绘制性能
- 提供逐层数据处理和要素复杂度测量
- 帮助识别性能瓶颈

**分析领域**：
| 分析项 | 说明 |
|----------|------|
| 高级符号系统和标注渲染 | 识别复杂符号/标注导致的性能问题 |
| 未转换、未索引或不可访问的数据 | 数据源问题检测 |
| 自定义查询表达式 | 复杂定义查询的性能影响 |

**价值**：精准定位地图性能瓶颈，是大规模数据生产的必备工具。

---

### 1.3 文件知识图谱（File Knowledge Graph）⭐⭐⭐⭐⭐

**功能描述**：
- 可在**本地文件夹**中创建和管理知识图谱
- **无需 ArcGIS Enterprise 部署**（重大变化！）
- 支持大多数高级可视化、分析和数据管理功能

**支持功能**：
| 功能 | 说明 |
|--------|------|
| 数据模型创建 | 定义实体-关系模型 |
| 图查询分析 | 实体连接分析 |
| 链接图表可视化 | 关系可视化 |
| 地图探索 | 在地图上探索图数据 |

**价值**：知识图谱能力从企业级下沉到桌面级，极大降低使用门槛。

---

### 1.4 提取扫描线条和多边形 ⭐⭐⭐⭐

**新增工具**：

| 工具 | 功能 | 参数控制 |
|------|------|------------|
| **Extract Scanned Lines** | 从扫描地图图像生成折线要素（沿栅格单元中心线） | 交叉点处理、压缩、平滑程度、角落/间隙/孔洞处理 |
| **Extract Scanned Polygons** | 沿栅格单元轮廓生成多边形要素 | 类似的压缩和平滑控制选项 |

**价值**：历史纸质地图数字化工作流的重大改进。

---

### 1.5 基于嵌入的分析（Embeddings-Based Analysis）⭐⭐⭐⭐⭐

**功能描述**：
- 使用 AI 生成的向量表示进行地理空间数据的语义分析
- 将影像、地理要素和文本转换为高维数值向量
- 在嵌入空间中执行分析，相似要素距离更近

**新增 GeoAI 工具集**：

| 工具 | 功能 |
|------|------|
| **Generate Embeddings Using AI Models** | 将空间数据转换为语义向量表示 |
| **Find Similar Features Using Embeddings** | 大规模相似性搜索 |
| **Merge Embeddings** | 将嵌入从一种空间级别聚合到另一种 |
| **Extract Embeddings To Fields** | 将嵌入转换为数值字段 |

**新增窗格**：Find Similar（交互式探索相似要素）

**价值**：AI + GIS 深度融合，开启语义级空间分析新范式。

---

### 1.6 电信域网络（Telecom Domain Networks）⭐⭐⭐⭐

**功能描述**：
- 公用设施网络（Utility Network）的新配置选项
- 需 Utility Network Version 8
- 专为管理电信基础设施的组织设计

**核心特性**：

| 特性 | 说明 |
|--------|------|
| 基于电路管理的独特架构 | 电信网络专属数据模型 |
| 分组功能 | 单个记录可代表具有共享属性和拓扑的多个对象（如电缆中的光纤束） |
| 两种追踪类型 | 路径追踪（Path Trace）和电路追踪（Circuit Trace） |
| 色彩方案 | 基于标准或自定义着色惯例识别单个光纤束 |
| 脏对象表 | 跟踪非空间对象和关联状态 |
| 基于外键的关联 | 将连通性存储为行内数据 |

**价值**：Utility Network 从电力/水务扩展至电信行业，覆盖全基础设施类型。

---

### 1.7 新的离线和在线帮助系统

**改进**：
- 离线帮助通过 **ArcGIS Documentation Center** 提供（My Esri 中的应用程序）
- 可下载多种语言和版本的帮助
- 离线帮助可在发布周期内更新
- 在线帮助遵循新的 URL 模式
- 全球部署节点，性能更好
- 支持浅色和深色主题

---

## 二、性能改进详细清单

### 2.1 数据加载与处理

| 改进领域 | 详细说明 |
|----------|---------|
| 企业级地理数据库（传统版本化） | 支持手动要素缓存操作 |
| 企业级地理数据库数据加载 | 将企业级地理数据库数据添加到地图或打开包含此类数据的地图速度显著加快 |
| 动态布局元素 | 暂停绘制时动态布局元素也暂停 |
| Python 环境克隆 | 克隆 Python 环境不再下载包，速度更快，支持离线计算机 |
| 地图文件导入 | 导入 .mapx 和 .pagx 文件速度更快 |
| LAS 压缩文件（LAZ） | 解压缩 .laz 文件性能改进；计算统计信息时创建空间索引 |
| Google Photorealistic 3D 底图 | 性能改进 |
| LAZ 文件 | 并行解压缩能力 |

---

### 2.2 生产力改进

| 改进领域 | 详细说明 |
|----------|---------|
| 系统收藏夹 | 管理员可创建系统收藏夹并通过应用程序设置分发给用户 |
| 符号搜索 | 可使用语义搜索查找符号和样式 |
| 要素选择 | 可按要素几何或符号系统选择地图要素 |
| 定义查询 | 可排序和复制定义查询 |
| 地理处理历史 | 历史记录条目可添加描述 |
| 编辑工具 | 多个编辑工具有新选项和功能 |
| 门户连接 | 可搜索门户连接并设置别名 |
| 自定义工具栏 | 可为地图和其他视图创建自定义工具栏 |
| 静默安装参数 | 新增 `DISABLE_EXTERNAL_TRAFFIC` 参数，防止向 ArcGIS Online 发送请求 |

---

## 三、各模块详细新功能

### 3.1 分析与地理处理（Analysis and Geoprocessing）

**通用改进**：
- 可为地理处理历史条目添加描述
- 从历史记录重新打开的工具作为附加工具在 Geoprocessing 窗格中打开
- 新增 **Initial browse location** 选项，指定浏览对话框的默认打开位置
- 系统管理员可覆盖地理处理环境设置的默认值
- **Append** 工具的 **Field Map** 参数增强，改进了目标与输入数据集之间的字段匹配
- 可在属性表中使用 **Calculate Field Toolbar** 添加新字段并进行计算，改进进度报告和取消功能

---

### 3.2 图表（Charts）

- 多系列折线图支持堆叠面积选项：
  - **Stacked Area**：系列堆叠显示各系列对总计的贡献
  - **100% Stacked Area**：系列堆叠使每个 x 轴位置的总和等于 100%
- 日期字段可用于配置散点图的 x 轴或 y 轴
- 时间轴标签可通过 **Date formatting** 设置自定义

---

### 3.3 地理处理服务与 Web 工具

- 经验丰富的发布者可直接从工具箱或 **Share** 功能区选项卡共享 Web 工具，无需先本地运行
- 新的发布整合选项，更好地控制数据、工具箱、脚本和 Python 资源的打包方式

---

### 3.4 ModelBuilder

**图表和布局全面增强**：
| 改进项 | 说明 |
|--------|------|
| 节点更紧凑 | 默认布局更紧凑 |
| 默认缩放级别 | 提高到 150% |
| 统一默认字体 | 类型、大小和文本对齐方式统一 |
| 字体颜色动态适应 | 浅色/深色主题自动切换 |
| 支持所有方向的节点调整大小 | 布局灵活性提升 |

**图表指示器改进**：
| 改进项 | 说明 |
|--------|------|
| 链接端点设计改进 | 主题对齐更好 |
| 参数指示器更可见 | 参数连接更清晰 |
| 运行状态指示器 | 有成功和错误图标 |
| 工具参数暴露为模型变量时 | 显示数据类型图标 |

---

### 3.5 3D Analyst 扩展 ⭐⭐⭐⭐⭐

#### 激光雷达和 LAS 数据集

| 新功能 | 说明 |
|----------|------|
| 自定义 LAS 分类代码标签和颜色 | 可创建自定义 LAS 分类标签和颜色方案 |
| LAZ 文件性能改进 | 生成统计信息和创建空间索引、并行解压缩 |
| 更改 LAS 数据集中选定点的颜色 | 支持按选定点修改颜色 |

#### 新增地理处理工具

| 工具 | 功能 |
|------|------|
| **Create Terrain From BIM** | 从 AutoCAD Civil 3D 文件或 IFC 文件创建 terrain 表面 |
| **TIN To Multipatch** | 将 TIN 数据集转换为 multipatch 要素类 |

#### 增强工具

| 工具 | 新增参数/功能 |
|------|----------------|
| **Contour List** | 新增 Contour Type 参数（线或面） |
| **Stack Profile** | 输出表支持创建折线图 |
| **Extract LOD2 Buildings** | 并行处理提升性能 |
| **Interpolate Shape** | 保留 M 值（如果输入数据中存在） |
| **Point File Information** | 从 LAZ 输入设置默认输出空间参考 |
| **Surface Parameters** | 矩形像元时 Neighborhood distance 默认值为宽度和长度的平均值 |
| **Aspect、Slope、Surface Parameters** | Z unit 参数支持 US Foot 选项 |

---

### 3.6 Business Analyst 扩展

| 新功能 | 说明 |
|----------|------|
| **Generate Customer Demographic Profile Report** 工具 | 汇总客户人口统计信息 |
| 可使用本地数据集运行信息图表 | 无需在线连接 |
| Target Marketing 向导增强 | 工作流中查看客户画像和市场区域画像；四象限分析中显示/隐藏异常值；使用调查画像作为客户数据代理 |
| 兴趣点搜索重新设计 | 更好的类别和代码系统支持；按地理单位聚合点；构建高级搜索查询；Area of Interest 设置定义搜索范围 |

---

### 3.7 Image Analyst 扩展 ⭐⭐⭐⭐⭐

#### 光谱分析

| 新功能 | 说明 |
|----------|------|
| Spectral Signature Viewer 新增功能 | Remove Continuum 和 Calculate Mean 预处理功能 |
| Add Hyperspectral Data 对话框 | 支持云路径数据 |
| 新增支持 | Dragonette 和 Tanager 高光谱卫星传感器 |

#### 深度学习

| 新功能 | 说明 |
|----------|------|
| 可标注视频图层 | 视频数据支持 AI 标注 |
| 三个新标注工具 | Point、Line、Segment using AI |
| Text Prompt 工具 | 可指定多个对象（如 "trees, houses"） |

#### 运动影像

| 新功能 | 说明 |
|----------|------|
| 可使用 **Convert Video Metadata** 工具配置元数据文件 | 支持更多视频元数据格式 |

#### 立体测图

| 新功能 | 说明 |
|----------|------|
| Softmouse 3D 输入设备系统按钮可配置 | 支持更多 3D 输入设备 |
| 状态栏新增高程单位下拉列表 | 快速切换高程单位 |

#### 合成孔径雷达（SAR）

| 新功能 | 说明 |
|----------|------|
| 新的 **SAR Feature Detection Wizard** | 引导海洋要素检测和提取 |
| 新增支持 | NISAR 和 PAZ SAR 栅格类型 |
| RADARSAT-2 | 支持 Extra Fine 处理模板 |

---

### 3.8 Network Analyst 扩展

| 新功能 | 说明 |
|----------|------|
| Waste Collection Layer 功能区新增工具 | **Select By Streets**（扩展停靠点选择集）；**Update Assignments**（更改停靠点的路线分配）；**Update Results**（使用当前路线分配调整停靠点排序） |
| 可为 **Explore Locations** 工具设置默认网络数据源和配置符号 | 自定义默认行为 |
| 网络数据集新增 Network Analyst 编辑选项 | 编辑体验改进 |

---

### 3.9 Spatial Analyst 扩展

| 新功能 | 说明 |
|----------|------|
| **Interactive Contour** 工具 | 点击表面栅格生成等高线（交互式） |
| **Suitability Modeler** | 支持成对加权（Pairwise weighting） |

---

## 四、地理处理工具箱 — 完整新增和增强

### 4.1 Analysis 工具箱

| 工具 | 新增/增强 | 说明 |
|------|-----------|------|
| **Pairwise Dissolve** | 增强 | 新增 **Output Lineage Table** 参数，生成溶解输入要素 FID 与对应输出 FID 的关系表 |

### 4.2 Aviation 工具箱

| 工具 | 新增/增强 | 说明 |
|------|-----------|------|
| **ICAO Annex 14 OFS OES** | 增强 | 参数更新，现可在 Obstruction Identification Surfaces 工具集中使用 |
| **Import AIXM 5.1 Message** | 增强 | 新增 **Set Fields To Null On Update** 和 **Custom Configuration File** 参数 |

### 4.3 Bathymetry 工具箱

| 工具 | 新增参数 | 说明 |
|------|-----------|------|
| **BIS To Mosaic Dataset** | Area of Interest、Honor BIS_Dataset_Status Field | 定义地理区域选择数据集；指定导出是否遵循 BIS_Dataset_Status 字段 |

### 4.4 Business Analyst 工具箱

| 工具 | 说明 |
|------|------|
| **Generate Customer Demographic Profile Report** | 新增工具，汇总客户人口统计信息 |
| **Color Coded Layer** | Area of Interest 参数接受点图层 |

### 4.5 Conversion 工具箱 ⭐⭐⭐⭐

#### From Raster 工具集新增：

| 工具 | 功能 |
|------|------|
| **Extract Scanned Lines** | 从扫描图像生成折线要素 |
| **Extract Scanned Polygons** | 从扫描图像生成多边形要素 |

#### To CAD 工具集增强：

| 工具 | 增强 |
|------|------|
| **Export To CAD** | 从带引线的注记要素生成多引线实体 |

#### To Geodatabase 工具集新增：

| 工具 | 功能 |
|------|------|
| **Convert Personal Geodatabase** | 将旧版个人地理数据库或 Access 数据库转换为移动地理数据库、文件地理数据库或 XML 工作空间文档 |

#### To Geodatabase 工具集增强：

| 工具 | 增强 |
|------|------|
| **BIM File To Geodatabase** | 支持建筑图层及其过滤内容作为输入 |

#### 新增 To Parquet 工具集：

| 工具 | 功能 |
|------|------|
| **Export To Parquet** | 将简单数据导出为 Apache Parquet 文件 |

### 4.6 Data Management 工具箱 ⭐⭐⭐⭐

#### Attachments 工具集增强：

| 工具 | 新增参数 |
|------|-----------|
| **Upgrade Attachments** | Upgrade level 参数决定添加哪些字段 |
| **Downgrade Attachments** | Downgrade level 参数决定移除哪些字段 |

#### Attribute Rules 工具集增强：

| 工具 | 新增支持 |
|------|-----------|
| **Evaluate Rules** | 分支版本化用户现可使用（ArcGIS Pro Basic 许可 + ArcGIS Advanced Editing 用户类型扩展） |

#### Distributed Geodatabase 工具集增强：

| 工具 | 新增参数 |
|------|-----------|
| **Create Replica** | Geometry Filter Type（定义空间关系）；Replicate（包含所有要素或仅方案） |

#### Domains 工具集新增：

| 工具 | 功能 |
|------|------|
| **Alter Coded Value Description** | 更新现有编码值对的描述值 |

#### Features 工具集增强：

| 工具 | 新增参数 |
|------|-----------|
| **Feature To Polygon** | Polygon Construction Source 参数支持从封闭输入线或多边形构建多边形 |

#### Fields 工具集新增：

| 工具 | 功能 |
|------|------|
| **Alter Geometry Index Preference** | SAP HANA 中更改空间索引类型设置 |

#### General 工具集增强：

| 工具 | 新增功能 |
|------|-----------|
| **Append** | 支持仅几何更新、候选字段指定子集更新/插入、Skip Options 选择 |

#### Indexes 工具集增强：

| 工具 | 新增参数 |
|------|-----------|
| **Add Full-Text Index** | 新增 Synchronize On Commit 参数（仅 Oracle） |

#### Layout 工具集新增：

| 工具 | 功能 |
|------|------|
| **Export Layouts** | 批量导出多个布局 |

#### Photos 工具集增强：

| 工具 | 新增支持 |
|------|-----------|
| **Geotagged Photos To Points** | 支持 HEIC 格式 |

#### Subtypes 工具集新增：

| 工具 | 功能 |
|------|------|
| **Alter Subtype** | 更改现有子类型代码的名称 |

#### Topology 工具集增强：

| 工具 | 新增支持 |
|------|-----------|
| **Validate Topology** | 分支版本化用户现可使用 |

#### Versions 工具集增强：

| 工具 | 新增支持 |
|------|-----------|
| 分支版本化工具 | 现对 ArcGIS Pro Basic 许可用户可用 |
| **Reconcile Versions** | 分支版本化支持 |
| **Prune Branch History** | 支持 parcel fabric 数据集 |

#### Workspace 工具集增强：

| 工具 | 新增支持 |
|------|-----------|
| 多个架构报告工具 | 支持电信域网络作为输入 |

### 4.7 Editing 工具箱

| 工具 | 新增参数 |
|------|-----------|
| **Simplify By Tangent Segments** | 新增 Anchor Points 参数 |

### 4.8 GeoAI 工具箱 ⭐⭐⭐⭐（全新工具箱）

| 工具 | 功能 |
|------|------|
| **Extract Embedding To Fields** | 将嵌入转换为数值字段 |
| **Find Similar Features Using Embeddings** | 基于嵌入的相似性搜索 |
| **Generate Embeddings Using AI Models** | 生成空间数据的 AI 嵌入向量 |
| **Merge Embeddings** | 聚合嵌入 |
| **Predict Missing Values Using AI Model** | 使用 AI 模型预测缺失值 |

### 4.9 Geocoding 工具箱

| 工具 | 说明 |
|------|------|
| **Split Match Narrative Into Fields** | 新增工具 |
| **Assign Streets To Points** | 支持阿根廷和危地马拉 |
| **Batch Geocode** | 新增 Match Narrative 参数 |
| **Create Locator** | 支持阿根廷和危地马拉 |
| **Geocode Addresses** | 新增 Match Narrative 参数 |

### 4.10 Image Analyst 工具箱 ⭐⭐⭐⭐（大量新增）

| 工具 | 功能 |
|------|------|
| **Convert Video Metadata** | 配置视频元数据 |
| **Extract Ocean Winds** | 提取海洋风场信息 |
| **Extract Spectra From Image** | 从影像提取光谱 |
| **Generate Video Metadata (Stationary)** | 生成静止视频元数据 |
| **Reduce Spectral Bands** | 降低光谱波段数 |
| **Translate Pixels Using Deep Learning** | 像素级深度学习翻译（超分辨率/着色） |
| **Train Deep Learning Model** | 新骨干网络支持：DOFA base/large、Clay large、ResNeXt50_32x4d、TerraMind Base/Large、Wide ResNet-50-2 |

### 4.11 Indoor Positioning 工具箱

| 工具 | 功能 |
|------|------|
| **Generate Beacon Placement Plan** | 新增工具，生成信标放置计划 |

### 4.12 Indoors 工具箱

| 工具 | 增强 |
|------|------|
| **360 Video To Oriented Imagery** | 多个新参数 |
| **Extract Floor Plan Features From PDF** | 多项增强 |
| **Import Features To Indoor Dataset** | 新增参数 |

### 4.13 Knowledge Graph 工具箱 ⭐⭐⭐⭐（全新工具箱）

| 工具 | 功能 |
|------|------|
| **Create File Knowledge Graph** | 创建本地文件知识图谱 |
| **Copy Knowledge Graph Types** | 复制知识图谱类型 |
| **Export Knowledge Graph** | 导出知识图谱 |

### 4.14 Location Referencing 工具箱

| 工具 | 新增/增强 |
|------|-----------|
| **Configure Utility Network Feature Classes** | 新增工具 |
| **Generate Events** | 新增 Bypass events with null route ID and measure fields 参数 |
| **Generate Linear Referenced Route Log** | LRS 交叉要素类可用作输入 |
| **Overlay Events** | 多项增强 |

### 4.15 Maritime 工具箱

| 工具 | 新增参数 |
|------|-----------|
| **Export S-101 Cell** | 新增 Sample Export 和 Suppress Exchange Set 参数 |
| **Import S-100 Cell** | 可选 Create S-57 Product 参数 |

### 4.16 Multidimension 工具箱

| 工具 | 功能 |
|------|------|
| **Export Voxel Isosurface** | 新增工具，导出体素等值面 |

### 4.17 Network Analyst 工具箱 ⭐⭐⭐⭐（大量新增）

| 工具 | 功能 |
|------|------|
| **Update Fleet Routing Assignments** | 更新车队路径分配 |
| **Update Fleet Routing Results** | 更新车队路径结果 |
| **Export Network Travel Modes** | 导出网络出行模式 |
| **Replace Network Travel Modes** | 替换网络出行模式 |

### 4.18 Network Diagram 工具箱

| 工具 | 新增支持 |
|------|-----------|
| **Add Trace Rule** | 支持 circuit 和 path 两种新追踪类型 |
| **Alter Diagram Template** | 新增多个可选参数 |

### 4.19 Oriented Imagery 工具箱

| 工具 | 新增支持 |
|------|-----------|
| **Add Images To Oriented Imagery Dataset** | 支持视频定向影像制作 |

### 4.20 Parcel 工具箱

| 工具 | 新增参数 |
|------|-----------|
| **Append Parcels** | 新增 Replace Point Method 参数 |
| **Select Parcel Features** | 选择历史宗地多边形时关联选择历史线和点 |

### 4.21 Reality Mapping 工具箱

| 工具 | 新增选项 |
|------|-----------|
| **Reconstruct Surface** | 新增 tiePointTablePath、slnPointTablePath 选项和 Rapid 质量选项 |

### 4.22 Server 工具箱

| 工具集 | 新增支持 |
|----------|-----------|
| Caching 工具集 | 支持 Kubernetes 离线工作流 |

### 4.23 Spatial Analyst 工具箱 ⭐⭐⭐⭐（大量新增和增强）

#### 新增工具：

| 工具 | 功能 |
|------|------|
| **Adjust Raster to Stream** | 调整栅格与河流对齐 |
| **Generate Breach Lines** | 生成 breaches 线 |
| **Generate Weighted Voronoi** | 生成加权 Voronoi 图 |
| **Geodesic Flow Direction** | 测地流方向 |
| **Multicriteria Overlay** | 多准则叠加 |
| **Raster to Weighted Points** | 栅格转为加权点 |
| **Surface Area Ratio** | 表面积比率 |
| **Top Hat Transform** | 顶帽变换 |
| **Validate Flow Direction** | 验证流方向 |

#### 增强工具：

| 工具 | 改进 |
|------|------|
| **Band Collection Statistics** | 性能改进 |
| **Basin、Sink** | CPU 性能改进，GPU 支持 |
| **Contour List** | 新增 Contour Type 参数 |
| **Flow Direction** | 新增 Method 参数（平面/大地测量方法） |
| **Least Cost Corridor** | 性能显著提升 |
| **Principal Components** | 重新设计提升性能 |
| **Zonal Geometry** | 重新设计，支持并行处理 |

### 4.24 Spatial Statistics 工具箱

| 工具 | 新增/增强 |
|------|-----------|
| **Evaluate Variable Influence for Predictions** | 新增工具 |
| **Evaluate Bin Sizes for Point Aggregation** | 新增多个参数 |
| **Build Balanced Zones** | 多项增强 |
| 多个工具 | 新增 Scale Data 参数 |

### 4.25 Trace Network 工具箱

| 工具 | 新增参数 |
|------|-----------|
| **Trace** 和 **Add Trace Configuration** | Functions 参数新增 Function Name 属性 |

### 4.26 Utility Network 工具箱 ⭐⭐⭐⭐（大量新增）

#### 新增工具：

| 工具 | 功能 |
|------|------|
| **Add Color Scheme** | 添加色彩方案 |
| **Add Color Set** | 添加色彩集 |
| **Add Telecom Domain Network** | 添加电信域网络 |
| **Add Wavelength Scheme** | 添加波长方案 |
| **Delete Color Scheme** | 删除色彩方案 |
| **Export Circuits** | 导出电路 |
| **Export Circuit Definitions** | 导出电路定义 |
| **Import Circuit Definitions** | 导入电路定义 |
| **Set Circuit Properties** | 设置电路属性 |
| **Set Telecom Object Combine Policy** | 设置电信对象合并策略 |
| **Set Telecom Object Divide Policy** | 设置电信对象分割策略 |
| **Verify Circuits** | 验证电路 |

#### 增强工具：

| 工具 | 新增参数/支持 |
|------|----------------|
| **Trace** | 新增 Stopping Points、Include flow directions、Include propagated values 参数 |
| **Trace** 和 **Add Trace Configuration** | 新增 Path 和 Circuit 追踪类型、Num Paths、Max Hops 参数 |
| **Upgrade Dataset** | 新增 Utility Network Version 参数 |

---

## 五、数据管理与工作流改进

### 5.1 BIM

- 改进 Revit 元素参数读取方法，包含更多用户定义参数
- BIM 文件工作区新增多个 OST 要素类
- 某些 Revit 类别支持线性表示

### 5.2 CAD

- 支持 DWG/DXF 文件中的多引线实体作为注记要素
- AutoDesk Civil 3D 文件新增两个要素类

### 5.3 Data Reviewer

- **Duplicate Row** 检查在验证属性规则中受支持
- Error Inspector 窗格高级过滤功能
- 多个检查工具新增 Select All 复选框和搜索功能
- 更新了将批处理作业转换为属性规则的工作流

### 5.4 地理编码

- 新定位器属性：Exclude intersection type、Distance
- Match narrative 增强：MatchNarrative 字段、Geocode Table 中的参数
- Locate 窗格搜索结果可折叠/展开

### 5.5 地理数据库

- 数据集属性显示最低 ArcGIS Pro 版本要求
- 改进子类型代码/名称和编码值域代码/描述修改性能
- 可转换个人地理数据库为移动/文件地理数据库
- 可从 Catalog 窗格验证拓扑

### 5.6 附件

- 升级附件时添加 EXIFINFO 列和 alt text 字段

### 5.7 属性规则

- 保存编辑前可恢复已删除行
- 属性规则视图支持多选操作
- 约束属性规则支持更改评估顺序

### 5.8 企业级地理数据库

- Float 和 Double 字段类型可定义精度和小数位数
- 支持 PostgreSQL 18.1 和 SQL Server 2025
- 传统版本化数据支持手动要素缓存管理

### 5.9 ArcGIS Knowledge

- 支持在本地文件夹中创建文件知识图谱

### 5.10 Parquet

- 可控制持久 Parquet 缓存的位置和持续时间
- 支持 Parquet 地理空间类型
- 可使用 Export Features/Export Table 工具复制 Parquet 数据到地理数据库

### 5.11 Tasks

- 任务完成后可将地图内容恢复到初始状态
- 任务步骤可开启/关闭地面到网格校正

### 5.12 Workflow Manager

- 可在 Workflow 窗格查看作业位置
- 作业详情包含关闭作业的人员名称
- 支持 Identity-Aware Proxies 配置

---

## 六、编辑功能增强

### 6.1 通用编辑改进

| 工具 | 改进 |
|------|------|
| **Annotation** 工具 | 单独的 Rotate 和 Resize 切换按钮 |
| **Change Line Length** 工具 | 新的 COGO 感知工具 |
| **Split** 工具 | 右键单击上下文菜单中可用 |
| **Attributes** 窗格中的附件 | 支持确认删除、查看/添加/修改附件属性 |
| **Clip** 工具 | 保留共享重合边界的要素几何 |
| **Streaming** 工具 | 按固定间隔流式传输顶点 |
| **Rotate** 工具 | 旋转标记符号图层并更新符号角度属性 |
| **Divide** 工具的 Distance 方法 | 可选择并分割多条线要素 |
| **Reverse Direction** 命令 | 在 Streaming 和 Trace 构建工具上下文菜单中可用 |
| **Vertices and Nodes** 设置 | 新增 Apply 按钮 |

### 6.2 Parcel Fabric

- **Parcel Features** 命令：选择历史宗地时关联选择历史线和点
- **Copy Lines To** 工具：支持复制单独选择的线作为连接线

---

## 七、影像与遥感

### 7.1 通用

- 可在栅格图层之间复制和粘贴属性

### 7.2 定向影像

- Explore Images 工具新增两个过滤器：3D 过滤和 Display Image 过滤
- 支持时间过滤器检索影像

### 7.3 栅格数据类型和传感器

| 新增支持 | 说明 |
|----------|------|
| 新增 SAR 栅格类型 | NISAR、PAZ |
| RADARSAT-2 | 支持 Extra Fine 处理模板 |
| 新增卫星传感器 | Cartosat-2、Cartosat-3 |
| 新增高光谱传感器 | Dragonette、Tanager |

### 7.4 STAC

- Explore STAC 窗格新增保存功能
- 可指向包含 .acs 文件的文件夹
- 添加多维数据时可选择变量
- 可查看静态目录集合中的所有项目

---

## 八、制图与可视化

### 8.1 通用

| 改进项 | 说明 |
|--------|------|
| **Analyze Map** 窗格 | 评估地图绘制性能 |
| 可按要素几何选择地图要素 | 新选择方式 |
| **Add Data From Path** | 支持 WFS 和 OGC API 要素服务 |
| 创建书签时可放入现有书签文件夹 | 书签管理改进 |
| 非活动地图和场景按字母顺序排序 | UI 改进 |
| **Vulkan** 作为新的渲染引擎选项 | 性能提升选项 |
| 渲染引擎不受硬件支持时发出绘制警报 | 更好的错误提示 |
| 剖面视图可反转 | 交互改进 |
| 地图文件(.mapx)的位置单位和高度单位在导入时保留 | 单位一致性 |
| 定义查询可排序和复制 | UI 改进 |
| 企业级地理数据库查询可在客户端应用子句 | 性能改进 |
| 导入 .mapx 和 .pagx 文件绘制速度和响应性提高 | 性能提升 |

### 8.2 3D 场景和图层

- Google Photorealistic 3D 底图支持替换网格修改
- 3D tiles 图层支持 EXT_texture_webp 和 EXT_meshopt_compression 扩展

### 8.3 注记和标注

- 场景中标注在 3D 空间中绘制

### 8.4 ArcGIS Arcade

- 支持 ArcGIS Arcade 1.35

### 8.5 坐标系统和变换 ⭐⭐⭐⭐

| 更新项 | 说明 |
|--------|------|
| 更新到 EPSG v12.049 | 最新 EPSG 数据集 |
| 新增投影坐标系 | Montana RMTCRS、Hall County 等 |
| 坐标系统文件夹 | 按大洲和地理区域重新组织 |
| 新增地理变换网格 | 不丹、希腊、英国 |
| 新增垂直变换模型 | 波罗的海、法属圭亚那、格陵兰、马约特 |
| WMS 服务 | 支持有限坐标系集合 |

### 8.6 ENC 图层

- S-101 Edition 2.0.0 使用 S-101 Portrayal Catalogue 2.0.0 符号化

### 8.7 探索性分析工具

- Elevation Profile 工具支持选择地面表面计算高程

### 8.8 布局

| 改进项 | 说明 |
|--------|------|
| 按地图框控制图层可见性（亮点功能） | 布局灵活性大幅提升 |
| 暂停绘制时暂停所有动态布局元素 | 性能改进 |
| 页面查询现适用于所有地图系列类型 | 功能扩展 |
| 表格框排序使用自然排序 | 排序改进 |
| ArcGIS 2D 系统样式中的图例样式项 | 有描述性名称 |

### 8.9 弹出窗口

| 改进项 | 说明 |
|--------|------|
| **Associations** 元素 | 显示公用设施网络关联类型 |
| 可刷新频繁变化图层的弹出窗口识别 | 动态刷新 |
| 附件元素 | 支持 HEIC 图像 |
| 字段元素 | 反映表格字体设置 |
| 栅格图层 | 支持 Imagery popup 和 Imagery popup element Arcade 配置文件 |

### 8.10 演示

| 改进项 | 说明 |
|--------|------|
| 隐藏页面在内容窗格中更易区分 | UI 改进 |
| 导出 PDF 时可包含隐藏页面和演讲者备注 | 导出选项扩展 |
| 可将演讲者备注保存到文本文件 | 备注管理 |
| 图像页面 | 有适应/填充背景图像的属性 |
| 内容窗格 | 有过滤和搜索功能 |
| 地图页面 | 新增线性飞行过渡效果 |

### 8.11 打印和导出

| 改进项 | 说明 |
|--------|------|
| 本地场景可导出为 .stl 或 .gltf 格式 | 3D 打印支持 |
| 可设置无障碍 PDF 的元素阅读顺序 | 无障碍支持 |
| 导出运行模式选择 | 性能控制 |
| EPS 导出 | 支持自适应和 JPEG 压缩选项 |

### 8.12 报告

| 改进项 | 说明 |
|--------|------|
| 可在地图中高亮显示报告中涉及的要素 | 联动高亮 |
| 组页眉/页脚和报告页脚 | 可保持在一起 |
| 附件元素增强 | 重复行配置、表达式过滤、每页一个显示 |

### 8.13 模拟

| 改进项 | 说明 |
|--------|------|
| 水源和汇水区之间可移动水 | 水利模拟改进 |
| 可从线要素创建渠道和障碍元素 | 地形修改 |
| 障碍可在创建时加密 | 精度控制 |
| 多维云栅格格式文件的时间戳 | 可定义起始水位 |

### 8.14 样式

| 改进项 | 说明 |
|--------|------|
| Web 样式共享 | 支持颜色和颜色方案 |
| 新增 5 个 MGRS 网格样式项 | 军事标准支持 |
| 新增 21 个可再生能源点符号 | 新能源符号库 |

### 8.15 符号

| 改进项 | 说明 |
|--------|------|
| 语义搜索查找符号和样式项 | 搜索改进 |
| 网格符号和 3D 多边形 | 支持描边符号图层 |
| 军事字典 | 支持可变宽度空中走廊 |

### 8.16 时间

- 要素服务图层的时间范围属性可调整或禁用

---

## 九、Production 制图

### 9.1 Airports

- 产品数据文件更新
- 多个模板新增或更新

### 9.2 Aviation Charting

- 新增 Aviation Resize 命令调整机场注记大小
- 新增 ICAO Instrument (SID and STAR) 模板
- 产品数据文件更新

### 9.3 Bathymetry

- 支持 S-111 规则网格生产
- BIS_Dataset_Status 字段支持
- 可使用 Deactivate Covered Data 工具

### 9.4 Maritime

- S-100 Set Scale Band 工具组过滤数据
- S-101 架构特征从多点改为点
- Color-Filled ZOC 工具可用
- IENC 2.6 架构更新

### 9.5 Pipeline Referencing

- 与 Utility Network 集成增强
- **Merge Centerlines** 工具减少分割
- LRS 交叉要素类可用作参考层
- Location Referencing 选项增强

---

## 十、ArcGIS Reality for ArcGIS Pro

- 不再支持 Single Use 许可类型
- 激光雷达点云和轨迹信息可与无人机影像处理集成
- 支持 pitch、roll、yaw 传感器姿态信息
- 新增 Challenging 块调整选项
- 支持信号化地面控制点自动检测和标记
- 新增 2D/3D 网格异常编辑工具
- 支持 Cartosat-2 和 Cartosat-3 传感器数据

---

## 十一、开发者/ArcPy 影响

### 11.1 ArcGIS Arcade

- 支持 ArcGIS Arcade 1.35 版本
- 新增 Imagery popup 和 Imagery popup element 配置文件
- 栅格图层、镶嵌图层和影像服务图层支持

### 11.2 Python

- 克隆 Python 环境不再下载包，速度更快，支持离线计算机
- 地理编码模块增强
- Network Analyst 模块增强

### 11.3 地理处理服务

- 可直接从工具箱发布 Web 工具，无需先本地运行
- 新的发布整合选项更好地控制资源打包

### 11.4 ArcPy 模块影响

- 新增大量地理处理工具需更新脚本引用
- 参数变更可能影响现有脚本
- 电信域网络相关工具可能需要新的工作流

---

## 十二、已知问题与注意事项

### 12.1 兼容性变化

| 变化项 | 说明 |
|--------|------|
| ArcGIS Reality for ArcGIS Pro | 不再支持 Single Use 许可类型，需使用 Named User 许可 + Reality 扩展 |
| 部分工具 | 现对 ArcGIS Pro Basic 许可用户可用（需特定扩展） |
| 数据格式 | 支持 PostgreSQL 18.1 和 Microsoft SQL Server 2025 |
| 个人地理数据库 | 可转换为现代格式（移动/文件地理数据库） |
| 坐标系统 | 更新到 EPSG v12.049（不含 ETRS89 修订） |
| Parquet | 支持 Apache Parquet 地理空间类型 |

### 12.2 渲染引擎

- 新增 **Vulkan** 作为渲染引擎选项
- 渲染引擎不受硬件支持时发出绘制警报

### 12.3 安装参数

- 新增 `DISABLE_EXTERNAL_TRAFFIC` 静默安装参数
- 防止向 ArcGIS Online 发送请求（离线环境适用）

---

## 十三、与 V3.3 知识库的关联

### 13.1 新增内容对应现有文件

| ArcGIS Pro 3.7 新功能 | 对应 GIS Skill 文件 | 关联方式 |
|--------------------------|---------------------|----------|
| Embeddings-Based Analysis | `27_AI_GIS.md` | 新增 AI 嵌入分析章节 |
| Telecom Domain Networks | `16_SuperMap_iDesktopX_实战.md` | Utility Network 扩展说明 |
| File Knowledge Graph | `23_WebGIS开发实战.md` | 知识图谱集成说明 |
| Extract Scanned Lines/Polygons | `14_CASS11.0实战.md` | 历史地形图数字化工作流 |
| Create Terrain From BIM | `30_GIS↔CAD数据转换实战.md` | BIM 到 GIS 工作流 |
| TIN To Multipatch | `20_移动采集与实景三维.md` | 三维格式转换 |
| Spatial Analyst 新增工具 | `24_遥感与GEE实战.md` | 栅格分析增强 |
| GeoAI 工具箱 | `27_AI_GIS.md` | 完整新章节 |
| Knowledge Graph 工具箱 | `23_WebGIS开发实战.md` | 知识图谱章节 |
| Trace Network 增强 | `16_SuperMap_iDesktopX_实战.md` | 网络分析扩展 |

### 13.2 建议后续行动

1. **更新 `14_CASS11.0实战.md`**：添加 ArcGIS Pro 3.7 扫描地图数字化新工作流
2. **更新 `27_AI_GIS.md`**：添加 Embeddings-Based Analysis 和 GeoAI 工具箱完整说明
3. **更新 `16_SuperMap_iDesktopX_实战.md`**：添加 Telecom Domain Networks 说明
4. **创建 `39_ArcGIS_Pro_与知识图谱.md`**（可选）：专门介绍 File Knowledge Graph 功能
5. **更新 `20_移动采集与实景三维.md`**：添加 TIN To Multipatch 工具说明

---

## 十四、总结

ArcGIS Pro 3.7（2026年5月发布）是一个**重大更新版本**，主要亮点：

| 亮点 | 价值 |
|------|------|
| 文件知识图谱 | 无需 Enterprise 即可使用知识图谱功能（门槛大幅降低） |
| 电信域网络 | Utility Network 覆盖电信行业 |
| 嵌入分析 | AI 驱动的语义分析能力（GIS + AI 深度融合） |
| Analyze Map 窗格 | 地图性能诊断工具（大规模数据生产必备） |
| 按地图框控制图层可见性 | 布局灵活性大幅提升 |
| 离线帮助系统重构 | 通过 Documentation Center 管理 |
| 大量新地理处理工具 | 涵盖所有主要工具箱（知识库需更新） |
| 性能和生产力 | 多个领域的显著改进 |

**对 GIS Skill 知识库的影响**：
- 需要更新多个现有文件以反映 ArcGIS Pro 3.7 的新功能
- 建议创建专门的 ArcGIS Pro 新功能追踪文件（本文档即为此目的）
- AI + GIS 深度融合是未来趋势，需在 `27_AI_GIS.md` 中重点加强

---

> **收录时间**：2026-06-03
> **来源**：Esri 官方文档（doc.esri.com）完整提取
> **价值评级**：A 级（完全新增，V3.3 无此内容）
> **交叉验证**：✅ 通过（官方来源，权威性最高）
> **神经链接**：本文档与 `SKILL.md`、`27_AI_GIS.md`、`14_CASS11.0实战.md`、`16_SuperMap_iDesktopX_实战.md`、`20_移动采集与实景三维.md`、`23_WebGIS开发实战.md`、`24_遥感与GEE实战.md` 建立双向链接

*创建时间：2026-06-03*
*创建版本：V3.4*
*文件编号：38*


<!-- wm:坤图_GIS:V1.0 -->
