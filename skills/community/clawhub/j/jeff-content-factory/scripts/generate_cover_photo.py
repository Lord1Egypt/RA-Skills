#!/usr/bin/env python3
"""
WeChat Cover Photo Generator using Seedream 5.0 API
Generates professional cover photos for WeChat Official Account articles
Supports 900x386 pixel WeChat standard size (21:9) with flat vector illustration style
Default API: Doubao Seedream 5.0 (火山方舟)
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional

import requests

# Try to import PIL for image resizing
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️  Warning: PIL/Pillow not installed. Image resizing will be skipped.")
    print("   Install with: pip install Pillow")


def load_env_file(env_path=".env"):
    """Load environment variables from .env file"""
    env_file = Path(env_path)
    if not env_file.exists():
        return False

    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                # Remove quotes
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                os.environ[key] = value
    return True


# Try to load .env file from script directory
script_dir = Path(__file__).parent.parent
env_path = script_dir / ".env"
if env_path.exists():
    load_env_file(env_path)


class SeedreamImageGenerator:
    """Seedream 5.0 API client (Doubao/火山方舟) for generating cover photos"""

    API_ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
    DEFAULT_MODEL = "doubao-seedream-5-0-260128"
    DEFAULT_SIZE = "1536x1024"  # Generate at 2K resolution
    DEFAULT_ASPECT_RATIO = "3:2"  # Then crop to 21:9
    WECHAT_SIZE = (900, 386)  # WeChat Official Account cover size (21:9)

    def __init__(self, api_key: str):
        """
        Initialize Seedream 5.0 generator

        Args:
            api_key: API key for authentication
        """
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def generate_image(
        self,
        prompt: str,
        model: str = DEFAULT_MODEL,
        size: str = DEFAULT_SIZE,
        aspect_ratio: str = DEFAULT_ASPECT_RATIO,
    ) -> dict:
        """
        Generate image using Seedream 5.0 API

        Args:
            prompt: Text description for image generation
            model: Model to use (default: doubao-seedream-5-0-260128)
            size: Image resolution (2K, etc.)
            aspect_ratio: Aspect ratio for the output

        Returns:
            API response dict with image URL

        Raises:
            requests.RequestException: If API call fails
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "aspect_ratio": aspect_ratio,
        }

        print(f"🎨 Generating cover photo with Seedream 5.0 API...")
        print(f"   Model: {model}")
        print(f"   Size: {size}")
        print(f"   Aspect Ratio: {aspect_ratio}")
        print(f"   Prompt: {prompt[:100]}...")

        try:
            response = requests.post(
                self.API_ENDPOINT,
                headers=self.headers,
                json=payload,
                timeout=120,
            )
            response.raise_for_status()
            result = response.json()

            if "data" in result and len(result["data"]) > 0:
                image_url = result["data"][0]["url"]
                print(f"✅ Image generated successfully!")
                print(f"   URL: {image_url}")
                return result
            else:
                raise ValueError(f"No image data in API response: {result}")

        except requests.RequestException as e:
            print(f"❌ API request failed: {e}")
            if hasattr(e, "response") and e.response is not None:
                print(f"   Response: {e.response.text}")
            raise

    def download_image(self, image_url: str, output_path: str) -> bool:
        """
        Download image from temporary URL to local file

        Args:
            image_url: Temporary image URL from API
            output_path: Local file path to save image

        Returns:
            True if download successful, False otherwise
        """
        try:
            print(f"📥 Downloading image to: {output_path}")
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()

            # Create output directory if needed
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            # Save image
            with open(output_path, "wb") as f:
                f.write(response.content)

            file_size = os.path.getsize(output_path)
            print(f"✅ Image downloaded successfully!")
            print(f"   Size: {file_size / 1024:.1f} KB")
            print(f"   Path: {output_path}")
            return True

        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False

    def resize_to_wechat(self, input_path: str, output_path: str = None) -> bool:
        """
        Resize image to WeChat Official Account cover size (900x386)

        Args:
            input_path: Path to input image
            output_path: Path to save resized image (optional, defaults to input_path)

        Returns:
            True if resize successful, False otherwise
        """
        if not PIL_AVAILABLE:
            print("⚠️  Skipping resize: PIL/Pillow not installed")
            return False

        try:
            print(f"📐 Resizing image to WeChat size (900x386, 21:9)...")

            # Open image
            img = Image.open(input_path)
            original_size = img.size
            print(f"   Original size: {original_size[0]}x{original_size[1]}")

            # Calculate crop box to maintain 21:9 aspect ratio
            target_ratio = self.WECHAT_SIZE[0] / self.WECHAT_SIZE[1]  # 900/386 ≈ 2.33
            img_ratio = img.width / img.height

            if img_ratio > target_ratio:
                # Image is wider, crop width
                new_width = int(img.height * target_ratio)
                left = (img.width - new_width) // 2
                crop_box = (left, 0, left + new_width, img.height)
            else:
                # Image is taller, crop height
                new_height = int(img.width / target_ratio)
                top = (img.height - new_height) // 2
                crop_box = (0, top, img.width, top + new_height)

            # Crop and resize
            img_cropped = img.crop(crop_box)
            img_resized = img_cropped.resize(self.WECHAT_SIZE, Image.Resampling.LANCZOS)

            # Save
            if output_path is None:
                output_path = input_path
            img_resized.save(output_path, quality=95, optimize=True)

            file_size = os.path.getsize(output_path)
            print(f"✅ Image resized successfully!")
            print(f"   New size: {self.WECHAT_SIZE[0]}x{self.WECHAT_SIZE[1]}")
            print(f"   File size: {file_size / 1024:.1f} KB")
            print(f"   Path: {output_path}")
            return True

        except Exception as e:
            print(f"❌ Resize failed: {e}")
            return False


