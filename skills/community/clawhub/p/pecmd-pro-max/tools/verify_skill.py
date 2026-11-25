#!/usr/bin/env python3
"""Verify PECMD Pro Max docs, links, fences, manifests and known-bad patterns."""
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
errors = []

REQUIRED = [
    "SKILL.md",
    "README.md",
    "README.en.md",
    "CHANGELOG.md",
    "RELEASE.md",
    "references/commands-full.md",
    "references/pecmd-gui.md",
    "references/pe-startup.md",
    "references/troubleshooting.md",
    "references/how-tos/storage.md",
    "references/how-tos/system.md",
    "references/how-tos/gui.md",
    "references/how-tos/net.md",
    "examples/README.md",
    "examples/MANIFEST.sha256",
    "bin/README.md",
    "bin/SHA256SUMS.txt",
    "tools/verify_skill.py",
    ".github/workflows/verify-skill.yml",
]

COUNT_DOCS = [
    "SKILL.md",
    "references/commands-full.md",
    "references/pecmd-gui.md",
    "references/pe-startup.md",
    "references/troubleshooting.md",
]

SCAN = [
    "SKILL.md",
    "references/commands-full.md",
    "references/pecmd-gui.md",
    "references/pe-startup.md",
    "references/how-tos/storage.md",
    "references/how-tos/system.md",
    "references/how-tos/gui.md",
    "references/how-tos/net.md",
]

# (regex, hint). Lines explicitly marked as wrong ("不是", "错误") are skipped.
FORBIDDEN = [
    (r"POS=\?;", "POS 查询用 ':' 分隔：POS=?&L:&T:&W:&H"),
    (r"\.Value\s*=", "PBAR 用 ENVI @PBar=进度，没有 .Value"),
    (r"SET\s+@@sendmsg", "用 ENVI @@SENDMSG"),
    (r"MiniNT\\\\WinPEShell", "不存在该注册表值；入口是 Setup\\CmdLine/winpeshl.ini"),
    (r"WinXShell\.xml", "WinXShell 配置是 .jcfg + .lua"),
    (r"CODE\s+\*[^\n]*\*HEX", "CODE 没有 *HEX 目标格式"),
    (r"-minb\b", "-minb 不存在；最小化默认可用，只有 -disminb"),
    (r"CALL\s+@--(?!popmenu\b)[A-Za-z]", "CALL @-- 卸载 Win 环境，不接窗口名；菜单用 CALL @--popmenu[:x.y] 菜单名"),
    (r"HKEY\s+\$Ctrl", "PE 全局热键用 HOTK"),
    (r"\.Check=\?;", "勾选状态用 %控件.Check%，没有 .Check=?;"),
    (r"MSTR[^\n]*<[0-9]+\*>[^\n]*(仅字段|单字段)", "<N*> 是 N 到末尾，单字段用 <N>"),
    (r"^\s*FILE\s+\S+\s*->[^\n]*(复制|copy)", "FILE -> 是移动；复制用 =>"),
    (r"REGI\s+\.HKLM[^\n]*(离线|offline)", "REGI . 是任意类型；离线用 HIVE"),
    (r"\bHIVE\s+[^\n,]+,\s*(HKLM|HKU)\\", "HIVE 语法是 子项名,文件"),
]


def read_text(rel):
    path = os.path.join(ROOT, rel)
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def fail(msg):
    errors.append(msg)


def check_required():
    for rel in REQUIRED:
        if not os.path.isfile(os.path.join(ROOT, rel)):
            fail(f"missing required file: {rel}")


def check_fences():
    for rel in SCAN:
        text = read_text(rel)
        fences = sum(1 for line in text.splitlines() if line.startswith("```"))
        if fences % 2:
            fail(f"unbalanced code fences: {rel} ({fences})")


def check_links():
    for rel in iter_markdown():
        base = os.path.dirname(os.path.join(ROOT, rel))
        text = read_text(rel)
        for target in re.findall(r"\]\(([^)]+)\)", text):
            target = target.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(base, target))):
                fail(f"broken link in {rel}: {target}")


def iter_markdown():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "node_modules"]
        for name in filenames:
            if name.endswith(".md"):
                yield os.path.relpath(os.path.join(dirpath, name), ROOT)


def check_line_counts():
    for readme in ("README.md", "README.en.md"):
        text = read_text(readme)
        for rel in COUNT_DOCS:
            name = re.escape(os.path.basename(rel))
            match = re.search(name + r"[^\n]*?[（(](\d+)\s*(?:行|lines?)", text)
            if not match:
                fail(f"{readme}: no line count for {rel}")
                continue
            actual = len(read_text(rel).splitlines())
            if int(match.group(1)) != actual:
                fail(f"{readme}: {rel} says {match.group(1)} lines, actual {actual}")


def check_forbidden():
    for rel in SCAN:
        for lineno, line in enumerate(read_text(rel).splitlines(), 1):
            if any(marker in line for marker in ("不是", "错误", "❌", "不存在", "没有", "不要")):
                continue
            for pattern, hint in FORBIDDEN:
                if re.search(pattern, line, re.IGNORECASE):
                    fail(f"{rel}:{lineno}: {hint} -> {line.strip()[:100]}")


