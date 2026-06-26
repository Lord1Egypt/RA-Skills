#!/usr/bin/env python3
"""hashcheck — File hash calculator and verifier. Zero dependencies."""
import hashlib, sys, argparse, os, json

ALGOS = ["md5", "sha1", "sha256", "sha512", "blake2b"]

def hash_file(path, algo="sha256", chunk_size=65536):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def hash_string(text, algo="sha256"):
    return hashlib.new(algo, text.encode()).hexdigest()

def human_size(n):
    for u in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.1f}{u}"
        n /= 1024
    return f"{n:.1f}TB"

def cmd_hash(args):
    algo = args.algo
    results = []
    for path in args.files:
        if not os.path.exists(path):
            print(f"❌ {path}: not found", file=sys.stderr)
            continue
        digest = hash_file(path, algo)
        size = os.path.getsize(path)
        r = {"file": path, "algo": algo, "hash": digest, "size": size}
        results.append(r)
        if not args.json:
            print(f"{digest}  {path} ({human_size(size)})")
    if args.json:
        print(json.dumps(results, indent=2))

def cmd_verify(args):
    expected = args.expected.lower().strip()
    digest = hash_file(args.file, args.algo)
    if digest == expected:
        print(f"✅ Match! {args.file} ({args.algo})")
    else:
        print(f"❌ Mismatch!")
        print(f"   Expected: {expected}")
        print(f"   Got:      {digest}")
        sys.exit(1)

def cmd_compare(args):
    h1 = hash_file(args.file1, args.algo)
    h2 = hash_file(args.file2, args.algo)
    if h1 == h2:
        print(f"✅ Files are identical ({args.algo}: {h1[:16]}...)")
    else:
        print(f"❌ Files differ")
        print(f"   {args.file1}: {h1}")
        print(f"   {args.file2}: {h2}")
        sys.exit(1)

def cmd_text(args):
    digest = hash_string(args.text, args.algo)
    print(f"{digest}  \"{args.text[:50]}{'...' if len(args.text)>50 else ''}\"")

def cmd_all(args):
    for path in args.files:
        if not os.path.exists(path):
            continue
        print(f"\n📄 {path} ({human_size(os.path.getsize(path))})")
        for algo in ALGOS:
            print(f"  {algo:>8}: {hash_file(path, algo)}")

def main():
    p = argparse.ArgumentParser(prog="hashcheck", description="File hash calculator and verifier")
    sub = p.add_subparsers(dest="cmd")

    h = sub.add_parser("hash", help="Calculate file hash")
    h.add_argument("files", nargs="+")
    h.add_argument("-a", "--algo", default="sha256", choices=ALGOS)
    h.add_argument("--json", action="store_true")

    v = sub.add_parser("verify", help="Verify file against expected hash")
    v.add_argument("file")
    v.add_argument("expected", help="Expected hash value")
    v.add_argument("-a", "--algo", default="sha256", choices=ALGOS)

    c = sub.add_parser("compare", help="Compare two files")
    c.add_argument("file1")
    c.add_argument("file2")
    c.add_argument("-a", "--algo", default="sha256", choices=ALGOS)

    t = sub.add_parser("text", help="Hash a text string")
    t.add_argument("text")
    t.add_argument("-a", "--algo", default="sha256", choices=ALGOS)

    a = sub.add_parser("all", help="Show all hash algorithms")
    a.add_argument("files", nargs="+")

    args = p.parse_args()
    cmds = {"hash": cmd_hash, "verify": cmd_verify, "compare": cmd_compare, "text": cmd_text, "all": cmd_all}
    if args.cmd in cmds:
        cmds[args.cmd](args)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
