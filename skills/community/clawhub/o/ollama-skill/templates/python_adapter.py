import os
from typing import Any
from ollama import Client


class OllamaAdapter:
    def __init__(self) -> None:
        self.client = Client(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
        self.model = os.getenv("OLLAMA_MODEL", "qwen3-coder")
        self.embed_model = os.getenv("OLLAMA_EMBED_MODEL", "embeddinggemma")

    def send_chat(self, messages: list[dict[str, Any]], stream: bool = False):
        return self.client.chat(model=self.model, messages=messages, stream=stream)

    def embed_texts(self, texts: list[str]):
        return self.client.embed(model=self.embed_model, input=texts)
