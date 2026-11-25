#!/usr/bin/env python3
"""house-skills-kit 仓库自检（stdlib only，无第三方依赖）。

检查项：
1. skills/<name>/ 必须存在 SKILL.md 与 README.md
2. SKILL.md 必须有 YAML frontmatter，且含 name / description / license
3. frontmatter 的 name 必须与目录名一致
4. description 长度 >= 40 字符（描述太短等于没有触发条件）
5. SKILL.md 正文里以反引号引用的本目录文件（如 `playbook.md`）必须真实存在
6. 主 README 里 skills/<name>/ 的链接必须指向存在的目录
7. 全仓不得出现疑似密钥（sk- 开头的长串、PRIVATE KEY、password=）
8. calc-toolkit 里的 .py 必须能被 py_compile 通过

用法：
    python3 tools/validate_skills.py          # 失败退出码 1
    python3 tools/validate_skills.py --quiet  # 只打印错误
"""
import os
import re
import sys
import py_compile
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")

SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9]{20,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\bpassword\s*=\s*[^\s\"']{6,}"),
    re.compile(r"(?i)\bapi[_-]?key\s*=\s*[A-Za-z0-9]{16,}"),
]
SKIP_DIRS = {".git", "node_modules", "__pycache__", "output"}


def parse_frontmatter(text):
    """极简 YAML frontmatter 解析：只取顶层的 key: value。"""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end]
    data = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or line.startswith((" ", "\t")):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
    return data


def check_skill(name):
    errors, warnings = [], []
    d = os.path.join(SKILLS, name)
    skill_md = os.path.join(d, "SKILL.md")
    if not os.path.isfile(skill_md):
        return ["%s: 缺少 SKILL.md" % name], warnings
    with open(skill_md, encoding="utf-8") as f:
        text = f.read()

    fm = parse_frontmatter(text)
    if fm is None:
        return ["%s: SKILL.md 缺少 YAML frontmatter" % name], warnings
    for key in ("name", "description", "license"):
        if not fm.get(key):
            errors.append("%s: frontmatter 缺少 %s" % (name, key))
    if fm.get("name") and fm["name"] != name:
        if name in fm["name"]:
            warnings.append("%s: frontmatter name=%r 含目录名（发布名与目录名不同，可接受）"
                            % (name, fm["name"]))
        else:
            errors.append("%s: frontmatter name=%r 与目录名不一致" % (name, fm["name"]))
    desc = fm.get("description", "")
    if desc and len(desc) < 40:
        warnings.append("%s: description 仅 %d 字符，触发条件可能不足" % (name, len(desc)))

    if not os.path.isfile(os.path.join(d, "README.md")):
        warnings.append("%s: 缺少 README.md（建议补一份给人看的说明）" % name)

    # 反引号引用的文件是否存在（本目录或 calc-toolkit 公共工具目录）
    calc_dir = os.path.join(SKILLS, "calc-toolkit")
    for ref in set(re.findall(r"`([A-Za-z0-9_\-]+\.(?:md|py|yaml))`", text)):
        if not (os.path.exists(os.path.join(d, ref)) or os.path.exists(os.path.join(calc_dir, ref))):
            errors.append("%s: SKILL.md 引用了不存在的文件 %s" % (name, ref))

    # 空章节探测
    if len(text.splitlines()) < 20:
        warnings.append("%s: SKILL.md 少于 20 行，内容可能过薄" % name)
    return errors, warnings


def check_readme_links():
    errors = []
    readme = os.path.join(ROOT, "README.md")
    if not os.path.isfile(readme):
        return ["根目录缺少 README.md"]
    with open(readme, encoding="utf-8") as f:
        text = f.read()
    for path in set(re.findall(r"\((skills/[A-Za-z0-9_\-]+/?)\)", text)):
        target = os.path.join(ROOT, path.rstrip("/"))
        if not os.path.isdir(target):
            errors.append("README.md 链接指向不存在的目录: %s" % path)
    # 反向：目录存在但 README 未提及
    mentioned = set(re.findall(r"skills/([A-Za-z0-9_\-]+)/?", text))
    for name in sorted(os.listdir(SKILLS)):
        if os.path.isdir(os.path.join(SKILLS, name)) and name not in mentioned:
            errors.append("skills/%s 未在主 README 中登记" % name)
    return errors


def scan_secrets():
    hits = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith((".md", ".py", ".yaml", ".yml", ".sh", ".json")):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, ROOT)
            try:
                with open(p, encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, 1):
                        for pat in SECRET_PATTERNS:
                            if pat.search(line):
                                hits.append("%s:%d 疑似密钥/口令" % (rel, i))
                                break
            except OSError:
                continue
    return hits


