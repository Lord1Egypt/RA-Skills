#!/usr/bin/env python3
import requests
import time
import os
import sys

def capture_image(output_path=None):
    url = "http://192.168.31.241/capture"
    try:
        print(f"Connecting to ESP32-CAM at {url}...")
        res = requests.get(url, timeout=10)
        
        if res.status_code == 200 and res.content:
            if not output_path:
                ts = time.strftime("%Y%m%d_%H%M%S")
                out_dir = os.path.dirname(os.path.abspath(__file__))
                output_path = os.path.join(out_dir, f"capture_{ts}.jpg")
            else:
                output_path = os.path.abspath(output_path)
                
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, "wb") as f:
                f.write(res.content)
            print(f"Success! Saved to: {output_path}")
        else:
            print(f"Capture failed with status: {res.status_code}")
    except Exception as e:
        print(f"Capture failed: {e}")

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else None
    capture_image(out_path)
