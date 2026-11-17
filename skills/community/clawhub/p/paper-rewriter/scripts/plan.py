# -*- coding: utf-8 -*-
"""plan.py — 句级改写优先级计划（v2.2.0）。

回答「下一句改哪里」：把整篇扫描降为逐句风险排序，输出可直接执行的深改
队列——每句带章节归属、命中类别、处理原则、贡献点数，并给出「改完前 K 句
之后的预估分」线性投影。供 agent 深改与作者自查使用。

口径与诚实声明：
- 逐句贡献 = 句内各类别 weight×count 近似（同类同权口径）；跨句结构信号
  （排比、连接词密度、节奏）无法落到单句，单列为「全文级信号」。
- 预估投影按线性近似重算，仅供排序与预算参考，不是承诺分数，更不是任何
  外部检测器的分数。

用法:
    python scripts/plan.py draft.txt
    python scripts/plan.py draft.md --top 20 -o plan.md
    cat draft.txt | python scripts/plan.py -
    python scripts/plan.py draft.txt --json > plan.json

退出码: 0 成功 | 2 用法/文件错误
"""

import argparse
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hxt_core

SECTION_LABELS = {
    "abstract": "摘要", "introduction": "引言", "methods": "方法",
    "results": "结果", "discussion": "讨论", "conclusion": "结论",
    "references": "参考文献", "preamble": "题头", "body": "正文",
}

_FALLBACK_ADVICE = {
    "model_artifact_zh": "模型残留 bug：直接删除或换成真实句（transform.py 可自动清理）",
    "model_artifact_en": "Model artifact: delete outright (transform.py can auto-clean)",
    "chatbot_zh": "聊天客套句：整句删除，改为直接陈述",
    "chatbot_en": "Chatbot filler: remove the sentence entirely",
    "cutoff_zh": "知识截止声明：整句删除（论文不需要它）",
    "cutoff_en": "Knowledge-cutoff line: remove it",
    "zh_punct": "半角标点混排：全角化（transform.py 可自动处理；参考文献行已豁免）",
}

# 单句扫描的实用上限（逐句 scan 是 O(句数×模式数)，超过建议分章节处理）
MAX_PLAN_CHARS = 2_000_000


def locate_sentences(text):
    """按行内分句，返回 [(sentence, offset)]。句是原文精确子串：先在行内定位
    stripped 起点，再逐句用游标在 stripped 上定位；定位失败的句跳过
    （宁可少列一句，不标错位置）。"""
    out = []
    cursor = 0
    for ln in text.split("\n"):
        base = cursor
        cursor += len(ln) + 1
        stripped = ln.strip()
        if not stripped:
            continue
        lead = ln.find(stripped)
        pos = 0
        for sent in hxt_core.split_sentences(stripped):
            idx = stripped.find(sent, pos)
            if idx == -1:
                continue
            pos = idx + len(sent)
            out.append((sent, base + lead + idx))
    return out


def section_at(sections, offset):
    for key, s, e in sections:
        if s <= offset < e:
            return key
    return "body"


def sentence_pts(r):
    return sum(c["weight"] * c["count"] for c in r["categories"].values())


def advice_str(cid):
    """_ADVICE 值是 (名称, 建议) 元组；统一转成「名称：建议」字符串。"""
    v = hxt_core._ADVICE.get(cid) or _FALLBACK_ADVICE.get(cid)
    if v is None:
        v = (hxt_core._ADVICE.get("en_vocab") if cid.startswith("en") else None) \
            or "按 style_guide 对应条目深改"
    if isinstance(v, (tuple, list)):
        return "：".join(str(x) for x in v)
    return str(v)


