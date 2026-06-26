---
name: jike-pork-query
description: 国内猪肉价格实时查询。按省份查询白条肉、精瘦肉、土杂猪、外三元、内三元价格，也支持不传省份返回全部地区价格。适用场景：用户说“四川今天猪肉价格多少”“查一下广东精瘦肉价格”“全国猪肉价格列表”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"🐖","requires":{"bins":["python3"],"env":["JIKE_PORK_QUERY_KEY"]},"primaryEnv":"JIKE_PORK_QUERY_KEY"}}
---

# 国内猪肉价格实时查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

支持查询：**白条肉、精瘦肉、土杂猪、外三元、内三元价格**。

## 前置配置

```bash
export JIKE_PORK_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

### 查询指定省份

```bash
python3 scripts/pork_query.py --province 四川
```

### 查询全部地区

```bash
python3 scripts/pork_query.py
```

### JSON 输出

```bash
python3 scripts/pork_query.py --province 四川 --json
```

直接调用 API：

```text
GET https://api.jikeapi.cn/v1/pork/query?province=四川&appkey=YOUR_APPKEY
```

## AI 使用步骤

1. 从用户消息中提取省份名称。
2. 如果用户问全国猪肉价格，不传 `--province`。
3. 执行 `python3 scripts/pork_query.py [--province <省份>]`。
4. 返回白条肉、精瘦肉、土杂猪、外三元、内三元价格。

## 返回字段

| 字段 | 含义 |
| --- | --- |
| `date` | 日期 |
| `time` | 更新时间 |
| `province` | 省份 |
| `carcass_pork` | 白条肉价格 |
| `lean_pork` | 精瘦肉价格 |
| `hyb_native` | 土杂猪价格 |
| `hyb_3way` | 外三元价格 |
| `hyb_3line` | 内三元价格 |

## 脚本位置

`scripts/pork_query.py`
