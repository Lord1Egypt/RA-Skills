"""A minimal read-only Nano RPC client (urllib, JSON over HTTP POST).

Only read actions are allowed: this tool never signs, never publishes a block,
and never holds a key. A public node such as rpc.nano.to answers python-urllib's
default User-Agent with 403, so a User-Agent is always sent.
"""
import json
import urllib.error
import urllib.request

DEFAULT_RPC = "https://rpc.nano.to"
USER_AGENT = "nano-invoice/0.1 (+https://github.com/dhyabi2/nano-invoice)"
READ_ACTIONS = frozenset({"account_history", "receivable", "block_info", "blocks_info", "account_info"})


class RpcError(RuntimeError):
    pass


class Rpc:
    def __init__(self, url=DEFAULT_RPC, timeout=20, user_agent=USER_AGENT):
        self.url = url
        self.timeout = timeout
        self.user_agent = user_agent

    def call(self, action, **params):
        if action not in READ_ACTIONS:
            raise RpcError(f"refused: {action!r} is not a read-only action")
        body = {"action": action}
        body.update({k: v for k, v in params.items() if v is not None})
        req = urllib.request.Request(
            self.url,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json", "User-Agent": self.user_agent,
                     "Accept": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            raise RpcError(f"{action}: HTTP {e.code} from {self.url}") from e
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            raise RpcError(f"{action}: {e}") from e
        if isinstance(data, dict) and "error" in data:
            raise RpcError(f"{action}: {data['error']}")
        return data


def as_rpc(rpc):
    """Accept None (default public node), a URL string, or any object with .call()."""
    if rpc is None:
        return Rpc()
    if isinstance(rpc, str):
        return Rpc(rpc)
    if not hasattr(rpc, "call"):
        raise TypeError("rpc must be a URL or an object with a call(action, **params) method")
    return rpc
