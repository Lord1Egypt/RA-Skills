# OpenClaw Feishu Quota Guard

这是一个给 OpenClaw 使用的 skill，并附带一个“一次运行即可生效”的修复工具，专门处理常见的 `OpenClaw + 飞书 / Lark` 额度异常消耗问题。

它主要针对下面两类场景：

- OpenClaw 的 heartbeat 后台任务过于频繁，持续消耗云端模型额度
- webhook、gateway 或 `/health` 探活逻辑误触发模型调用

这个仓库自带的修复器会优先自动处理低风险的标准 OpenClaw heartbeat 配置；如果检测到自定义 webhook 或 `/health` 代码，它会提示你继续人工检查，而不会盲目乱改业务代码。

## 它会修改什么

默认的 `throttle` 模式会把标准 OpenClaw heartbeat 配置调整为：

- `agents.defaults.heartbeat.every = "1h"`
- `agents.defaults.heartbeat.lightContext = true`
- `agents.defaults.heartbeat.isolatedSession = true`
- 如果缺失，则补上 `agents.defaults.heartbeat.target = "none"`

可选的 `disable` 模式会设置：

- `agents.defaults.heartbeat.every = "0m"`

每次真实写入前，都会先给 `openclaw.json` 创建一个带时间戳的备份文件。

## 依赖要求

- 目标机器已安装 OpenClaw
- Python 3.8 及以上，并且可通过 `python` 或 `py` 调用
- macOS / Linux 上如需使用 shell wrapper，需要 `bash`
- Windows 上如需使用 PowerShell wrapper，需要 PowerShell
- 推荐安装 `rg`（ripgrep）以获得更好的扫描结果，但不是必须

## 平台兼容性

这个仓库现在提供了三大平台的原生入口，同时保留跨平台 Python 主入口：

- macOS:
  - `install-openclaw-skill.sh`
  - `scripts/run-once.sh`
  - `scripts/find_feishu_quota_candidates.sh`
- Linux:
  - `install-openclaw-skill.sh`
  - `scripts/run-once.sh`
  - `scripts/find_feishu_quota_candidates.sh`
- Windows PowerShell:
  - `install-openclaw-skill.ps1`
  - `scripts/run-once.ps1`
  - `scripts/find-feishu-quota-candidates.ps1`
- Windows CMD:
  - `install-openclaw-skill.cmd`
  - `scripts/run-once.cmd`
  - `scripts/find-feishu-quota-candidates.cmd`
- 跨平台 Python 主入口:
  - `install_openclaw_skill.py`
  - `scripts/apply_feishu_quota_fix.py`
  - `scripts/find_feishu_quota_candidates.py`

推荐做法：

- 如果你要在多台不同系统的机器上自动化部署，优先使用 Python 入口
- 如果你只是在当前机器手动操作，优先使用当前系统对应的原生 wrapper

## 安装

### OpenClaw 自动安装

这里的“自动安装”要分成两种理解：

1. 通过 OpenClaw 公共技能注册表自动安装
2. 通过已经在运行的 OpenClaw agent 代你执行 clone、复制、安装和修复命令

