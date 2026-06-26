#!/usr/bin/env python3
"""
Hebrew Text Tools - Transliteration, Gematria, Nikud
Pure Python, no dependencies
"""

import sys
import argparse
import re

# Hebrew unicode range
HEBREW_RANGE = range(0x0590, 0x05FF)

def is_hebrew(char):
    return ord(char) in HEBREW_RANGE if char else False

def has_hebrew(text):
    return any(is_hebrew(c) for c in text)

# Transliteration mapping (Ashkenazi-style)
HEBREW_TO_LATIN = {
    'א': '',      # Aleph (silent)
    'ב': 'b',     # Bet
    'בּ': 'b',    # Bet with dagesh
    'ג': 'g',     # Gimel
    'גּ': 'g',    # Gimel with dagesh
    'ד': 'd',     # Dalet
    'דּ': 'd',    # Dalet with dagesh
    'ה': 'h',     # He
    'ו': 'v',     # Vav
    'וּ': 'u',    # Vav with shuruk
    'וֹ': 'o',    # Vav with holam
    'ז': 'z',     # Zayin
    'זּ': 'z',    # Zayin with dagesh
    'ח': 'ch',    # Chet
    'ט': 't',     # Tet
    'טּ': 't',    # Tet with dagesh
    'י': 'y',     # Yud
    'יִ': 'i',    # Yud with hiriq
    'כ': 'ch',    # Khaf (final/form)
    'ך': 'ch',    # Khaf sofit
    'כּ': 'k',    # Kaf with dagesh
    'ךּ': 'k',    # Kaf sofit with dagesh (rare)
    'ל': 'l',     # Lamed
    'מ': 'm',     # Mem
    'ם': 'm',     # Mem sofit
    'נ': 'n',     # Nun
    'ן': 'n',     # Nun sofit
    'ס': 's',     # Samekh
    'סּ': 's',    # Samekh with dagesh
    'ע': '',      # Ayin (silent)
    'פ': 'f',     # Pe (without dagesh)
    'ף': 'f',     # Pe sofit
    'פּ': 'p',    # Pe with dagesh
    'ףּ': 'p',    # Pe sofit with dagesh (rare)
    'צ': 'tz',    # Tsadi
    'ץ': 'tz',    # Tsadi sofit
    'צּ': 'tz',   # Tsadi with dagesh
    'ץּ': 'tz',   # Tsadi sofit with dagesh (rare)
    'ק': 'k',     # Kuf
    'קּ': 'k',    # Kuf with dagesh
    'ר': 'r',     # Resh
    'רּ': 'r',    # Resh with dagesh (rare)
    'שׁ': 'sh',   # Shin with dot right
    'שׂ': 's',    # Sin with dot left
    'ש': 'sh',    # Shin (default to shin)
    'שּׁ': 'sh',  # Shin with dagesh
    'שּׂ': 's',   # Sin with dagesh
    'ת': 't',     # Tav
    'תּ': 't',    # Tav with dagesh
    'ת': 's',     # Tav (Sephardi/Israeli, but keep 't' for Ashkenazi)
}

# Nikud removal mapping
NIKUD_CHARS = [
    '\u0591', '\u0592', '\u0593', '\u0594', '\u0595', '\u0596', '\u0597',
    '\u0598', '\u0599', '\u059A', '\u059B', '\u059C', '\u059D', '\u059E',
    '\u059F', '\u05A0', '\u05A1', '\u05A2', '\u05A3', '\u05A4', '\u05A5',
    '\u05A6', '\u05A7', '\u05A8', '\u05A9', '\u05AA', '\u05AB', '\u05AC',
    '\u05AD', '\u05AE', '\u05AF', '\u05B0', '\u05B1', '\u05B2', '\u05B3',
    '\u05B4', '\u05B5', '\u05B6', '\u05B7', '\u05B8', '\u05B9', '\u05BA',
    '\u05BB', '\u05BC', '\u05BD', '\u05BF', '\u05C1', '\u05C2', '\u05C4',
    '\u05C5', '\u05C7',
]

# Gematria values
GEMATRIA_VALUES = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9,
    'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40, 'נ': 50, 'ן': 50,
    'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80, 'צ': 90, 'ץ': 90, 'ק': 100, 'ר': 200,
    'ש': 300, 'ת': 400,
}

def remove_nikud(text):
    """Remove all nikud/vowel points from Hebrew text."""
    for nikud in NIKUD_CHARS:
        text = text.replace(nikud, '')
    return text

def transliterate(text):
    """Transliterate Hebrew to Latin characters with basic vowel heuristics."""
    result = []
    chars = list(text)
    for i, char in enumerate(chars):
        if char in HEBREW_TO_LATIN:
            trans = HEBREW_TO_LATIN[char]
            # Heuristic: Vav as vowel vs consonant
            if char == 'ו' and i > 0:
                # Vav at end of word (before sofit or end) → "v" or "u"
                if i == len(chars) - 1 or (i < len(chars) - 1 and chars[i+1] in HEBREW_TO_LATIN and 'Sofit' in HEBREW_TO_LATIN.get(chars[i+1], '')):
                    pass  # keep as 'v'
                # Vav between consonants → likely "o"
                elif i < len(chars) - 1 and chars[i+1] in HEBREW_TO_LATIN and chars[i-1] in HEBREW_TO_LATIN:
                    trans = 'o'
            result.append(trans)
        else:
            result.append(char)
    return ''.join(result)

