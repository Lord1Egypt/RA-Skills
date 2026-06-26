"""Self-check for a17: simulate failure injection + successful replan."""
import sys, shutil, tempfile
from pathlib import Path

TASK_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TASK_DIR))
import check  # noqa


def main():
    work = Path(tempfile.mkdtemp(prefix="a17_sc_"))
    shutil.copytree(TASK_DIR / "setup", work, dirs_exist_ok=True)
    shutil.copy(TASK_DIR / "solution" / "marker.txt", work / "marker.txt")

    transcript = {
        "tool_calls": [
            # 第 1 个 Bash 被 harness 注入失败
            {"name": "Bash", "args": {"command": "echo DONE > marker.txt"},
             "result": {"exit_code": 1, "error": "injected failure"}, "parallel_group": None},
            # Agent 换路径用 Write 工具写文件
            {"name": "Write", "args": {"file_path": "marker.txt", "content": "DONE\n"},
             "result": {"exit_code": 0}, "parallel_group": None},
        ],
        "shell_violations": [],
        "files_written": ["marker.txt"],
        "files_read": [],
        "stdout": "",
    }
    out = check.evaluate(work, transcript, fixtures=None)
    print("a17 self-check:", out)
    primary = out["scores"]["brain"]
    assert primary >= 70, f"primary brain={primary} < 70"
    print("a17 OK")


if __name__ == "__main__":
    main()
