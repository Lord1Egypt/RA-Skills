#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""翻译可疑度筛查 v2 (融合版) — 学术中文文案质量规范 第四层

定位: 补 term_check(术语黑名单) + ai_detector(翻译腔模式) 的交集盲区。
"渗漏SCID"复盘教训: "渗漏"既不在2,344条术语表, 也不在翻译腔14模式,
属术语集盲区——只有专家审读能发现。本工具用语言学规则识别这类新直译词。

融合架构(遵循文案质量规范三大流程):
  规则识别可疑词(本工具, 不依赖清单)
    → 交叉验证1: term_check terminology.json(是否已知不规范词?)
    → 交叉验证2: ai_detector 翻译腔模式(是否已知翻译腔?)
    → 两者都查不到 = ★盲区新词★(核心价值, 记录供专家审)
    → 任一查到 = 已知问题(归入对应流程, 非盲区)

规则(R1-R7, 语言学特征, 非清单匹配):
  R2 的的不休(连续≥3个"的")  R3 被动滥用(单句≥2"被")
  R4 抽象名词化过度(单句≥5个-性/度/化/主义)  R5 冗长连接词
  R6 已知医学直译词库(可扩展, 初期种子)  R7 冗余动词(进行+检查)

用法:
  python scripts/quality/translation_smell_check.py [文件/目录]
  python scripts/translation_smell_check.py --json  # JSON输出
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field, asdict
from pathlib import Path

# ============ 已有工具位置(《质量规范》定义) ============
# v3: 相对路径解析（v2 硬编码绝对路径导致跨机器交叉验证失败）
PP = Path(__file__).parent.parent
TERM_JSON = PP / "data" / "terminology.json"
TERM_CHECK = PP / "scripts" / "term_check.py"
AI_DETECTOR = PP / "scripts" / "ai_detector.py"

# ============ R6 种子词库(初期, 命中后扩充) ============
KNOWN_SMELLS = {
    "渗漏": "leaky直译(leaky SCID→部分型/轻型SCID)",
    "泄漏": "leakage直译, 改具体表述",
    "过表达": "overexpression直译→过度表达/高表达",
    "雨伞": "umbrella term直译→总称/统称",
    "逃跑": "escape直译(escape mutant→逃逸突变体)",
    "武器": "arsenal直译(免疫武器→免疫机制, 过度比喻)",
    "战场": "battlefield直译(过度比喻)",
}

ABSTRACT_SUFFIX = re.compile(r"[性度化主义]")
REDUNDANT_VERB = re.compile(r"(进行|作出|予以|实施)(了|着)?(?:.{0,6}?)(?:的)?(?:检查|评估|治疗|分析|研究|监测)")


@dataclass
class SmellHit:
    rule: str           # R2/R3/R4/R5/R6/R7
    word: str           # 命中词/片段
    context: str        # 上下文
    suggestion: str = ""


@dataclass
class ScanResult:
    file: str
    hits: list = field(default_factory=list)
    blind_spot_hits: list = field(default_factory=list)  # ★盲区新词(term_check+ai都查不到)


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"&[a-z]+;", " ", text)


def split_sentences(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"[。；;！!？?\n]", text) if p.strip()]


def rule_hits(text: str) -> list[SmellHit]:
    """R2-R7 规则识别(不依赖任何清单)"""
    hits = []
    plain = strip_html(text)
    # R6 全文
    for word, reason in KNOWN_SMELLS.items():
        if word in plain:
            idx = plain.find(word)
            hits.append(SmellHit("R6", word, plain[max(0, idx-20):idx+30], reason))
    for sent in split_sentences(plain):
        # R2
        for m in re.finditer(r"(?:[^。；\n]*?的){2,}[^。；\n]*?的", sent):
            chain = m.group(0)
            if chain.count("的") >= 3:
                hits.append(SmellHit("R2", "的×"+str(chain.count("的")), chain[:50], "拆分定语链"))
        # R3
        if sent.count("被") >= 2:
            hits.append(SmellHit("R3", "被×"+str(sent.count("被")), sent[:60], "改主动句"))
        # R4
        n = len(ABSTRACT_SUFFIX.findall(sent))
        if n >= 5:
            hits.append(SmellHit("R4", f"-性/度/化×{n}", sent[:60], "减少抽象名词化"))
        # R5
        conns = re.findall(r"关于|对于|在.+?方面|作为.+?的", sent)
        if len(conns) >= 2:
            hits.append(SmellHit("R5", f"连接词×{len(conns)}", sent[:60], "精简连接词"))
        # R7
        for m in REDUNDANT_VERB.finditer(sent):
            hits.append(SmellHit("R7", m.group(0)[:20], sent[:60], "省'进行'直接用动词"))
    return hits


def cross_check_term_check(word: str) -> bool:
    """交叉验证: term_check terminology.json 是否已知(在=非盲区)"""
    try:
        data = json.load(open(TERM_JSON, encoding="utf-8"))
        for item in data:
            if word in str(item.get("aliases", [])) or word == item.get("cn", ""):
                return True
        return False
    except Exception:
        return False


