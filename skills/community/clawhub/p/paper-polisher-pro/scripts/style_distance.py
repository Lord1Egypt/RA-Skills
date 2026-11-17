#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""style_distance.py v2 — 文体特征工程(替代embedding相似度)

原理转变(2026-06-24 决策):
  v1 用 bge-m3 语义embedding算相似度 → 失败(量的主题相似度非文体, EVAL差距-0.2)
  v2 用与主题无关的低层文体特征 + 绝对阈值判定 → 成功(特征判别力d>1.8)

核心洞察: AI医学写作有语言无关的普遍习惯:
  - 偏短句(避免长复合句)
  - 标点单调(几乎只用逗号句号)
  - 句长均匀(缺少长短交错)
  - 高虚词密度(中文堆"的了是在")
人类真实文献相反。这些特征不依赖语料分布, 用绝对阈值即可判定。

中英文分别建模(句长特征跨语言不可比)。
依赖: 无(纯本地计算, 不需embedding/语料库/网络)
用法:
  python3 style_distance.py <文件>
  python3 style_distance.py <文件> --json
"""
import sys, json, re, statistics

CN_FUNC = re.compile(r'[的了是在和与也就都也还把将被让对从向]')
EN_FUNC = re.compile(r'\b(the|of|and|to|a|in|is|that|for|it|as|with|on|by|this|be|are|from|or|an|was)\b', re.IGNORECASE)


def is_chinese(text):
    cn = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
    return (cn / len(text) > 0.3) if text else False


def extract_features(text):
    """提取与主题无关的文体特征。返回 dict 或 None。"""
    text = text.strip()
    if len(text) < 50:
        return None
    cn = is_chinese(text)
    sents = [s.strip() for s in re.split(r'[。！？.!?]', text) if len(s.strip()) > 3]
    if len(sents) < 2:
        return None
    slens = [len(s) for s in sents]
    avg_len = statistics.mean(slens)
    len_cv = (statistics.stdev(slens) / avg_len) if avg_len and len(slens) > 1 else 0

    if cn:
        cn_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
        func_density = len(CN_FUNC.findall(text)) / cn_chars if cn_chars else 0
        puncts = set(re.findall(r'[，。！？、；：""\u2018\u2019（）—…]', text))
        lang = "zh"
        long_thresh, short_thresh = 25, 8
    else:
        words = len(text.split())
        func_density = len(EN_FUNC.findall(text)) / words if words else 0
        puncts = set(re.findall(r'[,;:!?\'"()\u2014]', text))
        lang = "en"
        long_thresh, short_thresh = 120, 35

    long_ratio = sum(1 for l in slens if l > long_thresh) / len(slens)
    short_ratio = sum(1 for l in slens if l < short_thresh) / len(slens)

    return {
        "lang": lang,
        "avg_sent_len": round(avg_len, 1),
        "len_cv": round(len_cv, 3),
        "func_density": round(func_density, 4),
        "punct_diversity": len(puncts),
        "long_sent_ratio": round(long_ratio, 3),
        "short_sent_ratio": round(short_ratio, 3),
        "n_sents": len(sents),
    }


def style_score_from_features(f):
    """基于文体特征 + 绝对阈值, 算 0-100 文体分(越高越像人类)。
    每个特征按"偏离AI习惯的程度"打分, 加权汇总。
    阈值依据EVAL: 真实文献 vs AI 的分布(见 measure_features 输出)。"""
    lang = f["lang"]
    score = 0.0
    reasons = []

    if lang == "zh":
        # 中文AI习惯: 短句(均长<20)、标点少(<3)、句长均匀(CV<0.3)、虚词堆(>0.08)
        # 1. 句长 (权重30): 人类医学综述均长40-80, AI<20
        al = f["avg_sent_len"]
        if al >= 40:
            score += 30; reasons.append(f"句长{al}(人类级)")
        elif al >= 25:
            score += 18; reasons.append(f"句长{al}(中等)")
        else:
            score += 5; reasons.append(f"句长{al}(偏短,AI特征)")
        # 2. 标点多样性 (权重25): 人类3+, AI<3
        pd = f["punct_diversity"]
        score += min(25, pd * 7); reasons.append(f"标点{pd}种")
        # 3. 句长变异 (权重20): 人类CV>0.4, AI<0.3
        cv = f["len_cv"]
        score += min(20, cv * 45); reasons.append(f"句长CV{cv}")
        # 4. 长句占比 (权重15): 人类多用长句
        lr = f["long_sent_ratio"]
        score += lr * 15; reasons.append(f"长句占比{lr}")
        # 5. 虚词密度 (权重10): AI偏高>0.08
        fd = f["func_density"]
        if fd > 0.10:
            score += 2; reasons.append(f"虚词密度{fd}(偏高)")
        else:
            score += 10; reasons.append(f"虚词密度{fd}(正常)")
    else:
        # 英文AI习惯: 短句(均长<80)、标点极少、句长均匀
        al = f["avg_sent_len"]
        if al >= 100:
            score += 30; reasons.append(f"句长{al}(人类级)")
        elif al >= 70:
            score += 18
        else:
            score += 5; reasons.append(f"句长{al}(偏短,AI特征)")
        pd = f["punct_diversity"]
        score += min(25, pd * 5)
        cv = f["len_cv"]
        score += min(20, cv * 30)
        lr = f["long_sent_ratio"]
        score += lr * 15
        fd = f["func_density"]
        score += 10 if 0.2 <= fd <= 0.35 else 4

    score = min(100, score)
    # 判定: <45 疑似AI, 45-60 需复核, >=60 接近人类
    if score >= 60:
        verdict = "human_like"
    elif score >= 45:
        verdict = "borderline"
    else:
        verdict = "ai_like"
    return round(score, 1), verdict, reasons


NOTICE = "ℹ️ 供学术写作自查与质量改进使用；不用于规避机构 AIGC 检测，请遵循所在机构的 AI 使用与披露政策。"


def style_distance(text, json_out=False):
    """计算文本的文体分。返回结构化结果。"""
    paras = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip() and len(p.strip()) >= 50]
    if not paras:
        paras = [text]

    def is_body_paragraph(para):
        """排除非正文段落(参考文献/blockquote/图片标签/纯英文标题列表),
        这些不应参与文体判定。"""
        s = para.strip()
        # 参考文献: 以"数字. "开头的引用条目
        if re.match(r'^\d+\.\s+[A-Z]', s):
            return False
        # blockquote 引用区
        if s.startswith('>'):
            return False
        # 图片标签
        if s.startswith('!['):
            return False
        # 文献来源声明(含 et al. / doi / PMID 且短)
        if ('et al' in s or 'doi:' in s or 'PMID' in s) and len(s) < 300:
            return False
        # 表格行/分隔线
        if s.startswith('|') or s.startswith('---') or s.startswith('==='):
            return False
        return True

    para_scores = []
    all_reasons = []
    for para in paras:
        if not is_body_paragraph(para):
            continue
        f = extract_features(para)
        if f:
            sc, vd, rs = style_score_from_features(f)
            para_scores.append(sc)
            all_reasons.append({"lang": f["lang"], "score": sc, "reasons": rs})
    if not para_scores:
        result = {"error": "无有效段落可评：未能提取到带句边界的正文段落。常见原因："
                   "①全文无句号/问号等句终符（单个超长复句无法计算句长方差）；"
                   "②段落均被判定为非正文（引用块/表格/代码）。请检查文本后重试。",
                "style_score": None}
        print(json.dumps(result, ensure_ascii=False) if json_out else result["error"])
        return result  # v4.5.0: 返回结构化结果（SDK pp_api.style_report 依赖）

    mean_score = sum(para_scores) / len(para_scores)
    min_score = min(para_scores)
    if mean_score >= 60:
        verdict = "human_like"
    elif mean_score >= 45:
        verdict = "borderline"
    else:
        verdict = "ai_like"

    result = {
        "style_score": round(mean_score, 1),
        "verdict": verdict,
        "min_paragraph_score": round(min_score, 1),
        "paragraphs_checked": len(para_scores),
        "paragraph_details": all_reasons[:3],
        "note": "文体特征工程版(v2);score越高越像人类写作;<45疑似AI;<60需复核",
    }
    result["integrity_notice"] = NOTICE
    if json_out:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"文体分: {result['style_score']}/100 ({verdict})")
        print(NOTICE)
        print(f"  检测段落: {result['paragraphs_checked']} | 最低段: {result['min_paragraph_score']}")
        for pd in all_reasons[:2]:
            print(f"  [{pd['lang']}] {pd['score']}: {'; '.join(pd['reasons'])}")
        if verdict == "ai_like":
            print("  ⚠️ 文体偏离人类写作, 疑似AI生成")
    return result  # v4.5.0: 返回结构化结果（SDK pp_api.style_report 依赖）


if __name__ == "__main__":
    import sys as _sys
    try:  # v3.5: 中文 Windows 默认 GBK 控制台会因 emoji/警示符崩溃 stdout——统一 UTF-8
        _sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        _sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    # v3.5: 用法守卫——此前 --help 会被当成文件名抛 FileNotFoundError
    import os
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print("style_distance.py — 文体特征工程 v2 (人类相似分 0-100)")
        print("用法: python3 style_distance.py <文件> [--json]")
        sys.exit(0)
    if len(sys.argv) < 2:
        print("用法: python3 style_distance.py <文件> [--json]")
        sys.exit(1)
    if not os.path.exists(sys.argv[1]):
        print(f"Error: File not found: {sys.argv[1]}", file=sys.stderr)
        sys.exit(2)
    text = open(sys.argv[1], encoding='utf-8', errors='replace').read()
    style_distance(text, json_out="--json" in sys.argv)
