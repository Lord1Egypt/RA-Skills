# imutils-skill - 批量图像处理 Skill

> 📸 基于 PyImageSearch/imutils 的批量图像处理工具
> 
> ⭐ 原项目：https://github.com/PyImageSearch/imutils (4.6k stars)

---

## 🎯 功能

**批量处理图片：**
- ✅ 旋转图片（任意角度）
- ✅ 缩放图片（指定尺寸或比例）
- ✅ 平移图片（X/Y 轴移动）
- ✅ 骨架化（图像预处理）
- ✅ 批量列出图片

**适用场景：**
- 📦 电商产品图批量处理
- 📱 社交媒体配图批量调整
- 🖼️ 摄影师作品集水印
- 📊 数据增强（AI 训练图片）

---

## 🚀 快速开始

### 前提条件

1. **已安装 CLI-Anything 和 imutils CLI**
   ```bash
   # 如果还没安装，运行：
   cd E:\AI-Tools\CLI-Anything\CLI-Anything\imutils\agent-harness
   pip install -e .
   ```

2. **Python 3.10+**
3. **依赖包：** opencv-python, numpy, imutils

### 安装 Skill

```bash
# 方法 1：从 GitHub 安装（推荐）
npx skills add your-github-username/openclaw-skill-imutils

# 方法 2：本地安装
npx skills add E:\AI-Tools\CLI-Anything\openclaw-skill-imutils
```

### 使用示例

#### 1️⃣ 旋转图片

```
/rotate-image --input photo.jpg --output rotated.jpg --angle 90
```

**参数：**
- `--input` - 输入图片路径（必需）
- `--output` - 输出图片路径（必需）
- `--angle` - 旋转角度，默认 0（可选）
- `--scale` - 缩放比例，默认 1.0（可选）

**示例：**
```
/rotate-image --input cactus.jpg --output cactus_90.jpg --angle 90
```

---

#### 2️⃣ 缩放图片

```
/resize-image --input photo.jpg --output small.jpg --width 800 --height 600
```

**参数：**
- `--input` - 输入图片路径（必需）
- `--output` - 输出图片路径（必需）
- `--width` - 目标宽度（可选，0=自动计算）
- `--height` - 目标高度（可选，0=自动计算）
- `--interpolation` - 插值方法：nearest|bilinear|cubic|area|lanczos，默认 area（可选）

**示例：**
```
# 缩放到 800x600
/resize-image --input photo.jpg --output small.jpg --width 800 --height 600

# 等比例缩放（只指定宽度）
/resize-image --input photo.jpg --output small.jpg --width 800

# 等比例缩放（只指定高度）
/resize-image --input photo.jpg --output small.jpg --height 600
```

---

#### 3️⃣ 平移图片

```
/translate-image --input photo.jpg --output shifted.jpg --x 50 --y 30
```

**参数：**
- `--input` - 输入图片路径（必需）
- `--output` - 输出图片路径（必需）
- `--x` - X 轴平移像素，默认 0（可选）
- `--y` - Y 轴平移像素，默认 0（可选）

**示例：**
```
# 向右平移 50 像素，向下平移 30 像素
/translate-image --input photo.jpg --output shifted.jpg --x 50 --y 30
```

---

#### 4️⃣ 骨架化

```
/skeletonize --input photo.jpg --output skeleton.jpg
```

**参数：**
- `--input` - 输入图片路径（必需）
- `--output` - 输出图片路径（必需）

**示例：**
```
/skeletonize --input text.png --output text_skeleton.png
```

---

#### 5️⃣ 批量列出图片

```
/list-images --folder ./photos --ext .jpg
```

**参数：**
- `--folder` - 图片文件夹路径（必需）
- `--ext` - 图片扩展名，默认 .jpg（可选）

**示例：**
```
/list-images --folder E:\客户图片 --ext .jpg
```

---

## 💼 批量处理脚本

### 场景 1：批量旋转 90 度

```
批量旋转当前文件夹所有图片 90 度，输出到 rotated/ 文件夹
```

**AI 会执行：**
```powershell
New-Item -ItemType Directory -Path "rotated" -Force
$files = Get-ChildItem "*.jpg"
foreach ($file in $files) {
    $output = "rotated/" + $file.Name
    /rotate-image --input $file.FullName --output $output --angle 90
}
```

---

### 场景 2：批量缩放到社交媒体尺寸

```
把所有图片缩放到微信公众号封面尺寸（900x383）
```

**AI 会执行：**
```powershell
New-Item -ItemType Directory -Path "wechat" -Force
$files = Get-ChildItem "*.jpg"
foreach ($file in $files) {
    $output = "wechat/" + $file.Name
    /resize-image --input $file.FullName --output $output --width 900 --height 383
}
```

---

### 场景 3：批量添加边框（平移实现）

```
给所有图片添加 50 像素的白色边框
```

**AI 会执行：**
```powershell
New-Item -ItemType Directory -Path "bordered" -Force
$files = Get-ChildItem "*.jpg"
foreach ($file in $files) {
    # 先缩放图片（缩小）
    $temp = "temp_" + $file.Name
    /resize-image --input $file.FullName --output $temp --width 700 --height 700
    # 再平移（创造边框效果）
    $output = "bordered/" + $file.Name
    /translate-image --input $temp --output $output --x 50 --y 50
    Remove-Item $temp
}
```

---

## 📊 性能参考

| 任务 | 图片数量 | 用时 | 收费参考 |
|------|---------|------|---------|
| 批量旋转 | 100 张 | 1-2 分钟 | ¥500-800 |
| 批量缩放 | 500 张 | 3-5 分钟 | ¥1500-2500 |
| 批量平移 | 200 张 | 2-3 分钟 | ¥800-1200 |
| 混合处理 | 1000 张 | 10-15 分钟 | ¥3000-5000 |

*注：性能取决于 CPU 和图片大小，收费参考市场价*

---

## 🔧 技术细节

### CLI 实现

本 Skill 封装了 `cli-anything-imutils` 命令行工具：

```python
# 核心依赖
from imutils import rotate, resize, translate, skeletonize
import cv2
import numpy as np
```

### 文件结构

```
openclaw-skill-imutils/
├── SKILL.md              # 本文件
├── scripts/
│   ├── rotate.js         # 旋转脚本
│   ├── resize.js         # 缩放脚本
│   ├── translate.js      # 平移脚本
│   └── skeleton.js       # 骨架化脚本
└── references/
    └── imutils-docs.md   # 参考文档
```

---

## 📚 参考资源

- **原项目：** https://github.com/PyImageSearch/imutils
- **imutils 文档：** https://github.com/PyImageSearch/imutils#readme
- **OpenCV 文档：** https://docs.opencv.org/
- **PyImageSearch 教程：** https://www.pyimagesearch.com/

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

**作者：** Boss（通过 AI 辅助开发）  
**AI 助手：** Jarvis (OpenClaw)  
**发布日期：** 2026-03-14

---

## 📝 更新日志

### v1.0.0 (2026-03-14)
- ✅ 初始版本
- ✅ 实现旋转、缩放、平移、骨架化功能
- ✅ 添加批量处理示例
- ✅ 添加接单场景参考

---

## 💬 使用技巧

**对 AI 这样说：**
```
"用 imutils-skill 批量处理这些图片"
"把所有产品图旋转 90 度"
"缩放到微信公众号尺寸"
"给这 100 张图添加边框"
```

**AI 会自动：**
1. 调用对应的命令
2. 批量处理文件
3. 输出到指定文件夹
4. 报告处理结果

---

**Happy Coding! 🎉**
