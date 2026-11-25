# ~/.zshrc 逐块详解 + 插件推荐

> [English](zshrc-explained.md) · **简体中文**

> 基于一份真实用了几年的 .zshrc 整理（2026-06，已脱敏）。按文件中实际出现顺序分块解读，
> 每块说明：干什么的、为什么需要、推荐与否。文末附「已知问题清单」与修复方案。

---

## 块 1 · 文件句柄数上限

```bash
ulimit -n 10240 2>/dev/null
```

| 项 | 说明 |
|---|---|
| 干什么 | 把单进程可打开文件数上限从 macOS 默认 256 提到 10240 |
| 为什么 | zsh-autocomplete + zsh-autosuggestions 的异步 worker 会同时打开大量文件描述符，默认 256 会报 `too many open files` |
| 位置要求 | 放 .zshrc 最顶部（插件加载之前） |
| 推荐度 | ★★★★★ 用 zsh-autocomplete 必加 |

## 块 2 · oh-my-zsh 框架

```bash
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME=""          # prompt 交给 starship，主题留空
plugins=(git)
source $ZSH/oh-my-zsh.sh
```

| 项 | 说明 |
|---|---|
| 干什么 | 加载 oh-my-zsh 框架；主题留空（交给 starship）；只开 git 插件 |
| git 插件 | 提供 `gst`/`gco`/`gp` 等上百个 git 缩写 + 补全增强 |
| ⚠️ 注意 | 后面用了 Starship 接管 prompt，所以 `ZSH_THEME` 设空 —— 省一次 omz 主题加载。**模板（config/zshrc.template）即如此**。若你的旧 .zshrc 还写着 `ZSH_THEME="Minimal"`，那行其实被 starship 覆盖、不生效，留空即可 |
| 插件哲学 | `plugins=()` 保持精简是对的——omz 插件每多一个启动就慢一点。值得考虑加的：`sudo`（双击 Esc 加 sudo）、`extract`（`x 压缩包` 万能解压）、`z`（已被 zoxide 替代则不需要） |
| 推荐度 | ★★★★ 框架仍是补全生态最省心的底座；追求极致启动速度可换 zinit/znap 纯插件管理 |

## 块 3 · Znap 插件管理器 + zsh-autocomplete

```bash
zstyle ':znap:*' repos-dir ~/.zsh-plugins
[[ -r ~/.zsh-plugins/znap/znap.zsh ]] ||
    git clone --depth 1 -- https://github.com/marlonrichert/zsh-snap.git ~/.zsh-plugins/znap
source ~/.zsh-plugins/znap/znap.zsh
znap source marlonrichert/zsh-autocomplete
```

| 项 | 说明 |
|---|---|
| znap | 极简 zsh 插件管理器，自带「不存在就 git clone」的自举逻辑——新机器开 shell 自动装好 |
| zsh-autocomplete | **实时补全菜单**：边打字边弹出候选（命令/路径/历史/man 参数），Tab 进菜单方向键选。是「重型」插件，体验接近 IDE |
| 取舍 | 与 zsh-autosuggestions（块 4）功能有重叠但定位不同：autocomplete 是弹菜单，autosuggestions 是行内灰色幽灵字。两者可共存（本配置就是），但都开会吃性能——这正是块 1 要提 ulimit 的原因。嫌闹可只留 autosuggestions |
| 推荐度 | ★★★★ 重度键盘党神器；轻量党可跳过此块 |

## 块 4 · zsh-autosuggestions（灰色幽灵提示）

```bash
source /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh
```

| 项 | 说明 |
|---|---|
| 干什么 | 输入时按历史记录给出行内灰色补全，`→` 或 `End` 接受 |
| 安装 | `brew install zsh-autosuggestions` |
| 推荐度 | ★★★★★ 性价比最高的单个插件，必装 |

## 块 5 · Node 版本管理（⚠️ 本配置最大问题区）

**现行做法（2.8.0+）**：装机时四选一（`fnm` / `nvm` / `brew` / `vfox`），片段写在
`~/.config/hekouwang-terminal/node.sh`，`.zshrc` 只 `source` 那一份。换管理器跑
`./scripts/node-mgr.sh <名字>`，不用改 `.zshrc`。铁律仍是**只留一套**。

下面保留「原文件里四套共存」的反面教材，方便理解为什么要选一个：

原文件里同时存在 **4 套 Node 来源**：

