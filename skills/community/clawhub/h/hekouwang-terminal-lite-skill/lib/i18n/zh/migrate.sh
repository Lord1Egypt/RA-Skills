#!/bin/bash
# 词条表 · 中文 · migrate.sh

blk_migrate_help() {
  cat <<'EOF'
hekouwang-terminal-skill — 接管已有 .zshrc（而不是覆盖它）

用法:
  ./scripts/migrate.sh              先看报告，再决定要不要写
  ./scripts/migrate.sh --apply      直接执行（仍然会先备份）
  ./scripts/migrate.sh --lang en    切回英文

为什么要有这个脚本：install.sh 是拿模板覆盖 ~/.zshrc 的。新机器没问题，
但你要是已经用了几年、里面攒了一堆 alias / PATH / 公司环境变量，
覆盖 = 一次性全丢（虽然有 .bak，但你得自己一行行捞回来）。

这个脚本干的事：把你 .zshrc 里「只有你才有」的行挑出来搬进 ~/.zshrc.local，
把「模板本来就会提供」的行（omz 初始化、starship、fzf/zoxide/atuin 的 init、
插件 source 等）丢掉 —— 因为模板会用更好的顺序重新给你一份。

判定是保守的：拿不准的一律算「你的」，宁可多搬也不漏搬。
搬完 ~/.zshrc.local 会被模板自动 source，所以你的东西一条都不会少。
EOF
}

M_MIG_HEAD="═══ 接管已有 .zshrc ═══"
M_MIG_NO_ZSHRC="没有 ~/.zshrc —— 全新环境，直接跑 ./scripts/install.sh 就行，不需要迁移。"
M_MIG_OVERLAP="你的 ~/.zshrc 有 %s%% 的代码行和本套装模板一模一样"
M_MIG_OVERLAP_1="  —— 也就是说它本来就是这套模板（大概率是装过旧版本，现在想升级）。"
M_MIG_OVERLAP_2="这种情况不该迁移"
M_MIG_OVERLAP_3="：模板里的东西会被当成「你的」搬进 ~/.zshrc.local，"
M_MIG_OVERLAP_4="  结果两边各留一份，插件重复加载、别名重复定义，还可能起不来 shell。"
M_MIG_OVERLAP_5="直接跑 ./scripts/install.sh 就行"
M_MIG_OVERLAP_6="（它会先把 ~/.zshrc 备份进 ~/.hekouwang-terminal-backups/）。"
M_MIG_OVERLAP_7="真有极少数自定义散落在 .zshrc 里？先自己 diff 一眼："
M_MIG_OVERLAP_8="把属于你的几行手工挪进 ~/.zshrc.local，再 ./scripts/install.sh。"
M_MIG_OVERLAP_9="确实要强行迁移：./scripts/migrate.sh --force --apply"

M_MIG_SYNTAX_FAIL="⚠ 自动切分的结果语法不通过，已中止 —— 不会写出一个坏掉的 .zshrc.local"
M_MIG_SYNTAX_FIX1="请手动迁移：把 ~/.zshrc 里你自己的 alias/export/函数复制进 ~/.zshrc.local，"
M_MIG_SYNTAX_FIX2="然后 cp %s/config/zshrc.template ~/.zshrc"

M_MIG_TOTAL="原 ~/.zshrc 共 %s 行"
M_MIG_KEPT="%s 行是你自己的 → 搬进 ~/.zshrc.local"
M_MIG_DROPPED="%s 行模板会重新提供 → 丢掉"
M_MIG_DROP_HEAD="会丢掉哪些（以及为什么）"
M_MIG_KEEP_HEAD="会搬走哪些（前 30 行预览）"
M_MIG_KEEP_MORE="…还有 %s 行"
M_MIG_KEEP_NONE="（没有需要搬的东西）"
M_MIG_PREVIEW_ONLY="以上只是预览，什么都没动。"
M_MIG_PREVIEW_NEXT="确认没问题就跑：./scripts/migrate.sh --apply"
M_MIG_PREVIEW_WHAT="（--apply 会：备份原 .zshrc → 把上面这些行追加进 ~/.zshrc.local → 部署模板）"

M_MIG_RUNNING="执行中"
M_MIG_BAK="原 .zshrc 已备份 → %s"
M_MIG_LOCAL_BAK="原 .zshrc.local 已备份 → %s"
M_MIG_APPENDED="你的配置已追加进 %s"
M_MIG_TEMPLATE="已部署模板 ~/.zshrc（末尾会自动 source ~/.zshrc.local）"
M_MIG_BANNER1="以下内容由 migrate.sh 于 %s 从原 ~/.zshrc 搬来"
M_MIG_BANNER2="原文件备份在 %s"

M_MIG_VERIFY="验证：新配置能不能起一个 shell"
M_MIG_VERIFY_SLOW="⚠ 能起来，但花了 %ss（偏慢）"
M_MIG_VERIFY_SLOW_FIX="跑 ./scripts/doctor.sh --profile 看是谁占的时间。"
M_MIG_VERIFY_OK="✓ 正常（%ss 内）"
M_MIG_VERIFY_FAIL="✗ 起不来或超过 25 秒 —— 自动回滚"
M_MIG_ROLLED_BOTH="~/.zshrc 和 ~/.zshrc.local 都已还原成迁移前的样子"
M_MIG_ROLLED_ONE="~/.zshrc 已还原成迁移前的样子"
M_MIG_ROLLED_NOTE="没有把你留在坏掉的状态里。请手工迁移："
M_MIG_ROLLED_NOTE2="把 ~/.zshrc 里属于你的 alias/export/函数复制进 ~/.zshrc.local，"
M_MIG_ROLLED_NOTE3="然后 cp %s/config/zshrc.template ~/.zshrc"

M_MIG_DONE="完成。"
M_MIG_DONE_NOTE="开个新终端窗口验证；有问题就一键回退："
M_MIG_DONE_DOCTOR="建议顺手跑一次 ./scripts/doctor.sh 看加载顺序对不对。"
