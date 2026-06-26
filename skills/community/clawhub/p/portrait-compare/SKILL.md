---
name: portrait-compare
description: >
  人脸识别与相似度比对 skill。当用户上传两张照片并询问"是否为同一个人"、"人脸相似度"、"人脸比对"、"人脸识别"、"两张图片是不是同一个人"，或需要计算两张人脸照片的相似度分数时，必须使用此 skill。
  适用场景：人证比对、照片对比、身份核验、人脸匹配等任务。即使用户只是说"帮我看看这两张照片是不是同一个人"也应触发此 skill。
compatibility: "Python >=3.8, opencv-python >=4.5, numpy, scipy, pillow. 可选高精度模式需要 face_detection_yunet_2023mar.onnx 和 face_recognition_sface_2021dec.onnx 模型文件。"
---

# 人脸识别相似度比对 Skill

## 工作流程概览

```
输入: 图片A + 图片B
   ↓
① 人脸检测 (YuNet 或 Haar Cascade)
   ↓
② 人脸区域裁剪 + 对齐
   ↓
③ 特征提取 (SFace ONNX 或 HOG+Patch)
   ↓
④ 余弦相似度计算
   ↓
输出: 相似度分数 (0~1) + 判断结论
```

---

## 第一步：确认图片输入

用户上传的图片位于 `/mnt/user-data/uploads/` 下，使用 `view` 工具列出可用文件：

```bash
ls /mnt/user-data/uploads/
```

将两张图片路径记为 `IMAGE_A` 和 `IMAGE_B`。

---

## 第二步：选择算法方案

根据环境自动选择最优方案：

| 方案 | 检测器 | 特征提取器 | 精度 | 条件 |
|------|--------|------------|------|------|
| **方案A（推荐）** | YuNet ONNX | SFace ONNX | ★★★★★ | 需要 .onnx 模型文件 |
| **方案B（通用）** | Haar Cascade | HOG + Patch Histogram | ★★★☆☆ | 仅需 OpenCV 内置 |

**如何判断用哪个方案**：运行脚本时自动检测，优先使用方案A，若模型文件不存在则自动降级为方案B。

**方案A 模型下载（可选，推荐）**：
```
https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx
https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx
```
将两个 `.onnx` 文件放在工作目录或 `/tmp/` 下。

---

## 第三步：执行识别脚本

使用以下脚本（也可直接调用 `scripts/face_compare.py`）：

```bash
python3 /home/claude/face-recognition/scripts/face_compare.py \
  --img1 IMAGE_A \
  --img2 IMAGE_B \
  --output /tmp/face_result.jpg
```

脚本会自动：
1. 检测两张图片中的人脸区域
2. 裁剪并标注人脸框
3. 提取人脸特征向量
4. 计算余弦相似度
5. 输出带标注的对比图 + 相似度分数

---

## 第四步：解读结果并向用户汇报

### 相似度分数判读表

| 相似度分数 | 判断结论 |
|-----------|---------|
| 0.90 ~ 1.00 | ✅ **极高概率为同一人**（强烈匹配） |
| 0.75 ~ 0.90 | ✅ **很可能为同一人**（高置信度） |
| 0.60 ~ 0.75 | ⚠️ **可能为同一人**（中等置信度，建议人工核验） |
| 0.40 ~ 0.60 | ❓ **不确定**（低置信度） |
| 0.00 ~ 0.40 | ❌ **很可能不是同一人** |

> **注意**：以上阈值基于方案B（HOG特征）。若使用方案A（SFace），推荐阈值为 >0.593（余弦距离）。

### 向用户展示的格式示例

```
📊 人脸识别结果
━━━━━━━━━━━━━━━━━━━━
图片A：检测到 1 张人脸 ✓
图片B：检测到 1 张人脸 ✓

相似度分数：0.847
判断结论：✅ 很可能为同一人（高置信度）

使用算法：SFace (OpenCV FaceRecognizerSF)
━━━━━━━━━━━━━━━━━━━━
```

---

## 异常处理

| 问题 | 原因 | 处理方式 |
|------|------|---------|
| 未检测到人脸 | 图片质量差/无正脸 | 告知用户并建议换图 |
| 检测到多张人脸 | 图中有多人 | 取最大人脸（面积最大）处理，提示用户 |
| 图片无法读取 | 格式不支持 | 提示支持 JPG/PNG/BMP/WEBP |
| 相似度结果异常 | 光线/角度差异大 | 在结果中加注"受光照/角度影响，结果仅供参考" |

---

## 详细实现参考

→ 查看 `scripts/face_compare.py` 获取完整可执行代码
→ 查看 `references/algorithm_notes.md` 了解算法原理说明
