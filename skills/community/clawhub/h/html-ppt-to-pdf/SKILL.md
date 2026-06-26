---
name: html-ppt-to-pdf
description: Convert any HTML slide deck that uses the `<section class="slide">` convention into a high-fidelity, vector-text PDF using Playwright + Chromium's native `page.pdf()`. Supports decks from the `html-ppt` skill, `frontend-slides` / `frontend-design` skill, and any hand-written HTML that follows the same convention. Triggers on requests like "把 HTML PPT 转 PDF", "这个 HTML 幻灯片导出 PDF", "HTML 转 PDF 出现字体失真/页码错乱/丢页重页/部分内容看不见". DO NOT use for plain web pages (use browser print), Markdown (use pandoc), or `.pptx` (use the pptx skill).
---

# html-ppt-to-pdf

把 HTML 格式幻灯片转成矢量 PDF。文字是可选中可搜索的 live text（不是栅格化图片），字体以 subset 形式嵌入 PDF，页面尺寸和角标与原 HTML 一致。

## When to use

用户手上有一份 HTML 幻灯片要导出成 PDF，典型来源：

- `html-ppt` skill 产物（固定 1920×1080，有 `runtime.js` 注入 `.slide-number`）
- `frontend-slides` / `frontend-design` skill 产物（`100vh` 自适应，用 IntersectionObserver 触发 `.visible` class 做 reveal 动画）
- 任何手写/其他工具产的 HTML，只要用 `<section class="slide">` 约定

过去踩过这些坑本 skill 都处理了：字体和原 HTML 不一致、页码 "101/22" 错乱、截图丢页/重页、frontend-slides 里非首屏 slide 内容全部隐形（`.reveal` 元素 opacity:0）。

**不要用于**：普通网页存 PDF（让用户用浏览器打印即可）；Markdown 转 PDF（用 pandoc/typst）；`.pptx` 转 PDF（用 pptx skill 或 LibreOffice）。

## Input contract

- 输入：HTML 文件绝对路径
- HTML 约定：每张 slide 用 `<section class="slide">`；如果源 HTML 用别的 class（`.deck-slide`、`.page` 等），传 `--slide-selector`
- 默认尺寸：1920 × 1080。frontend-slides 类源码是 `100vh` 自适应，脚本会用 viewport 强制 1920×1080 排版（保证 16:9）
- 输出：单个矢量 PDF 文件，文字可选中，字体 subset 嵌入

## How to invoke

```bash
# 第一次用先装依赖（只需一次）
cd ~/.myagents/skills/html-ppt-to-pdf/scripts
npm install
npx playwright install chromium   # 仅作最后兜底

# 执行转换
node ~/.myagents/skills/html-ppt-to-pdf/scripts/html-to-pdf.mjs <input.html> <output.pdf>

# 自定义尺寸
node ~/.myagents/skills/html-ppt-to-pdf/scripts/html-to-pdf.mjs input.html out.pdf --width 1280 --height 720
```

**强烈推荐系统装 Chrome 或 Edge**。脚本默认自动用系统 Chrome/Edge 出 PDF——Playwright 自带的 Chromium（build 1208 实测）有 `page.pdf()` 绘制 bug：遇到 `display:flex; flex-direction:column` + 内联 `opacity:0; transform:translateY()` 的 reveal-card 结构时会静默丢内容（屏幕/截图正常，唯独 PDF 丢）。系统 Chrome 无此问题。若系统未装 Chrome/Edge，脚本会 fallback 到 bundled Chromium 并打警告。

## Why this approach (critical)

**不要走"截图合成 PDF"**。那条路线（`html-ppt/scripts/render.sh` + ImageMagick 拼 PDF）有三个硬伤：
1. PNG 把文字栅格化，字体信息丢失，放大即糊
2. 逐页 hash 跳转 + 循环截图的时序 bug，经典丢首页/重尾页
3. `runtime.js` 动态注入的页码与截图时序冲突

本 skill 用 Playwright 的 `page.pdf()`，由 Chromium 排版引擎一次性吐出多页矢量 PDF：
- 字体：等 `document.fonts.ready` 再排版 → Chromium 把用到的字形 subset 嵌入 `/FontFile2`
- 分页：注入 `@page` + `page-break-after` CSS → Chromium 原生分页，不存在循环
- 页码：自动把 `.slide-number` 的 `data-current` / `data-total` 修成正确值，解决 "101/22" 那种 DOM 硬写文本和 CSS `::before`/`::after` 叠加的 bug
- 排版差异适配：
  - **deck 风格**（html-ppt：所有 slide `position: absolute; top: 0`）→ 强制 `position: static` 把 slides 摊开
  - **flow 风格**（frontend-slides：`height: 100vh`）→ 用固定 px 尺寸覆盖 `vh` 单位
  - **reveal 动画**（frontend-slides 的 `.reveal` + IntersectionObserver 加 `.visible`）→ 强制给每张 slide 加 `.visible` class，并把 `.reveal` 的 `opacity`/`transform` 设为终态，避免非首屏内容隐形
  - 统一隐藏运行时 UI：`.progress-bar`、`.nav-dots`、`.edit-toggle`、`.edit-hotzone` 等不进 PDF

## Verification

跑完后必须验证（阿成踩过这些坑）：
- 页数 = HTML 里 `<section class="slide">` 的数量，不多不少
- 首页和末页和 HTML 一致
- 用 Adobe Reader 打开，文字能选中能复制（证明矢量嵌入）
- 页面尺寸正确（Acrobat → 文件属性 → 页面大小）
- 每页的角标/页码都在

## Troubleshooting

见 `~/.myagents/skills/html-ppt-to-pdf/README.md`。
