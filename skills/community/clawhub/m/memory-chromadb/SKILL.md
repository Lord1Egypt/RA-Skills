# ChromaDB Memory

ChromaDB long-term memory with Ollama embeddings. Auto-recall injects relevant context before each turn.

## Features

- ChromaDB vector database integration
- Ollama embedding support
- Auto-recall relevant memories
- Configurable collection names

## Config

```json
{
  "chromaUrl": "http://localhost:8100",
  "collectionName": "longterm_memory",
  "ollamaUrl": "http://localhost:11434",
  "embeddingModel": "nomic-embed-text",
  "autoRecall": true,
  "autoRecallResults": 3,
  "minScore": 0.5
}
```
