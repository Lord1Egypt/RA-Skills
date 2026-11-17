---
name: amazon-review-keyword-radar
description: >
  读取 Amazon 已采集评论的关键词、星级与趋势统计，整理买家常用词、痛点词、场景词和文案测试线索。
  用于评论词频、review keyword radar、买家用语和评论词云；读取免费。不提供真实搜索量、CPC、关键词排名，不生成付费报告或操作广告账户。
  Requires ARI authorization (ari_live_*); use setup for browser authorization.
allowed-tools: Bash
slug: keyword-radar
displayName: Review Keyword Radar
version: 1.5.3
summary: 读取评论关键词与相关统计，提炼买家用语、痛点词和场景词
license: MIT
---
# Review Keyword Radar

读取评论关键词与相关统计，提炼买家用语、痛点词和场景词

## 使用流程

首次使用通过 setup 在浏览器授权；不在聊天中索要密码或回显 API Key。
先运行 check 验证账户。401 时停止并引导重新授权；429 时停止密集请求。

- 从用户需求提取 ASIN、站点和时间窗口；读取已采集评论的关键词、星级与趋势图表，0 积点。
- 按返回的实际词频整理买家常用词、痛点词和场景词，再提出文案测试建议；推理建议与原始数字分开。
- --days 0 是全部历史，其余值只表示该窗口；频次不是真实搜索量、关键词排名、CPC 或转化率。
- 样本不足时说明缺口。不要抓取或隐式采集，也不要生成付费 AI 报告。
- 本包提供评论关键词及相关统计图表，不操作广告账户或修改商品页面。

## 命令

```bash
python scripts/ari.py setup        # 首次使用：浏览器授权并保存 Key
python scripts/ari.py configure    # 隐藏输入并手动保存 ARI API Key
python scripts/ari.py check        # 验证 Key、账户和积点余额
python scripts/ari.py version      # 显示版本与分发渠道（无需 Key）
python scripts/ari.py charts --asin B0XXXXXXXX --site amz_us --days 30
```

## 不适用

- 真实搜索量、CPC、关键词排名或广告效果
- 自动采集或生成付费关键词报告
- 投放广告、修改预算或商品页面

返回失败或部分失败时只使用成功返回的数据，不虚构缺失数据。

## 连接安全

API 与授权入口固定为 https://ari.funewa.com，禁止重定向。生产包不支持自定义端点，ARI_ALLOW_CUSTOM_BASE 不再生效。遇到 ARI_ENDPOINT_BLOCKED 或 ARI_REDIRECT_BLOCKED 时停止操作，清除自定义地址或联系 ARI 支持，不能绕过校验。
