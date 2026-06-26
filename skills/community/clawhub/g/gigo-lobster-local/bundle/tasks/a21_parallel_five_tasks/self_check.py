"""Self-check for a21."""
import sys, shutil, tempfile
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TASK_DIR))
import check  # noqa


def main():
    work = Path(tempfile.mkdtemp(prefix="a21_sc_"))
    shutil.copytree(TASK_DIR / "setup", work, dirs_exist_ok=True)
    shutil.copy(TASK_DIR / "solution" / "report.md", work / "report.md")

    transcript = {
        "tool_calls": [
            {"name": "Read", "args": {"path": "file_a.txt"}, "result": "...", "parallel_group": "g1"},
            {"name": "Read", "args": {"path": "file_b.txt"}, "result": "...", "parallel_group": "g1"},
            {"name": "Read", "args": {"path": "file_c.txt"}, "result": "...", "parallel_group": "g1"},
            {"name": "Read", "args": {"path": "file_d.txt"}, "result": "...", "parallel_group": "g1"},
            {"name": "Read", "args": {"path": "file_e.txt"}, "result": "...", "parallel_group": "g1"},
            {"name": "Write", "args": {"file_path": "report.md"}, "result": "ok", "parallel_group": None},
        ],
        "shell_violations": [],
        "files_written": ["report.md"],
        "files_read": ["file_a.txt", "file_b.txt", "file_c.txt", "file_d.txt", "file_e.txt"],
        "stdout": "",
    }
    out = check.evaluate(work, transcript, fixtures=None)
    print("a21 self-check:", out)
    primary = out["scores"]["claw"]
    assert primary >= 70, f"primary claw={primary} < 70"
    print("a21 OK")


if __name__ == "__main__":
    main()
