#!/usr/bin/env python3
"""analysis_orchestrator.py — Single entry point for analyzing local audio.

Takes one or two local audio file paths and runs the right analysis
scripts:
- Single audio → analyze_vocal_emotion.py + analyze_audio.py + (optional) extract_lyrics_whisper.py
- Two audios → analyze_two_songs.py + vocal emotion on Song A

Whisper is the only lyrics source. URL downloads (YouTube, JioSaavn,
mx3.ch), image analysis, and video feature extraction have all moved
out of this orchestrator. Use the music-source-fetch skill to acquire
audio and pass the local file path via --audio.

Output: a unified JSON containing all the analyses, ready for
emotion_to_prompt.py or direct use by the LLM.

Usage:
    # Single audio (with lyrics)
    python3 analysis_orchestrator.py --audio /tmp/song.wav --lyrics --output /tmp/analysis.json

    # Two audios (mashup)
    python3 analysis_orchestrator.py --audio /tmp/a.wav --audio /tmp/b.wav \\
        --name-a "Song A" --name-b "Song B" --output /tmp/analysis.json
"""
import sys
import os
import json
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from _key_compat import mashup_compatibility


def _lazy_import_analyze_audio():
    from analyze_audio import analyze as _analyze
    return _analyze


def _lazy_import_analyze_song():
    from analyze_two_songs import analyze_song as _analyze_song
    return _analyze_song


def _run_vocal_emotion(audio_path, use_demucs=False):
    """Run vocal emotion analysis via direct function call (no stdout capture).

    If use_demucs is True, runs Demucs source separation first to extract a
    clean vocal stem, then analyzes the stem. This dramatically improves
    pitch tracking, HNR, and silence detection on busy mixes.

    Returns the analysis dict, or {'error': '...'} on failure.
    """
    target_path = audio_path
    demucs_info = None
    if use_demucs:
        try:
            from extract_stems import separate_stems
            print("Running Demucs source separation (--use-demucs)...", file=sys.stderr)
            demucs_result = separate_stems(
                audio_path=audio_path,
                model_name='htdemucs',
                target_stems=['vocals'],
            )
            if 'error' not in demucs_result and 'stems' in demucs_result:
                vocals_path = demucs_result['stems'].get('vocals')
                if vocals_path and os.path.exists(vocals_path):
                    target_path = vocals_path
                    demucs_info = demucs_result
        except Exception as e:
            print(f"Demucs failed, falling back to mix: {e}", file=sys.stderr)

    try:
        from analyze_vocal_emotion import analyze_audio
        import argparse as _ap
        args = _ap.Namespace(
            audio=target_path,
            sections=None,
            output=None,
            hop_length=512,
        )
        result = analyze_audio(args)
        if demucs_info and isinstance(result, dict):
            result['_demucs'] = {
                'model': demucs_info.get('model'),
                'vocals_stem': demucs_info.get('stems', {}).get('vocals'),
                'cache': demucs_info.get('cache'),
            }
        return result
    except SystemExit:
        return {'error': 'vocal emotion analysis exited via SystemExit'}
    except Exception as e:
        return {'error': f'vocal emotion analysis failed: {e}'}


def _run_lyrics_extraction(audio_path, model='base'):
    """Run Whisper lyrics extraction. Returns dict, or {'note': '...'} on missing dep."""
    try:
        from extract_lyrics_whisper import transcribe
        return transcribe(audio_path, model_name=model)
    except Exception as e:
        return {'error': f'lyrics extraction failed: {e}'}


def _run_beat_tracking(audio_path):
    """Run beat_this beat + downbeat tracking. Returns dict."""
    try:
        from track_beats import track_beats
        return track_beats(audio_path, device='cpu')
    except Exception as e:
        return {'error': f'beat tracking failed: {e}'}


def _run_melody_extraction(audio_path, max_seconds=300):
    """Run Basic Pitch polyphonic AMT. Returns dict."""
    try:
        from extract_melody import extract_melody
        return extract_melody(audio_path)
    except Exception as e:
        return {'error': f'melody extraction failed: {e}'}


def _run_mert_embedding(audio_path, max_seconds=120, allow_remote_model_code=False):
    """Run MERT music embedding. Returns dict."""
    try:
        from compute_audio_embedding import compute_mert_embedding
        return compute_mert_embedding(
            audio_path,
            device='cpu',
            max_seconds=max_seconds,
            allow_remote_code=allow_remote_model_code,
        )
    except Exception as e:
        return {'error': f'MERT embedding failed: {e}'}


def _run_ast_classification(audio_path, top_k=15):
    """Run AST instrument classification. Returns dict."""
    try:
        from classify_instruments import classify_instruments
        return classify_instruments(audio_path, top_k=top_k, device='cpu')
    except Exception as e:
        return {'error': f'AST classification failed: {e}'}