def check_version():
    skill = read_text("SKILL.md")
    match = re.search(r"^version:\s*([0-9.]+)", skill, re.M)
    if not match:
        fail("SKILL.md frontmatter has no version")
        return
    version = match.group(1)
    for rel in ["README.md", "README.en.md"]:
        if f"version-{version}-blue" not in read_text(rel):
            fail(f"{rel} badge does not match SKILL.md version {version}")
    if f"## {version}" not in read_text("CHANGELOG.md"):
        fail(f"CHANGELOG.md has no entry for version {version}")
    return version


def check_example_counts():
    readme = read_text("examples/README.md")
    all_scripts = []
    for dirpath, _, filenames in os.walk(os.path.join(ROOT, "examples")):
        for name in filenames:
            if os.path.splitext(name)[1].lower() in (".wcs", ".ini", ".wci", ".wce"):
                all_scripts.append(os.path.join(dirpath, name))
    declared = re.search(r"(\d+)\s*个示例", readme)
    if declared and int(declared.group(1)) != len(all_scripts):
        fail(f"examples/README.md says {declared.group(1)} examples, actual {len(all_scripts)}")
    for name, claimed in re.findall(r"\|\s*`([^`]+\.(?:wcs|ini|wci|wce))`\s*\|\s*(\d+)\s*\|", readme):
        matches = [p for p in all_scripts if os.path.basename(p) == os.path.basename(name)]
        if len(matches) != 1:
            fail(f"examples/README.md: cannot resolve example {name}")
            continue
        raw = open(matches[0], "rb").read()
        if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
            candidates = ("utf-16",)
        elif raw.startswith(b"\xef\xbb\xbf"):
            candidates = ("utf-8-sig",)
        else:
            candidates = ("utf-8", "gbk")
        text = None
        for encoding in candidates:
            try:
                text = raw.decode(encoding)
                break
            except UnicodeDecodeError:
                pass
        if text is None:
            fail(f"examples/README.md: cannot decode {name}")
            continue
        actual = len(text.splitlines())
        if actual != int(claimed):
            fail(f"examples/README.md: {name} says {claimed} lines, actual {actual}")


def check_audit(version):
    name = "AUDIT.md"
    if not os.path.isfile(os.path.join(ROOT, name)):
        fail(f"missing audit report: {name}")
        return
    text = read_text(name)
    if f"修复版本：`{version}`" not in text:
        fail(f"{name} version line does not match SKILL.md version {version}")
    ids = re.findall(r"^\|\s*((?:V|G|D|S|PS|X)-\d+|C-MSTR)\s*\|", text, re.M)
    if len(ids) != len(set(ids)):
        fail(f"{name} contains duplicate issue IDs")
    if len(set(ids)) != 136:
        fail(f"{name} should cover 136 issues, found {len(set(ids))}")
    p0 = text.split("## 1. P0")[1].split("## 2. P1")[0]
    p0_ids = re.findall(r"^\|\s*((?:V|G|D|S|PS)-\d+|C-MSTR)\s*\|", p0, re.M)
    if len(set(p0_ids)) != 26:
        fail(f"{name} should list 26 P0 issues, found {len(set(p0_ids))}")


def check_manifest(manifest, root_rel, exclude=()):
    path = os.path.join(ROOT, manifest)
    if not os.path.isfile(path):
        return
    listed = set()
    for line in read_text(manifest).splitlines():
        line = line.strip()
        if not line:
            continue
        digest, name = line.split(None, 1)
        name = name.lstrip("*").strip()
        listed.add(name)
        target = os.path.join(ROOT, root_rel, name.replace("/", os.sep))
        if not os.path.isfile(target):
            fail(f"{manifest}: missing {name}")
            continue
        actual = hashlib.sha256(open(target, "rb").read()).hexdigest()
        if actual != digest:
            fail(f"{manifest}: hash mismatch {name}")
    actual_files = set()
    for dirpath, _, filenames in os.walk(os.path.join(ROOT, root_rel)):
        for name in filenames:
            rel = os.path.relpath(os.path.join(dirpath, name), os.path.join(ROOT, root_rel))
            rel = rel.replace(os.sep, "/")
            if rel not in exclude:
                actual_files.add(rel)
    for name in sorted(actual_files - listed):
        fail(f"{manifest}: unlisted file {name}")
    for name in sorted(listed - actual_files):
        fail(f"{manifest}: listed file not found {name}")


def main():
    check_required()
    if errors:
        for err in errors:
            print("FAIL:", err)
        return 1
    check_fences()
    check_links()
    check_forbidden()
    version = check_version()
    if version:
        check_audit(version)
    check_line_counts()
    check_example_counts()
    check_manifest("examples/MANIFEST.sha256", "examples", ("README.md", "MANIFEST.sha256"))
    check_manifest("bin/SHA256SUMS.txt", "bin", ("README.md", "SHA256SUMS.txt"))
    if errors:
        for err in errors:
            print("FAIL:", err)
        return 1
    print("OK: docs, links, fences, manifests and anti-patterns verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
