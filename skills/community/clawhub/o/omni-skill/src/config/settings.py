import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = BASE_DIR / "src"

# Database & File Paths
DB_PATH = os.environ.get("OMNI_DB_PATH", str(SRC_DIR / "cli" / "omni_registry.db"))
SKILL_MD_PATH = os.environ.get("OMNI_SKILL_MD_PATH", str(BASE_DIR / "SKILL.md"))

# Gateway Server
GATEWAY_HOST = os.environ.get("OMNI_GATEWAY_HOST", "127.0.0.1")
GATEWAY_PORT = int(os.environ.get("OMNI_GATEWAY_PORT", 9999))
GATEWAY_BUFFER_SIZE = int(os.environ.get("OMNI_GATEWAY_BUFFER_SIZE", 65536))

# Dispatcher Engine
CACHE_CAPACITY = int(os.environ.get("OMNI_CACHE_CAPACITY", 100))
WORKER_POOL_SIZE = int(os.environ.get("OMNI_WORKER_POOL_SIZE", 10))

# Security Sandbox
SANDBOX_TIMEOUT_DEFAULT = int(os.environ.get("OMNI_SANDBOX_TIMEOUT", 5))
SCORE_INITIAL = 100
SCORE_PENALTY_URL = 5
SCORE_PENALTY_OS_MODULE = 20
SCORE_PENALTY_EVAL = 15
SCORE_PENALTY_OPEN = 10
SCORE_PENALTY_TIMEOUT = 50
SCORE_PENALTY_NON_ZERO_EXIT = 10

# Metrics & Kernel
CIRCUIT_BREAKER_FAILURE_THRESHOLD = int(os.environ.get("OMNI_CB_FAILURE_THRESHOLD", 5))
CIRCUIT_BREAKER_RECOVERY_TIMEOUT = float(os.environ.get("OMNI_CB_RECOVERY_TIMEOUT", 30.0))
RATE_LIMIT_MAX_REQUESTS = int(os.environ.get("OMNI_RL_MAX_REQUESTS", 100))
RATE_LIMIT_TIME_WINDOW = float(os.environ.get("OMNI_RL_TIME_WINDOW", 1.0))
PLUGIN_TIMEOUT_DEFAULT = float(os.environ.get("OMNI_PLUGIN_TIMEOUT", 5.0))
