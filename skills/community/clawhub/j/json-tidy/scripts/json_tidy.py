import argparse, json, sys

def main():
    ap = argparse.ArgumentParser(description="json-tidy · JSON 格式化/压缩/校验（零依赖）")
    ap.add_argument("--file", help="JSON 文件路径（缺省读 stdin）")
    ap.add_argument("--minify", action="store_true", help="压缩为单行")
    ap.add_argument("--sort", action="store_true", help="键排序")
    ap.add_argument("--out", help="写出文件（缺省打印）")
    a = ap.parse_args()
    raw = open(a.file, encoding="utf-8-sig").read() if a.file else sys.stdin.read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        lines = raw.splitlines()
        line = lines[e.lineno - 1] if e.lineno - 1 < len(lines) else ""
        col = max(0, e.colno - 1)
        print("JSON 解析失败: 第%d行第%d列 %s" % (e.lineno, e.colno, e.msg))
        print("  " + line[:col] + "[HERE]" + line[col:col + 30])
        sys.exit(1)
    out = json.dumps(data, ensure_ascii=False,
                     indent=None if a.minify else 2,
                     separators=(",", ":") if a.minify else None,
                     sort_keys=a.sort)
    if a.out:
        open(a.out, "w", encoding="utf-8-sig").write(out)
        print("已写出 %s（%d bytes）" % (a.out, len(out)))
    else:
        print(out)
    sys.exit(0)

if __name__ == "__main__":
    main()
