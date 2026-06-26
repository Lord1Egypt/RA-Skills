# langchain-local

> Run LangChain AI chains 100% locally using Ollama — no API keys needed.

## What It Does
This OpenClaw skill lets you run LangChain pipelines powered by a local Ollama
model (phi4-mini by default). All inference happens on your machine — private,
offline, and free.

## Modes
| Mode | Use Case | Temperature |
|------|----------|-------------|
| coding | Python, Django, SQL code generation | 0.1 |
| devops | Nginx, Linux, Docker commands | 0.1 |
| chat | General assistant | 0.7 |
| rag | Document-grounded answers | 0.1 |

## Requirements
- macOS or Linux
- Ollama installed: brew install ollama
- Model pulled: ollama pull phi4-mini
- Python 3.9+: pip install langchain langchain-ollama langchain-community

## Quick Test
Run: python3 ~/.openclaw/skills/langchain-local/main.py

## License
MIT
