---
name: obsidian-note-to-mindmap-cn
description: 将用户明确提供的 Obsidian 笔记或 Markdown 大纲默认转换为 KMind 导图 PNG，并在明确要求时输出可编辑的 KMind 导图；如果缺少已审核的 KMind core skill，先征求确认后再从 ClawHub 安装。
version: 0.1.0
user-invocable: true
metadata: {"openclaw":{"skillKey":"obsidian-note-to-mindmap-cn","emoji":"🧠","requires":{"bins":["clawhub"]}}}
---

这个 skill 是一个轻量的 Obsidian 到 KMind 工作流 wrapper。

适用于以下输入：

- 用户直接贴出的 Obsidian 笔记
- 用户直接贴出的 Markdown 大纲
- 用户明确指定的单个笔记文件路径

目标是输出 KMind 导图结果，默认使用 `PNG`。

这个 wrapper 本身不内置渲染器，而是把实际转换委托给已经过审核的 core skill `suka233/kmind-markdown-to-mindmap`。

依赖的已审核 core skill：

- ClawHub slug：`suka233/kmind-markdown-to-mindmap`
- URL：`https://clawhub.ai/suka233/kmind-markdown-to-mindmap`

安全边界：

- 只处理用户明确提供的内容，或用户明确指定的单个笔记路径。
- 不扫描整个 vault。
- 不读取 Obsidian 全局配置文件。
- 除上面写死的 core skill 外，不安装任何插件、包、二进制或其他 skill。
- 若缺少 core skill，必须先征求明确确认，再执行安装。
- 若用户拒绝安装，则停止，并提供精确 ClawHub 链接，不要临时改走其他路径。
- 若当前运行环境不支持标准 ClawHub 安装流程，则直接说明限制，不要发明替代安装器。

安装规则：

- 只有在用户明确同意后，才允许通过运行时的标准 ClawHub 安装流程安装这个精确的已审核 core skill：
  `clawhub install suka233/kmind-markdown-to-mindmap --workdir ./`
- 不得替换成其他 slug，包括本地化变体。

首次确认文案：

`这个流程需要使用已经过审核的 core skill：suka233/kmind-markdown-to-mindmap，当前尚未安装。如果你同意，我可以从 ClawHub 安装这个精确的 skill，然后继续当前导图转换。我不会安装任何其他内容。是否继续？`

工作流：

1. 先确认输入是用户贴出的 Markdown/文本，或用户明确给出的单个笔记路径。
2. 如果输入是文件路径，只读取该精确文件。
3. 检查已审核 core skill 是否可用。
4. 若缺失，先征求明确确认，再执行上面的精确安装命令。
5. 安装完成后，将内容转交给 `suka233/kmind-markdown-to-mindmap`。
6. 当用户未指定输出格式时，默认输出 `PNG`。
7. 只有当用户明确要求可编辑的 KMind 导图时，才输出 `.kmindz.svg`。
8. 只有当用户明确要求 `SVG` 时，才输出 `SVG`。
9. 如果已安装 core skill 反馈缺少 Node.js 或浏览器依赖，要如实暴露结果，不要绕过。

禁止事项：

- 扫描整个 vault
- 自动发现笔记
- 读取 `~/Library/Application Support/obsidian/obsidian.json` 等宿主配置文件
- 重命名、移动、删除、改写笔记
- 建议强制安装可疑包或可疑 skill
- 隐藏安装步骤
