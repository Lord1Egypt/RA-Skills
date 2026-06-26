# Mermaid 图片生成与图床上传技能

将 Mermaid 图表转换为图片并上传到免费图床，专为公众号文章设计。

## 功能特性

- 🎨 将 Mermaid 代码转换为高质量图片
- ☁️ 支持多个免费图床上传
- 🔗 自动返回图片 URL
- 📝 批量处理 Markdown 文件中的 Mermaid 图表
- 🖼️ 支持多种图片格式 (PNG, SVG, JPG)

## 快速开始

### 安装依赖

```bash
pip install mermaid-cli requests
```

或者安装 Node.js 的 mermaid-cli：

```bash
npm install -g @mermaid-js/mermaid-cli
```

### 使用方法

```bash
# 转换单个 Mermaid 文件
python mermaid_uploader.py --input diagram.mmd --output diagram.png

# 转换 Markdown 文件中的所有 Mermaid 图表
python mermaid_uploader.py --markdown article.md --upload

# 指定图床
python mermaid_uploader.py --input diagram.mmd --image-host imgur
```

## 支持的图床

| 图床 | 需要API Key | 特点 |
|------|------------|------|
| Imgur | ✅ | 稳定，国外 |
| FreeImage.host | ❌ | 免费，国内访问快 |
| Postimages | ❌ | 简单易用 |
| Cloudinary | ✅ | 功能强大 |

## 文件结构

```
skills/mermaid-image-uploader/
├── SKILL.md                    # 本文件
├── package.json                # 技能配置
├── README.md                   # 详细说明
├── mermaid_uploader.py         # 主程序
├── mermaid_converter.py        # Mermaid 转换器
├── image_host_uploader.py      # 图床上传器
└── examples/                   # 示例
    ├── sample_diagram.mmd
    └── sample_article.md
```

## 使用示例

### 1. 转换单个 Mermaid 图表

```python
from mermaid_uploader import MermaidUploader

uploader = MermaidUploader()

# 转换并上传
url = uploader.convert_and_upload(
    mermaid_code="""
    graph LR
        A[开始] --> B[处理]
        B --> C[结束]
    """,
    image_host="freeimage"
)

print(f"图片URL: {url}")
```

### 2. 处理 Markdown 文件

```python
from mermaid_uploader import MarkdownProcessor

processor = MarkdownProcessor()

# 处理文件，替换所有 Mermaid 为图片链接
processor.process_file("article.md", "article_with_images.md")
```

## 命令行参数

```
--input, -i      输入的 Mermaid 文件
--output, -o     输出的图片文件
--markdown, -m   处理的 Markdown 文件
--upload, -u     是否上传到图床
--image-host     指定图床 (imgur, freeimage, postimages)
--format, -f     输出格式 (png, svg, jpg)
--api-key        图床 API Key
```

## 欢迎关注

欢迎关注微信公众号：**拿客**

获取更多技术干货和开源工具分享！

## 许可证

MIT License
