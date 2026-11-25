import re, os, sys, argparse
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_here = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_OUT = os.path.normpath(os.path.join(_here, "..", "..", "output", "full-react-expert"))
_ap = argparse.ArgumentParser(description="react kb 引用完整性审计（LAW/MO/NE/NX/RA/RC/TQ/TE/VT）")
_ap.add_argument("out_dir", nargs="?", default=_DEFAULT_OUT,
                 help="产物目录（默认 <repo>/output/full-react-expert）")
_args = _ap.parse_args()

out = os.path.abspath(_args.out_dir)
root = os.path.normpath(os.path.join(out, "..", ".."))
kb = os.path.join(out, "kb")
if not os.path.isdir(kb):
    print(f"[ERROR] kb 目录不存在: {kb}")
    sys.exit(2)
print(f"== 审计目标: {out} ==")

files = {"SKILL.md": os.path.join(out, "SKILL.md")}
for fn in sorted(os.listdir(kb)):
    if fn.endswith(".md"):
        files[fn] = os.path.join(kb, fn)

texts = {}
for k, p in files.items():
    with open(p, encoding="utf-8") as f:
        texts[k] = f.read()

defs = {}
def add(kind, num):
    defs.setdefault(kind, set()).add(int(num))

# laws.md 定义为 **LAW-N**；子领域 kb 定义为行首 [KIND-N]
law_text = texts["laws.md"]
for m in re.finditer(r"\*\*LAW-(\d+)\*\*", law_text):
    add("LAW", m.group(1))

kinds = {"monorepo.md": "MO", "nestjs.md": "NE", "nextjs.md": "NX",
         "react-admin.md": "RA", "react-core.md": "RC", "tanstack-query.md": "TQ",
         "testing.md": "TE", "vite-tooling.md": "VT"}
for fn, kind in kinds.items():
    for m in re.finditer(r"^\[%s-(\d+)\]" % kind, texts[fn], re.M):
        add(kind, m.group(1))

order = ["LAW", "MO", "NE", "NX", "RA", "RC", "TQ", "TE", "VT"]
print("== DEFINITIONS ==")
for kind in order:
    s = sorted(defs.get(kind, set()))
    missing = [i for i in range(1, (max(s) if s else 0) + 1) if i not in s]
    print(f"{kind}: n={len(s)} max={max(s) if s else 0} 定义缺口={missing if missing else '无'}")

print("\n== BROKEN REFS (引用了未定义编号) ==")
refpat = re.compile(r"\b(LAW|MO|NE|NX|RA|RC|TQ|TE|VT)-(\d+)\b")
broken = 0
for fn, text in texts.items():
    for lineno, line in enumerate(text.splitlines(), 1):
        for m in refpat.finditer(line):
            kind, n = m.group(1), int(m.group(2))
            if n not in defs.get(kind, set()):
                broken += 1
                print(f"  {fn}:{lineno}: [{kind}-{n}] -> 未定义  | {line.strip()[:70]}")
print(f"  共 {broken} 处")

print("\n== corpus 路径存在性 (跳过字面省略号) ==")
bad = 0
for fn, text in texts.items():
    for p in set(re.findall(r"corpus/[\w\-./~]+", text)):
        p2 = p.rstrip(".")
        if "~" in p2 or "..." in p2:
            continue
        full = os.path.join(root, p2.replace("/", os.sep))
        if not os.path.exists(full):
            bad += 1
            print(f"  {fn}: 不存在 -> {p2}")
print(f"  共 {bad} 处不存在")

print("\n== kb 文件引用存在性 ==")
badkb = 0
for fn, text in texts.items():
    for p in set(re.findall(r"kb/[\w\-]+\.md", text)):
        full = os.path.join(out, p.replace("/", os.sep))
        if not os.path.exists(full):
            badkb += 1
            print(f"  {fn}: 不存在 -> {p}")
print(f"  共 {badkb} 处不存在")

print("\n== 定义但零引用 (孤儿条款) ==")
any_orphan = False
for kind in order:
    refnums = set()
    for fn, text in texts.items():
        for m in re.finditer(r"\b%s-(\d+)\b" % kind, text):
            refnums.add(int(m.group(1)))
    orphan = sorted(defs.get(kind, set()) - refnums)
    if orphan:
        any_orphan = True
        print(f"  {kind}: {orphan}")
if not any_orphan:
    print("  无")
