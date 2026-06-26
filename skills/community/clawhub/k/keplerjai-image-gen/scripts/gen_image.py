#!/usr/bin/env python3
"""
ThinkZone AI Image Generation Script
支持 3 个图片生成模型：
- Gemini 3.1 Flash Image Preview
- MiniMax Image 01
- BytePlus Seedream 5.0 Lite
"""

import argparse
import json
import os
import sys
import base64
import urllib.request
import urllib.error
from pathlib import Path

# 支持的图片生成模型
SUPPORTED_MODELS = [
    "gemini-3.1-flash-image-preview",  # Gemini 3.1 Flash Image Preview
    "image-01",                         # MiniMax Image 01
    "doubao-seedream-5-0-260128",       # BytePlus Seedream 5.0 Lite
]

def get_config():
    """Get configuration from environment variables."""
    api_key = os.environ.get("THINKZONE_API_KEY")
    base_url = os.environ.get("THINKZONE_BASE_URL", "https://open.thinkzoneai.com")
    
    # Fallback to hardcoded values if env vars not set (for Gateway service)
    if not api_key:
        api_key = "amags_b6324919c0056a78dc326ef06011ecc7d2af896b6b659c216371e55d66895dac"
    
    if not api_key:
        print("Error: THINKZONE_API_KEY not set", file=sys.stderr)
        print("Get your API key at https://open.thinkzoneai.com", file=sys.stderr)
        sys.exit(1)
    
    return api_key, base_url

def load_images_as_base64(image_paths):
    """Load images from files and return as base64 data URLs."""
    images = []
    for path in image_paths:
        try:
            with open(path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode("utf-8")
            ext = Path(path).suffix.lower()
            mime_map = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".webp": "image/webp",
                ".gif": "image/gif"
            }
            mime = mime_map.get(ext, "image/jpeg")
            images.append(f"data:{mime};base64,{image_data}")
        except Exception as e:
            print(f"Warning: Failed to load image {path}: {e}", file=sys.stderr)
    return images

def generate_gemini(prompt, resolution="1K", aspect_ratio="1:1", 
                   images=None, thinking_level="minimal",
                   base_url="https://open.thinkzoneai.com",
                   api_key=None):
    """Call Gemini 3.1 Flash Image Preview API."""
    
    if api_key is None:
        api_key, base_url = get_config()
    
    url = f"{base_url}/v1beta/models/gemini-3.1-flash-image-preview:generateContent"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Build contents array
    contents = [{ "parts": [{ "text": prompt }] }]
    
    # Add images if provided
    if images:
        image_parts = []
        for img in images:
            if img.startswith("data:"):
                # Parse data URL
                mime, b64 = img.split(",", 1)
                mime = mime.split(":")[1].split(";")[0]
                image_parts.append({
                    "inlineData": {
                        "mimeType": mime,
                        "data": b64
                    }
                })
            else:
                # URL
                image_parts.append({
                    "fileData": {
                        "fileUri": img
                    }
                })
        contents.append({ "parts": image_parts })
    
    # Build request body
    data = {
        "contents": contents,
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": resolution
            },
            "thinkingConfig": {
                "thinkingLevel": thinking_level,
                "includeThoughts": False
            }
        }
    }
    
    # Make request
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    
    return result

def generate_minimax(prompt, width=1024, height=1024, aspect_ratio="1:1",
                    n=1, watermark=False, subject_reference=None,
                    base_url="https://open.thinkzoneai.com",
                    api_key=None):
    """Call MiniMax Image 01 API."""
    
    if api_key is None:
        api_key, base_url = get_config()
    
    url = f"{base_url}/v1/image_generation"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Build request body
    data = {
        "model": "image-01",
        "prompt": prompt,
        "width": width,
        "height": height,
        "n": n,
        "aigc_watermark": watermark
    }
    
    if aspect_ratio:
        data["aspect_ratio"] = aspect_ratio
    
    if subject_reference:
        data["subject_reference"] = [{
            "type": "character",
            "image_file": subject_reference
        }]
    
    # Make request
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    
    return result

def generate_seedream(prompt, size="2K", output_format="jpeg", watermark=False,
                     max_images=1, images=None, stream=False,
                     base_url="https://open.thinkzoneai.com",
                     api_key=None):
    """Call BytePlus Seedream 5.0 Lite API."""
    
    if api_key is None:
        api_key, base_url = get_config()
    
    url = f"{base_url}/v3/images/generations"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Build request body
    data = {
        "model": "doubao-seedream-5-0-260128",
        "prompt": prompt,
        "size": size,
        "output_format": output_format,
        "watermark": watermark,
        "stream": stream
    }
    
    # Add reference images
    if images:
        data["image"] = images
    
    # Sequential generation for multiple images
    if max_images > 1:
        data["sequential_image_generation"] = "auto"
        data["sequential_image_generation_options"] = {
            "max_images": min(max_images, 15)
        }
    
    # Make request
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    
    return result

