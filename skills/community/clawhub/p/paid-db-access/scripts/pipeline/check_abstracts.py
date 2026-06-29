#!/usr/bin/env python3

"""

检查 enriched.json 的摘要完整性 + Tier 2 自动分流。



读取 _abstract_file 引用的文件内容验证摘要 ≥ 80 字符。

缺失率 > 15% → 阻断，自动生成 memory/tier2_task.json。

同时输出 _needs_tier2 标记的论文（来自 enrich_abstracts 自动标记）。

"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json, os, sys



from utils.pipeline_schema import check_version, report



import sys, os




def main():

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'memory/enriched.json'



    d = json.load(open(input_file, encoding='utf-8'))

    papers = d.get('papers', d if isinstance(d, list) else [])

    total = len(papers)



    # --- 版本检查 ---

    ver_issues = check_version(d, stage="enriched")

    if ver_issues:

        report(ver_issues, stage="check_abstracts")



    missing = []

    tier2_papers = []  # 自动标记的需要走 Tier 2 的论文



    for p in papers:

        af = p.get('_abstract_file', '')

        has_abstract = False



        if af and os.path.exists(af):

            content = open(af, encoding='utf-8').read()

            abs_idx = content.find('\nAbstract:\n')

            if abs_idx > -1:

                abs_text = content[abs_idx + len('\nAbstract:\n'):].strip()

                if len(abs_text) >= 80:

                    has_abstract = True



        if not has_abstract:

            missing.append(p)

            # 检查是否需要 Tier 2

            if p.get('_needs_tier2'):

                tier2_papers.append(p)



    rate = len(missing) / max(total, 1) * 100



    # ── 摘要完整性报告 ──

    print(f"[Check] {total - len(missing)}/{total} abstracts OK ({100 - rate:.0f}%)"

          f"  |  missing: {len(missing)} ({rate:.0f}%)")

    print(f"        auto-flagged _needs_tier2: {len(tier2_papers)} papers")



    if tier2_papers:

        print(f"\n  >> Tier 2 detail-page extraction needed:")

        for p in tier2_papers:

            dbs = ','.join(p.get('_source_db', ['?']))

            reason = p.get('_tier2_reason', 'unknown')

            title = p.get('title', '?')[:80]

            link = p.get('link', '')

            print(f"  [{dbs}] {title}")

            print(f"       reason: {reason}  |  link: {link}")



    # ── 阻断判断 ──

    if rate > 5:

        print(f"\n  BLOCKED: {rate:.0f}% > 5%, Tier 2 required")



        # 自动生成 tier2_task.json（含所有需 Tier 2 的论文）

        # 优先级：有 _needs_tier2 标记的 > 其余缺失的

        task_papers = tier2_papers.copy()

        for p in missing:

            if p not in task_papers:

                task_papers.append(p)



        task = {

            "total_missing": len(missing),

            "tier2_auto_flagged": len(tier2_papers),

            "papers": []

        }

        for p in task_papers:

            dbs = p.get('_source_db', ['?'])

            db = dbs[0] if isinstance(dbs, list) else str(dbs)

            task["papers"].append({

                "title": p.get("title", ""),

                "link": p.get("link", ""),

                "doi": p.get("doi", ""),

                "source_db": db,

                "_needs_tier2": bool(p.get("_needs_tier2")),

                "_tier2_reason": p.get("_tier2_reason", "missing_abstract"),

                "detail_extractor": f"extractors/{db}_detail.js",

            })



        task_path = 'memory/tier2_task.json'

        with open(task_path, 'w', encoding='utf-8') as f:

            json.dump(task, f, ensure_ascii=False, indent=2)

        print(f"  tier2_task.json written ({len(task_papers)} papers) -> {task_path}")



        sys.exit(1)

    else:

        print(f"\n  OK: {rate:.0f}% <= 5%, continue pipeline")

        sys.exit(0)





if __name__ == '__main__':

    main()

