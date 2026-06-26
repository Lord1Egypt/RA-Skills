import inspect
from agentmail import AgentMail

# Create a dummy client object to access the inboxes method
client = AgentMail(api_key="DUMMY_KEY") # API key doesn't matter for inspection

# Get the signature of the create method
signature = inspect.signature(client.inboxes.create)

print(f"Signature of client.inboxes.create: {signature}")

# Also try to print the docstring
print(f"Docstring for client.inboxes.create:\n{client.inboxes.create.__doc__}")
