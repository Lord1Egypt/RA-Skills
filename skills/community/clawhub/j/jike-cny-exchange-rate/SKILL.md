---
name: jike-cny-exchange-rate
description: 人民币汇率查询。支持外汇牌价币种列表、人民币外汇牌价查询和汇率转换。适用场景：用户说“100美元等于多少人民币”“查一下美元兑人民币汇率”“支持哪些外汇币种”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"💱","requires":{"bins":["python3"],"env":["JIKE_CNY_EXCHANGE_RATE_KEY"]},"primaryEnv":"JIKE_CNY_EXCHANGE_RATE_KEY"}}
---

# 人民币汇率查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供。即刻数据专注稳定易用的数据 API、MCP 与 AI Skill 能力，帮助开发者和 AI 客户端快速接入可靠数据服务。

支持：**外汇币种列表、人民币外汇牌价查询、汇率转换**。

---

## 前置配置：获取 AppKey

```bash
export JIKE_CNY_EXCHANGE_RATE_KEY=你的AppKey
```

也可以使用通用 Key：

```bash
export JIKE_APPKEY=你的AppKey
```

---

## 使用方法

### 查询支持的币种列表

```bash
python3 scripts/cny_exchange_rate.py list
```

### 查询单个币种人民币牌价

```bash
python3 scripts/cny_exchange_rate.py query --currency usd
```

### 查询全部币种人民币牌价

```bash
python3 scripts/cny_exchange_rate.py query
```

### 汇率转换

```bash
python3 scripts/cny_exchange_rate.py convert --from-currency usd --to-currency cny --money 100
```

输出示例：

```text
💱 汇率转换结果

  日期: 2025-11-23
  金额: 712.6900
  说明: 100美元 = 712.6900人民币
```

### 直接调用 API

```text
GET https://api.jikeapi.cn/v1/cny_exchange_rate/currenc_list?appkey=YOUR_APPKEY
GET https://api.jikeapi.cn/v1/cny_exchange_rate/query?currency=usd&appkey=YOUR_APPKEY
GET https://api.jikeapi.cn/v1/cny_exchange_rate/convert?from_currency=usd&to_currency=cny&money=100&appkey=YOUR_APPKEY
```

---

## AI 使用步骤

当用户询问汇率、外汇牌价、金额换算时：

1. **判断意图**：问“支持哪些币种”用 `list`；问“某币种牌价”用 `query`；问“多少钱换算”用 `convert`。
2. **提取参数**：识别源币种、目标币种和金额。
3. **调用脚本**：执行对应子命令。
4. **展示结果**：说明汇率日期、转换金额和接口返回描述。

## 参数说明

| 子命令 | 参数 | 说明 | 示例 |
| --- | --- | --- | --- |
| `list` | 无 | 查询支持币种 | `list` |
| `query` | `--currency` | 币种代码，不传返回全部 | `usd` |
| `convert` | `--from-currency` | 源货币 | `usd` |
| `convert` | `--to-currency` | 目标货币 | `cny` |
| `convert` | `--money` | 金额 | `100` |

## 返回字段

| 字段 | 含义 |
| --- | --- |
| `currency` | 货币类型 |
| `currency_name` | 货币名称 |
| `spot_buying` | 现汇买入价 |
| `cash_buying` | 现钞买入价 |
| `spot_selling` | 现汇卖出价 |
| `cash_selling` | 现钞卖出价 |
| `money` | 转换后的金额 |
| `desc` | 转换说明 |

## 错误处理

| 情况 | 处理方式 |
| --- | --- |
| 未配置 AppKey | 提醒用户配置 `JIKE_CNY_EXCHANGE_RATE_KEY` 或 `JIKE_APPKEY` |
| 币种不存在 | 提醒用户先用 `list` 查询支持币种 |
| 金额非法 | 提醒用户提供大于 0 的数字 |
| 网络超时 | 建议稍后重试或检查网络 |

---

## 脚本位置

`scripts/cny_exchange_rate.py`：封装了 `currenc_list`、`query`、`convert` 三个接口的参数校验、请求和展示逻辑。
