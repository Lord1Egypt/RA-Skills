<!-- wm:坤图_GIS:V5.0 -->
---
knowledge_id: GIS-KB-G04-007-EXP01
group: 4
group_name: "开发与自动化"
title: "27号扩展：GeoAI全链路工程化·SAM/LangSAM·空间大模型·RAG·提示词工程"
source_file: "27_AI_GIS.md"
version: "V5.0"
last_updated: "2026-06-23"
---

# 27号模块 V5.0 扩展：GeoAI从理论到工程化落地

---

## 一、SAM/LangSAM 遥感影像分割全流程

### 1.1 SAM (Segment Anything Model)

```python
"""SAM遥感影像分割完整流水线"""
import rasterio
import numpy as np
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
import geopandas as gpd
from shapely.geometry import Polygon, mapping

# === 1. 加载SAM模型 ===
sam = sam_model_registry["vit_h"](
    checkpoint="sam_vit_h_4b8939.pth"
)
sam.to("cuda")

# === 2. 读取遥感影像(三波段RGB) ===
with rasterio.open("ortho_0.1m.tif") as src:
    image = src.read([1, 2, 3])  # R,G,B
    profile = src.profile
    transform = src.transform

# 归一化到0-255
image = ((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8)
image = np.transpose(image, (1, 2, 0))  # HWC

# === 3. 自动分割 ===
mask_generator = SamAutomaticMaskGenerator(
    model=sam,
    points_per_side=32,       # 每边采样点(越大越密)
    pred_iou_thresh=0.88,     # IoU阈值
    stability_score_thresh=0.95,
    min_mask_region_area=100,  # 最小区域面积(像素)
)

masks = mask_generator.generate(image)
print(f"检测到 {len(masks)} 个目标")

# === 4. 分割结果转GIS矢量 ===
geometries = []
for mask_data in masks:
    mask = mask_data['segmentation']
    
    # 二值掩膜 → 轮廓 → Polygon
    contours, _ = cv2.findContours(
        mask.astype(np.uint8), 
        cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_SIMPLE
    )
    
    for contour in contours:
        if len(contour) < 4:
            continue
        # 像素坐标 → 地理坐标
        geo_coords = [rasterio.transform.xy(transform, p[0][1], p[0][0]) 
                      for p in contour]
        poly = Polygon(geo_coords)
        if poly.is_valid and poly.area > 10:  # 最小面积10m²
            geometries.append({
                'geometry': mapping(poly),
                'properties': {
                    'area': poly.area,
                    'iou': mask_data['predicted_iou'],
                    'stability': mask_data['stability_score']
                }
            })

# === 5. 输出GeoJSON ===
gdf = gpd.GeoDataFrame.from_features(geometries, crs=src.crs)
gdf.to_file("sam_segmentation_results.gpkg", driver="GPKG")
```

### 1.2 LangSAM（语言驱动的SAM）

```python
"""LangSAM：用自然语言指定分割目标"""
from lang_sam import LangSAM

model = LangSAM()
image_pil = Image.open("ortho.tif").convert("RGB")

# 文本提示词驱动分割
text_prompt = "building with red roof"
masks, boxes, phrases, logits = model.predict(image_pil, text_prompt)

print(f"检测到 {len(phrases)} 个'{text_prompt}'")
for i, (mask, box, phrase) in enumerate(zip(masks, boxes, phrases)):
    print(f"  目标{i}: {phrase}, bbox={box}")
    # mask → GeoJSON (同上)
```

### 1.3 SAM在GIS中的典型场景

| 场景 | 提示词 | 成果 | 后处理 |
|------|--------|------|--------|
| 建筑物提取 | "building"/"house" | 建筑物轮廓面 | 规则化(直角化/最小面积过滤) |
| 道路提取 | "road"/"highway" | 道路中心线 | 骨架化+拓扑连接 |
| 水体提取 | "water"/"lake"/"river" | 水体面 | NDWI交叉验证 |
| 农田地块 | "farmland"/"field" | 地块面 | 面积统计+作物分类 |
| 车辆检测 | "car"/"vehicle" | 车辆点 | 去重(重叠框NMS) |

---

## 二、空间大模型与RAG部署

### 2.1 GIS LLM本地部署方案

```python
"""GIS领域RAG知识库搭建"""
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
import os

# === 1. 嵌入模型(中文优化) ===
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-zh-v1.5",  # 中文Embedding SOTA
    model_kwargs={'device': 'cuda'},
    encode_kwargs={'normalize_embeddings': True}
)

# === 2. 向量数据库 ===
vectorstore = Chroma(
    persist_directory="./gis_knowledge_db",
    embedding_function=embeddings
)

# === 3. 加载GIS文档到向量库 ===
from langchain_community.document_loaders import DirectoryLoader
loader = DirectoryLoader(
    "./GIS_SKILL/knowledge_base/",
    glob="**/*.md",
    show_progress=True
)
documents = loader.load()

# 分块存储
from langchain.text_splitter import MarkdownHeaderTextSplitter
splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("##", "Section"),
        ("###", "SubSection"),
    ]
)
docs = splitter.split_documents(documents)
vectorstore.add_documents(docs)
print(f"已索引 {len(docs)} 个文档块")

# === 4. 搭建RAG问答链 ===
llm = Ollama(model="qwen2.5:14b")  # 或其他本地模型

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(
        search_kwargs={"k": 5}  # 检索top-5相关文档
    ),
    return_source_documents=True
)

# === 5. GIS领域问答 ===
result = qa_chain({
    "query": "CGCS2000 3度带 36度带 的中央子午线和EPSG是什么？"
})
print(f"答案: {result['result']}")
print(f"参考文档: {[d.metadata for d in result['source_documents']]}")
```

