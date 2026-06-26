import threading
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import pytest

from src.client import fetch, FetchError


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *a, **kw):
        pass

    def do_GET(self):
        cnt = self.server.counter
        cnt["n"] += 1
        if cnt["n"] <= cnt["fail_first"]:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"err")
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ok")


def _start_server(fail_first):
    s = HTTPServer(("127.0.0.1", 0), _Handler)
    s.counter = {"n": 0, "fail_first": fail_first}
    t = threading.Thread(target=s.serve_forever, daemon=True)
    t.start()
    return s, f"http://127.0.0.1:{s.server_port}/"


@pytest.fixture
def server_fail_then_ok():
    s, url = _start_server(fail_first=2)
    yield s, url
    s.shutdown()


@pytest.fixture
def server_always_fail():
    s, url = _start_server(fail_first=99)
    yield s, url
    s.shutdown()


@pytest.fixture
def server_ok():
    s, url = _start_server(fail_first=0)
    yield s, url
    s.shutdown()


def test_first_call_ok(server_ok):
    s, url = server_ok
    body = fetch(url, max_retries=3)
    assert body == "ok"


def test_retry_eventually_succeeds(server_fail_then_ok):
    s, url = server_fail_then_ok
    sleeps = []
    body = fetch(url, max_retries=4, base_delay=0.001, sleep=sleeps.append)
    assert body == "ok"
    assert s.counter["n"] == 3  # 2 fails + 1 success


def test_max_retries_then_raise(server_always_fail):
    s, url = server_always_fail
    sleeps = []
    with pytest.raises(FetchError):
        fetch(url, max_retries=2, base_delay=0.001, sleep=sleeps.append)
    # initial attempt + 2 retries = 3 calls
    assert s.counter["n"] == 3


def test_backoff_increases(server_always_fail):
    s, url = server_always_fail
    sleeps = []
    with pytest.raises(FetchError):
        fetch(url, max_retries=3, base_delay=0.01, sleep=sleeps.append)
    # 3 retries -> 3 sleeps
    assert len(sleeps) == 3
    # exponential: each next >= previous * 1.5
    assert sleeps[1] > sleeps[0]
    assert sleeps[2] > sleeps[1]
