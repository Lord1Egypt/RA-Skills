---
name: amazon-monitor-center
description: >
  汇总当前账户已保存的评论采集计划、价格、BSR、评分与 Listing 变化、新增差评和未读预警。
  用于 Amazon 监控中心、产品最近怎么样、每周变化汇总、监控暂停排查。只读取现有数据，0 积点；不创建监控、采集评论或运行付费 AI。
  Requires ARI authorization (ari_live_*); use setup for browser authorization.
allowed-tools: Bash
slug: monitor-center
displayName: Amazon Monitor · 监控中心
version: 1.5.3
summary: 汇总评论、商品变化、差评与暂停项，免费查看整个账户的监控状态
license: MIT
---
# Amazon Monitor · 监控中心

汇总评论、商品变化、差评与暂停项，免费查看整个账户的监控状态

## 使用流程

首次使用通过 setup 在浏览器授权；不在聊天中索要密码或回显 API Key。
先运行 check 验证账户。401 时停止并引导重新授权；429 时停止密集请求。

- 运行 monitor 查看账户级 KPI、最近 7 天变化动态及商品趋势数据。读取已有数据为 0 积点。
- 先说明新增评论、差评、未读预警与暂停项，再区分价格、BSR、评分和页面变化。
- 数据为空或部分数据不足时如实说明；不要把首次入库的旧评论当作刚发生的新评论。
- 网页入口：https://ari.funewa.com/zh/monitor。评论采集与商品快照监控是独立计划。
- 本包不创建或变更周期计划，不采集评论，不调用付费 AI；需要管理监控时由用户进入网页操作。

## 命令

```bash
python scripts/ari.py setup        # 首次使用：浏览器授权并保存 Key
python scripts/ari.py configure    # 隐藏输入并手动保存 ARI API Key
python scripts/ari.py check        # 验证 Key、账户和积点余额
python scripts/ari.py version      # 显示版本与分发渠道（无需 Key）
python scripts/ari.py monitor
```

## 不适用

- 开启、修改或恢复周期采集与商品监控
- 实时或小时级价格、销量及库存数据
- 付费分析报告或 AI 运营周报

返回失败或部分失败时只使用成功返回的数据，不虚构缺失数据。

## 连接安全

API 与授权入口固定为 https://ari.funewa.com，禁止重定向。生产包不支持自定义端点，ARI_ALLOW_CUSTOM_BASE 不再生效。遇到 ARI_ENDPOINT_BLOCKED 或 ARI_REDIRECT_BLOCKED 时停止操作，清除自定义地址或联系 ARI 支持，不能绕过校验。
