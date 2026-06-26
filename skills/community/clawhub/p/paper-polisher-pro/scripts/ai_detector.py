#!/usr/bin/env python3
"""
AI Writing Detector — paper-polisher v1.1.0
Quantitative AI trace detection for academic text (Chinese + English).

v1.1.0 (2026-05-02): Added Perplexity proxy (bigram/trigram diversity) + upgraded Burstiness

Usage:
    python3 ai_detector.py <input_file>
    python3 ai_detector.py <input_file> --lang zh|en|auto
    python3 ai_detector.py <input_file> --format json|text|summary
    python3 ai_detector.py <input_file> --output report.json
"""

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

# v1.1: Perplexity proxy module
try:
    from perplexity import compute_perplexity_metrics, score_perplexity as _score_ppl
    _PPL_AVAILABLE = True
except ImportError:
    _PPL_AVAILABLE = False

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ParagraphResult:
    index: int
    text: str
    lang: str  # "zh" | "en"
    ai_score: float  # 0-100, higher = more AI-like
    matched_patterns: list = field(default_factory=list)
    ttr: float = 0.0
    avg_sentence_len: float = 0.0
    sentence_len_variance: float = 0.0
    paragraph_len: int = 0
    # v1.1: Perplexity proxy metrics
    bigram_diversity: float = 0.0
    trigram_diversity: float = 0.0
    ppl_burstiness: float = 0.0
    perplexity_score: float = 0.0
    burstiness_score: float = 0.0  # sentence-level burstiness (upgraded uniformity)

@dataclass
class DetectionReport:
    file: str = ""
    overall_ai_score: float = 0.0
    overall_risk: str = "low"  # low | medium | high
    total_paragraphs: int = 0
    avg_ttr: float = 0.0
    avg_sentence_len: float = 0.0
    avg_sentence_len_variance: float = 0.0
    paragraph_scores: list = field(default_factory=list)
    top_patterns: list = field(default_factory=list)
    language: str = "auto"
    details: str = ""


# ---------------------------------------------------------------------------
# Language detection helpers
# ---------------------------------------------------------------------------

def detect_lang(text: str) -> str:
    """Simple heuristic: if >30% CJK characters → zh, else en."""
    cjk = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff' or '\u3400' <= ch <= '\u4dbf')
    alpha = sum(1 for ch in text if ch.isalpha())
    total = max(alpha + cjk, 1)
    return "zh" if cjk / total > 0.3 else "en"


# ---------------------------------------------------------------------------
# Text statistics
# ---------------------------------------------------------------------------

def split_sentences(text: str, lang: str) -> list:
    if lang == "zh":
        parts = re.split(r'[。！？；\n]+', text)
    else:
        parts = re.split(r'(?<=[.!?])\s+|\n+', text)
    return [s.strip() for s in parts if s.strip()]


def tokenize(text: str, lang: str) -> list:
    """Tokenize text. For mixed content, extract both CJK chars and English words."""
    cjk = [ch for ch in text if '\u4e00' <= ch <= '\u9fff' or '\u3400' <= ch <= '\u4dbf']
    en = re.findall(r"[a-zA-Z]+(?:'[a-z]+)?", text.lower())
    if lang == "zh":
        return cjk if cjk else en  # fallback to en if no CJK
    else:
        return en if en else cjk  # fallback to CJK if no English


def calc_ttr(tokens: list) -> float:
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def calc_info_density(text: str, lang: str) -> float:
    """Calculate information density: ratio of content chars after removing stopwords.
    
    AI text has anomalously high info density (0.85-0.90) because it 
    compresses information densely. Human text has more filler/function 
    words (0.75-0.84). This is a powerful signal for newer models that 
    avoid cliché patterns.
    """
    if lang == "zh":
        chars = [c for c in text if '\u4e00' <= c <= '\u9fff']
        if not chars:
            return 0.0
        stopwords = set('的了是在有被人与和中为而从这那以可将对上但到又要就也都能很好很更还又再已其所如该本即或没得之于让把向吗吧呢啊呀嗯')
        content = [c for c in chars if c not in stopwords]
        return len(content) / len(chars)
    else:
        words = text.lower().split()
        if not words:
            return 0.0
        stopwords = {'the','a','an','is','are','was','were','be','been','being',
                     'in','on','at','to','for','of','with','by','from','as',
                     'it','its','this','that','these','those','and','or','but',
                     'not','no','do','does','did','has','have','had','will',
                     'would','could','should','can','may','might','shall'}
        content = [w for w in words if w not in stopwords]
        return len(content) / len(words)


