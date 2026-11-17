# Ollama Army quickstart (v0.9.0 local-only)

```bash
ollama pull llama3.2:1b
python scripts/self_check.py
python ollama_army_launcher.py --roles hb-light,draft-simple --model llama3.2:1b
# other terminal:
python queue_task.py --role draft-simple --prompt "Write one encouraging line"
```

Results: `ollama_results/*.result.json`
