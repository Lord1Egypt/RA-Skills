#!/usr/bin/env python3
"""Audio transcription module using OpenAI Whisper API."""

import os
import io
from openai import OpenAI, APIError
from pydub import AudioSegment

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def transcribe_audio(file_path: str, chunk_size_mins: int = 10) -> str:
    """Transcribe audio file using OpenAI Whisper API.

    Handles large files by splitting into chunks.
    Supports: mp3, mp4, mpeg, mpga, m4a, wav, webm (max 25MB per chunk).
    """
    try:
        audio = AudioSegment.from_file(file_path)
        chunk_size_ms = chunk_size_mins * 60 * 1000
        chunks = [audio[i:i + chunk_size_ms] for i in range(0, len(audio), chunk_size_ms)]

        full_transcript = ""

        for i, chunk in enumerate(chunks):
            buffer = io.BytesIO()
            buffer.name = f"chunk_{i}.mp3"
            chunk.export(buffer, format="mp3")
            buffer.seek(0)

            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=buffer,
                response_format="text",
            )
            full_transcript += transcript + "\n"

            print(f"Processed chunk {i + 1}/{len(chunks)}")

        return full_transcript.strip()

    except (APIError, OSError) as e:
        raise RuntimeError(f"Transcription failed: {e}") from e

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <audio_file_path>")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    transcript = transcribe_audio(audio_path)
    
    output_dir = "/workspace/generated"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{os.path.basename(audio_path)}.txt")
    with open(output_path, "w") as f:
        f.write(transcript)
    
    print(f"Transcription saved to {output_path}")
    print("\nTranscript:")
    print(transcript)