def compile_calc_toolkit():
    errors = []
    calc = os.path.join(SKILLS, "calc-toolkit")
    if not os.path.isdir(calc):
        return ["缺少 skills/calc-toolkit"]
    with tempfile.TemporaryDirectory() as tmp:
        for fn in sorted(os.listdir(calc)):
            if fn.endswith(".py"):
                try:
                    py_compile.compile(os.path.join(calc, fn),
                                       cfile=os.path.join(tmp, fn + "c"), doraise=True)
                except py_compile.PyCompileError as e:
                    errors.append("calc-toolkit/%s 编译失败: %s" % (fn, str(e).splitlines()[0]))
    return errors


SPEC_SECTIONS = [
    ("必问信息", r"必问信息"),
    ("知识库与数据来源", r"知识库|数据来源"),
    ("目标读者", r"目标读者"),
    ("写作风格", r"写作风格"),
    ("输出格式", r"输出格式"),
    ("数据时间戳", r"数据时间戳"),
]


def check_spec_coverage(names, strict=False):
    """--spec：软性检查必备 12 段中的六个新增段覆盖情况（只提示，不报错）。
    --spec-strict：同样输出，但缺失即返回 1，供 CI 拦截新增的不达标技能。"""
    rows, missing_total = [], 0
    for n in names:
        p = os.path.join(SKILLS, n, "SKILL.md")
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as f:
            text = f.read()
        miss = [label for label, pat in SPEC_SECTIONS if not re.search(pat, text)]
        rows.append((n, miss))
        missing_total += len(miss)
    print("\n规范覆盖（docs/SKILL-AUTHORING-SPEC.md 六段）：")
    for n, miss in rows:
        mark = "✓" if not miss else "缺 %d/6" % len(miss)
        detail = "" if not miss else " → " + "、".join(miss)
        print("  %-32s %s%s" % (n, mark, detail))
    ok = sum(1 for _, m in rows if not m)
    print("\n达标 %d/%d 个技能（六段齐）；合计缺失 %d 段。" % (ok, len(rows), missing_total))
    return 1 if (strict and missing_total) else 0


def check_readme_boundary(names):
    """每个技能 README 必须有「什么时候不要用我」边界段，且至少给 2 条走向别的技能的分流。
    理由：技能库最常见的误用是"拿对工具做错事"，边界段是使用者判断该不该打开它的第一道门。"""
    errors = []
    for n in names:
        p = os.path.join(SKILLS, n, "README.md")
        if not os.path.isfile(p):
            errors.append("%s: 缺少 README.md（应当说明适用谁/怎么用/什么时候不要用我）" % n)
            continue
        with open(p, encoding="utf-8") as f:
            text = f.read()
        if "什么时候不要用我" not in text:
            errors.append("%s: README 缺少「什么时候不要用我」边界段" % n)
            continue
        sec = text.split("什么时候不要用我", 1)[1]
        bullets = re.findall(r"^- \*\*.+?\*\* → ", sec, re.M)
        if len(bullets) < 2:
            errors.append("%s: 边界段要有至少 2 条「什么场景 → 该用哪个技能」的分流" % n)
    return errors


def check_skill_map(names):
    """每个技能必须在 docs/SKILL-MAP.md 里出现（去哪找、什么时候用都靠这一页）。"""
    p = os.path.join(os.path.dirname(SKILLS), "docs", "SKILL-MAP.md")
    if not os.path.isfile(p):
        return ["缺少 docs/SKILL-MAP.md（使用者按场景找技能的入口）"]
    with open(p, encoding="utf-8") as f:
        text = f.read()
    return ["%s: 未登记在 docs/SKILL-MAP.md" % n for n in names if n not in text]


def main():
    quiet = "--quiet" in sys.argv
    names = sorted(n for n in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, n)))
    if "--spec" in sys.argv or "--spec-strict" in sys.argv:
        return check_spec_coverage(names, strict="--spec-strict" in sys.argv)
    all_errors, all_warnings = [], []
    for n in names:
        e, w = check_skill(n)
        all_errors += e
        all_warnings += w
    all_errors += check_readme_links()
    all_errors += check_readme_boundary(names)
    all_errors += check_skill_map(names)
    all_errors += scan_secrets()
    all_errors += compile_calc_toolkit()

    if not quiet:
        print("扫描技能目录：%d 个 → %s" % (len(names), ", ".join(names)))
        for w in all_warnings:
            print("  [warn] %s" % w)
    for e in all_errors:
        print("  [error] %s" % e)

    if all_errors:
        print("\n✗ 自检失败：%d 个错误" % len(all_errors))
        return 1
    print("✓ 自检通过：%d 个技能，0 错误，%d 个提示" % (len(names), len(all_warnings)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
