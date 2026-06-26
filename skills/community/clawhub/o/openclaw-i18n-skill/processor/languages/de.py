"""
German-specific diacritics and typo corrections.
HIGH CONFIDENCE ONLY - false positives are worse than leaving errors.
"""
import re


# Common German words that models frequently get wrong
# Format: "wrong_form": "correct_form"
GERMAN_TYPO_DICT = {
    # umlaut corrections
    "Mueller": "Müller",
    "Muelller": "Müller",
    "Muller": "Müller",
    "Schuler": "Schüler",
    "Schuoler": "Schüler",
    "Frucht": "Frücht",  # not always wrong but common
    "Uber": "Über",
    "uber": "über",
    "Oko": "Öko",
    "oko": "öko",
    "Uber": "Über",
    "Buro": "Büro",
    "buro": "büro",
    "Fur": "für",
    "fur": "für",
    "uber": "über",
    "schon": "schon",  # already correct
    "schon": "schon",
    "gehen": "gehen",
    "stehen": "stehen",
    "sehen": "sehen",
    "nehmen": "nehmen",
    "geben": "geben",

    # Common German words with issues
    "dass": "dass",
    "das": "das",
    "man": "man",
    "nicht": "nicht",
    "ein": "ein",
    "eine": "eine",
    "einer": "einer",
    "einem": "einem",
    "einen": "einen",
    "und": "und",
    "auch": "auch",
    "aber": "aber",
    "oder": "oder",
    "so": "so",
    "wie": "wie",
    "was": "was",
    "wer": "wer",
    "wenn": "wenn",
    "weil": "weil",
    "noch": "noch",
    "schon": "schon",
    "schon": "schon",
    "schwer": "schwer",
    "sehr": "sehr",
    "wieder": "wieder",
    "wissen": "wissen",
    "konnen": "können",
    "mussen": "müssen",
    "sollen": "sollen",
    "wollen": "wollen",
    "durfen": "dürfen",
    "mogen": "mögen",
    "haben": "haben",
    "sein": "sein",
    "werden": "werden",
    "lassen": "lassen",
    "lassen": "lassen",

    # Articles and prepositions
    "der": "der",
    "die": "die",
    "das": "das",
    "den": "den",
    "dem": "dem",
    "des": "des",
    "von": "von",
    "mit": "mit",
    "nach": "nach",
    "bei": "bei",
    "aus": "aus",
    "auf": "auf",
    "zu": "zu",
    "um": "um",
    "in": "in",
    "an": "an",
    "durch": "durch",
    "uber": "über",
    "unter": "unter",
    "vor": "vor",
    "hinter": "hinter",
    "zwischen": "zwischen",

    # Common German words
    "heute": "heute",
    "heissen": "heißen",
    "gross": "groß",
    "klein": "klein",
    "neu": "neu",
    "alt": "alt",
    "gut": "gut",
    "bose": "böse",
    "hass": "Haß",  # note ß
    "strasse": "straße",
    "platz": "Platz",
    "land": "Land",
    "stadt": "Stadt",
    "welt": "Welt",
    "menschen": "Menschen",
    "zeit": "Zeit",
    "tag": "Tag",
    "jahr": "Jahr",
    "geld": "Geld",
    "sache": "Sache",
    "wort": "Wort",
    "buch": "Buch",
    "haus": "Haus",
    "raum": "Raum",
    "arbeit": "Arbeit",
    "schule": "Schule",
    "klasse": "Klasse",
    "nummer": "Nummer",
    "telefon": "Telefon",
    "adresse": "Adresse",
    "email": "E-Mail",
    "internet": "Internet",
    "computer": "Computer",
    "programm": "Programm",
    "software": "Software",

    # ß replacements (ue/ae/oe) - reverse fix
    "ss": "ß",  # rarely correct, but in some contexts
    "Sser": "ßer",
    "ssen": "ßen",
}


