"""
Transcribes reel audio and summarizes the transcript with OpenRouter (Nvidia Nemotron).
"""

from openai import OpenAI

import config
import transcriber

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=config.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )
    return _client


def _summarize_transcript(transcript: str, caption: str = "") -> str:
    client = _get_client()
    text = (
        "Here is a transcript from an Instagram reel. "
        "Summarize it in exactly 5 bullet points. Each bullet should capture a key point. "
        "Be concise.\n\n"
        f"Transcript:\n{transcript}"
        + (f"\n\nCaption: {caption}" if caption else "")
    )
    response = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        max_tokens=512,
        messages=[{"role": "user", "content": text}],
    )
    return response.choices[0].message.content


def analyze_all(results: dict) -> dict:
    """
    For each account, transcribe and summarize every reel in-place,
    adding 'transcript' and 'transcript_summary' keys to each item.
    Returns the same dict (mutated).
    """
    for username, data in results.items():
        print(f"\nProcessing @{username} …")

        for reel in data["reels"]:
            print(f"  -> reel {reel['shortcode']} — transcribing…")
            transcript = transcriber.transcribe_reel(reel["url"])
            reel["transcript"] = transcript
            reel["transcript_summary"] = _summarize_transcript(transcript, reel.get("caption", ""))

    return results
