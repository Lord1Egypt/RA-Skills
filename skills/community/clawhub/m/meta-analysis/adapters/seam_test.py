# -*- coding: utf-8 -*-
"""集成缝实测：ct-literature 下载 → meta-analysis pdf_extractor 抓取。

忠实走 Block A 的 A2 路径（block_a.a2_literature_search → execute_tool_cards
→ ct_literature.py 本地 CLI），拿到书目元数据后，先做 A3 摘要相关性门控，
仅对"通过门控 + 有下载入口"的 OA 文献按 DOI/PMID/直链落盘 PDF，再喂给
pdf_extractor.extract 验证 A4 输入形状。

关键新增：下载前先按摘要做相关性门控——未命中纳入关键词（标题/摘要）的文献
直接拦截为"待人工核验"，不浪费下载配额；能下到的落盘、下不到的留待用户上传。
全程本地，不经 coze 云（开发期冻结）。
"""
import os
import sys
import json
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import block_a          # A2 检索委派（本地 ct-literature）；A3 摘要门控
import pdf_extractor   # A4 抓取（本地 pdf_extractor）
import pdf_fetch       # OA PDF 下载（DOI/PMID → Unpaywall/PMC）

# 临时输出目录：优先 env(META_SEAM_DIR)，否则系统临时目录（不落任何固定本机路径）
SEAM_DIR = os.environ.get("META_SEAM_DIR") or os.path.join(tempfile.gettempdir(), "meta_analysis_seam_test")
os.makedirs(SEAM_DIR, exist_ok=True)
# 统一到 block_a 的 A4 缓存目录（绝对路径、不依赖 cwd），与工作台/上传端点共享，
# 落盘命名用 _pdf_stem，且下载前查 _a4_cached_pdf —— 杜绝 docN 覆盖式命名与重复下载。
PDF_DIR = block_a.A4_PDF_CACHE_DIR
os.makedirs(PDF_DIR, exist_ok=True)

TOPIC = "SGLT2 inhibitor randomized controlled trial cardiovascular"

# 相关性门控关键词（对应研究问题 PICOS：SGLT2i + 心血管结局 + RCT）
INCLUSION_HINTS = ["sglt2", "cardiovascular", "trial", "randomized",
                   "placebo", "type 2 diabetes", "mace"]

# 单次实测最多尝试下载的篇数（控制联网配额/耗时；门控后通过者才计数）
MAX_ATTEMPTS = 12


def pick_candidate(study):
    """返回 (kind, ident) 或 None。

    下载优先级（对应"能下载的先下，下不到的留待用户上传"）：
      1) 直链 PDF（oa 字段本身即 PDF 链接）→ 直接下，最稳、不经 Unpaywall
      2) pmid → PMC 全文直链
      3) 裸 doi → Unpaywall（注意：需剥掉 'https://doi.org/' 前缀）
    """
    oa = (study.get("url") or "").strip()
    if oa.lower().endswith(".pdf") or "doi/pdf/" in oa.lower():
        return ("url", oa)
    pmid = study.get("pmid")
    if pmid:
        return ("pmid", str(pmid))
    doi = (study.get("doi") or "").strip()
    if doi:
        bare = doi.split("doi.org/")[-1] if "doi.org/" in doi else doi
        return ("doi", bare)
    return None


def is_pdf(path):
    try:
        with open(path, "rb") as f:
            return f.read(5) == b"%PDF-"
    except Exception:
        return False


