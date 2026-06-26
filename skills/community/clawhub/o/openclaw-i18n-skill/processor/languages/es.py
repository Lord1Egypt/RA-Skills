"""
Spanish-specific diacritics and typo corrections.
HIGH CONFIDENCE ONLY — false positives are worse than leaving errors.
"""
import re


# Common Spanish words that models frequently get wrong
# Format: "wrong_form": "correct_form"
SPANISH_TYPO_DICT = {
    # Accent on vowels (á, é, í, ó, ú, ü)
    "año": "año",
    "años": "años",
    "niño": "niño",
    "niños": "niños",
    "niña": "niña",
    "niñas": "niñas",
    "español": "español",
    "española": "española",
    "mañana": "mañana",
    "mañanas": "mañanas",
    "cami\u00f3n": "camión",
    "cami\u00f3nes": "camiones",
    "electrico": "eléctrico",
    "publico": "público",
    "publica": "pública",
    "periodico": "periódico",
    "historico": "histórico",
    "grafico": "gráfico",
    "politico": "político",
    "politica": "política",
    "farmaco": "fármaco",
    "estatico": "estático",
    "tomate": "tomate",
    "habitacion": "habitación",
    "ubicaci\u00f3n": "ubicación",
    "telefono": "teléfono",
    "numero": "número",
    "canci\u00f3n": "canción",
    "raz\u00f3n": "razón",
    "coraci\u00f3n": "corazón",
    "relaci\u00f3n": "relación",
    "emoci\u00f3n": "emoción",
    "acci\u00f3n": "acción",
    "direcci\u00f3n": "dirección",
    "succi\u00f3n": "succión",
    "expresi\u00f3n": "expresión",
    "imagen": "imagen",
    "imágener": "imagen",
    "lavabo": "lavabo",
    "jab\u00f3n": "jabón",
    "mujer": "mujer",
    "hombre": "hombre",
    "ni\u00f1o": "niño",
    "espa\u00f1ol": "español",

    # Accent on "é" in verbs and nouns
    "cafe": "café",
    "sofá": "sofá",
    "chévere": "chévere",
    "revés": "revés",
    "pingüino": "pingüino",
    "güey": "güey",
    "búho": "búho",
    "albúmul": "albúmul",

    # Accent on "ó"
    "móvil": "móvil",
    "carro": "carro",
    "voz": "voz",
    "no": "no",
    "só": "só",
    "pero": "pero",
    "só": "só",
    "ará": "ará",

    # Accent on "í"
    "ší": "shí",
    "papá": "papá",
    "café": "café",
    "maripí": "maripí",

    # Common verb forms with accents
    "est\u00e1": "está",
    "est\u00e1s": "estás",
    "est\u00e1": "está",
    "est\u00e1amos": "estábamos",
    "est\u00e1is": "estáis",
    "est\u00e1n": "están",
    "est\u00e1": "está",
    "estabamos": "estábamos",
    "tienen": "tienen",
    "tiene": "tiene",
    "digan": "dígan",
    "digame": "dígame",
    "expl\u00edqueme": "explíqueme",
    "h\u00e1game": "hágame",
    "d\u00e9jeme": "déjeme",
    "cr\u00e9ame": "créame",
    "b\u00fasque": "busque",
    "qu\u00e9": "qué",
    "c\u00f3mo": "cómo",
    "d\u00f3nde": "dónde",
    "cu\u00e1ndo": "cuándo",
    "qui\u00e9n": "quién",
    "qui\u00e9nes": "quiénes",
    "cu\u00e1l": "cuál",
    "cu\u00e1les": "cuáles",

    # por / para confusions (handled via context)
    # These are lower confidence — skip in v1

    # Common Spanish words
    "gracias": "gracias",
    "hola": "hola",
    "buenos": "buenos",
    "buenas": "buenas",
    "días": "días",
    "noches": "noches",
    "años": "años",
    "favor": "favor",
    "favorito": "favorito",
    "favorita": "favorita",
    "importante": "importante",
    "diferente": "diferente",
    "mejor": "mejor",
    "peor": "peor",
    "mayor": "mayor",
    "menor": "menor",
    "primero": "primero",
    "primera": "primera",
    "último": "último",
    "última": "última",
    "próximo": "próximo",
    "próxima": "próxima",
    "nuevo": "nuevo",
    "nueva": "nueva",
    "bueno": "bueno",
    "buena": "buena",
    "malo": "malo",
    "mala": "mala",
    "pequeño": "pequeño",
    "pequeña": "pequeña",
    "grande": "grande",
    "pequeño": "pequeño",
    "hermoso": "hermoso",
    "hermosa": "hermosa",
    "lindo": "lindo",
    "linda": "linda",
    "muchacho": "muchacho",
    "muchacha": "muchacha",
    "chico": "chico",
    "chica": "chica",
    "amigo": "amigo",
    "amiga": "amiga",
    "familia": "familia",
    "padre": "padre",
    "madre": "madre",
    "hermano": "hermano",
    "hermana": "hermana",
    "hijo": "hijo",
    "hija": "hija",
    "esposo": "esposo",
    "esposa": "esposa",
    "novio": "novio",
    "novia": "novia",
    "trabajo": "trabajo",
    "oficina": "oficina",
    "empresa": "empresa",
    "negocio": "negocio",
    "dinero": "dinero",
    "tiempo": "tiempo",
    "persona": "persona",
    "gente": "gente",
    "mundo": "mundo",
    "país": "país",
    "ciudad": "ciudad",
    "calle": "calle",
    "casa": "casa",
    "habitación": "habitación",
    "comida": "comida",
    "agua": "agua",
    "aire": "aire",
    "fuego": "fuego",
    "tierra": "tierra",
}


