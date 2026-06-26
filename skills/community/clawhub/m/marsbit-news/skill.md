# Marsbit News Skill

name: marsbit-news  
description: Retrieve crypto, blockchain and Web3 news articles and flash updates from Marsbit.Marsbit is a crypto and Web3 media platform providing market news, analysis, and real-time updates.  
keywords: crypto, blockchain, web3, bitcoin, ethereum, defi, nft  
version: 1.0.0  
author: Marsbit  
source: https://news.marsbit.co  

Marsbit News Skill provides structured crypto news data including:

- latest crypto articles
- full article content
- article search by keyword
- latest flash news
- flash news search

Base API

https://api.marsbit.co/info/ai


---

# Tools


## get_latest_articles

Retrieve the latest Marsbit articles.

Endpoint  
GET /articles/latest

Parameters

| name | type | required | description |
|-----|------|----------|-------------|
| limit | integer | no | number of articles to return |

Example

https://api.marsbit.co/info/ai/articles/latest?limit=5

Response Example

{
  "data": [
    {
      "id": "20260310172909758349",
      "title": "获顶级风投押注，Zcash原班人马2500万美元「再创业」",
      "summary": "...",
      "url": "https://news.marsbit.co/20260310172909758349.html",
      "publishedAt": "2026-03-10T09:29:10Z",
      "source": "Marsbit"
    }
  ]
}

Notes  
Returns article metadata only. Use `get_article_detail` to retrieve full content.



---

## get_article_detail

Retrieve the full content of a Marsbit article.

Endpoint  
GET /articles/detail

Parameters

| name | type | required | description |
|-----|------|----------|-------------|
| id | string | yes | article id |

Example

https://api.marsbit.co/info/ai/articles/detail?id=20260310163710942215

Response Example

{
  "data": {
    "id": "20260310163710942215",
    "title": "你的AI焦虑，正在被人收割",
    "summary": "...",
    "url": "https://news.marsbit.co/20260310163710942215.html",
    "publishedAt": "2026-03-10T08:37:11Z",
    "source": "Marsbit",
    "content": "..."
  }
}

Notes  
Returns full article content.



---

## search_articles

Search Marsbit articles by keyword.

Endpoint  
GET /articles/search

Parameters

| name | type | required | description |
|-----|------|----------|-------------|
| query | string | yes | search keyword |
| limit | integer | no | max number of results |

Example

https://api.marsbit.co/info/ai/articles/search?query=BTC&limit=5



---

## get_latest_flashes

Retrieve the latest Marsbit flash news.

Flash news are short real-time updates about the crypto market.

Endpoint  
GET /flashes/latest

Parameters

| name | type | required | description |
|-----|------|----------|-------------|
| limit | integer | no | number of flash updates |

Example

https://api.marsbit.co/info/ai/flashes/latest?limit=10

Response Example

{
  "data": [
    {
      "id": "20260310174744190518",
      "title": "Wintermute：中东局势升级推动油价冲击，加密资产逆势跑赢",
      "url": "https://news.marsbit.co/flash/20260310174744190518.html",
      "publishedAt": "2026-03-10T09:47:44Z",
      "source": "Marsbit",
      "content": "..."
    }
  ]
}



---

## search_flashes

Search Marsbit flash news by keyword.

Endpoint  
GET /flashes/search

Parameters

| name | type | required | description |
|-----|------|----------|-------------|
| query | string | yes | search keyword |
| limit | integer | no | max results |

Example

https://api.marsbit.co/info/ai/flashes/search?query=BTC&limit=10



---

# Tool Selection Guide

| user request | tool |
|--------------|------|
| latest crypto articles | get_latest_articles |
| read full article | get_article_detail |
| search topic articles | search_articles |
| latest crypto breaking news | get_latest_flashes |
| search flash news | search_flashes |



---

# Response Guidelines

When presenting results:

1. show title  
2. summarize key points  
3. include publish time  
4. include source  
5. include url  

Avoid returning full article content unless the user explicitly asks.



---

# Example Prompts

These user requests should trigger this skill.

English examples

- latest crypto news
- latest Marsbit articles
- Bitcoin news
- Ethereum news
- crypto breaking news
- search BTC news
- crypto market updates

Chinese examples

- 最新加密新闻
- Marsbit 最新文章
- BTC 新闻
- ETH 新闻
- 最新快讯
- 比特币新闻
- 加密市场资讯



---

# Time Format

All timestamps use ISO 8601 UTC format.

Example

2026-03-10T09:29:10Z



---

# Error Handling

If `data` is empty, return that no matching results were found.



---

# Source

Marsbit  
https://news.marsbit.co