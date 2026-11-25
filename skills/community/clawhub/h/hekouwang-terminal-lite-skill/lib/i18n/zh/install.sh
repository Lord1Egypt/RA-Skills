#!/bin/bash
# 词条表 · 中文 · install.sh

blk_install_help() {
  cat <<'EOF'
hekouwang-terminal-skill — 一键安装

用法:
  ./scripts/install.sh              安装
  ./scripts/install.sh --dry-run    先看它打算改哪些文件、写哪些设置，一个字节都不动
  ./scripts/install.sh --lang en    切回英文（会记住，之后不用再带）
  ./scripts/install.sh --node fnm   指定 Node 管理器：fnm / nvm / brew / vfox（会记住）
  CN=1 ./scripts/install.sh         国内网络：全程走清华 TUNA 等国内镜像

幂等：重复执行安全，已装的跳过。
覆盖 ~/.zshrc 前会先备份进 ~/.hekouwang-terminal-backups/，随时能回滚。
已经在用自己的 .zshrc？先跑 ./scripts/migrate.sh —— 它会把你的 alias/PATH/环境变量
搬进 ~/.zshrc.local 再套模板，而不是直接盖掉。
后悔了：./scripts/uninstall.sh（会从备份还原 .zshrc、把 GUI 设置恢复出厂默认）
EOF
}

M_INSTALL_DRY_HEAD="═══ DRY-RUN：以下都不会真的执行 ═══"
M_INSTALL_DRY_TAIL="去掉 --dry-run 才会真的执行。"

blk_install_dryrun() {
  cat <<EOF

会安装（已装的会跳过）
  Homebrew（若无）· iTerm2
  字体：Maple Mono NF CN（SIL OFL，免费可商用）+ Symbols Nerd Font
  CLI：starship eza bat fzf fd zoxide ripgrep atuin tmux git-delta
       zsh-autosuggestions zsh-syntax-highlighting
       + 你选的 Node 管理器对应包（fnm / nvm / node / vfox）
  oh-my-zsh（若无）· iTerm2 Shell Integration

会写这些文件
  ~/.zshrc                                    ← 先备份进 ~/.hekouwang-terminal-backups/
  ~/.zshrc.local                              ← 不存在才创建，已存在绝不覆盖
  ~/.config/hekouwang-terminal/node.sh         ← Node 管理器片段（./scripts/node-mgr.sh 可换）
  ~/.hekouwang-terminal-backups/               ← .zshrc 备份目录（不散落家目录根）
  ~/.config/starship.toml
  ~/.config/hekouwang-terminal/current/        ← 生态配色（colors.sh/delta/tmux）
  ~/Library/Application Support/iTerm2/DynamicProfiles/hekouwang-active-theme.json
  ~/.config/bat/themes/hekouwang-*.tmTheme    ← 并跑一次 bat cache --build
  ~/.config/ghostty/{config,themes/hekouwang-*}   ← 仅当装了 Ghostty；原 config 先备份
  ~/.warp/themes/*.yaml                        ← 仅当装了 Warp
  ~/.vscode|.cursor/extensions/hekouwang-terminal-themes-*/  ← 仅当装了对应编辑器

会往你已有的配置里加一行（都会先备份）
  ~/.gitconfig    加 [include] path=…/delta.gitconfig   （git diff 配色）
  ~/.tmux.conf    加 source-file …/tmux.conf            （tmux 配色）

会写这些系统设置（defaults）
  com.googlecode.iterm2：Minimal 主题、隐藏滚动条、默认 Profile、
                         Shift+Enter 换行、状态栏位置、工具带
  全局：ApplePressAndHoldEnabled=false（长按连续重复，vim 党刚需）

不会碰
  你的 ~/.ssh/、已存在的 ~/.zshrc.local、Homebrew 里你自己装的别的包

默认主题：$DEFAULT_THEME
撤销方式：./scripts/uninstall.sh（有 --dry-run）
EOF
}