对于当前版本的 OpenClaw，公共技能安装走的是 [ClawHub](https://docs.openclaw.ai/tools/clawhub)，而不是直接从私有 GitHub 仓库安装。ClawHub 目前是公开分发模式，所以这个私有仓库本身不能直接作为公共注册表安装源。

如果你将来把这个 skill 发布到 ClawHub，那么标准安装流程会是：

```bash
clawhub install openclaw-feishu-quota-guard
```

安装后，OpenClaw 会从 workspace 的 `skills/` 目录中自动发现它。

如果你已经有一个可用的 OpenClaw agent，并且它具备 shell / 文件系统访问能力，也可以让它自动完成下面这些动作：

1. clone 这个仓库
2. 运行 `install-openclaw-skill.sh` 或对应平台的安装入口
3. 运行 `scripts/run-once.*` 或 Python 修复入口

这种方式在实际使用里也算“自动安装”，但底层本质上还是调用了本仓库提供的手动安装器。

### 手动安装：安装到单个 OpenClaw Workspace

这种方式只会把 skill 装到某一个 OpenClaw workspace 下。

macOS / Linux：

```bash
git clone git@github.com:HerbertWYT/openclaw-feishu-quota-guard.git
cd openclaw-feishu-quota-guard
bash install-openclaw-skill.sh /path/to/openclaw/workspace
```

Windows PowerShell：

```powershell
git clone git@github.com:HerbertWYT/openclaw-feishu-quota-guard.git
cd openclaw-feishu-quota-guard
powershell -ExecutionPolicy Bypass -File .\install-openclaw-skill.ps1 --workspace C:\path\to\openclaw\workspace
```

Windows CMD：

```bat
git clone git@github.com:HerbertWYT/openclaw-feishu-quota-guard.git
cd openclaw-feishu-quota-guard
install-openclaw-skill.cmd --workspace C:\path\to\openclaw\workspace
```

跨平台 Python：

```bash
python install_openclaw_skill.py --workspace /path/to/openclaw/workspace
```

安装后，skill 会被复制到：

```text
/path/to/openclaw/workspace/skills/openclaw-feishu-quota-guard
```

OpenClaw 的技能发现机制可以参考：

- [Skills system](https://docs.openclaw.ai/skills)
- [Creating custom skills](https://docs.openclaw.ai/tools/creating-skills)

### 手动安装：安装到本机共享技能目录

这种方式会把 skill 安装到 OpenClaw 的本机共享技能目录，让同一台机器上的多个本地 agent 都能看到。

macOS / Linux：

```bash
git clone git@github.com:HerbertWYT/openclaw-feishu-quota-guard.git
cd openclaw-feishu-quota-guard
bash install-openclaw-skill.sh --shared
```

Windows PowerShell：

```powershell
git clone git@github.com:HerbertWYT/openclaw-feishu-quota-guard.git
cd openclaw-feishu-quota-guard
powershell -ExecutionPolicy Bypass -File .\install-openclaw-skill.ps1 --shared
```

Windows CMD：

```bat
git clone git@github.com:HerbertWYT/openclaw-feishu-quota-guard.git
cd openclaw-feishu-quota-guard
install-openclaw-skill.cmd --shared
```

跨平台 Python：

```bash
python install_openclaw_skill.py --shared
```

默认会安装到：

```text
~/.openclaw/skills/openclaw-feishu-quota-guard
```

按照当前 OpenClaw 文档，技能优先级大致是：

- OpenClaw 自带技能
- `~/.openclaw/skills`
- `<workspace>/skills`

其中 `<workspace>/skills` 在同名冲突时优先级最高。参考文档：[OpenClaw Skills](https://docs.openclaw.ai/skills)

### 不使用安装脚本，手动复制

如果你不想用安装器，也可以直接复制目录。

macOS / Linux：

```bash
mkdir -p /path/to/openclaw/workspace/skills
cp -R openclaw-feishu-quota-guard /path/to/openclaw/workspace/skills/
```

或者安装到共享目录：

```bash
mkdir -p ~/.openclaw/skills
cp -R openclaw-feishu-quota-guard ~/.openclaw/skills/
```

Windows PowerShell：

```powershell
New-Item -ItemType Directory -Force C:\path\to\openclaw\workspace\skills | Out-Null
Copy-Item -Recurse -Force .\openclaw-feishu-quota-guard C:\path\to\openclaw\workspace\skills\
```

或者安装到共享目录：

```powershell
New-Item -ItemType Directory -Force "$HOME\.openclaw\skills" | Out-Null
Copy-Item -Recurse -Force .\openclaw-feishu-quota-guard "$HOME\.openclaw\skills\"
```

## 使用方法

### 1. 先确认 OpenClaw 能看到这个 Skill

安装完成后，建议开启一个新 session，或者重启相关 gateway / session，让 OpenClaw 重新发现技能。

可以先用下面的命令检查：

```bash
openclaw skills list
openclaw skills check
```

CLI 参考：

- [openclaw skills](https://docs.openclaw.ai/cli/skills)

### 2. 先做 Dry Run 预览

建议先预览修复器打算做什么。

跨平台 Python：

```bash
python /path/to/skill/scripts/apply_feishu_quota_fix.py --dry-run
```

macOS / Linux：

```bash
bash /path/to/skill/scripts/run-once.sh --dry-run
```

如果 skill 装在某个 workspace 里：

```bash
bash /path/to/openclaw/workspace/skills/openclaw-feishu-quota-guard/scripts/run-once.sh --dry-run
```

如果 skill 装在共享目录：

```bash
bash ~/.openclaw/skills/openclaw-feishu-quota-guard/scripts/run-once.sh --dry-run
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File C:\path\to\skill\scripts\run-once.ps1 --dry-run
```

Windows CMD：

```bat
C:\path\to\skill\scripts\run-once.cmd --dry-run
```

### 3. 执行推荐修复

推荐模式是 `throttle`，也就是“保留 heartbeat，但把它调成更省额度”。

跨平台 Python：

```bash
python /path/to/skill/scripts/apply_feishu_quota_fix.py
```

macOS / Linux：

```bash
bash /path/to/skill/scripts/run-once.sh
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File C:\path\to\skill\scripts\run-once.ps1
```

Windows CMD：

```bat
C:\path\to\skill\scripts\run-once.cmd
```

### 4. 完全关闭 Heartbeat

如果你确认当前部署根本不需要 heartbeat，可以直接改成禁用模式。

跨平台 Python：

```bash
python /path/to/skill/scripts/apply_feishu_quota_fix.py --mode disable
```

macOS / Linux：

```bash
bash /path/to/skill/scripts/run-once.sh --mode disable
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File C:\path\to\skill\scripts\run-once.ps1 --mode disable
```

### 5. 指定特定 Config 或 Workspace

如果一台机器上有多个 OpenClaw 实例，或者你的目录结构不是默认布局，建议显式传参。

跨平台 Python：

```bash
python /path/to/skill/scripts/apply_feishu_quota_fix.py \
  --config /path/to/openclaw.json \
  --workspace /path/to/workspace
```

macOS / Linux：

```bash
bash /path/to/skill/scripts/run-once.sh \
  --config /path/to/openclaw.json \
  --workspace /path/to/workspace
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File C:\path\to\skill\scripts\run-once.ps1 `
  --config C:\path\to\openclaw.json `
  --workspace C:\path\to\workspace
```

### 6. 深度扫描可疑文件

如果你怀疑问题不只是 heartbeat，而是来自自定义 Feishu gateway、webhook 或 `/health` 路由，可以额外跑扫描器。

跨平台 Python：

```bash
python /path/to/skill/scripts/find_feishu_quota_candidates.py /path/to/workspace
```

macOS / Linux：

```bash
bash /path/to/skill/scripts/find_feishu_quota_candidates.sh /path/to/workspace
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File C:\path\to\skill\scripts\find-feishu-quota-candidates.ps1 C:\path\to\workspace
```

Windows CMD：

```bat
C:\path\to\skill\scripts\find-feishu-quota-candidates.cmd C:\path\to\workspace
```

## `run-once` 实际会做什么

修复器会按下面这个顺序工作：

1. 找到当前生效的 `openclaw.json`
2. 推断对应的 workspace
3. 打印计划修改内容
4. 扫描是“官方 Feishu 配置”还是“自定义 webhook / gateway 线索”
5. 创建备份
6. 写入新的配置
7. 如果本机可用，则运行 `openclaw config validate`

它不会去粗暴改写任意业务代码。如果额度消耗来自你自己写的 `/health` 路由或 webhook 服务，它会提示你那一部分还需要人工处理。

## 验证修复结果

应用修复后，建议执行下面几步：

1. 重启相关的 OpenClaw gateway 或 agent 进程
2. 观察日志几分钟
3. 确认额度消耗速率恢复正常

常用命令：

```bash
openclaw config validate
openclaw status --deep
openclaw logs
```

如果你是把 skill 装进某个 workspace，要注意 OpenClaw 会按 session 维度缓存可见技能。也就是说，新装 skill 后通常需要新开 session，或者刷新原有 session，agent 才会看到它。参考文档：[OpenClaw Skills](https://docs.openclaw.ai/skills)

## 仓库结构

```text
.
├── install_openclaw_skill.py
├── install-openclaw-skill.cmd
├── install-openclaw-skill.ps1
├── SKILL.md
├── install-openclaw-skill.sh
├── scripts/
│   ├── apply_feishu_quota_fix.py
│   ├── find-feishu-quota-candidates.cmd
│   ├── find-feishu-quota-candidates.ps1
│   ├── find_feishu_quota_candidates.py
│   ├── find_feishu_quota_candidates.sh
│   ├── run-once.cmd
│   ├── run-once.ps1
│   └── run-once.sh
└── references/
    └── source-notes.md
```

## 参考资料

- [OpenClaw Skills](https://docs.openclaw.ai/skills)
- [openclaw skills CLI](https://docs.openclaw.ai/cli/skills)
- [ClawHub](https://docs.openclaw.ai/tools/clawhub)
- [Creating Custom Skills](https://docs.openclaw.ai/tools/creating-skills)
- [视频背景：BV1fvcuzVEsc](https://www.bilibili.com/video/BV1fvcuzVEsc/)
