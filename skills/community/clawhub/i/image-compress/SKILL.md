---
name: image-compress
description: 跨平台图片压缩工具，基于 sharp 实现高效压缩（节省 60-80% 体积）。支持单图/批量压缩、格式转换 (JPG/PNG/WebP/AVIF/HEIC)、画质调节、尺寸缩放。当用户需要压缩图片体积、转换格式、缩小尺寸、批量处理图片、优化图片用于微信/邮件/网页上传时使用此技能。触发词："压缩"、"缩小"、"转换格式"、"转成 JPG/WebP"、"图片太大"、"批量处理图片"。不处理：旋转、裁剪、水印、EXIF 读取等编辑操作；文件管理（删除、重命名、移动）；内容读取（分析图片、读取元数据）。
---

# Image Compress Skill

基于 sharp 的高效图片压缩技能，跨平台支持 (macOS/Windows/Linux)，平均节省 60-80% 体积。

## 何时使用

**立即使用此技能当用户提到：**

1. **压缩体积** — "图片太大"、"压缩一下"、"缩小文件"、"发不了微信"
2. **格式转换** — "转成 JPG"、"PNG 转 WebP"、"HEIC 转 JPG"、"转换格式"
3. **批量处理** — "批量压缩"、"处理这个文件夹"、"所有图片"
4. **尺寸调整** — "宽度太大"、"缩小到 1920px"、"用于网页展示"
5. **场景优化** — "用于邮件附件"、"上传网站"、"电商展示"、"微信发送"

**典型触发语句：**

- "帮我压缩这张图片，文件太大了发不了微信"
- "把这个 PNG 转成 JPG 格式"
- "这些照片是 iPhone 拍的 HEIC 格式，帮我转成 JPG"
- "批量压缩这个文件夹里的所有图片，用于上传网站"
- "图片宽度太大了，帮我缩小到 1920px 以内"
- "把这些设计稿都转成 WebP 格式"
- "压缩一下这张图用于邮件附件，控制在 500KB 以内"
- "Screenshot.png 这个文件 10MB 太大了，怎么变小一点？"

**不应触发的情况：**

- 图片编辑（旋转、裁剪、拼接、添加水印）
- 图片分析（识别内容、读取 EXIF）
- 文件管理（上传云盘、设置为壁纸、删除、重命名、移动）
- 文档操作（添加到 PDF）

---

## 快速开始

### 基础命令

```bash
/compress <图片路径>
```

首次运行自动：
1. ✅ 检测 Node.js 环境
2. ✅ 安装 sharp 依赖
3. ✅ 配置输出目录

### 常用场景

| 场景 | 命令 |
|------|------|
| 压缩单图 | `/compress ~/Desktop/screenshot.png` |
| 格式转换 | `/compress image.png --format jpg` |
| 调整画质 | `/compress photo.jpg --quality 0.6` |
| 限制尺寸 | `/compress photo.jpg --maxWidth 1920` |
| 批量压缩 | `/compress ~/Photos/ --recursive` |
| **使用预设** | `/compress photo.jpg --preset web` |
| 组合使用 | `/compress ./pics/ --preset wechat --recursive` |

### 压缩预设

快速选择适合场景的画质：

| 预设 | 画质 | 用途 | 节省 |
|------|------|------|------|
| `web` | 75% | 网页展示 | 60-70% |
| `wechat` | 65% | 微信发送 | 70-80% |
| `email` | 55% | 邮件附件 | 80-90% |
| `quality` | 95% | 高质量存档 | 30-40% |

**示例：**

```bash
# 网页优化
/compress photo.jpg --preset web

# 微信发送（体积优先）
/compress photo.jpg --preset wechat

# 邮件附件（最小体积）
/compress photo.jpg --preset email

# 高质量存档
/compress photo.jpg --preset quality
```

---

## 核心参数

### 压缩选项

