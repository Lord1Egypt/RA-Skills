#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "openai"
# ]
# ///

"""
Generate images using Gitee AI Image API.

Usage:
    python perform_image_gen.py --prompt "your image description" [--size 1024*1024] [--negative-prompt "..."] [--api-key KEY]
"""

import argparse
import os
import sys
from openai import OpenAI


def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument, config, or environment."""
    if provided_key:
        return provided_key
    return os.environ.get("GITEEAI_API_KEY")


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Gitee AI Image API"
    )
    parser.add_argument(
        "--model", "-m",
        default="Qwen-Image",
        choices=["Qwen-Image", "Kolors", "GLM-Image", "FLUX.2-dev", "HunyuanDiT-v1.2-Diffusers-Distilled"],
        help="Model to use for image generation"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Image description/prompt"
    )
    parser.add_argument(
        "--size", "-s",
        choices=["256x256", "512x512", "1024x1024", "1024x576", "576x1024", 
                 "1024x768", "768x1024", "1024x640", "640x1024","2048x2048"],
        default="1024x1024",
        help="Output size (default: 1024x1024)"
    )
    parser.add_argument(
        "--negative-prompt", "-n",
        default="低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。",
        help="Negative prompt to avoid unwanted elements"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Gitee AI API key (overrides GITEEAI_API_KEY env var)"
    )
    parser.add_argument("--guidance-scale", type=float, help="Guidance scale to adhere to prompt (overrides model default)")
    parser.add_argument("--num-inference-steps", type=int, help="Number of inference steps (overrides model default)")

    args = parser.parse_args()

    # Get API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set GITEEAI_API_KEY environment variable", file=sys.stderr)
        print("  3. Configure in ~/.openclaw/openclaw.json", file=sys.stderr)
        sys.exit(1)

    # Initialize OpenAI client
    client = OpenAI(
        base_url="https://ai.gitee.com/v1",
        api_key=api_key,
    )

    # Build extra_body parameters
    SUPPORTED_KWARGS = {
        "Qwen-Image": ["negative_prompt", "num_inference_steps"],
        "Kolors": ["num_inference_steps", "guidance_scale"],
        "GLM-Image": ["negative_prompt", "num_inference_steps", "guidance_scale"],
        "FLUX.2-dev": ["negative_prompt", "num_inference_steps", "guidance_scale"],
        "HunyuanDiT-v1.2-Diffusers-Distilled": ["negative_prompt", "num_inference_steps", "guidance_scale"],
    }
    
    MODEL_DEFAULTS = {
        "Qwen-Image": {"num_inference_steps": 30},
        "Kolors": {"num_inference_steps": 25, "guidance_scale": 7.5},
        "GLM-Image": {"num_inference_steps": 30, "guidance_scale": 1.5},
        "FLUX.2-dev": {"num_inference_steps": 20, "guidance_scale": 7.5},
        "HunyuanDiT-v1.2-Diffusers-Distilled": {"num_inference_steps": 25, "guidance_scale": 5.0},
    }

    allowed_params = SUPPORTED_KWARGS.get(args.model, [])
    model_defaults = MODEL_DEFAULTS.get(args.model, {})

    extra_body = {"response_format": "url"}
    
    if "negative_prompt" in allowed_params and args.negative_prompt:
        extra_body["negative_prompt"] = args.negative_prompt
        
    if "guidance_scale" in allowed_params:
        gs_val = args.guidance_scale if args.guidance_scale is not None else model_defaults.get("guidance_scale")
        if gs_val is not None:
            extra_body["guidance_scale"] = gs_val
            
    if "num_inference_steps" in allowed_params:
        nis_val = args.num_inference_steps if args.num_inference_steps is not None else model_defaults.get("num_inference_steps")
        if nis_val is not None:
            extra_body["num_inference_steps"] = nis_val

    print(f"Generating image using {args.model}...")
    print(f"Size: {args.size}")
    print(f"Prompt: {args.prompt}")
    print(f"Extra params: {extra_body}")

    try:
        # Make API request
        response = client.images.generate(
            prompt=args.prompt,
            model=args.model,
            size=args.size,
            extra_body=extra_body,
        )

        # Process response - only output URL
        for image_data in response.data:
            if image_data.url:
                image_url = image_data.url
                print(f"\nIMAGE_URL: {image_url}")

    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()