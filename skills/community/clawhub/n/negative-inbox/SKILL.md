---
name: amazon-negative-review-inbox
description: >
  读取当前账户已有 Amazon 预警，以及指定 ASIN 的低星评论，按重复问题和严重程度整理处理清单。
  用于差评收件箱、新差评、低星评论待办和预警排查；读取免费。仅在用户明确要求时将全部预警标为已读；不联系买家、发送回复、采集或调用付费 AI。
  Requires ARI authorization (ari_live_*); use setup for browser authorization.
allowed-tools: Bash
slug: negative-inbox
displayName: Negative Review Inbox
version: 1.5.3
summary: 汇总已有差评预警与低星评论，整理处理清单并按要求标记已读
license: MIT
---
# Negative Review Inbox

汇总已有差评预警与低星评论，整理处理清单并按要求标记已读

## 使用流程

首次使用通过 setup 在浏览器授权；不在聊天中索要密码或回显 API Key。
先运行 check 验证账户。401 时停止并引导重新授权；429 时停止密集请求。

- 读取现有预警及用户指定 ASIN 的低星评论，按严重程度和重复问题整理待处理清单，0 积点。
- 引用短句说明依据，保留 ASIN、站点和时间窗口；不把样本问题当成整体退货率。
- 默认只读取。alerts --mark-read 会将当前账户全部预警标为已读，仅在用户明确要求全部标记时执行。
- 标为已读不等于问题已解决；本包不提供差评处理状态修改、联系买家或发送回复。
- 本包不采集评论、不创建周期监控、不调用付费 AI。

## 命令

```bash
python scripts/ari.py setup        # 首次使用：浏览器授权并保存 Key
python scripts/ari.py configure    # 隐藏输入并手动保存 ARI API Key
python scripts/ari.py check        # 验证 Key、账户和积点余额
python scripts/ari.py version      # 显示版本与分发渠道（无需 Key）
python scripts/ari.py alerts --limit 20
python scripts/ari.py reviews --asin B0XXXXXXXX --site amz_us --stars negative --sort recent
python scripts/ari.py alerts --mark-read
```

## 不适用

- 联系买家、发送消息或公开回复
- 把标记已读等同于差评问题已解决
- 采集评论、创建监控或生成付费 AI 报告

返回失败或部分失败时只使用成功返回的数据，不虚构缺失数据。

## 连接安全

API 与授权入口固定为 https://ari.funewa.com，禁止重定向。生产包不支持自定义端点，ARI_ALLOW_CUSTOM_BASE 不再生效。遇到 ARI_ENDPOINT_BLOCKED 或 ARI_REDIRECT_BLOCKED 时停止操作，清除自定义地址或联系 ARI 支持，不能绕过校验。
