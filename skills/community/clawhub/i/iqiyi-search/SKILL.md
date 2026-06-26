---
name: iqiyi-search
description: 搜索爱奇艺平台的电影、电视剧、综艺等影视内容，返回搜索结果和播放链接。当用户需要搜索爱奇艺上的影视内容、查找爱奇艺播放链接、或询问"爱奇艺上有什么"时使用此技能。
version: 1.0.0
author: Alan
metadata: {"openclaw":{"emoji":"🎬","requires":{"bins":["agent-browser"]}}}
---

# 爱奇艺影视搜索

使用浏览器自动化搜索爱奇艺平台的影视内容。

## 功能

- 搜索电影、电视剧、综艺等内容
- 返回5-10条搜索结果
- 包含标题、类型、简介、播放链接

## 使用方法

### 搜索影视内容

```bash
bash ~/.openclaw/workspace/skills/iqiyi-search/scripts/search.sh "搜索关键词"
```

示例：
```bash
bash ~/.openclaw/workspace/skills/iqiyi-search/scripts/search.sh "狂飙"
```

## 搜索结果格式

返回JSON格式：
```json
{
  "results": [
    {
      "title": "影视标题",
      "type": "电影/电视剧/综艺",
      "description": "简介",
      "url": "播放链接",
      "rating": "评分（如有）"
    }
  ]
}
```

## 注意事项

- 需要安装 agent-browser：`npm install -g agent-browser`
- 搜索结果依赖爱奇艺网页版，页面结构变化可能影响抓取
- 部分VIP内容可能需要登录才能观看完整版
