# INSTALL

首方安装器需要 Python 3.9+；macOS/Linux 另需 curl，Windows 需要 PowerShell。不会安装其他 Skill，不会安装第二套客户端。
Shell：下载官网 install.sh 后运行 `sh install.sh --agent codex`。可选 claude、cursor、auto（多个宿主时拒绝自动选择）。
PowerShell：下载 install.ps1 后执行 `& ./install.ps1 --agent claude`。
宿主目录分别为用户目录下 `.codex/skills`、`.claude/skills`、`.cursor/skills`。安装后重启宿主，按兼容矩阵核验。
默认官网源；指定 `--source github --version 0.1.1` 使用 GitHub Release。离线可提供 `--manifest-file` 和 `--package-file`，仍校验摘要。
安装目录只含技能，状态/备份在 `~/.openlx/skills/openlx-weixin-baimindan/<agent>`，凭据不存入其中。
