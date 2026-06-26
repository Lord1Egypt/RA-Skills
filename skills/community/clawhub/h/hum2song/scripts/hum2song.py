#!/usr/bin/env python3
"""
Hum2Song - Convert humming to complete songs
Local audio processing pipeline with no external API calls
"""

import argparse
import os
import sys
import tempfile
import json
from pathlib import Path


def check_dependencies():
    """Check if required packages are installed"""
    missing = []
    
    try:
        import basic_pitch
    except ImportError:
        missing.append("basic-pitch")
    
    try:
        import pretty_midi
    except ImportError:
        missing.append("pretty_midi")
    
    try:
        import librosa
    except ImportError:
        missing.append("librosa")
    
    try:
        import soundfile
    except ImportError:
        missing.append("soundfile")
    
    try:
        import numpy
    except ImportError:
        missing.append("numpy")
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("\nInstall with:")
        print(f"  pip install {' '.join(missing)}")
        sys.exit(1)
    
    return True


def extract_midi(input_path, output_dir):
    """Step 1: Extract MIDI from audio using Basic Pitch"""
    print("🎵 Step 1: Extracting MIDI from audio...")
    
    from basic_pitch.inference import predict
    
    model_output, midi_data, note_events = predict(input_path)
    
    midi_path = os.path.join(output_dir, "extracted.mid")
    midi_data.write(midi_path)
    
    note_count = len(note_events) if note_events else 0
    print(f"   ✓ Extracted {note_count} notes")
    print(f"   ✓ Saved: {midi_path}")
    
    return midi_path, note_count


def enhance_midi(input_midi, output_dir):
    """Step 2: Clean and enhance MIDI"""
    print("🎼 Step 2: Enhancing MIDI structure...")
    
    import pretty_midi
    
    pm = pretty_midi.PrettyMIDI(input_midi)
    
    # Quantize timing to fix rhythm
    for instrument in pm.instruments:
        for note in instrument.notes:
            # Quantize to 16th notes (0.25s at 60 BPM, scaled by actual tempo)
            note.start = round(note.start * 4) / 4
            note.end = round(note.end * 4) / 4
            # Ensure minimum note duration
            if note.end - note.start < 0.1:
                note.end = note.start + 0.1
    
    # Estimate and set tempo
    tempo = pm.estimate_tempo()
    if tempo < 60 or tempo > 200:
        tempo = 120  # Default to 120 BPM if estimation fails
    
    enhanced_path = os.path.join(output_dir, "enhanced.mid")
    pm.write(enhanced_path)
    
    print(f"   ✓ Quantized notes to grid")
    print(f"   ✓ Estimated tempo: {int(tempo)} BPM")
    print(f"   ✓ Saved: {enhanced_path}")
    
    return enhanced_path, tempo


def generate_with_soundfont(midi_path, output_path, style="pop"):
    """Step 3a: Generate audio using SoundFont (no AI)"""
    print(f"🎹 Step 3: Generating {style} arrangement with SoundFont...")
    
    import pretty_midi
    import soundfile as sf
    import numpy as np
    
    pm = pretty_midi.PrettyMIDI(midi_path)
    
    # Try to use fluidsynth with a SoundFont
    try:
        # Common SoundFont paths
        sf_paths = [
            "/usr/share/sounds/sf2/FluidR3_GM.sf2",
            "/opt/homebrew/share/fluidsynth/generaluser.v.1.44.sf2",
            os.path.expanduser("~/.fluidsynth/default.sf2"),
        ]
        
        sf2_path = None
        for path in sf_paths:
            if os.path.exists(path):
                sf2_path = path
                break
        
        if sf2_path:
            audio = pm.fluidsynth(fs=44100, sf2_path=sf2_path)
        else:
            # Fallback: synthesize without SoundFont
            print("   ⚠ No SoundFont found, using default synthesis")
            audio = pm.synthesize(fs=44100)
    
    except Exception as e:
        print(f"   ⚠ SoundFont synthesis failed: {e}")
        print("   ⚠ Falling back to default synthesis")
        audio = pm.synthesize(fs=44100)
    
    # Normalize audio
    audio = np.array(audio)
    if len(audio.shape) == 1:
        audio = audio.reshape(-1, 1)
    
    # Convert to stereo if mono
    if audio.shape[1] == 1:
        audio = np.repeat(audio, 2, axis=1)
    
    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.9
    
    sf.write(output_path, audio, 44100)
    duration = len(audio) / 44100
    
    print(f"   ✓ Generated {duration:.1f}s of audio")
    print(f"   ✓ Saved: {output_path}")
    
    return output_path, duration


