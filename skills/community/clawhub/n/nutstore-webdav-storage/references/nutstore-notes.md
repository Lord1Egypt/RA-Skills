# Nutstore / WebDAV 注意事项

说明：
- 这份文档只负责“Nutstore / WebDAV 场景下的经验、排障顺序、使用注意事项”
- 默认/自定义同步边界与恢复边界，优先看 `storage-scope.md`
- 初始化顺序、cron 接入、检查脚本用法，优先看 `automation.md`

## 1. 坚果云只做备份层，不做运行盘

统一口径：
- 坚果云 WebDAV 只作为远端备份 / 归档 / 恢复源
- 不把坚果云挂载目录当 OpenClaw 工作区运行盘

原因：
- WebDAV 更适合备份与同步，不适合承载高频实时读写
- 运行中目录若直接放在远端挂载层，容易把同步延迟、网络波动、锁问题引入主工作区
- 当前 skill 的目标是“轻量备份 / 定点恢复”，不是远端实时工作盘

## 2. 先验证 remote，再谈自动化

推荐顺序：
1. 先完成 `rclone config`
2. 先执行 `rclone lsd nutstore:`
3. 再执行默认备份 dry-run
4. 再执行正式备份
5. 至少完成一次恢复 dry-run 或测试目录恢复验收
6. 最后才接 cron

不要跳过 `rclone lsd nutstore:` 这一步直接上自动化。

## 3. 优先使用应用密码，不用账号登录密码

统一规则：
- `rclone` 配坚果云时优先使用应用密码
- 不把账号登录密码直接写进脚本或仓库

建议：
- 优先通过 `rclone config` 交互录入
- 如必须自动化注入，使用临时环境变量
- 不在记忆、文档、仓库中记录敏感原文

## 4. 出现连通问题时，先查最小链路

遇到备份失败、恢复失败、远端访问异常时，优先按以下顺序排查：

1. `rclone version`
2. `rclone lsd nutstore:`
3. `rclone lsd nutstore:/openclaw-backup`
4. 再看具体 backup / restore / check 脚本输出

优先区分：
- 是 `rclone` / remote 本身不可用
- 还是 skill 脚本里的路径或参数问题

## 5. 真实恢复验收优先恢复到测试目录

统一规则：
- 真实恢复验收优先使用 `RESTORE_TARGET_ROOT`
- 不直接把首次真实恢复落到正式工作区

示例：

```bash
RESTORE_TARGET_ROOT="$PWD/temp/nutstore-restore-test" \
bash skills/nutstore-webdav-storage/scripts/restore-openclaw-from-nutstore.sh chief path memory/YYYY-MM-DD/YYYY-MM-DD.md
```

这样可以先确认：
- 远端路径是否正确
- 本地落点是否正确
- 恢复内容是否与预期一致

## 6. 区分“脚本故障”和“样本漂移”

真实恢复比对失败时，不要第一反应就判定恢复脚本坏了。

已验证过的一个典型现象：
- 备份完成后，本地源文件又继续被编辑
- 随后拿“当前本地文件”去和“之前备份版本恢复出的文件”比对
- 会出现 `cmp` 或哈希不一致

这类情况属于：
- 验收样本漂移
- 不是恢复链路必然故障

正确处理顺序：
1. 先确认恢复脚本落点是否正确
2. 再判断备份后源文件是否发生追加编辑
3. 如源文件已变化，先重备最新版本，再做比对

## 7. `path` 恢复到正式工作区必须显式确认

当前 V1.1 已新增保护规则：
- `path` 模式恢复到正式工作区时，必须显式设置 `RESTORE_FORCE=1`
- 恢复到测试目录不受影响

说明：
- 这里强调的是“为什么这条规则重要”与“实际使用时如何避免误操作”
- 这条规则本身的正式边界定义，优先看 `storage-scope.md`
- 具体执行示例，优先看 `automation.md`

## 8. 默认模式长期更稳，自定义模式只在明确需求下启用

统一建议：
- 没有特别说明时，长期跑默认模式即可
- 只有当额外目录确实值得长期保留时，再启用 `CUSTOM_BACKUP_PATHS`

原因：
- 默认模式边界清楚
- 更适合 cron 自动化
- 更不容易随着业务目录膨胀而失控

## 9. 路径统一口径优先用 WORKSPACE_ROOT

当前统一路径口径：
- 优先：`WORKSPACE_ROOT`
- 兼容：`OPENCLAW_ROOT`
- 默认通用根目录：`$HOME/.openclaw/workspace`

建议所有执行示例优先按这个口径走，避免继续写死个人绝对路径。
