# powpow-cli

PowPow 平台共享命令行执行层（零依赖 Node.js CLI），供 powpow-simple / powpow-publisher / powpow-integration 等 skill 调用。

## 为什么独立成包

此前每个 PowPow skill 各自携带一份相同脚本，其中：

- login 接受 argv 传密码（落 shell history / 进程列表）
- session.json 无文件权限约束
- publish / create-digital-human / delete-post 无代码级确认门
- 用户态 config.json 可改写 platformUrl，凭据可能被重定向

这些导致 ClawHub 扫描全部命中 suspicious。"一份脚本 × N 个语言包"也让修复无法收敛。

本包是一次性收口：**所有凭据与网络副作用集中在这里，skill 只做对话编排和预览确认**。

## 安全基线

| 项 | 行为 |
|---|---|
| 密码输入 | 仅 TTY 隐藏输入 / stdin / `POWPOW_PASSWORD` env；argv 直接拒绝 |
| 会话文件 | `~/.powpow/session.json`，0600，目录 0700（POSIX）；`logout` 可清除 |
| 写操作 | 无 `--confirm` 即 dry-run（exit 3），不触碰网络写 |
| platformUrl | 白名单锁定 `https://global.powpow.online` |
| 输出 | 任何命令不打印 token / 密码 |

## 使用

详见 [SKILL.md](SKILL.md)。

```bash
node scripts/doctor.js
node scripts/login.js <username>
node scripts/compose.js --text-file draft.txt
node scripts/publish.js post-draft.html            # dry-run
node scripts/publish.js post-draft.html --confirm  # 发布
node scripts/logout.js
```
