# 📸 openclaw-skill-imutils

> OpenClaw Skill for batch image processing - 批量图像处理工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/PyImageSearch/imutils?label=imutils)](https://github.com/PyImageSearch/imutils)

---

## 🎯 功能

- ✅ **旋转图片** - 任意角度旋转
- ✅ **缩放图片** - 指定尺寸或等比例缩放
- ✅ **平移图片** - X/Y 轴移动
- ✅ **骨架化** - 图像预处理
- ✅ **批量处理** - 一次处理成百上千张图片

---

## 🚀 快速开始

### 前提条件

1. **安装 Python 3.10+**
2. **安装 imutils CLI**
   ```bash
   cd E:\AI-Tools\CLI-Anything\CLI-Anything\imutils\agent-harness
   pip install -e .
   ```

### 安装 Skill

#### 方法 1：从 GitHub 安装（推荐）

```bash
npx skills add YOUR_GITHUB_USERNAME/openclaw-skill-imutils
```

#### 方法 2：本地安装

```bash
npx skills add E:\AI-Tools\CLI-Anything\openclaw-skill-imutils
```

### 使用示例

#### 旋转图片
```
/rotate-image --input photo.jpg --output rotated.jpg --angle 90
```

#### 缩放图片
```
/resize-image --input photo.jpg --output small.jpg --width 800 --height 600
```

#### 平移图片
```
/translate-image --input photo.jpg --output shifted.jpg --x 50 --y 30
```

---

## 💼 接单场景

| 任务 | 图片数量 | 用时 | 收费参考 |
|------|---------|------|---------|
| 批量旋转 | 100 张 | 1-2 分钟 | ¥500-800 |
| 批量缩放 | 500 张 | 3-5 分钟 | ¥1500-2500 |
| 批量平移 | 200 张 | 2-3 分钟 | ¥800-1200 |
| 混合处理 | 1000 张 | 10-15 分钟 | ¥3000-5000 |

---

## 📚 详细文档

查看 [SKILL.md](SKILL.md) 获取完整使用说明。

---

## 🔧 开发

### 项目结构

```
openclaw-skill-imutils/
├── SKILL.md              # 完整文档
├── package.json          # 项目配置
├── scripts/
│   ├── rotate.js         # 旋转脚本
│   ├── resize.js         # 缩放脚本
│   ├── translate.js      # 平移脚本
│   └── skeleton.js       # 骨架化脚本
└── README.md             # 本文件
```

### 测试

```bash
# 测试旋转
node scripts/rotate.js --input test.jpg --output test_rotated.jpg --angle 45

# 测试缩放
node scripts/resize.js --input test.jpg --output test_small.jpg --width 800
```

---

## 📦 依赖

- [PyImageSearch/imutils](https://github.com/PyImageSearch/imutils) - 4.6k stars
- [OpenCV](https://opencv.org/)
- [NumPy](https://numpy.org/)

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

**作者：** Boss  
**AI 助手：** Jarvis (OpenClaw)  
**发布日期：** 2026-03-14

---

## 📝 更新日志

### v1.0.0 (2026-03-14)
- ✅ 初始版本
- ✅ 实现旋转、缩放、平移、骨架化功能
- ✅ 添加批量处理示例

---

## 💬 使用技巧

**对 AI 这样说：**
```
"用 imutils-skill 批量处理这些图片"
"把所有产品图旋转 90 度"
"缩放到微信公众号尺寸"
```

---

## 📄 License

MIT License - 详见 [LICENSE](LICENSE)
