---
name: oil-price
description: "获取全国各省市油价信息。无需 API Key。Use when: user asks about gas prices, fuel costs in China."
homepage: https://v2.xxapi.cn
metadata: { "openclaw": { "emoji": "⛽", "requires": { "bins": ["curl", "jq"] } } }
---

# 油价查询技能

获取全国各省市最新油价信息。**无需 API Key**

## 使用方法

### 直接调用

```bash
./oil_price.sh
```

### 输出格式

每行一个地区，格式为：`地区 |92 号 |95 号 |98 号 |0 号`

```
北京|8.5|9.1|10.2|7.8
上海|8.6|9.2|10.3|7.9
...
```

### 在脚本中使用

```bash
OIL_DATA=$(./oil_price.sh)

# 获取北京油价
BEIJING=$(echo "$OIL_DATA" | grep "北京")

# 提取 92 号油价
P92=$(echo "$BEIJING" | cut -d'|' -f2)
```

## API 说明

- **接口**: https://v2.xxapi.cn/api/oilPrice
- **认证**: 无需 API Key
- **返回**: JSON 格式，包含 data 数组
- **字段**: 
  - `name`: 地区名称
  - `p92`: 92 号汽油价格
  - `p95`: 95 号汽油价格
  - `p98`: 98 号汽油价格
  - `p0`: 0 号柴油价格

## 注意事项

- 有 API 调用频率限制
- 建议每日调用一次即可
- 需要安装 `curl` 和 `jq`
