#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiniMax Image Generation Tool (Text-to-Image & Image-to-Image)

Usage:
    python3 minimax_image_gen.py "your prompt"           # t2i: text-to-image
    python3 minimax_image_gen.py "transform style" --image-url "https://..."  # i2i: image-to-image
    python3 minimax_image_gen.py "your prompt" --model image-01 --aspect-ratio 16:9 --n 2
    python3 minimax_image_gen.py "your prompt" --save output.png
    python3 minimax_image_gen.py tools
"""

import os
import sys
import json
import argparse
import requests

API_HOST = 'api.minimaxi.com'
ENDPOINT = '/v1/image_generation'


def get_api_key():
    """Get API key from environment or skill config."""
    # Try environment first
    key = os.environ.get('MINIMAX_API_KEY')
    if key:
        return key

    # Try to read from skill config
    config_path = os.path.expanduser('~/.openclaw/openclaw.json')
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                config = json.load(f)
            entries = config.get('skills', {}).get('entries', {})
            key = entries.get('minimax-image-generator', {}).get('apiKey')
            if key:
                return key
        except Exception:
            pass

    return None


def make_request(data: dict) -> dict:
    """Make request to MiniMax Image Generation API."""
    key = get_api_key()
    if not key:
        raise Exception(
            'MINIMAX_API_KEY not set. '
            'Set via environment or openclaw config: '
            'openclaw config set skills.entries.minimax-image-generator.apiKey "sk-your-key"'
        )

    url = f'https://{API_HOST}{ENDPOINT}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {key}'
    }
    response = requests.post(url, json=data, headers=headers, timeout=120)
    response.raise_for_status()
    return response.json()


def generate_image(
    prompt: str,
    model: str = "image-01",
    image_url: str = None,
    image_base64: str = None,
    style_type: str = None,
    style_weight: float = 0.8,
    aspect_ratio: str = "1:1",
    width: int = None,
    height: int = None,
    response_format: str = "url",
    seed: int = None,
    n: int = 1,
    prompt_optimizer: bool = False,
    aigc_watermark: bool = False
) -> dict:
    """
    Generate image(s) from text prompt or transform reference images using MiniMax API.

    Args:
        prompt: Image description text (max 1500 chars)
        model: Model name - "image-01" or "image-01-live"
        image_url: Reference image URL for image-to-image (i2i). Supports public URLs.
        image_base64: Reference image as base64 Data URL for i2i. Format: data:image/jpeg;base64,...
        style_type: Style type (only for image-01-live): "漫画", "元气", "中世纪", "水彩"
        style_weight: Style weight (0, 1], default 0.8
        aspect_ratio: Image ratio - "1:1", "16:9", "4:3", "3:2", "2:3", "3:4", "9:16", "21:9"
        width: Image width in pixels [512, 2048], must be multiple of 8
        height: Image height in pixels [512, 2048], must be multiple of 8
        response_format: Return format - "url" or "base64"
        seed: Random seed for reproducibility
        n: Number of images to generate [1, 9]
        prompt_optimizer: Enable auto prompt optimization
        aigc_watermark: Add watermark to generated image

    Returns:
        dict with success status, image URLs/base64, and metadata
    """
    if not prompt:
        return {'error': 'Missing required parameter: prompt'}

    if len(prompt) > 1500:
        return {'error': 'Prompt exceeds 1500 character limit'}

    data = {
        'model': model,
        'prompt': prompt,
        'aspect_ratio': aspect_ratio,
        'response_format': response_format,
        'n': n,
        'prompt_optimizer': prompt_optimizer,
        'aigc_watermark': aigc_watermark
    }

    # Add subject_reference for image-to-image (i2i)
    if image_url or image_base64:
        image_file = image_base64 if image_base64 else image_url
        data['subject_reference'] = [
            {
                'type': 'character',
                'image_file': image_file
            }
        ]

    # Add style for image-01-live
    if model == 'image-01-live' and style_type:
        data['style'] = {
            'style_type': style_type,
            'style_weight': style_weight
        }

    # Use width/height if explicitly provided
    if width and height:
        data['width'] = width
        data['height'] = height

    # Add seed if provided
    if seed is not None:
        data['seed'] = seed

    try:
        response = make_request(data)

        # Parse response
        base_resp = response.get('base_resp', {})
        status_code = base_resp.get('status_code', 0)

        if status_code != 0:
            return {
                'error': f"API error {status_code}: {base_resp.get('status_msg', 'Unknown error')}"
            }

        result = {
            'success': True,
            'id': response.get('id'),
            'model': model,
            'prompt': prompt,
            'metadata': response.get('metadata', {}),
        }

        # Extract images
        data_obj = response.get('data', {})
        if response_format == 'url':
            result['image_urls'] = data_obj.get('image_urls', [])
        else:
            result['image_base64'] = data_obj.get('image_base64', [])

        return result

    except requests.exceptions.Timeout:
        return {'error': 'Request timeout - generation may take longer, please try again'}
    except requests.exceptions.RequestException as e:
        return {'error': f'Request failed: {str(e)}'}
    except Exception as e:
        return {'error': str(e)}


def list_tools() -> dict:
    """Return available tools in OpenClaw skill format."""
    return {
        'tools': [
            {
                'name': 'minimax_image_gen',
                'description': 'Text-to-image generation using MiniMax API - creates images from text descriptions',
                'inputSchema': {
                    'type': 'object',
                    'properties': {
                        'prompt': {
                            'type': 'string',
                            'description': 'Image description text, max 1500 characters'
                        },
                        'model': {
                            'type': 'string',
                            'enum': ['image-01', 'image-01-live'],
                            'default': 'image-01',
                            'description': 'Model name: image-01 (default) or image-01-live'
                        },
                        'image_url': {
                            'type': 'string',
                            'description': 'Reference image URL for image-to-image (i2i)'
                        },
                        'image_base64': {
                            'type': 'string',
                            'description': 'Reference image as base64 Data URL for i2i'
                        },
                        'aspect_ratio': {
                            'type': 'string',
                            'enum': ['1:1', '16:9', '4:3', '3:2', '2:3', '3:4', '9:16', '21:9'],
                            'default': '1:1',
                            'description': 'Image aspect ratio'
                        },
                        'style_type': {
                            'type': 'string',
                            'enum': ['漫画', '元气', '中世纪', '水彩'],
                            'description': 'Style type (only for image-01-live)'
                        },
                        'n': {
                            'type': 'integer',
                            'minimum': 1,
                            'maximum': 9,
                            'default': 1,
                            'description': 'Number of images to generate'
                        },
                        'response_format': {
                            'type': 'string',
                            'enum': ['url', 'base64'],
                            'default': 'url',
                            'description': 'Return format: url or base64'
                        },
                        'prompt_optimizer': {
                            'type': 'boolean',
                            'default': False,
                            'description': 'Enable auto prompt optimization'
                        }
                    },
                    'required': ['prompt']
                }
            }
        ]
    }


DEFAULT_SAVE_DIR = os.path.expanduser('~/.openclaw/workspace/tmp')


def save_image_from_url(url: str, filepath: str = None) -> tuple:
    """
    Download image from URL and save to file.
    
    Args:
        url: Image URL to download
        filepath: Save path. If None, generates a filename in default save dir.
        
    Returns:
        tuple: (success: bool, filepath_or_error: str)
    """
    try:
        # Ensure save directory exists
        os.makedirs(DEFAULT_SAVE_DIR, exist_ok=True)
        
        # Generate filename if not provided
        if not filepath:
            import time
            filename = f"img_{int(time.time()*1000)}.png"
            filepath = os.path.join(DEFAULT_SAVE_DIR, filename)
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return (True, filepath)
    except Exception as e:
        return (False, str(e))


def main():
    parser = argparse.ArgumentParser(
        description='MiniMax Text-to-Image Generation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s "a beautiful sunset over ocean"
  %(prog)s "a cat" --model image-01-live --style-type 漫画 --n 2
  %(prog)s "architecture" --aspect-ratio 16:9 --save output.png
  %(prog)s tools
        '''
    )

    parser.add_argument('prompt', nargs='?', help='Image description text')
    parser.add_argument('--model', default='image-01',
                        choices=['image-01', 'image-01-live'],
                        help='Model name (default: image-01, image-01-live requires premium plan)')
    parser.add_argument('--image-url',
                        help='Reference image URL for image-to-image (i2i)')
    parser.add_argument('--image-base64',
                        help='Reference image as base64 Data URL for i2i')
    parser.add_argument('--style-type',
                        choices=['漫画', '元气', '中世纪', '水彩'],
                        help='Style type (only for image-01-live)')
    parser.add_argument('--style-weight', type=float, default=0.8,
                        help='Style weight 0-1 (default: 0.8)')
    parser.add_argument('--aspect-ratio', default='1:1',
                        choices=['1:1', '16:9', '4:3', '3:2', '2:3', '3:4', '9:16', '21:9'],
                        help='Aspect ratio (default: 1:1)')
    parser.add_argument('--width', type=int, help='Image width [512-2048]')
    parser.add_argument('--height', type=int, help='Image height [512-2048]')
    parser.add_argument('--response-format', default='url',
                        choices=['url', 'base64'],
                        help='Response format (default: url)')
    parser.add_argument('--seed', type=int, help='Random seed')
    parser.add_argument('--n', type=int, default=1,
                        help='Number of images [1-9] (default: 1)')
    parser.add_argument('--prompt-optimizer', action='store_true',
                        help='Enable prompt optimization')
    parser.add_argument('--watermark', action='store_true',
                        help='Add AIGC watermark')
    parser.add_argument('--save', nargs='?', const=True, help='Save first image to file (default: ~/.openclaw/workspace/tmp/)')
    parser.add_argument('--tools', action='store_true',
                        help='List available tools in JSON format')

    args = parser.parse_args()

    if args.tools:
        print(json.dumps(list_tools(), ensure_ascii=False, indent=2))
        return

    if not args.prompt:
        parser.print_help()
        sys.exit(1)

    result = generate_image(
        prompt=args.prompt,
        model=args.model,
        image_url=args.image_url,
        image_base64=args.image_base64,
        style_type=args.style_type,
        style_weight=args.style_weight,
        aspect_ratio=args.aspect_ratio,
        width=args.width,
        height=args.height,
        response_format=args.response_format,
        seed=args.seed,
        n=args.n,
        prompt_optimizer=args.prompt_optimizer,
        aigc_watermark=args.watermark
    )

    if result.get('success'):
        print(json.dumps(result, ensure_ascii=False, indent=2))

        # Save first image if requested
        if result.get('image_urls') and args.save is not None:
            first_url = result['image_urls'][0]
            # If --save specified without path (True), use default directory
            # If --save has a value, use that path
            save_path = None if args.save is True else args.save
            success, filepath = save_image_from_url(first_url, save_path)
            if success:
                print(f'\n✅ Image saved to: {filepath}')
            else:
                print(f'\n❌ Failed to save image: {filepath}')
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == '__main__':
    main()