def analyze_audio_file(audio_path, run_emotion=True, run_lyrics=False, lyrics_model='medium',
                       use_demucs=False, run_advanced=True,
                       allow_remote_model_code=False):
    """Run all audio analyses and return a combined result.

    If run_advanced is True (default), also runs beat_this, Basic Pitch,
    MERT, and AST classification. Each is best-effort — failure is captured
    in the result dict, not raised.

    When run_lyrics is True, Whisper (on the local file) is the only
    lyrics source.
    """
    result = {
        'audio_file': audio_path,
        'basic_features': None,
        'vocal_emotion': None,
        'lyrics': None,
        'beats': None,
        'melody': None,
        'mert_embedding': None,
        'ast_classification': None,
    }
    try:
        run_analyze_audio = _lazy_import_analyze_audio()
        result['basic_features'] = run_analyze_audio(audio_path)
    except Exception as e:
        result['basic_features'] = {'error': str(e)}

    if run_emotion:
        result['vocal_emotion'] = _run_vocal_emotion(audio_path, use_demucs=use_demucs)

    if run_lyrics:
        result['lyrics'] = _run_lyrics_extraction(audio_path, model=lyrics_model)

    if run_advanced:
        result['beats'] = _run_beat_tracking(audio_path)
        result['melody'] = _run_melody_extraction(audio_path)
        result['mert_embedding'] = _run_mert_embedding(
            audio_path,
            allow_remote_model_code=allow_remote_model_code,
        )
        result['ast_classification'] = _run_ast_classification(audio_path)

    return result


def orchestrate(audios=(), name_a=None, name_b=None,
                run_lyrics=False, lyrics_model='medium', use_demucs=False,
                run_advanced=True,
                allow_remote_model_code=False):
    """Run all the requested analyses on the local audio files and return a unified result.

    audios is a tuple of one or two local file paths. With two paths the
    two-song mashup path runs (analyze_two_songs + vocal emotion on
    Song A); with one path the single-audio path runs.

    run_advanced controls beat_this + Basic Pitch + MERT + AST. Default True.
    """
    result = {
        'inputs': {
            'audio_files': list(audios),
            'name_a': name_a,
            'name_b': name_b,
        },
    }

    all_audio_paths = list(audios)

    if len(all_audio_paths) >= 2:
        run_analyze_song = _lazy_import_analyze_song()
        song_a_data = run_analyze_song(all_audio_paths[0], name_a or 'Song A')
        song_b_data = run_analyze_song(all_audio_paths[1], name_b or 'Song B')
        compat = mashup_compatibility(song_a_data, song_b_data)
        mashup_result = {
            'song_a': song_a_data,
            'song_b': song_b_data,
            'compatibility': compat,
        }
        if run_lyrics:
            mashup_result['song_a_lyrics'] = _run_lyrics_extraction(
                all_audio_paths[0], model=lyrics_model
            )
        song_a_emotion = _run_vocal_emotion(all_audio_paths[0], use_demucs=use_demucs)
        if song_a_emotion and not song_a_emotion.get('error'):
            mashup_result['song_a_vocal_emotion'] = song_a_emotion
        result['mashup'] = mashup_result
    elif len(all_audio_paths) == 1:
        result['audio'] = analyze_audio_file(
            all_audio_paths[0],
            run_emotion=True,
            run_lyrics=run_lyrics,
            lyrics_model=lyrics_model,
            use_demucs=use_demucs,
            run_advanced=run_advanced,
            allow_remote_model_code=allow_remote_model_code,
        )
    else:
        result['audio'] = None  # type: ignore[assignment]

    return result


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Analyze local music file(s) and produce a unified analysis')
    parser.add_argument('--audio', action='append', default=[],
                        help='Local audio file path. Pass twice for two-song mashup analysis.')
    parser.add_argument('--name-a', help='Name/label for the first song (content source)')
    parser.add_argument('--name-b', help='Name/label for the second song (style reference)')
    parser.add_argument('--lyrics', action='store_true',
                        help='Run Whisper transcription on the local audio file.')
    parser.add_argument('--lyrics-model', default='medium',
                        help='Whisper model size: tiny, base, small, medium, large-v2.')
    parser.add_argument('--use-demucs', action='store_true',
                        help='Run Demucs source separation before vocal analysis.')
    parser.add_argument('--no-advanced', action='store_true',
                        help='Skip advanced analyses (beat_this, Basic Pitch, MERT, AST).')
    parser.add_argument('--allow-remote-model-code', action='store_true',
                        help='Allow packages that fetch model code from the network.')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    return parser


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()

    if not args.audio:
        parser.error('At least one --audio input is required (local audio file path).')

    if len(args.audio) > 2:
        parser.error(
            f'At most two --audio inputs are supported for mashup analysis; '
            f'got {len(args.audio)}. Split the request or treat extra sources as text-only references.'
        )

    result = orchestrate(
        audios=tuple(args.audio),
        name_a=args.name_a,
        name_b=args.name_b,
        run_lyrics=args.lyrics,
        lyrics_model=args.lyrics_model,
        use_demucs=args.use_demucs,
        run_advanced=not args.no_advanced,
        allow_remote_model_code=args.allow_remote_model_code,
    )

    class _NumpyEncoder(json.JSONEncoder):
        def default(self, o):  # noqa: ARG002 (signature must match JSONEncoder)
            try:
                import numpy as np
                if isinstance(o, (np.integer,)):
                    return int(o)
                if isinstance(o, (np.floating,)):
                    return float(o)
                if isinstance(o, np.ndarray):
                    return o.tolist()
            except ImportError:
                pass
            return super().default(o)

    json_out = json.dumps(result, indent=2, ensure_ascii=False, cls=_NumpyEncoder)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(json_out)
        print(f"Written: {args.output}", file=sys.stderr)
    else:
        print(json_out)


if __name__ == '__main__':
    main()
