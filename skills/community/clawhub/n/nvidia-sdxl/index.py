import os
import sys
import json
import base64
import requests
from datetime import datetime

# 1. Configuration - Use your nvapi- key
API_KEY = "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"
#INVOKE_URL = "https://ai.api.nvidia.com"
INVOKE_URL = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-xl-base"
# Directory where OpenClaw stores session files
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")

def generate_image(prompt, negative_prompt="", width=1024, height=1024):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json",
    }

    payload = {
        "text_prompts": [{"text": prompt, "weight": 1}],
        "cfg_scale": 7,
        "steps": 30,
        "seed": 0,
        "width": width,
        "height": height
    }
    
    if negative_prompt:
        payload["text_prompts"].append({"text": negative_prompt, "weight": -1})

    try:
        response = requests.post(INVOKE_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        # Save the image to the workspace
        artifacts = data.get("artifacts", [])
        if not artifacts:
            return "Error: No image artifacts returned from API."

        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sdxl_{timestamp}.png"
        filepath = os.path.join(WORKSPACE, filename)

        image_base64 = artifacts[0].get("base64")
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(image_base64))

        # OpenClaw expects a string or JSON response describing the result
        return f"SUCCESS: Image generated and saved to {filepath}"

    except Exception as e:
        return f"ERROR: {str(e)}"

if __name__ == "__main__":
    # OpenClaw passes arguments as a JSON string in the first system argument
    try:
        if len(sys.argv) > 1:
            args = json.loads(sys.argv[1])
            result = generate_image(
                prompt=args.get("prompt"),
                negative_prompt=args.get("negative_prompt", ""),
                width=args.get("width", 1024),
                height=args.get("height", 1024)
            )
            print(result)
        else:
            print("ERROR: No arguments provided.")
    except Exception as e:
        print(f"ERROR parsing arguments: {str(e)}")