```bash
# ① nvm（且被加载了两次！第 114 行和第 179 行）
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# ② brew 的 node@22 直接进 PATH
export PATH="/opt/homebrew/opt/node@22/bin:$PATH"

# ③ fnm（Fast Node Manager）
eval "$(fnm env --use-on-cd)"

# ④ 手动把 fnm 某个版本的 bin 写死进 PATH
export PATH="$HOME/.local/share/fnm/node-versions/v22.19.0/installation/bin:$PATH"
```

**问题**：
1. nvm 重复加载 → 启动时间白白 ×2（nvm 是出了名的慢，单次加载就 300-500ms）
2. 四套来源在 PATH 里互相打架，哪个生效取决于声明顺序，`nvm use` 切了版本也可能被后面的硬编码 PATH 盖掉
3. `$(nvm current)` 在 nvm 未加载完时会让 PATH 出现坏条目

**修复（推荐保留 fnm，删掉其余）**：

```bash
# fnm — 唯一的 Node 版本管理器（rust 写的，加载 <50ms，进目录自动切版本）
eval "$(fnm env --use-on-cd)"
```

| 对比 | nvm | fnm |
|---|---|---|
| 加载耗时 | 300-500ms | <50ms |
| 自动切版本 | 需插件 | `--use-on-cd` 原生支持（读 .nvmrc/.node-version） |
| 推荐度 | ★★ | ★★★★★ |

## 块 6 · SSH 服务器别名（🔒 私有，不进 git）

```bash
alias mycompany-dev-root="ssh -o ServerAliveInterval=60 root@x.x.x.x"
alias ecs:xxx:NN="ssh -o ServerAliveInterval=60 root@x.x.x.x"
# ……十余条
```

| 项 | 说明 |
|---|---|
| 干什么 | 公司各环境服务器一键 SSH；`ServerAliveInterval=60` 每 60 秒发心跳防断线 |
| 命名约定 | `ecs:项目:IP尾号` —— 冒号分隔在 zsh alias 中合法，且天然分组 |
| 更优方案 | 写进 `~/.ssh/config`（Host 块），这样 `scp`/`rsync`/VS Code Remote 也能用别名，而 alias 只对交互 shell 生效 |
| 🔒 红线 | **真实 IP 绝不进 GitHub**。放 `~/.zshrc.local`（模板已自动 source） |

`~/.ssh/config` 等价写法（推荐迁移）：

```
Host mycompany-dev
    HostName x.x.x.x
    User root
    ServerAliveInterval 60
```

## 块 7 · Git 短别名

```bash
alias gc="git commit -am "
alias gs="git status"
alias gaa="git add ."
alias gpld="git pull origin develop"   # gpud / gplm / gpum 同理
alias gcom="git checkout master"       # gcod 同理
alias gco="git checkout "
alias gr="git merge "
```

| 项 | 说明 |
|---|---|
| 设计 | 围绕 master/develop 双分支流的肌肉记忆缩写 |
| ⚠️ 冲突 | omz git 插件里 `gr` 默认是 `git remote`、`gco` 是 `git checkout`——自定义 alias 在 omz 之后声明所以会覆盖，行为以这里为准。知道即可，不算 bug |
| 推荐度 | ★★★★ 按自己工作流定制，照抄不如自己长出来 |

## 块 8 · Homebrew 国内镜像 + 降频

```bash
export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles
export HOMEBREW_API_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles/api
export HOMEBREW_PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/
export HOMEBREW_AUTO_UPDATE_SECS=3600   # brew 自动更新最多每小时一次（默认每次 install 前都检查）
```

| 推荐度 | ★★★★★ 国内网络必备；海外机器删掉前三行即可 |

> ⚠️ **前两行别再指阿里云**。那个 homebrew 镜像已基本停更（API 里 uv 还停在 0.7.6，
> 新版 bottle 全缺），而 Homebrew 6.x 的表现会把人绕进去：镜像 404 → 回退官方 ghcr.io
> **下载成功** → 但缓存文件名哈希是按**镜像 URL** 算的 → pour 时按镜像哈希找文件 →
> 找不到 → 硬失败报 `No such file or directory ... bottle.tar.gz`，重试多少次都卡同一处。
> 判镜像有没有停更：
> `curl -s "$HOMEBREW_API_DOMAIN/formula/uv.json" -o /tmp/uv.json`（官方 API，执行前可先审阅）
> `python3 -c "import json;print(json.load(open('/tmp/uv.json'))['versions']['stable'])"`（读取已保存的文件）
> —— 跟 `brew info uv` 对不上就是滞后。不动配置的应急绕开：
> `env -u HOMEBREW_BOTTLE_DOMAIN -u HOMEBREW_API_DOMAIN brew upgrade`。

