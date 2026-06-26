# Obsidian Note 转导图

[English](./README.md)

这是一个轻量 wrapper skill，用于把用户明确提供的 Obsidian 笔记或 Markdown 大纲转换为 KMind 导图，默认输出 `PNG` 图片。

这个 bundle 本身不内置渲染器，而是在首次缺少依赖时，先征求用户确认，再从 ClawHub 安装已经过审核的 core skill `suka233/kmind-markdown-to-mindmap`，随后把实际转换工作交给该 core skill。

## 仓库内容

- `SKILL.md`：wrapper 工作流与安全边界
- `agents/openai.yaml`：agent 元数据
- `package.json`：该发布 bundle 的版本真相源

## 运行要求

- 运行环境支持 `clawhub` CLI
- 首次安装已审核 core skill 时需要网络
- core skill 安装完成后，实际转换能力遵循 core skill 自身的运行时要求

## 安装行为

这个 wrapper 不允许隐藏安装步骤。

如果缺少已审核 core skill，必须先征求确认，然后才允许执行：

```bash
clawhub install suka233/kmind-markdown-to-mindmap --workdir ./
```

不得安装任何其他 skill。

## 安全边界

- 只处理用户贴出的内容，或用户明确指定的单个笔记路径
- 不扫描整个 vault
- 不读取 Obsidian 全局配置文件
- 不改写、移动、重命名或删除笔记
- 不建议强制安装可疑包或可疑 skill

## 推荐输出

- 默认输出：`PNG`
- 只有当用户明确要求可编辑的 KMind 导图时，才输出 `.kmindz.svg`
- 只有当用户明确要求 `SVG` 时，才输出 `SVG`

## 相关信息

- 已审核 core skill：`https://clawhub.ai/suka233/kmind-markdown-to-mindmap`
- KMind Zen：`https://kmind.app`
- skill id：`obsidian-note-to-mindmap`
