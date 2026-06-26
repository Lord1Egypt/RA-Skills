#!/usr/bin/env python3
"""Generate whiteboard-style slide images using Gemini API.

Usage:
  python3 generate_slide_images.py --prompts-file prompts.json --output-dir ./images --api-key KEY
  python3 generate_slide_images.py --prompts-file prompts.json --output-dir ./images  # uses GEMINI_API_KEY env

prompts.json format:
[
  {"name": "01-slide-name", "prompt": "Draw a whiteboard diagram showing..."},
  {"name": "02-slide-name", "prompt": "..."}
]
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request

DEFAULT_MODEL = "gemini-3-pro-image-preview"
FALLBACK_MODEL = "imagen-4.0-generate-001"


def generate_with_gemini3(prompt: str, api_key: str, model: str = DEFAULT_MODEL) -> tuple[bytes, str] | None:
    """Generate image using Gemini 3 Pro Image (generateContent with IMAGE modality)."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": f"Generate this image: {prompt}"}]}],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]},
    }).encode()

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
    except (urllib.error.URLError, ConnectionError, OSError) as e:
        print(f"    Network error: {e}")
        return None

    if "error" in data:
        print(f"    API error: {data['error'].get('message', 'unknown')}")
        return None

    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    for p in parts:
        if "inlineData" in p:
            mime = p["inlineData"]["mimeType"]
            ext = "jpg" if "jpeg" in mime else mime.split("/")[-1]
            return base64.b64decode(p["inlineData"]["data"]), ext
    return None


def generate_with_imagen(prompt: str, api_key: str, model: str = FALLBACK_MODEL) -> tuple[bytes, str] | None:
    """Generate image using Imagen 4.0 (predict endpoint)."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:predict?key={api_key}"
    payload = json.dumps({
        "instances": [{"prompt": prompt}],
        "parameters": {"sampleCount": 1, "aspectRatio": "16:9"},
    }).encode()

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
    except (urllib.error.URLError, ConnectionError, OSError) as e:
        print(f"    Network error: {e}")
        return None

    if "error" in data:
        print(f"    API error: {data['error'].get('message', 'unknown')}")
        return None

    predictions = data.get("predictions", [])
    if predictions and "bytesBase64Encoded" in predictions[0]:
        return base64.b64decode(predictions[0]["bytesBase64Encoded"]), "png"
    return None


def main():
    parser = argparse.ArgumentParser(description="Generate slide images via Gemini API")
    parser.add_argument("--prompts-file", required=True, help="JSON file with slide prompts")
    parser.add_argument("--output-dir", required=True, help="Output directory for images")
    parser.add_argument("--api-key", default=os.environ.get("GEMINI_API_KEY", ""), help="Gemini API key")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between requests in seconds")
    parser.add_argument("--retries", type=int, default=2, help="Number of retries on failure")
    args = parser.parse_args()

    if not args.api_key:
        print("Error: No API key provided. Use --api-key or set GEMINI_API_KEY env var.")
        sys.exit(1)

    with open(args.prompts_file) as f:
        slides = json.load(f)

    os.makedirs(args.output_dir, exist_ok=True)

    total = len(slides)
    ok = 0
    failed = []

    use_gemini3 = "gemini-3" in args.model or "gemini-2" in args.model
    generate_fn = generate_with_gemini3 if use_gemini3 else generate_with_imagen

    for i, slide in enumerate(slides):
        name = slide["name"]
        prompt = slide["prompt"]
        print(f"[{i + 1}/{total}] {name}...")

        result = None
        for attempt in range(1, args.retries + 1):
            result = generate_fn(prompt, args.api_key, args.model)
            if result:
                break
            if attempt < args.retries:
                wait = args.delay * attempt * 2
                print(f"    Retry {attempt}/{args.retries} in {wait}s...")
                time.sleep(wait)

        if result:
            img_data, ext = result
            outpath = os.path.join(args.output_dir, f"{name}.{ext}")
            with open(outpath, "wb") as f:
                f.write(img_data)
            print(f"    ✅ Saved: {outpath}")
            ok += 1
        else:
            print(f"    ❌ Failed after {args.retries} attempts")
            failed.append(name)

        if i < total - 1:
            time.sleep(args.delay)

    print(f"\nDone: {ok}/{total} images generated")
    if failed:
        print(f"Failed: {', '.join(failed)}")
    print(f"Output: {args.output_dir}")
    sys.exit(0 if ok == total else 1)


if __name__ == "__main__":
    main()
