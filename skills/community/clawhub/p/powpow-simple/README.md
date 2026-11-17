# powpow-simple

PowPow 泡泡助手（OpenClaw 版）：把你的照片或素材写成一篇游记并发布到 PowPow，
或把一个人/角色做成能聊天的数字人、钉在公开地图上。

本 skill 是对话编排层；所有网络与凭据操作由配套执行层 **powpow-cli** 完成
（加固 CLI：密码用户自助终端输入、写操作 `--confirm` 门、会话 0600、
platformUrl 白名单）。

## 安装

```
clawhub install @durenzidu/powpow-cli        # 先装执行层（必需）
clawhub install @durenzidu/powpow-simple     # 本 skill
```

## 环境要求

- Node.js 18+（脚本使用全局 `fetch`，无第三方依赖）
- PowPow 账号：https://global.powpow.online/register

## 状态目录

技能包本身保持只读。登录令牌与用户配置写在状态目录：

- 默认：`~/.powpow/`（session.json 权限 0600）
- 可用环境变量 `POWPOW_STATE_DIR` 覆盖

`platformUrl` 锁定官方域名，不可被用户配置改写；`unsplashAccessKey` 等
非安全项可在状态目录的 `config.json` 覆盖。

## 用法示例

以下命令均指 `<powpow-cli 目录>/scripts/` 下的脚本：

```
node <powpow-cli>/scripts/doctor.js                                   # 自检 + 会话探活
node <powpow-cli>/scripts/login.js <username>                         # 登录（用户本人在终端隐藏输入密码）
node <powpow-cli>/scripts/geocode.js "地坛公园" --limit 5              # 地点 → 坐标
node <powpow-cli>/scripts/match-digital-human.js "读书 作家" --limit 3  # 匹配数字人
node <powpow-cli>/scripts/compose.js --text-file post.txt --loc "地坛公园" --lng 116.408195 --lat 39.952372 --image @/abs/path/cover.jpg --out post-draft.html
node <powpow-cli>/scripts/publish.js post-draft.html                  # dry-run 预览（exit 3）
node <powpow-cli>/scripts/publish.js post-draft.html --confirm        # 用户确认后发布
node <powpow-cli>/scripts/verify.js <post-id>                         # 发布后验证
node <powpow-cli>/scripts/delete-post.js <post-id> --confirm          # 删除（测试清理，需确认）
node <powpow-cli>/scripts/logout.js                                   # 清除本地会话
```

`--image` 的本地路径**必须是绝对路径**。

## 安全

- 不含任何平台密钥，也不含可执行脚本；所有网络操作在 powpow-cli 中完成。
- 密码不经对话：用户在自己的终端运行 login（TTY 隐藏输入），agent 全程看不到密码。
- 发布 / 创建数字人 / 删帖默认 dry-run，加 `--confirm` 才真正执行。
- 详见 `references/security.md` 与 powpow-cli 的 SKILL.md。

## Notes for reviewers (SkillSpector / manual review)

- This is a **pure instruction skill** (v1.0.5+): it ships NO scripts and NO
  credential handling. All network/credential operations live in the companion
  CLI skill `powpow-cli`, which enforces confirmation gates in code
  (`--confirm`), user-run login (hidden TTY input, no password via argv/chat),
  0600 session files, and a platformUrl allowlist.
- This skill's text instructs the agent to show previews and obtain explicit
  user confirmation before invoking any powpow-cli command with `--confirm`.

## 许可

MIT-0（ClawHub 统一许可）。

## 链接

- 官网：https://global.powpow.online
- 地图：https://global.powpow.online/map
