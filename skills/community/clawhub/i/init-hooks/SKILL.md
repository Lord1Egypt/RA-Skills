---
name: init-hooks
description: >
  管理 OpenClaw 容器启动时自动执行的脚本钩子。gateway 重启、pod 重启、pod 重建均不丢失（数据持久化在 workspace/.init-hooks/）。
  支持 inline 命令、本地脚本（shell/python）、CDN URL（zip/tar.gz 自动下载解压）三种钩子类型。
  用于：新增/查看/修改/禁用/删除启动钩子、立即测试运行、查看执行日志。
  触发词：init-hooks、启动钩子、startup hook、重启初始化、pod重启执行、开机自启。
  安装触发词：帮我安装 init-hooks、初始化 init-hooks、设置 init-hooks、执行 init-hooks 安装。
  配置变更触发词：修改 openclaw.json、改 gateway 配置、改配置文件 → 执行后自动调用 sync_openclaw_config.py。
  能力边界：不主动修改任何配置项，不预设默认值；只把用户明确给出的 patch 原样写入，并把配置复制到用户配置的持久化路径。
---

# init-hooks

- **Version**: 1.0.4
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/better-agent-skills (skills/init-hooks)

> 管理 OpenClaw 容器/主机启动时自动执行的脚本钩子。gateway 重启、容器重启、容器重建均不丢失（数据持久化在 `workspace/.init-hooks/`）。支持 inline 命令 / 本地脚本（shell·python）/ CDN URL（zip·tar.gz 自动下载解压）三种钩子类型。

## 路径约定

```
~/.openclaw/workspace/.init-hooks/
├── hooks.json        # 注册表（truth）
├── dispatcher.sh     # 自动生成，post-init.sh 调用这个
├── last-run.log      # 每次启动执行日志
└── downloads/        # CDN URL 钩子下载缓存
    └── hook_<id>.*
```

脚本路径：

```
~/.openclaw/workspace/skills/init-hooks/scripts/
├── manage.py               # 主入口（所有 CRUD + run + install）
└── sync_openclaw_config.py # openclaw.json 多路径同步工具
```

## 操作命令速查

所有操作通过 `exec` 运行，工作目录任意：

```bash
SCRIPT="$HOME/.openclaw/workspace/skills/init-hooks/scripts/manage.py"

python3 $SCRIPT install          # 首次安装
python3 $SCRIPT list             # 列出所有钩子
python3 $SCRIPT show <id>        # 查看钩子详情
python3 $SCRIPT add ...          # 新增（见下方）
python3 $SCRIPT edit <id> ...    # 修改
python3 $SCRIPT enable <id>      # 启用
python3 $SCRIPT disable <id>     # 禁用
python3 $SCRIPT delete <id>      # 删除（需二次确认）
python3 $SCRIPT delete <id> --force  # 强制删除不确认
python3 $SCRIPT run              # 立即运行所有启用的钩子
python3 $SCRIPT run <id>         # 立即运行指定钩子
python3 $SCRIPT status           # 查看安装状态
```

## 新增钩子：三种类型

### inline（内嵌 shell 命令）

```bash
python3 $SCRIPT add \
  --name "初始化日志目录" \
  --type inline \
  --content "mkdir -p ~/logs && echo 'started' >> ~/logs/boot.log"
```

多行命令用 `\n` 分隔：

```bash
python3 $SCRIPT add \
  --name "环境变量初始化" \
  --type inline \
  --content $'export MY_VAR=hello\nmkdir -p ~/tmp'
```

### script（本地 shell 脚本）

```bash
python3 $SCRIPT add \
  --name "凭证/账号启动恢复" \
  --type script \
  --path "~/.openclaw/workspace/scripts/restore-credentials.sh"
```

### python（本地 Python 脚本）

```bash
python3 $SCRIPT add \
  --name "Agent workspace 配置" \
  --type python \
  --path "~/.openclaw/workspace/scripts/set-agents.py"
```

### CDN URL（zip/tar.gz 自动下载解压）

