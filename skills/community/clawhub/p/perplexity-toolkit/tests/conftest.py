"""Shared fixtures and the FakeDriver test double for perplexity-toolkit."""

import pytest

from perplexity_toolkit.config import Config, get_config, set_config
from perplexity_toolkit.drivers.base import BrowserDriver


class FakeDriver(BrowserDriver):
    """In-memory BrowserDriver implementation.

    Returns configurable mock data and records every call in ``self.calls``
    as a tuple, so tests can assert driver interactions.

    ``evaluate`` resolution order:
      1. if ``evaluate_result`` is callable, call it with the JS code;
      2. if ``evaluate_routes`` is given, return the value of the first key
         that is a substring of the JS code;
      3. otherwise return ``evaluate_result`` verbatim.
    """

    def __init__(self, snapshot_data="", evaluate_result=None, evaluate_routes=None):
        self.snapshot_data = snapshot_data
        self.evaluate_result = evaluate_result
        self.evaluate_routes = evaluate_routes or {}
        self.calls = []
        self.closed = False

    # -- BrowserDriver interface -------------------------------------------

    def navigate(self, url, new_tab=True, group_title=""):
        self.calls.append(("navigate", url, new_tab, group_title))
        return {"ok": True}

    def snapshot(self):
        self.calls.append(("snapshot",))
        return {"data": {"tree": self.snapshot_data}}

    def click(self, selector):
        self.calls.append(("click", selector))
        return {"ok": True}

    def fill(self, selector, value):
        self.calls.append(("fill", selector, value))
        return {"ok": True}

    def evaluate(self, code):
        self.calls.append(("evaluate", code[:100]))
        if callable(self.evaluate_result):
            return self.evaluate_result(code)
        for key, value in self.evaluate_routes.items():
            if key in code:
                return value
        return self.evaluate_result

    def screenshot(self, path=None):
        self.calls.append(("screenshot", path))
        return {"ok": True}

    def close(self):
        self.calls.append(("close",))
        self.closed = True
        return {"ok": True}

    def cdp(self, method, params=None):
        self.calls.append(("cdp", method, params))
        return {"ok": True}

    # -- test helpers -------------------------------------------------------

    def calls_of(self, method):
        """Return the recorded calls for a single method name."""
        return [c for c in self.calls if c[0] == method]


@pytest.fixture
def fake_driver():
    """A fresh FakeDriver with an empty snapshot tree and no mock JS data."""
    return FakeDriver()


@pytest.fixture
def fast_config():
    """Config with every wait zeroed so tests never sleep."""
    return Config(
        page_load_wait=0.0,
        search_wait=0.0,
        deep_research_wait=0.0,
        model_council_wait=0.0,
        step_by_step_wait=0.0,
        mode_switch_wait=0.0,
        action_wait=0.0,
        batch_delay=0.0,
    )


@pytest.fixture
def restore_default_config():
    """Snapshot the global default Config and restore it after the test.

    set_config() mutates the module-level singleton, so tests that call it
    must not leak changes into other tests.
    """
    snapshot = {
        name: getattr(get_config(), name)
        for name in Config.__dataclass_fields__
    }
    yield
    set_config(**snapshot)