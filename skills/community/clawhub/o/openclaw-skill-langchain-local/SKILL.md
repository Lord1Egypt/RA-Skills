# LangChain Local — Offline AI Chains with Ollama

Run LangChain pipelines locally using Ollama and phi4-mini (or any local model).
No API keys, no cloud, fully private and offline.

## Requirements
- Ollama installed and running (`ollama serve`)
- phi4-mini pulled (`ollama pull phi4-mini`)
- Python packages: `pip install langchain langchain-ollama langchain-community`

## Modes
- `coding` — Python/Django code generation (low temperature, precise)
- `devops` — Linux/Nginx/Docker shell commands
- `chat` — General conversation
- `rag` — Document-grounded answers (context-aware)

## Usage Examples
- "Ask langchain-local to write a Django REST API view"
- "Use langchain-local in devops mode to show how to check disk usage"
- "Run langchain-local chat mode: explain what is RAG"
- "Use langchain-local coding mode to write a PostgreSQL backup script"

## Implementation
Execute: python3 ~/.openclaw/skills/langchain-local/main.py

## Parameters
- mode: coding | devops | chat | rag (default: coding)
- query: Your question or instruction

## Author
Manoj — https://github.com/manoj
