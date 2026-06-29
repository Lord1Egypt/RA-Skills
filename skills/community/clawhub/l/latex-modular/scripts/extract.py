r"""extract.py - 从 .tex 提取组件，存入 components/
用法: python extract.py <input.tex> <output_dir>
"""
import json, os, sys

def _balanced_end(lines, start):
    r"""从 lines[start] 开始，找 { } 匹配的结束位置。
    返回第一个深度<=0的位置（exclusive end）。
    """
    depth = lines[start].count("{") - lines[start].count("}")
    if depth <= 0:
        return start + 1
    i = start + 1
    while i < len(lines):
        depth += lines[i].count("{") - lines[i].count("}")
        i += 1
        if depth <= 0:
            return i
    return len(lines)

def _save(out, sub, name, content):
    d = os.path.join(out, "scripts", "components", sub)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return "{}/{}".format(sub, name)

def extract(in_path, out_dir):
    with open(in_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 分离 preamble / body
    bs = text.find(r"\begin{document}")
    be = text.find(r"\end{document}")
    preamble = text[:bs].strip() if bs != -1 else ""
    body = text[bs+len(r"\begin{document}"):be].strip() if be != -1 else ""

    plines = preamble.splitlines()
    comps = []

    # ── 1. documentclass ────────────────────────────────
    for ln in plines:
        s = ln.strip()
        if s.startswith(r"\documentclass"):
            p = _save(out_dir, "preamble", "class-settings.txt", s.rstrip() + "\n")
            comps.append({"type":"preamble","name":"class-settings","path":p,"category":"class","description":"文档类"})
            break

    # ── 2. usepackage（按行，不过度解析）────────────
    pkg = [l.rstrip() for l in plines if l.strip().startswith(r"\usepackage")]
    if pkg:
        p = _save(out_dir, "preamble", "packages.txt", "\n".join(pkg) + "\n")
        comps.append({"type":"preamble","name":"packages","path":p,"category":"package","description":"宏包"})

    # ── 3. 字体设置块（\setmainfont 到下一个顶级命令）──
    font_lines = []
    i = 0
    while i < len(plines):
        s = plines[i].strip()
        if s.startswith(("\\setmainfont","\\setCJKmainfont","\\newCJKfontfamily",
                        "\\setCJKsansfont","\\setCJKmonofont")):
            end = _balanced_end(plines, i)
            font_lines.extend(plines[j].rstrip() for j in range(i, end))
            i = end
            continue
        i += 1
    if font_lines:
        p = _save(out_dir, "preamble", "font-settings.txt", "\n".join(font_lines) + "\n")
        comps.append({"type":"preamble","name":"font-settings","path":p,"category":"font","description":"字体设置"})

    # ── 4. ctexset 块 ─────────────────────────────────
    ctex_lines = []
    i = 0
    while i < len(plines):
        s = plines[i].strip()
        if s.startswith(r"\ctexset"):
            end = _balanced_end(plines, i)
            ctex_lines.extend(plines[j].rstrip() for j in range(i, end))
            i = end
            continue
        i += 1
    if ctex_lines:
        p = _save(out_dir, "styles", "section-style.txt", "\n".join(ctex_lines) + "\n")
        comps.append({"type":"styles","name":"section-style","path":p,"category":"style","description":"章节样式"})

    # ── 5. newcommand / renewcommand ────────────────────
    cmd_lines = []
    i = 0
    while i < len(plines):
        s = plines[i].strip()
        if s.startswith(("\\newcommand","\\renewcommand","\\providecommand")):
            end = _balanced_end(plines, i)
            cmd_lines.extend(plines[j].rstrip() for j in range(i, end))
            i = end
            continue
        i += 1
    if cmd_lines:
        p = _save(out_dir, "commands", "user-commands.txt", "\n".join(cmd_lines) + "\n")
        comps.append({"type":"commands","name":"user-commands","path":p,"category":"command","description":"自定义命令"})

    # ── 6. newenvironment / renewenvironment / NewDocumentEnvironment ──
    env_lines = []
    i = 0
    while i < len(plines):
        s = plines[i].strip()
        if s.startswith(("\\newenvironment","\\renewenvironment","\\NewDocumentEnvironment")):
            end = _balanced_end(plines, i)
            env_lines.extend(plines[j].rstrip() for j in range(i, end))
            i = end
            continue
        i += 1
    if env_lines:
        p = _save(out_dir, "environments", "user-environments.txt", "\n".join(env_lines) + "\n")
        comps.append({"type":"environments","name":"user-environments","path":p,"category":"environment","description":"自定义环境"})

    # ── 7. fancyhdr 设置 ───────────────────────────────
    fancy_lines = []
    i = 0
    while i < len(plines):
        s = plines[i].strip()
        if s == r"\pagestyle{fancy}":
            fancy_lines.append(plines[i].rstrip())  # 保留触发行
            j = i + 1  # 从下一行开始扫描，避免死循环
            while j < len(plines):
                t = plines[j].strip()
                if t.startswith(("\\fancyhead","\\fancyfoot","\\fancyhf",
                                 "\\headrulewidth","\\footrulewidth",
                                 "\\setlength")):
                    fancy_lines.append(plines[j].rstrip())
                    j += 1
                elif t == "" and j == i + 1:
                    j += 1
                else:
                    break
            i = j
            continue
        i += 1
    if fancy_lines:
        p = _save(out_dir, "styles", "header-footer.txt", "\n".join(fancy_lines) + "\n")
        comps.append({"type":"styles","name":"header-footer","path":p,"category":"header","description":"页眉页脚"})

    # ── 保存 body ───────────────────────────────────────
    p = _save(out_dir, "body", "body.txt", body + "\n")
    comps.append({"type":"body","name":"main-body","path":p,"category":"body","description":"正文"})

    # manifest
    manifest = {"components": comps, "version": "1.0.0"}
    mdir = os.path.join(out_dir, "scripts", "components")
    os.makedirs(mdir, exist_ok=True)
    with open(os.path.join(mdir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print("[OK] 提取完成：{} 个组件".format(len(comps)))
    for c in comps:
        print("  - [{}] {}: {}".format(c["type"], c["name"], c["path"]))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python extract.py <input.tex> <output_dir>")
        sys.exit(1)
    extract(sys.argv[1], sys.argv[2])
