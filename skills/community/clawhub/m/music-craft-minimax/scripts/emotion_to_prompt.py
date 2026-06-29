#!/usr/bin/env python3
"""emotion_to_prompt.py — Convert emotion analysis + style analysis into music generation prompts.

Takes the JSON outputs from:
  - analyze_vocal_emotion.py  (emotion dynamics from Song A)
  - analyze_audio.py or analyze_two_songs.py  (style features from Song B)
  - analysis_orchestrator.py  (full unified output; enables image/video/mashup consumption)

And produces a structured music generation prompt suitable for Suno, Udio,
MiniMax, or other music generation tools.

# DISCARDED (intentionally not consumed) — v0.1.1
# ---------------------------------------------
# analyze_vocal_emotion.py:
#   - emotion_sections[].avg_pitch_hz, pitch_std_hz, pitch_trend_val, max_intensity,
#     intensity_range, voiced_ratio, spectral_contrast (raw numeric per-section values)
#     Reason: only the categorical/classifier outputs are stable; raw values vary too
#     much between recordings to be useful as prompt text.
#   - formant_tracks_available (boolean flag, never used)
#   - per-section jitter_pct, shimmer_pct, hnr_db raw values (global aggregate used
#     instead; per-section "breathier in verse" style aggregation added in v0.1.1)
# analyze_audio.py / analyze_two_songs.py:
#   - beat_count, duration_formatted, approx_beat_count
#     Reason: redundant with BPM and duration_seconds which are already in the prompt.
#   - tempo_feel, key_confidence (text/values, not stable enough to inject)
# analyze_two_songs.py:
#   - song_b_reference.source_file (only used to compute has_song_b_audio; not in prompt)
# emotion_to_prompt.py internal:
#   - style_template_used, emotion_hints_used (dead output fields; removed in v0.1.1)

Usage:
    python3 emotion_to_prompt.py \
        --emotion /tmp/song_a_emotion.json \
        --style /tmp/song_b_style.json \
        [--target-duration 180] \
        [--language english] \
        [--output /tmp/prompt.json]

Output: JSON with:
  - final_prompt: ready-to-use music generation prompt
  - prompt_sections: per-section instructions
  - arrangement_plan: instrument layering guide
"""
import sys
import os
import json
import argparse


# ─── Style-to-prompt templates ──────────────────────────────────

# ─── Style-to-prompt templates ──────────────────────────────────

# MiniMax Music 2.6 “Production Sheet” formula:
#   [Genre/subgenre], [mood], [voice type], [instruments — name ALL],
#   [BPM] BPM in [key], [structure], [production/mix], [things to avoid]
#
# Critical: ALWAYS name all instruments, ALWAYS add “never drop to a cappella”,
# ALWAYS add “avoid sparse minimal arrangements”

STYLE_TEMPLATES = {
    # category: (instruments, mood, vocal_style, era, typical_bpm, key, avoid)
    "french_chanson": {
        "instruments": "accordion, upright bass, orchestral strings, piano",
        "mood": "melancholic romantic, dramatic, theatrical",
        "vocal": "passionate theatrical French vocalist, Edith Piaf style delivery",
        "era": "1960s Paris café",
        "bpm_range": (70, 90),
        "key": "E minor",
        "avoid": "avoid sparse minimal arrangements, avoid a cappella sections, avoid electronic sounds",
    },
    "rock": {
        "instruments": "electric guitars, bass, drums, rhythm guitar",
        "mood": "energetic, powerful, driving",
        "vocal": "powerful rock vocalist, belting",
        "era": "classic rock",
        "bpm_range": (120, 150),
        "key": "A major",
        "avoid": "avoid sparse minimal arrangements, avoid a cappella sections",
    },
    "acoustic": {
        "instruments": "acoustic guitar, light percussion, upright bass",
        "mood": "intimate, warm, organic",
        "vocal": "soft gentle vocals, close-mic",
        "era": "modern folk",
        "bpm_range": (80, 110),
        "key": "G major",
        "avoid": "avoid sparse minimal arrangements, avoid a cappella sections",
    },
    "epic_orchestral": {
        "instruments": "full symphony strings, brass, timpani, choir",
        "mood": "cinematic, grand, sweeping",
        "vocal": "operatic or cinematic vocals",
        "era": "modern cinematic",
        "bpm_range": (60, 85),
        "key": "D minor",
        "avoid": "avoid sparse minimal arrangements, avoid a cappella sections",
    },
    "jazz": {
        "instruments": "piano, double bass, brushed drums, brass section",
        "mood": "smooth, sophisticated, swing",
        "vocal": "jazz vocalist, scat capable",
        "era": "1940s-1950s jazz club",
        "bpm_range": (140, 180),
        "key": "Bb major",
        "avoid": "avoid sparse minimal arrangements, avoid a cappella sections",
    },
    "latin": {
        "instruments": "acoustic guitar, percussion, brass, bass",
        "mood": "warm, passionate, rhythmic",
        "vocal": "Latin vocalist, emotional delivery",
        "era": "timeless Latin",
        "bpm_range": (90, 130),
        "key": "A minor",
        "avoid": "avoid sparse minimal arrangements, avoid a cappella sections",
    },
    "pop": {
        "instruments": "synths, drums, bass, polished production",
        "mood": "catchy, upbeat, modern",
        "vocal": "clear pop vocals, polished",
        "era": "modern pop",
        "bpm_range": (100, 130),
        "key": "C major",
        "avoid": "avoid sparse minimal arrangements, avoid a cappella sections",
    },
    "blues": {
        "instruments": "electric guitar, harmonica, bass, drums",
        "mood": "soulful, gritty, emotional",
        "vocal": "gritty blues vocals, expressive",
        "era": "classic blues",
        "bpm_range": (70, 100),
        "key": "E major",
        "avoid": "avoid sparse minimal arrangements, avoid a cappella sections",
    },
    "electronic": {
        "instruments": "synthesizers, drum machines, pads, arpeggiators",
        "mood": "atmospheric, pulsing, immersive",
        "vocal": "processed vocals, ethereal or robotic",
        "era": "modern electronic",
        "bpm_range": (110, 140),
        "key": "A minor",
        "avoid": "avoid sparse minimal arrangements, avoid a cappella sections",
    },
    "ballad": {
        "instruments": "piano, strings, gentle percussion, bass",
        "mood": "tender, emotional, intimate",
        "vocal": "soft emotive vocals, gradual build",
        "era": "timeless ballad",
        "bpm_range": (60, 90),
        "key": "C minor",
        "avoid": "avoid sparse minimal arrangements, avoid a cappella sections",
    },
}


