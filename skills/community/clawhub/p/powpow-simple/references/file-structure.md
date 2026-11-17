# File Structure

> 仅维护/排查时参考。SKILL.md 运行时不需要通读。

```
powpow-simple/
├── SKILL.md                          # 主文件：对话编排；所有网络/凭据操作调用 powpow-cli
├── README.md
└── references/
    ├── changelog.md                  # 历史变更
    ├── security.md                   # 安全架构 + 平台接口清单
    ├── screenshots.md                # 产品界面截图清单与外链
    └── file-structure.md             # 本文件
```

自 v1.0.5 起，本包**不再携带 scripts/ 与 config.json**。执行层独立为
powpow-cli（`clawhub install powpow-cli`），其文件结构：

```
powpow-cli/
├── SKILL.md / README.md / config.json（platformUrl 白名单锁定）
└── scripts/
    ├── doctor.js / login.js（TTY 隐藏输入，拒收 argv 密码）/ logout.js
    ├── compose.js / publish.js（--confirm 门）/ verify.js
    ├── delete-post.js（--confirm 门）/ create-digital-human.js（--confirm 门）
    ├── geocode.js / list-digital-humans.js / match-digital-human.js
    ├── search-image.js / upload-image.js
    └── lib/（api-client.js / dh-match.js / coord-transform.js / html-formatter.js）
```

注：登录会话（`session.json`，权限 0600）**不写入任何技能包**，位于用户状态目录
（`POWPOW_STATE_DIR`，默认 `~/.powpow/`），约 7 天过期（客户端留 6 天重登余量）。
