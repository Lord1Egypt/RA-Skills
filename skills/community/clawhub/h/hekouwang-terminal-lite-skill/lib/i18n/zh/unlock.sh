#!/bin/bash
# 词条表 · 中文 · unlock.sh

blk_unlock_help() {
  cat <<'EOF'
hekouwang-terminal-skill — 一条命令装上付费包

  ./scripts/unlock.sh ~/Downloads/hekouwang-terminal-skill-paid-20260723.zip
  ./scripts/unlock.sh <zip> --dry-run     只说要做什么，不动任何文件
  ./scripts/unlock.sh <zip> --no-apply    解压并重新生成，但不重新部署主题
  ./scripts/unlock.sh --rollback          恢复最近一次付费更新前快照
  ./scripts/unlock.sh <zip> --allow-downgrade  明确安装旧版本
  ./scripts/unlock.sh <zip> --lang en     切回英文
EOF
}
M_UL_ROLLBACK_OK="已恢复付费更新快照 %s"
M_UL_ROLLBACK_NONE="没有找到付费更新快照"
M_UL_DOWNGRADE_BLOCKED="已阻止降级：当前 %s，升级包 %s"
M_UL_DOWNGRADE_HINT="只有明确需要旧版本时才使用 --allow-downgrade"
M_UL_SNAPSHOT_FAIL="无法创建付费更新安全快照"
M_UL_SNAPSHOT_OK="安全快照：%s"
M_UL_AUTO_ROLLBACK="更新失败，已自动恢复更新前的产品文件"
M_UL_AUTO_ROLLBACK_FAIL="自动恢复失败；快照位置：%s"

M_UL_USAGE="用法：./scripts/unlock.sh <付费包.zip> [--dry-run] [--no-apply] [--allow-downgrade]"
M_UL_USAGE_1="  还没有付费包？开源版本来就是完整可用的，不装它也不影响任何现有功能。"
M_UL_USAGE_2=""
M_UL_USAGE_3="  付费包解锁的是：4 套品牌主题（含 2 套亮色）+ Ghostty/Warp/自带终端同步"
M_UL_USAGE_4="  + bat/fzf/eza/git diff/tmux/VS Code 全生态同色 + 字体优先级表 + 速查卡。"
M_UL_UNKNOWN_ARG="未知参数：%s"

M_UL_S1="1. 校验付费包"
M_UL_NO_FILE="文件不存在：%s"
M_UL_FILE_OK="文件存在（%s）"
M_UL_ZIP_OK="压缩包完整（unzip -t 通过）"
M_UL_ZIP_BAD="压缩包损坏或不完整，重新下载一次"
M_UL_IS_PAID="确认是付费包（含 %s）"
M_UL_NOT_PAID="这不像是本套装的付费包 —— 里面没有 %s"
M_UL_YOUR_ZIP="  你选的 zip 是：%s"

M_UL_S2="2. 校验安装位置"
M_UL_DIR_OK="当前目录是 hekouwang-terminal-lite-skill：%s"
M_UL_DIR_BAD="这里不像 hekouwang-terminal-lite-skill 目录（缺 theme.sh 或 config/themes/_generate.py）"
M_UL_DIR_FIX="  把 unlock.sh 和付费包放在 clone 下来的 hekouwang-terminal-lite-skill 目录里再跑。"
M_UL_ALREADY="! 付费包已经装过一次了，本次会**覆盖**为新版本"

M_UL_S3="3. 解压（%s 个文件）"
M_UL_DRY_HEAD="═══ DRY-RUN：以下都不会真的执行 ═══"
M_UL_DRY_1="会把这些文件解压进 %s（同名覆盖）："
M_UL_DRY_MORE="…… 其余 %s 个"
M_UL_DRY_THEN="然后会跑："
M_UL_DRY_GEN="# 重新生成全部主题"
M_UL_DRY_APPLY="# 重新部署 + 建 bat 缓存"
M_UL_DRY_KEEP="不会碰：你的 ~/.zshrc、~/.zshrc.local、~/.ssh/"
M_UL_DRY_TAIL="去掉 --dry-run 才会真的执行。"

M_UL_UNPACKED="已解压 %s 个文件"
M_UL_UNPACK_FAIL="解压失败"
M_UL_MARKER_MISSING="解压后仍然找不到 %s，请把上面的输出发给我"
M_UL_MARKER_OK="指纹文件已就位"
M_UL_S4="4. 重新生成主题"
M_UL_GEN_OK="生成完成"
M_UL_GEN_FAIL="生成器跑失败了"
M_UL_S5_SKIP="5. 跳过部署（--no-apply）"
M_UL_S5_SKIP_NOTE="  想生效：./scripts/theme.sh ember"
M_UL_S5="5. 重新部署主题"
M_UL_KEEP_THEME="  当前主题是 %s，重新部署一遍让新增的生态配色生效"
M_UL_SWITCH_THEME="  切到默认品牌主题 %s（换别的：不带参数跑 ./scripts/theme.sh 看全部七套）"
M_UL_DONE="═══ 完成 ═══"
M_UL_DONE_1="  换主题：./scripts/theme.sh            （不带参数看全部七套）"
M_UL_DONE_3="  项目工作区：./scripts/workspace.sh"
M_UL_DONE_4="  从一个品牌色推自己的主题：./scripts/palette.sh --from '#e08a5f' --name 我的主题"
M_UL_DONE_5="  速查卡：docs/速查卡.pdf（A4，可直接打印）"
M_UL_DONE_6="  有哪里不对：./scripts/doctor.sh"
M_UL_APPLY_FAIL="主题部署失败 —— 跑 ./scripts/doctor.sh 看是哪一步"
# 版本比对：老免费仓 + 新付费包 = 树里两个版本号不一致
M_UL_VER_SKEW="你的开源版是 %s，这个付费包是 %s"
M_UL_VER_SKEW_FIX="建议先 git pull 再解压 —— 否则免费档那半边会比付费件旧一个版本"
