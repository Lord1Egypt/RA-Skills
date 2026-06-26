import os
import sys
import subprocess
import json
from pathlib import Path

def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result.stdout

def setup():
    print("=== OpenClaw Turbo-Bundle (Groq, OpenRouter & TTS) Setup ===")
    
    # 1. Install dependencies
    run_cmd("pip install -r requirements.txt")
    run_cmd("pip install free-ride")
    
    # 2. Free-Ride Auto Config
    print("\nConfiguring Free-AI Optimization (Free-Ride)...")
    print("Ensure your OPENROUTER_API_KEY is set in your environment.")
    # run_cmd("freeride auto") # Recommended to run manually for confirmation
    
    print("\nSetup complete!")
    print("1. Copy the 'skills/groq-arabic-tts' folder to your workspace/skills/.")
    print("2. Copy 'config/MODELS_JSON_EXAMPLE.txt' info into your models.json.")
    print("3. Rename 'ENV_EXAMPLE.txt' to '.env' and add your API key.")
    print("\nStay fast and free with your new vocal AI assistant!")

if __name__ == "__main__":
    setup()
