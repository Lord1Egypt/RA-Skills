"""The certificate authorities this server trusts by default exclude emSign ECC G3.

Every sign-in (msal, via requests) and every Graph call (httpx) checks the
server's certificate against the bundle ``certifi`` ships, unless the user
points ``SSL_CERT_FILE`` / ``REQUESTS_CA_BUNDLE`` elsewhere. certifi before
2026.10.19 bundles ``emSign ECC Root CA - G3``, eight of whose intermediate
CA keys were stolen (GHSA-6q48-6c7w-9gw2): anyone holding one can mint a
certificate for ``login.microsoftonline.com`` that both clients would accept.
2026.10.18 dropped every emSign root; 2026.10.19 restored the three that are
not affected, so the check names the one root, not the vendor.

Nothing else sets a minimum, so an existing install keeps the old bundle
through every upgrade of this package. ``pyproject.toml`` carries the floor
that moves it; these tests check the floor is there and that what the two
clients actually load, under the lock, no longer includes that root.
"""

from __future__ import annotations

import ssl
from pathlib import Path

import httpx
import pytest
import requests.utils

COMPROMISED = "emSign ECC Root CA - G3"


def _subjects(ctx: ssl.SSLContext) -> list[str]:
    names = []
    for cert in ctx.get_ca_certs():
        for rdn in cert.get("subject", ()):
            for key, value in rdn:
                if key == "commonName":
                    names.append(value)
    return names


@pytest.fixture(autouse=True)
def _default_trust(monkeypatch):
    # Measure the default, not whatever this machine overrides it with.
    for var in ("SSL_CERT_FILE", "SSL_CERT_DIR", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE"):
        monkeypatch.delenv(var, raising=False)


def test_graph_calls_do_not_trust_the_compromised_root():
    subjects = _subjects(httpx.create_ssl_context())
    assert subjects, "httpx loaded no CA certificates — the probe is measuring the wrong context"
    bad = [s for s in subjects if s == COMPROMISED]
    assert not bad, (
        f"httpx trusts {bad}: certifi is older than 2026.10.19 (GHSA-6q48-6c7w-9gw2). "
        "Check the certifi floor in pyproject.toml."
    )


def test_sign_in_does_not_trust_the_compromised_root():
    ctx = ssl.create_default_context(cafile=requests.utils.DEFAULT_CA_BUNDLE_PATH)
    subjects = _subjects(ctx)
    assert subjects, "requests' bundle loaded no CA certificates"
    bad = [s for s in subjects if s == COMPROMISED]
    assert not bad, f"requests (msal sign-in) trusts {bad}: GHSA-6q48-6c7w-9gw2"


def test_pyproject_floors_certifi_at_the_fix():
    # Plain text, not tomllib: the suite runs on 3.10, which has no tomllib.
    pyproject = (Path(__file__).parent.parent / "pyproject.toml").read_text()
    assert '"certifi>=2026.10.19"' in pyproject, (
        "certifi must be floored at 2026.10.19 (GHSA-6q48-6c7w-9gw2); "
        "without it an upgrade of this package keeps the old trust bundle"
    )
