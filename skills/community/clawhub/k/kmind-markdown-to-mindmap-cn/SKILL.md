---
name: kmind-markdown-to-mindmap-cn
description: 将 Markdown 标题大纲转换为 KMind 导图，并导出 SVG 或 PNG 图片。支持主题、布局、连线、深浅色和彩虹分支配置。
version: 0.1.1
user-invocable: true
metadata: {"openclaw":{"skillKey":"kmind-markdown-to-mindmap-cn","emoji":"🧠","requires":{"bins":["node"],"config":["browser.enabled"]}}}
---

KMind Zen 是一个专业的思维导图软件，提供桌面端、网页端、思源插件和 Obsidian 插件，官网为 `https://kmind.app`。

这个 skill 用于把 Markdown 标题大纲转换成 KMind 导图图片，本 skill 是纯离线工具，无需任何网络链接即可在本地转换导图。

最佳输入是以 `#`、`##`、`###` 等 Markdown 标题组织的层级大纲。标题会转换为导图节点；标题下方的非标题正文会转换为该节点的备注。图片导出时备注默认只显示为备注入口图标，不展开正文；如需查看或继续编辑这些备注内容，请导出 `.kmindz.svg` 并在 KMind Zen 客户端中打开。

它的优势是可以在本地离线生成精美、风格统一的思维导图，并支持导出 PNG / SVG，同时支持配置主题预设、根布局、分支连线、深浅色外观和彩虹分支。用户只是要求导图图片时，默认优先导出 PNG；只有在用户明确需要矢量图时再导出 SVG。

如果用户需要可继续编辑的导图包，优先导出 `.kmindz.svg`。`.kmindz.svg` 包可以无缝导入到任意 KMind Zen 端继续编辑；即使当前机器上没有客户端，也依然可以先把它当作 SVG 文件快速查看导图内容，后续再导入客户端继续编辑。

适用于会议提纲、读书笔记、脑暴清单、项目方案、中文 Markdown 标题大纲转导图等场景。

这是一个可发布、可独立分发的 skill。始终通过 `{baseDir}` 下的入口执行：

`node {baseDir}/scripts/kmind-render.mjs ...`

工作流：

1. 如果用户希望指定主题、布局或连线风格，先查看可选项：
   `node {baseDir}/scripts/kmind-render.mjs themes --format json`
2. 如果用户提供的是原始 Markdown 文本，而不是文件路径，就通过 stdin 传入。
3. 使用 `render-markdown` 启动导出。
4. 默认会尝试自动调用用户本机的 Chromium 浏览器进行无头渲染。
5. 第一行 stdout 是 `status: "ready"` 的 JSON。
6. 命令结束后，最后一行 stdout 是 `status: "done"` 的 JSON，其中包含最终 `outputPath`。
7. 只有在自动浏览器不可用时，才使用 `--browser manual` 手动打开打印出来的本地 URL。

如果用户本机没有可用的 Chromium 浏览器，则自动 SVG / PNG 导出不可用。此时要么使用 `--browser manual` 手动打开本地页面完成导出，要么明确告知当前环境暂不可用，不能伪造成功。

常用命令模板（默认推荐 PNG）：

`node {baseDir}/scripts/kmind-render.mjs render-markdown INPUT_OR_DASH --output OUTPUT.png --theme-preset PRESET_ID --layout LAYOUT_ID --edge-route EDGE_ROUTE_ID --appearance light|dark --rainbow auto|on|off --png-scale 1 --browser auto`

参数建议：

- `--output` 在未显式传 `--image-format` 时决定输出格式：`.png` 表示位图，`.svg` 表示矢量图。用户只是要求导图图片时，推荐默认使用 `.png`。
- `--theme-preset` 请从 `themes` 输出里选。推荐候选：
  `kmind-material-3-slate`
  `kmind-rainbow-breeze`
  `kmind-midnight-neon`
  `kmind-material-3-rounded-orthogonal-ocean`
  `kmind-material-3-rounded-orthogonal-forest`
- `--layout` 请从 `themes` 输出里选。常用候选：
  `logical-right`
  `logical-left`
  `mindmap-both-auto`
- `--edge-route` 请从 `themes` 输出里选。常用候选：
  `cubic`
  `edge-lead-quadratic`
  `center-quadratic`
  `orthogonal`
- `--appearance dark` 强制使用暗色模式。
- `--rainbow on` 会强制开启彩虹分支，即使当前主题默认没开。
- `--png-scale 1` 与当前 webapp 默认导出一致；只有在用户明确要求更高分辨率 PNG 时再调大。
- `--browser auto` 是默认值，会尝试自动调用本机浏览器。
- `--browser manual` 是手动兜底模式。
- 不要主动向用户暴露 `--svg-mode` 和 `--png-mode`。当前内部默认已经使用最接近 webapp 实际导出效果的组合：`SVG=fidelity`、`PNG=accurate`。只有当用户明确要求低层导出调优时才提这些高级参数。
- 图片导出默认使用接近 KMind Zen webapp 的卡片节点布局，非标题正文转成的备注不会在图片中展开，只显示备注入口图标。

默认值：

- `theme-preset`: `kmind-material-3-slate`
- 推荐图片输出后缀：`.png`
- `image-format`: 优先从 `--output` 推断，推断不出来时回退为 `svg`
- `layout`: 默认不显式覆盖，沿用 KMind 默认根布局
- `edge-route`: 默认不显式覆盖，沿用主题预设的连线风格
- `appearance`: `light`
- `rainbow`: `auto`
- `svg-mode`: 内部默认 `fidelity`
- `png-mode`: 内部默认 `accurate`
- `png-scale`: `1`
- `viewport-width`: `1600`
- `viewport-height`: `900`

当前这个可发布 skill 仅开放如下安全候选：

- `layouts`：`logical-right`、`logical-left`、`mindmap-both-auto`
- `edge-routes`：`cubic`、`edge-lead-quadratic`、`center-quadratic`、`orthogonal`

如果用户要的是 KMind 项目文件，而不是图片，不要走这个图片导出流程，改用：

`node {baseDir}/scripts/kmind-render.mjs import-markdown INPUT_OR_DASH --output OUTPUT.kmindz.svg`