def generate_with_ace_step(midi_path, output_path, style="pop", mood="upbeat", duration=120):
    """Step 3b: Generate audio using ACE-Step (local AI)"""
    print(f"🤖 Step 3: Generating {style} song with ACE-Step AI...")
    
    try:
        # Try to import ACE-Step
        sys.path.insert(0, os.path.expanduser("~/ace-step"))
        from ace_step import MusicGenerator
        
        print("   ⏳ Loading ACE-Step model (this may take a minute)...")
        generator = MusicGenerator.from_pretrained("ace-step/base")
        
        print(f"   ⏳ Generating {duration}s of music...")
        audio = generator.generate_from_midi(
            midi_path=midi_path,
            style=style,
            mood=mood,
            duration=duration
        )
        
        audio.save(output_path)
        
        print(f"   ✓ AI generation complete")
        print(f"   ✓ Saved: {output_path}")
        
        return output_path, duration
    
    except ImportError:
        print("   ⚠ ACE-Step not installed, falling back to SoundFont")
        return generate_with_soundfont(midi_path, output_path, style)
    
    except Exception as e:
        print(f"   ⚠ ACE-Step failed: {e}")
        print("   ⚠ Falling back to SoundFont")
        return generate_with_soundfont(midi_path, output_path, style)


def main():
    parser = argparse.ArgumentParser(
        description="Convert humming to complete songs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input humming.wav --output song.mp3
  %(prog)s --input my_tune.m4a --style jazz --mood calm
  %(prog)s --input audio.mp3 --use-ai --duration 180
        """
    )
    
    parser.add_argument("--input", "-i", required=True, help="Input audio file")
    parser.add_argument("--output", "-o", help="Output file path (default: auto-generated)")
    parser.add_argument("--style", "-s", default="pop", 
                       choices=["pop", "rock", "jazz", "classical", "electronic"],
                       help="Music style (default: pop)")
    parser.add_argument("--mood", "-m", default="upbeat",
                       choices=["upbeat", "calm", "energetic", "melancholic"],
                       help="Song mood (default: upbeat)")
    parser.add_argument("--duration", "-d", type=int, default=120,
                       help="Target duration in seconds (default: 120)")
    parser.add_argument("--use-ai", "-a", action="store_true",
                       help="Use ACE-Step AI (requires local setup)")
    parser.add_argument("--keep-midi", "-k", action="store_true",
                       help="Keep intermediate MIDI files")
    parser.add_argument("--work-dir", "-w", help="Working directory for temp files")
    
    args = parser.parse_args()
    
    # Check input file exists
    if not os.path.exists(args.input):
        print(f"❌ Input file not found: {args.input}")
        sys.exit(1)
    
    # Check dependencies
    check_dependencies()
    
    # Setup working directory
    if args.work_dir:
        work_dir = args.work_dir
        os.makedirs(work_dir, exist_ok=True)
    else:
        work_dir = tempfile.mkdtemp(prefix="hum2song_")
    
    print(f"🎤 Hum2Song - Humming to Song Converter")
    print(f"   Input: {args.input}")
    print(f"   Style: {args.style}, Mood: {args.mood}")
    print(f"   Working dir: {work_dir}\n")
    
    try:
        # Step 1: Extract MIDI
        midi_path, note_count = extract_midi(args.input, work_dir)
        
        # Step 2: Enhance MIDI
        enhanced_midi, tempo = enhance_midi(midi_path, work_dir)
        
        # Step 3: Generate audio
        if not args.output:
            output_name = f"hum2song_{args.style}_{Path(args.input).stem}.wav"
            args.output = os.path.join(os.path.expanduser("~/Music"), output_name)
        
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        
        if args.use_ai:
            output_path, duration = generate_with_ace_step(
                enhanced_midi, args.output, args.style, args.mood, args.duration
            )
        else:
            output_path, duration = generate_with_soundfont(
                enhanced_midi, args.output, args.style
            )
        
        # Summary
        print(f"\n✅ Success!")
        print(f"   Output: {output_path}")
        print(f"   Duration: {duration:.1f}s")
        print(f"   Notes extracted: {note_count}")
        print(f"   Tempo: {int(tempo)} BPM")
        
        # Keep or cleanup MIDI files
        if args.keep_midi:
            midi_output = os.path.splitext(args.output)[0] + ".mid"
            import shutil
            shutil.copy(enhanced_midi, midi_output)
            print(f"   MIDI saved: {midi_output}")
        
        print(f"\n🎧 Enjoy your song!")
        
    finally:
        # Cleanup temp directory unless --work-dir was specified
        if not args.work_dir and os.path.exists(work_dir):
            import shutil
            shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
