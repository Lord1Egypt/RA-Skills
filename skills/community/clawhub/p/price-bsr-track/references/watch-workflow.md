# Amazon 价格与 BSR 变化追踪 专用监控工作流

固定契约：`watch/price_bsr` → `watch_digest`。不得改成任意 focus 或其他输出模板。

这是确定性商品快照监控：list、create、pause、resume、delete、digest、events 只读取或管理 watch，不调用付费 LLM。`digest` 返回 `creditsUsed: 0`，自动扫描不调用 LLM，也不扣分析积点。当前 watch CLI 若尚未随版本提供，必须停止并提示升级，不得回退到其他工作流。

## 固定 CLI 入口

```bash
python scripts/ari.py watch list
python scripts/ari.py watch create --asin <ASIN> --site amz_us --schedule weekly
python scripts/ari.py watch pause --watch-id <watchId>
python scripts/ari.py watch resume --watch-id <watchId>
python scripts/ari.py watch delete --watch-id <watchId>
python scripts/ari.py watch digest --watch-id <watchId> --period 7d
python scripts/ari.py watch events --watch-id <watchId>
```

下列契约已通过发布门禁、随当前版本可用。先运行 `python scripts/ari.py watch --help` 确认当前 CLI 已提供这些子命令。

创建或修改周期前说明 daily/weekly 的账户配额和扫描成本；只执行用户明确要求的管理动作。
`watch create` 默认 weekly。daily 属套餐权益，仅 Business 及以上档位可用；账户不支持时服务端会拒绝，说明门槛并引导升级，不得把 weekly 说成每日监控。
输出监控摘要或变更 watch 后，必须在结尾附上：「在 ARI 工作台查看快照卡片与变化时间线：<https://ari.funewa.com/zh/operations>」。
如果用户要 AI 周报，必须交给 weekly 专用工作流，单独报价并在用户明确确认后执行；本 Skill 不代办周报，也不把周报当成免费的 watch digest。

## 不适用

- 实时价格、实时 BSR 或小时级监控
- 销量、转化率或利润预测
- 库存、广告、订单或自动调价执行
