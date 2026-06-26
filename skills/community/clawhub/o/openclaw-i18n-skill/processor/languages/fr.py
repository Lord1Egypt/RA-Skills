"""
French-specific diacritics and typo corrections.
HIGH CONFIDENCE ONLY — false positives are worse than leaving errors.
"""
import re


# Common French words that models frequently get wrong
# Format: "wrong_form": "correct_form"
FRENCH_TYPO_DICT = {
    # Accents on vowels
    "etude": "étude",
    "etudes": "études",
    "etudier": "étudier",
    "eleve": "élève",
    "eleves": "élèves",
    "ecole": "école",
    "facile": "facile",
    "difficile": "difficile",
    "interet": "intérêt",
    "interets": "intérêts",
    "societe": "société",
    "celebre": "célèbre",
    "prefere": "préféré",
    "preferee": "préférée",
    "communaute": "communauté",
    "academie": "académie",
    "anime": "animé",
    "cafe": "café",
    "foi": "foi",
    "honnetete": "honnêteté",
    "jevais": "je vais",
    "jesuis": "je suis",
    "television": "télévision",
    "heure": "heure",
    " heures": " heures",
    "peutetre": "peut-être",
    "quatrem": "quatre",
    "francais": "français",
    "francaise": "française",
    "etranger": "étranger",
    "etrangere": "étrangère",
    " deja ": " déjà ",
    "ca": "ça",
    "ca va": "ça va",
    "ou": "où",
    "la bas": "là-bas",
    "ej": "e.g.",
    "i.e.": "c.-à-d.",
    "e.g.": "p. ex.",
    "note": "note",
    "entre": "entre",
    "apres": "après",
    "tres": "très",
    "petit": "petit",
    "petits": "petits",
    "grands": "grands",
    "meme": "même",
    "mem": "mêm",
    "daccord": "d'accord",
    "aujourd": "aujourd'",
    "hui": "hui",
    "lorsque": "lorsque",
    "puisque": "puisque",
    "quoique": "quoique",
    "celui": "celui",
    "celle": "celle",
    "ceux": "ceux",
    "celles": "celles",
    "tous": "tous",
    "tout": "tout",
    "toute": "toute",
    "toutes": "toutes",
    "beaucoup": "beaucoup",
    "beacoup": "beaucoup",
    "quelque": "quelque",
    "quelques": "quelques",
    "chacun": "chacun",
    "chacune": "chacune",
    "personne": "personne",
    "rien": "rien",
    "autre": "autre",
    "autres": "autres",
    "premier": "premier",
    "premiere": "première",
    "second": "second",
    "seconde": "seconde",
    "dernier": "dernier",
    "derniere": "dernière",
    "nouveau": "nouveau",
    "nouvelle": "nouvelle",
    "petit": "petit",
    "grande": "grande",
    "jeune": "jeune",
    "vieux": "vieux",
    "vieille": "vieille",
    "bel": "bel",
    "belle": "belle",
    "nouvel": "nouvel",
    "nouvelle": "nouvelle",
}


def fix_diacritics_fr(text: str) -> str:
    """
    Fix missing French diacritics — HIGH CONFIDENCE ONLY.

    Rules applied:
    1. Known word dictionary (most reliable)
    2. Common accent patterns for verbs and common words

    NEVER change:
    - Words where accent is ambiguous (many French vowels sound the same)
    - Unknown contexts — leave as-is
    """
    result = text

    # Known word fixes — separate lowercase and uppercase
    word_fixes_lower = [
        # Accent corrections (highest confidence)
        (r'\betude\b', 'étude'),
        (r'\betudes\b', 'études'),
        (r'\betudier\b', 'étudier'),
        (r'\beleve\b', 'élève'),
        (r'\beleves\b', 'élèves'),
        (r'\becole\b', 'école'),
        (r'\binteret\b', 'intérêt'),
        (r'\binterets\b', 'intérêts'),
        (r'\bsociete\b', 'société'),
        (r'\bcelebre\b', 'célèbre'),
        (r'\bprefere\b', 'préféré'),
        (r'\bpreferee\b', 'préférée'),
        (r'\bcommunaute\b', 'communauté'),
        (r'\bacademie\b', 'académie'),
        (r'\banime\b', 'animé'),
        (r'\bcafe\b', 'café'),
        (r'\bhonnetete\b', 'honnêteté'),
        (r'\btelevision\b', 'télévision'),
        (r'\bfrancais\b', 'français'),
        (r'\bfrancaise\b', 'française'),
        (r'\betranger\b', 'étranger'),
        (r'\betrangere\b', 'étrangère'),
        # Accent on "ou" — où (where) vs ou (or)
        # Only fix when clearly "where" — in questions
        (r'\boù\b', 'où'),
        # Common "e" → "é" at start of words
        (r'\bepoque\b', 'époque'),
        (r'\beffet\b', 'effet'),
        (r'\befforts\b', 'efforts'),
        (r'\beleve\b', 'élève'),
        (r'\belevee\b', 'élevée'),
        (r'\bexecution\b', 'exécution'),
        (r'\bexemple\b', 'exemple'),
        (r'\beleve\b', 'élève'),
        # Common words
        (r'\bdiffcile\b', 'difficile'),
        (r'\bfacile\b', 'facile'),
        (r'\btres\b', 'très'),
        (r'\bpeutetre\b', 'peut-être'),
        (r'\b deja ', ' déjà '),
        (r'\bca\b', 'ça'),
        (r'\bdaccord\b', "d'accord"),
        (r'\bnimportequoi\b', "n'importe quoi"),
        (r'\bnimporte quoi\b', "n'importe quoi"),
        (r'\bquiestce\b', "qu'est-ce"),
        (r'\bjesuis\b', 'je suis'),
        (r'\bjevais\b', 'je vais'),
        # "e" → "è" before consonant + "e" (common pattern)
        # Only very specific high-confidence patterns
        (r'\bsn\b', 'sûr'),
    ]

    word_fixes_upper = [
        (r'\bEtude\b', 'Étude'),
        (r'\bEtudes\b', 'Études'),
        (r'\bEleve\b', 'Élève'),
        (r'\bEleves\b', 'Élèves'),
        (r'\bEcole\b', 'École'),
        (r'\bInteret\b', 'Intérêt'),
        (r'\bInterets\b', 'Intérêts'),
        (r'\bSociete\b', 'Société'),
        (r'\bCelebre\b', 'Célèbre'),
        (r'\bPrefere\b', 'Préféré'),
        (r'\bPreferee\b', 'Préférée'),
        (r'\bCommunaute\b', 'Communauté'),
        (r'\bAcademie\b', 'Académie'),
        (r'\bAnime\b', 'Animé'),
        (r'\bCafe\b', 'Café'),
        (r'\bHonnetete\b', 'Honnêteté'),
        (r'\bTelevision\b', 'Télévision'),
        (r'\bFrancais\b', 'Français'),
        (r'\bFrancaise\b', 'Française'),
        (r'\bEtranger\b', 'Étranger'),
        (r'\bEtrangere\b', 'Étrangère'),
        (r'\bEpoque\b', 'Époque'),
        (r'\bExemple\b', 'Exemple'),
        (r'\bExecution\b', 'Exécution'),
    ]

    for pattern, replacement in word_fixes_lower:
        result = re.sub(pattern, replacement, result)

    for pattern, replacement in word_fixes_upper:
        result = re.sub(pattern, replacement, result)

    return result


# Export typo dictionary for use in main processor
TYPO_DICT = FRENCH_TYPO_DICT
