"""Self-check for a13: simulate solved workdir + run check.evaluate."""
import sys, shutil, tempfile
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TASK_DIR))

import check  # noqa


def main():
    work = Path(tempfile.mkdtemp(prefix="a13_sc_"))
    # copy setup
    shutil.copytree(TASK_DIR / "setup", work, dirs_exist_ok=True)
    # apply solution
    shutil.copy(TASK_DIR / "solution" / "src" / "calc.py", work / "src" / "calc.py")

    transcript = {
        "tool_calls": [
            {"name": "Read", "args": {"path": "src/calc.py"}, "result": "...", "parallel_group": None},
            {"name": "Edit", "args": {"path": "src/calc.py"}, "result": "ok", "parallel_group": None},
        ],
        "shell_violations": [],
        "files_written": ["src/calc.py"],
        "files_read": ["src/calc.py"],
        "stdout": "",
    }
    out = check.evaluate(work, transcript, fixtures=None)
    print("a13 self-check:", out)
    primary = out["scores"]["brain"]
    assert primary >= 70, f"primary brain={primary} < 70"
    print("a13 OK")


if __name__ == "__main__":
    main()
