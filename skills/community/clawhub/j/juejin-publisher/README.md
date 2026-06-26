# juejin-publisher

⛏️ 掘金文章自动发布技能

通过掘金官方 API（Cookie 鉴权），将 Markdown 文章一键发布到稀土掘金平台。

## 快速开始

1. 配置 Cookie：`cp juejin.env.example juejin.env` 并填入掘金 Cookie
2. 发布文章：`python3 scripts/publish.py your-article.md`

详细说明见 [SKILL.md](./SKILL.md)
