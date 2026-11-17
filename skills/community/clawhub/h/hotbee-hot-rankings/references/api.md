# Hot Rankings API

Base: `https://www.smsz.xyz/prod-api`

All confirmed hot-ranking endpoints use:

- Method: `GET`
- Required query: `key`
- Default key source: `HOTBEE_API_KEY`

## Confirmed endpoints

| Platform | Chinese name | Endpoint | Confirmation |
| --- | --- | --- | --- |
| `xiaohongshu` | 小红书热搜榜 | `/tool/hot/xiaohongshu` | OpenAPI contract, 5 points per call |
| `douyin` | 抖音热榜 | `/tool/hot/douyin` | no-key probe returned missing `key` |
| `baidu` | 百度热榜 | `/tool/hot/baidu` | no-key probe returned missing `key` |
| `weibo` | 微博热搜榜 | `/tool/hot/weibo` | no-key probe returned missing `key` |
| `bilibili` | B站热榜 | `/tool/hot/bilibili` | no-key probe returned missing `key` |

Example:

```bash
npx -y github:shanye1402-hash/hotbee-social-data-skills#v1.1.0 call hot-rankings --dry-run --text "获取百度和抖音热榜"
```

All confirmed platforms:

```bash
npx -y github:shanye1402-hash/hotbee-social-data-skills#v1.1.0 call hot-rankings --dry-run --text "全网热榜"
```

Specific platform flag:

```bash
npx -y github:shanye1402-hash/hotbee-social-data-skills#v1.1.0 call hot-rankings --dry-run --platform baidu --platform douyin
```

Expected response shape follows the Xiaohongshu OpenAPI pattern when fields are present:

```json
{
  "msg": "成功获取热榜数据...",
  "code": 200,
  "datas_info": [
    {
      "score": "921万",
      "word_type": "热",
      "rank_change": 0,
      "title": "热搜标题"
    }
  ],
  "time": "2026-04-21 17:15:21",
  "tips": "提示信息"
}
```

## Current scope

Confirmed: 小红书、抖音、百度、微博、B站。

Not confirmed from public HotBee docs or no-key probes: 知乎、头条、快手、贴吧 and other platforms. Do not invent endpoints for them; ask for the official OpenAPI contract or use browsing/search tools with citations when available.