def sentence_length_stats(sentences: list, lang: str) -> tuple:
    if not sentences:
        return 0.0, 0.0
    if lang == "zh":
        lengths = [len(s) for s in sentences]
    else:
        lengths = [len(s.split()) for s in sentences]
    avg = sum(lengths) / len(lengths)
    if len(lengths) > 1:
        var = sum((l - avg) ** 2 for l in lengths) / len(lengths)
    else:
        var = 0.0
    return round(avg, 1), round(var, 1)


# ---------------------------------------------------------------------------
# Pattern matching
# ---------------------------------------------------------------------------

def load_patterns(lang: str) -> dict:
    ref_dir = Path(__file__).parent.parent / "references"
    fname = f"ai_patterns_{lang}.json"
    fpath = ref_dir / fname
    if not fpath.exists():
        return {}
    with open(fpath, "r", encoding="utf-8") as f:
        return json.load(f).get("categories", {})


def match_patterns(text: str, categories: dict) -> list:
    """Return list of {pattern, category, weight} matches."""
    results = []
    text_lower = text.lower()
    for cat_name, cat_data in categories.items():
        weight = cat_data.get("weight", 1)
        for pat in cat_data.get("patterns", []):
            if "." in pat or "[" in pat or "(" in pat or "{" in pat:
                # regex pattern
                try:
                    if re.search(pat, text, re.IGNORECASE):
                        results.append({"pattern": pat, "category": cat_name, "weight": weight})
                except re.error:
                    continue
            else:
                # literal match (case-insensitive)
                if pat.lower() in text_lower:
                    results.append({"pattern": pat, "category": cat_name, "weight": weight})
    return results


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def match_sentence_patterns(text: str, lang: str) -> list:
    """Match text against known AI sentence templates. Returns list of matched pattern IDs."""
    if lang != "zh":
        return []  # ZH patterns only for now
    
    ref_dir = Path(__file__).parent.parent / "references"
    fpath = ref_dir / "sentence_patterns_zh.json"
    if not fpath.exists():
        return []
    
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
    
    matched = []
    text_clean = text.replace(" ", "").replace("\n", "")
    
    for pat in data.get("patterns", []):
        # Convert template pattern to regex
        # Replace {placeholder} with wildcard
        template = pat["pattern"].replace(" ", "")
        # Escape special regex chars except {}
        import re as _re
        regex_str = _re.escape(template)
        # Replace escaped {xxx} with wildcard
        regex_str = _re.sub(r'\\{[^}]+\\}', '.{1,20}', regex_str)
        try:
            if _re.search(regex_str, text_clean):
                matched.append({
                    "id": pat["id"],
                    "category": pat["category"],
                    "pattern": pat["pattern"],
                    "ai_frequency": pat.get("ai_frequency", "medium"),
                })
        except _re.error:
            continue
    
    return matched


