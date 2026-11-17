---
name: hotbee-hot-rankings
description: Use when a user asks for HotBee all-web hot rankings, 热榜, 热搜, trending topics, or platform hot-search ranking data. Supports confirmed HotBee endpoints for Xiaohongshu, Douyin, Baidu, Weibo, and Bilibili hot rankings; do not invent unverified platform endpoints.
---

# HotBee Hot Rankings

中文名：HotBee 全网热榜

Hot-ranking calls are treated as paid. Start with `--dry-run`, explain the selected platforms and possible quota use, and confirm a live call unless the user already approved the spend. Read `HOTBEE_API_KEY` from the local environment only; never echo or persist it. Do not invent unsupported platform endpoints.

Use the confirmed HotBee hot-ranking endpoints:

- Base: `https://www.smsz.xyz/prod-api`
- Endpoints:
  - `GET /tool/hot/xiaohongshu`
  - `GET /tool/hot/douyin`
  - `GET /tool/hot/baidu`
  - `GET /tool/hot/weibo`
  - `GET /tool/hot/bilibili`
- Required query: `key`
- Known cost: Xiaohongshu OpenAPI states 5 points per call. Treat other confirmed hot endpoints as paid unless HotBee documents otherwise.

```bash
npx -y github:shanye1402-hash/hotbee-social-data-skills#v1.1.0 call hot-rankings --dry-run --text "获取百度和抖音热榜"
```

For all confirmed platforms:

- Select platform from Chinese text or `--platform`.
- Use all confirmed platforms when the user asks for `全网`, `全部`, `所有`, `各平台`, or `多平台`.
- Run live only when `HOTBEE_API_KEY` is available.
- Return API fields such as `datas_info[].title`, `score`, `word_type`, `rank_change`, plus `time` and `tips` when present.

If the user asks for Zhihu, Toutiao, Kuaishou, Tieba, or another unsupported platform, explain that the HotBee endpoint is not confirmed and ask for the official OpenAPI contract.

Read `references/api.md` for the exact request and response contract.

Official capability directory: [HotBee Skills](https://www.hotbee.cn/skills)
