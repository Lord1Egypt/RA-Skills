---
name: opencv
description: Computer vision and image processing using OpenCV WebAssembly. Uses opencv-component.wasm running in openclaw-wasm-sandbox plugin. Supports image processing, object detection, feature extraction, panorama stitching, photo filters, camera calibration, and ML. 图像处理、OpenCV、目标检测、特征提取、图像拼接、相机标定、机器学习
---

# OpenCV Computer Vision Skill

Comprehensive computer vision and image processing using OpenCV WebAssembly.

## Trigger When

使用此技能的场景：

- **图像处理 / Image Process**：resize（调整大小）、blur（模糊）、threshold（阈值）、morphology（形态学）、sharpen（锐化）、crop（裁剪）、stats（统计）
- **目标检测 / Detection**：cascade（级联检测）、dnn/YOLO（深度学习检测）、hog、contour（轮廓）、circle（圆检测）、line（直线检测）
- **特征提取 / Features**：orb、sift、akaze、match（特征匹配）、homography（单应性）、optflow（光流）、template（模板匹配）
- **图像拼接 / Stitching**：panorama（全景拼接）、stitch（多图拼接，扫描件模式）
- **照片处理 / Photo**：denoise（降噪）、inpaint（修复）、stylize（风格化）、hdr、pencil（素描）、detail（细节增强）
- **相机标定 / Calibration**：chessboard（棋盘格）、undistort（去畸变）、corners（亚像素角点）、pose（位姿估计）
- **机器学习 / ML**：train-knn（训练KNN）、train-svm（训练SVM）、predict（预测）、kmeans（聚类）
- **批处理 / Batch**：batch-process（批量处理）、batch-convert（格式转换）、batch-stats（批量统计），支持多线程

## Prerequisites

- **Required plugin:** `openclaw-wasm-sandbox`
- **WASM file:** `~/.openclaw/skills/opencv/files/opencv-component.wasm`
  - Download if missing:
    ```bash
    openclaw wasm-sandbox download \
      "https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/opencv/files/opencv-component.wasm" \
      "~/.openclaw/skills/opencv/files/opencv-component.wasm"
    ```

## Tool

Use `wasm-sandbox-run` tool with the WASM file:

```javascript
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/opencv/files/opencv-component.wasm",
  args: ["<operation>", ...args]
})
```

For file access, use `workDir` or `mapDir` to expose directories to the sandbox.

## Operations Overview

| Category | Operations |
|----------|-----------|
| **Image Process** | resize, blur, threshold, morphology, sharpen, crop, stats |
| **Detection** | cascade, dnn (YOLO), hog, contour, circle, line |
| **Features** | orb, sift, akaze, match, homography, optflow, template |
| **Stitching** | panorama, stitch |
| **Photo** | denoise, inpaint, stylize, hdr, pencil, detail |
| **Calibration** | chessboard, undistort, corners, pose |
| **ML** | train-knn, train-svm, predict, kmeans |
| **Batch** | batch-process, batch-convert, batch-stats |

## Detailed Usage

See [references/operations.md](references/operations.md) for complete operation reference with arguments, examples, and sandbox notes.
