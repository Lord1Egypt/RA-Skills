---
name: nuomi-xhs-card
description: 当用户提及渲染 Markdown/文本 为小红书风格卡片 ,当用户提及"生成小红书卡片"、"md 转图片"、"制作卡片"、"小红书图文" .
---

# XHS Card Generator

本地 Markdown/MDX 转小红书卡片图生成器。支持 24 种模板、light/dark 模式、智能分页。
不适用：通用图片编辑、截图、PDF 处理、视频制作。
## 快速开始

```bash
# 首次安装（安装依赖 + Playwright chromium）
bash scripts/setup.sh

# 环境检查
node scripts/xhs-card.cjs doctor

# 列出所有模板
node scripts/xhs-card.cjs templates list
```

## 渲染卡片

```bash
node scripts/xhs-card.cjs render ./article.md \
  --theme xiaohongshu --mode light --split auto \
  --size 440x586 --scale 4 --pager --output ./output
```

## CLI 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--theme` | xiaohongshu | 模板 ID，见下方列表 |
| `--mode` | light | light/dark（不支持时自动回退 light） |
| `--split` | auto | auto=智能分页，hr=按水平线分页，none=不分页 |
| `--size` | 440x586 | 卡片尺寸（宽x高） |
| `--scale` | 4 | 输出图片倍率 |
| `--pager` / `--no-pager` | pager | 显示/隐藏页码 |
| `--mdx-mode` | false | 启用 MDX 解析 |
| `--output` | ./output | 输出目录 |
| `--max-pages` | 80 | 分页上限 |

## 24 个内置模板

`apple-notes` `xiaohongshu` `instagram` `dreamy` `nature` `minimalist` `notebook` `coil-notebook` `business` `typewriter` `watercolor` `fairytale` `japanese-magazine` `traditional-chinese` `art-deco` `pop-art` `cyberpunk` `darktech` `glassmorphism` `warm` `meadow-dawn` `minimal` `bytedance` `alibaba`

完整模板介绍见 [references/templates.md](references/templates.md)

## 执行步骤
1. 查看用户提供的文案,如果不是 md 格式,请咨询用户是否修改符合要求的 md 格式或者重新提供.
2. 根据用户的模板内容,对文案的模板进行建议,并且咨询用户确定模板.
3. 在执行前,需要咨询用户输出目录,或者根据用户上下文或默认行为进行建议,并且要求用户确定.
4. 执行过程中出现任何阻塞性问题,及时反馈.
5. 完成执行后,向用户明确说明.

## 模板选择建议

根据用户文案类型做出笔记模板建议, 并且咨询用户确定需要的模板

| 内容类型 | 推荐模板 |
|----------|----------|
| 知识笔记 | apple-notes, notebook, coil-notebook |
| 生活方式 | xiaohongshu, warm, meadow-dawn |
| 时尚穿搭 | instagram, japanese-magazine |
| 科技数码 | minimalist, cyberpunk, darktech |
| 文艺情感 | typewriter, watercolor, dreamy |
| 商业职场 | business, bytedance, alibaba |

## 调试选项

```bash
# 导出中间产物用于调试
node scripts/xhs-card.cjs render ./article.md \
  --dump-preview-html ./debug/preview.html \
  --dump-structured-html ./debug/structured.html \
  --dump-pagination-json ./debug/pagination.json
```

## 执行后输出

每次渲染完成后，向用户明确说明：

1. **输出目录**和关键图片路径
2. `totalPages`（总页数）、是否回退主题模式、是否触发告警
3. 若失败：失败阶段（解析/结构化/分页/渲染）和下一步建议

## 架构

渲染管线：`Markdown → HTML → 结构化 → 分页 → PNG`

核心模块位于 `scripts/src/core/`：
- `markdown.ts` - Markdown/MDX 转 HTML
- `structure.ts` - HTML 后处理
- `paginate.ts` - 智能分页
- `render.ts` - Playwright PNG 导出
- `themes.ts` - 主题加载与验证

完整 CLI 参考见 [references/cli-reference.md](references/cli-reference.md)
