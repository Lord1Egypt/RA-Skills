import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".test_state.json"


def run(*args: str):
    return subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)


def main():
    result = run("scripts/health_check.py", "--write-state", str(STATE))
    assert result.returncode == 0, result.stderr
    state = json.loads(STATE.read_text())
    assert "models" in state

    result = run(
        "scripts/router.py",
        "--task",
        "Fix Go API auth bug and add fallback",
        "--state-file",
        str(STATE),
    )
    assert result.returncode == 0, result.stderr
    output = json.loads(result.stdout)
    assert output["lead_role"] in {"ministry-coding", "cabinet-planner", "emergency-scribe"}
    print("smoke ok")


if __name__ == "__main__":
    main()
