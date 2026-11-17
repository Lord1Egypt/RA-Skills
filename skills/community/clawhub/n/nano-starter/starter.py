#!/usr/bin/env python3
"""Nano starter: a receive-only Nano (XNO) wallet for an agent, in one command, with no node.

usage: python3 starter.py setup       create the wallet once (or show the one that exists); prints the address
       python3 starter.py address     print the address
       python3 starter.py balance     balance and what is waiting to be received
       python3 starter.py receive     pocket what is waiting (does the proof-of-work on this machine)
       python3 starter.py check ADDR  checksum-verify any Nano address before you rely on it

Every command prints one JSON object. The private key is written to a file readable only by you and is
never printed, returned or sent anywhere. This tool cannot send XNO: there is no send command in it.
"""
import hashlib
import json
import multiprocessing
import os
import sys
import urllib.error
import urllib.request

import keystore
import nanonode
import payments

KEY_FILE = os.path.expanduser(os.environ.get("NANO_STARTER_KEY_FILE", "~/.nano-starter/key"))
NODE_URL = os.environ.get("NANO_NODE_URL", "https://rpc.nano.to")
USER_AGENT = "nano-starter-skill/1.0"
RECEIVE_THRESHOLD = 0xFFFFFE0000000000   # what the network asks of a receive or open block
WORKERS = max(1, min(4, (os.cpu_count() or 2)))
BATCH = 200_000


def work_value(nonce: int, root: bytes) -> int:
    digest = hashlib.blake2b(nonce.to_bytes(8, "little") + root, digest_size=8).digest()
    return int.from_bytes(digest, "little")


def _search(args):
    root, start, count = args
    blake2b, threshold = hashlib.blake2b, RECEIVE_THRESHOLD
    for nonce in range(start, start + count):
        digest = blake2b(nonce.to_bytes(8, "little") + root, digest_size=8).digest()
        if int.from_bytes(digest, "little") >= threshold:
            return nonce
    return None


def local_receive_work(root_hex: str) -> str:
    """Proof-of-work for a receive/open block, computed here. About 8 million hashes on average."""
    root = bytes.fromhex(root_hex)
    base = int.from_bytes(os.urandom(7), "little") << 8
    with multiprocessing.Pool(WORKERS) as pool:
        position = 0
        while True:
            jobs = [(root, base + position + i * BATCH, BATCH) for i in range(WORKERS)]
            position += WORKERS * BATCH
            for found in pool.map(_search, jobs):
                if found is not None:
                    return "%016x" % found


class StarterNode(nanonode.HttpNanoNode):
    """A public node for reading and publishing; the work is done locally, because public nodes refuse it."""

    def _rpc(self, payload: dict) -> dict:
        request = urllib.request.Request(
            self.url, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                answer = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise nanonode.NodeError("node_unreachable", "could not reach the Nano node at %s: %s"
                                     % (nanonode.host_of(self.url), exc.reason)) from None
        except (ValueError, OSError) as exc:
            raise nanonode.NodeError("node_unreachable", "the Nano node at %s answered something unusable: %s"
                                     % (nanonode.host_of(self.url), exc)) from None
        if isinstance(answer, dict) and "error" in answer:
            raise nanonode.NodeError("node_error", "the Nano node at %s returned: %s"
                                     % (nanonode.host_of(self.url), answer["error"]))
        return answer

    def account_info(self, address: str) -> dict:
        # A brand-new account does not exist on the ledger until its first receive: the node says
        # "Account not found". That is an empty account, not a failure.
        try:
            return super().account_info(address)
        except nanonode.NodeError as error:
            if "account not found" in error.message.lower():
                return {}
            raise

    def work_generate(self, root_hex: str) -> str:
        return local_receive_work(root_hex)


def _keys():
    store = keystore.KeyStore()
    return store, store.load_file(KEY_FILE)


def main(argv) -> int:
    command = argv[1] if len(argv) > 1 else ""
    try:
        if command == "setup":
            if os.path.exists(KEY_FILE):
                _, address = _keys()
                out = {"address": address, "created": False, "key_file": KEY_FILE}
            else:
                made = payments.create_address(store="file", path=KEY_FILE)
                out = {"address": made["address"], "created": True, "key_file": KEY_FILE,
                       "next": "back up the key file; give the address to whoever pays you; then run: receive"}
        elif command == "address":
            _, address = _keys()
            out = {"address": address}
        elif command == "balance":
            _, address = _keys()
            out = payments.balance(address, StarterNode(NODE_URL, timeout=30))
        elif command == "receive":
            store, address = _keys()
            out = payments.receive(address, StarterNode(NODE_URL, timeout=30), store)
        elif command == "check" and len(argv) > 2:
            out = payments.validate_address(argv[2])
            print(json.dumps(out))
            return 0 if out.get("valid") else 1
        else:
            print(__doc__.strip(), file=sys.stderr)
            return 64
    except payments.ToolError as error:
        print(json.dumps(error.payload()))
        return 3
    except keystore.KeyStoreError as error:
        print(json.dumps({"error": error.reason, "message": error.message,
                          "hint": "run: python3 starter.py setup"}))
        return 3
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
