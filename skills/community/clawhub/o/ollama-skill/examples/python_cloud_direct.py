import os
from dotenv import load_dotenv
from ollama import Client

load_dotenv()
api_key = os.environ["OLLAMA_API_KEY"]
client = Client(
    host="https://ollama.com",
    headers={"Authorization": f"Bearer {api_key}"},
)

for part in client.chat(
    "gpt-oss:120b",
    messages=[{"role": "user", "content": "Why is the sky blue?"}],
    stream=True,
):
    print(part["message"]["content"], end="", flush=True)
print()
