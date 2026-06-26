---
name: jike-bank-branch-query
description: 银行支行、联行号查询。根据银行名称、省市代码、支行关键词查询支行名称、联行号、省份和城市，也支持查询银行列表。适用场景：用户说“查工商银行西安长安区支行联行号”“查询某银行支行信息”“工商银行有哪些机构”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"🏦","requires":{"bins":["python3"],"env":["JIKE_BANK_BRANCH_QUERY_KEY"]},"primaryEnv":"JIKE_BANK_BRANCH_QUERY_KEY"}}
---

# 银行支行、联行号查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

支持：**支行联行号查询、银行列表查询**。

## 前置配置

```bash
export JIKE_BANK_BRANCH_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

### 查询支行联行号

```bash
python3 scripts/bank_branch_query.py branch --bank-name 中国工商银行 --province-code 610000 --city-code 610100 --branch-name 长安区
```

### 查询银行列表

```bash
python3 scripts/bank_branch_query.py list --bank-name 工商 --bank-type 大型国有银行
```

### JSON 输出

```bash
python3 scripts/bank_branch_query.py branch --bank-name 中国工商银行 --branch-name 长安区 --json
```

## AI 使用步骤

1. 用户问支行、联行号时，使用 `branch` 子命令。
2. 用户问银行机构列表时，使用 `list` 子命令。
3. 优先提取银行名称，再提取省市代码和支行关键词。
4. 返回支行名称、联行号、省份、城市等信息。

## 返回字段

| 字段 | 含义 |
| --- | --- |
| `bank_name` | 银行名称 |
| `branch_name` | 支行名称 |
| `branch_code` | 支行联行号 |
| `province_name` | 所在省 |
| `province_code` | 所在省代码 |
| `city_name` | 所在城市 |
| `city_code` | 所在城市代码 |

## 脚本位置

`scripts/bank_branch_query.py`
