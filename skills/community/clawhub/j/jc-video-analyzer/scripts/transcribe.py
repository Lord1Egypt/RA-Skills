"""faster-whisper 转写脚本

用法：
    python transcribe.py <audio.wav> <output.txt> [model] [language]

示例：
    python transcribe.py audio_16k.wav transcript.txt tiny zh
"""

import sys
import time
from faster_whisper import WhisperModel


def transcribe(audio_path: str, output_path: str, model_name: str = "tiny", language: str = "zh"):
    print(f"Loading model '{model_name}'...")
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    
    print(f"Transcribing: {audio_path}")
    start = time.time()

    segments, info = model.transcribe(
        audio_path,
        language=language,
        beam_size=5,
        vad_filter=True
    )

    text_parts = []
    for seg in segments:
        text_parts.append(f"[{seg.start:.1f}s - {seg.end:.1f}s] {seg.text.strip()}")

    full_text = "\n".join(text_parts)
    elapsed = time.time() - start

    print(f"Completed in {elapsed:.1f}s")
    print(f"  Segments: {len(text_parts)}")
    print(f"  Characters: {len(full_text)}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"Saved to: {output_path}")
    return full_text


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    audio_path = sys.argv[1]
    output_path = sys.argv[2]
    model_name = sys.argv[3] if len(sys.argv) > 3 else "tiny"
    language = sys.argv[4] if len(sys.argv) > 4 else "zh"

    transcribe(audio_path, output_path, model_name, language)
