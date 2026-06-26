# 📚 PDF 学习工作流 (pdf-learning-workflow)

将扫描版 PDF 书籍转为学习优化笔记。支持中英文、公式、表格、代码块识别。

## 依赖

| 依赖 | 用途 | 安装 |
|:---|:---|:---|
| Python 3.10+ | 运行环境 | 系统自带 |
| `zai-sdk` | GLM-OCR API 调用 | `pip install zai-sdk` |
| `PyMuPDF` (fitz) | PDF 拆页为图片 | `pip install pymupdf` |
| `Pillow` | 图片裁剪处理 | `pip install Pillow` |
| **GLM-OCR API Key** | OCR 服务认证 | 去 https://bigmodel.cn 注册获取 |

一键安装依赖：
```bash
pip install zai-sdk pymupdf Pillow
```

## 凭证配置

```bash
mkdir -p ~/.config/glm-ocr
echo "your-api-key" > ~/.config/glm-ocr/api_key
chmod 600 ~/.config/glm-ocr/api_key
```

## 使用流程

1. 将扫描版 PDF 放入工作目录
2. 运行 `extract_pages.py` 拆页
3. 运行 `ocr_pipeline.py` OCR 识别
4. 运行 `postprocess.py` 后处理（公式清洗 + 代码块 + 图片裁剪）
5. 运行 `md2html.py` 生成 HTML 版本
6. 运行 `gen_index.py` 生成导航页

详细流程见 `SKILL.md`。

## 输出结构

```
output/<BookName>/
├── index.html                ← 导航页
├── <BookName>.md             ← 合并全文
├── <BookName>.html           ← 全文 HTML（含 KaTeX）
├── <BookName>-guide.md       ← 导读
├── chapter_structure.md      ← 章节结构
├── assets/                   ← 裁剪图片
└── learning/
    ├── chapter_001_标题.md
    ├── chapter_001_标题.html
    └── ...
```

## 许可证

MIT-0 (No Attribution)
