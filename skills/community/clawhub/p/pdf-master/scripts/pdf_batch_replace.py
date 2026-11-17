#!/usr/bin/env python3
"""pdf_batch_replace.py — 批量文本替换：备份 → 预览 → 执行 → 报告 → 可回滚（能力 #20）

用法：
  python3 pdf_batch_replace.py --dir ./pdfs --from "1999" --to "2199" --dry-run
  python3 pdf_batch_replace.py --dir ./pdfs --from "1999" --to "2199" --apply
  python3 pdf_batch_replace.py --dir ./pdfs --regex "1[3-9]\\d{9}" --to "[已隐藏]" --apply
  python3 pdf_batch_replace.py --dir ./pdfs --rollback
"""
import argparse, datetime, json, os, re, shutil, sys

BACKUP_DIR = ".replace_backup"
LOG = ".replace_log.json"

def iter_pdfs(d):
    for f in sorted(os.listdir(d)):
        if f.lower().endswith(".pdf"):
            yield os.path.join(d, f)

def find_hits(path, pattern, is_regex):
    import fitz
    doc = fitz.open(path)
    hits = 0
    pages = set()
    for pno in range(doc.page_count):
        text = doc[pno].get_text()
        found = re.findall(pattern, text) if is_regex else ([pattern] * text.count(pattern))
        if found:
            hits += len(found)
            pages.add(pno + 1)
    doc.close()
    return hits, sorted(pages)

def apply_file(src, dst, pattern, repl, is_regex):
    import fitz
    doc = fitz.open(src)
    n = 0
    for page in doc:
        text = page.get_text()
        targets = set(re.findall(pattern, text)) if is_regex else ({pattern} if pattern in text else set())
        for t in targets:
            for rect in page.search_for(t):
                new = re.sub(pattern, repl, t) if is_regex else repl
                page.add_redact_annot(rect)
                page.apply_redactions()
                page.insert_text((rect.x0, rect.y1 - 1), new, fontsize=max(rect.height - 1, 6))
                n += 1
    doc.save(dst, garbage=3, deflate=True)
    doc.close()
    return n

def main():
    ap = argparse.ArgumentParser(description="批量 PDF 文本替换")
    ap.add_argument("--dir", required=True)
    ap.add_argument("--from", dest="src", help="原文（精确匹配）")
    ap.add_argument("--regex", help="正则匹配（与 --from 二选一）")
    ap.add_argument("--to", default="")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--rollback", action="store_true")
    a = ap.parse_args()
    backup = os.path.join(a.dir, BACKUP_DIR)
    logp = os.path.join(a.dir, LOG)

    if a.rollback:
        if not os.path.isdir(backup):
            sys.exit("❌ 无备份可回滚")
        n = 0
        for f in os.listdir(backup):
            if f.endswith(".pdf"):
                shutil.copy2(os.path.join(backup, f), os.path.join(a.dir, f))
                n += 1
        print(f"✅ 已从备份回滚 {n} 个文件")
        return

    if not a.src and not a.regex:
        ap.error("需 --from 或 --regex")
    pattern = a.regex or re.escape(a.src)
    is_regex = bool(a.regex)

    if a.dry_run:
        total = 0
        print("📋 差异预览（未修改任何文件）：")
        for p in iter_pdfs(a.dir):
            hits, pages = find_hits(p, pattern, is_regex)
            total += hits
            if hits:
                print(f"   {os.path.basename(p)}：{hits} 处命中（页 {pages}）")
        print(f"合计：{total} 处命中。确认后执行 --apply")
        return

    os.makedirs(backup, exist_ok=True)
    results, fails = [], []
    for p in iter_pdfs(a.dir):
        name = os.path.basename(p)
        try:
            shutil.copy2(p, os.path.join(backup, name))
            n = apply_file(p, p + ".tmp", pattern, a.to, is_regex)
            os.replace(p + ".tmp", p)
            results.append({"file": name, "replaced": n})
            print(f"   ✅ {name}：替换 {n} 处")
        except Exception as e:
            fails.append({"file": name, "error": str(e)})
            print(f"   🔴 {name}：失败（{e}），原件已从备份保留")
    log = {"time": datetime.datetime.now().isoformat(timespec="seconds"),
           "pattern": a.regex or a.src, "to": a.to,
           "success": results, "failed": fails, "backup": backup}
    with open(logp, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    print(f"完成：成功 {len(results)} / 失败 {len(fails)}；备份于 {backup}；回滚：--rollback")

if __name__ == "__main__":
    main()
