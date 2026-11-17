# -*- coding: utf-8 -*-
"""赛事作品原创性查重器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：UIBC 原创性规范 + 学术不端界定
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "originality-check", "version": "1.1.0", "args": [{"name": "submission_hash", "help": "作品指纹（必填，缺失时报错 rc=2）", "required": False}, {"name": "known_hashes", "help": "历史/公开库指纹 JSON 字符串列表（缺省按空库从严告警）", "required": False}]}

class GateError(Exception):
    pass

def classify_originality(args):
    """作品与历史/公开库指纹相似度查重（原创性核验）。规则源：UIBC 原创性规范 + 学术不端界定。"""
    sub_hash = args.get('submission_hash') or ''
    known = args.get('known_hashes') or '[]'

    def _sim(h1, h2):
        n = min(len(h1), len(h2))
        if n == 0:
            return 0.0
        same = sum(1 for i in range(n) if h1[i] == h2[i])
        return same / max(len(h1), len(h2))

    if not sub_hash:
        raise GateError("缺少必要参数：submission_hash(作品指纹) 必填")
    try:
        corpus = json.loads(known) if isinstance(known, str) else known
    except Exception:
        # 指纹库 JSON 非法时直接判非法，不静默按空库输出「无重复」的宽松结论
        raise GateError("known_hashes 须为合法 JSON 字符串列表（如 [\"sha256:aaa111\"]）")
    if not isinstance(corpus, list) or not all(isinstance(h, str) for h in corpus):
        raise GateError("known_hashes 须为字符串列表（如 [\"sha256:aaa111\"]）")
    warnings = []
    if not corpus:
        # 从严推定：指纹库为空时查重无对照，「无重复」结论不可靠，明示告警
        warnings.append(
            "known_hashes 为空（未提供对照指纹库）：本输出「无重复」不可靠，"
            "请提供历史/公开库指纹后复核；不静默按原创通过处理。")
    exact = sub_hash in corpus
    sim = 0.0
    if not exact and corpus:
        sim = max(_sim(sub_hash, h) for h in corpus)
    is_dup = exact or sim >= 0.85
    matches = [h for h in corpus if h == sub_hash or _sim(sub_hash, h) >= 0.85]
    if is_dup:
        warnings.append("命中高相似作品，建议人工复核原创性")
    return {"similarity": round(sim, 3) if not exact else 1.0, "is_duplicate": is_dup,
            "exact_match": exact, "matches": matches[:5],
            "warnings": warnings,
            "notes": ["相似度为示意算法，正式查重须用 MinHash/SimHash + 人工判定", "最终原创性裁定归组委会"],
            "evidence": ["UIBC 原创性规范"]}


def _run(args):
    res = classify_originality(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="originality-check", description="赛事作品原创性查重器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR（默认）")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    AIGC = {"standard": "GB 45438-2025", "is_generated": True, "generator": META["slug"] + "@SynomosAI",
            "content_type": "decision_support_output",
            "label_note": "标识口径待核：输出由确定性规则代码计算，规则文本为 AI 辅助撰写",
            "disclaimer": "决策支持非权威结论，须人工复核"}
    if ns.demo:
        demos = [{"submission_hash": "sha256:aaa111", "known_hashes": "[\"sha256:aaa111\",\"sha256:bbb222\"]"}, {"submission_hash": "sha256:new999", "known_hashes": "[\"sha256:aaa111\",\"sha256:bbb222\"]"}, {"submission_hash": "sha256:new999"}]
        allok = True
        out_list = []
        for d in demos:
            try:
                res, rc = _run(dict(d))
                out_list.append({"tool": META["slug"], "input": d, "result": res, "rc": rc, "aigc_mark": AIGC})
            except GateError as e:
                allok = False
                out_list.append({"tool": META["slug"], "input": d, "errors": [str(e)], "rc": 2, "aigc_mark": AIGC})
        print(json.dumps(out_list, ensure_ascii=False, indent=2))
        sys.exit(0 if allok else 2)
    args = {k: getattr(ns, k) for k in argnames}
    try:
        res, rc = _run(args)
    except GateError as e:
        ir = {"tool": META["slug"], "version": META["version"], "input": args, "errors": [str(e)], "rc": 2, "aigc_mark": AIGC}
        print(json.dumps(ir, ensure_ascii=False, indent=2))
        sys.exit(2)
    ir = {"tool": META["slug"], "version": META["version"], "input": args, "result": res, "rc": rc, "aigc_mark": AIGC}
    print(json.dumps(ir, ensure_ascii=False, indent=2))
    sys.exit(rc)

if __name__ == "__main__":
    main()
