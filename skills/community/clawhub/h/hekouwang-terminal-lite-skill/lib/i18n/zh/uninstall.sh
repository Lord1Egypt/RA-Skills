#!/bin/bash
# 词条表 · 中文 · uninstall.sh

blk_uninstall_help() {
  cat <<'EOF'
hekouwang-terminal-skill — 卸载 / 还原

用法:
  ./scripts/uninstall.sh              交互式：逐项问，默认只删本套装的东西
  ./scripts/uninstall.sh --dry-run    只打印会干什么，一个字节都不动
  ./scripts/uninstall.sh --yes        不问，执行「默认档」（不卸 brew 包、不删 oh-my-zsh）
  ./scripts/uninstall.sh --lang en    切回英文

设计底线（和 install.sh 是一对，别单独改其中一个）：
  1. 只删本套装自己装的东西。Homebrew 本体、oh-my-zsh、你自己的
     ~/.zshrc.local、你 git 里的配置，一律不碰（除非你显式勾）。
  2. ~/.zshrc 从 install.sh 留下的 .bak 时间戳备份里还原，不是删掉了事。
     找不到备份就明说找不到，不假装成功。
  3. iTerm2 的 GUI 设置用 defaults delete 还原成「iTerm2 出厂默认」，
     不是写一个我们以为的默认值 —— 那样只是换一种方式改你的配置。
  4. 删之前先打印清单。--dry-run 跑完能看到一模一样的清单。
EOF
}

M_UN_HEAD="═══ hekouwang-terminal-skill 卸载 ═══"
M_UN_DRY="DRY-RUN：只打印，不动任何文件"
M_UN_S1="1. ~/.zshrc"
M_UN_BAK_FOUND="找到备份："
M_UN_ASK_RESTORE="把它还原成 ~/.zshrc？（当前 .zshrc 会另存为 .zshrc.uninstall.bak）"
M_UN_RESTORED="已还原 ~/.zshrc ← %s"
M_UN_KEEP_ZSHRC="保留当前 ~/.zshrc（里面 source 生态配色的那行会失效，可手动删）"
M_UN_NO_BAK="没找到 zshrc 备份（~/.hekouwang-terminal-backups/ 与家目录根）—— 不替你猜内容，请自己检查 ~/.zshrc"
M_UN_NO_BAK_NOTE="本套装在 .zshrc 里加的是：source ~/.config/hekouwang-terminal/current/colors.sh"

M_UN_S2="2. 本套装写的配置文件"
M_UN_RM_DP="删 iTerm2 Dynamic Profile"
M_UN_NO_DP="iTerm2 Dynamic Profile 不存在"
M_UN_RM_RUNTIME="删运行时目录 ~/.config/hekouwang-terminal/"
M_UN_NO_RUNTIME="运行时目录不存在"
M_UN_ASK_STARSHIP="处理 ~/.config/starship.toml？（有安装备份会先还原，没有才删除；你自己改过就选 n）"
M_UN_ASK_ITEM="执行这一项？%s"
M_UN_KEEP_ITEM="跳过"
M_UN_RM_APPLE="删 macOS 终端里本工具的 Profile"
M_UN_RM_GIT="从 ~/.gitconfig 移除本工具引用"
M_UN_RM_TMUX="从 ~/.tmux.conf 移除本工具引用"
M_UN_RM_STARSHIP="删 starship.toml"
M_UN_RESTORE_STARSHIP="从备份还原 starship.toml：%s"
M_UN_KEEP_STARSHIP="保留 starship.toml"
M_UN_RM_GHOSTTY_THEMES="删 Ghostty 的 hekouwang-* 主题"
M_UN_ASK_GHOSTTY="Ghostty config 有备份，还原它？"
M_UN_RESTORE_GHOSTTY="还原 Ghostty config ← %s"
M_UN_RM_GHOSTTY_CFG="删本套装写的 Ghostty config"
M_UN_RM_BAT="删 bat 的 hekouwang-* 主题"
M_UN_RM_VSC="删编辑器主题扩展（%s）"

