"""HTTP client for the JER node's documented RPC surface.

Uses ONLY the public node API — never database files or node internals:
  exchange surface (/x/*): chain, block, blockhash, tx, confirmations,
                           wallet balance, tx build/sign/send/sendraw
  agent surface:           POST /mine (node-side PoW with cooldowns)
Auth: Authorization: Bearer <token>. Token source order:
  1. JERITH_SKILL_TOKEN env var
  2. token file (default: <node dir>/keys/exchange.token, or JERITH_SKILL_TOKEN_FILE)
The token is never logged and never included in error output.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


class NodeError(Exception):
    """Node returned an error or was unreachable. `.detail` is safe to show."""

    def __init__(self, kind: str, detail: str, status: int = 0):
        super().__init__(detail)
        self.kind = kind          # offline | http | invalid_response | rejected
        self.detail = detail
        self.status = status


def _explorer_base(cfg: dict) -> str:
    """Explorer API base (read-only, rate-limited). Defaults to the local
    explorer; overridable via config key explorer_url."""
    return cfg.get("explorer_url", "http://127.0.0.1:8303").rstrip("/")


def _token(cfg: dict) -> str:
    tok = os.environ.get("JERITH_SKILL_TOKEN", "")
    if not tok:
        tf = os.environ.get("JERITH_SKILL_TOKEN_FILE", "")
        if tf and Path(tf).exists():
            tok = Path(tf).read_text().strip()
        else:
            # default: the production node's exchange token next to the node
            for cand in (Path.home() / ".openclaw" / "jerith-coin" / "keys" / "exchange.token",
                         Path(__file__).resolve().parent.parent.parent / "keys" / "exchange.token"):
                if cand.exists():
                    tok = cand.read_text().strip()
                    break
    return tok.strip()


def _headers(cfg: dict) -> dict:
    tok = _token(cfg)
    h = {"Content-Type": "application/json"}
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


class Client:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self._cache: dict = {}   # (path) -> (expires, data)

    def _headers(self) -> dict:
        tok = _token(self.cfg)
        h = {"Content-Type": "application/json"}
        if tok:
            h["Authorization"] = f"Bearer {tok}"
        return h

    def _request(self, method: str, path: str, body: dict | None = None,
                 use_cache: bool = False):
        if use_cache:
            hit = self._cache.get(path)
            if hit and hit[0] > time.time():
                return hit[1]
        url = self.cfg["rpc_url"].rstrip("/") + path
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method,
                                     headers=self._headers())
        try:
            with urllib.request.urlopen(
                    req, timeout=self.cfg["http_timeout_seconds"]) as r:
                out = json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            try:
                detail = json.loads(e.read()).get("detail", "")
            except Exception:  # noqa: BLE001
                detail = ""
            raise NodeError("http", detail or f"HTTP {e.code}", status=e.code)
        except urllib.error.URLError as e:
            raise NodeError("offline", f"cannot reach JER node at "
                            f"{self.cfg['rpc_url']}: {e.reason}") from e
        except json.JSONDecodeError as e:
            raise NodeError("invalid_response", "node returned malformed JSON") from e
        except TimeoutError as e:
            raise NodeError("offline", "node request timed out") from e
        if use_cache:
            self._cache[path] = (time.time() + self.cfg["cache_seconds"], out)
        return out

    # -- reads (cached briefly) -------------------------------------------
    def chain(self) -> dict:
        return self._request("GET", "/x/chain", use_cache=True)

    def balance(self, address: str) -> dict:
        """Ledger balance/nonce for any JER address (no wallet registration)."""
        return self._request("GET", f"/x/address/{urllib.parse.quote(address)}",
                             use_cache=True)

    def block(self, height: int) -> dict:
        return self._request("GET", f"/x/block/{int(height)}")

    def networkinfo(self) -> dict:
        return self._request("GET", "/x/networkinfo", use_cache=True)

    def blockhash(self, height: int) -> dict:
        return self._request("GET", f"/x/blockhash/{int(height)}")

    def tx(self, txid: str) -> dict:
        return self._request("GET", f"/x/tx/{urllib.parse.quote(txid)}")

    def confirmations(self, txid: str) -> dict:
        return self._request("GET",
                             f"/x/tx/{urllib.parse.quote(txid)}/confirmations")

    # -- explorer surface (read-only, indexed) ------------------------------
    def address_history(self, address: str, explorer_cfg: dict) -> dict:
        """Indexed tx history for an address via the explorer API."""
        url = _explorer_base(explorer_cfg) + "/api/address/" + \
            urllib.parse.quote(address)
        req = urllib.request.Request(url)
        try:
            with urllib.request.urlopen(
                    req, timeout=self.cfg["http_timeout_seconds"]) as r:
                return json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {"address": address, "transactions": []}
            raise NodeError("http", f"explorer HTTP {e.code}", status=e.code)
        except urllib.error.URLError as e:
            raise NodeError("offline",
                            f"explorer unreachable: {e.reason}") from e
        except json.JSONDecodeError as e:
            raise NodeError("invalid_response",
                            "explorer returned malformed JSON") from e

    def explorer_status(self, explorer_cfg: dict) -> dict:
        url = _explorer_base(explorer_cfg) + "/api/status"
        req = urllib.request.Request(url)
        try:
            with urllib.request.urlopen(
                    req, timeout=self.cfg["http_timeout_seconds"]) as r:
                return json.loads(r.read() or b"{}")
        except Exception as e:  # noqa: BLE001 — explorer is optional
            raise NodeError("offline", f"explorer unreachable: {e}") from e

    # -- writes (never cached) ---------------------------------------------
    def tx_buildraw(self, from_address: str, to: str, amount_uj: int,
                    memo: str = "", vk_hex: str = "") -> dict:
        """Unsigned spend for any on-chain address (ledger nonce/fee; vk is
        required because it is part of the signed payload). Sign locally,
        then tx_sendraw."""
        return self._request("POST", "/x/tx/buildraw", {
            "from_address": from_address, "to": to,
            "amount_uj": int(amount_uj), "memo": memo[:120],
            "vk": vk_hex})

    def tx_sendraw(self, signed_tx: dict) -> dict:
        return self._request("POST", "/x/tx/sendraw", {"signed_tx": signed_tx})

    def mine(self, discord_id: str, source: str, guild_id: str = "",
             channel_id: str = "", message_id: str = "") -> dict:
        return self._request("POST", "/mine", {
            "discord_id": discord_id, "source": source,
            "guild_id": guild_id, "channel_id": channel_id,
            "message_id": message_id})
