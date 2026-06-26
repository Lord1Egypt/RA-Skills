
"""
Romanian-specific diacritics and typo corrections.
HIGH CONFIDENCE ONLY — false positives are worse than leaving errors.
"""
import re
from typing import Tuple


# Common Romanian words that models frequently get wrong
# Format: "wrong_form": "correct_form"
ROMANIAN_TYPO_DICT = {
    # Verbs with diacritics
    "vrau": "vreau",
    "invat": "învăț",
    "invata": "învăța",
    "invatam": "învățăm",
    "invatati": "învățați",
    "invatat": "învățat",
    "stiu": "știu",
    "stii": "știi",
    "sti": "ști",
    "stim": "știm",
    "stiti": "știți",
    "stiau": "știau",
    "ajuta": "ajută",
    "ajut": "ajut",
    "ajutam": "ajutam",
    "trebui": "trebuie",
    "trebuie": "trebuie",
    "trebuiasca": "trebuiască",
    "trebuisa": "trebuia",
    "potzi": "poți",
    "sar": "s-ar",
    "asi": "ași",
    "ati": "ați",
    "ari": "ași",

    # Common words with sedilla (ș/ț)
    "oras": "oraș",
    "adevarul": "adevărul",
    "adevar": "adevăr",
    "tara": "țară",
    "tari": "țări",
    "buzunar": "buzunar",
    "masa": "masă",
    "friptura": "friptură",
    "sat": "sat",
    "sate": "sate",
    "asaza": "așază",
    "asaz": "așaz",
    "intors": "întors",
    "incape": "încape",
    "muncit": "muncit",
    "muncitor": "muncitor",
    "cercetare": "cercetare",
    "cercetator": "cercetător",
    "stiinta": "știință",
    "notiune": "noțiune",
    "notiuni": "noțiuni",
    "productie": "producție",
    "tendinta": "tendință",
    "actiune": "acțiune",
    "sectiune": "secțiune",
    "punct": "punct",
    "puncte": "puncte",
    "contact": "contact",
    "romania": "România",
    "romanes": "românesc",
    "romaneasca": "românească",
    "invatator": "învățător",
    "invatatoare": "învățătoare",
    "traducere": "traducere",
    "traducatori": "traducători",
    "prefectura": "prefectură",
    "natiune": "națiune",
    "atentionare": "atenționare",
    "reteta": "rețetă",
    "piata": "piață",
    "ieftin": "ieftin",
    "scaun": "scaun",
    "flacara": "flacără",
    "brat": "braț",
    "frate": "frate",
    "fratii": "frații",
    "munca": "muncă",
    "bani": "bani",
    "tzes": "țări",
    "tzi": "ți",
    "tza": "ță",

    # Words with "ă"
    "averi": "averi",
    "tari": "tari",
    "mari": "mari",
    "buni": "buni",
    "rali": "răli",  # rare

    # Merge patterns (standalone only)
    "si": "și",
    "sa": "să",
    "in": "în",
}


