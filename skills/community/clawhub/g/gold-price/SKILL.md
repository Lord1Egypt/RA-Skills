---
name: gold-price
description: "查询当前黄金大盘价格。用于回答关于黄金价格、金价走势、贵金属行情的问题。包括国内金价（银行金条、回收价、首饰品牌价）和国际金价。不需要 API key。"
metadata: { "openclaw": { "emoji": "🥇", "requires": { "bins": ["curl"] } } }
---

# Gold Price Skill

查询黄金、白银、铂金、钯金等贵金属的实时价格。

## 何时使用

✅ **使用场景：**

- "今天金价多少？"
- "黄金价格查询"
- "现在金条多少钱？"
- "金价涨了吗？"
- "足金价格"

❌ **不使用：**

- 历史金价数据分析 → 使用专业金融数据库
- 黄金投资建议 → 不提供投资建议

## 数据来源

- **银行投资金条**：浦发银行、工商银行、中国银行、建设银行、农业银行等
- **黄金回收价**：24K/18K/14K 金饰回收
- **首饰品牌金价**：周大福、周生生、老凤祥、老庙黄金、菜百等
- **国际金价**：美元/盎司（需额外 API）

## 命令

### 查询所有金价

```bash
curl -s "https://v2.xxapi.cn/api/goldprice"
```

### 解析输出

```bash
# 获取银行金条价格
curl -s "https://v2.xxapi.cn/api/goldprice" | jq '.data.bank_gold_bar_price'

# 获取首饰金价
curl -s "https://v2.xxapi.cn/api/goldprice" | jq '.data.precious_metal_price'

# 获取回收金价
curl -s "https://v2.xxapi.cn/api/goldprice" | jq '.data.gold_recycle_price'
```

## 响应格式

```json
{
  "code": 200,
  "data": {
    "bank_gold_bar_price": [
      { "bank": "浦发银行投资金条", "price": "1136.0" },
      { "bank": "工商银行如意金条", "price": "1131.83" }
    ],
    "gold_recycle_price": [
      { "gold_type": "24K金回收", "recycle_price": "1101.0", "updated_date": "2026-03-17" }
    ],
    "precious_metal_price": [
      { "brand": "周大福", "gold_price": "1551", "platinum_price": "832" }
    ]
  }
}
```

## 常用查询示例

### 简洁输出（用户友好）

```bash
curl -s "https://v2.xxapi.cn/api/goldprice" | jq -r '
"🌟 今日金价\n" +
"━━━━━━━━━━━━\n" +
"📈 首饰金价（部分品牌）：\n" +
(.data.precious_metal_price[:5][] | "\(.brand): \(.gold_price)元/克") +
"\n📍 更新日期：\(.data.precious_metal_price[0].updated_date)"
'
```

### 获取最低/最高品牌金价

```bash
curl -s "https://v2.xxapi.cn/api/goldprice" | jq -r '
"最低：\(.data.precious_metal_price | min_by(.gold_price | tonumber) | "\(.brand) \(.gold_price)元/克")\n" +
"最高：\(.data.precious_metal_price | max_by(.gold_price | tonumber) | "\(.brand) \(.gold_price)元/克")"
'
```

## 单位说明

- **银行金条**：元/克
- **首饰金价**：元/克
- **回收金价**：元/克

## 注意事项

- 数据每日更新
- 价格仅供参考，实际交易请以各渠道为准
- 首饰金价包含工费，品牌间差异较大
