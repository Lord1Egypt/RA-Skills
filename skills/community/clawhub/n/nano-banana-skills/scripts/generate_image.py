#!/usr/bin/env python3
"""Generate images using Google Gemini models via Wisdom Gate API."""

import argparse
import base64
import json
import os
import sys
import requests

# Model configurations
MODELS = {
    "nano-banana": {
        "id": "gemini-2.5-flash-image",
        "name": "Nano Banana (Cheapest)",
        "resolutions": ["1K", "2K"],
        "cost": "low"
    },
    "nano-banana-2": {
        "id": "gemini-3.1-flash-image-preview",
        "name": "Nano Banana 2 (Best Value)",
        "resolutions": ["0.5K", "1K", "2K", "4K"],
        "cost": "medium"
    },
    "nano-banana-pro": {
        "id": "gemini-3-pro-image-preview",
        "name": "Nano Banana Pro (Best Quality)",
        "resolutions": ["1K", "2K", "4K"],
        "cost": "high"
    }
}

def select_model(image_size, input_images, quality_priority=False):
    """
    Automatically select the best model based on requirements.
    
    Args:
        image_size: Requested resolution (0.5K, 1K, 2K, 4K)
        input_images: List of input images (for image-to-image)
        quality_priority: If True, prefer quality over cost
    
    Returns:
        Model ID string
    """
    # Image-to-image with multiple images -> use Pro for best quality
    if input_images and len(input_images) > 1:
        return MODELS["nano-banana-pro"]["id"]
    
    # 4K resolution -> only Nano Banana 2 or Pro support it
    if image_size == "4K":
        return MODELS["nano-banana-pro"]["id"] if quality_priority else MODELS["nano-banana-2"]["id"]
    
    # 0.5K resolution -> only Nano Banana 2 supports it
    if image_size == "0.5K":
        return MODELS["nano-banana-2"]["id"]
    
    # Quality priority -> use Pro
    if quality_priority:
        return MODELS["nano-banana-pro"]["id"]
    
    # Default: Nano Banana 2 (best balance)
    return MODELS["nano-banana-2"]["id"]

def generate_image(prompt, aspect_ratio="1:1", image_size="1K", output_path="generated_image.png", 
                   input_images=None, model=None, quality_priority=False):
    """Generate an image from a text prompt, optionally with input images (up to 14)."""
    
    api_key = os.getenv("WISGATE_KEY")
    if not api_key:
        print("Error: WISGATE_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    # Auto-select model if not specified
    if not model:
        model = select_model(image_size, input_images, quality_priority)
    
    api_url = f"https://api.wisgate.ai/v1beta/models/{model}:generateContent"
    
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    # Build parts array
    parts = [{"text": prompt}]
    
    # Add input images if provided (up to 14)
    if input_images:
        if len(input_images) > 14:
            print("Warning: Maximum 14 images supported, using first 14", file=sys.stderr)
            input_images = input_images[:14]
        
        for img_path in input_images:
            if not os.path.exists(img_path):
                print(f"Error: Input image not found: {img_path}", file=sys.stderr)
                sys.exit(1)
            
            with open(img_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Detect MIME type
            mime_type = "image/jpeg"
            if img_path.lower().endswith(".png"):
                mime_type = "image/png"
            elif img_path.lower().endswith(".webp"):
                mime_type = "image/webp"
            
            parts.append({
                "inline_data": {
                    "mime_type": mime_type,
                    "data": image_data
                }
            })
    
    payload = {
        "contents": [{
            "role": "user",
            "parts": parts
        }],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }
    
    # Add imageConfig only for text-to-image (not image-to-image)
    if not input_images:
        payload["tools"] = [{"google_search": {}}]
        payload["generationConfig"]["imageConfig"] = {
            "aspectRatio": aspect_ratio,
            "imageSize": image_size
        }
    
    print(f"Using model: {model}", file=sys.stderr)
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        # Extract image data
        for candidate in result.get("candidates", []):
            for part in candidate.get("content", {}).get("parts", []):
                if "inlineData" in part:
                    image_data = part["inlineData"]["data"]
                    mime_type = part["inlineData"].get("mimeType", "image/png")
                    
                    # Auto-detect extension if output_path doesn't have one
                    if "." not in os.path.basename(output_path):
                        extension = mime_type.split("/")[1]
                        output_path = f"{output_path}.{extension}"
                    
                    with open(output_path, "wb") as f:
                        f.write(base64.b64decode(image_data))
                    print(f"Image saved to: {output_path}")
                    return
        
        print("Error: No image data found in response", file=sys.stderr)
        sys.exit(1)
        
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate images using Gemini models")
    parser.add_argument("prompt", help="Text description of the image to generate")
    parser.add_argument("--input", nargs="+", help="Input image path(s) for image-to-image generation (up to 14)")
    parser.add_argument("--aspect-ratio", default="1:1", 
                       choices=["1:1", "16:9", "9:16", "21:9", "4:3", "3:4", "5:4", "4:5", "2:3", "3:2", "1:4", "4:1", "1:8", "8:1"],
                       help="Image aspect ratio (text-to-image only, default: 1:1)")
    parser.add_argument("--size", default="1K", choices=["0.5K", "1K", "2K", "4K"],
                       help="Image resolution (text-to-image only, default: 1K)")
    parser.add_argument("--output", default="generated_image.png",
                       help="Output file path (default: generated_image.png)")
    parser.add_argument("--model", choices=["nano-banana", "nano-banana-2", "nano-banana-pro"],
                       help="Force specific model (auto-select if not specified)")
    parser.add_argument("--quality", action="store_true",
                       help="Prioritize quality over cost (uses Nano Banana Pro when possible)")
    
    args = parser.parse_args()
    
    # Convert model alias to actual model ID
    model_id = None
    if args.model:
        model_id = MODELS[args.model]["id"]
    
    generate_image(args.prompt, args.aspect_ratio, args.size, args.output, args.input, model_id, args.quality)
