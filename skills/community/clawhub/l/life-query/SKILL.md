---
name: life-query
description: 日常生活信息查询助手。快递物流跟踪（顺丰/圆通/中通/韵达/京东）、实时和历史汇率换算（30 种货币）、 全国各省油价查询（92/95/柴油）、全球城市天气预报（当前+多日+逐小时）。 当用户提到"查快递"、"快递单号"、"物流"、"汇率"、"换算"、"美元人民币"、"油价"、"加油"、 "92号多少钱"、"天气"、"气温"、"会下雨吗"、"穿什么衣服"、"天气预报"时使用。 不适用于：股票行情、航班查询、地图导航、新闻资讯、空气质量 AQI。
clawhub-slug: life-query
clawhub-owner: eamanc-lab
homepage: https://github.com/eamanc-lab/life-query
allowed-tools: Bash({baseDir}/scripts/run.sh:*),Read({baseDir}/**)
---

# Life Query — 日常生活查询助手

快递物流跟踪、实时汇率换算、全国油价查询、全球天气预报。四合一日常信息查询。

## 前置条件

- **必需**：`curl`、`python3`（系统自带即可）
- **可选**：自有快递100凭证（不配也能用免费额度；配置后直连快递100，不经过第三方）

## 路由决策

根据用户意图选择接口，所有接口通过 `bash {baseDir}/scripts/run.sh call <接口名>` 调用：

| 用户意图 | 接口 | 关键参数 | 备注 |
|----------|------|---------|------|
| 发了快递单号、问物流在哪 | `courier-track` | `--trackingNumber <单号>` | 可选 `--carrierCode` 指定快递公司 |
| 没给单号 | — | — | 追问用户要单号 |
| "100美元换多少人民币"、问汇率 | `exchange-rate` | `--from USD --to CNY --amount 100` | 默认 USD→CNY |
| "最近一周日元走势" | `exchange-rate` | `--from JPY --to CNY --startDate --endDate` | 时间序列 |
| "今天油价多少"、"加油" | `oil-price` | 默认全国 | 可选 `--city 北京` 指定省份 |
| "北京最近几次油价调整" | `oil-price` | `--city 北京 --pageSize 5` | 历史记录 |
| "北京天气怎么样" | `weather` | `--city 北京` | 没提城市则追问 |
| "明天会下雨吗"、"这周气温" | `weather` | `--city <城市> --days 3` | 多日预报 |
| "逐小时天气" | `weather` | `--city <城市> --detail` | 含 hourly 数据 |
| 同时问多个 | 分别调用 | — | 单个接口失败不影响其他 |

所有接口支持 `--format table`（人类可读）或 `--format json`（默认）。

## 调用示例

```bash
# 快递查询（自动识别快递公司）
bash {baseDir}/scripts/run.sh call courier-track --trackingNumber SF1234567890

# 汇率换算
bash {baseDir}/scripts/run.sh call exchange-rate --from CNY --to USD,EUR,JPY --amount 100

# 历史汇率走势
bash {baseDir}/scripts/run.sh call exchange-rate --from USD --to CNY --startDate 2026-03-01 --endDate 2026-03-10

# 全国油价（表格）
bash {baseDir}/scripts/run.sh call oil-price --format table

# 指定省份油价
bash {baseDir}/scripts/run.sh call oil-price --city 北京

# 天气预报（3天）
bash {baseDir}/scripts/run.sh call weather --city Shanghai --days 3 --format table

# 列出所有接口
bash {baseDir}/scripts/run.sh list
```

常用货币代码：CNY（人民币）、USD（美元）、EUR（欧元）、JPY（日元）、GBP（英镑）、HKD（港币）、KRW（韩元）。

## 错误处理

| 现象 | 处理 |
|------|------|
| `missing_parameter` | 提示用户提供缺少的参数（单号/城市/币种） |
| curl 超时或返回非 0 | 告知用户"XX 服务暂时不可用"，建议稍后重试 |
| 单号查询返回空 data | 提示用户核实单号，建议检查位数和字母 |
| 快递公司识别失败（carrierName 为空） | 追问用户快递公司，用 `--carrierCode` 指定 |
| 不支持的货币代码（返回 404） | 提示检查货币代码，给出常用代码列表 |
| 城市名无法识别 | 建议换英文城市名或检查拼写 |
| python3 未安装 | 提示用户安装 python3 |

## 外部服务声明

| 接口 | 端点 | 发送的数据 | 凭证 |
|------|------|-----------|------|
| courier-track（免费） | `api.fenxianglife.com` | 仅快递单号 | 无 |
| courier-track（自有凭证） | `poll.kuaidi100.com` | 快递单号 + 签名 | 环境变量直连，不经过第三方 |
| exchange-rate | `api.frankfurter.app` | 货币代码、金额 | 无 |
| oil-price | `datacenter-web.eastmoney.com` | 省份名 | 无 |
| weather | `wttr.in` | 城市名 | 无 |

配置自有快递100凭证后自动切换直连通道：
```bash
export KUAIDI100_KEY=你的授权Key
export KUAIDI100_CUSTOMER=你的Customer编码
```

## 更新

```bash
npx clawhub@latest update life-query
```
