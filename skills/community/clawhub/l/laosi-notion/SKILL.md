---
name: notion-helper
description: Notion API助手 - 创建和管理Notion页面、数据库，支持笔记和知识管理。
metadata: {"openclaw": {"requires": {"python": ["notion-client"]}, "install": []}}
tags: [notion, notes, database, knowledge, api]
version: 1.0.0
author: laosi
source: adapted
---

# Notion Helper - Notion助手

> 激活词: Notion / 笔记管理 / 知识库

## 安装

```bash
pip install notion-client
```

## 获取API密钥

1. 访问 https://www.notion.so/my-integrations
2. 创建新集成
3. 复制API密钥
4. 分享数据库给集成

## Python实现

```python
from notion_client import AsyncClient
import asyncio

class NotionHelper:
    def __init__(self, token: str):
        self.client = AsyncClient(auth=token)
    
    async def create_page(self, parent_id: str, title: str, content: str = ""):
        await self.client.pages.create(
            parent={"database_id": parent_id},
            properties={
                "title": {
                    "title": [{"text": {"content": title}}]
                }
            },
            children=[{
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": content}}]
                }
            }]
        )
    
    async def query_database(self, db_id: str, filter_props: dict = None):
        params = {"database_id": db_id}
        if filter_props:
            params["filter"] = filter_props
        return await self.client.databases.query(**params)
    
    async def update_page(self, page_id: str, properties: dict):
        await self.client.pages.update(page_id, properties=properties)
    
    async def get_page(self, page_id: str):
        return await self.client.pages.retrieve(page_id)
    
    async def search(self, query: str):
        return await self.client.search(query)
```

## 使用示例

```python
async def main():
    helper = NotionHelper("secret_xxx")
    
    # 创建页面
    await helper.create_page(
        parent_id="database_id",
        title="AI学习笔记",
        content="今天学习了机器学习..."
    )
    
    # 搜索页面
    results = await helper.search("AI")
    for page in results['results']:
        print(page['title'])
    
    # 查询数据库
    pages = await helper.query_database("database_id")
    for page in pages['results']:
        print(page['properties']['title']['title'][0]['text']['content'])

asyncio.run(main())
```

## 数据类型

| 类型 | 说明 |
|------|------|
| title | 标题 |
| rich_text | 文本 |
| number | 数字 |
| checkbox | 复选框 |
| select | 单选 |
| multi_select | 多选 |
| date | 日期 |
| url | 链接 |
| email | 邮箱 |
| phone_number | 电话 |

## 使用场景

1. 知识库管理
2. 任务跟踪
3. 笔记整理
4. 项目管理