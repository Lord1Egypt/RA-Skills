# -*- coding: utf-8 -*-
"""lgd-three-laws-auditor · LGD 三律合规自检器 v1.0
==================================================
把「凡自治之物：有籍·有证·有门禁」做成一套**可自评的标准 rubric**——
本工具即标准的载体：谁用三律词汇自评，谁就采用了我们的治理定义权（竞争优势）。

三律 rubric（本工具定义的标准）：
  LGD-I 有籍 REGISTERED   凡造必登：身份/版本/血缘/责任 四项登记
  LGD-II 有证 EVIDENCED   凡所行必有证据：六类证据工件齐备
  LGD-III 有门禁 GATED    凡演化必经门禁：触发/评审/放行/复盘 四道门

三种用法：
  --rubric               打印完整三律标准（可作对外治理文档）
  --system "描述"        对一段 AI 系统描述做启发式自评（标注"推测，请确认"，不编造结论）
  --answers file.json    按你填的答卷 {law:{checkpoint:yes|partial|no}} 出正式评分卡

零依赖（纯 stdlib）。© SynomosAI Governance Line · LGD-Powered
"""
import argparse, json, sys, re

# ── 三律标准 rubric（本工具定义，市场无同类定义器）──
RUBRIC = {
    "LGD-I 有籍 REGISTERED": {
        "key": "I",
        "desc": "凡造必登：AI 产物从出生起可溯源、可归属。",
        "checks": {
            "身份登记": "模型/产物有唯一 ID 与创造者署名",
            "版本登记": "模型/提示/知识库版本可溯、可回滚",
            "血缘登记": "输入来源、训练/检索数据可溯源",
            "责任登记": "权属人与问责主体明确",
        },
    },
    "LGD-II 有证 EVIDENCED": {
        "key": "II",
        "desc": "凡所行必有证据：六类证据工件齐备、可重放。",
        "checks": {
            "01 身份证据": "护照/登记文件/DID",
            "02 数据证据": "数据集指纹与来源",
            "03 验证证据": "评测报告/指标带 CI/文献",
            "04 行为边界证据": "红线/人机边界/中止规程",
            "05 变更证据": "变更日志与评估记录",
            "06 签发证据": "门禁结论/签发人/时间戳",
        },
    },
    "LGD-III 有门禁 GATED": {
        "key": "III",
        "desc": "凡演化必经门禁：变更与放行受控。",
        "checks": {
            "触发门禁": "变更/上线前有评估触发条件",
            "评审门禁": "有权限边界评审（allow/deny/warn）",
            "放行门禁": "通过才放行，失败阻断",
            "复盘门禁": "事后复盘与回滚机制",
        },
    },
}

# 启发式关键词（仅作"推测提示"，绝不冒充结论）
HINTS = {
    "身份登记": ["署名", "作者", "owner", "creator", "id", "标识", "模型"],
    "版本登记": ["版本", "version", "commit", "快照", "回滚"],
    "血缘登记": ["来源", "source", "检索", "rag", "训练数据", "数据集"],
    "责任登记": ["权属", "主体", "负责", " accountability", "问责", "责任"],
    "01 身份证据": ["护照", "passport", "did", "登记文件"],
    "02 数据证据": ["数据指纹", "数据集", "哈希", "hash"],
    "03 验证证据": ["评测", "指标", "benchmark", "文献", "ci", "日志", "log"],
    "04 行为边界证据": ["红线", "边界", "中止", "kill switch", "人机"],
    "05 变更证据": ["变更日志", "changelog", "评估记录"],
    "06 签发证据": ["签发", "门禁结论", "时间戳", "签发人"],
    "触发门禁": ["门禁", "gate", "触发", "评估条件"],
    "评审门禁": ["审批", "permission", "权限", "评审", "allow", "deny"],
    "放行门禁": ["放行", "阻断", "block", "通过才"],
    "复盘门禁": ["复盘", "回滚", "rollback", "事后"],
}

