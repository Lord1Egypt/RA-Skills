"""Self-check for a23."""
import sys, tempfile
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TASK_DIR))
import check  # noqa


def main():
    work = Path(tempfile.mkdtemp(prefix="a23_sc_"))
    transcript = {
        "tool_calls": [
            {"name": "Bash",
             "args": {"command": "python3 -m http.server 8765", "run_in_background": True},
             "result": "started bg shell xyz", "parallel_group": None},
        ],
        "shell_violations": [],
        "files_written": [],
        "files_read": [],
        "stdout": "",
    }
    out = check.evaluate(work, transcript, fixtures=None)
    print("a23 self-check:", out)
    primary = out["scores"]["claw"]
    assert primary >= 70, f"primary claw={primary} < 70"
    print("a23 OK")


if __name__ == "__main__":
    main()
