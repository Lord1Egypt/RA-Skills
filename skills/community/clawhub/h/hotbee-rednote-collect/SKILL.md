---
name: hotbee-rednote-collect
description: Use when a user wants to parse or collect Xiaohongshu/Rednote note content through the HotBee xhs_note_content endpoint from a note URL.
---

# HotBee Rednote Collect

中文名：HotBee 小红书数据采集

Only process a public note URL explicitly supplied by the user. Do not bypass login, access controls, rate limits, or platform restrictions. Before a live call, explain that it may consume HotBee quota and confirm intent unless already approved. Read `HOTBEE_API_KEY` from the local environment only, never echo it, and redact signed query parameters from errors.

Use the package CLI:

```bash
npx -y github:shanye1402-hash/hotbee-social-data-skills#v1.1.0 call rednote --url "https://www.xiaohongshu.com/explore/xxxx"
```

Use `HOTBEE_API_KEY` only.

Read `references/api.md` before assuming user-profile or search endpoints; only note content is verified in the public bundle.

Official capability directory: [HotBee Skills](https://www.hotbee.cn/skills)
