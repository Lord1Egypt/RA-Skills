---
name: Image 3D Scene Reconstruction | 图像3D场景重建
description: Reconstruct 3D scenes from single images using depth estimation. 从单张图片重建3D场景结构（深度图、点云、Mesh）。
---

# Image 3D Scene Reconstruction | 图像3D场景重建

从卫星图、航拍图或普通照片重建三维场景结构。基于 DA3Metric-Large（Depth Anything 3）深度估计模型，单张图片即可输出深度图、点云和 3D 模型。

Reconstruct 3D scenes from satellite, aerial, or regular photos. Based on DA3Metric-Large (Depth Anything 3), outputs depth maps, point clouds, and 3D models from a single image.

---

## 能力 | Capabilities

- **单图深度估计**：输入一张图片，输出米制深度图（米为单位）
- **点云生成**：从深度图反投影生成彩色 3D 点云
- **3DGS 输出**：模型内置 3D Gaussian Splatting 能力
- **相机位姿估计**：自动估计相机内外参
- **多图融合**：支持多张图片输入做场景融合

## 使用方式 | Usage

### 快速开始

```bash
cd ~/.openclaw/workspace/projects/image-3d-scene-reconstruction
python3 scripts/reconstruct.py --input photo.jpg --output output/
```

### Python API

```python
from depth_anything_3.api import DepthAnything3
import cv2

model = DepthAnything3.from_pretrained('depth-anything/DA3Metric-Large')
model = model.cuda().eval()

img = cv2.imread('photo.jpg')
pred = model.inference([img])

depth = pred.depth[0]        # [H, W] 米制深度
extrinsics = pred.extrinsics  # 相机外参
intrinsics = pred.intrinsics  # 相机内参
```

### CLI

```bash
# 单张图片 → 3D 输出
python3 -m depth_anything_3.cli image photo.jpg --export-dir output/ --export-format glb

# 多张图片 → 融合场景
python3 -m depth_anything_3.cli images ./photos/ --export-dir output/
```

## 依赖 | Dependencies

| 包 | 用途 |
|---|------|
| depth-anything-3 | 深度估计 + 3D 重建引擎 |
| opencv-python | 图像处理 |
| torch + torchvision | PyTorch 深度学习框架 |
| open3d | 点云处理（可选） |
| trimesh | Mesh 处理（可选） |

## 硬件要求 | Hardware

- **GPU**：NVIDIA GPU，6GB+ VRAM（GTX 1060 及以上）
- **CUDA**：12.1+（PyTorch 2.5+）
- **CPU 模式**：可用但极慢，仅推荐测试

## 项目文件 | Project Files

详见 `~/.openclaw/workspace/projects/image-3d-scene-reconstruction/README.md`
