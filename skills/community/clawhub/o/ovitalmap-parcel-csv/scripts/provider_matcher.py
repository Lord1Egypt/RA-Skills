"""
Fuzzy provider-name deduplication for ovitalmap archive.

Compares a user-supplied name against a list of existing provider names using:
- Exact match (case-insensitive)
- Whitespace / punctuation normalization
- Chinese ↔ Pinyin overlap (via pypinyin if available)
- Partial / suffix / prefix overlap with common Chinese honorifics

CLI usage:
    echo '{"input_name":"李总","existing_names":["中非李总","三一李总","张三"]}' | python provider_matcher.py
    # {"matches":[...], "exact_match":null}
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Common Chinese honorifics / suffixes / prefixes that can vary
_HONORIFICS = {'总', '先生', '经理', '老板', '哥', '姐', '女士', '小姐', '老师', '师傅'}
_PREFIXES = {'中非', '三一', '非洲', '刚果', '金', '南', '北', '东', '西'}

# Try importing pypinyin for Chinese → Pinyin support
try:
    from pypinyin import lazy_pinyin
    _HAS_PYPINYIN = True
except ImportError:
    _HAS_PYPINYIN = False


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

def _normalize(s):
    """Lowercase, strip, collapse whitespace, remove common punctuation."""
    s = s.strip().lower()
    s = re.sub(r'[\s\-_.·]+', '', s)
    return s


def _strip_honorifics(name):
    """Remove common Chinese honorific suffixes/prefixes for comparison."""
    result = name
    for h in sorted(_HONORIFICS, key=len, reverse=True):
        if result.endswith(h):
            result = result[:-len(h)]
            break
    for p in sorted(_PREFIXES, key=len, reverse=True):
        if result.startswith(p):
            result = result[len(p):]
            break
    return result


def _to_pinyin(chinese_str):
    """Convert Chinese characters to pinyin (requires pypinyin). Returns None if unavailable."""
    if not _HAS_PYPINYIN:
        return None
    try:
        pinyin_list = lazy_pinyin(chinese_str)
        return ''.join(pinyin_list).lower()
    except Exception:
        return None


def _is_chinese(s):
    """Check if string contains Chinese characters."""
    return bool(re.search(r'[\u4e00-\u9fff]', s))


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------

def fuzzy_match(input_name, existing_names):
    """Match input_name against a list of existing provider names.

    Args:
        input_name: user-supplied provider name.
        existing_names: list of already-known provider names.

    Returns:
        dict with:
            exact_match: the exact match name (or None)
            candidates: list of {name, reason, score} sorted by score desc
            ambiguous: True when multiple candidates share the same highest score
                       (the LLM MUST ask the user to disambiguate).
            input_name: the original input name
    """
    candidates = []
    input_norm = _normalize(input_name)
    input_stripped = _strip_honorifics(input_name)
    input_pinyin = _to_pinyin(input_name) if _is_chinese(input_name) else None

    for existing in existing_names:
        existing_norm = _normalize(existing)
        existing_stripped = _strip_honorifics(existing)
        existing_pinyin = _to_pinyin(existing) if _is_chinese(existing) else None

        reason = None
        score = 0

        # 1) Exact match (case-insensitive, normalized)
        if input_norm == existing_norm:
            candidates.append({'name': existing, 'reason': 'exact', 'score': 100})
            continue

        # 2) Chinese ↔ Pinyin overlap
        if input_pinyin and existing_pinyin:
            if input_pinyin == existing_pinyin:
                candidates.append({'name': existing, 'reason': 'pinyin_match', 'score': 90})
                continue

        # 3) Cross-language: one has Chinese, other has pinyin in its name
        input_has_cn = _is_chinese(input_name)
        existing_has_cn = _is_chinese(existing)
        if input_has_cn != existing_has_cn:
            if input_has_cn and input_pinyin:
                if input_pinyin == existing_norm:
                    candidates.append({'name': existing, 'reason': 'pinyin_cross_match', 'score': 85})
                    continue
            if existing_has_cn and existing_pinyin:
                if existing_pinyin == input_norm:
                    candidates.append({'name': existing, 'reason': 'pinyin_cross_match', 'score': 85})
                    continue

        # 4) One is a substring of the other (strip honorifics first)
        #    Also check original (unstripped) for cases like "李总" ⊂ "中非李总"
        if input_stripped and existing_stripped:
            if input_stripped in existing_stripped or existing_stripped in input_stripped:
                candidates.append({'name': existing, 'reason': 'substring', 'score': 80})
                continue
        if input_name in existing or existing in input_name:
            candidates.append({'name': existing, 'reason': 'substring_raw', 'score': 80})
            continue

        # 5) Suffix/prefix variation (honorific stripped names match exactly)
        if input_stripped == existing_stripped and input_stripped:
            candidates.append({'name': existing, 'reason': 'honorific_variation', 'score': 75})
            continue

    # Sort by score descending
    candidates.sort(key=lambda x: x['score'], reverse=True)

    # Exact match is the first candidate with exact reason and score 100
    exact = next((c['name'] for c in candidates if c['reason'] == 'exact'), None)

    # Check for ambiguity: multiple candidates with the same highest score
    ambiguous = False
    if len(candidates) >= 2:
        top_score = candidates[0]['score']
        # Ambiguous if at least 2 candidates share the top score (and it's not an exact match)
        matching_top = [c for c in candidates if c['score'] == top_score]
        if len(matching_top) >= 2 and top_score < 100:
            ambiguous = True

    return {
        'exact_match': exact,
        'candidates': candidates,
        'ambiguous': ambiguous,
        'input_name': input_name,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    data = json.load(sys.stdin)
    input_name = data['input_name']
    existing_names = data.get('existing_names', [])

    result = fuzzy_match(input_name, existing_names)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()
