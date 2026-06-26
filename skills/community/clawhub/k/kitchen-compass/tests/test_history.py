import json


def _events(data_root):
    path = data_root / "history" / "events.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def test_duplicate_default_skips(data_root_indexed, run_cmd):
    run_cmd("record_meal_history.py", "--data-root", str(data_root_indexed),
            "--event-type", "made", "--recipe", "simple-beef-dinner",
            "--date", "2026-04-20")
    assert len(_events(data_root_indexed)) == 1

    result = run_cmd("record_meal_history.py", "--data-root", str(data_root_indexed),
                     "--event-type", "made", "--recipe", "simple-beef-dinner",
                     "--date", "2026-04-20")
    assert "duplicate history event" in result.stderr
    assert len(_events(data_root_indexed)) == 1


def test_allow_duplicate_writes_anyway(data_root_indexed, run_cmd):
    run_cmd("record_meal_history.py", "--data-root", str(data_root_indexed),
            "--event-type", "made", "--recipe", "simple-beef-dinner",
            "--date", "2026-04-20")
    run_cmd("record_meal_history.py", "--data-root", str(data_root_indexed),
            "--event-type", "made", "--recipe", "simple-beef-dinner",
            "--date", "2026-04-20", "--allow-duplicate")
    assert len(_events(data_root_indexed)) == 2


def test_replace_rewrites_in_place(data_root_indexed, run_cmd):
    run_cmd("record_meal_history.py", "--data-root", str(data_root_indexed),
            "--event-type", "made", "--recipe", "simple-beef-dinner",
            "--date", "2026-04-20", "--notes", "original")
    run_cmd("record_meal_history.py", "--data-root", str(data_root_indexed),
            "--event-type", "made", "--recipe", "simple-beef-dinner",
            "--date", "2026-04-20", "--notes", "updated", "--replace")
    events = _events(data_root_indexed)
    assert len(events) == 1
    assert events[0]["notes"] == "updated"
