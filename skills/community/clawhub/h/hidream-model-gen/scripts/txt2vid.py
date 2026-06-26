#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text to Video Generator
Generate videos from text prompts using Vivago AI.
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
        description='Generate videos from text using Vivago AI'
    )
    
    parser.add_argument(
        '--prompt', '-p',
        required=True,
        help='Text description of desired video'
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
        '--duration', '-d',
        type=int,
        default=5,
        choices=[5, 10],
        help='Video duration in seconds (default: 5)'
    )
    
    parser.add_argument(
        '--port',
        default='v3Pro',
        help='Specific port to use (v3Pro, v3L, kling-video)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='video_results.json',
        help='Output file for results (default: video_results.json)'
    )
    
    parser.add_argument(
        '--token',
        default=os.environ.get('HIDREAM_AUTHORIZATION') or os.environ.get('HIDREAM_TOKEN'),
        help='API token (or set HIDREAM_AUTHORIZATION env var)'
    )
    
    return parser.parse_args()

def main():
    args = setup_args()
    
    # Create client
    try:
        client = create_client(token=args.token)
    except MissingCredentialError:
        print("\nError: API Token not found.")
        print("Please set HIDREAM_AUTHORIZATION environment variable or use --token argument.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to create client: {e}")
        sys.exit(1)
    
    # Generate video
    print(f"\n🎥 Generating video...")
    print(f"   Prompt: {args.prompt}")
    print(f"   Ratio: {args.wh_ratio}")
    print(f"   Port: {args.port}")
    print(f"   Duration: {args.duration}s")
    
    start_time = time.time()
    try:
        results = client.text_to_video(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            wh_ratio=args.wh_ratio,
            duration=args.duration,
            port=args.port
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
            'duration': args.duration,
            'port': args.port
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
        status = result.get('task_status')
        status_map = {1: '✅ Completed', 3: '❌ Failed', 4: '🚫 Rejected'}
        status_text = status_map.get(status, f'❓ Unknown ({status})')
        
        print(f"\nVideo {i+1}: {status_text}")
        if status == 1:
            video_id = result.get('video', '')
            if video_id:
                # Remove 'v_' prefix if present, but don't append .mp4 if it already has it
                clean_id = video_id[2:] if video_id.startswith('v_') else video_id
                url = f"https://media.vivago.ai/{clean_id}"
                if not url.endswith('.mp4'):
                    url += '.mp4'
                print(f"   ID:  {video_id}")
                print(f"   URL: {url}")

if __name__ == '__main__':
    main()
