# 10 条日常技巧（免费版）

按使用频率排，每条只写「什么时候用 + 命令 + 一个坑」。

1. **装之前先预演**：`./scripts/install.sh --dry-run` 列出会改的文件和系统设置，确认后再去掉 `--dry-run`。
2. **国内网络卡住**：`CN=1 ./scripts/install.sh` 走镜像；卡在 `portable-ruby` / `SSL_ERROR_SYSCALL` 时先用这条。
3. **已有 `.zshrc` 不要直接 install**：先 `./scripts/migrate.sh` 看报告，再 `--apply`；它会按段落迁移，不会拦腰砍断 `for…done`。
4. **只看不换**：`./scripts/theme.sh --preview ember` 渲染一整块假终端（提示符、eza、git diff、语法高亮），不动物理配置。
5. **一次看全部**：`./scripts/theme.sh --list` 出画廊，每套带 16 色条；有 fzf 时直接 `./scripts/theme.sh` 模糊选。
6. **换之前看清单**：`./scripts/theme.sh --plan ember` 列出本次会管理的文件，一个字节都不写。
7. **换错了回退**：`./scripts/theme.sh --rollback` 恢复最近一次换肤前快照；最近 5 份用 `--history` 看。
8. **一眼体检**：`./scripts/doctor.sh --status` 看主题 / 跟随 / Node / 语义 / Ghostty 重载的状态机。
9. **启动慢先量再改**：`./scripts/doctor.sh --profile` 用临时 `ZDOTDIR` 跑 zprof，点名 top 8 耗时项，不靠猜。
10. **卸载前先看清单**：`./scripts/uninstall.sh --dry-run` 列出会还原什么；确认后才执行 `./scripts/uninstall.sh`。

## 一条给 AI CLI 的

`Shift + Enter` 换行不提交。给 Claude Code / CodeBuddy 写多行 prompt 时，这是每天用得最多的一条。
