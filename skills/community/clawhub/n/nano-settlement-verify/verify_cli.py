#!/usr/bin/env python3
"""Command-line front end for nano_settlement_verify.verify: one JSON verdict on stdout.

usage: python3 verify_cli.py BLOCK_HASH EXPECT_RAW ACCOUNT [RPC_URL]
exit 0 settled, 2 not confirmed yet, 3 mismatch or no such block, 4 node unreachable (nothing was checked)
"""
import json
import sys

from nano_settlement_verify import Mismatch, NotFound, verify


def main(argv):
    if len(argv) not in (4, 5):
        print(__doc__.strip(), file=sys.stderr)
        return 64
    block_hash, expect_raw, account = argv[1], int(argv[2]), argv[3]
    rpc_url = argv[4] if len(argv) == 5 else "https://rpc.nano.to"
    try:
        receipt = verify(block_hash=block_hash, expect_raw=expect_raw, account=account, rpc_url=rpc_url)
    except NotFound:
        print(json.dumps({"verdict": "no_such_block"}))
        return 3
    except Mismatch as error:
        print(json.dumps({"verdict": "mismatch", "expected": str(error.expected), "got": str(error.got)}))
        return 3
    except (OSError, ValueError) as error:
        print(json.dumps({"verdict": "node_unreachable", "detail": str(error)[:200]}))
        return 4
    print(receipt.to_json())
    return 0 if receipt.settled else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
