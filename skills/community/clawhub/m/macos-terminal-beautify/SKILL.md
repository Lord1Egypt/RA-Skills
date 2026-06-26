---
name: macos-terminal-beautify
description: 在 macOS 上对终端进行美化，使用 Ghostty + Starship + Oh My Zsh + Nerd Font 组合，实现彩色胶囊提示符终端效果。
agent_created: true
---

# macOS Terminal Beautify

在 macOS 上对终端进行美化，核心工具链为 **Ghostty（终端模拟器）+ Starship（提示符）+ Oh My Zsh（Shell 框架）+ Nerd Font（图标字体）**，最终实现 Catppuccin Mocha 主题的彩色胶囊提示符。

## 适用场景

- 用户要求美化 macOS 终端外观
- 用户需要配置 Ghostty 终端模拟器
- 用户需要安装配置 Starship 提示符工具
- 用户需要安装 Oh My Zsh 及相关插件

## 安装步骤

### 1. 安装核心工具

```bash
# 安装 Ghostty 终端模拟器
brew install --cask ghostty

# 安装 Starship 提示符
brew install starship

# 安装 Nerd Font 字体（必须，否则图标显示为方框）
brew install --cask font-meslo-lg-nerd-font font-fira-code-nerd-font
```

如果 brew 遇到 API 缓存问题（如 `cask.jws.json` 错误），先清除缓存：
```bash
rm -rf ~/Library/Caches/Homebrew/api/*.json
brew update
```

### 2. 安装 Oh My Zsh

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
```

注意：`--unattended` 参数避免交互式提示。

### 3. 安装 Zsh 插件

```bash
ZSH_CUSTOM=${ZSH_CUSTOM:-~/.oh-my-zsh/custom}
git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
git clone --depth=1 https://github.com/zsh-users/zsh-completions $ZSH_CUSTOM/plugins/zsh-completions
```

### 4. 配置 Ghostty

编辑 `~/.config/ghostty/config`：

```ini
font-family = MesloLGS Nerd Font Mono
font-size = 14
theme = Catppuccin Mocha
background = #282c34
foreground = #ffffff
background-opacity = 0.95
background-blur = true
window-padding-x = 12
window-padding-y = 12
macos-titlebar-style = tabs
cursor-style = block
cursor-style-blink = true
shell-integration = zsh
```

配置重载方式：在 Ghostty 中按 `Cmd + Shift + ,` 或重启应用。

验证主题可用性：
```bash
ghostty +list-themes | grep -i catppuccin
```

### 5. 配置 Starship

编辑 `~/.config/starship.toml`，使用 Catppuccin Mocha 调色板：

- 格式：`os -> username -> directory -> git_branch/git_status -> language -> time -> cmd_duration -> character`
- 每个模块使用不同颜色的背景胶囊（红/橙/黄/绿/蓝/紫）
- 命令提示符 `❯`：成功绿色，失败红色
- 语言模块统一使用绿色背景
- 确保 Nerd Font 使用正确字体才能显示图标

### 6. 更新 .zshrc

合并已有配置和新的 Oh My Zsh + Starship 配置：

```zsh
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME=""                         # 清空交给 Starship
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)  # syntax-highlighting 必须放最后
fpath+=${ZSH_CUSTOM:-$ZSH/custom}/plugins/zsh-completions/src
source $ZSH/oh-my-zsh.sh

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# 补全优化
autoload -Uz compinit && compinit
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=*' 'l:|=* r:|=*'
zstyle ':completion:*' menu select

# Homebrew + Starship
eval "$(/opt/homebrew/bin/brew shellenv)"
eval "$(starship init zsh)"

# 保留原有配置（API keys、PATH 等）
[ -f ~/.zshrc.local ] && source ~/.zshrc.local
```

### 7. 自检验证

运行验证脚本 `scripts/check_term.sh`，检查包括：
1. Nerd Font 已安装
2. 图标渲染测试（圆点 icon = OK，方框 = 字体问题）
3. 工具版本（Starship、Zsh、Ghostty）
4. 配置文件存在性
5. 插件安装状态
6. 环境变量

## 常见问题

| 现象 | 原因 | 解决 |
|------|------|------|
| 图标显示 □ | 字体不是 Nerd Font | 终端字体改为 MesloLGS NF Mono |
| Ghostty 报 theme not found | 主题名拼写错误 | `ghostty +list-themes` 查正确名字 |
| 历史灰字建议不出现 | 插件顺序错 | zsh-syntax-highlighting 必须放 plugins 最后 |
| compinit 报 insecure | 权限问题 | `compaudit \| xargs chmod g-w,o-w` |

## VS Code 集成终端字体配置

如果需要在 VS Code 的集成终端中也正确显示 Nerd Font 图标：

### 打开 settings.json

1. 按 `Cmd + Shift + P` 打开命令面板
2. 输入 `settings.json`，选择 **"首选项：打开设置 (JSON)"**

### 添加字体配置

在 `{ }` 花括号内添加：

```json
"terminal.integrated.fontFamily": "MesloLGS Nerd Font Mono",
```

保存后 VS Code 的集成终端即可正确显示所有 Nerd Font 图标。

## 最终效果

![终端美化效果](assets/preview.png)
