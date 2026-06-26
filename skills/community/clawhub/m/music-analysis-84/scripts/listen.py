#!/usr/bin/env python3
"""Unified full-track listener v2: snapshot + structure/groove/harmony/emotion + temporal journey + lyric alignment."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from analyze_music import analyze_with_librosa, ffprobe_meta  # noqa: E402
from instrument_detect import analyze_instruments  # noqa: E402
from music_analysis_v2 import format_ts, to_native  # noqa: E402
from temporal_listen import analyze_temporal  # noqa: E402

WHISPER_CLI = Path("/opt/homebrew/bin/whisper-cli")
WHISPER_MODEL = Path("~/.local/share/whisper-cpp/ggml-large-v3-turbo.bin").expanduser()
YOUTUBE_ARTIFACT_RE = re.compile(
    r"^(thanks for watching[!. ]*|thank you for watching[!. ]*|subscribe[!. ]*|like and subscribe[!. ]*)$",
    re.IGNORECASE,
)
BRACKET_TAG_RE = re.compile(r"\[[^\]]+\]")
NON_WORD_RE = re.compile(r"[^a-zA-Z0-9'\s-]+")
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "then", "to", "of", "in", "on", "for", "with", "at", "by", "from",
    "i", "you", "me", "my", "we", "our", "your", "it", "is", "are", "was", "were", "be", "been", "am",
}
DARK_WORDS = {
    "dark", "sad", "alone", "lonely", "hurt", "pain", "cry", "crying", "tears", "death", "dead", "die", "dying",
    "blood", "grave", "lost", "loss", "broken", "broke", "cold", "empty", "fear", "afraid", "shadow", "shadows",
    "ghost", "night", "sorrow", "blue", "black", "fall", "fallen", "bleed", "bleeding", "ash", "ashes", "void",
    "bad", "memory", "memories", "goodbye", "gone", "old", "regret", "regrets", "miss", "missing", "leave", "left",
}
TENDER_WORDS = {
    "love", "heart", "home", "hold", "kiss", "warm", "soft", "gentle", "light", "dream", "dreaming", "heaven",
    "safe", "touch", "beautiful", "grace", "bloom", "alive", "hope", "hoping",
}
UPLIFT_WORDS = {
    "sun", "shine", "gold", "dance", "free", "flying", "open", "rise", "rising", "good", "joy", "smile", "bright",
    "happy", "alive", "glow", "sweet", "summer",
}
AGGRESSION_WORDS = {
    "fire", "fight", "run", "wild", "burn", "burning", "crash", "rage", "knife", "gun", "loud", "scream", "screaming",
    "riot", "fast", "storm", "hit", "hits",
}
NEGATIONS = {"not", "never", "no", "don't", "dont", "won't", "wont", "can't", "cant"}


def seconds_overlap(a_start: float, a_end: float, b_start: float, b_end: float) -> float:
    return max(0.0, min(a_end, b_end) - max(a_start, b_start))


def run_ffmpeg_to_wav(audio_path: Path, wav_path: Path) -> None:
    cmd = ["ffmpeg", "-y", "-i", str(audio_path), "-ar", "16000", "-ac", "1", str(wav_path)]
    subprocess.run(cmd, check=True, capture_output=True, text=True)


def parse_whisper_stdout(stdout: str) -> list[dict[str, Any]]:
    segments = []
    line_re = re.compile(r"^\[(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})\]\s*(.*)$")

    def parse_clock(ts: str) -> float:
        hours, minutes, seconds = ts.split(":")
        return int(hours) * 3600 + int(minutes) * 60 + float(seconds)

    for raw_line in stdout.splitlines():
        line = raw_line.strip()
        match = line_re.match(line)
        if not match:
            continue
        start_s = parse_clock(match.group(1))
        end_s = parse_clock(match.group(2))
        text = re.sub(r"\s+", " ", match.group(3)).strip().strip('"')
        if not text:
            continue
        segments.append({
            "start": round(start_s, 3),
            "end": round(end_s, 3),
            "start_fmt": format_ts(start_s),
            "end_fmt": format_ts(end_s),
            "text": text,
        })
    return segments


def normalize_lyric_text(text: str) -> str:
    text = BRACKET_TAG_RE.sub(" ", text)
    text = NON_WORD_RE.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


WHISPER_HALLUCINATION_RE = re.compile(
    r"^(soft music|loud music|upbeat music|gentle music|dramatic music|instrumental music|piano music|"
    r"music playing|music continues|music|applause|laughter|cheering|audience cheering|audience applause|"
    r"silence|inaudible|unintelligible|foreign language|speaking foreign language)$",
    re.IGNORECASE,
)


def is_real_lyric_text(text: str) -> bool:
    normalized = normalize_lyric_text(text)
    if not normalized:
        return False
    if WHISPER_HALLUCINATION_RE.match(normalized.strip()):
        return False
    words = [w.lower() for w in normalized.split() if w.strip()]
    content_words = [w for w in words if w not in STOPWORDS and any(c.isalpha() for c in w)]
    return len(content_words) >= 2


def clean_lyric_segments(segments: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str]]:
    notes = []
    cleaned = []
    filtered_count = 0
    for seg in segments:
        raw = seg["text"].strip()
        if YOUTUBE_ARTIFACT_RE.match(raw):
            filtered_count += 1
            notes.append(f"Filtered likely end-card artifact: {raw}")
            continue
        normalized = normalize_lyric_text(raw)
        if not is_real_lyric_text(raw):
            filtered_count += 1
            continue
        enriched = dict(seg)
        enriched["raw_text"] = raw
        enriched["text"] = normalized
        cleaned.append(enriched)

    # Detect repetitive Whisper hallucinations: if >60% of segments are identical text, drop all
    if cleaned:
        texts = [s["text"].lower().strip() for s in cleaned]
        from collections import Counter
        counts = Counter(texts)
        most_common_text, most_common_count = counts.most_common(1)[0]
        if most_common_count / len(cleaned) > 0.6:
            filtered_count += len(cleaned)
            notes.append(f"Filtered {len(cleaned)} segments: Whisper hallucination detected ('{most_common_text}' repeated {most_common_count}/{len(cleaned)} times).")
            cleaned = []

    if filtered_count:
        notes.append(f"Filtered {filtered_count} non-lyric / artifact Whisper segment(s) total.")
    return cleaned, notes


def score_words(words: list[str], lexicon: set[str]) -> int:
    score = 0
    for idx, word in enumerate(words):
        if word not in lexicon:
            continue
        weight = 1
        if idx > 0 and words[idx - 1] in NEGATIONS:
            weight = -1
        score += weight
    return score


def analyze_lyric_vibe(lyrics: dict[str, Any]) -> dict[str, Any]:
    segments = lyrics.get("segments", [])
    full_text = lyrics.get("full_text", "")
    if not segments or not full_text:
        return {
            "available": False,
            "confidence": 0.0,
            "dominance": "none",
            "mood": "instrumental / lyric-insufficient",
            "overview": "No usable lyrical content was available, so the emotional read is driven by the music.",
            "word_count": 0,
            "scores": {},
            "notes": ["Lyric mood skipped: no real lyric text after filtering."],
        }

    words = [w.lower() for w in normalize_lyric_text(full_text).split() if w.strip()]
    content_words = [w for w in words if w not in STOPWORDS]
    dark = score_words(content_words, DARK_WORDS)
    tender = score_words(content_words, TENDER_WORDS)
    uplift = score_words(content_words, UPLIFT_WORDS)
    aggression = score_words(content_words, AGGRESSION_WORDS)
    weighted_dark = dark + max(0, aggression // 2)
    weighted_light = uplift + max(0, tender // 2)
    net_darkness = weighted_dark - weighted_light
    emotional_hits = abs(dark) + abs(tender) + abs(uplift) + abs(aggression)
    confidence = min(1.0, emotional_hits / max(3.0, len(content_words) * 0.08))

    if net_darkness >= 2:
        mood = "dark / heavy"
    elif net_darkness <= -2:
        mood = "uplifted / warm"
    elif aggression >= 2 and dark >= 1:
        mood = "volatile / intense"
    elif tender >= 2:
        mood = "tender / intimate"
    else:
        mood = "mixed / ambiguous"

    if confidence >= 0.45 and mood in {"dark / heavy", "volatile / intense", "tender / intimate", "uplifted / warm"}:
        dominance = "strong"
    elif confidence >= 0.25:
        dominance = "moderate"
    else:
        dominance = "light"

    overview = {
        "dark / heavy": "The lyrical content is unambiguously dark enough to steer the emotional read even if the arrangement feels bright.",
        "volatile / intense": "The lyric layer reads emotionally charged and unstable; it should weigh heavily in the final vibe.",
        "tender / intimate": "The lyrics read close, vulnerable, and human; they soften or deepen the musical surface.",
        "uplifted / warm": "The lyrics themselves pull toward warmth or lift rather than darkness.",
        "mixed / ambiguous": "The lyrics contribute, but they do not force a single emotional interpretation on their own.",
    }[mood]

    return {
        "available": True,
        "confidence": round(confidence, 3),
        "dominance": dominance,
        "mood": mood,
        "overview": overview,
        "word_count": len(content_words),
        "scores": {
            "dark": dark,
            "tender": tender,
            "uplift": uplift,
            "aggression": aggression,
            "net_darkness": net_darkness,
        },
        "notes": ["Lyric mood is derived from filtered Whisper text and can override the audio-only vibe when confidence is high."],
    }


def combine_emotional_read(audio_emotion: dict[str, Any], lyric_vibe: dict[str, Any]) -> dict[str, Any]:
    audio_color = audio_emotion.get("color_word", "mixed / bittersweet")
    audio_energy = audio_emotion.get("energy_word", "present / moving")
    if not lyric_vibe.get("available"):
        return {
            "primary_driver": "audio",
            "final_mood": audio_color,
            "overview": audio_emotion.get("overview", "Audio-led emotional read."),
            "reasoning": ["No reliable lyric layer was available, so the read stays music-first."],
        }

    lyric_mood = lyric_vibe["mood"]
    confidence = lyric_vibe.get("confidence", 0.0)
    dominance = lyric_vibe.get("dominance", "light")
    if dominance == "strong":
        final_mood = lyric_mood
        primary = "lyrics"
        overview = f"Lyrics dominate the final vibe: musically it may feel {audio_energy}, but the words make the track read {lyric_mood}."
    elif dominance == "moderate":
        final_mood = f"{lyric_mood} over {audio_energy} music"
        primary = "hybrid"
        overview = f"The final read is hybrid: the arrangement brings {audio_energy}, but the lyric content pushes the meaning toward {lyric_mood}."
    else:
        final_mood = audio_color
        primary = "audio"
        overview = f"The music still leads, but the lyric layer adds a {lyric_mood} tint." if confidence > 0 else audio_emotion.get("overview", "Audio-led emotional read.")
    return {
        "primary_driver": primary,
        "final_mood": final_mood,
        "overview": overview,
        "reasoning": [
            audio_emotion.get("overview", "Audio read available."),
            lyric_vibe.get("overview", "Lyric read available."),
        ],
    }


def transcribe_lyrics(audio_path: Path) -> dict[str, Any]:
    if not WHISPER_CLI.exists():
        return {"available": False, "skipped": True, "reason": f"whisper-cli not found at {WHISPER_CLI}", "segments": [], "notes": ["Lyrics skipped: whisper-cli unavailable."]}
    if not WHISPER_MODEL.exists():
        return {"available": False, "skipped": True, "reason": f"Whisper model not found at {WHISPER_MODEL}", "segments": [], "notes": ["Lyrics skipped: Whisper model missing."]}

    with tempfile.TemporaryDirectory(prefix="music-listen-") as tmpdir:
        wav_path = Path(tmpdir) / "input-16k.wav"
        try:
            run_ffmpeg_to_wav(audio_path, wav_path)
            cmd = [str(WHISPER_CLI), "-m", str(WHISPER_MODEL), "-f", str(wav_path), "-of", str(Path(tmpdir) / "whisper_out")]
            proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
            segments = parse_whisper_stdout(proc.stdout)
            cleaned, clean_notes = clean_lyric_segments(segments)
            full_text = " ".join(seg["text"] for seg in cleaned).strip()
            usable = bool(cleaned and full_text)
            return {
                "available": usable,
                "skipped": False,
                "engine": "whisper-cli",
                "model": str(WHISPER_MODEL),
                "wav_preprocessed": True,
                "segment_count": len(cleaned),
                "segments": cleaned,
                "full_text": full_text,
                "notes": clean_notes or (["Lyrics transcribed with timestamped Whisper segments."] if usable else ["No real lyric text found after filtering Whisper artifacts."]),
            }
        except subprocess.CalledProcessError as e:
            detail = (e.stderr or e.stdout or str(e)).strip()
            return {
                "available": True,
                "skipped": True,
                "reason": f"whisper-cli failed: {detail}",
                "segments": [],
                "notes": ["Lyrics skipped because whisper-cli returned an error."],
            }


def window_bounds(moment: dict[str, Any], window_sec: float) -> tuple[float, float]:
    mid = float(moment["time"])
    half = window_sec / 2.0
    return mid - half, mid + half


def attach_lyrics_to_timeline(temporal: dict[str, Any], lyrics: dict[str, Any]) -> list[dict[str, Any]]:
    segments = lyrics.get("segments", [])
    window_sec = float(temporal.get("window_sec", 4.0))
    aligned = []
    for moment in temporal.get("timeline", []):
        start, end = window_bounds(moment, window_sec)
        matching = []
        for seg in segments:
            overlap = seconds_overlap(start, end, float(seg["start"]), float(seg["end"]))
            if overlap > 0:
                matching.append({**seg, "overlap_sec": round(overlap, 3)})
        lyric_excerpt = " / ".join(seg["text"] for seg in matching)
        enriched = dict(moment)
        enriched["window_start"] = round(start, 2)
        enriched["window_end"] = round(end, 2)
        enriched["lyrics"] = matching
        if lyric_excerpt:
            enriched["lyric_excerpt"] = lyric_excerpt
        aligned.append(enriched)
    return aligned


def top_windows(timeline: list[dict[str, Any]], key: str, count: int = 3, min_separation_sec: float = 8.0, reverse: bool = True) -> list[dict[str, Any]]:
    if not timeline:
        return []
    ranked = sorted(timeline, key=lambda m: (m.get(key, 0), m.get("energy", 0)), reverse=reverse)
    picks = []
    for item in ranked:
        if any(abs(float(item["time"]) - float(existing["time"])) < min_separation_sec for existing in picks):
            continue
        picks.append(item)
        if len(picks) >= count:
            break
    return sorted(picks, key=lambda m: float(m["time"]))


def summarize_alignment(high_energy: list[dict[str, Any]], high_tension: list[dict[str, Any]], low_energy: list[dict[str, Any]]) -> str:
    if not any(item.get("lyric_excerpt") for item in [*high_energy, *high_tension, *low_energy]):
        return "No timestamped lyric overlap found, so lyric-energy alignment could not be evaluated."
    intense_words = {"burn", "fire", "run", "wild", "heart", "crash", "fight", "fall", "loud", "blood", "love", "die", "cry"}
    soft_words = {"night", "dream", "sleep", "soft", "ghost", "quiet", "home", "alone", "slow", "blue", "old", "fade"}
    hi = " ".join(item.get("lyric_excerpt", "") for item in high_energy).lower()
    ht = " ".join(item.get("lyric_excerpt", "") for item in high_tension).lower()
    lo = " ".join(item.get("lyric_excerpt", "") for item in low_energy).lower()
    hi_intense = sum(word in hi for word in intense_words) + sum(word in ht for word in intense_words)
    lo_soft = sum(word in lo for word in soft_words)
    if hi_intense > 0 and lo_soft > 0:
        return "Strong alignment: higher-energy and higher-tension windows carry more forceful language, while the softer valleys lean inward."
    if hi_intense == 0 and lo_soft == 0:
        return "Mixed alignment: the arrangement is carrying more of the emotion than the literal language."
    return "Partial alignment: there is some relationship between lyric content and the track's energy/tension contour, but it is nuanced rather than literal."


def synthesize_report(quick: dict[str, Any], temporal: dict[str, Any], lyrics: dict[str, Any]) -> dict[str, Any]:
    lyric_vibe = analyze_lyric_vibe(lyrics)
    integrated_emotion = combine_emotional_read(quick["emotion"], lyric_vibe)
    aligned_timeline = attach_lyrics_to_timeline(temporal, lyrics)
    peaks = top_windows(aligned_timeline, "energy")
    quiets = top_windows(aligned_timeline, "energy", reverse=False)
    tensions = top_windows(aligned_timeline, "tension")
    transitions = [m for m in aligned_timeline if "transition" in m]

    def pack(items, key_name=None):
        out = []
        for item in items:
            row = {
                "time": item["time_fmt"],
                "mood": item["mood"],
                "lyrics": item.get("lyric_excerpt", "(instrumental / no lyric overlap)"),
            }
            if key_name:
                row[key_name] = item.get(key_name)
            out.append(row)
        return out

    return {
        "aligned_timeline": aligned_timeline,
        "peak_lyric_moments": pack(peaks, "energy"),
        "quiet_lyric_moments": pack(quiets, "energy"),
        "tension_lyric_moments": pack(tensions, "tension"),
        "transition_lyric_moments": [
            {
                "time": item["time_fmt"],
                "transition": item["transition"],
                "mood": item["mood"],
                "lyrics": item.get("lyric_excerpt", "(instrumental / no lyric overlap)"),
            }
            for item in transitions[:8]
        ],
        "lyric_energy_alignment": summarize_alignment(peaks, tensions, quiets),
        "lyric_vibe": lyric_vibe,
        "integrated_emotion": integrated_emotion,
        "overview": {
            "tempo_bpm": quick["groove"]["tempo_bpm"],
            "key_estimate": quick["harmony"]["key_estimate"],
            "arc_shape": temporal.get("narrative", {}).get("arc_shape"),
            "mood_journey": temporal.get("narrative", {}).get("mood_journey"),
            "lyrics_available": bool(lyrics.get("segments")),
            "pulse": quick["groove"]["pocket"],
            "structure": quick["structure"]["structure_summary"],
            "emotion_overview": integrated_emotion["overview"],
            "final_mood": integrated_emotion["final_mood"],
            "primary_driver": integrated_emotion["primary_driver"],
        },
    }


def render_text(report: dict[str, Any]) -> str:
    meta = report["meta"]
    quick = report["quick_analysis"]
    temporal = report["temporal_listen"]
    lyrics = report["lyrics"]
    synthesis = report["synthesis"]
    narrative = temporal["narrative"]

    lines = []
    lines.append(f"🎧 FULL LISTEN: {Path(report['file']).name}")
    lines.append(f"   {format_ts(meta['duration_sec'])} | {quick['groove']['tempo_bpm']} BPM | key ≈ {quick['harmony']['key_estimate']} | {narrative.get('arc_shape', '?')} arc")
    lines.append("")
    lines.append("SNAPSHOT")
    lines.append(f"- Groove: {quick['groove']['pocket']} | pulse stability {quick['groove']['pulse_stability']} | swing proxy {quick['groove']['swing_proxy']}")
    lines.append(f"- Structure: {quick['structure']['structure_summary']}" + (f" | repeats: {', '.join(quick['structure']['repeated_sections'])}" if quick['structure']['repeated_sections'] else ""))
    lines.append(f"- Harmony: {quick['harmony']['key_estimate']} | key clarity {quick['harmony']['key_clarity']} | {quick['harmony']['tension_description']}")
    lines.append(f"- Timbre: {', '.join(quick['timbre']['descriptor_tags'])} | centroid {quick['timbre']['centroid_mean']} | dynamic range {quick['timbre']['dynamic_range']}")
    # Instrument palette — natural language, not a data dump
    instruments = report.get("instruments", {})
    instrument_narrative = instruments.get("narrative", "")
    if instrument_narrative:
        lines.append("")
        lines.append("INSTRUMENT READ")
        lines.append(f"- {instrument_narrative}")

    lines.append("")
    lines.append("TEMPORAL JOURNEY")
    lines.append(f"- Opening {narrative['opening']['mood']} → Middle {narrative['middle']['mood']} → Closing {narrative['closing']['mood']}")
    lines.append(f"- Peak: {narrative['peak']['time']} ({narrative['peak']['mood']}, energy {narrative['peak']['energy']})")
    lines.append(f"- Quietest: {narrative['quietest']['time']} ({narrative['quietest']['mood']}, energy {narrative['quietest']['energy']})")
    lines.append(f"- Tensest: {narrative['tensest']['time']} ({narrative['tensest']['mood']}, tension {narrative['tensest']['tension']})")
    lines.append(f"- Mood journey: {narrative['mood_journey']}")
    lines.append(f"- Transitions detected: {narrative['transitions']}")
    lines.append("")
    lines.append("EMOTIONAL READ")
    lines.append(f"- Final vibe: {synthesis['integrated_emotion']['final_mood']} ({synthesis['integrated_emotion']['primary_driver']}-led)")
    lines.append(f"- {synthesis['integrated_emotion']['overview']}")
    lines.append("- Audio layer:")
    lines.append(f"  • {quick['emotion']['overview']}")
    for reason in quick['emotion']['reasons']:
        lines.append(f"  • {reason}")
    lines.append("")
    lines.append("LYRICS")
    if lyrics.get("segments"):
        lines.append(f"- Whisper segments: {lyrics.get('segment_count', len(lyrics['segments']))}")
        lines.append(f"- Lyric mood: {synthesis['lyric_vibe']['mood']} | confidence {synthesis['lyric_vibe']['confidence']} | dominance {synthesis['lyric_vibe']['dominance']}")
        lines.append(f"- {synthesis['lyric_vibe']['overview']}")
        lines.append(f"- Excerpt: {lyrics['full_text'][:240]}" + ("..." if len(lyrics['full_text']) > 240 else ""))
    else:
        lines.append(f"- {lyrics.get('notes', ['Lyrics unavailable.'])[0]}")
    lines.append("")
    lines.append("SYNTHESIS")
    lines.append(f"- Lyric/energy read: {synthesis['lyric_energy_alignment']}")
    lines.append("- Peak lyric moments:")
    for item in synthesis["peak_lyric_moments"]:
        lines.append(f"  • {item['time']} | {item['mood']} | {item['lyrics']}")
    lines.append("- Tension lyric moments:")
    for item in synthesis["tension_lyric_moments"]:
        lines.append(f"  • {item['time']} | {item['mood']} | {item['lyrics']}")
    lines.append("- Quiet/ethereal lyric moments:")
    for item in synthesis["quiet_lyric_moments"]:
        lines.append(f"  • {item['time']} | {item['mood']} | {item['lyrics']}")
    if synthesis["transition_lyric_moments"]:
        lines.append("- Transition lyric moments:")
        for item in synthesis["transition_lyric_moments"]:
            lines.append(f"  • {item['time']} | {item['transition']} into {item['mood']} | {item['lyrics']}")
    lines.append("")
    lines.append("ALIGNED TIMELINE")
    for moment in synthesis["aligned_timeline"]:
        if "transition" in moment or moment.get("lyric_excerpt") or moment.get("tension", 0) > 0.55:
            marker = f" | {moment['transition']}" if "transition" in moment else ""
            lyric = f" | \"{moment['lyric_excerpt']}\"" if moment.get("lyric_excerpt") else ""
            lines.append(f"- {moment['time_fmt']} | {moment['mood']} | energy {moment['energy']} | tension {moment['tension']}{marker}{lyric}")
    return "\n".join(lines)


def build_report(audio_path: Path) -> dict[str, Any]:
    meta = ffprobe_meta(audio_path)
    quick = to_native(analyze_with_librosa(audio_path))
    temporal = to_native(analyze_temporal(str(audio_path)))
    lyrics = transcribe_lyrics(audio_path)

    # Instrument detection — uses structure sections for per-section analysis
    sections = quick.get("structure", {}).get("sections", [])
    instruments = to_native(analyze_instruments(audio_path, sections))

    synthesis = synthesize_report(quick, temporal, lyrics)
    return {
        "file": str(audio_path),
        "meta": meta,
        "quick_analysis": quick,
        "temporal_listen": temporal,
        "instruments": instruments,
        "lyrics": lyrics,
        "synthesis": synthesis,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Unified full-track listener with lyric alignment")
    ap.add_argument("audio")
    ap.add_argument("--json", action="store_true", help="Emit structured JSON instead of human-readable text")
    ap.add_argument("--out", help="Write output to file")
    args = ap.parse_args()

    audio_path = Path(args.audio).expanduser()
    if not audio_path.exists():
        raise SystemExit(f"audio not found: {audio_path}")

    report = build_report(audio_path)
    output = json.dumps(to_native(report), indent=2) if args.json else render_text(report)

    if args.out:
        Path(args.out).write_text(output)
    print(output)


if __name__ == "__main__":
    main()
