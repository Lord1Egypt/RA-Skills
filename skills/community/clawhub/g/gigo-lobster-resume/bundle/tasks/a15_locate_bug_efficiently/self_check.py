"""Self-check for a15."""
import sys, shutil, tempfile
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TASK_DIR))
import check  # noqa


def main():
    work = Path(tempfile.mkdtemp(prefix="a15_sc_"))
    shutil.copytree(TASK_DIR / "setup", work, dirs_exist_ok=True)
    shutil.copy(TASK_DIR / "solution" / "src" / "parser.py", work / "src" / "parser.py")

    transcript = {
        "tool_calls": [
            {"name": "Read", "args": {"path": "README.md"}, "result": "...", "parallel_group": None},
            {"name": "Read", "args": {"path": "src/parser.py"}, "result": "...", "parallel_group": None},
            {"name": "Edit", "args": {"path": "src/parser.py"}, "result": "ok", "parallel_group": None},
        ],
        "shell_violations": [],
        "files_written": ["src/parser.py"],
        "files_read": ["README.md", "src/parser.py"],
        "stdout": "",
    }
    out = check.evaluate(work, transcript, fixtures=None)
    print("a15 self-check:", out)
    primary = out["scores"]["brain"]
    assert primary >= 70, f"primary brain={primary} < 70"
    print("a15 OK")


if __name__ == "__main__":
    main()
