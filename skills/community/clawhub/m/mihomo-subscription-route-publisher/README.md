# Mihomo Subscription Route Publisher

This skill converts a routing request such as “let `example.com` use `定向出口`” into a repo change, a worker redeploy, and a verified subscription update.
这个 skill 会把类似“让 `example.com` 走 `定向出口`”这样的请求，转成仓库变更、worker 重发和已验证的订阅更新。

## What This Skill Is For | 适用场景

Use it when:
适用于：

- a user names one or more sites, domains, or Mihomo rule lines
- the user expects a specific route target such as `直连`, `故障转移`, or `定向出口`
- the published subscription at `rules.xiannai.me` must update
- the repo should remain the source of truth

## Canonical Repository | 规范仓库

- `/home/grey/mihomo-fullstack-deploy`

## Distribution Layer | 分发层

- Worker custom domain: `https://rules.xiannai.me`

## What It Produces | 产出物

- updated canonical route rules
- regenerated worker assets
- redeployed worker
- refreshed published subscription objects
- verification proof against the live subscription endpoint

## Included Files | 包含文件

- `SKILL.md`
- `README.md`
- `WORKFLOW.md`
- `FAQ.md`
- `CHANGELOG.md`

## Important Decision Rules | 关键判断规则

- prefer stable group names over raw node names
- keep the repo canonical and the worker distributive
- validate live output before closing the task
- only restart local Mihomo when the runtime config itself changed

## Local Use | 本地使用

Place this folder under one of these locations:

- `<workspace>/skills/`
- `~/.openclaw/skills/`

Then refresh skills or start a new session.

## ClawHub Publish Shape | ClawHub 发布方式

```bash
clawhub publish /home/grey/work/agent-knowledge-stack/skills/shared/mihomo-subscription-route-publisher \
  --slug mihomo-subscription-route-publisher \
  --name "Mihomo Subscription Route Publisher" \
  --version 1.0.0 \
  --tags latest,mihomo,subscription,route,worker,cloudflare
```
