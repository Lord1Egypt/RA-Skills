import argparse
import json
import sys

from memory_manager import MemoryManager


def _parser():
    p = argparse.ArgumentParser(prog="memory-core")
    sp = p.add_subparsers(dest="cmd")

    i = sp.add_parser("ingest")
    i.add_argument("--agent", required=True)
    i.add_argument("--text", required=True)

    r = sp.add_parser("retrieve")
    r.add_argument("--agent", required=True)
    r.add_argument("--query", required=True)
    r.add_argument("--scene", default="")

    f = sp.add_parser("forget")
    f.add_argument("--id", required=True)

    return p


def main(argv=None):
    args = _parser().parse_args(argv)
    mm = MemoryManager()

    if args.cmd == "ingest":
        out = mm.ingest(args.agent, args.text)
        print(json.dumps(out, ensure_ascii=False))
        return 0

    if args.cmd == "retrieve":
        out = mm.retrieve(args.agent, args.query, args.scene)
        print(json.dumps(out, ensure_ascii=False))
        return 0

    if args.cmd == "forget":
        out = mm.forget(args.id)
        print(json.dumps(out, ensure_ascii=False))
        return 0

    _parser().print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

