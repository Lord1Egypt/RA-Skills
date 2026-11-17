#!/usr/bin/env python3
"""
CAVEMAN SCRIPT: Open Brave Browser to DeepSeek
"""

import subprocess
import sys
import time
import platform

def open_brave_to_deepseek():
    """Open Brave browser with DeepSeek website"""
    
    url = "https://chat.deepseek.com"
    
    # FIGURE OUT WHAT COMPUTER YOU HAVE
    computer_type = platform.system()
    
    try:
        if computer_type == "Windows":
            # WINDOWS CAVEMAN WAY
            subprocess.Popen(["start", "brave", url], shell=True)
            
        elif computer_type == "Darwin":
            # MAC CAVEMAN WAY
            subprocess.Popen(["open", "-a", "Brave Browser", url])
            
        else:
            # LINUX CAVEMAN WAY
            subprocess.Popen(["brave-browser", url])
            
        print("✅ DeepSeek opening in Brave...")
        print("💬 Browser is ready! Type your prompt.")
        
    except FileNotFoundError:
        print("❌ OOPS! Brave not found!")
        print("📌 Make sure Brave is installed")
        print("🌐 Or try: https://chat.deepseek.com in any browser")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    open_brave_to_deepseek()