def infer_style_category(style_data):
    """Infer the style category from audio analysis features.

    Priority: CLAP zero-shot classification > heuristic BPM/energy mapping.
    """
    # Priority 1: CLAP zero-shot classification (most reliable when present)
    clap = style_data.get('clap_classification', {})
    if clap.get('detected'):
        genres = clap.get('top_genres', [])
        if genres:
            top_genre = genres[0][0].lower()  # (label, score) tuple
            genre_to_category = {
                'rock': 'rock', 'pop': 'pop', 'jazz': 'jazz', 'blues': 'blues',
                'electronic': 'electronic', 'hip hop': 'pop', 'rnb': 'pop', 'country': 'acoustic',
                'folk': 'acoustic', 'classical': 'epic_orchestral', 'metal': 'rock', 'punk': 'rock',
                'reggae': 'latin', 'latin': 'latin', 'soul': 'blues', 'funk': 'pop', 'disco': 'pop',
                'house': 'electronic', 'techno': 'electronic', 'synthwave': 'electronic',
                'ambient': 'ballad', 'indie': 'acoustic', 'alternative': 'rock', 'dream pop': 'pop',
                'post-rock': 'epic_orchestral', 'shoegaze': 'rock', 'lo-fi': 'acoustic',
            }
            category = genre_to_category.get(top_genre)
            if category:
                return category

    # Priority 2: Heuristic fallback (BPM + energy + instrument hints)
    bpm = style_data.get('bpm', 100)
    brightness = style_data.get('brightness', 'balanced')
    energy = style_data.get('energy_description', 'moderate')
    hints = style_data.get('instrument_hints', {})

    # Heuristic mapping
    if hints.get('likely_electronic'):
        return "electronic"
    if hints.get('likely_orchestral'):
        return "epic_orchestral"
    if hints.get('likely_acoustic'):
        if bpm < 95:
            return "ballad"
        return "acoustic"

    bpm_str = str(brightness).lower()
    energy_str = str(energy).lower()

    if bpm > 150:
        return "jazz" if 'warm' in bpm_str else "rock"
    if bpm > 120:
        if 'energetic' in energy_str or 'high' in energy_str:
            return "rock"
        return "pop"
    if bpm > 100:
        return "latin"
    if bpm > 85:
        return "pop"
    if bpm > 70:
        return "ballad"
    return "ballad"


def resolve_target_bpm(song_a_bpm, song_b_bpm, style_category):
    """Determine target BPM for the mashup."""
    template = STYLE_TEMPLATES.get(style_category, {})
    bpm_range = template.get('bpm_range', (80, 120))

    # Prefer the style's natural BPM range
    # But if Song A's BPM is close, keep it closer for recognition
    low, high = bpm_range

    if low <= song_a_bpm <= high:
        # Song A already fits style's range
        return song_a_bpm

    # Clamp Song B's BPM to the style range
    target = max(low, min(high, song_b_bpm))

    # If BPM change is extreme (>40%), note it
    return round(target, 1)


# ─── Section-by-section prompt building ─────────────────────────

def build_section_prompts(emotion_sections, style_template, style_category=None):
    """Build per-section arrangement instructions.

    IMPORTANT: 'sparse' means FEWER instruments, not NO instruments.
    Every section must have at least the minimum instrumentation for the style.
    """
    sections = []
    prev_label = None
    for sec in emotion_sections:
        label = sec.get('structural_label', 'section')
        effort = sec.get('vocal_effort', 'low')
        intensity = sec.get('avg_intensity', 0)
        emotions = sec.get('emotion_classification', [])
        trend = sec.get('pitch_trend', 'steady')

        # Determine arrangement density for this section
        if effort == 'high' or intensity > 0.1:
            density = "full"
            dynamics = "loud, powerful"
        elif effort == 'medium' or intensity > 0.04:
            density = "building" if trend == 'rising' else "moderate"
            dynamics = "medium intensity"
        else:
            density = "sparse"
            dynamics = "quiet, intimate"

        # Build the instruction — ALWAYS include instrumentation
        instruments = style_template.get('instruments', 'balanced arrangement')
        inst_list = [i.strip() for i in instruments.split(',')]
        # Minimum instrumentation: at least 2 core instruments always present
        min_instruments = ', '.join(inst_list[:2]) if len(inst_list) >= 2 else instruments
        full_instruments = instruments

        if density == "full":
            arrangement_desc = f"full arrangement with {full_instruments}"
        elif density == "moderate" or density == "building":
            arrangement_desc = f"moderate arrangement — {', '.join(inst_list[:3])} active"
        else:
            # CRITICAL: sparse still means instruments are playing,
            # just fewer of them — NOT silence or a cappella
            arrangement_desc = f"reduced arrangement — {min_instruments} only, still fully played"

        instruction = f"{label.upper()}: {dynamics} — {arrangement_desc}"

        # Add trend-specific note
        if trend == 'rising':
            instruction += ", building tension"
        elif trend == 'falling':
            instruction += ", releasing tension"

        # Add emotion-specific color
        if 'desperate' in emotions:
            instruction += ", raw emotional delivery"
        elif 'passionate' in emotions:
            instruction += ", heartfelt passionate vocals"
        elif 'calm' in emotions:
            instruction += ", gentle and restrained"

        # Add rhythm feel from tempogram analysis
        rhythm_feel = sec.get('rhythm_feel', '')
        if rhythm_feel == 'swing':
            instruction += ", swing feel"
        elif rhythm_feel == 'straight':
            instruction += ", straight rhythm"

        # Add vocal register if detected
        vocal_register = sec.get('vocal_register', '')
        if vocal_register and vocal_register not in ('unknown', 'mixed'):
            if vocal_register == 'falsetto':
                instruction += ", airy falsetto delivery"
            elif vocal_register == 'head_voice':
                instruction += ", light head voice"
            elif vocal_register == 'chest':
                instruction += ", full chest voice power"

        # Detect and add pause instruction at section transitions
        # Use [Break] and [Build Up] structure tags in MiniMax for better results
        if prev_label and prev_label != label:
            prev_sec = sections[-1] if sections else None
            if prev_sec:
                prev_density = prev_sec.get('arrangement_density', 'moderate')
                if prev_density in ('full', 'building') and density == 'sparse':
                    instruction += ", insert [Break] tag here for dramatic 1-2 second pause with reverb tail"
                elif density == 'full' and prev_density in ('sparse', 'moderate'):
                    instruction += ", preceded by [Build Up] tag for anticipation"

        sections.append({
            "section_label": label,
            "start_seconds": sec.get('start_seconds', 0),
            "end_seconds": sec.get('end_seconds', 0),
            "arrangement_density": density,
            "dynamics": dynamics,
            "instruction": instruction,
            "minimum_instruments": min_instruments,
        })

        prev_label = label

    return sections


