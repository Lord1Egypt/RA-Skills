---
name: jike-bank-card-query
description: 银行卡类型及真伪查询。输入银行卡号，查询卡类型、卡名称、卡 BIN、发卡行、银行官网和客服电话，也支持查询银行列表。适用场景：用户说“查一下这个银行卡是什么银行”“这个卡号是信用卡还是借记卡”“查询工商银行列表”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"💳","requires":{"bins":["python3"],"env":["JIKE_BANK_CARD_QUERY_KEY"]},"primaryEnv":"JIKE_BANK_CARD_QUERY_KEY"}}
---

# 银行卡类型及真伪查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

支持：**银行卡类型及真伪查询、银行列表查询**。

## 前置配置

```bash
export JIKE_BANK_CARD_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

### 查询银行卡

```bash
python3 scripts/bank_card_query.py card --bank-card 6252490030651111
```

默认脱敏展示卡号，如需完整展示：

```bash
python3 scripts/bank_card_query.py card --bank-card 6252490030651111 --no-mask
```

### 查询银行列表

```bash
python3 scripts/bank_card_query.py list --bank-name 工商 --bank-type 大型国有银行
```

### JSON 输出

```bash
python3 scripts/bank_card_query.py card --bank-card 6252490030651111 --json
```

## AI 使用步骤

1. 用户问银行卡归属、卡类型、真伪时，使用 `card` 子命令。
2. 用户问支持哪些银行或银行信息时，使用 `list` 子命令。
3. 银行卡号默认脱敏输出，除非用户明确要求完整展示。
4. 返回卡类型、卡名称、卡 BIN、发卡行、客服电话等字段。

## 返回字段

| 字段 | 含义 |
| --- | --- |
| `bank_card` | 银行卡号 |
| `is_luhn` | 是否支持 Luhn 校验 |
| `card_type` | 银行卡类型 |
| `card_name` | 银行卡名称 |
| `card_bin` | 卡 BIN |
| `bank_name` | 银行名称 |
| `bank_abbr` | 银行英文简称 |
| `bank_weburl` | 银行官网 |
| `bank_tel` | 银行客服电话 |

## 脚本位置

`scripts/bank_card_query.py`