> ⚠️ **安全模型**：URL 钩子会**下载并执行远程代码**。v1.0.1 起强制完整性校验，v1.0.2 起补齐"失败关闭"与解包防护：
> - `--sha256` 必填（`shasum -a 256` 的 64 位 hex 输出）。下载后立即校验，不匹配拒绝执行；缓存每次使用前也会复核校验标记
> - 校验或解包任一步失败，**一律不执行**，并且会先删掉上一轮留下的可执行入口（不会拿旧脚本顶替）
> - 解包**不创建任何链接**：压缩包内的符号链接 / 硬链接 / 设备文件 / FIFO 一律拒绝；绝对路径与 `..` 穿越同样拒绝；文件以 `O_NOFOLLOW` 落盘
> - 确实无法提供校验值时，加 `--allow-unverified` 显式豁免（不推荐，dispatcher 日志会持续警告）
> - 生成的 dispatcher.sh 内置相同校验与解包规则，启动时同样强制

```bash
# 先算校验值
curl -fsSL "https://cdn.example.com/my-init.zip" -o /tmp/pkg
shasum -a 256 /tmp/pkg        # → 64 位 hex

python3 $SCRIPT add \
  --name "远程初始化包" \
  --type script \
  --url "https://cdn.example.com/my-init.zip" \
  --sha256 "abc123..." \
  --entry "run.sh"
# --sha256 = 上一步 shasum 输出（必填，除非加 --allow-unverified 显式豁免）
# --entry  = 压缩包内入口文件名（不指定则自动找第一个 .sh/.py）
```

首次执行（启动或 `run` 命令）时自动下载解压到 `downloads/hook_<id>/`，缓存存在则直接使用，pod 重建后缓存丢失会自动重新下载。

> 解压按**文件内容**判断格式，不依赖 URL 后缀。zip 需要 Info-ZIP 版 `unzip`（要能 `unzip -Z` 枚举成员）；容器里若只有 busybox 的 unzip，会明确拒绝并建议改用 tar.gz。

### 追加 --order 控制执行顺序（默认步进 10）

```bash
python3 $SCRIPT add --name "..." --type inline --content "..." --order 5
```

## 修改钩子

```bash
# 改名称
python3 $SCRIPT edit 2 --name "新名称"
# 改内容
python3 $SCRIPT edit 2 --content "new command"
# 改路径
python3 $SCRIPT edit 1 --path ~/scripts/new.sh
# 改顺序
python3 $SCRIPT edit 1 --order 15
# 改为 URL 模式
python3 $SCRIPT edit 1 --url https://... --entry run.sh
```

## openclaw.json 变更必须同步持久化路径

**触发场景：** 用户说「修改 openclaw.json」「改 gateway 配置」「给我改配置」，或者用户直接提供了修改 openclaw.json 的脚本/内容。

> **能力边界**：`sync_openclaw_config.py` 只做两件事——把 `openclaw.json` 复制到 `INIT_HOOKS_SYNC_PATHS` 指定的持久化路径、把**用户明确给出的** patch 原样写进配置。它没有任何预置默认值，不会自己开启、关闭或"顺手"改动任何配置项；改什么完全由用户指定。

**必须在改完后立即执行：**

```bash
SYNC="$HOME/.openclaw/workspace/skills/init-hooks/scripts/sync_openclaw_config.py"

# 场景1：按用户明确要求 patch 某个字段 —— patch 内容由用户给出（写成文件），
#         Agent 不自己造字段、不预设默认值
python3 $SYNC --patch "$(cat ~/user-patch.json)"

# 场景2：用户提供了修改脚本，执行完后自动同步
python3 $SYNC --run ~/scripts/patch_config.py

# 场景3：inline 命令修改后同步
python3 $SYNC --run-inline "sed -i 's/old/new/' ~/.openclaw/openclaw.json"

# 场景4：只同步（已手动改了 runtime）
python3 $SYNC

# 检查各处是否一致
python3 $SYNC --check
```

