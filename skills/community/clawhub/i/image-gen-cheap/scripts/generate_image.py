#!/usr/bin/env python3
"""
Image Generation Script - LaoZhang API
Usage: python generate_image.py "prompt" [--model MODEL] [--ratio RATIO] [--output PATH]
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

# API Configuration
API_URL = "https://api.laozhang.ai/v1/chat/completions"

# Available Models
AVAILABLE_MODELS = {
    "sora_image": "Sora Image - $0.01/img, returns URL",
    "gpt-4o-image": "GPT-4o Image - $0.01/img, returns URL",
    "gemini-2.5-flash-image": "Nano Banana - $0.025/img, returns base64",
    "gemini-3.1-flash-image-preview": "Nano Banana2 - $0.03/img, returns base64",
    "gemini-3-pro-image-preview": "Nano Banana Pro - $0.05/img, returns base64",
}

DEFAULT_MODEL = "sora_image"
DEFAULT_TOKEN_PATH = Path.home() / ".laozhang_api_token"
DEFAULT_OUTPUT_DIR = Path.cwd() / "generated-images"


def get_api_token():
    """Get API token from file"""
    if DEFAULT_TOKEN_PATH.exists():
        return DEFAULT_TOKEN_PATH.read_text().strip()
    return None


def generate_filename(prompt: str, ratio: str = None):
    """Generate filename from prompt and date"""
    date_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    keywords = "".join(c for c in prompt[:20] if c.isalnum() or c in " -_").strip()
    keywords = keywords.replace(" ", "-")[:20]
    ratio_suffix = f"-{ratio.replace(':', 'x')}" if ratio else ""
    return f"{date_str}-{keywords}{ratio_suffix}.png"


def generate_image(prompt: str, token: str, model: str = None, ratio: str = None, verbose: bool = False):
    """
    Generate image using specified model
    
    Args:
        prompt: Image description
        token: API token
        model: Model to use (default: sora_image)
        ratio: Aspect ratio: "2:3", "3:2", "1:1"
        verbose: Show detailed info
    
    Returns:
        Tuple of (image_urls, full_response)
    """
    if model is None:
        model = DEFAULT_MODEL
    
    # Sora Image needs ratio marker
    if model == "sora_image" and ratio and ratio in ["2:3", "3:2", "1:1"]:
        prompt = f"{prompt}【{ratio}】"
    
    if verbose:
        print(f"Prompt: {prompt}")
        print(f"Ratio: {ratio or 'default'}")
        print(f"Model: {model}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        content = result['choices'][0]['message']['content']
        image_urls = re.findall(r'!\[.*?\]\((https?://[^)]+)\)', content)
        
        if verbose and image_urls:
            print(f"Generated {len(image_urls)} image(s)")
        
        return image_urls, result
    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return [], None


def download_image(url: str, output_path: Path):
    """Download image to local file"""
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


def main():
    parser = argparse.ArgumentParser(
        description="Image Generation - LaoZhang API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Models:
  sora_image                          $0.01/img, returns URL (default)
  gpt-4o-image                        $0.01/img, returns URL
  gemini-2.5-flash-image              $0.025/img, returns base64
  gemini-3.1-flash-image-preview      $0.03/img, returns base64
  gemini-3-pro-image-preview          $0.05/img, returns base64

Examples:
  %(prog)s "A cute cat playing in a garden"
  %(prog)s "Sunset beach" --ratio 3:2
  %(prog)s "A puppy" --output dog.png
  %(prog)s "Futuristic city" --model gpt-4o-image
        """
    )
    
    parser.add_argument("prompt", help="Image description")
    parser.add_argument("--model", "-m", choices=list(AVAILABLE_MODELS.keys()),
                       help=f"Model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--ratio", "-r", choices=["2:3", "3:2", "1:1"], 
                       help="Aspect ratio (sora_image only)")
    parser.add_argument("--output", "-o", type=Path, help="Output image path")
    parser.add_argument("--token", "-t", help="API token (or read from ~/.laozhang_api_token)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show details")
    parser.add_argument("--json", action="store_true", help="Output full JSON response")
    parser.add_argument("--no-save", action="store_true", help="Don't save (show URL only)")
    
    args = parser.parse_args()
    
    # Get token
    token = args.token or get_api_token()
    if not token:
        print("Error: No API token provided")
        print(f"Create {DEFAULT_TOKEN_PATH} with your token, or use --token")
        sys.exit(1)
    
    # Generate image
    urls, result = generate_image(args.prompt, token, args.model, args.ratio, args.verbose)
    
    if not urls:
        print("Failed to generate image")
        sys.exit(1)
    
    # Output results
    for i, url in enumerate(urls, 1):
        print(f"Image {i}: {url}")
    
    # Download image
    if not args.no_save and urls:
        if args.output:
            output_path = args.output
        else:
            filename = generate_filename(args.prompt, args.ratio)
            output_path = DEFAULT_OUTPUT_DIR / filename
        
        download_image(urls[0], output_path)
    
    # Output JSON
    if args.json and result:
        print("\nFull response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
