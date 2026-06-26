#!/usr/bin/env python3
"""Image generation module using OpenAI DALL-E 3 API."""

import os
import time
import requests
from openai import OpenAI, APIError

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def generate_image(
    prompt: str,
    output_dir: str = "/workspace/generated",
    size: str = "1024x1024",
    quality: str = "standard",
    style: str = "vivid",
) -> dict | None:
    """Generate image using OpenAI DALL-E 3 API and save to output directory."""
    try:
        print(f"Generating image for prompt: {prompt[:50]}...")

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            style=style,
            n=1,
        )

        image_url = response.data[0].url
        revised_prompt = response.data[0].revised_prompt

        # Download and save image
        img_response = requests.get(image_url, timeout=30)
        img_response.raise_for_status()
        img_data = img_response.content

        os.makedirs(output_dir, exist_ok=True)
        safe_prompt = "".join([c for c in prompt if c.isalnum() or c in (' ', '-', '_')]).rstrip()[:50].replace(' ', '_')
        filename = f"{safe_prompt}_{int(time.time())}.png"
        output_path = os.path.join(output_dir, filename)

        with open(output_path, 'wb') as f:
            f.write(img_data)

        print(f"Image saved to {output_path}")
        print(f"Revised prompt used: {revised_prompt}")

        return {
            "image_path": output_path,
            "revised_prompt": revised_prompt,
            "original_prompt": prompt,
        }

    except (APIError, requests.RequestException, OSError) as e:
        print(f"Image generation failed: {e}")
        return None


def batch_generate(prompts_file: str) -> list[dict]:
    """Batch generate images from a text file with one prompt per line."""
    if not os.path.exists(prompts_file):
        print(f"Prompts file {prompts_file} not found")
        return []

    with open(prompts_file, "r") as f:
        prompts = [line.strip() for line in f if line.strip()]

    results = []
    for prompt in prompts:
        result = generate_image(prompt)
        if result:
            results.append(result)

    return results


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            batch_generate(sys.argv[1])
        else:
            generate_image(sys.argv[1])
    else:
        print("Usage:")
        print("  python generate_images.py <prompt> - Generate single image from prompt")
        print("  python generate_images.py <prompts.txt> - Batch generate from text file")
