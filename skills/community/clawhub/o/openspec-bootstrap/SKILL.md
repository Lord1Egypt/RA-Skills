---
name: openspec-bootstrap
description: >
  ［何时使用］当用户要为项目初始化 OpenSpec/SDD（Spec-Driven Development）工作流时；当用户说"配置 SDD""初始化 openspec""搭建 spec-driven 开发环境"时。核心价值是把项目技术栈与工程约定写入 openspec/config.yaml——这一步官方 CLI 不会替你做，且每个新项目都要重复。
license: MIT
metadata:
  author: nieen
  version: 2.0.0
  created: 2026-07-25
  last-updated: 2026-09-24
  tags: [sdd, spec-driven, openspec, atomcode, opencode, bootstrap]
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# OpenSpec Bootstrap

## 📋 功能描述

帮助用户在任意项目中完成 OpenSpec 的安装与初始化，并把项目的技术栈、目录结构、工程约定写入 `openspec/config.yaml`，使后续所有 spec 生成与实现都带上项目上下文。

初始化本身（`openspec init`）是官方 CLI 的工作；本 skill 的核心增量在 **Step 3 —— config.yaml 项目上下文定制**：扫描项目、提炼约定、写好规则。这是每个新项目都要做、而官方工具不替你做的一步。

## 适用场景

- 新项目首次接入 OpenSpec
- 已有项目补配 config.yaml 上下文（init 过但 config 还是模板）
- 更换/新增 Agent CLI 集成（重新跑 init 指定工具即可）

## 前置条件

- 目标项目已是 git 仓库
- Node.js 与 npm 可用（OpenSpec 通过 npm 全局安装）
- 至少一个 OpenSpec 支持的 AI Agent CLI

## 工作流程概览

1. 安装并校验 OpenSpec CLI
2. `openspec init` 初始化（含选择 Agent 工具）
3. **项目上下文定制**：扫描项目 → 覆写 config.yaml（本 skill 的核心）
4. 验证

## Step 0 — 检查并安装 OpenSpec

```bash
# 检测，未安装则全局安装
openspec --version &>/dev/null || npm install -g @fission-ai/openspec@latest

# 验证，预期输出 x.y.z 形式的版本号
openspec --version
```

## Step 1 — 选择 Agent 工具

OpenSpec 支持大量 Agent CLI（claude、codex、opencode、atomcode、zcode、codebuddy 等，且列表随版本增长）。**始终以实际输出为准，不要依赖写死的清单**：

```bash
# 查看当前版本支持的全部工具 ID
openspec init --help
```

交叉检查本机可用的 CLI，确认要接入哪一个。若用户未指定，用 `request_user_input` 让用户选择。

## Step 2 — 初始化

```bash
cd /path/to/project
git status  # 确认工作区干净，init 会重新生成文件
openspec init --tools <tool-id>
```

常用参数：

| 参数 | 说明 |
|------|------|
| `--tools <list>` | 逗号分隔的工具 ID，或 `all`/`none` |
| `--language <lang>` | 让生成的工件使用指定语言（如 `zh-CN`） |
| `--force` | 自动清理旧版文件，不询问 |

生成：
- `openspec/config.yaml` —— 项目上下文与规则（模板，Step 3 定制）
- `openspec/specs/`、`openspec/changes/` —— spec 与变更目录
- `.<tool>/skills/`、`.<tool>/commands/` —— 所选工具的技能与斜杠命令

> **注意**：如果项目此前声明过 `store:`（外部存储根），init 会拒绝脚手架；先删除 `config.yaml` 中的 `store:` 行再 init。

## Step 3 — 项目上下文定制（核心）

`openspec init` 生成的 `config.yaml` 是模板。官方文档明确：项目专属指导应写入 config 的 `context` 字段，init 永远不会覆盖你已写好的项目指导。Agent 应按以下流程定制：

### 3a — 分析项目结构

扫描根目录，识别：

