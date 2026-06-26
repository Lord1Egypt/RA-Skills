---
name: nemo-community-hot-articles
description: Get trending articles from Nemo community/从Nemo社区获取热门文章 (no API key required).
homepage: https://www.link-nemo.com/popular
metadata: {"clawdbot":{"emoji":"🔥","requires":{"bins":["curl"]}}}
---

# Nemo Community Hot Articles

Free service, no API keys needed. Fetch trending posts from Nemo community.
免费服务，无需API秘钥，即可从Nemo社区获取热门文章

## Popular Articles API/热门文章API

Quick one-liner:
```bash
curl -s "https://www.link-nemo.com/api/popular/article" | jq '.data[0:3] | .[] | {title, section, hot, url}'
# Output:
# {"title":"文章标题","section":"早报","hot":457, "url": "文章链接"}
# {"title":"另一篇热文","section":"资讯","hot":389, "url": "文章链接"}
# ...
