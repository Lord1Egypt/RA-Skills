"""Block manipulation."""
from typing import Optional, Dict, Any, List
from .client import NotionClient


class BlockManager:
    """Manage Notion blocks."""
    
    def __init__(self, client: NotionClient):
        self.client = client
    
    def append(
        self,
        block_id: str,
        block_type: str,
        text: str,
        checked: Optional[bool] = None,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """Append a block to a page or block."""
        
        # Build block object based on type
        block_object: Dict[str, Any] = {
            "object": "block",
            "type": block_type
        }
        
        if block_type == "paragraph":
            block_object["paragraph"] = {
                "rich_text": [{"text": {"content": text}}]
            }
        elif block_type == "to_do":
            block_object["to_do"] = {
                "rich_text": [{"text": {"content": text}}],
                "checked": checked or False
            }
        elif block_type in ["heading_1", "heading_2", "heading_3"]:
            block_object[block_type] = {
                "rich_text": [{"text": {"content": text}}]
            }
        elif block_type == "code":
            block_object["code"] = {
                "rich_text": [{"text": {"content": text}}],
                "language": language or "plain text"
            }
        else:
            raise ValueError(f"Unsupported block type: {block_type}")
        
        payload = {"children": [block_object]}
        return self.client.patch(f"/blocks/{block_id}/children", json=payload)
    
    def get_children(self, block_id: str) -> Dict[str, Any]:
        """Get child blocks of a block."""
        return self.client.get(f"/blocks/{block_id}/children")
