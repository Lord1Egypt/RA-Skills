# GitHub to RedNote v1.2.0 🚀

将 GitHub 仓库一键转换为小红书风格的技术文章，支持自动生成封面图。

**基于 OpenClaw 内置 Agent 能力 - 无需外部 LLM API**

## ✨ v1.2.0 新功能

### 🎨 自动生成封面图
- 一键生成 1080×1440 小红书标准封面
- 科技感设计 + 智能配色（根据编程语言自动选择）
- Stars ≥ 100 时自动显示社交证明徽章

### 📝 内容质量升级
- **结构化内容**：一句话概括 + 适用场景 + 核心功能 + 技术亮点
- **智能数据提取**：自动识别 README Features、项目卖点
- **去除空话套话**：要求每个观点都有具体内容支撑

### ⭐ Stars 智能显示
- Stars ≥ 1000：显示为 "1.5k stars"
- Stars ≥ 100：显示为 "123 stars"
- Stars < 100：不显示（避免负面影响）

## 功能特性

- 🔍 **智能数据获取** - 自动获取仓库信息、Releases、Contributors、README Features
- 🤖 **内置 Agent 生成** - 使用 OpenClaw 内置 Agent 完成内容创作，无需外部 API Key
- 📝 **5种文章模板** - 项目介绍、深度测评、使用教程、工具清单、版本发布
- 🎨 **5种写作风格** - 轻松随意、专业严谨、热情推荐、故事叙事、极简干练
- 🖼️ **封面图生成** - 自动生成小红书标准封面图 (1080×1440)
- 💾 **智能缓存** - 缓存 GitHub API 响应，避免重复请求
- 📋 **一键复制** - 直接复制到剪贴板，方便发布

## 快速开始

### 安装

```bash
# 克隆仓库
git clone <repository-url>
cd github-to-rednote

# 安装依赖（可选，用于剪贴板和封面图功能）
pip install pyperclip cairosvg
```

### 配置

**仅需设置 GitHub Token（必需）：**

```bash
export GITHUB_TOKEN="your_github_token_here"
```

**无需 LLM API Key！** 本工具使用 OpenClaw 内置的 Agent 能力完成内容生成。

### 使用

#### 基础用法

```bash
# 基本生成（项目介绍 + 轻松风格）
python3 scripts/generate_article.py https://github.com/pallets/flask

# 深度测评 + 专业风格
python3 scripts/generate_article.py https://github.com/torvalds/linux --template review --style professional

# 保存到文件
python3 scripts/generate_article.py https://github.com/microsoft/vscode -o vscode_article.txt

# 复制到剪贴板
python3 scripts/generate_article.py https://github.com/expressjs/express --clipboard
```

#### 生成封面图（v1.2.0 新功能）

```bash
# 生成文章 + 封面图（--with-image 需要 --output 指定输出目录）
python3 scripts/generate_article.py https://github.com/pallets/flask \
    -o ./output/flask_article.md \
    --with-image

# 封面图将保存到: ./output/flask_cover.png

# 自定义封面图输出目录
python3 scripts/generate_article.py https://github.com/golang/go \
    -o ./articles/go.md \
    --with-image \
    --image-output ./images/

# 封面图将保存到: ./images/go_cover.png
```

#### 查看可用选项

```bash
# 查看文章模板
python3 scripts/generate_article.py --list-templates

# 查看写作风格
python3 scripts/generate_article.py --list-styles
```

#### 高级用法

```bash
# 禁用缓存（强制刷新数据）
python3 scripts/generate_article.py https://github.com/golang/go --no-cache

# 组合使用：生成带封面图的专业测评
python3 scripts/generate_article.py https://github.com/rust-lang/rust \
    --template review \
    --style professional \
    -o ./reviews/rust.md \
    --with-image
```

## 文章模板