**同步路径（跨部署环境可配置）：**
1. `~/.openclaw/openclaw.json`（runtime，source of truth，始终维护）
2. 额外持久化目标：由环境变量 `INIT_HOOKS_SYNC_PATHS`（冒号分隔）配置，不存在的路径自动跳过

```bash
# 纯本地/单机：通常无需额外同步，留空即可（只维护 runtime 一份）

# 容器/K8s：把 runtime 之外的持久化挂载点填进来（按你自己的挂载布局替换示例）
export INIT_HOOKS_SYNC_PATHS="/app/clawconfig/openclaw.json:/app/k8s-config/clawconfig/openclaw.json"
```

未配置 `INIT_HOOKS_SYNC_PATHS` 时只维护 runtime 一份（本地环境属正常）。

## 安装流程（install）

`install` 是幂等的，可重复执行：

1. 创建 `~/.openclaw/workspace/.init-hooks/` 目录
2. 初始化 `hooks.json`（若已存在则跳过）
3. 生成 `dispatcher.sh`
4. 检查 `~/.openclaw/workspace/scripts/post-init.sh`：
   - 存在 → 在末尾追加 dispatcher 调用（有标记防重复注入）
   - 不存在 → 创建，内容只有 dispatcher 调用
5. 检查容器启动脚本（`/app/start.sh`，可用 `INIT_HOOKS_START_SH` 覆盖；本地无此文件时跳过）：
   - 已有 `# post-init hook` → 间接调用，跳过
   - 否则在末尾追加 dispatcher 直接调用

## 执行行为

- **宽松模式**：单个钩子失败不中断后续
- **顺序执行**：按 `order` 字段从小到大
- **日志**：每次执行追加到 `last-run.log`，同时 tee 到 stdout
- **执行摘要**：每次执行结束后打印成功/失败列表

## 关于 start.sh 注入

`install` 会尝试向容器启动脚本（默认 `/app/start.sh`，可用 `INIT_HOOKS_START_SH` 覆盖）注入 dispatcher 调用。大多数用户没有写权限、或本地环境根本没有这个文件，都属**正常情况**，不影响使用：
- `post-init.sh` 已注入 → dispatcher 经由 post-init.sh 间接调用
- 启动脚本注入失败/不存在提示 `ℹ️` 而非 `⚠️` 或 `❌`，无需担心

## 用户意图识别

| 用户说 | Agent 动作 |
|--------|-----------|
| 帮我安装 / 初始化 / 设置 init-hooks | `install` |
| 添加一个启动钩子 / 加一个开机执行 | `add` |
| 列出 / 查看所有钩子 | `list` |
| 查看钩子 #2 / 第2个钩子内容 | `show 2` |
| 修改钩子 #1 | `edit 1 ...` |
| 禁用 / 停用 / 关闭 钩子 #3 | `disable 3` |
| 删除钩子 #2 | `delete 2`（展示详情后二次确认） |
| 立即运行 / 测试一下 / 跑一遍 | `run` |
| 只运行钩子 #1 | `run 1` |
| 查看状态 / 安装了吗 | `status` |
| 修改 openclaw.json / 改 gateway 配置 | 改完后 `sync_openclaw_config.py` |
| 查看上次执行日志 | `read ~/.openclaw/workspace/.init-hooks/last-run.log` |

## 钩子编写规范

详见 `references/best-practices.md`，包含三种类型的完整示例、路径规范、执行顺序建议。

**核心规则：** 钩子内容禁止硬编码 `/home/node/`，必须用 `$HOME`（shell）或 `Path.home()`（Python）。

---

## 注意事项

- 每次 `add` / `edit` / `enable` / `disable` / `delete` 后，`dispatcher.sh` 自动重新生成
- CDN URL 钩子：首次 `run` 时下载，缓存在 `downloads/`；re-install 不清除缓存（需手动删 `downloads/hook_<id>/`）
- `delete --force` 跳过确认，Agent 不应使用（除非用户明确说"直接删"）
- hooks.json 是 truth，dispatcher.sh 是生成物，手动改 dispatcher.sh 会在下次操作时被覆盖
