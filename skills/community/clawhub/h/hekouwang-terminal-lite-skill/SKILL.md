---
name: hekouwang-terminal-lite-skill
description: "会勇禾口王·终端工作台（免费版）/ Hekouwang Terminal Lite：安装或迁移 macOS 终端与 .zshrc；安装会联网——Homebrew、oh-my-zsh、iTerm2 Shell Integration 的官方安装脚本先下载到临时文件并打印 SHA-256，只有 HKW_ASSUME_YES=1 时才自动执行；Homebrew / oh-my-zsh 未装成会中止，Shell Integration 未执行时保留下载文件并继续后续 defaults / GUI 设置 / 自检；用 brew 安装 iTerm2、字体与命令行包，并把实际装上的包记到 ~/.config/hekouwang-terminal/installed-brew.txt；写系统级 defaults（ApplePressAndHoldEnabled）、iTerm2 偏好与 ~/.config/ghostty/config（非本工具生成的文件先备份），Ghostty 的 ssh-terminfo 会在首次 SSH 登录时往远端 ~/.terminfo 写 xterm-ghostty；向 ~/.gitconfig 追加 include.path，覆盖 ~/.config/starship.toml 前先备份；可选把已有 shell 历史导入 atuin（HKW_ATUIN_IMPORT=1，默认不导入）；检测到 VS Code / Cursor 时安装本工具的主题扩展，并替换同名的本工具旧版本目录；update.sh 在 git 安装下 fetch/pull（本地改动先 stash）并重跑更新后的生成器与 theme.sh，非 git 安装直接跳过；社区主题换肤与事务回滚（theme.sh --plan/--rollback）、doctor（全量体检为测启动耗时会多次以交互式 zsh 加载 ~/.zshrc；--status 跳过该段；--fix 逐项确认后执行修复命令；--profile 用临时 ZDOTDIR 的交互式 zsh 再加载 ~/.zshrc 做 zprof 取样）、CLI diff、换机迁移（sync.sh --export/--state-export/--state-import，--pull 按仓库重新部署）、卸载（交互模式先询问再删除/还原，--yes 跳过确认；从备份还原 ~/.zshrc，还原或删除 starship.toml 与 Ghostty config，删 Ghostty/bat 主题、VS Code/Cursor 主题扩展、iTerm2 与 macOS 终端 Profile、~/.oh-my-zsh 与运行时；brew 包只按安装清单卸）；可选安装专业版付费包（unlock.sh）；P3 广色域（--p3，读 HKW_P3_FACTOR）；AI CLI 主题检测与 --apply：只处理你用 --config <路径> 显式传入的设置文件，只改其中的 theme 字段并先备份，本技能不探测任何 CLI 配置目录。多终端批量编排、光学校准、场景、工作区、色板推导、跟随系统深浅色在专业版 hekouwang-terminal-skill。不用于与终端配色无关的普通编码。"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
metadata:
  version: 3.0.6
  displayName: 会勇禾口王·终端工作台（免费版）
  openclaw:
    requires:
      bins:
        - bash
        - zsh
        - python3
        - curl
        - git
      env:
        - HKW_P3_FACTOR
---

# 会勇禾口王·终端工作台（免费版）

> **定位**：免费版 Agent 操作协议。人类看 [`README.md`](README.md)；深手册看 [`docs/manual.zh-CN.md`](docs/manual.zh-CN.md)。
> **英文名**：Hekouwang Terminal Lite · Skill 名：`hekouwang-terminal-lite-skill`
> **专业版**：`hekouwang-terminal-skill`（另一名字，装一个不会覆盖另一个）。

`<skill>` = 本文件所在目录。

## Agent 协议

1. 先 `./scripts/doctor.sh --status`（跳过启动耗时取样）；已有自定义 `.zshrc` 先 `./scripts/migrate.sh`，禁止直接 `./scripts/install.sh`。全量 doctor（无 `--status`）为测启动耗时会多次以交互式 zsh 加载 `~/.zshrc`；`--profile` 再用临时 `ZDOTDIR` 的交互式 zsh 做 zprof。
2. 换肤先 `./scripts/theme.sh --plan <name>`；写操作须用户明确要求。
3. 改色板只改源再生成；禁手改生成物。
4. Node 管理器只留一个。
5. **本包是免费版**：不要承诺多终端批量编排、光学校准、场景、工作区、色板推导、跟随系统深浅色；那些能力在专业版里，本包没有对应命令。
6. `install.sh` 默认只下载 Homebrew / oh-my-zsh / Shell Integration 安装脚本并打印 SHA-256；用户明确同意联网执行时才加 `HKW_ASSUME_YES=1`。Homebrew / oh-my-zsh 未装成会中止；Shell Integration 未执行时保留下载文件并继续后续步骤。

## 免费版有什么

- iTerm2：3 套社区主题、毛玻璃、Triggers、语义 Cmd-click、Shift+Enter
- 安装 / 迁移 / 卸载 / doctor / sync / update / node-mgr / setup-gui / setup-cli
- `./scripts/theme.sh`：iTerm2 换肤 / 画廊 / 预览 / audit / P3
- `./scripts/unlock.sh`：把专业版 zip 解压覆盖进本树

专业版能力缺席时，生成器仍出完整 iTerm2 主题，多终端行显示跳过——不报错、不留半成品。

专业版文件不在本树；`scripts/theme.sh` / `scripts/doctor.sh` 里对专业版引擎的引用是存在性检测，缺失时静默跳过。

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/doctor.sh` | `--status` / `--parity` / `--profile` / `--fix` |
| `scripts/install.sh` / `scripts/migrate.sh` / `scripts/uninstall.sh` | 装 / 接管 / 卸（先 dry-run） |
| `scripts/theme.sh` | iTerm2 换肤；`--plan` / `--preview` / `--gallery` / `--audit` / `--rollback` / `--p3` |
| `scripts/node-mgr.sh` / `scripts/setup-gui.sh` / `scripts/setup-cli.sh` | Node；GUI；AI CLI diff（`--config <设置文件>` 显式传入） |
| `scripts/sync.sh` / `scripts/update.sh` / `scripts/unlock.sh` | 换机状态导出/导入；更新；装专业版 zip |

## 常用命令

```bash
./scripts/install.sh --dry-run && HKW_ASSUME_YES=1 ./scripts/install.sh
./scripts/migrate.sh && ./scripts/migrate.sh --apply
./scripts/theme.sh --plan tokyo-night && ./scripts/theme.sh tokyo-night
./scripts/setup-cli.sh --config <设置文件路径> --check
./scripts/doctor.sh --status
./scripts/uninstall.sh --dry-run
```

## 语言与文档层

站点 / README 默认中文。CLI 默认英文；`--lang zh` 可切。Agent 只读本协议；不要把 README 营销段复述成能力承诺。
