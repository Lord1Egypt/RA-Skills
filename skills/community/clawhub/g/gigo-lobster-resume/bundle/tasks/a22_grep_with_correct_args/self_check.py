"""Self-check for a22."""
import sys, shutil, tempfile
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TASK_DIR))
import check  # noqa


def main():
    work = Path(tempfile.mkdtemp(prefix="a22_sc_"))
    shutil.copytree(TASK_DIR / "setup", work, dirs_exist_ok=True)
    shutil.copy(TASK_DIR / "solution" / "answer.txt", work / "answer.txt")

    transcript = {
        "tool_calls": [
            {"name": "Grep", "args": {"pattern": "def main", "path": "src/"},
             "result": "src/main.py:1:def main():\nsrc/app.py:1:def main():", "parallel_group": None},
            {"name": "Write", "args": {"file_path": "answer.txt"}, "result": "ok", "parallel_group": None},
        ],
        "shell_violations": [],
        "files_written": ["answer.txt"],
        "files_read": [],
        "stdout": "",
    }
    out = check.evaluate(work, transcript, fixtures=None)
    print("a22 self-check:", out)
    primary = out["scores"]["claw"]
    assert primary >= 70, f"primary claw={primary} < 70"
    print("a22 OK")


if __name__ == "__main__":
    main()
