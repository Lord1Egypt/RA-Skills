#!/usr/bin/env python3
"""
Image Editing Script - LaoZhang API
Usage: python edit_image.py "image_url(s)" "edit_prompt" [--model MODEL] [--style STYLE]
"""

import argparse
import json
import re
import sys
import base64
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

# API Configuration
API_URL = "https://api.laozhang.ai/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o-image"
DEFAULT_TOKEN_PATH = Path.home() / ".laozhang_api_token"
DEFAULT_OUTPUT_DIR = Path.cwd() / "generated-images"

# Available Models
AVAILABLE_MODELS = {
    "gpt-4o-image": "GPT-4o Image - $0.01/img, returns URL",
    "sora_image": "Sora Image - $0.01/img, returns URL",
    "gemini-2.5-flash-image": "Nano Banana - $0.025/img, returns base64",
    "gemini-3.1-flash-image-preview": "Nano Banana2 - $0.03/img, returns base64",
    "gemini-3-pro-image-preview": "Nano Banana Pro - $0.05/img, returns base64",
}

# Preset Styles
STYLE_TEMPLATES = {
    "cartoon": "Convert to Disney cartoon style, bright colors",
    "oil-painting": "Convert to classic oil painting style, like Van Gogh",
    "ink-wash": "Convert to Chinese ink wash painting style",
    "cyberpunk": "Convert to cyberpunk style with neon light effects",
    "sketch": "Convert to pencil sketch style, black and white lines",
    "watercolor": "Convert to watercolor painting style",
}


def get_api_token():
    """Get API token from file"""
    if DEFAULT_TOKEN_PATH.exists():
        return DEFAULT_TOKEN_PATH.read_text().strip()
    return None


def generate_filename(prompt: str, style: str = ""):
    """Generate filename from prompt and date"""
    date_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    keywords = "".join(c for c in prompt[:15] if c.isalnum() or c in " -_").strip()
    keywords = keywords.replace(" ", "-")[:15]
    style_suffix = f"-{style}" if style else ""
    return f"{date_str}-edit-{keywords}{style_suffix}.png"


def edit_image(image_urls: list, prompt: str, token: str, model: str = None, verbose: bool = False):
    """
    Edit image(s) using specified model
    
    Args:
        image_urls: List of image URLs
        prompt: Edit description
        token: API token
        model: Model to use
        verbose: Show detailed info
    
    Returns:
        Tuple of (results_list, full_response)
        results_list contains tuples of (type, data) where type is "url" or "base64"
    """
    if model is None:
        model = DEFAULT_MODEL
    
    # Build message with images
    content = [{"type": "text", "text": prompt}]
    for url in image_urls:
        content.append({
            "type": "image_url",
            "image_url": {"url": url}
        })
    
    if verbose:
        print(f"Prompt: {prompt}")
        print(f"Input images: {len(image_urls)}")
        print(f"Model: {model}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": content}]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        result_content = result['choices'][0]['message']['content']
        
        # Try to extract URLs first
        urls = re.findall(r'!\[.*?\]\((https?://[^)]+)\)', result_content)
        
        results = []
        if urls:
            for url in urls:
                results.append(("url", url))
        else:
            # Try to extract base64 data
            base64_matches = re.findall(r'data:image/[^;]+;base64,([A-Za-z0-9+/=]+)', result_content)
            if not base64_matches:
                # Maybe it's just raw base64 in the content
                base64_matches = re.findall(r'([A-Za-z0-9+/]{100,}={0,2})', result_content)
            for b64 in base64_matches:
                results.append(("base64", b64))
        
        if verbose and results:
            print(f"Generated {len(results)} image(s)")
        
        return results, result
    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return [], None


def download_image(url: str, output_path: Path):
    """Download image from URL"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(response.content)
        print(f"Saved: {output_path}")
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False


def save_base64(b64_data: str, output_path: Path):
    """Save base64 encoded image"""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        image_data = base64.b64decode(b64_data)
        output_path.write_bytes(image_data)
        print(f"Saved: {output_path}")
        return True
    except Exception as e:
        print(f"Save failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Image Editing - LaoZhang API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Models:
  gpt-4o-image                        $0.01/img, returns URL (default)
  sora_image                          $0.01/img, returns URL
  gemini-2.5-flash-image              $0.025/img, returns base64
  gemini-3.1-flash-image-preview      $0.03/img, returns base64
  gemini-3-pro-image-preview          $0.05/img, returns base64

Preset Styles:
  cartoon      - Disney cartoon style
  oil-painting - Classic oil painting
  ink-wash     - Chinese ink wash painting
  cyberpunk    - Neon light effects
  sketch       - Pencil sketch
  watercolor   - Watercolor painting

Examples:
  %(prog)s "https://example.com/cat.jpg" "Change fur to rainbow"
  %(prog)s "https://example.com/photo.jpg" --style cartoon
  %(prog)s "https://a.jpg,https://b.jpg" "Merge these images"
        """
    )
    
    parser.add_argument("images", help="Image URL(s), comma-separated for multiple")
    parser.add_argument("prompt", nargs="?", help="Edit description (optional with --style)")
    parser.add_argument("--style", "-s", choices=list(STYLE_TEMPLATES.keys()),
                       help="Preset style")
    parser.add_argument("--model", "-m", choices=list(AVAILABLE_MODELS.keys()),
                       help=f"Model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--output", "-o", type=Path, help="Output image path")
    parser.add_argument("--token", "-t", help="API token (or read from ~/.laozhang_api_token)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show details")
    parser.add_argument("--json", action="store_true", help="Output full JSON response")
    parser.add_argument("--no-save", action="store_true", help="Don't save (show URL only)")
    
    args = parser.parse_args()
    
    # Handle preset style
    if args.style:
        prompt = STYLE_TEMPLATES[args.style]
    elif args.prompt:
        prompt = args.prompt
    else:
        print("Error: Either prompt or --style is required")
        sys.exit(1)
    
    # Parse image URLs
    image_urls = [url.strip() for url in args.images.split(",")]
    
    # Get token
    token = args.token or get_api_token()
    if not token:
        print("Error: No API token provided")
        print(f"Create {DEFAULT_TOKEN_PATH} with your token, or use --token")
        sys.exit(1)
    
    # Edit image
    results, response = edit_image(image_urls, prompt, token, args.model, args.verbose)
    
    if not results:
        print("Failed to generate image")
        sys.exit(1)
    
    # Output results
    for i, (img_type, data) in enumerate(results, 1):
        if img_type == "url":
            print(f"Image {i}: {data}")
        else:
            print(f"Image {i}: [base64, {len(data)} chars]")
    
    # Save image
    if not args.no_save and results:
        if args.output:
            output_path = args.output
        else:
            style_suffix = args.style or ""
            filename = generate_filename(prompt, style_suffix)
            output_path = DEFAULT_OUTPUT_DIR / filename
        
        img_type, data = results[0]
        if img_type == "url":
            download_image(data, output_path)
        else:
            save_base64(data, output_path)
    
    # Output JSON
    if args.json and response:
        print("\nFull response:")
        print(json.dumps(response, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
