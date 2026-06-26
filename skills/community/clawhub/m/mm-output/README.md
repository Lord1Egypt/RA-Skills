# PosterGen Parser Unit

PDF/Markdown 解析与多模态输出转换工具。

## 功能

- **输入**: PDF, Markdown
- **输出**: HTML, PDF, PNG, DOCX, PPTX
- **LLM 渲染**: 支持 OpenAI、Gemini、Qwen 等后端
- **图片生成**: 海报图、Slides 图（Gemini）
- **风格支持**: academic, doraemon, minimal

## 快速开始

### 安装

```bash
# 完整安装（系统依赖 + Python 环境）
bash install.sh

# 安装完成后，编辑 .env 文件填入 API 密钥
vi .env
```

### 使用

```bash
# PDF → HTML + PDF + PNG + DOCX
uv run python run.py --pdf_path input.pdf --output_dir ./output

# Markdown → HTML（指定模板）
uv run python run.py --md_path input.md --output_dir ./output --template templates/doubao.txt

# 生成海报图片
uv run python run.py --md_path input.md --output_dir ./output --output_type poster_image --style academic --density medium

# 生成 Slides 图片
uv run python run.py --md_path input.md --output_dir ./output --output_type slides_image --style doraemon --slides_length medium

# 生成 XHS Slides
uv run python run.py --md_path input.md --output_dir ./output --output_type xhs_slides --style academic --slides_length short

# HTML → PDF/PNG/DOCX
uv run python -m mm_output.cli input.html --format pdf --output-dir ./output
```

### 批量测试

```bash
# 运行完整功能测试
bash run.sh
```

## 配置

创建 `.env` 文件：

```bash
# OpenAI / 兼容 API
TEXT_MODEL=gpt-4.1-2025-04-14
OPENAI_API_KEY=your-key
OPENAI_BASE_URL=https://api.openai.com/v1

# 或 Gemini
TEXT_MODEL=gemini-3-pro-preview
RUNWAY_API_KEY=your-key
RUNWAY_API_BASE=https://runway.devops.xiaohongshu.com/openai
RUNWAY_API_VERSION=2024-12-01-preview
```

## 命令行参数

```
--pdf_path PATH          # PDF 输入文件
--md_path PATH           # Markdown 输入文件
--output_dir DIR         # 输出目录（必需）
--output_type TYPE       # 输出类型: html, poster_image, slides_image, xhs_slides
--style STYLE            # 视觉风格: academic, doraemon, minimal
--density DENSITY        # Poster 密度: sparse, medium, dense
--slides_length LENGTH   # Slides 长度: short, medium, long
--template PATH          # HTML 模板路径
--text_model MODEL       # LLM 模型名称
--language LANG          # 输出语言: auto, zh, en
```

## 目录结构

```
.
├── run.py              # 主程序
├── run.sh              # 功能测试脚本
├── parser_unit.py      # PDF/Markdown 解析
├── renderer_unit.py    # HTML 渲染

├── mm_output/          # 多模态转换（HTML→PDF/PNG/DOCX）
├── paper2slides/       # 图片生成（Poster/Slides）
├── templates/          # HTML 模板
├── install.sh          # 安装脚本
├── pyproject.toml      # UV 依赖配置
├── uv.lock             # 锁定依赖版本
└── README.md           # 本文件
```

## 依赖

- Python 3.12+
- UV (包管理器)
- Chromium (Playwright 自动安装)
- 中文字体 (Noto CJK)

## 模板列表

| 模板 | 描述 |
|------|------|
| `doubao.txt` | 默认风格 |
| `doubao_dark.txt` | 深色主题 |
| `doubao_minimal.txt` | 极简风格 |
| `doubao_newspaper.txt` | 报纸多栏布局 |
| `doubao_enterprise_blue.txt` | 企业蓝色风格 |
| `report_web.txt` | Web 报告风格 |
| `report_web_reduced.txt` | 简化 Web 风格 |
