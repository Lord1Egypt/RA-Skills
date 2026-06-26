import os
from dotenv import load_dotenv
from ollama import Client

load_dotenv()
client = Client(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
model = os.getenv("OLLAMA_MODEL", "qwen3-coder")

resp = client.chat(
    model=model,
    messages=[{"role": "user", "content": "Write a Python function that safely parses JSON."}],
)

print(resp["message"]["content"])
