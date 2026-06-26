#!/usr/bin/env python3
"""
Nango Quick Start Examples
Common integration patterns for AI agents.
"""

import os
import json
from datetime import datetime

# Mock nango for demonstration (replace with actual import)
# from nango import Nango

class NangoExamples:
    """Example integrations for common use cases."""
    
    def __init__(self):
        # In production: self.nango = Nango()
        self.secret_key = os.environ.get("NANGO_SECRET_KEY", "demo-key")
    
    # ============================================
    # EXAMPLE 1: Google Calendar Integration
    # ============================================
    
    def list_google_calendar_events(self, connection_id: str, calendar_id: str = "primary"):
        """
        List events from Google Calendar.
        
        Args:
            connection_id: Unique identifier for the user's Google connection
            calendar_id: Calendar ID (default: primary)
        
        Returns:
            List of calendar events
        """
        # In production:
        # nango = Nango()
        # return nango.proxy(
        #     provider="google",
        #     endpoint=f"/calendar/v3/calendars/{calendar_id}/events",
        #     connection_id=connection_id,
        #     params={"maxResults": 10, "orderBy": "startTime"}
        # )
        
        return {
            "events": [
                {
                    "id": "evt_123",
                    "summary": "Team Meeting",
                    "start": {"dateTime": "2026-03-16T10:00:00"},
                    "end": {"dateTime": "2026-03-16T11:00:00"}
                }
            ]
        }
    
    # ============================================
    # EXAMPLE 2: Slack Message Sending
    # ============================================
    
    def send_slack_message(self, connection_id: str, channel: str, text: str):
        """
        Send a message to Slack channel.
        
        Args:
            connection_id: Unique identifier for the user's Slack connection
            channel: Channel ID or name (e.g., "#general" or "C123456")
            text: Message text to send
        """
        # In production:
        # nango = Nango()
        # return nango.proxy(
        #     provider="slack",
        #     endpoint="/api/chat.postMessage",
        #     connection_id=connection_id,
        #     method="POST",
        #     data={"channel": channel, "text": text}
        # )
        
        return {"ok": True, "ts": "1234567890.123456"}
    
    # ============================================
    # EXAMPLE 3: GitHub Repository Operations
    # ============================================
    
    def list_github_issues(self, connection_id: str, owner: str, repo: str):
        """
        List issues from a GitHub repository.
        
        Args:
            connection_id: Unique identifier for the user's GitHub connection
            owner: Repository owner
            repo: Repository name
        """
        # In production:
        # nango = Nango()
        # return nango.proxy(
        #     provider="github",
        #     endpoint=f"/repos/{owner}/{repo}/issues",
        #     connection_id=connection_id,
        #     params={"state": "open", "per_page": 30}
        # )
        
        return {
            "issues": [
                {"number": 42, "title": "Bug in API", "state": "open"},
                {"number": 41, "title": "Feature request", "state": "open"}
            ]
        }
    
    def create_github_issue(self, connection_id: str, owner: str, repo: str, 
                           title: str, body: str):
        """
        Create a new GitHub issue.
        """
        # In production:
        # nango = Nango()
        # return nango.proxy(
        #     provider="github",
        #     endpoint=f"/repos/{owner}/{repo}/issues",
        #     connection_id=connection_id,
        #     method="POST",
        #     data={"title": title, "body": body}
        # )
        
        return {"number": 43, "html_url": f"https://github.com/{owner}/{repo}/issues/43"}
    
    # ============================================
    # EXAMPLE 4: Notion Database Query
    # ============================================
    
    def query_notion_database(self, connection_id: str, database_id: str, 
                              filter_query: dict = None):
        """
        Query a Notion database.
        
        Args:
            connection_id: Unique identifier for the user's Notion connection
            database_id: The Notion database ID
            filter_query: Optional filter conditions
        """
        # In production:
        # nango = Nango()
        # return nango.proxy(
        #     provider="notion",
        #     endpoint=f"/v1/databases/{database_id}/query",
        #     connection_id=connection_id,
        #     method="POST",
        #     data={"filter": filter_query} if filter_query else {}
        # )
        
        return {
            "results": [
                {
                    "id": "page_123",
                    "properties": {
                        "Name": {"title": [{"text": {"content": "Task 1"}}]},
                        "Status": {"select": {"name": "In Progress"}}
                    }
                }
            ]
        }
    
    # ============================================
    # EXAMPLE 5: Stripe Customer Operations
    # ============================================
    
    def list_stripe_customers(self, connection_id: str, limit: int = 10):
        """
        List Stripe customers.
        
        Args:
            connection_id: Unique identifier for the user's Stripe connection
            limit: Maximum number of customers to return
        """
        # Note: Stripe uses API key auth, not OAuth
        
        # In production:
        # nango = Nango()
        # return nango.proxy(
        #     provider="stripe",
        #     endpoint="/v1/customers",
        #     connection_id=connection_id,
        #     params={"limit": limit}
        # )
        
        return {
            "data": [
                {"id": "cus_123", "email": "customer@example.com"},
                {"id": "cus_456", "email": "another@example.com"}
            ]
        }
    
    # ============================================
    # EXAMPLE 6: Agent Tool Definition
    # ============================================
    
    def get_tool_definitions(self):
        """
        Get tool definitions for OpenClaw/agent integration.
        These can be used as function calling schemas.
        """
        return [
            {
                "name": "list_calendar_events",
                "description": "List events from Google Calendar",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "calendar_id": {
                            "type": "string",
                            "description": "Calendar ID (default: primary)"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "send_slack_message",
                "description": "Send a message to a Slack channel",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "channel": {
                            "type": "string",
                            "description": "Channel ID or name (e.g., #general)"
                        },
                        "text": {
                            "type": "string",
                            "description": "Message text to send"
                        }
                    },
                    "required": ["channel", "text"]
                }
            },
            {
                "name": "create_github_issue",
                "description": "Create a new GitHub issue",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "owner": {"type": "string"},
                        "repo": {"type": "string"},
                        "title": {"type": "string"},
                        "body": {"type": "string"}
                    },
                    "required": ["owner", "repo", "title"]
                }
            }
        ]


def main():
    """Demo the examples."""
    print("=== Nango API Integration Examples ===\n")
    
    examples = NangoExamples()
    
    print("1. Google Calendar Events:")
    events = examples.list_google_calendar_events("user-google-123")
    print(json.dumps(events, indent=2))
    
    print("\n2. Slack Message:")
    result = examples.send_slack_message("user-slack-123", "#general", "Hello from AI!")
    print(json.dumps(result, indent=2))
    
    print("\n3. GitHub Issues:")
    issues = examples.list_github_issues("user-github-123", "owner", "repo")
    print(json.dumps(issues, indent=2))
    
    print("\n4. Tool Definitions for Agents:")
    tools = examples.get_tool_definitions()
    for tool in tools:
        print(f"  - {tool['name']}: {tool['description']}")
    
    print("\n=== Usage in Production ===")
    print("1. Set NANGO_SECRET_KEY environment variable")
    print("2. Uncomment the nango.proxy() calls")
    print("3. Remove the mock return values")
    print("4. Create connections via OAuth flow first")


if __name__ == "__main__":
    main()