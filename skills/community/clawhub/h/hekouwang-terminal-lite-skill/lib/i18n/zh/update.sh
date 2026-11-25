#!/bin/bash
# 词条表 · 中文 · update.sh

blk_update_help() {
  cat <<'EOF'
hekouwang-terminal-skill — 更新到最新版

用法:
  ./scripts/update.sh              拉更新 → 重新生成主题 → 重新部署当前主题
  ./scripts/update.sh --check      只看有没有新版本和更了什么，不动任何东西
  ./scripts/update.sh --lang en    切回英文

为什么要有这个脚本：以前「更新」= 群里发个新压缩包、你自己重下重装，
既不知道自己是不是最新版，也不知道这次更了啥。这个脚本两件事都回答。

它不碰你的 ~/.zshrc.local、不碰你自己改过的 GUI 设置；
只重新生成主题文件、重新部署当前正在用的那套。
EOF
}

M_UP_HEAD="═══ hekouwang-terminal-skill 更新 ═══"
M_UP_CURRENT="当前版本 %s"
M_UP_UNKNOWN="未知"
M_UP_NOT_GIT="这不是 git 仓库（大概是解压的 zip 包）。"
M_UP_NOT_GIT_1="更新方式：去拿最新压缩包，解压到同一个目录覆盖，然后跑一次 ./scripts/install.sh。"
M_UP_NOT_GIT_2="你的 ~/.zshrc.local 和 GUI 设置不会被覆盖。"
M_UP_S1="1. 检查远端"
M_UP_NO_NET="⚠ 连不上远端（网络？国内需科学上网或用镜像），本地版本保持不变"
M_UP_UP_TO_DATE="✓ 已经是最新版，无需更新"
M_UP_N_COMMITS="有 %s 个新提交"
M_UP_S2="2. 这次更了什么"
M_UP_CHANGELOG="CHANGELOG 新增："
M_UP_CHECK_ONLY="--check 模式，什么都没动。真更新：./scripts/update.sh"
M_UP_S3="3. 检查本地改动"
M_UP_DIRTY="⚠ 你在这个目录里改过东西："
M_UP_ASK_STASH="先 stash 起来再更新？（选 n 会中止更新）"
M_UP_ABORTED="已中止。你可以自己 commit 或 stash 后重跑。"
M_UP_STASHED="✓ 已 stash（恢复：git stash pop）"
M_UP_STASH_MSG="update.sh 自动 stash %s"
M_UP_S4="4. 拉取更新"
M_UP_PULLED="✓ 代码已更新"
M_UP_PULL_FAIL="⚠ pull 失败（可能有冲突）。手动处理：git pull"
M_UP_BRAND_GONE="⚠ 品牌色板不见了 —— 这不该发生，从你的付费包里再拷一份 brand.py 回来"
M_UP_S5="5. 重新生成主题"
M_UP_S6="6. 刷新提示符配置"
M_UP_SS_NEW="✓ 已装上提示符配置"
M_UP_SS_SAME="· 提示符配置无变化"
M_UP_SS_UPDATED="✓ 提示符配置已更新"
M_UP_SS_BAK="旧的备份在 %s"
M_UP_SS_NOTE="自己改过的话，从备份里把你的改动挑回来"
M_UP_S7="7. 重新部署当前主题"
M_UP_NO_THEME="· 没记录当前主题，跳过（自己跑一次 ./scripts/theme.sh <主题>）"
M_UP_BAT="✓ bat 主题已刷新"
M_UP_DONE="═══ 更新完成 ═══"
M_UP_DONE_NOTE="新开一个终端窗口生效。有问题跑 ./scripts/doctor.sh。"
