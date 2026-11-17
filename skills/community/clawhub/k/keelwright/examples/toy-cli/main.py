import argparse
import sys


def main():
    p = argparse.ArgumentParser(description="Rename files by a pattern.")
    p.add_argument("--dry-run", action="store_true", help="don't actually rename")
    args = p.parse_args()
    # Toy: list files in cwd. Real loop-coders: keelwright reviews destructive ops (R3).
    import os
    for f in os.listdir("."):
        if f.endswith(".txt"):
            print(("would rename " if args.dry_run else "renamed ") + f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
