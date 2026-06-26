# html-ppt-to-pdf — Troubleshooting

## 一次性安装

```bash
cd ~/.myagents/skills/html-ppt-to-pdf/scripts
npm install                 # 装 Playwright + pdf-lib
npx playwright install chromium   # 下 Chromium（作为最后兜底）
```

> **强烈建议系统装 Chrome 或 Edge**。脚本默认用系统 Chrome/Edge 出 PDF——Playwright 自带的 Chromium（build 1208 实测）有一个具体场景的 PDF 绘制 bug：当 slide 里出现 `display:flex; flex-direction:column` + 带 `opacity:0; transform:translateY()` 内联样式的 reveal-card 时，输出的 PDF 会静默丢掉这部分内容（屏幕截图和 fullPage 截图都正常，只有 page.pdf() 受影响）。系统 Chrome 无此问题。

## 为什么不用截图合成

曾经走的 `render.sh + ImageMagick` 路线（把每页截成 PNG 再拼 PDF）三个病根：

| 症状 | 根因 |
|------|------|
| 字体和原 HTML 不一样、放大糊 | PNG 把文字栅格化，字体信息没进 PDF |
| 页码/角标错 | `runtime.js` 异步注入页码，截图时常没等到 |
| 第一页丢/最后一页重 | 循环 hash 跳转 + 截图的 off-by-one 时序 bug（Puppeteer issue #1576 同款） |

本 skill 用 `page.pdf()`，Chromium 一次性吐多页矢量 PDF：字体 subset 嵌入、`@page` 原生分页、无循环。

## 字体不对？

默认情况下 Chromium 会加载 HTML 里的 Google Fonts / Web Fonts，脚本用 `document.fonts.ready` 等字体 decode 完再排版。如果还是不对：

1. **网络问题（最常见）**：Google Fonts 在国内有时走不通。三种兜底：
   - `--proxy http://127.0.0.1:7897`（或你常用的代理地址）
   - 设环境变量 `HTTPS_PROXY=http://127.0.0.1:7897` 再跑脚本
   - **最稳**：把 HTML 里的 Google Fonts `<link>` 换成本地 `@font-face`，字体文件放旁边的 `fonts/` 目录，用 `url("./fonts/xxx.woff2")` 引用（可用 [google-webfonts-helper](https://gwfh.mranftl.com/fonts) 下载 WOFF2）
2. **系统缺字体**：Windows 上如果 HTML 用了不在系统里的字体（比如某些中文字库），Chromium 会 fallback。@font-face 本地嵌入是唯一正确解。
3. **字体没被 subset 嵌入**：Acrobat 打开 PDF → 文件属性 → 字体 → 应该看到字体名 + "Embedded Subset"。如果是 "Custom / 未嵌入"，说明脚本出 PDF 前字体没就绪——把 `--extra-wait` 调到 1500 或 2000 ms 重试。

## 页码/角标缺失？

- html-ppt 源：默认修 `.slide-number` 的 `data-current` / `data-total`，并清空里面硬写的文本，解决 "101/22" bug。日志里会打印 `page numbers: fixed N (M slide(s) had none)`
- frontend-slides 源通常没有 `.slide-number`，`missing = N` 不是错，PDF 正常
- 页码是 CSS counter 生成的？无需任何处理，原样呈现
- `runtime.js` 加载失败看终端里的 `[page-error]` 日志

## 页数不对？

脚本最后会打印 `detected N slide(s)`。
- 多了 / 少了 → HTML 里 `section.slide` 数量就不对，先修 HTML
- HTML 数量对但 PDF 页数不对 → 说明某张 slide 触发了 Chromium 的自动分页（内容溢出了 1080px）。调大 `--height`，或检查该 slide 的溢出内容

## frontend-slides / frontend-design 源的特殊处理

这类源的特征：slide 用 `height: 100vh`，字号用 `clamp()`，`.reveal` 元素默认 `opacity: 0`，靠 JS 的 IntersectionObserver 给 slide 加 `.visible` class 才显形。

本 skill 已经内置适配：
- viewport 强制 1920×1080，`100vh` 会被 `height: 1080px !important` 覆盖，保证 16:9
- **给每张 slide 主动加 `.visible` class**（JS 注入），让 reveal 动画的终态样式命中
- 同时把 `.reveal` 的 `opacity: 1 / transform: none / visibility: visible` 强制 `!important`，双保险
- 隐藏 `.nav-dots` / `.edit-toggle` / `.edit-hotzone` 这些运行时 UI

**症状：PDF 部分页白屏或只有标题没正文** → 极大概率是 reveal/visible 机制被作者用了更高优先级选择器绕过了脚本的 override。把 HTML 里搜 `opacity: 0`，看哪个选择器在控制，然后改成不依赖 JS 的静态可见即可。

## 第一页丢、最后一页重？

本 skill 用的是 `page.pdf()` 一次性全量排版，**不走循环截图**，本质上不会出这个问题。如果还是出，十有八九是 HTML 自己用了 `section.slide:not(.active) { display: none }` 之类的样式——脚本注入的 CSS 已经强制 `display: block !important; visibility: visible !important`，但如果 HTML 的选择器优先级更高（比如用了 `!important`），需要在 HTML 源头改或在 `--slide-selector` 的注入 CSS 里加更具体的选择器。

## 自定义选择器

不是 `<section class="slide">` 的 HTML：

```bash
node html-to-pdf.mjs in.html out.pdf \
  --slide-selector ".my-slide" \
  --wait-selector ".footer-num" \
  --width 1280 --height 720
```

## 已知限制

- 不支持 `reveal.js` / `impress.js` 的特殊分页（换算进 3D 变换里的 slide）。这类 HTML 用 [DeckTape](https://github.com/astefanutti/decktape) 更合适
- 不做 PDF 后处理（水印、页眉页脚）。要的话先出 PDF，再用 `pdf` skill 加工
- Playwright 的 Chromium 大约 200MB，第一次下载需要几分钟；一次装好永久用

## 验证 PDF 是否矢量

三个快检方法：
1. 浏览器打开 PDF，用鼠标选中一段文字 → 能选中 = 矢量
2. Acrobat → 文件属性 → 字体 → 能看到字体名 + "Embedded Subset" = 矢量
3. 放大到 400% 文字依然锐利 = 矢量