def parse_gemini_result(result):
    """Parse Gemini API result and extract image URLs/base64."""
    images = []
    candidates = result.get("candidates", [])
    
    for candidate in candidates:
        content = candidate.get("content", {})
        parts = content.get("parts", [])
        
        for part in parts:
            if "fileData" in part and "fileUri" in part["fileData"]:
                images.append(part["fileData"]["fileUri"])
            elif "inlineData" in part:
                inline = part["inlineData"]
                mime = inline.get("mimeType", "image/png")
                data = inline.get("data", "")
                if data:
                    images.append(f"data:{mime};base64,{data}")
    
    return images

def parse_minimax_result(result):
    """Parse MiniMax API result and extract image URLs/base64."""
    images = []
    data = result.get("data", {})
    
    # Image URLs
    image_urls = data.get("image_urls", [])
    images.extend(image_urls)
    
    # Base64 images
    image_base64 = data.get("image_base64", [])
    for b64 in image_base64:
        if b64.startswith("data:"):
            images.append(b64)
        else:
            images.append(f"data:image/png;base64,{b64}")
    
    return images

def parse_seedream_result(result):
    """Parse Seedream API result and extract image URLs."""
    images = []
    data_list = result.get("data", [])
    
    for item in data_list:
        if "url" in item:
            images.append(item["url"])
        elif "b64_json" in item:
            images.append(f"data:image/png;base64,{item['b64_json']}")
    
    return images

def save_images(images, output_dir, prompt, model):
    """Save generated images to files."""
    
    if not images:
        print("No images to save", file=sys.stderr)
        return []
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    saved_files = []
    
    for idx, img in enumerate(images):
        try:
            if img.startswith("http"):
                # Download from URL
                with urllib.request.urlopen(img, timeout=30) as resp:
                    image_data = resp.read()
                ext = "jpg"
            elif img.startswith("data:"):
                # Decode base64
                b64 = img.split(",", 1)[1]
                image_data = base64.b64decode(b64)
                mime = img.split(":")[1].split(";")[0]
                ext_map = {
                    "image/jpeg": "jpg",
                    "image/png": "png",
                    "image/webp": "webp",
                    "image/gif": "gif"
                }
                ext = ext_map.get(mime, "jpg")
            else:
                print(f"Unknown image format: {img[:50]}...", file=sys.stderr)
                continue
            
            # Extract filename from URL or use index
            try:
                if '/' in img:
                    stem = Path(img.split('?')[0].stem)
                else:
                    stem = str(idx)
            except:
                stem = str(idx)
            filename = f"image_{idx}_{model}_{stem}.{ext}"
            filepath = output_dir / filename
            
            with open(filepath, "wb") as f:
                f.write(image_data)
            
            saved_files.append(str(filepath))
            print(f"Saved: {filepath}")
            
        except Exception as e:
            print(f"Failed to save image {idx}: {e}", file=sys.stderr)
            continue
    
    # Save metadata
    if saved_files:
        info_file = output_dir / "generation_info.json"
        info = {
            "prompt": prompt,
            "model": model,
            "files": saved_files,
            "count": len(saved_files)
        }
        with open(info_file, "w") as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
    
    return saved_files