def fix_diacritics_es(text: str) -> str:
    """
    Fix missing Spanish diacritics — HIGH CONFIDENCE ONLY.

    Rules applied:
    1. Known word dictionary (most reliable)
    2. Common accent patterns for interrogatives (qué, cómo, dónde, etc.)
    3. Common verb forms

    NEVER change:
    - "si" (if) vs "sí" (yes) — ambiguous without context
    - "el" (the) vs "él" (he) — ambiguous without context
    - "tu" (your) vs "tú" (you) — ambiguous without context
    - Unknown contexts
    """
    result = text

    # High-confidence accent fixes
    word_fixes_lower = [
        # ñ corrections
        (r'\beñol\b', 'español'),
        (r'\bEspañol\b', 'Español'),
        (r'\bni\u00f1o\b', 'niño'),
        (r'\bni\u00f1os\b', 'niños'),
        (r'\bni\u00f1a\b', 'niña'),
        (r'\bni\u00f1as\b', 'niñas'),
        (r'\ba\u00f1o\b', 'año'),
        (r'\ba\u00f1os\b', 'años'),
        (r'\bma\u00f1ana\b', 'mañana'),
        # Accent corrections (high confidence)
        (r'\belectrico\b', 'eléctrico'),
        (r'\bpublico\b', 'público'),
        (r'\bpublica\b', 'pública'),
        (r'\bperiodico\b', 'periódico'),
        (r'\bhistorico\b', 'histórico'),
        (r'\bgrafico\b', 'gráfico'),
        (r'\btelefono\b', 'teléfono'),
        (r'\bnumero\b', 'número'),
        (r'\bcanci\u00f3n\b', 'canción'),
        (r'\braz\u00f3n\b', 'razón'),
        (r'\bcoraci\u00f3n\b', 'corazón'),
        (r'\brelaci\u00f3n\b', 'relación'),
        (r'\bemoci\u00f3n\b', 'emoción'),
        (r'\bacci\u00f3n\b', 'acción'),
        (r'\bdirecci\u00f3n\b', 'dirección'),
        (r'\bexpresi\u00f3n\b', 'expresión'),
        (r'\bjab\u00f3n\b', 'jabón'),
        (r'\bubi\u00f3n\b', 'ubićón'),
        (r'\bubi\u00f3n\b', 'ubicación'),
        # café
        (r'\bcafe\b', 'café'),
        # móvil
        (r'\bmovil\b', 'móvil'),
        # pingüino / güey
        (r'\bpinguino\b', 'pingüino'),
        (r'\bguey\b', 'güey'),
        # Interrogatives — very common
        (r'\bque\b', 'qué'),
        (r'\bcomo\b', 'cómo'),
        (r'\bdonde\b', 'dónde'),
        (r'\bcuando\b', 'cuándo'),
        (r'\bquien\b', 'quién'),
        (r'\bquienes\b', 'quiénes'),
        (r'\bcual\b', 'cuál'),
        (r'\bcuales\b', 'cuáles'),
        # Verb accents
        (r'\best\u00e1\b', 'está'),
        (r'\best\u00e1s\b', 'estás'),
        (r'\best\u00e1n\b', 'están'),
        (r'\bestabamos\b', 'estábamos'),
        (r'\bd\u00e9jame\b', 'déjame'),
        (r'\bd\u00edgame\b', 'dígame'),
        (r'\bh\u00e1game\b', 'hágame'),
        (r'\bcr\u00e9eme\b', 'créeme'),
        (r'\bexpl\u00edqueme\b', 'explíqueme'),
        # "sí" (yes) — fix when standalone
        (r'\bsi\b', 'sí'),
    ]

    word_fixes_upper = [
        (r'\bEspa\u00f1ol\b', 'Español'),
        (r'\bNi\u00f1o\b', 'Niño'),
        (r'\bNi\u00f1os\b', 'Niños'),
        (r'\bNi\u00f1a\b', 'Niña'),
        (r'\bA\u00f1o\b', 'Año'),
        (r'\bA\u00f1os\b', 'Años'),
        (r'\bMa\u00f1ana\b', 'Mañana'),
        (r'\bElectrico\b', 'Eléctrico'),
        (r'\bPublico\b', 'Público'),
        (r'\bPublica\b', 'Pública'),
        (r'\bPeriodico\b', 'Periódico'),
        (r'\bHistorico\b', 'Histórico'),
        (r'\bGrafico\b', 'Gráfico'),
        (r'\bTelefono\b', 'Teléfono'),
        (r'\bNumero\b', 'Número'),
        (r'\bCanci\u00f3n\b', 'Canción'),
        (r'\bRaz\u00f3n\b', 'Razón'),
        (r'\bCoraci\u00f3n\b', 'Corazón'),
        (r'\bRelaci\u00f3n\b', 'Relación'),
        (r'\bEmoci\u00f3n\b', 'Emoción'),
        (r'\bAcci\u00f3n\b', 'Acción'),
        (r'\bDirecci\u00f3n\b', 'Dirección'),
        (r'\bExpresi\u00f3n\b', 'Expresión'),
        (r'\bCafe\b', 'Café'),
        (r'\bM\u00f3vil\b', 'Móvil'),
        (r'\bQu\u00e9\b', 'Qué'),
        (r'\bC\u00f3mo\b', 'Cómo'),
        (r'\bD\u00f3nde\b', 'Dónde'),
        (r'\bCu\u00e1ndo\b', 'Cuándo'),
        (r'\bQui\u00e9n\b', 'Quién'),
        (r'\bQui\u00e9nes\b', 'Quiénes'),
        (r'\bCu\u00e1l\b', 'Cuál'),
        (r'\bCu\u00e1les\b', 'Cuáles'),
        (r'\bEspa\u00f1ola\b', 'Española'),
    ]

    for pattern, replacement in word_fixes_lower:
        result = re.sub(pattern, replacement, result)

    for pattern, replacement in word_fixes_upper:
        result = re.sub(pattern, replacement, result)

    return result


# Export typo dictionary for use in main processor
TYPO_DICT = SPANISH_TYPO_DICT