## 块 9 · Starship Prompt

```bash
eval "$(starship init zsh)"
```

| 项 | 说明 |
|---|---|
| 干什么 | 跨 shell 的 Rust prompt，读 `~/.config/starship.toml`。本套是 pure 风格双行：目录蓝 / git 分支灰 / 耗时黄 / `❯` 紫（出错变红、vim 模式变 `❮` 绿） |
| 与 omz 主题关系 | starship 接管 prompt 后 `ZSH_THEME` 失效 |
| 配置文件 | 见本 skill `config/starship.toml`，git_status 故意 `disabled = true` 保持极简 |
| 推荐度 | ★★★★★ 比 powerlevel10k 更简单、跨 bash/zsh/fish 通用 |

## 块 10 · 语言运行时与工具 PATH

```bash
export JAVA_HOME=/opt/homebrew/Cellar/openjdk@17/17.0.12/libexec/openjdk.jdk/Contents/Home
export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"      # Java 17
export PATH="$PATH:$HOME/.local/bin"                        # pipx 装的 Python CLI
export PATH="$HOME/.codeium/windsurf/bin:$PATH"             # Windsurf 编辑器 CLI
export LC_ALL=en_US.UTF-8                                   # 统一 locale，防 SSH 到服务器乱码
source "$HOME/.openclaw/completions/openclaw.zsh"           # OpenClaw 补全

# bun（⚠️ 原文件里这两行重复写了两遍，删一组即可）
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
[ -s "$HOME/.bun/_bun" ] && source "$HOME/.bun/_bun"        # bun 补全

export TERM=xterm-256color   # 强制 256 色（某些老服务器 TERM 识别不到时兜底）
```

| ⚠️ JAVA_HOME 隐患 | 路径写死了 `17.0.12` 小版本，brew 升级后会失效。更稳的写法：`export JAVA_HOME=$(/usr/libexec/java_home -v 17)` 或指向 `/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home`（opt 软链不随小版本变） |
| ⚠️ TERM 注意 | 在 .zshrc 里硬设 TERM 会覆盖 iTerm2 上报的 `xterm-256color`/`iterm2`，一般无害但 tmux 内可能干扰真彩色；如遇配色异常可删 |

## 块 11 · 代理（🔒 私有，不进 git）

```bash
export https_proxy=http://127.0.0.1:10080
export http_proxy=http://127.0.0.1:10080
export all_proxy=socks5://127.0.0.1:10081
```

| 问题 | 写死在 .zshrc 意味着**代理没开时所有网络命令都会卡死** |
| 更优方案 | 包成开关函数放 `~/.zshrc.local`： |

```bash
proxy_on()  { export https_proxy=http://127.0.0.1:10080 http_proxy=http://127.0.0.1:10080 all_proxy=socks5://127.0.0.1:10081; echo "proxy on"; }
proxy_off() { unset https_proxy http_proxy all_proxy; echo "proxy off"; }
```

## 块 12 · 现代 CLI 套件（本配置的精华）

> 安装：`brew install eza bat fzf fd zoxide ripgrep atuin`

### eza — `ls` 替代

```bash
alias ls="eza --icons"
alias ll="eza -l --icons --git"        # 长列表 + git 状态列
alias la="eza -la --icons --git"       # 含隐藏文件
alias lt="eza --tree --level=2 --icons" # 两层树形
```

图标渲染依赖 Nerd Font（见 GUI 文档字体策略）。`command -v` 守卫保证没装 eza 的机器回退原生 ls。★★★★★

### bat — `cat` 替代

```bash
alias cat="bat --paging=never"   # 语法高亮+行号，不进分页器（保持 cat 的直出习惯）
export BAT_THEME="hekouwang-ember"
```

> 本套装里**不用手设 `BAT_THEME`**：`install.sh` 一次把全部主题装进 bat 缓存并
> `bat cache --build`，变量由 `.zshrc` source 的那份生态配色给，所以换肤时它自动跟着变。
> ⚠️ bat 按主题内部的 `name` 字段索引，不是按文件名；**认不出主题时静默回退自己的默认配色**，
> 表现就是「别的都对，只有 `cat` 的颜色不对」。

★★★★★

### fzf — 模糊搜索一切

