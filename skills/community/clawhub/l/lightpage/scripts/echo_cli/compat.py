"""Small standard-library bridges for Python 3.6 through 3.12."""

from datetime import datetime, timezone
from http.server import HTTPServer
from socketserver import ThreadingMixIn

UTC = timezone.utc


def parse_datetime(value):
    # Server timestamps use ISO 8601 with UTC or a numeric timezone offset.
    if value.endswith("Z"):
        value = value[:-1] + "+0000"
    elif len(value) >= 6 and value[-3] == ":" and value[-6] in "+-":
        value = value[:-3] + value[-2:]
    pattern = "%Y-%m-%dT%H:%M:%S"
    if "." in value:
        pattern += ".%f"
    if value[-5:-4] in ("+", "-"):
        pattern += "%z"
    return datetime.strptime(value, pattern)


def unlink(path):
    try:
        path.unlink()
    except FileNotFoundError:
        pass


def subparsers(parser, **kwargs):
    commands = parser.add_subparsers(**kwargs)
    commands.required = True
    return commands


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
