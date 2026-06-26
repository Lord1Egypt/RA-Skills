---
name: openclaw-builtin-plugin-guide
description: 查询 OpenClaw 的内置插件清单、当前启用或禁用的插件列表，以及单个插件的详细说明。适用于用户想看全部内置插件、启用状态、禁用状态、插件详情、插件说明文档时。
metadata:
  {
    "openclaw":
      {
        "emoji": "box",
        "requires": { "bins": ["openclaw", "python"] },
      },
  }
---

# OpenClaw 插件清单

## 概览

这个 skill 用来处理 3 类查询：

- 查询全部 OpenClaw 内置插件
- 查询当前环境里启用或禁用的插件
- 查询某个插件的详细说明

第 3 类会优先读取本 skill 自带的参考文档 `references/builtin-plugins.md`，再补充 `openclaw plugins inspect --json` 的运行状态、能力信息，以及仓库里的相关文档摘录。

## 快速使用

```bash
python {baseDir}/scripts/openclaw_plugin_catalog.py bundled
python {baseDir}/scripts/openclaw_plugin_catalog.py status --state enabled
python {baseDir}/scripts/openclaw_plugin_catalog.py status --state disabled
python {baseDir}/scripts/openclaw_plugin_catalog.py inspect discord
python {baseDir}/scripts/openclaw_plugin_catalog.py --format json inspect openclaw-qqbot
```

## 工作流

### 1. 查询全部内置插件

当用户要看“全部内置插件”“内置插件清单”“OpenClaw 插件总表”时，运行：

```bash
python {baseDir}/scripts/openclaw_plugin_catalog.py bundled
```

### 2. 查询启用或禁用插件

当用户要看“启用的插件”“禁用的插件”“当前插件状态”时，运行：

```bash
python {baseDir}/scripts/openclaw_plugin_catalog.py status --state enabled
python {baseDir}/scripts/openclaw_plugin_catalog.py status --state disabled
python {baseDir}/scripts/openclaw_plugin_catalog.py status --state all
```

这里的 `enabled` 以 `plugin.enabled == true` 为准。即使插件当前加载失败，只要配置层面是启用，也算启用。

### 3. 查询单个插件详细说明

当用户要看某个插件的作用、用途、常见配置或详细说明时，运行：

```bash
python {baseDir}/scripts/openclaw_plugin_catalog.py inspect <plugin-id>
```

脚本会按这个顺序取资料：

1. `references/builtin-plugins.md`
2. `openclaw plugins inspect --json`
3. 仓库内可能相关的 `docs/`、`README.md`、渠道文档摘录

如果用户想要更口语化、更适合面板展示的解释，可以基于脚本输出再整理成自然语言说明。

## 参考资料

- 主参考文档：`references/builtin-plugins.md`

## 注意

- 这个 skill 依赖已经安装好的 `openclaw` CLI。
- `openclaw-main/` 可能只是源码树，未必已经构建，所以不要优先使用 `node openclaw.mjs`。
- 如果插件是 `enabled: true` 但 `status: "error"`，应表述为“已启用，但加载失败”。