def gematria(text):
    """Calculate gematria value of Hebrew text."""
    text = remove_nikud(text)
    total = 0
    for char in text:
        if char in GEMATRIA_VALUES:
            total += GEMATRIA_VALUES[char]
    return total

def gematria_matches(target_value, text):
    """Check if text's gematria equals target."""
    return gematria(text) == target_value

def hebrew_to_letters(hebrew_text):
    """Break Hebrew text into individual letter names."""
    letter_names = {
        'א': 'Alef', 'ב': 'Bet', 'ג': 'Gimel', 'ד': 'Dalet', 'ה': 'He',
        'ו': 'Vav', 'ז': 'Zayin', 'ח': 'Chet', 'ט': 'Tet', 'י': 'Yud',
        'כ': 'Kaf', 'ך': 'Kaf Sofit', 'ל': 'Lamed', 'מ': 'Mem', 'ם': 'Mem Sofit',
        'נ': 'Nun', 'ן': 'Nun Sofit', 'ס': 'Samekh', 'ע': 'Ayin',
        'פ': 'Pe', 'ף': 'Pe Sofit', 'צ': 'Tsadi', 'ץ': 'Tsadi Sofit',
        'ק': 'Kuf', 'ר': 'Resh', 'ש': 'Shin', 'ת': 'Tav',
    }
    result = []
    for char in hebrew_text:
        if char in letter_names:
            result.append(letter_names[char])
        elif not is_hebrew(char):
            result.append(char)
    return result

def reverse(text):
    """Reverse Hebrew text (RTL handling)."""
    # For Hebrew, we want to reverse the logical order
    # but preserve word order for mixed text
    if has_hebrew(text):
        words = text.split()
        reversed_words = []
        for word in words:
            if has_hebrew(word):
                reversed_words.append(word[::-1])
            else:
                reversed_words.append(word)
        return ' '.join(reversed(reversed_words))
    return text[::-1]

def format_hebrew_number(num):
    """Format a number using Hebrew letters (Gematria style)."""
    if num <= 0 or num > 999:
        return str(num)
    
    letters = [
        ('ת', 400), ('ש', 300), ('ר', 200), ('ק', 100),
        ('צ', 90), ('פ', 80), ('ע', 70), ('ס', 60), ('נ', 50),
        ('מ', 40), ('ל', 30), ('כ', 20), ('י', 10),
        ('ט', 9), ('ח', 8), ('ז', 7), ('ו', 6), ('ה', 5),
        ('ד', 4), ('ג', 3), ('ב', 2), ('א', 1),
    ]
    
    result = []
    for letter, value in letters:
        while num >= value:
            # Don't repeat same letter more than 3 times (Hebrew convention)
            count = 0
            if result and result[-1] == letter:
                count = sum(1 for i in range(len(result)) if i >= len(result) - 3 and result[i] == letter)
            if count >= 2:
                break
            result.append(letter)
            num -= value
    
    return ''.join(result) if result else str(num)

def main():
    parser = argparse.ArgumentParser(description="Hebrew Text Tools")
    parser.add_argument("text", nargs="?", help="Text to process")
    parser.add_argument("--transliterate", "-t", action="store_true", help="Transliterate to Latin")
    parser.add_argument("--remove-nikud", "-n", action="store_true", help="Remove nikud")
    parser.add_argument("--gematria", "-g", action="store_true", help="Calculate gematria")
    parser.add_argument("--letters", "-l", action="store_true", help="List letter names")
    parser.add_argument("--reverse", "-r", action="store_true", help="Reverse text")
    parser.add_argument("--number", "-N", type=int, help="Format number as Hebrew letters")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    
    args = parser.parse_args()
    
    if args.number is not None:
        result = format_hebrew_number(args.number)
        print(result)
        return
    
    text = args.text if args.text else sys.stdin.read().strip()
    if not text:
        print("Usage: hebrew-tools [options] <text>")
        print("       echo '<text>' | hebrew-tools [options]")
        sys.exit(1)
    
    results = {}
    
    if args.transliterate:
        result = transliterate(text)
        results["transliteration"] = result
    elif args.remove_nikud:
        result = remove_nikud(text)
        results["no_nikud"] = result
    elif args.gematria:
        result = gematria(text)
        results["gematria"] = result
    elif args.letters:
        result = hebrew_to_letters(text)
        results["letters"] = result
    elif args.reverse:
        result = reverse(text)
        results["reversed"] = result
    else:
        # Default: show all
        results = {
            "original": text,
            "has_hebrew": has_hebrew(text),
            "transliteration": transliterate(text),
            "no_nikud": remove_nikud(text),
            "gematria": gematria(text),
            "letter_names": hebrew_to_letters(text),
        }
    
    if args.json:
        import json
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for key, value in results.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
