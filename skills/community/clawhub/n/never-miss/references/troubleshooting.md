# 故障排查（troubleshooting）

> 用途：命令返回错误码时，对照本表给出修复指引。**按需加载。**

## 错误码速查

| code | 含义 | 处置 |
|---|---|---|
| `E_ARGS` | 参数/契约字段缺失或非法 | 检查命令参数与 Event JSON 字段，修正后重试 |
| `E_CONFIG` | 配置缺失/非法 | 运行 `init` 重新生成；或修正 config.yaml（保持模板结构、不含 password 键） |
| `E_KEYCHAIN` | 凭据缺失/读取失败 | 运行 `secret set <邮箱>`，密码经 stdin 传入 |
| `E_IMAP` | 连接/登录/网络失败 | 该账户游标不动、下次重试；对话中提示用户检查网络与专用密码 |
| `E_CALENDAR` | 日历不存在/不可写/Calendar.app 不可用 | 见下方"日历问题" |
| `E_AUTH` | osascript 自动化授权被拒 | 见下方"授权问题" |
| `E_UNSUPPORTED` | 非 macOS | 仅生成 .ics，提示用户手动导入 |
| `E_STATE` | state.json 损坏 / UIDVALIDITY 变化 | 游标已重置并告警；说明"邮箱可能被重建，将重新初始化" |
| `E_INTERNAL` | 未预期异常 | 上报原始错误信息 |

## 授权问题（E_AUTH / -1743）

1. 引导用户：系统设置 → 隐私与安全性 → 自动化 → 找到"日历"，勾选允许
2. 若列表里没有：重新跑一次 `doctor --write-test`，会再次弹出授权窗，点"好"
3. 授权长期有效；授权被拒期间 `create` 会自动降级为 .ics 输出

## 日历问题（E_CALENDAR）

- Calendar.app 未运行：osascript 报 `-600 应用程序没有运行`，需先启动日历（命令行 `open -a Calendar`，或让用户手动打开"日历"应用）再重试。自动扫描若 Calendar.app 未运行，`create` 会自动降级为 .ics，不会丢事件
- 专用日历不存在 → `doctor` 会自动创建
- `location: icloud` 但账号未登录 iCloud → 改用 `location: local`（On My Mac）后重试
- macOS 26 已移除 AppleScript 的 `source` 类，无法按名称指定 iCloud/On My Mac 位置；`calendar.location` 仅作语义保留，实际统一创建到系统默认位置

## 凭据失效（E_IMAP 登录失败）

- 提示用户重新生成专用密码，再 `secret set <邮箱>` 更新
- 该账户 `enabled: false` 可临时停用，不影响其他账户

## 游标异常（E_STATE）

- `UIDVALIDITY` 变化通常因邮箱被清空/迁移重建 → 脚本自动重置游标为"只处理新邮件"，历史不再回溯
- 如需回溯历史：设该账户 `backfill_days > 0` 后重跑

## .ics 手动导入

降级生成的 `.ics` 位于 `ics/` 目录。提示用户：双击文件 → 选择导入到"AI 提醒"日历；或"文件 → 导入"。文件以 UID 前缀命名，重复导入同一文件会被日历端按 UID 去重。

## 已知局限

- `.ics` 附件的 `TZID` 时区不解析 VTIMEZONE，非 UTC/本地时区的邀请时间可能有偏差；此时建议以正文时间为准复核
- 仅解析 `.ics` 附件，其他附件（含内联图片）一律忽略（需求 §6.5）
