#!/usr/bin/env python3
"""pdf_info.py — PDF 检测与元数据工具（能力 #1-#25 的入口检测；#10 元数据清洗）

用法：
  python3 pdf_info.py file.pdf                 # 检测报告（人类可读）
  python3 pdf_info.py file.pdf --json          # JSON 输出
  python3 pdf_info.py file.pdf --meta          # 完整元数据导出
  python3 pdf_info.py file.pdf --scrub out.pdf # 清洗元数据后另存
"""
import argparse, json, os, sys

def detect(path):
    import fitz
    info = {"file": os.path.basename(path), "size_mb": round(os.path.getsize(path) / 1048576, 2)}
    doc = fitz.open(path)
    info["encrypted"] = doc.needs_pass
    if doc.needs_pass:
        info.update(pages=None, type="encrypted", hint="需要密码：回复 密码:xxx")
        doc.close()
        return info
    info["pages"] = doc.page_count
    text_pages, image_pages, total_chars = 0, 0, 0
    sensitive_hits = []
    for page in doc:
        t = page.get_text().strip()
        total_chars += len(t)
        if len(t) > 50:
            text_pages += 1
        elif page.get_images():
            image_pages += 1
        # 密级标记检测（安全路由用）
        for mark in ("绝密", "机密", "秘密", "内部资料"):
            if mark in t:
                sensitive_hits.append(mark)
    info["text_pages"] = text_pages
    info["image_pages"] = image_pages
    info["chars_per_page"] = total_chars // max(doc.page_count, 1)
    if text_pages == doc.page_count:
        info["type"] = "text"
    elif image_pages >= doc.page_count * 0.8:
        info["type"] = "scanned"
    else:
        info["type"] = "mixed"
    info["sensitive_marks"] = sorted(set(sensitive_hits))
    info["metadata"] = {k: v for k, v in doc.metadata.items() if v}
    doc.close()
    return info

def scrub(src, dst):
    import fitz
    doc = fitz.open(src)
    doc.set_metadata({})
    try:
        doc.del_xml_metadata()
    except Exception:
        pass
    doc.scrub(metadata=True, xml_metadata=True, embedded_files=True,
              hidden_text=True, thumbnails=True, javascript=True)
    doc.save(dst, garbage=4, deflate=True)
    doc.close()

def main():
    ap = argparse.ArgumentParser(description="PDF 检测/元数据工具")
    ap.add_argument("pdf")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--meta", action="store_true", help="导出完整元数据")
    ap.add_argument("--scrub", metavar="OUT", help="清洗元数据另存为 OUT")
    a = ap.parse_args()
    if a.scrub:
        scrub(a.pdf, a.scrub)
        print(f"✅ 元数据已清洗：{a.scrub}")
        after = detect(a.scrub)
        print(f"清洗后元数据字段：{after['metadata'] or '（空）'}")
        return
    info = detect(a.pdf)
    if a.json:
        print(json.dumps(info, ensure_ascii=False, indent=2))
        return
    if a.meta:
        print(json.dumps(info.get("metadata", {}), ensure_ascii=False, indent=2) or "（无元数据）")
        return
    print(f"文件：{info['file']}  大小：{info['size_mb']}MB  页数：{info['pages']}")
    print(f"加密：{'是' if info['encrypted'] else '否'}  类型：{info['type']}"
          f"（文本页 {info.get('text_pages')} / 图像页 {info.get('image_pages')}）")
    if info.get("sensitive_marks"):
        print(f"⚠️ 检测到密级标记：{','.join(info['sensitive_marks'])} → 应路由本地模型")

if __name__ == "__main__":
    main()
