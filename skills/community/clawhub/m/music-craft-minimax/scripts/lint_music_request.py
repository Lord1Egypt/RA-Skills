#!/usr/bin/env python3
"""Heuristic linter for Music Skills request routing and prompt quality.

The linter produces a JSON payload describing:

- The request type (cover, style_transfer, mashup, emotion_prompt, ...)
- The route to take: ``base_prompt``, ``minimax_cover``, ``minimax_mashup``,
  ``minimax_style_transfer``, ``minimax_emotion_prompt``, or
  ``needs_clarification`` when blockers are present
- The detected fields with confidence levels (clear, inferred, missing)
- Missing fields, blockers, and prompt warnings
- Conflicts between the natural-language prompt and the ``mmx`` flags
- Retry guidance when prompt and flags disagree

The linter depends only on the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


LANGUAGE_PATTERNS = [
    ("Spanish", [r"\bspanish\b", r"\ben espa(?:ñ|n)ol\b", r"\bcastellano\b"]),
    ("French", [r"\bfrench\b", r"\ben fran(?:ç|c)ais\b"]),
    ("English", [r"\benglish\b", r"\bin english\b"]),
    ("Portuguese", [r"\bportuguese\b", r"\bem portugu(?:ê|e)s\b"]),
    ("Italian", [r"\bitalian\b", r"\bin italiano\b"]),
]

INSTRUMENT_WORDS = [
    "accordion",
    "bass",
    "brass",
    "cello",
    "choir",
    "drums",
    "flute",
    "guitar",
    "harp",
    "kazoo",
    "kick",
    "piano",
    "percussion",
    "saxophone",
    "strings",
    "synth",
    "synths",
    "tambourine",
    "trumpet",
    "ukulele",
    "violin",
]

VAGUE_PHRASES = [
    "make it good",
    "make this good",
    "make it better",
    "emotional",
    "epic",
    "vibes",
]

GENRE_WORDS = [
    "acoustic",
    "ballad",
    "blues",
    "chanson",
    "cinematic",
    "country",
    "electronic",
    "folk",
    "jazz",
    "jingle",
    "latin",
    "lofi",
    "lo-fi",
    "pop",
    "reggaeton",
    "rock",
    "synthwave",
]

MOOD_WORDS = [
    "angry",
    "bright",
    "celebratory",
    "dark",
    "dramatic",
    "energetic",
    "happy",
    "hopeful",
    "melancholic",
    "romantic",
    "sad",
    "tender",
    "uplifting",
]

ANTI_SPARSE_PATTERNS = [
    r"\bnever go a cappella\b",
    r"\ball instruments always playing\b",
    r"\bavoid sparse,\s*a cappella\b",
    r"\bavoid sparse,?\s*minimal arrangement\b",
    r"\banti-sparse\b",
    r"\bno sparse\b",
]

PROMPT_LENGTH_WARN_BYTES = 1800
PROMPT_LENGTH_ERROR_BYTES = 2000

LYRICS_PROVIDED_PATTERNS = [
    r"\bhere are (?:the )?lyrics\b",
    r"\bprovided lyrics\b",
    r"\bmy lyrics\b",
    r"\bthese lyrics\b",
    r"\blyrics\s*:",
]

LYRICS_GENERATED_PATTERNS = [
    r"\bwrite(?:\s+(?:new|original|fresh|translated|rewritten|[a-z]{2,12})){0,4}\s+lyrics\b",
    r"\bgenerate(?:\s+(?:new|original|fresh|translated|rewritten|[a-z]{2,12})){0,4}\s+lyrics\b",
    r"\bnew lyrics\b",
    r"\boriginal lyrics\b",
    r"\brewritten lyrics\b",
    r"\btranslated lyrics\b",
]

ALLOWED_LYRICS_TAGS = {
    "intro",
    "verse",
    "pre chorus",
    "chorus",
    "bridge",
    "outro",
    "interlude",
    "transition",
    "post chorus",
    "hook",
    "break",
    "build up",
    "inst",
    "solo",
    "instrumental",
    "instrumental break",
}

LYRICS_TAG_RE = re.compile(r"\[[^\]]+\]")
VOWEL_GROUP_RE = re.compile(r"[aeiouyAEIOUYáéíóúÁÉÍÓÚàèìòùÀÈÌÒÙäëïöüÄËÏÖÜãõÃÕâêîôûÂÊÎÔÛ]+")
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ']+")


def _field(value: Any, confidence: str) -> dict[str, Any]:
    return {"value": value, "confidence": confidence}


def _read_text_file(path: str | None) -> str:
    if not path:
        return ""
    return Path(path).read_text(encoding="utf-8")


def _load_flags(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    data = json.loads(_read_text_file(path))
    if not isinstance(data, dict):
        raise ValueError("mmx flags JSON must be an object")
    return data


def _normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _extract_theme(text: str) -> str | None:
    patterns = [
        r"\babout\s+([^.;:!?]+)",
        r"\babout the\s+([^.;:!?]+)",
        r"\bsobre\s+([^.;:!?]+)",
        r"\babout a\s+([^.;:!?]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            theme = _normalize_space(match.group(1))
            theme = re.sub(r"^(?:a|an|the)\s+", "", theme, flags=re.IGNORECASE)
            return theme
    return None


def _detect_language(text: str) -> tuple[str, str]:
    for language, patterns in LANGUAGE_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, text, flags=re.IGNORECASE):
                return language, "clear"
    return "missing", "missing"


def _detect_genre(text: str) -> tuple[str, str]:
    lowered = text.lower()
    found = [word for word in GENRE_WORDS if re.search(rf"\b{re.escape(word)}\b", lowered)]
    if found:
        return ", ".join(dict.fromkeys(found)), "clear"
    return "missing", "missing"


def _detect_mood(text: str) -> tuple[str, str]:
    lowered = text.lower()
    found = [word for word in MOOD_WORDS if re.search(rf"\b{re.escape(word)}\b", lowered)]
    if found:
        return ", ".join(dict.fromkeys(found)), "clear"
    return "missing", "missing"


def _detect_duration(text: str) -> tuple[str, str]:
    # Word-boundary pattern for "30 seconds", "3 second", "3 min", "3 mins", etc.
    match = re.search(r"\b(\d{1,2})[\s-]*(?:second|seconds|sec|secs|s|minute|minutes|min|mins)\b", text, flags=re.IGNORECASE)
    if match:
        amount = match.group(1)
        unit_raw = text[match.start() + len(amount):match.end()].strip()
        # Determine unit from the captured text (not the match group, which is just digits)
        # Strip leading whitespace/hyphens then check first char or abbreviation.
        unit_stripped = unit_raw.lstrip("- \t")
        if unit_stripped.lower().startswith("m") and not unit_stripped.lower().startswith("ms"):
            return f"{amount} minutes", "clear"
        return f"{amount} seconds", "clear"
    # MM:SS time notation like "3:00" or "4:30"
    match = re.search(r"\b(\d{1,2}):(\d{2})\b", text)
    if match:
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        total_seconds = minutes * 60 + seconds
        return f"{total_seconds} seconds", "clear"
    return "missing", "missing"


def _has_pattern(patterns: list[str], text: str) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)


def _detect_lyrics_source(text: str, lyrics_text: str = "") -> tuple[str, str]:
    lowered = text.lower()
    if lyrics_text.strip():
        return "lyrics_file", "clear"
    if any(token in lowered for token in ("audio file", "audio", "song file", ".mp3", ".wav", ".flac", ".m4a")):
        if any(token in lowered for token in ("lyrics", "lyric", "transcript", "words")):
            return "provided_or_extracted", "inferred"
        return "source_audio_or_url", "inferred"
    if _has_pattern(LYRICS_PROVIDED_PATTERNS, text):
        return "provided", "inferred"
    if _has_pattern(LYRICS_GENERATED_PATTERNS, text):
        return "generated_requested", "clear"
    return "missing", "missing"


def _detect_vocal_mode(text: str) -> tuple[str, str]:
    lowered = text.lower()
    if any(token in lowered for token in ("instrumental", "no vocals", "without vocals", "no singing", "jingle")):
        return "instrumental", "clear"
    if any(token in lowered for token in ("male vocal", "female vocal", "vocal", "voice")):
        return "vocal", "inferred"
    return "missing", "missing"


def _detect_references(text: str) -> tuple[str, str]:
    lowered = text.lower()
    if any(token in lowered for token in ("audio file", "audio source", "source audio", ".mp3", ".wav", ".flac", ".m4a")):
        return "audio source", "inferred"
    if "style of" in lowered or "similar to" in lowered or "like " in lowered:
        return "style reference", "inferred"
    if re.search(r"https?://|\bwww\.", lowered):
        return "url reference", "inferred"
    return "missing", "missing"


URL_HOST_RE = re.compile(r"https?://", re.IGNORECASE)
LOCAL_AUDIO_EXTS = {".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac", ".wma", ".opus"}


def _detect_source_type(text: str) -> tuple[str, str]:
    """Return (source_type, confidence).

    v1.5.0: only two outcomes plus an unknown fallback.
    - ``"local"`` : a local audio file path was mentioned.
    - ``"url"``   : any http(s):// URL was mentioned. The published skill
      refuses URLs and asks the user for a local file path, so the linter
      surfaces this through ``source_type == "url"`` and ``build_result``
      emits a ``url_not_accepted`` warning.
    - ``"unknown"`` if neither was found.
    """
    if URL_HOST_RE.search(text):
        return "url", "inferred"
    # Local audio file: a path-like token with a recognised extension. A
    # '://' in the token means it's a URL, not a local path, so we skip those.
    for match in re.finditer(r"\S+", text):
        token = match.group(0)
        if "://" in token:
            continue
        suffix = Path(token).suffix.lower()
        if suffix in LOCAL_AUDIO_EXTS:
            return "local", "inferred"
    return "unknown", "missing"


def _request_type(text: str) -> str:
    lowered = text.lower()
    if "style transfer" in lowered and not any(token in lowered for token in ("cover", "keep the melody", "preserve melody")):
        return "style_transfer"
    if any(token in lowered for token in ("cover", "reinterpret", "reimagine", "keep the melody", "preserve melody")):
        return "cover"
    if any(token in lowered for token in ("mashup", "blend", "combine two songs", "merge two songs", "mash up")):
        return "mashup"
    if any(token in lowered for token in ("emotion analysis", "mood analysis", "emotional arc", "feeling curve")):
        return "emotion_prompt"
    if any(token in lowered for token in ("precision", "exact bpm", "exact key", "structure", "flags")):
        return "mmx_precision"
    if re.search(r"https?://|\bwww\.", lowered) or any(token in lowered for token in ("image", "photo", "picture")):
        # v1.5.0: any URL is a soft signal only. The actual URL refusal
        # happens later in build_result, which inspects source_type and
        # emits a url_not_accepted warning while forcing the route to
        # needs_clarification. Here we only need a sensible request_type
        # for downstream blocker logic.
        return "url_or_image_enrichment"
    if _has_pattern(LYRICS_PROVIDED_PATTERNS, text):
        return "user_lyrics"
    if any(token in lowered for token in ("instrumental", "jingle", "no vocals", "without vocals")):
        return "instrumental"
    if any(token in lowered for token in ("style of", "similar to", "in the style of")) or re.search(
        r"\blike\s+(?!a\b|an\b|the\b|this\b|that\b)", lowered
    ):
        return "text_reference"
    if any(token in lowered for token in ("mini max", "minimax", "mmx")):
        return "minimax_redirect"
    if any(token in lowered for token in ("song", "track", "anthem", "ballad", "write a", "make a", "compose", "create")):
        return "standard_song"
    return "unknown"


def _has_conflicting_cover_style_intent(text: str) -> bool:
    """Return True when the user asks for both cover (melody preservation) and style transfer.

    These two intents are mutually exclusive: a cover preserves the source melody,
    while a style transfer re-produces the source style with a new melody/direction.
    Asking for both means the user has not yet chosen, so the linter must block.
    """
    lowered = text.lower()
    has_cover = any(
        token in lowered
        for token in ("cover", "reinterpret", "reimagine", "keep the melody", "preserve melody")
    )
    has_style_transfer = "style transfer" in lowered
    return has_cover and has_style_transfer


def _route_for(request_type: str, text: str, flags: dict[str, Any]) -> str:
    """Map a request type to a concrete route name.

    Routes:
    - ``base_prompt``: standard generation with no MiniMax-specific feature
    - ``minimax_cover``: melody-preserving cover
    - ``minimax_mashup``: two-song mashup
    - ``minimax_style_transfer``: style-only transfer (no melody preservation)
    - ``minimax_emotion_prompt``: emotion analysis or precision mmx usage
    """
    if request_type == "style_transfer":
        return "minimax_style_transfer"
    if request_type == "cover":
        return "minimax_cover"
    if request_type == "mashup":
        return "minimax_mashup"
    if request_type == "emotion_prompt":
        return "minimax_emotion_prompt"
    if request_type == "mmx_precision":
        return "minimax_emotion_prompt"
    if request_type == "minimax_redirect":
        lowered = text.lower()
        # v1.5.0: only force minimax_cover when the user asked for a cover.
        # A bare URL is not by itself cover intent — it may be a
        # feature-extract, emotion-prompt, or precision-mm redirect that
        # still needs clarification. URLs are now rejected upstream by
        # build_result, so the only way to land here with a URL is from a
        # non-cover intent, which routes to minimax_emotion_prompt.
        if "cover" in lowered:
            return "minimax_cover"
        return "minimax_emotion_prompt"
    if flags and any(key in flags for key in ("bpm", "key", "structure", "avoid", "prompt", "vocals", "instruments", "genre", "mood")):
        return "minimax_emotion_prompt"
    return "base_prompt"


def _instrument_count(text: str) -> int:
    lowered = text.lower()
    return sum(1 for word in INSTRUMENT_WORDS if re.search(rf"\b{re.escape(word)}\b", lowered))


def _canonical_lyrics_tag(tag: str) -> str:
    value = tag.strip()[1:-1].strip().lower()
    value = re.sub(r"[_-]+", " ", value)
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"\s+\d+$", "", value)
    return value


def _lyrics_tag_warnings(lyrics_text: str) -> tuple[list[str], list[str]]:
    if not lyrics_text.strip():
        return [], []
    tags = LYRICS_TAG_RE.findall(lyrics_text)
    invalid = [
        tag
        for tag in tags
        if _canonical_lyrics_tag(tag) not in ALLOWED_LYRICS_TAGS
    ]
    warnings: list[str] = []
    if not tags:
        warnings.append("no lyrics section tags found")
    if invalid:
        warnings.append(
            "invalid lyrics tags: "
            + ", ".join(invalid)
            + "; use only canonical structure tags because bracket text may be sung"
        )
    return warnings, invalid


def _count_lyrics_syllables(lyrics_text: str) -> int:
    total = 0
    plain_text = LYRICS_TAG_RE.sub(" ", lyrics_text)
    for word in WORD_RE.findall(plain_text):
        total += max(1, len(VOWEL_GROUP_RE.findall(word)))
    return total


def _duration_estimate(prompt_text: str, flags: dict[str, Any], lyrics_text: str) -> dict[str, Any] | None:
    if not lyrics_text.strip():
        return None
    prompt_numbers = _prompt_numbers(prompt_text)
    bpm = flags.get("bpm") or prompt_numbers.get("bpm")
    try:
        bpm_value = int(bpm) if bpm is not None else None
    except (TypeError, ValueError):
        bpm_value = None
    target_seconds = None
    if prompt_numbers.get("duration"):
        target_seconds = _parse_duration_to_seconds(str(prompt_numbers["duration"]))
    flag_duration = flags.get("duration") or flags.get("length")
    if target_seconds is None and flag_duration:
        target_seconds = _parse_duration_to_seconds(str(flag_duration))
    syllables = _count_lyrics_syllables(lyrics_text)
    if not bpm_value or bpm_value <= 0:
        return {
            "bpm": bpm_value,
            "syllables": syllables,
            "estimated_lyrics_seconds": None,
            "target_seconds": target_seconds,
            "recommendation": "provide BPM to estimate lyric pacing",
        }
    estimated = int(round((syllables / bpm_value) * 60 * 1.2))
    recommendation = "ok"
    if target_seconds and estimated > target_seconds * 1.15:
        recommendation = "lyrics are dense for the target duration; shorten lyrics or use a longer/exact-duration backend"
    elif target_seconds and target_seconds > 150 and estimated > target_seconds * 0.75:
        recommendation = "long lyric-heavy generation; cloud duration may undershoot, prefer ACE-Step if exact length matters"
    return {
        "bpm": bpm_value,
        "syllables": syllables,
        "estimated_lyrics_seconds": estimated,
        "target_seconds": target_seconds,
        "recommendation": recommendation,
    }


def _prompt_warnings(prompt_text: str) -> list[str]:
    warnings: list[str] = []
    lowered = prompt_text.lower()
    prompt_bytes = len(prompt_text.encode("utf-8"))
    if PROMPT_LENGTH_WARN_BYTES < prompt_bytes <= PROMPT_LENGTH_ERROR_BYTES:
        warnings.append(
            f"prompt length is {prompt_bytes} UTF-8 bytes; MiniMax prompts are safest around 1000-1550 bytes and should stay below {PROMPT_LENGTH_ERROR_BYTES} bytes"
        )
    instrument_count = _instrument_count(prompt_text)
    if instrument_count < 2:
        warnings.append("explicit instruments are missing or too sparse")
    if not any(re.search(pattern, lowered) for pattern in ANTI_SPARSE_PATTERNS):
        warnings.append("anti-sparse guard is missing")
    has_dynamics = any(
        phrase in lowered
        for phrase in ("dynamic", "dynamics", "build", "contrast", "quiet sections", "loud", "soft")
    )
    if any(phrase in lowered for phrase in VAGUE_PHRASES) and (instrument_count < 2 or not has_dynamics):
        warnings.append("vague placeholder language needs concrete instruments or dynamics")
    if has_dynamics:
        pass
    else:
        warnings.append("prompt lacks dynamics guidance")
    # MiniMax lyric-heavy generations commonly come back shorter than requested
    # (often 120-150 seconds for a 180+ second request). Warn when lyrics density
    # and a long target duration are both present.
    lyric_density_tokens = ("[verse]", "[chorus]", "lyrics", "full song", "male lead vocal", "female lead vocal")
    has_lyrics_density = any(token in lowered for token in lyric_density_tokens)
    if has_lyrics_density:
        numbers = _prompt_numbers(prompt_text)
        duration_value = numbers.get("duration")
        if duration_value:
            duration_seconds = _parse_duration_to_seconds(duration_value)
            if duration_seconds is not None and duration_seconds > 150:
                warnings.append(
                    "MiniMax lyric-heavy generations often return shorter output than requested "
                    "(commonly about 120-150 seconds). If exact full length matters, prefer "
                    "music-craft with ACE-Step."
                )
    return warnings


def _prompt_length_blockers(prompt_text: str) -> list[str]:
    prompt_bytes = len(prompt_text.encode("utf-8"))
    if prompt_bytes > PROMPT_LENGTH_ERROR_BYTES:
        return [
            f"prompt length is {prompt_bytes} UTF-8 bytes, above the {PROMPT_LENGTH_ERROR_BYTES}-byte MiniMax safety limit; shorten before generation"
        ]
    return []


def _parse_duration_to_seconds(value: str) -> int | None:
    """Convert a duration string like '30 seconds' or '2 minutes' to seconds."""
    match = re.match(r"^\s*(\d+)\s*(seconds?|secs?|s|minutes?|mins?|m)\s*$", value, flags=re.IGNORECASE)
    if not match:
        return None
    amount = int(match.group(1))
    unit = match.group(2).lower()
    if unit.startswith("m") and not unit.startswith("ms"):
        return amount * 60
    return amount


def _prompt_numbers(prompt_text: str) -> dict[str, Any]:
    bpm_match = re.search(r"\b(\d{2,3}(?:\.\d+)?)\s*bpm\b", prompt_text, flags=re.IGNORECASE)
    key_match = re.search(r"\b([A-G](?:#|b)?\s+(?:major|minor|maj|min))\b", prompt_text, flags=re.IGNORECASE)
    structure_match = re.search(
        r"\b((?:intro|verse|pre[-\s]*chorus|chorus|interlude|bridge|outro|post[-\s]*chorus|transition|break|hook|build[-\s]*up|inst|solo)(?:[-\s]+(?:intro|verse|pre[-\s]*chorus|chorus|interlude|bridge|outro|post[-\s]*chorus|transition|break|hook|build[-\s]*up|inst|solo))+\b)",
        prompt_text,
        flags=re.IGNORECASE,
    )
    avoid_match = re.search(r"\bavoid(?:ing)?\s+([^.;:!?]+)", prompt_text, flags=re.IGNORECASE)
    duration_match = re.search(
        r"\b(\d{1,3})[\s-]*(?:second|seconds|sec|secs|s|minute|minutes|min|mins)\b",
        prompt_text,
        flags=re.IGNORECASE,
    )
    duration_value: str | None = None
    if duration_match:
        amount = duration_match.group(1)
        # Determine unit from the text that follows the digits, inside the match span.
        # Example: "3 minutes" -> match span covers "3 minutes", unit_text = "minutes"
        unit_text = prompt_text[duration_match.start() + len(amount):duration_match.end()].strip().lstrip("- \t")
        if unit_text.lower().startswith("m") and not unit_text.lower().startswith("ms"):
            duration_value = f"{amount} minutes"
        else:
            duration_value = f"{amount} seconds"
    else:
        # Try MM:SS format like "3:00" or "4:30"
        mm_match = re.search(r"\b(\d{1,2}):(\d{2})\b", prompt_text)
        if mm_match:
            minutes = int(mm_match.group(1))
            seconds = int(mm_match.group(2))
            total = minutes * 60 + seconds
            duration_value = f"{total} seconds"
    vocal_mode = "missing"
    lowered = prompt_text.lower()
    if any(token in lowered for token in ("instrumental", "no vocals", "without vocals", "no singing")):
        vocal_mode = "instrumental"
    elif any(token in lowered for token in ("vocal", "voice", "singing", "singer")):
        vocal_mode = "vocal"
    language_value = "missing"
    for language, patterns in LANGUAGE_PATTERNS:
        for pattern in patterns:
            if re.search(pattern, prompt_text, flags=re.IGNORECASE):
                language_value = language
                break
        if language_value != "missing":
            break
    return {
        "bpm": int(float(bpm_match.group(1))) if bpm_match else None,
        "key": (
            re.sub(r"\bmin\b", "minor", re.sub(r"\bmaj\b", "major", key_match.group(1), flags=re.IGNORECASE), flags=re.IGNORECASE)
            if key_match
            else None
        ),
        "structure": re.sub(r"\s+", "-", structure_match.group(1).lower()) if structure_match else None,
        "avoid": _normalize_space(avoid_match.group(1)) if avoid_match else None,
        "duration": duration_value,
        "vocal_mode": vocal_mode,
        "language": language_value,
    }


def _flag_conflicts(prompt_text: str, flags: dict[str, Any]) -> list[str]:
    """Return a list of human-readable conflict strings between prompt and flags.

    Conflicts covered: BPM, key, structure, duration, vocal mode, language, avoid list.
    """
    conflicts: list[str] = []
    if not prompt_text or not flags:
        return conflicts
    prompt_numbers = _prompt_numbers(prompt_text)
    prompt_bpm = prompt_numbers["bpm"]
    flag_bpm = flags.get("bpm")
    if prompt_bpm is not None and flag_bpm is not None and int(flag_bpm) != int(prompt_bpm):
        conflicts.append(f"bpm conflict: prompt says {prompt_bpm} BPM but flags.json says {flag_bpm}")

    prompt_key = prompt_numbers["key"]
    flag_key = flags.get("key")
    if prompt_key and flag_key and str(prompt_key).lower() != str(flag_key).lower():
        conflicts.append(f"key conflict: prompt says {prompt_key} but flags.json says {flag_key}")

    prompt_structure = prompt_numbers["structure"]
    flag_structure = flags.get("structure")
    if prompt_structure and flag_structure and str(prompt_structure).lower() != str(flag_structure).lower():
        conflicts.append(f"structure conflict: prompt says {prompt_structure} but flags.json says {flag_structure}")

    prompt_avoid = prompt_numbers["avoid"]
    flag_avoid = flags.get("avoid")
    if prompt_avoid and flag_avoid and _normalize_space(str(prompt_avoid)).lower() != _normalize_space(str(flag_avoid)).lower():
        conflicts.append(f"avoid conflict: prompt says {prompt_avoid} but flags.json says {flag_avoid}")

    prompt_duration = prompt_numbers["duration"]
    flag_duration = flags.get("duration") or flags.get("length")
    if prompt_duration and flag_duration:
        prompt_seconds = _parse_duration_to_seconds(prompt_duration)
        flag_seconds = _parse_duration_to_seconds(str(flag_duration))
        if prompt_seconds is not None and flag_seconds is not None and abs(prompt_seconds - flag_seconds) > 1:
            conflicts.append(
                f"duration conflict: prompt says {prompt_duration} but flags.json says {flag_duration}"
            )

    prompt_vocal = prompt_numbers["vocal_mode"]
    flag_vocal = flags.get("vocals")
    if prompt_vocal != "missing" and flag_vocal:
        flag_vocal_lower = str(flag_vocal).lower()
        if prompt_vocal == "instrumental" and not any(
            token in flag_vocal_lower for token in ("instrumental", "no vocal", "no vocals")
        ):
            conflicts.append(
                f"vocal mode conflict: prompt says instrumental but flags.json says {flag_vocal}"
            )
        if prompt_vocal == "vocal" and any(
            token in flag_vocal_lower for token in ("instrumental", "no vocal", "no vocals")
        ):
            conflicts.append(
                f"vocal mode conflict: prompt says vocals but flags.json says {flag_vocal}"
            )

    prompt_language = prompt_numbers["language"]
    flag_language = flags.get("language")
    if prompt_language != "missing" and flag_language and str(prompt_language).lower() != str(flag_language).lower():
        conflicts.append(
            f"language conflict: prompt says {prompt_language} but flags.json says {flag_language}"
        )

    return conflicts


def _retry_guidance(conflicts: list[str]) -> list[str]:
    """Produce retry guidance messages corresponding to each conflict.

    When prompt and flags disagree, the operator must choose which one is
    authoritative. The guidance below tells the operator the safest default
    (flags win for numeric facts, prompt wins for descriptive content) and how
    to re-align both.
    """
    guidance: list[str] = []
    for conflict in conflicts:
        lowered = conflict.lower()
        if "bpm" in lowered:
            guidance.append(
                "bpm: flags are usually the authoritative numeric value. Re-run with the same --bpm and remove the BPM from the prompt text, or update the flag to match the prompt."
            )
        elif "key" in lowered:
            guidance.append(
                "key: re-align the prompt key with --key, or update --key to match the prompt. Music theory facts must agree."
            )
        elif "structure" in lowered:
            guidance.append(
                "structure: keep the structure line in lockstep with --structure. Drop one of them or rewrite so they describe the same sections in the same order."
            )
        elif "duration" in lowered:
            guidance.append(
                "duration: mmx does not have a single duration flag; remove the duration from the prompt or set --lyrics-optimizer with an explicit length expectation. Keep one source of truth."
            )
        elif "vocal" in lowered:
            guidance.append(
                "vocal mode: decide between instrumental and vocal before retry. Update --vocals or remove the conflicting word from the prompt."
            )
        elif "language" in lowered:
            guidance.append(
                "language: ensure the prompt language and --language flag agree. Lyrics language drives generation regardless of the prompt text."
            )
        elif "avoid" in lowered:
            guidance.append(
                "avoid list: the prompt and --avoid must be the same comma-separated set. Use one source of truth to avoid the prompt and the flag fighting each other."
            )
    return guidance


def _blockers(request_type: str, fields: dict[str, dict[str, Any]], text: str) -> list[str]:
    """Return a list of blocker strings describing what is missing for the request."""
    blockers: list[str] = []

    # v1.5.0: only local audio files are usable sources. URLs are
    # explicitly rejected by build_result (see the url_not_accepted
    # warning) and must not bypass the "missing source file" blocker —
    # the agent should ask the user for a local file path.
    source_type_value = fields.get("source_type", {}).get("value", "unknown")
    has_usable_source = source_type_value == "local"
    references_missing = fields["references"]["confidence"] == "missing" and not has_usable_source
    references_value = fields["references"]["value"]
    lyrics_missing = fields["lyrics_source"]["confidence"] == "missing"
    style_missing = fields["genre"]["confidence"] == "missing" and fields["mood"]["confidence"] == "missing"
    lowered = text.lower()

    if request_type == "mashup":
        if not _has_song_a_b(text):
            blockers.append("unclear Song A vs Song B assignment")
        if references_missing:
            blockers.append("missing source file or usable URL")
        if style_missing:
            blockers.append("missing target style")
        if lyrics_missing:
            blockers.append("missing lyrics decision")
        return blockers

    if request_type in {"cover", "style_transfer", "minimax_redirect"}:
        if references_missing:
            blockers.append("missing source file or usable URL")
        if style_missing:
            blockers.append("missing target style")
        if lyrics_missing:
            blockers.append("missing lyrics decision")
        if _has_conflicting_cover_style_intent(text):
            blockers.append(
                "conflicting cover/style-transfer intent: pick either 'cover' (preserves melody) or 'style transfer' (reproduces the style), not both"
            )
        return blockers

    if request_type == "emotion_prompt":
        if references_missing:
            blockers.append("missing source file or usable URL")
        if style_missing:
            blockers.append("missing target style")
        return blockers

    if request_type == "mmx_precision":
        if not any(token in lowered for token in ("bpm", "key", "structure", "avoid", "vocals", "instruments", "genre", "mood")):
            blockers.append("mmx precision requested but no specific mmx flag value is present")
        return blockers

    if request_type == "user_lyrics":
        if references_value == "missing":
            blockers.append("missing lyrics source (text, file, or URL)")
        return blockers

    if request_type in {"text_reference", "url_or_image_enrichment"}:
        if style_missing:
            blockers.append("missing target style or mood for the new song")
        return blockers

    return blockers


def _has_song_a_b(text: str) -> bool:
    """Return True when the user has named or supplied both Song A and Song B.

    Detects: explicit "Song A"/"Song B", "first/second song", "one song and another",
    "song X and song Y", and conjunction-based references between two song names.

    A simple "song and song" without labels is NOT enough — the user must show
    intent that one is A and the other is B.
    """
    lowered = text.lower()
    a_patterns = [
        r"\bsong\s*a\b",
        r"\btrack\s*a\b",
        r"\bpart\s*a\b",
        r"\bverse\s*a\b",
        r"\bchorus\s*a\b",
        r"\boriginal\s*a\b",
        r"\bfirst\s+(?:song|track)\b",
        r"\bone\s+(?:song|track)\b",
    ]
    b_patterns = [
        r"\bsong\s*b\b",
        r"\btrack\s*b\b",
        r"\bpart\s*b\b",
        r"\bverse\s*b\b",
        r"\bchorus\s*b\b",
        r"\bsecond\s+(?:song|track)\b",
        r"\bother\s+(?:song|track)\b",
        r"\banother\s+(?:\w+\s+)?(?:song|track)\b",
    ]
    has_a = any(re.search(pattern, lowered) for pattern in a_patterns)
    has_b = any(re.search(pattern, lowered) for pattern in b_patterns)
    if has_a and has_b:
        return True
    if re.search(r"\b(?:and|&|\+)\b", lowered) and re.search(
        r"\b(?:two|2|3|three|several)\s+(?:songs|tracks)\b", lowered
    ):
        return True
    return False


def build_result(text: str, prompt_text: str, flags: dict[str, Any], lyrics_text: str = "") -> dict[str, Any]:
    combined_text = "\n".join(part for part in (text, prompt_text) if part)
    request_type = _request_type(combined_text)
    route = _route_for(request_type, combined_text, flags)

    language_value, language_confidence = _detect_language(combined_text)
    theme_value = _extract_theme(combined_text)
    genre_value, genre_confidence = _detect_genre(combined_text)
    mood_value, mood_confidence = _detect_mood(combined_text)
    duration_value, duration_confidence = _detect_duration(combined_text)
    lyrics_source_value, lyrics_source_confidence = _detect_lyrics_source(combined_text, lyrics_text)
    vocal_mode_value, vocal_mode_confidence = _detect_vocal_mode(combined_text)
    references_value, references_confidence = _detect_references(combined_text)
    source_type_value, source_type_confidence = _detect_source_type(combined_text)

    if request_type == "instrumental":
        vocal_mode_value = "instrumental"
        vocal_mode_confidence = "clear"

    if request_type == "standard_song" and language_value == "Spanish" and theme_value is None:
        theme_value = "missing"

    fields = {
        "language": _field(language_value, language_confidence),
        "genre": _field(genre_value, genre_confidence),
        "mood": _field(mood_value, mood_confidence),
        "theme": _field(theme_value if theme_value is not None else "missing", "inferred" if theme_value else "missing"),
        "duration": _field(duration_value, duration_confidence),
        "lyrics_source": _field(lyrics_source_value, lyrics_source_confidence),
        "vocal_mode": _field(vocal_mode_value, vocal_mode_confidence),
        "references": _field(references_value, references_confidence),
        "source_type": _field(source_type_value, source_type_confidence),
    }

    missing_fields = [name for name, data in fields.items() if data["confidence"] == "missing"]
    if request_type == "standard_song" and "lyrics_source" not in missing_fields and lyrics_source_value == "missing":
        missing_fields.append("lyrics_source")

    prompt_warnings = _prompt_warnings(prompt_text) if prompt_text else []
    lyrics_warnings, invalid_lyrics_tags = _lyrics_tag_warnings(lyrics_text)
    duration_estimate = _duration_estimate(prompt_text, flags, lyrics_text)
    if duration_estimate and duration_estimate["recommendation"] != "ok":
        lyrics_warnings.append(duration_estimate["recommendation"])
    flag_conflicts = _flag_conflicts(prompt_text, flags)
    blockers = _blockers(request_type, fields, combined_text)
    blockers.extend(_prompt_length_blockers(prompt_text) if prompt_text else [])
    if invalid_lyrics_tags:
        blockers.append("invalid lyrics tags: " + ", ".join(invalid_lyrics_tags))

    # v1.5.0: URLs are not accepted. Emit a soft warning and force the route
    # to needs_clarification so the agent asks the user for a local file
    # path. This applies to cover, mashup, and style_transfer requests where
    # the user is clearly trying to do something with a source audio file.
    soft_warnings: list[dict[str, str]] = []
    if request_type in {"cover", "mashup", "style_transfer"} and source_type_value == "url":
        soft_warnings.append({
            "code": "url_not_accepted",
            "message": (
                "URLs are not accepted by this skill. Please provide a local "
                "audio file path. If you want auto-download from YouTube or "
                "JioSaavn, use the private music-source-fetch skill first, "
                "then pass the resulting local file path here."
            ),
        })
        route = "needs_clarification"

    if flags and request_type == "unknown":
        request_type = "mmx_precision"
        route = _route_for(request_type, combined_text, flags)
        blockers = _blockers(request_type, fields, combined_text)
        blockers.extend(_prompt_length_blockers(prompt_text) if prompt_text else [])
        if invalid_lyrics_tags:
            blockers.append("invalid lyrics tags: " + ", ".join(invalid_lyrics_tags))

    if blockers:
        route = "needs_clarification"

    retry_guidance = _retry_guidance(flag_conflicts)

    return {
        "route": route,
        "request_type": request_type,
        "fields": fields,
        "missing_fields": missing_fields,
        "warnings": soft_warnings,
        "blockers": blockers,
        "prompt_warnings": prompt_warnings,
        "lyrics_warnings": lyrics_warnings,
        "duration_estimate": duration_estimate,
        "flag_conflicts": flag_conflicts,
        "retry_guidance": retry_guidance,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint a music request for routing and prompt quality.")
    parser.add_argument("--text", help="Quick routing / missing-field detection text.")
    parser.add_argument("--prompt-file", help="Path to a prompt text file.")
    parser.add_argument("--lyrics-file", help="Path to a lyrics text file for tag lint and duration estimate.")
    parser.add_argument("--mmx-flags", help="Path to mmx flags JSON.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    prompt_text = _read_text_file(args.prompt_file)
    lyrics_text = _read_text_file(args.lyrics_file)
    flags = _load_flags(args.mmx_flags)
    text = args.text or ""

    result = build_result(text=text, prompt_text=prompt_text, flags=flags, lyrics_text=lyrics_text)
    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