VAL = {"yes": 1.0, "partial": 0.5, "no": 0.0, "unknown": 0.0}


def print_rubric():
    print("# LGD 三律合规标准（凡自治之物：有籍·有证·有门禁）\n")
    for law, v in RUBRIC.items():
        print(f"## {law}\n{v['desc']}\n")
        for c, d in v["checks"].items():
            print(f"- [ ] **{c}**：{d}")
        print()


def heuristic_scan(text):
    """返回 {law:{checkpoint:'partial'/'unknown'}}，仅提示。"""
    low = text.lower()
    out = {}
    for law, v in RUBRIC.items():
        out[law] = {}
        for c in v["checks"]:
            hits = [k for k in HINTS.get(c, []) if k.lower() in low]
            out[law][c] = "partial" if hits else "unknown"
    return out


def score(answers):
    rows = []
    law_scores = {}
    for law, v in RUBRIC.items():
        a = answers.get(law, {})
        tot = len(v["checks"])
        s = 0.0
        for c in v["checks"]:
            st = a.get(c, "unknown")
            s += VAL.get(st, 0.0)
            rows.append((law, c, st))
        law_scores[law] = round(100 * s / tot) if tot else 0
    overall = round(sum(law_scores.values()) / len(law_scores)) if law_scores else 0
    return rows, law_scores, overall


def gaps(law_scores):
    g = []
    for law, sc in law_scores.items():
        if sc < 100:
            g.append(f"{law}（{sc}分）— 未达标，请补齐对应证据工件/登记项")
    return g


def fmt_markdown(rows, law_scores, overall, source):
    L = ["# LGD 三律合规自检报告", f"> 来源：{source}\n"]
    L.append(f"## 总评：**{overall}/100**\n")
    for law, sc in law_scores.items():
        L.append(f"- **{law}**：{sc}/100")
    L.append("\n## 逐条明细\n")
    cur = None
    for law, c, st in rows:
        if law != cur:
            cur = law
            L.append(f"### {cur}")
        tag = {"yes": "✓ 达标", "partial": "◐ 部分(推测/待确认)", "no": "✗ 缺失", "unknown": "? 未评估"}[st]
        L.append(f"- [{tag}] {c}")
    g = gaps(law_scores)
    L.append("\n## 改进项（补齐即加固竞争优势）\n")
    L += [f"- {x}" for x in g] or ["- 三项全部达标，竞争优势闭环完整。"]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="LGD 三律合规自检器（有籍·有证·有门禁）")
    ap.add_argument("--rubric", action="store_true", help="打印完整三律标准")
    ap.add_argument("--system", help="AI 系统/工作流描述文本（启发式自评）")
    ap.add_argument("--answers", help="答卷 JSON 路径 {律:{检查项:yes|partial|no}}")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    a = ap.parse_args()

    if a.rubric:
        print_rubric()
        return
    if a.answers:
        try:
            answers = json.load(open(a.answers, encoding="utf-8-sig"))
        except Exception as e:
            print(f"[!] 答卷读取失败：{e}", file=sys.stderr); sys.exit(2)
        src = f"答卷 {a.answers}"
    elif a.system:
        answers = heuristic_scan(a.system)
        src = "启发式自评（关键词推测，请人工确认每项）"
    else:
        print("[!] 用法：--rubric ｜ --system \"描述\" ｜ --answers file.json")
        print("    本工具即 LGD 三律标准载体；先 --rubric 看标准，再自评。")
        sys.exit(1)

    rows, law_scores, overall = score(answers)
    if a.json:
        print(json.dumps({"overall": overall, "law_scores": law_scores,
                          "rows": [{"law": l, "check": c, "status": s} for l, c, s in rows]},
                         ensure_ascii=False, indent=2))
    else:
        print(fmt_markdown(rows, law_scores, overall, src))


if __name__ == "__main__":
    main()
