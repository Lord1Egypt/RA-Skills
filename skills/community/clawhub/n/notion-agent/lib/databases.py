"""Database query and manipulation."""
from typing import Optional, Dict, Any, List
from .client import NotionClient


class DatabaseManager:
    """Manage Notion databases."""
    
    def __init__(self, client: NotionClient):
        self.client = client
    
    def query(self, db_id: str, filter_dict: Optional[Dict] = None, sort_list: Optional[List] = None) -> Dict[str, Any]:
        """Query a database with optional filters and sorts."""
        payload: Dict[str, Any] = {}
        
        if filter_dict:
            payload["filter"] = filter_dict
        
        if sort_list:
            payload["sorts"] = sort_list
        
        return self.client.post(f"/databases/{db_id}/query", json=payload)
    
    def add_page(self, db_id: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Add a page to a database."""
        payload = {
            "parent": {"database_id": db_id},
            "properties": properties
        }
        return self.client.post("/pages", json=payload)
    
    def list_all(self) -> List[Dict[str, Any]]:
        """List all databases (via search with filter)."""
        payload = {
            "filter": {"property": "object", "value": "database"}
        }
        result = self.client.post("/search", json=payload)
        return result.get("results", [])
