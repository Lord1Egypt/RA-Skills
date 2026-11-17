from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path


TRANSITIONS_BY_LANGUAGE = {
    "de": re.compile(r"\b(?:erstens|zweitens|schließlich|darüber hinaus|außerdem|jedoch|deshalb|daher|inzwischen|zusammenfassend)\b", re.IGNORECASE),
    "zh": re.compile(r"首先|其次|最后|此外|另外|然而|因此|所以|与此同时|综上所述|总而言之|值得注意的是"),
    "ja": re.compile(r"まず|次に|最後に|さらに|しかし|したがって|そのため|一方で|要するに|結論として"),
    "en": re.compile(r"\b(?:firstly|secondly|finally|moreover|furthermore|however|therefore|meanwhile|in conclusion|to summarize|it is worth noting)\b", re.IGNORECASE),
    "fr": re.compile(r"\b(?:premi[eè]rement|deuxi[eè]mement|enfin|en outre|cependant|donc|par cons[eé]quent|en conclusion|en r[eé]sum[eé])\b", re.IGNORECASE),
    "es": re.compile(r"\b(?:primero|en segundo lugar|finalmente|adem[aá]s|sin embargo|por lo tanto|mientras tanto|en conclusi[oó]n|en resumen)\b", re.IGNORECASE),
    "pt": re.compile(r"\b(?:primeiro|em segundo lugar|finalmente|al[eé]m disso|no entanto|portanto|enquanto isso|em conclus[aã]o|em resumo)\b", re.IGNORECASE),
    "la": re.compile(r"\b(?:primum|deinde|denique|praeterea|tamen|igitur|interea|in summa)\b", re.IGNORECASE),
    "ar": re.compile(r"(?:أولاً|أولا|ثانياً|ثانيا|أخيراً|أخيرا|بالإضافة إلى ذلك|ومع ذلك|لذلك|في الختام|باختصار)"),
}
LATIN_LANGUAGE_MARKERS = {
    "de": re.compile(r"\b(?:der|die|das|und|dass|mit|für|ist|sind|ein|eine|nicht|darüber)\b", re.IGNORECASE),
    "en": re.compile(r"\b(?:the|and|that|with|from|this|is|are|of|to|in)\b", re.IGNORECASE),
    "fr": re.compile(r"\b(?:le|la|les|des|une|et|dans|avec|pour|est|sont|du)\b", re.IGNORECASE),
    "es": re.compile(r"\b(?:el|la|los|las|una|y|en|con|para|es|son|del|que)\b", re.IGNORECASE),
    "pt": re.compile(r"\b(?:o|a|os|as|uma|e|em|com|para|é|são|do|que)\b", re.IGNORECASE),
    "la": re.compile(r"\b(?:et|in|est|sunt|cum|ad|de|non|qui|quae|quod|per)\b", re.IGNORECASE),
}


@dataclass(frozen=True)
class StyleStatistics:
    language: str
    confidence: str
    character_count: int
    token_count: int
    sentence_count: int
    paragraph_count: int
    average_sentence_length: float
    sentence_length_cv: float
    paragraph_length_cv: float | None
    mattr: float | None
    repeated_trigram_ratio: float | None
    transition_density_per_1000: float | None
    warnings: tuple[str, ...]
    disclaimer: str = (
        "These are editing diagnostics, not evidence of AI authorship. "
        "Genre, language, length, and deliberate style affect every metric."
    )

    def to_dict(self) -> dict:
        result = asdict(self)
        result["warnings"] = list(self.warnings)
        return result