def fix_diacritics_de(text: str) -> str:
    """
    Fix missing German umlauts and ß - HIGH CONFIDENCE ONLY.

    Rules applied:
    1. Known word dictionary (most reliable)
    2. Common ß patterns
    3. Common umlaut patterns

    NEVER change:
    - Words where "ss" is legitimately correct (not ß)
    - Unknown contexts
    """
    result = text

    # Known word fixes (highest confidence)
    # Separate uppercase and lowercase patterns to preserve case correctly
    # For compound words (Strasse, Mueller etc.), use lookbehind to match
    # after another word (no word boundary needed between word chars)
    word_fixes_lower = [
        (r'\bmueller\b', 'müller'),
        (r'\bmuelller\b', 'müller'),
        (r'\bmuller\b', 'müller'),
        (r'\bschuler\b', 'schüler'),
        (r'\bschuoler\b', 'schüler'),
        (r'\bburo\b', 'büro'),
        (r'\buber\b', 'über'),
        (r'\bfur\b', 'für'),
        (r'\bkonnen\b', 'können'),
        (r'\bmussen\b', 'müssen'),
        (r'\bsollen\b', 'sollen'),
        (r'\bwollen\b', 'wollen'),
        (r'\bdurfen\b', 'dürfen'),
        (r'\bmogen\b', 'mögen'),
        # Use lookbehind for compound words: preceded by lowercase letter
        (r'(?<=[a-z])strasse\b', 'straße'),
        (r'\bgross\b', 'groß'),
        (r'\bssigt?\b', 'ßigt'),
        (r'\bheissen\b', 'heißen'),
        (r'\bschon\b', 'schön'),
        (r'\bnachste\b', 'nächste'),
        (r'\bhaufig\b', 'häufig'),
        (r'\bzuruck\b', 'zurück'),
        (r'\buberall\b', 'überall'),
        (r'\bbereits\b', 'bereits'),
        (r'\bverstandnis\b', 'verständnis'),
        (r'\bgrosse\b', 'größe'),
        (r'\bmunchen\b', 'münchen'),
        (r'\bmuunchen\b', 'münchen'),
        (r'\bkoln\b', 'köln'),
    ]

    word_fixes_upper = [
        (r'\bMueller\b', 'Müller'),
        (r'\bMuelller\b', 'Müller'),
        (r'\bMuller\b', 'Müller'),
        (r'\bSchuler\b', 'Schüler'),
        (r'\bSchuoler\b', 'Schüler'),
        (r'\bBuro\b', 'Büro'),
        (r'\bUber\b', 'Über'),
        (r'\bFur\b', 'Für'),
        (r'\bKonnen\b', 'können'),
        (r'\bMussen\b', 'müssen'),
        (r'\bSollen\b', 'sollen'),
        (r'\bWollen\b', 'wollen'),
        (r'\bDurfen\b', 'dürfen'),
        (r'\bMogen\b', 'mögen'),
        (r'(?<=[A-Z])strasse\b', 'Straße'),  # HauptStrasse → HauptStraße
        (r'\bStrasse\b', 'Straße'),  # standalone Strasse
        (r'\bGross\b', 'Groß'),
        (r'\bHeissen\b', 'heißen'),
        (r'\bSchon\b', 'schön'),
        (r'\bNachste\b', 'nächste'),
        (r'\bHaufig\b', 'häufig'),
        (r'\bZuruck\b', 'zurück'),
        (r'\bUberall\b', 'überall'),
        (r'\bBereits\b', 'bereits'),
        (r'\bVerstandnis\b', 'Verständnis'),
        (r'\bGrosse\b', 'Größe'),
        (r'\bMunchen\b', 'München'),
        (r'\bMuunchen\b', 'München'),
        (r'\bKoln\b', 'Köln'),
        (r'\bFrankfurt\b', 'Frankfurt'),
        (r'\bDanke\b', 'Danke'),
    ]

    # Apply lowercase patterns (case-sensitive)
    for pattern, replacement in word_fixes_lower:
        result = re.sub(pattern, replacement, result)

    # Apply uppercase patterns (case-sensitive)
    for pattern, replacement in word_fixes_upper:
        result = re.sub(pattern, replacement, result)

    # ß → ss in specific contexts where it's commonly wrong
    # Only apply when we have high confidence
    # "dass" is always correct (not ß)

    return result


# Export typo dictionary for use in main processor
TYPO_DICT = GERMAN_TYPO_DICT
