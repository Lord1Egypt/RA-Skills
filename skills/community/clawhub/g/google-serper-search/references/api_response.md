# Serper API 响应格式

## 网页搜索响应 (POST /search)

```json
{
  "searchParameters": {
    "q": "搜索关键词",
    "type": "search"
  },
  "knowledgeGraph": {
    "title": "标题",
    "type": "类型",
    "description": "描述",
    "attributes": {}
  },
  "organic": [
    {
      "title": "结果标题",
      "link": "https://example.com",
      "snippet": "结果摘要",
      "position": 1
    }
  ],
  "peopleAlsoAsk": [
    {
      "question": "相关问题",
      "snippet": "答案摘要",
      "link": "https://example.com"
    }
  ],
  "relatedSearches": [
    {
      "query": "相关搜索词"
    }
  ]
}
```

## 图片搜索响应 (POST /images)

```json
{
  "searchParameters": {
    "q": "搜索关键词",
    "type": "images"
  },
  "images": [
    {
      "title": "图片标题",
      "imageUrl": "https://example.com/image.jpg",
      "imageWidth": 800,
      "imageHeight": 600,
      "thumbnailUrl": "https://example.com/thumb.jpg",
      "source": "来源网站",
      "link": "https://example.com"
    }
  ]
}
```
