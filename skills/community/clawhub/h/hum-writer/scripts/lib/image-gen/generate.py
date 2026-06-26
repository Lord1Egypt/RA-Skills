#!/usr/bin/env python3
from __future__ import annotations
"""
generate.py — Multi-provider AI image generation.

Usage:
    python3 generate.py --prompt "your image description"
    python3 generate.py --prompt "..." --provider gemini --platform linkedin
    python3 generate.py --prompt "..." --no-enhance

Providers: gemini (default), grok, minimax, openai
Platforms: twitter, linkedin, instagram, instagram-sq, instagram-st,
           facebook, og, 1:1, 16:9, 9:16, 4:3, 3:4
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


# ── Platform presets ──────────────────────────────────────────────────────────

PLATFORM_SIZES: dict[str, tuple[int, int]] = {
    "twitter":      (1200, 675),
    "linkedin":     (1200, 627),
    "instagram":     (1080, 1080),
    "instagram-sq":  (1080, 1080),
    "instagram-st":  (1080, 1920),
    "facebook":      (1200, 630),
    "og":            (1200, 630),
    "1:1":           (1024, 1024),
    "16:9":          (1920, 1080),
    "9:16":          (1080, 1920),
    "4:3":           (1024, 768),
    "3:4":           (768, 1024),
}


# ── Provider loader ───────────────────────────────────────────────────────────

def load_providers() -> dict:
    """Load providers from sibling providers module."""
    from importlib.machinery import SourceFileLoader

    providers_file = Path(__file__).parent / "providers.py"
    loader = SourceFileLoader("providers", str(providers_file))
    providers = loader.load_module()

    return {
        "gemini": providers.GeminiProvider,
        "grok": providers.GrokProvider,
        "minimax": providers.MiniMaxProvider,
        "openai": providers.OpenAIProvider,
    }


# ── Prompt enhancement via LLM ────────────────────────────────────────────────

def enhance_prompt(prompt: str) -> str:
    """
    Use the configured LLM to expand a short/vague prompt into a detailed,
    specific image generation prompt suitable for AI image models.
    """
    # Try to find an API key
    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("IMAGE_ENHANCE_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[image-gen] No LLM API key for enhancement — using original prompt", file=sys.stderr)
        return prompt

    try:
        system_prompt = (
            "You are an expert image prompt engineer. The user gives you a rough idea "
            "for an image. Expand it into a vivid, specific, detailed image generation prompt "
            "suitable for an AI image model. Include: subject, setting, lighting, style, mood, "
            "colors, composition, and any text that should appear. "
            "Do NOT add marketing speak or commentary — only output the enhanced prompt. "
            "Keep it under 500 characters."
        )

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 400,
            "temperature": 0.7,
        }

        url = f"{base_url.rstrip('/')}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers=headers,
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())

        enhanced = data["choices"][0]["message"]["content"].strip()
        print(f"[image-gen] Enhanced: {enhanced[:200]}", file=sys.stderr)
        return enhanced

    except Exception as exc:
        print(f"[image-gen] Enhancement failed ({exc}) — using original prompt", file=sys.stderr)
        return prompt


# ── Main generation ───────────────────────────────────────────────────────────


def generate_image(
    prompt: str,
    platform: str | None = None,
    output_path: str | None = None,
    *,
    provider: str = "gemini",
    size: str | None = None,
    model: str | None = None,
    style: str | None = None,
    no_enhance: bool = False,
    emit_json: bool = False,
) -> str:
    """Generate an image and return the output path (or base64 if no output_path).

    Args:
        prompt: Image description.
        platform: Target platform preset (e.g. "twitter", "linkedin").
        output_path: Where to save the image. If None and emit_json is False,
            returns base64-encoded image bytes as a string.
        provider: Provider name ("gemini", "grok", "minimax", "openai").
        size: Size string "WxH" — overrides platform.
        model: Provider-specific model override.
        style: Style directive passed to the provider.
        no_enhance: Skip LLM prompt enhancement.
        emit_json: Print JSON result to stdout instead of saving file.

    Returns:
        output_path if saved, or base64 string if no output_path.

    Raises:
        RuntimeError: If provider is unknown, initialization fails, or generation fails.
    """
    # Resolve size
    resolved_size: tuple[int, int] | None = None
    if size:
        w, h = size.lower().split("x")
        resolved_size = (int(w), int(h))
    elif platform:
        resolved_size = PLATFORM_SIZES.get(platform)

    # Enhance prompt
    enhanced = prompt
    if not no_enhance:
        enhanced = enhance_prompt(prompt)

    # Instantiate provider
    providers = load_providers()
    cls = providers.get(provider)
    if not cls:
        raise RuntimeError(
            f"[image-gen] Unknown provider: {provider}. "
            f"Available: {', '.join(providers.keys())}"
        )

    try:
        prov_instance = cls()
    except Exception as exc:
        raise RuntimeError(f"[image-gen] Failed to initialize {provider}: {exc}") from exc

    print(f"[image-gen] Generating with {provider} (size={resolved_size or 'default'})...", file=sys.stderr)

    try:
        result = prov_instance.generate(
            prompt=enhanced,
            size=resolved_size,
            model=model,
            style=style,
        )
    except Exception as exc:
        raise RuntimeError(f"[image-gen] Generation failed: {exc}") from exc

    if emit_json:
        output = {
            "success": True,
            "provider": result.provider,
            "model": result.model,
            "size": resolved_size,
            "prompt": prompt,
            "enhanced_prompt": enhanced if not no_enhance else None,
            "revised_prompt": result.revised_prompt,
            "image_b64": base64.b64encode(result.image_bytes).decode(),
            "mime_type": result.mime_type,
        }
        print(json.dumps(output, indent=2))
        return ""

    if output_path:
        Path(output_path).write_bytes(result.image_bytes)
        print(f"[image-gen] Saved: {output_path} ({len(result.image_bytes):,} bytes)", file=sys.stderr)
        return output_path

    return base64.b64encode(result.image_bytes).decode()


def main():
    parser = argparse.ArgumentParser(description="AI image generation — multi-provider")
    parser.add_argument("--prompt", "-p", required=True, help="Image description")
    parser.add_argument(
        "--provider", default="gemini",
        choices=["gemini", "grok", "minimax", "openai"],
        help="Provider (default: gemini)",
    )
    parser.add_argument(
        "--platform", "-P",
        choices=list(PLATFORM_SIZES.keys()),
        help="Target platform preset",
    )
    parser.add_argument(
        "--size", "-s",
        help="Image size WxH (e.g. 1024x1024). Overrides --platform.",
    )
    parser.add_argument("--model", "-m", help="Model override (provider-specific)")
    parser.add_argument("--style", help="Style directive (passed to provider if supported)")
    parser.add_argument(
        "--no-enhance", action="store_true",
        help="Skip LLM prompt enhancement",
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path. If omitted, prints base64 to stdout.",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Machine-readable JSON output",
    )
    args = parser.parse_args()

    try:
        result = generate_image(
            prompt=args.prompt,
            platform=args.platform,
            output_path=args.output,
            provider=args.provider,
            size=args.size,
            model=args.model,
            style=args.style,
            no_enhance=args.no_enhance,
            emit_json=args.json,
        )
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

    if result and not args.json and not args.output:
        sys.stdout.write(result)
    elif result and args.output:
        print(result)


if __name__ == "__main__":
    main()
