#!/usr/bin/env python3
"""
Adapter for Kling I2V (Image-to-Video) Skill.
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

# Import real Kling implementation
# Note: The original scripts use relative imports like 'from common.base_video import ...'
# So we need the parent dir in sys.path.
try:
    from scripts.kling import run as run_kling
except ImportError as e:
    # If direct import fails (e.g. structure mismatch), try adding scripts dir explicitly
    sys.path.append(SCRIPT_DIR)
    try:
        from kling import run as run_kling
    except ImportError:
        raise RuntimeError(f"Failed to import Kling script: {e}")

def log_err(msg):
    """Write to stderr to avoid polluting stdout."""
    sys.stderr.write(f"[KlingWrapper] {msg}\n")
    sys.stderr.flush()

def main():
    try:
        # 1. Read Payload from STDIN
        input_data = sys.stdin.read()
        if not input_data:
            raise ValueError("Empty input from stdin")
            
        payload = json.loads(input_data)
        log_err(f"Received payload: {list(payload.keys())}")
        
        # 2. Extract Parameters
        prompt = payload.get("prompt")
        image_input = payload.get("image_input")
        duration = payload.get("duration", 5) # 5 or 10
        
        if not prompt or not image_input:
            raise ValueError("Missing required fields: 'prompt' and 'image_input'")

        # 3. Call Underlying Skill
        # Note: 'image_input' is passed as 'images' to Kling
        log_err(f"Invoking Kling I2V (Duration: {duration}s)...")
        
        # Determine model version based on duration/tier
        version = "Q2.5T-std" # Default
        
        # Real call
        api_result = run_kling(
            version=version,
            prompt=prompt,
            images=image_input,
            duration=duration,
            wh_ratio="16:9" # Default for I2V if needed
        )
        
        # 4. Parse & Validate Result
        if api_result.get("code") != 0:
            raise RuntimeError(f"Kling API Error: {api_result.get('message')}")
            
        task_data = api_result.get("data", {})
        works_result = task_data.get("works_result", [])
        
        if not works_result:
            raise RuntimeError("Kling API returned no works_result")
            
        video_url = works_result[0].get("url")
        
        # 5. Output Standard JSON to STDOUT
        output = {
            "status": "success",
            "video_url": video_url,
            "task_id": task_data.get("task_id"),
            "duration_requested": duration
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
        sys.exit(1) # Non-zero exit code triggers CircuitBreaker

if __name__ == "__main__":
    main()
