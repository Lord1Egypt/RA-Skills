"""
test_school_roster.py — Unit tests for get_school_roster().

The school email runner classifies each email to a child using teacher names
and classroom sender addresses. Those are real names and addresses, so they
live in config.json and reach the runner only through this tool — never copied
into its tracked prompt files. (Naming the runner's path here would trip the
boundary grep in ../../../CLAUDE.md, which greps *.py for it; a check that
cries wolf gets ignored, so the path stays out of the .py files.)

Covers:
  - the shape the runner parses: {"school", "kids":[{name, teachers, email_sender}]}
  - configs predating the `teachers` / `email_sender` fields still load
"""
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))


def test_roster_has_the_shape_the_runner_parses(monkeypatch):
    import core.config_loader as config_loader
    from core.config_loader import Kid
    from tools import get_school_roster

    # Stub the loaded config rather than reading the real one: this file is
    # tracked, and the real roster is the family's actual teachers and
    # classroom addresses (principle 9).
    stub = MagicMock()
    stub.school_name = "Test School"
    stub.kids = [
        Kid({"name": "Kid A", "teachers": ["Teacher One"],
             "email_sender": "one@example.com"}),
        Kid({"name": "Kid B", "teachers": ["Teacher Two", "Teacher Three"],
             "email_sender": "two@example.com"}),
    ]
    monkeypatch.setattr(config_loader, "config", stub)

    doc = json.loads(get_school_roster())

    assert doc["school"] == "Test School"
    assert [k["name"] for k in doc["kids"]] == ["Kid A", "Kid B"]
    for kid in doc["kids"]:
        assert set(kid) == {"name", "teachers", "email_sender"}
        assert isinstance(kid["teachers"], list)
        assert isinstance(kid["email_sender"], str)
    assert doc["kids"][1]["teachers"] == ["Teacher Two", "Teacher Three"]


def test_kid_without_school_fields_still_loads():
    """
    `teachers` and `email_sender` were added on 2026-08-17. A kid entry written
    before that must not raise — attribution just falls back to whatever other
    signal the email carries.
    """
    from core.config_loader import Kid

    kid = Kid({"name": "Kid A"})

    assert kid.teachers == []
    assert kid.email_sender == ""


def test_teachers_and_sender_round_trip():
    from core.config_loader import Kid

    kid = Kid({
        "name": "Kid A",
        "teachers": ["Teacher One", "Teacher Two"],
        "email_sender": "teacher.one@example.com",
    })

    assert kid.teachers == ["Teacher One", "Teacher Two"]
    assert kid.email_sender == "teacher.one@example.com"
