<h1 align="center">会勇禾口王·终端工作台</h1>

<p align="center">
  <sub>转化页 · 深手册见 <a href="docs/manual.zh-CN.md">docs/manual.zh-CN.md</a> · Agent 见 <code>SKILL.md</code> / <code>SKILL.lite.md</code></sub>
</p>

<p align="center">
  <b>一份色板，穿透终端和整条命令行工具链。</b><br>
  macOS 终端工作台：7 套出厂主题（3 套社区免费 · 4 套品牌在专业档），外加 Ghostty 自带 463 套导入器。<br>
  装前可预演，换肤可回滚，卸载能还原。英文名 <b>Hekouwang Terminal</b>。
</p>

<p align="center">
  <a href="README.en.md">English</a> · <b>简体中文</b>
  · <a href="https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/index.html?lang=zh"><b>产品主页</b></a>
  · <a href="https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/guide/index.html?lang=zh">文档</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/free-3%20community%20themes-06a88c">
  <img src="https://img.shields.io/badge/7%20factory%20themes-%2B%20463%20imports-6a45e0">
  <img src="https://img.shields.io/badge/license-MIT-00d4aa">
</p>

```bash
git clone https://github.com/huiyonghkw/hekouwang-terminal-lite-skill.git
cd hekouwang-terminal-lite-skill
./scripts/install.sh --dry-run   # 预演：改哪些文件、写哪些设置；确认后去掉 --dry-run 再跑
```

<p align="center">
  <img src="docs/images/cmp-iterm2-free.png" width="49%" alt="免费档：eza、bat、git diff 各用一套配色，也都不跟终端底色搭">
  <img src="docs/images/cmp-iterm2-paid.png" width="49%" alt="专业档：四样东西由同一份色板生成">
</p>

<p align="center"><sub>同一台机器、同一条命令：左＝免费档，右＝专业档</sub></p>

`eza` 列目录、`cat` 看代码、`git diff` 看改动，一条命令都没变。
左边不是「配色难看」——Monokai 是经典，delta 的红绿是出厂设置；问题是三个工具各说各话，还都跟终端底色不搭。
右边四样东西出自同一份色板，所以是一家人。

只用 iTerm2，免费版就够；想让 `ls` / `cat` / `git diff` 也跟着终端同色，见第七节。

---

## 一、你可能正卡在这里

用上 Claude Code 这类 CLI agent 之后，我每天泡在终端里的时间翻了倍。
以前终端是敲两条命令就切走的地方；现在它是我和 AI 一起干活的主界面——
四个 tab 同时跑四个任务，输出哗哗往上刷，我得一眼看出哪个报错了、哪个跑完了、哪个还在转。

原来那套用了五年的配置，是给「敲命令」设计的，不是给「看 AI 干活」设计的：

- 四个 tab 长得一模一样，切过去半天认不出哪个在跑什么
- agent 吐几百行日志，`ERROR` 和正常输出一个颜色，全靠肉眼扫
- 想给 AI 写个多行 prompt，回车直接就提交了
- 白天靠窗、开会投屏，一片深色底什么都看不清
- 好不容易调顺手，换台电脑全没了

这套配置就是冲着这些场景长的：**凡是能用 AI 干的活，我先跑通，再写进脚本**——
它是我每天在用的那一套，不是演示机。

Triggers 随 Profile 交付 4 条规则：`ERROR` / `WARN` / `SUCCESS` 分别标色，`Password:` 直接弹 iTerm2 密码管理器。

## 二、它不是又一个 dotfiles