| 参数 | 短参数 | 类型 | 默认值 | 说明 |
|------|--------|------|--------|------|
| `--format` | `-f` | string | `original` | 输出格式：`jpg`, `png`, `webp`, `avif` |
| `--quality` | `-q` | number | `0.85` | 画质 (0.1-1.0)，越低体积越小 |
| `--maxWidth` | `-w` | number | `null` | 最大宽度（等比缩放） |
| `--maxHeight` | `-h` | number | `null` | 最大高度（等比缩放） |
| `--recursive` | `-r` | boolean | `false` | 递归处理子文件夹 |
| `--outputDir` | `-o` | string | 默认目录 | 自定义输出目录 |
| `--preset` | `-p` | string | `无` | 压缩预设：`web`, `wechat`, `email`, `quality` |
| `--no-confirm` | | boolean | `false` | 跳过确认提示 |

### 画质建议

使用预设更简单：

| 预设 | 画质 | 体积节省 | 用途 |
|------|------|---------|------|
| `web` | 75% | 60-70% | 网页展示、博客文章 |
| `wechat` | 65% | 70-80% | 微信发送、社交媒体 |
| `email` | 55% | 80-90% | 邮件附件、快速传输 |
| `quality` | 95% | 30-40% | 高质量存档、打印 |

手动设置画质参考：

| 用途 | 推荐值 | 体积节省 |
|------|--------|---------|
| 网页展示 | 0.7-0.8 | 60-70% |
| 微信发送 | 0.6-0.7 | 70-80% |
| 邮件附件 | 0.5-0.6 | 80-90% |
| 高质量存档 | 0.9-0.95 | 30-40% |

---

## 输出规则

### 目录结构

```
~/Downloads/compressed-images/
├── 2026-03-11/
│   ├── photo.png           # 保持原名
│   ├── photo_001.png       # 同名自动编号
│   └── trip/image001.jpg   # 保持原目录结构
└── 2026-03-12/
    └── ...
```

### 安全保护

- ⚠️ **永不覆盖原图** — 输出到独立目录
- ⚠️ **永不覆盖输出** — 同名文件自动添加 `_001`, `_002` 后缀
- ⚠️ **大文件警告** — 单张超过 50MB 时先确认
- ⚠️ **进度显示** — 批量压缩时显示进度条

### 格式转换规则

| 转换 | 处理方式 |
|------|---------|
| PNG → JPG | 透明通道用白色填充 |
| JPG → PNG | 直接转换 |
| 任意 → WebP | 有损压缩（可指定 quality） |
| 任意 → AVIF | 高效压缩（可指定 quality） |

---

## 脚本说明

### 环境检测

```bash
node scripts/detect-env.js
```

检测 Node.js/npm，缺失时给出安装建议。

### 依赖安装

```bash
node scripts/install.js
```

自动执行 `npm install` 安装 sharp。

### 核心压缩

```bash
# 单图
node scripts/compress.js ~/Pictures/photo.png --quality 0.8

# 批量
node scripts/compress.js ~/Pictures/ --recursive --format webp
```

**编程调用：**

```javascript
import { compress } from './scripts/compress.js';

const result = await compress('/path/to/image.png', {
  quality: 0.85,
  format: 'webp',
  maxWidth: 1920
});

console.log(`压缩完成：${result.originalSize}KB → ${result.compressedSize}KB`);
```

详细 API 参考：[references/technical.md](references/technical.md)

---

## 故障排查

### sharp 安装失败

```bash
# 清理缓存
npm cache clean --force

# 重新安装
cd ~/.openclaw/workspace/skills/image-compress
npm install
```

### 权限问题

```bash
# macOS/Linux
chmod -R 755 ~/.openclaw/workspace/skills/image-compress
```

### 输出目录不可写

修改配置文件 `~/.openclaw/workspace/skills/image-compress/config.json` 中的 `outputDir`。

---

## 支持格式

**输入：** JPG, JPEG, PNG, WebP, GIF, BMP, HEIC, HEIF

**输出：** JPG, PNG, WebP, AVIF

详细格式规格：[references/technical.md](references/technical.md)

---

## 配置管理

配置文件：`~/.openclaw/workspace/skills/image-compress/config.json`

```json
{
  "outputDir": "~/Downloads/compressed-images",
  "defaultQuality": 0.85,
  "defaultFormat": "original"
}
```