def main():
    parser = argparse.ArgumentParser(
        description="ThinkZone AI Image Generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported models:
  gemini-3.1-flash-image-preview  Gemini 3.1 Flash Image Preview
  image-01                        MiniMax Image 01
  seedream-5-0-260128             BytePlus Seedream 5.0 Lite (default)

Gemini Examples:
  python gen_image.py -p "一只穿宇航服的虾" -m gemini-3.1-flash-image-preview --resolution 2K --aspect-ratio 16:9
  python gen_image.py -p "基于参考图" -m gemini-3.1-flash-image-preview --images ref1.jpg ref2.jpg

MiniMax Examples:
  python gen_image.py -p "可爱的猫咪" -m image-01 --width 1024 --height 1024 --n 4
  python gen_image.py -p "古装角色" -m image-01 --subject-reference char.jpg --aspect-ratio 3:4

Seedream Examples:
  python gen_image.py -p "中国风山水画" -m seedream-5-0-260128 --size 3K --max-images 4
  python gen_image.py -p "基于参考图" -m seedream-5-0-260128 --images ref1.jpg ref2.jpg --no-watermark
        """
    )
    
    # Common parameters
    parser.add_argument("--prompt", "-p", required=True, help="Image prompt")
    parser.add_argument("--model", "-m", default="seedream-5-0-260128",
                       choices=SUPPORTED_MODELS,
                       help="Model name (default: seedream-5-0-260128)")
    parser.add_argument("--output-dir", "-d", help="Output directory")
    parser.add_argument("--api-key", help="API key (or set THINKZONE_API_KEY)")
    parser.add_argument("--base-url", help="Base URL (or set THINKZONE_BASE_URL)")
    
    # Gemini parameters
    gemini_group = parser.add_argument_group("Gemini 3.1 Flash Image Preview")
    gemini_group.add_argument("--resolution", choices=["0.5K", "1K", "2K", "4K"],
                             default="1K", help="Resolution (Gemini only)")
    gemini_group.add_argument("--aspect-ratio", 
                             default="1:1",
                             help="Aspect ratio (Gemini/MiniMax)")
    gemini_group.add_argument("--images", "-i", nargs="+",
                             help="Reference image paths (Gemini/Seedream)")
    gemini_group.add_argument("--thinking-level", choices=["minimal", "high"],
                             default="minimal", help="Thinking level (Gemini)")
    
    # MiniMax parameters
    minimax_group = parser.add_argument_group("MiniMax Image 01")
    minimax_group.add_argument("--width", type=int, default=1024,
                              help="Width in pixels (MiniMax, 512-2048)")
    minimax_group.add_argument("--height", type=int, default=1024,
                              help="Height in pixels (MiniMax, 512-2048)")
    minimax_group.add_argument("--n", type=int, default=1,
                              help="Number of images (MiniMax, 1-9)")
    minimax_group.add_argument("--subject-reference",
                              help="Subject reference image (MiniMax)")
    minimax_group.add_argument("--watermark", "-w", action="store_true",
                              help="Add watermark (MiniMax/Seedream)")
    
    # Seedream parameters
    seedream_group = parser.add_argument_group("BytePlus Seedream 5.0 Lite")
    seedream_group.add_argument("--size", choices=["2K", "3K"],
                               default="2K", help="Output size (Seedream)")
    seedream_group.add_argument("--output-format", choices=["jpeg", "png"],
                               default="jpeg", help="Output format (Seedream)")
    seedream_group.add_argument("--max-images", type=int, default=1,
                               help="Max images (Seedream, 1-15)")
    seedream_group.add_argument("--stream", action="store_true",
                               help="Stream output (Seedream)")
    seedream_group.add_argument("--no-watermark", action="store_false",
                               dest="watermark", help="Disable watermark")
    
    args = parser.parse_args()
    
    # Get config
    api_key = args.api_key or os.environ.get("THINKZONE_API_KEY")
    base_url = args.base_url or os.environ.get("THINKZONE_BASE_URL", "https://open.thinkzoneai.com")
    
    if not api_key:
        print("Error: API key required. Set THINKZONE_API_KEY or use --api-key", file=sys.stderr)
        sys.exit(1)
    
    # Set default output directory
    output_dir = args.output_dir or Path("./tmp/thinkzone-image")
    
    print(f"[IMAGE] Generating with prompt: {args.prompt}")
    print(f"[MODEL] {args.model}")
    
    # Load reference images if provided
    images = None
    if args.images:
        images = load_images_as_base64(args.images)
        print(f"[IMAGES] Loaded {len(images)} reference image(s)")
    
    # Call appropriate API based on model
    if args.model == "gemini-3.1-flash-image-preview":
        print(f"[RESOLUTION] {args.resolution}")
        print(f"[ASPECT RATIO] {args.aspect_ratio}")
        print(f"[THINKING] {args.thinking_level}")
        
        result = generate_gemini(
            prompt=args.prompt,
            resolution=args.resolution,
            aspect_ratio=args.aspect_ratio,
            images=images,
            thinking_level=args.thinking_level,
            base_url=base_url,
            api_key=api_key
        )
        image_list = parse_gemini_result(result)
        
    elif args.model == "image-01":
        print(f"[SIZE] {args.width}x{args.height}")
        print(f"[COUNT] {args.n}")
        if args.subject_reference:
            print(f"[SUBJECT REF] {args.subject_reference}")
        
        # Load subject reference if provided
        subject_ref = None
        if args.subject_reference:
            subject_images = load_images_as_base64([args.subject_reference])
            subject_ref = subject_images[0] if subject_images else None
        
        result = generate_minimax(
            prompt=args.prompt,
            width=args.width,
            height=args.height,
            aspect_ratio=args.aspect_ratio,
            n=args.n,
            watermark=args.watermark,
            subject_reference=subject_ref,
            base_url=base_url,
            api_key=api_key
        )
        image_list = parse_minimax_result(result)
        
    else:  # seedream-5-0-260128
        print(f"[SIZE] {args.size}")
        print(f"[FORMAT] {args.output_format}")
        if args.max_images > 1:
            print(f"[COUNT] {args.max_images}")
        
        # Convert base64 images to URLs for Seedream
        image_urls = images if images else None
        
        result = generate_seedream(
            prompt=args.prompt,
            size=args.size,
            output_format=args.output_format,
            watermark=args.watermark,
            max_images=args.max_images,
            images=image_urls,
            stream=args.stream,
            base_url=base_url,
            api_key=api_key
        )
        image_list = parse_seedream_result(result)
    
    # Print response preview
    result_preview = json.dumps(result, indent=2, ensure_ascii=False)
    if len(result_preview) > 500:
        result_preview = result_preview[:500] + "..."
    print(f"\n[RESPONSE]\n{result_preview}")
    
    # Save images
    if image_list:
        saved = save_images(image_list, output_dir, args.prompt, args.model)
        if saved:
            print(f"\n[SUCCESS] Generated {len(saved)} image(s)")
            print(f"[OUTPUT] Directory: {output_dir}")
        else:
            print("\n[ERROR] Failed to save images")
            sys.exit(1)
    else:
        print("\n[ERROR] No images generated")
        print(f"[FULL RESPONSE] {result_preview}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
