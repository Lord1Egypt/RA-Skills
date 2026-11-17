"""The one place in this package that touches the network.

Everything else - address creation, validation, block construction and
signing - runs offline in the caller's process. That separation is the
point: an operator reviewing this install can read this single file to
see every byte that leaves the machine, and `receive-only` mode adds
nothing to it.

`NanoNode` is an interface, not a class to inherit from for its
behaviour. `HttpNanoNode` speaks the standard Nano node RPC over HTTP;
the test-suite substitutes an in-memory fake. No test in this repository
opens a socket.
"""

import json
import urllib.error
import urllib.request

DEFAULT_TIMEOUT = 10.0


class NodeError(Exception):
    """A node was unreachable, or answered something unusable.

    `reason` is the stable machine-readable code from the spec's error
    table. The message NEVER carries the node URL's credentials - only
    its host - because node URLs are routinely of the form
    https://user:key@node.example.
    """

    def __init__(self, reason: str, message: str):
        super().__init__(message)
        self.reason = reason
        self.message = message


class NanoNode:
    """The RPC surface this wallet needs. Five calls, no more."""

    def account_info(self, address: str) -> dict:
        """`{"frontier","balance_raw","representative","block_count","confirmed"}`,
        or `{}` for an account that has never been opened."""
        raise NotImplementedError

    def receivable(self, address: str, count: int) -> list:
        """`[{"hash","amount_raw","source"}]`, newest first, at most `count`."""
        raise NotImplementedError

    def work_generate(self, root_hex: str) -> str:
        raise NotImplementedError

    def process(self, block: dict) -> str:
        """Publish a signed block; return its hash."""
        raise NotImplementedError


def host_of(url: str) -> str:
    """The host of a node URL, with any credentials stripped.

    Used for every message that names the node, so a misconfigured
    `https://user:secret@node/` can never reach a log line or an API
    response.
    """
    try:
        rest = url.split("://", 1)[1] if "://" in url else url
        authority = rest.split("/", 1)[0]
        return authority.rsplit("@", 1)[-1] or "the configured node"
    except Exception:                                   # pragma: no cover - defensive
        return "the configured node"


class HttpNanoNode(NanoNode):
    """A Nano node's JSON-RPC endpoint, over urllib. No dependencies."""

    def __init__(self, url: str, timeout: float = DEFAULT_TIMEOUT, auth_header: str = None):
        if not url:
            raise NodeError("node_not_configured",
                            "no node URL: set NANO_NODE_URL to a Nano RPC endpoint")
        self.url = url
        self.timeout = timeout
        self.auth_header = auth_header

    def _rpc(self, payload: dict) -> dict:
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            self.url, data=body, headers={"Content-Type": "application/json"}
        )
        if self.auth_header:
            request.add_header("Authorization", self.auth_header)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                answer = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise NodeError(
                "node_unreachable",
                "could not reach the Nano node at %s: %s" % (host_of(self.url), exc.reason),
            ) from None
        except (ValueError, OSError) as exc:
            raise NodeError(
                "node_unreachable",
                "the Nano node at %s answered something unusable: %s"
                % (host_of(self.url), exc),
            ) from None
        if isinstance(answer, dict) and "error" in answer:
            raise NodeError("node_error", "the Nano node at %s returned: %s"
                            % (host_of(self.url), answer["error"]))
        return answer

    def account_info(self, address: str) -> dict:
        answer = self._rpc({
            "action": "account_info", "account": address,
            "representative": "true", "include_confirmed": "true",
        })
        if not answer.get("frontier"):
            return {}
        return {
            "frontier": answer["frontier"],
            "balance_raw": int(answer.get("confirmed_balance", answer["balance"])),
            "representative": answer.get("confirmed_representative", answer.get("representative")),
            "block_count": int(answer.get("block_count", 0)),
            "confirmed": answer.get("confirmed_height") is not None,
        }

    def receivable(self, address: str, count: int) -> list:
        answer = self._rpc({
            "action": "receivable", "account": address, "count": str(count),
            "source": "true", "include_only_confirmed": "true",
        })
        blocks = answer.get("blocks") or {}
        if not isinstance(blocks, dict):        # the node answers "" for none
            return []
        out = []
        for block_hash, info in blocks.items():
            if isinstance(info, dict):
                out.append({"hash": block_hash,
                            "amount_raw": int(info["amount"]),
                            "source": info.get("source")})
            else:
                out.append({"hash": block_hash, "amount_raw": int(info), "source": None})
        return out[:count]

    def work_generate(self, root_hex: str) -> str:
        answer = self._rpc({"action": "work_generate", "hash": root_hex})
        work = answer.get("work")
        if not work:
            raise NodeError("work_unavailable",
                            "the node at %s did not return proof-of-work; enable "
                            "work generation on it or set a work peer" % host_of(self.url))
        return work

    def process(self, block: dict) -> str:
        answer = self._rpc({
            "action": "process", "json_block": "true",
            "subtype": block.pop("_subtype"), "block": block,
        })
        block_hash = answer.get("hash")
        if not block_hash:
            raise NodeError("publish_failed",
                            "the node at %s accepted no block" % host_of(self.url))
        return block_hash
