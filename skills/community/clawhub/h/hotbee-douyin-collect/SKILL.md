---
name: hotbee-douyin-collect
description: Use when a user wants to parse or collect verified Douyin video, comment, creator, fan portrait, or hashtag data through HotBee APIs using Chinese natural-language instructions and Douyin links.
---

# HotBee Douyin Collect

中文名：HotBee 抖音数据采集

Only process public Douyin links or public identifiers the user explicitly provides. Before a key-authenticated live call, explain that it may consume HotBee quota and confirm intent unless the user already approved the spend. Read `HOTBEE_API_KEY` from the local environment only; never echo it or persist it in output. Redact request query parameters from errors.

Use the package CLI:

```bash
npx -y github:shanye1402-hash/hotbee-social-data-skills#v1.1.0 call douyin --text "解析这个视频的播放量和评论 https://v.douyin.com/xxxx/"
```

Use `HOTBEE_API_KEY` only for VIP endpoints. Free/no-key endpoints can run without a key. If a requested Douyin catalog path is listed as stale in `references/api.md`, explain the current contract gap instead of calling it.

Read `references/api.md` for endpoint list and Chinese intent mapping.

Official capability directory: [HotBee Skills](https://www.hotbee.cn/skills)
