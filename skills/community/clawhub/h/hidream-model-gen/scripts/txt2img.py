#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text to Image Generator
Generate images from text prompts using Vivago AI.
"""

import argparse
import json
import logging
import os
import sys
import time
from typing import Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from scripts.vivago_client import create_client
    from scripts.exceptions import MissingCredentialError
except ImportError:
    print("Error: Failed to import required modules. Please ensure you are running from the project root.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def setup_args():
    parser = argparse.ArgumentParser(
        description='Generate images from text using Vivago AI'
    )
    
    parser.add_argument(
        '--prompt', '-p',
        required=True,
        help='Text description of desired image'
    )
    
    parser.add_argument(
        '--negative-prompt', '-np',
        default='',
        help='What to avoid in generation'
    )
    
    parser.add_argument(
        '--wh-ratio', '-r',
        default='16:9',
        choices=['1:1', '4:3', '3:4', '16:9', '9:16'],
        help='Aspect ratio (default: 16:9)'
    )
    
    parser.add_argument(
        '--batch-size', '-b',
        type=int,
        default=1,
        help='Number of images to generate (1-4, default: 1)'
    )
    
    parser.add_argument(
        '--version', '-v',
        default='v3L',
        help='Model version (default: v3L)'
    )

    parser.add_argument(
        '--port',
        default='hidream-txt2img',
        help='Specific port to use (default: hidream-txt2img)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='results.json',
        help='Output file for results (default: results.json)'
    )
    
    parser.add_argument(
        '--token',
        default=os.environ.get('HIDREAM_AUTHORIZATION') or os.environ.get('HIDREAM_TOKEN'),
        help='API token (or set HIDREAM_AUTHORIZATION env var)'
    )
    
    # Advanced parameters
    parser.add_argument(
        '--guidance-scale',
        type=float,
        default=7.5,
        help='Guidance scale (default: 7.5)'
    )
    
    parser.add_argument(
        '--sample-steps',
        type=int,
        default=40,
        help='Sampling steps (default: 40)'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        default=-1,
        help='Random seed (-1 for random, default: -1)'
    )
    
    parser.add_argument(
        '--enhance',
        default='1k',
        choices=['1k', '2k', '4k'],
        help='Enhancement level (default: 1k)'
    )
    
    return parser.parse_args()

def main():
    args = setup_args()
    
    # Validate batch size
    if not 1 <= args.batch_size <= 4:
        logger.error("Batch size must be between 1 and 4")
        sys.exit(1)
    
    # Create client
    try:
        client = create_client(token=args.token)
    except MissingCredentialError:
        print("\nError: API Token not found.")
        print("Please set HIDREAM_AUTHORIZATION environment variable or use --token argument.")
        print("\nTo set it for this session:")
        print('export HIDREAM_AUTHORIZATION="your_token_here"')
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to create client: {e}")
        sys.exit(1)
    
    # Generate images
    print(f"\n🎨 Generating {args.batch_size} image(s)...")
    print(f"   Prompt: {args.prompt}")
    print(f"   Ratio: {args.wh_ratio}")
    print(f"   Model: {args.version}")
    if args.port:
        print(f"   Port: {args.port}")
    
    start_time = time.time()
    try:
        results = client.text_to_image(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            wh_ratio=args.wh_ratio,
            batch_size=args.batch_size,
            version=args.version,
            port=args.port,
            guidance_scale=args.guidance_scale,
            sample_steps=args.sample_steps,
            seed=args.seed,
            enhance=args.enhance
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Generation failed: {e}")
        sys.exit(1)
        
    duration = time.time() - start_time
    
    if not results:
        print("\n❌ Generation failed: No results returned.")
        sys.exit(1)
    
    # Save results
    output_data = {
        'prompt': args.prompt,
        'parameters': {
            'wh_ratio': args.wh_ratio,
            'batch_size': args.batch_size,
            'version': args.version,
            'guidance_scale': args.guidance_scale,
            'sample_steps': args.sample_steps,
            'seed': args.seed,
            'enhance': args.enhance
        },
        'results': results
    }
    
    try:
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\n💾 Results saved to: {args.output}")
    except IOError as e:
        logger.error(f"Failed to save results: {e}")
    
    # Print summary
    print(f"\n✨ Done in {duration:.1f}s")
    
    for i, result in enumerate(results):
        if not isinstance(result, dict):
            print(f"[{i+1}] Invalid result format")
            continue
            
        status = result.get('task_status')
        status_map = {1: '✅ Completed', 3: '❌ Failed', 4: '🚫 Rejected'}
        status_text = status_map.get(status, f'❓ Unknown ({status})')
        
        print(f"\nImage {i+1}: {status_text}")
        if status == 1:
            image_id = result.get('image', '')
            if image_id and image_id.startswith('p_'):
                url = f"https://storage.vivago.ai/image/{image_id}.jpg"
                print(f"   ID:  {image_id}")
                print(f"   URL: {url}")
            elif image_id:
                print(f"   URL: {image_id}")


if __name__ == '__main__':
    main()
