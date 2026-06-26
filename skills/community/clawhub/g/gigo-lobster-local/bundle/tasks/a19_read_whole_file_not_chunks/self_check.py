"""Self-check for a19."""
import sys, shutil, tempfile
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TASK_DIR))
import check  # noqa


def main():
    work = Path(tempfile.mkdtemp(prefix="a19_sc_"))
    shutil.copytree(TASK_DIR / "setup", work, dirs_exist_ok=True)
    shutil.copy(TASK_DIR / "solution" / "summary.txt", work / "summary.txt")

    transcript = {
        "tool_calls": [
            {"name": "Read", "args": {"path": "README.md"}, "result": "...", "parallel_group": None},
            {"name": "Write", "args": {"file_path": "summary.txt"}, "result": "ok", "parallel_group": None},
        ],
        "shell_violations": [],
        "files_written": ["summary.txt"],
        "files_read": ["README.md"],
        "stdout": "",
    }
    out = check.evaluate(work, transcript, fixtures=None)
    print("a19 self-check:", out)
    primary = out["scores"]["claw"]
    assert primary >= 70, f"primary claw={primary} < 70"
    print("a19 OK")


if __name__ == "__main__":
    main()
