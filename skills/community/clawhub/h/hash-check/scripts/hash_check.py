import argparse, hashlib, json, os, sys

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def scan(root):
    out = {}
    for r, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(r, f)
            out[os.path.relpath(p, root).replace("\\", "/")] = sha256(p)
    return out

def main():
    ap = argparse.ArgumentParser(description="hash-check · SHA-256 清单生成/校验（零依赖）")
    ap.add_argument("mode", choices=["gen", "check"], help="gen=生成清单 check=校验")
    ap.add_argument("--dir", required=True)
    ap.add_argument("--manifest", default="manifest.sha256")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(a.dir):
        print("目录不存在: %s" % a.dir); sys.exit(2)
    cur = scan(a.dir)
    if a.mode == "gen":
        mpath = os.path.join(a.dir, a.manifest)
        with open(mpath, "w", encoding="utf-8-sig") as f:
            for k in sorted(cur):
                f.write("%s  %s\n" % (cur[k], k))
        print("已生成 %s（%d 个文件）" % (mpath, len(cur)))
        sys.exit(0)
    mpath = os.path.join(a.dir, a.manifest)
    if not os.path.isfile(mpath):
        print("清单不存在: %s（先运行 gen）" % mpath); sys.exit(2)
    base = {}
    for line in open(mpath, encoding="utf-8-sig"):
        if line.strip():
            h, k = line.split(None, 1)
            base[k.strip()] = h
    missing = sorted(set(base) - set(cur))
    added = sorted(set(cur) - set(base))
    changed = sorted(k for k in set(base) & set(cur) if base[k] != cur[k])
    ok = not missing and not changed
    if a.json:
        print(json.dumps({"ok": ok, "checked": len(base), "missing": missing,
                          "added": added, "changed": changed}, ensure_ascii=False, indent=2))
    else:
        print("校验: %d/%d 一致%s" % (len(base) - len(changed), len(base), " ｜ PASS" if ok else " ｜ FAIL"))
        for k in changed:
            print("  [改动] " + k)
        for k in missing:
            print("  [缺失] " + k)
        for k in added:
            print("  [新增] " + k)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
