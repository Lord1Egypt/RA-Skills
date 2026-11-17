#!/usr/bin/env python3
"""Check the selected interpreter and Ladybug API without opening a user database."""
import argparse
from contextlib import ExitStack
import importlib.metadata
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expect-version", default="0.21.2")
    parser.add_argument("--smoke", action="store_true", help="Verify the native engine with an in-memory RETURN 1 query")
    args = parser.parse_args()
    try:
        import ladybug as lb
        version = importlib.metadata.version("ladybug")
    except (ImportError, importlib.metadata.PackageNotFoundError):
        print("FAIL: this interpreter needs the LadybugDB distribution ladybug==0.21.2; no automatic installation was performed.", file=sys.stderr)
        return 1
    print(f"Python: {sys.executable}")
    print(f"Ladybug: {version}")
    if version != args.expect_version:
        print(f"FAIL: expected {args.expect_version}; verify compatibility before selecting another version.", file=sys.stderr)
        return 1
    checks = [(lb, "Database"), (lb, "Connection"), (lb, "AsyncConnection"),
              (getattr(lb, "Connection", None), "set_query_timeout"),
              (getattr(lb, "Connection", None), "close"),
              (getattr(lb, "QueryResult", None), "get_num_tuples"),
              (getattr(lb, "QueryResult", None), "get_next")]
    missing = [name for owner, name in checks if not callable(getattr(owner, name, None))]
    if missing:
        print("FAIL: missing API: " + ", ".join(missing), file=sys.stderr)
        return 1
    if args.smoke:
        try:
            with ExitStack() as stack:
                db = lb.Database(":memory:", buffer_pool_size=256 * 1024 * 1024)
                stack.callback(db.close)
                conn = lb.Connection(db)
                stack.callback(conn.close)
                conn.set_query_timeout(5000)
                result = conn.execute("RETURN 1")
                stack.callback(result.close)
                if result.get_next() != [1]:
                    raise RuntimeError("unexpected smoke-query result")
        except (ImportError, OSError, ValueError, RuntimeError) as exc:
            print(f"FAIL: native engine unavailable: {exc}", file=sys.stderr)
            return 1
        print("OK: native engine query passed in memory; no user database was opened.")
    else:
        print("OK: Python API checks passed; native execution is untested. Use --smoke to check it in memory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
