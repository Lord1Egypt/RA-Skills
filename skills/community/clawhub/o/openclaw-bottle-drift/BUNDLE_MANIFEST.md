# Bundle Manifest

## Bundle Name
openclaw-bottle-drift-skill

## Included Skill
- bottle-drift

## File List
- SKILL.md
- README.md
- SELF_CHECK.md
- BUNDLE_MANIFEST.md
- scripts/bottle_drift.py
- scripts/relay_server.py
- resources/dashboard.html
- resources/dashboard.js
- resources/reply_page.html
- resources/message_schema.json
- examples/demo-session.md
- examples/sample-bottle.json
- tests/smoke-test.md

## Packaging Notes
- 保持 `resources/` 与 `scripts/` 的相对路径不变
- 建议以当前目录为根直接压缩，不要再套额外一层随机目录
- 若接入真实公网，请为 relay 配置 HTTPS / 反向代理 / 速率限制
- 若在 ClawHub 发布，请确认 frontmatter 字段与当前 loader 版本一致

## Final Bundle Manifest
```json
{
  "bundle": "openclaw-bottle-drift-skill",
  "skill": "bottle-drift",
  "entrypoints": [
    "scripts/relay_server.py",
    "scripts/bottle_drift.py"
  ],
  "web": {
    "dashboard": "/",
    "reply_page": "/r/{reply_token}"
  }
}
```
