import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODO = ROOT / "todo.py"
DATA = ROOT / "todos.json"


def run(*args):
    return subprocess.run(
        [sys.executable, str(TODO), *args],
        cwd=str(ROOT), capture_output=True, text=True, check=False,
    )


def setup_function(_):
    if DATA.exists():
        DATA.unlink()


def test_add():
    r = run("add", "buy milk")
    assert r.returncode == 0
    assert "Added #1" in r.stdout
    assert "buy milk" in r.stdout


def test_list():
    run("add", "task one")
    run("add", "task two")
    r = run("list")
    assert r.returncode == 0
    assert "#1" in r.stdout and "task one" in r.stdout
    assert "#2" in r.stdout and "task two" in r.stdout
    assert "[ ]" in r.stdout


def test_done():
    run("add", "finish report")
    r = run("done", "1")
    assert r.returncode == 0
    assert "Done #1" in r.stdout
    listed = run("list").stdout
    assert "[x]" in listed
    assert "finish report" in listed


def test_delete():
    run("add", "throwaway")
    r = run("delete", "1")
    assert r.returncode == 0
    assert "Deleted #1" in r.stdout
    listed = run("list").stdout
    assert "throwaway" not in listed


def test_persist_across_runs():
    run("add", "persistent item")
    # Independent process — must read back from disk
    r = run("list")
    assert "persistent item" in r.stdout
    # And the json file actually exists
    assert DATA.exists()
    data = json.loads(DATA.read_text())
    assert any("persistent item" in str(x) for x in (data if isinstance(data, list) else data.values()))
