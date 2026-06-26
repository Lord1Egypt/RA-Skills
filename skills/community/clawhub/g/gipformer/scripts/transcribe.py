#!/usr/bin/env python3
"""
Gipformer ASR Client - Transcribe audio files via the serving API.

The server handles chunking and text merging internally.
Just send the audio file and get the full transcript back.

Usage:
    python transcribe.py audio.wav
    python transcribe.py audio.mp3 --server http://localhost:8910
    python transcribe.py *.wav --output results.json
"""

import argparse
import base64
import json
import os
import sys
import time

try:
    import requests
except ImportError:
    print("Error: requests not installed. Run: pip install requests")
    sys.exit(1)

DEFAULT_SERVER = "http://127.0.0.1:8910"


def check_server(server_url: str) -> bool:
    try:
        resp = requests.get(f"{server_url}/health", timeout=5)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def transcribe_file(file_path: str, server_url: str = DEFAULT_SERVER) -> dict:
    """Transcribe an audio file via the gipformer server."""
    t0 = time.time()

    with open(file_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode("ascii")

    resp = requests.post(
        f"{server_url}/transcribe",
        json={"audio_b64": audio_b64},
        timeout=600,
    )

    if resp.status_code != 200:
        raise RuntimeError(f"Server error {resp.status_code}: {resp.text}")

    data = resp.json()
    data["file"] = file_path
    data["client_time_s"] = round(time.time() - t0, 3)
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio files via Gipformer ASR server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python transcribe.py audio.wav\n"
            "  python transcribe.py recording.mp3\n"
            "  python transcribe.py *.wav --output results.json\n"
        ),
    )
    parser.add_argument("files", nargs="+", help="Audio file(s) to transcribe")
    parser.add_argument(
        "--server", default=DEFAULT_SERVER,
        help=f"Server URL (default: {DEFAULT_SERVER})",
    )
    parser.add_argument("--output", "-o", help="Write JSON results to file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if not check_server(args.server):
        print(f"Error: cannot reach gipformer server at {args.server}")
        print("Start the server first: python serve.py")
        sys.exit(1)

    results = []

    for file_path in args.files:
        if not os.path.exists(file_path):
            print(f"Warning: file not found: {file_path}", file=sys.stderr)
            continue

        try:
            result = transcribe_file(file_path, server_url=args.server)
            results.append(result)

            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                n_chunks = len(result.get("chunks", []))
                print(f"\n  File: {result['file']}")
                print(f"  Text: {result['transcript']}")
                print(
                    f"  Audio: {result['duration_s']:.2f}s | "
                    f"Process: {result['process_time_s']:.2f}s | "
                    f"Chunks: {n_chunks}"
                )
                if n_chunks > 1:
                    for c in result["chunks"]:
                        print(f"    {c['start_s']:7.2f}s - {c['end_s']:7.2f}s: {c['text']}")

        except Exception as e:
            print(f"Error transcribing {file_path}: {e}", file=sys.stderr)
            results.append({"file": file_path, "error": str(e)})

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\nResults written to {args.output}")


if __name__ == "__main__":
    main()