M_UN_S2B="2b. macOS 自带「终端」"
M_UN_INSIDE_APPLE="本脚本正跑在自带终端里，跳过（改了会被它退出时覆盖，且可能关掉你自己）"
M_UN_INSIDE_APPLE_FIX="换个终端跑一次本脚本即可还原"
M_UN_APPLE_DRY="删掉自带终端里本套装的 Profile，默认 Profile 还原成原来那个"
M_UN_APPLE_NONE="自带终端没有本套装的 Profile"
M_UN_APPLE_RUNNING="自带终端正开着 —— 它退出时会覆盖，请 Cmd+Q 完全退出一次"
M_UN_APPLE_BAK="首次改动前的完整备份留在 ~/.hekouwang-AppleTerminal-prefs.bak.plist（要彻底还原：defaults import com.apple.Terminal <该文件>）"

M_UN_S3="3. 从你自己的配置里摘掉引用"
M_UN_GIT_DRY="从 ~/.gitconfig 摘掉 hekouwang-terminal 的 [include]"
M_UN_GIT_DONE="已从 ~/.gitconfig 摘掉 include（原文件已备份）"
M_UN_GIT_NONE="~/.gitconfig 里没有本套装的 include"
M_UN_TMUX_DRY="从 ~/.tmux.conf 摘掉 source-file 行"
M_UN_TMUX_DONE="已从 ~/.tmux.conf 摘掉 source-file（原文件已备份）"
M_UN_TMUX_NONE="~/.tmux.conf 里没有本套装的引用"


M_UN_S5="5. iTerm2 GUI 设置（还原成 iTerm2 出厂默认）"
M_UN_INSIDE_ITERM="本脚本正跑在 iTerm2 里，跳过 GUI 设置的还原"
M_UN_INSIDE_ITERM_WHY="原因：还原这几项要先退出 iTerm2，而在这儿退出=关掉你正在用的终端、卸载中断"
M_UN_INSIDE_ITERM_FIX="补法：用系统自带「终端」App 跑一次 %s/uninstall.sh"
M_UN_INSIDE_ITERM_WHAT="跳过的是：Minimal 主题 / 默认 Profile / Shift+Enter / 隐藏滚动条等外观项"
M_UN_ASK_GUI="把本套装写的 iTerm2 设置删掉、恢复出厂默认？"
M_UN_ITERM_RUNNING="iTerm2 正在运行，先退出它（否则写入会被它的内存配置覆盖）"
M_UN_DEFAULT_KEPT="默认 Profile 已不是本套装的，保持不动"
M_UN_KEYMAP_DRY="摘掉 Shift+Enter 键映射（保留你自己的其它映射）"
M_UN_ASK_PRESSHOLD="顺便恢复「长按按键弹重音菜单」（本套装为 vim 关掉了它）？"
M_UN_KEEP_GUI="保留 iTerm2 GUI 设置"

M_UN_S6="6. 命令行工具（默认不卸 —— 它们对你可能已经是日常工具）"
M_UN_INSTALLED_HERE="本机装着：%s"
M_UN_ASK_BREW="把这些 brew 包也卸掉？（大多数人应该选 n）"
M_UN_KEEP_BREW="保留（它们不依赖本套装，卸载后照常能用）"
M_UN_NO_BREW="没有本工具的 brew 安装记录（旧版安装不记录，无法区分哪些是当时装的）"
M_UN_ASK_OMZ="删掉 oh-my-zsh？（不是本套装的东西，只是被它用了）"
M_UN_RM_OMZ="删 ~/.oh-my-zsh"
M_UN_KEEP_OMZ="保留 oh-my-zsh"

M_UN_DONE="═══ 完成 ═══"
M_UN_DONE_DRY="以上是 dry-run，什么都没动。去掉 --dry-run 才真执行。"
M_UN_DONE_REAL_A="已还原。"
M_UN_DONE_REAL_B="关掉当前终端窗口重开一个，新配置才生效。"
M_UN_DONE_KEPT="没被碰过的：Homebrew 本体、~/.zshrc.local、你自己的 ssh/git 配置、"
M_UN_DONE_KEPT2="  ~/Library/Fonts 里的字体（想删：brew uninstall --cask font-maple-mono-nf-cn）。"
