#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Markdown 链接体检器（零依赖 / 默认离线 / JSON IR / 修复回执）
# 内部相对链接与本地锚点为确定性判定；外链仅在 --net 时校验（HEAD，8s 超时，一次重试）。
import argparse, json, os, re, sys, urllib.request, urllib.error

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def slugify(t):
    t = t.strip().lower()
    t = re.sub(r"[^\w\u4e00-\u9fff\- ]", "", t)
    t = t.replace(" ", "-")
    return t


def headings(path):
    out = set()
    try:
        with open(path, encoding="utf-8-sig", errors="replace") as fh:
            for line in fh:
                m = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
                if m:
                    out.add(slugify(m.group(1)))
    except Exception:
        pass
    return out


def walk_md(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.lower().endswith((".md", ".markdown")):
                yield os.path.join(dirpath, fn)


def check_external(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "md-link-audit/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return None if resp.status < 400 else "http %d" % resp.status
    except urllib.error.HTTPError as e:
        if e.code in (405, 501):
            try:
                req2 = urllib.request.Request(url, headers={"User-Agent": "md-link-audit/1.0"})
                with urllib.request.urlopen(req2, timeout=8) as resp:
                    return None if resp.status < 400 else "http %d" % resp.status
            except Exception:
                return "unreachable"
        return "http %d" % e.code
    except Exception:
        return "unreachable"


def main():
    ap = argparse.ArgumentParser(prog="md_link_audit", description="Markdown 链接体检（默认离线，内部链接确定性判定）")
    ap.add_argument("root", nargs="?", default=".", help="文档目录")
    ap.add_argument("--net", action="store_true", help="联网校验外部链接")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isdir(a.root):
        print(json.dumps({"errors": [{"code": "MLK_E_NO_DIR", "subject": a.root,
                                      "evidence": "目录不存在", "fixes": ["传入正确的文档目录"]}]},
                         ensure_ascii=False))
        sys.exit(2)
    files = list(walk_md(a.root))
    if not files:
        print(json.dumps({"errors": [{"code": "MLK_E_NO_MD", "subject": a.root,
                                      "evidence": "未发现 Markdown 文件", "fixes": ["确认目录或改用其他目录"]}]},
                         ensure_ascii=False))
        sys.exit(2)
    ext_cache = {}
    results = []
    total = internal_broken = external_bad = 0
    for path in files:
        rel = os.path.relpath(path, a.root)
        try:
            text = open(path, encoding="utf-8-sig", errors="replace").read()
        except Exception:
            continue
        own = headings(path)
        broken = []
        for m in LINK_RE.finditer(text):
            target = m.group(1).strip()
            total += 1
            if target.startswith(("http://", "https://")):
                if a.net:
                    if target not in ext_cache:
                        ext_cache[target] = check_external(target)
                    reason = ext_cache[target]
                    if reason:
                        external_bad += 1
                        broken.append({"target": target, "reason": reason})
                continue
            if target.startswith("mailto:"):
                continue
            if target.startswith("#"):
                anchor = slugify(target[1:])
                if anchor not in own:
                    internal_broken += 1
                    broken.append({"target": target, "reason": "本文件无对应标题"})
                continue
            filepart, _, anchor = target.partition("#")
            fp = os.path.normpath(os.path.join(os.path.dirname(path), filepart))
            if not os.path.exists(fp):
                internal_broken += 1
                broken.append({"target": target, "reason": "文件不存在"})
            elif anchor:
                anchor_s = slugify(anchor)
                if anchor_s not in headings(fp):
                    internal_broken += 1
                    broken.append({"target": target, "reason": "目标文件无对应标题"})
        if broken:
            results.append({"file": rel, "broken": broken})
    summary = {"files": len(files), "links": total, "internal_broken": internal_broken,
               "external_bad": external_bad}
    if a.json:
        print(json.dumps({"summary": summary, "broken_by_file": results}, ensure_ascii=False, indent=2))
    else:
        print("扫描 %d 个 Markdown 文件 · 链接 %d 条" % (len(files), total))
        for r in results:
            print("  %s" % r["file"])
            for b in r["broken"]:
                print("    %s  （%s）" % (b["target"], b["reason"]))
        if not a.net:
            print("  外部链接未校验（--net 未开启）")
        print("%s，rc=%d" % ("发现断链" if (internal_broken or external_bad) else "全部通过",
                             1 if (internal_broken or external_bad) else 0))
    sys.exit(1 if (internal_broken or external_bad) else 0)


if __name__ == "__main__":
    main()
