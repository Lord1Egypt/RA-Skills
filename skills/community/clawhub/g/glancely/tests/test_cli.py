"""Smoke tests for glancely CLI."""

import json
import sys


def test_glancely_version():
    from glancely import __version__

    assert __version__ is not None


def test_glancely_help():
    from glancely.cli import main

    rc = main(["help"])
    assert rc == 0


def test_glancely_list_no_components(tmp_path, monkeypatch):
    """list should return empty when no components exist."""
    monkeypatch.setenv("GLANCE_HOME", str(tmp_path))

    import io

    from glancely.cli import cmd_list

    saved = sys.stdout
    sys.stdout = io.StringIO()
    try:
        rc = cmd_list([])
        output = sys.stdout.getvalue()
        result = json.loads(output)
        assert isinstance(result, list)
        assert rc == 0
    finally:
        sys.stdout = saved
