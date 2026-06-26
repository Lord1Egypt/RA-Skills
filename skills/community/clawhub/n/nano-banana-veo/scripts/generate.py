#!/usr/bin/env python3
"""
Nano Banana + Veo Workflow Script
Generates images using Gemini 3 Pro Image (Nano Banana) and animates them using Veo 3.1
"""
import os
import sys
import json
import time
import base64
import argparse
from pathlib import Path

def get_api_key():
    """Get Gemini API key from environment"""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("ERROR: GEMINI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    return api_key

def generate_image(prompt, output_path, resolution="1K", aspect_ratio=None):
    """Generate image using Nano Banana (Gemini 3 Pro Image)"""
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=get_api_key())
        
        # Build generation config
        config = types.GenerateContentConfig()
        
        # Handle resolution and aspect ratio
        if resolution:
            config.response_modalities = ["IMAGE"]
        
        print(f"Generating image with prompt: {prompt[:60]}...")
        
        response = client.models.generate_content(
            model='gemini-3-pro-image-preview',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(image_size=resolution)
            )
        )
        
        # Extract image from response
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_data = part.inline_data.data
                    with open(output_path, 'wb') as f:
                        f.write(image_data)
                    print(f"✅ Image saved to: {output_path}")
                    return output_path
        
        print("ERROR: No image data in response", file=sys.stderr)
        return None
        
    except ImportError:
        print("ERROR: google-genai not installed. Run: pip install google-genai", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR generating image: {e}", file=sys.stderr)
        return None

def generate_video_from_image(image_path, video_prompt, output_path, duration=4, resolution="720p"):
    """Generate video using Veo 3.1 from an image"""
    try:
        import requests
        
        api_key = get_api_key()
        
        # Read and encode image
        with open(image_path, 'rb') as f:
            image_b64 = base64.b64encode(f.read()).decode('utf-8')
        
        # Start video generation
        url = "https://generativelanguage.googleapis.com/v1beta/models/veo-3.1-generate-preview:predictLongRunning"
        headers = {
            "x-goog-api-key": api_key,
            "Content-Type": "application/json"
        }
        data = {
            "instances": [{
                "prompt": video_prompt,
                "image": {
                    "bytesBase64Encoded": image_b64,
                    "mimeType": "image/png" if image_path.endswith('.png') else "image/jpeg"
                }
            }],
            "parameters": {
                "sampleCount": 1,
                "resolution": resolution,
                "aspectRatio": "16:9",
                "durationSeconds": max(4, min(8, duration))  # Veo requires 4-8 seconds
            }
        }
        
        print(f"Starting Veo video generation (duration: {duration}s)...")
        response = requests.post(url, headers=headers, json=data, timeout=120)
        result = response.json()
        
        if response.status_code != 200:
            print(f"ERROR: {response.status_code} - {result}", file=sys.stderr)
            return None
        
        operation_name = result.get('name')
        if not operation_name:
            print("ERROR: No operation name returned", file=sys.stderr)
            return None
        
        print(f"Operation started: {operation_name}")
        
        # Poll for completion (max 10 minutes)
        poll_url = f"https://generativelanguage.googleapis.com/v1beta/{operation_name}"
        
        for i in range(60):  # 60 attempts, 10s each = 10 min max
            time.sleep(10)
            print(f"Poll {i+1}/60...")
            
            poll_response = requests.get(poll_url, headers={"x-goog-api-key": api_key}, timeout=30)
            poll_result = poll_response.json()
            
            if poll_result.get('done'):
                print("✅ Video generation complete!")
                
                # Extract video URL
                outputs = poll_result.get('response', {}).get('generateVideoResponse', {}).get('generatedSamples', [])
                if outputs:
                    video_uri = outputs[0].get('video', {}).get('uri')
                    if video_uri:
                        print(f"Downloading video from: {video_uri[:60]}...")
                        video_response = requests.get(video_uri, headers={"x-goog-api-key": api_key}, timeout=60)
                        with open(output_path, 'wb') as f:
                            f.write(video_response.content)
                        print(f"✅ Video saved to: {output_path}")
                        return output_path
                
                print("ERROR: Video URI not found in response", file=sys.stderr)
                return None
            else:
                print("  Still processing...")
        
        print("⚠️ Timeout waiting for video generation", file=sys.stderr)
        return None
        
    except ImportError:
        print("ERROR: requests not installed. Run: pip install requests", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR generating video: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description='Nano Banana + Veo Workflow')
    parser.add_argument('--image-prompt', required=True, help='Prompt for image generation')
    parser.add_argument('--video-prompt', help='Prompt for video animation (if not provided, defaults to image prompt)')
    parser.add_argument('--output-image', required=True, help='Output path for generated image')
    parser.add_argument('--output-video', help='Output path for generated video (optional)')
    parser.add_argument('--resolution', default='1K', choices=['1K', '2K', '4K'], help='Image resolution')
    parser.add_argument('--video-duration', type=int, default=4, help='Video duration in seconds (4-8)')
    parser.add_argument('--video-resolution', default='720p', choices=['720p', '1080p', '4k'], help='Video resolution')
    
    args = parser.parse_args()
    
    # Generate image
    image_result = generate_image(
        prompt=args.image_prompt,
        output_path=args.output_image,
        resolution=args.resolution
    )
    
    if not image_result:
        sys.exit(1)
    
    # Generate video if requested
    if args.output_video:
        video_prompt = args.video_prompt or f"{args.image_prompt} - animated, smooth motion, cinematic"
        video_result = generate_video_from_image(
            image_path=args.output_image,
            video_prompt=video_prompt,
            output_path=args.output_video,
            duration=args.video_duration,
            resolution=args.video_resolution
        )
        
        if not video_result:
            sys.exit(1)
        
        print(f"\n✅ Workflow complete!")
        print(f"   Image: {args.output_image}")
        print(f"   Video: {args.output_video}")
    else:
        print(f"\n✅ Image generation complete: {args.output_image}")

if __name__ == '__main__':
    main()