def score_paragraph(text: str, lang: str, categories: dict) -> ParagraphResult:
    matches = match_patterns(text, categories)
    tokens = tokenize(text, lang)
    sentences = split_sentences(text, lang)
    ttr = calc_ttr(tokens)
    avg_slen, slen_var = sentence_length_stats(sentences, lang)

    para_len = len(text)

    # --- Pattern match score (proportional, no hard cap) ---
    matches = match_patterns(text, categories)
    sentence_pat_matches = match_sentence_patterns(text, lang)
    match_score = sum(m["weight"] for m in matches)
    pattern_points = min(match_score / 15.0, 1.0) * 50
    
    # --- Sentence template match score (v1.1) ---
    # Each matched template adds points based on ai_frequency
    sent_tmpl_score = 0.0
    for sp in sentence_pat_matches:
        freq = sp.get("ai_frequency", "medium")
        if freq == "very_high":
            sent_tmpl_score += 3.0
        elif freq == "high":
            sent_tmpl_score += 2.0
        else:
            sent_tmpl_score += 1.0
    # Cap at 10 points
    sent_tmpl_score = min(sent_tmpl_score, 10.0)

    # --- TTR penalty: very uniform vocabulary → AI-like ---
    if lang == "zh":
        ttr_score = max(0, (0.5 - ttr) / 0.3) * 15
    else:
        ttr_score = max(0, (0.6 - ttr) / 0.3) * 15

    # --- Burstiness score (v1.1: upgraded from simple uniformity) ---
    # Combines: (1) sentence length CV, (2) adjacent sentence jumps,
    # (3) sentence length range ratio
    sentences_list = split_sentences(text, lang)
    if lang == "zh":
        slens = [len(s) for s in sentences_list]
    else:
        slens = [len(s.split()) for s in sentences_list]

    if len(slens) >= 3 and avg_slen > 0:
        # Component A: CV of sentence lengths (original metric, refined)
        cv = math.sqrt(slen_var) / avg_slen
        cv_score = max(0, (0.45 - cv) / 0.30) * 6  # 0-6 pts (v1.1.1: lowered from 8 to reduce FP)

        # Component B: Adjacent sentence jump consistency
        # AI: jumps are large but regular (systematic); Human: jumps vary more
        # Key insight: AI sentences tend to be uniformly LONG (avg 28-38 chars ZH)
        # Human sentences are shorter with more variation (avg 15-22 chars ZH)
        diffs = [abs(slens[i] - slens[i+1]) for i in range(len(slens)-1)]
        avg_diff = sum(diffs) / len(diffs)
        max_diff = max(diffs)
        # The key signal is: high avg sentence length + low range ratio = AI
        # Jump score only matters when sentences are uniformly long
        if lang == "zh":
            if avg_slen > 30:  # AI tends to have avg sentence length > 30
                jump_score = max(0, (12 - avg_diff) / 12) * 6
            else:
                jump_score = max(0, (8 - avg_diff) / 8) * 3  # Lower weight for shorter text
        else:
            if avg_slen > 15:  # EN AI tends to have longer sentences
                jump_score = max(0, (5 - avg_diff) / 5) * 6
            else:
                jump_score = max(0, (3 - avg_diff) / 3) * 3

        # Component C: Sentence length range ratio (max/min)
        min_slen = min(slens)
        if min_slen > 0:
            range_ratio = max(slens) / min_slen
            # AI: ratio 1.0-1.3 (uniform), Human: ratio 1.5-5.0+ (varied)
            # v1.1.1 fix: lowered threshold from 1.5→1.3 to reduce false positives
            # on formal academic text with moderately uniform sentences
            if range_ratio < 1.2:
                range_score = 6.0
            elif range_ratio < 1.3:
                range_score = 4.0
            elif range_ratio < 1.8:
                range_score = 1.0
            else:
                range_score = 0.0
        else:
            range_score = 3.0

        burstiness_score = cv_score + jump_score + range_score  # 0-20 pts total
    elif len(slens) == 2 and avg_slen > 0:
        # Two sentences: only CV available
        cv = math.sqrt(slen_var) / avg_slen
        burstiness_score = max(0, (0.45 - cv) / 0.30) * 20
    else:
        burstiness_score = 10  # single sentence = can't assess = moderate default

    # --- Paragraph length bonus (AI likes medium-long paragraphs) ---
    if lang == "zh":
        ideal_range = (80, 300)
    else:
        ideal_range = (40, 200)
    length_score = 5 if ideal_range[0] <= para_len <= ideal_range[1] else 0

    # --- Information density penalty (catches evolved AI models) ---
    # AI text: 0.86-0.90 (anomalously dense), Human: 0.75-0.85
    # Use density as an AMPLIFIER when patterns are also present, not standalone
    info_density = calc_info_density(text, lang)
    if lang == "zh" and para_len >= 50:
        if info_density >= 0.86:
            # High density: amplify existing pattern signals by 1.5x
            density_score = min(pattern_points * 0.5, 15)
        elif info_density >= 0.84:
            density_score = min(pattern_points * 0.3, 8)
        else:
            density_score = 0
    elif lang == "en" and para_len >= 30:
        if info_density >= 0.65:
            density_score = 8
        elif info_density >= 0.58:
            density_score = 4
        else:
            density_score = 0
    else:
        density_score = 0

    # --- Sentence opener diversity (catches evolved AI models) ---
    # AI text frequently uses PREP/CONN sentence openers ("在...中", "然而", "综上")
    # Human text almost always starts with direct subject (0% PREP/CONN)
    if lang == "zh" and len(sentences) >= 3:
        prep_conn_openers = 0
        for s in sentences:
            s = s.strip()
            if len(s) < 3: continue
            first3 = s[:3]
            if re.match(r'^(然而|尽管|此外|因此|不过|从而|进而|综上|基于|同时|鉴于|另外|其次|最后|关于|对于|通过|根据|由于|虽然)', first3):
                prep_conn_openers += 1
            elif re.match(r'^在', first3) and re.search(r'[中上下面里]', s[:15]):
                prep_conn_openers += 1
            elif re.match(r'^而', first3):
                prep_conn_openers += 1
        opener_ratio = prep_conn_openers / len(sentences)
        if opener_ratio >= 0.4:
            opener_score = 10  # very AI-like: 40%+ sentences start with connectors
        elif opener_ratio >= 0.25:
            opener_score = 5
        else:
            opener_score = 0
    else:
        opener_score = 0

    # --- Short text: scale down but don't zero out (B1/B2 fix) ---
    raw_score = pattern_points + sent_tmpl_score + ttr_score + burstiness_score + length_score + density_score + opener_score

    # --- v1.1: Perplexity proxy (n-gram diversity + burstiness) ---
    ppl_score = 0.0
    ppl_metrics = {}
    if _PPL_AVAILABLE:
        ppl_metrics = compute_perplexity_metrics(text, lang)
        ppl_score = _score_ppl(text, lang, para_len)
    raw_score += ppl_score

    if para_len < 30:
        # Scale proportionally instead of zeroing
        scale = max(para_len / 30.0, 0.2)
        ai_score = raw_score * scale
    else:
        ai_score = min(100, raw_score)

    return ParagraphResult(
        index=0,
        text=text[:200] + ("..." if len(text) > 200 else ""),
        lang=lang,
        ai_score=round(ai_score, 1),
        matched_patterns=matches,
        ttr=round(ttr, 3),
        avg_sentence_len=avg_slen,
        sentence_len_variance=slen_var,
        paragraph_len=para_len,
        bigram_diversity=ppl_metrics.get("bigram_diversity", 0.0),
        trigram_diversity=ppl_metrics.get("trigram_diversity", 0.0),
        ppl_burstiness=ppl_metrics.get("burstiness", 0.0),
        perplexity_score=ppl_score,
        burstiness_score=burstiness_score,
    )


