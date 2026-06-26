---
name: smart-file-organizer
description: 智能文件整理助手 - 一键自动分类、重命名、清理重复文件，4500+文件/秒
version: 1.0.0
icon: 🗂️
metadata:
  clawdbot:
    emoji: 🗂️
    requires:
      bins: ["python3"]
    install: []
    tags: ["file", "organize", "automation", "productivity", "tool", "utility"]
    category: "productivity"
    author: "Your Name"
    license: "MIT"
    features:
      - "smart-categorization"
      - "auto-renaming"
      - "duplicate-detection"
      - "safety-backup"
      - "preview-mode"
      - "cross-platform"
---

# 智能文件整理助手 🗂️

## ✨ 功能亮点
- ⚡ **4500+文件/秒** - 极速处理
- 🛡️ **安全可靠** - 预览模式 + 自动备份
- 🎯 **智能分类** - 一键自动分类文件
- 📝 **智能重命名** - 基于日期/内容自动命名
- 🔍 **重复检测** - 智能识别重复文件
- 🔄 **跨平台** - Windows/macOS/Linux

---

一键自动化文件整理工具，智能分类、重命名、清理重复文件，让你的电脑井井有条。

## 为什么需要这个工具？

### 常见问题
- 下载文件夹杂乱无章，找文件困难
- 照片、文档、视频混在一起
- 文件命名不规范，难以识别
- 重复文件占用大量空间

### 我们的解决方案
- **一键整理**：自动分类到对应文件夹
- **智能命名**：基于内容自动重命名
- **重复清理**：智能识别并处理重复文件
- **批量操作**：支持整个文件夹处理

## 核心功能

### 1. 智能分类
自动按文件类型分类：
- **图片** → `Pictures/` (jpg, png, gif, webp等)
- **文档** → `Documents/` (pdf, doc, xls, ppt等)
- **视频** → `Videos/` (mp4, mov, avi等)
- **音频** → `Music/` (mp3, wav, flac等)
- **压缩包** → `Archives/` (zip, rar, 7z等)
- **代码** → `Code/` (py, js, java, cpp等)
- **其他** → `Others/`

### 2. 智能重命名
基于文件内容自动重命名：
- **图片**：`IMG_日期_内容描述.jpg`
- **文档**：`DOC_主题_版本.pdf`
- **通用**：`类型_创建日期_序号.扩展名`

支持自定义命名规则。

### 3. 重复文件检测
智能识别重复文件：
- 基于文件哈希值（MD5/SHA）
- 基于文件名和大小
- 基于图片相似度（可选）
- 提供处理选项：删除、移动、重命名

### 4. 批量操作
- 支持整个文件夹递归处理
- 支持文件类型过滤
- 支持大小限制
- 支持预览模式（不实际操作）

## 快速开始

### 基本整理
```bash
# 整理当前目录
python3 scripts/organize.py --path .

# 整理指定目录
python3 scripts/organize.py --path ~/Downloads

# 整理并重命名
python3 scripts/organize.py --path . --rename
```

### 高级选项
```bash
# 整理并检测重复文件
python3 scripts/organize.py --path . --deduplicate

# 仅整理特定类型文件
python3 scripts/organize.py --path . --types "jpg,png,pdf"

# 预览模式（不实际操作）
python3 scripts/organize.py --path . --preview

# 自定义分类规则
python3 scripts/organize.py --path . --config my_rules.json
```

### 批量重命名
```bash
# 批量重命名图片
python3 scripts/rename.py --path ./photos --pattern "vacation_{date}_{index}"

# 批量重命名文档
python3 scripts/rename.py --path ./docs --pattern "{title}_v{version}"
```

### 重复文件清理
```bash
# 查找重复文件
python3 scripts/deduplicate.py --path . --find

# 删除重复文件（保留一个）
python3 scripts/deduplicate.py --path . --delete

# 移动重复文件到指定目录
python3 scripts/deduplicate.py --path . --move ./duplicates
```

## 使用场景

### 场景1：整理下载文件夹
```bash
# 每月整理一次下载文件夹
python3 scripts/organize.py --path ~/Downloads --rename --deduplicate
```

### 场景2：整理照片库
```bash
# 按日期整理照片
python3 scripts/organize.py --path ~/Pictures --types "jpg,png" --rename --pattern "{year}/{month}/{day}/IMG_{index}"
```

### 场景3：清理项目文件
```bash
# 清理代码项目中的临时文件
python3 scripts/clean.py --path ./project --patterns "*.tmp,*.log,*.bak"
```

## 配置选项

### 配置文件示例
```json
{
  "organize": {
    "image_extensions": ["jpg", "jpeg", "png", "gif", "webp", "bmp"],
    "document_extensions": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"],
    "video_extensions": ["mp4", "mov", "avi", "mkv", "flv"],
    "audio_extensions": ["mp3", "wav", "flac", "m4a"],
    "archive_extensions": ["zip", "rar", "7z", "tar", "gz"]
  },
  "rename": {
    "image_pattern": "IMG_{date}_{index}",
    "document_pattern": "DOC_{title}_{date}",
    "date_format": "YYYYMMDD"
  },
  "deduplicate": {
    "method": "hash",
    "action": "delete",
    "keep": "oldest"
  }
}
```

## 安全特性

### 数据安全
- **预览模式**：所有操作前可预览
- **备份功能**：重要操作前自动备份
- **撤销功能**：支持操作撤销
- **日志记录**：详细记录所有操作

### 文件保护
- 不处理系统文件
- 不处理隐藏文件
- 大小限制保护
- 权限检查

## 系统要求

### 最低要求
- Python 3.7+
- 100MB可用空间
- 支持主流操作系统（Windows/macOS/Linux）

### 推荐配置
- Python 3.9+
- 1GB可用空间
- SSD硬盘以获得最佳性能

## 更新计划

### V1.1（计划中）
- 图形用户界面（GUI）
- 更多文件类型支持
- 性能优化

### V1.2（计划中）
- 云端存储集成
- 移动端应用
- 高级分析报告

### V2.0（计划中）
- AI智能分类
- 自定义工作流
- 团队协作功能

---

## 📝 许可证

MIT License - 自由使用、修改和分发

---

*智能文件整理助手 - 让文件整理变得简单*