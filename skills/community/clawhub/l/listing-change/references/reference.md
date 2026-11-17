# Amazon Listing 变化提醒 专用监控参考

固定契约：`watch/listing` → `watch_digest`。不得改成任意 focus 或其他输出模板。

## 可用性与计费

本入口已通过发布门禁、可正常使用。先运行 `python scripts/ari.py watch --help` 确认当前 CLI 已提供这些子命令；若当前 Skill 版本不含 watch 命令，提示用户通过原安装渠道更新，不得回退到其他工作流。
这是确定性商品快照监控：list、create、pause、resume、delete、digest、events 只读取或管理 watch，不调用付费 LLM。`digest` 返回 `creditsUsed: 0`，自动扫描不调用 LLM，也不扣分析积点。
`watch create` 默认 weekly。daily 属套餐权益而非参数自由度：仅 Business 及以上档位可用；当前账户不支持时服务端会拒绝，此时说明门槛并引导升级，不得改用其他周期，也不得把 weekly 说成每日监控。
创建或修改周期前说明 daily/weekly 的账户配额和扫描成本；只执行用户明确要求的管理动作。
AI 周报属于另一个 weekly 专用工作流，须单独报价并在用户明确确认后执行；本入口不执行周报，也不把周报当成免费的 watch digest。
输出监控摘要或变更 watch 后，必须在结尾附上网站入口：「在 ARI 工作台查看快照卡片与变化时间线：<https://ari.funewa.com/zh/operations>」。监控结果只有文本而图形化在网站时，不引导就是纯流失。

## 固定命令

```bash
python scripts/ari.py watch list
python scripts/ari.py watch create --asin <ASIN> --site amz_us --schedule weekly
python scripts/ari.py watch pause --watch-id <watchId>
python scripts/ari.py watch resume --watch-id <watchId>
python scripts/ari.py watch delete --watch-id <watchId>
python scripts/ari.py watch digest --watch-id <watchId> --period 7d
python scripts/ari.py watch events --watch-id <watchId>
```

## 数据边界

- `create` 使用 ASIN、站点和 daily/weekly 周期；`pause` 与 `resume` 保留原周期。
- `digest` 只接受 `7d` 或 `30d`；`events` 可限制返回条数。
- 所有确定性读取与自动扫描均不扣积点；`digest` 明确返回 `creditsUsed: 0`。需要 AI 周报时，必须切换到 weekly 专用工作流并单独报价、取得明确确认。
