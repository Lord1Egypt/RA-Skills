#!/bin/bash
# 词条表 · 中文 · sync.sh

blk_sync_help() {
  cat <<'EOF'
hekouwang-terminal-skill — 换机迁移 / 配置漂移检查 / 钉住状态迁移

用法:
  ./scripts/sync.sh                      体检：部署出去的配置和仓库里的还一致吗（只读）
  ./scripts/sync.sh --pull               按仓库重新部署一遍，把漂掉的对回来
  ./scripts/sync.sh --export <路径>       打一个可以带去第二台机器的包（整仓）
  ./scripts/sync.sh --state-export [文件] 导出本机钉住状态（主题/跟随/Node/光学/场景/badge）
  ./scripts/sync.sh --state-import <文件> 在新机按 manifest 还原钉住状态
  ./scripts/sync.sh --lang en            切回英文

解决的问题：你在 A 机器上手改过 Ghostty config、B 机器还是老配置、
半年后完全想不起哪台是对的。这个脚本让「哪儿漂了」变成一句话能看清的事。

换机只带「钉住了什么」用 --state-export / --state-import；
整仓搬家仍用 --export。
EOF
}

M_SY_EXPORT_HEAD="打包用于第二台机器…"
M_SY_EXPORT_COUNT="  %s 个文件 → %s"
M_SY_EXPORT_OK="✓ 打包完成"
M_SY_EXPORT_NEXT="第二台机器上：解压 → cd 进去 → ./scripts/install.sh"
M_SY_EXPORT_BRAND="（含品牌主题包，仅供你本人的机器使用，别转发）"
M_SY_EXPORT_NO_BRAND="（不含品牌主题包，装完只有 3 套社区主题）"

M_SY_STATE_EXPORT_HEAD="导出本机钉住状态…"
M_SY_STATE_EXPORT_OK="✓ 已写入 %s"
M_SY_STATE_EXPORT_NEXT="新机上装好套件后：./scripts/sync.sh --state-import <这份 json>"
M_SY_STATE_IMPORT_NEED="✗ 用法：./scripts/sync.sh --state-import <manifest.json>"
M_SY_STATE_IMPORT_HEAD="按 manifest 还原：%s"
M_SY_STATE_APPLIED_LANG="语言 → %s"
M_SY_STATE_APPLIED_NODE="Node → %s"
M_SY_STATE_APPLIED_THEME="主题 → %s"
M_SY_STATE_APPLIED_OPTICAL="光学 → %s"
M_SY_STATE_APPLIED_SCENE="场景 → %s"
M_SY_STATE_APPLIED_BADGE="badge → %s"
M_SY_STATE_APPLIED_BADGE_FILE="badge 已写入 runtime 文件"
M_SY_STATE_FAIL_NODE="Node 还原失败"
M_SY_STATE_FAIL_THEME="主题还原失败（新机可能没有这套主题）"
M_SY_STATE_FAIL_OPTICAL="光学还原失败"
M_SY_STATE_FAIL_SCENE="场景还原失败"
M_SY_STATE_SKIP_PAID="跳过付费项 %s（开源树没有对应脚本）"
M_SY_STATE_IMPORT_DONE="✓ 钉住状态已尽量还原"
M_SY_STATE_IMPORT_NEXT="建议再跑 ./scripts/doctor.sh --status 看一眼"

M_SY_HEAD="═══ 配置漂移检查 ═══"
M_SY_CURRENT="当前主题：%s"
M_SY_NOT_DEPLOYED="未部署"
M_SY_GEN_HEAD="生成物（应该和仓库逐字节一致）"
M_SY_PROFILE_MISSING="iTerm2 Profile：没部署"
M_SY_PROFILE_NO_SRC="iTerm2 Profile：仓库里没有对应文件"
M_SY_PROFILE_SAME="iTerm2 Profile   [字体按本机探测：%s]"
M_SY_PROFILE_DIFF="iTerm2 Profile 已被改过（字体之外的字段）"
M_SY_COMPARE="对比：diff '%s' '%s'"
M_SY_ECO_COLORS="生态配色 colors.sh"
M_SY_ECO_DELTA="git diff 配色"
M_SY_ECO_TMUX="tmux 配色"
M_SY_ECO_GHOSTTY="Ghostty 主题"
M_SY_NO_THEME="还没部署过主题（跑 ./scripts/theme.sh <主题>）"
M_SY_TPL_HEAD="模板（你改过是正常的，这里只是告诉你改过）"
M_SY_TPL_STARSHIP="starship.toml"
M_SY_TPL_GHOSTTY="Ghostty config"
M_SY_TPL_ZSHRC=".zshrc"
M_SY_LOCAL_HEAD="只属于这台机器的（永远不该进仓库）"
M_SY_LOCAL_OK="~/.zshrc.local 在（%s 行）"
M_SY_LOCAL_MISSING="~/.zshrc.local 不存在（SSH 别名/代理该放这儿）"
M_SY_NOT_DEPLOYED_ITEM="%s：没部署"
M_SY_NO_SRC_ITEM="%s：仓库里没有对应文件"
M_SY_EDITED_ITEM="%s 已被改过"
M_SY_RESULT="═══ 结论 ═══"
M_SY_NO_DRIFT="没有漂移，这台机器和仓库一致。"
M_SY_DRIFT="%d 处和仓库不一致。"
M_SY_DRIFT_KEEP="  想保留本机改动 → 什么都不用做（生成物除外，它们下次重跑生成器会被覆盖）"
M_SY_DRIFT_PULL="  想对回仓库版本 → ./scripts/sync.sh --pull"
M_SY_PULL_HEAD="按仓库重新部署…"
M_SY_PULL_SS="✓ starship.toml 已对回"
M_SY_PULL_SS_SAME="· starship.toml 与仓库一致，没动"
M_SY_PULL_SS_BAK="原配置已备份：%s"
M_SY_PULL_NOTE="注意：~/.zshrc 没动 —— 它可能含你 migrate 过来的东西。"
M_SY_PULL_NOTE2="要连它一起对回：cp %s/config/zshrc.template ~/.zshrc（先自己备份）"
