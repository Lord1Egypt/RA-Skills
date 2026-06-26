"""Workspace search."""
from typing import Optional, Dict, Any
from .client import NotionClient


class SearchManager:
    """Search Notion workspace."""
    
    def __init__(self, client: NotionClient):
        self.client = client
    
    def search(self, query: str, object_type: Optional[str] = None) -> Dict[str, Any]:
        """Search workspace for pages or databases."""
        payload: Dict[str, Any] = {"query": query}
        
        if object_type:
            payload["filter"] = {"property": "object", "value": object_type}
        
        return self.client.post("/search", json=payload)
