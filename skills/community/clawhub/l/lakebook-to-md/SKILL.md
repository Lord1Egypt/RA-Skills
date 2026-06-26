---
name: lakebook-to-md
version: 1.1.0
description: 将语雀导出的 .lakebook 文件转换为 Markdown + Excel 文件夹。支持 lake 富文本、laketable 数据库表格（同时输出 Excel）、lakesheet 电子表格、书签卡片、本地附件下载、代码块、加密内容占位等。自动生成详细的转换报告。
---

# 语雀 Lakebook 转 Markdown + Excel 工具

## 概述

将语雀导出的 `.lakebook` 文件转换为有组织的文件夹，保留原始文档目录树结构。

**核心特性**：
- 📝 富文本文档 → Markdown
- 📊 数据库表格 → **同时输出 Markdown 和 Excel (.xlsx)**
- 📎 附件自动下载并记录状态
- 📋 自动生成详细的转换报告

本工具基于 [PZh101/YuqueExportToMarkdown](https://github.com/PZh101/YuqueExportToMarkdown) 项目，在其基础上扩展修复了多项问题，增加了更多格式支持。

**依赖**（自动安装）：
- `beautifulsoup4` — HTML/ASL 解析
- `PyYAML` — 元数据解析
- `Requests` — 图片/附件下载
- `openpyxl` — Excel 文件生成

## 支持的文档格式

| 语雀格式 | 类型 | 说明 | 输出 |
|---|---|---|---|
| `lake` | Doc | 富文本文档 | Markdown (.md) |
| `laketable` | Table | 数据库式表格 | **Markdown + Excel (.xlsx)** |
| `lakesheet` | Sheet | 电子表格（zlib 压缩） | Markdown 表格 |

## 支持的卡片类型

| 卡片 | 输出 | 备注 |
|---|---|---|
| `codeblock` | 带语言标注的代码块 | |
| `image` | 下载图片，`![]()` 语法 | 自动下载并记录状态 |
| `hr` | `---` 分割线 | |
| `label` | 标签文本 | |
| `math` | LaTeX 公式 + 图片 | |
| `file` | 文件附件链接 | |
| `bookmarkInline` | `> **[标题](URL)** — 来源` | |
| `bookmarklink` | `[标题](URL)` | |
| `localdoc` | 附件下载 + 链接 | **自动下载，记录成功/失败状态** |
| `lockedtext` | 占位符：`[加密内容 - ...]` | |
| `yuque` | 跨文档链接 | |

## 转换报告

每次转换会自动生成 `转换报告.md`，包含：

1. **总体统计** - 文档数量、类型分布
2. **成功转换的文档** - 列出所有成功转换的文件
3. **转换失败的文档** - 列出失败原因
4. **图片下载统计** - 成功/失败的图片
5. **附件下载统计** - 成功/失败的附件
6. **过期链接** - 无法下载的资源
7. **加密内容** - 无法解密的内容
8. **需要手动处理的内容** - 汇总需要人工介入的项目

## 使用方法

### 基本转换

```bash
cd scripts
python startup.py -l /path/to/your.lakebook -o /path/to/output_folder
```

### 可选参数

```bash
# 禁用图片下载（更快）
python startup.py -l your.lakebook -o output -d False

# 跳过已下载的资源
python startup.py -l your.lakebook -o output --skip-existing-resources

# 直接使用已解压的 meta.json（高级用法）
python startup.py -i /path/to/extracted/\$meta.json -o output
```

### 作为 Python 模块调用

```python
import sys
sys.path.insert(0, "/path/to/lakebook-to-md/scripts")
from lake.lake_setup import start_convert

start_convert(
    meta=None,
    lake_book="/path/to/your.lakebook",
    output="/path/to/output",
    download_image_of_in=True,
    skip_existing=False
)
```

## 输出结构

```
output_folder/
├── 转换报告.md          # 转换统计报告
├── 笔记本名称/
│   ├── 文档1.md
│   ├── 文档1.xlsx       # laketable 同时生成 Excel
│   ├── 文档1.assert/    # 图片/附件目录
│   │   ├── image1.png
│   │   └── attachment.pdf
│   └── 子目录/
│       └── 文档2.md
```

## 关键实现说明

### 路径处理
- 文档标题可能包含 `/`（如 `2022/11/21 会议记录`），会被替换为 `_` 以避免路径嵌套问题
- Windows 路径分隔符通过 `os.path.join` 和 `os.path.sep` 进行标准化

### laketable 转 Excel
- 自动解析 select/multi_select 类型的选项值（ID → 显示文本）
- 数字类型列自动转换为数值格式
- 日期类型列提取可读文本
- 自动调整列宽

### lakesheet 解码
- `lakesheet` 格式使用 zlib 压缩存储在 `body_draft` 字段中
- `sheet` 字段编码为 latin-1 字符串，需要 `encode('latin-1')` → `zlib.decompress()` → JSON 解析

### 公式单元格
- `lakesheet` 中 `{'class': 'formula', 'value': ...}` 类型的单元格使用计算后的 `value` 渲染，而非原始 JSON

### 加密内容
- `lockedtext` 卡片使用 AES-256-GCM 客户端加密，密钥**不在** lakebook 导出中
- 这些内容会渲染为占位符。如需访问，请在语雀 App 中解锁后重新导出

### 附件下载
- `localdoc` 卡片包含 OSS 签名下载链接，可能过期
- 自动下载附件到 `.assert` 目录
- 下载状态记录在转换报告中

## 限制

- 加密的 `lockedtext` 内容无法解密（密钥不在导出中）
- `lakesheet` 合并表头在 Markdown 中会拆分显示（Markdown 不支持单元格合并）
- OSS 附件下载链接有过期时间，建议尽快转换
- 不支持语雀内部跨知识库引用
- 幻灯片文档暂不支持转换为 PPT 格式