def build_arrangement_plan(emotion_data, style_category):
    """Build a layering plan: which instruments enter when."""
    profile = emotion_data.get('emotion_profile', {})
    sections = emotion_data.get('emotion_sections', [])
    curve = profile.get('intensity_curve', {}).get('pattern', 'unknown')
    template = STYLE_TEMPLATES.get(style_category, {})

    instruments = template.get('instruments', 'balanced arrangement')
    inst_list = [i.strip() for i in instruments.split(',')]

    plan = {
        "intro": f"reduced: {inst_list[0] if inst_list else 'piano'} + {inst_list[1] if len(inst_list) > 1 else 'light bass'} only — instruments are present but minimal, NOT silent",
        "verse_1": f"add: {inst_list[2] if len(inst_list) > 2 else 'light percussion'} alongside the intro instruments",
        "pre_chorus": f"add: {inst_list[3] if len(inst_list) > 3 else 'strings'} — building toward full sound, insert [Build Up] tag",
        "chorus": f"FULL arrangement: all instruments active — {instruments}",
        "verse_2": "pull back slightly from chorus density, but keep at least 3 instruments active",
        "bridge": f"contrast: reduce to {inst_list[0] if inst_list else 'piano'} and bass — but still played, not silent. Insert [Break] tag before bridge.",
        "final_chorus": "maximum intensity: all instruments + backing harmonies + doubled parts",
        "outro": "gradual fade with instruments still playing, or dramatic final chord sustained",
        "_note": "CRITICAL: 'sparse' or 'reduced' means FEWER instruments playing, NOT silence or a cappella. Every section has at least 2 instruments active. Use [Break] tags for dramatic pauses, [Build Up] before choruses.",
    }

    # Adjust based on curve
    if curve == 'crescendo':
        plan['intro'] = f"very reduced: single {inst_list[0] if inst_list else 'instrument'} + subtle {inst_list[1] if len(inst_list) > 1 else 'bass'} — quiet but instruments ARE playing"
        plan['outro'] = "powerful sustained ending at peak intensity — all instruments at full volume"
    elif curve == 'decrescendo':
        plan['intro'] = f"full arrangement from the start — all instruments active"
        plan['outro'] = f"fade to {inst_list[0] if inst_list else 'single instrument'} — gentle ending, instruments still audible"

    return plan


# ─── Final prompt builder ───────────────────────────────────────

def build_vocal_speed_prompts(vocal_speed, pitch_bends):
    """Convert vocal speed patterns into specific music generation instructions.

    MiniMax doesn't have a direct 'vocal speed' parameter, but elongation can be
    achieved through:
    1. Fewer syllables per line in lyrics (gives model space to stretch)
    2. Repeated vowels in lyrics text ("yoooou", "I caaan't")
    3. Prompt cues: "restrained", "raw and emotional", "rubato"
    4. Section tags with parenthetical vocal cues: [Chorus] (slow, stretching words)
    5. Energy cue 'intimate' or 'restrained' slows delivery
    """
    if not vocal_speed or not vocal_speed.get('detected', True):
        return {
            "detected": False,
            "prompt_additions": [],
            "lyrics_modifications": [],
            "section_cues": [],
        }

    pattern = vocal_speed.get('pattern', 'steady')
    sections = vocal_speed.get('sections', [])
    avg_sps = vocal_speed.get('average_syllables_per_second', 4.0)

    prompt_additions = []
    lyrics_modifications = []
    section_cues = []

    # Pattern-specific prompt additions
    if pattern == 'decelerating':
        prompt_additions.append(
            "vocal delivery progressively slows with emotional elongation, "
            "final sections sung with stretched syllables and rubato timing"
        )
    elif pattern == 'late_elongation':
        prompt_additions.append(
            "final chorus features emotionally stretched syllables, "
            "vocalist holds and bends notes at phrase endings"
        )
    elif pattern == 'gradual_slowing':
        prompt_additions.append(
            "gradual rubato throughout, vocalist increasingly stretches phrases"
        )
    elif pattern == 'accelerating':
        prompt_additions.append(
            "urgent driving vocal delivery, words come faster as emotion builds"
        )

    # Per-section cues based on speed classification
    for sec in sections:
        label = sec.get('structural_label', 'section')
        speed_class = sec.get('speed_classification', 'normal')
        sps = sec.get('syllables_per_second', avg_sps)
        syllables = sec.get('estimated_syllables', 0)
        duration = sec.get('duration_seconds', 0)
        deviation = sec.get('tempo_deviation', 0)

        if speed_class == 'slowed':
            cue = {
                "section": label,
                "lyrics_instruction": (
                    f"Use fewer syllables per line ({max(4, int(sps * 2))} syllables for "
                    f"~{duration:.0f}s), allowing space for word stretching"
                ),
                "prompt_cue": f"{label}: slow, emotionally stretched delivery, hold last syllable",
                "lyrics_tip": (
                    "Repeat key vowels: 'yoooou', 'mooooore', 'I caaaan't' — "
                    "MiniMax responds to repeated characters by elongating"
                ),
            }
            section_cues.append(cue)

            # Suggest specific lyrics modifications
            lyrics_modifications.append({
                "section": label,
                "instruction": (
                    f"Reduce to ~{max(4, int(sps * 2))} syllables per line, "
                    f"use repeated vowels for elongation effect"
                ),
                "example": "I caaan't goooo on with yoooou",
            })

        elif speed_class == 'accelerated':
            section_cues.append({
                "section": label,
                "prompt_cue": f"{label}: urgent, driving delivery, rapid-fire words",
            })

    # Pitch bend analysis → additional cues
    significant_bends = [b for b in pitch_bends if b.get('pitch_range_hz', 0) > 40]
    if significant_bends:
        prompt_additions.append(
            f"{len(significant_bends)} phrase-ending pitch bends detected — "
            "include vocal slides and melismas at phrase endings"
        )

    return {
        "detected": pattern != 'steady',
        "pattern": pattern,
        "prompt_additions": prompt_additions,
        "lyrics_modifications": lyrics_modifications,
        "section_cues": section_cues,
        "significant_pitch_bends": len(significant_bends),
    }


# ─── Structured lyrics template generator ───────────────────────

