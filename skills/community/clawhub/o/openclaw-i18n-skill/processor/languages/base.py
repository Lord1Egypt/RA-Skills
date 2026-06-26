"""
Base rules shared across all languages.
These are always applied, regardless of target language.
"""
import re
import unicodedata


def remove_non_latin_characters(text: str) -> str:
    """
    Remove stray non-Latin characters that models sometimes insert.
    Only removes SINGLE characters surrounded by Latin text.
    Preserves intentional non-Latin (quoted text, names, etc.).
    """
    # Pattern: single non-Latin char between Latin chars or at word boundaries
    # We remove only isolated characters that are clearly errors
    result = []
    i = 0
    while i < len(text):
        char = text[i]
        code = ord(char)
        
        # Check if it's a non-Latin character (not ASCII, not common punct, not space)
        is_latin = (
            (0x0041 <= code <= 0x007A) or  # basic latin uppercase/lowercase
            (0x00C0 <= code <= 0x024F) or  # latin extended
            (0x0030 <= code <= 0x0039) or  # digits
            (char in ' \t\n\r.,!?;:()[]{}—–-"\'') or
            (char in 'ăâîșțĂÂÎȘȚ') or  # Romanian diacritics
            (char in 'üöäßÜÖÄ') or  # German diacritics
            (char in 'àâçéèêëîïôûùÀÂÇÉÈÊËÎÏÔÛÙ') or  # French
            (char in 'áéíóúñüÁÉÍÓÚÑÜ')  # Spanish
        )
        
        is_mark = char in ' \t\n\r'  # whitespace
        
        if is_latin or is_mark:
            result.append(char)
        else:
            # Non-Latin, non-mark char — check if it's a stray model artifact
            #
            # REMOVE if:
            # 1. Directly preceded by Latin without space — e.g. "t理" or "tС"
            #    Remove the ENTIRE consecutive non-Latin sequence after Latin.
            #    This catches the most common model error.
            # 2. Isolated single non-Latin between Latin on BOTH sides
            #    (e.g. "a理b" — remove just the single char)
            #
            # KEEP if:
            # - Preceded by whitespace (intentional foreign text)
            # - Preceded by another non-Latin char (part of a foreign word)
            before_latin = False
            before_space = (i > 0 and text[i - 1] in ' \t\n\r')
            before_non_latin = False

            if i > 0:
                prev_code = ord(text[i - 1])
                before_latin = (0x0041 <= prev_code <= 0x007A) or (0x00C0 <= prev_code <= 0x024F)
                before_non_latin = not before_latin and not (text[i - 1] in ' \t\n\r')

            is_stray = _is_stray_char(char, text, i)

            if is_stray and before_latin:
                # Remove the ENTIRE consecutive non-Latin sequence after Latin
                j = i
                while j < len(text) and _is_stray_char(text[j], text, j):
                    j += 1
                i = j - 1  # will be incremented by for loop
            elif is_stray and (before_space or before_non_latin):
                # Preceded by space OR by another non-Latin (foreign word)
                # Keep it - it's intentional foreign text
                result.append(char)
            elif is_stray:
                # Isolated stray — remove
                pass
            else:
                # Not a stray artifact (emoji, math, etc.)
                result.append(char)
        i += 1
    
    return ''.join(result)


def _is_stray_char(char: str, text: str, pos: int) -> bool:
    """
    Detect if a non-Latin character is likely a stray model error.
    Returns True if it should be removed.
    """
    code = ord(char)
    
    # Chinese, Japanese, Korean, Cyrillic, Arabic — almost always errors
    # when mixed into Latin text
    if _is_cjk(code):
        return True
    if _is_cyrillic(code):
        return True
    if _is_arabic(code):
        return True
    if _is_devanagari(code):
        return True
    
    # Greek — usually error when mixed into European language text
    if _is_greek(code):
        return True
    
    # Other scripts that don't mix with Latin — likely errors
    if _is_thai(code) or _is_hangul(code) or _is_hebrew(code):
        return True
    
    return False


def _is_cjk(code: int) -> bool:
    return (
        (0x4E00 <= code <= 0x9FFF) or  # CJK Unified Ideographs
        (0x3400 <= code <= 0x4DBF) or  # CJK Extension A
        (0x3000 <= code <= 0x303F) or  # CJK Symbols
        (0xFF00 <= code <= 0xFFEF)    # Halfwidth/Fullwidth Forms
    )


def _is_cyrillic(code: int) -> bool:
    return (0x0400 <= code <= 0x04FF)


def _is_arabic(code: int) -> bool:
    return (0x0600 <= code <= 0x06FF)


def _is_devanagari(code: int) -> bool:
    return (0x0900 <= code <= 0x097F)


def _is_greek(code: int) -> bool:
    return (0x0370 <= code <= 0x03FF)


def _is_thai(code: int) -> bool:
    return (0x0E00 <= code <= 0x0E7F)


def _is_hangul(code: int) -> bool:
    return (0xAC00 <= code <= 0xD7AF)


def _is_hebrew(code: int) -> bool:
    return (0x0590 <= code <= 0x05FF)


def normalize_whitespace(text: str) -> str:
    """
    Normalize all whitespace variations to standard spaces.
    - Double spaces → single space
    - Trailing/leading spaces → trimmed
    - Tab/newline → space (unless preserving paragraph structure)
    """
    # Replace multiple spaces with single space
    text = re.sub(r'  +', ' ', text)
    
    # Remove leading/trailing whitespace from each line
    lines = text.split('\n')
    lines = [line.strip() for line in lines]
    
    # Remove empty lines at start/end
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    
    return '\n'.join(lines)


def fix_merged_words(text: str) -> str:
    """
    Fix obvious merged words — conservative only.
    Only fixes clear cases where:
    1. Two known words are concatenated without space
    2. The result would make sense and is a common phrase
    
    This is HIGHLY CONSERVATIVE to avoid false positives.
    """
    # Common Romanian merges — conservative, only clear cases
    # Patterns use word boundaries without extra spaces in replacement
    merges_ro = [
        # si → și only after punctuation or start of sentence
        (r'(?<=[.!?;]) si', ' și'),
        (r'^si ', 'și '),
        # sa → să only after punctuation or start of sentence
        (r'(?<=[.!?;]) sa', ' să'),
        (r'^sa ', 'să '),
    ]
    
    for pattern, replacement in merges_ro:
        text = re.sub(pattern, replacement, text)
    
    return text


def fix_common_typos(text: str, typo_dict: dict) -> str:
    """
    Apply a language-specific typo dictionary.
    Only applies exact matches (whole word) to avoid partial replacements.
    """
    for wrong, correct in typo_dict.items():
        # Use word boundary matching for safety
        pattern = r'\b' + re.escape(wrong) + r'\b'
        text = re.sub(pattern, correct, text)
    
    return text