| 模板 | 说明 | 适用场景 |
|------|------|----------|
| `intro` | 项目介绍 | 快速了解项目，突出亮点 |
| `review` | 深度测评 | 详细分析优缺点，适合技术选型 |
| `tutorial` | 使用教程 | 入门指南，包含代码示例 |
| `list` | 工具清单 | 同类对比，适合系列推荐 |
| `release` | 版本发布 | 新特性解读，更新说明 |

## 写作风格

| 风格 | 说明 | 语气特点 |
|------|------|----------|
| `casual` | 轻松随意 | 像朋友聊天，口语化 |
| `professional` | 专业严谨 | 技术深度，数据驱动 |
| `enthusiastic` | 热情推荐 | 感染力强，强烈推荐 |
| `story` | 故事叙事 | 有情节，有代入感 |
| `minimal` | 极简干练 | 信息密度高，无废话 |

## 内容质量优化

v1.2.0 对内容生成进行了全面升级：

### 结构化内容要求

生成的文章现在包含以下结构化部分：

1. **一句话概括** - 开头明确说明"这是什么"
2. **适用场景** - 目标用户、解决的问题、使用场景
3. **核心功能** - 具体列出 3-5 个功能点（禁止空话）
4. **技术亮点** - 技术优势、独特之处

### 智能数据提取

自动从仓库中提取：
- ✅ README Features 部分
- ✅ 项目卖点（Stars、活跃度、文档完善度等）
- ✅ 最新 Release 信息

### Stars 智能显示规则

| Stars 数 | 显示方式 | 文章中提及 |
|----------|----------|------------|
| ≥ 1000 | ⭐ 1.5k stars | ✅ 作为社交证明 |
| ≥ 100 | ⭐ 123 stars | ✅ 作为社交证明 |
| < 100 | 不显示 | ❌ 不提及 |

## 封面图设计

### 封面规格
- **尺寸**: 1080 × 1440 像素（小红书标准）
- **格式**: PNG/SVG
- **风格**: 科技感、简洁

### 封面元素
- 🎨 根据编程语言自动选择配色方案
- 📛 项目名称（大标题）
- 📝 项目描述（副标题）
- 💻 主要语言徽章
- ⭐ Stars 徽章（≥100 时显示）
- 🔗 GitHub 相关装饰元素

### 配色方案
| 语言 | 主色调 |
|------|--------|
| Python | #306998 |
| JavaScript | #F7DF1E |
| TypeScript | #3178C6 |
| Go | #00ADD8 |
| Rust | #CE422B |
| Java | #007396 |

## 项目结构

```
github-to-rednote/
├── README.md              # 本文档
├── SKILL.md              # Skill 说明
├── manifest.yaml         # Skill 配置
├── prompts.md            # Prompt 设计文档
├── rednote-style.md      # 小红书风格指南
└── scripts/
    ├── generate_article.py    # 主脚本
    ├── github_api.py          # GitHub API 封装（v1.2.0 增强数据提取）
    ├── llm_generator.py       # OpenClaw Agent 内容生成（v1.2.0 改进 Prompt）
    ├── formatters.py          # 小红书格式工具（v1.2.0 Stars 智能显示）
    ├── image_generator.py     # 封面图生成（v1.2.0 新增）
    └── test_github_api.py     # 测试脚本
```

## API 说明

### GitHubAPI

```python
from scripts.github_api import GitHubAPI, GitHubCache

# 初始化（带缓存）
cache = GitHubCache(ttl_hours=1)
api = GitHubAPI(cache=cache)

# 获取仓库摘要
summary = api.get_repo_summary("https://github.com/pallets/flask")

# v1.2.0 新增数据字段：
# - readme_features: 从 README 提取的功能列表
# - selling_points: 自动识别的项目卖点
# - latest_release: 最新版本详情
```

### 封面图生成

```python
from scripts.image_generator import generate_cover_image

# 生成封面图
image_path = generate_cover_image(repo_data, output_dir="./images/")
# 输出: ./images/flask_cover.png
```

### ArticleGenerator

