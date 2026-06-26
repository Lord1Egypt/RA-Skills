import os
from agentmail import AgentMail
from agentmail.inboxes import CreateInboxRequest # Import the request object
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

client = AgentMail(api_key=os.getenv("AGENTMAIL_API_KEY"))

try:
    # Create the request object with the desired parameters
    request = CreateInboxRequest(
        username="hammer",  # Use 'username' within the request object
        client_id="clawhammer" # Use 'client_id' within the request object
    )
    inbox = client.inboxes.create(request=request)
    print(f"Created inbox: {inbox.inbox_id}")
except Exception as e:
    print(f"Error creating inbox: {e}")
