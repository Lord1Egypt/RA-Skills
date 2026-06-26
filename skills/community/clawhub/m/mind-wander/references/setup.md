# Setup & Installation

## Requirements

| Component | Purpose | Required |
|-----------|---------|----------|
| Ollama with Qwen3.5-9B-Q8 | The wander LLM | ✅ |
| FalkorDB | Wander graph (dead ends, sessions) | ✅ |
| Perplexity API key | Web search for the agent | Recommended |
| graph-rag-memory skill | Shared graph, memwatchd | Recommended |

## Install

```bash
bash mind-wander/scripts/install.sh [OPTIONS]

Options:
  --workspace DIR        Path to OpenClaw workspace
  --ollama-url URL       Ollama URL (default: http://172.18.0.1:11436)
  --model-variant q4|q8  Which quantization (default: q8)
  --falkordb-host HOST   FalkorDB host (default: 172.18.0.1)
  --perplexity-key KEY   Perplexity API key
  --dry-run              Show what would happen without doing it
```

The installer:
1. Downloads the Qwen3.5 GGUF from HuggingFace
2. Uploads to Ollama and registers as `qwen3.5-wander-q4` / `qwen3.5-wander-q8`
3. Initialises the wander FalkorDB graph
4. Creates the OpenClaw 30-minute cron job (requires gateway API access)
5. Creates `ON_YOUR_MIND.md` template if not present

## Manual Ollama setup

If you prefer to set up Ollama manually:

```bash
# Download from HuggingFace
pip install huggingface_hub
python3 -c "
from huggingface_hub import hf_hub_download
path = hf_hub_download(
    repo_id='Jackrong/Qwen3.5-9B-Claude-4.6-Opus-Reasoning-Distilled-v2-GGUF',
    filename='Qwen3.5-9B.Q8_0.gguf',
    local_dir='/tmp/qwen35'
)
print('Downloaded to:', path)
"

# Register with Ollama via Python (curl can't handle 9.5GB)
python3 mind-wander/scripts/register_model.py --gguf /tmp/qwen35/Qwen3.5-9B.Q8_0.gguf --variant q8
```

## OpenClaw cron registration

The installer creates the cron job automatically if the OpenClaw gateway is running.
To register manually via the gateway API:

```python
import httpx, json

GATEWAY = "http://localhost:18789"
TOKEN   = "your-gateway-token"

job = {
    "name": "mind-wander Q8 (30min)",
    "schedule": {"kind": "cron", "expr": "*/30 * * * *", "tz": "UTC"},
    "payload": {
        "kind": "agentTurn",
        "message": "Run the mind-wander agent (Q8). Write /tmp/mw.py:\nimport subprocess,sys\nr=subprocess.run([sys.executable,'/path/to/workspace/mind-wander/run.py','--model','q8'],capture_output=True,text=True,timeout=600,cwd='/path/to/workspace')\nprint(r.stdout[-800:])\nThen run it.",
        "timeoutSeconds": 660
    },
    "delivery": {"mode": "none"},
    "sessionTarget": "isolated"
}
resp = httpx.post(f"{GATEWAY}/api/cron/jobs",
    headers={"Authorization": f"Bearer {TOKEN}"},
    json=job)
print(resp.json())
```

## After install

```bash
# Verify everything works
python3 mind-wander/run.py --status

# Run once manually to test
python3 mind-wander/run.py --verbose

# Check the wander graph
python3 -c "
import sys; sys.path.insert(0,'mind-wander')
from wander_graph import get_exploration_stats
print(get_exploration_stats())
"
```

## Upgrading

```bash
clawhub update mind-wander
# Re-run install.sh to pick up any new dependencies
bash mind-wander/scripts/install.sh --skip-download
```
