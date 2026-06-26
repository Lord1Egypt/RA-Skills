#!/usr/bin/env python3
"""Ollama OCR tool - recognize text from images"""

import base64
import urllib.request
import json
import sys

OLLAMA_HOST = "172.17.0.2"
OLLAMA_PORT = "11434"
DEFAULT_MODEL = "glm-ocr:latest"

def ollama_ocr(image_path, model=DEFAULT_MODEL):
    """Call Ollama API for image text recognition"""
    
    try:
        # Read and encode image
        with open(image_path, 'rb') as f:
            img_b64 = base64.b64encode(f.read()).decode()
        
        # Prepare request
        data = json.dumps({
            'model': model,
            'messages': [{
                'role': 'user',
                'content': 'Extract all text from this image',
                'images': [img_b64]
            }]
        }).encode()
        
        url = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}/api/chat"
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        # Get response
        resp = urllib.request.urlopen(req, timeout=120)
        
        # Parse streaming response
        result = ''
        for line in resp.read().decode().strip().split('\n'):
            if line:
                try:
                    obj = json.loads(line)
                    if 'message' in obj and 'content' in obj['message']:
                        result += obj['message']['content']
                except:
                    pass
        
        return result
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ollama_ocr.py <image_path> [model]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_MODEL
    
    result = ollama_ocr(image_path, model)
    print(result)
