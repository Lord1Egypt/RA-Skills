# Leaderboard Discovery 策略

## 7 种发现策略

| 策略 | Category | TimePeriod | OrderBy | Limit | 目的 |
|------|----------|------------|---------|-------|------|
| 历史总榜 | OVERALL | ALL | PNL | 200 | 长期稳定盈利者 |
| 本周热门 | OVERALL | WEEK | PNL | 50 | 近期活跃高手 |
| 本月热门 | OVERALL | MONTH | PNL | 50 | 中期趋势交易者 |
| Crypto专家 | CRYPTO | ALL | PNL | 50 | Crypto 领域专家 |
| 政治专家 | POLITICS | ALL | PNL | 50 | 政治预测专家 |
| 体育专家 | SPORTS | ALL | PNL | 50 | 体育博彩专家 |
| 高交易量 | OVERALL | ALL | VOL | 50 | 大资金玩家（用于交叉验证） |

## API 参数

```
GET https://data-api.polymarket.com/v1/leaderboard
  ?category=OVERALL    # OVERALL/POLITICS/SPORTS/CRYPTO/CULTURE/WEATHER/ECONOMICS/TECH/FINANCE
  &timePeriod=ALL      # DAY/WEEK/MONTH/ALL
  &orderBy=PNL         # PNL/VOL
  &limit=50            # 1-50
  &offset=0            # 0-1000
```

## 返回字段

```json
{
  "rank": "1",
  "proxyWallet": "0x...",
  "userName": "Theo4",
  "vol": 43013259,
  "pnl": 22053934,
  "profileImage": "...",
  "xUsername": "...",
  "verifiedBadge": true
}
```

## 去重逻辑

同一地址可能出现在多个策略中。去重时：
- 保留最高 PnL 和 Volume
- 合并所有来源标签
- 保留最佳排名
- 合并 Twitter 用户名和认证状态

## 可用分类

OVERALL, POLITICS, SPORTS, CRYPTO, CULTURE, MENTIONS, WEATHER, ECONOMICS, TECH, FINANCE
