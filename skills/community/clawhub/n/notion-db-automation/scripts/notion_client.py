#!/usr/bin/env python3
"""
Notion Database Client
Simplified wrapper for Notion API to handle common database operations.
"""

import os
import requests
from typing import Dict, List, Any, Optional

class NotionDBClient:
    """Client for interacting with Notion databases."""
    
    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize the Notion client.
        
        Args:
            api_token: Notion API token. If None, reads from NOTION_API_TOKEN env var.
        """
        self.api_token = api_token or os.environ.get('NOTION_API_TOKEN')
        if not self.api_token:
            raise ValueError("API token required. Set NOTION_API_TOKEN or pass it explicitly.")
        
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
    
    def query_database(
        self,
        database_id: str,
        filter: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
        start_cursor: Optional[str] = None,
        page_size: int = 100
    ) -> List[Dict]:
        """
        Query a database with filtering and sorting. Handles pagination automatically.
        
        Args:
            database_id: ID of the Notion database
            filter: Filter object according to Notion API spec
            sorts: List of sort objects
            start_cursor: Pagination start cursor
            page_size: Results per page (max 100)
        
        Returns:
            List of all matching page objects
        """
        all_results = []
        has_more = True
        
        while has_more:
            payload: Dict[str, Any] = {"page_size": page_size}
            if filter:
                payload["filter"] = filter
            if sorts:
                payload["sorts"] = sorts
            if start_cursor:
                payload["start_cursor"] = start_cursor
            
            response = requests.post(
                f"{self.base_url}/databases/{database_id}/query",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            
            all_results.extend(data["results"])
            has_more = data["has_more"]
            start_cursor = data.get("next_cursor")
        
        return all_results
    
    def create_page(
        self,
        database_id: str,
        properties: Dict,
        children: Optional[List] = None
    ) -> Dict:
        """
        Create a new page in the database.
        
        Args:
            database_id: ID of the Notion database
            properties: Properties object matching the database schema
            children: Optional list of block content for the page body
        
        Returns:
            Created page object
        """
        payload = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        if children:
            payload["children"] = children
        
        response = requests.post(
            f"{self.base_url}/pages",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def update_page(self, page_id: str, properties: Dict) -> Dict:
        """
        Update properties of an existing page.
        
        Args:
            page_id: ID of the page to update
            properties: Updated properties
        
        Returns:
            Updated page object
        """
        response = requests.patch(
            f"{self.base_url}/pages/{page_id}",
            headers=self.headers,
            json={"properties": properties}
        )
        response.raise_for_status()
        return response.json()
    
    def archive_page(self, page_id: str, archived: bool = True) -> Dict:
        """Archive (delete) or unarchive a page."""
        response = requests.patch(
            f"{self.base_url}/pages/{page_id}",
            headers=self.headers,
            json={"archived": archived}
        )
        response.raise_for_status()
        return response.json()
    
    def get_database_schema(self, database_id: str) -> Dict:
        """Get the database schema/properties metadata."""
        response = requests.get(
            f"{self.base_url}/databases/{database_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_page_content(self, block_id: str, page_size: int = 100) -> List[Dict]:
        """Get all child blocks (page content) for a page."""
        all_blocks = []
        has_more = True
        start_cursor = None
        
        while has_more:
            params: Dict[str, Any] = {"page_size": page_size}
            if start_cursor:
                params["start_cursor"] = start_cursor
            
            response = requests.get(
                f"{self.base_url}/blocks/{block_id}/children",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            all_blocks.extend(data["results"])
            has_more = data["has_more"]
            start_cursor = data.get("next_cursor")
        
        return all_blocks


# Helper functions for building property objects

def title_property(value: str) -> Dict:
    """Create a title property object."""
    return {
        "title": [{"text": {"content": value}}]
    }

def text_property(value: str) -> Dict:
    """Create a rich text property object."""
    return {
        "rich_text": [{"text": {"content": value}}]
    }

def number_property(value: float) -> Dict:
    """Create a number property object."""
    return {
        "number": value
    }

def select_property(value: str) -> Dict:
    """Create a select property object."""
    return {
        "select": {"name": value}
    }

def multi_select_property(values: List[str]) -> Dict:
    """Create a multi-select property object."""
    return {
        "multi_select": [{"name": v} for v in values]
    }

def checkbox_property(value: bool) -> Dict:
    """Create a checkbox property object."""
    return {
        "checkbox": value
    }

def date_property(start: str, end: Optional[str] = None) -> Dict:
    """Create a date property object."""
    date_obj = {"start": start}
    if end:
        date_obj["end"] = end
    return {
        "date": date_obj
    }

def url_property(url: str) -> Dict:
    """Create a URL property object."""
    return {
        "url": url
    }

def email_property(email: str) -> Dict:
    """Create an email property object."""
    return {
        "email": email
    }
