# KMind Markdown To Mind Map

[English](./README.md)

将 Markdown 标题大纲离线转换为高质量的 KMind 导图。

这个 skill 支持导出：

- `PNG` 位图
- `SVG` 矢量图
- 可继续在 KMind 中编辑的 `.kmindz.svg`

它支持主题预设、根布局、连线样式、明暗模式和彩虹分支。

推荐输入是以 `#`、`##`、`###` 等 Markdown 标题组织的层级大纲。标题会转换为导图节点；标题下方的非标题正文会转换为该节点的备注。图片导出时备注默认只显示为备注入口图标，不展开正文；如需查看或继续编辑这些备注内容，请导出 `.kmindz.svg` 并在 KMind Zen 客户端中打开。

如果用户只是要求导图图片，推荐默认导出 `PNG`；只有在明确需要矢量图时再导出 `SVG`。

## 仓库内容

这个仓库是 `kmind-markdown-to-mindmap` 的可发布 skill bundle。

主要文件：

- `SKILL.md`：给 agent runtime 使用的 skill 说明
- `scripts/kmind-render.mjs`：本地命令入口
- `scripts/vendor/*`：打包后的 KMind CLI 运行时
- `agents/openai.yaml`：agent 元数据

## 环境要求

- 本机已安装 Node.js
- 若要自动导出 `SVG` / `PNG`，本机需要有可用的 Chromium 浏览器
- 本地转换本身不依赖网络连接

说明：

- `.kmindz.svg` 导出不依赖浏览器渲染
- `SVG` / `PNG` 导出会走本地浏览器渲染流程

## 快速开始

查看可用主题、布局和连线：

```bash
node ./scripts/kmind-render.mjs themes --format json
```

导出可编辑的 KMind 项目文件：

```bash
node ./scripts/kmind-render.mjs import-markdown ./outline.md \
  --output ./outline.kmindz.svg
```

导出 PNG 导图（推荐默认图片格式）：

```bash
node ./scripts/kmind-render.mjs render-markdown ./outline.md \
  --output ./outline.png \
  --theme-preset kmind-material-3-slate \
  --layout mindmap-both-auto \
  --edge-route orthogonal \
  --appearance dark \
  --rainbow on
```

导出 SVG 导图：

```bash
node ./scripts/kmind-render.mjs render-markdown ./outline.md \
  --output ./outline.svg \
  --theme-preset kmind-rainbow-breeze \
  --layout logical-left \
  --edge-route edge-lead-quadratic \
  --appearance dark \
  --rainbow auto
```

通过 stdin 输入 Markdown：

```bash
node ./scripts/kmind-render.mjs render-markdown - \
  --output ./stdin-demo.png <<'EOF'
# 终端输入示例
## 分支 A
### 条目 1
## 分支 B
### 条目 2
EOF
```

## 常用参数

- `--output`：输出路径；通常会按文件后缀推断格式。普通图片需求推荐 `.png`，明确需要矢量图时再使用 `.svg`
- `--theme-preset`：主题预设 id
- `--layout`：根布局 id
- `--edge-route`：连线样式 id
- `--appearance`：`light` 或 `dark`
- `--rainbow`：`auto`、`on`、`off`
- `--png-scale`：PNG 导出倍率，默认 `1`
- `--browser`：`auto` 或 `manual`

当前对外开放的布局：

- `logical-right`
- `logical-left`
- `mindmap-both-auto`

当前对外开放的连线：

- `cubic`
- `edge-lead-quadratic`
- `center-quadratic`
- `orthogonal`

## 推荐默认值

- `theme-preset`：`kmind-material-3-slate`
- 图片输出后缀：`.png`
- `appearance`：`light`
- `rainbow`：`auto`
- `png-scale`：`1`

如果你想要的是可继续编辑的 KMind 文件，而不是图片，优先使用：

```bash
node ./scripts/kmind-render.mjs import-markdown INPUT_OR_DASH \
  --output OUTPUT.kmindz.svg
```

## 典型场景

- 会议纪要
- 读书笔记
- 头脑风暴清单
- 项目提案
- Markdown 标题大纲转导图工作流

## 限制说明

- 自动图片导出依赖本机可用的 Chromium 浏览器
- skill 本身不会内置浏览器
- 如果自动浏览器拉起不可用，请使用 `--browser manual`
- 长段落等非标题正文会保存为节点备注。导出图片时，这些备注以备注图标表示，不展开为正文。

## 相关信息

- KMind Zen：`https://kmind.app`
- skill id：`kmind-markdown-to-mindmap`
