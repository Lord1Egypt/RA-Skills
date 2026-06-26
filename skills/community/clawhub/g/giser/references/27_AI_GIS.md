# AI+GIS 深度融合 | 关联：24_遥感与GEE.md 16_SuperMap_iDesktopX.md 25_三维GIS与数字孪生.md | V4.0 2026-06-04

> 从占位模块升级为完整 AI+GIS 知识库 | 覆盖 GeoAI/深度学习/SAM/GIS LLM/智能体
> 数据来源：Esri 官方博客 / opengeos/geoai / Meta SAM 论文 / SuperMap 2026 发布会 / QGIS GeoAI 插件

---

## 一、GeoAI 概述：AI 如何改变 GIS

### 1.1 定义与范畴

GeoAI（地理空间人工智能）= GIS + AI，核心范畴：

| 方向 | 说明 | 代表技术 |
|------|------|---------|
| **计算机视觉** | 图像理解/分割/检测 | SAM, YOLO, Mask R-CNN, DETR |
| **时空预测** | 时间序列空间预测 | LSTM, Transformer, GNN |
| **自然语言处理** | 空间文本理解 | LLM + GIS, GeoGPT |
| **强化学习** | 空间决策优化 | 路径规划, 资源调度 |
| **生成式AI** | 空间数据生成 | 地图风格迁移, 地形生成 |

### 1.2 GeoAI 技术栈三层架构

```
┌─────────────────────────────────────────────────┐
│ 应用层：智能制图 | 变化检测 | 地物分类 | 灾害评估 │
├─────────────────────────────────────────────────┤
│ 框架层：GeoAI-py | ArcGIS Learn | TorchGeo      │
│         Raster Vision | SuperMap AI SDK         │
├─────────────────────────────────────────────────┤
│ 基础层：PyTorch | TensorFlow | ONNX | CUDA      │
└─────────────────────────────────────────────────┘
```

---

## 二、深度学习遥感解译实战

### 2.1 目标检测（Object Detection）

检测遥感影像中的建筑物、车辆、船舶、飞机等地物目标。

#### ArcGIS Pro 目标检测工作流

```
1. 标注样本 → Labeling Tools (矩形框标注)
2. 导出训练数据 → Export Training Data for Deep Learning
   - 格式：PASCAL VOC / RCNN Masks
   - 切块大小：400~800px
   - 步长：50%~75%
3. 训练模型 → Train Deep Learning Model
   - 模型：Faster R-CNN / YOLOv3 / SSD / RetinaNet
   - 骨干网络：ResNet-50 / ResNet-101
   - 关键参数：batch_size=4~16, epochs=50~200
4. 推理 → Detect Objects Using Deep Learning
   - 置信度阈值：0.3~0.7
   - NMS IoU：0.15~0.4
5. 后处理 → 非极大值抑制 + 面积过滤
```

#### Python 调用 ArcPy 检测

```python
import arcpy
from arcpy.ia import *

# 目标检测推理
arcpy.ia.DetectObjectsUsingDeepLearning(
    in_raster="ortho_0.1m.tif",
    out_detected_objects="buildings_detected.shp",
    in_model_definition="building_detection.dlpk",
    arguments="padding 56;batch_size 4;threshold 0.5;"
              "return_bboxes True;nms_overlap 0.1"
)
```

#### YOLO 遥感检测（Python独立方案）

```python
from ultralytics import YOLO
import geopandas as gpd
from osgeo import gdal

# 加载预训练遥感YOLO模型
model = YOLO('yolov8x-obb.pt')  # OBB = Oriented Bounding Box

# 遥感影像检测
results = model('aerial_image.tif', 
    imgsz=1024,      # 遥感影像用大尺寸
    conf=0.25,       # 置信度阈值
    iou=0.45,        # NMS IoU阈值
    device='cuda:0'
)

# 结果转GeoDataFrame
gdf = results[0].to_geodataframe()
print(f"检测到 {len(gdf)} 个目标")
```

---

### 2.2 语义分割（Semantic Segmentation）

像素级分类——每个像素赋予类别标签（如：建筑/道路/植被/水体）。

