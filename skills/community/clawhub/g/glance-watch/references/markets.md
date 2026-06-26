# 盯盘插件参考文档

## 环境配置

```bash
# 基础配置（桥接地址固定为 ws://glanceup-pre.100credit.cn）
export OPENCLAW_WS_TOKEN="<token>"

# Token 申请：在网页上申请 OPENCLAW_WS_TOKEN
```

## 市场类型与产品代码

| 市场 | productType | productCode 示例 | 行情频率 |
|------|-------------|-----------------|----------|
| A股个股 | stock | 000001 | 约每 3 秒 |
| A股指数 | index | 000300 | 约每 3 秒 |
| 港股 | hk_stock | 00700 | 延迟约 15 分钟 |
| 比特币 | crypto | BTCUSDT | 约每 10 秒 |

## 条件表达式

### 可用变量

- 通用: `price`, `volume`, `change_percent`
- A股/港股额外: `turnover_rate`
- 比特币: 不支持 `turnover_rate`

### 示例条件

```javascript
// 单一条件
'price >= threshold'

// 多条件
'price >= threshold and change_percent >= cp_threshold'

// A股专用
'price >= threshold and turnover_rate >= tr_threshold'
```

## 产品代码速查

### A股主要指数
- 沪深300: 000300
- 上证指数: 000001
- 创业板指: 399006

### 热门港股
- 腾讯控股: 00700
- 阿里巴巴: 09988
- 美团: 03690
- 比亚迪股份: 01211

### 主流加密货币
- 比特币: BTCUSDT
- 以太坊: ETHUSDT
- Solana: SOLUSDT
