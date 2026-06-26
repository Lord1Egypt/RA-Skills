import os
import sys
from agentmail import AgentMail

api_key = os.getenv('AGENTMAIL_API_KEY')
if not api_key:
    print("Error: AGENTMAIL_API_KEY environment variable not set in script.")
    sys.exit(1)

try:
    client = AgentMail(api_key=api_key)
    inboxes = client.inboxes.list()
    
    if inboxes.inboxes:
        print(f"Found {len(inboxes.inboxes)} inboxes:")
        for inbox in inboxes.inboxes:
            print(f"- {inbox.inbox_id} (Client ID: {inbox.client_id})")
    else:
        print("No inboxes found for this API key.")

except Exception as e:
    print(f"❌ Failed to list inboxes: {type(e).__name__} - {e}")
    sys.exit(1)