# ---------------------------------------------------------------------------
# Main detection
# ---------------------------------------------------------------------------

def split_paragraphs(text: str) -> list:
    """Split text into paragraphs."""
    paras = re.split(r'\n\s*\n|\n', text)
    return [p.strip() for p in paras if p.strip() and len(p.strip()) > 3]


def detect(text: str, lang: str = "auto") -> DetectionReport:
    if lang == "auto":
        lang = detect_lang(text)

    categories = load_patterns(lang)
    paragraphs = split_paragraphs(text)

    if not paragraphs:
        return DetectionReport(
            overall_risk="unknown",
            details="文本过短或无法分段，无法进行检测。"
        )

    results = []
    all_matches = []
    for i, para in enumerate(paragraphs):
        r = score_paragraph(para, lang, categories)
        r.index = i
        results.append(r)
        all_matches.extend(r.matched_patterns)

    # Weighted overall score
    if results:
        # Weight by paragraph length
        total_len = sum(r.paragraph_len for r in results)
        if total_len > 0:
            overall = sum(r.ai_score * r.paragraph_len for r in results) / total_len
        else:
            overall = sum(r.ai_score for r in results) / len(results)
    else:
        overall = 0

    # Top patterns
    pat_counter = Counter(m["pattern"] for m in all_matches)
    top = [{"pattern": p, "count": c} for p, c in pat_counter.most_common(10)]

    # Risk level
    if overall >= 60:
        risk = "high"
    elif overall >= 35:
        risk = "medium"
    else:
        risk = "low"

    # Detail summary
    details = _build_summary(results, lang, risk, overall)

    return DetectionReport(
        file="",
        overall_ai_score=round(overall, 1),
        overall_risk=risk,
        total_paragraphs=len(results),
        avg_ttr=round(sum(r.ttr for r in results) / max(len(results), 1), 3),
        avg_sentence_len=round(sum(r.avg_sentence_len for r in results) / max(len(results), 1), 1),
        avg_sentence_len_variance=round(sum(r.sentence_len_variance for r in results) / max(len(results), 1), 1),
        paragraph_scores=[asdict(r) for r in results],
        top_patterns=top,
        language=lang,
        details=details,
    )


