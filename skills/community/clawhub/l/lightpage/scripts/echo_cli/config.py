"""CLI endpoint selection; the official origin is set here before distribution."""

import os
from urllib.parse import urlparse

# Official Echo instance. Explicit overrides and saved custom instances remain supported.
DEFAULT_SERVER = "https://echo.hqdx.store"


def resolve_server(override, config):
    server = override or os.getenv("ECHO_SERVER") or config.get("server") or DEFAULT_SERVER
    if not server:
        raise RuntimeError(
            "This release has no official Echo domain yet; configure ECHO_SERVER once "
            "or use --server for a custom service"
        )
    server = server.rstrip("/")
    parsed = urlparse(server)
    if (
        parsed.scheme != "https"
        or not parsed.netloc
        or parsed.username
        or parsed.path
        or parsed.query
        or parsed.fragment
    ):
        raise RuntimeError("Server must be an HTTPS origin without credentials or path")
    return server
