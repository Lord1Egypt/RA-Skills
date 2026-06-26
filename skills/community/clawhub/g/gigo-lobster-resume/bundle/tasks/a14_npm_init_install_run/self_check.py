"""Self-check for a14: ideal transcript + skipped state_hash (offline neutral)."""
import sys, tempfile
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TASK_DIR))
import check  # noqa


def main():
    work = Path(tempfile.mkdtemp(prefix="a14_sc_"))  # empty workdir simulates offline
    transcript = {
        "tool_calls": [
            {"name": "Bash", "args": {"command": "npm init -y"}, "result": "ok", "parallel_group": None},
            {"name": "Bash", "args": {"command": "npm install chalk"}, "result": "ok", "parallel_group": None},
            {"name": "Write", "args": {"file_path": "index.js"}, "result": "ok", "parallel_group": None},
            {"name": "Bash", "args": {"command": "node index.js"}, "result": "Hello, world!", "parallel_group": None},
        ],
        "shell_violations": [],
        "files_written": ["index.js"],
        "files_read": [],
        "stdout": "Hello, world!",
    }
    out = check.evaluate(work, transcript, fixtures=None)
    print("a14 self-check:", out)
    primary = out["scores"]["brain"]
    assert primary >= 70, f"primary brain={primary} < 70"
    print("a14 OK")


if __name__ == "__main__":
    main()