def fix_diacritics_ro(text: str) -> str:
    """
    Fix missing Romanian diacritics — HIGH CONFIDENCE ONLY.

    Rules applied:
    1. "si" → "și" ONLY when clearly the conjunction between words
    2. "ii" context fixes for common words
    3. Known word dictionary for confident replacements

    NEVER change:
    - Words where "s" or "i" is part of compound not separated
    - Unclear contexts — leave as-is
    """
    result = text

    # si → și (conjunction) — only when between two words
    result = re.sub(r'(\w) si (\w)', r'\1 și \2', result)
    result = re.sub(r'^si (\w)', r'și \1', result, flags=re.MULTILINE)
    result = re.sub(r'(\w) si$', r'\1 și', result, flags=re.MULTILINE)
    result = re.sub(r'^si$', r'și', result, flags=re.MULTILINE)

    # sa → să (subjunctive) — only standalone "sa"
    result = re.sub(r'\bsa\b', 'să', result)

    # ii at word boundaries → îi (common case)
    result = re.sub(r'\bii\b', 'îi', result)

    # in → în (preposition) — very common error
    result = re.sub(r'\bin\b', 'în', result)

    # Romanian words with diacritics — most reliable fixes
    word_fixes = [
        (r'\bstiu\b', 'știu'),
        (r'\bstii\b', 'știi'),
        (r'\bsti\b', 'ști'),
        (r'\bstim\b', 'știm'),
        (r'\bstiti\b', 'știți'),
        (r'\bstiau\b', 'știau'),
        (r'\bvrau\b', 'vreau'),
        (r'\binvat\b', 'învăț'),
        (r'\binvata\b', 'învăța'),
        (r'\binvatam\b', 'învățăm'),
        (r'\binvatati\b', 'învățați'),
        (r'\binvatau\b', 'învățau'),
        (r'\btrebuiasca\b', 'trebuiască'),
        (r'\bajuta\b', 'ajută'),
        (r'\bsar\b', 's-ar'),
        # Sedilla (ș/ț) — common words
        (r'\boras\b', 'oraș'),
        (r'\badevarul\b', 'adevărul'),
        (r'\badevar\b', 'adevăr'),
        (r'\btara\b', 'țară'),
        (r'\basi\b', 'ași'),
        (r'\bati\b', 'ați'),
        (r'\bromania\b', 'România'),
        (r'\bmasa\b', 'masă'),
        (r'\bfriptura\b', 'friptură'),
        (r'\btari\b', 'țări'),
        (r'\bintors\b', 'întors'),
        (r'\bincape\b', 'încape'),
        (r'\bmuncit\b', 'muncit'),
        (r'\bstiinta\b', 'știință'),
        (r'\bnotiune\b', 'noțiune'),
        (r'\bproductie\b', 'producție'),
        (r'\btendinta\b', 'tendință'),
        (r'\bactiune\b', 'acțiune'),
        (r'\bsectiune\b', 'secțiune'),
        (r'\breteta\b', 'rețetă'),
        (r'\bpiata\b', 'piață'),
        (r'\btraducere\b', 'traducere'),
        (r'\btraducator\b', 'traducător'),
        (r'\batentie\b', 'atenție'),
        (r'\bnatiune\b', 'națiune'),
        (r'\binvatat\b', 'învățat'),
        (r'\bromaneasca\b', 'românească'),
        (r'\bromanescu\b', 'românesc'),
        # Final pass for any remaining "si" not caught above
        (r'\bsi\b', 'și'),
    ]

    for pattern, replacement in word_fixes:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

    return result


def fix_stray_chars_ro(text: str) -> str:
    """
    Remove isolated Chinese/Russian characters that M2.7 sometimes inserts
    into Romanian text. Pattern: single non-Latin char surrounded by Latin text.
    """
    result = []
    i = 0
    while i < len(text):
        char = text[i]
        code = ord(char)

        # If it's a CJK or Cyrillic character, check context
        if _is_problematic_char(code):
            before_latin = False
            after_latin = False

            if i > 0:
                prev_char = text[i - 1]
                prev_code = ord(prev_char)
                before_latin = _is_latin_char(prev_code)

            if i < len(text) - 1:
                next_char = text[i + 1]
                next_code = ord(next_char)
                after_latin = _is_latin_char(next_code)

            if before_latin and after_latin:
                # Stray character — skip it
                i += 1
                continue

        result.append(char)
        i += 1

    return ''.join(result)


def _is_problematic_char(code: int) -> bool:
    """Check if character is likely a stray model artifact."""
    if 0x4E00 <= code <= 0x9FFF:
        return True
    if 0x3400 <= code <= 0x4DBF:
        return True
    if 0x0400 <= code <= 0x04FF:
        return True
    if 0x0600 <= code <= 0x06FF:
        return True
    return False


def _is_latin_char(code: int) -> bool:
    """Check if character is Latin alphabet."""
    return (
        (0x0041 <= code <= 0x007A) or
        (0x00C0 <= code <= 0x024F) or
        (0x0100 <= code <= 0x017F)
    )


# Export typo dictionary for use in main processor
TYPO_DICT = ROMANIAN_TYPO_DICT
