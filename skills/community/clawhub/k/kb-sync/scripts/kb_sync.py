#!/usr/bin/env python3
"""本地知识库增量同步（dry-run diff）：基于内容哈希计算待新增/更新/删除。"""
import argparse, os, sys, json, hashlib


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def scan(src):
    out = {}
    for dp, _, fs in os.walk(src):
        for f in fs:
            if f.lower().endswith((".md", ".txt", ".markdown", ".json")):
                fp = os.path.join(dp, f)
                rel = os.path.relpath(fp, src)
                out[rel] = file_hash(fp)
    return out


def diff(src, manifest_path, dry_run=True):
    current = scan(src)
    prev = {}
    if os.path.exists(manifest_path):
        try:
            prev = json.load(open(manifest_path, encoding="utf-8"))
        except Exception:
            pass
    adds = [k for k in current if k not in prev]
    updates = [k for k in current if k in prev and current[k] != prev[k]]
    deletes = [k for k in prev if k not in current]
    plan = {"add": adds, "update": updates, "delete": deletes}
    print(f"源目录：{src}")
    print(f"待新增：{len(adds)}  ｜ 待更新：{len(updates)}  ｜ 待删除：{len(deletes)}")
    for k in adds[:10]:
        print(f"  + {k}")
    for k in updates[:10]:
        print(f"  ~ {k}")
    for k in deletes[:10]:
        print(f"  - {k}")
    if not dry_run:
        json.dump(current, open(manifest_path, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        print(f"✅ 已写入 manifest：{manifest_path}")
    else:
        print("（dry-run，未写入 manifest）")
    return plan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["diff"])
    ap.add_argument("--src", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--no-dry-run", dest="dry_run", action="store_false")
    args = ap.parse_args()
    if args.mode == "diff":
        diff(args.src, args.manifest, args.dry_run)


if __name__ == "__main__":
    main()