def build_handoff(rows, sections, source="", lang=None):
    """v3.0.0 深改交接块：把 P0 队列变成执行改写 agent 可直接照做的逐句指令单。

    评审反馈（completeness/summary）指出深改环节依赖外部 agent 而工具未把
    交接做透——本函数把「哪句、改什么、守什么、改完怎么验」一次给全。
    lang（v4.2.0，评审 P2-10）：英文稿指令单首选锚 style_guide_en.md，
    不再让 agent 从中文锚里猜；None=由 build_queue 的全文语言自动判。"""
    guide = "references/style_guide_en.md" if lang == "en" else "references/style_guide_zh.md"
    guide_note = ("" if lang == "en"
                  else "\n（英文稿请改用 references/style_guide_en.md）")
    lines = ["## 深改交接块（复制给执行改写的 agent）", "",
             "```text",
             "守卫铁律：数字/量纲/DOI/PMID/术语/专有名词/引文内容一律原样保留；",
             "每完成 3-5 句运行一次 verify，出现任何 GUARD/ERROR 立即回滚该句。",
             "处理原则详见 %s，%s" % (guide, guide_note),
             "流程细节见 references/deep_rewrite_guide.md。"]
    for i, r in enumerate(rows, 1):
        sec = SECTION_LABELS.get(section_at(sections, r["off"]), "正文")
        ops = "；".join(dict.fromkeys(advice_str(cid) for cid in r["cats"]))
        lineno = r.get("line")
        loc = ("（原文 L%d 行）" % lineno) if lineno else ""
        lines.append("")
        lines.append("%d. [%s]%s %s" % (i, sec, loc, r["sent"]))
        lines.append("   操作：%s" % ops)
    lines += ["", "全部改完后运行（任一 FAIL 都不得交付）：",
              "  python scripts/verify.py <原文件> <改后文件>",
              "  python scripts/stylecheck.py <改后文件> --compare <原文件>",
              "提示：以上交接块也可由一句命令随管线直接产出——",
              "  python scripts/pipeline.py <原文件> -o <改后文件> --handoff <本文件>",
              "```"]
    return "\n".join(lines)


def build_queue(text, lang=None, profile="academic", source_ext=".txt", top=15):
    """v3.8.0 抽取：逐句风险排序核心（供 pipeline --handoff 复用；plan 主流程
    保持独立不动）。返回 (top_rows, sections, full)；行结构与 --json 的 top
    一致（另带 sent/off 原文与偏移）。超 MAX_PLAN_CHARS 抛 ValueError。"""
    if len(text) > MAX_PLAN_CHARS:
        raise ValueError(
            "文本超过 %d 字符，逐句扫描成本过高——请按章节拆分后分别生成交接块"
            % MAX_PLAN_CHARS)
    full = (hxt_core.scan_chunked(text, lang=lang, profile=profile,
                                  source_ext=source_ext)
            if len(text) > 800_000 else
            hxt_core.scan(text, lang=lang, profile=profile, source_ext=source_ext))
    sections = hxt_core.detect_sections(text)
    sents = locate_sentences(text)
    if not sents:
        return [], sections, full
    rows = []
    for sent, off in sents:
        r = hxt_core.scan(sent, lang=full["lang"], profile=profile,
                          source_ext=source_ext)
        pts = sentence_pts(r)
        if pts > 0:
            rows.append({"sent": sent, "off": off, "pts": round(pts, 2),
                         "cats": {cid: c["count"]
                                  for cid, c in r["categories"].items() if c["count"]},
                         "labels": {cid: c["label"]
                                    for cid, c in r["categories"].items() if c["count"]}})
    # v5.1.0：句级行号锚（handoff 指令单「原文 L{行}」）——off → 行号一次换算
    for _r in rows:
        if isinstance(_r.get("off"), int):
            _r["line"] = text.count("\n", 0, _r["off"]) + 1
    rows.sort(key=lambda x: (-x["pts"], x["off"]))
    return rows[:max(1, top)], sections, full


