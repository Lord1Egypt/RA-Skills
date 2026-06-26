#!/usr/bin/env python3
"""
Knowledge Base Connector Script
This script demonstrates how to connect to a knowledge base API
and perform searches or chat interactions.
"""

import json
import requests
import argparse
from typing import Dict, List, Optional


class KnowledgeBaseConnector:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the knowledge base connector
        
        Args:
            base_url: The base URL of the knowledge base API
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Content-Type': 'application/json'
        }
        if api_key:
            self.headers['Authorization'] = f'Bearer {api_key}'
    
    def health_check(self) -> bool:
        """Check if the knowledge base API is accessible"""
        try:
            response = requests.get(f"{self.base_url}/health", headers=self.headers)
            return response.status_code == 200
        except Exception:
            return False
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Perform a search in the knowledge base
        
        Args:
            query: The search query
            top_k: Number of results to return
            
        Returns:
            List of search results
        """
        search_payload = {
            "query": query,
            "top_k": top_k
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/search", 
                headers=self.headers, 
                json=search_payload
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Search failed with status {response.status_code}: {response.text}")
                return []
        except Exception as e:
            print(f"Error performing search: {str(e)}")
            return []
    
    def chat(self, message: str, history: Optional[List[Dict]] = None) -> str:
        """
        Engage in a chat conversation with the knowledge base
        
        Args:
            message: The user's message
            history: Conversation history (list of {'role': 'user'|'assistant', 'content': '...'})
            
        Returns:
            Assistant's response
        """
        chat_payload = {
            "message": message,
            "history": history or []
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/chat", 
                headers=self.headers, 
                json=chat_payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', result.get('answer', 'No response'))
            else:
                print(f"Chat request failed with status {response.status_code}: {response.text}")
                return "Sorry, I couldn't process your request."
        except Exception as e:
            print(f"Error during chat: {str(e)}")
            return "Sorry, I encountered an error processing your request."


def main():
    parser = argparse.ArgumentParser(description="Knowledge Base Connector")
    parser.add_argument("--url", required=True, help="Knowledge base API URL")
    parser.add_argument("--api-key", help="API key for authentication")
    parser.add_argument("--action", choices=["health", "search", "chat"], required=True, 
                       help="Action to perform")
    parser.add_argument("--query", help="Search query")
    parser.add_argument("--message", help="Chat message")
    parser.add_argument("--top-k", type=int, default=5, help="Number of search results")
    
    args = parser.parse_args()
    
    kb = KnowledgeBaseConnector(args.url, args.api_key)
    
    if args.action == "health":
        if kb.health_check():
            print("✓ Knowledge base is accessible")
        else:
            print("✗ Knowledge base is not accessible")
    
    elif args.action == "search":
        if not args.query:
            print("Error: --query is required for search action")
            return
        
        results = kb.search(args.query, args.top_k)
        print(json.dumps(results, indent=2))
    
    elif args.action == "chat":
        if not args.message:
            print("Error: --message is required for chat action")
            return
        
        response = kb.chat(args.message)
        print(response)


if __name__ == "__main__":
    main()