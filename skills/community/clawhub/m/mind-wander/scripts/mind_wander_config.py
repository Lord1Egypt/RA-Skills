"""
mind-wander configuration.
Edit this file to tune the agent's behaviour.
"""
import os
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/home/node/.openclaw/workspace"))

# ── Model endpoints ───────────────────────────────────────────────────────────
WANDER_MODEL_Q4  = "qwen3.5-wander-q4"   # registered in Ollama after pull
WANDER_MODEL_Q8  = "qwen3.5-wander-q8"
WANDER_MODEL     = os.environ.get("WANDER_MODEL", WANDER_MODEL_Q4)
WANDER_OLLAMA    = os.environ.get("WANDER_OLLAMA", "http://172.18.0.1:11436")
WANDER_CTX       = int(os.environ.get("WANDER_CTX", "16384"))   # context window
WANDER_TIMEOUT   = int(os.environ.get("WANDER_TIMEOUT", "120")) # seconds per LLM call

# ── Memory / graph ────────────────────────────────────────────────────────────
MEM_DIR        = WORKSPACE / "memory-upgrade"
FALKORDB_HOST  = os.environ.get("FALKORDB_HOST", "172.18.0.1")
FALKORDB_PORT  = int(os.environ.get("FALKORDB_PORT", "6379"))
GRAPH_NAME     = "workspace"
GRAPH_LIMIT    = 8   # max facts to inject as context per query

# ── Perplexity (web search) ───────────────────────────────────────────────────
PERPLEXITY_KEY = os.environ.get("PERPLEXITY_API_KEY", "")
# Falls back to reading from openclaw.json if not set

# ── Sandbox ───────────────────────────────────────────────────────────────────
SANDBOX_TIMEOUT   = 30         # seconds
SANDBOX_MAX_LINES = 50         # max lines of code per run
SANDBOX_MEMORY_MB = 256        # soft memory limit
SANDBOX_ALLOWED_IMPORTS = {
    "math", "statistics", "itertools", "functools", "collections",
    "re", "json", "hashlib", "base64", "datetime", "time",
    "numpy", "scipy",  # if available
}

# ── Files ─────────────────────────────────────────────────────────────────────
ON_YOUR_MIND_FILE      = WORKSPACE / "ON_YOUR_MIND.md"
MENTAL_EXPLORATION_FILE = WORKSPACE / "MENTAL_EXPLORATION.md"
WANDER_LOG_FILE        = WORKSPACE / "mind-wander" / "wander.log"
WANDER_STATE_FILE      = WORKSPACE / "mind-wander" / "state.json"

# ── Agent behaviour ───────────────────────────────────────────────────────────
MAX_TOOL_CALLS   = 20     # increased from 12 for research synthesis tasks
MIN_NOVELTY_SCORE = 0.6   # 0-1; below this, elevate() is blocked
FOCUS_ONE_THREAD = True   # agent must pick ONE question and stay on it
COOLDOWN_HOURS   = 3      # min hours between runs on same ON_YOUR_MIND item