def main():
    ap = argparse.ArgumentParser(
        description="句级改写优先级计划：逐句风险排序 + 预算投影（本地启发式口径）")
    ap.add_argument("file", help="输入文件（.txt/.md/.docx/.pdf；- 读 stdin）")
    ap.add_argument("--lang", choices=["zh", "en", "auto"], default="auto")
    ap.add_argument("--profile", choices=["academic", "general"], default="academic")
    ap.add_argument("--top", type=int, default=15, help="P0 队列长度（默认 15）")
    ap.add_argument("-o", "--output", help="把 markdown 计划写到该文件（仅显式路径）")
    ap.add_argument("--json", action="store_true", help="输出 JSON（供 agent 消费）")
    ap.add_argument("--handoff", action="store_true",
                    help="输出深改交接块（逐句操作指令单，供执行改写的 agent 直接照做）")
    ap.add_argument("--pdf-min-confidence", choices=["高", "中", "低"], default="中",
                 help="PDF 最低置信度门闸（v3.8.0，与 detect/pipeline 同款同缺省）："
                      "低于阈值拒收；「低」恢复仅标注旧行为")
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + hxt_core.__version__)
    args = ap.parse_args()

    try:
        if args.file == "-":
            text = sys.stdin.read()
            source_ext = ".txt"
        else:
            source_ext = os.path.splitext(args.file)[1].lower()
            if source_ext == ".pdf":
                # 门闸同款（v3.8.0 评测员 P0：宣称支持 .pdf 就不能旁路安全门——
                # 乱码 PDF 进逐句队列会把深改 agent 引到乱码上）
                text, _pm = hxt_core.read_text_ex(args.file)
                if _pm and not hxt_core.pdf_confidence_ok(
                        _pm.get("confidence"), args.pdf_min_confidence):
                    raise hxt_core.pdf_gate_error(
                        _pm.get("confidence"), args.pdf_min_confidence,
                        notes=_pm.get("notes"))
            else:
                text = hxt_core.read_text(args.file)
        if len(text) > MAX_PLAN_CHARS:
            raise ValueError(
                "文本超过 %d 字符，逐句扫描成本过高——请按章节拆分后分别执行 plan"
                % MAX_PLAN_CHARS)
        if not text.strip():
            raise ValueError("输入为空")

        lang = None if args.lang == "auto" else args.lang
        big = len(text) > 800_000
        full = (hxt_core.scan_chunked(text, lang=lang, profile=args.profile,
                                      source_ext=source_ext) if big
                else hxt_core.scan(text, lang=lang, profile=args.profile,
                                   source_ext=source_ext))
        eff_lang = full["lang"]
        sections = hxt_core.detect_sections(text)
        sents = locate_sentences(text)
        if not sents:
            raise ValueError("未能分句——请检查输入是否为可读文本")

        # 逐句风险
        rows = []
        sent_cat_totals = {}
        for sent, off in sents:
            r = hxt_core.scan(sent, lang=eff_lang, profile=args.profile,
                              source_ext=source_ext)
            pts = sentence_pts(r)
            for cid, c in r["categories"].items():
                sent_cat_totals[cid] = sent_cat_totals.get(cid, 0) + c["count"]
            if pts > 0:
                rows.append({"sent": sent, "off": off, "pts": round(pts, 2),
                             "cats": {cid: c["count"]
                                      for cid, c in r["categories"].items()
                                      if c["count"]},
                             "labels": {cid: c["label"]
                                        for cid, c in r["categories"].items()
                                        if c["count"]}})
        # v5.1.0：句级行号锚（main 路径与 build_queue 同款换算）
        for _r in rows:
            if isinstance(_r.get("off"), int):
                _r["line"] = text.count("\n", 0, _r["off"]) + 1
        rows.sort(key=lambda x: (-x["pts"], x["off"]))
        top = rows[:max(1, args.top)]

        # 全文级信号：全文命中数 > 逐句命中数合计（跨句结构信号）
        fulltext_signals = []
        for cid, c in full["categories"].items():
            if c["count"] > sent_cat_totals.get(cid, 0):
                fulltext_signals.append({
                    "id": cid, "label": c["label"], "count": c["count"],
                    "note": "跨句/结构信号，无法归到单句——按 style_guide 全局处理"})

        # 预算投影：改完前 K 句后的线性近似重算（K 去重保序；
        # 小文档三个 K 可能坍缩——补一个中位 K 保证至少两个投影点）
        k_cands = sorted({min(5, len(top)), min(10, len(top)), len(top)})
        if len(k_cands) == 1:
            k_cands = sorted({max(1, len(top) // 2), k_cands[0]})
        projections = []
        for k in k_cands:
            if k <= 0:
                continue
            adj = copy.deepcopy(full["categories"])
            for row in top[:k]:
                for cid, n in row["cats"].items():
                    if cid in adj:
                        adj[cid]["count"] = max(0, adj[cid]["count"] - n)
            adj_pts = sum(c["weight"] * c["count"] for c in adj.values())
            stats2 = copy.deepcopy(full["stats"])
            score2, level2, _ = hxt_core._score(adj_pts, stats2, full["units"],
                                                adj, eff_lang)
            projections.append({"fix_top_k": k, "projected_score": score2,
                                "projected_level": level2})

        result = {
            "meta": {
                "source": args.file, "lang": eff_lang, "score": full["score"],
                "level": full["level"], "units": full["units"],
                "sections": [{"key": k, "label": SECTION_LABELS.get(k, k),
                              "start": s, "end": e} for k, s, e in sections],
                "sentence_count": len(sents),
                "disclaimer": "本地启发式风格诊断的线性近似投影，非外部检测分数，"
                              "不构成对任何改写效果的承诺",
            },
            "top": [{
                "rank": i + 1,
                "section": SECTION_LABELS.get(
                    section_at(sections, r["off"]), "正文"),
                "offset": r["off"],
                "pts": r["pts"],
                "hits": [{"id": cid, "label": r["labels"][cid], "count": n}
                         for cid, n in r["cats"].items()],
                "advice": [advice_str(cid) for cid in r["cats"]],
                "excerpt": (r["sent"][:80] + "…") if len(r["sent"]) > 80 else r["sent"],
            } for i, r in enumerate(top)],
            "fulltext_signals": fulltext_signals,
            "projections": projections,
        }

        if args.handoff:
            result["handoff"] = build_handoff(top, sections, source=args.file,
                                              lang=full.get("lang"))

        if args.json:
            out = json.dumps(result, ensure_ascii=False, indent=2)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(out)
                print("JSON 计划已写入 %s" % args.output)
            else:
                print(out)
            return

        # markdown 计划
        m = result["meta"]
        lines = ["# 改写优先级计划：%s" % (m["source"] or "stdin"), ""]
        lines.append("> 本地启发式风格诊断的线性近似投影；不是外部检测分数，"
                     "不构成改写效果承诺。")
        lines.append("")
        lines.append("## 文档概况")
        lines.append("")
        lines.append("- 风格特征分 %d/100（%s）｜语言 %s｜评分单元 %s"
                     % (m["score"], m["level"], m["lang"], m["units"]))
        sec_str = "、".join("%s" % s["label"] for s in m["sections"][:8])
        lines.append("- 章节结构：%s（共 %d 句）" % (sec_str or "未识别", m["sentence_count"]))
        lines.append("")
        if result["fulltext_signals"]:
            lines.append("## 全文级信号（不落在单句）")
            lines.append("")
            for s in result["fulltext_signals"]:
                lines.append("- [%s] ×%d：%s" % (s["label"], s["count"], s["note"]))
            lines.append("")
        lines.append("## P0 改写队列（Top %d，按贡献降序）" % len(result["top"]))
        lines.append("")
        for t in result["top"]:
            hits = "、".join("%s ×%d" % (h["label"], h["count"]) for h in t["hits"])
            lines.append("### %d. [%s] 贡献 %.1f 点｜%s"
                         % (t["rank"], t["section"], t["pts"], hits))
            lines.append("")
            lines.append("> %s" % t["excerpt"].replace("\n", " "))
            lines.append("")
            for a in dict.fromkeys(t["advice"]):
                lines.append("- 处理原则：%s" % a)
            lines.append("")
        lines.append("## 预算投影")
        lines.append("")
        lines.append("| 改完前 K 句 | 预估分 | 档位 |")
        lines.append("|---|---|---|")
        for p in result["projections"]:
            lines.append("| K=%d | %d | %s |"
                         % (p["fix_top_k"], p["projected_score"],
                            p["projected_level"]))
        lines.append("")
        lines.append("## 改写后自检")
        lines.append("")
        lines.append("1. `python scripts/verify.py 原稿 新稿` —— 数字/引用/术语守卫（exit 0 才算过）")
        lines.append("2. `python scripts/compare.py 原稿 -o 新稿` —— 前后对比")
        lines.append("3. 改写时的误报词：`python scripts/learn_guards.py from-text 词 样本` 固化守卫")
        lines.append("")
        lines.append("---")
        lines.append("> 本文档由 paper-rewriter 生成"
                     "（[GitHub](https://github.com/docsor1212/paper-rewriter) · "
                     "[SkillHub](https://skillhub.cn/skills/indiv-sorsor/paper-rewriter)）"
                     "· 觉得有用欢迎 Star / 收藏")
        lines.append("")
        if args.handoff:
            lines.append(build_handoff(top, sections, source=args.file,
                                       lang=full.get("lang")))
            lines.append("")
        out_text = "\n".join(lines)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(out_text)
            print("计划已写入 %s" % args.output)
        else:
            print(out_text)
    except (OSError, ValueError) as e:
        print("错误: %s" % e, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    hxt_core.cli_entry(main)