1. **语言生态与框架** —— package.json / go.mod / pyproject.toml / Cargo.toml 等；框架从依赖或入口文件判断（Gin/FastAPI/Next.js/Spring…）
2. **目录结构** —— 实际布局（如 `cmd/ internal/ pkg/`、`src/`、`app/`），不要照搬模板示例
3. **既有约定** —— Makefile / Dockerfile / CI 配置 / .editorconfig / lint 配置中体现的规范

### 3b — 提炼项目规则

从上述信息中提炼会约束每个 spec/实现的具体规则，典型来源：

- 数据库迁移方式（是否必须附带迁移脚本）
- API 兼容性要求（向后兼容、版本化策略）
- 分层与提交规范（按层拆分 PR、测试先行等）
- 错误处理模式（返回 error、不 panic 等）

规则必须来自项目实际（配置文件、既有代码），不要凭空编造。

### 3c — 覆写 config.yaml

用 `write_file` **整体覆写** `openspec/config.yaml`——YAML 结构需要整体替换而非局部 patch。更新后的典型结构：

```yaml
project:
  name: "<项目目录名>"
  description: "<从 README 或 package.json 提取的一句话描述>"

context: |
  项目技术栈：Go 1.22 + Gin + PostgreSQL
  目录结构：<实际布局>
  编码约定：<从项目实际提炼，如错误处理统一返回 (data, error)>

rules:
  proposal:
    - <约束提案的规则，如"数据库变更需附带迁移脚本">
  tasks:
    - <约束任务拆分的规则，如"按 service / handler / model 分层提交">
```

> **区分两个"context"**：config.yaml 里的 `context:` 字段是注入到指令中的项目背景；`openspec context` 命令是查看工作集（根目录 + 引用的 store），两者无关。

### 3d — 语言与全局偏好（可选）

- 工件语言在 init 时用 `--language` 指定；事后调整可编辑 config。
- 全局设置（默认 profile、默认 store 等）用 `openspec config` 系列命令管理，与项目 config.yaml 分开。

## Step 4 — 验证

```bash
# config 已不是模板（context/rules 有实际内容）
cat openspec/config.yaml

# 目录已生成
ls .<tool-id>/skills/ .<tool-id>/commands/ 2>/dev/null || ls .<tool-id>/commands/

# CLI 可正常读取项目
openspec list --json
```

最后在所选 Agent 工具中实际调用一次斜杠命令（如 `/opsx:propose "test"`）确认端到端可用。

## ⚠️ 常见错误

- **init 前先 commit** —— `openspec init` 会重新生成文件，干净状态便于审查与回滚
- **不要手改工具目录下生成的 skill/command 文件** —— 属生成物，升级用 `openspec update` 处理
- **context 写空话没用** —— 写具体技术栈与可执行规则，OpenSpec 会原样注入每次指令

## 🔧 故障排查

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| npm 安装失败 | 网络或权限问题 | 切换 npm 镜像源，或以管理员权限重试 |
| `openspec --version` 找不到命令 | npm 全局 bin 不在 PATH | `export PATH="$PATH:$(npm prefix -g)/bin"`；检测并自动添加，而非让用户重置终端 |
| `--tools` 列表没有目标工具 | OpenSpec 版本过旧 | `npm update -g @fission-ai/openspec` 后重新查看 |
| init 提示已有 store 声明 | 项目曾配置外部存储根 | 删除 config.yaml 中的 `store:` 行后重跑 init |
| init 覆盖了已有改动 | init 会重新生成文件 | 提前 git commit；已被覆盖时用 `git diff` 找回 |
| 工具内看不到 opsx 命令 | 工具目录未生成或未刷新 | 重跑 `openspec init --tools <id>`；确认工具扫描对应目录 |

## 🔗 相关资源

- OpenSpec GitHub：https://github.com/Fission-AI/OpenSpec
- OpenSpec npm：https://www.npmjs.com/package/@fission-ai/openspec
- 支持工具清单：https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md
- 如需了解其他 SDD 工具（Spec-Kit、Superpowers、BMad 等）的选型对比，可参考社区调研 https://github.com/cameronsjo/spec-compare （本 skill 不覆盖选型，仅做 OpenSpec 初始化）
