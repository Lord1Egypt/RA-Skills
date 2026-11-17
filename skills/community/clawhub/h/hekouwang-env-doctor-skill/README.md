<div align="right"><sub><b>中文</b> · <a href="README.en.md">English</a></sub></div>

<h1 align="center">env-doctor · 开发环境体检器</h1>

<p align="center">
  <b>别的清理工具问「哪个目录大」，它问「这个工具你还在用吗」。</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Skill-a855f7?style=flat-square&logo=anthropic&logoColor=white" alt="Claude Code Skill">
  <img src="https://img.shields.io/badge/platform-macOS_·_Linux-6d28d9?style=flat-square&logo=apple&logoColor=white" alt="platform">
  <img src="https://img.shields.io/badge/shell-bash_3.2%2B-4EAA25?style=flat-square&logo=gnubash&logoColor=white" alt="bash">
  <img src="https://img.shields.io/badge/dependencies-none-3f8a82?style=flat-square" alt="zero dependencies">
  <img src="https://img.shields.io/badge/scan-read--only-179?style=flat-square" alt="read only">
  <img src="https://img.shields.io/badge/license-MIT-b88a3e?style=flat-square" alt="MIT">
  <img src="https://img.shields.io/github/stars/huiyonghkw/hekouwang-env-doctor-skill?style=flat-square&color=ff8a3d" alt="stars">
</p>

<p align="center">
  <img src="demo/env-doctor.gif?v=2" alt="在 Claude Code 里出体检报告：把磁盘占用分成 残留/缓存/数据 三组" width="100%">
</p>

---

## 一句话

Mac 用久了空间告急，你翻相册删视频——**真正的大户是开发工具在你看不见的地方囤的东西**。而其中最该清、也最难发现的一类是：**你已经换掉、但从没卸干净的旧工具**。

作者本机实测：`~/.nvm` 占着 **9.8 GB**，可 node 早就由 fnm 提供了，那个目录一年多没动过。**按这份报告清完，腾出约 10 GB。**

## 凭什么它能发现别人发现不了的

体积可以测量，**身份只能推理**。判断 nvm 是不是残留，得同时看四件事：

| 信号 | 看什么 | 权重 |
|---|---|---|
| `shell_loaded` | shell 配置里是否**真的加载**它（注释行不算） | 高 |
| `cmd_in_path` | 命令是否还在 PATH 里 | 高 |
| `runtime owner` | `node` / `python` **实际由谁提供** | 最高 |
| `last_modified` | 目录多久没动过 | 佐证 |

实测输出长这样：

```
nvm    9.8 GB   未加载  不在PATH  node由fnm提供   最后改动 2025-03  → 残留 ✅可清
fnm    1.7 GB   已加载  在PATH    node由它提供    最后改动 2026-05  → 活跃 ⛔别动
pyenv  121 MB   未加载  不在PATH  python由brew来  最后改动 2024-07  → 残留 ✅可清
```

顺带还能抓到一类没人提的：**同一个版本被两个管理器各存了一份**（作者机器上 `v16.20.2` 在 nvm 和 fnm 里各有一份）。

### 和常见清理工具的差别

| | 常见 Mac 清理器 | env-doctor |
|---|---|---|
| 判断依据 | 目录体积 | **工具身份**（还在不在用） |
| 能否识别「换掉没卸」 | ✗ | ✅ 核心能力 |
| 最大的目录 | 优先建议删 | **可能恰恰不该删**（模型权重） |
| 删除方式 | 确认后批量删 | 逐项勾选，数据类勾不上 |
| 清理后遗症 | 不管 | 提示你清 shell 里的初始化行 |

---

## 30 秒验收

```bash
bash scripts/scan.sh --profile ai-dev    # AI 开发机快扫（只读）
bash scripts/run-all-doctors.sh .        # 三件套（md + skill + env）
```

## 免费 / 付费

| | 免费（开源） | 付费增值 |
|---|---|---|
| 体检 | `scan.sh` 只读扫描 + 文本报告 | 品牌可视化占用图（可选） |
| 清理 | `clean.sh` 交互选择器 | — |
| 联系 | GitHub Issue | **@huiyonghkw** |

## 安装

```bash
git clone https://github.com/huiyonghkw/hekouwang-env-doctor-skill.git \
  ~/.claude/skills/hekouwang-env-doctor-skill
```

