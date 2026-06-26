#!/usr/bin/env python3
"""
OpenLens CLI - Command Line Interface for AI Video Generation
Raw transparency: no content filtering, pure pass-through to your API.
"""

import argparse
import json
import os
import sys
import time
import requests
from tqdm import tqdm

# Get skill directory
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SKILL_DIR, "config.json")
DEFAULT_SAVE_PATH = "./outputs"
DEFAULT_MODEL = "wan2.2"

# ============================================================
# CONFIGURATION
# ============================================================

def load_config():
    """Load configuration from config.json"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    """Save configuration to config.json"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

REFINER_SYSTEM_PROMPT = """You are a top-tier AI video director. Transform the user's description into a professional, cinematic video prompt.

Requirements:
- Enhance with visual details: lighting, camera angles, color grading, atmosphere
- Add motion dynamics: movements, transitions, physics-based animations
- Include technical quality terms: high quality, detailed, 4K, cinematic
- Output ONLY the refined prompt, NO explanations"""

def log_msg(msg):
    """Print log message with timestamp"""
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def refine_prompt(api_url, api_key, model, user_prompt, image_url=None):
    """Call Text API to refine the prompt"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    if image_url:
        messages = [
            {"role": "system", "content": REFINER_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_url}},
                    {"type": "text", "text": f"Original: {user_prompt}"}
                ]
            }
        ]
    else:
        messages = [
            {"role": "system", "content": REFINER_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    
    payload = {"model": model, "messages": messages, "temperature": 0.7, "max_tokens": 500}
    
    for endpoint in [f"{api_url}/chat/completions", f"{api_url}/responses"]:
        try:
            resp = requests.post(endpoint, headers=headers, json=payload, timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                if "choices" in data:
                    return data["choices"][0]["message"]["content"]
                elif "output" in data:
                    return data["output"][0]["content"][0]["text"]
        except Exception as e:
            log_msg(f"API error: {e}")
            continue
    
    return None

def submit_video_task(api_url, api_key, prompt, image_url=None, resolution="720p", duration=5, model=None):
    """Submit video generation task"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Use custom model or default
    if model is None or model == "":
        model = DEFAULT_MODEL
    
    payload = {
        "model": model,
        "input": {"prompt": prompt},
        "parameters": {"size": resolution, "duration": duration}
    }
    
    if image_url:
        payload["input"]["img_url"] = image_url
    
    log_msg(f"Submitting to {api_url}/video/generations...")
    resp = requests.post(f"{api_url}/video/generations", headers=headers, json=payload, timeout=30)
    
    if resp.status_code == 200:
        data = resp.json()
        return data.get("task_id"), data.get("status")
    return None, None

def poll_task_status(api_url, api_key, task_id, max_attempts=120):
    """Poll task status until complete"""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    for attempt in range(max_attempts):
        try:
            resp = requests.get(f"{api_url}/video/generations/{task_id}", headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                status = data.get("status")
                progress = data.get("progress_percent", 0)
                
                log_msg(f"Status: {status} ({progress}%)")
                
                if status == "SUCCEED":
                    return data.get("videos", [{}])[0].get("video_url")
                elif status == "FAILED":
                    return None
                
                time.sleep(5)
        except Exception as e:
            log_msg(f"Poll error: {e}")
            time.sleep(5)
    
    return None

def download_video(video_url, output_path, show_progress=True):
    """Download video using streaming for large files"""
    log_msg(f"Downloading to: {output_path}")
    
    response = requests.get(video_url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    
    with open(output_path, 'wb') as f, tqdm(
        desc="Downloading",
        total=total_size,
        unit='B',
        unit_scale=True,
        disable=not show_progress
    ) as pbar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                pbar.update(len(chunk))
    
    log_msg(f"Saved: {output_path}")
    return output_path

# ============================================================
# MAIN CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="OpenLens CLI - AI Video Generation")
    parser.add_argument("--prompt", "-p", required=True, help="Video description prompt")
    parser.add_argument("--image_url", "-i", default="", help="Image URL for I2V")
    parser.add_argument("--model", "-m", default="", help="Video model ID (e.g., wan2.2, seedance1.5, wan2.6-i2v)")
    parser.add_argument("--output", "-o", default="", help="Output file path")
    parser.add_argument("--refine", "-r", action="store_true", help="Enable prompt refinement")
    parser.add_argument("--resolution", default="720p", help="Video resolution (720p, 1080p)")
    parser.add_argument("--duration", type=int, default=5, help="Video duration (5, 10, 15)")
    parser.add_argument("--config", "-c", default="", help="Custom config file")
    
    args = parser.parse_args()
    
    # Load config
    config = load_config()
    if args.config and os.path.exists(args.config):
        with open(args.config, 'r') as f:
            config = json.load(f)
    
    # Get API credentials
    video_api_url = config.get("video_api_url", "")
    video_api_key = config.get("video_api_key", "")
    text_api_url = config.get("text_api_url", "")
    text_api_key = config.get("text_api_key", "")
    text_model = config.get("text_model", "")
    save_path = config.get("default_save_path", DEFAULT_SAVE_PATH)
    
    # Validate
    if not video_api_url or not video_api_key:
        log_msg("Error: Video API URL and Key are required")
        log_msg("Run with --video_api_url and --video_api_key or set in config")
        sys.exit(1)
    
    log_msg("="*50)
    log_msg("OpenLens CLI - Video Generation")
    log_msg("="*50)
    
    # Step 1: Prompt refinement
    final_prompt = args.prompt
    if args.refine:
        if not text_api_url or not text_api_key or not text_model:
            log_msg("Refine enabled but Text API not configured. Using original prompt.")
        else:
            log_msg("Refining prompt...")
            refined = refine_prompt(text_api_url, text_api_key, text_model, args.prompt, args.image_url or None)
            if refined:
                final_prompt = refined
                log_msg(f"Refined: {final_prompt[:100]}...")
            else:
                log_msg("Refinement failed, using original")
    
    # Step 2: Submit video task
    log_msg("Submitting video generation task...")
    image_url = args.image_url if args.image_url else None
    
    # Determine model - use custom if provided, otherwise use default
    if args.model:
        video_model = args.model
    else:
        video_model = DEFAULT_MODEL
    
    log_msg(f"Using model: {video_model}")
    task_id, status = submit_video_task(video_api_url, video_api_key, final_prompt, image_url, args.resolution, args.duration, video_model)
    
    if not task_id:
        log_msg("Failed to submit task")
        sys.exit(1)
    
    log_msg(f"Task submitted: {task_id}")
    
    # Step 3: Poll for result
    log_msg("Waiting for video generation...")
    video_url = poll_task_status(video_api_url, video_api_key, task_id)
    
    if not video_url:
        log_msg("Video generation failed or timed out")
        sys.exit(1)
    
    log_msg("Video ready!")
    
    # Step 4: Download
    if not args.output:
        os.makedirs(save_path, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        args.output = os.path.join(save_path, f"video_{timestamp}.mp4")
    
    download_video(video_url, args.output)
    
    log_msg("="*50)
    log_msg("Generation complete!")
    log_msg(f"File: {args.output}")
    log_msg("="*50)

if __name__ == "__main__":
    main()
