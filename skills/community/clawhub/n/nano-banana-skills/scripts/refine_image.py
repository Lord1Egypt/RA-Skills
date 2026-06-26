#!/usr/bin/env python3
"""Multi-turn image refinement using conversation history."""

import argparse
import base64
import json
import os
import sys
import requests

# Model configurations (same as generate_image.py)
MODELS = {
    "nano-banana": {
        "id": "gemini-2.5-flash-image",
        "name": "Nano Banana (Cheapest)",
        "cost": "low"
    },
    "nano-banana-2": {
        "id": "gemini-3.1-flash-image-preview",
        "name": "Nano Banana 2 (Best Value)",
        "cost": "medium"
    },
    "nano-banana-pro": {
        "id": "gemini-3-pro-image-preview",
        "name": "Nano Banana Pro (Best Quality)",
        "cost": "high"
    }
}

def load_conversation(history_file):
    """Load conversation history from JSON file."""
    if not os.path.exists(history_file):
        return []
    with open(history_file, "r") as f:
        return json.load(f)

def save_conversation(history_file, contents):
    """Save conversation history to JSON file."""
    with open(history_file, "w") as f:
        json.dump(contents, f, indent=2)

def refine_image(prompt, history_file="conversation.json", output_path="refined_image.png", 
                 model=None, quality_priority=False):
    """Refine an image based on conversation history."""
    
    api_key = os.getenv("WISGATE_KEY")
    if not api_key:
        print("Error: WISGATE_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    # Auto-select model if not specified
    if not model:
        model = MODELS["nano-banana-pro"]["id"] if quality_priority else MODELS["nano-banana-2"]["id"]
    
    api_url = f"https://api.wisgate.ai/v1beta/models/{model}:generateContent"
    
    headers = {
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    # Load existing conversation
    contents = load_conversation(history_file)
    
    # Add new user prompt
    contents.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })
    
    payload = {
        "contents": contents,
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }
    
    print(f"Using model: {model}", file=sys.stderr)
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        
        # Extract model response
        model_parts = result["candidates"][0]["content"]["parts"]
        
        # Add model response to conversation
        contents.append({
            "role": "model",
            "parts": model_parts
        })
        
        # Save updated conversation
        save_conversation(history_file, contents)
        
        # Extract and save image
        for part in model_parts:
            if "inlineData" in part:
                image_data = part["inlineData"]["data"]
                mime_type = part["inlineData"].get("mimeType", "image/png")
                
                # Auto-detect extension if output_path doesn't have one
                if "." not in os.path.basename(output_path):
                    extension = mime_type.split("/")[1]
                    output_path = f"{output_path}.{extension}"
                
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(image_data))
                print(f"Image saved to: {output_path}")
                print(f"Conversation saved to: {history_file}")
                return
        
        print("Error: No image data found in response", file=sys.stderr)
        sys.exit(1)
        
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-turn image refinement")
    parser.add_argument("prompt", help="Refinement instruction or initial prompt")
    parser.add_argument("--history", default="conversation.json",
                       help="Conversation history file (default: conversation.json)")
    parser.add_argument("--output", default="refined_image.png",
                       help="Output file path (default: refined_image.png)")
    parser.add_argument("--reset", action="store_true",
                       help="Reset conversation history and start fresh")
    parser.add_argument("--model", choices=["nano-banana", "nano-banana-2", "nano-banana-pro"],
                       help="Force specific model (auto-select if not specified)")
    parser.add_argument("--quality", action="store_true",
                       help="Prioritize quality over cost (uses Nano Banana Pro)")
    
    args = parser.parse_args()
    
    # Reset history if requested
    if args.reset and os.path.exists(args.history):
        os.remove(args.history)
        print(f"Conversation history reset: {args.history}")
    
    # Convert model alias to actual model ID
    model_id = None
    if args.model:
        model_id = MODELS[args.model]["id"]
    
    refine_image(args.prompt, args.history, args.output, model_id, args.quality)
