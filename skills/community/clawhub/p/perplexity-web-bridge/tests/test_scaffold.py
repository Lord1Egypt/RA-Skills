# tests/test_scaffold.py
from jev_webbridge.driver import WebBridgeDriver


def test_driver_session_and_endpoint_defaults():
    d = WebBridgeDriver(session="unit-test")
    assert d.session == "unit-test"
    assert d.endpoint.endswith("/command")

def test_driver_requires_session():
    import pytest
    with pytest.raises(ValueError):
        WebBridgeDriver(session="")

import json
import pathlib


def test_fixtures_parse_and_have_interactive_nodes():
    for name in ("snap_home.json", "snap_thread.json"):
        data = json.loads((pathlib.Path(__file__).parent / "fixtures" / name).read_text())
        assert "tree" in data and "url" in data
        roles = []
        def walk(n):
            if isinstance(n, list):
                for c in n: walk(c)
                return
            if not isinstance(n, dict): return
            roles.append(n.get("role", ""))  # noqa: B023 -- walk used in-iteration
            for c in n.get("children") or []:
                walk(c)
        walk(data["tree"])
        assert sum(1 for r in roles if r in {"button", "textbox", "link", "combobox"}) >= 6