装完重开一个 Claude Code 会话即可自动加载，无需任何配置。**零依赖**——只用 `du` / `df` / `grep` 这些系统自带命令，macOS 自带的 bash 3.2 也能跑。

## 用法

在 Claude Code 里直接说：

```
磁盘满了，帮我看看什么占了空间
```

或者直接跑脚本：

```bash
bash scripts/scan.sh              # 体检（只读，全量）
bash scripts/scan.sh --quick      # 体检（只读，快扫）
bash scripts/clean.sh --dry-run   # 清理选择器 · 只演示不执行 ← 第一次建议先跑这个
bash scripts/clean.sh             # 清理选择器 · 勾选后执行
```

体检结果会分成 🟠**残留** / 🟡**缓存** / 🔴**数据** 三组**逐组问你**，每条都带「是什么 / 多大 / 凭什么这么判 / 官方命令 / 代价」。

### 想清理时：交互式选择器

<p align="center">
  <img src="demo/selector.gif?v=2" alt="清理选择器：逐项勾选、数据类锁死、确认后才执行" width="100%">
</p>

`空格`勾选 · `↑↓`移动 · `a`全选 · `n`全不选 · `回车`确认 · `q`退出

## 安全设计

这是个会删东西的工具，所以边界写死在 [`references/safety.md`](references/safety.md) 里：

1. **默认全不选** —— 不存在「一路回车就删光」的可能
2. **数据类 🔒 锁死** —— 模型权重、容器卷、Ollama 模型，按空格也勾不上
3. **只跑白名单里写死的命令** —— 命令与路径固定在数组里，不从任何输入拼装
4. **确认页逐条列出命令与代价，输入 `yes` 才动手**
5. **`--dry-run` 随时可用**
6. **不替你改 `.zshrc`** —— 删完只提示你去清初始化行，自动改配置比删目录更危险

另外：扫描器 `scan.sh` **全文只读**，删除只发生在 `clean.sh` 里；**不联网、不上报**任何扫描结果。

## 覆盖范围

**版本管理器**　nvm · fnm · volta · pyenv · rbenv · rvm · asdf · mise · sdkman · jenv · conda
**包管理器缓存**　npm · yarn · pnpm · bun · pip · uv · cargo · go · maven · gradle
**容器与模拟器**　Docker · CoreSimulator · Xcode DerivedData / iOS DeviceSupport
**AI 模型缓存**　huggingface · ollama · torch

**不覆盖**：系统缓存、照片、邮件、聊天软件——那些交给系统「存储空间」界面。

## 常见问题

**清理命令可靠吗？**　每条都核自官方文档或工具自带 `--help`，来源记在 [`references/rules.md`](references/rules.md) 里。比如 nvm 的卸载法出自它官方 README 的 Manual Uninstall 一节。

**为什么最大的目录反而不建议删？**　作者机器上最大的是 `~/.cache/huggingface`（7.3 GB 模型权重），删了要重下几小时。**按体积排序开刀，第一刀就砍错。**

**判定错了怎么办？**　信号矛盾时它会归入「不确定」组并说明矛盾在哪，不会硬下结论。最终删不删由你勾。

**规则会过期吗？**　会。工具生态每年都在变（nvm→fnm→mise、pip→uv），规则库带版本号，欢迎提 issue 补新工具。

## 结构

```
SKILL.md                 # 路由 + 铁律
scripts/
  scan.sh                # 只读扫描器
  clean.sh               # 清理选择器（唯一允许删除处，白名单驱动）
references/
  rules.md               # 残留特征规则库（工具→目录→判活法→官方命令→代价）
  report.md              # 报告格式与对话流程
  safety.md              # 安全铁律与自检清单
demo/                    # 两段真机实录
```

## 贡献

补新工具的规则最受欢迎。提 PR 时请把五列填齐：**目录 / 身份 / 判活特征 / 官方命令 / 代价**，并注明官方命令的出处（文档链接或 `--help` 输出）。

## 许可

MIT · © 2026 [会勇禾口王的AI笔记](https://hekouwang.pages.dev) [@huiyonghkw](https://github.com/huiyonghkw)

<sub>体检器家族：[claude-md-doctor](https://github.com/huiyonghkw/hekouwang-claude-md-doctor-skill)（体检配置）· [skill-doctor](https://github.com/huiyonghkw/hekouwang-claude-skill-doctor-skill)（体检技能）· **env-doctor**（体检机器）</sub>
