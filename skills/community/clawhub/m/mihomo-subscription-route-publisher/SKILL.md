---
name: mihomo-subscription-route-publisher
description: Update Mihomo site routing rules from natural-language requests, rebuild the published subscription, and verify the live output. 根据自然语言路由请求更新 Mihomo 规则、重建已发布订阅并验证线上结果。
license: CC-BY-4.0
compatibility: OpenClaw, Codex, Claude Code, and ClawHub-style markdown skill runners with bash, git, node, wrangler, network access, and 1Password CLI available.
---

# Mihomo Subscription Route Publisher

Use this skill when the user says a site, domain, or Mihomo rule should use a specific route target and expects the published subscription to update.
当用户说某个网站、域名或 Mihomo 规则应该走某个目标出口，并希望已发布订阅同步更新时，使用这个 skill。

## Read First | 先读这些

- `{baseDir}/README.md`
- `{baseDir}/WORKFLOW.md`
- `{baseDir}/FAQ.md`
- `{baseDir}/CHANGELOG.md`

## Primary Rule | 核心原则

Treat `/home/grey/mihomo-fullstack-deploy` as the canonical source, `rules.xiannai.me` as the distribution layer, and live validation as mandatory before declaring success.
把 `/home/grey/mihomo-fullstack-deploy` 当作规范源，把 `rules.xiannai.me` 当作分发层，并把线上验证当作必选步骤。

## Workflow | 执行流程

1. normalize the user request into explicit Mihomo rule lines
   把自然语言请求归一化成明确的 Mihomo 规则行
2. map the requested node to a stable group when possible
   尽量把节点名映射到稳定代理组
3. edit the canonical source file for that target
   修改该目标对应的规范源文件
4. regenerate worker artifacts
   重生成 worker 构建产物
5. validate syntax and config
   校验语法和配置
6. deploy worker and trigger `/sync`
   发布 worker 并触发 `/sync`
7. verify the live published artifact with `?ts=`
   用 `?ts=` 校验线上已发布产物
8. update the local Linux runtime config only if needed
   仅在需要时同步本机 Linux 运行时配置
9. commit and push if the repo should remain canonical upstream
   如果仓库要保持上游规范源，就提交并推送

## Stable Route Map | 稳定路由映射

- `直连`
  Canonical source:
  `/home/grey/mihomo-fullstack-deploy/worker/src/inline-rules.js`
- `故障转移`
  Canonical source:
  `/home/grey/mihomo-fullstack-deploy/rules/user_ruleset/user_proxy_rules.txt`
- `定向出口`
  Canonical source:
  - `/home/grey/mihomo-fullstack-deploy/etc/mihomo/config.yaml`
  - `/home/grey/mihomo-fullstack-deploy/etc/mihomo/config.windows.yaml`

Node-name aliases:

- `onlygays1` -> `故障转移`
- `racknerd-reality` -> `定向出口`
- `DIRECT` -> `直连`

## Strong Heuristics | 强判断规则

- if the user names a raw node, prefer the stable group backed by that node
- if the route should affect all clients, do not stop after only changing Linux
- if only `故障转移` rules changed, do not restart local Mihomo unnecessarily
- if `定向出口` rules changed, validate the Linux config and published Linux/Windows configs
- if the repo is dirty in unrelated files, touch only the routing files required for the task
- always verify remote output with cache busting

中文解释：

- 用户说的是裸节点名时，优先落到对应的稳定代理组。
- 如果目标是所有客户端生效，不要只改 Linux 就结束。
- 只改 `故障转移` 规则时，不要无意义重启本机 Mihomo。
- 改了 `定向出口` 时，要同时校验 Linux 配置和已发布的 Linux/Windows 配置。
- 仓库里有不相关脏文件时，只碰本次路由任务需要的文件。
- 远端验证必须带缓存穿透参数。

## Safe Commands | 安全命令

```bash
sed -n '1,120p' /home/grey/mihomo-fullstack-deploy/rules/user_ruleset/user_proxy_rules.txt
sed -n '1,80p' /home/grey/mihomo-fullstack-deploy/worker/src/inline-rules.js
cd /home/grey/mihomo-fullstack-deploy/worker && node --check src/index.js
HOME=/etc/mihomo XDG_CONFIG_HOME=/etc/mihomo/.config /usr/local/bin/mihomo -t -f /home/grey/mihomo-fullstack-deploy/etc/mihomo/config.yaml
curl -fsSL "https://rules.xiannai.me/sync?ts=$(date +%s)"
curl -fsSL "https://rules.xiannai.me/configs/linux.yaml?ts=$(date +%s)"
```

## Response Format | 输出格式

Always return:
始终返回：

1. normalized routing request
2. files changed
3. publish status
4. live verification result
5. next action if anything is still pending

## Constraints | 约束

- do not reveal Cloudflare or GitHub token values
- do not treat `rules.xiannai.me` as canonical; the repo stays canonical
- do not silently leave live and repo state diverged
- do not promise cross-client parity for `定向出口` unless the relevant configs were updated in the same change
