---
name: juhe-exchange-rate
description: 全球汇率查询与货币换算。根据货币代码查询实时汇率、换算金额。使用场景：用户说"查一下汇率"、"美元兑人民币"、"100美元等于多少人民币"、"USD兑换CNY"、"汇率多少"等。通过聚合数据（juhe.cn）API 实时查询，支持 120+ 种货币，数据仅供参考。
homepage: https://www.juhe.cn/docs/api/id/80
metadata: {"openclaw":{"emoji":"💱","requires":{"bins":["python3"],"env":["JUHE_EXCHANGE_KEY"]},"primaryEnv":"JUHE_EXCHANGE_KEY"}}
---

# 全球汇率查询换算

> 数据由 **[聚合数据](https://www.juhe.cn)** 提供 — 根据货币代码查询汇率和换算，支持全球 120+ 个国家和地区货币。数据来源于网络，仅供参考，交易时以银行柜台成交价为准。

根据 [官方文档](https://www.juhe.cn/docs/api/id/80)，API 80 提供两个接口：**货币列表**、**实时汇率查询换算**。

---

## 前置配置：获取 API Key

1. 前往 [聚合数据官网](https://www.juhe.cn) 免费注册账号
2. 进入 [全球汇率查询换算 API](https://www.juhe.cn/docs/api/id/80) 页面，点击「申请使用」
3. 审核通过后在「我的API」中获取 AppKey
4. 配置 Key（**三选一**）：

```bash
# 方式一：环境变量（推荐）
export JUHE_EXCHANGE_KEY=你的AppKey

# 方式二：.env 文件
echo "JUHE_EXCHANGE_KEY=你的AppKey" > scripts/.env

# 方式三：命令行传入
python scripts/exchange_rate.py --key 你的AppKey --from USD --to CNY
```

> 计费说明：该接口为订阅付费，具体免费额度以聚合数据后台为准。

---

## 使用方法

### 查询两种货币的汇率并换算

```bash
# 查询 USD 兑 CNY 汇率
python scripts/exchange_rate.py --from USD --to CNY

# 换算 100 美元等于多少人民币
python scripts/exchange_rate.py --from USD --to CNY --amount 100
```

### 查询支持的货币列表

```bash
python scripts/exchange_rate.py --list
```

### 直接调用 API（无需脚本）

官方文档仅包含以下两个接口：

```
# 1. 货币列表
GET http://op.juhe.cn/onebox/exchange/list?key=YOUR_KEY

# 2. 实时汇率查询换算
GET http://op.juhe.cn/onebox/exchange/currency?key=YOUR_KEY&from=USD&to=CNY
```

---

## 输出示例

### 人民币对美元汇率

```bash
$ python scripts/exchange_rate.py --from CNY --to USD
```

```
💱 CNY → USD
   汇率: 1 CNY = 0.145055 USD
   更新: 2026-03-24 10:36:37

{
  "success": true,
  "data": {
    "currencyF": "CNY",
    "currencyF_Name": "人民币",
    "currencyT": "USD",
    "currencyT_Name": "美元",
    "currencyFD": "1",
    "exchange": "0.14505500",
    "result": "0.14505500",
    "updateTime": "2026-03-24 10:36:37"
  },
  "rate": 0.145055,
  "updateTime": "2026-03-24 10:36:37"
}
```

### 美元兑人民币并换算金额

```bash
$ python scripts/exchange_rate.py --from USD --to CNY --amount 100
```

```
💱 USD → CNY
   汇率: 1 USD = 6.894 CNY
   更新: 2026-03-24 10:36:37
   换算: 100.0 USD = 689.4 CNY

{
  "success": true,
  "data": {
    "currencyF": "USD",
    "currencyF_Name": "美元",
    "currencyT": "CNY",
    "currencyT_Name": "人民币",
    "currencyFD": "1",
    "exchange": "6.89400000",
    "result": "6.89400000",
    "updateTime": "2026-03-24 10:36:37"
  },
  "rate": 6.894,
  "updateTime": "2026-03-24 10:36:37"
}
```

---

## 常用货币代码

| 代码 | 货币 |
|------|------|
| CNY | 人民币 |
| USD | 美元 |
| EUR | 欧元 |
| JPY | 日元 |
| GBP | 英镑 |
| HKD | 港币 |
| AUD | 澳元 |
| CAD | 加元 |
| KRW | 韩元 |
| SGD | 新加坡元 |

---

## AI 使用指南

当用户询问汇率或货币换算时，按以下步骤操作：

1. **识别意图** — 查两种货币汇率、换算金额，或查货币列表
2. **提取货币代码** — 从用户消息提取（如「美元」→ USD，「人民币」→ CNY）
3. **提取金额** — 若有「100 美元」「5000 日元」等，提取数值
4. **调用脚本或 API** — 执行查询
5. **展示结果** — 清晰呈现汇率和换算结果

### 错误处理

| 情况 | 处理方式 |
|------|----------|
| 208001 | 货币兑换名称不能为空，需提供 from 和 to |
| 208002/208004/208006 | 查询不到汇率，检查货币代码是否正确 |
| 208005 | 不存在的货币种类 |
| 10001/10002 | API Key 无效，引导用户至 [聚合数据](https://www.juhe.cn/docs/api/id/80) 重新申请 |
| 10012 | 请求超过次数限制，建议升级套餐 |

---

## 脚本位置

`scripts/exchange_rate.py` — 封装货币列表、实时汇率换算和错误处理。

---

## 关于聚合数据

[聚合数据（juhe.cn）](https://www.juhe.cn) 是国内专业的 API 数据服务平台，提供：

- **金融数据**：汇率、油价、股票、黄金
- **生活服务**：天气、新闻、快递
- **身份核验**：手机归属地、身份证验证

注册即可使用，适合个人开发者和企业接入。
