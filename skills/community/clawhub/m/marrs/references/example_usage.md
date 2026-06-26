# MARRS Example Usage

## Basic Pattern

```python
from save_memory import save_memory

# Save agent memory
save_memory("# Daily Summary\n\nKey insights from today...", 
            collection="agent-memory")
```

## Cron Setup

Add these crons in your system:

- Monitor Agent: every 15 minutes
- Defrag Agent: every hour

## Customization

1. Edit `config.py` to point to your RAG system
2. Extend `monitor_agent.py` and `defrag_agent.py` with your specific logic
3. Modify `save_memory.py` to call your RAG backend's ingest API

This is a starting template. Adapt it to your environment.