def main():
    print(f"[A2] 检索主题: {TOPIC}")
    studies, outs, card = block_a.a2_literature_search(
        TOPIC, max_results=30, out_dir=SEAM_DIR)
    print(f"[A2] 命中文献数: {len(studies)}")
    for s in studies[:10]:
        print("   ·", (s.get("title") or "")[:70],
              "| pmid:", s.get("pmid"), "| doi:", s.get("doi"))

    # A3 摘要相关性门控：用纳入关键词匹配标题/摘要，未命中者标"待人工核验"
    screened, nha = block_a.a3_screening(studies, inclusion_hints=INCLUSION_HINTS)
    n_incl = sum(s["include"] for s in screened)
    print(f"[A3] 相关性门控：{n_incl}/{len(screened)} 篇通过"
          f"（其余标记为需人工核验，下载前拦截）")

    results = []
    dl_index = 0
    attempted = 0
    n_deferred = 0
    for s, sc in zip(studies, screened):
        title = s.get("title") or ""
        doi = s.get("doi")
        cand = pick_candidate(s)

        if not sc["include"]:
            # 相关性门控未通过 → 不下载，待人工核验（先于配额判定，确保正确归类）
            print(f"  [门控] ✋ {title[:48]} → 未通过摘要相关性门控：{sc['reason']}")
            results.append({"gate": "relevance_skip", "title": title, "doi": doi,
                            "reason": sc["reason"], "candidate": cand})
            continue

        if not cand:
            print(f"  [门控] ⏭ {title[:48]} → 通过相关性，但无可下载候选"
                  f"（无 PMID/DOI/直链），留待用户上传")
            results.append({"gate": "no_candidate", "title": title, "doi": doi,
                            "reason": "通过相关性门控但无下载入口，需用户上传 PDF"})
            continue

        # 通过门控 + 有候选 → 下载（受 MAX_ATTEMPTS 配额约束）
        # 下载前先查统一缓存：已落盘且确为真 PDF 直接复用，绝不重复下载/覆盖。
        cached = block_a._a4_cached_pdf(study, PDF_DIR)
        pdf_path = cached or os.path.join(PDF_DIR, block_a._pdf_stem(study) + ".pdf")
        if cached:
            kind, ident = "cached", os.path.basename(cached)
            print(f"  [缓存] ♻ {title[:48]} → 复用 {ident}，跳过下载")
            ok = True  # _a4_cached_pdf 已用 _is_pdf 校验为真 PDF
        else:
            if attempted >= MAX_ATTEMPTS:
                n_deferred += 1
                results.append({"gate": "quota_deferred", "title": title, "doi": doi,
                                "reason": f"通过门控但超过本次 MAX_ATTEMPTS={MAX_ATTEMPTS}"})
                continue
            attempted += 1
            kind, ident = cand
            url = None
            tried = []
            try:
                if kind == "url":
                    url = ident
                    tried.append(("直链", ident))
                elif kind == "pmid":
                    url = pdf_fetch.pmid_to_pdf(ident)
                    tried.append(("pmid→PMC", ident))
                elif kind == "doi":
                    # Unpaywall → PMC OA 兜底
                    url = pdf_fetch.doi_to_pdf(ident, pdf_fetch.DEFAULT_EMAIL)
                    tried.append(("doi→Unpaywall", ident))
                    if not url:
                        url = pdf_fetch.doi_to_pmc_pdf(ident)
                        tried.append(("doi→PMC-OA", ident))
            except Exception as e:
                url = None
                print(f"  [{kind}={ident}] → 解析异常: {e}")
            if not url:
                print(f"  [下载] ⛔ {title[:48]} → 无 OA 副本"
                      f"（试过: {[t[0] for t in tried]}），需用户上传")
                results.append({"gate": "pass_no_oa", "title": title, "doi": doi,
                                "kind": kind, "id": ident, "status": "no_oa",
                                "tried": [t[0] for t in tried],
                                "note": "通过相关性门控但无开放获取全文，需用户手动上传 PDF"})
                continue
            ok = pdf_fetch.download(url, pdf_path)
        res = pdf_extractor.extract(pdf_path)
        rs = res["review_summary"]
        tworows = [r for r in res["rows"]
                   if {"ai", "bi", "ci", "di"}.issubset(r)]
        print(f"  [抓取] ✅ {title[:48]} → 页={res['n_pages']} 行={rs['n_rows']} "
              f"verified={rs['verified']} needs_review={rs['needs_review']} "
              f"四格表行={len(tworows)} 正文候选={len(res['candidates'])}")
        results.append({"gate": "pass_downloaded", "title": title, "doi": doi,
                        "kind": kind, "id": ident, "status": "extracted",
                        "pdf": pdf_path, "summary": rs,
                        "n_tworows": len(tworows),
                        "n_candidates": len(res["candidates"]),
                        "tried": [t[0] for t in tried]})

    out = {"topic": TOPIC, "inclusion_hints": INCLUSION_HINTS,
           "n_studies": len(studies),
           "n_included": n_incl,
           "n_excluded": len(screened) - n_incl,
           "n_downloaded": sum(1 for r in results if r.get("gate") == "pass_downloaded"),
           "results": results}
    sp = os.path.join(SEAM_DIR, "seam_result.json")
    with open(sp, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, default=str)
    print(f"[DONE] 写入 {sp}（通过门控={out['n_included']}，"
          f"拦截={out['n_excluded']}，实际下载成功={out['n_downloaded']}）")


if __name__ == "__main__":
    main()
