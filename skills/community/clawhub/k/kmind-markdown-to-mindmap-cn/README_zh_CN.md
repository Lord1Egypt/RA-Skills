# KMind Markdown To Mind Map CN

[English](./README.md)

这是 `kmind-markdown-to-mindmap` 的中文本地化版本，面向中文工作流和中文 agent 提示词。

它可以将 Markdown 标题大纲离线转换为 KMind 导图，并支持：

- `PNG` 导出
- `SVG` 导出
- 可继续编辑的 `.kmindz.svg` 导出

推荐输入是以 `#`、`##`、`###` 等 Markdown 标题组织的层级大纲。标题会转换为导图节点；标题下方的非标题正文会转换为该节点的备注。图片导出时备注默认只显示为备注入口图标，不展开正文；如需查看或继续编辑这些备注内容，请导出 `.kmindz.svg` 并在 KMind Zen 客户端中打开。

如果用户只是要求导图图片，推荐默认导出 `PNG`；只有在明确需要矢量图时再导出 `SVG`。

与主 skill 相比，这个版本的运行时能力一致，但 skill 标识、默认提示与文案更偏中文使用场景。

## 仓库内容

- `SKILL.md`：本地化后的 skill 说明
- `scripts/kmind-render.mjs`：本地命令入口
- `scripts/vendor/*`：打包后的 KMind CLI 运行时
- `agents/openai.yaml`：本地化后的 agent 元数据

## 环境要求

- 本机已安装 Node.js
- 若要自动导出 `SVG` / `PNG`，本机需要有可用的 Chromium 浏览器
- 本地转换本身不依赖网络连接

## 快速开始

查看可用主题：

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

## 说明

- `.kmindz.svg` 导出不依赖浏览器渲染
- 自动图片导出依赖本机可用的 Chromium 浏览器
- 普通图片需求推荐优先导出 `PNG`
- 如果自动浏览器拉起不可用，请使用 `--browser manual`

## 相关信息

- KMind Zen：`https://kmind.app`
- skill id：`kmind-markdown-to-mindmap-cn`