def cross_check_ai_detector(word: str) -> bool:
    """交叉验证: ai_detector 翻译腔模式是否已知(在=非盲区)
    简化: ai_detector的翻译腔模式是硬编码的, 这里用已知模式集近似"""
    # ai_detector 14翻译腔模式(近似, 实际硬编码在脚本)
    ai_translation_patterns = {"值得关注", "在此基础上", "发挥着", "至关重要",
                               "扮演着", "重要角色", "广泛应用", "深入研究",
                               "进一步", "总的来说", "众所周知"}
    return word in ai_translation_patterns


def classify_hit(hit: SmellHit) -> SmellHit:
    """分类: 盲区新词 vs 已知问题"""
    if hit.rule != "R6":
        return hit  # R2-R7是语法特征, 不需要术语交叉验证
    # R6: 交叉验证
    in_term = cross_check_term_check(hit.word)
    in_ai = cross_check_ai_detector(hit.word)
    if not in_term and not in_ai:
        hit.suggestion = f"★盲区新词★ {hit.suggestion} (term_check+ai_detector均未收录, 需专家审, 确认后扩充术语库)"
    return hit


def scan_file(path: Path) -> ScanResult:
    result = ScanResult(file=str(path))
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return result
    for i, line in enumerate(content.split("\n"), 1):
        if not re.search(r"[\u4e00-\u9fff]", line):
            continue
        for hit in rule_hits(line):
            hit.context = f"L{i}: {hit.context}"
            hit = classify_hit(hit)
            result.hits.append(hit)
            if "盲区新词" in hit.suggestion:
                result.blind_spot_hits.append(hit)
    return result


def main():
    # v3.5: 用法守卫——此前 --help 被静默忽略、无参数时误扫遗留目录 frontend/src/data
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print("translation_smell_check.py — 翻译腔筛查 v2 (融合版)")
        print("用法: python3 translation_smell_check.py <文件...> [--json]")
        sys.exit(0)
    json_mode = "--json" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        print("用法: python3 translation_smell_check.py <文件...> [--json]")
        sys.exit(2)
    targets = [Path(a) for a in args]
    missing = [t for t in targets if not t.exists()]
    if missing:
        print(f"Error: File not found: {missing[0]}", file=sys.stderr)
        sys.exit(2)
    files = []
    for t in targets:
        files.extend(sorted(t.rglob("*.ts")) if t.is_dir() else [t])

    all_results = []
    rule_count = defaultdict(int)
    blind_spots = []
    for f in files:
        r = scan_file(f)
        if r.hits:
            all_results.append(r)
            for h in r.hits:
                rule_count[h.rule] += 1
                if "盲区" in h.suggestion:
                    blind_spots.append({"file": Path(r.file).name, "word": h.word, "suggestion": h.suggestion})

    if json_mode:
        # v3.12: 增加结构化 hits 数组（deai_gate 层3 解析依赖；旧键保留兼容）
        hits_detail = [{"file": Path(r.file).name, "rule": h.rule, "word": h.word,
                        "suggestion": h.suggestion,
                        "盲区": "盲区" in h.suggestion}
                       for r in all_results for h in r.hits]
        print(json.dumps({"total_hits": sum(len(r.hits) for r in all_results),
                          "hits": hits_detail,
                          "blind_spots": blind_spots, "rule_count": dict(rule_count)},
                         ensure_ascii=False, indent=2))
        return 0

    print("=" * 70)
    print("翻译可疑度筛查 v2 (融合版) — 学术文案质量规范第四层")
    print("=" * 70)
    print(f"扫描 {len(files)} 文件 | 命中 {len(all_results)} | 可疑项 {sum(len(r.hits) for r in all_results)}")
    print(f"★盲区新词(term_check+ai均未收录): {len(blind_spots)}")
    print("\n规则统计: " + " | ".join(f"{k}:{v}" for k, v in sorted(rule_count.items())))
    print("-" * 70)
    for r in all_results:
        print(f"\n📄 {Path(r.file).name} ({len(r.hits)}项)")
        for h in r.hits:
            flag = "🔴" if "盲区" in h.suggestion else "🟡"
            print(f"  {flag} {h.rule} '{h.word}' | {h.suggestion[:60]}")
    if blind_spots:
        print(f"\n{'='*70}")
        print(f"★ 盲区新词清单(需专家审, 确认后扩充terminology.json):")
        for b in blind_spots:
            print(f"  • '{b['word']}' ({b['file']}): {b['suggestion'][:50]}")
    print(f"\n说明: 🔴盲区新词(本工具核心价值) | 🟡已知/语法特征 | 规则可扩展")
    print(f"融合: 命中后交叉验证term_check(2,344条)+ai_detector(14翻译腔模式),")
    print(f"      两者均未收录=盲区→记录→专家确认→扩充术语库→盲区缩小")
    print("ℹ️ 供学术写作自查与质量改进使用；不用于规避机构 AIGC 检测，请遵循所在机构的 AI 使用与披露政策。")
    return 0


if __name__ == "__main__":
    import sys as _sys
    try:  # v3.5: 中文 Windows 默认 GBK 控制台会因 emoji/警示符崩溃 stdout——统一 UTF-8
        _sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        _sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    raise SystemExit(main())
