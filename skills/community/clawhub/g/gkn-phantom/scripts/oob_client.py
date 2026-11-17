#!/usr/bin/env python3
"""OOB (Out-of-Band) callback channel client — GKN-Phantom v1.0.0.

Real OOB verification for blind vulnerabilities (SSRF / blind injection /
XXE / stored-XSS callbacks). Replaces the static "oob.authorized.test"
placeholder with an actually-pollable channel.

Providers (priority order, auto-detected):
  1. interactsh-client binary in PATH — self-hosted server or oast.fun
  2. ceye.io API (GKN_CEYE_IDENTIFIER + GKN_CEYE_TOKEN env or CLI args)
  3. dnslog.cn session API (explicit selection only — needs outbound net)

Interface:
  client = get_oob_client()                 # None when nothing configured
  domain = client.get_domain("gkn-ssrf")    # unique tagged callback domain
  hits   = client.poll("gkn-ssrf", wait=6) # interactions; [] when none
  state  = client.to_dict()                 # serializable session state
  client.close()

Every method is failure-tolerant: provider errors degrade to "no channel"
(empty domain / empty interactions) instead of raising, so the combat
pipeline can treat OOB as a pure upgrade — never a hard dependency.

Environment variables:
  GKN_OOB_PROVIDER          auto | interactsh | ceye | dnslog | none
  GKN_CEYE_IDENTIFIER       ceye.io identifier
  GKN_CEYE_TOKEN            ceye.io API token
  GKN_INTERACTSH_SERVER     self-hosted interactsh server URL

Usage (CLI self-test):
  python oob_client.py --provider auto --tag gkn-test --wait 5
"""

from __future__ import annotations

import argparse
import json
import os
import queue
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

INTERACTSH_BINARIES = ("interactsh-client", "interactsh")
DEFAULT_CEYE_API = "https://api.ceye.io"
DEFAULT_DNSLOG_API = "http://www.dnslog.cn"
DEFAULT_INTERACTSH_DOMAIN = "oast.fun"


# =============================================================================
# Client implementations
# =============================================================================

class OOBClient:
    """Abstract OOB channel. All methods are failure-tolerant."""

    provider = "base"

    def get_domain(self, tag: str = "gkn") -> str | None:
        """Return a unique tagged callback domain (None on failure)."""
        raise NotImplementedError

    def poll(self, tag: str | None = None, wait: float = 4.0) -> list[dict]:
        """Return interactions seen so far (optionally filtered by tag).

        When `tag` is given, blocks up to `wait` seconds for at least one
        matching interaction. Never raises — returns [] on any failure.
        """
        return []

    def to_dict(self) -> dict:
        """Serializable session state (for manifest persistence)."""
        return {"provider": self.provider}

    def close(self) -> None:
        """Release provider resources (subprocess, session)."""
        pass


class InteractshClient(OOBClient):
    """interactsh-client subprocess in -json streaming mode.

    Domain layout: {tag}.{correlation-id}.{server-domain} — any leftmost
    label routes to the same correlation, so each probe gets a unique,
    matchable subdomain without extra registrations.
    """

    provider = "interactsh"
    _CORR_RE = re.compile(r"correlation[- ]?id[^0-9a-z]*([0-9a-z]{16,})", re.IGNORECASE)

    def __init__(self, binary: str, server: str | None = None,
                 startup_timeout: float = 15.0):
        self._binary = binary
        self._server = server
        self._correlation: str | None = None
        self._queue: queue.Queue = queue.Queue()
        cmd = [binary, "-json", "-silent", "-N", "1"]
        if server:
            cmd += ["-s", server]
        self._proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace",
        )
        self._ready = threading.Event()
        threading.Thread(target=self._read_stderr, daemon=True).start()
        threading.Thread(target=self._read_stdout, daemon=True).start()
        self._ready.wait(max(1.0, startup_timeout))

    def _read_stderr(self) -> None:
        try:
            for line in self._proc.stderr or []:
                m = self._CORR_RE.search(line)
                if m and not self._correlation:
                    self._correlation = m.group(1)
                    self._ready.set()
        except Exception:
            pass
        finally:
            self._ready.set()

    def _read_stdout(self) -> None:
        try:
            for line in self._proc.stdout or []:
                line = line.strip()
                if line:
                    self._queue.put(line)
        except Exception:
            pass

    def _server_host(self) -> str:
        if self._server:
            raw = self._server if "//" in self._server else "https://" + self._server
            host = urllib.parse.urlsplit(raw).netloc or self._server
            return host.split("@")[-1]
        return DEFAULT_INTERACTSH_DOMAIN

    def get_domain(self, tag: str = "gkn") -> str | None:
        if not self._correlation:
            return None
        return f"{tag}.{self._correlation}.{self._server_host()}"

    def poll(self, tag: str | None = None, wait: float = 4.0) -> list[dict]:
        def _drain() -> list[dict]:
            out = []
            while True:
                try:
                    line = self._queue.get_nowait()
                except queue.Empty:
                    return out
                try:
                    obj = json.loads(line)
                except Exception:
                    obj = {"raw": line}
                out.append(obj)

        if tag is None:
            return _drain()
        deadline = time.monotonic() + max(0.5, wait)
        matched: list[dict] = []
        while True:
            for obj in _drain():
                if tag in json.dumps(obj, ensure_ascii=False):
                    matched.append(obj)
            if matched or time.monotonic() >= deadline:
                return matched
            time.sleep(0.4)

    def to_dict(self) -> dict:
        return {
            "provider": self.provider,
            "correlation_id": self._correlation,
            "server": self._server_host(),
            "binary": self._binary,
        }

    def close(self) -> None:
        try:
            self._proc.terminate()
        except Exception:
            pass