def _detect_language(text: str) -> str:
    han = len(re.findall(r"[\u3400-\u9fff]", text))
    kana = len(re.findall(r"[\u3040-\u30ff]", text))
    arabic = len(re.findall(r"[\u0600-\u06ff]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    if kana >= 4 and kana >= latin // 2:
        return "ja"
    if arabic >= max(10, latin):
        return "ar"
    if han >= max(20, latin) and kana < 4:
        return "zh"
    if latin >= max(20, (han + kana + arabic) * 2):
        scores = {
            language: len(pattern.findall(text))
            for language, pattern in LATIN_LANGUAGE_MARKERS.items()
        }
        language, score = max(scores.items(), key=lambda item: item[1])
        return language if score >= 2 else "latin"
    return "mixed"


def _tokens(text: str, language: str) -> list[str]:
    if language == "zh":
        return re.findall(r"[\u3400-\u9fff]|[A-Za-z0-9]+", text.lower())
    if language == "ja":
        return re.findall(r"[\u3400-\u9fff]|[\u3040-\u309f]|[\u30a0-\u30ff]|[A-Za-z0-9]+", text.lower())
    return re.findall(r"[^\W_]+(?:['’\-][^\W_]+)*", text.lower(), re.UNICODE)


ABBREVIATIONS = {
    "en": ("Mr", "Mrs", "Ms", "Dr", "Prof", "Sr", "Jr"),
    "de": ("Dr", "Prof", "Hr", "Fr"),
    "fr": ("M", "Mme", "Mlle", "Dr", "Pr"),
    "es": ("Sr", "Sra", "Srta", "Dr", "Dra", "Prof"),
    "pt": ("Sr", "Sra", "Dr", "Dra", "Prof"),
}


def _sentence_lengths(text: str, language: str) -> list[int]:
    # Mask internal punctuation without changing token boundaries. These are
    # conservative rules, not a complete linguistic sentence segmenter.
    masked = re.sub(r"(?<=\d)\.(?=\d)", "∯", text)
    masked = re.sub(r"\b(?:[A-Za-z]\.){2,}", lambda m: m.group().replace(".", "∯"), masked)
    names = ABBREVIATIONS.get(language, ())
    if names:
        masked = re.sub(r"\b(?:" + "|".join(names) + r")\.(?=\s+\S)",
                        lambda m: m.group().replace(".", "∯"), masked, flags=re.I)
    parts = [part.strip().replace("∯", ".") for part in re.split(r"[。！？.!?؟｡]+", masked) if part.strip()]
    return [len(_tokens(part, language)) for part in parts if _tokens(part, language)]


def _paragraph_lengths(text: str, language: str) -> list[int]:
    parts = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    return [len(_tokens(part, language)) for part in parts if _tokens(part, language)]


def _coefficient_of_variation(values: list[int]) -> float:
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    if mean == 0:
        return 0.0
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    return math.sqrt(variance) / mean


def _mattr(tokens: list[str], window: int = 50) -> float | None:
    if len(tokens) < 30:
        return None
    size = min(window, len(tokens))
    ratios = [
        len(set(tokens[index : index + size])) / size
        for index in range(len(tokens) - size + 1)
    ]
    return round(sum(ratios) / len(ratios), 3)


def _repeated_trigram_ratio(tokens: list[str]) -> float | None:
    if len(tokens) < 30:
        return None
    trigrams = [tuple(tokens[index : index + 3]) for index in range(len(tokens) - 2)]
    repeated = sum(count - 1 for count in Counter(trigrams).values() if count > 1)
    return round(repeated / max(len(trigrams), 1), 3)


def analyze_style_statistics(text: str, style: str = "general", language: str = "auto") -> StyleStatistics:
    if not isinstance(language, str) or not re.fullmatch(r"[a-z]{2,8}(?:-[A-Za-z0-9]{2,8})*", language):
        raise ValueError("Language must be auto or a language tag such as en, de, or pt-BR.")
    language = _detect_language(text) if language == "auto" else language.split("-", 1)[0]
    tokens = _tokens(text, language)
    sentence_lengths = _sentence_lengths(text, language)
    paragraph_lengths = _paragraph_lengths(text, language)
    sentence_cv = _coefficient_of_variation(sentence_lengths)
    paragraph_cv = (
        _coefficient_of_variation(paragraph_lengths) if len(paragraph_lengths) >= 3 else None
    )
    transition_pattern = TRANSITIONS_BY_LANGUAGE.get(language)
    transition_count = len(transition_pattern.findall(text)) if transition_pattern else None
    transition_density = transition_count * 1000 / max(len(tokens), 1) if transition_count is not None else None

    warnings: list[str] = []
    if transition_pattern is None:
        warnings.append("Transition markers are not covered for this language; density is unavailable, not zero.")
    serious = style in {"academic-paper", "formal-document", "news-report"}
    calibrated = language in {"zh", "en"}
    if not calibrated:
        warnings.append(
            "No validated language-and-genre thresholds for this profile; inspect metrics against native reference samples."
        )
    else:
        warnings.append("Thresholds are editorial heuristics, not independently validated quality or authorship measures.")
    if calibrated and len(sentence_lengths) >= 6 and sentence_cv < (0.12 if serious else 0.18):
        warnings.append("Sentence lengths are unusually uniform for this style and sample length.")
    if calibrated and paragraph_cv is not None and len(paragraph_lengths) >= 5 and paragraph_cv < 0.16:
        warnings.append("Paragraph blocks are unusually uniform; verify that breaks mark real turns.")
    trigram_ratio = _repeated_trigram_ratio(tokens)
    if calibrated and trigram_ratio is not None and trigram_ratio > (0.18 if serious else 0.12):
        warnings.append("Repeated three-token sequences are dense; inspect phrase and transition reuse.")
    if calibrated and len(tokens) >= 100 and transition_density is not None and transition_density > (35 if serious else 22):
        warnings.append("Explicit transition markers are dense relative to the sample length.")

    confidence = "low" if len(tokens) < 120 else "medium" if len(tokens) < 400 else "high"
    return StyleStatistics(
        language=language,
        confidence=confidence,
        character_count=len(text),
        token_count=len(tokens),
        sentence_count=len(sentence_lengths),
        paragraph_count=len(paragraph_lengths),
        average_sentence_length=round(
            sum(sentence_lengths) / max(len(sentence_lengths), 1), 2
        ),
        sentence_length_cv=round(sentence_cv, 3),
        paragraph_length_cv=round(paragraph_cv, 3) if paragraph_cv is not None else None,
        mattr=_mattr(tokens),
        repeated_trigram_ratio=trigram_ratio,
        transition_density_per_1000=round(transition_density, 2) if transition_density is not None else None,
        warnings=tuple(warnings),
    )


def analyze_style_file(path: str, style: str = "general", language: str = "auto") -> StyleStatistics:
    return analyze_style_statistics(Path(path).read_text(encoding="utf-8"), style=style, language=language)


def format_style_statistics(report: StyleStatistics, output_format: str = "markdown") -> str:
    if output_format == "json":
        return json.dumps(report.to_dict(), ensure_ascii=False, indent=2) + "\n"
    rows = [
        "# Style Statistics",
        "",
        f"- Language profile: `{report.language}`",
        f"- Confidence: `{report.confidence}`",
        f"- Tokens / sentences / paragraphs: `{report.token_count}` / `{report.sentence_count}` / `{report.paragraph_count}`",
        f"- Average sentence length: `{report.average_sentence_length}`",
        f"- Sentence-length CV: `{report.sentence_length_cv}`",
        f"- Paragraph-length CV: `{report.paragraph_length_cv if report.paragraph_length_cv is not None else 'n/a'}`",
        f"- MATTR: `{report.mattr if report.mattr is not None else 'n/a'}`",
        f"- Repeated trigram ratio: `{report.repeated_trigram_ratio if report.repeated_trigram_ratio is not None else 'n/a'}`",
        f"- Transition density / 1000 tokens: `{report.transition_density_per_1000 if report.transition_density_per_1000 is not None else 'n/a'}`",
        f"- Disclaimer: {report.disclaimer}",
        "",
        "## Warnings",
        "",
    ]
    rows.extend(f"- {warning}" for warning in report.warnings)
    if not report.warnings:
        rows.append("- No threshold warning; inspect the metrics in genre context.")
    return "\n".join(rows) + "\n"
