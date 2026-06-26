---
name: ppt-master
description: AI-driven multi-format SVG content generation system for presentations, social media graphics, and marketing materials. Use when creating PPTs, posters, or visual content from documents.
---

# PPT Master - AI 视觉内容生成系统

基于 AI 多角色协作的 SVG 内容生成系统，支持演示文稿、社交媒体、营销海报等多种格式。

## 何时使用此 Skill

- 从 Markdown/PDF/URL 生成 PPT 演示文稿
- 创建小红书、朋友圈等社交媒体图文
- 设计营销海报、信息图
- 批量生成可视化内容

## 核心工作流

```
源文档 → 创建项目 → 模板选择 → Strategist 规划 → [Image Generator 配图] → Executor 生成 SVG → 后处理 → 导出 PPTX
```

## 快速开始

### 1. 前置检查

**阅读角色定义前必须加载对应文件：**
- [Strategist](roles/Strategist.md) - 内容规划
- [Executor](roles/Executor_General.md) - SVG 生成
- [Image Generator](roles/Image_Generator.md) - 配图生成

**阅读技术约束：**
- [AGENTS.md](AGENTS.md) - 完整工作流程和规则手册
- [设计指南](docs/design_guidelines.md) - 配色、排版规范

### 2. 创建项目

```bash
mkdir -p projects/<name>/{src,output/images,output/final}
# 源文档放入 src/ 目录
```

### 3. 源文档处理

| 格式 | 工具 | 命令 |
|------|------|------|
| PDF | `tools/pdf_to_md.py` | `python3 tools/pdf_to_md.py <pdf> <out.md>` |
| URL | `tools/web_to_md.py` | `python3 tools/web_to_md.py <url> <out.md>` |
| 微信公众号 | `tools/web_to_md.cjs` | `node tools/web_to_md.cjs <url> <out.md>` |

### 4. 执行工作流

**Step 1: Strategist 分析**
- 读取源文档
- 确定画布格式（PPT 16:9 / 小红书 / 海报等）
- 规划页数、内容结构
- 输出：`projects/<name>/plan.md`

**Step 2: Image Generator 配图（可选）**
- 根据内容需求搜索或生成图片
- 图片放入 `projects/<name>/output/images/`
- 使用 `tools/embed_images.py` 嵌入 SVG

**Step 3: Executor 生成 SVG**
- 按规划逐页生成 SVG
- 输出到 `projects/<name>/output/`
- 使用 `tools/finalize_svg.py` 后处理

**Step 4: 导出 PPTX**
```bash
python3 tools/svg_to_pptx.py projects/<name> -o output.pptx
# 或使用 --use-final 使用 final/ 目录的 SVG
```

## 支持的画布格式

参考 [docs/canvas_formats.md](docs/canvas_formats.md)：

| 格式 | 尺寸 | 用途 |
|------|------|------|
| `ppt169` | 1920×1080 | 标准 PPT 16:9 |
| `ppt43` | 1440×1080 | 传统 PPT 4:3 |
| `xiaohongshu` | 900×1200 | 小红书图文 |
| `moments` | 1080×1080 | 朋友圈方形 |
| `phone9_16` | 1080×1920 | 手机全屏海报 |
| `a4` | 595×842 | A4 文档 |

## 工具速查

```bash
# SVG → PPTX
python3 tools/svg_to_pptx.py <project> -o <out.pptx>

# PDF/网页 → Markdown
python3 tools/pdf_to_md.py <in.pdf> <out.md>
python3 tools/web_to_md.py <url> <out.md>

# 图片处理
python3 tools/embed_images.py <svg> <image_dir>
python3 tools/crop_images.py <image> [options]
python3 tools/fix_image_aspect.py <image>

# SVG 后处理
python3 tools/finalize_svg.py <project>
python3 tools/svg_quality_checker.py <project>

# 项目管理
python3 tools/project_manager.py create <name>
python3 tools/project_manager.py list
```

## 示例项目

- [examples/ppt169_demo](examples/ppt169_demo/) - PPT 16:9 完整示例
- [examples/xiaohongshu_demo](examples/xiaohongshu_demo/) - 小红书图文示例
- [examples/poster_demo](examples/poster_demo/) - 海报设计示例

## 依赖安装

```bash
# Python 依赖
pip install python-pptx Pillow beautifulsoup4 requests lxml

# Node.js 工具（可选，用于微信公众号抓取）
npm install
```

## 关键约束

1. **SVG 技术限制**: 禁用 `filter`、`mask`、`clipPath` 等 PPT 不兼容特性
2. **图片格式**: 嵌入前必须使用 `embed_images.py` 处理
3. **字体**: 使用系统标准字体（微软雅黑、思源黑体等）
4. **颜色**: 遵循设计规范中的配色方案

## 完整文档

- [📖 工作流教程](docs/workflow_tutorial.md) - 详细步骤和案例
- [🎨 设计指南](docs/design_guidelines.md) - 视觉规范
- [📐 画布格式](docs/canvas_formats.md) - 所有支持格式
- [🖼️ 图片嵌入指南](docs/svg_image_embedding.md) - 图片处理最佳实践
- [📊 图表模板](templates/charts/) - 13 种标准化图表

## 在线预览

查看生成效果：[GitHub Pages 预览](https://hugohe3.github.io/ppt-master/)
