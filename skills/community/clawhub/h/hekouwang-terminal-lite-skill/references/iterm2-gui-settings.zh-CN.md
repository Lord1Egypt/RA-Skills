# iTerm2 GUI 设置清单 + 高级功能

> [English](iterm2-gui-settings.md) · **简体中文**

> **这三件事现在已由 `setup-gui.sh` 自动写好（install.sh 会调用它），通常不用手点。**
> 本节保留手动步骤作为：① 自动化没生效时的兜底；② 想理解每项在改什么。
> 验证是否写好：跑 `./scripts/doctor.sh` 第 4 节。打开设置面板：`Cmd+,`
>
> `setup-gui.sh` 用 `defaults write` 写这三项（外加去窗口边框、单 tab 隐藏 tab bar）：
> `TabStyleWithAutomaticOption=5`（Minimal）、`Default Bookmark Guid`（默认 Profile）、
> `GlobalKeyMap` 加 Shift+Enter 换行（新旧两种键映射格式都写）。
> ⚠️ 写之前会先退出 iTerm2（否则写入会被 iTerm2 退出时覆盖），写完别 `killall cfprefsd`（会丢未落盘的写入）。

## 一、必做三件事（已自动，手动为兜底）⭐

### 1. Minimal 主题

`Settings → Appearance → General → Theme` → **Minimal**

标签栏与终端背景融合、去掉灰色标题栏，整窗一块纯色画布。同面板顺手设：

| 项 | 位置 | 值 |
|---|---|---|
| 全屏显示标签栏 | Appearance → Tabs | ✅ Show tab bar in fullscreen |
| 单标签隐藏标签栏 | Appearance → Tabs | ✅ hide tab bar when there is only one tab |
| 新输出指示 | Appearance → Tabs | ✅ Show "new output" indicator |
| 窗口边框 | Appearance → Windows | ❌ Show border around window |

### 2. 设默认 Profile

install.sh 已把 `hekouwang-active-theme.json` 放入 DynamicProfiles 目录（保存即生效，无需重启）。
`Settings → Profiles` → 选中那个带 **Dynamic** 标签的 Profile → `Other Actions... → Set as Default`

### 3. Shift+Enter 换行（AI CLI 必备）

`Settings → Keys → Key Bindings → +`

| 字段 | 值 |
|---|---|
| Keyboard Shortcut | 按 `Shift+Enter` |
| Action | **Send Text** |
| 文本 | `\n` |

用途：Claude Code 等 AI CLI 中 `Enter` 提交、`Shift+Enter` 换行——和聊天软件一致的肌肉记忆。

## 二、Dynamic Profile 详解（配置即代码 ⭐ 核心理念）

Profile 不在 GUI 手点，用 JSON 管理，放进：

```
~/Library/Application Support/iTerm2/DynamicProfiles/
```

四大优点：① 保存即生效（iTerm2 监听目录）② 可版本管理，换机拷一个文件 ③ 自包含 ④ 复制改 Guid 换色值即新主题。

关键字段（完整文件见 `config/themes/ember.json`，每套主题结构相同）：

```jsonc
{
  "Profiles": [{
    "Name": "hekouwang · Ember",
    "Guid": "catppuccin-mocha-dynamic-2026",  // 必须唯一且稳定
    "Normal Font": "OperatorMono-Book 14",     // 主字体（可换 JetBrainsMono-Regular 14）
    "Non Ascii Font": "SymbolsNFM 14",         // Nerd Font 图标兜底
    "Use Non-ASCII Font": true,                // ⚠️ 少这行图标兜底不生效
    "Unlimited Scrollback": true,
    "Silence Bell": true
  }]
}
```

> ⚠️ **踩坑**：不要用 `"Dynamic Profile Parent Name"` 继承字体——父 Profile 一旦被删，
> 字体静默回退系统默认，重启后满屏细体小字。关键设置直接写进 JSON。

**字体策略**：「优雅主字体 + Symbols Nerd Font 兜底」。主字体不必是 Nerd 补丁版，
图标交给 `font-symbols-only-nerd-font` 专职渲染，换主字体永远不缺字。

## 三、可选 GUI 微调

| 路径 | 项 | 值 | 为什么 |
|---|---|---|---|
| Profiles → Terminal | Unlimited scrollback | ✅ | 回滚不丢，`Cmd+F` 变全文检索 |
| Profiles → Terminal | Silence bell + Flash visual bell | ✅ | 静音改视觉闪烁 |
| Profiles → General | Working Directory | 你的工作区 | 新窗口直达 |
| General → Startup | Window restoration | Only Restore Hotkey Window | 不恢复一堆旧窗口 |
| General → Selection | Copy to pasteboard on selection | ✅ | 选中即复制 |
| General → Selection | Triple-click selects wrapped lines | ✅ | 三击选整行含折行 |
| Profiles → Text | Cursor: Vertical bar, 不闪烁 | — | 光标稳定 |