#### ArcGIS Pro 语义分割工作流

| 步骤 | 工具 | 关键参数 |
|------|------|---------|
| 标注 | Labeling Tools（多边形） | 至少50个样本/类 |
| 导出 | Export Training Data | tile_size=256, stride=128 |
| 训练 | Train Deep Learning Model (U-Net/DeepLabV3/PSPNet) | chip_size=256~512 |
| 推理 | Classify Pixels Using Deep Learning | padding=56, batch_size=8 |
| 后处理 | Majority Filter + Boundary Clean | 去除椒盐噪声 |

#### SAM 分割实战（segment-geospatial）

```python
import leafmap
from samgeo import SamGeo
from samgeo.text_sam import LangSAM

# === 方案1: 自动分割（Segment Anything） ===
sam = SamGeo(
    model_type="vit_h",          # vit_h / vit_l / vit_b
    checkpoint="sam_vit_h_4b8939.pth",
    sam_kwargs=None,
)
# 生成分割掩膜
sam.generate("ortho.tif", "masks.tif")
# 矢量化
sam.tiff_to_vector("masks.tif", "segments.shp")

# === 方案2: 文本提示分割（Text SAM / LangSAM） ===
lang_sam = LangSAM()
# "提取所有建筑物"
lang_sam.predict("ortho.tif", 
    text_prompt="building", 
    box_threshold=0.24, 
    text_threshold=0.24
)
lang_sam.show_anns()
# 导出矢量
lang_sam.raster_to_vector("output.shp")
```

#### SAM 参数调优经验

| 参数 | 建议值 | 说明 |
|------|--------|------|
| model_type | vit_h（精度最高） | vit_l平衡，vit_b快速 |
| points_per_side | 32（默认） | 越大越精细，越慢 |
| pred_iou_thresh | 0.88 | IOU低于此值的掩膜被过滤 |
| stability_score_thresh | 0.95 | 稳定性低于此值的掩膜被过滤 |
| box_threshold (Text SAM) | 0.2~0.3 | 越低召回越多（含误检） |

---

### 2.3 变化检测（Change Detection）

对比双时相影像，自动提取变化区域。

```python
# ArcGIS Pro 变化检测
arcpy.ia.DetectObjectsUsingDeepLearning(
    in_raster=[r"t1_2023.tif", r"t2_2025.tif"],  # 双时相输入
    out_detected_objects="changes.shp",
    in_model_definition="change_detection.dlpk",
    arguments="mode change_detection"
)
```

```python
# Python GeoAI 变化检测
from geoai.change_detection import ChangeDetector

cd = ChangeDetector(
    model="changestar",
    backbone="resnet50",
    img_size=512
)
# 双时相推理
change_map = cd.detect("image_2023.tif", "image_2025.tif")
change_map.save("change_binary.tif")
```

---

## 三、GeoAI Python 生态

### 3.1 核心库速查

| 库名 | 用途 | 安装 | 规模 |
|------|------|------|------|
| **geoai-py** | 全能GIS+AI工具箱 | `pip install geoai-py` | 80+ Notebooks |
| **segment-geospatial** | SAM遥感分割 | `pip install segment-geospatial` | 快速分割 |
| **TorchGeo** | 地理空间PyTorch | `pip install torchgeo` | 数据集+模型 |
| **Raster Vision** | 遥感深度学习框架 | `pip install rastervision` | 端到端pipeline |
| **leafmap** | 交互式地图+AI集成 | `pip install leafmap` | 可视化 |

### 3.2 GeoAI 功能矩阵

| 功能 | 模块 | 示例场景 |
|------|------|---------|
| 建筑提取 | `geoai.extract` | 从高分辨率影像提取建筑物轮廓 |
| 水体检测 | `geoai.water` | Sentinel-2水体指数+深度学习 |
| 道路提取 | `geoai.segment` | DeepRoadMapper / RoadTracer |
| 土地利用分类 | `geoai.classify` | 随机森林/CNN/Transformer |
| 变化检测 | `geoai.change_detection` | 双时相变化自动标记 |
| 车辆检测 | `geoai.object_detect` | YOLO/NAS车辆计数 |
| 超分辨率 | `geoai.esrgan` | 低分辨率影像增强 |
| 冠层高度 | `geoai.canopy` | LiDAR+遥感树木高度 |
| AI代理 | `geoai.geo_agents` | LLM驱动的地理分析代理 |

