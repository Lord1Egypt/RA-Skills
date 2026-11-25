import re, os, sys, argparse
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_here = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_OUT = os.path.normpath(os.path.join(_here, "..", "..", "output", "ai-docgen-expert"))
_ap = argparse.ArgumentParser(description="ai-docgen kb 引用完整性审计（LAW/G/P/DT/AD/CC/AC/AW/AV/DG/DQ/PT/PJ）")
_ap.add_argument("out_dir", nargs="?", default=_DEFAULT_OUT,
                 help="产物目录（默认 <repo>/output/ai-docgen-expert）")
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

# laws.md 定义为行首 [LAW-N]
for m in re.finditer(r"^\[LAW-(\d+)\]", texts["laws.md"], re.M):
    add("LAW", m.group(1))

# gotchas.md 定义为标题 [G-N]（### [G-N] ...）
for m in re.finditer(r"^#{1,6}\s*\[G-(\d+)\]", texts["gotchas.md"], re.M):
    add("G", m.group(1))

# patterns.md 定义为二级标题 P-N
for m in re.finditer(r"^## P-(\d+) ", texts["patterns.md"], re.M):
    add("P", m.group(1))

# 子领域 kb 定义行式五变体兼容：<DT-N> / **AD-N** / **AC-N 标题** / **AW-N [GLOBAL]...** / [PT-N] / [PJ-N]
kinds = {"doc-taxonomy.md": "DT", "api-doc-gen.md": "AD", "code-comment.md": "CC",
         "adr-changelog.md": "AC", "ai-docgen-workflow.md": "AW", "ai-doc-verification.md": "AV",
         "doc-governance.md": "DG", "doc-quality.md": "DQ", "doc-templates.md": "PT",
         "proj-docs.md": "PJ"}
for fn, kind in kinds.items():
    if fn not in texts:
        print(f"  [WARN] kb/{fn} 尚未生成，跳过 {kind} 扫描")
        continue
    for m in re.finditer(r"^(?:<|\*\*|\[)?%s-(\d+)" % kind, texts[fn], re.M):
        add(kind, m.group(1))

order = ["LAW", "G", "P", "DT", "AD", "CC", "AC", "AW", "AV", "DG", "DQ", "PT", "PJ"]
print("== DEFINITIONS ==")
for kind in order:
    s = sorted(defs.get(kind, set()))
    missing = [i for i in range(1, (max(s) if s else 0) + 1) if i not in s]
    print(f"{kind}: n={len(s)} max={max(s) if s else 0} 定义缺口={missing if missing else '无'}")

print("\n== BROKEN REFS (引用了未定义编号) ==")
refpat = re.compile(r"\b(LAW|DT|AD|CC|AC|AW|AV|DG|DQ|PT|PJ|P)-(\d+)\b|\bG-(\d+)\b")
# 冲突消解记录/对账记录为历史登记小节（退役编号、旧映射），不做活引用检查
strippat = re.compile(r"\n## (冲突消解记录|对账记录)[\s\S]*?(?=\n## |\Z)")
broken = 0
for fn, text in texts.items():
    text = strippat.sub("\n", text)
    for lineno, line in enumerate(text.splitlines(), 1):
        for m in refpat.finditer(line):
            kind = m.group(1) or "G"
            n = int(m.group(2) or m.group(3))
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
