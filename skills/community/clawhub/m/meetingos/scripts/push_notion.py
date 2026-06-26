"""
MeetingOS — Notion 集成
将行动项推送到 Notion Database，创建会议纪要页面
"""
import os
from notion_client import Client

def push_to_notion(analysis: dict, markdown: str) -> dict:
    notion = Client(auth=os.getenv("NOTION_API_KEY"))
    db_id = os.getenv("NOTION_DATABASE_ID")
    
    # 创建主纪要页面
    page = notion.pages.create(
        parent={"database_id": db_id},
        properties={
            "Name": {"title": [{"text": {"content": analysis["meeting_metadata"]["title"]}}]},
            "Date": {"date": {"start": analysis["meeting_metadata"]["date_detected"]}},
            "Type": {"select": {"name": analysis["meeting_metadata"]["meeting_type"]}},
            "Action Items": {"number": analysis["statistics"]["total_action_items"]},
        },
        children=[{
            "object": "block", "type": "paragraph",
            "paragraph": {"rich_text": [{"text": {"content": markdown[:2000]}}]}
        }]
    )
    return {"page_url": page["url"], "page_id": page["id"]}
