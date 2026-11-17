# Iterate Skill

> [English](./README.md) · **简体中文**

> 一个可移植、可配置的 AI 编程助手技能：全自动多轮代码审查与修复。

<p align="center">
  <a href="https://github.com/jingzhao-l/iterate-skill/blob/main/badges/downloads.json">
    <img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjingzhao-l%2Fiterate-skill%2Fmain%2Fbadges%2Fdownloads.json&query=total&label=Total%20Downloads&style=for-the-badge&color=2ea44f&logo=download&logoColor=white" alt="Total Downloads">
  </a>
</p>

<p align="center">
  <a href="https://clawhub.ai/jingzhao-l/skills/iterate-skill"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjingzhao-l%2Fiterate-skill%2Fmain%2Fbadges%2Fdownloads.json&query=clawhub&label=ClawHub&color=4285F4&logo=cloudflare&logoColor=white" alt="ClawHub"></a>
  <a href="https://skillhub.cloud.tencent.com/"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjingzhao-l%2Fiterate-skill%2Fmain%2Fbadges%2Fdownloads.json&query=skillhub&label=SkillHub&color=624aff&logo=alibabacloud&logoColor=white" alt="SkillHub"></a>
  <a href="https://www.npmjs.com/package/iterate-skill-installer"><img src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjingzhao-l%2Fiterate-skill%2Fmain%2Fbadges%2Fdownloads.json&query=npm&label=npm&color=CB3837&logo=npm&logoColor=white" alt="npm"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow" alt="License"></a>
  <a href="https://github.com/jingzhao-l/iterate-skill/releases"><img src="https://img.shields.io/github/v/release/jingzhao-l/iterate-skill" alt="GitHub release"></a>
  <a href="https://github.com/jingzhao-l/iterate-skill"><img src="https://img.shields.io/github/stars/jingzhao-l/iterate-skill?style=social&label=Star" alt="GitHub stars"></a>
</p>

> ⭐ 如果这个项目对你有帮助，欢迎点亮 GitHub Star，让 iterate 被更多开发者看见。你的支持就是持续开源迭代最大的动力！

---

## 目录 / Table of Contents

