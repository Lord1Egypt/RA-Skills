# Amazon 价格与 BSR 变化追踪

从商品快照摘要展示价格与 BSR 字段变化

固定工作流：`watch/price_bsr`，输出 `watch_digest`；确定性 digest 为 0 积点，自动扫描不调用 LLM。

本包已随当前版本可用。先运行 `python scripts/ari.py watch --help`；当前 CLI 未提供 watch 子命令时必须停止并提示升级。
在 ARI 工作台查看快照卡片与变化时间线：<https://ari.funewa.com/zh/operations>

`watch create` 默认 weekly；daily 属套餐权益，仅 Business 及以上档位可用。

## 使用

```bash
python scripts/ari.py watch list
python scripts/ari.py watch create --asin <ASIN> --site amz_us --schedule weekly
python scripts/ari.py watch pause --watch-id <watchId>
python scripts/ari.py watch resume --watch-id <watchId>
python scripts/ari.py watch delete --watch-id <watchId>
python scripts/ari.py watch digest --watch-id <watchId> --period 7d
python scripts/ari.py watch events --watch-id <watchId>
```

watch 只提供快照变化和确定性摘要，不承诺实时价格、销量、库存或广告数据。
AI 周报须使用 weekly 专用工作流，单独报价并在用户明确确认后执行；本 Skill 不代办。

## 不适用

- 实时价格、实时 BSR 或小时级监控
- 销量、转化率或利润预测
- 库存、广告、订单或自动调价执行
