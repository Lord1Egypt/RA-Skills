---
name: hekouwang-env-doctor-skill
slug: hekouwang-env-doctor-skill
displayName: 开发环境体检器（env-doctor）
summary: Disk cleanup / dev env doctor / Mac Linux cache scanner — 四信号判「工具还在用吗」，分 数据/缓存/残留。AI dev profile + interactive cleaner. Third of hekouwang-doctor-suite.
license: MIT
homepage: https://github.com/huiyonghkw/hekouwang-env-doctor-skill
version: 1.3.0
allowed-tools: Bash, Read
description: "开发环境与磁盘体检：默认只读扫描（不读用户文档内容、不联网、不上报），按数据/缓存/残留三分法给出判定与官方清理建议。clean 子命令只跑各工具官方的缓存与旧版本清理命令（npm、yarn、pnpm、brew、pip、uv），逐项确认后执行；不删除版本管理器目录、不删模型权重与容器数据；被判为残留的版本管理器只在报告里给手动卸载步骤。附 scripts/run-all-doctors.sh：会调用 claude-md-doctor 与 skill-doctor，额外报告配置与技能分数，属附加能力。"
---

# 开发环境体检器 · env-doctor

> 「体检器家族」第三把：`claude-md-doctor`（配置）→ `skill-doctor`（技能）→ **`env-doctor`（环境）**。
> 前两把体检文件，这把体检机器。

## 它跟市面清理工具差在哪（先读这条，它决定了全部行为）

市面上的 Mac 清理工具回答的是「**哪个目录大**」。
本器回答的是「**这个工具你还在用吗**」。

体积能扫出来，身份只能推理出来——要判断 nvm 是不是残留，得同时看 shell 配置加载了谁、PATH 里有谁、`node` 实际由谁提供、目录多久没动。**这是本器唯一的差异化，任何改动都不许削弱它。**

---

## ⛔ 四条铁律（细则见 `references/safety.md`）

1. **清理只能来自用户逐项勾选**（走 `scripts/clean.sh`）。**模型自己不拼 `rm` 去跑**；用户说「你直接帮我删」→ 引导他跑选择器。默认全不选、数据类锁死、只跑白名单命令、输入 yes 才动手。
2. **清理器只跑官方缓存命令**。`clean.sh` 不删除用户目录——唯一的 `rm -r` 只用于清理它自己创建的临时目录；不删版本管理器目录（`~/.nvm`、`~/.pyenv`、`~/.rbenv`、`~/.asdf`、`~/.volta` 等），不删模型权重与容器数据，也不改 shell 配置。残留版本管理器由报告给手动卸载步骤，用户自己执行。
3. **只读扫描**。`scripts/scan.sh` 不含任何写操作。
4. **不确定就说不确定**。信号矛盾时如实标注，不为报告好看而猜。

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

按 `references/report.md` 的四步对话流程走：**先给结论 → 分三组呈现（残留→缓存→数据）→ 逐组问用户 → 确认后缓存交给选择器、残留给手动步骤**。

⚠️ 别把几十行清单一次糊给用户；⚠️ 每条建议必带「是什么 / 多大 / 凭什么判 / 官方命令 / 代价」五要素。

### 第 4 步 · 想清缓存时，交给选择器

```bash
bash scripts/clean.sh --dry-run   # 先看不执行（第一次强烈建议）
bash scripts/clean.sh             # 勾选后清理
```

交互式勾选：`空格`勾选 · `↑↓`移动 · `a`全选 · `n`全不选 · `回车`确认 · `q`退出。
**数据类带 🔒 锁死勾不上**；可勾选的只有有官方清理子命令的缓存项（npm / yarn / pnpm / brew / pip / uv），数据类照列但锁死。
确认页逐条列出命令与代价，输入 `yes` 才动手；执行时每项再打印路径单独确认一次。

**残留的版本管理器不进选择器**：报告里给出官方手动步骤（见 `references/rules.md` 第二节），由用户自己执行；提醒他同步清理 shell 初始化行。

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
- **「删完会怎样」** → 每条都有「代价」栏；缓存类一律「会重下，费时间和流量」。
- **「残留的 nvm 你怎么不帮我清」** → 版本管理器整目录不在选择器范围内（会连已装版本、环境一起删）。报告给官方手动步骤，你确认后自己执行，记得同步删 shell 初始化行。
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
