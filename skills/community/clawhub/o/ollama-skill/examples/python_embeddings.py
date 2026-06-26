import os
from dotenv import load_dotenv
from ollama import Client

load_dotenv()
client = Client(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
model = os.getenv("OLLAMA_EMBED_MODEL", "embeddinggemma")

resp = client.embed(model=model, input=["semantic retrieval", "agent harness adapter"])
print(f"vectors: {len(resp['embeddings'])}")
print(f"dims: {len(resp['embeddings'][0])}")
