---
name: hekouwang-env-doctor-skill
slug: hekouwang-env-doctor-skill
displayName: 开发环境体检器（env-doctor）
summary: Disk cleanup / dev env doctor / Mac Linux cache scanner — 四信号判「工具还在用吗」，分 数据/缓存/残留。AI dev profile + interactive cleaner. Third of hekouwang-doctor-suite.
license: MIT
homepage: https://github.com/huiyonghkw/hekouwang-env-doctor-skill
version: 1.2.4
allowed-tools: Bash, Read
description: 会勇禾口王 · 开发环境体检器（第三把 doctor）。扫描 Mac/Linux 上被开发工具占掉的磁盘空间，把每个目录判定成「数据 / 缓存 / 残留」三类，重点识别**你已经换掉但从没卸干净的旧工具**（如还留着 nvm 却早就在用 fnm），逐条给出判定依据、官方清理命令与代价。配交互式清理选择器（空格勾选、数据类锁死勾不上、确认后才执行、支持 --dry-run），删什么由你逐项勾。附三件套一键体检 `run-all-doctors.sh`：会调用 claude-md-doctor 与 skill-doctor，额外报告项目配置和技能分数，属附加能力，不是清理前置。触发：用户说「磁盘满了 / 硬盘不够了 / 清理缓存 / 电脑越用越满 / 开发环境体检 / 查查什么占空间 / env-doctor / 环境体检 / disk doctor / 我的 Mac 空间去哪了 / node_modules 太大 / 缓存清理 / 残留清理 / 换过 nvm 想清干净」。任何「查/清 本机磁盘被开发工具占用」的请求都应触发。
---

# 开发环境体检器 · env-doctor

> 「体检器家族」第三把：`claude-md-doctor`（配置）→ `skill-doctor`（技能）→ **`env-doctor`（环境）**。
> 前两把体检文件，这把体检机器。

## 它跟市面清理工具差在哪（先读这条，它决定了全部行为）

市面上的 Mac 清理工具回答的是「**哪个目录大**」。
本器回答的是「**这个工具你还在用吗**」。

体积能扫出来，身份只能推理出来——要判断 nvm 是不是残留，得同时看 shell 配置加载了谁、PATH 里有谁、`node` 实际由谁提供、目录多久没动。**这是本器唯一的差异化，任何改动都不许削弱它。**

---

## ⛔ 三条铁律（细则见 `references/safety.md`）

1. **删除只能来自用户逐项勾选**（走 `scripts/clean.sh`）。**模型自己不拼 `rm` 去跑**；用户说「你直接帮我删」→ 引导他跑选择器。默认全不选、数据类锁死、只跑白名单命令、输入 yes 才动手。
2. **只读扫描**。`scripts/scan.sh` 不含任何写操作。
3. **不确定就说不确定**。信号矛盾时如实标注，不为报告好看而猜。

---

## 标准流程

### 第 1 步 · 扫描

```bash
bash scripts/scan.sh                      # 全量（含家目录大户发现，约 30–60 秒）
bash scripts/scan.sh --quick              # 快扫（跳过发现扫描，约 20 秒）
bash scripts/scan.sh --profile ai-dev     # AI 开发机快扫（Agent 宿主目录 + 跳过大户发现）
```

输出六节原始数据：`DISK` · `SIZES` · `MANAGERS` · `RUNTIME` · `AI_AGENTS`（有 Agent 宿主时）· `DISCOVER`（全量才有）。

### 第 2 步 · 判定

对照 `references/rules.md`：
- **三分法**（数据 / 缓存 / 残留）给每个目录定身份；
- **四信号判定表**（shell_loaded × cmd_in_path × runtime owner × last_modified）判版本管理器是活跃还是残留；
- 同一版本被两个管理器各装一份 → 单列一条提示。

### 第 3 步 · 出报告

按 `references/report.md` 的四步对话流程走：**先给结论 → 分三组呈现（残留→缓存→数据）→ 逐组问用户 → 确认后才生成命令块**。

⚠️ 别把几十行清单一次糊给用户；⚠️ 每条建议必带「是什么 / 多大 / 凭什么判 / 官方命令 / 代价」五要素。

### 第 4 步 · 想清理时，交给选择器

```bash
bash scripts/clean.sh --dry-run   # 先看不执行（第一次强烈建议）
bash scripts/clean.sh             # 勾选后清理
```

交互式勾选：`空格`勾选 · `↑↓`移动 · `a`全选 · `n`全不选 · `回车`确认 · `q`退出。
**数据类带 🔒 锁死勾不上**；确认页逐条列出将执行的命令与代价，输入 `yes` 才动手。

---

## 路由

| 要做什么 | 读哪个 |
|---|---|
| 判定某个目录属于哪一类、官方清理命令是什么 | `references/rules.md` |
| 报告怎么写、对话怎么推进 | `references/report.md` |
| 边界在哪、什么绝对不能做 | `references/safety.md` |
| 扫描器实现与自检 | `scripts/scan.sh` |
| 清理选择器（唯一允许删除处） | `scripts/clean.sh` |

## 常见追问的标准答法

- **「你直接帮我删吧」** → 我不替你按回车。跑 `bash scripts/clean.sh` 勾选，它会先把命令和代价列给你看；想先看不执行就加 `--dry-run`。
- **「最大的那个能删吗」** → 先看身份不看体积。最大的往往是模型权重或容器卷（数据类），恰恰最不该删。
- **「删完会怎样」** → 每条都有「代价」栏；缓存类一律「会重下，费时间和流量」，残留类才是净赚。
- **「为什么判它是残留」** → 报出四信号原文，让用户自己复核。

## 边界

- 只覆盖**开发工具**占用（版本管理器 / 包管理器 / 构建缓存 / 容器 / AI 模型）。系统缓存、照片、邮件附件、微信不在范围内——那些交给系统「存储空间」界面。
- 家目录范围内扫描，不碰系统目录、不碰其他用户。
- 不联网、不上报任何扫描结果。

## 体检器家族互链

| 层 | Skill | 何时转交 |
|---|---|---|
| 配置 | `hekouwang-claude-md-doctor-skill` | `AGENTS.md`/`CLAUDE.md` 重复、路由错、缺 frontmatter |
| 技能 | `hekouwang-claude-skill-doctor-skill` | `SKILL.md` 结构、死链、OpenClaw 声明 |
| 环境 | **本 skill** | 磁盘满、版本管理器残留、AI 宿主目录膨胀 |

报告里若发现配置/技能问题，**点名另外两把**，不要在本报告里硬做文件内容审计。