- [这是什么 / About This Project](#这是什么--about-this-project)
- [30 秒了解 / At a Glance](#30-秒了解--at-a-glance)
- [3 分钟上手 / Quick Start](#3-分钟上手--quick-start)
- [安装 / Installation](#安装--installation)
- [使用 / Usage](#使用--usage)
- [CLI 命令参考 / CLI Command Reference](#cli-命令参考--cli-command-reference)
- [它如何工作 / How It Works](#它如何工作--how-it-works)
- [配置参考 / Configuration](#配置参考--configuration)
- [常见问题 / FAQ](#常见问题--faq)
- [安全说明 / Security](#安全说明--security)
- [目录结构 / Directory Structure](#目录结构--directory-structure)
- [贡献 / Contributing](#贡献--contributing)
- [免责声明 / Disclaimer](#免责声明--disclaimer)
- [许可证 / License](#许可证--license)

---

## 这是什么 / About This Project

**iterate** 是一个让 AI 编程助手具备**多轮自主代码审查与修复**能力的开源项目。你无需从任何"iterate"概念开始——它解决的是一个很具体的痛点：

> AI 助手往往"说得多、做得浅"：一次对话只改几行、看过一个文件就不再管全局，也很少回头复核自己改坏的东西。`/iterate` 把这些琐碎但关键的收尾工作——逐项审查、分维度排查、修复、验证、再迭代——自动化，让 AI 真正像一位资深工程师一样把改动**做完、做对**。

它的运行机制可以概括为一条自闭合流水线：

```text
定目标 → 多维度并行审查 → 原子修复 + 架构修复（需你批准）→ 验证 → 再审查 → 循环直到收敛 / 达轮数上限 → 输出总结
```

技能本身也随大版本持续演进：

- **v2** — 确定性收敛：反复多维度审查直到某一轮零新问题，配合隔离的 `iterate/*` 分支与决策日志。
- **v3.0** — 双模式：原 `/iterate` 审查/修复闭环保持不变，新增**防御式编程模式**（`/iterate defensive`）覆盖日常增量编码任务（新增功能、修 bug、重构），以确定性的 `iterate guard` 动手前/后校验与 `invariant` 交付门禁加固。
- **v3.1** — 新增 `iterate fingerprint` 非阻塞式 manifest 漂移校验、更聪明的 `iterate doctor`（汇总显示通过了几项检查）、guard 语义 fail-closed。

**iterate 不是一个独立的工具，而是一套附着在现有 AI 助手之上的技能生态。** 它不会替换你的 IDE 或 AI 工具，而是在你已有的工作流里，加一层"严格的代码把关"。整个生态由三个组件构成，共用同一套配置与审查维度：

- **Core Skill + CLI** — 可移植 AI 技能 `/iterate` + `iterate` 命令行（本仓库根目录）。在 Trae / Claude Code / Cursor / Copilot / Codex 等 25+ 助手的对话式界面里多轮迭代。
- **[iterate-harness](https://github.com/jingzhao-l/iterate-harness)** — 独立无头引擎，命令 `ih`（源码 `harness/iterate-harness`，npm: `iterate-harness`）。在终端 / CI / Git 钩子里，脱离对话式助手运行同一套闭环。
- **[iterate-plugin](https://github.com/jingzhao-l/iterate-plugin)** — dsh 桌面客户端插件（源码 `harness/iterate-plugin`，npm: `iterate-plugin`）。使用 dsh 桌面客户端，把 iterate 的收敛仪表盘、review 进度带进界面。

三者的关系：**skill**（本仓库核心交付物）面向任意 AI 助手的对话式迭代；**harness** 面向无头 / CI 场景的同一闭环引擎实现；**plugin** 把 harness 的运行时体验接入 dsh。配置（`iterate.config.yaml`）与维度体系在三者间完全一致——理解其一即可举一反三。

**相关项目：[GlassPane](https://github.com/jingzhao-l/GlassPane)。** [`kernel/`](kernel) 里的 JSON Schema 契约层（`iterate-kernel`）同时也是 GlassPane 所讲的方言——它是 macOS 上面向 AI 代理的运行时验证引擎：代理经 MCP 动手，GlassPane 返回"界面到底变了没有"的证据（无障碍树与像素差异、归因结论、可回滚检查点）。iterate 回答"这段代码对不对"，GlassPane 回答"那次操作真的生效了吗"。它刻意保持独立：不读 `iterate.config.yaml`，也走自己的发布线。

独立不等于不往来：2026-10-25 起两边交换的是**可核验的记录**——GlassPane 的证据账本与审查回路的
决定日志是同一种哈希链格式，从对方那本引来的主张要先整链验通才被使用。这个读者今天长在回路这一侧：
fork 带着同一个校验器，也有一条固定点测试证明这边写出的链在那边验得过，但它自己的生产路径只写自己的
账本、不读回路的。`dimension` 声明跟着验证调用走，与已有见证矛盾的决定会被拒；回路把"修复完成了"
钉在一条链可验的账本行上，而不是代理的自述。命令是
`ih iterate gate` / `ih iterate glasspane-ledger <路径>`（session 里是 `/iterate` 那两条同名子命令），
整套交换的细节写在[那份 harness 的 README](https://github.com/jingzhao-l/iterate-harness#-glasspane-integration)。

其中，harness 与 plugin 也可脱离本仓库独立安装使用：

```bash
# iterate-harness：一键安装（npm 包装器，最简）
npm install -g iterate-harness

# 或脚本安装（oh / ohmo 已全面迁移为 ih）。harness 仓库也提供 shell 安装器：
# 请固定 release tag 并校验 checksum，不要把 main 分支直接管道进 shell：
#   https://github.com/jingzhao-l/iterate-harness/releases
ih iterate init && ih iterate review

# iterate-plugin：dsh 桌面插件的 GitHub 安装
dsh plugin --profile web add github:jingzhao-l/iterate-plugin#main
```

> harness 内置 OrcaRouter 网关 provider（含免费模型档），通过 [推广链接注册](https://www.orcarouter.ai/ref/ref_5eca75a9c809c95ab152) 即完成项目支持，配置引导见 [iterate-harness README](https://github.com/jingzhao-l/iterate-harness)。

> 本文档接下来以 **skill（本仓库根目录）** 为核心，讲解最常用的对话式用法。harness 与 plugin 的详细文档见它们各自的独立仓库：[iterate-harness](https://github.com/jingzhao-l/iterate-harness)（源码 `harness/iterate-harness/README.md`）、[iterate-plugin](https://github.com/jingzhao-l/iterate-plugin)（源码 `harness/iterate-plugin/README.md`）。

---

## 30 秒了解 / At a Glance

**Iterate Skill** 让 AI 助手像一位严谨的资深工程师一样，对代码库进行多轮审查与修复。

- **双模式** — `/iterate`：原模式，多轮审查 → 修复 → 收敛闭环（v2 行为，零破坏）；`/iterate defensive`：防御式编程模式，面向正常增量式编程任务，最终以同一套 iterate 收敛门禁收尾。
- **9 维度并行审查** — correctness、security、performance、architecture、style-tests、tech-debt、spec-compliance、frontend-backend、ui-ux。
- **按范围维度集** — onboarding 时预置命名 `dimension_sets`（如 `frontend`、`api`、`security`）；指定范围的 goal 会路由到对应维度集，未命中的偏门范围触发 on-the-fly 重定义并记录到 `.iterate_decisions.md`（禁止照抄预设）。
- **双轨修复** — 原子问题（≤20 行、单文件）自动修；架构问题经你批准后再修。
- **确定性门禁 CLI** — `iterate guard pre-check` / `post-check` + `iterate invariant`：宿主 AI 在动手前后与交付时执行的精确、响亮失败校验（防御式模式）。
- **Git 隔离** — 每轮在独立 `iterate/*` 分支或 worktree 中完成；merge/push 默认关闭，需显式开启。
- **Secure-by-default** — `push_per_round` 和 `auto_merge` 默认均为 `false`。
- **命令白名单** — 配置时 + 个性化时双层校验，拒绝危险 shell 元字符。
- **校验和验证** — 从 GitHub Release 更新时强制 SHA256 校验。
- **多助手支持** — Trae、Claude Code、Cursor、Windsurf、GitHub Copilot、Codex、Roo Code 等 25+ 工具。
- **项目知识库** — 自动生成 `ITERATE.md` + `iterate.config.yaml`，支持漂移检测和增量刷新。

---

## 3 分钟上手 / Quick Start

### 1. 安装技能

```bash
npx iterate-skill-installer
```

运行后会自动检测你已安装的 AI 编程工具，交互选择要安装到哪些助手。支持 `--ai <name>` 直接指定单个助手。安装器还会自动安装 `iterate` CLI（用于下面第 2 步的 `iterate onboard` 等命令），一条命令即可完成 skill + CLI 的安装。

### 2. 进入项目并完成 onboarding

```bash
cd /path/to/your-project
iterate onboard
```

`iterate onboard` 会生成本项目的知识库：

- `ITERATE.md`：技术栈、模块地图、约定、禁区等
- `iterate.config.yaml`：迭代目标、审查维度、验证命令等

### 3. 开始迭代

在 AI 助手对话中输入：

```text
/iterate "提升代码质量，确保所有函数 ≤80 行且测试通过"
```

或在终端里直接启动 CLI：

```bash
iterate status      # 查看 onboarding 状态和漂移
iterate refresh     # 增量刷新 ITERATE.md
iterate personalize # 追加项目专属约束
```

---

## 安装 / Installation

### 推荐：npx 一键安装（适合绝大多数用户）

无需克隆仓库，无需手动配置 Python 环境，一条命令完成 skill 下载、校验、安装，并自动安装 `iterate` CLI：

```bash
# 自动检测已安装的 AI 助手并交互选择
npx iterate-skill-installer

# 仅安装到 Trae
npx iterate-skill-installer --ai trae

# 安装到指定项目目录
npx iterate-skill-installer --target /path/to/project

# 强制覆盖已安装的技能
npx iterate-skill-installer --ai trae --global --force
```

常用选项：

- `--ai <name>` — 仅安装到指定助手，如 `trae`、`claude`、`cursor`
- `--target <path>` — 项目级安装到指定目录
- `--global` — 安装到用户主目录（默认）
- `--force` — 覆盖已存在的 skill 文件
- `--token <token>` — GitHub token，用于提高 API 速率限制
- `-h, --help` / `-v, --version` — 查看帮助 / 版本

> **安装器会安装 `iterate` CLI 到你的 PATH**（优先 `pipx` 隔离安装，否则 `pip install --user`）。这是为了让 `npx iterate-skill-installer` 一条命令完成 "skill + CLI"，但安装器确实会在你的系统上放置一个可执行文件。若不希望自动安装 CLI，可改用下方的"手动复制 SKILL.md"或"源码脚本"方式。
>
> 安装器需要 Node.js 18+ 和 Python 3.10+。它会自动创建隔离的 Python 虚拟环境、安装依赖、调用 `scripts/install.py` 完成文件复制。下载 release 时强制校验 `SHA256SUMS.txt`，校验失败则拒绝安装。若 `iterate` 命令安装失败，仍可手动执行 `pipx install .` 或 `pip install .` 补装。

### 其他安装方式

如果你无法使用 npm，或者希望完全控制安装过程，可选用以下方式。

#### 方式 A：本地安装 iterate CLI

通过 npx 一键安装时已自动安装 `iterate` CLI。若你未使用 npx，或希望手动/升级安装 CLI，可在此手动安装：

```bash
git clone https://github.com/jingzhao-l/iterate-skill.git
cd iterate-skill

# 推荐用 pipx 隔离安装
pipx install .

# 或直接用 pip
pip install .

# 验证
iterate --version
```

安装后可在任意项目目录使用 `iterate onboard`、`iterate personalize`、`iterate status`、`iterate refresh`、`iterate reonboard`。

#### 方式 B：手动复制 skill 目录

> ⚠️ **必须复制整个 `iterate/` 目录，而不是只复制 `SKILL.md`。** `SKILL.md` 运行时依赖同目录下的 `config/`、`scripts/validate.py`、`templates/`（按安装目录相对路径解析）。只拷一个文件会导致 `/iterate` 找不到配置与校验脚本而失败。

如果你不想用 npx 安装器，把整个 skill 目录复制到对应助手目录即可：

```bash
# 先在本地克隆或下载源码，得到含 SKILL.md、config/、scripts/、templates/ 的 iterate/ 目录
git clone https://github.com/jingzhao-l/iterate-skill.git
SKILL_DIR=$(pwd)/iterate-skill

# Trae
mkdir -p ~/.trae/skills/iterate
cp -R "$SKILL_DIR"/SKILL.md "$SKILL_DIR"/config "$SKILL_DIR"/scripts "$SKILL_DIR"/templates ~/.trae/skills/iterate/

# Claude Code
mkdir -p ~/.claude/skills/iterate
cp -R "$SKILL_DIR"/SKILL.md "$SKILL_DIR"/config "$SKILL_DIR"/scripts "$SKILL_DIR"/templates ~/.claude/skills/iterate/

# Cursor
mkdir -p ~/.cursor/skills/iterate
cp -R "$SKILL_DIR"/SKILL.md "$SKILL_DIR"/config "$SKILL_DIR"/scripts "$SKILL_DIR"/templates ~/.cursor/skills/iterate/
```

更多工具的路径请参考 [`SKILL.md`](./SKILL.md) 中的"工具映射表"。

#### 方式 C：源码脚本（开发者）

```bash
git clone https://github.com/jingzhao-l/iterate-skill.git
cd iterate-skill

python scripts/install.py install --ai trae --global
python scripts/install.py update --ai trae --target /path/to/project
python scripts/install.py uninstall --ai trae --target /path/to/project --yes
```

### 全局安装 vs 项目级安装

- **全局安装**（`~/.trae/skills/iterate/`）— 所有项目首次调用 `/iterate` 都会触发 onboarding。
- **项目级安装**（`/project/.trae/skills/iterate/`）— onboarding 完成后直接复用项目根目录的 `ITERATE.md`，无需重复 onboarding。

建议：先在全局安装一次，让助手认识你；再在重要项目里做一次项目级安装，避免重复 onboarding。

### 为什么不推荐 skills.sh 安装？

本项目早期曾在 skills.sh / SkillHub 等平台分发。从 v2.1 起，**推荐统一使用 `npx iterate-skill-installer`**，原因如下：

1. **一条命令完成**：自动下载、SHA256 校验、环境准备、助手选择，无需手动克隆或复制文件。
2. **版本一致**：始终从 GitHub Release 安装，避免平台缓存导致的版本错乱。
3. **跨助手统一**：同一份安装逻辑支持 25+ AI 助手，而不是每个平台各自维护。
4. **安全可验证**：强制校验 SHA256SUMS.txt，校验失败则拒绝安装。

skills.sh 等市场页面仍会保留，用于展示和发现，但不再作为首选安装入口。

---

## 使用 / Usage

### 在 AI 助手中

安装 skill 后，在支持该技能的 AI 工具中输入：

```text
/iterate "你的目标"
/iterate "你的目标" 10
/iterate "你的目标" no-limit
/iterate "审查代码质量" review-only    # 纯审查模式：反复审查到零 findings，只读不改代码
/iterate "full health check" --dry-run # 纯审查别名：出审查报告 + meta-review 最终审查报告
/iterate defensive "新增用户登录 + 修复支付 bug"   # 防御式编程模式（v3.0）：从设计到交付全程防御式纪律
```

首次调用会自动触发 onboarding（如果项目还没有 `ITERATE.md`）。

> **防御式编程模式（`/iterate defensive`）**：当你想让 AI 做**正常的增量式编程任务**——新增功能、修 bug、重构、接入 API、补测试——而不是纯审查时，用 `/iterate defensive`。宿主 AI 从动手前到收尾**从头至尾贯彻防御式编程理念**：动手前声明假设并跑 `iterate guard pre-check` 确认、动手时最小步进 + 信任边界验证、每次改动后跑 `iterate guard post-check`，收尾时用 `iterate invariant` + 完整 9 维度审查→修复→收敛闭环作为**交付门禁**——不收敛不交付。原模式（`/iterate`，v2）行为完全不变。

> **纯审查模式 / review-only（dry-run）**：调用参数含 `review-only` 或 `dry-run` 时，本 skill 只做只读健康检查，**绝不修改任何文件**。它会反复并行审查直到某一轮 0 个新 findings（收敛），生成审查报告；随后**再审查这份报告本身**（meta-review，校验报告内部一致性），给出带 `approved` / `needs_revision` 判定的最终审查报告。适用于发布前体检、代码质量审计、不想让 AI 动代码的场景。

### 在终端中

```bash
# 交互式 onboarding（首次/非首次会自动分支）
iterate onboard

# 中途追加/查看/清空个性化约束
iterate personalize          # 进入 9 步个性化向导
iterate personalize --clear  # 清空所有个性化（结构化规则 + ITERATE.md 相关段落）
iterate personalize --clear --yes  # 跳过确认，直接清空
iterate show                 # 只读查看合并后的配置与个性化详情（--json 输出结构数据）

# 引导式「下一步」：现在该跑哪条命令、为什么（只读，恒 exit 0）
iterate next                 # 空项目→init/onboard；漂移→refresh --diff；体检失败→doctor --fix；健康→/iterate "<goal>"
iterate next --json          # 脚本/CI 用的稳定计划：state、blocking、drift、next、steps、notes

# 查看 onboarding 状态和漂移检测
iterate status

# 增量刷新（保留 ITERATE.md 用户手写区）
iterate refresh

# 完整重新 onboarding（备份旧文件）
iterate reonboard

# 校验 manifest 指纹与当前项目状态是否一致（非阻塞漂移检查）
iterate fingerprint           # verify（默认）：退出码 0 = 无漂移，1 = 新增/移除/变更了 manifest
iterate fingerprint --json    # 结构化 JSON 输出（脚本友好）

# 一份可直接贴 PR / 存 CI artifact 的健康报告
iterate report                # 默认 Markdown：技术栈 + 生效配置 + doctor 全项 + 漂移 + 下一步
iterate report --out report.md   # 原子写入文件（stdout 保持为空）
iterate report --json         # 单个结构化 JSON 文档
iterate report --strict       # warning 也判失败（退出码 1），适合 CI 门禁

# Shell 补全（命令 / 参数 / 固定取值 / 路径）
iterate completion bash
iterate completion bash --install      # 写入常规用户补全目录
iterate completion zsh --install       # ~/.zfunc 或 ~/.oh-my-zsh/completions
iterate completion fish --install      # ~/.config/fish/completions/iterate.fish
iterate completion bash --install --dir ./completions --force  # 指定目录

# 非交互式配置查看与修改（不走向导）
iterate config                      # 列出全部可设值
iterate config get max_rounds      # 读单个解析值（--json 输出 {"key": value}）
iterate config set goal "..."      # 校验并写回单个值（写前自动生成时间戳备份）

# 防御式编程确定性校验（v3.0 防御式模式）
iterate guard pre-check src/        # 动手前：目标存在 / worktree 干净 / manifest 就绪
iterate guard post-check python     # 每次改动后：精确执行 validation.commands.<module>
iterate invariant                   # 交付时：文件断言 + 精确命令（缺省退化为 validation.commands）

# 列出 / 恢复 / 清理写命令留下的时间戳备份
iterate backup list                 # 枚举 *.configset-* / *.doctorfix-* / *.refresh-* / *.bak-* 等
iterate backup restore <file>       # 恢复某个备份（先备份当前文件；可逆）
iterate backup prune --keep 5       # 每个原文件保留最新 5 份备份，删除其余
iterate backup prune --older-than 30d  # 删除超过 30 天的备份（也接受 7d/24h/90m）
```

### 常见边界场景 / Edge Cases

- **onboarding 中途取消（Ctrl+C / 选择"跳过"）**：不会留下半成品。所有文件均以**原子写入**（临时文件 + `os.replace`）落盘，取消时未写入任何内容，下次直接重跑即可。
- **手写 `ITERATE.md` 缺少 `USER-OWNED` 标记**：`iterate refresh`（以及 AI 刷新）会**拒绝覆盖并报错**，而不是销毁你的手写内容。补齐 `<!-- ITERATE:USER-OWNED:START/END -->` 标记后即可正常刷新。
- **非 Git 项目**：`onboard` / `status` / `refresh` / `doctor` / `personalize` 等 CLI 命令不依赖 git，可直接使用；但 `/iterate` 迭代流程中的 Git 隔离分支、合并、推送等步骤需要 git 仓库，缺省时这些步骤会被跳过或提示。
- **空项目 / 无 manifest 文件**：onboarding 正常生成知识库；由于没有 `package.json` / `pyproject.toml` 等指纹文件，漂移检测会跳过指纹比对。
- **`iterate.config.yaml` 损坏（YAML 语法错误 / 不符合 schema）**：`iterate doctor` 会报告 schema 错误；`doctor --fix` 只修可安全自动修复项，其余需手工修正。`/iterate` 调用时若配置无法通过 schema 校验会立即中止并报错，不会带病运行。
- **多轮收敛提前终止**：某一轮并行审查返回 0 个新 findings 时，迭代提前结束（Early Stop），不会空转到 `max_rounds`。

### 新手推荐路径 / New-User Path

```text
1. 安装        npx iterate-skill-installer      # 自动装 skill + iterate CLI
2. 初始化      iterate onboard                  # 生成 ITERATE.md + iterate.config.yaml
3. 体检        iterate doctor                    # 确认配置健康（可选，但推荐）
4. 补充约束    iterate personalize              # 项目专属约束（可选）
5. 开始迭代    /iterate "你的目标"               # 或在 AI 助手中直接调用
```

> 不确定当前在哪一步？直接跑 **`iterate next`**：它读取项目状态，只给出「下一条该跑的命令」以及原因、后续步骤和环境缺口（例如未初始化 git），无需先读文档；`iterate next --json` 返回同一份计划供脚本/其它 skill 消费。

首次调用 `/iterate` 时若项目还没有知识库，skill 会**先做 onboarding** 再进入迭代——看到"正在初始化项目"的提示是正常流程，不是失效。之后每轮改动都保留在隔离的 `iterate/*` 分支/worktree 中，merge/push 默认关闭，由你 review 后再合并。

---

## CLI 命令参考 / CLI Command Reference

### iterate doctor（项目健康诊断）

`iterate doctor` 会对照 skill 自身的规范定义检查你的项目，尽早发现与预期漂移的地方。它逐项校验：

- **Onboarding 完整性** — `ITERATE.md` 与 `iterate.config.yaml` 是否存在
- **配置可解析且合法** — config 能被解析为 YAML，且**完整**匹配 `config/config.schema.json`
- **维度合法** — `dimensions` 只引用 9 个规范维度之一
- **审查范围合法** — `review.scope` 只允许 `full` / `changed-only`
- **合并目标分支** — `git.target_branch` 为非空字符串
- **验证命令** — `validation.commands` 是非空字符串列表
- **命令白名单** — `command_whitelist` 条目安全，且每条命令都在白名单内
- **个性化维度引用** — `personalization` 的维度引用指向已启用的维度
- **版本一致** — onboarding 时的 `skill_version` 与当前安装的 skill 版本一致
- **漂移检测** — 自 onboarding 以来技术栈 manifest 是否变化

```bash
iterate doctor            # TUI 输出；健康退出码 0，发现问题退出码 1
iterate doctor --json     # 结构化 JSON 报告输出到 stdout（脚本友好）
iterate doctor --json-out report.json   # 把 JSON 报告写入文件（自动建目录）
iterate doctor --fix      # 先应用安全、非破坏性修复（自动写时间戳备份），再重跑诊断
iterate doctor --list-checks            # 列出全部可用检查名后退出
iterate doctor --check config.schema    # 只运行指定检查（可重复 / 逗号分隔）
```

`--fix` 只做可安全自动修复的项，且每次修复前都会为 `iterate.config.yaml` 生成带时间戳的备份（`.doctorfix-<时间戳>` 后缀）；破坏性/有歧义的修复不会自动执行，会在报告中提示你手工处理。目前可自动修复的项包括：`dimensions` 去重/空时恢复默认、`language` 非法值重置为 `en`、`max_rounds` 非整数移除/越界收敛到 `[1, 50]`、`git.target_branch` 空值重置为 `main`、`onboarding.skill_version` 同步为当前安装版本。

### iterate scan（只读导出项目扫描结果）

`iterate scan` 展示项目扫描器识别到的内容——与 onboarding 内部使用的是同一套检测，但无需走完交互向导即可查看。它**只读文件/目录是否存在**（manifest、顶层目录名、特性目录），**绝不写入任何文件**，因此可安全地在任意项目与 CI 中运行。它**恒退出 0**：完全没识别出技术栈是正常结果，不是失败。

```bash
iterate scan         # TUI 报告
iterate scan --json  # stdout 输出单个 JSON 文档
```

报告包含识别到的 `manifests`、`detected_languages`、`detected_package_managers` 与 `top_level_dirs`，五个特性开关（`has_specs` / `has_tests` / `has_ci` / `has_frontend` / `has_api`），以及由它们推导出的建议：`suggested_dimensions`、`suggested_dimension_sets`（可直接用于 `dimension_sets` 的具名范围蓝图）、`suggested_validation_commands`（可直接用作 `validation.commands` 的形状）与 `suggested_command_whitelist`（用于 `validation.whitelist`）。`has_api` 除顶层目录外，也识别常见的嵌套布局（`src/api`、`app/routes`、`src/controllers` 等）。

```json
{
  "project": "/path/to/project",
  "manifests": ["pyproject.toml"],
  "detected_languages": ["Python"],
  "detected_package_managers": ["pip/poetry"],
  "top_level_dirs": ["iterate_cli", "scripts", "tests"],
  "has_specs": false, "has_tests": true, "has_ci": true, "has_frontend": false,
  "has_api": false,
  "suggested_dimensions": ["correctness", "security", "..."],
  "suggested_dimension_sets": {"backend": {"dimensions": ["..."]}},
  "suggested_validation_commands": {"python": ["ruff check .", "mypy . --ignore-missing-imports", "pytest tests -x -q"]},
  "suggested_command_whitelist": ["python", "python3", "ruff", "mypy", "pytest"]
}
```

用 `iterate init`（一条命令、无提问）、`iterate onboard`（交互式）或 `iterate config set <key> <value>` 落地这些建议。

### iterate init（无提问初始化）

`iterate onboard` 是交互式的：CI、脚本和其它 skill 无法驱动它（会卡在第一个提问上）。`iterate init` 复用同一套扫描器与生成器，**全程不提问**，一条命令完成初始化：

```bash
iterate init --yes                  # 写入 ITERATE.md + iterate.config.yaml
iterate init --dry-run --json       # 只预览识别到的技术栈与将写入的配置，不落盘
iterate init --yes --json           # 输出单个 JSON 文档，供脚本/agent 消费
iterate init --yes --language zh --target-branch develop --goal "加固 API"
```

生成的配置使用扫描器建议的维度、维度集（裁剪到已启用维度）、校验命令与命令白名单，与向导产物同构：`iterate doctor` 直接通过，`iterate show` / `iterate refresh` 立即可用。

安全语义：

- **幂等**：`iterate.config.yaml` 已存在时不改动任何文件，报告「已初始化」并退出 `0`；要调整已配置项目请用 `onboard` / `refresh`。
- **不覆盖手写内容**：已有 `ITERATE.md` 只有在带 USER-OWNED 标记时才重写，且保留该区内容；否则拒绝并提示改用 `reonboard`（先备份）。
- **非交互契约**：stdin 非终端时必须加 `--yes`（否则退出 `2`）；`--json` 时 stdout 恰好一个 JSON 文档。

### iterate export / import（可移植的项目状态）

`iterate export` 把项目的 iterate 状态——`iterate.config.yaml` 与 `ITERATE.md`——快照为一个带格式版本的 JSON bundle。项目本身不会被修改，只写出 bundle 文件。适合备份、把调好的配置迁移到另一台机器、随 review 附带精确状态，或在另一个仓库复用同一套 profile。

```bash
iterate export                       # 在项目根目录写出 iterate-bundle-<UTC>.json
iterate export --out state.json      # 指定路径（默认拒绝覆盖，需 --force）
iterate export --json > state.json   # 把 bundle 打到 stdout，不写文件
```

`iterate import` 会**先**校验 bundle（配置还要通过 JSON schema），再生成带时间戳的备份（`.import-<UTC>-<salt>`），最后才写回 `iterate.config.yaml` / `ITERATE.md`：

```bash
iterate import state.json --dry-run   # 预览新增 / 变更 / 删除的键
iterate import state.json --yes       # 直接应用（stdin 非终端时必需）
cat state.json | iterate import - --yes
iterate import state.json --yes --reset-fingerprints  # bundle 来自另一个仓库
```

`--reset-fingerprints` 会丢弃导出项目记录的 manifest 指纹，避免导入后立刻把原项目的 manifest 报成漂移；`iterate refresh` 会为当前仓库重新采集。非法或外来 bundle 退出码为 `1`，项目保持原样；带 `--json` 时 stdout 仍是恰好一个 JSON 文档。用法错误（例如同时给 `--json` 与 `--out`）退出码为 `2`。

### iterate fingerprint（校验 manifest 指纹 / 漂移）

`iterate fingerprint`（默认动作 `verify`）将 onboarding / refresh 时记录的 manifest SHA-256 指纹与当前项目根目录比对，检测技术栈清单的新增 / 移除 / 变更——属于**非阻塞**的信息化健康检查。无漂移（或漂移检查不可用）时退出码 0，检测到漂移时退出码 1，适合接入 CI：

```bash
iterate fingerprint         # verify（默认）：TUI 输出
iterate fingerprint --json  # 结构化 JSON：{"project": ..., "available": bool, "drift": bool, ...}
```

指纹由 `iterate onboard` / `iterate refresh` / `iterate reonboard`（重新）采集；同一套检查也会静默运行在 `iterate status` 及每次 `/iterate` 调用的漂移提示路径中。

### iterate show（只读查看合并配置与个性化）

`iterate show` 只读展示项目当前生效的合并后状态，适合快速核对配置与约束，**不会写任何文件**：

```bash
iterate show        # TUI 输出：onboarding 元数据 + 生效配置 + 个性化详情 + 漂移状态
iterate show --json # 结构化 JSON 输出到 stdout（供脚本 / CI / 快速 diff）
```

当你只想确认当前个性化里配了什么（禁区、风险区、已知意图、维度定制、修复顺序、注意点、代码约定、额外验证命令），或核对合并后的 `validation.commands` / 白名单时，用 `iterate show` 比直接翻 `iterate.config.yaml` + `ITERATE.md` 更直观。

### iterate personalize --clear（清空个性化）

需要清掉此前配置的个性化约束时，可在确认后一次性清空（结构化规则从 `iterate.config.yaml` 移除、关联的额外验证命令从 `validation.commands` 清理、`ITERATE.md` 用户区中的个性化段落移除，同时保留你手写的内容）：

```bash
iterate personalize --clear       # 带确认提示
iterate personalize --clear --yes # 跳过确认直接清空
```

若当前没有任何个性化内容，会提示"无个性化可清空"并正常退出（退出码 0）。

### iterate config（非交互式配置 get/set）

`iterate config` 让你无需打开交互向导即可查看或修改配置值，适合脚本 / CI / 快速编辑：

```bash
iterate config                 # TUI：列出每个可设键及其当前值
iterate config --json          # 输出全部可设值的 JSON 对象（stdout 保持纯净，供脚本消费）
iterate config get max_rounds  # 打印单个解析值；--json -> {"max_rounds": ...}
iterate config set language zh # 校验并写回单个值（写入前自动生成时间戳备份）
iterate config set goal "..."  # 成功时输出确认对象 {"key": ..., "value": ...}
iterate config schema          # 输出 iterate.config.yaml 的规范 JSON Schema（供编辑器 / CI / 工具链）
iterate config schema --out schema.json --force  # 写入文件（yaml-language-server / CI）
```

支持扁平键（`goal`、`max_rounds`、`reasoning_effort`、`language`、`mode`、`dimensions`）以及每个嵌套键的点分形式（`atomic.max_lines`、`atomic.max_adjacent_methods`、`git.target_branch`、`git.use_worktree`、`git.push_per_round`、`git.auto_merge`、`review.scope`、`reviewer.output_schema_validation`、`reviewer.evidence_validation`、`reviewer.coverage_validation`、`reviewer.scope_chunk_size`）。`validation.commands` / `command_whitelist` 与 `invariants.*` **不支持**在此设置——请在 `iterate.config.yaml` 中编辑（或由 `iterate onboard` 写入），并用 `python scripts/validate.py config` 重新校验。损坏配置**不会被覆写**——`set` 会中止并报清晰错误。

`iterate config schema` 把规范 JSON Schema（`doctor` 与 `scripts/validate.py` 校验所依据的同一份文档）以纯 JSON 输出到 stdout，这样编辑器（yaml-language-server 的 `yaml.schemas`）、CI 校验器或其它工具就能与 CLI 强制同一套配置契约。`--out PATH` 写入文件（默认拒绝覆盖已存在、`--force` 覆盖；确认信息走 stderr 保持 stdout 纯净），`--compact` 输出单行 JSON，且不需要存在 `iterate.config.yaml`（schema 描述的是 CLI 配置契约而非某个项目）。

### iterate guard（防御式模式动手前/后校验，v3.0）

宿主 AI 在防御式模式下围绕每个编码步骤执行的确定性、响亮失败校验。契约：退出码 0 = 可以开工 / 本次改动安全；1 = 必须先修复或回滚。

- `iterate guard pre-check [paths...]` — **动手前**执行：目标存在、git worktree 干净、manifest 就绪、验证配置安全（`PASS`/`FAIL`）。
- `iterate guard post-check [module...]` — **每次改动后**执行：精确执行配置的 `validation.commands.<module>`（运行时唯一权威白名单——不拼装、不加前缀）。

两者都支持 `--json` 与 `--dry-run`（仅预览将要执行的精确命令，不真正执行）。

### iterate invariant（防御式模式交付门禁，v3.0）

`iterate invariant` 校验配置中声明的项目级 `invariants`（`invariants.ensure` 文件存在断言 + `invariants.commands` 精确按模块命令列表）。未配置 `invariants` 段时**自动退化为执行 `validation.commands`**，因此旧配置无需任何改动。退出码 0 = 不变量成立，1 = 存在违反项。支持 `--json` / `--dry-run`。

### iterate help（帮助与拼写容错）

`iterate help` 打印命令总览，`iterate help <command>` 打印单个命令的详细帮助——不必记住 `--help` 该放在哪：

```bash
iterate help          # 等价 `iterate --help`
iterate help doctor   # doctor 的帮助文本
```

命令拼错时会直接给出最接近的真实命令，而不是只丢一堵 usage 墙：

```text
$ iterate statu
iterate: error: argument command: invalid choice: 'statu' (choose from onboard, …, help)
did you mean 'status'? Run `iterate help` to list every command.
```

子命令动作同样适用（`iterate fingerprint verfy` → `did you mean 'verify'?`）。用法错误退出码仍为 2；带 `--json` 时 stdout 仍是恰好一个 JSON 文档，建议放在 `did_you_mean` 字段：

```bash
iterate statu --json
# {"error": "invalid usage", "hint": "run `iterate --help`", "did_you_mean": "status"}
```

若没有足够接近的候选就不猜（错误的建议比没有更糟），原始诊断信息保持原样。

### iterate report（一份可直接分享的项目报告）

`status` / `scan` / `doctor` 各自回答一个问题；`iterate report` 把它们聚合成一份只读文档，可直接贴进 PR、issue 或作为 CI artifact 上传：

```bash
iterate report                  # 默认输出 GitHub Markdown
iterate report --out report.md  # 原子写入文件（stdout 保持为空）
iterate report --out report.md --force  # 覆盖已存在的报告文件
iterate report --json           # 单个结构化 JSON 文档
iterate report --strict         # warning 也判失败（退出码 1），同 doctor --strict
```

Markdown 包含技术栈、生效的审查配置（目标分支、范围、维度、维度集、校验命令/白名单、个性化规则数）、doctor 全项检查表、漂移与建议、以及可直接执行的下一步命令。单元格中的 `|`、换行、反引号与 HTML 标记会转义，粘贴后表格不会散，也不会被项目内容注入裸 HTML。`--out` 默认拒绝覆盖已存在文件（以及 iterate 自己的状态文件），需显式 `--force`，避免误删你的笔记。健康时退出码 0，阻塞时 1（错误；`--strict` 下还包括警告），可直接作为 CI 门禁。

### iterate completion（Shell Tab 补全）

补全脚本与 `--help` 由同一个 argparse parser 生成，命令/参数永远不会与文档漂移：

```bash
iterate completion bash                # 打印脚本
iterate completion zsh > "${fpath[1]}/_iterate"
iterate completion fish > ~/.config/fish/completions/iterate.fish
iterate completion bash --uninstall    # 删除已安装文件（幂等）
source <(iterate completion bash)      # 或直接 source
```

补全命令、各命令参数（隐藏参数不会出现）、固定取值（如 `init --language zh|en`）、`-p/--project` 目录、`import`/`--out` 文件路径，以及 `iterate help <command>` 的命令名。加 `--install` 会按 shell 惯例写入用户补全目录（遵循 `XDG_DATA_HOME` / `XDG_CONFIG_HOME`），自动创建父目录；已有文件默认拒绝覆盖，需 `--force`；`--json` 输出单个 `{shell, path, bytes, reload_hint}` 结果文档。加 `--uninstall` 只删除安装时写入的那一个文件（绝不触碰任意路径），且幂等——没装过也退出 0 并返回 `removed:false`，可安全放进卸载脚本；`--json` 输出 `{shell, path, removed, reload_hint}`。

---

## 它如何工作 / How It Works

### Onboarding（项目知识库初始化）

每次调用 `/iterate` 时，skill 会检查项目根目录是否存在 `ITERATE.md`。若不存在，触发 onboarding，可通过任一条通道：

- **AI Onboarding** — AI 根据项目目录结构/清单文件自动识别技术栈并生成 `ITERATE.md` + `iterate.config.yaml`。
- **CLI Onboarding** — CLI 扫描后由你手动确认/调整技术栈与配置，产出相同产物。

扫描仅读取文件/目录**存在性**和 README.md 等少量公开上下文文件，不会读取 `.env`、密钥、凭证或其他敏感文件内容。项目专属约束可通过 `iterate personalize` 补充。

`ITERATE.md` 分为两个区域：

- `<!-- ITERATE:AI-MAINTAINED:START -->`：AI 维护区，刷新时会更新。
- `<!-- ITERATE:USER-OWNED:START -->`：用户维护区，手写约定、禁区、风险区，刷新时保留。

### 漂移检测

每次调用 `/iterate` 时，会重新计算 `package.json`、`pyproject.toml` 等 manifest 文件的 SHA-256 指纹：

- 无漂移 → 静默通过
- 有漂移 → 提示用户选择：继续 / 增量刷新 / 完整重新 onboarding

### 个性化配置

AI 扫描能发现技术栈和目录结构，但无法发现项目专属约束。`iterate personalize` 把这些知识沉淀下来：

- **禁区** — iterate 不得修改的文件/目录 → `iterate.config.yaml`
- **风险区** — 改动需架构审批 → `iterate.config.yaml`
- **已知意图** — 抑制误报 → `iterate.config.yaml`
- **维度定制** — 为特定维度追加 focus → `iterate.config.yaml`
- **优先修复顺序** — 维度修复优先级 → `iterate.config.yaml`
- **禁止的修复方式** — 不可使用的手法 → `iterate.config.yaml`
- **项目约定与注意点** — 经验教训、已知陷阱 → `ITERATE.md` 用户区
- **补充验证命令** — 项目特有验证命令 → `iterate.config.yaml`

完整示例请参考 [`config/iterate.config.yaml`](./config/iterate.config.yaml)。

### 按范围维度集与审查路由

顶层 `dimensions` 是**整仓 / 全局**审查的默认维度。对于**指定范围**的 goal，skill 的维度规划（SKILL.md Phase 0）会路由到合适的维度方案：

1. **goal 为空或泛化**（如"提升代码质量"）→ 直接用全局 `dimensions`。零摩擦。
2. **goal 命中已预置的 `dimension_sets` 命名集**（如"审查前端" → `frontend`）→ 直接采用该集的 `dimensions` + `focus` 覆盖，简要确认后即可。
3. **goal 未命中任何命名集（偏门范围）**→ AI **从根重新定义维度**：从 9 个规范维度出发（**不**以全局 `dimensions` 或任一已有维度集为起点——那只是惰性照抄），挑选真正与当前范围相关的维度，为每个维度给出**本范围特有的独立理由**，并可新增临时非标准维度。这次重定义会记录在 `.iterate_decisions.md` 的专用 `### Scope Dimension Redefinition (on-the-fly)` 小节中，并由 `scripts/validate.py decisions` **机器校验**——保证每个理由都不是照抄该维度默认 focus 提示词。

预设集只存于 `iterate.config.yaml`（`dimension_sets`）；`ITERATE.md` 只渲染一次"推荐审查蓝图（按范围）"清单。临时的重定义被**有界记录**在 `.iterate_decisions.md` 的当轮段落中，绝不会把 `ITERATE.md` 或 `iterate.config.yaml` 撑大——无论迭代积累多少轮，知识库都保持精简。

### 决策日志（`.iterate_decisions.md`）

每轮 AI 的决策——原子修复（直接）、架构修复（批准+执行 / 顺延）、回滚的修复、重要 AI 决策、验证结果，以及任何偏门范围的重定义——都会记录在 `.iterate_decisions.md`（模板见 `templates/iterate-decisions.template.md`）。这让过程可审计，同时保持 `ITERATE.md` 的 AI 维护区只是**最新快照**。

### 核心流程

```text
Step 0 — Onboarding Check
  └─ 定位项目根 → 检查 ITERATE.md → 漂移检测 →（缺失则触发 onboarding）

Setup
  └─ 提取 goal → 加载配置 → 读取项目上下文 → 创建隔离分支/worktree

Loop (round = 1 .. max_rounds)
  ├─ Phase 1: N 维度并行审查
  ├─ Phase 2: 原子问题自动修复
  ├─ Phase 3: 架构问题用户批准后执行
  ├─ Phase 4: 记录本轮结果
  └─ Phase 5: 验证 → merge（若 auto_merge=true）→ push（若 push_per_round=true）

Summary
```

详细流程请参考 [`SKILL.md`](./SKILL.md)。

---

## 配置参考 / Configuration

默认配置位于 [`config/iterate.config.yaml`](./config/iterate.config.yaml)。项目级配置会递归覆盖 Master 配置的同名字段。

常用配置项（每条格式：键 — 类型，默认值，含义）：

- `goal` — string，默认 `"Improve code quality"` — 迭代目标
- `max_rounds` — int，默认 `7` — 最大轮数（上限 50）
- `language` — string，默认 `"en"` — 输出语言：`zh` / `en`
- `mode` — string，默认 `"iterate"` — 默认执行模式：`iterate` / `defensive`（v3.0）
- `reasoning_effort` — string?，默认 `null` — `low` / `medium` / `high`；`null` = 跟随 provider 默认
- `dimensions` — list，默认全部 9 维度 — 启用的审查维度（整仓默认）
- `dimension_sets` — object — 命名范围蓝图（`frontend`/`api`/`security`/…），含 `dimensions` + 可选 `focus`
- `invariants` — object — `ensure` 文件存在断言 + `commands` 精确按模块命令列表（防御式模式交付门禁）
- `review.scope` — string，默认 `"full"` — `full` 全量 / `changed-only` 增量
- `atomic.max_lines` — int，默认 `20` — 原子问题最大行数
- `atomic.max_adjacent_methods` — int，默认 `3` — 原子问题最多的相邻方法数
- `git.target_branch` — string，默认 `main` — 合并目标分支
- `git.use_worktree` — bool，默认 `false` — 是否优先用 worktree 隔离
- `git.push_per_round` — bool，默认 `false` — 每轮通过后是否 push
- `git.auto_merge` — bool，默认 `false` — 验证后是否自动 merge
- `validation.command_whitelist` — list，默认常用前缀 — 允许执行的命令前缀（配置期安全）
- `validation.commands` — object，默认示例 — 按语言分组的验证命令（运行时唯一权威白名单）
- `reviewer.evidence_validation` — bool，默认 `true` — 硬证据门禁：每个 finding 的 file/line 必须真实存在
- `reviewer.coverage_validation` — bool，默认 `true` — 遗漏分配文件时提示 `COVERAGE_GAP`
- `reviewer.scope_chunk_size` — int，默认 `25` — `full` 范围审查每批分配的文件数
- `onboarding.drift_check` — bool，默认 `true` — 是否检查 manifest 漂移

示例：

```yaml
goal: "提升代码质量，确保所有函数 ≤80 行且测试通过"
max_rounds: 7
language: zh
mode: iterate          # 或 defensive

dimensions:
  - correctness
  - security
  - performance
  - architecture
  - style-tests
  - tech-debt
  - spec-compliance
  - frontend-backend
  - ui-ux

# 命名范围蓝图：指定范围的 goal 会路由到对应维度集，而不是全局 dimensions。
dimension_sets:
  frontend:
    dimensions:
      - ui-ux
      - frontend-backend
      - correctness
      - performance
    focus:
      ui-ux: "响应式布局、可访问性，以及视图特有的状态处理"
  security:
    dimensions:
      - security
      - correctness
    focus:
      security: "OWASP Top 10、认证/授权、注入、密钥处理"

# 防御式模式交付门禁：交付时必须存在的产物与必须通过的命令（缺省退化为 validation.commands）。
invariants:
  ensure:
    - "README.md"
  commands:
    python:
      - "pytest tests/ -x -q"

validation:
  command_whitelist:
    - "ruff"
    - "mypy"
    - "pytest"
    - "swift"
    - "npm run"
  commands:
    python:
      - "ruff check src/"
      - "mypy src/ --ignore-missing-imports"
      - "pytest tests/ -x -q"
    swift:
      - "swift build -c debug"
    typescript:
      - "npm run compile"
```

> `validation.commands` 中的命令**必须**以 `command_whitelist` 中的前缀开头，否则会被拒绝。

---

## 常见问题 / FAQ

### 安装 / Installation

**Q: 安装时提示要访问 GitHub 等国外网络，国内网络环境装不上怎么办？**
A: 安装器通过 GitHub Release 下载并校验，确实需要能访问 GitHub 的网络。若网络受限，可改用不依赖 GitHub 的方式：
- 手动复制 [`SKILL.md`](./SKILL.md) 到对应助手目录（见"方式 B"）。
- 国内镜像渠道（ModelScope / SkillHub CN）已上架，可从中获取 skill 文件。
- 社区代理镜像下载后，再执行 `python scripts/install.py install` 本地安装。

**Q: `npx iterate-skill-installer` 报 Python 或 Node 版本不符合？**
A: 安装器要求 Node.js 18+ 和 Python 3.10+。请先升级系统 Python/Node，或在终端确认 `python3` / `node` 在 PATH 中。安装器会优先使用 `python3`，再回退到 `python`。

**Q: 安装器会自动安装 `iterate` CLI 到我的电脑上，我能不装吗？**
A: 可以。`npx iterate-skill-installer` 会顺带安装 `iterate` CLI（优先 `pipx`，否则 `pip install --user`）以便直接运行 `iterate onboard`。若不希望自动安装 CLI，请改用"手动复制 SKILL.md"或"源码脚本"方式，仅复制 skill 文件即可。

**Q: 安装到一半想取消，会留下半成品吗？**
A: 不会。安装器在临时目录中完成下载、校验、解压，选中助手后才会写入助手目录；取消或失败时不会覆盖已安装的 skill。若已安装过，重装默认提示覆盖，需确认或加 `--force`。

### 使用 / Usage

**Q: 这个 Skill 适合什么场景？不适合什么场景？**
A: 适合**多轮**的代码审查与自动修复——例如压制技术债、多轮消除 lint/类型/测试问题、项目级重构。**不适合**单次简单改动（改一行、加个注释），这类需求直接用普通对话即可，无需 `/iterate`。

**Q: 该用 `iterate` 模式还是 `defensive` 模式？**
A: `/iterate` 适合**审查/修复已有代码**直到收敛。`/iterate defensive` 适合让 AI 做**正常编码工作**（新增功能、修 bug、重构、接入 API、补测试）：宿主 AI 动手前跑 `guard pre-check`、每次改动后跑 `guard post-check`，收尾用 `invariant` + 完整审查→修复→收敛闭环作为交付门禁。想让 AI"把东西做对"→ `defensive`；想让 AI"把已有的打磨到零 findings"→ `iterate`。

**Q: 第一次使用为什么什么都不做？**
A: 首次调用 `/iterate` 或运行 `iterate onboard` 前，项目还没有 `ITERATE.md` 与 `iterate.config.yaml`。首次使用时 skill 会**先进行项目初始化（Onboarding）**：AI 会明确告知"这是首次使用，将先初始化项目"，扫描代码库生成 `ITERATE.md` 与配置后再进入迭代。若你看到初始化提示而不是立刻审查，这是正常流程，不是失效；也可直接在项目根目录运行 `iterate onboard` 手动完成初始化。

**Q: 处理大项目时感觉卡住，没有进度提示？**
A: 大项目首轮要并行审查多个维度，可能耗时较长。为缓解"卡住"观感，skill 现在会在对话中**持续输出进度**：每轮开始显示 `▶ Round N/max`、并行审查期间逐维度提示 `⏳ 正在审查 …`、每轮结束显示 `✅ Round N complete`。若仍觉慢，可通过以下方式提速：
- 在 `iterate.config.yaml` 中把 `review.scope` 设为 `changed-only`，只审查本轮改动。
- 按目录/模块拆分 reviewer 任务（见 SKILL.md 的 Reviewer Prompt 检查清单）。
- 适当降低 `max_rounds`，避免无谓的额外轮次。

**Q: 运行时提示有漂移（drift）是什么意思？**
A: 漂移检测会对比 `package.json`、`pyproject.toml` 等 manifest 文件的 SHA-256 指纹（onboarding 时记录的指纹 vs 当前项目状态）。若依赖或配置发生变化，说明项目状态与上次 onboarding 不一致，会提示你选择：继续 / 增量刷新（`iterate refresh`）/ 完整重新 onboarding（`iterate reonboard`）。若想在不触发迭代的情况下单独检查漂移，可运行 `iterate fingerprint`（检测到漂移时退出码为 1）。

**Q: 修改没有合并到主分支，也没推送到远程？**
A: 这是**安全默认**行为：`git.auto_merge` 与 `git.push_per_round` 默认均为 `false`，改动保留在隔离的 `iterate/*` 分支或 worktree 中，由你 review 后决定是否合并/推送。如需自动合并推送，请在 `iterate.config.yaml` 中显式开启这两个选项。

**Q: 我手动改了 `iterate.config.yaml`，为什么某些验证命令不生效？**
A: `validation.commands` 中的命令**必须**以 `validation.command_whitelist` 中的前缀开头，否则会被拒绝。个性化添加的 `extra_validation_commands` 也只会接受 30+ 预批准工具前缀，拒绝 `;`、`|`、`&` 等 shell 元字符——这是为了安全，防止项目配置被执行任意命令。

**Q: 想增加一个新的验证工具（比如 `sphinx`），怎么办？**
A: 严格白名单只接受预批准的工具前缀（这防止项目配置执行任意命令）。新增工具有两种**安全**方式：
- **操作者级环境变量（推荐，无需改源码）**：在运行环境中设置 `ITERATE_EXTRA_SAFE_COMMAND_PREFIXES=sphinx`（逗号/空格分隔多个工具名）。该变量**只能在系统层面设置**，项目配置文件无法设置，因此不会破坏安全模型；含 `;`、`|`、`&` 等元字符的条目会被直接丢弃（fail-closed）。
- **源码级扩展**：在 `iterate_cli/personalize.py` 的 `KNOWN_SAFE_COMMAND_PREFIXES` 中追加工具名后重新安装。
- 或改用 `validation.command_whitelist` + `validation.commands` 直接配置（需通过 `python scripts/validate.py config` 校验）。

### 安全 / Security

**Q: 这个 Skill 会读取我的密钥、`.env` 吗？**
A: 不会。skill 及 onboarding 扫描仅读取 manifest 文件的存在性和 `README.md` / `CLAUDE.md` 等公开上下文文件，明确不读取 `.env`、`*.key`、`secrets/`、`*.pem` 等敏感文件。`projectContext` 也不会包含 API 密钥、密码、Token。

**Q: 下载更新时安全吗？**
A: 安全。`scripts/install.py update` 与 `npx iterate-skill-installer` 从 GitHub Release 下载预上传的 `iterate-skill.tar.gz` + `SHA256SUMS.txt`，下载后强制 SHA256 校验，缺失或不匹配则拒绝安装。

---

## 安全说明 / Security

- **高自主性**：本 skill 会自主执行文件编辑、`git` 操作以及 `validation.commands` 中配置的命令。所有修改先在隔离分支/worktree 中进行，架构修复必须经用户批准。
- **Secure-by-default Git**：`push_per_round` 和 `auto_merge` 默认均为 `false`；merge/push 为 opt-in，未显式开启时改动保留在迭代分支。回滚使用 `git restore` 等非破坏性命令。
- **双层命令白名单**：
  - 配置时校验命令前缀。
  - 个性化添加 `extra_validation_commands` 时仅接受 30+ 预批准工具前缀，拒绝 `;`、`|`、`&` 等 shell 元字符；命令加载/合并时也会重新校验，手工编辑的配置无法绕过白名单。
- **敏感文件**：skill 及其 installer 不读取 `.env`、密钥、凭证等敏感文件；onboarding 扫描仅检查 manifest 等公开文件的存在性。
- **Update 安全**：`scripts/install.py update` 与 `npx iterate-skill-installer` 从 GitHub Release 下载预上传的 `iterate-skill.tar.gz` + `SHA256SUMS.txt`，下载后强制 SHA256 校验，缺失或不匹配则拒绝安装。
- **安装器披露**：`npx iterate-skill-installer` 会顺带把 `iterate` CLI 安装到 PATH（优先 `pipx` 隔离，否则 `--user`）。若不希望安装 CLI，请使用手动复制或源码脚本方式。

---

## 目录结构 / Directory Structure

```text
iterate-skill/
├── SKILL.md                          # 核心技能文件
├── README.md                         # 英文 README
├── README.zh-CN.md                   # 中文 README（本文件）
├── LICENSE                           # MIT 许可证
├── CONTRIBUTING.md                   # 开源贡献指南
├── CHANGELOG.md                      # 版本变更记录
├── pyproject.toml                    # iterate CLI 包定义
├── npm-installer/                    # npx 一键安装器源码
│   ├── bin/cli.js
│   ├── lib/installer.js
│   └── package.json
├── config/
│   ├── iterate.config.yaml           # 默认配置（Master）
│   ├── config.schema.json            # 配置 JSON Schema
│   ├── dimensions.yaml               # 聚合版维度定义
│   └── dimensions/                   # 数据驱动的维度定义
├── examples/                         # 各语言项目示例
├── harness/                          # iterate 生态的两个工程化落地组件（monorepo）
│   ├── iterate-harness/              # 独立无头引擎（npm: iterate-harness，命令 ih）
│   │   ├── src/iterate_harness/      #   CLI / 引擎 / web / UI 源码
│   │   ├── frontend/                 #   终端 / web 前端界面
│   │   ├── npm/                      #   npm 包装器（ih）
│   │   └── scripts/                  #   安装脚本与 e2e 测试
│   └── iterate-plugin/               # dsh 桌面插件（npm: iterate-plugin）
│       ├── src/                      #   服务端逻辑（TypeScript，编译到 dist/）
│       ├── lib/                      #   客户端 UI 注入入口
│       └── cordis.patch.yml          #   dsh bundle 声明
├── templates/
│   ├── ITERATE.template.md           # 知识库模板
│   └── iterate-decisions.template.md # 每轮决策日志模板
├── iterate_cli/                      # onboarding CLI 源码
│   ├── cli.py                        #   顶层命令分发器
│   ├── guard.py                      #   guard 动手前/后校验（防御式模式）
│   ├── configcmd.py                  #   iterate config get/set
│   ├── dimension_sets.py             #   范围维度集 建议/规范化/合并
│   ├── wizard.py / scan.py / generator.py / refresh.py / personalize.py /
│   │   doctor.py / show.py / fingerprint.py / tui.py
│   └── data/
│       ├── ITERATE.template.md       # wheel 打包模板
│       └── config.schema.json        # wheel 打包 schema（与主文件保持同步）
├── scripts/
│   ├── install.py                    # 安装/卸载/配置/校验脚本
│   ├── validate.py                   # 配置与决策日志校验（含范围重定义检查）
│   └── requirements.txt              # 脚本依赖
├── tools/                            # 各 AI 助手专属实现示例
├── tests/                            # 单元测试
└── .github/workflows/                # CI / Release
```

---

## 贡献 / Contributing

欢迎提交 Issue 和 PR！

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feat/your-feature`
3. 提交改动：`git commit -m "feat: description"`
4. 推送分支：`git push origin feat/your-feature`
5. 创建 Pull Request

请保持 `SKILL.md` 的中英双语结构，新增功能需补充配置示例。

---

## 免责声明 / Disclaimer

本项目按「现状」（AS IS）提供，不附带任何明示或暗示的担保，包括但不限于对适销性、特定用途适用性及不侵权性的担保。

**自动化的代码审查与修复存在固有风险。** normal 模式下产生的改动均由 AI 模型生成，可能引入缺陷、回归或非预期行为。在合并改动前，你应当：

- 在应用到主分支或推送前，逐条 review 每一处 diff。
- 确保项目处于 git 版本控制之下，并可随时回滚（`git restore`、revert 或从备份恢复）。
- 在每轮修复后运行项目自身的测试与构建检查。
- 切勿在密钥、凭证、`.env` 或任何不允许修改的文件上运行本项目；请在 `iterate.config.yaml` 的 `protected_paths` 中配置相应的保护路径。

使用者需为本项目使用过程中所产生、修改或提交的代码负全部责任。使用本项目即表示你同意：维护者与贡献者不对因使用本项目而导致的任何损失、损害或法律后果承担责任。

---

## 许可证 / License

[MIT](./LICENSE) © 2026 iterate-skill contributors