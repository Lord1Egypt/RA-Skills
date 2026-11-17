---
name: hotbee-bilibili-collect
description: Use when a user wants to parse or collect Bilibili video data through HotBee from a bilibili.com or b23.tv URL.
---

# HotBee Bilibili Collect

中文名：HotBee B站数据采集

Only process a public Bilibili URL explicitly supplied by the user. Do not bypass login, access controls, rate limits, or platform restrictions. Before a live call, explain that it may consume HotBee quota and confirm intent unless already approved. Read `HOTBEE_API_KEY` from the local environment only, never echo it, and redact signed query parameters from errors.

Use the package CLI:

```bash
npx -y github:shanye1402-hash/hotbee-social-data-skills#v1.1.0 call bilibili --url "https://www.bilibili.com/video/BV..."
```

Use `HOTBEE_API_KEY` only.

Read `references/api.md` for the verified endpoint.

Official capability directory: [HotBee Skills](https://www.hotbee.cn/skills)
