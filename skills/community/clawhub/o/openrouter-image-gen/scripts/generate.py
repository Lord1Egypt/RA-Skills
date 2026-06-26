#!/usr/bin/env python3
"""
Gemini Image Generation via OpenRouter API.
Supports text-to-image and image-guided generation (with reference image).

Usage:
  python3 generate.py "a cute cat in watercolor style" -o cat.png
  python3 generate.py "draw this character smiling" -o smile.png --ref reference.png
  python3 generate.py "redesign this logo" -o logo.png --ref old_logo.jpg --size 1024

Environment:
  OPENROUTER_API_KEY  — required (or pass --api-key)
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.request
import urllib.error


def encode_image(path: str) -> dict:
    """Read an image file and return an OpenAI-style image_url content part."""
    mime, _ = mimetypes.guess_type(path)
    if mime is None:
        mime = "image/png"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return {
        "type": "image_url",
        "image_url": {"url": f"data:{mime};base64,{b64}"},
    }


def generate(
    prompt: str,
    output: str,
    ref_image: str | None = None,
    model: str = "google/gemini-3.1-flash-image-preview",
    api_key: str | None = None,
    base_url: str = "https://openrouter.ai/api/v1",
) -> str:
    """Generate an image and save to *output*. Returns the output path."""

    api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        sys.exit("Error: OPENROUTER_API_KEY not set and --api-key not provided.")

    # Build message content
    content: list[dict] = []
    if ref_image:
        content.append(encode_image(ref_image))
    content.append({"type": "text", "text": prompt})

    payload = {
        "model": model,
        "modalities": ["text", "image"],
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 4096,
    }

    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        sys.exit(f"API error {e.code}: {body}")

    # Extract image from response
    choice = result.get("choices", [{}])[0]
    message = choice.get("message", {})

    # Try images array first (OpenRouter Gemini format)
    images = message.get("images", [])
    if images:
        data_url = images[0].get("image_url", {}).get("url", "")
    else:
        # Fallback: scan content parts
        data_url = ""
        for part in message.get("content", []) if isinstance(message.get("content"), list) else []:
            if part.get("type") == "image_url":
                data_url = part.get("image_url", {}).get("url", "")
                break

    if not data_url:
        # Dump response for debugging
        debug_path = output + ".debug.json"
        with open(debug_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        sys.exit(f"No image in response. Debug saved to {debug_path}")

    # Decode base64
    if "," in data_url:
        b64_data = data_url.split(",", 1)[1]
    else:
        b64_data = data_url

    img_bytes = base64.b64decode(b64_data)
    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    with open(output, "wb") as f:
        f.write(img_bytes)

    # Print text response if any
    text = message.get("content") if isinstance(message.get("content"), str) else ""
    if not text:
        for part in message.get("content", []) if isinstance(message.get("content"), list) else []:
            if part.get("type") == "text":
                text = part.get("text", "")
                break

    size_kb = len(img_bytes) / 1024
    print(f"✅ Saved: {output} ({size_kb:.0f} KB)")
    if text:
        print(f"📝 Model response: {text[:200]}")

    # Print usage if available
    usage = result.get("usage", {})
    if usage:
        print(f"📊 Tokens: {usage.get('prompt_tokens', '?')} in / {usage.get('completion_tokens', '?')} out")

    return output


def main():
    parser = argparse.ArgumentParser(description="Generate images via Gemini on OpenRouter")
    parser.add_argument("prompt", help="Text prompt for image generation")
    parser.add_argument("-o", "--output", default="generated.png", help="Output file path (default: generated.png)")
    parser.add_argument("--ref", help="Reference image path (for style/character guidance)")
    parser.add_argument("--model", default="google/gemini-3.1-flash-image-preview", help="Model ID")
    parser.add_argument("--api-key", help="OpenRouter API key (or set OPENROUTER_API_KEY)")
    args = parser.parse_args()

    generate(
        prompt=args.prompt,
        output=args.output,
        ref_image=args.ref,
        model=args.model,
        api_key=args.api_key,
    )


if __name__ == "__main__":
    main()
