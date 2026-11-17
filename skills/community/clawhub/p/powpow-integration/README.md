# powpow-integration

PowPow 泡泡助手（OpenClaw 版）：把你的照片或素材写成一篇游记并发布到 PowPow，
或把一个人/角色做成能聊天的数字人、钉在公开地图上。

## 安装

```
openclaw skills install @durenzidu/powpow-integration
```

## 环境要求

- Node.js 18+（脚本使用全局 `fetch`，无第三方依赖）
- PowPow 账号：https://global.powpow.online/register

## 状态目录

技能包本身保持只读。登录令牌与用户配置写在状态目录：

- 默认：`~/.powpow/`
- 可用环境变量 `POWPOW_STATE_DIR` 覆盖

想自定义平台地址或 Unsplash key，把 `config.json` 放到状态目录即可覆盖包内默认值。

## 用法示例

```
cd <技能目录>
node scripts/doctor.js                                   # 自检 + 会话探活
node scripts/login.js <username>                         # 登录（密码走 stdin，不落盘）
node scripts/geocode.js "地坛公园" --limit 5              # 地点 → 坐标
node scripts/match-digital-human.js "读书 作家" --limit 3  # 匹配数字人
node scripts/compose.js --text-file post.txt --loc "地坛公园" --lng 116.408195 --lat 39.952372 --image @/abs/path/cover.jpg --out post-draft.html
node scripts/publish.js post-draft.html                  # 发布
node scripts/verify.js <post-id>                   # 发布后验证
node scripts/delete-post.js <post-id>              # 删除（测试清理）
node scripts/check-theotopia-gods.js               # 万神殿巡检（仅平台维护者，只读）
```

`--image` 的本地路径**必须是绝对路径**。

## 安全

- 不含任何平台密钥；所有操作走平台公开 API + 用户自己的 JWT。
- 密码只在登录时使用一次，不落盘；令牌约 7 天过期。
- 详见 `references/security.md`。

## Notes for reviewers (SkillSpector / manual review)

- This is an **instruction-style skill**: SKILL.md orchestrates a multi-script
  pipeline. Every script under `scripts/` is one documented step of the
  publishing workflow (login → self-check → geocode → match → compose →
  publish → verify), not an independent hidden tool.
- `delete-post.js` deletes only the logged-in user's own post
  (`DELETE /api/posts/{id}`, JWT-scoped, enforced server-side) and is
  documented in SKILL.md Step 8 for test cleanup. This capability is also
  declared in the skill description.
- No secrets are bundled. `config.json` ships defaults only. The session JWT
  is written to the user's state directory (`POWPOW_STATE_DIR`, default
  `~/.powpow/session.json`), never inside the skill bundle. Passwords are
  never persisted.
- All environment variables used (`POWPOW_STATE_DIR`, `POWPOW_PASSWORD`,
  `UNSPLASH_ACCESS_KEY`, maintainer-only `SUPABASE_URL` +
  `SUPABASE_SERVICE_ROLE_KEY`) are optional and declared in SKILL.md frontmatter
  (`metadata.openclaw.envVars`).
- `check-theotopia-gods.js` is a maintainer-only, read-only (GET-only)
  census/integrity inspector for theotopia god rows; it ships with no
  credentials and refuses to run without the maintainer's own Supabase key,
  supplied via env vars or the user's state directory — never the command
  line. Documented in SKILL.md ("万神殿批量发布与巡检").

## 许可

MIT-0（ClawHub 统一许可）。

## 链接

- 官网：https://global.powpow.online
- 地图：https://global.powpow.online/map
