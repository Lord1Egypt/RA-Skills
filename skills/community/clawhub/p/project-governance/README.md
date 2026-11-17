# project-governance

给 AI 长期项目建立「项目记忆 + 文件索引 + 工作规则 + 版本记录」的治理系统。
让 AI 换会话、换模型、甚至换 Agent 后，仍然能正确接着项目做，而不是重新猜项目。

## 三层结构：治理规范 / CLI / Skill 适配器

```
project-governance
│
├── 治理规范本体（Agent-agnostic，跨平台通用）
│   ├── templates/AGENTS.md        — 项目协议模板（核心规则 + 项目定制）
│   ├── templates/index.md         — 目录地图模板（带链接 + 注释）
│   ├── templates/index_notes.json — index 短注释注册表
│   ├── templates/VERSIONS.md      — 稳定版本索引模板（权威等级）
│   ├── templates/LESSONS.md       — 错误档案模板
│   ├── templates/CHANGELOG.md     — 变更记录模板
│   ├── templates/whitelist.json   — 通过参数注册表
│   └── templates/blacklist.json   — 失败参数注册表
│
├── CLI / Validator（Agent-agnostic）
│   └── scripts/governance.py      — init / validate / index / check
│
└── Skill 封装（Agent-specific）
    └── SKILL.md                   — 告诉 Trae 如何发现和使用这套体系
```

核心原则：

> **治理数据保持 Agent-agnostic；适配层才允许 Agent-specific。**

`VERSIONS.md` / `LESSONS.md` / `whitelist.json` / `blacklist.json` / `index.md`
是跨 Agent 的公共协议；`SKILL.md` / `CLAUDE.md` / `AGENTS.md` / `.cursor/rules/`
属于适配器。这样即使某个 AI 平台改变 Skill 机制，治理体系本身不会跟着废掉。

Skill 只是「告诉某个 Agent 如何理解和使用这套治理体系的适配器」，不是治理体系本身。

## Memory & Governance Boundary

平台记忆（如 Trae 的用户档案 / 项目记忆）与治理文件是互补关系，不是重复：

| 层 | 回答什么 |
|---|---|
| 平台记忆 | "以前发生过什么 / 这个用户通常怎么做" |
| 治理文件 | "这个项目现在必须怎么做、文件在哪、哪个版本是权威" |

冲突时的权威优先级：

1. 当前项目文件 / 冻结版本
2. 项目治理文件（AGENTS.md / index.md / VERSIONS.md / 注册表）
3. 项目记忆
4. 用户长期记忆
5. AI 推测

记忆是**上下文来源，不是权威事实库**。当记忆与治理文件冲突时，以治理文件为准；
从记忆获得的长期约定，应在人工确认后沉淀进治理文件，记忆本身永远不能成为项目权威。

## 快速开始

```bash
python scripts/governance.py init --project-dir /path/to/project --project-name "My Project"
python scripts/governance.py index --project-dir /path/to/project
python scripts/governance.py check --project-dir /path/to/project
```

## 子命令

| 子命令 | 作用 |
|---|---|
| `init` | 从 templates/ 生成 11 个治理文件（--force 覆盖已有文件） |
| `validate` | 校验 whitelist/blacklist 是否符合 schema（--relaxed 用于迁移旧注册表） |
| `index` | 从文件系统重建 index.md 目录地图（带链接 + index_notes.json 注释，可自定义章节名） |
| `check` | 健康检查：必需文件、注册表、index_notes.json、index 是否最新 |

## 验收：Trae 冷启动实测

安装 Skill 后，用新会话进入一个陌生项目，验证：

1. Trae 是否发现并加载 Skill
2. AI 是否主动读取 `index.md`
3. 是否找到正确版本（而不是历史错误文件）
4. 是否遵守 `AGENTS.md`
5. 是否读取 `whitelist.json` / `blacklist.json`
6. 修改文件后是否更新 `index.md` / `CHANGELOG.md` / `session_handoff.md`
7. 第二次冷启动能否无人工解释继续工作

## Limitations

**Agent compatibility**

This package is currently designed and tested primarily for Trae Skills. Other
AI coding agents may use the generated governance files, but automatic Skill
discovery, loading, and instruction behavior are not guaranteed outside Trae.

The governance files and CLI are intentionally kept as agent-neutral as
practical, allowing future adapters for other AI agents without changing the
core governance structure.

## 验证

CLI 已通过 76 用例健壮性测试（基础 + 边界 + 对抗性，stdlib-only），覆盖空目录、非 UTF-8 编码、目录型路径、超长路径、特殊字符文件名等破坏式场景。测试套件保留在开发仓库中，未随包发布。