1. **可测量，不靠眼缘** —— 对比度、diff 明度差、色盲分离都是生成期约束，不是事后调色。`./scripts/theme.sh --audit` 随时可复跑。
2. **换肤可回滚** —— `--plan` 先列出会改哪些文件，一个字节都不写；写入失败自动还原；留 5 份快照，`--rollback` 退回上一步。
3. **一份色板 fan-out** —— 换肤不动 `.zshrc`：所有工具固定读 `current/`，换主题只是换这个目录的内容。
4. **字体光学校准**〔付费〕 —— 读字体表算字格偏差，验中文字符（U+4E00）是不是正好两格宽。不是「装个 Nerd Font」就算完。
5. **它本身是一个 Agent Skill** —— 你说「换成亮色」「终端怎么这么慢」，Agent 自己挑脚本、执行、解释结果。免费版带基础 Skill，专业版带完整版。

一份色板走出去，长这样（除 iTerm2 外均为专业档）：

```text
config/themes/palettes/brand.py        一份色板：16 个 ANSI 槽 + 语义表面
        ├─ iTerm2 / Ghostty / Terminal.app      全量 7 套
        ├─ Warp / Tabby                          5/7
        ├─ cmux                                  侧栏底色
        └─ bat / fzf / eza / delta / tmux / VS Code
```

## 三、证据

### 7 套出厂主题

| 主题 | 底色 | 档位 |
|---|---|---|
| Catppuccin Mocha | 暗 | 免费 |
| Tokyo Night | 暗 | 免费 |
| Gruvbox Dark | 暗 | 免费 |
| 暖烬 Ember | 暗 | 付费 |
| 霓虹电压 Voltage | 暗 | 付费 |
| 暖纸 Parchment | 亮 | 付费 |
| 账簿 Ledger | 亮 | 付费 |

导入器另算：Ghostty 自带 463 套配色，导进来之后同一套色会铺到上面整条链〔付费〕。

### 终端覆盖

| 终端 | 7 套覆盖 | 说明 |
|---|---|---|
| iTerm2 | 7/7 | 免费档的默认目标，Dynamic Profile 保存即生效 |
| Ghostty | 7/7 | 配置即文件，重载即生效 |
| Terminal.app | 7/7 | 导出 `.terminal` 描述文件 |
| Warp | 5/7 | 缺 Catppuccin Mocha、Tokyo Night：Warp 的主题 YAML 色槽表达不了这两套 |
| Tabby | 5/7 | 同上 |
| cmux | 侧栏 | 终端渲染走 Ghostty，会勇禾口王·终端工作台只改侧栏底色 |

缺口如实标出：与其硬凑一套看起来像、实际会漂的，不如把边界写清楚。
免费版只覆盖 iTerm2 上的 3 套社区配色，表里其余组合都属于专业档。

### 审计门槛

`./scripts/theme.sh --audit` 跑的是写进生成器的约束，不是人工看一眼：

| 检查 | 门槛 |
|---|---|
| 正文槽 1–6 对背景 | ≥ 4.5:1（WCAG AA） |
| 强调槽 9–14 对背景 | ≥ 6.0:1 |
| 暗字槽 8 对背景 | ≥ 3.0:1 |
| diff 新增 / 删除底明度差 | ΔL ≥ 0.025，灰度下也分得开 |
| 红绿在色盲模拟下 | ΔE ≥ 0.03 |
| 中性梯 surface / overlay / border | 1.12 / 1.22 / 1.35，且 fg 对 surface ≥ 4.5:1 |

<p align="center">
  <img src="docs/images/doctor-status.webp" width="82%" alt="doctor.sh --status：theme / auto / node / optical / scene / semantic">
</p>

> `./scripts/doctor.sh --status` 一眼看钉住了什么。完整体检跑 `./scripts/doctor.sh`；Lite 缺的付费件会标成专业档，不是装坏了。

## 四、免费版给什么

免费版不是演示版：缺的只有主题数和覆盖面，脚本一个不少。

