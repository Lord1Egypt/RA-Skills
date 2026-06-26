from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, List, Optional


TranslateFn = Callable[..., str]


@dataclass
class TranslationBundle:
    original_fa: str
    english: str
    arabic: str
    chinese: str


def _simple_fallback(text: str, target_lang: str) -> str:
    if target_lang == "en":
        return f"[EN fallback] {text}"
    if target_lang == "ar":
        return f"[AR fallback] {text}"
    if target_lang == "zh":
        return f"[ZH fallback] {text}"
    return text


def translate_text_multi(
    text: str,
    translate_text_tool: Optional[TranslateFn] = None,
    languages: Optional[Iterable[str]] = None,
) -> Dict[str, str]:
    requested = list(languages or ["en", "ar", "zh"])
    out: Dict[str, str] = {}

    for lang in requested:
        if translate_text_tool is None:
            out[lang] = _simple_fallback(text, lang)
            continue
        try:
            out[lang] = translate_text_tool(text=text, source_lang="fa", target_lang=lang)
        except Exception:
            out[lang] = _simple_fallback(text, lang)

    return out


def build_translation_bundle(
    text: str,
    translate_text_tool: Optional[TranslateFn] = None,
    languages: Optional[Iterable[str]] = None,
) -> TranslationBundle:
    translated = translate_text_multi(
        text=text,
        translate_text_tool=translate_text_tool,
        languages=languages,
    )
    return TranslationBundle(
        original_fa=text,
        english=translated.get("en", _simple_fallback(text, "en")),
        arabic=translated.get("ar", _simple_fallback(text, "ar")),
        chinese=translated.get("zh", _simple_fallback(text, "zh")),
    )
