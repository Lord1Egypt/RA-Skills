---
name: computer-vision-opencv
description: 计算机视觉：OpenCV+PyTorch 图像/视频处理、目标检测、分割、特征提取
source:
  type: derived
  repo: skills-repo/machine-learning-engineer
  path: skills/computer-vision-opencv/SKILL.md
  url: https://skills.sh/mindrally/skills/computer-vision-opencv
  version: 1.0.0
  updated: 2026-07-30
metadata:
  author: hope
  category: 视觉
  platform: 通用
  difficulty: 进阶
  version: 1.0.0
  created: 2026-07-30
tags:
  - computer-vision
  - opencv
  - pytorch
  - image-processing
  - object-detection
---

# Computer Vision OpenCV — 计算机视觉

> 使用 OpenCV 和 PyTorch 构建图像处理、目标检测和视频分析应用。覆盖传统 CV 方法和现代深度学习技术。

## 能力

- **图像处理**：滤波、变换、形态学操作、颜色空间转换
- **目标检测**：YOLO/RT-DETR 推理、自定义检测器训练
- **图像分割**：语义分割、实例分割、SAM 集成
- **特征提取**：SIFT/ORB 传统特征 + CNN 深度特征
- **视频分析**：帧处理、光流、目标跟踪、视频摘要

## 使用方式

在 Claude Code 中使用 `/computer-vision-opencv` 调用。

```
/computer-vision-opencv 帮我用 YOLO 检测这批图片中的物体
/computer-vision-opencv 写一个实时视频流的人脸检测和模糊处理脚本
/computer-vision-opencv 从视频中提取关键帧并做目标跟踪
```

## 工作流

1. **理解需求** — 输入类型（图像/视频/流）、检测目标、精度要求
2. **预处理** — 缩放、归一化、增强、颜色校正
3. **方法选择** — 传统 CV 方法 vs 深度学习模型（按精度/速度选）
4. **实现** — OpenCV 管线或 PyTorch 模型推理
5. **后处理** — NMS、结果过滤、可视化标注

## 方法选择矩阵

| 任务 | 简单场景 | 复杂场景 |
|------|---------|---------|
| 目标检测 | Haar Cascade | YOLO/RT-DETR |
| 图像分类 | Color histograms | ResNet/ViT |
| 特征匹配 | ORB / SIFT | SuperPoint |
| 分割 | Threshold/GrabCut | SAM / Mask R-CNN |
| 跟踪 | CSRT / KCF | DeepSORT |

## 适用场景

- 图像预处理和增强（为后续深度学习准备数据）
- 使用预训练模型做目标检测/分割
- 视频流实时分析和处理
- 传统 CV 和深度学习混合方案设计

## 限制

- YOLO 等模型需要 GPU 才能实时推理
- 极低光照或遮挡场景精度有限
- 不覆盖 3D 视觉和点云处理
- 视频分析需要用户安装 ffmpeg 依赖

## 相关参考（Playbook）

- [model-evaluation playbook](../../references/model-evaluation.md) — 视觉任务的指标选择与防泄漏验证
