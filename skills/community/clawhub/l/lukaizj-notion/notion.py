import os
import asyncio
from typing import Optional, Dict, Any, List

NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")
BASE_URL = "https://api.notion.com/v1"


class NotionClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    async def create_page(self, parent_id: str, title: str, content: str = "") -> Dict[str, Any]:
        import requests
        if not requests:
            return {"success": False, "error": "requests not available"}
        
        url = f"{BASE_URL}/pages"
        properties = {"title": {"title": [{"text": {"content": title}}]}}
        
        if parent_id.startswith("http"):
            properties["parent"] = {"page_id": parent_id}
        else:
            properties["parent"] = {"database_id": parent_id}
        
        children = []
        if content:
            children.append({"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": content}}]}})
        
        payload = {"properties": properties}
        if children:
            payload["children"] = children
        
        try:
            loop = asyncio.get_event_loop()
            resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=self.headers, json=payload, timeout=30))
            data = resp.json()
            if resp.status_code == 200:
                return {"success": True, "page_id": data.get("id")}
            return {"success": False, "error": data.get("message", "Error")}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def query_database(self, database_id: str) -> Dict[str, Any]:
        import requests
        if not requests:
            return {"success": False, "error": "requests not available"}
        
        url = f"{BASE_URL}/databases/{database_id}/query"
        try:
            loop = asyncio.get_event_loop()
            resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=self.headers, json={}, timeout=30))
            data = resp.json()
            if resp.status_code == 200:
                return {"success": True, "results": data.get("results", [])}
            return {"success": False, "error": data.get("message", "Error")}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def search(self, query: str = "") -> Dict[str, Any]:
        import requests
        if not requests:
            return {"success": False, "error": "requests not available"}
        
        url = f"{BASE_URL}/search"
        payload = {"query": query} if query else {}
        try:
            loop = asyncio.get_event_loop()
            resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=self.headers, json=payload, timeout=30))
            data = resp.json()
            if resp.status_code == 200:
                return {"success": True, "results": data.get("results", [])}
            return {"success": False, "error": data.get("message", "Error")}
        except Exception as e:
            return {"success": False, "error": str(e)}


_client = None

def _get_client():
    global _client
    if not _client and NOTION_API_KEY:
        _client = NotionClient(NOTION_API_KEY)
    return _client


async def notion_create_page(parent_id: str, title: str, content: str = "") -> Dict[str, Any]:
    client = _get_client()
    if not client:
        return {"success": False, "error": "NOTION_API_KEY not configured"}
    return await client.create_page(parent_id, title, content)


async def notion_query_database(database_id: str) -> Dict[str, Any]:
    client = _get_client()
    if not client:
        return {"success": False, "error": "NOTION_API_KEY not configured"}
    return await client.query_database(database_id)


async def notion_search(query: str = "") -> Dict[str, Any]:
    client = _get_client()
    if not client:
        return {"success": False, "error": "NOTION_API_KEY not configured"}
    return await client.search(query)


TOOLS = [
    {"name": "notion_create_page", "description": "Create a new Notion page", "input_schema": {"type": "object", "properties": {"parent_id": {"type": "string", "description": "Parent page or database ID"}, "title": {"type": "string", "description": "Page title"}, "content": {"type": "string", "description": "Page content"}}, "required": ["parent_id", "title"]}},
    {"name": "notion_query_database", "description": "Query a Notion database", "input_schema": {"type": "object", "properties": {"database_id": {"type": "string", "description": "Database ID"}}, "required": ["database_id"]}},
    {"name": "notion_search", "description": "Search Notion pages", "input_schema": {"type": "object", "properties": {"query": {"type": "string", "description": "Search query"}}}},
]


if __name__ == "__main__":
    print("Notion Skill loaded")