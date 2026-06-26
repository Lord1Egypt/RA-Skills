"""Notion API client wrapper."""
import os
import requests
from typing import Optional, Dict, Any


class NotionClient:
    """Low-level Notion API client."""
    
    BASE_URL = "https://api.notion.com/v1"
    API_VERSION = "2022-06-28"
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("NOTION_TOKEN")
        if not self.token:
            raise ValueError("NOTION_TOKEN environment variable not set")
        
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": self.API_VERSION,
            "Content-Type": "application/json"
        }
    
    def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a request to the Notion API."""
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            if status == 401:
                raise Exception("Invalid NOTION_TOKEN - check your integration token")
            elif status == 404:
                raise Exception(f"Resource not found: {endpoint}")
            elif status == 403:
                raise Exception("Permission denied - check integration access")
            else:
                try:
                    error_data = e.response.json()
                    raise Exception(f"API error: {error_data.get('message', str(e))}")
                except:
                    raise Exception(f"API error: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
    
    def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return self.request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return self.request("POST", endpoint, **kwargs)
    
    def patch(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        return self.request("PATCH", endpoint, **kwargs)
