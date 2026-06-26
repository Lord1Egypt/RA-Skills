#!/usr/bin/env python3
"""
Adapter for Seedream T2I (Text-to-Image) Skill.
Strict I/O Discipline:
1. STDIN: JSON Payload
2. STDOUT: Pure JSON Result ONLY
3. STDERR: Logs and Debug info
"""

import sys
import json
import os
import traceback

# Ensure we can import the original scripts
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR) # hidream-api-gen root
sys.path.append(PARENT_DIR)

# Import real Seedream implementation
try:
    from scripts.seedream import run as run_seedream
except ImportError as e:
    sys.path.append(SCRIPT_DIR)
    try:
        from seedream import run as run_seedream
    except ImportError:
        raise RuntimeError(f"Failed to import Seedream script: {e}")

def log_err(msg):
    sys.stderr.write(f"[SeedreamWrapper] {msg}\n")
    sys.stderr.flush()

def main():
    try:
        # 1. Read Input
        input_data = sys.stdin.read()
        if not input_data:
            raise ValueError("Empty input")
            
        payload = json.loads(input_data)
        log_err(f"Received payload: {list(payload.keys())}")
        
        # 2. Extract Params
        prompt = payload.get("prompt")
        negative_prompt = payload.get("negative_prompt", "")
        aspect_ratio = payload.get("aspect_ratio", "16:9")
        
        if not prompt:
            raise ValueError("Missing 'prompt'")
            
        # 3. Call Skill
        log_err("Invoking Seedream T2I...")
        api_result = run_seedream(
            version="M2", # Default
            prompt=prompt,
            negative_prompt=negative_prompt,
            resolution="2048*1152" # 16:9 equivalent
        )
        
        # 4. Validate
        if api_result.get("code") != 0:
            raise RuntimeError(f"Seedream API Error: {api_result.get('message')}")
            
        works_result = api_result.get("data", {}).get("works_result", [])
        if not works_result:
            raise RuntimeError("No works_result returned")
            
        image_url = works_result[0].get("url")
        
        # 5. Output Success
        output = {
            "status": "success",
            "image_url": image_url,
            "aspect_ratio": aspect_ratio
        }
        print(json.dumps(output))
        sys.exit(0)

    except Exception as e:
        # 6. Global Error Handler
        log_err(f"CRITICAL ERROR: {str(e)}")
        log_err(traceback.format_exc())
        
        error_output = {
            "status": "error",
            "error_type": type(e).__name__,
            "message": str(e)
        }
        print(json.dumps(error_output))
        sys.exit(1)

if __name__ == "__main__":
    main()