def generate_structured_lyrics_template(emotion_sections, vocal_speed_patterns,
                                         silence_gaps, arrangement_plan,
                                         style_category, language="english"):
    """Generate a lyrics skeleton with MiniMax structure tags and vocal delivery hints.

    Produces a template with:
    - [Verse], [Chorus], [Bridge], etc. at section boundaries
    - [Break] tags where natural silence gaps exist in the original
    - [Build Up] tags before chorus/crescendo sections
    - Vocal delivery hints per section (from emotion analysis)
    - Elongation markers for slowed sections
    - Placeholders {like_this} for LLM to fill with actual lyrics

    The output is designed to be filled by the LLM or parody_writer,
    then used directly as the `lyrics` parameter for MiniMax music_generation.
    """
    if not emotion_sections:
        return {
            "template": "[Intro]\n(Instrumental)\n\n[Verse]\n{verse_lines}\n\n[Chorus]\n{chorus_lines}",
            "note": "No emotion sections detected — using generic template",
        }

    template_lines = []
    prev_label = None
    seen_labels = set()
    label_counts = {}

    # Count label occurrences for numbering
    for sec in emotion_sections:
        label = sec.get('structural_label', 'section')
        label_counts[label] = label_counts.get(label, 0) + 1

    for i, sec in enumerate(emotion_sections):
        label = sec.get('structural_label', 'section')
        effort = sec.get('vocal_effort', 'low')
        trend = sec.get('pitch_trend', 'steady')
        start = sec.get('start_seconds', 0)
        end = sec.get('end_seconds', 0)

        # Map structural_label to MiniMax structure tag
        tag_map = {
            'intro': '[Intro]',
            'verse': '[Verse]',
            'pre-chorus': '[Pre Chorus]',
            'pre_chorus': '[Pre Chorus]',
            'chorus': '[Chorus]',
            'bridge': '[Bridge]',
            'outro': '[Outro]',
            'interlude': '[Interlude]',
            'post-chorus': '[Post Chorus]',
            'post_chorus': '[Post Chorus]',
            'solo': '[Solo]',
            'section': '[Verse]' if i > 0 else '[Intro]',
        }
        tag = tag_map.get(label, '[Verse]')

        # Check if a silence gap aligns with this section boundary
        has_silence_before = False
        if silence_gaps and prev_label is not None:
            for gap in silence_gaps:
                gap_start = gap.get('start_seconds', 0)
                gap_dur = gap.get('duration_seconds', 0)
                # If a silence gap starts within 2s of this section start
                if abs(gap_start - start) < 2.0 and gap_dur >= 0.8:
                    has_silence_before = True
                    break

        # Insert [Break] tag before section if natural pause exists
        if has_silence_before and prev_label is not None:
            template_lines.append('')
            template_lines.append('[Break]')
            template_lines.append('(1-2 second dramatic pause — reverb tail, not dead silence)')
            template_lines.append('')

        # Insert [Build Up] before chorus sections
        if tag == '[Chorus]' and prev_label is not None:
            template_lines.append('')
            template_lines.append('[Build Up]')
            template_lines.append('(Tension building)')
            template_lines.append('')

        # Add section tag
        template_lines.append('')
        template_lines.append(tag)

        # Add vocal delivery hint as comment
        delivery_hints = []
        if effort == 'high':
            delivery_hints.append('powerful, passionate delivery')
        elif effort == 'medium':
            delivery_hints.append('moderate intensity, building')
        else:
            delivery_hints.append('gentle, intimate delivery')

        if trend == 'rising':
            delivery_hints.append('vocals rising in pitch')
        elif trend == 'falling':
            delivery_hints.append('vocals releasing, settling')

        # Check vocal speed for this section
        vocal_sections = vocal_speed_patterns.get('sections', []) if vocal_speed_patterns else []
        for vs in vocal_sections:
            vs_label = vs.get('structural_label', '')
            vs_start = vs.get('start_seconds', 0)
            if vs_label == label or abs(vs_start - start) < 3.0:
                speed_class = vs.get('speed_classification', 'normal')
                if speed_class == 'slowed':
                    delivery_hints.append('SLOW — stretch syllables, hold last word: "yoooou", "mooooore"')
                elif speed_class == 'accelerated':
                    delivery_hints.append('urgent, rapid-fire delivery')
                break

        if delivery_hints:
            template_lines.append('(' + ', '.join(delivery_hints) + ')')

        # Add placeholder for lyrics
        if label in ('intro', 'outro'):
            template_lines.append('{instrumental_or_adlibs}')
        else:
            template_lines.append('{lyrics_here}')

        prev_label = label

    # Ensure we have [Break] before final chorus if there's a bridge
    template_text = '\n'.join(template_lines)

    return {
        "template": template_text,
        "sections_count": len(emotion_sections),
        "silence_gaps_used": len([g for g in (silence_gaps or []) if g.get('duration_seconds', 0) >= 0.8]),
        "vocal_delivery_hints": True,
        "note": ("Fill {lyrics_here} placeholders with actual lyrics. "
                  "Keep vocal delivery hints in parentheses for LLM reference — "
                  "they will be stripped before sending to MiniMax API. "
                  "Structure tags ([Verse], [Chorus], [Break], [Build Up]) "
                  "MUST be preserved in final lyrics sent to MiniMax."),
    }


# ─── Cover workflow recommendation ──────────────────────────────

def recommend_workflow(emotion_data, style_data, has_song_a_audio=False,
                       has_song_b_audio=False):
    """Recommend which MiniMax workflow to use based on available inputs.

    MiniMax provides several workflows:
    - music-2.6 (standard): Best for creative reimagining with custom lyrics
    - music-cover (one-step): Quick style transfer, preserves melody from audio
    - music-cover (two-step): Style transfer with modified lyrics + melody preservation
    - lyrics_generation: Generate lyrics first, then use with music-2.6

    The cover workflow is CRITICAL for melody preservation — it uses the original
    audio's melodic features to guide generation. Without it, the generated song
    will have a new melody that may not be recognizable.

    Returns:
        dict with:
        - workflow: 'cover_two_step' | 'cover_one_step' | 'standard' | 'standard_with_lyrics_gen'
        - reasoning: Why this workflow is recommended
        - steps: Ordered list of steps to execute
        - model: Which MiniMax model to use
    """
    has_lyrics = bool(style_data.get('lyrics') or style_data.get('formatted_lyrics'))
    # Also accept the orchestrator's detected_lyrics format (raw_transcript / tagged_lyrics)
    if not has_lyrics and isinstance(style_data.get('detected_lyrics'), dict):
        has_lyrics = bool(style_data['detected_lyrics'].get('tagged_lyrics') or
                          style_data['detected_lyrics'].get('raw_transcript'))
    song_name = style_data.get('song_name', style_data.get('name_b', 'unknown'))

    # Decision logic
    if has_song_a_audio and has_lyrics:
        # BEST: We have audio + lyrics → two-step cover for melody preservation
        return {
            "workflow": "cover_two_step",
            "model": "music-cover",
            "reasoning": (
                "Original audio available AND lyrics available → Two-step cover workflow. "
                "music_cover_preprocess extracts melody features, then music_generation "
                "with cover_feature_id preserves the melody while applying new style. "
                "This is the BEST option for melody recognition."
            ),
            "steps": [
                "1. Call POST /v1/music_cover_preprocess with audio_url of Song A",
                "2. Receive cover_feature_id + formatted_lyrics (editable)",
                "3. Edit formatted_lyrics if needed (translate, add structure tags, add [Break]/[Build Up])",
                "4. Call POST /v1/music_generation with model='music-cover', cover_feature_id, edited lyrics, style prompt",
                "5. Download result URL within 24 hours",
            ],
            "cover_feature_id_valid": "24 hours",
            "note": "cover_feature_id is free to generate. Lyrics MUST be 10-1000 chars with structure tags.",
        }

    elif has_song_a_audio and not has_lyrics:
        # Good: Audio but no custom lyrics → one-step cover
        return {
            "workflow": "cover_one_step",
            "model": "music-cover",
            "reasoning": (
                "Original audio available but no custom lyrics → One-step cover. "
                "MiniMax will extract lyrics from audio via ASR and transform style. "
                "Less control over lyrics but preserves melody automatically."
            ),
            "steps": [
                "1. Call POST /v1/music_generation with model='music-cover', audio_url, prompt",
                "2. MiniMax extracts lyrics from audio (ASR) and transforms style",
                "3. Download result URL within 24 hours",
            ],
            "note": "ASR-extracted lyrics may be inaccurate. For better control, use two-step workflow.",
        }

    elif not has_song_a_audio and has_lyrics:
        # Standard generation with custom lyrics
        return {
            "workflow": "standard",
            "model": "music-2.6",
            "reasoning": (
                "No original audio available but have lyrics → Standard generation. "
                "MiniMax will create a new melody. Song recognition depends on "
                "lyrics accuracy and prompt quality. Use production sheet formula "
                "for best results."
            ),
            "steps": [
                "1. Prepare structured lyrics with [Verse], [Chorus], [Break], [Build Up] tags",
                "2. Build production sheet prompt (genre, mood, voice, instruments, BPM, key, structure, production, avoid)",
                "3. Call POST /v1/music_generation with model='music-2.6', prompt, lyrics",
                "4. Download result URL within 24 hours",
            ],
            "note": "Without original audio, melody will be AI-generated. Recognition depends on lyrics and prompt quality.",
        }

    else:
        # No audio, no lyrics → generate everything
        return {
            "workflow": "standard_with_lyrics_gen",
            "model": "music-2.6",
            "reasoning": (
                "No original audio AND no lyrics → Use lyrics_optimizer to auto-generate lyrics "
                "from prompt, then generate music. Least control but fastest."
            ),
            "steps": [
                "1. (Optional) Call POST /v1/lyrics_generation with mode='write_full_song' to get structured lyrics",
                "2. Build production sheet prompt",
                "3. Call POST /v1/music_generation with model='music-2.6', prompt, lyrics_optimizer=true",
                "4. Download result URL within 24 hours",
            ],
            "note": "Consider using lyrics_generation first for better structure control, then pass those lyrics to music-2.6.",
        }