```python
from scripts.llm_generator import OpenClawAgentClient, ArticleGenerator

# 初始化 Agent 客户端
client = OpenClawAgentClient()
generator = ArticleGenerator(client)

# 生成文章（v1.2.0 结构化内容）
article = generator.generate(
    repo_data=summary,
    template="intro",      # intro/review/tutorial/list/release
    style="casual"         # casual/professional/enthusiastic/story/minimal
)
```

### 格式化工具

```python
from scripts.formatters import RedNoteFormatter, format_rednote_article

formatter = RedNoteFormatter()

# v1.2.0 Stars 智能显示
formatter.format_repo_card(repo_data)  # Stars < 100 时不显示
formatter.format_stars_display(1500)   # 返回 "⭐ 1.5k stars | "
formatter.format_stars_display(50)     # 返回 "" (不显示)

# 一键格式化完整文章
article = format_rednote_article(
    content=content,
    title=title,
    repo_data=repo_data,
    tags=["#Python", "#开源"]
)
```

## 缓存机制

GitHub API 响应默认缓存 1 小时，缓存位置：`~/.cache/github-to-rednote/`

```python
from scripts.github_api import GitHubCache

# 查看缓存统计
cache = GitHubCache()
print(cache.stats())

# 清除缓存
cache.clear()
```

## 测试

```bash
# 运行完整测试套件
cd scripts
python3 test_github_api.py

# 测试单个仓库
python3 github_api.py https://github.com/pallets/flask

# 测试文章生成
python3 llm_generator.py https://github.com/pallets/flask intro casual

# 测试封面图生成
python3 image_generator.py
```

## 环境要求

- Python 3.8+
- GitHub Token（必需）
- OpenClaw 环境（用于 Agent 内容生成和封面图生成）
- 可选依赖：
  - `pyperclip` - 剪贴板复制
  - `cairosvg` - SVG 转 PNG（封面图）
  - `Pillow` - 图像处理

## 技术栈

- **GitHub API** - 仓库数据获取（增强数据提取 v1.2.0）
- **OpenClaw Agent** - 内置内容生成（改进 Prompt v1.2.0）
- **Canvas/SVG** - 封面图生成（v1.2.0 新增）
- **缓存** - 文件系统缓存（JSON）
- **输出格式** - 小红书风格 Markdown

## 变更日志

### v1.5.0 (2026-03-19)
- 🔗 **封面显示 GitHub 地址** - 自动生成封面图时显示仓库 URL
- 🎨 **浅色主题** - 封面图改用浅色配色方案
- 🦞 **OpenClaw Skill 标识** - 替换 Python 标识为 OpenClaw Skill 品牌
- 🇨🇳 **中文功能提取** - 支持从 README 的「功能特点/特性」部分提取功能点
- ✨ **实用内容提取** - 封面文案优先显示安装/使用/效果等实用信息

### v1.4.0 (2026-03-19)
- 功能优化版本

### v1.3.0 (2026-03-19)
- 样式更新版本

### v1.2.0 (2026-03-18)
- 🎨 **新增封面图生成** - 自动生成 1080×1440 小红书封面
- 📝 **内容质量升级** - 结构化内容：一句话概括 + 适用场景 + 核心功能 + 技术亮点
- 🔍 **增强数据提取** - 自动提取 README Features、项目卖点、最新 Release
- ⭐ **Stars 智能显示** - 根据 Stars 数量智能决定是否显示（≥100 才显示）
- 🎯 **改进 Prompt 模板** - 移除空话套话，要求具体内容支撑

### v1.1.0 (2026-03-18)
- ✨ **重大更新**：从外部 LLM API 迁移到 OpenClaw 内置 Agent 能力
- 🔥 移除所有外部 LLM 配置需求（OpenAI、Anthropic、Moonshot、DeepSeek）
- 🎨 简化配置流程，仅需 GitHub Token

### v1.0.0
- 初始版本，支持多种 LLM 提供商

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 PR！

---

Made with ❤️ for the open source community