class GLMImageGenerator:
    """GLM-Image API client (fallback option)"""

    API_ENDPOINT = "https://open.bigmodel.cn/api/paas/v4/images/generations"
    DEFAULT_MODEL = "glm-image"
    DEFAULT_SIZE = "1280x720"
    DEFAULT_QUALITY = "standard"
    WECHAT_SIZE = (900, 386)

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def generate_image(
        self,
        prompt: str,
        model: str = DEFAULT_MODEL,
        size: str = DEFAULT_SIZE,
        quality: str = DEFAULT_QUALITY,
    ) -> dict:
        payload = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "quality": quality,
        }

        print(f"🎨 Generating cover photo with GLM-Image API...")
        print(f"   Model: {model}")

        try:
            response = requests.post(
                self.API_ENDPOINT,
                headers=self.headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            result = response.json()

            if "data" in result and len(result["data"]) > 0:
                image_url = result["data"][0]["url"]
                print(f"✅ Image generated successfully!")
                return result
            else:
                raise ValueError("No image data in API response")

        except requests.RequestException as e:
            print(f"❌ API request failed: {e}")
            raise

    def download_image(self, image_url: str, output_path: str) -> bool:
        try:
            print(f"📥 Downloading image to: {output_path}")
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()

            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            with open(output_path, "wb") as f:
                f.write(response.content)

            print(f"✅ Image downloaded successfully!")
            return True

        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False

    def resize_to_wechat(self, input_path: str, output_path: str = None) -> bool:
        if not PIL_AVAILABLE:
            return False

        try:
            print(f"📐 Resizing image to WeChat size (900x386, 21:9)...")
            img = Image.open(input_path)
            target_ratio = self.WECHAT_SIZE[0] / self.WECHAT_SIZE[1]
            img_ratio = img.width / img.height

            if img_ratio > target_ratio:
                new_width = int(img.height * target_ratio)
                left = (img.width - new_width) // 2
                crop_box = (left, 0, left + new_width, img.height)
            else:
                new_height = int(img.width / target_ratio)
                top = (img.height - new_height) // 2
                crop_box = (0, top, img.width, top + new_height)

            img_cropped = img.crop(crop_box)
            img_resized = img_cropped.resize(self.WECHAT_SIZE, Image.Resampling.LANCZOS)

            if output_path is None:
                output_path = input_path
            img_resized.save(output_path, quality=95, optimize=True)

            print(f"✅ Image resized successfully!")
            return True

        except Exception as e:
            print(f"❌ Resize failed: {e}")
            return False


def build_cover_prompt(
    title: str,
    theme: str,
    style: str = "flat vector illustration",
    color_scheme: str = "blue gradient",
) -> str:
    """
    Build optimized prompt for WeChat cover photo generation
    Uses flat vector illustration style (平面矢量插画风格)
    """
    prompt = f"""平面矢量插画风格的微信公众号封面图，主题：{theme}。
扁平化设计，几何图形，简洁现代。
{color_scheme}背景，{style}风格。
文章标题：{title}。
21:9横版构图，高质量输出。
专业商务风格，适合企业内容传播，吸引眼球。"""

    return prompt.strip()


def main():
    parser = argparse.ArgumentParser(
        description="Generate WeChat cover photo using Seedream 5.0 API (900x386 flat vector style)"
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Article title",
    )
    parser.add_argument(
        "--theme",
        required=True,
        help="Main theme/topic (e.g., 'AI enterprise automation')",
    )
    parser.add_argument(
        "--style",
        default="flat vector illustration",
        help="Visual style (default: flat vector illustration)",
    )
    parser.add_argument(
        "--color-scheme",
        default="blue gradient",
        help="Color scheme (default: blue gradient)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path (e.g., output/2026-01-19-article-cover.png)",
    )
    parser.add_argument(
        "--model",
        default="doubao-seedream-5-0-260128",
        help="Model to use (default: doubao-seedream-5-0-260128)",
    )
    parser.add_argument(
        "--size",
        default="1536x1024",
        help="Image resolution (default: 1536x1024)",
    )
    parser.add_argument(
        "--aspect-ratio",
        default="3:2",
        help="Aspect ratio (default: 3:2)",
    )
    parser.add_argument(
        "--api-key",
        help="API key (or set SEEDREAM_API_KEY environment variable)",
    )
    parser.add_argument(
        "--glm-api-key",
        help="GLM API key (fallback, or set GLM_API_KEY environment variable)",
    )
    parser.add_argument(
        "--use-glm",
        action="store_true",
        help="Use GLM-Image API instead of Seedream",
    )
    parser.add_argument(
        "--custom-prompt",
        help="Use custom prompt instead of auto-generated one",
    )
    parser.add_argument(
        "--no-resize",
        action="store_true",
        help="Skip resizing to 900x386 (keep original size)",
    )

    args = parser.parse_args()

    # Get API key
    if args.use_glm:
        api_key = args.glm_api_key or os.environ.get("GLM_API_KEY")
        if not api_key:
            print("❌ Error: GLM API key required!")
            print("   Set GLM_API_KEY environment variable or use --glm-api-key argument")
            sys.exit(1)
    else:
        api_key = args.api_key or os.environ.get("SEEDREAM_API_KEY")
        if not api_key:
            # Try to load from credentials file
            cred_path = Path.home() / ".openclaw" / "credentials" / "seedream.json"
            if cred_path.exists():
                with open(cred_path) as f:
                    cred = json.load(f)
                    api_key = cred.get("api_key", "")
            if not api_key:
                print("❌ Error: SEEDREAM_API_KEY required!")
                print("   Set SEEDREAM_API_KEY environment variable or use --api-key argument")
                print("   Or configure ~/.openclaw/credentials/seedream.json")
                sys.exit(1)

    # Build or use custom prompt
    if args.custom_prompt:
        prompt = args.custom_prompt
    else:
        prompt = build_cover_prompt(
            title=args.title,
            theme=args.theme,
            style=args.style,
            color_scheme=args.color_scheme,
        )

    # Initialize generator
    if args.use_glm:
        generator = GLMImageGenerator(api_key)
    else:
        generator = SeedreamImageGenerator(api_key)

    try:
        if args.use_glm:
            result = generator.generate_image(
                prompt=prompt,
                model=args.model,
                size=args.size,
                quality="standard",
            )
        else:
            result = generator.generate_image(
                prompt=prompt,
                model=args.model,
                size=args.size,
                aspect_ratio=args.aspect_ratio,
            )

        # Extract image URL
        image_url = result["data"][0]["url"]

        # Download image
        success = generator.download_image(image_url, args.output)

        if not success:
            print("\n❌ Failed to download image")
            sys.exit(1)

        # Resize to WeChat size (900x386) unless --no-resize flag is set
        if not args.no_resize:
            resize_success = generator.resize_to_wechat(args.output)
            if not resize_success and PIL_AVAILABLE:
                print("⚠️  Warning: Resize failed, but original image was saved")

        print("\n" + "=" * 60)
        print("✅ Cover photo generation completed!")
        print(f"   Output: {args.output}")
        if not args.no_resize and PIL_AVAILABLE:
            print(f"   Size: 900x386 (WeChat standard)")
        print("=" * 60)
        sys.exit(0)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