系统级（vim 党刚需，长按按键连续重复而非弹重音菜单）：

```bash
defaults write -g ApplePressAndHoldEnabled -bool false
```

## 四、高级功能

### 4.1 Shell Integration（官方增强）

```bash
# 官方脚本，执行前可先审阅
curl -L -o /tmp/iterm2-shell-integration.sh https://iterm2.com/shell_integration/install_shell_integration_and_utilities.sh
# 已保存到：/tmp/iterm2-shell-integration.sh
bash /tmp/iterm2-shell-integration.sh
```

| 能力 | 用法 |
|---|---|
| 命令块导航 | `Cmd+Shift+↑/↓` 在命令输出间跳转 |
| 命令状态标记 | 每条命令左侧小三角，失败标红 |
| 终端内看图 | `imgcat 图片.png` |
| 远程复制 | SSH 远程机上 `it2copy` 直进本地剪贴板 |
| 下载/上传 | `it2dl 文件` / 拖拽上传 |
| 脚本换肤 | `it2setcolor preset "Snazzy"` |

### 4.2 Hotkey Window（系统级下拉终端）

`Settings → Keys → Hotkey → Create a Dedicated Hotkey Window...`
热键建议 `Opt+Space`：任何应用里一按，终端从屏幕顶部滑下，再按收回。
可在该 Profile 的 Window 设置里加轻微透明 + Blur。

### 4.3 tmux 集成模式（iTerm2 独家）⭐ SSH 重度用户必备

先装：`brew install tmux`（已纳入 install.sh 的 CLI 全家桶 / doctor.sh 检查项）。

**核心价值**：`-CC` 控制模式下，tmux 的 window/pane 映射成**原生** iTerm2 tab/分屏（不是字符画，鼠标、滚动、复制全部原生）。SSH 断线/合盖/换网络，**远程会话不丢**，重连原样恢复——服务器上跑长任务时这是救命功能。

```bash
# 本地起一个集成会话
tmux -CC
# 远程：有就接管、没有就新建（断线重连不丢会话）
ssh server -t 'tmux -CC attach || tmux -CC'
# 指定会话名（多个项目分开，重连点名接）
ssh server -t 'tmux -CC new -A -s deploy'
```

**用法备注（最常用的就这几条）**：

| 操作 | 怎么做 |
|---|---|
| 新建 window（= 新 tab） | `Cmd+T`（原生 iTerm2 快捷键直接生效） |
| 分屏 | `Cmd+D` / `Cmd+Shift+D`（同原生） |
| 临时脱离会话（让它后台继续跑） | 关掉那个 iTerm2 窗口即可，或 tmux 前缀 `Ctrl+B` 然后 `d` |
| 重新接回 | 再跑一次上面的 `tmux -CC attach`（远程则连 SSH 再 attach） |
| 看有哪些会话 | 远程上 `tmux ls` |
| 彻底结束会话 | 会话里 `exit` 退完所有 window，或 `tmux kill-session -t 名字` |

> ⚠️ 注意：`-CC` 集成模式下不要再用 tmux 自己的 `Ctrl+B %` / `Ctrl+B "` 分屏——交给 iTerm2 的 `Cmd+D` 即可，前缀键基本只在 `Ctrl+B d`（脱离）时才用得上。

**给 SSH 别名加 tmux**（可选，写进 `~/.zshrc.local`）：把常断线、常跑长任务的机器别名末尾加上 `-t 'tmux -CC new -A -s main'`，以后一连就进持久会话。例如：

```bash
# ~/.zshrc.local —— 持久会话版别名（断线重连不丢）
alias ecs:prod:web="ssh -o ServerAliveInterval=60 -t root@<你的服务器IP> 'tmux -CC new -A -s main'"
```

> ⚠️ **先确认远程装了 tmux 再改别名**。否则一连就甩 `command not found: tmux`。
> 远程装 tmux：`apt install tmux`（Debian/Ubuntu）或 `yum install tmux`（CentOS/RHEL）。
> 不确定哪些机器有、又想一把改全部时，用带回退的写法——没 tmux 时自动退成普通登录 shell，不报错：
>
> ```bash
> alias ecs:prod:web="ssh -o ServerAliveInterval=60 -t root@<你的服务器IP> 'tmux -CC new -A -s main || exec \$SHELL -l'"
> ```
>
> 注意 `\$SHELL` 要转义，确保发到远程才展开。另外 `-CC` 是 iTerm2 独家，别名在 VS Code 终端等其它 App 里只会以普通 tmux 模式起，不映射成原生 tab。

