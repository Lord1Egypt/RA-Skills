# FAQ

## Can I say a node name instead of a group name? | 我可以直接说节点名吗？

Yes, but the skill should usually map it to a stable group.

- `onlygays1` -> `故障转移`
- `racknerd-reality` -> `定向出口`

可以，但通常应先映射到稳定代理组。

## Does this skill edit the live server too? | 这个 skill 会改本机正在运行的配置吗？

Only when needed.

- Rule-file-only changes do not require changing `/etc/mihomo/config.yaml`
- Config-level `定向出口` changes may require syncing `/etc/mihomo/config.yaml` and restarting `mihomo`

只有在需要时才会。

## Which file handles `故障转移` routes? | `故障转移` 规则改哪个文件？

- `/home/grey/mihomo-fullstack-deploy/rules/user_ruleset/user_proxy_rules.txt`

## Which file handles `直连` routes? | `直连` 规则改哪个文件？

- `/home/grey/mihomo-fullstack-deploy/worker/src/inline-rules.js`

## Which file handles `定向出口` routes? | `定向出口` 规则改哪个文件？

- `/home/grey/mihomo-fullstack-deploy/etc/mihomo/config.yaml`
- `/home/grey/mihomo-fullstack-deploy/etc/mihomo/config.windows.yaml`

## Why not stop after editing the repo? | 为什么不能只改仓库不发布？

Because the user asked for client-visible subscription updates. Repo-only changes are not enough.

因为目标是让客户端订阅更新，只改仓库还不够。
