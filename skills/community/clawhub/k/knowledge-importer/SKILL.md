---
name: knowledge-importer
description: 将 Word/Excel/PPT/PDF/MD 等格式的文档转换为 Markdown 格式，并保存到 Obsidian 知识库。图片可上传到图床，生成外部 URL 链接。当用户需要：1) 导入文档到知识库 2) 将文件转换为 MD 格式 3) 提取文档内容并保留图片时使用此技能。
---

# Knowledge Importer

将各种格式的文档转换为 Markdown 并保存到知识库。

## 环境配置

首次使用前，请配置以下环境变量或修改 `scripts/config.py`：

```bash
# 图床服务地址
export DUFS_SERVER_URL="http://你的服务器IP:端口"

# 知识库存放路径
export KNOWLEDGE_BASE_PATH="/你的/Obsidian/路径"
```

## 支持的格式

| 格式 | 扩展名 | 依赖库 | 图片处理 |
|------|--------|--------|----------|
| Word | .docx | python-docx | ✅ 图床/Base64 |
| Excel | .xlsx / .xls | openpyxl | - |
| PPT | .pptx | python-pptx | ✅ 图床/Base64 |
| PDF | .pdf | pdfplumber | ✅ 图床/Base64 |
| Markdown | .md | 原生支持 | - |

## 图片处理方式

### 方式一：图床上传（推荐）

配置图床服务器后，图片会上传到图床生成外部 URL：

```python
DUFs_CONFIG = {
    "server_url": "http://你的服务器IP:端口",
    "timeout": 30,
    "retry_times": 3,
}
```

上传路径：`http://你的服务器IP:端口/Picture/<uuid>.png`

### 方式二：Base64 内嵌（备用）

如果图床不可用，自动降级为 Base64 内嵌方式：

```markdown
![image](data:image/png;base64,iVBORw0KGgo...)
```

## Obsidian CLI 前提条件

1. **在 Obsidian 中启用 CLI**：
   - Settings → General → Command line interface → 启用
   - 按照提示完成注册

2. **CLI 命令格式**：
   ```bash
   xvfb-run obsidian create name="文件名" content="内容"
   xvfb-run obsidian append file="文件" content="内容"
   ```

## 知识库目录结构

默认路径：`$KNOWLEDGE_BASE_PATH`（见环境配置）

### 目录结构（两级分类）

```
知识库/
├── 申报方案/
│   └── <行业/产品>/
├── 解决方案/
│   └── <行业/产品>/
├── 技术文档/
│   └── <行业/产品>/
└── <其他分类>/
```

### 分类原则
- **申报方案/**：申报书、投标书、建设方案申请等
- **解决方案/**：面向客户的解决方案文档
- **技术文档/**：产品使用经验、技术部署文档
- **<其他分类>/**：根据需要自定义

## 使用方式

### 1. 单文件转换

```
将 /path/to/document.docx 导入知识库
```

### 2. 指定输出目录

```
将文件导入到 [目录名]
```

## 转换规则

- **文件名**：保留原文件名（去掉扩展名）
- **图片**：Word/PPT/PDF 中的图片会提取并上传图床
- **表格**：Excel/PDF 中的表格会保持 Markdown 格式

## 执行脚本

```bash
# 进入脚本目录
cd skills/knowledge-importer/scripts

# 配置环境变量（或修改 config.py）
export DUFS_SERVER_URL="http://192.168.1.100:5000"
export KNOWLEDGE_BASE_PATH="/path/to/Obsidian"

# 单文件转换
python3 import_doc.py /path/to/document.docx

# 批量转换
python3 import_doc.py --batch /path/to/folder

# 查看帮助
python3 import_doc.py --help
```

## 依赖安装

```bash
pip3 install python-docx python-pptx openpyxl pdfplumber
```

## 图床推荐

- **Dufs**：轻量文件服务器，支持上传 API
  - Docker 部署：`docker run -v /path:/data -p 5000:5000 sigoden/dufs`
- **PicList**：支持多种图床
- **兰空图床**：自建图床解决方案