```bash
source <(fzf --zsh)   # 接管 Ctrl+R（历史）/ Ctrl+T（文件）/ Alt+C（cd）
export FZF_DEFAULT_COMMAND="fd --type f --hidden --follow --exclude .git"  # 用 fd 做文件源：快 + 尊重 .gitignore
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
# FZF_DEFAULT_OPTS（配色 + 40% 高度带边框窗）由生态配色文件给，所以跟着主题走。
# ⚠️ 别在这里写死 hex —— 写死了换肤就漂，只有 fzf 那个弹窗还是旧色。
```

注意：atuin（下面）会再接管 Ctrl+R，所以 fzf 实际负责 Ctrl+T 和 Alt+C。★★★★★

### zoxide — `cd` 替代

```bash
eval "$(zoxide init zsh)"
```

按访问频率学习目录，`z pi` 直达 `~/Dashboard/Pi.dev`，`zi` 进入交互选择（走 fzf）。★★★★★

### atuin — 命令历史数据库

```bash
eval "$(atuin init zsh --disable-up-arrow)"
```

SQLite 全文存储每条命令（含目录、耗时、退出码），接管 `Ctrl+R` 为全屏搜索界面；`--disable-up-arrow` 保留 `↑` 原生行为（只在当前会话翻历史）。装完跑一次 `atuin import auto` 导入存量历史，`atuin stats` 看常用命令排行。可选注册账号跨机加密同步。★★★★★

### ripgrep（rg）— `grep` 替代

无需配置，装上即用。代码搜索速度天花板，自动跳过 .gitignore。★★★★★

## 块 13 · zsh-syntax-highlighting（必须最后）

```bash
[ -f /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ] && \
  source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
```

命令合法绿色 / 非法红色 / 字符串黄色，**回车前**就知道命令打错没。
它通过包裹 ZLE widget 实现，**必须在所有改键位的插件之后加载**——这就是它钉死在 .zshrc 倒数第二行的原因。★★★★★

## 块 14 · iTerm2 Shell Integration（最末行）

```bash
test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"
```

iTerm2 官方增强：命令块导航（`Cmd+Shift+↑/↓`）、失败命令红标、`imgcat` 终端看图、`it2copy` 远程复制到本地剪贴板等。安装见 GUI 文档 4.2。★★★★

---

# 已知问题清单（原 .zshrc 体检结果）

| # | 问题 | 影响 | 修复 |
|---|---|---|---|
| 1 | nvm 加载两次（114 行 + 179 行） | 启动慢 600ms-1s | 删掉两处，只留 fnm |
| 2 | nvm + fnm + brew node@22 + 手写 fnm 路径，4 套 Node 来源 | PATH 打架，切版本不生效 | 只留 `eval "$(fnm env --use-on-cd)"` |
| 3 | bun 的 BUN_INSTALL/PATH 写了两遍 | 无害但冗余 | 删一组 |
| 4 | `ZSH_THEME="Minimal"` 被 starship 覆盖 | 白加载一次主题 | 改 `ZSH_THEME=""` |
| 5 | JAVA_HOME 写死小版本号 17.0.12 | brew 升级后 Java 失踪 | 用 `/usr/libexec/java_home -v 17` |
| 6 | 代理写死且无开关 | 代理没开时全网络命令卡死 | proxy_on/proxy_off 函数进 .zshrc.local |
| 7 | SSH 别名含真实 IP | 上 GitHub 即泄露 | 移入 .zshrc.local 或 ~/.ssh/config |
| 8 | `export TERM=xterm-256color` 硬编码 | tmux 真彩色可能异常 | 可删（iTerm2 自己会设对） |

> 以上修复已全部体现在 `config/zshrc.template` 中。

# 插件推荐总表

| 名称 | 类型 | 一句话 | 必装 |
|---|---|---|---|
| zsh-autosuggestions | zsh 插件 | 行内灰色幽灵补全 | ✅ |
| zsh-syntax-highlighting | zsh 插件 | 命令对错实时着色（放最后） | ✅ |
| zsh-autocomplete | zsh 插件 | 实时弹出补全菜单（重型，配 ulimit） | 可选 |
| omz git 插件 | omz | git 缩写 + 补全 | ✅ |
| starship | prompt | 极简跨 shell prompt | ✅ |
| eza / bat / fd / ripgrep | CLI | ls/cat/find/grep 现代替代 | ✅ |
| fzf | CLI | 模糊搜文件(Ctrl+T)/目录(Alt+C) | ✅ |
| zoxide | CLI | 频率学习版 cd | ✅ |
| atuin | CLI | 命令历史数据库(Ctrl+R) | ✅ |
| fnm | CLI | Node 版本管理（替代 nvm） | ✅ |
| znap | 插件管理 | 自举式 zsh 插件管理器 | 可选 |