def _build_summary(results: list, lang: str, risk: str, score: float) -> str:
    if lang == "zh":
        risk_map = {"high": "🔴 高风险", "medium": "🟡 中等风险", "low": "🟢 低风险"}
    else:
        risk_map = {"high": "🔴 High Risk", "medium": "🟡 Medium Risk", "low": "🟢 Low Risk"}

    total_patterns = sum(len(r.matched_patterns) for r in results)
    hot_paras = [r for r in results if r.ai_score >= 50]
    
    if lang == "zh":
        lines = [
            f"AI痕迹评分: {score:.1f}/100  {risk_map[risk]}",
            f"共 {len(results)} 段，命中 {total_patterns} 条AI模式",
        ]
        if hot_paras:
            lines.append(f"⚠️ 高风险段落: 第 {', '.join(str(r.index+1) for r in hot_paras)} 段")
        lines.append("\n段落明细:")
        for r in results:
            bar = "█" * int(r.ai_score / 5) + "░" * (20 - int(r.ai_score / 5))
            lines.append(f"  P{r.index+1:02d} [{bar}] {r.ai_score:5.1f}  (TTR={r.ttr:.2f} 句长方差={r.sentence_len_variance:.1f})")
    else:
        lines = [
            f"AI Trace Score: {score:.1f}/100  {risk_map[risk]}",
            f"Total {len(results)} paragraphs, {total_patterns} AI patterns matched",
        ]
        if hot_paras:
            lines.append(f"⚠️ High-risk paragraphs: {', '.join(str(r.index+1) for r in hot_paras)}")
        lines.append("\nParagraph breakdown:")
        for r in results:
            bar = "█" * int(r.ai_score / 5) + "░" * (20 - int(r.ai_score / 5))
            lines.append(f"  P{r.index+1:02d} [{bar}] {r.ai_score:5.1f}  (TTR={r.ttr:.2f} sent-var={r.sentence_len_variance:.1f})")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="AI Writing Detector")
    parser.add_argument("input", help="Input text file")
    parser.add_argument("--lang", choices=["zh", "en", "auto"], default="auto", help="Language")
    parser.add_argument("--format", choices=["json", "text", "summary"], default="summary", help="Output format")
    parser.add_argument("--output", help="Output file (default: stdout)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    report = detect(text, args.lang)

    # When writing to file, default to JSON unless format explicitly set
    use_json = args.format == "json" or (args.output and args.format == "summary")

    if use_json:
        output = json.dumps(asdict(report), ensure_ascii=False, indent=2)
    else:
        output = report.details

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Report saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
