#!/usr/bin/env python3
"""
music-gen.py - Generate instrumental music via Google Lyria API (Vertex AI)
Strictly follows: https://ai.google.dev/gemini-api/docs/music-generation

Pure functional script - no hardcoded credentials.
Configuration via JSON config file + CLI arguments.
"""

import requests
import base64
import sys
import json
import os
from datetime import datetime


def load_config(config_path: str) -> dict:
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in config file: {e}", file=sys.stderr)
        sys.exit(1)


def generate_music(project_id: str, location: str, prompt: str, token: str, output_dir: str, name: str = None, sample_count: int = 1) -> list:
    """
    Generate music using Lyria API.
    
    Args:
        project_id: Google Cloud project ID
        location: Vertex AI location (e.g., us-central1)
        prompt: Text description of desired music
        token: Bearer token for authentication
        output_dir: Directory to save the generated WAV file(s)
        name: Optional custom filename base (without extension). If None, uses timestamp.
        sample_count: Number of samples to generate (default: 1)
    
    Returns:
        List of paths to generated WAV files
    """
    # Build endpoint URL per Vertex AI Lyria docs
    url = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/publishers/google/models/lyria-002:predict"
    
    # Headers per API spec
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Request body per Lyria API spec
    data = {
        "instances": [
            {
                "prompt": prompt
            }
        ],
        "parameters": {
            "sample_count": sample_count
        }
    }
    
    print(f"Sending request to Lyria API...")
    print(f"Prompt: {prompt}")
    print(f"Sample count: {sample_count}")
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}", file=sys.stderr)
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    
    # Parse response
    result = response.json()
    
    if "predictions" not in result or not result["predictions"]:
        print("Error: No predictions in response", file=sys.stderr)
        print(f"Response: {json.dumps(result, indent=2)}", file=sys.stderr)
        sys.exit(1)
    
    # Debug: show how many predictions received
    predictions = result["predictions"]
    print(f"Received {len(predictions)} prediction(s) from API")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    generated_files = []
    
    for i, prediction in enumerate(predictions):
        # Extract audio content (base64 encoded WAV)
        audio_content = prediction.get("bytesBase64Encoded") or prediction.get("audioContent")
        
        if not audio_content:
            print(f"Error: No audio content in prediction {i+1}. Keys: {list(prediction.keys())}", file=sys.stderr)
            continue
        
        # Generate filename
        if name:
            # Sanitize filename: replace spaces and special chars
            safe_name = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in name)
            if len(predictions) > 1:
                filename = f"{safe_name}_{i+1}.wav"
            else:
                filename = f"{safe_name}.wav"
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if len(predictions) > 1:
                filename = f"music_{timestamp}_{i+1}.wav"
            else:
                filename = f"music_{timestamp}.wav"
        
        output_file = os.path.join(output_dir, filename)
        
        # Decode and save
        with open(output_file, "wb") as f:
            f.write(base64.b64decode(audio_content))
        
        print(f"Generated: {output_file} (30s 48kHz instrumental)")
        generated_files.append(output_file)
    
    return generated_files


def main():
    if len(sys.argv) < 3:
        print("Usage: python music-gen.py <config_file> <prompt> [name] [sample_count]", file=sys.stderr)
        print("", file=sys.stderr)
        print("Arguments:", file=sys.stderr)
        print("  config_file   - Path to JSON config with project_id, location, bearer_token, output_dir", file=sys.stderr)
        print("  prompt        - Text description of desired music", file=sys.stderr)
        print("  name          - Optional: custom filename base (no extension)", file=sys.stderr)
        print("  sample_count  - Optional: number of samples to generate (default: 1)", file=sys.stderr)
        print("", file=sys.stderr)
        print("Example:", file=sys.stderr)
        print("  python music-gen.py ~/.openclaw/workspace/lyria/config.json 'chill piano' 'my_song' 3", file=sys.stderr)
        sys.exit(1)
    
    config_path = sys.argv[1]
    prompt = sys.argv[2]
    name = sys.argv[3] if len(sys.argv) > 3 else None
    sample_count = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    
    # Load config - contains all credentials and settings
    config = load_config(config_path)
    project_id = config.get("project_id")
    location = config.get("location")
    token = config.get("bearer_token")
    output_dir = config.get("output_dir")
    
    # Validate config
    missing = []
    if not project_id:
        missing.append("project_id")
    if not location:
        missing.append("location")
    if not token:
        missing.append("bearer_token")
    if not output_dir:
        missing.append("output_dir")
    
    if missing:
        print(f"Error: Config file missing required fields: {', '.join(missing)}", file=sys.stderr)
        print(f"Config file: {config_path}", file=sys.stderr)
        sys.exit(1)
    
    outputs = generate_music(project_id, location, prompt, token, output_dir, name, sample_count)
    print(f"Success: Generated {len(outputs)} file(s)")
    for f in outputs:
        print(f"  - {f}")


if __name__ == "__main__":
    main()