- **3 套社区配色**：Catppuccin Mocha / Tokyo Night / Gruvbox Dark
- **Minimal 外观**：无标题栏、无边框、无滚动条 + 毛玻璃，安装脚本用 `defaults write` 写好
- **日志染色**：`ERROR` / `WARN` / `SUCCESS` / `Password:` 四条 Triggers 规则随 Profile 交付
- **语义 Cmd-click**：`path:line`、Git SHA、`localhost:port` 点一下就开
- **Shift+Enter 换行不提交**：给 AI 写多行 prompt 用
- **现代 CLI 全家桶**：eza / bat / delta / fzf / zoxide / atuin / starship
- **能自己修的体检**：`doctor.sh --status` / `--fix` / `--profile`
- **安全装卸**：`install.sh --dry-run`、`migrate.sh` 搬旧配置、`uninstall.sh` 从备份还原
- **基础 Skill**：安装 / 换肤 / 体检 / 同步 / 卸载，交给 Agent 执行

## 五、安装

前置：一台 Mac（Apple 芯片或 Intel）、能联网、会在「终端」里复制粘贴。

| 你的情况 | 用哪个 |
|---|---|
| 新 Mac，或没有自定义 `~/.zshrc` | `HKW_ASSUME_YES=1 ./scripts/install.sh` |
| 已经在用自己的 `.zshrc` | 先 `./scripts/migrate.sh` |

`install.sh` 会覆盖 `~/.zshrc`（先备份）。用了多年的配置走迁移：alias / PATH 搬进 `~/.zshrc.local`，再套模板。

装 Homebrew / oh-my-zsh 时，脚本先把官方安装脚本下载到临时文件并打印 SHA-256，**默认不执行**；确认来源后加 `HKW_ASSUME_YES=1` 才自动跑完。

```bash
git clone https://github.com/huiyonghkw/hekouwang-terminal-lite-skill.git
cd hekouwang-terminal-lite-skill

./scripts/migrate.sh             # 只看报告
./scripts/migrate.sh --apply     # 确认后再执行

./scripts/install.sh --dry-run   # 先看：改哪些文件、写哪些设置、什么绝对不碰
HKW_ASSUME_YES=1 ./scripts/install.sh
```

国内网络卡在 `portable-ruby` / `SSL_ERROR_SYSCALL`：

```bash
CN=1 HKW_ASSUME_YES=1 ./scripts/install.sh
```

顺序大致是：Homebrew → iTerm2 + 字体 → CLI → oh-my-zsh → 主题（全生态同色属专业档）→ `.zshrc` → GUI 三项设置 → 自检。
脚本幂等，重跑安全；跑完会打印「全部完成」，并自动跑一遍 `doctor.sh`。

**回滚**：`~/.zshrc` 先备份进 `~/.hekouwang-terminal-backups/`；`./scripts/uninstall.sh --dry-run` 看要还原什么，再执行 `./scripts/uninstall.sh`。

## 六、每天用到的命令

| 工具 | 一句话 | 怎么用 |
|---|---|---|
| **starship** | 提示符：目录 / git 分支 / 上条命令耗时 | 自动 |
| **eza** | 带图标的文件列表 | 直接敲 `ls` |
| **bat** | 高亮 + 行号的 `cat` | 直接敲 `cat 文件名` |
| **delta** | 带语法高亮的 diff | 直接敲 `git diff` |
| **fzf** | 模糊搜一切 | `Ctrl+T` 搜文件，`Alt+C` 跳目录 |
| **zoxide** | 一个词跳目录 | `z 关键词` |
| **atuin** | 全文搜历史 | `Ctrl+R` |

给 AI 用的一条：**`Shift + Enter` 换行不提交**。

语义层：`Cmd-click` `path:line` 打开编辑器，`Cmd-click` Git SHA 看 `git show`，`Cmd-click` `localhost:3000` 开浏览器。

全部快捷键 → [`references/shortcuts.md`](references/shortcuts.md)

## 七、专业版给什么

