"""
Web Dashboard Utilities
"""

import json
import os
import subprocess
from typing import Dict, Any

from .config import SKILL_DIR, FOOD_STORAGE_DEFAULTS


def run_script(user: str, script_name: str, *args) -> Dict[str, Any]:
    """Run a skill script and return parsed JSON."""
    script_path = os.path.join(SKILL_DIR, 'scripts', script_name)
    cmd = ['python3', script_path, '--user', user] + list(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {"status": "error", "error": result.stderr}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def get_default_storage(food_name: str) -> str:
    """Get default storage location for food."""
    for key, value in FOOD_STORAGE_DEFAULTS.items():
        if key in food_name:
            return value
    return '冰箱'
