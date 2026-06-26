#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "openai"
# ]
# ///

"""
Perform OCR on images using Gitee AI Vision API.

Usage:
    python perform_ocr.py --image /path/to/image.jpg --prompt "Users requirements" [--api-key KEY]
"""

import argparse
import os
import sys
import base64
import mimetypes
from openai import OpenAI

def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument, config, or environment."""
    if provided_key:
        return provided_key
    return os.environ.get("GITEEAI_API_KEY")

def main():
    parser = argparse.ArgumentParser(
        description="Perform OCR on images using Gitee AI Vision API"
    )
    parser.add_argument(
        "--image", "-i",
        required=True,
        help="Path to the local image file"
    )
    parser.add_argument(
        "--prompt", "-p",
        default="请提取这张图片中的所有文字内容。",
        help="Prompt/Instructions for the OCR task"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Gitee AI API key (overrides GITEEAI_API_KEY env var)"
    )

    args = parser.parse_args()

    # Get API key
    api_key = get_api_key(args.api_key)
    
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set GITEEAI_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    # Initialize OpenAI client
    client = OpenAI(
        base_url="https://ai.gitee.com/v1",
        api_key=api_key,
    )

    print(f"Processing image for OCR...")
    print(f"Image: {args.image}")
    print(f"Prompt: {args.prompt}")

    try:
        filepath = args.image
        
        # Prepare image_url (support both local file paths and URLs)
        if filepath.startswith(("http://", "https://")):
            image_url = filepath
        else:
            if not os.path.exists(filepath):
                print(f"Error: Image file not found at {filepath}", file=sys.stderr)
                sys.exit(1)
            mime_type, _ = mimetypes.guess_type(filepath)
            mime_type = mime_type or "image/jpeg"
            with open(filepath, "rb") as f:
                base64_image = base64.b64encode(f.read()).decode('utf-8')
            image_url = f"data:{mime_type};base64,{base64_image}"

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful and harmless assistant. You should think step-by-step."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        },
                        {
                            "type": "text",
                            "text": args.prompt
                        }
                    ]
                }
            ],
            model="PaddleOCR-VL-1.5",
            stream=False,
            max_tokens=512,
            temperature=0.7,
            top_p=1,
            extra_body={
                "top_k": 1,
            },
            frequency_penalty=0,
        )

        print("\nOCR_RESULT:")
        
        # Extract and print the final content directly
        if response.choices and len(response.choices) > 0:
            result_text = response.choices[0].message.content
            if result_text:
                print(result_text.strip())
            else:
                print("No text recognized.")
        else:
            print("No response choices returned.")

    except Exception as e:
        print(f"\nError performing OCR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()