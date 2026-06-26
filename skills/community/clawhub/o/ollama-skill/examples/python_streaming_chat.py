import os
from dotenv import load_dotenv
from ollama import Client

load_dotenv()
client = Client(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
model = os.getenv("OLLAMA_MODEL", "qwen3-coder")

for part in client.chat(
    model=model,
    messages=[{"role": "user", "content": "Explain how streaming helps in a coding copilot."}],
    stream=True,
):
    chunk = part.get("message", {}).get("content", "")
    if chunk:
        print(chunk, end="", flush=True)
print()
