---
name: powpow-cli
description: PowPow 平台命令行执行层 — login/publish/create-digital-human/delete-post 等已加固的本地 CLI，被各 PowPow skill 调用。所有写操作默认 dry-run，必须 --confirm 才执行。
---

# PowPow CLI — 共享执行层

本包是各 PowPow skill（powpow-simple / powpow-publisher / powpow-integration 等）共用的**加固执行层**。skill 负责对话编排与预览确认，本包负责所有网络与凭据操作。

## 安全契约（请完整阅读后再使用）

1. **密码永远不进对话、不进命令行参数。** 用户自行在终端运行 login（TTY 隐藏输入），或由 agent 用 stdin 管道转交。login 不接受位置参数形式的密码。
2. **写操作默认 dry-run。** `publish` / `create-digital-human` / `delete-post` / `upload-image` 不传 `--confirm` 时只打印计划/预览并以退出码 3 结束，**不触碰网络写操作**（连图片上传都不会发生）。
3. **会话文件受保护。** JWT 存于 `~/.powpow/session.json`（可用 `POWPOW_STATE_DIR` 覆盖），文件权限 0600、目录 0700（POSIX 系统）。完成后用 `node scripts/logout.js` 清除。
4. **平台地址不可被用户配置改写。** `platformUrl` 锁定白名单 `https://global.powpow.online`；state 目录里的 config.json 无法重定向凭据。
5. **token 永不上屏。** 任何命令的输出都不包含 token 或密码。

## 前置条件

- Node.js >= 18（需要全局 fetch）
- 可选：Unsplash key（config.json `unsplashAccessKey` 或环境变量 `UNSPLASH_ACCESS_KEY`），仅图片搜索需要

## 命令清单

自检（任何异常先跑这个）：

```bash
node scripts/doctor.js
```

登录 / 登出 / 状态：

```bash
node scripts/login.js <username>        # TTY 隐藏输入密码；或 echo <pw> | node scripts/login.js <username>
node scripts/logout.js                  # 清除本地会话
```

只读操作（无确认门）：

```bash
node scripts/geocode.js "<地名>" [--city <城市>] [--limit N] [--json]
node scripts/list-digital-humans.js [关键词] [--all] [--limit N] [--json]
node scripts/match-digital-human.js <topic> [--limit N] [--json]
node scripts/search-image.js <query | unsplash-photo-page-url>
node scripts/verify.js <post-id>
```

草稿编排（纯本地，无网络写）：

```bash
node scripts/compose.js --text-file <path> [--dh <id|name:<名>|auto>] [--topic "<topic>"] \
  [--loc <dh|name> --lng x --lat y] [--image <@path|url|search:kw>] [--out <path>] [--no-preview] [--json]
```

写操作（默认 dry-run，加 `--confirm` 才真正执行）：

```bash
node scripts/publish.js <draft.html>             # 只打印摘要，exit 3
node scripts/publish.js <draft.html> --confirm   # 公开发布（不可撤回，只能删帖）

node scripts/create-digital-human.js --name ... --desc ... --lng x --lat y --avatar ... --confirm
                                                   # 消耗 2 徽章，删除不退款
node scripts/delete-post.js <post-id>              # 拉取帖子摘要，exit 3
node scripts/delete-post.js <post-id> --confirm    # 真正删除（不可逆）

node scripts/upload-image.js <local-image-path>              # 只打印上传计划，exit 3
node scripts/upload-image.js <local-image-path> --confirm    # 真正上传并返回公开 URL
```

## 标准工作流（agent 视角）

1. `doctor` 自检；未登录则**请用户自己运行 login**（不要替用户收密码）。
2. `compose` 生成草稿和 `.preview.html`，把预览交给用户过目。
3. 用户明确同意后，对该写操作重新运行同一命令并附加 `--confirm`。
4. 结束或共享机器上，`logout` 清除会话。

## 退出码

| 码 | 含义 |
|---|---|
| 0 | 成功 / 自检全过 |
| 1 | 错误（参数、校验、平台拒绝等） |
| 2 | 未登录或会话过期 |
| 3 | dry-run 完成，等待用户确认后加 `--confirm` 重跑 |

## 文件说明

- `config.json` — 可改 `unsplashAccessKey`、`sessionMaxAgeDays`；`platformUrl` 不可偏离白名单。
- `~/.powpow/session.json` — JWT 会话（0600），服务侧约 7 天过期，本地 6 天强制重登。
- `<draft>.manifest.json` — compose 生成的本地图片清单，publish 时据此上传。
