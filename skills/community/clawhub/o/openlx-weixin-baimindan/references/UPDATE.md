# UPDATE

首次使用或距上次检查超过7天才联网，最长约4秒，失败退出码0，不阻断网关任务，无调度器。
`check-update.sh --agent codex` 检查；`update.sh --agent codex` 提示确认；无交互不覆盖。用户已明确同意时传 `--yes`。
本地修改总是先备份，另需 `--confirm-local-changes` 才覆盖。回退 `rollback.sh --agent codex --yes`；指定历史版本用安装器 `--version 0.1.1`。
拒绝更新不影响当前技能。回退不更改远端版本。卸载 `uninstall.sh --agent codex`，备份保留。Windows 使用同名 ps1。
