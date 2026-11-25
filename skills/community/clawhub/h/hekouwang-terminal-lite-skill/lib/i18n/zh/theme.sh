#!/bin/bash
# 词条表 · 中文 · theme.sh

blk_theme_help() {
  cat <<'EOF'
hekouwang-terminal-skill — 一键换肤（终端 + 整条工具链）

用法:
  ./scripts/theme.sh                      有 fzf：模糊选主题 + 右侧 ANSI 整块预览；否则画廊
  ./scripts/theme.sh --pick               强制走 fzf 选肤（没有 fzf 则退回画廊）
  ./scripts/theme.sh --list               只出画廊，不进 fzf
  ./scripts/theme.sh ember             切到某套主题
  ./scripts/theme.sh ember --p3        切到某套主题并启用 P3 广色域（iTerm2 + Ghostty）
  ./scripts/theme.sh ember --plain     切到某套主题并关闭所有终端的 eza 图标（没有 Nerd Font）
  ./scripts/theme.sh --preview ember   单套整块预览（提示符/文件列表/git diff/语法高亮/标色）
  ./scripts/theme.sh --gallery            全部主题挨个整块预览（给付费仓截图用）
  ./scripts/theme.sh --plan ember      写入前列出本次会管理的文件
  ./scripts/theme.sh --rollback           恢复最近一次换肤前快照
  ./scripts/theme.sh --history            查看保留的最近五份快照
  ./scripts/theme.sh --audit              色板体检：对比度地板 / 明暗分档 / 暗字槽
  ./scripts/theme.sh --lang en            切回英文

一条命令切的不只是终端底色，还有 bat / fzf / eza / delta(git diff) /
tmux / Ghostty / Warp / cmux / Tabby / VS Code —— 全部来自同一份色板，不会互相漂。
EOF
}

M_THEME_LIST_TITLE="可选主题："
M_THEME_CURRENT="← 当前"
M_THEME_TONE_DARK="暗底"
M_THEME_TONE_LIGHT="亮底"
M_THEME_HINT_SWITCH="换肤 "
M_THEME_HINT_PREVIEW="    看整块预览 "
M_THEME_HINT_GALLERY="    整套预览 "
M_THEME_HINT_PICK="模糊选 "
M_THEME_HINT_PICK_HOW="（装了 fzf 时；右侧是 ANSI 预览）"
M_THEME_PICK_PROMPT="主题 ›"
M_THEME_PICK_HEADER="当前：%s   Enter 切换 · Ctrl+/ 显隐预览 · Esc 取消"
M_THEME_PICK_NO_FZF="本机没有 fzf，退回画廊。装：brew install fzf"
M_THEME_PICK_NO_TTY="非交互终端，退回画廊"
M_THEME_PICK_ABORT="已取消，主题未改"

M_THEME_PREVIEW_WHICH="✗ 要预览哪套？"
M_THEME_PREVIEW_FAIL="✗ 预览渲染失败"
M_THEME_PREVIEW_NEED="  需要 python3，且 config/themes/ 下有 %s.json（先跑 python3 _generate.py）"