| | 免费版（MIT） | 专业版 |
|---|---|---|
| 主题 | 3 套社区配色 | + 4 套品牌（2 套亮色）+ 导入器（Ghostty 自带 463 套） |
| 终端 | iTerm2 | iTerm2 / Ghostty / Terminal.app 全量 7 套；Warp / Tabby 5/7；cmux 侧栏 |
| 工具链 | — | bat / fzf / eza / delta / tmux / VS Code 同色 |
| 光学校准 | — | 字格偏差 + 中文两格宽，三档密度 |
| 场景 | — | 日常 / 专注 / 投屏 / 录屏 / 远程 |
| 工作区 | — | `cd` 进项目，tab 自动换色并印项目名 |
| 跟随系统深浅色 | — | 专业版支持 |
| Skill | 基础版 | 完整版 |
| 更新与答疑 | GitHub Issues | 一年内更新 + 群内答疑 |

**专业版 3.0.5**：支付宝 [SkillPay](https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/index.html?lang=zh) 按季度订阅（¥14.9/季度，不自动续费，约 ¥59.6/年）· 腾讯 SkillHub 按次（¥2.99/次）。购买只走平台渠道，详见 [产品主页](https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/index.html?lang=zh)。

## 八、维护

```bash
./scripts/doctor.sh            # 体检（第 0 节是状态机仪表盘）
./scripts/doctor.sh --status   # 只看仪表盘：主题 / 跟随 / Node / 光学 / 场景 / 语义 / 视觉 / Ghostty 重载
./scripts/doctor.sh --parity   # 源色板一致性验收（只读）
./scripts/doctor.sh --fix      # 逐项确认后自动修，不批量执行
./scripts/doctor.sh --profile  # 启动慢？点名是哪个插件

./scripts/update.sh            # 更新（git 安装）
./scripts/sync.sh              # 换机迁移

./scripts/uninstall.sh         # 从备份还原 + GUI 恢复出厂
./scripts/uninstall.sh --dry-run
```

个人 alias / PATH 写进 `~/.zshrc.local`（模板会自动加载），别改会被覆盖的模板段。

## 九、限制、FAQ 与许可

- **Warp / Tabby 只有 5/7**：缺 Catppuccin Mocha、Tokyo Night，原因是主题 YAML 的色槽表达限制，不是漏做。
- **cmux 只跟侧栏**：终端渲染本身走 Ghostty，会勇禾口王·终端工作台不接管。
- **只支持 macOS**：iTerm2 / Ghostty / Terminal.app 都是 macOS 应用。
- **字体要自己装**：仓库不分发字体文件。缺 Nerd Font 图标会显示成 `?`，装一个 Nerd Font 就好。
- **`cat` 的颜色单独生效**：bat 认不出主题时**不报错**，会静默用自己的默认配色——表现为「终端、fzf、git diff 都对，只有 `cat` 是另一套」。第一次切主题会停几秒建缓存，别打断。
- **`cat file | head` 验色不准**：管道会让 bat 退回纯文本模式，直接 `cat file` 才作数。
- **导入的主题只在你机器上**：`import.sh` 导入的配色不进产品包，也不会随更新分发。
- **工作区依赖 Shell Integration**：项目 tab 自动换色靠 iTerm2 的 APS 按路径切。

完整 FAQ、tmux `-CC`、Triggers、Shell Integration → [`docs/manual.zh-CN.md`](docs/manual.zh-CN.md)（English: [`docs/manual.md`](docs/manual.md)）。
文档站：[安装](https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/guide/install.html?lang=zh) · [换肤](https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/guide/theme.html?lang=zh) · [终端覆盖](https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/guide/terminals.html?lang=zh) · [语义层](https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/guide/semantic.html?lang=zh) · [体检](https://huiyonghkw.github.io/hekouwang-terminal-lite-skill/guide/doctor.html?lang=zh)

| 其他 | 去哪 |
|---|---|
| 快捷键 | [`references/shortcuts.md`](references/shortcuts.md) |
| 更新记录 | [`CHANGELOG.md`](CHANGELOG.md) |
| English | [`README.en.md`](README.en.md) |

### 许可

免费版 [MIT](LICENSE.txt)：随便用、随便改、商用也行。付费件另见付费包内的授权说明。