### 3.3 GeoAI + QGIS 插件

QGIS GeoAI 插件允许零代码运行AI地理空间工作流：

```bash
# QGIS插件市场搜索 "GeoAI" 即可安装
# 支持功能：
# - 树冠分割 (DeepForest)
# - 水体分割 (OmniWaterMask)
# - Moondream视觉语言模型
# - Segment Anything (SAM)
# - 建筑足迹提取
# - 变化检测
```

---

## 四、ArcGIS Pro 深度学习工具箱（完整版）

### 4.1 预训练模型库（Living Atlas）

从 [ArcGIS Living Atlas](https://livingatlas.arcgis.com/en/browse/?q=dlpk#q=dlpk&d=2) 可直接下载使用：

| 模型 | 用途 | 分辨率要求 |
|------|------|-----------|
| SAM / Text SAM | 通用分割/文本提示分割 | 任意 |
| Building Footprint Extraction | 建筑物轮廓提取 | 30-50cm |
| Road Extraction | 道路中心线提取 | 30-50cm |
| Land Cover Classification (Landsat) | 土地覆盖10类 | 30m |
| Tree Point Cloud Classification | 点云树木分类 | LiDAR |
| Palm Tree Detection | 棕榈树检测 | 10-20cm |
| Swimming Pool Detection | 游泳池检测 | 15-30cm |
| Construction Site Detection | 建筑工地检测 | 50cm |
| Wind Turbine Detection | 风力发电机检测 | 15-30cm |
| Cloud Mask Generation | 云检测(Sentinel-2) | 10m |

### 4.2 深度学习环境配置

```bash
# ArcGIS Pro 深度学习环境（推荐 conda）
conda create -n dl_gis python=3.9
conda activate dl_gis

# ArcGIS Pro自带Python环境下安装
conda install -c esri arcgis
conda install -c esri deep-learning-essentials
conda install pytorch torchvision pytorch-cuda=11.8 -c pytorch -c nvidia

# 验证安装
python -c "from arcgis.learn import prepare_data, UnetClassifier; print('OK')"
```

### 4.3 File Knowledge Graph（3.7 新增）

ArcGIS Pro 3.7 新增的桌面级**文件知识图谱**：
- 自动发现文件系统中的GIS文件关系
- 支持.dwg/.shp/.gdb/.tif等格式互关联
- 为Embeddings-Based Analysis提供数据底座

---

## 五、智能体时代：SuperMap AgentX 与 GIS LLM

### 5.1 SuperMap AgentX 核心能力

| 能力 | 说明 |
|------|------|
| **自然语言交互** | 用自然语言描述GIS任务，AgentX自动执行 |
| **IM远程任务** | 通过IM工具（如企业微信）远程下发GIS任务 |
| **专业Skills库** | 空间分析/遥感提取/数据质检/智能制图等预置技能 |
| **GIS专家库** | 内置领域知识，自动选择合适的工具和参数 |
| **Skill Hub集成** | 社区贡献的技能可无缝接入 |

### 5.2 GIS+LLM 典型应用场景

```
用户："帮我分析这个区域的过去5年土地利用变化，出报告"
  → AgentX 拆解任务：
    1. 调用遥感解译 Skill（Landsat/Sentinel分类）
    2. 调用变化检测 Skill（逐年对比）
    3. 调用统计分析 Skill（面积/转移矩阵）
    4. 调用制图 Skill（变化专题图）
    5. 调用报告生成 Skill（自动撰写分析报告）
    6. 输出：分类图+变化图+统计表+分析报告.doc
```

### 5.3 文本驱动 GIS 操作

```python
# 概念示例：LLM + GIS 操作链
# "提取研究区内所有建筑物，计算每个建筑的阴影面积比例"

# LLM 自动生成执行代码：
def extract_buildings_shadow_ratio(aoi, imagery):
    # Step 1: 裁剪研究区影像
    clipped = gdal.Warp("clipped.tif", imagery, 
                        cutlineDSName=aoi, cropToCutline=True)
    # Step 2: SAM 建筑提取
    from samgeo import SamGeo
    sam = SamGeo(model_type="vit_h", ...)
    sam.generate("clipped.tif", "buildings_mask.tif")
    # Step 3: 阴影检测（NDUI指数计算）
    # Step 4: 空间叠加 + 面积统计
    # Step 5: 输出结果表
    return result_df
```

---

## 六、实战案例

### 6.1 案例1：城市违建识别

**任务**：从0.5m高分辨率影像中识别疑似违建。

**方案**：
```
双时相影像(2025.03 vs 2025.09)
  → SAM 建筑分割（两个时相分别）
  → ChangeDetector 变化检测
  → 叠加规划红线
  → 输出：变化图斑 + 疑似违建列表
```

**关键代码**：
```python
# 步骤1：SAM分割两期影像
sam_v1 = SamGeo().generate("202503.tif", "mask_v1.tif")
sam_v2 = SamGeo().generate("202509.tif", "mask_v2.tif")

# 步骤2：变化检测
import numpy as np
v1 = gdal.Open("mask_v1.tif").ReadAsArray()
v2 = gdal.Open("mask_v2.tif").ReadAsArray()
change = (v1 == 0) & (v2 > 0)  # 新增建筑

# 步骤3：空间叠加规划红线判断合规性
```

### 6.2 案例2：作物类型分类

**任务**：Sentinel-2 时序影像识别水稻/小麦/玉米/大豆。

**方案**：使用 TorchGeo + Transformer
```python
from torchgeo.models import get_weight
from torchgeo.datasets import EuroSAT, SeasonalContrastS2C

# 加载预训练时序模型
model = get_weight("ssl4eo_l_rn50")  # 自监督预训练
# 微调作物分类
```

---

## 七、AI+GIS 前沿趋势

| 趋势 | 说明 | 成熟度 |
|------|------|--------|
| **基础模型（Foundation Models）** | Prithvi(SATLAS) / ClimaX / SatCLIP 预训练遥感大模型 | 🟡 2025成长期 |
| **多模态GIS** | 图像+文本+时序+矢量统一理解 | 🟡 研究阶段 |
| **Agent化GIS** | GIS从工具→任务执行智能体 | 🟢 2026落地(SuperMap AgentX) |
| **实时AI** | 边缘计算+卫星视频实时分析 | 🟡 2025-2026 |
| **NeRF/3DGS GIS** | 神经渲染三维重建（替代传统倾斜摄影） | 🟡 2025试验 |

---

## 八、学习资源

| 资源 | 链接 |
|------|------|
| Esri GeoAI Blog | https://www.esri.com/arcgis-blog/products/arcgis-pro/geoai/ |
| GeoAI Python 文档 | https://geoai.gishub.org/ |
| SAM 遥感分割 | https://samgeo.gishub.org/ |
| TorchGeo 官方 | https://torchgeo.readthedocs.io/ |
| QGIS GeoAI 插件 | plugins.qgis.org/plugins/geoai/ |
| SuperMap 2026 AgentX | www.supermap.com |

---

> **神经连接**：
> - `24_遥感与GEE.md` — 遥感数据预处理与GEE云计算
> - `16_SuperMap_iDesktopX.md` — SuperMap AgentX 智能体详细操作
> - `25_三维GIS与数字孪生.md` — AI驱动三维建模
> - `29_避坑库110+.md` — B.20 GeoAI+深度学习避坑条目
> - `36_LiDAR360_点云处理软件.md` — 点云AI分类（PTD/CSF）

*创建时间：2026-06-03（V3.0预留占位）→ 2026-06-04（V4.0完整重写，45%→75%）*
*维护者：GIS Skill 自进化引擎*


<!-- wm:坤图_GIS:V1.0 -->
