import os
import glob
from datetime import datetime, timedelta
from pathlib import Path

def get_recent_memory_files(days=7):
    """
    Scans the memory/ directory relative to the OpenClaw workspace.
    """
    workspace = os.getenv("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace")
    memory_dir = Path(workspace) / "memory"
    
    if not memory_dir.exists():
        # Fallback to local discovery for development
        memory_dir = Path("./memory")
        if not memory_dir.exists():
            return []

    cutoff = datetime.now() - timedelta(days=days)
    recent_files = []

    for file_path in memory_dir.glob("*.md"):
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        if mtime > cutoff:
            recent_files.append(file_path)
    
    return sorted(recent_files, key=lambda x: x.stat().st_mtime, reverse=True)

if __name__ == "__main__":
    files = get_recent_memory_files()
    print(f"Found {len(files)} files in the last 7 days:")
    for f in files:
        print(f"- {f.name}")