### 2.2 空间提示词工程模板

```python
"""GIS专用结构化提示词"""
GIS_SYSTEM_PROMPT = """你是GIS地理信息专家，基于知识库回答测绘/GIS相关问题。

回答规则:
1. 坐标系问题必须附带EPSG/WKID
2. 国标问题必须引用标准编号
3. 坐标转换问题必须说明适用精度范围
4. 软件操作必须区分ArcGIS/QGIS/SuperMap
5. 数据格式问题必须说明优缺点和适用场景
6. 不确定的信息明确标注[需验证]
"""

COORDINATE_TRANSFORM_PROMPT = """
数据概况:
- 源坐标系: {source_crs}
- 目标坐标系: {target_crs}
- 数据范围: {bbox}
- 数据量: {count}条

问题: 如何进行批量坐标转换?

请提供:
1. 转换方法(三参数/四参数/七参数选择依据)
2. 完整的Python/GDAL代码
3. 常见错误和解决方案
4. 精度评估方法
"""

DATA_QC_PROMPT = """
质检任务: {task_type}
数据格式: {format}
坐标系: {crs}
检查标准: {standard}

请输出:
1. 质检项清单(按致命/严重/一般/轻微分级)
2. 自动化检查脚本
3. 质检报告模板
"""
```

---

## 三、深度学习遥感解译全栈

### 3.1 地物分类（PyTorch + Rasterio）

```python
"""基于预训练模型的遥感影像语义分割"""
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import rasterio
import numpy as np

class UNet(nn.Module):
    """轻量级UNet用于遥感分割"""
    def __init__(self, in_channels=3, out_channels=6):
        super().__init__()
        # Encoder
        self.enc1 = self._conv_block(in_channels, 64)
        self.enc2 = self._conv_block(64, 128)
        self.enc3 = self._conv_block(128, 256)
        self.pool = nn.MaxPool2d(2)
        
        # Bottleneck
        self.bottleneck = self._conv_block(256, 512)
        
        # Decoder
        self.up3 = nn.ConvTranspose2d(512, 256, 2, 2)
        self.dec3 = self._conv_block(512, 256)
        self.up2 = nn.ConvTranspose2d(256, 128, 2, 2)
        self.dec2 = self._conv_block(256, 128)
        self.up1 = nn.ConvTranspose2d(128, 64, 2, 2)
        self.dec1 = self._conv_block(128, 64)
        
        self.final = nn.Conv2d(64, out_channels, 1)
    
    def _conv_block(self, in_c, out_c):
        return nn.Sequential(
            nn.Conv2d(in_c, out_c, 3, padding=1),
            nn.BatchNorm2d(out_c),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_c, out_c, 3, padding=1),
            nn.BatchNorm2d(out_c),
            nn.ReLU(inplace=True),
        )
    
    def forward(self, x):
        e1 = self.enc1(x); p1 = self.pool(e1)
        e2 = self.enc2(p1); p2 = self.pool(e2)
        e3 = self.enc3(p2); p3 = self.pool(e3)
        b = self.bottleneck(p3)
        d3 = self.dec3(torch.cat([self.up3(b), e3], 1))
        d2 = self.dec2(torch.cat([self.up2(d3), e2], 1))
        d1 = self.dec1(torch.cat([self.up1(d2), e1], 1))
        return self.final(d1)

# 影像Tile读取器
class GeoTileDataset(torch.utils.data.Dataset):
    def __init__(self, image_path, mask_path, tile_size=256):
        self.image_src = rasterio.open(image_path)
        self.mask_src = rasterio.open(mask_path)
        self.tile_size = tile_size
        
    def __getitem__(self, idx):
        # 随机裁切256×256 tile
        row = np.random.randint(0, self.image_src.height - self.tile_size)
        col = np.random.randint(0, self.image_src.width - self.tile_size)
        
        img = self.image_src.read(window=((row, row+self.tile_size), 
                                           (col, col+self.tile_size)))
        mask = self.mask_src.read(1, window=((row, row+self.tile_size),
                                              (col, col+self.tile_size)))
        
        # 归一化
        img = img.astype(np.float32) / 255.0
        mask = mask.astype(np.int64)
        
        return torch.FloatTensor(img), torch.LongTensor(mask)
```

### 3.2 常用模型选择决策

| 模型 | 遥感任务 | 精度 | 速度 | 显存需求 | 推荐场景 |
|------|---------|------|------|---------|---------|
| **UNet** | 语义分割 | ★★★★ | ★★★ | 4-8GB | 通用地物分类 |
| **DeepLabV3+** | 语义分割 | ★★★★★ | ★★ | 8-16GB | 精细边界提取 |
| **YOLOv8** | 目标检测 | ★★★★★ | ★★★★★ | 4-8GB | 车辆/建筑检测 |
| **SAM** | 通用分割(Zero-shot) | ★★★★ | ★★★ | 8-16GB | 无需训练/快速探索 |
| **Swin Transformer** | 语义分割(大模型) | ★★★★★ | ★ | 16-32GB | 最高精度场景 |
| **ResNet50** | 场景分类 | ★★★★ | ★★★★ | 4-8GB | Land Use分类 |
| **PointNet++** | 点云分类 | ★★★★ | ★★★ | 8-16GB | LiDAR点云分类 |

---

> **V5.0 新增内容说明**：SAM/LangSAM遥感分割完整流水线(含GeoJSON输出/PyTorch UNet/GIS本地RAG部署/LangChain向量化/空间提示词工程模板/模型选型决策表。原27号模块(403行)仅涉及基础GeoAI概念，现扩展至完整工程化解决方案。