def build_final_prompt(emotion_data, style_data, style_category, target_bpm,
                       duration_seconds=180, language="english", silence_gaps=None,
                       compatibility_notes=None, image_data=None, video_data=None,
                       mashup_plan=None):
    """Build the complete music generation prompt."""
    profile = emotion_data.get('emotion_profile', {})
    hints = emotion_data.get('music_generation_hints', [])
    template = STYLE_TEMPLATES.get(style_category, {})

    # Key from style data or emotion data
    key = style_data.get('estimated_key', 'C major')

    # Build prompt components
    # Build prompt using the Production Sheet formula:
    #   [Genre/subgenre], [mood], [voice type], [instruments — name ALL],
    #   [BPM] BPM in [key], [structure], [production/mix], [things to avoid]

    instruments = template.get('instruments', 'balanced arrangement')
    mood = template.get('mood', 'expressive')
    vocal = template.get('vocal', 'clear emotive vocals')
    era = template.get('era', 'modern')
    avoid = template.get('avoid', 'avoid sparse minimal arrangements, avoid a cappella sections')

    # Duration string
    mins = int(duration_seconds // 60)
    secs = int(duration_seconds % 60)
    duration_str = f"{mins}:{secs:02d}"

    # Start building production sheet prompt
    parts = [
        # 1. Genre + era
        f"{style_category.replace('_', ' ')} style, {era} atmosphere",
        # 2. Mood
        f"{mood} mood",
        # 3. Voice
        f"{vocal}",
        # 4. Instruments — CRITICAL: always listed, always playing
        f"FULL ARRANGEMENT: {instruments} — all instruments always playing throughout, never drop to a cappella or silence",
    ]

    # New analysis: chord progression (autochord)
    chords = emotion_data.get('chord_progression', {})
    if chords.get('detected') and chords.get('progression_string'):
        parts.append(f"chord progression: {chords['progression_string']}")

    # Phase 3: beat tracking (beat_this)
    beats = style_data.get('beat_tracking', {})
    if isinstance(beats, dict) and beats.get('bpm_estimated') and beats.get('bpm_confidence', 0) > 0.5:
        time_sig = beats.get('time_signature_estimate', 4)
        bpm = beats['bpm_estimated']
        conf = beats['bpm_confidence']
        # Override target BPM with the more accurate beat_this value if confidence is high
        if conf > 0.8 and 60 < bpm < 200:
            target_bpm = bpm
        parts.append(f"beat grid: {time_sig}/4 at {bpm:.0f} BPM (confidence {conf:.2f})")

    # Phase 3: Basic Pitch melody analysis
    melody = style_data.get('melody_analysis', {})
    if isinstance(melody, dict) and melody.get('key_estimate_from_midi'):
        # Use the MIDI-confirmed key as a stronger signal than librosa's K-S estimate
        key_from_midi = melody['key_estimate_from_midi']
        key = key_from_midi
        interval_pattern = melody.get('interval_pattern', '')
        scale_modes = melody.get('scale_modes', [])
        bits = [f"melodic key from MIDI: {key_from_midi}"]
        if interval_pattern and interval_pattern != 'unknown':
            bits.append(f"interval motion: {interval_pattern.replace('_', ' ')}")
        if scale_modes:
            bits.append(f"modal character: {', '.join(scale_modes[:2])}")
        parts.append("; ".join(bits))

    # BPM + key should reflect the most accurate signals available.
    parts.append(f"tempo {target_bpm:.0f} BPM in {key}")

    # Phase 3: AST classification (top instruments / genres)
    ast = style_data.get('ast_classification', {})
    if isinstance(ast, dict) and ast.get('top_instruments'):
        top = ast['top_instruments'][:5]
        inst_str = ", ".join(
            f"{t['label'].lower()} ({t['score']:.2f})" for t in top if t['score'] > 0.1
        )
        if inst_str:
            parts.append(f"AST-detected sound palette: {inst_str}")

    # New analysis: loudness dynamics (LUFS / LRA)
    loudness = emotion_data.get('loudness_profile', {})
    if loudness.get('integrated_lufs') is not None:
        dynamics_class = loudness.get('dynamics_classification', '')
        if dynamics_class == 'wide_dynamic_range':
            parts.append("wide dynamic range with natural compression — quiet passages contrasted with loud climaxes")
        elif dynamics_class == 'compressed_consistent':
            parts.append("heavily compressed wall-of-sound production — consistent energy throughout")

    # New analysis: harmonic/percussive balance (HPSS)
    hpss = emotion_data.get('harmonic_percussive', {})
    hpss_class = hpss.get('classification', '')
    if hpss_class == 'smooth_melodic':
        parts.append("smooth melodic texture with minimal percussive harshness")
    elif hpss_class == 'percussive_rhythmic':
        parts.append("driving rhythmic texture with prominent percussive elements")

    # New analysis: vocal quality (parselmouth)
    vocal_quality = emotion_data.get('vocal_quality', {})
    vq = vocal_quality.get('voice_quality', '')
    if vq == 'smooth_clean':
        parts.append("clean polished vocal production")
    elif vq == 'rough_pressed':
        parts.append("raw gritty vocal delivery with pressed quality")
    elif vq == 'slightly_rough':
        parts.append("slightly rough edgy vocal character")

    # New analysis: CLAP classification (append to template, don't replace)
    clap = style_data.get('clap_classification', {})
    if clap.get('detected'):
        top_moods = clap.get('top_moods', [])
        if top_moods:
            # APPEND detected moods to template mood, don't replace
            detected_mood_str = ", ".join([m[0] for m in top_moods[:3]])
            parts.insert(2, f"detected mood from audio: {detected_mood_str}")
        top_instruments = clap.get('top_instruments', [])
        if top_instruments:
            # APPEND detected instruments to template, don't replace
            detected_inst_str = ", ".join([i[0] for i in top_instruments[:5]])
            parts.insert(4, f"audio also features: {detected_inst_str}")

    # Aggregate detected emotions across all sections
    all_emotion_sections = emotion_data.get('emotion_sections', [])
    detected_emotions = []
    for sec in all_emotion_sections:
        for e in sec.get('emotion_classification', []):
            detected_emotions.append(e)
    if detected_emotions:
        from collections import Counter
        emotion_counts = Counter(detected_emotions)
        top_emotions = [e for e, _ in emotion_counts.most_common(3)]
        emotion_str = ", ".join(top_emotions)
        parts.append(f"emotion signature from analysis: {emotion_str}")

    # Aggregate vocal characteristics across sections
    section_registers = [s.get('vocal_register', 'unknown') for s in all_emotion_sections if s.get('vocal_register') and s.get('vocal_register') not in ('unknown', 'mixed')]
    section_harmonies = [s.get('harmony_quality', 'unknown') for s in all_emotion_sections if s.get('harmony_quality') and s.get('harmony_quality') != 'unknown']
    section_rhythms = [s.get('rhythm_feel', 'unknown') for s in all_emotion_sections if s.get('rhythm_feel') and s.get('rhythm_feel') not in ('unknown', 'mixed')]

    if section_registers:
        from collections import Counter
        dominant_register = Counter(section_registers).most_common(1)[0][0]
        register_map = {
            'chest': 'full chest voice power throughout',
            'head': 'light head voice mix throughout',
            'falsetto': 'airy falsetto delivery throughout',
        }
        if dominant_register in register_map:
            parts.append(f"vocal character: {register_map[dominant_register]}")

    if section_harmonies:
        from collections import Counter
        dominant_harmony = Counter(section_harmonies).most_common(1)[0][0]
        harmony_map = {
            'consonant': 'consonant, smooth harmonic content',
            'tense': 'tense, dissonant harmonic character',
            'rich': 'rich harmonic movement and color',
        }
        if dominant_harmony in harmony_map:
            parts.append(f"harmonic character: {harmony_map[dominant_harmony]}")

    if section_rhythms:
        from collections import Counter
        dominant_rhythm = Counter(section_rhythms).most_common(1)[0][0]
        rhythm_map = {
            'swing': 'swing feel, laid-back groove',
            'straight': 'straight eighth-note rhythm',
        }
        if dominant_rhythm in rhythm_map:
            parts.append(f"rhythm: {rhythm_map[dominant_rhythm]}")

    # ── Tonal character (from analyze_audio.brightness + energy_description) ──
    brightness = style_data.get('brightness')
    energy_desc = style_data.get('energy_description')
    brightness_text = str(brightness).lower() if brightness is not None else ''
    if brightness_text and brightness_text != 'balanced':
        bright_map = {
            'bright': 'bright treble, crisp presence',
            'dark': 'dark warm tone, rolled-off highs',
        }
        if any(token in brightness_text for token in ('bright', 'treble')):
            parts.append(f"tonal character: {bright_map['bright']}")
        elif any(token in brightness_text for token in ('dark', 'warm', 'mellow', 'bass')):
            parts.append(f"tonal character: {bright_map['dark']}")
    if energy_desc and energy_desc not in ('moderate', 'medium'):
        # Use the energy description as-is (already human-readable)
        parts.append(f"energy profile: {energy_desc}")

    # ── Rhythm metrics (from analyze_audio.tempo_consistency, onset_density) ──
    tempo_consistency = style_data.get('tempo_consistency')
    onset_density = style_data.get('onset_density')
    if tempo_consistency is not None:
        if tempo_consistency > 0.85:
            parts.append("rhythm: tight, on-beat delivery")
        elif tempo_consistency < 0.5:
            parts.append("rhythm: loose, with tempo drift")
    if onset_density is not None:
        if onset_density > 5:
            parts.append("high note density — busy, intricate")
        elif onset_density < 1.5:
            parts.append("low note density — spacious, with room")

    # ── Instrument hints (from analyze_audio / analyze_two_songs) ──
    instrument_hints = style_data.get('instrument_hints', {})
    if instrument_hints:
        hint_map = {
            'likely_acoustic': 'acoustic-leaning timbres',
            'likely_electronic': 'electronic / synthetic textures',
            'likely_orchestral': 'orchestral / cinematic textures',
            'likely_distorted': 'distorted / overdriven tones',
        }
        matched = [hint_map[k] for k in hint_map if instrument_hints.get(k)]
        if matched:
            parts.append(f"instruments detected: {', '.join(matched)}")

    # Per-section vocal texture aggregation (jitter, shimmer, HNR)
    # These were computed per section in analyze_vocal_emotion but only the global
    # voice_quality was used. Now we surface per-section variation.
    hnrs = [s.get('hnr_db') for s in all_emotion_sections if s.get('hnr_db') is not None]
    jitters = [s.get('jitter_pct') for s in all_emotion_sections if s.get('jitter_pct') is not None]
    shimmers = [s.get('shimmer_pct') for s in all_emotion_sections if s.get('shimmer_pct') is not None]
    if hnrs or jitters or shimmers:
        # Identify sections that stand out: breathier than average (low HNR) or more raw (high jitter)
        avg_hnr = sum(hnrs) / len(hnrs) if hnrs else 0
        breathy_sections = [s for s in all_emotion_sections
                            if s.get('hnr_db') is not None and s.get('hnr_db', 99) < avg_hnr - 5]
        if breathy_sections:
            labels = sorted({s.get('structural_label', 'section') for s in breathy_sections})[:3]
            parts.append(
                f"vocal texture in {'/'.join(labels)}: breathier / more intimate than average"
            )
        high_jitter_sections = [s for s in all_emotion_sections
                                if s.get('jitter_pct', 0) > 1.0]
        if high_jitter_sections:
            labels = sorted({s.get('structural_label', 'section') for s in high_jitter_sections})[:3]
            parts.append(
                f"vocal texture in {'/'.join(labels)}: raw / strained delivery"
            )

    # Add emotion-specific dynamics
    curve = profile.get('intensity_curve', {}).get('pattern', '')
    dynamic_range = profile.get('dynamic_range', 0)

    # Vocal speed / elongation
    vocal_speed = emotion_data.get('vocal_speed_patterns', {})
    speed_pattern = vocal_speed.get('pattern', 'steady')

    if speed_pattern == 'decelerating':
        parts.append("vocal delivery progressively slows with emotional syllable stretching toward the end")
    elif speed_pattern == 'late_elongation':
        parts.append("final sections feature emotionally stretched syllables, vocalist holds and bends notes")
    elif speed_pattern == 'gradual_slowing':
        parts.append("gradual rubato throughout, vocalist increasingly stretches phrases")

    # Pitch bends
    pitch_bends = emotion_data.get('pitch_bends', [])
    significant_bends = [b for b in pitch_bends if b.get('pitch_range_hz', 0) > 40]
    if len(significant_bends) > 3:
        parts.append("expressive pitch bends and vocal slides at phrase endings")

    # Intensity curve → arrangement build strategy
    # IMPORTANT: 'sparse' sections still have instruments — just fewer
    inst_list = [i.strip() for i in instruments.split(',')]
    min_inst = ', '.join(inst_list[:2]) if len(inst_list) >= 2 else instruments

    if curve == 'crescendo':
        parts.append(f"starts with reduced arrangement ({min_inst} only), progressively adds layers, builds to full orchestration at climax")
    elif curve == 'decrescendo':
        parts.append(f"opens with full arrangement, gradually reduces to {min_inst} for intimate ending")
    elif curve == 'wave':
        parts.append(f"dynamic contrast between sections — fuller for peaks, reduced to {min_inst} for valleys, but ALWAYS with instrumental backing")
    elif curve == 'climax_late':
        parts.append(f"restrained through early sections (fewer instruments but never silent), explosive climax in final third with full arrangement")

    if dynamic_range > 0.08:
        parts.append("wide dynamic range — quiet passages contrasted with loud climaxes, include 1-2 second dramatic pauses between major sections")

    # Use detected silence gaps for precise pause positioning
    if silence_gaps:
        significant_gaps = [g for g in silence_gaps if g.get('duration_seconds', 0) >= 0.8]
        if significant_gaps:
            gap_positions = [f"{g['start_seconds']:.0f}s ({g['duration_seconds']:.1f}s pause)" for g in significant_gaps[:4]]
            parts.append(f"natural dramatic pauses detected at: {', '.join(gap_positions)} — preserve these with [Break] tags in lyrics")

    # Repetitive intensification
    rep = profile.get('repetitive_intensification', {})
    if rep.get('detected'):
        parts.append("for repeated phrases: each repetition grows more intense and powerful")

    # Emotional shifts
    shifts = profile.get('emotional_shifts', [])
    sudden = [s for s in shifts if s.get('type') == 'sudden']
    if sudden:
        # Provide specific pause timing for the top sudden shifts
        pause_positions = []
        for s in sudden[:3]:
            pos = int(s['at_seconds'])
            pause_positions.append(f"{pos}s")
        parts.append(f"include dramatic 1-2 second pauses before sudden intensity shifts at approximately: {', '.join(pause_positions)}")
        parts.append("silence gaps between sections should have brief instrumental sustain or reverb tail — not abrupt silence")

    # Language
    if language and language.lower() not in ('english', 'en'):
        lang_names = {
            'fr': 'French', 'french': 'French',
            'es': 'Spanish', 'spanish': 'Spanish',
            'de': 'German', 'german': 'German',
            'it': 'Italian', 'italian': 'Italian',
            'pt': 'Portuguese', 'portuguese': 'Portuguese',
        }
        lang = lang_names.get(language.lower(), language)
        parts.append(f"{lang} lyrics")

    # Quality + duration
    parts.append("studio recording quality")

    # Image-driven style cues (album art / image input)
    if image_data and not image_data.get('error'):
        image_bits = []
        if image_data.get('mood') and image_data['mood'] != 'unknown':
            image_bits.append(f"visual mood: {image_data['mood']}")
        for hint in image_data.get('style_hints', [])[:3]:
            if hint:
                image_bits.append(f"art suggests: {hint}")
        for hint in image_data.get('production_hints', [])[:2]:
            if hint:
                image_bits.append(f"production cue: {hint}")
        for hint in image_data.get('era_hints', [])[:2]:
            if hint:
                image_bits.append(f"era cue: {hint}")
        if image_bits:
            parts.append("; ".join(image_bits))

    # Video-driven style cues (music video / video input)
    if video_data and not video_data.get('error'):
        video_bits = []
        cp = video_data.get('color_palette', {})
        if isinstance(cp, dict) and cp.get('dominant_mood'):
            video_bits.append(f"video palette mood: {cp['dominant_mood']}")
        if video_data.get('vocal_emotion') and not video_data['vocal_emotion'].get('error'):
            ve = video_data['vocal_emotion']
            if ve.get('emotion_profile', {}).get('overall_emotion_type'):
                video_bits.append(f"video vocal emotion: {ve['emotion_profile']['overall_emotion_type']}")
        top_genres = video_data.get('audio_features', {}).get('clap_classification', {}).get('top_genres')
        if top_genres:
            genre_labels = []
            for genre in top_genres[:2]:
                if isinstance(genre, (list, tuple)) and genre:
                    genre_labels.append(str(genre[0]))
                elif isinstance(genre, dict) and genre.get('label'):
                    genre_labels.append(str(genre['label']))
                else:
                    genre_labels.append(str(genre))
            if genre_labels:
                video_bits.append(f"video audio: {', '.join(genre_labels)}")
        if video_data.get('motion_arc'):
            avg_motion = sum(video_data['motion_arc']) / max(len(video_data['motion_arc']), 1)
            motion_descriptor = "high-motion" if avg_motion > 0.4 else "low-motion" if avg_motion < 0.1 else "moderate-motion"
            video_bits.append(f"video energy: {motion_descriptor}")
        if video_bits:
            parts.append("; ".join(video_bits))

    # Mashup-specific cues from analyze_two_songs.generate_mashup_recommendations
    if mashup_plan:
        style_notes = mashup_plan.get('style_notes')
        if style_notes:
            parts.append(f"style direction: {style_notes}")
        inst_additions = mashup_plan.get('instrument_prompt_additions')
        if inst_additions:
            parts.append(inst_additions)

    # Music generation hints (computed by analyze_vocal_emotion.generate_music_hints).
    # These cover anti-sparse-silence guard, repetitive intensification, sudden shifts,
    # and overall mood keywords. Inject as a single trailing sentence so they reach
    # the model rather than being silently dropped.
    if hints:
        # De-duplicate with parts already added
        unique_hints = []
        existing = " ".join(parts).lower()
        for h in hints:
            if h and h.lower()[:40] not in existing:
                unique_hints.append(h)
        if unique_hints:
            parts.append("; ".join(unique_hints[:4]))

    # Avoid list — from template
    parts.append(avoid)

    # Mashup compatibility notes (from _key_compat.py)
    if compatibility_notes:
        notes_text = "; ".join(compatibility_notes[:3])
        parts.append(f"mashup compatibility: {notes_text}")

    final_prompt = ",\n".join(parts)
    return final_prompt


# ─── Main ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Convert emotion + style analysis to music generation prompt')
    parser.add_argument('--emotion', required=True, help='Emotion analysis JSON (from analyze_vocal_emotion.py)')
    parser.add_argument('--style', required=True, help='Style analysis JSON (from analyze_audio.py or analyze_two_songs.py)')
    parser.add_argument('--orchestrator-output', help='Full orchestrator JSON (analysis_orchestrator.py output) — '
                        'enables image/video/mashup emotion consumption')
    parser.add_argument('--style-category', choices=list(STYLE_TEMPLATES.keys()),
                        help='Force style category (auto-detected if omitted)')
    parser.add_argument('--target-duration', type=int, default=180, help='Target duration in seconds (default 180)')
    parser.add_argument('--language', default='english', help='Lyrics language')
    parser.add_argument('--song-a-bpm', type=float, help='Override Song A BPM')
    parser.add_argument('--output', help='Output JSON file path')
    args = parser.parse_args()

    # Load inputs
    with open(args.emotion) as f:
        emotion_data = json.load(f)

    # Style might be from analyze_audio.py (single song) or analyze_two_songs.py (two songs)
    with open(args.style) as f:
        raw_style = json.load(f)

    # Optional: full orchestrator output for image/video/mashup emotion
    orchestrator_data = None
    if args.orchestrator_output:
        with open(args.orchestrator_output) as f:
            orchestrator_data = json.load(f)

    # Normalise: extract Song B style from either format
    if 'song_b_reference' in raw_style:
        style_data = raw_style['song_b_reference']
        song_a_data = raw_style.get('song_a_original', {})
        mashup_plan = raw_style.get('mashup_plan', {})
    elif 'mashup_plan' in raw_style:
        style_data = raw_style.get('song_b_reference', raw_style)
        song_a_data = raw_style.get('song_a_original', {})
        mashup_plan = raw_style.get('mashup_plan', {})
    else:
        # Single song analysis (analyze_audio.py format)
        style_data = raw_style
        song_a_data = {}
        mashup_plan = {}

    # If orchestrator output is available, prefer mashup_vocal_emotion over plain emotion_data
    if orchestrator_data and orchestrator_data.get('mashup', {}).get('song_a_vocal_emotion'):
        emotion_data = orchestrator_data['mashup']['song_a_vocal_emotion']

    # Pull detected lyrics and advanced analysis from the orchestrator output
    # and inject into style_data so the prompt + workflow recommendation see them.
    if orchestrator_data:
        audio_part = orchestrator_data.get('audio') or {}
        mashup_part = orchestrator_data.get('mashup') or {}

        # 1) Detected lyrics → workflow recommendation sees them
        _dl = audio_part.get('lyrics') or mashup_part.get('song_a_lyrics')
        if _dl and isinstance(_dl, dict):
            style_data = dict(style_data)
            style_data['detected_lyrics'] = _dl

        # 2) Beat tracking (beat_this) → BPM confidence + time sig
        beats = audio_part.get('beats') or {}
        if isinstance(beats, dict) and not beats.get('error'):
            style_data = dict(style_data)
            style_data['beat_tracking'] = beats

        # 3) Basic Pitch melody analysis → MIDI-confirmed key + scale modes
        melody = audio_part.get('melody') or {}
        if isinstance(melody, dict) and not melody.get('error'):
            style_data = dict(style_data)
            style_data['melody_analysis'] = melody

        # 4) AST classification (instruments / genres)
        ast = audio_part.get('ast_classification') or {}
        if isinstance(ast, dict) and not ast.get('error'):
            style_data = dict(style_data)
            style_data['ast_classification'] = ast

    # Determine style category
    if args.style_category:
        category = args.style_category
    else:
        category = infer_style_category(style_data)

    # Target BPM
    song_a_bpm = args.song_a_bpm or song_a_data.get('bpm', style_data.get('bpm', 100))
    song_b_bpm = style_data.get('bpm', 100)
    target_bpm = mashup_plan.get('target_bpm') or resolve_target_bpm(song_a_bpm, song_b_bpm, category)

    # Compatibility notes from _key_compat (if available)
    compat = mashup_plan.get('compatibility', {})
    compatibility_notes = compat.get('notes', [])

    # Build outputs
    template = STYLE_TEMPLATES.get(category, {})

    # If allin1 song structure is available, upgrade emotion section labels
    # by matching allin1 segment labels to emotion sections via time overlap.
    song_structure = emotion_data.get('song_structure', {})
    if song_structure.get('detected') and song_structure.get('segments'):
        struct_segments = song_structure['segments']
        emotion_sections = emotion_data.get('emotion_sections', [])
        for esec in emotion_sections:
            es_start = esec.get('start_seconds', 0)
            es_end = esec.get('end_seconds', 0)
            es_mid = (es_start + es_end) / 2
            for sseg in struct_segments:
                ss_start = sseg.get('start_seconds', 0)
                ss_end = sseg.get('end_seconds', 0)
                if ss_start <= es_mid <= ss_end:
                    allin1_label = sseg.get('label', '')
                    if allin1_label:
                        esec['structural_label'] = allin1_label
                    break

    section_prompts = build_section_prompts(emotion_data.get('emotion_sections', []), template)
    arrangement_plan = build_arrangement_plan(emotion_data, category)

    # Vocal speed patterns → prompts and lyrics modifications
    vocal_speed_data = emotion_data.get('vocal_speed_patterns', {})
    pitch_bends_data = emotion_data.get('pitch_bends', [])
    vocal_speed_prompts = build_vocal_speed_prompts(vocal_speed_data, pitch_bends_data)

    final_prompt = build_final_prompt(
        emotion_data, style_data, category, target_bpm,
        duration_seconds=args.target_duration, language=args.language,
        silence_gaps=emotion_data.get('silence_gaps', []),
        compatibility_notes=compatibility_notes,
        image_data=(orchestrator_data or {}).get('image'),
        video_data=(orchestrator_data or {}).get('video'),
        mashup_plan=mashup_plan or None,
    )

    # Generate structured lyrics template with [Break] and [Build Up] tags
    structured_lyrics = generate_structured_lyrics_template(
        emotion_sections=emotion_data.get('emotion_sections', []),
        vocal_speed_patterns=vocal_speed_data,
        silence_gaps=emotion_data.get('silence_gaps', []),
        arrangement_plan=arrangement_plan,
        style_category=category,
        language=args.language,
    )

    # Recommend MiniMax workflow (cover vs standard generation)
    has_audio = bool(emotion_data.get('audio_info', {}).get('file'))
    # Song B has audio when its source_file points to a real file (not LLM-knowledge-only).
    # In analyze_two_songs.py, song_b_reference.source_file is set when an actual audio path was provided.
    has_song_b_audio = bool(style_data.get('source_file')) and os.path.isfile(style_data.get('source_file', ''))
    workflow_rec = recommend_workflow(
        emotion_data=emotion_data,
        style_data=style_data,
        has_song_a_audio=has_audio,
        has_song_b_audio=has_song_b_audio,
    )

    # Pull detected lyrics from the orchestrator output (for the result field)
    detected_lyrics = None
    if orchestrator_data:
        audio_part = orchestrator_data.get('audio') or {}
        mashup_part = orchestrator_data.get('mashup') or {}
        detected_lyrics = audio_part.get('lyrics') or mashup_part.get('song_a_lyrics')

    result = {
        "style_category": category,
        "target_bpm": target_bpm,
        "target_duration_seconds": args.target_duration,
        "language": args.language,
        "final_prompt": final_prompt,
        "structured_lyrics_template": structured_lyrics,
        "workflow_recommendation": workflow_rec,
        "section_prompts": section_prompts,
        "arrangement_plan": arrangement_plan,
        "vocal_speed_patterns": vocal_speed_prompts,
        # style_template_used removed in v0.1.1 (always == style_category; no downstream consumer)
        # emotion_hints_used removed in v0.1.1 (hints are now injected into final_prompt directly)
        "detected_lyrics": detected_lyrics,
    }

    json_out = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(json_out)
        print(f"Written: {args.output}", file=sys.stderr)
    else:
        print(json_out)


if __name__ == '__main__':
    main()