class CeyeClient(OOBClient):
    """ceye.io API — needs an identifier + token from ceye.io."""

    provider = "ceye"

    def __init__(self, identifier: str, token: str,
                 api_base: str = DEFAULT_CEYE_API, timeout: float = 8.0):
        self._identifier = identifier
        self._token = token
        self._api = (api_base or DEFAULT_CEYE_API).rstrip("/")
        self._timeout = timeout

    def get_domain(self, tag: str = "gkn") -> str | None:
        return f"{tag}.{self._identifier}.ceye.io"

    def _fetch_records(self) -> list[dict]:
        out: list[dict] = []
        for rtype in ("dns", "http"):
            try:
                qs = urllib.parse.urlencode(
                    {"token": self._token, "type": rtype})
                url = f"{self._api}/v1/records?{qs}"
                req = urllib.request.Request(
                    url, headers={"User-Agent": "GKN-Phantom/5.4 OOB"})
                resp = urllib.request.urlopen(req, timeout=self._timeout)
                data = json.loads(
                    resp.read(262144).decode("utf-8", "replace"))
                out.extend(data.get("data") or [])
            except Exception:
                continue
        return out

    def poll(self, tag: str | None = None, wait: float = 4.0) -> list[dict]:
        if tag is None:
            return self._fetch_records()
        deadline = time.monotonic() + max(0.5, wait)
        matched: list[dict] = []
        while True:
            for r in self._fetch_records():
                if tag in json.dumps(r, ensure_ascii=False):
                    matched.append(r)
            if matched or time.monotonic() >= deadline:
                return matched
            time.sleep(1.0)

    def to_dict(self) -> dict:
        # NOTE: token intentionally NOT serialized — manifests are shared
        return {"provider": self.provider, "identifier": self._identifier}


class DnslogClient(OOBClient):
    """dnslog.cn session API — domain per HTTP session (cookie-bound)."""

    provider = "dnslog"

    def __init__(self, api_base: str = DEFAULT_DNSLOG_API, timeout: float = 8.0):
        import http.cookiejar
        self._api = (api_base or DEFAULT_DNSLOG_API).rstrip("/")
        self._timeout = timeout
        self._domain: str | None = None
        self._opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def get_domain(self, tag: str = "gkn") -> str | None:
        if self._domain is None:
            try:
                req = urllib.request.Request(
                    f"{self._api}/getdomain.php",
                    headers={"User-Agent": "GKN-Phantom/5.4 OOB"})
                resp = self._opener.open(req, timeout=self._timeout)
                dom = resp.read(256).decode("utf-8", "replace").strip()
                if "." in dom:
                    self._domain = dom
            except Exception:
                return None
        if not self._domain:
            return None
        return f"{tag}.{self._domain}"

    def _fetch_records(self) -> list[dict]:
        try:
            req = urllib.request.Request(
                f"{self._api}/getrecords.php",
                headers={"User-Agent": "GKN-Phantom/5.4 OOB"})
            resp = self._opener.open(req, timeout=self._timeout)
            data = json.loads(resp.read(262144).decode("utf-8", "replace"))
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def poll(self, tag: str | None = None, wait: float = 4.0) -> list[dict]:
        if tag is None:
            return self._fetch_records()
        deadline = time.monotonic() + max(0.5, wait)
        matched: list[dict] = []
        while True:
            for r in self._fetch_records():
                if tag in json.dumps(r, ensure_ascii=False):
                    matched.append(r)
            if matched or time.monotonic() >= deadline:
                return matched
            time.sleep(1.0)

    def to_dict(self) -> dict:
        return {"provider": self.provider, "domain": self._domain}


