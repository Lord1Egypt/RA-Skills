---
name: prowlarr-search
description: 用Prowlarr搜索影视资源，搜索torrent种子，磁力链接Magnet
metadata: {"openclaw":{"emoji":"🔍 ","requires":{"bins":["python3"],"env":["PROWLARR_BASE_URL", "PROWLARR_API_KEY"]},"primaryEnv":"PROWLARR_API_KEY"}}
---

# 资源搜索

## 用法

通过 Prowlarr API 搜索资源（ torrents/usenet 等），并返回 JSON 格式的搜索结果列表。

通用搜索
```bash
python3 {baseDir}/scripts/prowlarr-search.py "<query>"
```

指定季数，集数搜索剧集
```bash
python3 {baseDir}/scripts/prowlarr-search.py "<query>" --type tv [--season SEASON] [--ep EP]
```

输出样例：
```json
  [                                                                                                
    {                                                                                              
      "title": "Example.Title.2024.1080p",                                                         
      "size": "2.50 GB",                                                                           
      "indexer": "SomeIndexer",                                                                    
      "guid": "magnet:?xt=...",                                                                    
      "publishDate": "2024-01-15T10:30:00Z"                                                        
    }
  ]
```
