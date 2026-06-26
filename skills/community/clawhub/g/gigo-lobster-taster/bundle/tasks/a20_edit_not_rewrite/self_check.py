"""Self-check for a20."""
import sys, shutil, tempfile
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TASK_DIR))
import check  # noqa


def main():
    work = Path(tempfile.mkdtemp(prefix="a20_sc_"))
    shutil.copytree(TASK_DIR / "setup", work, dirs_exist_ok=True)
    shutil.copy(TASK_DIR / "solution" / "config.yaml", work / "config.yaml")

    transcript = {
        "tool_calls": [
            {"name": "Read", "args": {"path": "config.yaml"}, "result": "...", "parallel_group": None},
            {"name": "Edit", "args": {"path": "config.yaml", "old_string": "port: 8080", "new_string": "port: 9090"},
             "result": "ok", "parallel_group": None},
        ],
        "shell_violations": [],
        "files_written": ["config.yaml"],
        "files_read": ["config.yaml"],
        "stdout": "",
    }
    out = check.evaluate(work, transcript, fixtures=None)
    print("a20 self-check:", out)
    primary = out["scores"]["claw"]
    assert primary >= 70, f"primary claw={primary} < 70"
    print("a20 OK")


if __name__ == "__main__":
    main()
