#!/usr/bin/env python3
"""Run reviewed Cypher locally with Ladybug 0.21.2; read-only by default."""
import argparse
import json
import sys
from pathlib import Path


def positive_int(value):
    value = int(value)
    if value <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=Path, help="Explicit local database file")
    query = parser.add_mutually_exclusive_group(required=True)
    query.add_argument("-c", "--command", help="Reviewed Cypher statement(s)")
    query.add_argument("-f", "--file", type=Path, help="Local UTF-8 Cypher file")
    params = parser.add_mutually_exclusive_group()
    params.add_argument("--params", help="JSON object of bound query parameters")
    params.add_argument("--params-file", type=Path, help="Local JSON parameter file")
    parser.add_argument("--write", action="store_true", help="Enable authorized database writes")
    parser.add_argument("--create", action="store_true", help="Create a new database; requires --write")
    parser.add_argument("--print-rows", action="store_true", help="Print a bounded result preview")
    parser.add_argument("--max-rows", type=positive_int, default=20, help="Preview rows per statement (default 20)")
    parser.add_argument("--timeout-ms", type=positive_int, default=30000, help="Query timeout in milliseconds (default 30000)")
    parser.add_argument("--buffer-mib", type=positive_int, default=256, help="Database buffer pool in MiB (default 256)")
    args = parser.parse_args()
    if args.create and not args.write:
        parser.error("--create requires --write")
    db_path = args.database.expanduser().absolute()
    if args.create and db_path.exists():
        parser.error("--create refuses an existing path")
    if not args.create and not db_path.is_file():
        parser.error("database file does not exist; creation requires --write --create")
    if not db_path.parent.is_dir():
        parser.error("database parent directory does not exist")

    db = conn = None
    results = []
    try:
        import ladybug as lb
        cypher = args.file.read_text(encoding="utf-8") if args.file else args.command
        if not cypher.strip():
            raise ValueError("Cypher must not be empty")
        raw_params = args.params_file.read_text(encoding="utf-8") if args.params_file else args.params
        parameters = json.loads(raw_params) if raw_params is not None else {}
        if not isinstance(parameters, dict):
            raise ValueError("query parameters must be a JSON object")
        db = lb.Database(db_path, read_only=not args.write, buffer_pool_size=args.buffer_mib * 1024 * 1024)
        conn = lb.Connection(db)
        conn.set_query_timeout(args.timeout_ms)
        result = conn.execute(cypher, parameters=parameters)
        results = result if isinstance(result, list) else [result]
        for i, part in enumerate(results):
            label = f"statement[{i}]" if isinstance(result, list) else "result"
            count = part.get_num_tuples()
            print(f"{label}: {count} row(s)")
            if args.print_rows:
                print("columns:", json.dumps(part.get_column_names()))
                for _ in range(min(count, args.max_rows)):
                    print(json.dumps(part.get_next(), ensure_ascii=False, default=str))
                if count > args.max_rows:
                    print(f"{label}: preview truncated to {args.max_rows} of {count} rows")
        return 0
    except ImportError:
        print("ERROR: use the selected Python environment with ladybug==0.21.2 installed; run check_env.py first.", file=sys.stderr)
        return 1
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    finally:
        for result in results:
            result.close()
        if conn is not None:
            conn.close()
        if db is not None:
            db.close()


if __name__ == "__main__":
    raise SystemExit(main())