> ⚠️ **和 Claude Code 的 fullscreen 模式冲突（2026-07 官方明确）**：如果你在 `-CC` 会话里开了 Claude Code 的**全屏渲染**（`/tui fullscreen`，是 opt-in 预览功能），会出问题——**滚轮失灵、双击可能损坏终端状态**。原因：`-CC` 下 iTerm2 把每个 pane 渲染成原生 split、不让 tmux 自己画，这跟全屏程序要的 alternate screen buffer 打架。
> - **官方原话**：*"Fullscreen rendering is incompatible with iTerm2's tmux integration mode... Don't enable fullscreen rendering in `tmux -CC` sessions."*（[code.claude.com/docs/en/fullscreen](https://code.claude.com/docs/en/fullscreen)）
> - **别慌，影响面很窄**：① 只针对 fullscreen **预览**功能；Claude Code **默认的 classic renderer 不受影响**，`-CC` 照常用。② 官方称**普通 tmux（不带 `-CC`）在 iTerm2 里正常**——但这是厂商口径，个别版本（issue #58364）报过普通模式也有滚轮/scrollback 小毛病，遇到再说。
> - **结论**：跑 Claude Code 时想用它的全屏预览，就**别在 `-CC` 会话里跑**——要么用默认渲染器 + `-CC`，要么全屏模式 + 不带 `-CC` 的普通 tmux（或不套 tmux）。日常 SSH 保命用 `-CC` 依旧是招牌功能，不受影响。

### 4.4 Triggers（输出触发自动化）⭐ 已默认随 Profile 交付

**这 4 条已经写进主题 Profile JSON，跟着 `install.sh` / `theme.sh` 自动交付，不用手点 GUI。**
`doctor.sh` 第 3 节会体检在不在；想看/改去 `Settings → Profiles → Advanced → Triggers → Edit`。

| 正则（节选） | Action | 效果 |
|---|---|---|
| `\b(ERROR\|FATAL\|FAILED\|PANIC\|Exception)\b` | HighlightTrigger 错误表面 | 日志错误词走主题的语义错误底（文字 ≥4.5:1） |
| `\b(WARN\|WARNING\|DEPRECATED\|TODO\|FIXME)\b` | HighlightTrigger 警告表面 | 警告/待办走语义警告底 |
| `\b(SUCCESS\|SUCCEEDED\|SUCCESSFUL\|PASSED)\b` | HighlightTrigger 成功表面 | 成功词走语义成功底 |
| `…[Pp]assword…:` | PasswordTrigger（Instant） | 密码提示自动弹密码管理器 |

> ⚠️ 正则区分大小写：只标 **大写** 的 `ERROR`/`WARNING`/`SUCCEEDED` 等（日志惯例），
> 避免把正文里的小写 "error"、"0 warnings" 也染色造成噪音。

**实现要点（配置即代码，写在 `config/themes/_generate.py` 的 `triggers()`）**：

- 高亮配色用 Dynamic Profile 专用简写 `{#前景,#背景}`（[官方文档](https://iterm2.com/documentation-dynamic-profiles.html)），
  背景是**解算出来的语义表面**（`error_bg` / `warn_bg` / `success_bg`），不再是 raw ANSI 红黄绿；
  文字色保证 ≥4.5:1，所以 `./scripts/theme.sh` 换肤时标注色自动跟着变。
- `action` 就是 iTerm2 的 trigger 类名：`HighlightTrigger` / `PasswordTrigger`。
- `partial:true` 即 GUI 里的 **Instant**（不等换行就触发）；密码提示行没有换行，必须 Instant。
- 改触发规则：编辑 `triggers()` → `cd config/themes && python3 _generate.py` → `./scripts/theme.sh <当前主题>` → **新开一个 tab** 生效（Triggers 只对新会话生效，老 tab 不变）。

> 为什么不做「长任务完成弹系统通知」：macOS 真实通知版式固定，iTerm2 自带的 Post Notification
> 会硬塞一行删不掉的 `A trigger fired in session…`；换 `terminal-notifier` 既要多装依赖、又要手动
> 放行「触发器运行命令」，实测也不好看。权衡下来不收录，保持这 4 条干净可靠。

### 4.4b 语义交互层 v1 ⭐ 已默认随 Profile 交付

**Smart Selection + Semantic History** —— 同样由 `_generate.py` 的 `smart_selection_rules()` /
`semantic_history()` 写进 Dynamic Profile。

| 匹配 | Cmd-click / 第一条动作 | 右键还可 |
|---|---|---|
| `path/to/file.ext:42` 或 `:42:8` | 打开到行（本机最佳编辑器） | Copy path:line |
| Git SHA（`[0-9a-f]{7,40}`） | 在仓库目录 `git show --stat` | Copy SHA |
| `localhost:3xxx` / `127.0.0.1:…` | 浏览器打开 `http://…` | Copy host:port |

出厂 Paths / HTTP URL 等规则一并保留——写了 `Smart Selection Rules` 会**整表替换**继承，
所以生成器必须自带那一组。

Semantic History = `best editor`（本机有 Cursor / VS Code 就会用）。
`setup-gui.sh` 钉住 `CommandSelection=YES`，避免 Cmd-click 被静默关掉。

```bash
./scripts/doctor.sh --status          # semantic 行应有产品规则 + SH=best editor
./scripts/theme.sh <主题> && Cmd+T    # 必须新开 tab
```

### 4.5 状态栏（可选）

`Settings → Profiles → Session → Status bar enabled → Configure`
可拖入 CPU/内存/网速/git 分支组件；Minimal 主题下放底部、底色 `#1e1e2e`。
重度 starship 用户可不开，避免信息重复。

## 五、换主题（推荐用 theme.sh）

本 skill 自带七套主题（3 套社区 + 4 套品牌），**一键切换、保存即生效、不用重启**：

```bash
./scripts/theme.sh                  # 主题画廊（带真彩色色条）+ 当前主题
./scripts/theme.sh ember         # 切回默认（Ember 暖烬：暖黑 + 暖橙光标）
./scripts/theme.sh voltage          # 切到 Voltage 霓虹电压（近黑 + 薄荷光标）
./scripts/theme.sh tokyo-night      # 切到 Tokyo Night（还有 gruvbox-dark / catppuccin-mocha）
./scripts/theme.sh --preview voltage  # 先看不换：整块「假终端」预览
```

原理：`config/themes/*.json` 五套 Profile **共享同一个 Guid**，`theme.sh` 把选中的拷成
`~/Library/Application Support/iTerm2/DynamicProfiles/hekouwang-active-theme.json`，
并清掉会撞 Guid 的旧文件。因为 Guid 不变，「默认 Profile」绑定永远不断。
主题列表是扫 `config/themes/*.json` 自动发现的，加主题不用改 `theme.sh`。

**加新主题**：在 `config/themes/palettes/` 下加一份 16 色色板（新建 `palettes/mine.py`
会被自动发现），`cd config/themes && python3 _generate.py` 重跑即可生成同构 Profile JSON。
装了付费包时，同一次重跑还会一并出 Warp YAML、Ghostty 主题和整套 `ecosystem/`，
之后 `./scripts/theme.sh <名字>` 一条命令把它们全切过去 —— **不用再手动去 Warp 里点**。

⚠️ **别手改生成出来的 JSON/YAML**，下次重跑就被覆盖。改色去改 `palettes/*.py`。
⚠️ **Dynamic Profile 只覆盖 JSON 里声明过的键**——没声明的键会沿用 iTerm2 缓存
（`New Bookmarks`）里的旧值。所以要清掉一个曾被 GUI 误设的值（比如 `Initial Text`），
必须在 JSON 里把它**显式声明为空**，光是"不写"清不掉。

> 想临时试别的配色方案，仍可下 `.itermcolors` 手动导入
> （`Settings → Profiles → Colors → Color Presets... → Import...`），
> 例如 mbadolato/iTerm2-Color-Schemes 仓库里几百套。但常用主题建议沉淀进 `config/themes/`。

## 六、配置文件路径备忘

| 内容 | 路径 |
|---|---|
| Dynamic Profile | `~/Library/Application Support/iTerm2/DynamicProfiles/` |
| iTerm2 主偏好 | `~/Library/Preferences/com.googlecode.iterm2.plist` |
| Starship | `~/.config/starship.toml` |
| zsh 配置 | `~/.zshrc` + `~/.zshrc.local`（私有） |
| Shell Integration | `~/.iterm2_shell_integration.zsh` + `~/.iterm2/` |
| atuin 数据库 | `~/.local/share/atuin/history.db` |
| 语言设置 | `~/.config/hekouwang-terminal/lang` |
| 导出全部设置 | `Settings → General → Settings → Export All Settings...` |