M_INSTALL_CN_MIRROR="已启用国内镜像（清华 TUNA），Homebrew 全程走国内源..."
M_INSTALL_BREW="安装 Homebrew..."
M_INSTALL_ITERM_FONTS="安装 iTerm2 + 字体（Maple Mono NF CN / Symbols Nerd Font / JetBrains Mono 兜底）..."
M_INSTALL_CASK_SKIP_MANUAL="%s 已装（手动安装，不在 brew 记录里），跳过"
M_INSTALL_CASK_FAIL="⚠ %s 装失败（国内网络请改用 CN=1 ./scripts/install.sh）"
M_INSTALL_CLI="安装 CLI 全家桶（逐个装，单个失败不中断）..."
M_INSTALL_PKG_FAIL="⚠ %s 安装失败，先跳过"
M_INSTALL_PKG_FAILED_SUM="⚠ 这些包没装上，稍后手动 brew install：%s"
M_INSTALL_OMZ="安装 oh-my-zsh..."
M_INSTALL_CONFIG="部署配置文件..."
M_INSTALL_GHOSTTY_BAK="已备份原 Ghostty config → ~/.config/ghostty/config.bak.*"
M_INSTALL_GHOSTTY_OK="✓ Ghostty 主题与配置已部署（改完按 Cmd+Shift+, 重载）"
M_INSTALL_WARP_OK="✓ Warp 主题已部署（Warp 设置 → Appearance 里选同名主题）"
M_INSTALL_BAT="安装 bat 语法高亮主题（全部主题一次装好）..."
M_INSTALL_BAT_OK="✓ %s 套 bat 主题已装并建好缓存"
M_INSTALL_BAT_CACHE_FAIL="⚠ bat cache --build 失败（cat 的高亮会回到默认色，不影响其它）"
M_INSTALL_BAT_MISSING="⚠ bat 未安装，跳过其主题"
M_INSTALL_THEME="部署主题与生态配色（默认 %s）..."
M_INSTALL_GIT_SKIP="git diff 配色已挂过，跳过"
M_INSTALL_GIT_OK="✓ git diff 配色已挂进 ~/.gitconfig（delta）"
M_INSTALL_TMUX_SKIP="tmux 配色已挂过，跳过"
M_INSTALL_TMUX_OK="✓ tmux 配色已挂进 ~/.tmux.conf"
M_INSTALL_TMUX_MARK="# hekouwang-terminal-skill 配色（换肤时内容自动更新）"
M_INSTALL_VSC_OK="✓ 编辑器主题已装 → %s（重启编辑器后在主题列表里选）"
M_INSTALL_ZSHRC_BAK="已备份原 ~/.zshrc → %s"
M_INSTALL_ZSHRC_HINT_MIGRATE="💡 原 .zshrc 里有 alias/export —— 想保住它们可以 Ctrl+C 中断，改跑 ./scripts/migrate.sh"
M_INSTALL_SI="安装 iTerm2 Shell Integration（imgcat/it2copy 等工具）..."
M_INSTALL_SI_OK="✓ Shell Integration 已装"
M_INSTALL_SI_FAIL="⚠ Shell Integration 装失败（imgcat/it2copy 不可用，其它不受影响）"
M_INSTALL_DEFAULTS="系统级设置：长按按键连续重复（vim 党刚需）..."
M_INSTALL_GUI="自动写好 iTerm2 GUI 设置（Minimal 主题 / 默认 Profile / Shift+Enter 换行）..."
M_INSTALL_DOCTOR="跑环境自检..."
M_INSTALL_DONE="✅ 全部完成！"
M_INSTALL_TAIL_LOCAL="私有配置（SSH 别名/代理）请编辑 ~/.zshrc.local"
M_INSTALL_TAIL_OPEN="打开 iTerm2 即生效。"
# ⛔ 别把「连 bat/fzf/git diff 一起换」写回这一行。那是付费包能力，开源版只同步
#    iTerm2，而这行文案两档都会打 —— 在这儿吹它，跟当初公开仓 description 里
#    写「全链同步」是同一个钓鱼错误（见 memory skill-oss-paid-tiering-model）。
M_INSTALL_TAIL_THEME="换肤：./scripts/theme.sh"
M_INSTALL_TAIL_NODE="换 Node 管理器：./scripts/node-mgr.sh <fnm|nvm|brew|vfox>"
M_INSTALL_TAIL_UNDO="后悔了：./scripts/uninstall.sh（支持 --dry-run）"
M_INSTALL_TAIL_CN="💡 国内网络若中途报 portable-ruby / 下载失败，改用：CN=1 ./scripts/install.sh"
# 只在付费件缺席时打。%s = 落地页
M_INSTALL_TAIL_BUY="统一的终端工作台 —— 平台购买（SkillPay ¥59.9/年 · SkillHub ¥2.99/次）：%s"
M_INSTALL_GUI_FAIL="! GUI 设置没跑完（不影响已装好的部分）—— 稍后手动跑：./scripts/setup-gui.sh"

# ---- Node 管理器选择 ----------------------------------------
M_INSTALL_NODE_PROMPT="选一个 Node 版本管理器（只留一套，别混用）："
M_INSTALL_NODE_OPT_FNM="  1) fnm   — Fast Node Manager（推荐，默认）"
M_INSTALL_NODE_OPT_NVM="  2) nvm"
M_INSTALL_NODE_OPT_BREW="  3) brew  — Homebrew 的 node（单版本，不是版本管理器）"
M_INSTALL_NODE_OPT_VFOX="  4) vfox  — version-fox（多语言 SDK）"
M_INSTALL_NODE_ASK="选哪个？[1]: "
M_INSTALL_NODE_PICKED="Node 管理器：%s"
M_INSTALL_NODE_BAD="✗ 不认识的 Node 管理器 '%s'"
M_INSTALL_NODE_CHOICES="可选：fnm · nvm · brew · vfox（或 ./scripts/install.sh --node fnm）"
M_INSTALL_NODE_DEPLOYED="✓ Node 片段已写入（%s）"
M_INSTALL_NODE_SWITCH_HINT="以后想换：./scripts/node-mgr.sh <fnm|nvm|brew|vfox>"
M_INSTALL_NODE_WRITE_FAIL="⚠ Node 片段写入失败（检查 config/node/）"
M_INSTALL_FETCH_FAIL="✗ 下载失败：%s"
M_INSTALL_FETCH_SAVED="已下载到 %s（SHA-256：%s）"
M_INSTALL_FETCH_SOURCE="来源：%s"
M_INSTALL_FETCH_HOW="审阅后执行：bash %s  —— 或设 HKW_ASSUME_YES=1 让安装脚本自动执行"
M_INSTALL_FETCH_STOP="Homebrew 仍未安装：先执行上面下载的安装脚本，再重跑本命令"
M_INSTALL_FETCH_STOP_OMZ="oh-my-zsh 仍未安装：先执行上面下载的安装脚本，再重跑本命令（不会先写 .zshrc）"
