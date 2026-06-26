# 股票配置参考

## A股列表

| 名称 | 代码 | 市场 |
|------|------|------|
| 美的集团 | 000333.SZ | A股 |
| 中控技术 | 688777.SH | A股 |
| 工商银行 | 601398.SH | A股 |
| 中国中车 | 601766.SH | A股 |
| 长安汽车 | 000625.SZ | A股 |
| 爱尔眼科 | 300015.SZ | A股 |
| 宋城演艺 | 300144.SZ | A股 |
| 青岛啤酒 | 600600.SH | A股 |

## 港股列表

| 名称 | 代码 | 市场 |
|------|------|------|
| 美团-W | 3690.HK | 港股 |
| 阿里巴巴-SW | 9988.HK | 港股 |
| 腾讯控股 | 0700.HK | 港股 |
| 吉利汽车 | 0175.HK | 港股 |
| 山高控股 | 0412.HK | 港股 |
| 华润燃气 | 1193.HK | 港股 |
| 顺丰控股 | 6936.HK | 港股 |
| 海尔智家 | 6690.HK | 港股 |

## 自定义股票

编辑 `scripts/monitor.js` 中的 CONFIG：

```javascript
const CONFIG = {
  aStocks: [
    { name: '股票名称', code: '代码', market: 'A股' },
    ...
  ],
  hkStocks: [
    { name: '股票名称', code: '代码', market: '港股' },
    ...
  ],
  ...
};
```

## 代码格式

- A股：`000333.SZ`（深市）、`601398.SH`（沪市）
- 港股：`3690.HK`（港股）

## 特殊告警配置

在 `scripts/alert-check.js` 中配置：

```javascript
const CONFIG = {
  stocks: [
    { name: '中国中车', code: '601766.SH', volumeAlert: true }, // 放量告警
    { name: '美团-W', code: '3690.HK', priceTargets: [80, 85] }, // 价格告警
    ...
  ]
};
```

- `volumeAlert: true` - 放量时告警
- `priceTargets: [价格列表]` - 价格触及时告警