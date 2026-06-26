"""Page CRUD operations."""
from typing import Optional, Dict, Any
from .client import NotionClient


class PageManager:
    """Manage Notion pages."""
    
    def __init__(self, client: NotionClient):
        self.client = client
    
    def create(self, parent_id: str, title: str, content: Optional[str] = None) -> Dict[str, Any]:
        """Create a new page."""
        payload = {
            "parent": {"page_id": parent_id},
            "properties": {
                "title": {
                    "title": [{"text": {"content": title}}]
                }
            }
        }
        
        # Add content as paragraph block if provided
        if content:
            payload["children"] = [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"text": {"content": content}}]
                    }
                }
            ]
        
        return self.client.post("/pages", json=payload)
    
    def get(self, page_id: str) -> Dict[str, Any]:
        """Retrieve a page."""
        return self.client.get(f"/pages/{page_id}")
    
    def update(self, page_id: str, title: Optional[str] = None) -> Dict[str, Any]:
        """Update a page's properties."""
        payload = {"properties": {}}
        
        if title:
            payload["properties"]["title"] = {
                "title": [{"text": {"content": title}}]
            }
        
        return self.client.patch(f"/pages/{page_id}", json=payload)
    
    def delete(self, page_id: str) -> Dict[str, Any]:
        """Archive (soft delete) a page."""
        payload = {"archived": True}
        return self.client.patch(f"/pages/{page_id}", json=payload)
    
    def list_children(self, page_id: str) -> Dict[str, Any]:
        """List child pages (via blocks endpoint)."""
        return self.client.get(f"/blocks/{page_id}/children")
