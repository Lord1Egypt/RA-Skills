#!/usr/bin/env python3
"""
Integration example: Using msgraph skill with an LLM (OpenAI, etc).

Shows how to:
1. Fetch email/calendar data
2. Format for LLM context
3. Handle LLM instructions to modify email/calendar
4. Parse and execute resulting commands
"""

import sys
import json
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import auth
import mail
import cal
import graph_api
import utils


# ── Utility: Format email for LLM context ──────────────────────────────────

def format_inbox_for_context(max_messages=10):
    """
    Fetch and format inbox for inclusion in LLM prompt context.
    
    Returns a string suitable for passing to LLM:
    "Here are your recent emails:\n
    1. [unread] Alice Smith: Subject (2026-03-03 10:30)
    2. [read] Bob Johnson: Subject (2026-03-02 14:15)
    ..."
    """
    try:
        path = "/me/mailFolders/inbox/messages"
        params = {
            "$select": "id,subject,from,isRead,receivedDateTime",
            "$top": str(max_messages),
            "$orderby": "receivedDateTime desc"
        }
        result = graph_api.graph_get(path, params)
        
        emails = result.get("value", [])
        if not emails:
            return "No unread messages."
        
        formatted = "Recent emails:\n"
        for i, msg in enumerate(emails, 1):
            sender = msg.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
            subject = msg.get("subject", "(no subject)")
            date = msg.get("receivedDateTime", "")
            is_read = msg.get("isRead", False)
            msg_id = msg.get("id", "")
            
            # Format date
            try:
                date_formatted = utils.format_datetime(date)
            except:
                date_formatted = date[:10]
            
            # Indicator
            indicator = "[read]" if is_read else "[UNREAD]"
            
            formatted += f"{i}. {indicator} {sender}: {subject}\n"
            formatted += f"   Date: {date_formatted} | ID: {msg_id[:8]}...\n"
        
        return formatted
        
    except Exception as e:
        return f"Error fetching inbox: {e}"


# ── Utility: Format calendar for LLM context ───────────────────────────────

def format_calendar_for_context(days=7):
    """
    Fetch and format upcoming events for LLM prompt.
    
    Returns formatted string:
    "Upcoming events (next 7 days):
    • 2026-03-03 14:00: Team Sync
    • 2026-03-04 10:00: Client Call
    ..."
    """
    try:
        # In real usage, set proper date range
        path = "/me/calendarview"
        params = {
            "$select": "id,subject,start,end,organizer",
            "$orderby": "start/dateTime",
            "$top": "20"
        }
        result = graph_api.graph_get(path, params)
        
        events = result.get("value", [])
        if not events:
            return f"No events scheduled (next {days} days)."
        
        formatted = f"Upcoming events (next {days} days):\n"
        for event in events[:10]:
            subject = event.get("subject", "(no title)")
            start = event.get("start", {}).get("dateTime", "")
            
            # Format datetime
            try:
                start_formatted = utils.format_datetime(start)
            except:
                start_formatted = start[:16]
            
            formatted += f"• {start_formatted}: {subject}\n"
        
        return formatted
        
    except Exception as e:
        return f"Error fetching calendar: {e}"


# ── LLM Integration Example ────────────────────────────────────────────────

class EmailCalendarAssistant:
    """
    Example LLM-powered assistant that can read and modify email/calendar.
    
    This shows the pattern for integrating with OpenAI, Claude, etc.
    """
    
    def __init__(self):
        """Initialize assistant and check auth."""
        self.token = auth.load_tokens()
        if not self.token:
            raise RuntimeError("Not authenticated. Run: python scripts/auth.py login")
    
    def get_context_for_llm(self):
        """Build context string to pass to LLM."""
        sections = []
        
        # Email context
        sections.append("## Email")
        sections.append(format_inbox_for_context(5))
        
        # Calendar context
        sections.append("\n## Calendar")
        sections.append(format_calendar_for_context(7))
        
        return "\n".join(sections)
    
    def execute_command(self, command):
        """
        Execute an email/calendar command.
        
        Commands might be like:
        - "move message abc123 to folder Newsletters"
        - "create event on 2026-03-10 at 14:00 titled 'Team Sync'"
        - "search for emails from alice@example.com"
        """
        print(f"Executing: {command}")
        # Implementation would parse and execute the command
        return "Command executed"
    
    def process_llm_response(self, response):
        """
        Parse LLM response that might contain action commands.
        
        LLM might respond with structured actions:
        {'message': '...', 'actions': [{'type': 'move', 'id': '...', 'folder': '...'}]}
        """
        try:
            data = json.loads(response)
            actions = data.get("actions", [])
            
            results = []
            for action in actions:
                action_type = action.get("type")
                
                if action_type == "move":
                    msg_id = action.get("id")
                    folder = action.get("folder")
                    folder_id = mail.resolve_folder_id(folder)
                    result = graph_api.graph_post(
                        f"/me/messages/{msg_id}/move",
                        {"destinationId": folder_id}
                    )
                    results.append(f"✓ Moved message to {folder}")
                
                elif action_type == "create_event":
                    payload = action.get("payload")
                    result = graph_api.graph_post("/me/events", payload)
                    results.append(f"✓ Created event: {payload.get('subject')}")
                
                elif action_type == "search":
                    query = action.get("query")
                    params = {"$search": f'"{query}"', "$top": "10"}
                    result = graph_api.graph_get("/me/messages", params)
                    results.append(f"✓ Found {len(result.get('value', []))} messages")
            
            return results
            
        except json.JSONDecodeError:
            print("Warning: Response not valid JSON")
            return []


# ── Example Usage ──────────────────────────────────────────────────────────

def main():
    """Demonstrate LLM integration pattern."""
    
    print("=== Email/Calendar + LLM Integration Example ===\n")
    
    try:
        assistant = EmailCalendarAssistant()
        
        # 1. Get context for LLM
        print("📋 Building context for LLM...\n")
        context = assistant.get_context_for_llm()
        print(context)
        print("\n" + "="*50 + "\n")
        
        # 2. Example: Show what you'd send to LLM
        llm_prompt = f"""You are an email and calendar assistant. 
Help the user manage their inbox and schedule.

{context}

User request: "Show me my unread emails and upcoming meetings"

Respond with:
1. A summary message
2. If you need to take actions, include a JSON block:
   {{"message": "...", "actions": [...]}}
"""
        print("📨 Example prompt for LLM:")
        print(llm_prompt)
        print("\n" + "="*50 + "\n")
        
        # 3. Example LLM response
        example_response = {
            "message": "You have 3 unread emails and 5 meetings this week.",
            "actions": [
                {
                    "type": "search",
                    "query": "important"
                }
            ]
        }
        
        print("🤖 Example LLM response:")
        print(json.dumps(example_response, indent=2))
        print("\n" + "="*50 + "\n")
        
        # 4. Process response
        print("⚙️  Processing LLM response...")
        results = assistant.process_llm_response(json.dumps(example_response))
        for result in results:
            print(f"  {result}")
        
    except RuntimeError as e:
        print(f"❌ {e}")


if __name__ == "__main__":
    main()