# =============================================================================
# Factory
# =============================================================================

def detect_interactsh() -> str | None:
    """Return the interactsh-client binary path, or None."""
    for name in INTERACTSH_BINARIES:
        path = shutil.which(name)
        if path:
            return path
    return None


def get_oob_client(provider: str = "auto",
                   ceye_identifier: str | None = None,
                   ceye_token: str | None = None,
                   interactsh_server: str | None = None,
                   startup_timeout: float = 15.0) -> OOBClient | None:
    """Build the best available OOB client, or None when nothing is usable.

    Provider resolution:
      - "auto" (default): interactsh binary in PATH, else ceye.io when
        GKN_CEYE_IDENTIFIER + GKN_CEYE_TOKEN are set, else None.
      - Explicit "interactsh" / "ceye" / "dnslog" skip auto-detection.
      - "none"/"off" always returns None.
    """
    provider = (provider or "auto").strip().lower()
    if provider in ("none", "off", "no", "disabled"):
        return None

    if provider == "auto":
        provider = os.environ.get("GKN_OOB_PROVIDER", "auto").strip().lower()
    if provider == "auto":
        if detect_interactsh():
            provider = "interactsh"
        elif os.environ.get("GKN_CEYE_IDENTIFIER") and os.environ.get("GKN_CEYE_TOKEN"):
            provider = "ceye"
        else:
            return None

    if provider == "interactsh":
        binary = detect_interactsh()
        if not binary:
            return None
        try:
            client = InteractshClient(
                binary,
                interactsh_server or os.environ.get("GKN_INTERACTSH_SERVER"),
                startup_timeout=startup_timeout,
            )
            if client.get_domain("probe"):
                return client
            client.close()
            return None
        except Exception:
            return None

    if provider == "ceye":
        identifier = ceye_identifier or os.environ.get("GKN_CEYE_IDENTIFIER")
        token = ceye_token or os.environ.get("GKN_CEYE_TOKEN")
        if not (identifier and token):
            return None
        return CeyeClient(identifier, token)

    if provider == "dnslog":
        return DnslogClient()

    return None


# =============================================================================
# CLI — self-test the channel
# =============================================================================

def main() -> int:
    ap = argparse.ArgumentParser(description="OOB channel client self-test")
    ap.add_argument("--provider", default="auto",
                    choices=["auto", "interactsh", "ceye", "dnslog", "none"])
    ap.add_argument("--ceye-identifier", default=None)
    ap.add_argument("--ceye-token", default=None)
    ap.add_argument("--interactsh-server", default=None)
    ap.add_argument("--tag", default="gkn-selftest")
    ap.add_argument("--wait", type=float, default=5.0)
    args = ap.parse_args()

    client = get_oob_client(
        provider=args.provider,
        ceye_identifier=args.ceye_identifier,
        ceye_token=args.ceye_token,
        interactsh_server=args.interactsh_server,
    )
    if client is None:
        print("[!] No OOB provider available "
              "(install interactsh-client, or set GKN_CEYE_IDENTIFIER/"
              "GKN_CEYE_TOKEN, or pick --provider dnslog)")
        return 1

    domain = client.get_domain(args.tag)
    print(f"[+] provider: {client.provider}")
    print(f"[+] callback domain: {domain}")
    if not domain:
        client.close()
        return 1
    print(f"[+] poll for {args.wait}s (trigger a DNS/HTTP hit to the domain to test)")
    hits = client.poll(args.tag, wait=args.wait)
    print(f"[+] interactions: {json.dumps(hits, ensure_ascii=False)}")
    client.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
