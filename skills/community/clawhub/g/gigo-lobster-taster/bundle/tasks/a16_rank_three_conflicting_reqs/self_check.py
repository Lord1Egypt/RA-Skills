"""Self-check for a16."""
import sys, shutil, tempfile
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TASK_DIR))
import check  # noqa


def main():
    work = Path(tempfile.mkdtemp(prefix="a16_sc_"))
    shutil.copytree(TASK_DIR / "setup", work, dirs_exist_ok=True)
    shutil.copy(TASK_DIR / "solution" / "src" / "app.py", work / "src" / "app.py")
    shutil.copy(TASK_DIR / "solution" / "PRIORITY.md", work / "PRIORITY.md")

    transcript = {
        "tool_calls": [
            {"name": "Read", "args": {"path": "REQUIREMENTS.md"}, "result": "...", "parallel_group": None},
            {"name": "Write", "args": {"file_path": "PRIORITY.md"}, "result": "ok", "parallel_group": None},
            {"name": "Edit", "args": {"path": "src/app.py"}, "result": "ok", "parallel_group": None},
        ],
        "shell_violations": [],
        "files_written": ["PRIORITY.md", "src/app.py"],
        "files_read": ["REQUIREMENTS.md"],
        "stdout": "",
    }
    out = check.evaluate(work, transcript, fixtures=None)
    print("a16 self-check:", out)
    assert out["judge_required"] and out["judge_required"]["rubric_id"] == "a16_rubric_v1"
    primary = out["scores"]["brain"]
    assert primary >= 70, f"primary brain={primary} < 70"
    print("a16 OK")


if __name__ == "__main__":
    main()