M_THEME_NO_SUCH="✗ 没有主题 '%s'"
M_THEME_TX_SNAPSHOT="安全快照：%s"
M_THEME_TX_SNAPSHOT_FAIL="✗ 无法创建安全快照，本次没有修改任何配置"
M_THEME_TX_APPLY_FAIL="✗ 主题应用失败"
M_THEME_TX_AUTO_ROLLBACK="已自动恢复到切换前状态"
M_THEME_TX_ROLLBACK_FAIL="自动回滚失败；快照位置：%s"
M_THEME_PLAN_HEAD="%s 的变更计划"
M_THEME_PLAN_NOTE="这里只读不写；确认后运行 ./scripts/theme.sh <主题>。"
M_THEME_ROLLBACK_OK="✓ 已恢复快照 %s"
M_THEME_ROLLBACK_NOTE="请新开一个 tab；Ghostty 可能还要按 Cmd+Shift+,"
M_THEME_ROLLBACK_NONE="✗ 没有找到可用的快照"
M_THEME_SEC_TERMINAL="终端"
M_THEME_SEC_MULTI="多终端"
M_THEME_SEC_TOOLCHAIN="工具链"
M_THEME_ITERM_FONT="字体 %s"
M_THEME_ITERM_NOTE="保存即生效；已开着的窗口按 Cmd+T 开新 tab 看效果"
M_THEME_MULTI_ITEMS="Ghostty / Warp / cmux / Tabby / macOS 自带终端"
M_THEME_PAID_ONLY="付费包能力"
M_THEME_ECO_ITEMS="bat / fzf / eza / git diff / tmux"
M_THEME_ECO_SAME="同色"
M_THEME_ECO_NOTE="当前 shell 立刻生效：source ~/.config/hekouwang-terminal/current/colors.sh"
M_THEME_ECO_TMUX="tmux 已重载"
M_THEME_ECO_DEFAULT="保持各自默认色"
M_THEME_ECO_PAID_NOTE="一份色板管住整条工具链是付费包能力；开源版只同步 iTerm2"
M_THEME_WS_OK="项目工作区变体"
M_THEME_WS_REBUILT="已跟着重建"
M_THEME_SEE_IT="看这套主题长什么样："
# 只在付费件缺席时打。上面的回执已经说了那几行被跳过，这一行负责告诉他去哪儿拿。%s = 落地页
M_THEME_PAID_WHERE="让这份色板走出 iTerm2：%s"

M_THEME_NO_LIGHT="✗ 没有亮色主题可用"
M_THEME_NO_LIGHT_NOTE1="  亮色主题（parchment / ledger）在付费包里；"
M_THEME_NO_LIGHT_NOTE2="  也可以自己在 config/themes/palettes/ 加一套 light=True 的色板。"

# ---- 付费半边（config/themes/_apply_pro.sh）----
M_THEME_PRO_BAT_CACHE="  首次使用这套主题，正在为 bat 建缓存（几秒）…"
M_THEME_PRO_GHOSTTY_NOTE="不会自动重载，按 Cmd+Shift+, 生效"
M_THEME_PRO_GHOSTTY_PAID="多终端同步是付费包能力，开源版只管 iTerm2"
M_THEME_PRO_GHOSTTY_ABSENT="本机未安装或未配置过"
M_THEME_PRO_WARP_NOTE="已改 settings.toml；Warp 里没变就重启它"
M_THEME_PRO_WARP_FAIL="settings.toml 改写失败 —— 主题文件已就位，但没切过去"
M_THEME_PRO_WARP_MANUAL="没找到 ~/.warp/settings.toml，Settings → Appearance 里手动选一次"
M_THEME_PRO_APPLE="macOS 自带终端"
M_THEME_PRO_APPLE_PAID="多终端同步是付费包能力"
M_THEME_PRO_APPLE_INSIDE="本脚本正跑在它里面，改了会被它退出时覆盖"
M_THEME_PRO_APPLE_INSIDE_NOTE="换个终端跑一次 ./scripts/theme.sh %s 即可同步"
M_THEME_PRO_APPLE_ICONS="策略 icons：它只支持单字体，选了自带 Nerd 图标的那套"
M_THEME_PRO_APPLE_ICONS2="想统一用 %s：把 config/font.conf 的 APPLE_TERMINAL_FONT 改成 match"
M_THEME_PRO_APPLE_MATCH="策略 match：与主字体统一；它不含 Nerd 图标，所以这里的 ls 不显示图标（不是坏了）"
M_THEME_PRO_APPLE_RUNNING="⚠ 自带终端正开着 —— 它退出时会覆盖设置，请 Cmd+Q 完全退出再打开"
M_THEME_PRO_APPLE_NEXT="下次打开即生效（已设为默认 Profile）"
M_THEME_PRO_APPLE_FAIL="同步失败（不影响其它终端）"
