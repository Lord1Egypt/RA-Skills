"""
i18n_processor.py — Main entry point for OpenClaw i18n post-processing.

Usage:
    from i18n_processor import process
    cleaned = process(raw_output, language_code)
    # send 'cleaned' to user

Language codes: 'ro', 'de', 'fr', 'es', 'en' (passthrough)
"""

from languages import base, ro, de, fr, es


def process(text: str, language: str) -> str:
    """
    Main entry point. Takes raw model output and language code.
    Returns cleaned text ready to send to user.

    Processing order:
    1. Base rules (always applied)
    2. Language-specific rules (if supported)

    Args:
        text: Raw output from the model
        language: Language code ('ro', 'de', 'fr', 'es', 'en')

    Returns:
        Cleaned text with diacritics fixed, stray chars removed, etc.
    """
    if not text:
        return text

    # Step 1: Always apply base rules (language-agnostic)
    text = base.remove_non_latin_characters(text)
    text = base.normalize_whitespace(text)

    # Step 2: Language-specific processing
    if language == 'ro':
        text = ro.fix_diacritics_ro(text)
        text = ro.fix_stray_chars_ro(text)
        text = base.fix_common_typos(text, ro.TYPO_DICT)
    elif language == 'de':
        text = de.fix_diacritics_de(text)
        text = base.fix_common_typos(text, de.TYPO_DICT)
    elif language == 'fr':
        text = fr.fix_diacritics_fr(text)
        text = base.fix_common_typos(text, fr.TYPO_DICT)
    elif language == 'es':
        text = es.fix_diacritics_es(text)
        text = base.fix_common_typos(text, es.TYPO_DICT)
    elif language == 'en':
        # English passthrough — apply only base rules
        pass
    else:
        # Unknown language — apply base rules only, no language-specific
        pass

    # Step 3: Final pass — fix merged words (conservative)
    text = base.fix_merged_words(text)

    return text


def process_ro(text: str) -> str:
    """Convenience function for Romanian."""
    return process(text, 'ro')


def process_de(text: str) -> str:
    """Convenience function for German."""
    return process(text, 'de')


def get_supported_languages() -> list:
    """Return list of supported language codes."""
    return ['ro', 'de', 'fr', 'es', 'en']


if __name__ == '__main__':
    # Simple CLI test
    import sys

    if len(sys.argv) < 3:
        print("Usage: python i18n_processor.py <text> <language_code>")
        print("Example: python i18n_processor.py 'stiu' ro")
        sys.exit(1)

    text = sys.argv[1]
    lang = sys.argv[2]

    result = process(text, lang)
    print(f"Input:  {text}")
    print(f"Output: {result}")
