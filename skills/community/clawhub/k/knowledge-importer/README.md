# Knowledge Importer

将 Word/Excel/PPT/PDF/Markdown 文档转换为 Markdown 格式，并保存到 Obsidian 知识库。支持图片上传到图床，生成外部 URL 链接。

## 功能特点

- 📄 **多格式支持**：Word (.docx)、Excel (.xlsx)、PPT (.pptx)、PDF、Markdown
- 🖼️ **图片处理**：自动提取文档中的图片并上传到图床
- 🔗 **外部链接**：生成图床 URL，Markdown 文件体积更小
- 💾 **Base64 备用**：图床不可用时自动降级为 Base64 内嵌
- 📁 **批量导入**：支持整个目录批量转换
- 🗂️ **两级分类**：按类型和行业自动分类

## 快速开始

### 1. 安装依赖

```bash
pip3 install python-docx python-pptx openpyxl pdfplumber
```

### 2. 配置

复制配置文件并修改：

```bash
cd scripts
cp config.py.example config.py
```

编辑 `config.py`，填入你的图床地址和知识库路径：

```python
DUFs_CONFIG = {
    "server_url": "http://你的服务器IP:5000",
    "timeout": 30,
    "retry_times": 3,
}

DEFAULT_KNOWLEDGE_BASE = "/你的/Obsidian/路径"
```

### 3. 使用

```bash
# 单文件转换
python3 import_doc.py /path/to/document.docx

# 指定输出目录
python3 import_doc.py /path/to/document.docx /path/to/output

# 批量转换
python3 import_doc.py --batch /path/to/folder
```

## 图床配置

### 推荐：Dufs（轻量文件服务器）

```bash
# Docker 部署
docker run -v /path/to/data:/data -p 5000:5000 sigoden/dufs
```

Dufs 支持：
- ✅ 文件上传/下载 API
- ✅ 目录浏览
- ✅ Web 界面
- ✅ 搜索功能

### 其他图床方案

- **PicList**：支持多种图床的桌面应用
- **兰空图床**：自建图床服务
- **SM.MS**：免费图床服务

## 目录结构

```
knowledge-importer/
├── SKILL.md              # OpenClaw 技能说明
├── README.md             # 本文件
└── scripts/
    ├── config.py.example # 配置文件模板
    ├── import_doc.py     # 主程序
    └── __pycache__/      # Python 缓存（自动生成）
```

## 输出格式

### Markdown 文件

```markdown
# 文档标题

**源文件:** 原始文件名.docx

---

正文内容...

## 图片内容

### 图片 1: word_xxx.png

![word_xxx.png](http://服务器IP:5000/Picture/xxx.png)
```

### 知识库目录结构（示例）

```
Obsidian/
├── 申报方案/
│   └── 行业A/
├── 解决方案/
│   └── 客户A/
├── 技术文档/
│   ├── 产品A/
│   └── 产品B/
└── 赛事/
    └── 赛项A/
```

## 环境变量

也可以通过环境变量配置：

```bash
export DUFS_SERVER_URL="http://192.168.1.100:5000"
export KNOWLEDGE_BASE_PATH="/home/user/Obsidian"
```

## 常见问题

### Q: 图片上传失败怎么办？

程序会自动降级为 Base64 内嵌方式，确保内容不丢失。

### Q: 如何只提取文本不处理图片？

修改 `config.py` 中的图床配置为一个无效地址即可。

### Q: 支持 Word 的 .doc 格式吗？

不支持，请使用 .docx 格式。可以用 Word 另存为功能转换。

## License

MIT
