---
name: photo-organizer
description: 照片批量整理工具，支持按时间、地点自动分类和打标签。适用于手机照片整理、相册归档等场景，帮助用户快速整理成千上万张照片！
---

# Photo Organizer - 照片批量整理工具

## 功能特性
- ✅ 读取照片 EXIF 信息（拍摄时间、GPS 地点等）
- ✅ 按时间自动分类（年/月文件夹结构）
- ✅ 按地点自动分类（如果有 GPS 信息）
- ✅ 批量打标签
- ✅ 预览模式（先看效果再执行）
- ✅ 撤销操作（安全可靠）

## 安装
```bash
# 方法一：通过 clawhub 安装
clawhub install photo-organizer

# 方法二：作为 Python 包安装
pip install photo-organizer
```

## 快速开始

### 1. 按时间整理照片
```bash
photo-organizer organize ./photos --by date --output ./organized
```

### 2. 按地点整理照片（需要 GPS 信息）
```bash
photo-organizer organize ./photos --by location --output ./organized
```

### 3. 预览模式（不实际执行）
```bash
photo-organizer organize ./photos --by date --preview
```

### 4. 撤销操作
```bash
photo-organizer undo ./organized
```

## 详细使用说明

### 整理模式
- `--by date`：按拍摄时间整理（默认）
- `--by location`：按拍摄地点整理（需要 GPS 信息）

### 文件夹结构
默认按时间整理的文件夹结构：
```
organized/
├── 2026/
│   ├── 03/
│   │   ├── photo_001.jpg
│   │   └── photo_002.jpg
│   └── 04/
└── 2025/
```

### 配置文件
可以在项目根目录创建 `.photo-organizer.json`：
```json
{
  "output_dir": "./organized",
  "folder_structure": "{year}/{month}",
  "auto_tag": true,
  "backup_original": true
}
```

## 示例场景

### 场景 1：整理手机照片
```bash
# 将 DCIM 文件夹里的照片按时间整理
photo-organizer organize ./DCIM --by date --output ./my-photos
```

### 场景 2：旅行照片整理
```bash
# 将旅行照片按地点整理（如果有 GPS）
photo-organizer organize ./trip-photos --by location --output ./trip-by-place
```

## 注意事项
- 确保有照片的读写权限
- 建议先用 --preview 预览效果
- 大量照片整理可能需要一些时间
- 整理前建议先备份原照片

## 更新日志
### v0.1.0 (2026-03-06)
- 初始版本发布
- 支持按时间整理
- 支持预览模式
- 支持撤销操作
