<p align="center">
  <h1 align="center">🧠 Memory Store Skill</h1>
  <p align="center"><strong>跨会话、多 Agent 的结构化记忆 · Structured memory for AI agents</strong></p>
  <p align="center">
    <a href="README.zh.md">中文文档</a> · <a href="README.en.md">English docs</a>
  </p>
  <p align="center">
    <a href="https://www.npmjs.com/package/memory-store-skill"><img src="https://img.shields.io/npm/v/memory-store-skill?style=flat-square&logo=npm" alt="npm version"></a>
    <img src="https://img.shields.io/badge/runtime-Node.js%2018%2B-339933?style=flat-square&logo=nodedotjs" alt="Node.js 18+">
    <img src="https://img.shields.io/badge/dependencies-zero-2ea44f?style=flat-square" alt="zero runtime dependencies">
  </p>
</p>

Memory Store 是一个轻量级 Agent skill：Agent 负责判断什么值得记、何时检索，纯 Node.js CLI 负责校验、存储、过滤、排序和归档。

Memory Store is a lightweight agent skill. The agent decides what is worth remembering and when history is relevant; a zero-dependency Node.js CLI handles validation, persistence, filtering, ranking, and archiving.

## Install · 安装

Requires Node.js 18+ · 需要 Node.js 18+

```bash
npm i memory-store-skill
npx memory-store setup --agent codex --mode explicit
```

Installing the npm package does not run lifecycle hooks or modify Agent directories. The explicit second command installs the skill for the selected platform. Start a new Agent session afterward.

npm 包安装不会运行生命周期脚本，也不会修改 Agent 目录。第二条显式命令才会把 skill 安装到指定平台；完成后请新开一个 Agent 会话。

Memory policy can be changed later · 记忆策略可在安装后调整：

```bash
npx memory-store mode
npx memory-store mode balanced --global
npx memory-store mode explicit --workspace
```

Profiles: `off`, `explicit` (safe default), `balanced`, and `proactive`. Workspace configuration overrides the global profile.

档位包括 `off`、`explicit`（安全默认值）、`balanced` 和 `proactive`；工作区配置会覆盖全局配置。

```bash
# Verify · 验证
npx memory-store status

# Inspect or select a platform · 查看或指定平台
npx memory-store setup --list
npx memory-store setup --agent codex
```

## Update · 更新

```bash
npm i memory-store-skill@latest
npx memory-store setup --sync
```

The first command explicitly upgrades the npm package. The second syncs only existing skill installations from that local package, verifies the result, and leaves memory data unchanged. The updater does not download or execute remote code.

第一条命令显式升级 npm 包；第二条命令从本地包同步已有的 skill 安装并完成校验，不会修改记忆数据。更新器本身不会下载或执行远程代码。

```bash
# Preview or update one platform · 预览或指定平台
npx memory-store setup --sync --dry-run
npx memory-store setup --sync --agent codex
```

| Capability | 说明 / Description |
|---|---|
| Two scopes | 全局 `global` + 项目 `workspace` |
| Visibility labels | `private` / `shared` / `global` cooperative filtering |
| Eight memory types | fact, decision, preference, workflow, debug_solution, state, event, relation |
| Retrieval | keyword, tags, type, freshness, importance, and Chinese n-grams |
| Lifecycle | TTL, priority-aware decay, archive, restore, merge |
| Runtime | Node.js 18+, no third-party runtime dependencies, no daemon |

## One-command terminal · 单命令终端

Run `npx memory-store` in an interactive terminal to open a numbered menu for setup, search, adding memories, profile changes, status, and maintenance preview. With no TTY, the same command prints compact help and exits without waiting.

在交互终端运行 `npx memory-store` 即可打开数字菜单，完成安装、搜索、添加记忆、档位设置、状态查看和维护预览。非交互环境不会等待输入，而是输出精简帮助后退出。

Automation and Agents can use the short commands directly:

```bash
npx memory-store remember decision "数据库选型" "使用 SQLite，适合本地单用户部署" --workspace
npx memory-store recall "数据库选型" --json
npx memory-store mode balanced --global
npx memory-store status --json
```

> `private` is not encryption or an operating-system security boundary. Do not store credentials, tokens, keys, or raw personal data.

## Start here

- [中文：完整说明与 5 分钟上手](README.zh.md)
- [English: full guide and quick start](README.en.md)
- [CLI 速查表](CHEATSHEET.md)
- [常见问题](FAQ.md)
- [安全边界 / Security model](SECURITY.md)
- [Agent 指令](SKILL.md)

需要从源码安装或参与开发时：

```bash
git clone https://github.com/Revolves/memory-store-skill.git
cd memory-store-skill
node scripts/install.js --all
```

## License

MIT.
